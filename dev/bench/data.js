window.BENCHMARK_DATA = {
  "lastUpdate": 1683479476052,
  "repoUrl": "https://github.com/XuehaiPan/torchrl",
  "entries": {
    "CPU Benchmark Results": [
      {
        "commit": {
          "author": {
            "email": "vincentmoens@gmail.com",
            "name": "Vincent Moens",
            "username": "vmoens"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "6d030c9ec1db72c252a23dff04dcad2a553678d2",
          "message": "[Versioning] v0.1.1 (#1137)",
          "timestamp": "2023-05-06T22:32:41+01:00",
          "tree_id": "e67968d9103684ef3d59b0ff3b48bd4eecb0f1b7",
          "url": "https://github.com/XuehaiPan/torchrl/commit/6d030c9ec1db72c252a23dff04dcad2a553678d2"
        },
        "date": 1683479473632,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/test_collectors_benchmark.py::test_single",
            "value": 0.04358102871811584,
            "unit": "iter/sec",
            "range": "stddev: 0.44649944070713327",
            "extra": "mean: 22.945764003599994 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_collectors_benchmark.py::test_sync",
            "value": 0.08006261511382787,
            "unit": "iter/sec",
            "range": "stddev: 0.39139172885246853",
            "extra": "mean: 12.490224039999998 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_collectors_benchmark.py::test_async",
            "value": 0.08242248827699707,
            "unit": "iter/sec",
            "range": "stddev: 0.16596728996610152",
            "extra": "mean: 12.13261114659997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_envs_benchmark.py::test_simple",
            "value": 0.7647890049395498,
            "unit": "iter/sec",
            "range": "stddev: 0.042229846357415515",
            "extra": "mean: 1.3075501785999677 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_envs_benchmark.py::test_transformed",
            "value": 0.42959302343913014,
            "unit": "iter/sec",
            "range": "stddev: 0.03305633726265323",
            "extra": "mean: 2.327784543600001 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_envs_benchmark.py::test_serial",
            "value": 0.30427012821470306,
            "unit": "iter/sec",
            "range": "stddev: 0.04904148055617353",
            "extra": "mean: 3.2865533197999866 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_envs_benchmark.py::test_parallel",
            "value": 0.3381302472325207,
            "unit": "iter/sec",
            "range": "stddev: 0.024750854148049613",
            "extra": "mean: 2.957440241400036 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_objectives_benchmarks.py::test_values[generalized_advantage_estimate-True-True]",
            "value": 24.74843473475859,
            "unit": "iter/sec",
            "range": "stddev: 0.0007425752712616169",
            "extra": "mean: 40.40659583999968 msec\nrounds: 50"
          },
          {
            "name": "benchmarks/test_objectives_benchmarks.py::test_values[vec_generalized_advantage_estimate-True-True]",
            "value": 1.2360977171033771,
            "unit": "iter/sec",
            "range": "stddev: 0.02461694769356837",
            "extra": "mean: 808.9975300200058 msec\nrounds: 50"
          },
          {
            "name": "benchmarks/test_objectives_benchmarks.py::test_values[td0_return_estimate-False-False]",
            "value": 3323.8269667425616,
            "unit": "iter/sec",
            "range": "stddev: 0.00003933217995818046",
            "extra": "mean: 300.8580199889366 usec\nrounds: 50"
          },
          {
            "name": "benchmarks/test_objectives_benchmarks.py::test_values[td1_return_estimate-False-False]",
            "value": 69.14907120952765,
            "unit": "iter/sec",
            "range": "stddev: 0.00024687868997438954",
            "extra": "mean: 14.461510219998672 msec\nrounds: 50"
          },
          {
            "name": "benchmarks/test_objectives_benchmarks.py::test_values[vec_td1_return_estimate-False-False]",
            "value": 1.1271095332047332,
            "unit": "iter/sec",
            "range": "stddev: 0.027138607099017383",
            "extra": "mean: 887.2252168399996 msec\nrounds: 50"
          },
          {
            "name": "benchmarks/test_objectives_benchmarks.py::test_values[td_lambda_return_estimate-True-False]",
            "value": 28.20786118813317,
            "unit": "iter/sec",
            "range": "stddev: 0.0003085007241968883",
            "extra": "mean: 35.45111035999753 msec\nrounds: 50"
          },
          {
            "name": "benchmarks/test_objectives_benchmarks.py::test_values[vec_td_lambda_return_estimate-True-False]",
            "value": 1.1410343957273128,
            "unit": "iter/sec",
            "range": "stddev: 0.009929361202098178",
            "extra": "mean: 876.3977700800024 msec\nrounds: 50"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_sample_rb[TensorDictReplayBuffer-ListStorage-RandomSampler-4000]",
            "value": 0.14927954373262517,
            "unit": "iter/sec",
            "range": "stddev: 0.061457293957654924",
            "extra": "mean: 6.6988414822000095 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_sample_rb[TensorDictReplayBuffer-LazyMemmapStorage-RandomSampler-10000]",
            "value": 0.14637711234791495,
            "unit": "iter/sec",
            "range": "stddev: 0.10137831853629184",
            "extra": "mean: 6.831669131600028 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_sample_rb[TensorDictReplayBuffer-LazyTensorStorage-RandomSampler-10000]",
            "value": 0.14788104714469635,
            "unit": "iter/sec",
            "range": "stddev: 0.048000013509913335",
            "extra": "mean: 6.762191770399999 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_sample_rb[TensorDictReplayBuffer-ListStorage-SamplerWithoutReplacement-4000]",
            "value": 0.15129979546679423,
            "unit": "iter/sec",
            "range": "stddev: 0.03800284206261286",
            "extra": "mean: 6.609394261999978 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_sample_rb[TensorDictReplayBuffer-LazyMemmapStorage-SamplerWithoutReplacement-10000]",
            "value": 0.14636525675782555,
            "unit": "iter/sec",
            "range": "stddev: 0.12315769308519994",
            "extra": "mean: 6.8322224970000205 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_sample_rb[TensorDictReplayBuffer-LazyTensorStorage-SamplerWithoutReplacement-10000]",
            "value": 0.14642862945060275,
            "unit": "iter/sec",
            "range": "stddev: 0.14685365916682733",
            "extra": "mean: 6.829265586599968 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_sample_rb[TensorDictPrioritizedReplayBuffer-ListStorage-None-4000]",
            "value": 0.15065162716213276,
            "unit": "iter/sec",
            "range": "stddev: 0.031752235353852014",
            "extra": "mean: 6.6378307279999715 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_sample_rb[TensorDictPrioritizedReplayBuffer-LazyMemmapStorage-None-10000]",
            "value": 0.14728982489814327,
            "unit": "iter/sec",
            "range": "stddev: 0.12957026770050858",
            "extra": "mean: 6.789335248999987 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_sample_rb[TensorDictPrioritizedReplayBuffer-LazyTensorStorage-None-10000]",
            "value": 0.1477719964402046,
            "unit": "iter/sec",
            "range": "stddev: 0.034520447031042505",
            "extra": "mean: 6.767182037800012 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_iterate_rb[TensorDictReplayBuffer-ListStorage-RandomSampler-4000]",
            "value": 26.24877331604292,
            "unit": "iter/sec",
            "range": "stddev: 0.0006292912100699178",
            "extra": "mean: 38.09701840004891 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_iterate_rb[TensorDictReplayBuffer-LazyMemmapStorage-RandomSampler-10000]",
            "value": 25.831122434668607,
            "unit": "iter/sec",
            "range": "stddev: 0.0005014881558686355",
            "extra": "mean: 38.71299059997 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_iterate_rb[TensorDictReplayBuffer-LazyTensorStorage-RandomSampler-10000]",
            "value": 25.837776866798915,
            "unit": "iter/sec",
            "range": "stddev: 0.000442476417680524",
            "extra": "mean: 38.70302020004601 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_iterate_rb[TensorDictReplayBuffer-ListStorage-SamplerWithoutReplacement-4000]",
            "value": 16.14274598943527,
            "unit": "iter/sec",
            "range": "stddev: 0.05362578451457416",
            "extra": "mean: 61.947329200029344 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_iterate_rb[TensorDictReplayBuffer-LazyMemmapStorage-SamplerWithoutReplacement-10000]",
            "value": 25.933726579585304,
            "unit": "iter/sec",
            "range": "stddev: 0.00037062504142313323",
            "extra": "mean: 38.55982659997608 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_iterate_rb[TensorDictReplayBuffer-LazyTensorStorage-SamplerWithoutReplacement-10000]",
            "value": 26.087788245831057,
            "unit": "iter/sec",
            "range": "stddev: 0.0003421520429472778",
            "extra": "mean: 38.332111199952124 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_iterate_rb[TensorDictPrioritizedReplayBuffer-ListStorage-None-4000]",
            "value": 26.275913562139436,
            "unit": "iter/sec",
            "range": "stddev: 0.0003238322712326785",
            "extra": "mean: 38.057668200008266 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_iterate_rb[TensorDictPrioritizedReplayBuffer-LazyMemmapStorage-None-10000]",
            "value": 25.896203108026004,
            "unit": "iter/sec",
            "range": "stddev: 0.0005828393753799419",
            "extra": "mean: 38.61569959999542 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_iterate_rb[TensorDictPrioritizedReplayBuffer-LazyTensorStorage-None-10000]",
            "value": 25.964907233423922,
            "unit": "iter/sec",
            "range": "stddev: 0.0005593221615612024",
            "extra": "mean: 38.51352100009535 msec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_populate_rb[TensorDictReplayBuffer-ListStorage-RandomSampler-400]",
            "value": 0.03483527543175834,
            "unit": "iter/sec",
            "range": "stddev: 0.04415599016095039",
            "extra": "mean: 28.706533466600014 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_populate_rb[TensorDictReplayBuffer-LazyMemmapStorage-RandomSampler-400]",
            "value": 0.03532063071333002,
            "unit": "iter/sec",
            "range": "stddev: 0.2134414686609837",
            "extra": "mean: 28.312065209599997 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_populate_rb[TensorDictReplayBuffer-LazyTensorStorage-RandomSampler-400]",
            "value": 0.035545910307204664,
            "unit": "iter/sec",
            "range": "stddev: 0.032765883990591584",
            "extra": "mean: 28.132631612399972 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_populate_rb[TensorDictReplayBuffer-ListStorage-SamplerWithoutReplacement-400]",
            "value": 0.035509061061639084,
            "unit": "iter/sec",
            "range": "stddev: 0.04172758659009662",
            "extra": "mean: 28.161826027000007 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_populate_rb[TensorDictReplayBuffer-LazyMemmapStorage-SamplerWithoutReplacement-400]",
            "value": 0.035501710626942774,
            "unit": "iter/sec",
            "range": "stddev: 0.09513939101106085",
            "extra": "mean: 28.167656778799984 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_populate_rb[TensorDictReplayBuffer-LazyTensorStorage-SamplerWithoutReplacement-400]",
            "value": 0.035543869859702905,
            "unit": "iter/sec",
            "range": "stddev: 0.08536918884471002",
            "extra": "mean: 28.134246607000115 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_populate_rb[TensorDictPrioritizedReplayBuffer-ListStorage-None-400]",
            "value": 0.03552630362990433,
            "unit": "iter/sec",
            "range": "stddev: 0.08145551802664461",
            "extra": "mean: 28.148157782400084 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_populate_rb[TensorDictPrioritizedReplayBuffer-LazyMemmapStorage-None-400]",
            "value": 0.03544355877526542,
            "unit": "iter/sec",
            "range": "stddev: 0.09455412709634446",
            "extra": "mean: 28.213871139200002 sec\nrounds: 5"
          },
          {
            "name": "benchmarks/test_replaybuffer_benchmark.py::test_populate_rb[TensorDictPrioritizedReplayBuffer-LazyTensorStorage-None-400]",
            "value": 0.03551542783451058,
            "unit": "iter/sec",
            "range": "stddev: 0.08088194858525448",
            "extra": "mean: 28.15677751819994 sec\nrounds: 5"
          }
        ]
      }
    ]
  }
}