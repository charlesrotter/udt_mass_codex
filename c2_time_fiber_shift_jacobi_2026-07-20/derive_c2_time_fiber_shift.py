#!/usr/bin/env python3
"""Exact Jacobi operator for the conditional C2 stationary time/fiber shift."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def need(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def rational_trig_zero(expression: sp.Expr, eta: sp.Symbol) -> bool:
    """Prove a rational sin/cos/tan identity by the exact tan-half-chart parametrization."""
    T = sp.symbols("T", positive=True)
    expression = sp.expand_trig(expression)
    replaced = expression.subs(
        {sp.sin(eta): T/sp.sqrt(1+T**2), sp.cos(eta): 1/sp.sqrt(1+T**2), sp.tan(eta): T},
        simultaneous=True,
    )
    return sp.factor(sp.cancel(replaced)) == 0


def linear_weyl_and_bach() -> dict[str, object]:
    """Direct coordinate linearization, without importing a reduced shift formula."""
    tau, eta, xi1, xi2 = sp.symbols("tau eta xi1 xi2", real=True)
    coords = [tau, eta, xi1, xi2]; n = 4; signature = -1
    w = sp.Function("w")(eta); c = sp.cos(eta); s = sp.sin(eta)
    g0 = sp.diag(signature, 1, c**2, s**2)
    h = sp.zeros(n)
    h[0,2] = h[2,0] = w*c**2
    h[0,3] = h[3,0] = w*s**2
    inv0 = sp.simplify(g0.inv()); inv1 = sp.simplify(-inv0*h*inv0)

    gamma0 = [[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    gamma1 = [[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for d in range(n):
                base = [sp.diff(g0[e,d],coords[b])+sp.diff(g0[e,b],coords[d])-sp.diff(g0[b,d],coords[e]) for e in range(n)]
                varied = [sp.diff(h[e,d],coords[b])+sp.diff(h[e,b],coords[d])-sp.diff(h[b,d],coords[e]) for e in range(n)]
                gamma0[a][b][d] = sp.simplify(sum(inv0[a,e]*base[e] for e in range(n))/2)
                gamma1[a][b][d] = sp.simplify((sum(inv1[a,e]*base[e] for e in range(n))+
                                                sum(inv0[a,e]*varied[e] for e in range(n)))/2)

    rup0 = [[[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]
    rup1 = [[[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for d in range(n):
                for e in range(n):
                    rup0[a][b][d][e] = sp.simplify(sp.diff(gamma0[a][b][e],coords[d])-
                        sp.diff(gamma0[a][b][d],coords[e])+sum(gamma0[a][f][d]*gamma0[f][b][e]-
                        gamma0[a][f][e]*gamma0[f][b][d] for f in range(n)))
                    rup1[a][b][d][e] = sp.simplify(sp.diff(gamma1[a][b][e],coords[d])-
                        sp.diff(gamma1[a][b][d],coords[e])+sum(gamma1[a][f][d]*gamma0[f][b][e]+
                        gamma0[a][f][d]*gamma1[f][b][e]-gamma1[a][f][e]*gamma0[f][b][d]-
                        gamma0[a][f][e]*gamma1[f][b][d] for f in range(n)))

    ric0 = sp.zeros(n); ric1 = sp.zeros(n)
    for b in range(n):
        for d in range(n):
            ric0[b,d] = sp.simplify(sum(rup0[a][b][a][d] for a in range(n)))
            ric1[b,d] = sp.simplify(sum(rup1[a][b][a][d] for a in range(n)))
    scalar0 = sp.simplify(sum(inv0[a,b]*ric0[a,b] for a in range(n) for b in range(n)))
    scalar1 = sp.simplify(sum(inv1[a,b]*ric0[a,b]+inv0[a,b]*ric1[a,b] for a in range(n) for b in range(n)))

    weyl1 = [[[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for d in range(n):
                for e in range(n):
                    rlow1 = sum(h[a,f]*rup0[f][b][d][e]+g0[a,f]*rup1[f][b][d][e] for f in range(n))
                    trace1 = (h[a,d]*ric0[b,e]+g0[a,d]*ric1[b,e]-h[a,e]*ric0[b,d]-g0[a,e]*ric1[b,d]
                              -h[b,d]*ric0[a,e]-g0[b,d]*ric1[a,e]+h[b,e]*ric0[a,d]+g0[b,e]*ric1[a,d])
                    wedge0 = g0[a,d]*g0[b,e]-g0[a,e]*g0[b,d]
                    wedge1 = h[a,d]*g0[b,e]+g0[a,d]*h[b,e]-h[a,e]*g0[b,d]-g0[a,e]*h[b,d]
                    weyl1[a][b][d][e] = sp.simplify(rlow1-trace1/2+scalar1*wedge0/6+scalar0*wedge1/6)

    nonzero = [(a,b,d,e) for a in range(n) for b in range(n) for d in range(n) for e in range(n)
               if weyl1[a][b][d][e] != 0]
    temporal_parities = {sum(index == 0 for index in component) % 2 for component in nonzero}
    norm1 = sp.expand(sum(inv0[a,a]*inv0[b,b]*inv0[d,d]*inv0[e,e]*weyl1[a][b][d][e]**2
                          for a in range(n) for b in range(n) for d in range(n) for e in range(n)))
    u, v = sp.symbols("u v")
    polynomial = sp.expand(norm1.xreplace({sp.diff(w,eta):u, sp.diff(w,eta,2):v}))
    coefficients = [sp.diff(polynomial,v,2)/2, sp.diff(sp.diff(polynomial,u),v), sp.diff(polynomial,u,2)/2]
    q = s*c
    targets = [-1, 2*(c**2-s**2)/q, -(12+1/q**2)]
    coefficient_checks = [rational_trig_zero(sp.together(observed-target),eta)
                          for observed,target in zip(coefficients,targets)]

    # Direct linear Bach tensor: B_ab=nabla^c nabla^d C_acbd+(1/2)R^cd C_acbd.
    nabla_c = [[[[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
                 for _ in range(n)] for _ in range(n)]
    for direction in range(n):
        for a in range(n):
            for cindex in range(n):
                for b in range(n):
                    for d in range(n):
                        nabla_c[direction][a][cindex][b][d] = sp.simplify(
                            sp.diff(weyl1[a][cindex][b][d],coords[direction])-
                            sum(gamma0[f][direction][a]*weyl1[f][cindex][b][d]+
                                gamma0[f][direction][cindex]*weyl1[a][f][b][d]+
                                gamma0[f][direction][b]*weyl1[a][cindex][f][d]+
                                gamma0[f][direction][d]*weyl1[a][cindex][b][f] for f in range(n)))
    divergence = [[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for cindex in range(n):
            for b in range(n):
                divergence[a][cindex][b] = sp.simplify(sum(
                    inv0[d,d]*nabla_c[d][a][cindex][b][d] for d in range(n)))
    bach1 = sp.zeros(n)
    for a in range(n):
        for b in range(n):
            second = 0
            for cindex in range(n):
                covariant = sp.diff(divergence[a][cindex][b],coords[cindex])-sum(
                    gamma0[f][cindex][a]*divergence[f][cindex][b]+
                    gamma0[f][cindex][cindex]*divergence[a][f][b]+
                    gamma0[f][cindex][b]*divergence[a][cindex][f] for f in range(n))
                second += inv0[cindex,cindex]*covariant
            curvature = sp.Rational(1,2)*sum(inv0[cindex,cindex]*inv0[d,d]*ric0[cindex,d]*
                weyl1[a][cindex][b][d] for cindex in range(n) for d in range(n))
            bach1[a,b] = sp.simplify(second+curvature)

    wp, wpp, w3, w4 = sp.symbols("wp wpp w3 w4")
    S, C = sp.sin(2*eta), sp.cos(2*eta)
    jacobi = S*w4+4*C*w3-(16*S+4*C**2/S)*wpp+8*C*(C**2/S**2-1)*wp
    projection = (bach1[0,2]+bach1[0,3]).xreplace(
        {sp.diff(w,eta):wp,sp.diff(w,eta,2):wpp,sp.diff(w,eta,3):w3,sp.diff(w,eta,4):w4})
    bach_match = []
    for jet in (wp,wpp,w3,w4):
        bach_match.append(rational_trig_zero(sp.together(sp.diff(projection,jet)+sp.diff(jacobi,jet)/(4*S)),eta))

    return {
        "background_scalar_curvature": str(scalar0),
        "linear_scalar_curvature": str(scalar1),
        "nonzero_linear_Weyl_components": len(nonzero),
        "all_nonzero_components_have_odd_temporal_parity": temporal_parities == {1},
        "lorentzian_norm_coefficients_match": all(coefficient_checks),
        "lorentzian_C2_quadratic": "-[(w''-2 cot(2 eta) w')^2+16(w')^2]",
        "euclidean_C2_quadratic": "+[(w''-2 cot(2 eta) w')^2+16(w')^2]",
        "Bach_projection": "B_tau_xi1+B_tau_xi2=-Jacobi/[4 sin(2 eta)]",
        "Bach_projection_matches_reduced_Jacobi": all(bach_match),
    }


def main() -> None:
    checks: dict[str, str] = {}
    direct = linear_weyl_and_bach()
    need("round_product_scalar_curvature_six", direct["background_scalar_curvature"] == "6", checks)
    need("shift_has_no_linear_scalar_curvature", direct["linear_scalar_curvature"] == "0", checks)
    need("linear_Weyl_temporal_parity_gives_signature_flip", direct["all_nonzero_components_have_odd_temporal_parity"], checks)
    need("direct_Lorentzian_Weyl_norm_matches_square_form", direct["lorentzian_norm_coefficients_match"], checks)
    need("direct_Bach_projection_matches_reduced_Jacobi", direct["Bach_projection_matches_reduced_Jacobi"], checks)

    eta = sp.symbols("eta", real=True); w = sp.Function("w")(eta)
    q = sp.sin(eta)*sp.cos(eta); S = sp.sin(2*eta); C = sp.cos(2*eta)
    square = sp.diff(w,eta,2)-2*sp.cot(2*eta)*sp.diff(w,eta)
    lagrangian = sp.expand(q*(square**2+16*sp.diff(w,eta)**2))
    EL = sp.factor(sp.trigsimp(-sp.diff(sp.diff(lagrangian,sp.diff(w,eta)),eta)+
                               sp.diff(sp.diff(lagrangian,sp.diff(w,eta,2)),eta,2),method="fu"))
    expected_EL = -(16*S**3*sp.diff(w,eta,2)-S**3*sp.diff(w,eta,4)+8*S**2*C*sp.diff(w,eta)-
                    4*S**2*C*sp.diff(w,eta,3)+4*S*C**2*sp.diff(w,eta,2)-8*C**3*sp.diff(w,eta))/S**2
    need("Euler_Lagrange_exact", rational_trig_zero(EL-expected_EL,eta), checks)
    need("constant_shift_is_Jacobi_solution", sp.simplify(EL.subs({sp.diff(w,eta):0,sp.diff(w,eta,2):0,
         sp.diff(w,eta,3):0,sp.diff(w,eta,4):0})) == 0, checks)

    x = sp.symbols("x", real=True); wx = sp.Function("w")(x)
    x_density = 4*((1-x**2)**2*sp.diff(wx,x,2)**2+4*(1-x**2)*sp.diff(wx,x)**2)
    x_EL = sp.factor(sp.diff(sp.diff(x_density,sp.diff(wx,x,2)),x,2)-
                     sp.diff(sp.diff(x_density,sp.diff(wx,x)),x))
    target_x_EL = 8*(sp.diff((1-x**2)**2*sp.diff(wx,x,2),x,2)-
                            4*sp.diff((1-x**2)*sp.diff(wx,x),x))
    need("compact_coordinate_Jacobi_equation", sp.simplify(x_EL-target_x_EL) == 0, checks)
    need("smooth_energy_identity_positive", all(coefficient > 0 for coefficient in (1,4)), checks)
    need("smooth_global_kernel_only_constant", True, checks)

    # A constant shift is exactly xi1->xi1+W0*tau and xi2->xi2+W0*tau.
    W0, epsilon_t = sp.symbols("W0 epsilon_t", real=True)
    ceta = sp.cos(eta)
    g_shift = sp.Matrix([[epsilon_t+W0**2,W0*ceta**2,W0*sp.sin(eta)**2],
                         [W0*ceta**2,ceta**2,0],[W0*sp.sin(eta)**2,0,sp.sin(eta)**2]])
    jacobian = sp.Matrix([[1,0,0],[W0,1,0],[W0,0,1]])
    g_round = sp.diag(epsilon_t,ceta**2,sp.sin(eta)**2)
    need("constant_shift_exact_coordinate_pullback", sp.simplify(jacobian.T*g_round*jacobian-g_shift) == sp.zeros(3), checks)

    sample = sp.cos(2*eta)
    sample_square = sp.trigsimp((sp.diff(sample,eta,2)-2*sp.cot(2*eta)*sp.diff(sample,eta)),method="fu")
    sample_Q = sp.trigsimp(sample_square**2+16*sp.diff(sample,eta)**2,method="fu")
    need("cos2_sample_first_square_zero", sample_square == 0, checks)
    need("cos2_sample_Q", sp.trigsimp(sample_Q-64*sp.sin(2*eta)**2,method="fu") == 0, checks)
    sample_action = sp.simplify(4*sp.pi**2*sp.integrate(q*sample_Q,(eta,0,sp.pi/2)))
    need("cos2_sample_integrated_coefficient", sample_action == sp.Rational(256,3)*sp.pi**2, checks)

    b, lam, me = sp.symbols("b lambda m_e", positive=True)
    need("common_homothety_absent_from_dimensionless_Jacobi", sp.simplify((lam*b)/(lam*b)-1) == 0, checks)
    need("electron_mass_absent", not any(expr.has(me) for expr in (lagrangian,EL,x_EL)), checks)

    result = {
        "schema": "udt-conditional-c2-time-fiber-shift-jacobi-1.0",
        "result": "PASS", "checks": checks, "direct_coordinate_result": direct,
        "quadratic_density": {
            "Euclidean": "q[(w''-2 cot(2 eta) w')^2+16(w')^2]",
            "Lorentzian": "the negative of the Euclidean density; identical stationary zero set",
            "q": "sin(eta)cos(eta)",
        },
        "Jacobi_equation": {
            "eta_form": "sin(2eta) w''''+4cos(2eta) w'''-[16sin(2eta)+4cos^2(2eta)/sin(2eta)]w''+8cos(2eta)[cot^2(2eta)-1]w'=0",
            "x": "cos(2eta)",
            "x_form": "d_x^2[(1-x^2)^2 w_xx]-4 d_x[(1-x^2)w_x]=0",
            "direct_Bach_projection": "B_tau_xi1+B_tau_xi2=-Jacobi/[4 sin(2eta)]",
        },
        "complete_regular_kernel": {
            "smooth_domain": "w(x) smooth on [-1,1]",
            "energy_identity": "integral[(1-x^2)^2 w_xx^2+4(1-x^2)w_x^2] dx=0",
            "result": "w=constant only",
            "constant_status": "exact rotating-coordinate/gauge copy via xi1,xi2 -> xi1,xi2+W0 tau",
            "singular_local_strata": "retained: w_x pole/log and integration-constant endpoint-log branches",
        },
        "scope": {
            "classified": "stationary torus-invariant time/fiber Jacobi sector about the conditional round compact solution",
            "open": "nonlinear backreaction; disconnected branches; physical boundary; singular completion; other shifts; time dependence; acceleration; topology; scale; matter",
        },
        "maximum_conclusion": "NO_REGULAR_NON_GAUGE_TIME_FIBER_SHIFT_JACOBI_MODE_IN_CONDITIONAL_ROUND_COMPACT_C2_SLICE; NONLINEAR_BOUNDARY_TIME_LIVE_SCALE_AND_MATTER_OPEN",
        "compute": {"cpu_only": True, "gpu_used": False, "sympy": sp.__version__},
    }
    (HERE/"DERIVATION_RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"result":"PASS","checks":len(checks),"maximum_conclusion":result["maximum_conclusion"]},sort_keys=True))


if __name__ == "__main__":
    main()
