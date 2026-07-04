#!/usr/bin/env python3
"""D2b check 3 — ADVERSARIAL: hunt escapes. Result: the strong reading of the theorem is
REFUTED by an exact counterexample within the banked admissible matter class.

Sources: D3 sigma-admissibility — "potential-only L_m = -U(rho) realizes essentially ANY
smooth sigma" = banked ADMISSIBLE phi-blind matter class, and "a universe cell closed by
choosing sigma carries ZERO evidential weight" [universe_cell_fold_jc_sigma_results.md:81-84].
Banked carrier: L_m = -(xi/2)(rho^2 I_r + I_th + N^2 I_s) - (kappa N^2/2)(I_4r + I_4th/rho^2),
pins f(r,0)=0, f(r,pi)=pi [round_matter_reduction_results.md:13-16].
"""
import sympy as sp

ok = []
def check(name, cond):
    ok.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name)

r = sp.Symbol('r', positive=True)
Z, k, b, rho0, phi0 = sp.symbols('Z k b rho_0 phi_0', positive=True)

# =========== E1: EXACT two-mirror matter-closed G-cell (potential-only admissible matter) ===========
# candidate: phi == phi0 (const), rho(r) = rho0 + b sin^2(kr) on [0, pi/(2k)];
#            L_m = -U(rho), U(rho) = 2 + 8k^2 (rho - rho0)(rho0 + b - rho).
rho = rho0 + b*sp.sin(k*r)**2
rhosym = sp.Symbol('rho', positive=True)
U = 2 + 8*k**2*(rhosym - rho0)*(rho0 + b - rhosym)
L_G_tot = sp.Rational(1,2)*Z*rho**2*0 - 2*sp.diff(rho, r)**2 + 2 - U.subs(rhosym, rho)  # phi'=0

# (i) both field equations hold EXACTLY:
#   phi-EL: (Z rho^2 phi')' = 0 with phi' == 0: trivially exact.
#   rho-EL: -4 rho'' - Z rho phi'^2 - dLm/drho = 0  ->  4 rho'' = -U'(rho) ... sign:
#   dLm/drho = -U'(rho); so rho-EL: -4 rho'' + U'(rho) = 0.
res_rho = sp.simplify(-4*sp.diff(rho, r, 2) + sp.diff(U, rhosym).subs(rhosym, rho))
check("rho-EL holds EXACTLY: -4 rho'' + U'(rho(r)) == 0 identically in r", sp.simplify(sp.expand_trig(res_rho)) == 0)

# (ii) both ends are derived EVEN-FOLD pins: phi'(0)=phi'(L)=0 (phi const) and rho'(0)=rho'(L)=0:
L_end = sp.pi/(2*k)
check("rho'(0) = 0 and rho'(pi/2k) = 0 (both even-fold pins satisfied; phi' == 0 everywhere)",
      sp.simplify(sp.diff(rho, r).subs(r, 0)) == 0 and sp.simplify(sp.diff(rho, r).subs(r, L_end)) == 0)

# (iii) the free-endpoint CRITICAL CLOSURE H = 0 holds IDENTICALLY (not just at the ends):
H = -2*sp.diff(rho, r)**2 - 2 + U.subs(rhosym, rho)     # H = -2rho'^2 - 2 + E_m, E_m = U
check("H == 0 identically (free-endpoint transversality closure satisfied EXACTLY)",
      sp.simplify(sp.expand_trig(H)) == 0)

# (iv) F5-type criticality at both folds: E_m(fold) = U = 2 exactly:
check("E_m = 2 EXACTLY at both folds (the F5-critical value, same as P's E_m(core)=2)",
      sp.simplify(U.subs(rhosym, rho).subs(r, 0)) == 2 and sp.simplify(sp.expand_trig(U.subs(rhosym, rho).subs(r, L_end))) == 2)

# (v) the SAME configuration FAILS in Branch P (consistency with T1 rigidity):
#   P phi-EL: Z(rho^2 phi')' - 4 e^{-2phi} rho'^2 = 0; with phi==phi0: residual = -4 e^{-2phi0} rho'^2 != 0.
resP = sp.simplify(0 - 4*sp.exp(-2*phi0)*sp.diff(rho, r)**2)
check("in Branch P the same phi-flat profile VIOLATES the phi-EL (residual -4e^{-2phi0}rho'^2 != 0):"
      " the escape object is G-EXCLUSIVE", sp.simplify(resP) != 0)

print("   => E1: a finite two-even-fold Branch-G cell, closed (H=0, E_m(folds)=2), nonconstant geometry,")
print("      exists EXACTLY for admissible phi-blind matter. It is phi-FLAT: zero anchor, zero seal flux.")

# =========== E1 fate for the DERIVED carrier: center obstruction + fold-radius pinning ===========
th = sp.Symbol('theta', positive=True)
f = sp.Function('f')(th)
# winding lower bound: with pins f(0)=0, f(pi)=pi:  Int_0^pi sin(f) f_th dth = cos f(0) - cos f(pi) = 2:
Iexact = sp.integrate(sp.sin(f)*sp.diff(f, th), (th, 0, sp.pi))
check("Int_0^pi sin(f) f' dth = cos f(0) - cos f(pi) = 2 under the pins (exact, any profile)",
      sp.simplify(Iexact - (sp.cos(f.subs(th,0)) - sp.cos(f.subs(th,sp.pi)))) == 0)
