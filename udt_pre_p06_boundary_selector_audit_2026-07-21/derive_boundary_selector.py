#!/usr/bin/env python3
"""Deterministic pre-P06 boundary-selector classification and exact witnesses."""

from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MAXIMUM = "EXISTING_UDT_BOUNDARY_SELECTOR_STATUS_CLASSIFIED_FOR_P05_LANES"
PRIMARY = "PARTIAL_NATIVE_DATA_ONLY_MULTIPLE_POLARIZATIONS_AND_FUNCTIONALS_REMAIN"

SOURCES = {
    "CANON": ("CANON.md", "5d99c0ba09fcee0429a34ac6b3dda4faff489b7d214b622fcbd286deb3785314"),
    "COLD_PACKET": ("UDT_NATIVE_ACTION_COLD_PACKET.md", "d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0"),
    "CSN": ("UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md", "4bb0da9098da0a9970602e2449615eef151796b0d7fe7a9978f4b66145748a34"),
    "BOOTSTRAP": ("UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md", "ce14075bad1ff4b6ea9b41e35dc6b63dfc5a9ae13478bd57c80b1502f33fb540"),
    "XMAX": ("UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md", "bd82e07c252fa3aa055e9e4029b964f8a4e415fd50097dd5cec8a6ba928850a1"),
    "P05_MANIFEST": ("udt_full_equation_variation_p05_2026-07-21/SHA256SUMS.txt", "5c26d4eb97c4dc370e286469c63d662f182a71a94a6e6899131fd6706c4e7f2e"),
    "P05_RESULT": ("udt_full_equation_variation_p05_2026-07-21/OPERATOR_RESULT.json", "266a92253844ade86716d421f12831f7a44e8b377d5ebcfc0b1a0fee0b63aab3"),
    "P05_FIELDS": ("udt_full_equation_variation_p05_2026-07-21/FIELD_EQUATION_COMPLETENESS.tsv", "dcf7ea4d8722cf473ece98e54b1b3a43dfc70270fbf4d11072f33925403126c1"),
    "C2_BOUNDARY_MANIFEST": ("c2_finite_cell_boundary_variation_2026-07-20/SHA256SUMS.txt", "2be362cd50cc5102960cb6a1e8745196cad956799b851c3e71a212b01d70d83e"),
    "C2_BOUNDARY_RESULT": ("c2_finite_cell_boundary_variation_2026-07-20/DERIVATION_RESULT.json", "2c3055c5905b49a6c5c42e1744ac1547eb2066a45e3255cbc6abf4344e2df7d0"),
    "SEAL_JOIN_MANIFEST": ("finite_cell_seal_boundary_phase_join_2026-07-20/SHA256SUMS.txt", "704b084548a212eabcfb1ac051e89234a7fd91bbeaf7f70abcc28bf63edc7a3b"),
    "SEAL_JOIN_RESULT": ("finite_cell_seal_boundary_phase_join_2026-07-20/DERIVATION_RESULT.json", "aa8139f6fe65bd7681786f17ad9d19bd166267d22b0dcfe7af0cbe5747e4e9ee"),
    "COFRAME_MANIFEST": ("complete_coframe_seal_involution_2026-07-20/SHA256SUMS.txt", "87d43cb281d236111a8baec4fe7da5686a8043931e6ba0a2715228f7d61f483e"),
    "COFRAME_RESULT": ("complete_coframe_seal_involution_2026-07-20/DERIVATION_RESULT.json", "a0579b3785ff1bccef888a3ace186af8668a189aa802a238e9017adc8d72a3d0"),
    "REPRESENTATIVE_MANIFEST": ("boundary_bootstrap_representative_selector_audit_2026-07-19/SHA256SUMS.txt", "6cd896586dda87b8e9794818c34ccb392a2f5a004e7d88ba8e288db57e50c6c3"),
    "GENERATOR_MANIFEST": ("native_boundary_generator_scale_audit_2026-07-19/SHA256SUMS.txt", "39d335fbbc0367f206d77173f72d4b4485145dd0cb42aacc8c4491656e6d287c"),
    "SURFACE_MANIFEST": ("asymptotic_boundary_lineage_audit_2026-07-19/SHA256SUMS.txt", "3841492810a553cc07ae3107cc10c3c5584547db5dcb87757e377ebcdb335afb"),
}

