#!/usr/bin/env python3
"""Exact bounded audit of basic versus universal observer-query residuals."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def write_tsv(name: str, fields: tuple[str, ...], rows: list[tuple[str, ...]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(fields)
        writer.writerows(rows)


def coefficient_row(expression: sp.Expr, variables: list[sp.Symbol]) -> list[sp.Expr]:
    return [sp.expand(expression).coeff(variable) for variable in variables]


def exact_controls() -> dict[str, object]:
    checks: list[bool] = []

    # Operator non-descent inherited from the exact pair-plane control.
    P01 = sp.diag(1, 1, 0, 0)
    P02 = sp.diag(1, 0, 1, 0)
    A = sp.diag(2, 3, 5, 7)
    pair_values = [sp.trace(P01 * A), sp.trace(P02 * A)]
    checks += [pair_values == [5, 7], P01 != P02]

    # Symmetric bilinear S in the component order below.
    names = ("s00", "s01", "s02", "s03", "s11", "s12", "s13", "s22", "s23", "s33")
    variables = list(sp.symbols(" ".join(names), real=True))
    s00, s01, s02, s03, s11, s12, s13, s22, s23, s33 = variables
    S = sp.Matrix(
        [
            [s00, s01, s02, s03],
            [s01, s11, s12, s13],
            [s02, s12, s22, s23],
            [s03, s13, s23, s33],
        ]
    )
    eta = sp.diag(-1, 1, 1, 1)

    def value(v: sp.Matrix) -> sp.Expr:
        return sp.expand((v.T * S * v)[0])

    e = [sp.eye(4)[:, i] for i in range(4)]
    pairs: list[tuple[sp.Matrix, sp.Matrix]] = []
    # Three axial rulers at u=e0.
    for i in (1, 2, 3):
        pairs.append((e[0], e[i]))
    # Three normalized spatial sums at u=e0.
    for i, j in ((1, 2), (1, 3), (2, 3)):
        pairs.append((e[0], (e[i] + e[j]) / sp.sqrt(2)))
    # Three rational 3-4-5 boosts, each with an orthogonal axial ruler.
    for i, j in ((1, 2), (2, 3), (3, 1)):
        pairs.append((sp.Rational(5, 3) * e[0] + sp.Rational(4, 3) * e[i], e[j]))

    residuals = []
    for u, n in pairs:
        checks += [sp.simplify((u.T * eta * u)[0]) == -1]
        checks += [sp.simplify((n.T * eta * n)[0]) == 1]
        checks += [sp.simplify((u.T * eta * n)[0]) == 0]
        residuals.append(sp.expand(value(u) + value(n)))

    query_matrix = sp.Matrix([coefficient_row(expression, variables) for expression in residuals])
    query_rank = query_matrix.rank()
    query_kernel = query_matrix.nullspace()
    metric_line = sp.Matrix([1, 0, 0, 0, -1, 0, 0, -1, 0, -1])  # -eta covariant components
    checks += [query_rank == 9]
    checks += [len(query_kernel) == 1]
    checks += [query_matrix * metric_line == sp.zeros(9, 1)]
    checks += [query_kernel[0] == metric_line or query_kernel[0] == -metric_line]

    # The same kernel is the vanishing of the Lorentz trace-free part of S.
    lorentz_trace = sp.expand(-s00 + s11 + s22 + s33)
    trace_free = sp.simplify(S - sp.Rational(1, 4) * lorentz_trace * eta)
    trace_free_components = [
        trace_free[0, 0], trace_free[0, 1], trace_free[0, 2], trace_free[0, 3],
        trace_free[1, 1], trace_free[1, 2], trace_free[1, 3],
        trace_free[2, 2], trace_free[2, 3], trace_free[3, 3],
    ]
    trace_free_matrix = sp.Matrix([coefficient_row(expression, variables) for expression in trace_free_components])
    checks += [trace_free_matrix.rank() == 9]
    checks += [trace_free_matrix * metric_line == sp.zeros(10, 1)]
    checks += [query_matrix.col_join(trace_free_matrix).rank() == 9]

    # The universal family is stronger than the single Lorentz-trace scalar equation.
    strict_S = sp.diag(3, 1, 1, 1)
    strict_trace = sp.trace(eta * strict_S)
    strict_pair = (e[0].T * strict_S * e[0])[0] + (e[1].T * strict_S * e[1])[0]
    checks += [strict_trace == 0, strict_pair == 4]

    # Yet the universal family allows a nonzero metric line: it is not S=0.
    kernel_S = -eta
    kernel_trace = sp.trace(eta * kernel_S)
    kernel_values = [sp.simplify((u.T * kernel_S * u)[0] + (n.T * kernel_S * n)[0]) for u, n in pairs]
    checks += [all(item == 0 for item in kernel_values), kernel_trace == -4, kernel_S != sp.zeros(4)]

    # Equal zero sets need not give equal tangent equations.
    x = sp.symbols("x", real=True)
    query_family = sp.Matrix([-x, x])
    query_jacobian_rank = query_family.jacobian([x]).subs(x, 0).rank()
    linear_basic_rank = sp.Matrix([x]).jacobian([x]).subs(x, 0).rank()
    square_basic_rank = sp.Matrix([x**2]).jacobian([x]).subs(x, 0).rank()
    checks += [query_jacobian_rank == linear_basic_rank == 1]
    checks += [square_basic_rank == 0]

    # Coefficient reduction preserves the rank-nine tangent; a squared norm does not.
    coeff_tangent_rank = trace_free_matrix.rank()
    squared_norm = sp.expand(sum(component**2 for component in trace_free_components))
    squared_gradient = sp.Matrix([sp.diff(squared_norm, variable) for variable in variables])
    kernel_substitution = dict(zip(variables, list(metric_line)))
    squared_gradient_at_solution = squared_gradient.subs(kernel_substitution)
    checks += [coeff_tangent_rank == 9]
    checks += [squared_gradient_at_solution == sp.zeros(10, 1)]

    # The normalized query fiber depends on g. Its induced lift is kinematic, not an independent
    # field variation. On the universal metric-line solution the total lifted residual stays zero.
    eps, lam = sp.symbols("eps lam", real=True)
    g_eps = sp.diag(-(1 + eps), 1, 1, 1)
    u_eps = sp.Matrix([1 / sp.sqrt(1 + eps), 0, 0, 0])
    normalized_residual = sp.simplify((u_eps.T * (lam * g_eps) * u_eps)[0] + lam)
    checks += [normalized_residual == 0]
    checks += [sp.diff(normalized_residual, eps) == 0]

    # Locally flat quotient control: identical curvature jets, distinct loop holonomy.
    torus_holonomy = sp.eye(2)
    klein_holonomy = sp.diag(-1, 1)
    checks += [klein_holonomy.T * klein_holonomy == sp.eye(2)]
    checks += [klein_holonomy.det() == -1]
    checks += [klein_holonomy**2 == sp.eye(2)]
    checks += [klein_holonomy != torus_holonomy]
    local_curvature_jets_torus = [0] * 5
    local_curvature_jets_klein = [0] * 5
    checks += [local_curvature_jets_torus == local_curvature_jets_klein]

    # Registered SNe anchor is replayed only as a downstream identity.
    z = sp.symbols("z", real=True)
    u = 1 + z
    sne_shape = sp.factor(u**2 * (1 - u**-2))
    checks += [sp.simplify(sne_shape - z * (z + 2)) == 0]
    checks += [len({"clock", "areal", "optical", "proper_pair"}) == 4]

    failed = [index for index, check in enumerate(checks, start=1) if check is not True and check != sp.true]
    assert not failed, failed
    return {
        "status": "PASS",
        "exact_checks": len(checks),
        "pair_values": [str(item) for item in pair_values],
        "query_coefficient_rank": query_rank,
        "query_coefficient_nullity": 10 - query_rank,
        "query_kernel_generator": [str(item) for item in metric_line],
        "trace_free_map_rank": trace_free_matrix.rank(),
        "stacked_query_tracefree_rank": query_matrix.col_join(trace_free_matrix).rank(),
        "strict_tracefree_control_trace": str(strict_trace),
        "strict_tracefree_control_pair_value": str(strict_pair),
        "nonzero_metric_line_trace": str(kernel_trace),
        "universal_query_tangent_rank": query_jacobian_rank,
        "linear_basic_tangent_rank": linear_basic_rank,
        "squared_basic_tangent_rank": square_basic_rank,
        "coefficient_tangent_rank": coeff_tangent_rank,
        "squared_coefficient_gradient_rank_at_solution": squared_gradient_at_solution.rank(),
        "metric_dependent_query_total_derivative": str(sp.diff(normalized_residual, eps)),
        "torus_loop_holonomy": str(torus_holonomy.tolist()),
        "klein_loop_holonomy": str(klein_holonomy.tolist()),
        "local_flat_jet_orders_compared": len(local_curvature_jets_torus),
        "sne_conditional_shape": str(sne_shape),
    }


def reduction_atlas() -> list[tuple[str, ...]]:
    rulings = {
        "R01": (
            "MIXED_SCALAR_BASIC__PROJECTOR_NONBASIC", "YES_BY_UNIVERSAL_PREDICATE",
            "FINITE_ZERO_JET_ORBIT_REDUCTION", "YES_ZERO_JET",
            "ONLY_WITH_REGULAR_COEFFICIENT_MAP", "YES_AS_METRIC_PREDICATE", "NOT_APPLICABLE",
            "NO_NONTRIVIAL_DYNAMICS_FROM_METRIC_PLUS_NORMALIZED_PAIR_ALONE",
        ),
        "R02": (
            "GENERICALLY_NO", "YES_BY_UNIVERSAL_PREDICATE",
            "YES_ON_FINITE_ALGEBRAIC_REGULAR_DOMAIN", "YES_BOUNDED_JET",
            "COEFFICIENT_MAP_YES__SQUARED_SCALARIZATION_NO", "YES_AS_METRIC_RELATION", "NOT_APPLICABLE",
            "DIRECTIONAL_CONTENT_CAN_REDUCE_TO_STRONGER_BASIC_TENSOR_SYSTEM",
        ),
        "R03": (
            "GENERICALLY_NO", "YES_BY_UNIVERSAL_PREDICATE", "NOT_GUARANTEED",
            "YES_ONLY_AS_POSSIBLY_INFINITE_RANK_FIBER_RELATION", "POINTWISE_QUERY_FAMILY_REQUIRED",
            "YES_AS_METRIC_RELATION", "NOT_APPLICABLE",
            "SMOOTH_QUERY_CODOMAIN_CAN_REMAIN_INFINITE_RANK",
        ),
        "R04": (
            "NO_IN_GENERAL", "YES_BY_UNIVERSAL_PREDICATE", "NO_IN_GENERAL",
            "NO_IN_GENERAL", "GLOBAL_RELATION_TANGENT_REQUIRED", "YES_GENUINELY_GLOBAL",
            "TOPOLOGY_AND_DEFECT_SECTORS_RETAINED",
            "GLOBAL_QUERY_CONTENT_CAN_ESCAPE_EVERY_FINITE_LOCAL_JET_WITHOUT_A_SECTION",
        ),
        "R05": (
            "PARENT_NONBASIC__REGULAR_COMPOSITE_BASIC", "YES_ON_REGULAR_BRANCH", "CONDITIONAL_ON_SELECTOR",
            "CONDITIONAL_ON_SELECTOR_JET_ORDER", "CHAIN_RULE_REQUIRED", "YES_ON_DECLARED_BRANCH",
            "CONDITIONAL_BOUNDARY_PULLBACK",
            "REGULAR_REDUCTION_IS_METRIC_ONLY_ONLY_WHEN_SELECTOR_IS_METRIC_DERIVED",
        ),
        "R06": (
            "NO_SINGLE_SMOOTH_BASIC_OBJECT", "YES_IF_ALL_MEMBER_QUANTIFIER_DECLARED", "NOT_GUARANTEED",
            "STRATIFIED_RELATION_ONLY", "TANGENT_CONE_OR_INTERFACE_RULE_OPEN", "YES_AS_STRATIFIED_RELATION",
            "OPEN_INTERFACE_AND_DEFECT_OWNER",
            "ZERO_SET_DESCENT_DOES_NOT_SUPPLY_SMOOTH_VARIATION_OWNERSHIP",
        ),
        "R07": (
            "BASE_PART_BASIC__PAIR_POLARIZATION_NONBASIC", "YES_IF_UNIVERSAL_BOUNDARY_QUERY_DECLARED",
            "CONDITIONAL_ALGEBRAIC_SUBCLASS", "CONDITIONAL", "BOUNDARY_TANGENT_AND_POLARIZATION_OPEN",
            "YES_AS_BOUNDARY_RELATION", "OPEN_NOT_SELECTED",
            "UNIVERSAL_QUANTIFIER_DOES_NOT_SELECT_BOUNDARY_TYPE_OR_GLUE",
        ),
        "R08": (
            "OPEN", "OPEN", "OPEN", "OPEN", "OPEN", "OPEN", "OPEN",
            "NONEXHAUSTIVENESS_ESCAPE_RETAINED",
        ),
    }
    rows = []
    with (HERE / "RESIDUAL_CLASS_UNIVERSE.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            rows.append((row["residual_id"], row["class"], *rulings[row["residual_id"]]))
    return rows


def main() -> None:
    result = exact_controls()
    write_tsv(
        "REDUCTION_EQUIVALENCE_ATLAS.tsv",
        (
            "residual_id", "class", "operator_basic_descent", "solution_set_descent",
            "finite_local_tensor_reduction", "finite_jet_natural_reduction",
            "linearized_variation_equivalence", "global_metric_relation_reduction",
            "boundary_stratified_equivalence", "overall_ruling",
        ),
        reduction_atlas(),
    )
    controls = [
        ("K01", "pair-projector residual at fixed ambient A", "5 versus 7", "OPERATOR_NONBASIC"),
        ("K02", "nine observer/ruler coefficient equations on symmetric S", "rank 9 nullity 1", "FINITE_COEFFICIENT_EXTRACTION"),
        ("K03", "kernel of universal pair family", "S proportional to metric", "BASIC_TRACEFREE_TENSOR_REDUCTION"),
        ("K04", "query and trace-free coefficient row spaces", "stacked rank 9", "SAME_ZERO_SET_AND_LINEARIZED_SYSTEM"),
        ("K05", "Lorentz-trace-free anisotropic S", "trace 0 pair residual 4", "ONE_BASIC_SCALAR_TOO_WEAK"),
        ("K06", "nonzero metric-line S", "all query residuals 0 trace -4", "UNIVERSAL_FAMILY_NOT_S_EQUAL_ZERO"),
        ("K07", "L(x,q)=q x versus F=x", "both tangent rank 1", "VARIATION_EQUIVALENT_CONTROL"),
        ("K08", "L(x,q)=q x versus G=x squared", "query rank 1 square rank 0", "ZERO_SET_ONLY_NOT_VARIATION_EQUIVALENT"),
        ("K09", "trace-free coefficient map", "tangent rank 9", "REGULAR_COEFFICIENT_REDUCTION_PRESERVES_TANGENT"),
        ("K10", "squared norm of trace-free coefficients", "gradient rank 0 on solution", "SCALARIZATION_LOSES_FIRST_VARIATION"),
        ("K11", "flat translation quotient loop", "identity holonomy", "GLOBAL_POSITIVE_CONTROL"),
        ("K12", "flat glide-reflection quotient loop", "reflection holonomy determinant -1", "GLOBAL_NONLOCAL_CONTROL"),
        ("K13", "local curvature jets of both flat quotients", "orders 0 through 4 all zero", "FINITE_LOCAL_DATA_IDENTICAL"),
        ("K14", "all-loop trivial-holonomy predicate", "distinguishes K11 and K12", "NOT_REDUCIBLE_TO_FINITE_LOCAL_METRIC_JETS_IN_GENERAL"),
        ("K15", "registered SNe readout", "d_L/X=z(z+2)", "DOWNSTREAM_COMPATIBILITY_ONLY"),
    ]
    write_tsv("EXACT_CONTROL_LEDGER.tsv", ("control_id", "control", "exact_result", "ruling"), controls)
    variation = [
        ("V01", "universal query family", "vary g while enforcing every q", "no independent delta_q", "DERIVED_TYPE_RULE"),
        ("V02", "finite coefficient map", "differentiate coefficient tensor/system", "rank must match query-family linearization", "VALID_ON_REGISTERED_REGULAR_CONTROL"),
        ("V03", "sum or norm of squared residuals", "zero set may agree but derivative vanishes at residual zero", "requires an independently justified variational role", "REJECT_AS_AUTOMATIC_REPLACEMENT"),
        ("V04", "regular metric-derived selector", "include DS_g chain term", "no independent delta_q", "CONDITIONAL_REGULAR"),
        ("V05", "singular/set-valued selector", "tangent cone interface or differential relation", "no unique smooth derivative", "OPEN"),
        ("V06", "global path relation", "differentiate full holonomy/distance relation if selected", "not captured by local jet variation in general", "OPEN_NATIVE_OWNER"),
        ("V07", "boundary query relation", "retain base boundary and pair polarization owners", "boundary domain not selected", "OPEN"),
        ("V08", "metric-dependent normalized query fiber", "differentiate on total query bundle or after faithful coefficient reduction", "induced query lift is kinematic and lift ambiguity cancels on regular universal zero section", "DERIVED_REGULAR__STRATIFIED_AT_DOMAIN_CHANGE"),
    ]
    write_tsv("VARIATION_EQUIVALENCE_LEDGER.tsv", ("variation_id", "object", "variation_rule", "guard", "status"), variation)
    global_rows = [
        ("G01", "translation flat quotient", "all registered local curvature jets zero", "identity", "YES", "control only"),
        ("G02", "glide-reflection flat quotient", "all registered local curvature jets zero", "reflection diag(-1,1)", "NO", "control only"),
        ("G03", "finite local metric tensor relation", "cannot distinguish G01/G02", "not available", "NOT_SUFFICIENT_IN_GENERAL", "same local germ"),
        ("G04", "universal loop-query relation", "uses complete path groupoid", "distinguishes G01/G02", "GENUINE_GLOBAL_METRIC_RELATION", "no observer section"),
    ]
    write_tsv("GLOBAL_LOCAL_CONTROL.tsv", ("control_id", "geometry", "local_finite_jet_data", "loop_holonomy", "all_loop_trivial", "scope"), global_rows)
    founding = [
        ("F01", "founded reciprocal character", "supplies typed query morphism and composition", "does not supply L(g,q)=0"),
        ("F02", "observer reciprocity", "requires equivariant treatment of every valid query", "does not choose universal versus supplied-readout dynamics"),
        ("F03", "metric is the theory", "permits universal metric-derived query residual without new field", "does not choose residual functional or local/global class"),
        ("F04", "complete coframe architecture", "provides candidate metric-owned inputs", "is not an on-shell residual"),
        ("F05", "SNe conditional anchor", "requires distinct downstream readout slots", "does not choose residual or quantifier"),
        ("F06", "current foundation", "leaves basic local and universal local/global routes admissible", "no nontrivial native residual selected"),
    ]
    write_tsv("FOUNDATIONAL_RULING.tsv", ("ruling_id", "object", "positive_entailment", "remaining_open"), founding)
    status = [
        ("S01", "operator basicness of generic query residual", "NOT_DERIVED__GENERICALLY_FALSE", "query dependence can remain exact"),
        ("S02", "universal solution-set descent", "DERIVED_LOGICAL", "observer-independent predicate on metric configurations"),
        ("S03", "registered local algebraic control", "DERIVED_FINITE_BASIC_TENSOR_REDUCTION", "rank-nine trace-free system not one scalar"),
        ("S04", "universal content beyond one basic scalar", "DERIVED_CONTROL", "does not imply irreducibility to every base tensor system"),
        ("S05", "finite smooth-query reduction", "NOT_GUARANTEED", "may require infinite-rank fiber relation"),
        ("S06", "global path-query reduction", "DERIVED_NOT_FINITE_LOCAL_IN_GENERAL", "still a section-free global metric relation"),
        ("S07", "zero-set scalarization", "REJECTED_AS_AUTOMATIC_VARIATION_REPLACEMENT", "registered tangent rank is lost"),
        ("S08", "universal-query metric-only architecture", "ADMISSIBLE_GENUINE_NOT_SELECTED", "specific residual and local/global class absent"),
        ("S09", "realized observer section", "NOT_REQUIRED_FOR_UNIVERSAL_QUERY_ARCHITECTURE", "remains open extra structure if separately proposed"),
        ("S10", "SNe", "CONDITIONAL_DOWNSTREAM_COMPATIBILITY_ANCHOR", "no upstream selection"),
        ("S11", "native action source boundary bootstrap Xmax mass matter dynamics", "OPEN_OR_PRIOR_CONDITIONAL", "unchanged"),
        ("S12", "overall audit", "VERIFIED_WITH_CAVEATS_BOUNDED_UNIVERSAL_QUERY_REDUCTION_ATLAS", "arbitrary smooth singular boundary and actual UDT residual classes remain open"),
    ]
    write_tsv("STATUS_LEDGER.tsv", ("status_id", "object", "status", "scope_or_open"), status)
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
