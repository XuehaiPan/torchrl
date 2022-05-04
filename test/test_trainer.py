# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from argparse import Namespace

from tensorboard.backend.event_processing import event_accumulator
from torch.utils.tensorboard import SummaryWriter
from torchrl.envs.libs.dm_control import _has_dmc

import tempfile
from torchrl.trainers import Recorder
from torchrl.trainers.helpers import transformed_env_constructor
from os import walk, path

import argparse
from collections import OrderedDict

import pytest
import torch
from torchrl.data import (
    TensorDict,
    TensorDictPrioritizedReplayBuffer,
    TensorDictReplayBuffer,
)
from torchrl.trainers import Trainer
from torchrl.trainers.trainers import (
    SelectKeys,
    ReplayBufferTrainer,
    LogReward,
    RewardNormalizer,
    mask_batch,
    BatchSubSampler,
    UpdateWeights,
    CountFramesLog,
)


class MockingOptim:
    param_groups = [{"params": []}]


class MockingCollector:
    called_update_policy_weights_ = False

    def set_seed(self, seed):
        return seed

    def update_policy_weights_(self):
        self.called_update_policy_weights_ = True


def mocking_agent() -> Trainer:
    agent = Trainer(
        MockingCollector(),
        *[
            None,
        ]
        * 3,
        MockingOptim()
    )
    agent.collected_frames = 0
    agent._pbar_str = OrderedDict()
    return agent


def test_selectkeys():
    agent = mocking_agent()
    key1 = "first key"
    key2 = "second key"
    td = TensorDict(
        {
            key1: torch.randn(3),
            key2: torch.randn(3),
        },
        [],
    )
    agent.register_op("batch_process", SelectKeys([key1]))
    td_out = agent._process_batch_hook(td)
    assert key1 in td_out.keys()
    assert key2 not in td_out.keys()


@pytest.mark.parametrize("prioritized", [True, False])
def test_rb_agent(prioritized):
    agent = mocking_agent()
    S = 100
    if prioritized:
        replay_buffer = TensorDictPrioritizedReplayBuffer(S, 1.1, 0.9)
    else:
        replay_buffer = TensorDictReplayBuffer(S)

    N = 9
    rb_agent = ReplayBufferTrainer(replay_buffer=replay_buffer, batch_size=N)

    agent.register_op("batch_process", rb_agent.extend)
    agent.register_op("process_optim_batch", rb_agent.sample)
    agent.register_op("post_loss", rb_agent.update_priority)

    key1 = "first key"
    key2 = "second key"
    batch = 101
    td = TensorDict(
        {
            key1: torch.randn(batch, 3),
            key2: torch.randn(batch, 3),
        },
        [batch],
    )
    td_out = agent._process_batch_hook(td)
    assert td_out is td

    td_out = agent._process_optim_batch_hook(td)
    assert td_out is not td
    assert td_out.shape[0] == N

    if prioritized:
        td_out.set(replay_buffer.priority_key, torch.rand(N))

    td_out = agent._post_loss_hook(td_out)
    if prioritized:
        for idx in range(min(S, batch)):
            if idx in td_out.get("index"):
                assert replay_buffer._sum_tree[idx] != 1.0
            else:
                assert replay_buffer._sum_tree[idx] == 1.0
    else:
        assert "index" not in td_out.keys()


@pytest.mark.parametrize("logname", ["a", "b"])
def test_log_reward(logname):
    agent = mocking_agent()
    agent.collected_frames = 0
    agent._pbar_str = OrderedDict()

    log_reward = LogReward(logname)
    agent.register_op("pre_steps_log", log_reward)
    td = TensorDict({"reward": torch.ones(3)}, [3])
    agent._pre_steps_log_hook(td)
    assert agent._pbar_str[logname] == 1


def test_reward_norm():
    torch.manual_seed(0)
    agent = mocking_agent()

    reward_normalizer = RewardNormalizer()
    agent.register_op("batch_process", reward_normalizer.update_reward_stats)
    agent.register_op("process_optim_batch", reward_normalizer.normalize_reward)

    batch = 10
    reward = torch.randn(batch, 1)
    td = TensorDict({"reward": reward.clone()}, [batch])
    td_out = agent._process_batch_hook(td)
    assert (td_out.get("reward") == reward).all()
    assert not reward_normalizer._normalize_has_been_called

    td_norm = agent._process_optim_batch_hook(td)
    assert reward_normalizer._normalize_has_been_called
    torch.testing.assert_close(td_norm.get("reward").mean(), torch.zeros([]))
    torch.testing.assert_close(td_norm.get("reward").std(), torch.ones([]))


