# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import warnings
from typing import Optional, Tuple

import torch
from tensordict import TensorDict
from tensordict.nn import TensorDictModule

from torchrl.envs.model_based.dreamer import DreamerEnv
from torchrl.envs.utils import ExplorationType, set_exploration_type, step_mdp
from torchrl.objectives.common import LossModule
from torchrl.objectives.utils import (
    _GAMMA_LMBDA_DEPREC_WARNING,
    default_value_kwargs,
    distance_loss,
    hold_out_net,
    ValueEstimators,
)
from torchrl.objectives.value import TD0Estimator, TD1Estimator, TDLambdaEstimator


class DreamerModelLoss(LossModule):
    """Dreamer Model Loss.

    Computes the loss of the dreamer world model. The loss is composed of the
    kl divergence between the prior and posterior of the RSSM,
    the reconstruction loss over the reconstructed observation and the reward
    loss over the predicted reward.

    Reference: https://arxiv.org/abs/1912.01603.

    Args:
        world_model (TensorDictModule): the world model.
        lambda_kl (float, optional): the weight of the kl divergence loss. Default: 1.0.
        lambda_reco (float, optional): the weight of the reconstruction loss. Default: 1.0.
        lambda_reward (float, optional): the weight of the reward loss. Default: 1.0.
        reco_loss (str, optional): the reconstruction loss. Default: "l2".
        reward_loss (str, optional): the reward loss. Default: "l2".
        free_nats (int, optional): the free nats. Default: 3.
        delayed_clamp (bool, optional): if ``True``, the KL clamping occurs after
            averaging. If False (default), the kl divergence is clamped to the
            free nats value first and then averaged.
        global_average (bool, optional): if ``True``, the losses will be averaged
            over all dimensions. Otherwise, a sum will be performed over all
            non-batch/time dimensions and an average over batch and time.
            Default: False.
    """

    def __init__(
        self,
        world_model: TensorDictModule,
        *,
        lambda_kl: float = 1.0,
        lambda_reco: float = 1.0,
        lambda_reward: float = 1.0,
        reco_loss: Optional[str] = None,
        reward_loss: Optional[str] = None,
        free_nats: int = 3,
        delayed_clamp: bool = False,
        global_average: bool = False,
    ):
        super().__init__()
        self.world_model = world_model
        self.reco_loss = reco_loss if reco_loss is not None else "l2"
        self.reward_loss = reward_loss if reward_loss is not None else "l2"
        self.lambda_kl = lambda_kl
        self.lambda_reco = lambda_reco
        self.lambda_reward = lambda_reward
        self.free_nats = free_nats
        self.delayed_clamp = delayed_clamp
        self.global_average = global_average

    def forward(self, tensordict: TensorDict) -> torch.Tensor:
        tensordict = tensordict.clone(recurse=False)
        tensordict.rename_key_(("next", "reward"), ("next", "true_reward"))
        tensordict = self.world_model(tensordict)
        # compute model loss
        kl_loss = self.kl_loss(
            tensordict.get(("next", "prior_mean")),
            tensordict.get(("next", "prior_std")),
            tensordict.get(("next", "posterior_mean")),
            tensordict.get(("next", "posterior_std")),
        ).unsqueeze(-1)
        reco_loss = distance_loss(
            tensordict.get(("next", "pixels")),
            tensordict.get(("next", "reco_pixels")),
            self.reco_loss,
        )
        if not self.global_average:
            reco_loss = reco_loss.sum((-3, -2, -1))
        reco_loss = reco_loss.mean().unsqueeze(-1)

        reward_loss = distance_loss(
            tensordict.get(("next", "true_reward")),
            tensordict.get(("next", "reward")),
            self.reward_loss,
        )
        if not self.global_average:
            reward_loss = reward_loss.squeeze(-1)
        reward_loss = reward_loss.mean().unsqueeze(-1)
        # import ipdb; ipdb.set_trace()
        return (
            TensorDict(
                {
                    "loss_model_kl": self.lambda_kl * kl_loss,
                    "loss_model_reco": self.lambda_reco * reco_loss,
                    "loss_model_reward": self.lambda_reward * reward_loss,
                },
                [],
            ),
            tensordict.detach(),
        )

    def kl_loss(
        self,
        prior_mean: torch.Tensor,
        prior_std: torch.Tensor,
        posterior_mean: torch.Tensor,
        posterior_std: torch.Tensor,
    ) -> torch.Tensor:
        kl = (
            torch.log(prior_std / posterior_std)
            + (posterior_std**2 + (prior_mean - posterior_mean) ** 2)
            / (2 * prior_std**2)
            - 0.5
        )
        if not self.global_average:
            kl = kl.sum(-1)
        if self.delayed_clamp:
            kl = kl.mean().clamp_min(self.free_nats)
        else:
            kl = kl.clamp_min(self.free_nats).mean()
        return kl


