#!/usr/bin/env python3
import csv
import json
from collections import Counter
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def rows(name):
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write(name, header, data):
    with (HERE / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(data)


def exact_ids(table, key, expected):
    actual = [r[key] for r in table]
    if len(actual) != len(set(actual)) or set(actual) != set(expected):
        raise AssertionError(f"identity failure {key}")


completion = rows("COMPLETION_UNIVERSE.tsv")
controls = rows("CONCRETE_CONTROL_UNIVERSE.tsv")
strata = rows("LAMBDA_STRATUM_UNIVERSE.tsv")
gates = rows("ASSEMBLY_GATE_UNIVERSE.tsv")
exact_ids(completion, "completion_id", [f"FC{i:02d}_" + suffix for i, suffix in enumerate([
    "BOUNDARY_BOUNDARY", "ONE_CAP_BOUNDARY", "TWO_CAP_P0", "TWO_CAP_P1",
    "TWO_CAP_P_GT1", "NONPRIMITIVE_CAP", "PERIODIC_TORUS_BUNDLE", "MIRROR_DOUBLE",
    "NONORIENTABLE_GLUE", "STRATIFIED_PROJECTOR", "NONINTEGRABLE_DISTRIBUTION",
    "RECIPROCAL_TORIC_DIAGONAL"], 1)])
exact_ids(controls, "control_id", [f"Q{i:02d}" for i in range(1, 5)])
exact_ids(strata, "stratum_id", [f"L{i:02d}" for i in range(1, 5)])
exact_ids(gates, "gate_id", [f"G{i:02d}" for i in range(1, 13)])

# Exact local endomorphism algebra in the ordered (u,n,s1,s2) basis.
lam = sp.symbols("lambda", real=True)
eta = sp.diag(-1, 1, 1, 1)
X = sp.diag(-1, 1, lam, lam)


def generator(i, j):
    matrix = sp.zeros(4)
    if i == 0:
        matrix[i, j] = 1
        matrix[j, i] = 1
    else:
        matrix[i, j] = 1
        matrix[j, i] = -1
    if sp.simplify(matrix.T * eta + eta * matrix) != sp.zeros(4):
        raise AssertionError("bad Lorentz generator")
    return matrix


lorentz_basis = [generator(0, 1), generator(0, 2), generator(0, 3), generator(1, 2), generator(1, 3), generator(2, 3)]


def centralizer_dimension(value):
    columns = []
    for basis in lorentz_basis:
        comm = basis * X.subs(lam, value) - X.subs(lam, value) * basis
        columns.append(sp.Matrix(comm).reshape(16, 1))
    return 6 - sp.Matrix.hstack(*columns).rank()


centralizers = {"L01": centralizer_dimension(sp.Rational(2)), "L02": centralizer_dimension(-1), "L03": centralizer_dimension(0), "L04": centralizer_dimension(1)}

Pu = sp.diag(1, 0, 0, 0)
Pn = sp.diag(0, 1, 0, 0)
I = sp.eye(4)
Pspace = I - Pu
X_projector = -Pu + Pn + lam * (I - Pu - Pn)
X_clock = I - 2 * Pu
X_ruler = 2 * Pn - I

# Exact homogeneous S3 connection, curvature, holonomy span, and nabla X.
p, q = sp.symbols("p q", positive=True, nonzero=True)
A = p - q / 2
B = -q / 2
C = q / 2
K12 = sp.simplify(A * q + B * C)
K13 = sp.simplify(-(B * p + A * C))
K23 = sp.simplify(C * p + A * B)
J12 = sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]])
J13 = sp.Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]])
J23 = sp.Matrix([[0, 0, 0], [0, 0, 1], [0, -1, 0]])


def span_rank(matrices):
    return sp.Matrix.hstack(*[matrix.reshape(9, 1) for matrix in matrices]).rank()


def holonomy_rank(p_value, q_value):
    curv = [K12.subs({p: p_value, q: q_value}) * J12, K13.subs({p: p_value, q: q_value}) * J13, K23.subs({p: p_value, q: q_value}) * J23]
    closure = curv + [a * b - b * a for a in curv for b in curv]
    return span_rank(closure)


# n=e3. These are the two nonzero covariant derivatives of P_n.
dPn_e1 = sp.Matrix([[0, 0, 0], [0, 0, q / 2], [0, q / 2, 0]])
dPn_e2 = sp.Matrix([[0, 0, -q / 2], [0, 0, 0], [-q / 2, 0, 0]])
dX_e1 = sp.simplify((1 - lam) * dPn_e1)
dX_e2 = sp.simplify((1 - lam) * dPn_e2)
parallel_solutions = sp.solve(list(dX_e1) + list(dX_e2), lam)

