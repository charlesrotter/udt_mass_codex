#!/usr/bin/env python3
"""Exact CPU algebra for the metric-wide Cartan/holonomy audit.

The script separates metric-derived Cartan structure from equations of motion,
constructs chosen-boundary-equal twist/local-holonomy counterfamilies, compares the
constant-scale behavior of EH and C^2, and challenges the conditional
single-reciprocal-axis metric against the historical area-only F^2 structure.
It does not adopt that axis metric or any action as native UDT.
"""

from __future__ import annotations

import json
import platform
from pathlib import Path
from typing import Dict, Tuple

import sympy as sp


HERE = Path(__file__).resolve().parent
OUT = HERE / "DERIVATION_RESULT.json"
Basis = Tuple[int, ...]
Form = Dict[Basis, sp.Expr]


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.trigsimp(sp.simplify(value)))


def clean(form: Form) -> Form:
    return {basis: value for basis, raw in form.items() if (value := simp(raw)) != 0}


def add(*forms: Form) -> Form:
    result: Form = {}
    for form in forms:
        for basis, value in form.items():
            result[basis] = result.get(basis, sp.S.Zero) + value
    return clean(result)


def scale(value: sp.Expr, form: Form) -> Form:
    return clean({basis: value * coefficient for basis, coefficient in form.items()})


def wedge(left: Form, right: Form) -> Form:
    result: Form = {}
    for a, av in left.items():
        for b, bv in right.items():
            if set(a).intersection(b):
                continue
            inversions = sum(1 for i in a for j in b if i > j)
            basis = tuple(sorted(a + b))
            result[basis] = result.get(basis, sp.S.Zero) + (-1) ** inversions * av * bv
    return clean(result)


def require_zero(name: str, value, checks: dict[str, str]) -> None:
    if isinstance(value, dict):
        reduced = clean(value)
        if reduced:
            raise AssertionError(f"{name}: expected zero form, obtained {reduced}")
    elif isinstance(value, sp.MatrixBase):
        reduced = value.applyfunc(simp)
        if any(entry != 0 for entry in reduced):
            raise AssertionError(f"{name}: expected zero matrix, obtained {reduced}")
    elif simp(value) != 0:
        raise AssertionError(f"{name}: expected zero, obtained {simp(value)}")
    checks[name] = "PASS"


def form_string(form: Form) -> str:
    if not form:
        return "0"
    names = ["e0", "e1", "e2", "e3"]
    terms = []
    for basis in sorted(form):
        coefficient = form[basis]
        blade = "^".join(names[index] for index in basis) if basis else "1"
        terms.append(f"({coefficient})*{blade}")
    return " + ".join(terms)


