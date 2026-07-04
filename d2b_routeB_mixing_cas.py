#!/usr/bin/env python3
"""D2b check 4 — the Route-B mixing-term escape in Branch G.

Standing OWED tension: live solvers carry Z=8 (Route-B value) without Route B's forced
mixing term 2√h e^{phi} K phi' [universe_cell_vacuum_impossibility_results.md L2, :127-132;
universe_cell_fold_jc_sigma_results.md Route-B carry]. Question here: does that term, if it
belongs in the action, BREAK the G phi-deadness theorem? (It is shift-invariant, hence
R1-LEGAL in G — it cannot be excluded by the depth-gauge argument.)
"""
import sympy as sp

ok = []
def check(name, cond):
    ok.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name)

r = sp.Symbol('r', positive=True)
Z, lam, c0 = sp.symbols('Z lambda c_0', real=True, nonzero=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho', positive=True)(r)

# mixing term, reduced on h = rho^2 Omega, per 4pi:  2 √h e^{phi} K phi'
#   K = 2 e^{-phi} rho'/rho  [two-player doc:95],  √h per-4pi -> rho^2
Mix = 2*rho**2*sp.exp(phi)*(2*sp.exp(-phi)*rho.diff(r)/rho)*phi.diff(r)
check("reduced mixing term = 4 rho rho' phi'  (phi-free coefficient: e^{phi}K is shift-invariant)",
      sp.simplify(Mix - 4*rho*rho.diff(r)*phi.diff(r)) == 0)
check("mixing term is EXACTLY shift-invariant (R1-legal in G: the depth gauge does NOT exclude it)",
      sp.simplify(Mix.subs(phi, phi + lam).doit() - Mix) == 0)

# G + mixing: L = (Z/2)rho^2 phi'^2 + 4 rho rho' phi' - 2 rho'^2 + 2
L = Z/2*rho**2*phi.diff(r)**2 + 4*rho*rho.diff(r)*phi.diff(r) - 2*rho.diff(r)**2 + 2
EL_phi = sp.simplify(sp.diff(sp.diff(L, phi.diff(r)), r) - sp.diff(L, phi))
FluxB = Z*rho**2*phi.diff(r) + 4*rho*rho.diff(r)
check("phi-EL = d/dr[ Z rho^2 phi' + 4 rho rho' ]: modified flux Phi~ = Z rho^2 phi' + 2(rho^2)'"
      " EXACTLY conserved (matches the banked Route-B P-flux form Phi~ = Z rho^2 phi' + 4 rho rho')",
      sp.simplify(EL_phi - sp.diff(FluxB, r)) == 0)

# closed cell, canon folds: every end pins rho'=0, and even/center/odd-untwisted also force the
# constant to vanish exactly as before (at ends FluxB = Z rho^2 phi' since rho'=0 there):
# even fold: phi'=rho'=0 -> Phi~=0; odd fold: rho'=0, phi' free -> Phi~(end)=Z rho^2 phi'(end).
# So Phi~ == 0 for any closed cell with an even fold or center; then:
slaved = sp.solve(sp.Eq(FluxB, 0), phi.diff(r))[0]
check("Phi~ = 0 slaves phi to the geometry: phi' = -4 rho'/(Z rho)  =>  phi = -(4/Z) ln rho + c",
      sp.simplify(slaved + 4*rho.diff(r)/(Z*rho)) == 0
      and sp.simplify(sp.diff(-sp.Rational(4,1)/Z*sp.log(rho) + c0, r) - (-4*rho.diff(r)/(Z*rho))) == 0)
# => phi is NONCONSTANT wherever rho varies: the "phi == const" wording of the deadness theorem
#    FAILS under Route B. What SURVIVES: (a) zero seal charge (Phi~ == 0); (b) phi carries no
#    independent DOF (slaved 1:1 to rho); (c) the phi-equation stays SOURCE-FREE (no analog of the
#    P-source 4e^{-2phi}rho'^2, hence no flux ladder / no quantization-closure structure).
Dphi = -sp.Rational(4,1)/Z*sp.log(sp.Symbol('rho_s')/sp.Symbol('rho_c'))
print("   Route-B G-cell: Delta phi = -(4/Z) ln(rho_s/rho_c) — an OUTPUT of the rho-profile, not an")
print("   independent anchor; still q=0 and still no phi-angular source. Deadness WORDING conditional on Route A.")

# corollary: CANON (untwisted) odd+odd folds under Route B — rho'=0 pinned at both ends but phi'
# free there, so Phi~ = q is NOT forced to zero; integrating phi' = (q - 4 rho rho')/(Z rho^2)
# with phi(r1)=phi(r2)=0 gives q = 4 ln(rho_2/rho_1)/I — nonzero whenever the fold radii differ:
q, I1 = sp.symbols('q I', positive=True)
rho1, rho2 = sp.symbols('rho_1 rho_2', positive=True)
phi_int = (q/Z)*I1 - sp.Rational(4,1)/Z*sp.log(rho2/rho1)   # Delta phi = (q/Z)I - (4/Z)ln(rho2/rho1)
# check the integrand identity: (q - 4 rho rho')/(Z rho^2) = q/(Z rho^2) - (4/Z)(ln rho)'
check("phi' = (q - 4 rho rho')/(Z rho^2) = q/(Z rho^2) - (4/Z) d(ln rho)/dr (exact split)",
      sp.simplify((q - 4*rho*rho.diff(r))/(Z*rho**2) - (q/(Z*rho**2) - sp.Rational(4,1)/Z*sp.diff(sp.log(rho), r))) == 0)
qsol = sp.solve(sp.Eq(phi_int, 0), q)
check("canon odd+odd under Route B: q = 4 ln(rho_2/rho_1)/I — nonzero flux WITHOUT twist if rho_1 != rho_2",
      len(qsol) == 1 and sp.simplify(qsol[0] - 4*sp.log(rho2/rho1)/I1) == 0)

print()
print("ALL PASS" if all(c for _, c in ok) else "SOME FAILED")