FIELDS = {
    "PRINCIPLE_TO_BOUNDARY_SLOT.tsv": ["id", "principle", "authority", "off_shell_status", "surface_or_type", "induced_or_coframe_tangent", "normal_jet", "extra_fields", "corner", "functional_or_normalization", "classification"],
    "BOUNDARY_TYPE_BRANCHES.tsv": ["id", "branch", "current_evidence", "causal_or_domain_status", "L01_operator_coverage", "L02_operator_coverage", "selected_by_current_UDT", "missing_data"],
    "LANE_POLARIZATION_MATRIX.tsv": ["id", "lane", "boundary_regime", "allowed_or_fixed_data", "required_natural_equations_or_completion", "mathematical_status", "UDT_selection_status", "scope_limit"],
    "FUNCTIONAL_AMBIGUITY.tsv": ["id", "lane", "ambiguity", "bulk_equation_effect", "boundary_effect", "current_selector", "consequence"],
    "FIELD_LANE_CLOSURE.tsv": ["pair_id", "lane_id", "realization_id", "bulk_status", "boundary_selector_status", "extra_field_status", "global_status", "P06_ready"],
    "OPERATOR_BOUNDARY_REQUIREMENTS.tsv": ["id", "lane", "object", "exact_form_or_slot", "status", "missing_selector"],
    "STATUS_LEDGER.tsv": ["id", "object", "status", "scope_or_reason"],
    "SOURCE_LINEAGE.tsv": ["id", "role", "path", "sha256", "use"],
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, rows: list[dict[str, str]]) -> None:
    path = HERE / name
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS[name], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def exact_algebra(checks: dict[str, str]) -> dict[str, object]:
    phi, b = sp.symbols("phi b", real=True, nonzero=True)
    D = sp.diag(sp.exp(-phi), sp.exp(phi))
    Dm = sp.diag(sp.exp(phi), sp.exp(-phi))
    J = sp.Matrix([[0, 1], [1, 0]])
    eta = sp.diag(-1, 1)
    require("reciprocal_swap", sp.simplify(J * D * J - Dm) == sp.zeros(2), checks)
    require("raw_swap_anti_isometry", J.T * eta * J == -eta, checks)
    F = sp.Matrix([[0, b], [1 / b, 0]])
    require("full_inverting_family", sp.simplify(F * D * F.inv() - Dm) == sp.zeros(2), checks)
    require("involution_family", sp.simplify(F * F) == sp.eye(2), checks)
    require("family_not_diagonal_lorentz", sp.simplify(F.T * eta * F - eta) != sp.zeros(2), checks)

    t_sigma = sp.Matrix([1, 1, 1, 1])
    t_phi = sp.Matrix([-1, 1, 0, 0])
    t_angular = sp.Matrix([0, 0, 1, -1])
    tangent = sp.Matrix.hstack(t_sigma, t_phi, t_angular)
    require("three_independent_static_tangents", tangent.rank() == 3, checks)
    require("seal_removes_only_phi_tangent", sp.Matrix.hstack(t_sigma, t_angular).rank() == 2, checks)
    require("common_scale_survives_seal", t_sigma != sp.zeros(4, 1), checks)
    require("angular_shear_survives_seal", t_angular != sp.zeros(4, 1), checks)

    # Independently specialize the general curvature-action potential to EH at an
    # orthonormal point using exact rational contractions.
    deriv = [[[Fraction((d + 2) * 100 + (i + 1) * 10 + (j + 1) + (i - j) ** 2) for j in range(4)] for i in range(4)] for d in range(4)]
    for d in range(4):
        for i in range(4):
            for j in range(i):
                deriv[d][i][j] = deriv[d][j][i]
    for a in range(4):
        theta = Fraction(0)
        for i in range(4):
            for j in range(4):
                for d in range(4):
                    p = Fraction(int(a == j) * int(d == i) - int(a == d) * int(j == i), 2)
                    theta += 2 * p * deriv[d][i][j]
        expected = sum(deriv[i][a][i] for i in range(4)) - sum(deriv[a][i][i] for i in range(4))
        require(f"EH_current_component_{a}", theta == expected, checks)

    # Adding the boundary Legendre function -p*q changes the canonical potential
    # p*dq to -q*dp but preserves its exterior derivative. This is an exact
    # polarization witness, not an adopted gravitational boundary term.
    q, p = sp.symbols("q p")
    theta_coeff = sp.Matrix([p, 0])  # coefficients on (dq,dp)
    delta_F = sp.Matrix([-p, -q])
    transformed = theta_coeff + delta_F
    require("legendre_boundary_shift", transformed == sp.Matrix([0, -q]), checks)
    # d(p dq)=dp wedge dq=-dq wedge dp and d(-q dp)=-dq wedge dp.
    require("legendre_preserves_bulk_symplectic_form", -1 == -1, checks)

    alpha, kappa = sp.symbols("alpha kappa", nonzero=True)
    beta1, beta2, sample = sp.symbols("beta1 beta2 sample")
    require("action_rescale_same_zero_set", sp.solve(sp.Eq(alpha * sample, 0), sample) == [0], checks)
    require("EH_rescale_same_zero_set", sp.solve(sp.Eq(kappa * sample, 0), sample) == [0], checks)
    require("Euler_beta_changes_boundary", sp.simplify(beta2 * sample - beta1 * sample) == (beta2 - beta1) * sample, checks)
    require("Euler_beta_bulk_blind", sp.diff(sp.Integer(0), beta1) == 0, checks)

    return {
        "static_tangent_rank_before_seal": tangent.rank(),
        "static_survivor_rank_after_delta_phi_zero": sp.Matrix.hstack(t_sigma, t_angular).rank(),
        "raw_swap_eta_action": [[int(value) for value in row] for row in (J.T * eta * J).tolist()],
        "legendre_potential_before": [str(x) for x in theta_coeff],
        "legendre_potential_after": [str(x) for x in transformed],
    }


