#!/usr/bin/env python3
"""Fail-closed verifier; does not import or execute build_reconciliation.py."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def index_unique(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    values = [row[key] for row in rows]
    if len(values) != len(set(values)):
        raise AssertionError(f"duplicate {key}")
    return {row[key]: row for row in rows}


def validate(families: list[dict[str, str]], mechanisms: list[dict[str, str]],
             sources: list[dict[str, str]], check_disk: bool = True) -> None:
    fam = index_unique(families, "family_id")
    mech = index_unique(mechanisms, "axis_id")
    src = index_unique(sources, "source_id")
    assert set(fam) == {f"F{i:02d}" for i in range(1, 8)}
    assert set(mech) == {f"M{i:02d}" for i in range(1, 17)}
    assert set(src) == {f"A{i:02d}" for i in range(1, 21)}

    expected_kinds = {
        "F01": "CONDITIONAL_REALIZED_P4_CONSTANTS_FAMILY",
        "F02": "CONDITIONAL_REALIZED_P4_FIELDS_FAMILY",
        "F03": "CONTROL_STRATUM_NOT_FAMILY",
        "F04": "CONDITIONAL_REALIZED_HOPFION_MODEL_FAMILY",
        "F05": "STRUCTURAL_COMPLETION_CLASS_NOT_FAMILY",
        "F06": "EXACT_EMPTY_SCOPE_NOT_FAMILY",
        "F07": "FORMAL_MODULE_CLASS_NOT_FAMILY",
    }
    assert {key: row["object_kind"] for key, row in fam.items()} == expected_kinds

    assert "FOUR_LABELED_CANDIDATE_MASS_READINGS_NONZERO" in fam["F01"]["mass_or_energy_reading"]
    assert "NONE_PROMOTED" in fam["F01"]["mass_or_energy_reading"]
    assert "POINTWISE_ROWS_KILL_NONZERO_BRANCH" in fam["F01"]["variation_census"]
    assert "ALL_FOUR_OWNED_LOCAL_JOINT_INDICES_ONE" in fam["F01"]["stability_status"]
    assert "TWO_WALL_RESPONSES_CAN_CONDITIONALLY_REPAIR_RESTRICTED_FORM" in fam["F01"]["effect_of_more_structure"]
    assert fam["F01"]["maximum_claim"] == "CONDITIONAL_GEOMETRIC_MASS_BEARING_BRANCH"

    assert "M_WALL_ZERO_DISSENTS" in fam["F02"]["mass_or_energy_reading"]
    assert "JET_QUADRATIC_SECTOR_NONNEGATIVE_IFF" in fam["F02"]["stability_status"]
    assert "NO_FULL_CERTIFICATE" in fam["F02"]["stability_status"]
    assert "ADDING_CYCLIC_OR_FOLD_COMPLETION_CAN_KILL" in fam["F02"]["effect_of_more_structure"]

    assert fam["F04"]["mass_or_energy_reading"] == "NONZERO_CONDITIONAL_STATIC_ENERGY__NO_NATIVE_UDT_MASS_ASSIGNMENT"
    assert "S2_POSIT" in fam["F04"]["carrier_action_status"]
    assert fam["F04"]["maximum_claim"] == "CONDITIONAL_ENERGY_BEARING_STATIC_MODEL_NOT_NATIVE_MASS"
    assert fam["F05"]["maximum_claim"] == "COMPLETION_AND_MASS_CLASSIFICATION_ONLY"
    assert "DOES_NOT_CREATE_A_PEER_FAMILY" in fam["F05"]["effect_of_more_structure"]
    assert fam["F07"]["time_angular_status"] == "FORMAL_COMPATIBILITY_ONLY__NO_COMMON_NONZERO_ONSHELL_OBJECT"

    for family_id in ("F02", "F04", "F05"):
        assert "F01" not in fam[family_id]["maximum_claim"]
        assert "RULED_OUT_BY_F01" not in "\t".join(fam[family_id].values())

    assert mech["M01"]["structure_state"] == "INTEGRATED_MODULI_ROWS"
    assert mech["M02"]["structure_state"] == "POINTWISE_MODULI_ROWS"
    assert "REMOVES_THE_F01_NONZERO_BRANCH" in mech["M02"]["exact_effect"]
    assert "NONNEGATIVE_IFF" in mech["M05"]["exact_effect"]
    assert "RESTORED_MU_GIVES_NEGATIVE_JOINT_WITNESS" in mech["M07"]["exact_effect"]
    assert "RESPONSES_NOT_SELECTED" in mech["M08"]["selection_status"]
    assert "MASS_BEARING_COMPLETION" in mech["M09"]["exact_effect"]
    assert "NONZERO_MASSIVE_SCOPE_EMPTY" in mech["M10"]["exact_effect"]
    assert mech["M12"]["bounded_layer"] == "TIME_LIVE_T1_TO_T3"
    assert mech["M12"]["structure_state"] == "EVERYTHING_ON_WITHIN_TIME_JET_LE_2_REGISTERED_LAYER"
    assert "NO_COMMON_ONSHELL_SOLUTION" in mech["M12"]["exact_effect"]
    assert mech["M13"]["structure_state"] == "FULL_REGISTERED_SMOOTH_TORUS_TO_TWO_CAP_S3_CENSUS"
    assert "ON_SHELL" not in mech["M13"]["selection_status"]
    assert "POSIT_AND_CONDITIONAL_NOT_METRIC_NATIVE" == mech["M14"]["selection_status"]
    assert "ZERO_EXACT_F01_SECOND_WALL_GERM_MAPS" in mech["M15"]["exact_effect"]
    assert "SELECTS_NO_FAMILY_RESPONSE_BOUNDARY_OR_MASS_VALUE" in mech["M16"]["exact_effect"]

    required_source_tokens = {
        "A03": ["INTEGRATED", "POINTWISE", "massive under ALL four readings"],
        "A05": ["M-GEN = M-DENS-coord = M-DENS-proper", "M-WALL dissenting at 0"],
        "A07": ["crease | glue MIXED chain", "all-definite members"],
        "A08": ["STABLE-in-this-sector iff 64 E0^2 l^4 <= g_p c_m", "UNSTABLE"],
        "A09": ["EVERYTHING-ON", "BOUNDED BY LAYER"],
        "A11": ["completion join", "on-shell coexistence"],
        "A12": ["S2 carrier", "SETTLED_STATIC_FINITE_BOX_CONDITIONAL"],
        "A14": ["OPERATIONAL_EVIDENCE_MAP_NOT_SOLUTION_PARTITION", "FORMAL_EMBEDDING_ONLY"],
        "A16": ["NATIVE_OFFSHELL_PARENT_ARENA_DERIVED__REALIZATION_VARIATION_OPEN"],
        "A17": ["All four full local conditional domains have one negative direction"],
        "A18": ["PARTIAL_ANALOGIES_ONLY__F01_BOUNDARY_BRIDGE_OPEN"],
        "A19": ["TWO_PARAMETER_CONDITIONAL_STABILITY_THRESHOLD_SURFACE_DERIVED"],
        "A20": ["no time/angular-live on-shell massive"],
    }
    if check_disk:
        for source_id, row in src.items():
            data = (ROOT / row["path"]).read_bytes()
            assert str(len(data)) == row["bytes"]
            assert sha256(data) == row["sha256"]
            text = data.decode("utf-8")
            for token in required_source_tokens.get(source_id, []):
                assert token in text, (source_id, token)


def expect_failure(name: str, mutator, families, mechanisms, sources) -> tuple[str, str]:
    f, m, s = copy.deepcopy(families), copy.deepcopy(mechanisms), copy.deepcopy(sources)
    mutator(f, m, s)
    try:
        validate(f, m, s, check_disk=True)
    except (AssertionError, KeyError, FileNotFoundError):
        return name, "PASS"
    return name, "FAIL"


def main() -> None:
    families = read_tsv(OUT / "FAMILY_RECONCILIATION.tsv")
    mechanisms = read_tsv(OUT / "MECHANISM_EFFECT_MATRIX.tsv")
    sources = read_tsv(OUT / "SOURCE_INVENTORY.tsv")
    validate(families, mechanisms, sources)

    mutations = [
        ("missing_family", lambda f, m, s: f.pop()),
        ("duplicate_family", lambda f, m, s: f.append(copy.deepcopy(f[0]))),
        ("mass_definition_promotion", lambda f, m, s: f[0].__setitem__("mass_or_energy_reading", "PHYSICAL_MASS_DERIVED")),
        ("f01_negative_overgeneralization", lambda f, m, s: f[1].__setitem__("maximum_claim", "RULED_OUT_BY_F01")),
        ("formal_module_promoted_onshell", lambda f, m, s: f[6].__setitem__("time_angular_status", "COMMON_ONSHELL_SOLUTION")),
        ("hopfion_carrier_promoted_native", lambda f, m, s: f[3].__setitem__("carrier_action_status", "NATIVE_METRIC_CARRIER")),
        ("integrated_pointwise_conflation", lambda f, m, s: f[0].__setitem__("variation_census", "INTEGRATED_EQUALS_POINTWISE")),
        ("unbounded_everything_on", lambda f, m, s: m[11].__setitem__("structure_state", "COMPLETE_UDT_EVERYTHING_ON")),
        ("completion_class_promoted_family", lambda f, m, s: f[4].__setitem__("object_kind", "CONDITIONAL_REALIZED_MASS_FAMILY")),
        ("source_mutation", lambda f, m, s: s[0].__setitem__("sha256", "0" * 64)),
        ("stale_f01_positive_slice", lambda f, m, s: f[0].__setitem__("stability_status", "ODD_PIN_LOCAL_SURVIVOR_POSITIVE")),
        ("f02_sector_promoted_full_stability", lambda f, m, s: f[1].__setitem__("stability_status", "NATIVE_FULLY_STABLE")),
        ("f04_energy_promoted_mass", lambda f, m, s: f[3].__setitem__("mass_or_energy_reading", "NATIVE_UDT_MASS_DERIVED")),
        ("missing_wall_response_nonselection", lambda f, m, s: m[7].__setitem__("selection_status", "NATIVE_SELECTED")),
    ]
    catches = [expect_failure(name, mutation, families, mechanisms, sources) for name, mutation in mutations]
    assert all(status == "PASS" for _, status in catches)
    with (OUT / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["catch", "result"])
        writer.writerows(catches)

    result = json.loads((OUT / "RESULT.json").read_text(encoding="utf-8"))
    assert result["external_cold_review"] == "PASS_AFTER_REQUIRED_PRIORITY_WORDING_REPAIR__CLOSED"
    verification = {
        "status": "PASS",
        "family_rows": len(families),
        "mechanism_rows": len(mechanisms),
        "source_rows": len(sources),
        "catch_proofs_passed": len(catches),
        "catch_proofs_total": len(catches),
        "outcome_checked": result["outcome"],
    }
    (OUT / "VERIFICATION_RESULT.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(verification, sort_keys=True))


if __name__ == "__main__":
    main()
