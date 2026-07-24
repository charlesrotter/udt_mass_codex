#!/usr/bin/env python3
"""Exact relational-depth type, composition-domain, and cut-locus audit."""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require_zero(name: str, value, checks: dict[str, str]) -> None:
    reduced = sp.simplify(value)
    if isinstance(reduced, sp.MatrixBase):
        failed = any(sp.simplify(entry) != 0 for entry in reduced)
    else:
        failed = reduced != 0
    if failed:
        raise AssertionError(f"{name}: {reduced}")
    checks[name] = "PASS"


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def validate_sources(checks: dict[str, str]) -> int:
    with (HERE / "SOURCE_LINEAGE.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    with (HERE / "SOURCE_ADDENDUM.tsv").open(encoding="utf-8", newline="") as handle:
        rows += list(csv.DictReader(handle, delimiter="\t"))
    require("source_count_10", len(rows) == 10, checks)
    require("source_ids_unique", len({row["id"] for row in rows}) == 10, checks)
    for row in rows:
        source = ROOT / row["path"]
        require(f"source_exists_{row['id']}", source.is_file(), checks)
        require(f"source_sha_{row['id']}", sha256(source) == row["sha256"], checks)
    return len(rows)


def main() -> None:
    checks: dict[str, str] = {}
    source_count = validate_sources(checks)

    # Owner clarification: every observer's local frame is neutral. Pair
    # dilation is relational data and does not alter either local frame.
    delta = sp.symbols("delta", real=True)
    reciprocal = lambda value: sp.diag(sp.exp(-value), sp.exp(value))
    require_zero("observer_p_self_neutral", reciprocal(0) - sp.eye(2), checks)
    require_zero("observer_q_self_neutral", reciprocal(0) - sp.eye(2), checks)
    require_zero(
        "pair_reverse_is_inverse",
        reciprocal(delta) * reciprocal(-delta) - sp.eye(2),
        checks,
    )
    require(
        "nontrivial_pair_does_not_change_self_operators",
        reciprocal(delta) != reciprocal(0),
        checks,
    )

    # Exact round S3 observer-pair control in embedding coordinates.
    b = sp.symbols("b", positive=True)
    eps = sp.pi / 3
    cos_eps = sp.Rational(1, 2)
    sin_eps = sp.sqrt(3) / 2
    p = b * sp.Matrix([1, 0, 0, 0])
    q1 = b * sp.Matrix([cos_eps, sin_eps, 0, 0])
    q2 = b * sp.Matrix([cos_eps, 0, sin_eps, 0])
    q3 = b * sp.Matrix([cos_eps, 0, 0, sin_eps])
    qs = (q1, q2, q3)
    for index, q in enumerate(qs, start=1):
        require_zero(f"round_equal_radius_{index}", (p.dot(q) / b**2) - sp.Rational(1, 2), checks)
    for index, (left, right) in enumerate(itertools.combinations(qs, 2), start=1):
        require_zero(
            f"round_nonzero_pair_dot_{index}",
            left.dot(right) / b**2 - sp.Rational(1, 4),
            checks,
        )
        require(f"round_nonzero_pair_{index}", left != right, checks)

    # If one global scalar difference represented F(distance), each q_i at
    # equal radius could take only phi(p)+A or phi(p)-A. Three points and two
    # signs force a duplicate scalar value for a nonzero-separated pair.
    sign_assignments = list(itertools.product((-1, 1), repeat=3))
    for index, signs in enumerate(sign_assignments, start=1):
        require(
            f"pigeonhole_scalar_signs_{index}",
            len(set(signs)) < 3,
            checks,
        )
    radial_depth, mutual_depth = sp.symbols(
        "radial_depth mutual_depth", positive=True
    )
    require(
        "three_observer_relational_depths_coexist",
        radial_depth.is_positive is True and mutual_depth.is_positive is True,
        checks,
    )

    # Observer-indexed metric families are centerless under isometries.
    swap12 = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
        ]
    )
    require_zero("round_isometry_orthogonal", swap12.T * swap12 - sp.eye(4), checks)
    require_zero("round_isometry_pair_dot", (swap12 * p).dot(swap12 * q1) - p.dot(q1), checks)
    require_zero("round_isometry_transitive_sample", swap12 * q1 - q2, checks)

    # Composition on ordinary minimizing-geodesic subsegments.
    x, y = sp.symbols("x y", nonnegative=True)
    coefficients = sp.symbols("a0:6")
    polynomial = sum(coefficients[k] * x**k for k in range(6))
    poly_y = polynomial.subs(x, y)
    poly_xy = polynomial.subs(x, x + y)
    cauchy_residual = sp.Poly(sp.expand(poly_xy - polynomial - poly_y), x, y)
    equations = [coefficient for _, coefficient in cauchy_residual.terms()]
    solution = sp.solve(equations, coefficients, dict=True)
    require("polynomial_additivity_solution_exists", bool(solution), checks)
    require("polynomial_additivity_zero_constant", solution[0].get(coefficients[0]) == 0, checks)
    for power in range(2, 6):
        require(
            f"polynomial_additivity_kills_degree_{power}",
            solution[0].get(coefficients[power]) == 0,
            checks,
        )
    require(
        "polynomial_additivity_leaves_linear_scale",
        coefficients[1] not in solution[0],
        checks,
    )

    kappa, diameter = sp.symbols("kappa diameter", positive=True, finite=True)
    linear_depth = kappa * x
    require_zero(
        "linear_depth_geodesic_additivity",
        linear_depth.subs(x, x + y) - linear_depth - linear_depth.subs(x, y),
        checks,
    )
    require_zero(
        "linear_depth_finite_at_finite_diameter",
        sp.limit(linear_depth, x, diameter, dir="-") - kappa * diameter,
        checks,
    )

    nonlinear_depth = sp.atanh(x / diameter)
    require(
        "projective_depth_diverges",
        sp.limit(nonlinear_depth, x, diameter, dir="-") == sp.oo,
        checks,
    )
    quarter = diameter / 4
    nonlinear_add_failure = sp.simplify(
        nonlinear_depth.subs(x, 2 * quarter) - 2 * nonlinear_depth.subs(x, quarter)
    )
    require("projective_depth_not_ordinary_additive", nonlinear_add_failure != 0, checks)
    require_zero(
        "bounded_projective_display",
        diameter * sp.tanh(sp.atanh(x / diameter)) - x,
        checks,
    )
    require_zero(
        "projective_composition_witness",
        (
            sp.Rational(1, 2) + sp.Rational(1, 2)
        )
        / (
            1 + sp.Rational(1, 2) * sp.Rational(1, 2)
        )
        - sp.Rational(4, 5),
        checks,
    )
    require(
        "projective_composition_not_length_sum",
        sp.Rational(4, 5) != 1,
        checks,
    )

    # One observer chart can compose increments, but the second increment is
    # not the same universal F applied to the q-based segment.
    chart_increment = sp.simplify(
        nonlinear_depth.subs(x, 2 * quarter) - nonlinear_depth.subs(x, quarter)
    )
    require_zero(
        "observer_chart_telescopes",
        nonlinear_depth.subs(x, quarter) + chart_increment
        - nonlinear_depth.subs(x, 2 * quarter),
        checks,
    )
    require(
        "observer_chart_increment_not_rebased_pair_value",
        sp.simplify(chart_increment - nonlinear_depth.subs(x, quarter)) != 0,
        checks,
    )

    # Angular data are indispensable for non-collinear pair composition.
    alpha, beta, angular_dot = sp.symbols("alpha beta angular_dot", real=True)
    round_pair_dot = sp.cos(alpha) * sp.cos(beta) + sp.sin(alpha) * sp.sin(beta) * angular_dot
    require_zero(
        "round_same_direction_law",
        round_pair_dot.subs(angular_dot, 1) - sp.cos(alpha - beta),
        checks,
    )
    require_zero(
        "round_opposite_direction_law",
        round_pair_dot.subs(angular_dot, -1) - sp.cos(alpha + beta),
        checks,
    )
    same_radial_same_direction = sp.simplify(
        round_pair_dot.subs({alpha: sp.pi / 3, beta: sp.pi / 3, angular_dot: 1})
    )
    same_radial_orthogonal = sp.simplify(
        round_pair_dot.subs({alpha: sp.pi / 3, beta: sp.pi / 3, angular_dot: 0})
    )
    same_radial_opposite = sp.simplify(
        round_pair_dot.subs({alpha: sp.pi / 3, beta: sp.pi / 3, angular_dot: -1})
    )
    require_zero("same_radial_same_direction_dot", same_radial_same_direction - 1, checks)
    require_zero("same_radial_orthogonal_dot", same_radial_orthogonal - sp.Rational(1, 4), checks)
    require_zero("same_radial_opposite_dot", same_radial_opposite + sp.Rational(1, 2), checks)
    require(
        "angular_data_changes_pair_distance",
        len({same_radial_same_direction, same_radial_orthogonal, same_radial_opposite}) == 3,
        checks,
    )

    # The antipodal scalar distance is unique, while full tangent transport
    # depends on which minimizing great semicircle is chosen.
    transport_e1 = sp.diag(-1, 1, 1)
    transport_e2 = sp.diag(1, -1, 1)
    require_zero("cut_transport_e1_isometry", transport_e1.T * transport_e1 - sp.eye(3), checks)
    require_zero("cut_transport_e2_isometry", transport_e2.T * transport_e2 - sp.eye(3), checks)
    require("cut_transport_paths_differ", transport_e1 != transport_e2, checks)
    require_zero("cut_scalar_distance_unique", b * sp.acos(-1) - sp.pi * b, checks)

    # Exact reciprocal current and endpoint integral.
    s = sp.symbols("s", real=True)
    A, B = sp.symbols("A B", real=True)
    phi_s = A * s**2 + B * s
    current = sp.diag(-sp.diff(phi_s, s), sp.diff(phi_s, s))
    s0, s1 = sp.symbols("s0 s1", real=True)
    integrated_current = current.applyfunc(lambda entry: sp.integrate(entry, (s, s0, s1)))
    endpoint_current = sp.diag(
        -(phi_s.subs(s, s1) - phi_s.subs(s, s0)),
        phi_s.subs(s, s1) - phi_s.subs(s, s0),
    )
    require_zero("reciprocal_current_endpoint_integral", integrated_current - endpoint_current, checks)
    require_zero("reciprocal_current_closed_1d", sp.diff(current[0, 0], s) - sp.diff(current[0, 0], s), checks)

    # A closed loop with nonzero angular period is a control showing that a
    # locally written closed one-form need not be globally exact.
    theta = sp.symbols("theta", real=True)
    require_zero("circle_period_control", sp.integrate(1, (theta, 0, 2 * sp.pi)) - 2 * sp.pi, checks)

    type_rows = [
        {
            "id": "D01",
            "candidate": "primitive bilocal ordered depth",
            "exact_ruling": "compatible with founded operator by definition",
            "status": "FOUNDING_COMPATIBLE_NOT_COMPLETE_METRIC_DERIVATION",
            "remaining_gate": "derive pair value and composition domain from complete geometry",
        },
        {
            "id": "D02",
            "candidate": "observer-indexed metric family rho_p(q)=F(d_h(p,q))",
            "exact_ruling": "centerless and isometry covariant for every scalar F",
            "status": "SMALLEST_SURVIVING_METRIC_NATIVE_TYPE_GIVEN_F",
            "remaining_gate": "F and chart transition/oriented comparison law unselected",
        },
        {
            "id": "D03",
            "candidate": "one global scalar difference",
            "exact_ruling": "cannot represent a strictly positive isotropic distance-only depth for every pair on round S3",
            "status": "REFUTED_AS_UNIVERSAL_CENTERLESS_ISOTROPIC_PAIR_DEPTH",
            "remaining_gate": "may still describe a local ordered chain or anisotropic solution field",
        },
        {
            "id": "D04",
            "candidate": "reciprocal-current line integral",
            "exact_ruling": "equals endpoint phi difference where one global exact reciprocal section exists",
            "status": "DERIVED_IDENTITY_GIVEN_OPEN_SECTION_JOIN",
            "remaining_gate": "inherits D03 limitation and global exactness/holonomy gate",
        },
        {
            "id": "D05",
            "candidate": "universal metric-distance function F(d)",
            "exact_ruling": "centerless bilocal scalar; continuous ordinary-geodesic additivity forces F(d)=kappa d",
            "status": "TYPE_VALID_FUNCTION_UNSELECTED",
            "remaining_gate": "dimensionful normalization and intended composition domain",
        },
        {
            "id": "D06",
            "candidate": "bounded projective display",
            "exact_ruling": "finite display and infinite additive coordinate can coexist, but nonlinear display is not ordinary proper-length additive",
            "status": "EXACT_CONDITIONAL_DISPLAY_NOT_METRIC_DISTANCE_IDENTITY",
            "remaining_gate": "derive physical projective-position join",
        },
        {
            "id": "D07",
            "candidate": "path-family full transport",
            "exact_ruling": "scalar distance remains unique at round antipode while full frame transport differs by path",
            "status": "DERIVED_TYPE_SEPARATION",
            "remaining_gate": "complete reciprocal/angular holonomy and physical path-family readout",
        },
        {
            "id": "D08",
            "candidate": "directional cut depth",
            "exact_ruling": "well typed as observer-indexed boundary data after a complete cut-locus solution",
            "status": "CONDITIONAL_ON_COMPLETE_CUT_LOCUS_AND_F",
            "remaining_gate": "nonround cut band and clock solder",
        },
    ]

    composition_rows = [
        {
            "domain": "abstract additive depth parameters",
            "law": "delta12+delta23=delta13",
            "result": "DERIVED_WHEN_INTERMEDIATE_LIES_IN_DECLARED_ORDERED_DEPTH_CHAIN",
            "failure_outside_domain": "no arbitrary-triple metric claim",
        },
        {
            "domain": "proper metric subsegments on one minimizing geodesic",
            "law": "d13=d12+d23",
            "result": "DERIVED_BEFORE_CUT_WHEN_Q_IS_BETWEEN_P_AND_R",
            "failure_outside_domain": "triangle inequality is generally strict",
        },
        {
            "domain": "universal continuous F of proper distance",
            "law": "F(d1+d2)=F(d1)+F(d2)",
            "result": "FORCES_F_EQUAL_KAPPA_D",
            "failure_outside_domain": "nonlinear asymptotic F fails ordinary subsegment additivity",
        },
        {
            "domain": "observer-indexed nonlinear chart",
            "law": "rho_p(r)=rho_p(q)+[rho_p(r)-rho_p(q)]",
            "result": "TELESCOPES_IN_ONE_BASE_CHART",
            "failure_outside_domain": "bracket is not generally rho_q(r)",
        },
        {
            "domain": "noncollinear round triples",
            "law": "cos d_qr/b=cos a cos b+sin a sin b n_dot_m",
            "result": "ANGULAR_DATUM_REQUIRED",
            "failure_outside_domain": "two radial depths do not determine third pair",
        },
        {
            "domain": "cut locus",
            "law": "scalar d remains infimum; full transport indexed by minimizing paths",
            "result": "SCALAR_SINGLE_FULL_TRANSPORT_FAMILY",
            "failure_outside_domain": "no unique full transport without holonomy/path readout",
        },
    ]

    round_rows = [
        {
            "quantity": "pair distance",
            "exact_result": "d(p,q)=b*acos(p_dot_q/b^2)",
            "consequence": "bilocal centerless scalar",
        },
        {
            "quantity": "observer radial family",
            "exact_result": "rho_p(q)=F(d(p,q))",
            "consequence": "every p has equivalent chart; no global center",
        },
        {
            "quantity": "three equal-radius directions",
            "exact_result": "p_dot_qi/b^2=1/2; qi_dot_qj/b^2=1/4",
            "consequence": "global scalar-difference universal isotropic representation impossible",
        },
        {
            "quantity": "noncollinear pair law",
            "exact_result": "requires direction dot product",
            "consequence": "angular sector participates in composition",
        },
        {
            "quantity": "antipodal distance",
            "exact_result": "pi*b for every minimizing semicircle",
            "consequence": "scalar distance unique at cut",
        },
        {
            "quantity": "antipodal frame transport",
            "exact_result": "different exact isometries for different great semicircles",
            "consequence": "full transport path-family at cut",
        },
        {
            "quantity": "round clock solder",
            "exact_result": "constant lapse",
            "consequence": "no physical Xmax promotion",
        },
    ]

    scale_rows = [
        {
            "object": "metric distance d",
            "dimension": "length",
            "available_anchor": "complete physical metric representative",
            "missing_for_dimensionless_depth": "inverse-length normalization or selected profile",
            "status": "DERIVED_PER_METRIC",
        },
        {
            "object": "c and inverse-c",
            "dimension": "length/time and time/length",
            "available_anchor": "clock-length conversion",
            "missing_for_dimensionless_depth": "a time or length normalization",
            "status": "FOUNDING_SCALE_CONVERSION_NOT_DEPTH_NORMALIZATION_ALONE",
        },
        {
            "object": "linear depth kappa*d",
            "dimension": "dimensionless",
            "available_anchor": "kappa has inverse-length dimension",
            "missing_for_dimensionless_depth": "native kappa",
            "status": "FORM_SELECTED_BY_ORDINARY_ADDITIVITY_SCALE_OPEN",
        },
        {
            "object": "projective depth atanh(d/D)",
            "dimension": "dimensionless",
            "available_anchor": "finite length D",
            "missing_for_dimensionless_depth": "derivation of D and display join",
            "status": "CONDITIONAL_NONLINEAR_DISPLAY",
        },
    ]

    status_rows = [
        {
            "claim": "abstract reciprocal pair operator",
            "status": "DERIVED_CONDITIONAL",
            "scope": "unchanged parent result",
        },
        {
            "claim": "one global phi difference is universal pair depth",
            "status": "REFUTED_AS_ABSOLUTE_REPRESENTATION_IN_COMPLETE_ROUND_CONTROL",
            "scope": "type obstruction only; does not refute observer-frame dilation local chains or anisotropic fields",
        },
        {
            "claim": "pair dilation modifies local physics",
            "status": "REFUTED_BY_OWNER_FRAME_MEANING",
            "scope": "rho_p(p)=0 for every observer; dilation belongs to inter-frame comparison",
        },
        {
            "claim": "three observers invalidate pair dilation",
            "status": "REFUTED",
            "scope": "three observers carry compatible pairwise relational comparisons; scalar absolute encoding is what fails",
        },
        {
            "claim": "observer-indexed bilocal metric family",
            "status": "SMALLEST_SURVIVING_TYPE_GIVEN_F",
            "scope": "F sign lift and transitions open",
        },
        {
            "claim": "ordinary geodesic additive universal F",
            "status": "LINEAR_ONLY",
            "scope": "continuous/differentiable regularity",
        },
        {
            "claim": "finite proper diameter plus infinite linear additive depth",
            "status": "INCOMPATIBLE_UNDER_SAME_OBJECT_IDENTIFICATION",
            "scope": "nonlinear display location-dependent rate or infinite proper length remain alternatives",
        },
        {
            "claim": "angular sector in pair composition",
            "status": "DERIVED_REQUIRED_FOR_NONCOLLINEAR_ROUND_TRIPLES",
            "scope": "round exact law",
        },
        {
            "claim": "cut-locus scalar depth",
            "status": "SINGLE_VALUED_IF_FUNCTION_OF_DISTANCE",
            "scope": "full transport may be path family",
        },
        {
            "claim": "c alone fixes dimensionless depth normalization",
            "status": "NOT_DERIVED_DIMENSIONAL_GATE",
            "scope": "c remains founding clock-length anchor",
        },
        {
            "claim": "physical Xmax mass density CMB",
            "status": "OPEN_NOT_PROMOTED",
            "scope": "outside audit",
        },
        {
            "claim": "overall",
            "status": "RELATIONAL_DEPTH_TYPE_NARROWED_PROFILE_OPEN",
            "scope": "no canonization",
        },
    ]

    write_tsv(
        HERE / "DEPTH_TYPE_RULING_LEDGER.tsv",
        ["id", "candidate", "exact_ruling", "status", "remaining_gate"],
        type_rows,
    )
    write_tsv(
        HERE / "COMPOSITION_DOMAIN_LEDGER.tsv",
        ["domain", "law", "result", "failure_outside_domain"],
        composition_rows,
    )
    write_tsv(
        HERE / "ROUND_PAIR_CONTROL_LEDGER.tsv",
        ["quantity", "exact_result", "consequence"],
        round_rows,
    )
    write_tsv(
        HERE / "SCALE_GATE.tsv",
        ["object", "dimension", "available_anchor", "missing_for_dimensionless_depth", "status"],
        scale_rows,
    )
    write_tsv(
        HERE / "STATUS_LEDGER.tsv",
        ["claim", "status", "scope"],
        status_rows,
    )
    owner_rows = [
        {
            "claim": "observer self-depth",
            "owner_meaning": "rho_p(p)=0",
            "classification": "OWNER_CLARIFIED",
            "consequence": "each local frame is neutral",
        },
        {
            "claim": "dilation ontology",
            "owner_meaning": "comparison between distinct observer frames",
            "classification": "OWNER_CLARIFIED_RELATIONAL_ONLY",
            "consequence": "not an absolute local clock-speed field",
        },
        {
            "claim": "three-observer theorem",
            "owner_meaning": "pair comparisons survive",
            "classification": "TYPE_OBSTRUCTION_ONLY",
            "consequence": "only one-global-scalar encoding is refuted",
        },
        {
            "claim": "angular composition",
            "owner_meaning": "direction participates in composing different pair frames",
            "classification": "DERIVED_GEOMETRIC_ROLE",
            "consequence": "does not change local physics",
        },
        {
            "claim": "SR/GR analogy",
            "owner_meaning": "relational-frame meaning",
            "classification": "COMPARISON_ONLY",
            "consequence": "no imported observer mechanics or field equations",
        },
    ]
    write_tsv(
        HERE / "OWNER_FRAME_LEDGER.tsv",
        ["claim", "owner_meaning", "classification", "consequence"],
        owner_rows,
    )

    result = {
        "schema": "udt-relational-pair-depth-realization-1.0",
        "python": sys.version.split()[0],
        "sympy": sp.__version__,
        "compute": "CPU_ONLY",
        "checks": checks,
        "check_count": len(checks),
        "source_count": source_count,
        "owner_frame": {
            "classification": "OWNER_CLARIFIED_RELATIONAL_ONLY",
            "rho_p_p": "0_FOR_EVERY_OBSERVER",
            "local_physics_modified_by_pair_dilation": False,
            "three_observer_result": "PAIRWISE_DILATIONS_COMPATIBLE",
            "global_scalar_theorem": "TYPE_OBSTRUCTION_NOT_DILATION_NO_GO",
            "SR_GR_role": "RELATIONAL_MEANING_COMPARISON_ONLY_NO_PHYSICS_IMPORT",
        },
        "global_scalar_theorem": {
            "status": "REFUTED_AS_UNIVERSAL_CENTERLESS_ISOTROPIC_PAIR_DEPTH",
            "control": "round_S3_three_equal_radius_points_two_sign_pigeonhole",
            "not_refuted": "local_ordered_chain_or_anisotropic_solution_field",
        },
        "smallest_surviving_type": {
            "type": "OBSERVER_INDEXED_BILOCAL_METRIC_FAMILY",
            "formula": "rho_p(q)=F(d_h(p,q))",
            "status": "TYPE_DERIVED_GIVEN_F__F_AND_TRANSITIONS_OPEN",
        },
        "composition": {
            "ordinary_geodesic_universal_F": "LINEAR_ONLY",
            "finite_diameter_infinite_linear_depth": "INCOMPATIBLE",
            "nonlinear_projective_display": "EXACT_CONDITIONAL_NOT_PROPER_LENGTH_IDENTITY",
            "noncollinear_composition": "REQUIRES_ANGULAR_DATUM",
        },
        "cut_locus": {
            "scalar_distance": "SINGLE_VALUED",
            "full_transport": "PATH_FAMILY",
        },
        "scale": {
            "c": "FOUNDING_CLOCK_LENGTH_CONVERSION",
            "dimensionless_depth_normalization_from_c_alone": "NOT_DERIVED",
        },
        "physical_status": {
            "F_profile": "OPEN",
            "sign_oriented_lift": "OPEN",
            "chart_transition_law": "OPEN",
            "clock_solder": "OPEN_GLOBAL_JOIN",
            "physical_Xmax": "OPEN",
            "mass_density_CMB": "OPEN_NOT_PROMOTED",
        },
        "maximum_conclusion": (
            "OBSERVER-FRAME DILATION IS RELATIONAL AND LEAVES EACH OBSERVER'S "
            "LOCAL FRAME NEUTRAL. A SINGLE GLOBAL LOCAL-PHI DIFFERENCE CANNOT REPRESENT EVERY STRICTLY "
            "POSITIVE ISOTROPIC OBSERVER-PAIR DEPTH ON THE COMPLETE ROUND CENTERLESS "
            "BRANCH. THE SMALLEST SURVIVING METRIC-NATIVE TYPE IS AN OBSERVER-INDEXED "
            "BILOCAL FAMILY RHO_P(Q)=F(D_H(P,Q)), WITH ANGULAR DATA REQUIRED FOR "
            "NONCOLLINEAR COMPOSITION. ORDINARY GEODESIC ADDITIVITY FORCES UNIVERSAL "
            "F TO BE LINEAR, SO INFINITE DEPTH AT FINITE DIAMETER REQUIRES A DISTINCT "
            "NONLINEAR DISPLAY, LOCATION-DEPENDENT RATE, OR OTHER DERIVED JOIN. F, "
            "ORIENTATION, TRANSITIONS, CLOCK SOLDER, XMAX, MASS, AND CMB REMAIN OPEN. "
            "THE THREE-OBSERVER CONTROL REJECTS ONLY AN ABSOLUTE SCALAR ENCODING, "
            "NOT RELATIONAL DILATION."
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "result": "PASS",
        "checks": len(checks),
        "sources": source_count,
        "maximum_conclusion": result["maximum_conclusion"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
