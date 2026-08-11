#!/usr/bin/env python3
"""Exercise fail-closed semantic mutations against the G74 verifier."""

from __future__ import annotations

import copy
import csv
import json
import runpy
from pathlib import Path


HERE = Path(__file__).resolve().parent
VERIFIER = runpy.run_path(HERE / "verify_package.py")
validate = VERIFIER["validate"]


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def rejected(mutator, baseline: tuple) -> bool:
    trial = copy.deepcopy(baseline)
    mutator(*trial)
    try:
        validate(*trial)
    except (AssertionError, KeyError):
        return True
    return False


def main() -> None:
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    center = rows(HERE / "CENTER_REGULARITY_ATLAS.tsv")
    atlas = rows(HERE / "SKY_TOPOLOGY_ATLAS.tsv")
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    premises = rows(HERE / "PREMISE_LEDGER.tsv")
    baseline = (production, center, atlas, independent, premises)
    validate(*copy.deepcopy(baseline))

    blocked_name = next(row["profile_id"] for row in center if row["center_status"].startswith("BLOCKED"))
    persistent_name = next(name for name, row in production["profiles"].items() if row["authority"].startswith("OBSERVED"))
    catches = {
        "missing_candidate": rejected(lambda p, c, a, i, r: c.pop(), baseline),
        "duplicate_candidate": rejected(lambda p, c, a, i, r: c.append(copy.deepcopy(c[0])), baseline),
        "blocked_promoted_to_eligible": rejected(
            lambda p, c, a, i, r: next(row for row in c if row["profile_id"] == blocked_name).__setitem__("center_status", "CENTER_C2_ELIGIBLE"), baseline
        ),
        "blocked_profile_inserted_into_atlas": rejected(
            lambda p, c, a, i, r: a.append({**copy.deepcopy(a[0]), "profile_id": blocked_name}), baseline
        ),
        "persistent_promoted_to_derived_global": rejected(
            lambda p, c, a, i, r: p["profiles"][persistent_name].__setitem__("authority", "DERIVED_GLOBAL_BIJECTION"), baseline
        ),
        "degree_perturbed": rejected(
            lambda p, c, a, i, r: a[0].__setitem__("degree_signed_area_estimate", "0.75"), baseline
        ),
        "negative_face_hidden": rejected(
            lambda p, c, a, i, r: a[0].__setitem__("negative_faces", "1"), baseline
        ),
        "physical_owner_promoted": rejected(
            lambda p, c, a, i, r: p.__setitem__("physical_owner", "OWNED_NATIVE"), baseline
        ),
        "scale_selected": rejected(
            lambda p, c, a, i, r: p.__setitem__("scale_status", "PHYSICAL_SCALE_SELECTED"), baseline
        ),
        "twist_topology_claim": rejected(
            lambda p, c, a, i, r: p["exact_checks"].__setitem__("axisymmetric_twist_drops_from_area_jacobian", False), baseline
        ),
        "source_activated": rejected(
            lambda p, c, a, i, r: next(row for row in r if row["premise"] == "source distribution").__setitem__("status", "OWNED_NATIVE"), baseline
        ),
        "independent_failure_ignored": rejected(
            lambda p, c, a, i, r: i.__setitem__("status", "FAIL"), baseline
        ),
    }
    if not all(catches.values()):
        raise AssertionError([name for name, value in catches.items() if not value])
    payload = {
        "schema": "udt-cmb-g74-catch-proofs-v1",
        "status": "PASS",
        "catches": catches,
        "passed": sum(catches.values()),
        "total": len(catches),
        "protected_draft_read": False,
    }
    (HERE / "CATCH_PROOF_RESULTS.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
