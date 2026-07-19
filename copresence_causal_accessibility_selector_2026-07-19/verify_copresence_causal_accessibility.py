#!/usr/bin/env python3
"""Independent fail-closed verifier for the co-presence/causal-accessibility package."""

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
RESULT_PATH = HERE / "DERIVATION_RESULT.json"
VERIFY_PATH = HERE / "VERIFICATION_RESULT.json"
OUTCOME = "COPRESENCE_CAUSAL_PARTITION_COHERENT_CONFORMAL_LAYER_DERIVED_ACTION_BRIDGE_OPEN"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name: str, condition: bool, out: dict[str, bool]) -> None:
    out[name] = bool(condition)
    if not condition:
        raise AssertionError(name)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def contains_normalized(text: str, phrase: str) -> bool:
    pattern = r"\s+".join(re.escape(word) for word in phrase.split())
    return re.search(pattern, text) is not None


def validate_semantic_payload(payload: dict, report: str, ledger_rows: list[dict[str, str]]) -> None:
    if payload.get("outcome") != OUTCOME:
        raise ValueError("wrong outcome")
    classifications = payload.get("classification", {})
    required_classifications = {
        "copresence": "WORKING_DEFINITION_SHARED_DOMAIN_OF_ONE_WHOLE_SOLUTION",
        "causal_reachability": "DERIVED_FROM_TIME_ORIENTED_LORENTZIAN_CONFORMAL_CLASS",
        "reciprocal_coordinate_warping": "CONDITIONAL_STATIC_ADAPTED_REPRESENTATIVE",
        "operational_no_signalling": "POSIT_REQUIRES_DYNAMICS_COUPLING_AND_DATA_DOMAIN",
        "source_absorber_relation": "WORKING_CONDITIONAL_ENDPOINT_INTERPRETATION_NOT_PHOTON_ONTOLOGY",
        "pre_post_scale_layering": "COMPATIBLE_ARCHITECTURE_NOT_UNIQUE_BRIDGE",
        "action_selection": "OPEN",
        "physical_calibration": "OPEN_REQUIRES_MATERIAL_TRANSFORMATION_AND_COUPLING",
        "udt_uniqueness": "NOT_ESTABLISHED",
    }
    if classifications != required_classifications:
        raise ValueError("classification drift")

    expected_derived = {
        "conformal_cotangent_factor": "omega**(-2)",
        "conformal_tangent_factor": "omega**2",
        "constant_lapse_static_chart_null_coordinate_time": "L/(c0*n**2)",
        "global_boundary_response": ["1/2", "1/2"],
        "optical_characteristic_speeds": ["-c0", "c0"],
        "optical_coordinate_density": "n**(-2)",
        "reciprocal_coordinate_null_slope": "c0*n**2",
        "shared_characteristic_polynomials": ["q", "q**2"],
        "timelike_null_spacelike_examples": ["-3*L**2", "0", "L**2"],
    }
    if payload.get("derived") != expected_derived:
        raise ValueError("derived field drift")

    expected_terminology = {
        "causal_partition": "LAY_SHORTHAND_FOR_EVENT_RELATIVE_CAUSAL_REACHABILITY_NOT_AN_EQUIVALENCE_PARTITION",
        "time_normalization_convention": "t_prime=t/lambda",
    }
    if payload.get("terminology") != expected_terminology:
        raise ValueError("terminology drift")

    expected_exact_keys = {
        "boundary_retuning_changes_both_components",
        "candidate_star_emission_offset_is_null_related",
        "coordinate_slope_changes_under_time_normalization",
        "derivative_order_not_selected_by_cone",
        "finite_nonzero_static_chart_coordinate_time",
        "general_radial_null_slope",
        "global_constraint_solution_exact",
        "global_member_pair_can_be_null",
        "global_member_pair_can_be_spacelike",
        "global_member_pair_can_be_timelike",
        "ingoing_optical_characteristic",
        "lower_order_dynamics_not_selected_by_cone",
        "nonconstant_lapse_chain_rule_cancellation",
        "optical_wave_principal_part",
        "outgoing_optical_characteristic",
        "positive_conformal_characteristic_identity",
        "positive_conformal_tangent_identity",
        "proper_length_changes_with_representative",
        "proper_time_changes_with_representative",
        "reciprocal_radial_null_slope",
        "second_and_fourth_order_share_characteristic_zero_set_forward",
        "second_and_fourth_order_share_characteristic_zero_set_reverse",
        "star_remote_same_chart_time_is_spacelike",
    }
    exact_payload = payload.get("exact_checks", {})
    exact_map = exact_payload.get("checks", {})
    if (
        set(exact_map) != expected_exact_keys
        or not all(value is True for value in exact_map.values())
        or exact_payload.get("passed") != 23
        or exact_payload.get("total") != 23
    ):
        raise ValueError("derivation exact-check set drift")

    forbidden = set(payload.get("forbidden_inferences", []))
    required_forbidden = {
        "copresence_is_simultaneity",
        "copresence_implies_zero_travel_time",
        "global_boundary_dependence_is_instantaneous_signalling",
        "metric_cone_alone_proves_material_retarded_support",
        "positive_CSN_rescaling_changes_causal_order",
        "conformal_class_alone_fixes_proper_clocks_or_mass",
        "copresence_uniquely_selects_C2_EH_or_two_stage_bridge",
    }
    if forbidden != required_forbidden:
        raise ValueError("forbidden inference disclosure drift")

    required_report_phrases = [
        "not zero-time separation",
        "does not erase the temporal relations",
        "ordinary whole-solution event-domain co-membership",
        "not an equivalence partition",
        "positive common-scale change does not alter who can causally reach whom",
        "not a locally measured variable scalar speed",
        "not correct to say that the detector receives the star's state at the same chosen static-chart time",
        "The null proper time is zero",
        "Electron identity exchange",
        "global retuning",
        "localized intervention comparison",
        "both sides are counterfactual comparisons between solutions",
        "POSIT/CONSISTENCY OBLIGATION",
        "does not uniquely select conditional pre-scale `C^2`/Bach",
        "does not uniquely select conditional post-scale EH",
        "not uniquely derived",
        "not co-presence alone",
        "substrate, and recycling",
    ]
    for phrase in required_report_phrases:
        if not contains_normalized(report, phrase):
            raise ValueError(f"missing disclosure: {phrase}")

    required_report_formulas = [
        r"p\;C_S\;q \quad\Longleftrightarrow\quad p,q\in M_S=\operatorname{dom}(S)",
        r"R_{\rm src}=(t_o,\chi_e)",
        r"d\chi=\frac{dr}{N^2}",
        r"\frac{d\chi}{dt}=\pm c_0",
        r"\Delta t=\frac{1}{c_0}\int\frac{dr}{N^2}=\frac{\Delta\chi}{c_0}",
        r"Q(k)=g^{\mu\nu}k_\mu k_\nu",
    ]
    for formula in required_report_formulas:
        if not contains_normalized(report, formula):
            raise ValueError(f"missing or changed load-bearing formula: {formula}")

    by_id = {row["claim_id"]: row for row in ledger_rows}
    if len(by_id) != 24 or len(ledger_rows) != 24:
        raise ValueError("status ledger identity/count drift")
    exact_statuses = {
        "C01": "WORKING",
        "C02": "DERIVED",
        "C03": "DERIVED",
        "C04": "DERIVED",
        "C05": "DERIVED",
        "C06": "CONDITIONAL",
        "C07": "CONDITIONAL",
        "C08": "CONDITIONAL",
        "C09": "DERIVED",
        "C10": "DERIVED",
        "C11": "DERIVED",
        "C12": "POSIT",
        "C13": "WORKING",
        "C14": "CONDITIONAL",
        "C15": "CONDITIONAL",
        "C16": "DERIVED",
        "C17": "DERIVED",
        "C18": "CONDITIONAL",
        "C19": "REJECTED_AS_INFERENCE",
        "C20": "REJECTED_AS_INFERENCE",
        "C21": "REJECTED_AS_INFERENCE",
        "C22": "REJECTED_AS_INFERENCE",
        "C23": "OPEN",
        "C24": "OPEN",
    }
    if {key: by_id[key]["status"] for key in sorted(by_id)} != exact_statuses:
        raise ValueError("status ledger promotion or drift")


