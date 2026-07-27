#!/usr/bin/env python3
from __future__ import annotations

import csv
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

import torch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
INDEPENDENT_SOURCE = (
    ROOT / "udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27"
    / "verify_intrinsic_pair_independent.py"
)
F = Fraction
HOLDOUTS = [F(-5, 2), F(-1, 2), F(3, 4), F(3, 2), F(7, 2)]
TOLERANCE_SCALE = 2e-9


def load_independent_geometry():
    spec = importlib.util.spec_from_file_location("lambda_atlas_independent_torch_geometry", INDEPENDENT_SOURCE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def polynomial() -> list[F]:
    with (HERE / "POLYNOMIAL_COEFFICIENTS.tsv").open(newline="", encoding="utf-8") as handle:
        return [F(row["coefficient"]) for row in csv.DictReader(handle, delimiter="\t")]


def evaluate(coefficients: list[F], value: F) -> F:
    result = F(0)
    for coefficient in reversed(coefficients):
        result = result * value + coefficient
    return result


def main() -> int:
    geometry = load_independent_geometry()
    coefficients = polynomial()
    origin = torch.zeros(3, dtype=torch.float64)
    outcomes = []
    maximum_error = 0.0
    maximum_scaled_error = 0.0
    for value in HOLDOUTS:
        gradients = geometry.jacfwd(
            lambda point: geometry.curvature_invariants(
                point, float(value), float(F(1, 50)), float(F(1, 64))
            )
        )(origin)
        observed = float(torch.linalg.det(gradients).item())
        exact_fraction = evaluate(coefficients, value)
        expected = float(exact_fraction)
        error = abs(observed - expected)
        scale = max(1.0, abs(expected))
        scaled_error = error / scale
        maximum_error = max(maximum_error, error)
        maximum_scaled_error = max(maximum_scaled_error, scaled_error)
        assert error <= TOLERANCE_SCALE * scale
        outcomes.append({
            "lambda": str(value),
            "exact_determinant": str(exact_fraction),
            "torch_determinant": format(observed, ".17g"),
            "absolute_error": format(error, ".17g"),
            "scaled_error": format(scaled_error, ".17g"),
            "tolerance": "2e-9*max(1,abs(D_exact))",
            "result": "PASS",
        })
    with (HERE / "TORCH_HOLDOUT_OUTCOMES.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(outcomes[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(outcomes)
    result = {
        "method": "INHERITED_INDEPENDENT_TORCH_AUTODIFF_FULL_RIEMANN_NO_EXACT_ENGINE_IMPORT",
        "torch_version": torch.__version__,
        "holdouts": len(outcomes),
        "passed": sum(row["result"] == "PASS" for row in outcomes),
        "maximum_absolute_error": maximum_error,
        "maximum_scaled_error": maximum_scaled_error,
        "tolerance_scale": TOLERANCE_SCALE,
        "exact_polynomial_controls": True,
    }
    (HERE / "TORCH_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("PASS independent_Torch_holdouts 5/5")
    print(f"MAX_ABSOLUTE_ERROR {maximum_error:.17g}")
    print(f"MAX_SCALED_ERROR {maximum_scaled_error:.17g}")
    print(f"TORCH_VERSION {torch.__version__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
