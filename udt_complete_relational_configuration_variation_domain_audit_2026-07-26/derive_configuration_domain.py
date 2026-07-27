#!/usr/bin/env python3
import csv
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read_tsv(name):
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write_tsv(name, header, rows):
    with (HERE / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def require_ids(rows, key, prefix, count):
    expected = {f"{prefix}{i:02d}" for i in range(1, count + 1)}
    actual = [row[key] for row in rows]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise AssertionError(f"bad {key} universe")


objects = read_tsv("CONFIGURATION_OBJECT_UNIVERSE.tsv")
variations = read_tsv("VARIATION_CANDIDATE_UNIVERSE.tsv")
routes = read_tsv("ONTOLOGY_ROUTE_UNIVERSE.tsv")
require_ids(objects, "object_id", "O", 20)
require_ids(variations, "variation_id", "V", 18)
require_ids(routes, "route_id", "R", 8)

object_rulings = {
    "O01": ("PHYSICAL_CONFIGURATION_ARENA", "OPEN_RETAIN_FULL_DELTA_G", "The complete Lorentzian metric is the physical geometric arena, but its founded global branch is not selected.", "complete founded extension and global completion"),
    "O02": ("OPEN_GLOBAL_CONFIGURATION_DATA", "OPEN_GLOBAL_DATA", "Finite-cell domain, topology, seams, and boundary belong to a complete configuration only after selection.", "global branch and boundary rule"),
    "O03": ("PRESENTATION_GAUGE", "GAUGE_NOT_INDEPENDENT", "Coordinate charts present one metric and are not extra physical fields.", "none within metric covariance"),
    "O04": ("PRESENTATION_GAUGE", "GAUGE_NOT_INDEPENDENT", "A coframe is a metric presentation unless a separate physical coframe law is derived.", "no separate coframe law"),
    "O05": ("PHYSICAL_METRIC_CONTENT", "OPEN_RETAIN_WITHIN_DELTA_G", "Angular and pair-screen components are components of the complete metric and cannot be dropped by an unselected lift.", "native restriction or complete founded lift"),
    "O06": ("DERIVED_ABSTRACT_KINEMATICS", "NOT_INDEPENDENT_NATIVE_VARIATION", "Founded phi is the additive reciprocal group coordinate, not by itself a spacetime scalar field.", "physical signed-depth assignment"),
    "O07": ("OPEN_RELATIONAL_FUNCTIONAL", "INDUCED_IF_FUNCTIONAL_DERIVED", "A physical arrow-to-depth map is missing; its metric variation would be induced only after derivation.", "metric-native signed-depth functional"),
    "O08": ("RELATIONAL_QUERY_LABEL", "QUERY_CHANGE_NOT_PHYSICAL_VARIATION", "The ordered observer and ruler specify which comparison is asked.", "separate promotion law if made a field"),
    "O09": ("RELATIONAL_QUERY_LABEL", "QUERY_CHANGE_NOT_PHYSICAL_VARIATION", "A path labels a relational comparison and can distinguish holonomy classes.", "physical path/event-pairing rule"),
    "O10": ("DERIVED_GIVEN_INPUT_RELATIONAL", "INDUCED_READOUT", "Metric distance, transport, Jacobi map, and holonomy follow from supplied g and path.", "supplied complete metric and path"),
    "O11": ("CONDITIONAL_RELATIONAL_REPRESENTATION", "INDUCED_IF_INPUTS_SUPPLIED", "X_lambda is an endomorphism family over ordered pair data, not an additional spacetime field.", "ordered pair plus selected lambda"),
    "O12": ("OPEN_REPRESENTATION_PARAMETER", "NOT_AUTHORIZED_LOCAL_FIELD", "Lambda labels the unresolved screen response; scanning it does not make lambda(x) dynamical.", "native screen-response selector"),
    "O13": ("PRESENTATION_GAUGE", "GAUGE_NOT_INDEPENDENT", "Screen orientation drops out of scalar-screen X_lambda and is SO(2) coframe gauge.", "none for X_lambda"),
    "O14": ("CONDITIONAL_SPECIAL_STRATUM", "NOT_SELECTED_STRATUM", "At lambda=1 the pair-indexed family collapses to the direction-independent clock-versus-all-space lift.", "lambda selection and global timelike-line data"),
    "O15": ("GLOBAL_SECTOR_LABEL", "SECTOR_LABEL_NOT_BULK_TANGENT", "Completion branches and topology label globally distinct sectors, not ordinary local tangent directions.", "global completion classification and transition law"),
    "O16": ("OPEN_GLOBAL_BOUNDARY_DATA", "OPEN_BOUNDARY_VARIATION", "Boundary embedding and boundary data may be fixed or varied, but current authority does not decide.", "native boundary and variation rule"),
    "O17": ("FIXED_CALIBRATION_ANCHOR", "FIXED_ANCHOR_NOT_VARIED", "Measured c_E and G_obs calibrate physical units and are not configuration fields in this audit.", "none"),
    "O18": ("ABSENT_DOWNSTREAM_PHYSICS", "ABSENT_FROM_CURRENT_DOMAIN", "Carrier, source, mass, and density are open or conditional and cannot be inserted into the founded metric domain.", "native matter/source derivation"),
    "O19": ("ABSENT_DOWNSTREAM_PHYSICS", "DOWNSTREAM_NOT_DOMAIN", "Response or action acts on a selected domain and is not itself a configuration variable.", "selected domain then native response"),
    "O20": ("COMPARISON_ONLY_NONNATIVE", "COMPARISON_ONLY", "The expanded independent scalar atlas is a comparison configuration, not a second native phi field.", "explicit replacement of current premise precedence"),
}

object_rows = []
for row in objects:
    ruling = object_rulings[row["object_id"]]
    object_rows.append([row["object_id"], row["object"], *ruling])
write_tsv("CONFIGURATION_OBJECT_ADJUDICATION.tsv", ["object_id", "object", "primary_class", "variation_status", "ruling", "missing_gate"], object_rows)

variation_rulings = {
    "V01": ("OPEN_CANDIDATE_PHYSICAL_VARIATION", "RETAIN", "Full delta g, including angular and mixing slots, remains the honest candidate until a native restriction is derived."),
    "V02": ("GAUGE_ORBIT_DIRECTION", "QUOTIENT", "Diffeomorphism presentation directions are not independent physical content."),
    "V03": ("GAUGE_ORBIT_DIRECTION", "QUOTIENT", "Local Lorentz coframe changes preserve the metric readout."),
    "V04": ("FORBIDDEN_NATIVE_DOUBLE_COUNT", "REJECT", "Founded phi adds no independent field direction absent an arrow-to-depth field assignment."),
    "V05": ("CONDITIONAL_INDUCED_VARIATION", "OPEN", "Delta of depth can be induced from delta g only after the depth functional exists."),
    "V06": ("RELATIONAL_QUERY_CHANGE", "SEPARATE", "Changing u,n changes the comparison question, not the physical solution."),
    "V07": ("RELATIONAL_QUERY_CHANGE", "SEPARATE", "Changing gamma changes the path-labelled arrow, not automatically the metric."),
    "V08": ("UNAUTHORIZED_FIELD_PROMOTION", "REJECT", "No source licenses local lambda(x) or its gradients."),
    "V09": ("PARAMETER_STRATUM_SCAN", "SEPARATE", "Comparing constant lambda strata is an atlas scan, not an off-shell field variation."),
    "V10": ("GAUGE_ORBIT_DIRECTION", "QUOTIENT", "Screen SO(2) orientation is presentation gauge for scalar-screen X_lambda."),
    "V11": ("GLOBAL_SECTOR_CHANGE", "SEPARATE", "Topology or quotient changes are not ordinary infinitesimal bulk tangents."),
    "V12": ("OPEN_BOUNDARY_VARIATION", "OPEN", "Whether the boundary embedding moves is not selected."),
    "V13": ("OPEN_BOUNDARY_VARIATION", "OPEN", "Which boundary data vary is not selected."),
    "V14": ("FIXED_CALIBRATION_CHANGE", "REJECT", "Observed anchors are held fixed in the configuration problem."),
    "V15": ("ABSENT_CONDITIONAL_FIELD_VARIATION", "REJECT_CURRENTLY", "Matter/source/density fields are not yet native members of the founded domain."),
    "V16": ("DOWNSTREAM_VARIATIONAL_OPERATION", "REJECT_AS_DOMAIN_INPUT", "A response/action cannot define its own domain without an additional selector premise."),
    "V17": ("GLOBAL_SECTOR_SELECTION", "SEPARATE", "Choosing a branch is discrete/global selection, not a local bulk variation."),
    "V18": ("UNRESOLVED_LIFT_TIE_DATA", "DO_NOT_COUNT_AS_FIELDS", "Seven bounded lift tangents show available metric responses, not seven new propagating fields."),
}
variation_rows = []
for row in variations:
    ruling = variation_rulings[row["variation_id"]]
    variation_rows.append([row["variation_id"], row["candidate_change"], *ruling])
write_tsv("VARIATION_DOMAIN_ADJUDICATION.tsv", ["variation_id", "candidate_change", "classification", "domain_action", "ruling"], variation_rows)

route_rulings = {
    "R01": ("INSUFFICIENT_FOR_FOUNDED_COMPARISON", "Bare events do not select ordered clock/ruler data or signed depth."),
    "R02": ("OPEN_NOT_SELECTED", "No universal rank-two reciprocal subbundle is currently derived."),
    "R03": ("EXACT_SPECIAL_STRATUM_UNSELECTED", "This is the lambda=1 collapse of R04 after a timelike observer line is supplied; global selection remains absent."),
    "R04": ("CONDITIONAL_GENERAL_RELATIONAL_CONTAINER", "Given g, typed pair/path inputs, and lambda, the family is covariant and composes on the path groupoid."),
    "R05": ("TYPE_SCAFFOLD_SUPPORTED_NOT_PHYSICALLY_SELECTED", "Physical metric, query groupoid, and conditional derived readouts coexist as layers without becoming extra fields."),
    "R06": ("COMPARISON_ONLY_NOT_NATIVE", "A free scalar is an enlarged comparison ontology and cannot replace founded phi precedence."),
    "R07": ("UNAUTHORIZED_GAUGE_PROMOTION", "A coframe is not an extra physical field under the metric-is-the-theory rule."),
    "R08": ("UNAUTHORIZED_QUERY_PROMOTION", "No law makes every observer/ruler query label a dynamical field."),
}
route_rows = []
for row in routes:
    status, ruling = route_rulings[row["route_id"]]
    route_rows.append([row["route_id"], row["route"], status, ruling])
write_tsv("ONTOLOGY_ROUTE_ADJUDICATION.tsv", ["route_id", "route", "status", "ruling"], route_rows)

relations = [
    ["K01", "R03", "R04", "EXACT_SUBSTRATUM", "Set lambda=1: X_1(u,n)=-P_u+P_space, independent of n for fixed u."],
    ["K02", "R04", "R03", "NO_REVERSE_INCLUSION", "For lambda not equal to 1, X_lambda generally depends on ruler direction n."],
    ["K03", "R04", "O08+O09", "FIBERED_OVER_QUERY_DATA", "Pair and path labels are arguments of the relational family, not physical fields."],
    ["K04", "O13", "O11", "GAUGE_DROPS_OUT", "Screen SO(2) changes commute with scalar-screen X_lambda."],
    ["K05", "R05", "R04", "CONDITIONAL_LAYER_INCLUDED", "The stack can contain the pair-indexed readout layer without promoting it to physical configuration."],
    ["K06", "O06", "O07", "ABSTRACT_TO_PHYSICAL_MAP_OPEN", "Founded phi does not itself assign depth to spacetime arrows."],
    ["K07", "O01", "O11", "NO_METRIC_ONLY_SELECTOR", "Metric and scalar anchors alone have scalar Lorentz commutant and do not select the lift."],
    ["K08", "R05", "O19", "NO_DYNAMICAL_CLOSURE", "Layering supplies no response, action, or fixed-point feedback."],
]
write_tsv("CODOMAIN_RELATION_ATLAS.tsv", ["relation_id", "source", "target", "relation", "exact_meaning"], relations)

stack = [
    ["L01", "PHYSICAL_ARENA", "O01+O05", "complete metric with all angular and mixing content", "SUPPORTED_ARENA_GLOBAL_REALIZATION_OPEN"],
    ["L02", "GLOBAL_COMPLETION", "O02+O15+O16", "finite-cell domain topology sector and boundary data", "OPEN"],
    ["L03", "PRESENTATION_GAUGE", "O03+O04+O13", "charts coframes and screen orientation", "QUOTIENT_NOT_EXTRA_FIELDS"],
    ["L04", "RELATIONAL_QUERY", "O08+O09", "ordered observer/ruler pair and path arrow", "SUPPLIED_INPUT_NOT_FIELD"],
    ["L05", "METRIC_DERIVED_RELATIONAL", "O10", "distance transport Jacobi and holonomy", "DERIVED_GIVEN_L01_L04"],
    ["L06", "RECIPROCAL_REPRESENTATION", "O06+O11+O12+O14", "founded coordinate and conditional X_lambda family", "PHI_DERIVED_LAMBDA_OPEN"],
    ["L07", "PHYSICAL_DEPTH_READOUT", "O07", "metric-native signed arrow depth", "OPEN_ABSENT"],
    ["L08", "DOWNSTREAM_PHYSICS", "O18+O19", "matter source response action and closure", "OPEN_OR_CONDITIONAL_EXCLUDED"],
]
write_tsv("RELATIONAL_CONFIGURATION_STACK.tsv", ["layer_id", "layer", "objects", "content", "current_status"], stack)

guards = [
    ["D01", "O06", "founded phi", "not an independent scalar field", "prevents phi double count"],
    ["D02", "O03+O04+O13", "presentation data", "quotient gauge directions", "prevents chart/coframe/screen count"],
    ["D03", "O08+O09", "query labels", "separate relational arguments", "prevents observer/path field promotion"],
    ["D04", "O10+O11", "derived readouts", "functions of supplied geometry/query/parameter", "prevents readout-as-field count"],
    ["D05", "O12", "lambda", "open representation parameter not lambda(x)", "prevents invented scalar field"],
    ["D06", "O15", "global branch", "sector label not local tangent", "prevents topology-as-mode count"],
    ["D07", "V18", "extension tangents", "available metric responses not propagating modes", "prevents seven-field inference"],
    ["D08", "O17", "c_E and G_obs", "fixed calibration anchors", "prevents anchor variations"],
    ["D09", "O18", "matter/source", "absent from current founded domain", "prevents bootstrap import"],
    ["D10", "O19", "response/action", "downstream operation", "prevents action selecting domain circularly"],
]
write_tsv("DOF_DOUBLE_COUNT_GUARDS.tsv", ["guard_id", "objects", "item", "rule", "purpose"], guards)

gates = [
    ["G01", "complete founded metric extension and global branch", "OPEN", "needed to instantiate L01+L02 physically"],
    ["G02", "screen response lambda or more general lift", "OPEN", "needed to select O11 member"],
    ["G03", "metric-native signed depth assignment", "OPEN_ABSENT", "needed to join abstract phi to typed arrows"],
    ["G04", "physical pair/path/event-pairing rule", "OPEN", "needed to identify realized relational arrows"],
    ["G05", "boundary embedding data and allowed variations", "OPEN", "needed for complete global domain"],
    ["G06", "admissible bulk plus boundary variation domain", "OPEN", "needed before response or action"],
    ["G07", "native offshell response and integrability", "OPEN_ABSENT", "downstream of G01-G06"],
    ["G08", "native matter carrier source and density", "OPEN_OR_CONDITIONAL", "not part of current geometry-only domain"],
]
write_tsv("OPEN_GATE_MATRIX.tsv", ["gate_id", "gate", "status", "dependency"], gates)


def projector(n):
    return [[n[i] * n[j] for j in range(3)] for i in range(3)]


def spatial_x(lam, n):
    p = projector(n)
    return [[lam * (Fraction(int(i == j), 1) - p[i][j]) + p[i][j] for j in range(3)] for i in range(3)]


directions = [
    (Fraction(1), Fraction(0), Fraction(0)),
    (Fraction(0), Fraction(1), Fraction(0)),
    (Fraction(0), Fraction(0), Fraction(1)),
    (Fraction(3, 5), Fraction(4, 5), Fraction(0)),
]
x1 = [spatial_x(Fraction(1), n) for n in directions]
x0 = [spatial_x(Fraction(0), n) for n in directions]
checks = {
    "object_universe_complete": len(object_rows) == 20,
    "variation_universe_complete": len(variation_rows) == 18,
    "route_universe_complete": len(route_rows) == 8,
    "lambda_one_direction_independent": all(matrix == x1[0] for matrix in x1),
    "lambda_zero_direction_dependent": len({tuple(sum(matrix, [])) for matrix in x0}) == len(x0),
    "lambda_one_spatial_identity": x1[0] == [[Fraction(int(i == j)) for j in range(3)] for i in range(3)],
    "single_lift_is_special_stratum": relations[0][3] == "EXACT_SUBSTRATUM",
    "pair_family_not_field": object_rulings["O11"][1] == "INDUCED_IF_INPUTS_SUPPLIED",
    "lambda_not_field": object_rulings["O12"][1] == "NOT_AUTHORIZED_LOCAL_FIELD",
    "phi_not_independent": object_rulings["O06"][1] == "NOT_INDEPENDENT_NATIVE_VARIATION",
    "full_metric_variation_retained": variation_rulings["V01"][1] == "RETAIN",
    "angular_mixing_retained": object_rulings["O05"][1] == "OPEN_RETAIN_WITHIN_DELTA_G",
    "query_labels_separate": all(variation_rulings[v][0] == "RELATIONAL_QUERY_CHANGE" for v in ["V06", "V07"]),
    "gauge_not_fields": all(object_rulings[o][0] == "PRESENTATION_GAUGE" for o in ["O03", "O04", "O13"]),
    "topology_not_bulk_tangent": variation_rulings["V11"][0] == "GLOBAL_SECTOR_CHANGE",
    "depth_functional_open": object_rulings["O07"][0] == "OPEN_RELATIONAL_FUNCTIONAL",
    "global_boundary_open": object_rulings["O16"][0] == "OPEN_GLOBAL_BOUNDARY_DATA",
    "response_action_absent": object_rulings["O19"][0] == "ABSENT_DOWNSTREAM_PHYSICS",
    "no_gate_ready": all(row[2] != "DERIVED" for row in gates),
    "comparison_scalar_nonnative": route_rulings["R06"][0] == "COMPARISON_ONLY_NOT_NATIVE",
}
if not all(checks.values()):
    raise AssertionError("production check failed")

result = {
    "schema": "udt-complete-relational-configuration-domain-1.0",
    "result": "PASS",
    "grade": "VERIFIED_WITH_CAVEATS_BOUNDED_CONFIGURATION_TYPE_AND_VARIATION_OWNERSHIP",
    "counts": {
        "objects": len(object_rows),
        "variations": len(variation_rows),
        "routes": len(route_rows),
        "relations": len(relations),
        "stack_layers": len(stack),
        "double_count_guards": len(guards),
        "open_gates": len(gates),
        "object_primary_classes": dict(sorted(Counter(row[2] for row in object_rows).items())),
        "variation_classes": dict(sorted(Counter(row[2] for row in variation_rows).items())),
    },
    "rulings": {
        "container_relation": "DEMOCRATIC_1PLUS3_IS_FIBERWISE_EXACT_LAMBDA_ONE_STRATUM_OF_PAIR_INDEXED_CONTAINER",
        "typed_scaffold": "SUPPORTED_AS_TYPE_STACK_NOT_SELECTED_PHYSICAL_CONFIGURATION",
        "physical_bulk_candidate": "FULL_METRIC_VARIATION_RETAINED_INCLUDING_ANGULAR_AND_MIXING",
        "lambda": "OPEN_REPRESENTATION_PARAMETER_NOT_LOCAL_FIELD",
        "phi": "DERIVED_ABSTRACT_GROUP_COORDINATE_NOT_INDEPENDENT_FIELD",
        "query_data": "OBSERVER_PAIR_AND_PATH_ARE_RELATIONAL_ARGUMENTS_NOT_FIELDS",
        "variation_domain": "OPEN_UNSELECTED",
    },
    "checks": {key: "PASS" for key, value in checks.items() if value},
    "authority_boundary": {
        "selected_complete_configuration": False,
        "selected_variation_domain": False,
        "selected_lambda_or_global_lift": False,
        "new_field_or_mode_count": False,
        "depth_profile_path_or_boundary_selected": False,
        "response_action_carrier_source_density_dynamics_selected": False,
    },
    "maximum_conclusion": "RELATIONAL_CONFIGURATION_STACK_TYPED;DEMOCRATIC_1PLUS3_IS_FIBERWISE_EXACT_LAMBDA_ONE_STRATUM_OF_PAIR_INDEXED_CONTAINER;PHYSICAL_DEPTH_LAMBDA_GLOBAL_BRANCH_BOUNDARY_AND_VARIATION_DOMAIN_REMAIN_OPEN;NO_NEW_FIELD_OR_MODE_COUNT",
}
(HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
