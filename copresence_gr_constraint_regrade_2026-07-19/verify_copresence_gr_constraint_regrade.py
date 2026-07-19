#!/usr/bin/env python3
"""Independent fail-closed verifier for the co-presence GR-constraint regrade."""

from __future__ import annotations

import ast
import copy
import csv
import hashlib
import json
import re
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
RESULT_PATH = HERE / "DERIVATION_RESULT.json"
VERIFY_PATH = HERE / "VERIFICATION_RESULT.json"
OUTCOME = "PRIOR_ALGEBRA_SURVIVES_CONSTRAINT_ROLES_RECLASSIFIED_NO_NATIVE_GR_CONSTRAINT_SELECTED"
SOURCE_HASHES = {
    "gr_constraint_paired_trial_2026-07-18/SHA256SUMS.txt": "8d5c617d9bb611f67b15524b34271de7f121ea9a71fa14d8e131cf85bc2c63a2",
    "bootstrap_variation_selector_2026-07-18/SHA256SUMS.txt": "cad3c4f0dccc1599c5b4ff48c6adafa32fb64b590e4ef4f0f6e20e5e96de9bed",
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md": "db4a426b021e375fa4bca0d870aaf973de319de3b08072195d001a056630832d",
    "copresence_causal_accessibility_selector_2026-07-19/SHA256SUMS.txt": "14e13dd27aa7036a6fef7db9208681459b86c06186bfffc7990ee877947d8356",
    "copresence_causal_accessibility_selector_2026-07-19/DERIVATION_RESULT.json": "ae2396cd8b041536075be6b38a4e8c60bcd23263652c7ff258c3ecbdd865d709",
    "copresence_causal_accessibility_selector_2026-07-19/STATUS_LEDGER.tsv": "1179529aacf4ffeec576a982d71ea4753e4432ce4eda13e2b0467a19de2ab283",
}
MANIFEST_SOURCES = {
    "gr_constraint_paired_trial_2026-07-18/SHA256SUMS.txt",
    "bootstrap_variation_selector_2026-07-18/SHA256SUMS.txt",
    "copresence_causal_accessibility_selector_2026-07-19/SHA256SUMS.txt",
}
EXPECTED_BUNDLE_HASHES = {
    "report": "060e76be7ffe18f43752f5d228fa341715c830edd0da25ee03c10279b9af49b5",
    "status": "0ae5dfefddd462ec99a849d18e6b3e70abaafce2b26f0de3a5ced1444f46507d",
    "reclass": "08af08a282c1a2a46d06c555322c064e72afb5d759241630e169236fdce45a75",
    "taxonomy": "d4829b829c30fef30323c1b836ad7faab8e677546bc511266f2377e47d782c3a",
    "premises": "4de45b80bfd065dd89f16ddf181406d2268b89630c4e4256910d6b0493b435d1",
    "crosswalk": "c58c43351e9415d5d475b8837c7cc4157094d1149adacd11de7dd7f7e59f416d",
}
EXPECTED_CORRECTION_SHA256 = "21a2720348a1c0ea737894a49576fa36aafa5a8291e573d0d2a589535cee49d6"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def rows_sha(data: list[dict[str, str]]) -> str:
    encoded = json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return text_sha(encoded)


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def check(name: str, condition: bool, out: dict[str, bool]) -> None:
    out[name] = bool(condition)
    if not condition:
        raise AssertionError(name)


def contains(text: str, phrase: str) -> bool:
    pattern = r"\s+".join(re.escape(word) for word in phrase.split())
    return re.search(pattern, text) is not None


def replay_manifest(path: Path, corrupt_entry: bool = False) -> int:
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        expected, relative = line.split("  ", 1)
        observed = sha(path.parent / relative)
        if corrupt_entry and count == 0:
            observed = "0" * 64
        if observed != expected:
            raise ValueError(f"source manifest replay drift: {path.parent.name}/{relative}")
        count += 1
    if count == 0:
        raise ValueError(f"empty source manifest: {path}")
    return count


def validate_sources(corrupt: str | None = None) -> None:
    for index, (relative, expected) in enumerate(SOURCE_HASHES.items()):
        observed = sha(REPO / relative)
        if corrupt == "manifest_hash" and index == 0:
            observed = "0" * 64
        if observed != expected:
            raise ValueError(f"source hash drift: {relative}")
    replayed = 0
    for index, relative in enumerate(sorted(MANIFEST_SOURCES)):
        replayed += replay_manifest(REPO / relative, corrupt_entry=corrupt == "manifest_entry" and index == 0)
    if replayed != 36:
        raise ValueError(f"source manifest entry-count drift: {replayed}")


