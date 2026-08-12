#!/usr/bin/env python3
"""Exercise preregistered G84 fail-closed mutations in memory."""

from __future__ import annotations

import copy
import csv
import importlib.util
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_verifier():
    spec = importlib.util.spec_from_file_location("g84_verify_for_catches", HERE / "verify_package.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def rejected(callable_) -> bool:
    try:
        callable_()
    except (AssertionError, KeyError, ValueError):
        return True
    return False


def main() -> None:
    verify = load_verifier()
    profiles = rows(HERE / "PROFILE_COMPLETION_ATLAS.tsv")
    recentered = rows(HERE / "RECENTERED_OBSERVER_LIMIT_ATLAS.tsv")
    counters = rows(HERE / "PAIR_DISTANCE_COUNTEREXAMPLES.tsv")
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    checks: dict[str, bool] = {}

    checks["missing_profile_rejected"] = rejected(lambda: verify.validate_profiles(copy.deepcopy(profiles[:-1])))
    duplicate = copy.deepcopy(profiles)
    duplicate[-1] = copy.deepcopy(duplicate[0])
    checks["duplicate_profile_rejected"] = rejected(lambda: verify.validate_profiles(duplicate))

    wrong_radius = copy.deepcopy(result["geometry"])
    wrong_radius["spatial_radius_over_R"] = "1"
    checks["wrong_radius_rejected"] = rejected(lambda: verify.validate_geometry(wrong_radius))
    wrong_diameter = copy.deepcopy(result["geometry"])
    wrong_diameter["spatial_diameter_over_R"] = "pi"
    checks["wrong_diameter_rejected"] = rejected(lambda: verify.validate_geometry(wrong_diameter))
    injective_x = copy.deepcopy(result["geometry"])
    injective_x["x_map_multiplicity"] = "ONE_TO_ONE"
    checks["false_x_injectivity_rejected"] = rejected(lambda: verify.validate_geometry(injective_x))

    wrong_equator = copy.deepcopy(counters)
    wrong_equator[0]["spatial_distance_over_R"] = "2*pi"
    checks["x2_as_antipode_rejected"] = rejected(lambda: verify.validate_counterexamples(wrong_equator))

    promoted_profile = copy.deepcopy(profiles)
    promoted_profile[0]["physical_status"] = "PHYSICAL_XMAX_SELECTED"
    checks["profile_promotion_rejected"] = rejected(lambda: verify.validate_profiles(promoted_profile))

    false_global = copy.deepcopy(profiles)
    index = next(i for i, row in enumerate(false_global) if row["profile_id"] != "G75_F01_AM")
    false_global[index]["extension_class"] = "ZERO_MIXING_CONSTANT_CURVATURE_GLOBAL_EXTENSION_EXISTS"
    checks["immutable_mixed_companion_rejected"] = rejected(lambda: verify.validate_profiles(false_global))

    false_recenter = copy.deepcopy(recentered)
    false_recenter[0]["status"] = "UNCONDITIONAL_ALL_OBSERVERS"
    checks["unconditional_frame_claim_rejected"] = rejected(lambda: verify.validate_recenter(false_recenter))

    wrong_same_patch = copy.deepcopy(counters)
    same_patch = next(row for row in wrong_same_patch if row["case"] == "SAME_LATITUDE_NORTH_PATCH_GAMMA_RANGE")
    same_patch["stationary_depth"] = "+infinity_limit"
    checks["same_patch_stationary_depth_as_global_distance_rejected"] = rejected(lambda: verify.validate_counterexamples(wrong_same_patch))

    promoted_text = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8") + "\nPHYSICAL_XMAX_SELECTED\n"
    checks["physical_Xmax_promotion_rejected"] = rejected(lambda: verify.validate_authority(promoted_text))

    assert all(checks.values())
    payload = {
        "schema": "udt-cmb-g84-catch-proofs-v1",
        "all_passed": True,
        "count": len(checks),
        "checks": checks,
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
