#!/usr/bin/env python3
"""Exact native global-coframe construction-law audit.

The algebra is intentionally small and symbolic.  The script characterizes
the surviving construction family and source capabilities; it does not solve
field equations or select a physical branch.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_rule(path: str) -> tuple[str, str, str, str]:
    name = Path(path).name
    if path.startswith("CURRENT_SCIENTIFIC_PREMISES"):
        return (
            "CURRENT_PREMISE_CONTROL", "CONSTRAINS_ONLY", "O01;O02;O10;O11;O12",
            "Controls active status and exclusions; not a construction by itself.",
        )
    if path.startswith("udt_founded_phi_complete_coframe_extension_audit"):
        return (
            "FOUNDED_PAIR_AND_EXTENSION_CLASS", "CONSTRAINS_ONLY", "O01;O02;O06;O11",
            "Fixes the pair action and exhibits residual extension freedom.",
        )
    if path.startswith("udt_complete_coframe_native_selector_audit"):
        return (
            "POINTWISE_SELECTOR_RANK", "CONSTRAINS_ONLY", "O02;O04;O06;O11",
            "Active selector rank is zero in the registered pointwise class.",
        )
    if path.startswith("udt_complete_coframe_physical_comparison_functor_audit"):
        return (
            "FINITE_PATH_FUNCTOR_AND_DESCENT_GATES", "CONDITIONAL_ON_EXTRA_PREMISE", "O02;O04;O05;O07;O11",
            "Arbitrary transported members compose; physical functor and section remain open.",
        )
    if path.startswith("udt_founded_pair_global_alignment_audit"):
        return (
            "LOCAL_PHYSICAL_PAIR_ALIGNMENT", "SUPPLIES", "O01;O02;O03;O04;O06;O11",
            "Sharpens invariant-pair lifts to one screen modulus; global assembly remains open.",
        )
    if path.startswith("udt_covariant_reciprocal_coframe_lift_atlas"):
        return (
            "COVARIANT_LOCAL_LIFT_ATLAS", "CONSTRAINS_ONLY", "O02;O03;O04;O06;O09;O11",
            "Derives the conditional lift family and exact surviving lambda modulus.",
        )
    if path.startswith("udt_founding_observer_comparison_semantics_audit"):
        return (
            "FOUNDING_SEMANTICS", "CONSTRAINS_ONLY", "O04;O05;O07;O11",
            "Derives abstract ordered comparison but selects neither endpoint nor path semantics.",
        )
    if path.startswith("udt_native_reciprocal_comparison_bundle_audit"):
        return (
            "RECIPROCAL_RESPONSE_QUERY_BUNDLE", "SUPPLIES", "O02;O04;O06;O07;O11",
            "Derives the affine response bundle and tensorial transitions; finite lift and section remain open.",
        )
    if path.startswith("udt_observer_pair_path_groupoid_assembly_audit"):
        return (
            "PAIR_PATH_GROUPOID", "CONDITIONAL_ON_EXTRA_PREMISE", "O04;O05;O07;O11",
            "Composition closes for all lambda given additive depth; metric-native depth remains open.",
        )
    if path.startswith("udt_global_reciprocal_bundle_assembly_audit"):
        return (
            "GLOBAL_PAIR_BUNDLE", "CONSTRAINS_ONLY", "O04;O05;O07;O08;O11",
            "Global path-labelled bundle exists; endpoint collapse and signed depth remain unselected.",
        )
    if path.startswith("udt_intrinsic_reciprocal_holonomy_audit"):
        return (
            "HOLONOMY_COUNTERCONTROL", "CONSTRAINS_ONLY", "O04;O07;O08;O11",
            "Full holonomy blocks ordinary endpoint descent on its bounded off-shell control.",
        )
    if path.startswith("udt_complete_nonultrastatic_reciprocal_branch_audit"):
        return (
            "COMPLETE_NONULTRASTATIC_CONFIGURATION_FAMILY", "CONDITIONAL_ON_EXTRA_PREMISE", "O02;O03;O05;O06;O07;O08;O10;O11;O12",
            "Supplies coherent complete off-shell clock-angular counterfamilies but no selected profile, lambda, or equations.",
        )
    if path.startswith("complete_coframe_seal_involution"):
        return (
            "SEAL_LIFT_FAMILY", "CONSTRAINS_ONLY", "O07;O08;O09;O11",
            "Classifies multiple conditional seal lifts without selecting a global completion.",
        )
    if path.startswith("udt_global_metric_assembly_atlas"):
        return (
            "COMPLETION_TAXONOMY", "CONSTRAINS_ONLY", "O07;O08;O09;O11",
            "Registers completion requirements and arithmetic controls, not one selected metric.",
        )
    if path.startswith("udt_finite_cell_cartan_transport_atlas"):
        return (
            "CAUSAL_AND_CARTAN_TRANSITION_ATLAS", "CONSTRAINS_ONLY", "O03;O07;O08;O09",
            "Classifies local causal persistence and degeneration; through-interface law remains open.",
        )
    if path.startswith("udt_complete_branch_founded_pair_pullback_audit"):
        return (
            "COMPLETE_BRANCH_PULLBACK", "CONSTRAINS_ONLY", "O02;O05;O06;O08;O11",
            "Earlier ultrastatic controls fail founded depth; bounded conclusion retained in its source scope.",
        )
    if path.startswith("udt_clock_anchor_scale_threading_audit"):
        return (
            "CLOCK_AND_SCALE_CALIBRATION", "CALIBRATES_ONLY", "O03;O05;O09;O10;O11",
            "Places c_E locally and proves c_E,G_obs do not select dimensionless threading or absolute scale.",
        )
    if path.startswith("udt_common_scale_neutrality_provenance_audit"):
        return (
            "CSN_PRECEDENCE_CORRECTION", "CONFLICTING_OR_SUPERSEDED", "O02;O10;O11",
            "Strong local CSN is inactive; common-factor cancellation is algebra only.",
        )
    if path.startswith("udt_global_coframe_compatibility_p03"):
        return (
            "PRIOR_BOUNDED_SOURCE_GATE", "CONSTRAINS_ONLY", "O02;O05;O07;O08;O09;O11",
            "Exact inside its 57-source freeze, but its repository-wide source completeness requires correction.",
        )
    if path.startswith("udt_full_local_jet_strata_p02"):
        role = "DORMANT_P02_DETAIL" if name in {"STRATUM_LEDGER.tsv", "P02B_CANDIDATE_LEDGER.tsv"} else "DORMANT_P02_AGGREGATE"
        return (
            role, "DOES_NOT_ADDRESS", "O02;O03;O05;O06;O09",
            "Frozen to prevent another projection-source omission; not activated before the definition gate.",
        )
    raise AssertionError(f"no source rule: {path}")


def exact_algebra() -> dict[str, object]:
    phi, psi, lam, R, a, c = sp.symbols("phi psi lambda R a c", real=True)
    eta = sp.diag(-1, 1, 1, 1)

    # Full Lorentz centralizer.
    generators = []
    for i in range(1, 4):
        B = sp.zeros(4); B[0, i] = 1; B[i, 0] = 1; generators.append(B)
    for i, j in ((1, 2), (1, 3), (2, 3)):
        J = sp.zeros(4); J[i, j] = 1; J[j, i] = -1; generators.append(J)
    variables = sp.symbols("x0:16")
    X = sp.Matrix(4, 4, variables)
    equations = []
    for generator in generators:
        equations.extend(list(X * generator - generator * X))
    matrix, _ = sp.linear_eq_to_matrix(equations, variables)
    lorentz_centralizer_nullity = len(variables) - matrix.rank()
    assert lorentz_centralizer_nullity == 1

    # Ordered physical pair, SO(2)-equivariant, metric-self-adjoint lift.
    J23 = sp.zeros(4); J23[2, 3] = 1; J23[3, 2] = -1
    pair_equations = list(X * J23 - J23 * X) + list(X.T * eta - eta * X)
    for i in range(4):
        for j in range(4):
            if i < 2 or j < 2:
                target = -1 if (i, j) == (0, 0) else 1 if (i, j) == (1, 1) else 0
                pair_equations.append(X[i, j] - target)
    pair_matrix, pair_rhs = sp.linear_eq_to_matrix(pair_equations, variables)
    pair_solution = sp.linsolve((pair_matrix, pair_rhs), variables)
    solution_tuple = next(iter(pair_solution))
    free = sorted(set().union(*(entry.free_symbols for entry in solution_tuple)), key=str)
    assert len(free) == 1
    ordered_pair_moduli = 1

    Xlam = sp.diag(-1, 1, lam, lam)
    assert sp.simplify(Xlam.trace() - 2 * lam) == 0
    assert sp.simplify(sp.exp(phi * Xlam[0, 0]) * sp.exp(psi * Xlam[0, 0]) - sp.exp((phi + psi) * Xlam[0, 0])) == 0
    assert sp.simplify(sp.exp(phi * Xlam[2, 2]) * sp.exp(psi * Xlam[2, 2]) - sp.exp((phi + psi) * Xlam[2, 2])) == 0

    # Complete R x S3 coframe relative to (c dt, sigma3, sigma1, sigma2).
    E = sp.Matrix([
        [sp.exp(-phi), a * sp.exp(-phi), 0, 0],
        [0, R * sp.exp(phi), 0, 0],
        [0, 0, R * sp.exp(lam * phi), 0],
        [0, 0, 0, R * sp.exp(lam * phi)],
    ])
    metric = sp.simplify(E.T * eta * E)
    coframe_det = sp.simplify(E.det())
    metric_det = sp.simplify(metric.det())
    assert sp.simplify(coframe_det - R**3 * sp.exp(2 * lam * phi)) == 0
    assert sp.simplify(metric_det + R**6 * sp.exp(4 * lam * phi)) == 0
    assert sp.simplify(metric[0, 0] + sp.exp(-2 * phi)) == 0
    assert sp.simplify(metric[1, 1] - (R**2 * sp.exp(2 * phi) - a**2 * sp.exp(-2 * phi))) == 0

    # The same complete domain and founded pair admit inequivalent lambda values.
    spectra = {
        str(value): [str(sp.simplify(v)) for v in sp.diag(-1, 1, value, value).diagonal()]
        for value in (-1, 0, 1, 2)
    }
    assert len({tuple(value) for value in spectra.values()}) == 4

    # c_E and G_obs alone have no dimensionless monomial.
    # Rows are (L,M,T), columns are c and G.
    dimension_matrix = sp.Matrix([[1, 3], [0, -1], [-1, -2]])
    assert dimension_matrix.rank() == 2
    assert len(dimension_matrix.nullspace()) == 0

    # Additive endpoint depths form a family; composition does not select f.
    fp, fq, fr = sp.symbols("f_p f_q f_r")
    telescoping = sp.simplify((fq - fp) + (fr - fq) - (fr - fp))
    assert telescoping == 0

    return {
        "schema": "udt-native-global-coframe-definition-algebra-1.0",
        "status": "PASS",
        "lorentz_centralizer_nullity": lorentz_centralizer_nullity,
        "ordered_pair_SO2_self_adjoint_physical_moduli": ordered_pair_moduli,
        "ordered_pair_generator": "diag(-1,1,lambda,lambda)",
        "generator_trace": "2*lambda",
        "complete_RxS3_coframe_determinant": "R^3*exp(2*lambda*phi)",
        "complete_RxS3_metric_determinant": "-R^6*exp(4*lambda*phi)",
        "stationary_clock_norm": "-c_E^2*exp(-2*phi)",
        "spacelike_slice_sigma3_coefficient": "R^2*exp(2*phi)-a^2*exp(-2*phi)",
        "sample_lambda_spectra": spectra,
        "c_G_dimension_matrix_rank": 2,
        "c_G_dimensionless_monomial_nullity": 0,
        "endpoint_depth_telescoping": str(telescoping),
    }


CAPABILITY = {
    "N01": {"O01": "SUPPLIES", "O05": "CONSTRAINS_ONLY", "O11": "CONSTRAINS_ONLY"},
    "N02": {"O01": "SUPPLIES", "O02": "CONSTRAINS_ONLY", "O06": "CONSTRAINS_ONLY", "O11": "CONSTRAINS_ONLY"},
    "N03": {"O04": "SUPPLIES", "O02": "COVARIANCE_ONLY", "O05": "COVARIANCE_ONLY", "O06": "COVARIANCE_ONLY", "O07": "COVARIANCE_ONLY", "O11": "COVARIANCE_ONLY"},
    "N04": {"O02": "CONSTRAINS_ONLY", "O03": "CONSTRAINS_ONLY", "O06": "CONSTRAINS_ONLY", "O11": "CONSTRAINS_ONLY"},
    "N07": {"O07": "CONSTRAINS_ONLY", "O08": "CONSTRAINS_ONLY", "O09": "CONSTRAINS_ONLY", "O11": "CONSTRAINS_ONLY"},
    "N08": {"O03": "CONSTRAINS_ONLY", "O09": "CONSTRAINS_ONLY"},
    "N09": {"O10": "CALIBRATES_ONLY"},
    "N10": {"O10": "CALIBRATES_ONLY"},
    "N11": {key: "CONFLICTING_OR_SUPERSEDED" for key in [f"O{i:02d}" for i in range(1, 13)]},
    "N12": {"O10": "CONSTRAINS_ONLY", "O11": "CONSTRAINS_ONLY"},
    "N14": {"O02": "CONSTRAINS_ONLY", "O03": "CONSTRAINS_ONLY", "O05": "CONSTRAINS_ONLY", "O06": "CONSTRAINS_ONLY", "O09": "CONSTRAINS_ONLY"},
}


def capability_basis(premise: str, obligation: str, status: str) -> str:
    if status == "SUPPLIES":
        return "exact active source operation supplies this bounded obligation"
    if status == "COVARIANCE_ONLY":
        return "transforms candidate families consistently but selects no member"
    if status == "CALIBRATES_ONLY":
        return "sets dimensions or local conversion but no dimensionless representation data"
    if status == "CONFLICTING_OR_SUPERSEDED":
        return "inactive strong-CSN premise cannot be used in current physics"
    if status == "CONSTRAINS_ONLY":
        return "narrows or classifies the obligation without closing it"
    if premise == "N13":
        return "working co-presence interpretation supplies no registered mathematical construction map"
    if premise in {"N15", "N16"}:
        return "object is excluded from this audit"
    if premise == "N17":
        return "external/GR material is comparison-only"
    return "no registered typed operation from this premise to this obligation"


def git_output(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return result.stdout.strip()


def main() -> None:
    manifest = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == 99
    assert len({row["path"] for row in manifest}) == 99
    paths = {row["path"] for row in manifest}
    detailed = {
        "udt_full_local_jet_strata_p02_2026-07-27/STRATUM_LEDGER.tsv",
        "udt_full_local_jet_strata_p02_2026-07-27/P02B_CANDIDATE_LEDGER.tsv",
    }
    assert detailed <= paths

    source_rows = []
    for row in manifest:
        path = ROOT / row["path"]
        assert path.is_file()
        assert path.stat().st_size == int(row["size_bytes"])
        assert sha256(path) == row["sha256"]
        role, capability, obligations, ruling = source_rule(row["path"])
        source_rows.append({
            "source_id": row["source_id"], "path": row["path"], "sha256": row["sha256"],
            "source_role": role, "construction_capability": capability,
            "obligations_addressed": obligations, "ruling": ruling,
        })
    write_tsv(
        HERE / "SOURCE_ADJUDICATION.tsv",
        ["source_id", "path", "sha256", "source_role", "construction_capability", "obligations_addressed", "ruling"],
        source_rows,
    )

    premises = read_tsv(HERE / "PREMISE_LEDGER.tsv")
    obligations = read_tsv(HERE / "CONSTRUCTION_OBLIGATIONS.tsv")
    matrix_rows = []
    for premise in premises:
        for obligation in obligations:
            pid, oid = premise["premise_id"], obligation["obligation_id"]
            status = CAPABILITY.get(pid, {}).get(oid, "DOES_NOT_ADDRESS")
            matrix_rows.append({
                "premise_id": pid,
                "obligation_id": oid,
                "capability": status,
                "basis": capability_basis(pid, oid, status),
                "selection_closed": "YES" if status == "SUPPLIES" and oid in {"O01", "O04"} else "NO",
            })
    assert len(matrix_rows) == 17 * 12
    write_tsv(
        HERE / "PRINCIPLE_CAPABILITY_MATRIX.tsv",
        ["premise_id", "obligation_id", "capability", "basis", "selection_closed"],
        matrix_rows,
    )

    algebra = exact_algebra()
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(algebra, indent=2, sort_keys=True) + "\n")

    counterfamilies = [
        {
            "id": "C01", "family": "complete_twisted_RxS3_lambda_family",
            "fixed_data": "same_RxS3_domain;same_phi;same_a;same_R;c_E_explicit;founded_clock_ruler_weights",
            "varied_data": "lambda_in_R",
            "exact_survival": "global_coframe;Lorentz_signature;group_composition;observer_covariance;stationary_depth_given_K;twist_ruler_if_a*kappa_nonzero",
            "open_gate": "lambda_not_selected;K_line_uniqueness_not_general;off_shell",
            "consequence": "refutes_unique_screen_response_and_unique_complete_lift",
        },
        {
            "id": "C02", "family": "complete_twisted_RxS3_profile_family",
            "fixed_data": "same_RxS3_domain;same_lambda;same_a;same_R;c_E_explicit",
            "varied_data": "arbitrary_smooth_phi_subject_to_explicit_slice_inequality",
            "exact_survival": "global_nondegenerate_coframe;founded_inverse_weights;stationary_norm_depth",
            "open_gate": "no_profile_equation_or_selection",
            "consequence": "refutes_unique_realized_phi_profile",
        },
        {
            "id": "C03", "family": "ordered_pair_endpoint_depth_cocycles",
            "fixed_data": "same_typed_pair_objects;same_lambda;same_transport",
            "varied_data": "delta_f(p,q)=f(q)-f(p)_for_arbitrary_f_including_zero",
            "exact_survival": "neutrality;reversal;three-point_composition",
            "open_gate": "metric_native_f_and_physical_endpoint_semantics_not_selected",
            "consequence": "composition_does_not_select_depth",
        },
        {
            "id": "C04", "family": "ordered_pair_SO2_self_adjoint_lifts",
            "fixed_data": "same_metric;same_ordered_clock_ruler_pair;same_screen_SO2_covariance",
            "varied_data": "X_lambda=diag(-1,1,lambda,lambda)",
            "exact_survival": "pair_action;metric_self_adjointness;frame_equivariance;finite_exponential_group_law",
            "open_gate": "lambda_not_selected",
            "consequence": "one_physical_pointwise_modulus_survives",
        },
        {
            "id": "C05", "family": "complete_twist_on_off_controls",
            "fixed_data": "same_RxS3_coframe_family;same_phi;same_lambda;same_R",
            "varied_data": "a=0_versus_a*kappa_nonzero",
            "exact_survival": "complete_clock_depth_in_both",
            "open_gate": "ruler_line_absent_when_twist_zero",
            "consequence": "signed_depth_and_intrinsic_ruler_selection_are_independent",
        },
        {
            "id": "C06", "family": "scalar_anchor_dimension_system",
            "fixed_data": "c_E_and_G_obs_only",
            "varied_data": "none",
            "exact_survival": "dimension_matrix_rank_2_nullity_0",
            "open_gate": "no_absolute_length_mass_or_dimensionless_lift_parameter",
            "consequence": "anchors_calibrate_but_do_not_select_lambda_profile_or_completion",
        },
        {
            "id": "C07", "family": "complete_off_shell_configuration_without_equations",
            "fixed_data": "any_C01_or_C02_member",
            "varied_data": "configuration_member",
            "exact_survival": "complete_global_geometry",
            "open_gate": "no_native_EOM_variation_or_bootstrap_fixed_point",
            "consequence": "kinematic_constructibility_does_not_select_a_realized_branch",
        },
    ]
    write_tsv(
        HERE / "COUNTERFAMILY_ATLAS.tsv",
        ["id", "family", "fixed_data", "varied_data", "exact_survival", "open_gate", "consequence"],
        counterfamilies,
    )

    selectors = [
        {
            "selector_id": "S01", "missing_object": "physical_comparison_base_and_signed_depth",
            "obligations": "O04;O05;O07", "status": "OPEN_INDEPENDENT",
            "independence_witness": "C03_all_endpoint_cocycles_compose;path_groupoid_all_lambda",
            "minimum_required_operation": "assign_physical_observer_event_or_path_arrows_and_metric_native_signed_depth",
        },
        {
            "selector_id": "S02", "missing_object": "finite_reciprocal_lift_and_screen_response",
            "obligations": "O02;O06;O11", "status": "OPEN_INDEPENDENT",
            "independence_witness": "C01_and_C04_same_pair_and_domain_retain_lambda",
            "minimum_required_operation": "select_and_integrate_the_transverse_or_mixing_response_equivariantly",
        },
        {
            "selector_id": "S03", "missing_object": "global_completion_descent_and_causal_interfaces",
            "obligations": "O07;O08;O09", "status": "OPEN_INDEPENDENT",
            "independence_witness": "local_lift_atlas_exists_without_selected_completion;registered_completions_have_distinct_join_data",
            "minimum_required_operation": "supply_complete_chart_cocycle_caps_seams_quotients_and_type_change_rules",
        },
        {
            "selector_id": "S04", "missing_object": "realization_equations_and_variation_domain",
            "obligations": "O12", "status": "OPEN_DOWNSTREAM_INDEPENDENT",
            "independence_witness": "C07_complete_configurations_exist_off_shell",
            "minimum_required_operation": "derive_native_equations_or_equivalent_whole_solution_closure",
        },
        {
            "selector_id": "S05", "missing_object": "absolute_scale_and_G_obs_placement",
            "obligations": "O10", "status": "PARTIAL_C_E_PLACED_G_OBS_OPEN_DOWNSTREAM",
            "independence_witness": "C06_dimension_rank",
            "minimum_required_operation": "supply_a_native_dimensional_quantity_or_mass_geometry_relation_beyond_c_E_and_G_obs",
        },
    ]
    write_tsv(
        HERE / "MINIMAL_SELECTOR_SET.tsv",
        ["selector_id", "missing_object", "obligations", "status", "independence_witness", "minimum_required_operation"],
        selectors,
    )

    nonultra_path = "udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27/AUDIT_REPORT.md"
    p03_manifest = read_tsv(ROOT / "udt_global_coframe_compatibility_p03_2026-07-27/SOURCE_MANIFEST.tsv")
    p03_paths = {row["path"] for row in p03_manifest}
    assert nonultra_path not in p03_paths
    introducing_commit = git_output("log", "-1", "--format=%H", "--", nonultra_path)
    p03_base = "6727b74878103a91eac855bad91a97b0a5c2e167"
    ancestor_check = subprocess.run(["git", "merge-base", "--is-ancestor", introducing_commit, p03_base], cwd=ROOT).returncode == 0
    assert ancestor_check
    correction_rows = [
        {
            "claim": "P03_57_source_census_and_zero_eligibility_inside_freeze",
            "ruling": "RETAIN_SCOPED",
            "basis": "exactly_reproducible_for_its_frozen_source_universe",
        },
        {
            "claim": "P03_source_universe_complete_for_registered_repository_at_base",
            "ruling": "CORRECT_FALSE_BY_OMISSION",
            "basis": f"{nonultra_path}_introduced_at_{introducing_commit}_and_ancestor_of_P03_base_but_not_frozen",
        },
        {
            "claim": "only_ultrastatic_complete_controls_registered",
            "ruling": "SUPERSEDED_REPOSITORY_WIDE",
            "basis": "complete_nonultrastatic_RxS3_configuration_family_preexisted_P03",
        },
        {
            "claim": "lossless_P02_projection_blocked_in_P03",
            "ruling": "RETAIN_PROCEDURAL",
            "basis": "both_detailed_ledgers_were_absent_from_P03_freeze_and_are_present_in_this_preregistration",
        },
        {
            "claim": "P03B_not_launched",
            "ruling": "RETAIN_AUTHORITY_BOUNDARY",
            "basis": "new_family_does_not_supply_native_selection_and_no_P03B_dispatch_exists",
        },
    ]
    write_tsv(HERE / "P03_SCOPE_CORRECTION.tsv", ["claim", "ruling", "basis"], correction_rows)

    capability_counts = Counter(row["capability"] for row in matrix_rows)
    result = {
        "schema": "udt-native-global-coframe-definition-audit-1.0",
        "status": "OPEN_MULTIPLE_INDEPENDENT_SELECTOR_GAPS",
        "source_count": 99,
        "source_role_counts": dict(sorted(Counter(row["source_role"] for row in source_rows).items())),
        "principle_obligation_rows": len(matrix_rows),
        "principle_capability_counts": dict(sorted(capability_counts.items())),
        "complete_coherent_counterfamilies": len(counterfamilies),
        "kinematic_minimal_selector_count": 3,
        "selected_realized_branch_additional_selector_count": 1,
        "absolute_scale_additional_open_count": 1,
        "P03_nonultrastatic_source_omission": True,
        "P03_nonultrastatic_source_introducing_commit": introducing_commit,
        "P03_nonultrastatic_source_ancestor_of_base": ancestor_check,
        "P02_detailed_ledgers_frozen": sorted(detailed),
        "P02_projection_activated": False,
        "P03B_launched": False,
        "GPU_launched": False,
        "maximum_conclusion": "ACTIVE_UDT_FOUNDATION_DERIVES_RECIPROCAL_PAIR_AND_COVARIANT_RESPONSE_ARCHITECTURE_BUT_NOT_A_UNIQUE_GLOBAL_COFRAME_CONSTRUCTION;THREE_INDEPENDENT_KINEMATIC_SELECTOR_GAPS_REMAIN;REALIZATION_EQUATIONS_AND_ABSOLUTE_SCALE_ARE_SEPARATE_DOWNSTREAM_GAPS",
    }
    (HERE / "AUDIT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
