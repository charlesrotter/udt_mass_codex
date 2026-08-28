#!/usr/bin/env python3
"""Verify the frozen G286 result artifacts and preregistered gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REQUIRED = [
    "MAP.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "COMMANDS.md",
    "EXACT_DERIVATION.md", "PROPAGATION_PRINCIPLE_MAP.md", "AUDIT_REPORT.md",
    "LAY_REPORT.md", "STATUS_LEDGER.tsv", "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json", "VERIFICATION_RESULT.json",
    "derive_propagation_discriminator.py",
    "verify_independent.py",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        raise SystemExit(f"missing required files: {missing}")
    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    checks = {
        "production_pass": production.get("pass") is True,
        "independent_pass": independent.get("pass") is True,
        "prior_zero": production.get("prior_samples_exactly_zero") is True,
        "future_curvature": production.get("future_curvature_nonzero") is True,
        "trace_free": production.get("future_tidal_trace") == 0.0,
        "determinant": production.get("metric_determinant") == -1.0,
        "production_symplectic": production.get("production_symplectic_defect", 1.0) < 2e-11,
        "independent_symplectic": independent.get("independent_symplectic_defect", 1.0) < 2e-8,
        "cross_method": independent.get("production_independent_transfer_difference", 1.0) < 2e-6,
        "future_separator": production.get("future_transfer_difference_from_flat", 0.0) > 1e-5,
    }
    result = {"checks": checks, "pass": all(checks.values())}
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
