# P01 command and environment log

Production environment: Python 3.10.12, PyTorch 2.5.1+cu121, SciPy 1.15.3,
Tesla V100-PCIE-32GB, float64, one GPU process.

Primary production:

```bash
python3 udt_complete_coframe_metric_telescope_p01_2026-07-27/metric_telescope_gpu.py \
  --production \
  --output-dir udt_complete_coframe_metric_telescope_p01_2026-07-27
```

Wall time 18.6225 s; peak allocation 20,687,226,368 bytes.  The incorrect
memory estimate triggered the separately recorded resource replay.

Independent CPU anchor:

```bash
python3 udt_complete_coframe_metric_telescope_p01_2026-07-27/verify_metric_telescope_cpu.py \
  udt_complete_coframe_metric_telescope_p01_2026-07-27/CPU_ANCHOR_GPU.json \
  --output udt_complete_coframe_metric_telescope_p01_2026-07-27/CPU_ANCHOR_VERIFICATION.json
```

Batch-16 resource replay:

```bash
python3 udt_complete_coframe_metric_telescope_p01_2026-07-27/metric_telescope_gpu.py \
  --device cuda:0 \
  --output-dir udt_complete_coframe_metric_telescope_p01_2026-07-27/resource_replay_batch16 \
  --configs-per-shell 1024 \
  --shells 0.03 0.1 0.3 1.0 2.5 \
  --grid-t 17 --grid-x 33 --rk4 64 --batch 16 --seed 20260727
```

Wall time 49.3678 s; peak allocation 5,183,212,032 bytes.

Scoped replay verification:

```bash
python3 udt_complete_coframe_metric_telescope_p01_2026-07-27/verify_resource_replay_scoped.py \
  udt_complete_coframe_metric_telescope_p01_2026-07-27 \
  udt_complete_coframe_metric_telescope_p01_2026-07-27/resource_replay_batch16 \
  --output udt_complete_coframe_metric_telescope_p01_2026-07-27/RESOURCE_REPLAY_SCOPED_VERIFICATION.json
```

Descriptive census:

```bash
python3 udt_complete_coframe_metric_telescope_p01_2026-07-27/analyze_metric_telescope.py \
  udt_complete_coframe_metric_telescope_p01_2026-07-27 \
  --output udt_complete_coframe_metric_telescope_p01_2026-07-27/STRUCTURE_CENSUS.json
```