class DreamerActorLoss(LossModule):
    """Dreamer Actor Loss.

    Computes the loss of the dreamer actor. The actor loss is computed as the
    negative average lambda return.

    Reference: https://arxiv.org/abs/1912.01603.

    Args:
        actor_model (TensorDictModule): the actor model.
        value_model (TensorDictModule): the value model.
        model_based_env (DreamerEnv): the model based environment.
        imagination_horizon (int, optional): The number of steps to unroll the
            model. Defaults to ``15``.
        discount_loss (bool, optional): if ``True``, the loss is discounted with a
            gamma discount factor. Default to ``False``.

    """

    default_value_estimator = ValueEstimators.TDLambda

    def __init__(
        self,
        actor_model: TensorDictModule,
        value_model: TensorDictModule,
        model_based_env: DreamerEnv,
        *,
        imagination_horizon: int = 15,
        discount_loss: bool = False,  # for consistency with paper
        gamma: int = None,
        lmbda: int = None,
    ):
        super().__init__()
        self.actor_model = actor_model
        self.value_model = value_model
        self.model_based_env = model_based_env
        self.imagination_horizon = imagination_horizon
        self.discount_loss = discount_loss
        if gamma is not None:
            warnings.warn(_GAMMA_LMBDA_DEPREC_WARNING, category=DeprecationWarning)
            self.gamma = gamma
        if lmbda is not None:
            warnings.warn(_GAMMA_LMBDA_DEPREC_WARNING, category=DeprecationWarning)
            self.lmbda = lmbda

    def forward(self, tensordict: TensorDict) -> Tuple[TensorDict, TensorDict]:
        with torch.no_grad():
            tensordict = tensordict.select("state", "belief")
            tensordict = tensordict.reshape(-1)

        with hold_out_net(self.model_based_env), set_exploration_type(
            ExplorationType.RANDOM
        ):
            tensordict = self.model_based_env.reset(tensordict.clone(recurse=False))
            fake_data = self.model_based_env.rollout(
                max_steps=self.imagination_horizon,
                policy=self.actor_model,
                auto_reset=False,
                tensordict=tensordict,
            )

            next_tensordict = step_mdp(
                fake_data,
                keep_other=True,
            )
            with hold_out_net(self.value_model):
                next_tensordict = self.value_model(next_tensordict)

        reward = fake_data.get(("next", "reward"))
        next_value = next_tensordict.get("state_value")
        lambda_target = self.lambda_target(reward, next_value)
        fake_data.set("lambda_target", lambda_target)

        if self.discount_loss:
            gamma = self.value_estimator.gamma.to(tensordict.device)
            discount = gamma.expand(lambda_target.shape)
            discount[..., 0, :] = 1
            discount = discount.cumprod(dim=-2)
            actor_loss = -(lambda_target * discount).sum((-2, -1)).mean()
        else:
            actor_loss = -lambda_target.sum((-2, -1)).mean()
        loss_tensordict = TensorDict({"loss_actor": actor_loss}, [])
        return loss_tensordict, fake_data.detach()

    def lambda_target(self, reward: torch.Tensor, value: torch.Tensor) -> torch.Tensor:
        done = torch.zeros(reward.shape, dtype=torch.bool, device=reward.device)
        input_tensordict = TensorDict(
            {
                ("next", "reward"): reward,
                ("next", "state_value"): value,
                ("next", "done"): done,
            },
            [],
        )
        return self.value_estimator.value_estimate(input_tensordict)

    def make_value_estimator(self, value_type: ValueEstimators = None, **hyperparams):
        if value_type is None:
            value_type = self.default_value_estimator
        self.value_type = value_type
        value_net = None
        value_key = "state_value"
        hp = dict(default_value_kwargs(value_type))
        if hasattr(self, "gamma"):
            hp["gamma"] = self.gamma
        hp.update(hyperparams)
        if value_type is ValueEstimators.TD1:
            self._value_estimator = TD1Estimator(
                **hp,
                value_network=value_net,
                value_target_key="value_target",
                value_key=value_key,
            )
        elif value_type is ValueEstimators.TD0:
            self._value_estimator = TD0Estimator(
                **hp,
                value_network=value_net,
                value_target_key="value_target",
                value_key=value_key,
            )
        elif value_type is ValueEstimators.GAE:
            if hasattr(self, "lmbda"):
                hp["lmbda"] = self.lmbda
            raise NotImplementedError(
                f"Value type {value_type} it not implemented for loss {type(self)}."
            )
        elif value_type is ValueEstimators.TDLambda:
            if hasattr(self, "lmbda"):
                hp["lmbda"] = self.lmbda
            self._value_estimator = TDLambdaEstimator(
                **hp,
                value_network=value_net,
                value_target_key="value_target",
                value_key=value_key,
            )
        else:
            raise NotImplementedError(f"Unknown value type {value_type}")


