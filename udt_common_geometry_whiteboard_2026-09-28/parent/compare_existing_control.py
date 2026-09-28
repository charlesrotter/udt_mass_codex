#!/usr/bin/env python3
"""Pointwise, unretuned constant-H control under OFS1's supplied BAO interface."""
import datetime
import hashlib
import json
import math
from pathlib import Path
import platform

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "udt_observation_guided_function_search_2026-09-28/observations/comparison_checked/RESULT.json"
OUT = Path(__file__).parent / "CONSTANT_H_INTERFACE_CHECK.json"
FREEZE = Path(__file__).parent / "COMPARISON_FREEZE.md"

data = json.loads(SOURCE.read_text())
indices = [i for i, include in enumerate(data["within_sne_domain"]) if include]
if len(indices) != 5 or len(data["z"]) != len(data["ratios"]):
    raise ValueError("OFS1 source shape/domain differs from frozen comparison")
rows = []
for i in indices:
    z = data["z"][i]
    observed = data["ratios"][i]
    variance = data["ratio_covariance"][i][i]
    if not all(math.isfinite(v) for v in (z, observed, variance)) or variance <= 0:
        raise ValueError("Nonfinite datum or nonpositive supplied diagonal variance")
    # FREE: constant H>0 cancels in this supplied flat homogeneous control.
    # IMPORTED: conventional comoving-ruler/optical comparison interface.
    # Exact derivation: exp(x) F/F' = exp(x)-1 = z for F=exp(x)-1.
    predicted = z
    rows.append(dict(z=z, observed_ratio=observed, inherited_linear_sigma=math.sqrt(variance),
                     constant_H_prediction=predicted, prediction_minus_observed=predicted-observed))
result = dict(
    utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    python=platform.python_version(), arithmetic="Python binary64; exact prediction AP=z",
    source=str(SOURCE.relative_to(ROOT)), source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    freeze_sha256=hashlib.sha256(FREEZE.read_bytes()).hexdigest(),
    status="Exposed conditional pointwise comparison only; no fit, statistic, threshold or native-law exclusion",
    rows=rows,
    omissions="No likelihood, new uncertainty propagation, physical positional-component isolation, or general conformal-class test",
)
with OUT.open("x") as stream:
    json.dump(result, stream, indent=2)
    stream.write("\n")
print(json.dumps(result, indent=2))