def validate_crosswalk_sources(crosswalk: list[dict[str, str]]) -> None:
    cache: dict[str, dict[str, str]] = {}
    for row in crosswalk:
        source = row["source_artifact"]
        record = row["source_record"]
        expected_status = row["exact_source_status"]
        if source.endswith("STATUS_LEDGER.tsv"):
            if source not in cache:
                source_rows = rows(REPO / source)
                key = "id" if "id" in source_rows[0] else "claim_id"
                cache[source] = {item[key]: item["status"] for item in source_rows}
            if cache[source].get(record) != expected_status:
                raise ValueError(f"crosswalk source-status drift: {source}:{record}")
        elif row["crosswalk_id"] == "S36":
            source_text = (REPO / source).read_text(encoding="utf-8")
            if "| Common-Scale Neutrality | `FOUNDING` |" not in source_text or expected_status != "FOUNDING":
                raise ValueError("CSN founding source drift")
        elif row["crosswalk_id"] == "S37":
            payload = json.loads((REPO / source).read_text(encoding="utf-8"))
            actual = payload["tests"]["T5_covariance_field_census"]["illustrative_4D_bulk_witness"]["classification"]
            if actual != expected_status:
                raise ValueError("existence-witness source drift")
        else:
            raise ValueError(f"unhandled crosswalk source: {row['crosswalk_id']}")