def validate_auxiliary(lay: str, premise_rows: list[dict[str, str]], transcript: str) -> None:
    required_lay = [
        "ordinary whole-solution co-membership, not yet a UDT selector",
        "**if** the physical signal follows the metric-null characteristic",
        "this calculation does not make it observable at the detector",
        "The null curve has zero proper time",
        "requires the still-missing matter equation and coupling",
        "partitioned” is lay shorthand for event-relative causal reachability",
    ]
    for phrase in required_lay:
        if not contains_normalized(lay, phrase):
            raise ValueError(f"lay disclosure drift: {phrase}")

    expected_premises = {
        "one_complete_solution_referent": "CHOSE_WORKING",
        "smooth_time_oriented_lorentzian_metric": "CONDITIONAL_PINNED_BY_HABIT",
        "positive_common_scale_factor": "PINNED_BY_THEORY",
        "reciprocal_static_radial_block": "CONDITIONAL",
        "static_flow_and_radial_chart": "PINNED_BY_HABIT",
        "metric_scalar_principal_operator": "IMPORTED_COMPARISON_READOUT",
        "retarded_intervention_rule": "POSIT_CONSISTENCY_OBLIGATION",
        "preferred_foundational_time": "REJECTED_AS_UNREGISTERED",
        "photon_source_absorber_relation": "WORKING_INTERPRETATION",
        "pre_scale_post_scale_hierarchy": "CANDIDATE_ARCHITECTURE",
    }
    observed_premises = {row["premise"]: row["status"] for row in premise_rows}
    if len(premise_rows) != 10 or observed_premises != expected_premises:
        raise ValueError("premise ledger drift")

    if "exact_checks=23/23" not in transcript:
        raise ValueError("transcript check-count drift")
    if f"result_sha256={sha(RESULT_PATH)}" not in transcript:
        raise ValueError("transcript result-hash drift")


