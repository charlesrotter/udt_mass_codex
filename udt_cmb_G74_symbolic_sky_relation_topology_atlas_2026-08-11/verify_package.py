#!/usr/bin/env python3
"""Fail-closed verifier for the G74 package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def validate(
    production: dict,
    center: list[dict[str, str]],
    atlas: list[dict[str, str]],
    independent: dict,
    premises: list[dict[str, str]],
) -> dict[str, bool]:
    identities = [row["profile_id"] for row in center]
    eligible = {row["profile_id"] for row in center if row["center_status"] == "CENTER_C2_ELIGIBLE"}
    blocked = set(identities) - eligible
    atlas_ids = {row["profile_id"] for row in atlas}
    profiles = production["profiles"]
    persistent = {name for name in eligible if profiles[name]["authority"] == "OBSERVED_SAMPLED_REGULAR_NOT_GLOBAL_PROOF"}
    f01 = {name for name in eligible if profiles[name]["authority"] == "DERIVED_GLOBAL_BIJECTION_F01_OPTICAL_GEOMETRY"}
    premise_by_name = {row["premise"]: row for row in premises}
    checks = {
        "candidate_count": len(identities) == 21,
        "candidate_unique": len(set(identities)) == 21,
        "production_identity_match": set(profiles) == set(identities),
        "center_counts": len(eligible) == 9 and len(blocked) == 12,
        "profile_class_counts": len(f01) == 3 and len(persistent) == 6,
        "status_counts": production["status_counts"] == {
            "DERIVED_GLOBAL_BIJECTION_F01": 3,
            "OBSERVED_SAMPLED_REGULAR_PERSISTENT": 6,
            "BLOCKED_SUPPLIED_PROFILE_NOT_C2_AT_CENTER": 12,
        },
        "blocked_not_solved": atlas_ids.isdisjoint(blocked),
        "all_eligible_solved": atlas_ids == eligible,
        "atlas_rows": len(atlas) == 36,
        "four_trials_each": all(sum(row["profile_id"] == name for row in atlas) == 4 for name in eligible),
        "all_vertices_reach": all(int(row["missing_vertices"]) == 0 for row in atlas),
        "no_negative_faces": all(int(row["negative_faces"]) == 0 for row in atlas),
        "no_near_zero_faces": all(int(row["near_zero_faces"]) == 0 for row in atlas),
        "degree_plus_one": all(abs(float(row["degree_signed_area_estimate"]) - 1.0) < 2.0e-12 for row in atlas),
        "finest_area_positive": all(
            float(profiles[name]["finest_min_signed_area_ratio"]) > 0.5 for name in eligible
        ),
        "persistent_not_promoted": all(
            profiles[name]["authority"] == "OBSERVED_SAMPLED_REGULAR_NOT_GLOBAL_PROOF" for name in persistent
        ),
        "blocked_authority": all(
            profiles[name]["authority"] == "BLOCKED_NO_WHOLE_SKY_SOLVE_NO_REPAIR" for name in blocked
        ),
        "physical_owner_open": production["physical_owner"] == "OPEN_NO_OWNER",
        "scale_symbolic": production["scale_status"] == "POSITIVE_SYMBOLIC_COMMON_SCALE_TOPOLOGY_INVARIANT",
        "twist_neutral_exact": production["exact_checks"]["axisymmetric_twist_drops_from_area_jacobian"] is True,
        "independent_pass": independent["status"] == "PASS" and independent["passed"] == independent["total"] == 13,
        "source_inactive": premise_by_name["source distribution"]["status"] == "OPEN_INACTIVE",
        "survey_inactive": premise_by_name["deep-sky survey structure"]["status"] == "OPEN_INACTIVE",
        "xmax_bootstrap_inactive": premise_by_name["X_max SNe bootstrap"]["status"] == "WORKING_INACTIVE",
    }
    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(failed)
    return checks


def main() -> None:
    manifest = rows(HERE / "SOURCE_MANIFEST.tsv")
    source_ok = all((ROOT / row["path"]).is_file() and digest(ROOT / row["path"]) == row["sha256"] for row in manifest)
    if not source_ok:
        raise AssertionError("source manifest mismatch")
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    center = rows(HERE / "CENTER_REGULARITY_ATLAS.tsv")
    atlas = rows(HERE / "SKY_TOPOLOGY_ATLAS.tsv")
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    premises = rows(HERE / "PREMISE_LEDGER.tsv")
    checks = validate(production, center, atlas, independent, premises)
    npz = np.load(HERE / "SKY_ENDPOINTS.npz")
    endpoint_checks = {
        "npz_key_count": len(npz.files) == 90,
        "all_fine_endpoints": all(
            key.endswith("__endpoint") or key.endswith("__directions") or key.endswith("__endpoint_t")
            or key.endswith("__endpoint_affine") or "__level" in key
            for key in npz.files
        ),
    }
    if not all(endpoint_checks.values()):
        raise AssertionError(endpoint_checks)
    payload = {
        "schema": "udt-cmb-g74-package-verification-v1",
        "status": "PASS",
        "checks": {**checks, **endpoint_checks, "source_manifest": source_ok},
        "passed": len(checks) + len(endpoint_checks) + 1,
        "total": len(checks) + len(endpoint_checks) + 1,
        "protected_draft_read": False,
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
