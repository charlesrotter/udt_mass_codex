#!/usr/bin/env python3
"""Validate the independently saved FD1 records using the frozen all-three-n family semantics."""

from __future__ import annotations

import copy
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INDEPENDENT = ROOT / "phase2_independent_verification_failed_outside.json"
BOUNDARY = ROOT / "phase2_transition_refinement_failed_boundary.json"
OUT = ROOT / "phase2_family_semantics_verification.json"
KEYS: dict[str, bool] = {}


def key(name: str, condition: bool) -> None:
    KEYS[name] = bool(condition)
    print(f"KEY {name}: {KEYS[name]}")


def validate(records: list[dict[str, object]], metadata: dict[str, object]) -> tuple[bool, dict[str, object]]:
    identities = [tuple(record["identity"]) for record in records]
    if len(records) != 36 or len(set(identities)) != 36:
        return False, {}
    if metadata.get("boundary_failure") is not True or metadata.get("strict_outside_failure") is not True:
        return False, {}
    inside = [record for record in records if record["expected_inside"]]
    outside = [record for record in records if not record["expected_inside"]]
    if len(inside) != 12 or not all(record["comparison"]["inside"] for record in inside):
        return False, {}
    grouped: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for record in outside:
        identity = record["identity"]
        grouped[(identity[1], identity[2], identity[3])].append(record)
    if len(grouped) != 8:
        return False, {}
    for family in grouped.values():
        if len(family) != 3 or len({record["identity"][0] for record in family}) != 3:
            return False, {}
        if all(record["comparison"]["inside"] for record in family):
            return False, {}
    for record in inside:
        comparison = record["comparison"]
        if comparison.get("affine_offset_spent") is not True:
            return False, {}
        if comparison.get("absolute_contained") is not True:
            return False, {}
        if float(comparison.get("one_scale_max_abs_fractional_residual", 0.0)) <= 0.20:
            return False, {}
    summary = {
        "inside_configurations": len(inside),
        "outside_families": len(grouped),
        "outside_individual_rows_that_flipped_inside": sum(
            bool(record["comparison"]["inside"]) for record in outside
        ),
        "outside_family_states": [
            {
                "family": family_id,
                "individual_inside_states": [bool(record["comparison"]["inside"]) for record in family],
                "family_inside_all_three_n": all(record["comparison"]["inside"] for record in family),
            }
            for family_id, family in sorted(grouped.items())
        ],
    }
    return True, summary


def main() -> None:
    independent = json.loads(INDEPENDENT.read_text(encoding="utf-8"))
    boundary = json.loads(BOUNDARY.read_text(encoding="utf-8"))
    records = independent["records"]
    metadata = {
        "boundary_failure": boundary["keys"]["FD1_R2_boundary_grid_convergence"] is False,
        "strict_outside_failure": independent["keys"]["FD1_IV4_independent_outside"] is False,
    }
    passed, semantic_summary = validate(records, metadata)
    key("FD1_FS1_prior_failures_preserved", all(metadata.values()))
    key("FD1_FS2_family_semantics", passed)
    key("FD1_FS3_independent_numerics", independent["keys"]["FD1_IV5_frequency_agreement"] and independent["keys"]["FD1_IV6_raw_backward_residual"])
    key("FD1_FS4_inside_absolute_troughs", independent["keys"]["FD1_IV7_absolute_trough_containment"])
    key("FD1_FS5_one_scale_caveat", independent["keys"]["FD1_IV8_one_scale_mismatch_disclosed"])

    mutations = []
    duplicate = copy.deepcopy(records); duplicate.append(copy.deepcopy(duplicate[0]))
    mutations.append(("duplicate_identity", not validate(duplicate, metadata)[0]))
    missing = copy.deepcopy(records[:-1])
    mutations.append(("missing_identity", not validate(missing, metadata)[0]))
    failed_inside = copy.deepcopy(records); failed_inside[0]["comparison"]["inside"] = False
    mutations.append(("failed_inside", not validate(failed_inside, metadata)[0]))
    all_inside_outside = copy.deepcopy(records)
    target = (all_inside_outside[12]["identity"][1], all_inside_outside[12]["identity"][2], all_inside_outside[12]["identity"][3])
    for record in all_inside_outside:
        identity = record["identity"]
        if not record["expected_inside"] and (identity[1], identity[2], identity[3]) == target:
            record["comparison"]["inside"] = True
    mutations.append(("outside_family_promoted", not validate(all_inside_outside, metadata)[0]))
    no_offset = copy.deepcopy(records); no_offset[0]["comparison"]["affine_offset_spent"] = False
    mutations.append(("offset_disclosure_removed", not validate(no_offset, metadata)[0]))
    no_one_scale = copy.deepcopy(records); no_one_scale[0]["comparison"]["one_scale_max_abs_fractional_residual"] = 0.01
    mutations.append(("one_scale_caveat_removed", not validate(no_one_scale, metadata)[0]))
    erased_failure = copy.deepcopy(metadata); erased_failure["boundary_failure"] = False
    mutations.append(("boundary_failure_erased", not validate(records, erased_failure)[0]))
    key("FD1_FS6_catch_proofs", all(passed for _, passed in mutations))

    payload = {
        "phase": "FD1_PHASE2_FAMILY_SEMANTICS_CORRECTION",
        "keys": KEYS,
        "metadata": metadata,
        "summary": {
            **semantic_summary,
            "maximum_frequency_drift_from_g240": independent["summary"]["maximum_frequency_drift_from_g240"],
            "maximum_raw_backward_residual": independent["summary"]["maximum_raw_backward_residual"],
            "minimum_inside_affine_margin_to_3p1pct": independent["summary"]["minimum_inside_affine_margin_to_3p1pct"],
            "minimum_inside_centered_margin": independent["summary"]["minimum_inside_centered_margin"],
            "minimum_inside_one_scale_mismatch": independent["summary"]["minimum_inside_one_scale_mismatch"],
            "boundary_locations_certified": False,
        },
        "catch_proofs": [{"name": name, "rejected": passed} for name, passed in mutations],
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"WROTE {OUT}")
    print(f"TOTAL KEYS {sum(KEYS.values())}/{len(KEYS)}")
    if not all(KEYS.values()):
        raise SystemExit(f"failed keys: {[name for name, passed in KEYS.items() if not passed]}")


if __name__ == "__main__":
    main()