class DreamerValueLoss(LossModule):
    """Dreamer Value Loss.

    Computes the loss of the dreamer value model. The value loss is computed
    between the predicted value and the lambda target.

    Reference: https://arxiv.org/abs/1912.01603.

    Args:
        value_model (TensorDictModule): the value model.
        value_loss (str, optional): the loss to use for the value loss.
            Default: ``"l2"``.
        discount_loss (bool, optional): if ``True``, the loss is discounted with a
            gamma discount factor. Default: False.
        gamma (float, optional): the gamma discount factor. Default: ``0.99``.

    """

    def __init__(
        self,
        value_model: TensorDictModule,
        value_loss: Optional[str] = None,
        discount_loss: bool = False,  # for consistency with paper
        gamma: int = 0.99,
    ):
        super().__init__()
        self.value_model = value_model
        self.value_loss = value_loss if value_loss is not None else "l2"
        self.gamma = gamma
        self.discount_loss = discount_loss

    def forward(self, fake_data) -> torch.Tensor:
        lambda_target = fake_data.get("lambda_target")
        tensordict_select = fake_data.select(*self.value_model.in_keys)
        self.value_model(tensordict_select)
        if self.discount_loss:
            discount = self.gamma * torch.ones_like(
                lambda_target, device=lambda_target.device
            )
            discount[..., 0, :] = 1
            discount = discount.cumprod(dim=-2)
            value_loss = (
                (
                    discount
                    * distance_loss(
                        tensordict_select.get("state_value"),
                        lambda_target,
                        self.value_loss,
                    )
                )
                .sum((-1, -2))
                .mean()
            )
        else:
            value_loss = (
                distance_loss(
                    tensordict_select.get("state_value"),
                    lambda_target,
                    self.value_loss,
                )
                .sum((-1, -2))
                .mean()
            )

        loss_tensordict = TensorDict({"loss_value": value_loss}, [])
        return loss_tensordict, fake_data