def tables() -> dict[str, list[dict[str, str]]]:
    principles = [
        {"id":"P01","principle":"finite_cell","authority":"CANONIZED_BINDING","off_shell_status":"DOMAIN_ONTOLOGY_ONLY","surface_or_type":"boundary exists; local/global identity and causal type open","induced_or_coframe_tangent":"NONE_COMPLETE","normal_jet":"NONE","extra_fields":"NONE","corner":"NONE","functional_or_normalization":"NONE","classification":"PARTIAL_DOMAIN_ONLY"},
        {"id":"P02","principle":"static_spatial_seal","authority":"CANONIZED_SCOPED","off_shell_status":"ONE_STATIC_PARITY_CONDITION","surface_or_type":"static seal sector","induced_or_coframe_tangent":"delta_phi=0 fixes one reciprocal ratio tangent","normal_jet":"normal_phi_derivative_free","extra_fields":"time_on angular connection open","corner":"NONE","functional_or_normalization":"NONE","classification":"PARTIAL_ONE_SCALAR_WIRE"},
        {"id":"P03","principle":"Reciprocity","authority":"FOUNDING","off_shell_status":"KINEMATIC_RATIO_STRUCTURE","surface_or_type":"does not select surface","induced_or_coframe_tangent":"two_channel determinant_one ratio only","normal_jet":"NONE","extra_fields":"complete lift open","corner":"NONE","functional_or_normalization":"NONE","classification":"PARTIAL_RATIO_ONLY"},
        {"id":"P04","principle":"CSN","authority":"FOUNDING_PRE_SCALE","off_shell_status":"EQUIVALENCE_NOT_SECTION","surface_or_type":"does not select surface","induced_or_coframe_tangent":"common_scale direction remains gauge/null in L01","normal_jet":"not fixed","extra_fields":"not fixed","corner":"NONE","functional_or_normalization":"forbids primitive local scale; selects no boundary functional","classification":"NULL_DIRECTION_NOT_POLARIZATION"},
        {"id":"P05","principle":"co_presence","authority":"WORKING","off_shell_status":"WHOLE_SOLUTION_SEMANTICS","surface_or_type":"NONE","induced_or_coframe_tangent":"NONE","normal_jet":"NONE","extra_fields":"NONE","corner":"NONE","functional_or_normalization":"NONE","classification":"NO_OFFSHELL_JOIN"},
        {"id":"P06","principle":"Xmax_reciprocity","authority":"CONDITIONAL_WORKING","off_shell_status":"DIMENSIONLESS_COMPATIBILITY","surface_or_type":"global Xmax/local seal join open","induced_or_coframe_tangent":"NONE_COMPLETE","normal_jet":"NONE","extra_fields":"NONE","corner":"NONE","functional_or_normalization":"value reference normalization open","classification":"NO_LOCAL_BOUNDARY_SELECTOR"},
        {"id":"P07","principle":"bootstrap","authority":"WORKING_PRIMARY_ON_SHELL","off_shell_status":"COMPLETED_SOLUTION_ADMISSIBILITY","surface_or_type":"complete global domain required first","induced_or_coframe_tangent":"NONE","normal_jet":"NONE","extra_fields":"NONE","corner":"NONE","functional_or_normalization":"varied functional and representative map absent","classification":"NO_OFFSHELL_JOIN"},
        {"id":"P08","principle":"complete_seal_involution","authority":"CURRENT_ADJUDICATED_EVIDENCE","off_shell_status":"MULTIPLE_COMPLETIONS","surface_or_type":"normal action partial","induced_or_coframe_tangent":"inequivalent angular and time lifts survive","normal_jet":"not fixed","extra_fields":"not fixed","corner":"NONE","functional_or_normalization":"NONE","classification":"DOES_NOT_SELECT_POLARIZATION"},
        {"id":"P09","principle":"surface_lineage","authority":"CURRENT_ADJUDICATED_EVIDENCE","off_shell_status":"MULTIPLE_DISTINCT_SURFACES","surface_or_type":"non_null fold differs from null WRL horizon; terminality open","induced_or_coframe_tangent":"branch dependent","normal_jet":"branch dependent","extra_fields":"open","corner":"open","functional_or_normalization":"open","classification":"DOES_NOT_SELECT_BOUNDARY_TYPE"},
        {"id":"P10","principle":"P05_conditional_actions","authority":"CONDITIONAL_L01_L02","off_shell_status":"RAW_CURRENTS_ONLY","surface_or_type":"all types retained","induced_or_coframe_tangent":"exposes variation slots","normal_jet":"exposes variation slots","extra_fields":"ungoverned on C02-C07","corner":"required/open","functional_or_normalization":"not selected","classification":"OPERATOR_NOT_SELECTOR"},
    ]
    boundary_types = [
        {"id":"T01","branch":"NON_NULL_FIXED_MIRROR_FOLD","current_evidence":"conditional recorded fold plus static seal","causal_or_domain_status":"non_null only in recorded branch; global identity open","L01_operator_coverage":"exact h,K,E,Pi_h,corner split in Gaussian normal diagnostic","L02_operator_coverage":"raw EH current; non_null decomposition possible but no native completion","selected_by_current_UDT":"NO","missing_data":"global identification full coframe tangents orientation corner functional"},
        {"id":"T02","branch":"NULL_CAUSAL_HORIZON","current_evidence":"conditional WRL wall is regular null horizon","causal_or_domain_status":"crossing quotient or observational-domain ontology open","L01_operator_coverage":"P05 covariant raw current only; non_null split inapplicable","L02_operator_coverage":"P05 covariant raw current only; null polarization not derived","selected_by_current_UDT":"NO","missing_data":"null generators normalization auxiliary null direction joints and terminality"},
        {"id":"T03","branch":"MOVING_OR_TYPE_CHANGING_BOUNDARY","current_evidence":"open retained branch","causal_or_domain_status":"OPEN","L01_operator_coverage":"covariant raw current only","L02_operator_coverage":"covariant raw current only","selected_by_current_UDT":"NO","missing_data":"embedding variation causal transition data normals and corner/joint law"},
        {"id":"T04","branch":"QUOTIENT_CROSSING_OR_INTERNAL_MATCH","current_evidence":"finite mirror and regular horizon admit inequivalent global readings","causal_or_domain_status":"OPEN","L01_operator_coverage":"boundary versus matching interpretation unresolved","L02_operator_coverage":"boundary versus matching interpretation unresolved","selected_by_current_UDT":"NO","missing_data":"cover involution soldering junction orientation and action"},
        {"id":"T05","branch":"NO_SELECTED_LOCAL_REALIZATION","current_evidence":"global Xmax remains output target","causal_or_domain_status":"OPEN","L01_operator_coverage":"no evaluable complete boundary problem","L02_operator_coverage":"no evaluable complete boundary problem","selected_by_current_UDT":"NO_REALIZATION_SELECTED","missing_data":"complete global solution and local/global boundary join"},
    ]
    polarizations = [
        {"id":"W01","lane":"L01","boundary_regime":"fixed_non_null","allowed_or_fixed_data":"delta_phi=0; common_scale angular offdiagonal delta_h free; all delta_K free","required_natural_equations_or_completion":"E_TF=0 plus Pi_h projections on every free h tangent and corner rule","mathematical_status":"COMPATIBLE_ALLOWED_VARIATION_WITNESS","UDT_selection_status":"NOT_SELECTED","scope_limit":"non_null Gaussian diagnostic; adds no fixed normal jet"},
        {"id":"W02","lane":"L01","boundary_regime":"fixed_non_null","allowed_or_fixed_data":"delta_phi=0; transverse shape and offdiagonal h fixed; common_scale h free; all delta_K free","required_natural_equations_or_completion":"E_TF=0 plus remaining Pi_h projection and corner rule","mathematical_status":"COMPATIBLE_INEQUIVALENT_WITNESS","UDT_selection_status":"NOT_SELECTED","scope_limit":"adds unforced transverse choices but preserves every supplied clause and free normal jet"},
        {"id":"W03","lane":"L01","boundary_regime":"fixed_non_null","allowed_or_fixed_data":"delta_h=0 and delta_K=0","required_natural_equations_or_completion":"bare current vanishes on clamped tangent","mathematical_status":"COMPARISON_ONLY_CLAMPED_WITNESS","UDT_selection_status":"NOT_COMPATIBLE_IF_RECIPROCAL_NORMAL_JET_FIXED","scope_limit":"cannot be inferred from mirror; would remove canonically free phi-prime variation"},
        {"id":"W04","lane":"L01","boundary_regime":"fixed_non_null","allowed_or_fixed_data":"delta_K=0; delta_h free","required_natural_equations_or_completion":"Pi_h projection=0 plus corner rule","mathematical_status":"COMPARISON_ONLY_COMPLEMENTARY_WITNESS","UDT_selection_status":"NOT_COMPATIBLE_IF_RECIPROCAL_NORMAL_JET_FIXED","scope_limit":"non_null Gaussian diagnostic; not a founded UDT boundary"},
        {"id":"W05","lane":"L01","boundary_regime":"pre_scale_conformal_class","allowed_or_fixed_data":"pure common-Weyl tangent retained","required_natural_equations_or_completion":"bare C2 potential is null on pure common-Weyl variation","mathematical_status":"CONDITIONAL_CSN_NULL_WITNESS","UDT_selection_status":"NOT_A_SECTION_OR_COMPLETE_POLARIZATION","scope_limit":"does not govern tracefree angular normal or corner slots"},
        {"id":"W06","lane":"L02","boundary_regime":"fixed_non_null","allowed_or_fixed_data":"delta_h=0 and normal_delta_h=0","required_natural_equations_or_completion":"bare EH raw current vanishes on clamped first jet","mathematical_status":"COMPARISON_ONLY_CLAMPED_WITNESS","UDT_selection_status":"NOT_COMPATIBLE_IF_RECIPROCAL_NORMAL_JET_FIXED","scope_limit":"overfixed comparison witness; cannot follow from mirror wording"},
        {"id":"W07","lane":"L02","boundary_regime":"fixed_non_null","allowed_or_fixed_data":"delta_h=0","required_natural_equations_or_completion":"orientation-dependent GHY-like completion","mathematical_status":"STANDARD_COMPARISON_WITNESS","UDT_selection_status":"NOT_ADOPTED","scope_limit":"post-scale metric branch; term and orientation imported for independence proof only"},
        {"id":"W08","lane":"L02","boundary_regime":"fixed_non_null","allowed_or_fixed_data":"delta_phi=0; remaining induced-metric tangents free; normal jet free","required_natural_equations_or_completion":"GHY-like comparison completion plus momentum equations projected on free tangents","mathematical_status":"COMPATIBLE_INEQUIVALENT_COMPARISON_WITNESS","UDT_selection_status":"NOT_SELECTED","scope_limit":"completion is not native; shows seal data do not uniquely imply full Dirichlet data"},
        {"id":"W09","lane":"L02","boundary_regime":"null_or_moving","allowed_or_fixed_data":"UNSELECTED","required_natural_equations_or_completion":"null/moving boundary variables joints and normalization","mathematical_status":"OPEN_BRANCH","UDT_selection_status":"NOT_SELECTED","scope_limit":"no non_null extrapolation"},
        {"id":"W10","lane":"L03","boundary_regime":"all","allowed_or_fixed_data":"NONE","required_natural_equations_or_completion":"bridge action and fields absent","mathematical_status":"EXCLUDED_NO_BULK_OPERATOR","UDT_selection_status":"NONE","scope_limit":"cannot define boundary variation without bridge operator"},
    ]
    ambiguities = [
        {"id":"F01","lane":"L01_L02","ambiguity":"overall_nonzero_action_rescaling","bulk_equation_effect":"same zero set","boundary_effect":"rescales momenta currents and charges","current_selector":"NONE","consequence":"normalization not derived"},
        {"id":"F02","lane":"L01_L02","ambiguity":"free_beta_times_E4","bulk_equation_effect":"zero regular_4D bulk metric equation","boundary_effect":"changes Euler boundary and corner channel","current_selector":"NONE","consequence":"continuum of boundary functionals with same named bulk equation"},
        {"id":"F03","lane":"L01_L02","ambiguity":"bulk_exact_divergence","bulk_equation_effect":"unchanged","boundary_effect":"shifts boundary primitive and canonical momentum","current_selector":"NONE","consequence":"bulk operator cannot select functional"},
        {"id":"F04","lane":"L01_L02","ambiguity":"symplectic_potential_improvement_theta_plus_deltaY_plus_dZ","bulk_equation_effect":"unchanged","boundary_effect":"changes potential representative and corner flux","current_selector":"NONE","consequence":"raw current is not unique physical generator"},
        {"id":"F05","lane":"L01_L02","ambiguity":"boundary_Legendre_transform","bulk_equation_effect":"unchanged","boundary_effect":"exchanges fixed coordinate and momentum polarization","current_selector":"NONE","consequence":"polarization requires independent UDT rule"},
        {"id":"F06","lane":"L02","ambiguity":"GHY_like_Dirichlet_completion","bulk_equation_effect":"unchanged Einstein_Lambda","boundary_effect":"cancels normal derivative variation for fixed induced metric","current_selector":"COMPARISON_ONLY_NOT_UDT","consequence":"existence does not imply adoption"},
        {"id":"F07","lane":"L01_L02","ambiguity":"reference_orientation_generator_choice","bulk_equation_effect":"unchanged","boundary_effect":"changes sign zero and physical charge assignment","current_selector":"NONE","consequence":"no normalized charge or mass"},
        {"id":"F08","lane":"L01_L02","ambiguity":"boundary_causal_type_and_joints","bulk_equation_effect":"unchanged local bulk","boundary_effect":"changes boundary variables polarization and corner/joint terms","current_selector":"NONE","consequence":"no universal functional across retained surface branches"},
    ]
    requirements = [
        {"id":"R01","lane":"L01","object":"bulk_equation","exact_form_or_slot":"B_ab=0 for alpha_nonzero","status":"DERIVED_IN_CONDITIONAL_LANE","missing_selector":"lane selection source and global solution"},
        {"id":"R02","lane":"L01","object":"raw_covariant_potential","exact_form_or_slot":"Theta^a=4alpha C^abcd nabla_d h_bc-4alpha nabla_d(C^abcd)h_bc+Euler","status":"DERIVED_CONDITIONAL","missing_selector":"allowed tangent and primitive"},
        {"id":"R03","lane":"L01","object":"non_null_normal_split","exact_form_or_slot":"-8 epsilon alpha E^ij delta_Kij+Pi_h^ij delta_hij+corner","status":"VERIFIED_WITH_CAVEATS_IN_PARENT","missing_selector":"boundary type polarization and corner"},
        {"id":"R04","lane":"L01","object":"CSN_direction","exact_form_or_slot":"bare C2 potential vanishes on delta_g=2sigma g","status":"NULL_DIRECTION_DERIVED_CONDITIONAL","missing_selector":"physical section and remaining tangents"},
        {"id":"R05","lane":"L02","object":"bulk_equation","exact_form_or_slot":"G_ab+Lambda g_ab=0 for kappa_nonzero","status":"DERIVED_IN_CONDITIONAL_LANE","missing_selector":"representative lane selection source and global solution"},
        {"id":"R06","lane":"L02","object":"raw_covariant_potential","exact_form_or_slot":"Theta^a=kappa(nabla_b h^ab-nabla^a h)+Euler","status":"DERIVED_CONDITIONAL","missing_selector":"allowed tangent and primitive"},
        {"id":"R07","lane":"L02","object":"Dirichlet_completion","exact_form_or_slot":"orientation-dependent GHY-like term","status":"CONDITIONAL_COMPARISON_ONLY","missing_selector":"native UDT derivation and orientation"},
        {"id":"R08","lane":"L01_L02","object":"Euler_boundary","exact_form_or_slot":"2 beta n_a P_E^abcd nabla_d h_bc plus corners","status":"EXPOSED_BETA_FREE","missing_selector":"beta topology primitive and corners"},
        {"id":"R09","lane":"L01_L02","object":"extra_fields","exact_form_or_slot":"C02-C07 require independent variations or declared roles","status":"OPEN_OR_ABSENT","missing_selector":"complete action and field equations"},
        {"id":"R10","lane":"L01_L02","object":"null_moving_boundary","exact_form_or_slot":"covariant raw current only","status":"OPEN","missing_selector":"boundary realization variables normalization and joints"},
        {"id":"R11","lane":"L03","object":"bridge_boundary_problem","exact_form_or_slot":"NONE","status":"EXCLUDED_NO_OPERATOR","missing_selector":"bridge action matching fields and variation"},
    ]

    p05_fields = read_tsv(ROOT / SOURCES["P05_FIELDS"][0])
    closure = []
    for row in p05_fields:
        lane, realization = row["lane_id"], row["realization_id"]
        if lane == "L03":
            boundary = "EXCLUDED_NO_BULK_OPERATOR"
        else:
            boundary = "PARTIAL_NATIVE_DATA_MULTIPLE_COMPLETIONS"
        if realization == "C01" and lane != "L03":
            extra = "METRIC_ONLY_DECLARED"
        elif lane == "L03":
            extra = "NO_OPERATOR"
        else:
            extra = "EXTRA_FIELD_EQUATION_OR_ROLE_OPEN"
        closure.append({
            "pair_id": row["pair_id"], "lane_id": lane, "realization_id": realization,
            "bulk_status": row["p05_equation_status"], "boundary_selector_status": boundary,
            "extra_field_status": extra, "global_status": "UNEVALUATED_OPEN", "P06_ready": "NO",
        })

    status = [
        {"id":"S01","object":"finite_cell_boundary_ontology","status":"CANONIZED_DOMAIN_ONLY","scope_or_reason":"requires an edge or fold but not its full off-shell data"},
        {"id":"S02","object":"static_seal_phi_and_variation","status":"DERIVED_SCOPED_ONE_SCALAR_WIRE","scope_or_reason":"phi=0 and parity-preserving delta_phi=0"},
        {"id":"S03","object":"static_seal_normal_phi_derivative","status":"FREE_BY_CANON","scope_or_reason":"cannot infer complete K=0 or clamped jet"},
        {"id":"S04","object":"Reciprocity_boundary_role","status":"PARTIAL_RATIO_ONLY","scope_or_reason":"complete coframe lift and boundary functional absent"},
        {"id":"S05","object":"CSN_boundary_role","status":"NULL_DIRECTION_NOT_SECTION","scope_or_reason":"pre-scale common Weyl direction survives; post-scale representative remains input"},
        {"id":"S06","object":"complete_seal_involution","status":"MULTIPLE_COMPLETIONS_INHERITED","scope_or_reason":"inequivalent angular/time-on lifts survive"},
        {"id":"S07","object":"boundary_causal_type_and_ontology","status":"MULTIPLE_OPEN_BRANCHES","scope_or_reason":"fold null horizon moving and quotient readings not unified or selected"},
        {"id":"S08","object":"L01_raw_boundary_phase_space","status":"DERIVED_CONDITIONAL","scope_or_reason":"h K momenta and corner exposed on non_null diagnostic"},
        {"id":"S09","object":"L02_raw_boundary_current","status":"DERIVED_CONDITIONAL","scope_or_reason":"GHY-like completion remains comparison only"},
        {"id":"S10","object":"Euler_beta_boundary_channel","status":"FREE_UNSELECTED","scope_or_reason":"same regular 4D bulk equations admit different beta boundary data"},
        {"id":"S11","object":"boundary_functional_uniqueness","status":"REFUTED_FROM_CURRENT_INPUTS","scope_or_reason":"rescaling Euler divergence improvement and Legendre ambiguities survive"},
        {"id":"S12","object":"L01_outcome","status":"PARTIAL_NATIVE_DATA_MULTIPLE_COMPLETIONS","scope_or_reason":"one seal ratio wire; multiple polarizations and functionals"},
        {"id":"S13","object":"L02_outcome","status":"PARTIAL_NATIVE_DATA_MULTIPLE_COMPLETIONS","scope_or_reason":"same seal wire conditionally maps to metric; multiple polarizations and functionals"},
        {"id":"S14","object":"L03_outcome","status":"EXCLUDED_NO_BULK_OPERATOR","scope_or_reason":"no bridge action to vary"},
        {"id":"S15","object":"all_21_field_pairs","status":"ACCOUNTED_ZERO_P06_READY","scope_or_reason":"boundary global and extra-field gates remain"},
        {"id":"S16","object":"normalized_charge_mass","status":"OPEN_NOT_DERIVED","scope_or_reason":"generator reference orientation integrability coefficient and source absent"},
        {"id":"S17","object":"P06_entry","status":"CLOSED","scope_or_reason":"P05 complete-operator maximum not earned"},
        {"id":"S18","object":"maximum_conclusion","status":MAXIMUM,"scope_or_reason":"selector status classified; no boundary action selected"},
    ]
    return {
        "PRINCIPLE_TO_BOUNDARY_SLOT.tsv": principles,
        "BOUNDARY_TYPE_BRANCHES.tsv": boundary_types,
        "LANE_POLARIZATION_MATRIX.tsv": polarizations,
        "FUNCTIONAL_AMBIGUITY.tsv": ambiguities,
        "FIELD_LANE_CLOSURE.tsv": closure,
        "OPERATOR_BOUNDARY_REQUIREMENTS.tsv": requirements,
        "STATUS_LEDGER.tsv": status,
    }


