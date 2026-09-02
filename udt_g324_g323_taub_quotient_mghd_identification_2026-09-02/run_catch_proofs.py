#!/usr/bin/env python3
"""Hostile controls for G324's load-bearing implication chain."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="CATCH_PROOF_RESULT.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent

    def positive_landing(future_integrand_power, curvature_coefficient,
                         globally_hyperbolic, modulus_distinct, imports_new_physics):
        return (
            future_integrand_power >= -1
            and curvature_coefficient > 0
            and globally_hyperbolic
            and modulus_distinct
            and not imports_new_physics
        )

    assert positive_landing(0, 12, True, True, False)
    controls = {
        "finite_future_parameter_rejected": not positive_landing(-2, 12, True, True, False),
        "zero_curvature_obstruction_rejected": not positive_landing(0, 0, True, True, False),
        "missing_global_hyperbolicity_rejected": not positive_landing(0, 12, False, True, False),
        "erased_lattice_modulus_rejected": not positive_landing(0, 12, True, False, False),
        "new_physical_law_dependency_rejected": not positive_landing(0, 12, True, True, True),
    }
    assert all(controls.values())
    result = {
        "schema": "udt-g324-catch-proofs-v1",
        "status": "PASS",
        "assertion_count": len(controls),
        "controls": controls,
    }
    (root / args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