def validate_bundle(bundle: dict, *, enforce_hash: bool = True) -> None:
    payload = bundle["payload"]
    report = bundle["report"]
    status = bundle["status"]
    reclass = bundle["reclass"]
    taxonomy = bundle["taxonomy"]
    premises = bundle["premises"]
    crosswalk = bundle["crosswalk"]

    observed_bundle_hashes = {
        "report": text_sha(report),
        "status": rows_sha(status),
        "reclass": rows_sha(reclass),
        "taxonomy": rows_sha(taxonomy),
        "premises": rows_sha(premises),
        "crosswalk": rows_sha(crosswalk),
    }
    if enforce_hash and observed_bundle_hashes != EXPECTED_BUNDLE_HASHES:
        raise ValueError("semantic bundle byte/field drift")
    if sha(HERE / "POST_PREREG_SEMANTIC_CORRECTION.md") != EXPECTED_CORRECTION_SHA256:
        raise ValueError("post-prereg semantic correction drift")

    if payload.get("schema") != "udt-copresence-gr-constraint-regrade-v1":
        raise ValueError("result schema drift")
    if payload.get("date") != "2026-07-19":
        raise ValueError("result date drift")
    if payload.get("scope") != "constraint-role and provenance regrade; no concrete GR constraint adopted":
        raise ValueError("result scope drift")
    if payload.get("versions") != {"python": "3.10.12", "sympy": "1.13.1"}:
        raise ValueError("result runtime-version drift")
    if payload.get("outcome") != OUTCOME:
        raise ValueError("outcome drift")
    if payload.get("maximum_conclusion") != "RECLASSIFICATION_OVERLAY_ONLY":
        raise ValueError("maximum conclusion drift")
    if payload.get("role_counts") != {
        "RETAINED": 11,
        "RECLASSIFIED_CONDITIONAL": 4,
        "OPEN": 7,
        "REJECTED_AS_INFERENCE": 5,
    }:
        raise ValueError("role count drift")

    expected_classification = {
        "prior_gr_constraint_algebra": "RETAINED",
        "prior_paired_top_level": "RETAINED_BOTH_CONDITIONALLY_ADMISSIBLE",
        "bootstrap_whole_solution_role": "RETAINED_AND_CLARIFIED_ON_SHELL_ADMISSIBILITY",
        "hamiltonian_momentum_constraints": "PARENT_EQUATION_AND_FOLIATION_CONDITIONAL_NOT_NATIVE",
        "lapse": "FORMAL_MULTIPLIER_EXAMPLE_NOT_NATIVE_ONTOLOGY",
        "shift": "OPEN_NATIVE_ONTOLOGY_AND_DETAILED_ROLE_NOT_DERIVED_HERE",
        "constraint_propagation": "OPEN_REQUIRES_LOCAL_DYNAMICS_AND_DATA",
        "copresence_as_propagation_mechanism": "REJECTED_AS_INFERENCE",
        "field_census_selection": "OPEN_NOT_SELECTED",
        "action_selection": "OPEN_NOT_SELECTED",
        "physical_calibration": "OPEN_REQUIRES_REPRESENTATIVE_AND_MATERIAL_RULES",
        "same_copresence_countermodels": "DERIVED_NONSELECTION_OF_CONSTRAINT_LAW",
    }
    if payload.get("classification") != expected_classification:
        raise ValueError("classification drift")

    expected_derived = {
        "boosted_hamiltonian_like_projection": "sinh(zeta)**2",
        "boosted_momentum_like_projection": "sinh(2*zeta)/2",
        "boundary_momentum": "lambda + qprime",
        "finite_penalty_residual": "-1/(alpha + 1)",
        "lapse_multiplier_equation": "-p**2/2 - q**2/2 + 1/2",
        "metric_only_predicate_residual": "-1",
        "metric_only_root": ["0", "0"],
        "multiplier_root": ["1/2", "1/2", "-1"],
        "noether_identity": "0",
        "propagated_constraint": "u0 - v0",
        "restricted_root": "1/2",
        "unpropagated_constraint": "a*t - b*t + u0 - v0",
        "whole_history_coefficients": ["a - b", "u0 - v0"],
    }
    if payload.get("derived") != expected_derived:
        raise ValueError("derived field drift")

    expected_check_keys = {
        "after_solution_predicate_not_automatically_satisfied",
        "aligned_constraint_root_exact",
        "boosted_frame_orthogonal",
        "boosted_normal_unit_timelike",
        "boosted_tangent_unit_spacelike",
        "complete_tensor_zero_implies_all_projections_zero",
        "finite_noether_identity",
        "finite_penalty_constraint_residual_nonzero",
        "finite_penalty_root_exact",
        "lapse_adds_p_reaction",
        "lapse_adds_q_reaction",
        "lapse_variation_imposes_constraint",
        "momentum_projection_slice_dependent",
        "multiplier_changes_boundary_momentum",
        "multiplier_reaction_nonzero",
        "noether_equations_not_each_identity",
        "normal_projection_nonzero_in_boosted_slice",
        "normal_projection_slice_dependent",
        "normal_projection_vanishes_in_reference_slice",
        "paired_dynamics_propagates_constraint",
        "restricted_tangent_root_exact",
        "same_background_allows_distinct_parent_tensor_projections",
        "same_copresence_domain_allows_distinct_constraint_propagation",
        "unpaired_dynamics_constraint_drift",
        "unrestricted_root_exact",
        "varied_multiplier_root_exact",
        "whole_history_admissibility_requires_two_conditions",
        "zero_initial_constraint_not_sufficient_without_propagation_law",
        "zero_initial_constraint_propagates_under_paired_dynamics",
    }
    observed_checks = payload.get("exact_checks", {}).get("checks", {})
    if (
        set(observed_checks) != expected_check_keys
        or not all(value is True for value in observed_checks.values())
        or payload["exact_checks"].get("passed") != 29
        or payload["exact_checks"].get("total") != 29
    ):
        raise ValueError("exact check set drift")

    expected_statuses = {
        **{f"G{number:02d}": "RETAINED" for number in range(1, 9)},
        **{f"G{number:02d}": "RECLASSIFIED_CONDITIONAL" for number in range(9, 13)},
        "G13": "OPEN",
        "G14": "RETAINED",
        **{f"G{number:02d}": "OPEN" for number in range(15, 20)},
        **{f"G{number:02d}": "REJECTED_AS_INFERENCE" for number in range(20, 25)},
        "G25": "RETAINED",
        "G26": "OPEN",
        "G27": "RETAINED",
    }
    status_map = {row["claim_id"]: row["status"] for row in status}
    if len(status) != 27 or status_map != expected_statuses:
        raise ValueError("status ledger drift")
    status_claims = {row["claim_id"]: row["claim"] for row in status}
    if status_claims.get("G10") != "Hamiltonian_like_equation_is_a_parent_and_foliation_conditional_projection":
        raise ValueError("Hamiltonian-like claim drift")
    if status_claims.get("G27") != "hard_substitution_is_not_unrestricted_parent_variation":
        raise ValueError("hard-substitution claim drift")

    expected_reclass = {
        **{f"R{number:02d}": "RETAINED" for number in range(1, 9)},
        **{f"R{number:02d}": "RECLASSIFIED_CONDITIONAL" for number in range(9, 13)},
        "R13": "OPEN",
        "R14": "RETAINED",
        **{f"R{number:02d}": "OPEN" for number in range(15, 20)},
        **{f"R{number:02d}": "REJECTED_AS_INFERENCE" for number in range(20, 25)},
        "R25": "RETAINED",
        "R26": "OPEN",
        "R27": "RETAINED",
    }
    reclass_map = {row["item_id"]: row["overlay_disposition"] for row in reclass}
    if len(reclass) != 27 or reclass_map != expected_reclass:
        raise ValueError("reclassification table drift")

    expected_reclass_roles = {
        "R01": "VARIED_MULTIPLIER_CONSTRAINT",
        "R02": "CATEGORY_A_EXISTENCE_WITNESS",
        "R03": "SOFT_PENALTY_APPROXIMATION",
        "R04": "NOETHER_IDENTITY",
        "R05": "BOUNDARY_DIFFERENTIABILITY_CONDITION",
        "R06": "FIELD_CENSUS_OR_ONTOLOGY",
        "R07": "WHOLE_SOLUTION_ADMISSIBILITY",
        "R08": "SPACETIME_DOMAIN_ONTOLOGY",
        "R09": "SYMMETRY_PREMISE",
        "R10": "FOLIATION_PROJECTED_EQUATION",
        "R11": "FOLIATION_PROJECTED_EQUATION",
        "R12": "VARIED_MULTIPLIER_CONSTRAINT",
        "R13": "FIELD_CENSUS_OR_ONTOLOGY",
        "R14": "KINEMATIC_OR_SCALING_SELECTOR",
        "R15": "PARENT_DYNAMICAL_LAW_OR_ACTION_BRIDGE",
        "R16": "FIELD_CENSUS_OR_ONTOLOGY",
        "R17": "INITIAL_DATA_CONSTRAINT",
        "R18": "WHOLE_SOLUTION_SELECTION_MAP",
        "R19": "MATERIAL_CAUSAL_RESPONSE_CONDITION",
        "R20": "INITIAL_DATA_CONSTRAINT",
        "R21": "FOLIATION_PROJECTED_EQUATION",
        "R22": "FIELD_CENSUS_OR_ONTOLOGY",
        "R23": "FOLIATION_PROJECTED_EQUATION",
        "R24": "PARENT_DYNAMICAL_LAW_OR_ACTION_BRIDGE",
        "R25": "KINEMATIC_OR_SCALING_SELECTOR",
        "R26": "REPRESENTATIVE_CALIBRATION_RULE",
        "R27": "RESTRICTED_VARIATION_DOMAIN",
    }
    observed_reclass_roles = {row["item_id"]: row["role_under_copresence"] for row in reclass}
    if observed_reclass_roles != expected_reclass_roles:
        raise ValueError("reclassification role drift")
    r10 = next(row for row in reclass if row["item_id"] == "R10")
    if r10["co_presence_effect"] != "co_presence_does_not_make_projection_native_or_initial_data":
        raise ValueError("Hamiltonian-like co-presence effect drift")

    expected_roles = {
        "T01": "WHOLE_SOLUTION_ADMISSIBILITY",
        "T02": "VARIED_MULTIPLIER_CONSTRAINT",
        "T03": "RESTRICTED_VARIATION_DOMAIN",
        "T04": "SOFT_PENALTY_APPROXIMATION",
        "T05": "NOETHER_IDENTITY",
        "T06": "SYMMETRY_PREMISE",
        "T07": "FOLIATION_PROJECTED_EQUATION",
        "T08": "INITIAL_DATA_CONSTRAINT",
        "T09": "BOUNDARY_DIFFERENTIABILITY_CONDITION",
        "T10": "MATERIAL_CAUSAL_RESPONSE_CONDITION",
        "T11": "SPACETIME_DOMAIN_ONTOLOGY",
        "T12": "FIELD_CENSUS_OR_ONTOLOGY",
        "T13": "REPRESENTATIVE_CALIBRATION_RULE",
        "T14": "PARENT_DYNAMICAL_LAW_OR_ACTION_BRIDGE",
        "T15": "DECLARED_FIELD_VARIATION_RULE",
        "T16": "KINEMATIC_OR_SCALING_SELECTOR",
        "T17": "WHOLE_SOLUTION_SELECTION_MAP",
        "T18": "CATEGORY_A_EXISTENCE_WITNESS",
    }
    if len(taxonomy) != 18 or {row["role_id"]: row["role"] for row in taxonomy} != expected_roles:
        raise ValueError("role taxonomy drift")

    expected_reclass_columns = {
        "item_id",
        "prior_item",
        "source_artifact",
        "source_record",
        "scientific_status",
        "operator_provenance",
        "role_under_copresence",
        "prerequisites",
        "co_presence_effect",
        "overlay_disposition",
        "remaining_scope",
        "future_gate",
    }
    if set(reclass[0]) != expected_reclass_columns:
        raise ValueError("reclassification schema drift")
    if len(crosswalk) != 37 or {row["crosswalk_id"] for row in crosswalk} != {f"S{number:02d}" for number in range(1, 38)}:
        raise ValueError("source crosswalk coverage drift")
    validate_crosswalk_sources(crosswalk)

    expected_premises = {
        "P01": "WORKING",
        "P02": "DERIVED_CONDITIONAL",
        "P03": "INHERITED",
        "P04": "CANONIZED_BINDING",
        "P05": "TRIAL_CONDITIONAL",
        "P06": "NOT_ASSUMED",
        "P07": "COMPARISON_FORMALISM_ONLY_NO_SHIFT_ANCHOR",
        "P08": "WORKING_ON_SHELL",
        "P09": "CATEGORY_A_MATHEMATICS",
        "P10": "OPEN_REQUIRES_DYNAMICS",
        "P11": "NOT_ADOPTED",
        "P12": "BINDING",
    }
    if len(premises) != 12 or {row["premise_id"]: row["status"] for row in premises} != expected_premises:
        raise ValueError("premise ledger drift")

    required_phrases = [
        "The word “constraint” was carrying too many meanings",
        "Whole-solution admissibility",
        "A Noether identity is not a new constraint law",
        "Hamiltonian and momentum constraints are conditional projections",
        "Co-presence does not propagate constraints",
        "A lapse-like multiplier is formal; shift remains uninstantiated",
        "whole completed history",
        "physical clock/ruler calibration remains open",
        "standalone ADM constraints are native UDT laws",
        "No concrete GR constraint has been adopted",
        "A projected equation is also not automatically an initial-data constraint",
        "same co-present event domain but have different constraint propagation laws",
        "REFUTED_GENERICALLY",
        "ON_SHELL_CLOSURE_OR_ADMISSIBILITY",
        "The reaction vector at the constrained root is `(-1,-1)`",
    ]
    for phrase in required_phrases:
        if not contains(report, phrase):
            raise ValueError(f"missing report disclosure: {phrase}")

    required_formulas = [
        r"\mathcal B[S]=0",
        r"I_{\rm aug}=I_0+\eta\mathcal B",
        r"H(\zeta)=n^TEn=\sinh^2\zeta",
        r"M(\zeta)=n^TEs=\sinh\zeta\cosh\zeta",
        r"C(t)=u_0-v_0+(a-b)t",
        r"C=-\frac{1}{\alpha+1}\ne0",
        r"\frac{\partial L}{\partial q'}=q'+\lambda",
    ]
    for formula in required_formulas:
        if not contains(report, formula):
            raise ValueError(f"missing report formula: {formula}")

    forbidden_report_phrases = {
        "Co-presence uniquely selects native ADM constraints",
        "Adopt GR spatial infinity and ADM charge as native boundary input",
    }
    for phrase in forbidden_report_phrases:
        if contains(report, phrase):
            raise ValueError(f"forbidden report promotion: {phrase}")


