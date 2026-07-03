"""sf_cas2_endpoint.py -- CAS part 2: second variation endpoint terms at both moving folds.

Method (mechanical, independent of the hand algebra): background = Taylor polynomial around the
fold with coefficients EOM-substituted; perturbation z1, z2 = free Taylor polynomials; endpoint
shift beta = eps*b1 + eps^2*b2 (outer), alpha = eps*a1 + eps^2*a2 (inner). U is represented by a
generic Taylor polynomial U(x) = U0 + U1(x-R) + U2(x-R)^2/2 + U3(x-R)^3/6 (exact to this order).
Collect the eps^1 and eps^2 endpoint contributions of S exactly.

Outer fold r_s (odd): pins phi_s=0, rho'_s=0; essential constraint phi_tot(r_s+beta)=0 solved
order-by-order; transversality H(r_s)=0 (U0 = 2 - (Z/2)R^2 Pp^2).
 C8  eps^1 == 0 (recovers transversality).
 C9  eps^2 independent of b2, b1^2, z2, z1phi'(r_s), 3rd-order background coeffs (all cancel).
 C10 eps^2 == L_rho(r_s)*b1*z1rho(r_s),  L_rho(r_s) = Z*R*Pp^2 - U1  (= -4 rho''_s).
Inner fold r_c=0 (even): pins phi'(0)=rho'(0)=0; no essential constraint; H(0)=0 <=> V0=2.
 C11 eps^1 == 0.
 C12 eps^2 == -L_rho(0)*a1*z1rho(0) = +U'(rho_c)*a1*z1rho(0); independent of a2, a1^2, z2,
     z1phi(0), z1phi'(0), z1rho'(0), 3rd-order background coeffs.
"""
import sympy as sp

eps, Z, d = sp.symbols('epsilon Z delta')

def L_of(pv, pp, rv, rp, Upoly, x):
    return sp.Rational(1,2)*Z*rv**2*pp**2 - 2*sp.exp(-2*pv)*rp**2 + 2 - Upoly.subs(x, rv)