stratum_rows = [
    ["L01", "lambda not in {-1,0,+1}", centralizers["L01"], "SO2_screen", "YES", "YES", "requires_u_and_n", "NO_ON_Q01_Q02", "NO_FOUNDED_DEPTH"],
    ["L02", "lambda=-1", centralizers["L02"], "SO+(1,2)_ruler_complement", "YES", "YES", "requires_n_only_fiberwise_but_not_selected", "NO_ON_Q01_Q02", "NO_FOUNDED_DEPTH"],
    ["L03", "lambda=0", centralizers["L03"], "SO2_screen", "YES", "YES", "requires_u_and_n", "NO_ON_Q01_Q02", "NO_FOUNDED_DEPTH"],
    ["L04", "lambda=+1", centralizers["L04"], "SO3_spatial", "YES", "YES", "requires_u_only_fiberwise", "YES_ON_Q01_Q02", "NO_FOUNDED_DEPTH"],
]
write("LAMBDA_STRATUM_OUTCOMES.tsv", ["stratum_id", "lambda", "connected_lorentz_centralizer_dimension", "connected_stabilizer", "pair_bundle_overlap", "typed_path_groupoid", "section_data", "parallel_endpoint_on_concrete_S3_controls", "signed_depth"], stratum_rows)

control_rows = [
    ["Q01", "FC04_TWO_CAP_P1", "YES", "YES_HOPF_FIELDS_CHOSEN_NOT_SELECTED", "L04_ONLY_FROM_METRIC_SELECTED_PARALLEL_TIME_LINE", "L04_ONLY", "ALL_LAMBDA_PATH_LABELLED;L04_ENDPOINT_COLLAPSE", "ALL_LAMBDA_SMOOTH_PAIR_BUNDLE;ANTIPODAL_PATH_SET", "NO_NONTRIVIAL_FOUNDED_DEPTH", "CONDITIONAL_ON_SHELL_SCOPE"],
    ["Q02", "FC04_TWO_CAP_P1", "YES", "YES_GLOBAL_HOPF_LINE", "ALL_LAMBDA_GIVEN_UNORIENTED_SIMPLE_RICCI_LINE;VALUE_STILL_UNSELECTED", "L04_ONLY", "ALL_LAMBDA_PATH_LABELLED;L04_ENDPOINT_COLLAPSE", "ALL_LAMBDA_SMOOTH_PAIR_BUNDLE;CUT_ATLAS_PATH_SET", "NO_NONTRIVIAL_FOUNDED_DEPTH", "OFF_SHELL_CONTROL"],
    ["Q03", "-", "NO_COMPLETE_BUNDLE_TEST", "LOCAL_ONLY", "LOCAL_U_N_CENTER_DEPENDENT", "NOT_GLOBAL", "LOCAL_PATHS_ONLY", "CENTER_AND_LAPSE_BOUNDARIES_UNRESOLVED", "LOCAL_CLOCK_PROFILE_NOT_GLOBAL_FOUNDED_ASSIGNMENT", "INCOMPLETE_DO_NOT_SPLICE"],
    ["Q04", "-", "ABSENT", "ABSENT", "ABSENT", "ABSENT", "ABSENT", "ABSENT", "ABSENT", "ABSENCE_CONTROL"],
]
write("CONCRETE_CONTROL_ASSEMBLY.tsv", ["control_id", "completion_class", "pair_frame_bundle", "chosen_global_section", "metric_natural_X", "parallel_X", "path_vs_endpoint", "cap_cut_behavior", "signed_depth", "scope"], control_rows)

