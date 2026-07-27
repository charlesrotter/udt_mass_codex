#!/usr/bin/env python3
"""Fail-closed verification and exercised mutations for the selector audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MAXIMUM = (
    "TWELVE_PREREGISTERED_CANDIDATE_FAMILY_BOUNDARY;"
    "NO_ACTIVE_UDT_AUTHORITATIVE_LOCAL_LORENTZ_EQUIVARIANT_COMPLETE_EXTENSION_SECTION_EVIDENCED;"
    "SUPPLIED_REDUCED_HOLONOMY_CONDITIONALLY_FORCES_POINTWISE_FULL_CHART_PLUS_OR_MINUS_MEMBER;"
    "NON_LORENTZ_TWISTED_ZERO_REMAINS_PARTIAL_IN_FULL_CLASS;"
    "GLOBAL_BUNDLE_TRANSITION_LAW_ADMISSIBLE_SECTIONS_AND_PHYSICAL_VARIATION_DOMAIN_REMAIN_OPEN"
)
ALLOWED_OUTCOMES = {
    "SELECTED_DERIVED",
    "SELECTED_CONDITIONAL",
    "PARTIAL_CONSTRAINT",
    "SET_VALUED_ONLY",
    "AVAILABLE_CONDITIONAL",
    "OBSTRUCTED_ON_CONTROL",
    "NO_ACTIVE_AUTHORITY",
    "OPEN_SOURCE",
}
ALLOWED_STATUS_PREFIXES = ("PASS", "FAIL", "PARTIAL", "OPEN", "NOT_APPLICABLE")
EXPECTED_REASONS = {
    "C01": "founded_pair_fixes_only_the_two_channel_projection",
    "C02": "unique_Killing_line_exists_on_some_complete_witnesses_but_not_a_complete_extension",
    "C03": "nonnull_dphi_selects_a_line_split_but_not_the_ordered_pair_and_fails_null_zero_type_change",
    "C04": "three_pairings_exist_only_on_the_real_Segre_1_111_stratum_while_complex_repeated_and_Einstein_strata_do_not_supply_a_complete_section",
    "C05": "principal_bivector_data_does_not_supply_a_complete_founded_extension_and_degenerates",
    "C06": "curvature_operator_reductions_are_not_complete_sections_and_full_holonomy_obstructs_descent",
    "C07": "angular_axes_require_a_supplied_split_and_fail_round_ties_wall_crossing_and_monodromy",
    "C08": "projectors_presuppose_the_solder_or_nonnull_direction_they_would_need_to_select",
    "C09": "dual_systole_is_globally_set_covariant_but_has_exact_two_and_three_way_ties",
    "C10": "supplied_SO3_or_SOplus12_centralizer_conditions_force_pointwise_full_chart_plus_or_minus_members_but_the_non_Lorentz_twisted_zero_leaves_two_full_class_mixing_freedoms_and_no_global_branch_is_selected",
    "C11": "phi_zero_makes_every_extension_identity_and_supplies_zero_selector_rank",
    "C12": "supplied_completion_cocycles_constrain_descent_but_neither_completion_nor_section_is selected",
}
EXPECTED_SOURCE_FACTS = {
    "C01": ("FOUNDED_PAIR_ALONE", "S03", "three_angular_generator_and_four_base-angular_mixing_parameters_remain", "positive_constraint_rank"),
    "C02": ("KILLING_LINE_OR_PLANE", "S10", "EXISTS_COMPLETE_FULL_KILLING_ALGEBRA_ONE_DIMENSIONAL", "conditional_geometric_availability"),
    "C03": ("NONNULL_DPHI_PROJECTOR", "S05", "COVARIANT_LINE_SPLIT_NOT_ORDERED_PAIR", "conditional_geometric_availability"),
    "C04": ("RICCI_SPECTRAL_STRUCTURE", "S05", "three_pairings_even_for_simple_spectrum", "set_or_plane_only"),
    "C05": ("WEYL_PRINCIPAL_STRUCTURE", "S05", "CHOICE_DEPENDENT_DERIVATIVE_LIFT", "set_or_plane_only"),
    "C06": ("RIEMANN_CURVATURE_OPERATOR", "S05", "CHOICE_DEPENDENT_DERIVATIVE_LIFT", "set_or_plane_only"),
    "C07": ("ANGULAR_METRIC_SPECTRAL_DATA", "S11", "preferred_base_screen_projector\tOPEN", "conditional_geometric_availability"),
    "C08": ("RECIPROCAL_PROJECTOR_FAMILY", "S05", "NO_FOUNDED_PHYSICAL_LIFT_FROM_PLANE_ALONE", "conditional_geometric_availability"),
    "C09": ("DUAL_SYSTOLE_MODULE", "S13", "TWO_WAY_TIE_AT_PHI_ZERO", "set_or_plane_only"),
    "C10": ("HOLONOMY_FIXED_SUBSPACE", "S06", "UNIQUE_CONDITIONAL", "conditional_geometric_availability"),
    "C11": ("FINITE_CELL_SEAL_ISOTROPY", "S04", "SCALAR_SEAL_VALUE_HAS_ZERO_EXTENSION_RANK", "positive_constraint_rank"),
    "C12": ("GLOBAL_COMPLETION_TRANSITION_DATA", "S12", "NOT_EVALUABLE", "conditional_geometric_availability"),
}
EXPECTED_OUTCOMES = {
    "C01": "PARTIAL_CONSTRAINT",
    "C02": "AVAILABLE_CONDITIONAL",
    "C03": "AVAILABLE_CONDITIONAL",
    "C04": "SET_VALUED_ONLY",
    "C05": "SET_VALUED_ONLY",
    "C06": "SET_VALUED_ONLY",
    "C07": "AVAILABLE_CONDITIONAL",
    "C08": "AVAILABLE_CONDITIONAL",
    "C09": "SET_VALUED_ONLY",
    "C10": "AVAILABLE_CONDITIONAL",
    "C11": "PARTIAL_CONSTRAINT",
    "C12": "AVAILABLE_CONDITIONAL",
}
# Filled from the independently generated canonical TSV and then protected by
# the committed package manifest.  It prevents a coordinated mutation of the
# production constant and both in-memory matrices from becoming self-validating.
EXPECTED_MATRIX_SHA256 = "ec55c57925ad7f72fb75fbbbddaea47a12c46cd6d6049706aa5b66dd20fe0fd3"
EXPECTED_REPORT_SHA256 = {
    "ADVERSARIAL_CORRECTION_LAYER.md": "505a6ed0a88d86b86930f4e2ff77a12f488d7058836bc1dbc546188b84b02392",
    "AUDIT_REPORT.md": "729a40c218585af020526294a74c7246715d13ed5c8c4363dc12eda8cc1de0f6",
    "COMPLETENESS_TILE.tsv": "346b5822c56167a6b7f15819862ec39720fdbb0b7b9d649bfd33afa390dbaf58",
    "DEPENDENCY_CHAIN.tsv": "39b4cf34628dc49fcfa9df8a702d06d4ffea1c790db2d3e3f95cba57d00fa015",
    "EXACT_DERIVATION.md": "15341969195924fa578a9c3a83f56c8270c093c03622f7ee233de51358b5b2d3",
    "FRESH_ADVERSARIAL_REVIEW.md": "317d36474e444238e6e35fec9a681d7a57581550ebd763b527c2af33eeba8292",
    "LAY_REPORT.md": "df5c15a38e74229b88b4a0bd149c76a5cddcd0b3cf90031838bb9358bf27c67f",
    "NEXT_STEP.md": "1ffd57f7f8a864a5d98b8426a81ca89e249d938f81151ae509aa79a0ed2bf45e",
    "STATUS_LEDGER.tsv": "f5cf1420e3bf05904531100fa0e08dcae3f753e4ea6e68166d235317f5d03efb",
}


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def read_json(name: str):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def tsv_sha256(rows: list[dict[str, str]], fields: list[str]) -> str:
    lines = ["\t".join(fields)]
    for row in rows:
        lines.append("\t".join(row[field] for field in fields))
    return hashlib.sha256(("\n".join(lines) + "\n").encode("utf-8")).hexdigest()


def git_tsv(name: str) -> list[dict[str, str]]:
    relative = (HERE.relative_to(ROOT) / name).as_posix()
    data = subprocess.check_output(["git", "show", f"HEAD:{relative}"], cwd=ROOT, text=True)
    return list(csv.DictReader(data.splitlines(), delimiter="\t"))


def outcome_from_gate_cells(cid: str, matrix_map: dict[tuple[str, str], str]) -> str:
    first_fifteen = [matrix_map[(cid, f"G{i:02d}")] for i in range(1, 16)]
    if all(value == "PASS" for value in first_fifteen):
        return "SELECTED_DERIVED"
    g03, g04 = matrix_map[(cid, "G03")], matrix_map[(cid, "G04")]
    if g03 == "PARTIAL_PAIR_ONLY" or g04 == "FAIL_SEAL_IDENTITY_HAS_ZERO_EXTENSION_RANK":
        return "PARTIAL_CONSTRAINT"
    set_only_targets = {
        "FAIL_EIGENLINES_NOT_EXTENSION",
        "FAIL_BIVECTOR_PLANES_NOT_EXTENSION",
        "FAIL_BIVECTOR_OPERATOR_NOT_EXTENSION",
        "FAIL_CHARACTER_SET_NOT_EXTENSION",
    }
    if g04 in set_only_targets:
        return "SET_VALUED_ONLY"
    return "AVAILABLE_CONDITIONAL"


def validate(
    candidates,
    gates,
    matrix,
    outcomes,
    independent,
    manifest,
    premises,
    reports,
    independent_matrix,
    source_facts,
    derivation,
    exact,
    independent_result,
) -> None:
    assert candidates == git_tsv("CANDIDATE_UNIVERSE.tsv")
    assert gates == git_tsv("GATE_SCHEMA.tsv")
    assert premises == git_tsv("PREMISE_LEDGER.tsv")
    canonical_scope = git_tsv("SOURCE_SCOPE.tsv")
    cids = [row["candidate_id"] for row in candidates]
    gids = [row["gate_id"] for row in gates]
    assert cids == [f"C{i:02d}" for i in range(1, 13)]
    assert gids == [f"G{i:02d}" for i in range(1, 17)]
    candidate_family = {row["candidate_id"]: row["candidate_family"] for row in candidates}
    gate_name = {row["gate_id"]: row["gate"] for row in gates}

    keys = [(row["candidate_id"], row["gate_id"]) for row in matrix]
    assert len(keys) == 192 and len(set(keys)) == 192
    assert set(keys) == {(cid, gid) for cid in cids for gid in gids}
    assert all(row["candidate_family"] == candidate_family[row["candidate_id"]] for row in matrix)
    assert all(row["gate"] == gate_name[row["gate_id"]] for row in matrix)
    assert all(row["status"].startswith(ALLOWED_STATUS_PREFIXES) for row in matrix)
    matrix_fields = ["candidate_id", "candidate_family", "gate_id", "gate", "status"]
    assert len(independent_matrix) == 192
    assert [(row["candidate_id"], row["gate_id"]) for row in independent_matrix] == keys
    assert independent_matrix == matrix
    assert tsv_sha256(matrix, matrix_fields) == EXPECTED_MATRIX_SHA256
    assert tsv_sha256(independent_matrix, matrix_fields) == EXPECTED_MATRIX_SHA256

    assert len(outcomes) == 12 and len({row["candidate_id"] for row in outcomes}) == 12
    assert len(independent) == 12 and len({row["candidate_id"] for row in independent}) == 12
    assert all(row["candidate_family"] == candidate_family[row["candidate_id"]] for row in outcomes)
    assert all(row["candidate_family"] == candidate_family[row["candidate_id"]] for row in independent)
    matrix_map = {(row["candidate_id"], row["gate_id"]): row["status"] for row in matrix}
    outcome_map = {row["candidate_id"]: row for row in outcomes}
    independent_map = {row["candidate_id"]: row for row in independent}
    for cid in cids:
        assert outcome_map[cid]["outcome"] in ALLOWED_OUTCOMES
        assert independent_map[cid]["outcome"] in ALLOWED_OUTCOMES
        derived_outcome = outcome_from_gate_cells(cid, matrix_map)
        assert outcome_map[cid]["outcome"] == derived_outcome
        assert independent_map[cid]["outcome"] == derived_outcome
        assert outcome_map[cid]["native_section_selected"] == "NO"
        assert independent_map[cid]["native_section_selected"] == "NO"
        assert outcome_map[cid]["variation_domain"] == "OPEN_SEPARATE_GATE"
        assert independent_map[cid]["variation_domain"] == "OPEN_SEPARATE_GATE"
        assert matrix_map[(cid, "G16")] == "OPEN_SEPARATE_GATE"
        assert outcome_map[cid]["reason"] == EXPECTED_REASONS[cid]
        assert outcome_map[cid]["outcome"] == EXPECTED_OUTCOMES[cid]
        assert outcome_map[cid]["reason"] == EXPECTED_REASONS[cid]
    assert Counter(row["outcome"] for row in outcomes) == {
        "AVAILABLE_CONDITIONAL": 6,
        "PARTIAL_CONSTRAINT": 2,
        "SET_VALUED_ONLY": 4,
    }
    assert sum(row["outcome"] == "SELECTED_DERIVED" for row in outcomes) == 0

    assert matrix_map[("C10", "G15")] == "FAIL_POSITIVE_VALUES_OCCUR_ON_DIFFERENT_BRANCHES"
    assert matrix_map[("C10", "G04")] == "PASS_CONDITIONAL_POINTWISE_FULL_PLUS_MINUS_MEMBERS_TWISTED_ZERO_PARTIAL"
    assert matrix_map[("C10", "G08")] == "PASS_PLUS_MINUS_ONLY_TWISTED_ZERO_NOT_UNIQUE_FULL_CLASS"
    assert matrix_map[("C10", "G12")] == "PARTIAL_TWIST_IS_EXTERNAL_NOT_LORENTZ_HOLONOMY"
    assert matrix_map[("C09", "G09")] == "FAIL_TWO_AND_THREE_WAY_TIES"
    assert matrix_map[("C04", "G08")] == "FAIL_THREE_PAIRINGS_ONLY_ON_REAL_SEGRE_1_111_STRATUM"
    assert matrix_map[("C11", "G04")] == "FAIL_SEAL_IDENTITY_HAS_ZERO_EXTENSION_RANK"
    assert matrix_map[("C03", "G07")] == "FAIL_COMPLEMENT_CHARACTER_CHOSEN"
    assert matrix_map[("C03", "G10")] == "FAIL_NULL_ZERO_TYPE_CHANGE"
    assert matrix_map[("C06", "G11")] == "FAIL_FULL_HOLONOMY_CONTROL"
    assert matrix_map[("C01", "G03")] == "PARTIAL_PAIR_ONLY"
    for cid in cids[1:]:
        assert not matrix_map[(cid, "G03")].startswith("PASS")

    premise_map = {row["premise_id"]: row for row in premises}
    assert premise_map["P06"]["status"] == "CHALLENGED_NOT_DERIVED_INACTIVE"
    assert premise_map["P06"]["use_in_audit"] == "not_used"
    assert premise_map["P08"]["status"] == "OPEN"
    assert premise_map["P14"]["status"] == "OPEN"

    assert len(manifest) == 15
    assert len({row["source_id"] for row in manifest}) == 15
    assert len({row["path"] for row in manifest}) == 15
    assert [{key: row[key] for key in ("source_id", "path", "role")} for row in manifest] == canonical_scope
    normalized_paths = []
    for row in manifest:
        lexical = PurePosixPath(row["path"])
        assert not lexical.is_absolute() and "." not in lexical.parts and ".." not in lexical.parts
        assert lexical.as_posix() == row["path"]
        path = ROOT / row["path"]
        assert not path.is_symlink()
        resolved = path.resolve()
        assert resolved.is_relative_to(ROOT.resolve())
        normalized_paths.append(resolved)
        data = path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == row["sha256"]
        assert len(data) == int(row["bytes"])
        blob = subprocess.check_output(["git", "rev-parse", f"HEAD:{row['path']}"], cwd=ROOT, text=True).strip()
        assert blob == row["git_blob"]
    assert len(set(normalized_paths)) == 15

    assert len(source_facts) == 12
    assert [row["candidate_id"] for row in source_facts] == cids
    assert all(row["candidate_family"] == candidate_family[row["candidate_id"]] for row in source_facts)
    assert {
        row["candidate_id"]: (
            row["candidate_family"],
            row["source_id"],
            row["required_token"],
            row["derived_feature"],
        )
        for row in source_facts
    } == EXPECTED_SOURCE_FACTS
    assert Counter(row["derived_feature"] for row in source_facts) == {
        "conditional_geometric_availability": 6,
        "positive_constraint_rank": 2,
        "set_or_plane_only": 4,
    }
    manifest_map = {row["source_id"]: row for row in manifest}
    for fact in source_facts:
        assert fact["source_id"] in manifest_map
        source_text = (ROOT / manifest_map[fact["source_id"]]["path"]).read_text(encoding="utf-8")
        assert fact["required_token"] in source_text

    assert derivation["maximum_conclusion"] == MAXIMUM
    assert set(derivation) == {
        "candidate_count", "exact_algebra_sha256", "gate_count", "matrix_cell_count",
        "maximum_conclusion", "native_selected_count", "outcome_counts", "source_claims",
        "status_counts",
    }
    assert derivation["candidate_count"] == 12
    assert derivation["gate_count"] == 16
    assert derivation["matrix_cell_count"] == 192
    assert derivation["outcome_counts"] == {
        "AVAILABLE_CONDITIONAL": 6,
        "PARTIAL_CONSTRAINT": 2,
        "SET_VALUED_ONLY": 4,
    }
    assert derivation["native_selected_count"] == 0
    assert derivation["source_claims"]["explicit_unbounded_remainder"]
    assert hashlib.sha256((HERE / "EXACT_ALGEBRA.json").read_bytes()).hexdigest() == derivation["exact_algebra_sha256"]
    assert exact["full_extension_holonomy_solutions"]["spatial_SO3_L12_L13_L23"] == [["0", "0", "0", "0", "1", "0", "1"]]
    assert exact["full_extension_holonomy_solutions"]["lorentz_SOplus12_L02_L03_L23"] == [["0", "0", "0", "0", "-1", "0", "-1"]]
    assert exact["full_extension_holonomy_solutions"]["twisted_reciprocal_swap_odd"] == [["-c01", "c01", "-c11", "c11", "0", "0", "0"]]
    assert exact["reciprocal_swap_is_lorentz"] is False
    assert exact["ricci_complex_control_is_eta_self_adjoint"] is True
    assert independent_result["full_extension_holonomy"]["twisted_reciprocal_swap_odd"]["dimension"] == 2
    assert independent_result["reciprocal_swap_is_lorentz"] is False
    assert independent_result["ricci_scope_control"]["has_nonreal_simple_pair"] is True
    assert independent_result["outcome_counts"] == derivation["outcome_counts"]
    assert independent_result == {
        "candidate_count": 12,
        "extension_ranks": {"determinant": 1, "joint": 7, "mixing": 4, "physical": 7, "transverse": 3},
        "full_extension_holonomy": {
            "base_boost": {"consistent": False, "dimension": None, "rank": 4},
            "full_lorentz": {"consistent": False, "dimension": None, "rank": 7},
            "lorentz_SOplus12": {
                "consistent": True, "dimension": 0, "null_basis": [],
                "particular": [0, 0, 0, 0, -1, 0, -1], "rank": 7,
            },
            "screen_SO2": {
                "consistent": True, "dimension": 1,
                "null_basis": [[0, 0, 0, 0, 1, 0, 1]],
                "particular": [0, 0, 0, 0, 0, 0, 0], "rank": 6,
            },
            "spatial_SO3": {
                "consistent": True, "dimension": 0, "null_basis": [],
                "particular": [0, 0, 0, 0, 1, 0, 1], "rank": 7,
            },
            "twisted_reciprocal_swap_odd": {
                "consistent": True, "dimension": 2,
                "null_basis": [
                    [-1, 1, 0, 0, 0, 0, 0],
                    [0, 0, -1, 1, 0, 0, 0],
                ],
                "particular": [0, 0, 0, 0, 0, 0, 0], "rank": 5,
            },
        },
        "gate_count": 16,
        "hex_shortest_count": 3,
        "hex_shortest_lines": [[0, 1], [1, 0], [1, 1]],
        "independent_matrix_cell_count": 192,
        "independent_matrix_sha256": EXPECTED_MATRIX_SHA256,
        "lorentz_commutant_dimension": 1,
        "lorentz_commutant_rank": 15,
        "native_selected_count": 0,
        "nonnull_projector_idempotent": True,
        "null_projector_undefined": True,
        "outcome_counts": {"AVAILABLE_CONDITIONAL": 6, "PARTIAL_CONSTRAINT": 2, "SET_VALUED_ONLY": 4},
        "reciprocal_swap_is_lorentz": False,
        "ricci_scope_control": {
            "charpoly_descending": [1, -5, 7, -5, 6],
            "complex_block_discriminant": -4,
            "eta_self_adjoint": True,
            "has_nonreal_simple_pair": True,
            "real_Segre_1_111_clock_spatial_pairings": 3,
        },
        "round_shortest_count": 2,
        "round_shortest_lines": [[0, 1], [1, 0]],
        "seal_identity_independent_of_generator": True,
        "source_manifest_count": 15,
        "verdict": "INDEPENDENT_RECONSTRUCTION_PASS",
        "zero_bivector_operator_eigenspace_dimension": 6,
    }

    required_reports = {
        "ADVERSARIAL_CORRECTION_LAYER.md", "AUDIT_REPORT.md", "COMPLETENESS_TILE.tsv",
        "DEPENDENCY_CHAIN.tsv", "EXACT_DERIVATION.md", "FRESH_ADVERSARIAL_REVIEW.md",
        "LAY_REPORT.md", "NEXT_STEP.md", "STATUS_LEDGER.tsv",
    }
    assert set(reports) == required_reports
    forbidden_promotion = re.compile(
        r"(?:ACTION_AND_MASS_DERIVED|COMPLETE[ _]ACTION[ _]AND[ _]MASS[ _](?:IS|ARE)[ _]DERIVED)",
        flags=re.IGNORECASE,
    )
    for name, text in reports.items():
        assert hashlib.sha256(text.encode("utf-8")).hexdigest() == EXPECTED_REPORT_SHA256[name]
        assert "CURRENT_REGISTERED_METRIC_NATURAL_SELECTOR_BOUNDARY" not in text
        assert "UNIVERSAL_NO_GO" not in text
        assert not forbidden_promotion.search(text)
        assert not re.search(r"holonomy\s+conditionally\s+forces[^\n]{0,80}\bsection", text, flags=re.IGNORECASE)
    fresh = reports["FRESH_ADVERSARIAL_REVIEW.md"]
    assert "VERIFIED-WITH-CAVEATS" in fresh
    assert "twelve preregistered candidate families" in fresh
    assert "fifteen frozen source records" in fresh


def mutation_catches(
    candidates, gates, matrix, outcomes, independent, manifest, premises, reports,
    independent_matrix, source_facts, derivation, exact, independent_result,
):
    catches = []

    def expect_fail(fid, description, mutate):
        args = copy.deepcopy((
            candidates, gates, matrix, outcomes, independent, manifest, premises, reports,
            independent_matrix, source_facts, derivation, exact, independent_result,
        ))
        mutate(*args)
        try:
            validate(*args)
        except (AssertionError, KeyError, FileNotFoundError):
            catches.append({"contract_id": fid, "mutation": description, "result": "PASS_REJECTED"})
        else:
            raise AssertionError(f"mutation escaped: {fid}")

    expect_fail("F01", "drop_candidate", lambda c, *rest: c.pop())
    expect_fail("F02", "drop_matrix_cell", lambda c, g, m, *rest: m.pop())
    expect_fail("F03", "false_selected_derived", lambda c, g, m, o, *rest: o[0].update(outcome="SELECTED_DERIVED", native_section_selected="YES"))
    expect_fail("F04", "close_variation_domain", lambda c, g, m, o, *rest: o[0].update(variation_domain="DERIVED"))
    expect_fail("F05", "promote_set_to_section", lambda c, g, m, o, *rest: o[3].update(outcome="SELECTED_DERIVED", native_section_selected="YES"))
    expect_fail("F06", "erase_auxiliary_failure", lambda c, g, m, *rest: next(row for row in m if row["candidate_id"] == "C03" and row["gate_id"] == "G07").update(status="PASS"))
    expect_fail("F07", "erase_tie_failure", lambda c, g, m, *rest: next(row for row in m if row["candidate_id"] == "C09" and row["gate_id"] == "G09").update(status="PASS"))
    expect_fail("F08", "erase_type_change_failure", lambda c, g, m, *rest: next(row for row in m if row["candidate_id"] == "C03" and row["gate_id"] == "G10").update(status="PASS"))
    expect_fail("F09", "erase_full_holonomy_failure", lambda c, g, m, *rest: next(row for row in m if row["candidate_id"] == "C06" and row["gate_id"] == "G11").update(status="PASS"))
    expect_fail("F10", "erase_cross_branch_failure", lambda c, g, m, *rest: next(row for row in m if row["candidate_id"] == "C10" and row["gate_id"] == "G15").update(status="PASS"))
    expect_fail("F11", "activate_inactive_strong_CSN", lambda c, g, m, o, i, s, p, *rest: next(row for row in p if row["premise_id"] == "P06").update(status="ACTIVE_DERIVED"))
    expect_fail("F12", "promote_completion_candidate", lambda c, g, m, o, *rest: o[11].update(outcome="SELECTED_DERIVED", native_section_selected="YES"))
    expect_fail("F13", "universal_no_go", lambda c, g, m, o, i, *rest: i[0].update(outcome="UNIVERSAL_NO_GO"))
    expect_fail("F14", "promote_downstream_variation", lambda c, g, m, o, *rest: o[-1].update(variation_domain="ACTION_DERIVED"))
    expect_fail("F15", "independent_disagreement", lambda c, g, m, o, i, *rest: i[1].update(outcome="SET_VALUED_ONLY"))
    expect_fail("F16", "source_hash_drift", lambda c, g, m, o, i, s, *rest: s[0].update(sha256="0" * 64))
    expect_fail("A01", "bogus_agreed_outcome", lambda c, g, m, o, i, *rest: (o[0].update(outcome="AVAILABLE_CONDITIONAL"), i[0].update(outcome="AVAILABLE_CONDITIONAL")))
    expect_fail("A02", "agreed_unrecognized_universal", lambda c, g, m, o, i, *rest: (o[0].update(outcome="UNIVERSAL_NO_GO"), i[0].update(outcome="UNIVERSAL_NO_GO")))
    expect_fail("A03", "unrecognized_gate_status", lambda c, g, m, *rest: m[0].update(status="NONSENSE"))
    expect_fail("A04", "duplicate_manifest_path", lambda c, g, m, o, i, s, *rest: s[1].update(path=s[0]["path"]))
    expect_fail("A05", "downstream_action_mass_overclaim", lambda c, g, m, o, *rest: o[0].update(reason="ACTION_AND_MASS_DERIVED"))
    expect_fail("A06", "candidate_family_mismatch", lambda c, g, m, *rest: m[0].update(candidate_family="WRONG_FAMILY"))
    expect_fail("B01", "arbitrary_PASS_prefixed_gate_status", lambda c, g, m, *rest: next(row for row in m if row["candidate_id"] == "C05" and row["gate_id"] == "G01").update(status="PASS_ARBITRARY_BOGUS"))

    def coordinated_outcome_swap(c, g, m, o, i, *rest):
        next(row for row in m if row["candidate_id"] == "C02" and row["gate_id"] == "G04").update(status="FAIL_EIGENLINES_NOT_EXTENSION")
        next(row for row in m if row["candidate_id"] == "C04" and row["gate_id"] == "G04").update(status="FAIL_LINE_NOT_EXTENSION")
        next(row for row in o if row["candidate_id"] == "C02").update(outcome="SET_VALUED_ONLY")
        next(row for row in i if row["candidate_id"] == "C02").update(outcome="SET_VALUED_ONLY")
        next(row for row in o if row["candidate_id"] == "C04").update(outcome="AVAILABLE_CONDITIONAL")
        next(row for row in i if row["candidate_id"] == "C04").update(outcome="AVAILABLE_CONDITIONAL")

    expect_fail("B02", "coordinated_agreed_bogus_outcome_swap", coordinated_outcome_swap)
    expect_fail("B03", "normalized_duplicate_manifest_path", lambda c, g, m, o, i, s, *rest: s[1].update(path="./LIVE.md", git_blob=s[0]["git_blob"], sha256=s[0]["sha256"], bytes=s[0]["bytes"]))

    def coordinated_family_relabel(c, g, m, o, i, *rest):
        c[0]["candidate_family"] = "WRONG_FAMILY"
        for rows in (m, o, i):
            for row in rows:
                if row["candidate_id"] == "C01":
                    row["candidate_family"] = "WRONG_FAMILY"

    expect_fail("B04", "coordinated_candidate_family_relabel", coordinated_family_relabel)
    expect_fail("B05", "arbitrary_unchecked_premise_status", lambda c, g, m, o, i, s, p, *rest: next(row for row in p if row["premise_id"] == "P01").update(status="OPEN_BOGUS"))
    expect_fail("B06", "downstream_report_overclaim", lambda c, g, m, o, i, s, p, r, *rest: r.__setitem__("AUDIT_REPORT.md", r["AUDIT_REPORT.md"] + "\nComplete action and mass are DERIVED from this audit.\n"))
    expect_fail("C01", "row_keyed_source_fact_reassignment", lambda c, g, m, o, i, s, p, r, im, sf, *rest: [row.update(source_id="S01", required_token="OPEN") for row in sf])
    expect_fail("C02", "broad_action_mass_global_section_overclaim", lambda c, g, m, o, i, s, p, r, *rest: r.__setitem__("AUDIT_REPORT.md", r["AUDIT_REPORT.md"] + "\nThis audit establishes a native complete action, physical mass, and a globally selected extension section.\n"))
    expect_fail("C03", "pointwise_to_global_section_promotion", lambda c, g, m, o, i, s, p, r, *rest: r.__setitem__("LAY_REPORT.md", r["LAY_REPORT.md"] + "\nThe pointwise holonomy members form a unique global section.\n"))
    expect_fail("C04", "independent_result_semantic_tamper", lambda c, g, m, o, i, s, p, r, im, sf, d, e, ir: ir.update(native_selected_count=12, nonnull_projector_idempotent=False, verdict="UNIVERSAL_NO_GO"))

    def coordinated_both_matrix_mutation(c, g, m, o, i, s, p, r, im, *rest):
        for rows in (m, im):
            next(row for row in rows if row["candidate_id"] == "C05" and row["gate_id"] == "G01").update(status="PASS_ARBITRARY_BOGUS")

    expect_fail("C05", "coordinated_production_and_independent_matrix_mutation", coordinated_both_matrix_mutation)
    return catches


def main() -> None:
    candidates = read_tsv("CANDIDATE_UNIVERSE.tsv")
    gates = read_tsv("GATE_SCHEMA.tsv")
    matrix = read_tsv("SELECTOR_GATE_MATRIX.tsv")
    outcomes = read_tsv("SELECTOR_OUTCOMES.tsv")
    independent = read_tsv("INDEPENDENT_OUTCOMES.tsv")
    manifest = read_tsv("SOURCE_MANIFEST.tsv")
    premises = read_tsv("PREMISE_LEDGER.tsv")
    report_names = [
        "ADVERSARIAL_CORRECTION_LAYER.md", "AUDIT_REPORT.md", "COMPLETENESS_TILE.tsv",
        "DEPENDENCY_CHAIN.tsv", "EXACT_DERIVATION.md", "FRESH_ADVERSARIAL_REVIEW.md",
        "LAY_REPORT.md", "NEXT_STEP.md", "STATUS_LEDGER.tsv",
    ]
    reports = {name: (HERE / name).read_text(encoding="utf-8") for name in report_names}
    independent_matrix = read_tsv("INDEPENDENT_GATE_MATRIX.tsv")
    source_facts = read_tsv("INDEPENDENT_SOURCE_FACTS.tsv")
    derivation = read_json("DERIVATION_RESULT.json")
    exact = read_json("EXACT_ALGEBRA.json")
    independent_result = read_json("INDEPENDENT_RESULT.json")
    validate(
        candidates, gates, matrix, outcomes, independent, manifest, premises, reports,
        independent_matrix, source_facts, derivation, exact, independent_result,
    )
    catches = mutation_catches(
        candidates, gates, matrix, outcomes, independent, manifest, premises, reports,
        independent_matrix, source_facts, derivation, exact, independent_result,
    )
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["contract_id", "mutation", "result"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)
    result = {
        "candidate_count": len(candidates),
        "gate_count": len(gates),
        "matrix_cell_count": len(matrix),
        "candidate_outcome_agreement_count": len(outcomes),
        "native_selected_count": 0,
        "catch_proofs_passed": len(catches),
        "source_manifest_count": len(manifest),
        "verdict": "PASS_VERIFIED_WITH_CAVEATS",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