def expect_rejection(name: str, bundle: dict, mutate, catches: dict[str, bool]) -> None:
    candidate = copy.deepcopy(bundle)
    mutate(candidate)
    rejected = False
    try:
        validate_bundle(candidate, enforce_hash=False)
    except (ValueError, KeyError):
        rejected = True
    check(name, rejected, catches)


def main() -> None:
    exact: dict[str, bool] = {}
    catches: dict[str, bool] = {}
    bundle = {
        "payload": json.loads(RESULT_PATH.read_text(encoding="utf-8")),
        "report": (HERE / "DERIVATION_REPORT.md").read_text(encoding="utf-8"),
        "status": rows(HERE / "STATUS_LEDGER.tsv"),
        "reclass": rows(HERE / "RECLASSIFICATION_TABLE.tsv"),
        "taxonomy": rows(HERE / "ROLE_TAXONOMY.tsv"),
        "premises": rows(HERE / "PREMISE_LEDGER.tsv"),
        "crosswalk": rows(HERE / "SOURCE_CONCLUSION_CROSSWALK.tsv"),
    }
    validate_sources()
    validate_bundle(bundle)
    check("source_hashes_match", True, exact)
    check("semantic_bundle_baseline", True, exact)
    check("post_prereg_semantic_correction_bound", sha(HERE / "POST_PREREG_SEMANTIC_CORRECTION.md") == EXPECTED_CORRECTION_SHA256, exact)
    check("pinned_sympy_version", sp.__version__ == "1.13.1", exact)

    # Independent multiplier solve using a linear KKT matrix.
    kkt = sp.Matrix([[2, 0, 1], [0, 2, 1], [1, 1, 0]])
    rhs = sp.Matrix([0, 0, 1])
    kkt_root = kkt.inv() * rhs
    check("independent_multiplier_root", kkt_root == sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2), -1]), exact)

    # Independent penalty solve and residual.
    alpha = sp.symbols("alpha", positive=True, finite=True)
    penalty_matrix = sp.Matrix([[2 + alpha, alpha], [alpha, 2 + alpha]])
    penalty_rhs = sp.Matrix([alpha, alpha])
    penalty_root = sp.simplify(penalty_matrix.inv() * penalty_rhs)
    expected_penalty_root = sp.Matrix([alpha / (2 * (alpha + 1)), alpha / (2 * (alpha + 1))])
    check(
        "independent_penalty_root",
        all(sp.simplify(penalty_root[index] - expected_penalty_root[index]) == 0 for index in range(2)),
        exact,
    )
    check("independent_penalty_residual", sp.simplify(sum(penalty_root) - 1) == -1 / (alpha + 1), exact)

    # Independent frame projection and invariants.
    zeta = sp.symbols("zeta", real=True)
    metric = sp.diag(-1, 1)
    n = sp.Matrix([sp.cosh(zeta), sp.sinh(zeta)])
    s = sp.Matrix([sp.sinh(zeta), sp.cosh(zeta)])
    tensor = sp.diag(0, 1)
    check("independent_frame_norms", sp.simplify((n.T * metric * n)[0] + 1) == 0 and sp.simplify((s.T * metric * s)[0] - 1) == 0, exact)
    check("independent_frame_orthogonality", sp.simplify((n.T * metric * s)[0]) == 0, exact)
    h = sp.simplify((n.T * tensor * n)[0])
    m = sp.simplify((n.T * tensor * s)[0])
    check("independent_slice_projection_H", h == sp.sinh(zeta) ** 2, exact)
    check("independent_slice_projection_M", sp.simplify(m - sp.sinh(zeta) * sp.cosh(zeta)) == 0, exact)
    check("independent_reference_slice_false_completion", h.subs(zeta, 0) == 0 and tensor != sp.zeros(2), exact)
    check("independent_same_background_distinct_projection_laws", tensor != sp.zeros(2) and h != 0, exact)

    # Independent propagation comparison.
    t, u0, v0, a, b = sp.symbols("t u0 v0 a b", real=True)
    paired = sp.expand((u0 + a * t) - (v0 + a * t))
    unpaired = sp.expand((u0 + a * t) - (v0 + b * t))
    check("independent_paired_propagation", paired == u0 - v0, exact)
    check("independent_unpaired_drift", sp.diff(unpaired, t) == a - b, exact)
    check("independent_whole_history_coefficients", sp.Poly(unpaired, t).all_coeffs() == [a - b, u0 - v0], exact)
    check("independent_same_domain_distinct_propagation_laws", sp.simplify(unpaired - paired) == t * (a - b), exact)

    # Independent Noether, canonical multiplier, and boundary anchors.
    u, v = sp.symbols("u v", real=True)
    gauge = (u - v) ** 2
    check("independent_noether_identity", sp.simplify(sp.diff(gauge, u) + sp.diff(gauge, v)) == 0, exact)
    p, q, lapse, qdot = sp.symbols("p q N qdot", real=True)
    h_constraint = (p**2 + q**2 - 1) / 2
    lagrangian = p * qdot - lapse * h_constraint
    check("independent_lapse_equation", sp.diff(lagrangian, lapse) == -h_constraint, exact)
    qprime, lam = sp.symbols("qprime lambda", real=True)
    check("independent_boundary_momentum", sp.diff(qprime**2 / 2 + lam * qprime, qprime) == qprime + lam, exact)

    # CPU/import provenance.
    allowed = {"__future__", "ast", "copy", "csv", "hashlib", "json", "pathlib", "platform", "re", "sympy"}
    for name in ("derive_copresence_gr_constraint_regrade.py", "verify_copresence_gr_constraint_regrade.py"):
        tree = ast.parse((HERE / name).read_text(encoding="utf-8"))
        imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        check(f"allowed_imports_{name}", imports <= allowed, exact)
        check(f"no_gpu_imports_{name}", not ({"torch", "cupy", "jax", "tensorflow"} & imports), exact)

    # Exercised semantic/structured catches.
    expect_rejection("catch_outcome_promotion", bundle, lambda b: b["payload"].__setitem__("outcome", "COPRESENCE_SELECTS_GR_HAMILTONIAN_AND_MOMENTUM_CONSTRAINTS_AS_NATIVE"), catches)
    expect_rejection("catch_result_schema_drift", bundle, lambda b: b["payload"].__setitem__("schema", "udt-unbound"), catches)
    expect_rejection("catch_result_date_drift", bundle, lambda b: b["payload"].__setitem__("date", "2026-07-20"), catches)
    expect_rejection("catch_result_scope_promotion", bundle, lambda b: b["payload"].__setitem__("scope", "native ADM adoption"), catches)
    expect_rejection("catch_result_python_version_drift", bundle, lambda b: b["payload"]["versions"].__setitem__("python", "0.0"), catches)
    expect_rejection("catch_result_sympy_version_drift", bundle, lambda b: b["payload"]["versions"].__setitem__("sympy", "0.0"), catches)
    expect_rejection("catch_derived_projection_corruption", bundle, lambda b: b["payload"]["derived"].__setitem__("boosted_hamiltonian_like_projection", "0"), catches)
    expect_rejection("catch_missing_exact_check", bundle, lambda b: b["payload"]["exact_checks"]["checks"].pop("normal_projection_slice_dependent"), catches)
    expect_rejection("catch_role_conflation", bundle, lambda b: next(row for row in b["reclass"] if row["item_id"] == "R10").__setitem__("role_under_copresence", "WHOLE_SOLUTION_ADMISSIBILITY"), catches)
    expect_rejection("catch_native_claim_rename", bundle, lambda b: next(row for row in b["status"] if row["claim_id"] == "G10").__setitem__("claim", "GR_Hamiltonian_constraint_is_native_UDT_law"), catches)
    expect_rejection("catch_native_surviving_content", bundle, lambda b: next(row for row in b["reclass"] if row["item_id"] == "R10").__setitem__("co_presence_effect", "standalone_ADM_is_native"), catches)
    expect_rejection("catch_contradictory_report_append", bundle, lambda b: b.__setitem__("report", b["report"] + "\nCo-presence uniquely selects native ADM constraints.\n"), catches)
    expect_rejection("catch_ADM_native_promotion", bundle, lambda b: next(row for row in b["status"] if row["claim_id"] == "G21").__setitem__("status", "RETAINED"), catches)
    expect_rejection("catch_lapse_native_promotion", bundle, lambda b: next(row for row in b["status"] if row["claim_id"] == "G22").__setitem__("status", "RETAINED"), catches)
    expect_rejection("catch_shift_role_promotion", bundle, lambda b: next(row for row in b["status"] if row["claim_id"] == "G13").__setitem__("status", "DERIVED"), catches)
    expect_rejection("catch_projection_invariance_promotion", bundle, lambda b: next(row for row in b["status"] if row["claim_id"] == "G23").__setitem__("status", "DERIVED"), catches)
    expect_rejection("catch_propagation_without_dynamics", bundle, lambda b: next(row for row in b["status"] if row["claim_id"] == "G17").__setitem__("status", "DERIVED"), catches)
    expect_rejection("catch_copresence_as_propagator", bundle, lambda b: next(row for row in b["status"] if row["claim_id"] == "G20").__setitem__("status", "DERIVED"), catches)
    expect_rejection("catch_noether_as_independent_law", bundle, lambda b: next(row for row in b["reclass"] if row["item_id"] == "R04").__setitem__("role_under_copresence", "VARIED_MULTIPLIER_CONSTRAINT"), catches)
    expect_rejection("catch_predicate_multiplier_conflation", bundle, lambda b: next(row for row in b["reclass"] if row["item_id"] == "R07").__setitem__("role_under_copresence", "VARIED_MULTIPLIER_CONSTRAINT"), catches)
    expect_rejection("catch_penalty_as_restricted_variation", bundle, lambda b: next(row for row in b["reclass"] if row["item_id"] == "R03").__setitem__("role_under_copresence", "RESTRICTED_VARIATION_DOMAIN"), catches)
    expect_rejection("catch_covariance_as_noether_identity", bundle, lambda b: next(row for row in b["reclass"] if row["item_id"] == "R09").__setitem__("role_under_copresence", "NOETHER_IDENTITY"), catches)
    expect_rejection("catch_CSN_as_foliation_projection", bundle, lambda b: next(row for row in b["reclass"] if row["item_id"] == "R14").__setitem__("role_under_copresence", "FOLIATION_PROJECTED_EQUATION"), catches)
    expect_rejection("catch_finite_cell_as_boundary_condition", bundle, lambda b: next(row for row in b["reclass"] if row["item_id"] == "R08").__setitem__("role_under_copresence", "BOUNDARY_DIFFERENTIABILITY_CONDITION"), catches)
    expect_rejection("catch_selection_map_as_predicate", bundle, lambda b: next(row for row in b["reclass"] if row["item_id"] == "R18").__setitem__("role_under_copresence", "WHOLE_SOLUTION_ADMISSIBILITY"), catches)
    expect_rejection("catch_parent_law_as_constraint", bundle, lambda b: next(row for row in b["reclass"] if row["item_id"] == "R15").__setitem__("role_under_copresence", "VARIED_MULTIPLIER_CONSTRAINT"), catches)
    expect_rejection("catch_field_census_as_constraint", bundle, lambda b: next(row for row in b["reclass"] if row["item_id"] == "R16").__setitem__("role_under_copresence", "VARIED_MULTIPLIER_CONSTRAINT"), catches)
    expect_rejection("catch_action_selector_as_constraint", bundle, lambda b: next(row for row in b["reclass"] if row["item_id"] == "R24").__setitem__("role_under_copresence", "WHOLE_SOLUTION_ADMISSIBILITY"), catches)
    expect_rejection("catch_missing_hard_substitution_row", bundle, lambda b: b["reclass"].__setitem__(slice(None), [row for row in b["reclass"] if row["item_id"] != "R27"]), catches)
    expect_rejection("catch_field_census_promotion", bundle, lambda b: next(row for row in b["status"] if row["claim_id"] == "G16").__setitem__("status", "DERIVED"), catches)
    expect_rejection("catch_action_bridge_promotion", bundle, lambda b: next(row for row in b["status"] if row["claim_id"] == "G24").__setitem__("status", "DERIVED"), catches)
    expect_rejection("catch_finite_cell_demotion", bundle, lambda b: next(row for row in b["status"] if row["claim_id"] == "G08").__setitem__("status", "OPEN"), catches)
    expect_rejection("catch_missing_status_row", bundle, lambda b: b["status"].pop(), catches)
    expect_rejection("catch_duplicate_reclass_row", bundle, lambda b: b["reclass"].append(copy.deepcopy(b["reclass"][0])), catches)
    expect_rejection("catch_taxonomy_role_loss", bundle, lambda b: b["taxonomy"].pop(), catches)
    expect_rejection("catch_premise_parent_equation_assumed", bundle, lambda b: next(row for row in b["premises"] if row["premise_id"] == "P06").__setitem__("status", "DERIVED"), catches)
    expect_rejection("catch_report_projection_formula_corruption", bundle, lambda b: b.__setitem__("report", b["report"].replace(r"H(\zeta)=n^TEn=\sinh^2\zeta", r"H(\zeta)=0", 1)), catches)
    expect_rejection("catch_report_penalty_exact_promotion", bundle, lambda b: b.__setitem__("report", b["report"].replace(r"C=-\frac{1}{\alpha+1}\ne0", r"C=0", 1)), catches)
    expect_rejection("catch_report_boundary_term_drop", bundle, lambda b: b.__setitem__("report", b["report"].replace(r"\frac{\partial L}{\partial q'}=q'+\lambda", r"\frac{\partial L}{\partial q'}=q'", 1)), catches)
    expect_rejection("catch_multiplier_reaction_drop", bundle, lambda b: b.__setitem__("report", b["report"].replace("The reaction vector at the constrained root is `(-1,-1)`.", "The reaction vector is omitted.", 1)), catches)
    expect_rejection("catch_GR_asymptotic_boundary_import", bundle, lambda b: b.__setitem__("report", b["report"] + "\nAdopt GR spatial infinity and ADM charge as native boundary input.\n"), catches)
    expect_rejection("catch_crosswalk_status_rewrite", bundle, lambda b: next(row for row in b["crosswalk"] if row["crosswalk_id"] == "S10").__setitem__("exact_source_status", "RETAIN_TRIAL"), catches)
    expect_rejection("catch_crosswalk_row_loss", bundle, lambda b: b["crosswalk"].pop(), catches)

    source_hash_rejected = False
    try:
        validate_sources(corrupt="manifest_hash")
    except ValueError:
        source_hash_rejected = True
    check("catch_source_hash_corruption", source_hash_rejected, catches)
    source_entry_rejected = False
    try:
        validate_sources(corrupt="manifest_entry")
    except ValueError:
        source_entry_rejected = True
    check("catch_source_manifest_entry_corruption", source_entry_rejected, catches)

    output = {
        "schema": "udt-copresence-gr-constraint-regrade-verification-v1",
        "result": "PASS",
        "sympy": sp.__version__,
        "exact_checks": {"passed": sum(exact.values()), "total": len(exact), "checks": exact},
        "catch_proofs": {"passed": sum(catches.values()), "total": len(catches), "checks": catches},
        "source_hashes": SOURCE_HASHES,
        "source_manifest_replay": {"packages": 3, "entries": 36, "result": "PASS"},
        "verified_hashes": {
            "DERIVATION_RESULT.json": sha(RESULT_PATH),
            "DERIVATION_REPORT.md": sha(HERE / "DERIVATION_REPORT.md"),
            "STATUS_LEDGER.tsv": sha(HERE / "STATUS_LEDGER.tsv"),
            "RECLASSIFICATION_TABLE.tsv": sha(HERE / "RECLASSIFICATION_TABLE.tsv"),
            "ROLE_TAXONOMY.tsv": sha(HERE / "ROLE_TAXONOMY.tsv"),
            "PREMISE_LEDGER.tsv": sha(HERE / "PREMISE_LEDGER.tsv"),
            "POST_PREREG_SEMANTIC_CORRECTION.md": sha(HERE / "POST_PREREG_SEMANTIC_CORRECTION.md"),
            "SOURCE_CONCLUSION_CROSSWALK.tsv": sha(HERE / "SOURCE_CONCLUSION_CROSSWALK.tsv"),
            "LAY_DECISION_TREE.md": sha(HERE / "LAY_DECISION_TREE.md"),
            "DERIVATION_TRANSCRIPT.txt": sha(HERE / "DERIVATION_TRANSCRIPT.txt"),
            "PREREGISTRATION.md": sha(HERE / "PREREGISTRATION.md"),
            "derive_copresence_gr_constraint_regrade.py": sha(HERE / "derive_copresence_gr_constraint_regrade.py"),
            "verify_copresence_gr_constraint_regrade.py": sha(HERE / "verify_copresence_gr_constraint_regrade.py"),
            "requirements-cpu.txt": sha(HERE / "requirements-cpu.txt"),
        },
        "gpu_imports": [],
    }
    VERIFY_PATH.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("verification=PASS")
    print(f"exact_checks={sum(exact.values())}/{len(exact)}")
    print(f"catch_proofs={sum(catches.values())}/{len(catches)}")
    print(f"verification_sha256={sha(VERIFY_PATH)}")


if __name__ == "__main__":
    main()