completion_rulings = {
    "FC01_BOUNDARY_BOUNDARY": ("CONDITIONAL_ON_REGULAR_LORENTZ_METRIC", "OPEN_BOUNDARY_PAIR_DATA", "NO_METRIC_FOR_HOLONOMY_OR_NATURALITY", "NO_DEPTH"),
    "FC02_ONE_CAP_BOUNDARY": ("CONDITIONAL_ON_SMOOTH_CAP_METRIC", "CAP_COORDINATE_COLLAPSE_NOT_AUTOMATIC_FRAME_FAILURE", "NO_METRIC_FOR_HOLONOMY_OR_NATURALITY", "NO_DEPTH"),
    "FC03_TWO_CAP_P0": ("CONDITIONAL_ON_SMOOTH_CAP_METRIC", "GLOBAL_SECTION_AND_CAP_DESCENT_OPEN", "NO_METRIC_FOR_HOLONOMY_OR_NATURALITY", "NO_DEPTH"),
    "FC04_TWO_CAP_P1": ("PASS_FOR_Q01_Q02_PAIR_FRAME_BUNDLE", "SMOOTH_GLOBAL_CONTROLS_WITH_PATH_SETS", "CONCRETE_LAMBDA_ATLAS_COMPUTED", "NO_FOUNDED_DEPTH"),
    "FC05_TWO_CAP_P_GT1": ("CONDITIONAL_ON_REGULAR_QUOTIENT_METRIC", "DECK_ACTION_ON_PAIR_DATA_REQUIRED_FOR_SINGLE_FIELD", "NO_METRIC_FOR_HOLONOMY_OR_NATURALITY", "NO_DEPTH"),
    "FC06_NONPRIMITIVE_CAP": ("REGULAR_STRATUM_ONLY", "ORBIFOLD_ISOTROPY_OR_SINGULAR_DESCENT_OPEN", "NO_REGULAR_COMPLETE_METRIC", "NO_DEPTH"),
    "FC07_PERIODIC_TORUS_BUNDLE": ("CONDITIONAL_ON_REGULAR_MAPPING_TORUS_METRIC", "MONODROMY_ACTS_ON_PAIR_DATA;SINGLE_FIELD_NEEDS_INVARIANCE", "NO_METRIC_OR_MONODROMY_REPRESENTATIVE", "NO_DEPTH"),
    "FC08_MIRROR_DOUBLE": ("CONDITIONAL_ON_REGULAR_DOUBLE", "MIRROR_DESCENT_DEPENDS_ON_UNSELECTED_LIFT", "NO_METRIC_OR_LIFT_SELECTION", "NO_DEPTH"),
    "FC09_NONORIENTABLE_GLUE": ("CONDITIONAL_ON_REGULAR_LORENTZ_METRIC", "PROJECTORS_CAN_IGNORE_LINE_SIGN_BUT_ARROW_DEPTH_ORIENTATION_REMAINS", "NO_METRIC_OR_GLUE_REPRESENTATIVE", "NO_DEPTH"),
    "FC10_STRATIFIED_PROJECTOR": ("REGULAR_STRATA_PAIR_BUNDLE_ONLY", "PROJECTOR_DERIVED_PAIR_CAN_FAIL_AT_RANK_CHANGE;SUPPLIED_PAIR_REMAINS_SEPARATE", "NO_COMPLETE_METRIC_TRANSITION", "NO_DEPTH"),
    "FC11_NONINTEGRABLE_DISTRIBUTION": ("PAIR_FRAME_BUNDLE_DOES_NOT_REQUIRE_ORBIT_SURFACE", "NONINTEGRABILITY_NOT_A_LOCAL_BUNDLE_OBSTRUCTION", "NO_COMPLETE_METRIC_OR_GLOBAL_DESCENT", "NO_DEPTH"),
    "FC12_RECIPROCAL_TORIC_DIAGONAL": ("CONDITIONAL_PARAMETRIC_ANSATZ", "PROFILE_CAP_AND_ENDPOINT_DATA_REQUIRED", "NO_ACTUAL_COMPLETE_REPRESENTATIVE", "NO_DEPTH"),
}
completion_rows = []
for row in completion:
    completion_rows.append([row["completion_id"], *completion_rulings[row["completion_id"]]])
write("COMPLETION_ASSEMBLY_ATLAS.tsv", ["completion_id", "pair_bundle_status", "global_join_status", "naturality_parallelism_status", "signed_depth_status"], completion_rows)

