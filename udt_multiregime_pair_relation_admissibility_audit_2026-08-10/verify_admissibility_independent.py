#!/usr/bin/env python3
"""Independent stdlib reconstruction of the G55 counts and load-bearing branch rulings."""

from __future__ import annotations

import csv
import json
import subprocess
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def local(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def frozen(source_id: str) -> list[dict[str, str]]:
    manifest = {row["source_id"]: row for row in local("SOURCE_MANIFEST.tsv")}
    raw = subprocess.check_output(["git", "show", manifest[source_id]["source_ref"]], cwd=ROOT, text=True)
    return list(csv.DictReader(raw.splitlines(), delimiter="\t"))


def main() -> int:
    branches = frozen("S10")
    relations = {row["branch_id"]: row for row in frozen("S11")}
    transitions = {row["branch_id"]: row for row in frozen("S15")}
    measurements = frozen("S03")
    profiles = local("BRANCH_ADMISSIBILITY_PROFILES.tsv")
    matrix = local("BRANCH_MEASUREMENT_MATRIX.tsv")
    axes = local("BRANCH_AXIS_MATRIX.tsv")
    families = local("GEOMETRIC_PATTERN_FAMILIES.tsv")

    checks: dict[str, bool] = {}
    checks["24_source_branches"] = len(branches) == len(relations) == len(transitions) == 24
    checks["six_measurements"] = len(measurements) == 6
    checks["24_profiles"] = len(profiles) == 24 and len({row["branch_id"] for row in profiles}) == 24
    checks["144_unique_measurement_cells"] = len(matrix) == len({(row["branch_id"], row["measurement_id"]) for row in matrix}) == 144
    checks["240_unique_axis_cells"] = len(axes) == len({(row["branch_id"], row["axis_id"]) for row in axes}) == 240
    checks["11_pattern_families"] = len(families) == 11 and sum(int(row["branch_count"]) for row in families) == 24

    source_dispositions = Counter(row["primary_disposition"] for row in relations.values())
    checks["source_disposition_partition"] = source_dispositions == Counter({
        "INSUFFICIENT_TYPED_EVIDENCE": 9,
        "LOCAL_RELATIONS_GLOBAL_OWNERSHIP_OPEN": 5,
        "NO_COMPLETE_FAMILY_ON_DECLARED_BRANCH": 4,
        "PATH_BRANCH_GROUPOID_OWNED": 2,
        "STRATIFIED_MIXTURE_OWNED": 2,
        "COMMON_CALIBRATED_ATLAS_OWNED": 1,
        "HISTORICAL_PREMISES_CHANGED_REVIEW_REQUIRED": 1,
    })
    transition_dispositions = Counter(row["primary_disposition"] for row in transitions.values())
    checks["transition_disposition_partition"] = transition_dispositions == Counter({
        "INSUFFICIENT_TYPED_EVIDENCE": 9,
        "CONDITIONAL_QUERY_OR_PRESENTATION_TRANSITION_ONLY": 5,
        "NO_COMPLETE_REGULAR_BRANCH": 4,
        "ISOMETRIC_PATH_TRANSPORT_ONLY": 2,
        "AGGREGATE_MEMBER_DEPENDENT": 1,
        "HISTORICAL_REDERIVATION_REQUIRED": 1,
        "PARTIAL_CLOCK_SCALE_TRANSITION_OWNED": 1,
        "STRATIFIED_PROJECTOR_TRANSPORT_ONLY": 1,
    })
    checks["R04_parent_is_member_dependent"] = (
        relations["R04"]["local_observer_query_object"] == "MEMBER_DEPENDENT"
        and relations["R04"]["transition_or_path_arrow"] == "MEMBER_DEPENDENT"
        and relations["R04"]["middle_state_ownership"] == "MEMBER_DEPENDENT"
        and transitions["R04"]["intrinsic_clock_scale"] == "MEMBER_DEPENDENT"
        and transitions["R04"]["intrinsic_ruler_or_grading"] == "MEMBER_DEPENDENT"
        and transitions["R04"]["owned_geometric_transport"] == "MEMBER_DEPENDENT"
        and transitions["R04"]["terminal_reciprocal_status"] == "NO_CLASS_WIDE_SCALAR"
    )

    profile = {row["branch_id"]: row for row in profiles}
    cell = {(row["branch_id"], row["measurement_id"]): row for row in matrix}
    axis = {(row["branch_id"], row["axis_id"]): row for row in axes}
    checks["schema_family_exact"] = {bid for bid, row in profile.items() if row["pattern_family"] == "F01_SCHEMA_ONLY"} == {"R01", "R02", "R03", "R05", "R07", "R08", "R09", "R10", "R11"}
    checks["no_complete_family_exact"] = {bid for bid, row in profile.items() if row["pattern_family"] == "F03_NO_COMPLETE_REGULAR_BRANCH"} == {"R06", "R16", "R21"}
    checks["query_unowned_family_exact"] = {bid for bid, row in profile.items() if row["pattern_family"] == "F05_GLOBAL_METRIC_QUERY_UNOWNED"} == {"R13", "R14", "R20"}
    checks["clock_only_family_exact"] = {bid for bid, row in profile.items() if row["pattern_family"] == "F08_CLOCK_ONLY"} == {"R18", "R22"}
    checks["R17_full_conditional"] = profile["R17"]["pattern_family"] == "F07_FULL_RECIPROCAL_PATH_CONDITIONAL"
    checks["R23_screen_path_no_scale"] = profile["R23"]["pattern_family"] == "F10_COMPLETE_SCREEN_PATH_NO_SCALE"
    checks["R24_set_projector"] = profile["R24"]["pattern_family"] == "F11_SET_VALUED_PROJECTOR"

    checks["no_physical_pair_owner"] = not any(axis[(bid, "A01")]["disposition"] in {"BRANCH_OWNED", "GLOBAL_COMPLETION_OWNED"} for bid in profile)
    checks["no_nonisometric_arrow_owner"] = not any(axis[(bid, "A07")]["disposition"] in {"BRANCH_OWNED", "GLOBAL_COMPLETION_OWNED"} for bid in profile)
    checks["no_optional_selector_owner"] = not any(axis[(bid, "A08")]["disposition"] in {"BRANCH_OWNED", "GLOBAL_COMPLETION_OWNED"} for bid in profile)
    checks["no_physical_regime_owner"] = not any(axis[(bid, "A10")]["disposition"] in {"BRANCH_OWNED", "GLOBAL_COMPLETION_OWNED"} for bid in profile)
    checks["five_global_structure_owners"] = {bid for bid in profile if axis[(bid, "A09")]["disposition"] == "GLOBAL_COMPLETION_OWNED"} == {"R04", "R17", "R18", "R23", "R24"}

    checks["founded_phi_branch_set"] = {bid for bid in profile if cell[(bid, "M02")]["disposition"] == "FOUNDED_AFTER_PAIR_SUPPLIED"} == {"R13", "R14", "R17", "R20", "R23"}
    checks["R04_no_aggregate_panel_inheritance"] = all(
        cell[("R04", f"M{i:02d}")]["disposition"] == "INSUFFICIENT_EVIDENCE"
        for i in range(1, 6)
    ) and all(
        axis[("R04", f"A{i:02d}")]["disposition"] == "INSUFFICIENT_EVIDENCE"
        for i in range(2, 7)
    )
    checks["R17_measurement_vector"] = tuple(cell[("R17", f"M{i:02d}")]["disposition"] for i in range(1, 7)) == (
        "CONDITIONALLY_AVAILABLE", "FOUNDED_AFTER_PAIR_SUPPLIED", "CONDITIONALLY_AVAILABLE",
        "CONDITIONALLY_AVAILABLE", "CONDITIONALLY_AVAILABLE", "OPEN_OWNER",
    )
    checks["R18_not_complete_reciprocal"] = all(cell[("R18", f"M{i:02d}")]["disposition"] == "OPEN_OWNER" for i in range(1, 7))
    checks["R23_measurement_vector"] = tuple(cell[("R23", f"M{i:02d}")]["disposition"] for i in range(1, 7)) == (
        "CONDITIONALLY_AVAILABLE", "FOUNDED_AFTER_PAIR_SUPPLIED", "CONDITIONALLY_AVAILABLE",
        "CONDITIONALLY_AVAILABLE", "INSUFFICIENT_EVIDENCE", "OPEN_OWNER",
    )
    checks["R24_density_type_absent"] = all(cell[("R24", f"M{i:02d}")]["disposition"] == "TYPE_INAPPLICABLE" for i in range(1, 6))
    checks["R15_local_scope_retained"] = cell[("R15", "M02")]["disposition"] == "CONDITIONALLY_AVAILABLE" and cell[("R15", "M04")]["disposition"] == "TYPE_INAPPLICABLE"
    checks["R20_no_invented_path"] = cell[("R20", "M04")]["disposition"] == "OPEN_OWNER"
    checks["all_regime_labels_open"] = all(row["physical_regime_label"] == "OPEN_NOT_ASSIGNED" for row in families)
    checks["kappa_retained"] = any(row["measurement_id"] == "M01" and row["object"] == "kappa" for row in matrix)
    checks["beta_retained"] = any(row["measurement_id"] == "M03" and row["object"] == "beta" for row in matrix)
    checks["angular_path_retained"] = any(row["measurement_id"] == "M04" and row["object"] == "U_gamma" for row in matrix)

    failed = sorted(name for name, passed in checks.items() if not passed)
    result = {
        "schema_version": 1,
        "method": "INDEPENDENT_STDLIB_SOURCE_PARTITION_AND_EXACT_CELL_RECONSTRUCTION",
        "status": "PASS" if not failed else "FAIL",
        "passed": sum(checks.values()),
        "total": len(checks),
        "failed": failed,
        "checks": checks,
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