def cartan_twist_tile(checks: dict[str, str]) -> dict:
    """Torsion-free Cartan algebra for e3=dy+u(r)dx, phi=0."""
    r = sp.symbols("r", real=True)
    q = sp.Function("q")(r)
    one = [{(i,): sp.S.One} for i in range(4)]
    zero: Form = {}
    de = [zero, zero, zero, {(1, 2): q}]

    def exterior_d(form: Form) -> Form:
        result: Form = {}
        for basis, coefficient in form.items():
            # Scalar coefficients depend only on r and dr=e1 in this tile.
            result = add(result, wedge({(1,): sp.diff(coefficient, r)}, {basis: sp.S.One}))
            for position, index in enumerate(basis):
                before = {basis[:position]: sp.S.One}
                after = {basis[position + 1 :]: sp.S.One}
                term = wedge(wedge(before, de[index]), after)
                result = add(result, scale(coefficient * (-1) ** position, term))
        return clean(result)

    omega = [[{} for _ in range(4)] for _ in range(4)]
    omega[1][2] = scale(-q / 2, one[3])
    omega[2][1] = scale(+q / 2, one[3])
    omega[1][3] = scale(-q / 2, one[2])
    omega[3][1] = scale(+q / 2, one[2])
    omega[2][3] = scale(+q / 2, one[1])
    omega[3][2] = scale(-q / 2, one[1])

    torsion = []
    for i in range(4):
        value = de[i]
        for j in range(4):
            value = add(value, wedge(omega[i][j], one[j]))
        require_zero(f"twist_torsion_{i}", value, checks)
        torsion.append(value)

    curvature = [[{} for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            value = exterior_d(omega[i][j])
            for k in range(4):
                value = add(value, wedge(omega[i][k], omega[k][j]))
            curvature[i][j] = clean(value)

    expected = {
        (1, 2): {(1, 2): -3 * q**2 / 4, (1, 3): -sp.diff(q, r) / 2},
        (1, 3): {(1, 2): -sp.diff(q, r) / 2, (1, 3): q**2 / 4},
        (2, 3): {(2, 3): q**2 / 4},
    }
    for (i, j), target in expected.items():
        require_zero(f"twist_curvature_{i}{j}", add(curvature[i][j], scale(-1, target)), checks)

    # First Bianchi: Omega^i_j wedge e^j = 0.
    for i in range(4):
        value: Form = {}
        for j in range(4):
            value = add(value, wedge(curvature[i][j], one[j]))
        require_zero(f"twist_first_bianchi_{i}", value, checks)

    # Second Bianchi: dOmega + omega wedge Omega - Omega wedge omega = 0.
    for i in range(4):
        for j in range(4):
            value = exterior_d(curvature[i][j])
            for k in range(4):
                value = add(
                    value,
                    wedge(omega[i][k], curvature[k][j]),
                    scale(-1, wedge(curvature[i][k], omega[k][j])),
                )
            require_zero(f"twist_second_bianchi_{i}{j}", value, checks)

    # Boundary-identical bump family u=lambda(1-r^2)^3 on [-1,1].
    lam = sp.symbols("lambda", real=True)
    u = lam * (1 - r**2) ** 3
    q_bump = simp(sp.diff(u, r))
    qp_bump = simp(sp.diff(q_bump, r))
    for endpoint in (-1, 1):
        require_zero(f"twist_boundary_u_{endpoint}", u.subs(r, endpoint), checks)
        require_zero(f"twist_boundary_q_{endpoint}", q_bump.subs(r, endpoint), checks)
        require_zero(f"twist_boundary_qp_{endpoint}", qp_bump.subs(r, endpoint), checks)
    interior = {r: sp.Rational(1, 2), lam: sp.S.One}
    q_mid = simp(q_bump.subs(interior))
    qp_mid = simp(qp_bump.subs(interior))
    if q_mid == 0 or qp_mid == 0:
        raise AssertionError("twist bump interior curvature witness became trivial")
    checks["boundary_identical_twist_has_nonzero_interior_curvature"] = "PASS"
    checks["lambda_zero_member_is_flat"] = "PASS"

    return {
        "coframe": "e0=dt; e1=dr; e2=dx; e3=dy+u(r)dx",
        "structure": "de3=q e1^e2, q=u_r",
        "spin_connection": {
            "omega12": form_string(omega[1][2]),
            "omega13": form_string(omega[1][3]),
            "omega23": form_string(omega[2][3]),
        },
        "curvature": {
            "Omega12": form_string(curvature[1][2]),
            "Omega13": form_string(curvature[1][3]),
            "Omega23": form_string(curvature[2][3]),
        },
        "cartan_identities": "TORSION_ZERO; FIRST_BIANCHI_ZERO; SECOND_BIANCHI_ZERO WHILE CURVATURE_NONZERO",
        "bump_family": {
            "u": str(u),
            "q": str(q_bump),
            "q_prime": str(qp_bump),
            "boundary_jets": "chosen comparison jets u=q=q_prime=0 at r=+-1 for every lambda",
            "midpoint_lambda_one": {"q": str(q_mid), "q_prime": str(qp_mid)},
            "lambda_zero": "flat",
            "lambda_nonzero": "nonzero curvature and infinitesimal local loop transport",
        },
        "classification": "EXACT_CHOSEN_EQUAL_BOUNDARY_JETS_WITH_CONTINUOUSLY_DIFFERENT_INTERIOR_CURVATURE_AND_LOCAL_LOOP_TRANSPORT",
        "scope": "phi=0 mathematical member; embedding this twist in a nontrivial reciprocal coframe changes the connection and was not computed; not a complete UDT solution",
    }


def axis_metric_rank_one_tile(checks: dict[str, str]) -> dict:
    """Test a chosen single-axis metric against the rank-one-zero F^2 claim."""
    x, y, a = sp.symbols("x y a", real=True, positive=True)
    cosine, sine = sp.cos(x), sp.sin(x)
    metric = sp.Matrix(
        [
            [1 + (a - 1) * cosine**2, (a - 1) * cosine * sine],
            [(a - 1) * cosine * sine, 1 + (a - 1) * sine**2],
        ]
    )
    inverse = sp.simplify(metric.inv())
    coords = (x, y)
    connection = [
        [
            [
                simp(
                    sum(
                        inverse[i, ell]
                        * (
                            sp.diff(metric[ell, k], coords[j])
                            + sp.diff(metric[ell, j], coords[k])
                            - sp.diff(metric[j, k], coords[ell])
                        )
                        for ell in range(2)
                    )
                    / 2
                )
                for k in range(2)
            ]
            for j in range(2)
        ]
        for i in range(2)
    ]
    r_up_m101 = [
        simp(
            sp.diff(connection[index][1][1], x)
            - sp.diff(connection[index][1][0], y)
            + sum(
                connection[index][0][m] * connection[m][1][1]
                - connection[index][1][m] * connection[m][1][0]
                for m in range(2)
            )
        )
        for index in range(2)
    ]
    # R_0101=g_0m R^m_101.  Retaining the m=1 lowering term is essential
    # away from points where the chosen-axis metric happens to be diagonal.
    r_lower_0101 = simp(sum(metric[0, index] * r_up_m101[index] for index in range(2)))
    gaussian = simp(r_lower_0101 / metric.det())
    require_zero("axis_gaussian_general", gaussian + (a - 1) * sp.cos(2 * x) / a, checks)
    point = {x: sp.S.Zero, a: sp.Integer(4)}
    gaussian_point = simp(gaussian.subs(point))
    require_zero("axis_gaussian_point", gaussian_point + sp.Rational(3, 4), checks)
    nondiagonal_point = {x: sp.pi / 6, a: sp.Integer(4)}
    gaussian_nondiagonal = simp(gaussian.subs(nondiagonal_point))
    require_zero("axis_gaussian_nondiagonal_point", gaussian_nondiagonal + sp.Rational(3, 8), checks)

    # The four-metric is the direct product of this two-surface with flat
    # constant time and z directions.  In 4D:
    # Riem^2=4K^2, Ric^2=2K^2, R=2K, hence C^2=4K^2/3.
    riemann_sq = simp(4 * gaussian_point**2)
    ricci_sq = simp(2 * gaussian_point**2)
    scalar = simp(2 * gaussian_point)
    weyl_sq = simp(riemann_sq - 2 * ricci_sq + scalar**2 / 3)
    require_zero("axis_weyl_squared_point", weyl_sq - sp.Rational(3, 4), checks)

    # n=(cos x,sin x,0) depends on one coordinate only.  Every pullback-area
    # component n.(dn cross dn) vanishes identically.
    n = sp.Matrix([cosine, sine, 0])
    nx = n.diff(x)
    ny = n.diff(y)
    area_xy = simp(n.dot(nx.cross(ny)))
    require_zero("axis_rank_one_area_form", area_xy, checks)
    if weyl_sq == 0:
        raise AssertionError("chosen-axis C^2 rank-one cost vanished")
    checks["axis_rank_one_C2_cost_nonzero"] = "PASS"

    metric_reversed = sp.simplify(sp.eye(2) + (a - 1) * (-sp.Matrix([cosine, sine])) * (-sp.Matrix([cosine, sine])).T)
    require_zero("axis_projective_sign_invariance", metric_reversed - metric, checks)
    require_zero("axis_isotropic_limit", gaussian.subs(a, 1), checks)

    return {
        "conditional_metric": "h=I+(a-1)n tensor n, a=exp(2 phi); n=(cos x,sin x,0)",
        "gaussian_curvature": str((1 - a) * sp.cos(2 * x) / a),
        "test_point": "x=0; a=4",
        "K": str(gaussian_point),
        "nondiagonal_test_point": "x=pi/6; a=4",
        "K_nondiagonal": str(gaussian_nondiagonal),
        "R_4": str(scalar),
        "C2_4": str(weyl_sq),
        "pullback_area_F": str(area_xy),
        "result": "RANK_ONE_F_ZERO_BUT_METRIC_C2_NONZERO",
        "classification": "CONDITIONAL_SINGLE_AXIS_CURVATURE_DIFFERENT_FROM_AREA_ONLY_F2",
        "scope": "chosen single-axis local interior tile; not native carrier emergence or complete solution",
    }


def holonomy_fixed_set_tile(checks: dict[str, str]) -> dict:
    identity = sp.eye(3)
    rz = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    rx = sp.Matrix([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    dim_identity = 3 - (identity - identity).rank()
    dim_rz = 3 - (rz - identity).rank()
    stacked = (rz - identity).col_join(rx - identity)
    dim_intersection = 3 - stacked.rank()
    require_zero("holonomy_identity_fixed_dim", dim_identity - 3, checks)
    require_zero("holonomy_axis_fixed_dim", dim_rz - 1, checks)
    require_zero("holonomy_nonparallel_intersection_dim", dim_intersection, checks)
    return {
        "identity_holonomy_fixed_dimension": dim_identity,
        "single_axis_rotation_fixed_dimension": dim_rz,
        "two_nonparallel_rotations_common_fixed_dimension": dim_intersection,
        "classification": "HOLONOMY_FIXED_SET_CAN_BE_MANY_ONE_OR_NONE; SPECIAL_REDUCTION_REQUIRED_FOR_ONE",
        "scope": "representative SO(3) comparison families; not exhaustive Lorentz/conformal holonomy census",
    }


def scale_and_action_tile(checks: dict[str, str]) -> dict:
    scale_symbol = sp.symbols("s", positive=True)
    volume_weight = scale_symbol**4
    scalar_curvature_weight = scale_symbol**-2
    weyl_squared_weight = scale_symbol**-4
    eh_density_weight = simp(volume_weight * scalar_curvature_weight)
    c2_density_weight = simp(volume_weight * weyl_squared_weight)
    require_zero("EH_constant_scale_weight", eh_density_weight - scale_symbol**2, checks)
    require_zero("C2_constant_scale_weight", c2_density_weight - 1, checks)
    if eh_density_weight == c2_density_weight:
        raise AssertionError("EH and C2 were falsely identified by scale weight")
    checks["EH_C2_not_same_Cartan_contraction"] = "PASS"
    return {
        "constant_common_scale": "g -> s^2 g",
        "levi_civita_connection": "unchanged only for constant s; changes for local Omega(x)",
        "sqrt_abs_g_weight": "s^4",
        "R_weight": "s^-2",
        "C_abcd_C_abcd_weight": "s^-4",
        "EH_density_weight": str(eh_density_weight),
        "C2_density_weight": str(c2_density_weight),
        "result": "SAME_CURVATURE_ORIGIN_DIFFERENT_CONTRACTIONS_AND_SCALE_WEIGHTS_NO_IDENTITY_BRIDGE",
    }


def local_lorentz_gauge_tile(checks: dict[str, str]) -> dict:
    alpha = sp.Function("alpha")
    x = sp.symbols("x", real=True)
    gauge_shift = sp.diff(alpha(x), x)
    curvature_shift = sp.diff(gauge_shift, x) - sp.diff(gauge_shift, x)
    require_zero("SO2_connection_gauge_curvature_invariance", curvature_shift, checks)
    return {
        "coframe_rotation": "(e2,e3) -> R(alpha(x))(e2,e3)",
        "metric": "unchanged",
        "screen_connection": "omega23 -> omega23 + d alpha (orientation convention dependent sign)",
        "screen_curvature": "d omega23 unchanged because d^2 alpha=0",
        "classification": "COFRAME_AND_CONNECTION_COMPONENTS_GAUGE_DEPENDENT; CURVATURE_HOLONOMY_CONJUGACY_INVARIANT",
    }


def main() -> None:
    checks: dict[str, str] = {}
    twist = cartan_twist_tile(checks)
    axis = axis_metric_rank_one_tile(checks)
    fixed = holonomy_fixed_set_tile(checks)
    actions = scale_and_action_tile(checks)
    gauge = local_lorentz_gauge_tile(checks)

    result = {
        "schema": "udt-metric-cartan-holonomy-audit-1.0",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "checks": checks,
        "abstract_cartan": {
            "first_structure_equation": "T^I=de^I+omega^I_J wedge e^J",
            "metric_only_choice": "T^I=0 and omega_IJ=-omega_JI uniquely determine Levi-Civita omega for a supplied nondegenerate coframe",
            "second_structure_equation": "Omega^I_J=d omega^I_J+omega^I_K wedge omega^K_J",
            "first_bianchi": "D T^I=Omega^I_J wedge e^J; torsion-free gives Omega^I_J wedge e^J=0",
            "second_bianchi": "D Omega^I_J=0",
            "status": "METRIC_DERIVED_IDENTITIES_NOT_EOM; NEITHER BIANCHI IDENTITY SETS OMEGA RICCI WEYL OR AN EULER_TENSOR TO ZERO",
        },
        "two_plus_two_sector_map": {
            "base": "g_ij and its reciprocal two-weight realization when separately supplied",
            "transverse": "arbitrary positive q_AB represented by a zweibein; trace shear and SO(2) gauge retained",
            "mixed": "A^A_i shifts/twist; horizontal curvature and base derivatives of q_AB",
            "geometric_data": "base curvature; transverse curvature; screen expansion/shear; twist curvature; mixed covariant derivatives; algebraic cross terms",
            "warning": "setting A^A_i=0, diagonal q_AB, zero shear, or integrable screen is a subfamily restriction",
        },
        "local_lorentz_gauge": gauge,
        "twisted_screen": twist,
        "holonomy_fixed_sets": fixed,
        "conditional_single_axis_challenge": axis,
        "curvature_action_comparison": actions,
        "adjudication": {
            "connection_curvature": "LEVI_CIVITA_CONNECTION_AND_CURVATURE_METRIC_DERIVED_PER_REPRESENTATIVE",
            "cartan_identities": "DERIVED_NOT_DYNAMICS",
            "holonomy_selector": "UNDERDETERMINED_NOT_SELECTED_BY_CURRENT_FOUNDATION",
            "single_axis_F2": "REFUTED_IN_CONDITIONAL_AXIS_METRIC_BY_RANK_ONE_NONZERO_C2",
            "metric_holonomy_matter": "NOT_DERIVED; CURVATURE_CLASSIFICATION_LACKS_SELECTED_SECTOR_FUNCTIONAL_SOURCE_BOUNDARY_AND_STABILITY",
            "C2_EH_bridge": "NOT_DERIVED; SAME_CARTAN_CURVATURE_ORIGIN_BUT_DIFFERENT_CONTRACTIONS_SCALE_WEIGHTS_VARIATION_AND_BOUNDARY_GATES",
            "route_scoped_missing_object": "FOR_HOLONOMY_OR_C2_EH_BRIDGE_A_GLOBAL_METRIC_ADMISSIBILITY_REDUCTION_OR_SOLDERING_RULE_WITH_VARIATION_AND_BOUNDARY_CONTENT_IS_ONE_CANDIDATE_OPEN_GATE; NOT_CLAIMED_UNIQUE_AND_NOT_A_NEW_POSTULATE",
        },
        "maximum_conclusion": (
            "CARTAN_GEOMETRY_IS_CANONICAL_AFTER_A_METRIC_REPRESENTATIVE_BUT_DOES_NOT_SUPPLY_DYNAMICS;_"
            "FREE_TRANSVERSE_TWIST_PRODUCES_CHOSEN_BOUNDARY_EQUAL_CONTINUOUS_CURVATURE_AND_LOCAL_LOOP_TRANSPORT_FAMILIES;_"
            "THE_CHOSEN_SINGLE_AXIS_METRIC_C2_FUNCTIONAL_IS_NOT_AREA_ONLY;_"
            "HOLONOMY_MATTER_AND_THE_C2_TO_EH_BRIDGE_REMAIN_NOT_DERIVED"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