def test_masking():
    torch.manual_seed(0)
    agent = mocking_agent()

    agent.register_op("batch_process", mask_batch)
    batch = 10
    td = TensorDict(
        {
            "mask": torch.zeros(batch, dtype=torch.bool).bernoulli_(),
            "tensor": torch.randn(batch, 51),
        },
        [batch],
    )
    td_out = agent._process_batch_hook(td)
    assert td_out.shape[0] == td.get("mask").sum()
    assert (td["tensor"][td["mask"].squeeze(-1)] == td_out["tensor"]).all()


def test_subsampler():
    torch.manual_seed(0)
    agent = mocking_agent()

    batch_size = 10
    sub_traj_len = 5

    key1 = "key1"
    key2 = "key2"

    agent.register_op(
        "process_optim_batch",
        BatchSubSampler(batch_size=batch_size, sub_traj_len=sub_traj_len),
    )

    td = TensorDict(
        {
            key1: torch.stack([torch.arange(0, 10), torch.arange(10, 20)], 0),
            key2: torch.stack([torch.arange(0, 10), torch.arange(10, 20)], 0),
        },
        [2, 10],
    )

    td_out = agent._process_optim_batch_hook(td)
    assert td_out.shape == torch.Size([batch_size // sub_traj_len, sub_traj_len])
    assert (td_out.get(key1) == td_out.get(key2)).all()


@pytest.mark.skipif(not _has_dmc, reason="No dm_control library")
def test_recorder():
    with tempfile.TemporaryDirectory() as folder:
        writer = SummaryWriter(log_dir=folder)
        args = Namespace()
        args.env_name = "humanoid"
        args.env_task = "walk"
        args.env_library = "dm_control"
        args.frame_skip = 1
        args.from_pixels = False
        args.vecnorm = False
        args.norm_rewards = False
        args.reward_scaling = False
        args.noops = 0
        args.record_frames = 24 // args.frame_skip
        args.record_interval = 2

        N = 8

        recorder = transformed_env_constructor(
            args,
            video_tag="tmp",
            norm_obs_only=True,
            stats={'loc': 0, 'scale': 1},
            writer=writer,
        )()

        recorder = Recorder(
            record_frames=args.record_frames,
            frame_skip=args.frame_skip,
            policy_exploration=None,
            recorder=recorder,
            record_interval=args.record_interval,
        )

        for _ in range(N):
            recorder(None)

        for (dirpath, dirnames, filenames) in walk(folder):
            break

        filename = filenames[0]
        ea = event_accumulator.EventAccumulator(
            path.join(folder, filename),
            size_guidance={event_accumulator.IMAGES: 0, })
        ea.Reload()
        print(ea.Tags())
        img = ea.Images('tmp_humanoid_video')
        assert len(img) == N // args.record_interval

def test_updateweights():
    torch.manual_seed(0)
    agent = mocking_agent()

    T = 5
    update_weights = UpdateWeights(agent.collector, T)
    agent.register_op("post_steps", update_weights)
    for t in range(T):
        agent._post_steps_hook()
        assert agent.collector.called_update_policy_weights_ is (t == T - 1)
    assert agent.collector.called_update_policy_weights_


def test_countframes():
    torch.manual_seed(0)
    agent = mocking_agent()

    frame_skip = 3
    batch = 10
    count_frames = CountFramesLog(frame_skip=frame_skip)
    agent.register_op("pre_steps_log", count_frames)
    td = TensorDict(
        {"mask": torch.zeros(batch, dtype=torch.bool).bernoulli_()}, [batch]
    )
    agent._pre_steps_log_hook(td)
    assert count_frames.frame_count == td.get("mask").sum() * frame_skip


if __name__ == "__main__":
    args, unknown = argparse.ArgumentParser().parse_known_args()
    pytest.main([__file__, "--capture", "no", "--exitfirst"] + unknown)