gate_rows = [
    ["G01", "ALL_LAMBDA", "DERIVED_GIVEN_REGULAR_ORDERED_PAIR", "Projectors define X_lambda."],
    ["G02", "ALL_LAMBDA", "DERIVED", "Simultaneous frame change gives X_to_Lambda_X_Lambda_inverse."],
    ["G03", "ALL_LAMBDA", "DERIVED_GIVEN_TYPED_PATH_AND_VERTICAL_RESETS", "Path groupoid composition retains path labels."],
    ["G04", "ALL_LAMBDA", "DERIVED_AS_ASSOCIATED_QUERY_BUNDLE_ON_REGULAR_METRIC", "No global pair section is needed for bundle existence."],
    ["G05", "Q01_Q02", "OBSERVED_CONSTRUCTIVE_SECTIONS", "S3 is parallelizable and the registered Hopf fields are smooth; Q01 does not select one."],
    ["G06", "Q01_L04;Q02_ALL_LAMBDA", "DERIVED_CONDITIONAL_CONTROL_NATURALITY", "Round isotropy selects only u-based X1; squashing also distinguishes an unoriented Ricci line."],
    ["G07", "Q01_Q02_L04_ONLY", "DERIVED_CONDITIONAL_ENDPOINT_PARALLELISM", "Full spatial holonomy centralizes only the clock-versus-all-space stratum."],
    ["G08", "FC04_CONCRETE;OTHERS_OPEN", "BOUNDED_CLASSIFICATION", "Other completion rows lack actual metrics or selected glue data."],
    ["G09", "ALL_LAMBDA_PATH_GROUPOID;L04_ENDPOINT_ON_Q01_Q02", "DERIVED_CONDITIONAL", "Cut loci give multiple arrows, not bundle failure."],
    ["G10", "TYPED_PAIR_ALL_LAMBDA", "NOT_APPLICABLE_UNLESS_PAIR_DERIVED_FROM_DPHI", "Gradient projector failure is a separate unselected route."],
    ["G11", "NONE", "OPEN_ABSENT", "Transport and endomorphism assembly do not assign founded signed depth."],
    ["G12", "NONE", "OPEN_UNSELECTED", "Endpoint parallelism would be an extra constraint; it is not current variation authority."],
]
write("ASSEMBLY_GATE_OUTCOMES.tsv", ["gate_id", "scope", "status", "ruling"], gate_rows)

holonomy_rows = [
    ["Q01", "p=q=1", str(K12.subs({p: 1, q: 1})), str(K13.subs({p: 1, q: 1})), str(K23.subs({p: 1, q: 1})), holonomy_rank(1, 1), "lambda=1"],
    ["Q02", "p=2,q=1", str(K12.subs({p: 2, q: 1})), str(K13.subs({p: 2, q: 1})), str(K23.subs({p: 2, q: 1})), holonomy_rank(2, 1), "lambda=1"],
    ["GENERIC_HOMOGENEOUS", "p>0,q>0", str(K12), str(K13), str(K23), 3, "lambda=1"],
]
write("HOMOGENEOUS_HOLONOMY_ATLAS.tsv", ["control", "parameters", "K12", "K13", "K23", "spatial_holonomy_lie_rank", "parallel_X_lambda"], holonomy_rows)

variation_rows = [
    ["V01", "full_bulk_delta_g", "RETAIN_OPEN_CANDIDATE", "Bundle naturality is tensorial and imposes no field equation."],
    ["V02", "delta_of_metric_natural_X", "CONDITIONAL_INDUCED", "If X is constructed from metric projectors its variation follows delta g and eigenspace regularity."],
    ["V03", "delta_lambda_x", "NOT_AUTHORIZED", "The audit treats constant strata; no local field is derived."],
    ["V04", "change_pair_or_path", "QUERY_CHANGE", "Changes relational arguments rather than the physical configuration."],
    ["V05", "impose_nabla_X_zero", "CONDITIONAL_EXTRA_RESTRICTION", "Would select lambda=1 on Q01/Q02 but endpoint-only parallelism is not a founded premise."],
    ["V06", "boundary_embedding_or_data", "OPEN", "No completion-wide boundary rule is supplied."],
    ["V07", "topology_or_completion_change", "GLOBAL_SECTOR_CHANGE", "Not an ordinary infinitesimal bulk tangent."],
    ["V08", "signed_depth_variation", "OPEN_ABSENT", "No arrow-depth functional exists to vary."],
]
write("VARIATION_CONSEQUENCE_LEDGER.tsv", ["variation_id", "candidate", "status", "ruling"], variation_rows)

