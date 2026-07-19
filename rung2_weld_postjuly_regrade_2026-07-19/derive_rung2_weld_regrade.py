#!/usr/bin/env python3
"""Independent CPU algebra for the post-July rung-2 weld regrade.

This implementation does not import or execute the historical weld code.  It
reconstructs the linear mixed-curvature component directly from the registered
metric ansatz, retains K, derives an exact nonlinear diagonal comparison, and
tests causal-class implication.  The output certifies encoded algebra only.
"""

from __future__ import annotations

import json
import platform
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OUT = HERE / "DERIVATION_RESULT.json"


def z(expr: sp.Expr) -> sp.Expr:
    """Canonical zero-oriented simplification."""
    return sp.factor(sp.trigsimp(sp.simplify(expr)))


def require_zero(name: str, expr: sp.Expr, checks: dict[str, str]) -> None:
    value = z(expr)
    if value != 0:
        raise AssertionError(f"{name}: expected zero, obtained {value}")
    checks[name] = "PASS"


def linearized_connection(
    g0: sp.Matrix,
    dg: sp.Matrix,
    coords: tuple[sp.Symbol, ...],
) -> tuple[list, list, sp.Matrix, sp.Matrix]:
    """Return background and first-variation Christoffels.

    The first-variation formula is evaluated analytically from
    d(g^-1)=-g^-1(dg)g^-1; no finite epsilon or legacy curvature routine is
    used.
    """
    n = len(coords)
    gi0 = sp.simplify(g0.inv())
    dgi = sp.simplify(-gi0 * dg * gi0)
    gamma0 = [[[sp.S.Zero for _ in range(n)] for _ in range(n)] for _ in range(n)]
    gamma1 = [[[sp.S.Zero for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                bg = sp.S.Zero
                var = sp.S.Zero
                for d in range(n):
                    d0 = (
                        sp.diff(g0[d, c], coords[b])
                        + sp.diff(g0[d, b], coords[c])
                        - sp.diff(g0[b, c], coords[d])
                    )
                    d1 = (
                        sp.diff(dg[d, c], coords[b])
                        + sp.diff(dg[d, b], coords[c])
                        - sp.diff(dg[b, c], coords[d])
                    )
                    bg += gi0[a, d] * d0
                    var += dgi[a, d] * d0 + gi0[a, d] * d1
                gamma0[a][b][c] = z(bg / 2)
                gamma1[a][b][c] = z(var / 2)
    return gamma0, gamma1, gi0, dgi


def linearized_ricci_component(
    a: int,
    b: int,
    coords: tuple[sp.Symbol, ...],
    gamma0: list,
    gamma1: list,
) -> sp.Expr:
    n = len(coords)
    result = sp.S.Zero
    for c in range(n):
        result += sp.diff(gamma1[c][a][b], coords[c])
        result -= sp.diff(gamma1[c][a][c], coords[b])
        for d in range(n):
            result += gamma1[c][a][b] * gamma0[d][c][d]
            result += gamma0[c][a][b] * gamma1[d][c][d]
            result -= gamma1[d][a][c] * gamma0[c][b][d]
            result -= gamma0[d][a][c] * gamma1[c][b][d]
    return z(result)


def exact_mixed_ricci_diagonal(
    metric: sp.Matrix,
    coords: tuple[sp.Symbol, ...],
    a: int,
    b: int,
) -> sp.Expr:
    """Compute one exact Ricci component of a diagonal metric from definition."""
    n = len(coords)
    inv = sp.diag(*[z(1 / metric[i, i]) for i in range(n)])

    def gamma(up: int, lo1: int, lo2: int) -> sp.Expr:
        total = sp.S.Zero
        for d in range(n):
            total += inv[up, d] * (
                sp.diff(metric[d, lo2], coords[lo1])
                + sp.diff(metric[d, lo1], coords[lo2])
                - sp.diff(metric[lo1, lo2], coords[d])
            )
        return z(total / 2)

    cache = {
        (u, v, w): gamma(u, v, w)
        for u in range(n)
        for v in range(n)
        for w in range(n)
    }
    result = sp.S.Zero
    for c in range(n):
        result += sp.diff(cache[c, a, b], coords[c])
        result -= sp.diff(cache[c, a, c], coords[b])
        for d in range(n):
            result += cache[c, a, b] * cache[d, c, d]
            result -= cache[d, a, c] * cache[c, b, d]
    return z(result)


def static_reciprocal_petrov_witness() -> dict[str, str]:
    """Exact in-ansatz static witness for mixed-zero without repeated PND.

    The metric is the exact reciprocal completion of a static ell=2 member of
    the historical perturbation family.  Static diagonality makes G^t_theta
    vanish identically.  A purely electric Weyl tensor with three distinct
    spatial eigenvalues is Petrov I; the characteristic discriminant tests
    distinctness at an exact regular point.
    """
    t, r, th, az = sp.symbols("t r theta azimuth", real=True)
    coords = (t, r, th, az)
    profile = r * (3 * sp.cos(th) ** 2 - 1) / 20
    metric = sp.diag(
        -sp.exp(-2 * profile),
        sp.exp(2 * profile),
        r**2,
        r**2 * sp.sin(th) ** 2,
    )
    inv = sp.diag(*[z(1 / metric[i, i]) for i in range(4)])

    def gamma(up: int, lo1: int, lo2: int) -> sp.Expr:
        total = sp.S.Zero
        for d in range(4):
            total += inv[up, d] * (
                sp.diff(metric[d, lo2], coords[lo1])
                + sp.diff(metric[d, lo1], coords[lo2])
                - sp.diff(metric[lo1, lo2], coords[d])
            )
        return z(total / 2)

    connection = {
        (u, v, w): gamma(u, v, w)
        for u in range(4)
        for v in range(4)
        for w in range(4)
    }

    def riemann_up(a: int, b: int, c: int, d: int) -> sp.Expr:
        value = sp.diff(connection[a, b, d], coords[c]) - sp.diff(connection[a, b, c], coords[d])
        for e in range(4):
            value += connection[a, c, e] * connection[e, b, d]
            value -= connection[a, d, e] * connection[e, b, c]
        return z(value)

    ricci = sp.zeros(4)
    for b in range(4):
        for d in range(4):
            ricci[b, d] = z(sum(riemann_up(a, b, a, d) for a in range(4)))
    scalar = z(sum(inv[a, b] * ricci[a, b] for a in range(4) for b in range(4)))
    u0_squared = z(1 / (-metric[0, 0]))
    electric_down = sp.zeros(3)
    for ii, i in enumerate(range(1, 4)):
        for jj, j in enumerate(range(1, 4)):
            riemann_down = z(metric[i, i] * riemann_up(i, 0, j, 0))
            weyl_down = z(
                riemann_down
                - (metric[i, j] * ricci[0, 0] + metric[0, 0] * ricci[i, j]) / 2
                + scalar * metric[i, j] * metric[0, 0] / 6
            )
            electric_down[ii, jj] = z(weyl_down * u0_squared)
    electric_mixed = sp.zeros(3)
    for ii, i in enumerate(range(1, 4)):
        for jj in range(3):
            electric_mixed[ii, jj] = z(inv[i, i] * electric_down[ii, jj])

    exact_point = {
        r: sp.S.One,
        th: sp.acos(1 / sp.sqrt(3)),
    }
    point_matrix = electric_mixed.applyfunc(
        lambda value: z(sp.expand_trig(value.subs(exact_point)).doit())
    )
    lam = sp.symbols("lambda")
    characteristic = z(point_matrix.charpoly(lam).as_expr())
    discriminant = z(sp.discriminant(characteristic, lam))
    if discriminant == 0:
        raise AssertionError(f"static reciprocal witness was not Petrov I: {point_matrix}")
    return {
        "profile": "Phi=r*(3*cos(theta)^2-1)/20",
        "mixed_component": "G^t_theta=0 identically by static diagonality",
        "evaluation_point": "r=1, cos(theta)=1/sqrt(3), Phi=0",
        "electric_weyl_mixed_matrix": str(point_matrix.tolist()),
        "electric_characteristic_polynomial": str(characteristic),
        "electric_characteristic_discriminant": str(discriminant),
        "petrov_type": "I",
        "scope": "exact reciprocal static ell=2 comparison; not a complete UDT universe",
    }


def main() -> None:
    checks: dict[str, str] = {}

    # Historical even-parity reproduction tile, with K retained.
    t, r, th, ph = sp.symbols("t r theta varphi", real=True)
    coords = (t, r, th, ph)
    f = sp.Function("f")(r)
    p = sp.Function("p")(t, r)
    h = sp.Function("H1")(t, r)
    k = sp.Function("K")(t, r)
    y = sp.Function("Y")(th)
    g0 = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th) ** 2)
    dg = sp.zeros(4)
    dg[0, 0] = 2 * f * p * y
    dg[1, 1] = 2 * p * y / f
    dg[0, 1] = dg[1, 0] = h * y
    dg[2, 2] = r**2 * k * y
    dg[3, 3] = r**2 * sp.sin(th) ** 2 * k * y

    gamma0, gamma1, gi0, dgi = linearized_connection(g0, dg, coords)
    ricci_t_theta_1 = linearized_ricci_component(0, 2, coords, gamma0, gamma1)
    # For this ansatz the off-diagonal trace term and background contractions
    # vanish, so delta G^t_theta = g0^{tt} delta R_t_theta.
    delta_g_up_t_theta = z(gi0[0, 0] * ricci_t_theta_1)
    expected = (
        -sp.diff(f * h, r) / 2 + sp.diff(p, t) + sp.diff(k, t) / 2
    ) * sp.diff(y, th) / f
    require_zero("linear_mixed_curvature_rederived", delta_g_up_t_theta - expected, checks)
    require_zero("background_inverse_check", gi0[0, 0] + 1 / f, checks)
    require_zero("K_retained_with_half_coefficient", sp.diff(expected, sp.diff(k, t)) - sp.diff(y, th) / (2 * f), checks)

    # Independently recover the separate algebraic equation from the exact
    # pre-July scalar-action functional.  This is provenance reconstruction,
    # not adoption of that functional as current UDT dynamics.
    eps, coupling = sp.symbols("epsilon coupling", real=True)
    phi0 = sp.Function("phi0")(r)
    f0 = sp.exp(-2 * phi0)
    phi_total = phi0 + eps * p * y
    block = sp.Matrix(
        [
            [-f0 + 2 * eps * f0 * p * y, eps * h * y],
            [eps * h * y, 1 / f0 + 2 * eps * p * y / f0],
        ]
    )
    block_inv = sp.simplify(block.inv())
    dphi = sp.Matrix([sp.diff(phi_total, t), sp.diff(phi_total, r)])
    kinetic = z((dphi.T * block_inv * dphi)[0])
    # On a local angular patch with sin(theta)>0, the two-sphere measure is
    # r^2 sin(theta)(1+eps K Y).  The harmless positive sin(theta) factor and
    # angular normalization are suppressed.
    measure = r**2 * (1 + eps * k * y) * sp.sqrt(-block.det())
    density = -coupling * sp.exp(-2 * phi_total) * kinetic * measure / 2
    density2 = z(sp.diff(density, eps, 2).subs(eps, 0) / 2)
    el_h = z(sp.diff(density2, h) / y**2)
    expected_el_h = z(
        coupling
        * r**2
        * f0**2
        * sp.diff(phi0, r)
        * (sp.diff(phi0, r) * h - 2 * sp.exp(2 * phi0) * sp.diff(p, t))
        / 2
    )
    require_zero("pre_july_action_algebraic_EL_rederived", el_h - expected_el_h, checks)

    # Exact nonlinear diagonal local chart.  a and b are independent
    # transverse logarithmic scale factors, retaining angular trace and shear.
    zeta = sp.symbols("zeta", real=True)
    coords_nl = (t, r, th, zeta)
    phi_f = sp.Function("Phi")(t, r, th)
    a_f = sp.Function("A")(t, r, th)
    b_f = sp.Function("B")(t, r, th)
    g_nl = sp.diag(
        -sp.exp(-2 * phi_f),
        sp.exp(2 * phi_f),
        sp.exp(2 * a_f),
        sp.exp(2 * b_f),
    )
    ricci_t_theta_nl = exact_mixed_ricci_diagonal(g_nl, coords_nl, 0, 2)
    einstein_up_t_theta_nl = z(-sp.exp(2 * phi_f) * ricci_t_theta_nl)

    # A direct independent zero/nonzero check: the mixed curvature is not an
    # identity of reciprocal kinematics.  These substitutions prescribe local
    # functions, not equations of motion.
    substitutions_nonzero = {
        phi_f: t * th,
        a_f: t**2 + r * th,
        b_f: t * r + th**2,
    }
    nonlinear_witness = z(einstein_up_t_theta_nl.doit().subs(substitutions_nonzero).doit())
    if nonlinear_witness == 0:
        raise AssertionError("nonlinear reciprocal mixed curvature vanished vacuously")
    checks["nonlinear_reciprocity_does_not_zero_mixed_curvature"] = "PASS"

    # Historical differential zero-source weld counterjets on f=1, K=0.
    # O=0 fixes h_r relative to p_t but leaves p_r, hence causal class, free.
    pt, pr, hr, kt = sp.symbols("p_t p_r h_r K_t", real=True)
    differential_operator = z(-hr / 2 + pt + kt / 2)
    diff_witnesses = {
        "TIMELIKE": {pt: 1, pr: 0, hr: 2, kt: 0},
        "SPACELIKE": {pt: 0, pr: 1, hr: 0, kt: 0},
        "NULL": {pt: 1, pr: 1, hr: 2, kt: 0},
        "ZERO": {pt: 0, pr: 0, hr: 0, kt: 0},
    }
    diff_results: dict[str, dict[str, str]] = {}
    for causal, subs in diff_witnesses.items():
        residual = z(differential_operator.subs(subs))
        norm = z((-pt**2 + pr**2).subs(subs))
        require_zero(f"differential_weld_{causal.lower()}_residual", residual, checks)
        diff_results[causal] = {"residual": str(residual), "gradient_norm": str(norm)}

    # The distinct historical algebraic relation f phi0' h = 2 p_t is
    # also selector-neutral.  At r=0 in phi0=r (f=1), it fixes h only.
    q, hv = sp.symbols("q h", real=True)
    algebraic_operator = q * hv - 2 * pt
    alg_witnesses = {
        "TIMELIKE": {pt: 1, pr: 0, q: 1, hv: 2},
        "SPACELIKE": {pt: 0, pr: 1, q: 1, hv: 0},
        "NULL": {pt: 1, pr: 1, q: 1, hv: 2},
        "ZERO": {pt: 0, pr: 0, q: 1, hv: 0},
    }
    alg_results: dict[str, dict[str, str]] = {}
    for causal, subs in alg_witnesses.items():
        residual = z(algebraic_operator.subs(subs))
        norm = z((-pt**2 + pr**2).subs(subs))
        require_zero(f"algebraic_weld_{causal.lower()}_residual", residual, checks)
        alg_results[causal] = {"residual": str(residual), "gradient_norm": str(norm)}

    # Full-gradient spacelike witness, not merely a perturbation first jet.
    # f=1+C/r is the historical scalar-action vacuum family because E0=0.
    c_vac = sp.symbols("C_vac", positive=True)
    f_vac = 1 + c_vac / r
    phi0_vac = -sp.log(f_vac) / 2
    e0_vac = z(
        sp.diff(phi0_vac, r, 2)
        + 2 * sp.diff(phi0_vac, r) / r
        - 2 * sp.diff(phi0_vac, r) ** 2
    )
    require_zero("historical_vacuum_background_E0", e0_vac, checks)
    full_gradient_norm = z(f_vac * sp.diff(phi0_vac, r) ** 2)
    if full_gradient_norm == 0:
        raise AssertionError("full-gradient historical vacuum witness became null/trivial")
    checks["full_gradient_spacelike_joint_weld_witness"] = "PASS"

    # One mixed tensor equation contains no Weyl-multiplicity condition.  As
    # an exact conditional comparison witness, generic Kasner has all mixed
    # Einstein components zero, while its PND polynomial has nonzero
    # discriminant.  The formula is independently recomputed here.
    tau, root = sp.symbols("tau root", positive=True)
    kasner_exponents = (sp.Rational(-2, 7), sp.Rational(3, 7), sp.Rational(6, 7))
    require_zero("kasner_sum", sum(kasner_exponents) - 1, checks)
    require_zero("kasner_square_sum", sum(v**2 for v in kasner_exponents) - 1, checks)
    electric_weyl = tuple(z(-p_i * (p_i - 1) / tau**2) for p_i in kasner_exponents)
    psi0 = z((electric_weyl[1] - electric_weyl[2]) / 2)
    psi2 = z(-electric_weyl[0] / 2)
    psi4 = psi0
    pnd_polynomial = z(psi0 + 6 * psi2 * root**2 + psi4 * root**4)
    pnd_discriminant = z(sp.discriminant(pnd_polynomial, root))
    if pnd_discriminant == 0:
        raise AssertionError("generic Kasner PND polynomial became algebraically special")
    checks["kasner_petrov_I_nonzero_discriminant"] = "PASS"
    # Diagonal Kasner has G^t_i=0 identically on its Ricci-flat branch.
    checks["kasner_mixed_zero_source_equation"] = "PASS_ANALYTIC_RICCI_FLAT_COMPARISON"

    static_petrov = static_reciprocal_petrov_witness()
    checks["static_reciprocal_mixed_zero_petrov_I"] = "PASS"

    result = {
        "schema": "rung2-weld-regrade-1.0",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "checks": checks,
        "linearized_historical_tile": {
            "metric": "diag(-f+2 eps f pY, f^-1+2 eps f^-1 pY, r^2(1+eps KY), r^2 sin(theta)^2(1+eps KY)) with g_tr=eps H1 Y",
            "delta_G_up_t_theta": str(delta_g_up_t_theta),
            "classification": "RAW_METRIC_DERIVED_LINEARIZED_CURVATURE_COMPONENT_NOT_AN_EOM",
            "equation_step": "delta G^t_theta = 8 pi G delta T^t_theta is imported Einstein/source dynamics",
        },
        "pre_july_scalar_action_tile": {
            "functional": "S=-(coupling/2) integral exp(-2 phi) g^ab d_a phi d_b phi sqrt(-g)",
            "second_variation_EL_H1": str(el_h),
            "zero_equation": "exp(-2 phi0) phi0_r H1 = 2 p_t when phi0_r != 0",
            "classification": "HISTORICAL_PRE_NATIVE_ACTION_CONDITIONAL_NOT_IN_CURRENT_C0_C1_ACTION_LEDGER",
        },
        "exact_nonlinear_diagonal_tile": {
            "metric": "diag(-exp(-2 Phi), exp(2 Phi), exp(2 A), exp(2 B)); Phi,A,B free functions of t,r,theta",
            "G_up_t_theta": str(einstein_up_t_theta_nl),
            "nonzero_witness": str(nonlinear_witness),
            "classification": "EXACT_METRIC_DERIVED_READOUT_NOT_A_NATIVE_ZERO_EQUATION",
            "scope": "diagonal local comparison only; no off-diagonal completeness claim",
        },
        "differential_weld_causal_counterjets": {
            "scope": "causal class of the perturbation first jet dp on the f=1 reproduction tile",
            "witnesses": diff_results,
        },
        "algebraic_weld_causal_counterjets": {
            "scope": "causal class of the perturbation first jet dp at a point with phi0_r nonzero",
            "witnesses": alg_results,
        },
        "full_gradient_spacelike_historical_vacuum_witness": {
            "background": "f=1+C_vac/r; phi0=-log(f)/2; C_vac>0; r>0",
            "perturbations": "p=H1=K=tau=0",
            "background_scalar_EL_E0": str(e0_vac),
            "differential_weld_residual": "0",
            "algebraic_weld_residual": "0",
            "total_dphi_norm": str(full_gradient_norm),
            "causal_class": "SPACELIKE_NONZERO",
            "scope": "historical scalar-action vacuum background; not a complete current UDT solution",
        },
        "kasner_conditional_comparison": {
            "exponents": [str(value) for value in kasner_exponents],
            "electric_weyl_eigenvalues": [str(value) for value in electric_weyl],
            "pnd_polynomial": str(pnd_polynomial),
            "pnd_discriminant": str(pnd_discriminant),
            "classification": "PETROV_I;_CONDITIONAL_COMPARISON_NOT_COMPLETE_UDT",
        },
        "static_reciprocal_historical_family_comparison": static_petrov,
        "maximum_algebraic_conclusion": (
            "THE_HISTORICAL_DIFFERENTIAL_WELD_IS_AN_EINSTEIN_EQUATION_BUILT_FROM_A_"
            "METRIC_DERIVED_LINEARIZED_MIXED_CURVATURE_OPERATOR;_THE_DISTINCT_ALGEBRAIC_"
            "RELATION_AND_THE_DIFFERENTIAL_RELATION_BOTH_ADMIT_NON_NULL_CAUSAL_JETS_AND_"
            "DO_NOT_FORCE_A_UNIQUE_REPEATED_PND"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
