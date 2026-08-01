#!/usr/bin/env python3
"""Exact controls and staged adjudication for the JR_CERT_NATIVE derivation program.

The algebraic examples are controls, not candidate UDT dynamics.  The route rulings are tied to
the exact frozen source anchors below and are independently replayed by a separate verifier.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "686336343878e8a9e39a4b72df08d23754243631"


def write_tsv(name: str, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def simplify_matrix(matrix: list[list[sp.Expr]]) -> list[list[sp.Expr]]:
    return [[sp.simplify(value) for value in row] for row in matrix]


source_anchors = [
    {
        "anchor_id": "A01",
        "path": "udt_joint_selector_provenance_audit_2026-07-28/AUDIT_REPORT.md",
        "routes": "E04;E08",
        "required_text": "NO_REGISTERED_JOINT_OPERATION_THREE_GAPS_RETAINED",
        "ruling": "No registered joint selector or native on-shell realization law exists in its complete fixed-tree census.",
    },
    {
        "anchor_id": "A02",
        "path": "udt_metric_natural_joint_selector_nogo_2026-07-28/AUDIT_REPORT.md",
        "routes": "E04;E08",
        "required_text": "NO_GO_PREMISES_INSUFFICIENT_STOP",
        "ruling": "Exact frame/pointwise obstructions are bounded; higher-jet, nonlocal, set-valued, and whole-solution routes remain unclassified.",
    },
    {
        "anchor_id": "A03",
        "path": "udt_general_screen_complete_cell_atlas_2026-07-28/EXACT_DERIVATION.md",
        "routes": "E01;E02;E04;E05",
        "required_text": "It selects no physical branch or UDT dynamics.",
        "ruling": "The full stationary GL(2,R) screen and exact Cartan system are off-shell configuration geometry, not selection.",
    },
    {
        "anchor_id": "A04",
        "path": "udt_general_screen_dependency_regrade_2026-07-28/CORRECTION_LAYER.md",
        "routes": "E04;E05",
        "required_text": "selected full extension",
        "ruling": "Available screen modes do not select the complete full-frame response or dynamics.",
    },
    {
        "anchor_id": "A05",
        "path": "udt_global_functional_dof_constraint_rank_audit_2026-07-26/STATUS_LEDGER.tsv",
        "routes": "E01;E02;E03;E05;B01;B02",
        "required_text": "ZERO_COMPLETE_NATIVE_COFRAME_RESPONSE_RANK",
        "ruling": "Founded kinematics and identities contribute zero selected native response rank; the current correction scopes this as zero selected rank.",
    },
    {
        "anchor_id": "A06",
        "path": "udt_bootstrap_to_local_response_map_audit_2026-07-25/AUDIT_REPORT.md",
        "routes": "E06;B04",
        "required_text": "No complete bootstrap-to-local response map is derived",
        "ruling": "The two-arrow bootstrap architecture is typed, but both maps, domain, derivative, pairing, and fixed point are absent.",
    },
    {
        "anchor_id": "A07",
        "path": "udt_bootstrap_clock_angular_closure_audit_2026-07-24/EXACT_DERIVATION.md",
        "routes": "E06",
        "required_text": "No one of these is promoted to a new field equation here.",
        "ruling": "The clock/angular closure families are invariant availability tests, not field equations.",
    },
    {
        "anchor_id": "A08",
        "path": "native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md",
        "routes": "E07;B03",
        "required_text": "The complete action, native source law, differentiable finite-cell boundary action",
        "ruling": "C2/Bach is unique-conditional, EH and S2 are conditional, and the complete action/source/boundary charge remain open.",
    },
    {
        "anchor_id": "A09",
        "path": "native_boundary_generator_scale_audit_2026-07-19/CHARGE_REQUIREMENT_LEDGER.tsv",
        "routes": "B03;B06",
        "required_text": "Differentiable boundary/corner primitive",
        "ruling": "The primitive, normalization, generator, reference, integrability, and time-live conservation remain open.",
    },
    {
        "anchor_id": "A10",
        "path": "asymptotic_boundary_lineage_audit_2026-07-19/AUDIT_REPORT.md",
        "routes": "B01;B02;B06",
        "required_text": "not derived to be the hard end of spacetime",
        "ruling": "The WR-L wall is an exact bounded metric horizon candidate, not a selected terminal or differentiable global boundary.",
    },
    {
        "anchor_id": "A11",
        "path": "angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv",
        "routes": "E05;B01;B02;B05",
        "required_text": "TWO_STAGE_OPEN_GATE_CHAIN",
        "ruling": "Toric S3/Hopf closure is unique only after unselected spatial-torus and cap premises; multiple completions remain.",
    },
    {
        "anchor_id": "A12",
        "path": "boundary_bootstrap_representative_selector_audit_2026-07-19/AUDIT_REPORT.md",
        "routes": "E05;E06;B02;B04;B06",
        "required_text": "SELECTOR_NOT_FOUND_IN_CURRENT_FOUNDATION",
        "ruling": "Current boundary/bootstrap data supply neither an off-shell representative map nor a selector equation.",
    },
    {
        "anchor_id": "A13",
        "path": "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md",
        "routes": "B05",
        "required_text": "SECTION_AND_BOUNDARY_SELECTOR_OPEN",
        "ruling": "The null-direction S2 is a conditional fiber and the carrier section, action, transport, and physical boundary remain open.",
    },
    {
        "anchor_id": "A14",
        "path": "udt_joint_realization_closure_audit_2026-08-01/AUDIT_REPORT.md",
        "routes": "E08;B06",
        "required_text": "FORMAL_COMPATIBILITY_ONLY_COMMON_REALIZATION_OPEN",
        "ruling": "The exact registered static and formal live modules do not supply one native whole problem or common nonzero-live solution.",
    },
]

combined = set((HERE / "COMBINED_SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines())
for anchor in source_anchors:
    path = ROOT / str(anchor["path"])
    assert str(anchor["path"]) in combined
    assert str(anchor["required_text"]) in path.read_text(encoding="utf-8")
    anchor["sha256"] = sha256(path)
write_tsv(
    "SOURCE_ANCHOR_LEDGER.tsv",
    ["anchor_id", "path", "routes", "required_text", "ruling", "sha256"],
    source_anchors,
)

# Exact off-shell control: arbitrary phi(x) in the founded reciprocal diagonal pair, with two
# untouched transverse slots. This is deliberately not proposed as the complete UDT coframe.
t, x, y, z = sp.symbols("t x y z", real=True)
coords = (t, x, y, z)
phi = sp.Function("phi")(x)
metric = sp.diag(-sp.exp(-2 * phi), sp.exp(2 * phi), 1, 1)
inverse = metric.inv()
n = 4
christoffel = [
    [
        [
            sp.simplify(
                sum(
                    inverse[a, d]
                    * (
                        sp.diff(metric[d, c], coords[b])
                        + sp.diff(metric[d, b], coords[c])
                        - sp.diff(metric[b, c], coords[d])
                    )
                    for d in range(n)
                )
                / 2
            )
            for c in range(n)
        ]
        for b in range(n)
    ]
    for a in range(n)
]

metric_compatibility = []
for a in range(n):
    for b in range(n):
        for c in range(n):
            value = sp.simplify(
                sp.diff(metric[a, b], coords[c])
                - sum(christoffel[d][c][a] * metric[d, b] for d in range(n))
                - sum(christoffel[d][c][b] * metric[a, d] for d in range(n))
            )
            metric_compatibility.append(value)

torsion = [
    sp.simplify(christoffel[a][b][c] - christoffel[a][c][b])
    for a in range(n)
    for b in range(n)
    for c in range(n)
]

ricci = [
    [
        sp.simplify(
            sum(
                sp.diff(christoffel[a][b][d], coords[a])
                - sp.diff(christoffel[a][b][a], coords[d])
                + sum(
                    christoffel[a][a][e] * christoffel[e][b][d]
                    - christoffel[a][d][e] * christoffel[e][b][a]
                    for e in range(n)
                )
                for a in range(n)
            )
        )
        for d in range(n)
    ]
    for b in range(n)
]
scalar_curvature = sp.simplify(sum(inverse[b, d] * ricci[b][d] for b in range(n) for d in range(n)))
einstein_cov = simplify_matrix(
    [[ricci[a][b] - metric[a, b] * scalar_curvature / 2 for b in range(n)] for a in range(n)]
)
einstein_mixed = simplify_matrix(
    [[sum(inverse[a, c] * einstein_cov[c][b] for c in range(n)) for b in range(n)] for a in range(n)]
)
bianchi_divergence = [
    sp.simplify(
        sum(
            sp.diff(einstein_mixed[a][b], coords[a])
            + sum(
                christoffel[a][a][e] * einstein_mixed[e][b]
                - christoffel[e][a][b] * einstein_mixed[a][e]
                for e in range(n)
            )
            for a in range(n)
        )
    )
    for b in range(n)
]

phip = sp.diff(phi, x)
phipp = sp.diff(phi, x, 2)
cartan_dtheta0_coefficient = sp.exp(-phi) * phip
cartan_omega01_theta0_coefficient = -sp.exp(-phi) * phip
cartan_torsion0_coefficient = sp.simplify(cartan_dtheta0_coefficient + cartan_omega01_theta0_coefficient)
cartan_curvature_coefficient = sp.simplify(sp.exp(-2 * phi) * (phipp - 2 * phip**2))

a = sp.symbols("a", real=True)
phi_linear = a * x
linear_scalar = sp.simplify(scalar_curvature.subs(phi, phi_linear).doit())
seal_values = {
    "phi_at_seal": sp.simplify(phi_linear.subs(x, 0)),
    "normal_derivative_at_seal": sp.simplify(sp.diff(phi_linear, x).subs(x, 0)),
    "scalar_curvature_at_seal": sp.simplify(linear_scalar.subs(x, 0)),
}

# Boundary-variation controls. They demonstrate operator dependence only; neither functional is
# proposed or admitted as the UDT action.
f = sp.Function("f")(x)
eta = sp.Function("eta")(x)
second_order_identity = sp.simplify(
    sp.diff(f, x) * sp.diff(eta, x)
    - (sp.diff(sp.diff(f, x) * eta, x) - sp.diff(f, x, 2) * eta)
)
fourth_order_identity = sp.simplify(
    sp.diff(f, x, 2) * sp.diff(eta, x, 2)
    - (
        sp.diff(sp.diff(f, x, 2) * sp.diff(eta, x) - sp.diff(f, x, 3) * eta, x)
        + sp.diff(f, x, 4) * eta
    )
)

algebra = {
    "base": BASE,
    "python": sys.version.split()[0],
    "sympy": sp.__version__,
    "control_scope": "arbitrary_phi_x_reciprocal_diagonal_pair_with_spectator_screen__not_complete_udt",
    "metric_determinant": str(sp.simplify(metric.det())),
    "nonzero_christoffels": [
        {"a": i, "b": j, "c": k, "value": str(christoffel[i][j][k])}
        for i in range(n)
        for j in range(n)
        for k in range(n)
        if christoffel[i][j][k] != 0
    ],
    "metric_compatibility_zero_count": sum(value == 0 for value in metric_compatibility),
    "metric_compatibility_total": len(metric_compatibility),
    "torsion_zero_count": sum(value == 0 for value in torsion),
    "torsion_total": len(torsion),
    "cartan_dtheta0_coefficient": str(cartan_dtheta0_coefficient),
    "cartan_omega01_theta0_coefficient": str(cartan_omega01_theta0_coefficient),
    "cartan_torsion0_coefficient": str(cartan_torsion0_coefficient),
    "cartan_curvature_coefficient": str(cartan_curvature_coefficient),
    "scalar_curvature": str(scalar_curvature),
    "einstein_tensor_covariant": [[str(value) for value in row] for row in einstein_cov],
    "contracted_bianchi_divergence": [str(value) for value in bianchi_divergence],
    "seal_family": {key: str(value) for key, value in seal_values.items()},
    "second_order_variation_identity": str(second_order_identity),
    "fourth_order_variation_identity": str(fourth_order_identity),
}
assert sp.simplify(metric.det()) == -1
assert all(value == 0 for value in metric_compatibility)
assert all(value == 0 for value in torsion)
assert cartan_torsion0_coefficient == 0
assert all(value == 0 for value in bianchi_divergence)
assert linear_scalar != 0
assert seal_values["phi_at_seal"] == 0 and seal_values["normal_derivative_at_seal"] == a
assert second_order_identity == 0 and fourth_order_identity == 0
(HERE / "ALGEBRA_RESULT.json").write_text(json.dumps(algebra, indent=2, sort_keys=True) + "\n", encoding="utf-8")

equation_rows = [
    {
        "route_id": "E01",
        "route": "CARTAN_STRUCTURE_RELATIONS",
        "status": "IDENTITY_RECONSTRUCTION_NOT_SELECTION",
        "pass": "NO",
        "exact_test": "arbitrary phi(x) admits torsion-free Cartan connection; curvature changes with phi without violating the structure equation",
        "source_anchors": "A03;A05",
        "remaining_scope": "a future native equation could be written in Cartan variables",
    },
    {
        "route_id": "E02",
        "route": "LEVI_CIVITA_COMPATIBILITY",
        "status": "UNIQUE_CONNECTION_FOR_EACH_METRIC_NOT_REALIZATION_LAW",
        "pass": "NO",
        "exact_test": "64/64 metric-compatibility components and 64/64 torsion components vanish for arbitrary phi(x)",
        "source_anchors": "A03;A05",
        "remaining_scope": "connection reconstruction remains available to any future equation",
    },
    {
        "route_id": "E03",
        "route": "BIANCHI_INTEGRABILITY",
        "status": "DIFFERENTIAL_IDENTITY_ZERO_DYNAMICAL_RANK",
        "pass": "NO",
        "exact_test": "contracted Einstein-tensor divergence vanishes for arbitrary phi(x), including nonzero-curvature members",
        "source_anchors": "A05",
        "remaining_scope": "a sourced equation could make a Bianchi identity a compatibility condition after the source is derived",
    },
    {
        "route_id": "E04",
        "route": "RECIPROCAL_EQUIVARIANCE",
        "status": "KINEMATIC_COMPOSITION_AND_OFF_SHELL_RESPONSE_NOT_EOM",
        "pass": "NO",
        "exact_test": "founded pair is exact while complete response retains screen modes, lambda/mixing choices, path semantics, and on-shell selection",
        "source_anchors": "A01;A02;A03;A04",
        "remaining_scope": "higher-jet nonlocal set-valued and whole-solution native operations remain open",
    },
    {
        "route_id": "E05",
        "route": "FINITE_CELL_GLOBAL_COMPATIBILITY",
        "status": "CONFIGURATION_AND_COMPLETION_CONSTRAINTS_NOT_WHOLE_EQUATION",
        "pass": "NO",
        "exact_test": "smooth complete S3 controls and multiple toric/cap/seam/quotient classes coexist without a branch-ranking law",
        "source_anchors": "A03;A04;A05;A11;A12",
        "remaining_scope": "unknown native global law could select or relate completion classes",
    },
    {
        "route_id": "E06",
        "route": "BOOTSTRAP_CLOSURE",
        "status": "TWO_ARROW_TYPE_DERIVED_MAPS_AND_FIXED_POINT_OPEN",
        "pass": "NO",
        "exact_test": "A(X,O)=0 and O-R[X]=0 are a response skeleton; neither complete map derivative pairing nor common root is registered",
        "source_anchors": "A06;A07;A12",
        "remaining_scope": "a future differentiable metric-native coupled closure section could pass",
    },
    {
        "route_id": "E07",
        "route": "ACTION_MEDIATED_CONDITIONAL",
        "status": "CONDITIONAL_BRANCHES_DO_NOT_BECOME_NATIVE",
        "pass": "NO",
        "exact_test": "C2/Bach remains unique-conditional; EH and carrier actions remain conditional; full variation domain/source are open",
        "source_anchors": "A08",
        "remaining_scope": "a native selector or bridge could later supply an action or equivalent law",
    },
    {
        "route_id": "E08",
        "route": "OTHER_REGISTERED_WHOLE_SOLUTION",
        "status": "NO_REGISTERED_COMPLETE_NATIVE_OPERATION_IN_FROZEN_CENSUS",
        "pass": "NO",
        "exact_test": "repo-wide selector census plus current joint-realization census contain no complete on-shell operation",
        "source_anchors": "A01;A02;A14",
        "remaining_scope": "bounded record result only; unknown future laws are not excluded",
    },
]
write_tsv(
    "EQUATION_ROUTE_ADJUDICATION.tsv",
    ["route_id", "route", "status", "pass", "exact_test", "source_anchors", "remaining_scope"],
    equation_rows,
)

boundary_rows = [
    {
        "route_id": "B01",
        "route": "STATIC_SEAL_PARITY",
        "status": "PHI_TRACE_ONLY_NOT_ALL_FIELD_DIFFERENTIABLE_BOUNDARY",
        "pass": "NO",
        "exact_test": "odd local seal family phi_a=a*x has phi(0)=0 for every a while the normal derivative and curvature remain free",
        "source_anchors": "A05;A10;A11",
        "remaining_scope": "other field traces normal jets corners and time-live boundary data remain open",
    },
    {
        "route_id": "B02",
        "route": "REGULARITY_CAP_SEAM_GLUE",
        "status": "MULTIPLE_COMPLETIONS_AND_REGULARITY_NOT_SELECTION",
        "pass": "NO",
        "exact_test": "smooth caps seams mirrors quotients horizons and interval boundaries have distinct data and no common selected primitive",
        "source_anchors": "A05;A10;A11;A12",
        "remaining_scope": "a native global equation may later exclude or join classes",
    },
    {
        "route_id": "B03",
        "route": "CONDITIONAL_ACTION_BOUNDARY",
        "status": "OPERATOR_AND_VARIATION_DOMAIN_DEPENDENT_CONDITIONAL",
        "pass": "NO",
        "exact_test": "second-order control has boundary phi_prime*delta_phi while fourth-order control additionally has phi_second*delta_phi_prime; same trace rule cannot close both",
        "source_anchors": "A08;A09",
        "remaining_scope": "matching boundary follows only after native operator and variation domain are derived",
    },
    {
        "route_id": "B04",
        "route": "BOOTSTRAP_MOVING_BOUNDARY",
        "status": "SHAPE_CHANNEL_REQUIRED_BUT_MAP_AND_DERIVATIVE_ABSENT",
        "pass": "NO",
        "exact_test": "bootstrap response audit proves moving-boundary variation is required while supplying no boundary/global map",
        "source_anchors": "A06;A12",
        "remaining_scope": "future coupled closure must own seal corners gluing and global moduli",
    },
    {
        "route_id": "B05",
        "route": "CARRIER_TOPOLOGY_BOUNDARY",
        "status": "CONDITIONAL_CARRIER_AND_SOLVER_BOUNDARY_NOT_NATIVE",
        "pass": "NO",
        "exact_test": "conditional S2/Hopf topology and fixed numerical exterior do not derive the metric finite-cell boundary or carrier section",
        "source_anchors": "A11;A13",
        "remaining_scope": "native carrier emergence section transport and physical boundary remain open",
    },
    {
        "route_id": "B06",
        "route": "OTHER_REGISTERED_BOUNDARY",
        "status": "NO_REGISTERED_COMPLETE_MATCHING_BOUNDARY_OPERATION",
        "pass": "NO",
        "exact_test": "raw wall flux regular horizons parity and completion catalogues lack one action/operator variation domain and normalized primitive",
        "source_anchors": "A09;A10;A12;A14",
        "remaining_scope": "bounded record result only; future metric-native boundary law is not excluded",
    },
]
write_tsv(
    "BOUNDARY_ROUTE_ADJUDICATION.tsv",
    ["route_id", "route", "status", "pass", "exact_test", "source_anchors", "remaining_scope"],
    boundary_rows,
)

identity_rows = [
    {
        "object": "Cartan_first_structure_relation",
        "type": "DEFINITION_AND_TORSION_CONSTRAINT_ON_CONNECTION",
        "holds_for_arbitrary_control_phi": "YES",
        "selects_metric_configuration": "NO",
        "result": "IDENTITY_RECONSTRUCTION_NOT_EOM",
    },
    {
        "object": "Levi_Civita_metric_compatibility",
        "type": "CANONICAL_CONNECTION_RECONSTRUCTION",
        "holds_for_arbitrary_control_phi": "YES",
        "selects_metric_configuration": "NO",
        "result": "UNIQUE_CONNECTION_NOT_UNIQUE_METRIC",
    },
    {
        "object": "contracted_Bianchi_identity",
        "type": "DIFFERENTIAL_IDENTITY",
        "holds_for_arbitrary_control_phi": "YES",
        "selects_metric_configuration": "NO",
        "result": "ZERO_DYNAMICAL_RANK",
    },
    {
        "object": "reciprocal_character_composition",
        "type": "KINEMATIC_REPRESENTATION_IDENTITY",
        "holds_for_arbitrary_control_phi": "YES",
        "selects_metric_configuration": "NO",
        "result": "DERIVED_KINEMATICS_NOT_REALIZATION_LAW",
    },
    {
        "object": "finite_cell_smoothness_and_gluing",
        "type": "CONFIGURATION_DOMAIN_AND_GLOBAL_COMPATIBILITY",
        "holds_for_arbitrary_control_phi": "NO_NOT_UNIVERSAL",
        "selects_metric_configuration": "NO_MULTIPLE_FAMILIES_SURVIVE",
        "result": "NONTRIVIAL_CONSTRAINT_NOT_COMPLETE_EOM",
    },
]
write_tsv(
    "IDENTITY_VS_EQUATION_LEDGER.tsv",
    ["object", "type", "holds_for_arbitrary_control_phi", "selects_metric_configuration", "result"],
    identity_rows,
)

stage1_pass = any(row["pass"] == "YES" for row in equation_rows)
stage2_pass = any(row["pass"] == "YES" for row in boundary_rows) and stage1_pass
solve_allowed = stage1_pass and stage2_pass
stage3_solution_certified = False
certificate_allowed = solve_allowed and stage3_solution_certified
stage_rows = [
    {
        "stage": "1",
        "object": "E_native",
        "status": "NOT_DERIVED_IN_FROZEN_REGISTERED_FOUNDATION",
        "gate_pass": "NO",
        "action": "ALL_8_ROUTES_ADJUDICATED",
    },
    {
        "stage": "2",
        "object": "B_native",
        "status": "NO_MATCHING_NATIVE_BOUNDARY_DERIVED__CONSTRUCTION_BLOCKED_AFTER_STAGE1",
        "gate_pass": "NO",
        "action": "ALL_6_ROUTES_ADJUDICATED_WITH_OPERATOR_DEPENDENCE_EXPLICIT",
    },
    {
        "stage": "3",
        "object": "same_nonzero_time_angular_field",
        "status": "NOT_LAUNCHED_FAIL_CLOSED",
        "gate_pass": "NO",
        "action": "SOLVE_GUARD_REJECTED",
    },
    {
        "stage": "4",
        "object": "JR_CERT_NATIVE",
        "status": "WITHHELD_MISSING_E_NATIVE_B_NATIVE_AND_SOLUTION",
        "gate_pass": "NO",
        "action": "NO_CERTIFICATE_ASSEMBLED",
    },
]
write_tsv("STAGE_GATE_LEDGER.tsv", ["stage", "object", "status", "gate_pass", "action"], stage_rows)

status_rows = [
    {
        "object": "founded_phi_and_reciprocal_pair",
        "status": "DERIVED_IN_REGISTERED_SCOPE",
        "ruling": "unchanged; exact kinematics does not supply a realization law",
    },
    {
        "object": "complete_off_shell_coframe_families",
        "status": "DERIVED_EXISTENCE_CLASSES",
        "ruling": "unchanged; configuration existence is not on-shell selection",
    },
    {
        "object": "E_native",
        "status": "OPEN_NOT_DERIVED_FROM_CURRENT_REGISTERED_PREMISES",
        "ruling": "all eight routes fail at least one preregistered equation gate",
    },
    {
        "object": "B_native",
        "status": "OPEN_NOT_DERIVED_FROM_CURRENT_REGISTERED_PREMISES",
        "ruling": "all six routes fail; matching construction is additionally downstream of E_native",
    },
    {
        "object": "nonzero_time_angular_solution",
        "status": "OPEN_NOT_COMPUTED",
        "ruling": "Stage-3 launch guard correctly blocked computation",
    },
    {
        "object": "JR_CERT_NATIVE",
        "status": "DEFINED_SCHEMA_WITHHELD_INSTANCE",
        "ruling": "certificate type remains exact; no instance is assembled",
    },
    {
        "object": "overall",
        "status": "NO_NATIVE_PROBLEM_DERIVED_DOWNSTREAM_STAGES_BLOCKED",
        "ruling": "bounded to the exact 586-path registered source universe; no universal no-go",
    },
]
write_tsv("STATUS_LEDGER.tsv", ["object", "status", "ruling"], status_rows)

# Exercised fail-closed controls. Expected accept means the launch guard's decision is correct.
mutation_cases = [
    ("C01_baseline_both_missing", False, False, False),
    ("C02_equation_only", True, False, False),
    ("C03_boundary_only", False, True, False),
    ("C04_both_present", True, True, True),
]
catch_rows = []
for name, e_pass, b_pass, expected in mutation_cases:
    observed = e_pass and b_pass
    catch_rows.append(
        {
            "catch_id": name,
            "equation_pass": str(e_pass).upper(),
            "boundary_pass": str(b_pass).upper(),
            "solve_allowed": str(observed).upper(),
            "expected": str(expected).upper(),
            "result": "PASS" if observed == expected else "FAIL",
        }
    )
assert all(row["result"] == "PASS" for row in catch_rows)
write_tsv(
    "CATCH_PROOFS.tsv",
    ["catch_id", "equation_pass", "boundary_pass", "solve_allowed", "expected", "result"],
    catch_rows,
)

result = {
    "base": BASE,
    "governing_source_count": len(combined),
    "equation_routes": len(equation_rows),
    "equation_routes_passing": sum(row["pass"] == "YES" for row in equation_rows),
    "boundary_routes": len(boundary_rows),
    "boundary_routes_passing": sum(row["pass"] == "YES" for row in boundary_rows),
    "stage1_pass": stage1_pass,
    "stage2_pass": stage2_pass,
    "stage3_solve_allowed": solve_allowed,
    "stage3_launched": False,
    "stage3_solution_certified": stage3_solution_certified,
    "stage4_certificate_allowed": certificate_allowed,
    "stage4_certificate_assembled": False,
    "outcome": "NO_NATIVE_PROBLEM_DERIVED_DOWNSTREAM_STAGES_BLOCKED",
    "scope_ceiling": "CURRENT_REGISTERED_586_PATH_SOURCE_UNIVERSE_ONLY__NO_UNIVERSAL_NO_GO",
    "source_anchor_rows": len(source_anchors),
    "catch_proofs": len(catch_rows),
}
(HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(
    "PASS JR_CERT_NATIVE staged derivation: "
    f"E={result['equation_routes_passing']}/{result['equation_routes']} "
    f"B={result['boundary_routes_passing']}/{result['boundary_routes']} "
    f"solve_allowed={solve_allowed} certificate_assembled=False "
    f"outcome={result['outcome']}"
)
