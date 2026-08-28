#!/usr/bin/env python3
"""Verify the frozen G286 result artifacts and preregistered gates."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REQUIRED = [
    "MAP.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "COMMANDS.md",
    "EXACT_DERIVATION.md", "PROPAGATION_PRINCIPLE_MAP.md", "AUDIT_REPORT.md",
    "LAY_REPORT.md", "STATUS_LEDGER.tsv", "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json", "VERIFICATION_RESULT.json", "REPAIR_RESULT.json",
    "EXTERNAL_REVIEW_GPT54.md", "REPAIR_PREREGISTRATION.md",
    "derive_propagation_discriminator.py",
    "verify_independent.py", "run_repair_catch.py",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        raise SystemExit(f"missing required files: {missing}")
    frozen_production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    frozen_independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="udt_g286_verify_") as temporary:
        temporary_root = Path(temporary)
        production_path = temporary_root / "DERIVATION_RESULT.replay.json"
        independent_path = temporary_root / "INDEPENDENT_VERIFICATION.replay.json"
        production_run = subprocess.run(
            [sys.executable, "-S", str(ROOT / "derive_propagation_discriminator.py"),
             "--output", str(production_path)],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        independent_run = subprocess.run(
            [sys.executable, "-S", str(ROOT / "verify_independent.py"),
             "--production", str(production_path), "--output", str(independent_path)],
            cwd=ROOT, capture_output=True, text=True, check=False,
        ) if production_run.returncode == 0 else None
        production = json.loads(production_path.read_text(encoding="utf-8")) \
            if production_path.is_file() else {}
        independent = json.loads(independent_path.read_text(encoding="utf-8")) \
            if independent_path.is_file() else {}

    production_reproduced = production == frozen_production
    independent_reproduced = independent == frozen_independent
    checks = {
        "production_replay_exit": production_run.returncode == 0,
        "independent_replay_exit": independent_run is not None and independent_run.returncode == 0,
        "production_pass": production.get("pass") is True,
        "independent_pass": independent.get("pass") is True,
        "sampled_prior_zero": production.get("sampled_prior_points_zero") is True,
        "sampled_future_tidal": production.get("sampled_future_tidal_nonzero") is True,
        "analytic_boundary_labelled": len(production.get("analytic_claims_not_mechanized", [])) == 3,
        "trace_free": production.get("future_tidal_trace") == 0.0,
        "determinant": production.get("metric_determinant") == -1.0,
        "production_symplectic": production.get("production_symplectic_defect", 1.0) < 2e-11,
        "independent_symplectic": independent.get("independent_symplectic_defect", 1.0) < 2e-8,
        "cross_method": independent.get("production_independent_transfer_difference", 1.0) < 2e-6,
        "future_separator": production.get("future_transfer_difference_from_flat", 0.0) > 1e-5,
        "production_frozen_reproduced": production_reproduced,
        "independent_frozen_reproduced": independent_reproduced,
    }
    result = {"checks": checks, "pass": all(checks.values())}
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