# Cauchy-Schwarz: 2^2 = [Int sinf f']^2 <= [Int sin th][Int sin^2 f f'^2 / sin th] = 2 * (2 I_4th)
check("Int_0^pi sin(th) dth = 2  (the C-S companion factor)", sp.integrate(sp.sin(th), (th, 0, sp.pi)) == 2)
#   => I_4th = (1/2) Int sin^2 f f'^2/sin th >= 1, equality at f = theta. Verify the equality case:
I4th_rigid = sp.Rational(1,2)*sp.integrate(sp.sin(th)**2*1/sp.sin(th), (th, 0, sp.pi))
check("rigid hedgehog f=theta: I_4th = 1 exactly (saturates the bound; banked value)", I4th_rigid == 1)
# numeric spot-checks of I_4th >= 1 for pin-respecting non-rigid profiles:
import math
def I4th_num(ff, dff, n=4000):
    s = 0.0
    for i in range(1, n):
        x = math.pi*i/n
        s += math.sin(ff(x))**2*dff(x)**2/math.sin(x)
    return 0.5*s*math.pi/n
profs = [(lambda x: x + 0.3*math.sin(2*x), lambda x: 1 + 0.6*math.cos(2*x)),
         (lambda x: math.pi*(x/math.pi)**2, lambda x: 2*x/math.pi),
         (lambda x: x - 0.45*math.sin(2*x), lambda x: 1 - 0.9*math.cos(2*x))]
vals = [I4th_num(ff, dff) for ff, dff in profs]
check("numeric spot-checks: I_4th >= 1 for pin-respecting non-rigid profiles %s" % [round(v,4) for v in vals],
      all(v >= 1.0 - 1e-6 for v in vals))
# => near a center rho -> 0 the G rho-source term -(kappa N^2/4) I_4th/rho^3 <= -(kappa N^2/4)/rho^3 -> -oo:
#    rho'' diverges, incompatible with a regular center (rho ~ rho'(0) r needs rho'' -> 0).
#    So: the DERIVED carrier (threading all shells, N>=1, kappa>0) OBSTRUCTS regular centers in G too;
#    the two-mirror (center-free shell) topology is the carrier's only candidate home — same as P's R2 shape.

# fold-radius pinning by criticality with the carrier (rigid values I_th=1, I_s=1, I_4th=1, I_r=I_4r=0):
xi, kap, N, rhoF = sp.symbols('xi kappa N rho_f', positive=True)
E_m_rigid = sp.Rational(1,2)*xi*(1 + N**2) + sp.Rational(1,2)*kap*N**2/rhoF**2
sol = sp.solve(sp.Eq(E_m_rigid, 2), rhoF**2)
check("criticality E_m(fold)=2 with the carrier PINS the fold radius: rho_f^2 = kappa N^2/(4 - xi(1+N^2))",
      sp.simplify(sol[0] - kap*N**2/(4 - xi*(1+N**2))) == 0)
print("   => 'scale-freedom forbids a pinned size' is FALSE with the carrier present: the L4 term breaks")
print("      the vacuum scale family and criticality pins rho_fold (existence of the full BVP solution OPEN).")

# =========== vacuum scale family (the lack that IS real, vacuum-only) ===========
s = sp.Symbol('s', positive=True)
rr = sp.Symbol('rbar', positive=True)
rhoV = sp.Function('rho', positive=True)(rr); phiV = sp.Function('phi')(rr)
L_G = Z/2*rhoV**2*phiV.diff(rr)**2 - 2*rhoV.diff(rr)**2 + 2
# under r = s*rbar, rho = s*rhobar (phi unscaled): L_G dr -> s * L_G[rhobar,phibar] drbar
rhoS = s*rhoV; # d/dr = (1/s) d/drbar
L_scaled = Z/2*rhoS**2*(phiV.diff(rr)/s)**2 - 2*(rhoS.diff(rr)/s*s/s)**2*0 - 0  # build carefully below
L_scaled = Z/2*(s*rhoV)**2*(phiV.diff(rr)/s)**2 - 2*(sp.diff(s*rhoV, rr)/s)**2 + 2
check("VACUUM L_G: under (r,rho)->(s r, s rho), L_G dr -> s * L_G drbar (exact scale covariance:"
      " every vacuum G solution comes in a scale family)",
      sp.simplify(s*L_G - s*L_scaled) == 0 and sp.simplify(L_scaled - L_G) == 0)
# and the carrier BREAKS it: the term -(kappa N^2/2) I_4th/rho^2 in L_m scales as 1/s^2, not s^0:
check("carrier L4 angular term ~ 1/rho^2 breaks scale covariance (scales s^{-2} != s^0)",
      sp.simplify((1/(s*rhoV)**2)*s**2 - 1/rhoV**2) == 0 and sp.simplify((1/(s*rhoV)**2) - 1/rhoV**2) != 0)

print()
print("ALL PASS" if all(c for _, c in ok) else "SOME FAILED")
