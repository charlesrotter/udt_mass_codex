#!/usr/bin/env python3
"""Mutation catches for the G236 package-level evidence validator."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
OUT = PACKAGE / "CATCH_PROOF_RESULT.json"
spec = importlib.util.spec_from_file_location("g236_verify", PACKAGE / "verify_package.py")
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def caught(production: dict, independent: dict, key: str) -> bool:
    return module.validate_payload(production, independent).get(key) is False


def main() -> None:
    production = json.loads((PACKAGE / "PRODUCTION_RESULT.json").read_text())
    independent = json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = {}

    p = copy.deepcopy(production)
    p["landing"] = "UNREGISTERED_POSITIVE"
    catches["wrong_landing"] = caught(p, independent, "production_landing")

    p = copy.deepcopy(production)
    p["samples"]["pantheon_non_des_common_support"] += 1
    catches["wrong_sample_count"] = caught(p, independent, "pantheon_count")

    p = copy.deepcopy(production)
    p["samples"]["exact_cid_overlap"] = 0
    catches["missing_overlap"] = caught(p, independent, "exact_overlap_count")

    p = copy.deepcopy(production)
    p["hostile_controls"]["slope_mutation_pass"] = False
    catches["disabled_slope_hostile"] = caught(p, independent, "slope_hostile")

    p = copy.deepcopy(production)
    p["checks"]["processed_release_caveat_retained"] = False
    catches["dropped_processing_caveat"] = caught(p, independent, "processed_caveat")

    p = copy.deepcopy(production)
    p["resolutions"]["12"]["comparison"]["concordant"] = False
    catches["false_concordance"] = caught(p, independent, "K12_concordant")

    p = copy.deepcopy(production)
    p["resolutions"]["24"]["classification"] = "TENSION"
    catches["wrong_resolution_class"] = caught(p, independent, "K24_classification")

    q = copy.deepcopy(independent)
    q["resolutions"]["12"]["pantheon"]["theta"][3] += 1e-3
    catches["cross_implementation_theta_drift"] = caught(
        production, q, "theta_cross_tolerance"
    )

    q = copy.deepcopy(independent)
    q["resolutions"]["16"]["comparison"]["chi2"] += 1e-3
    catches["cross_implementation_chi_drift"] = caught(
        production, q, "shape_chi2_cross_tolerance"
    )

    result = {
        "audit": "G236_CATCH_PROOFS",
        "status": "PASS" if all(catches.values()) else "FAIL",
        "catches": catches,
        "count": len(catches),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