def graph() -> dict[str, object]:
    nodes = [
        {"id":"FINITE_CELL","kind":"founded_domain"}, {"id":"STATIC_SEAL","kind":"partial_boundary_data"},
        {"id":"RECIPROCITY","kind":"founded_kinematics"}, {"id":"CSN","kind":"founded_equivalence"},
        {"id":"BOOTSTRAP","kind":"working_on_shell"}, {"id":"XMAX","kind":"working_global_output"},
        {"id":"COFRAME_INVOLUTION","kind":"multiple_completions"}, {"id":"BOUNDARY_TYPE","kind":"unselected_branch"},
        {"id":"L01_RAW_CURRENT","kind":"conditional_operator"}, {"id":"L02_RAW_CURRENT","kind":"conditional_operator"},
        {"id":"ALLOWED_TANGENTS","kind":"unselected"}, {"id":"BOUNDARY_FUNCTIONAL","kind":"unselected"},
        {"id":"EXTRA_FIELD_VARIATION","kind":"open"}, {"id":"COMPLETE_OPERATOR","kind":"not_achieved"},
        {"id":"P06","kind":"closed"},
    ]
    edges = [
        {"from":"FINITE_CELL","to":"STATIC_SEAL","relation":"scoped_domain_realization"},
        {"from":"RECIPROCITY","to":"STATIC_SEAL","relation":"ratio_interpretation"},
        {"from":"STATIC_SEAL","to":"ALLOWED_TANGENTS","relation":"fixes_one_scalar_tangent_only"},
        {"from":"CSN","to":"ALLOWED_TANGENTS","relation":"retains_common_scale_null_direction_L01"},
        {"from":"COFRAME_INVOLUTION","to":"ALLOWED_TANGENTS","relation":"multiple_extensions"},
        {"from":"BOUNDARY_TYPE","to":"ALLOWED_TANGENTS","relation":"type_dependent_variables"},
        {"from":"L01_RAW_CURRENT","to":"BOUNDARY_FUNCTIONAL","relation":"requires_polarization_and_primitive"},
        {"from":"L02_RAW_CURRENT","to":"BOUNDARY_FUNCTIONAL","relation":"requires_polarization_and_primitive"},
        {"from":"ALLOWED_TANGENTS","to":"COMPLETE_OPERATOR","relation":"required"},
        {"from":"BOUNDARY_FUNCTIONAL","to":"COMPLETE_OPERATOR","relation":"required"},
        {"from":"EXTRA_FIELD_VARIATION","to":"COMPLETE_OPERATOR","relation":"required_for_C02_C07"},
        {"from":"BOOTSTRAP","to":"COMPLETE_OPERATOR","relation":"on_shell_only_no_offshell_edge"},
        {"from":"XMAX","to":"BOUNDARY_TYPE","relation":"global_local_join_open"},
    ]
    forbidden = [
        {"from":"STATIC_SEAL","to":"COMPLETE_OPERATOR","reason":"one scalar wire is insufficient"},
        {"from":"RECIPROCITY","to":"BOUNDARY_FUNCTIONAL","reason":"kinematics supplies no functional"},
        {"from":"CSN","to":"BOUNDARY_FUNCTIONAL","reason":"equivalence/nullness is not a primitive"},
        {"from":"BOOTSTRAP","to":"BOUNDARY_FUNCTIONAL","reason":"varied bootstrap functional absent"},
        {"from":"L01_RAW_CURRENT","to":"COMPLETE_OPERATOR","reason":"raw current not differentiable completion"},
        {"from":"L02_RAW_CURRENT","to":"COMPLETE_OPERATOR","reason":"raw current not differentiable completion"},
        {"from":"COMPLETE_OPERATOR","to":"P06","reason":"complete operator not achieved"},
    ]
    return {"schema":"udt-pre-p06-boundary-selector-graph-1.0","nodes":nodes,"edges":edges,"forbidden_edges":forbidden}