def run_fold(name, inner):
    x = sp.symbols('x')
    if not inner:
        Pp, R = sp.symbols('Pp R')
        U0, U1, U2, U3 = sp.symbols('U0 U1 U2 U3')
        Upoly = U0 + U1*(x-R) + U2*(x-R)**2/2 + U3*(x-R)**3/6
        Pv, Rv = sp.Integer(0), R              # phi(r_s)=0, rho(r_s)=R
        Pp_v, Rp_v = Pp, sp.Integer(0)         # phi'(r_s)=Pp, rho'(r_s)=0
        # EOM 2nd derivatives at the fold (CAS1-verified EOMs):
        Ppp = 4*sp.exp(-2*Pv)*Rp_v**2/(Z*Rv**2) - 2*Pp_v*Rp_v/Rv          # -> 0
        Rpp = 2*Pp_v*Rp_v - sp.Rational(1,4)*Z*Rv*sp.exp(2*Pv)*Pp_v**2 + sp.exp(2*Pv)/4*U1
        Hval = sp.Rational(1,2)*Z*Rv**2*Pp_v**2 - 2*sp.exp(-2*Pv)*Rp_v**2 - 2 + U0
        Hsub = sp.solve(Hval, U0)[0]           # U0 = 2 - (Z/2)R^2Pp^2
        p_phi = Z*Rv**2*Pp_v; p_rho = -4*sp.exp(-2*Pv)*Rp_v
        L_rho_fold = Z*Rv*Pp_v**2 - U1
    else:
        Pc, Rc = sp.symbols('Pc Rc')
        V0, V1, V2, V3 = sp.symbols('V0 V1 V2 V3')
        Upoly = V0 + V1*(x-Rc) + V2*(x-Rc)**2/2 + V3*(x-Rc)**3/6
        Pv, Rv = Pc, Rc
        Pp_v, Rp_v = sp.Integer(0), sp.Integer(0)
        Ppp = sp.Integer(0)
        Rpp = sp.exp(2*Pc)/4*V1
        Hsub = 2                                # V0 = 2 from H(0)=0 with K(0)=0
        p_phi = Z*Rv**2*Pp_v; p_rho = -4*sp.exp(-2*Pv)*Rp_v            # both 0
        L_rho_fold = Z*Rv*Pp_v**2 - V1                                  # = -V1
        U0sym = V0
    P3, R3 = sp.symbols('P3 R3')
    phibar = Pv + Pp_v*d + Ppp*d**2/2 + P3*d**3/6
    rhobar = Rv + Rp_v*d + Rpp*d**2/2 + R3*d**3/6
    z1p0, z1pp0, z1r0, z1rp0, z2p0, z2r0 = sp.symbols('z1p0 z1pp0 z1r0 z1rp0 z2p0 z2r0')
    z1phi = z1p0 + z1pp0*d; z1rho = z1r0 + z1rp0*d
    b1, b2 = sp.symbols('b1 b2')
    beta = eps*b1 + eps**2*b2
    sgn = -1 if inner else +1                    # inner: integral from alpha to 0 = -int_0^alpha

    # build the eps-expansion by hand (the only non-polynomial eps-dependence is exp(-2 eps z1phi)):
    pv = phibar + eps*z1phi; rv = rhobar + eps*z1rho
    pv_d = sp.diff(pv, d); rv_d = sp.diff(rv, d)
    exp_fac = sp.exp(-2*phibar)*(1 - 2*eps*z1phi + 2*eps**2*z1phi**2)   # exact to O(eps^2)
    integrand = (sp.Rational(1,2)*Z*rv**2*pv_d**2 - 2*exp_fac*rv_d**2 + 2 - Upoly.subs(x, rv))
    ig = sp.expand(integrand)
    ig = ig.coeff(eps, 0) + eps*ig.coeff(eps, 1) + eps**2*ig.coeff(eps, 2)
    ig_d = sum(sp.expand(sp.diff(ig, d, j)).subs(d, 0)/sp.factorial(j)*d**j for j in range(3))
    assert not ig_d.has(sp.nan)
    G = sgn*sp.integrate(sp.expand(ig_d), (d, 0, beta))
    # piece-1 boundary term at the fold: sgn * p(fold).z(fold)  (background momenta)
    T_bdry = sgn*(p_phi*(eps*z1p0 + eps**2*z2p0) + p_rho*(eps*z1r0 + eps**2*z2r0))
    T = sp.expand(T_bdry + G)
    T = T.coeff(eps, 1)*eps + T.coeff(eps, 2)*eps**2   # drop higher orders

    if not inner:
        # essential constraint phi_tot(r_s + beta) = 0, order by order
        con = sp.expand((phibar + eps*z1phi).subs(d, beta) + eps**2*z2p0)
        c1 = con.coeff(eps, 1); c2 = con.coeff(eps, 2)
        sol1 = sp.solve(c1, z1p0)[0]
        sol2 = sp.solve(c2.subs(z1p0, sol1), z2p0)[0]
        T = T.subs(z2p0, sol2).subs(z1p0, sol1)
        print(f"[outer] constraint: z1phi(r_s) = {sol1}")
    T = sp.expand(T)
    e1 = sp.simplify(T.coeff(eps, 1))
    if not inner:
        e1h = sp.simplify(e1.subs(sp.Symbol('U0'), Hsub))
        print("C8 outer eps^1 == 0 given H(r_s)=0:", e1h == 0)
        e2 = sp.expand(sp.simplify(T.coeff(eps, 2)).subs(sp.Symbol('U0'), Hsub))
        deps = {'b2': b2, 'z2r0': z2r0, "z1phi'": z1pp0, 'P3': P3, 'R3': R3,
                "z1rho'": z1rp0}
        for nm, s in deps.items():
            ok = sp.simplify(sp.diff(e2, s)) == 0
            print(f"C9 outer eps^2 independent of {nm}:", ok)
        tgt = L_rho_fold*b1*z1r0
        print("C10 outer eps^2 == L_rho(r_s)*b1*z1rho(r_s):", sp.simplify(e2 - tgt) == 0)
        print("    residual:", sp.simplify(e2 - tgt))
        print("    (== -4 rho''_s b1 z1r0):", sp.simplify(e2 - (-4*Rpp)*b1*z1r0) == 0)
    else:
        e1h = sp.simplify(e1.subs(sp.Symbol('V0'), 2))
        print("C11 inner eps^1 == 0 given U(rho_c)=2:", e1h == 0)
        e2 = sp.expand(sp.simplify(T.coeff(eps, 2)).subs(sp.Symbol('V0'), 2))
        for nm, s in {'a2(=b2)': b2, 'z2r0': z2r0, 'z1phi(0)': z1p0, "z1phi'(0)": z1pp0,
                      "z1rho'(0)": z1rp0, 'z2p0': z2p0, 'P3': P3, 'R3': R3}.items():
            ok = sp.simplify(sp.diff(e2, s)) == 0
            print(f"C12 inner eps^2 independent of {nm}:", ok)
        V1 = sp.Symbol('V1')
        print("C12 inner eps^2 == +U'(rho_c)*a1*z1rho(0):",
              sp.simplify(e2 - V1*b1*z1r0) == 0, "| residual:", sp.simplify(e2 - V1*b1*z1r0))

run_fold('outer', inner=False)
run_fold('inner', inner=True)