def expect_rejection(name: str, payload: dict, report: str, rows: list[dict[str, str]], mutate, out: dict[str, bool]) -> None:
    p = copy.deepcopy(payload)
    r = report
    l = copy.deepcopy(rows)
    p, r, l = mutate(p, r, l)
    rejected = False
    try:
        validate_semantic_payload(p, r, l)
    except (ValueError, KeyError):
        rejected = True
    check(name, rejected, out)


def remove_report_phrase(phrase: str):
    def mutate(payload, report, rows):
        pattern = r"\s+".join(re.escape(word) for word in phrase.split())
        return payload, re.sub(pattern, "REMOVED_DISCLOSURE", report, count=1), rows

    return mutate


def remove_forbidden(item: str):
    def mutate(payload, report, rows):
        payload["forbidden_inferences"].remove(item)
        return payload, report, rows

    return mutate


def main() -> None:
    exact: dict[str, bool] = {}
    catches: dict[str, bool] = {}
    payload = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
    report = (HERE / "DERIVATION_REPORT.md").read_text(encoding="utf-8")
    ledger_rows = read_tsv(HERE / "STATUS_LEDGER.tsv")
    layer_rows = read_tsv(HERE / "SELECTOR_LAYER_MAP.tsv")
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_DECISION_TREE.md").read_text(encoding="utf-8")
    premise_rows = read_tsv(HERE / "PREMISE_LEDGER.tsv")
    transcript = (HERE / "DERIVATION_TRANSCRIPT.txt").read_text(encoding="utf-8")

    validate_semantic_payload(payload, report, ledger_rows)
    validate_auxiliary(lay, premise_rows, transcript)
    check("semantic_payload_baseline", True, exact)
    check("registered_outcome_present", OUTCOME in prereg, exact)
    correction = (HERE / "POST_PREREG_FORMALIZATION_CORRECTION.md").read_text(encoding="utf-8")
    check("post_prereg_type_correction_present", "p,q\\in M_S=\\operatorname{dom}(S)" in correction, exact)
    check("causal_partition_explicitly_lay_only", "not an equivalence partition" in correction, exact)
    check("result_sympy_pinned", payload["versions"]["sympy"] == "1.13.1", exact)
    check("derivation_all_checks_pass", payload["exact_checks"]["passed"] == payload["exact_checks"]["total"] == 23, exact)
    check(
        "result_status_counts_match_ledger",
        payload["status_counts"]
        == {
            "DERIVED": 9,
            "CONDITIONAL": 6,
            "WORKING": 2,
            "POSIT": 1,
            "OPEN": 2,
            "REJECTED_AS_INFERENCE": 4,
        },
        exact,
    )
    check("five_selector_layers", len(layer_rows) == 5 and len({row["layer"] for row in layer_rows}) == 5, exact)
    check("action_and_bridge_open_in_layer_map", any(row["layer"] == "L3_response_dynamics" and row["status"] == "OPEN" for row in layer_rows), exact)

    # Independent matrix calculation of the conformal and reciprocal claims.
    c, n, omega = sp.symbols("c n Omega", positive=True, finite=True)
    metric = sp.diag(-n**2 * c**2, n**-2)
    metric_tilde = sp.simplify(omega**2 * metric)
    inverse = sp.simplify(metric.inv())
    inverse_tilde = sp.simplify(metric_tilde.inv())
    check("independent_conformal_metric_factor", metric_tilde == omega**2 * metric, exact)
    check("independent_conformal_inverse_factor", inverse_tilde == omega**-2 * inverse, exact)
    check("independent_reciprocal_determinant", sp.simplify(metric.det() + c**2) == 0, exact)

    # Transform r -> chi using dr/dchi=n^2.
    jac = sp.diag(1, n**2)
    optical_metric = sp.simplify(jac.T * metric * jac)
    check("independent_optical_metric", optical_metric == sp.diag(-n**2 * c**2, n**2), exact)
    check("independent_optical_metric_conformal_minkowski", sp.simplify(optical_metric / n**2) == sp.diag(-c**2, 1), exact)

    dt, dr = sp.symbols("dt dr", real=True)
    null_roots = sp.solve(sp.Eq(-n**2 * c**2 * dt**2 + n**-2 * dr**2, 0), dr)
    check("independent_reciprocal_null_roots", set(null_roots) == {-c * dt * n**2, c * dt * n**2}, exact)

    psi_tt, psi_xx = sp.symbols("psi_tt psi_xx", real=True)
    transformed_box = sp.simplify(n**2 * (-psi_tt / (n**2 * c**2) + psi_xx / n**2))
    check("independent_optical_wave_operator", transformed_box == -psi_tt / c**2 + psi_xx, exact)

    radius = sp.symbols("radius", real=True)
    lapse = sp.Function("lapse")(radius)
    chi = sp.Function("chi")(radius)
    field = sp.Function("field")
    radial = sp.diff(lapse**2 * sp.diff(field(chi), radius), radius)
    radial = radial.subs(sp.diff(chi, radius, 2), sp.diff(lapse**-2, radius))
    radial = radial.subs(sp.diff(chi, radius), lapse**-2)
    expected_radial = sp.diff(field(chi), chi, 2) / lapse**2
    check("independent_nonconstant_lapse_chain_rule", sp.simplify(radial - expected_radial) == 0, exact)

    length = sp.symbols("L", positive=True, finite=True)
    check("independent_nonzero_travel_expression", sp.simplify(length / (c * n**2)) != 0, exact)
    intervals = [
        sp.expand(-(c * (2 * length / c)) ** 2 + length**2),
        sp.expand(-(c * (length / c)) ** 2 + length**2),
        length**2,
    ]
    check("independent_three_causal_classes", intervals == [-3 * length**2, 0, length**2], exact)

    matrix = sp.Matrix([[1, 1], [1, -1]])
    check("independent_global_constraint_response", matrix.inv()[:, 0] == sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2)]), exact)

    kt, kr = sp.symbols("kt kr", real=True)
    q = -kt**2 / c**2 + kr**2
    q_value = sp.symbols("q_value", real=True)
    check(
        "independent_Q_and_Q2_same_real_zero_set",
        set(sp.solve(sp.Eq(q_value, 0), q_value))
        == set(sp.solve(sp.Eq(q_value**2, 0), q_value))
        == {sp.Integer(0)},
        exact,
    )
    check("independent_Q_and_Q2_different_degree", sp.Poly(q**2, kt, kr).total_degree() == 4 and sp.Poly(q, kt, kr).total_degree() == 2, exact)
    m2 = sp.symbols("m2", real=True)
    polynomial_q = sp.Poly(q, kt, kr)
    polynomial_massive = sp.Poly(q + m2, kt, kr)
    top_q = sum(
        coefficient * kt**powers[0] * kr**powers[1]
        for powers, coefficient in polynomial_q.terms()
        if sum(powers) == polynomial_q.total_degree()
    )
    top_massive = sum(
        coefficient * kt**powers[0] * kr**powers[1]
        for powers, coefficient in polynomial_massive.terms()
        if sum(powers) == polynomial_massive.total_degree()
    )
    check("independent_lower_order_same_principal_homogeneous_part", sp.simplify(top_q - top_massive) == 0, exact)

    # Import provenance: stdlib plus SymPy only; never GPU.
    allowed = {"__future__", "ast", "copy", "csv", "hashlib", "json", "pathlib", "platform", "re", "sympy"}
    for source_name in ["derive_copresence_causal_accessibility.py", "verify_copresence_causal_accessibility.py"]:
        tree = ast.parse((HERE / source_name).read_text(encoding="utf-8"))
        roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                roots.add(node.module.split(".")[0])
        check(f"allowed_imports_{source_name}", roots <= allowed, exact)
        check(f"no_gpu_import_{source_name}", not ({"torch", "cupy", "jax", "tensorflow"} & roots), exact)

    check("status_ledger_24_unique_rows", len(ledger_rows) == len({row["claim_id"] for row in ledger_rows}) == 24, exact)
    check("no_complete_action_promotion", next(row for row in ledger_rows if row["claim_id"] == "C23")["status"] == "OPEN", exact)
    check("no_foundational_infinite_speed_promotion", next(row for row in ledger_rows if row["claim_id"] == "C21")["status"] == "REJECTED_AS_INFERENCE", exact)

    # Exercised catch-proofs.
    for item in payload["forbidden_inferences"]:
        expect_rejection(f"catch_missing_forbidden_{item}", payload, report, ledger_rows, remove_forbidden(item), catches)

    phrases = [
        "not zero-time separation",
        "does not erase the temporal relations",
        "ordinary whole-solution event-domain co-membership",
        "not an equivalence partition",
        "positive common-scale change does not alter who can causally reach whom",
        "not a locally measured variable scalar speed",
        "not correct to say that the detector receives the star's state at the same chosen static-chart time",
        "The null proper time is zero",
        "Electron identity exchange",
        "global retuning",
        "localized intervention comparison",
        "both sides are counterfactual comparisons between solutions",
        "POSIT/CONSISTENCY OBLIGATION",
        "does not uniquely select conditional pre-scale `C^2`/Bach",
        "does not uniquely select conditional post-scale EH",
        "not uniquely derived",
        "not co-presence alone",
        "substrate, and recycling",
    ]
    for index, phrase in enumerate(phrases, start=1):
        expect_rejection(f"catch_missing_disclosure_{index:02d}", payload, report, ledger_rows, remove_report_phrase(phrase), catches)

    def wrong_outcome(p, r, l):
        p["outcome"] = "COPRESENCE_UNIQUELY_SELECTS_UDT_ACTION_AND_BRIDGE"
        return p, r, l

    expect_rejection("catch_unique_action_outcome", payload, report, ledger_rows, wrong_outcome, catches)

    def promote_no_signalling(p, r, l):
        next(row for row in l if row["claim_id"] == "C12")["status"] = "DERIVED"
        return p, r, l

    expect_rejection("catch_no_signalling_promotion", payload, report, ledger_rows, promote_no_signalling, catches)

    def promote_bridge(p, r, l):
        next(row for row in l if row["claim_id"] == "C19")["status"] = "DERIVED"
        return p, r, l

    expect_rejection("catch_bridge_promotion", payload, report, ledger_rows, promote_bridge, catches)

    def delete_status_row(p, r, l):
        return p, r, l[:-1]

    expect_rejection("catch_missing_status_row", payload, report, ledger_rows, delete_status_row, catches)

    def duplicate_status_row(p, r, l):
        return p, r, l + [copy.deepcopy(l[0])]

    expect_rejection("catch_duplicate_status_row", payload, report, ledger_rows, duplicate_status_row, catches)

    def corrupt_derived_optical_density(p, r, l):
        p["derived"]["optical_coordinate_density"] = "1"
        return p, r, l

    expect_rejection(
        "catch_corrupt_derived_optical_density",
        payload,
        report,
        ledger_rows,
        corrupt_derived_optical_density,
        catches,
    )

    def corrupt_report_optical_formula(p, r, l):
        return p, r.replace(r"d\chi=\frac{dr}{N^2}", r"d\chi=\frac{dr}{N^3}", 1), l

    expect_rejection(
        "catch_corrupt_report_optical_formula",
        payload,
        report,
        ledger_rows,
        corrupt_report_optical_formula,
        catches,
    )

    def corrupt_counterfactual_symmetry(p, r, l):
        return p, r.replace(
            "both sides are counterfactual comparisons between solutions",
            "only the first side is a counterfactual comparison between solutions",
            1,
        ), l

    expect_rejection(
        "catch_counterfactual_asymmetry",
        payload,
        report,
        ledger_rows,
        corrupt_counterfactual_symmetry,
        catches,
    )

    lay_conditional = "**if** the physical signal follows the metric-null characteristic"
    lay_pattern = r"\s+".join(re.escape(word) for word in lay_conditional.split())
    bad_lay = re.sub(
        lay_pattern,
        "the physical signal follows the metric-null characteristic",
        lay,
        count=1,
    )
    lay_rejected = False
    try:
        validate_auxiliary(bad_lay, premise_rows, transcript)
    except ValueError:
        lay_rejected = True
    check("catch_unconditional_lay_signal", lay_rejected, catches)

    bad_premises = copy.deepcopy(premise_rows)
    next(row for row in bad_premises if row["premise"] == "metric_scalar_principal_operator")["status"] = "DERIVED"
    premise_rejected = False
    try:
        validate_auxiliary(lay, bad_premises, transcript)
    except ValueError:
        premise_rejected = True
    check("catch_native_scalar_promotion_in_premise_ledger", premise_rejected, catches)

    output = {
        "schema": "udt-copresence-causal-accessibility-verification-v1",
        "result": "PASS",
        "sympy": sp.__version__,
        "exact_checks": {"passed": sum(exact.values()), "total": len(exact), "checks": exact},
        "catch_proofs": {"passed": sum(catches.values()), "total": len(catches), "checks": catches},
        "verified_hashes": {
            "DERIVATION_RESULT.json": sha(RESULT_PATH),
            "DERIVATION_REPORT.md": sha(HERE / "DERIVATION_REPORT.md"),
            "STATUS_LEDGER.tsv": sha(HERE / "STATUS_LEDGER.tsv"),
            "SELECTOR_LAYER_MAP.tsv": sha(HERE / "SELECTOR_LAYER_MAP.tsv"),
            "PREMISE_LEDGER.tsv": sha(HERE / "PREMISE_LEDGER.tsv"),
            "LAY_DECISION_TREE.md": sha(HERE / "LAY_DECISION_TREE.md"),
            "DERIVATION_TRANSCRIPT.txt": sha(HERE / "DERIVATION_TRANSCRIPT.txt"),
            "PREREGISTRATION.md": sha(HERE / "PREREGISTRATION.md"),
            "POST_PREREG_FORMALIZATION_CORRECTION.md": sha(HERE / "POST_PREREG_FORMALIZATION_CORRECTION.md"),
            "derive_copresence_causal_accessibility.py": sha(HERE / "derive_copresence_causal_accessibility.py"),
            "verify_copresence_causal_accessibility.py": sha(HERE / "verify_copresence_causal_accessibility.py"),
            "verify_repository_gates.py": sha(HERE / "verify_repository_gates.py"),
            "requirements-cpu.txt": sha(HERE / "requirements-cpu.txt"),
            "REVIEW_CONCEPTUAL.md": sha(HERE / "REVIEW_CONCEPTUAL.md"),
            "REVIEW_MATH_ACTION.md": sha(HERE / "REVIEW_MATH_ACTION.md"),
            "ADVERSARIAL_AUDIT.md": sha(HERE / "ADVERSARIAL_AUDIT.md"),
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