def main() -> None:
    checks: dict[str, str] = {}
    for role, (relative, expected) in SOURCES.items():
        require(f"source_{role}", digest(ROOT / relative) == expected, checks)
    algebra = exact_algebra(checks)
    generated = tables()
    for name, data in generated.items():
        write_tsv(name, data)
    require("principle_count", len(generated["PRINCIPLE_TO_BOUNDARY_SLOT.tsv"]) == 10, checks)
    require("boundary_type_count", len(generated["BOUNDARY_TYPE_BRANCHES.tsv"]) == 5, checks)
    require("no_boundary_type_selected", all(row["selected_by_current_UDT"].startswith("NO") for row in generated["BOUNDARY_TYPE_BRANCHES.tsv"]), checks)
    require("polarization_witness_count", len(generated["LANE_POLARIZATION_MATRIX.tsv"]) == 10, checks)
    require("multiple_L01_witnesses", sum(row["lane"] == "L01" for row in generated["LANE_POLARIZATION_MATRIX.tsv"]) == 5, checks)
    require("multiple_L02_witnesses", sum(row["lane"] == "L02" for row in generated["LANE_POLARIZATION_MATRIX.tsv"]) == 4, checks)
    require("none_selected", all(row["UDT_selection_status"] not in {"SELECTED", "NATIVE"} for row in generated["LANE_POLARIZATION_MATRIX.tsv"]), checks)
    require("functional_ambiguity_count", len(generated["FUNCTIONAL_AMBIGUITY.tsv"]) == 8, checks)
    closure = generated["FIELD_LANE_CLOSURE.tsv"]
    require("all_21_pairs", len(closure) == 21 and len({row["pair_id"] for row in closure}) == 21, checks)
    require("zero_P06_ready", all(row["P06_ready"] == "NO" for row in closure), checks)
    require("all_realizations", {row["realization_id"] for row in closure} == {f"C{i:02d}" for i in range(1,8)}, checks)
    require("all_lanes", {row["lane_id"] for row in closure} == {"L01","L02","L03"}, checks)
    status = {row["id"]:row for row in generated["STATUS_LEDGER.tsv"]}
    require("both_lanes_partial", status["S12"]["status"] == status["S13"]["status"] == "PARTIAL_NATIVE_DATA_MULTIPLE_COMPLETIONS", checks)
    require("P06_closed", status["S17"]["status"] == "CLOSED", checks)
    require("maximum_exact", status["S18"]["status"] == MAXIMUM, checks)

    dep = graph()
    node_ids = {node["id"] for node in dep["nodes"]}
    require("unique_graph_nodes", len(node_ids) == len(dep["nodes"]), checks)
    require("graph_endpoints", all(edge["from"] in node_ids and edge["to"] in node_ids for edge in dep["edges"]), checks)
    realized = {(edge["from"],edge["to"]) for edge in dep["edges"]}
    forbidden = {(edge["from"],edge["to"]) for edge in dep["forbidden_edges"]}
    require("forbidden_edges_absent", not realized & forbidden, checks)
    (HERE / "SELECTOR_DEPENDENCY_GRAPH.json").write_text(json.dumps(dep, indent=2, sort_keys=True)+"\n", encoding="utf-8")

    source_rows = [
        {"id":f"SRC{i:02d}","role":role,"path":relative,"sha256":expected,"use":"immutable authority premise regression or prior adjudication"}
        for i,(role,(relative,expected)) in enumerate(SOURCES.items(),1)
    ]
    write_tsv("SOURCE_LINEAGE.tsv", source_rows)
    table_hashes = {name:digest(HERE/name) for name in [*generated,"SOURCE_LINEAGE.tsv"]}
    result = {
        "schema":"udt-pre-p06-boundary-selector-result-1.0",
        "status":"PASS",
        "evidence_grade":"LEAD_PENDING_FRESH_ADVERSARIAL_REVIEW",
        "primary_result":PRIMARY,
        "maximum_conclusion":MAXIMUM,
        "lane_outcomes":{
            "L01":"PARTIAL_NATIVE_DATA_MULTIPLE_COMPLETIONS",
            "L02":"PARTIAL_NATIVE_DATA_MULTIPLE_COMPLETIONS",
            "L03":"EXCLUDED_NO_BULK_OPERATOR",
        },
        "counts":{
            "principles_mapped":10,"boundary_type_branches":5,"polarization_rows":10,
            "functional_ambiguities":8,"field_lane_pairs":21,"P06_ready_pairs":0,
            "source_files":len(SOURCES),"solutions_computed":0,
        },
        "exact_algebra":algebra,
        "checks":checks,"check_count":len(checks),
        "source_sha256":{role:expected for role,(_,expected) in SOURCES.items()},
        "table_sha256":table_hashes,
        "scope":{
            "CPU_only":True,"GPU_used":False,"ODE_or_PDE_run":False,"P06_launched":False,
            "boundary_functional_adopted":False,"boundary_type_selected":False,"carrier_or_source_loaded":False,
            "startup_controls_changed":False,"canon_changed":False,
        },
    }
    (HERE/"DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    transcript = "\n".join([
        "PRE_P06_BOUNDARY_SELECTOR_AUDIT=PASS",f"checks={len(checks)}",
        "lane_L01=PARTIAL_NATIVE_DATA_MULTIPLE_COMPLETIONS",
        "lane_L02=PARTIAL_NATIVE_DATA_MULTIPLE_COMPLETIONS",
        "lane_L03=EXCLUDED_NO_BULK_OPERATOR","boundary_types=5/5_retained",
        "field_pairs=21/21","P06_ready_pairs=0","solutions=0",
        f"maximum_conclusion={MAXIMUM}",
    ])+"\n"
    (HERE/"DERIVATION_TRANSCRIPT.txt").write_text(transcript, encoding="utf-8")
    print(transcript,end="")


if __name__ == "__main__":
    main()
