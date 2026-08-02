#!/usr/bin/env python3
"""Replay and capture the fresh reviewer's independent CPU/Torch implementation."""

from __future__ import annotations

import contextlib
import io
import json
import sys
from pathlib import Path

import torch

import independent_torch_curvature as model


HERE = Path(__file__).resolve().parent

primary_stream = io.StringIO()
with contextlib.redirect_stdout(primary_stream):
    cases = [
        ((1/5,1/7,1/11),0,1.0,"primary"),
        ((1/3,-1/5,1/7),0,1.0,"primary"),
        ((1/5,1/7,1/11),0,1.0,"constant"),
        ((1/5,1/7,1/11),0,0.0,"primary"),
        ((0.0,0.0,0.0),0,4.0,"primary"),
    ]
    print(json.dumps([model.run(*case) for case in cases], indent=2))
(HERE / "independent_torch_curvature.stdout.json").write_text(primary_stream.getvalue(), encoding="utf-8")

point = (1/5,1/7,1/11)
additional = [
    model.run(point,-1,1.0,"primary"),
    model.run(point,1,1.0,"primary"),
    model.run(point,0,1.0,"repeated"),
]
(HERE / "independent_torch_curvature.additional.stdout.json").write_text(
    json.dumps(additional, indent=2) + "\n",
    encoding="utf-8",
)
(HERE / "independent_torch_curvature.environment.txt").write_text(
    "\n".join((
        f"python_full={sys.version}",
        f"torch={torch.__version__}",
        f"cuda_build={torch.version.cuda}",
        "run_dtype=torch.float64",
        f"cuda_available={torch.cuda.is_available()}",
        "device=cpu",
    )) + "\n",
    encoding="utf-8",
)
print("PASS independent captures written")