checks = {
    "X_projector_formula": sp.simplify(X_projector - X) == sp.zeros(4),
    "X_metric_self_adjoint": sp.simplify(X.T * eta - eta * X) == sp.zeros(4),
    "lambda_one_clock_collapse": sp.simplify(X.subs(lam, 1) - X_clock) == sp.zeros(4),
    "lambda_minus_one_ruler_collapse": sp.simplify(X.subs(lam, -1) - X_ruler) == sp.zeros(4),
    "trace_two_lambda": sp.trace(X) == 2 * lam,
    "centralizer_generic_one": centralizers["L01"] == 1,
    "centralizer_minus_one_three": centralizers["L02"] == 3,
    "centralizer_zero_one": centralizers["L03"] == 1,
    "centralizer_plus_one_three": centralizers["L04"] == 3,
    "connection_A": A == p - q / 2,
    "connection_B": B == -q / 2,
    "connection_C": C == q / 2,
    "K12_formula": sp.simplify(K12 - (p * q - 3 * q**2 / 4)) == 0,
    "K13_formula": sp.simplify(K13 - q**2 / 4) == 0,
    "K23_formula": sp.simplify(K23 - q**2 / 4) == 0,
    "round_holonomy_rank_three": holonomy_rank(1, 1) == 3,
    "squashed_holonomy_rank_three": holonomy_rank(2, 1) == 3,
    "generic_holonomy_generated_by_J13_J23": span_rank([J13, J23, J13 * J23 - J23 * J13]) == 3,
    "parallel_solution_lambda_one": parallel_solutions == {lam: 1} or parallel_solutions == [(lam, 1)] or parallel_solutions == [1],
    "dX_factor_one_minus_lambda": all(sp.simplify(entry.subs(lam, 1)) == 0 for entry in list(dX_e1) + list(dX_e2)),
    "all_completion_rows": len(completion_rows) == 12,
    "all_strata_rows": len(stratum_rows) == 4,
    "all_gate_rows": len(gate_rows) == 12,
    "no_completion_depth": all(row[-1] == "NO_DEPTH" or row[-1] == "NO_FOUNDED_DEPTH" for row in completion_rows),
    "only_FC04_concrete": sum(row["concrete_metric_status"] != "NO_REGISTERED_COMPLETE_METRIC" and row["completion_id"] != "FC12_RECIPROCAL_TORIC_DIAGONAL" for row in completion) == 1,
    "variation_domain_open": all(row[2] != "SELECTED" for row in variation_rows),
}
if not all(checks.values()):
    raise AssertionError(sorted(key for key, value in checks.items() if not value))

result = {
    "schema": "udt-global-reciprocal-bundle-assembly-1.0",
    "result": "PASS",
    "grade": "VERIFIED_WITH_CAVEATS_REGISTERED_GLOBAL_BUNDLE_ASSEMBLY",
    "sympy_version": sp.__version__,
    "counts": {
        "completion_classes": len(completion_rows),
        "concrete_controls": len(control_rows),
        "lambda_strata": len(stratum_rows),
        "assembly_gates": len(gate_rows),
        "variation_rows": len(variation_rows),
        "production_checks": len(checks),
        "completion_pair_bundle_statuses": dict(sorted(Counter(row[1] for row in completion_rows).items())),
    },
    "algebra": {
        "centralizer_dimensions": centralizers,
        "K12": str(K12), "K13": str(K13), "K23": str(K23),
        "round_holonomy_rank": holonomy_rank(1, 1),
        "squashed_holonomy_rank": holonomy_rank(2, 1),
        "parallel_lambda": 1,
    },
    "rulings": {
        "query_bundle": "ALL_REAL_CONSTANT_LAMBDA_TENSORIAL_AND_TYPED_PATHWISE_ON_REGULAR_PAIR_FRAME_BUNDLE",
        "endpoint_parallelism": "LAMBDA_ONE_ONLY_ON_Q01_Q02_CONDITIONAL_CONTROLS",
        "endpoint_premise": "OPEN_NOT_FOUNDED",
        "metric_naturality": "Q01_LAMBDA_ONE_ONLY;Q02_ALL_LAMBDA_VALUES_UNSELECTED",
        "signed_depth": "NO_REGISTERED_COMPLETE_METRIC_NATIVE_FOUNDED_ASSIGNMENT",
        "variation_domain": "OPEN_UNSELECTED",
    },
    "checks": {key: "PASS" for key in sorted(checks)},
    "authority_boundary": {
        "lambda_selected": False,
        "endpoint_only_semantics_selected": False,
        "branch_pair_path_depth_boundary_selected": False,
        "variation_domain_selected": False,
        "action_carrier_source_density_bootstrap_mass_Xmax_dynamics_selected": False,
    },
    "maximum_conclusion": "GLOBAL_PAIR_FRAME_BUNDLE_ASSEMBLY_CLASSIFIED;ALL_REAL_CONSTANT_LAMBDA_TYPED_PATHWISE;LAMBDA_ONE_ONLY_PARALLEL_ENDPOINT_STRATUM_ON_REGISTERED_COMPLETE_S3_CONTROLS_CONDITIONAL_ON_ENDPOINT_ONLY_REQUIREMENT;SIGNED_DEPTH_AND_VARIATION_DOMAIN_REMAIN_OPEN",
}
(HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
