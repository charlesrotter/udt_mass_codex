"""Blind-verifier CAS: Q1 (first integral), Q2 (regular center), Q3 (H at special points),
Q4 (vacuum classification). Round Branch-P system, W=1:
   phi'' = 4 e^{-2phi} rho'^2/(Z rho^2) - 2 phi' rho'/rho
   rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2
"""
import sympy as sp

r, Z = sp.symbols('r Z', positive=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho')(r)
phip, rhop = phi.diff(r), rho.diff(r)

PHIPP = 4*sp.exp(-2*phi)*rhop**2/(Z*rho**2) - 2*phip*rhop/rho
RHOPP = 2*phip*rhop - (Z/4)*rho*sp.exp(2*phi)*phip**2

def onshell(expr):
    """Substitute second derivatives using the EOMs (repeatedly for higher orders)."""
    e = expr
    for _ in range(4):
        e = e.subs({phi.diff(r, 2): PHIPP, rho.diff(r, 2): RHOPP})
    return sp.simplify(e)

print("="*70)
print("Q1: first integral")
# Candidate reduced Lagrangian from native action S = int c sqrt(h)[(Z/2)phi'^2 + R2 + K]
# round: sqrt(h)/(4pi-normalized) = rho^2 ; R2 = 2/rho^2 ; Kcal = -2 e^{-2phi} rho'^2/rho^2
L = (Z/2)*rho**2*phip**2 - 2*sp.exp(-2*phi)*rhop**2 + 2

# check EL equations reproduce the EOMs
EL_phi = sp.diff(sp.diff(L, phip), r) - sp.diff(L, phi)
EL_rho = sp.diff(sp.diff(L, rhop), r) - sp.diff(L, rho)
res_phi = onshell(EL_phi)
res_rho = onshell(EL_rho)
print("EL_phi residual on-shell (0 => L reproduces phi-EOM):", res_phi)
print("EL_rho residual on-shell (0 => L reproduces rho-EOM):", res_rho)

# Legendre transform
H = phip*sp.diff(L, phip) + rhop*sp.diff(L, rhop) - L
H = sp.expand(H)
print("H (Legendre) =", H)
E = (Z/2)*rho**2*phip**2 - 2*sp.exp(-2*phi)*rhop**2
print("H - (E - 2) =", sp.simplify(H - (E - 2)))
dE = onshell(E.diff(r))
print("dE/dr on-shell =", dE)

print("="*70)
print("Q1b: homothety (second) integral and monotone flux")
W = -4*sp.exp(-2*phi)*rho*rhop
print("d/dr[-4 e^{-2phi} rho rho'] - 2E on-shell =", onshell(W.diff(r) - 2*E))
Phi = Z*rho**2*phip
print("d/dr[Z rho^2 phi'] - 4 e^{-2phi} rho'^2 on-shell =",
      onshell(Phi.diff(r) - 4*sp.exp(-2*phi)*rhop**2))

print("="*70)
print("Q2: regular-center series expansion")
# regular center at r=0: rho ~ rho1*r + ..., phi smooth: phi0 + b1 r + b2 r^2 + ...
# (regularity from metric g_rr=e^{2phi}: no conical defect <=> rho'(0)=e^{phi0};
#  keep rho1 GENERAL to show the obstruction is independent of it)
phi0, b1, b2, b3, rho1, rho2, rho3 = sp.symbols('phi0 b1 b2 b3 rho1 rho2 rho3')
rr = sp.symbols('rr', positive=True)
phis = phi0 + b1*rr + b2*rr**2 + b3*rr**3
rhos = rho1*rr + rho2*rr**2 + rho3*rr**3
phips, rhops = phis.diff(rr), rhos.diff(rr)
resid = phis.diff(rr, 2) - (4*sp.exp(-2*phis)*rhops**2/(Z*rhos**2) - 2*phips*rhops/rhos)
ser = sp.series(sp.expand(resid), rr, 0, 1).removeO()
ser = sp.expand(ser)
c_m2 = sp.simplify(ser.coeff(rr, -2))
c_m1 = sp.simplify(ser.coeff(rr, -1))
print("phi-EOM residual, coeff of r^-2 (the obstruction):", c_m2)
print("phi-EOM residual, coeff of r^-1:", c_m1)
print("  -> r^-2 coeff independent of rho1,b1,b2,... ?",
      not any(s in c_m2.free_symbols for s in (rho1, rho2, rho3, b1, b2, b3)))
print("  -> with regularity rho1=e^{phi0}: obstruction = -4 e^{-2phi0}/Z * r^-2 =",
      sp.simplify(c_m2))
print("  -> expressed in rho (rho ~ rho1 r): 4 e^{-2phi} rho'^2/(Z rho^2) -> 4/(Z rho^2)"
      " when rho' = e^{phi}; Z=8 gives 1/(2 rho^2)")

# also check: can b1 (a conical phi-kink) cancel? c_m1 shows where b1 enters
print("="*70)
print("Q3: E at special points")
# center: rho->0, e^{-phi}rho' -> 1, rho*phi' -> 0
Q, P = sp.symbols('Q P')  # Q = e^{-phi} rho', P = rho phi'
E_general = (Z/2)*P**2 - 2*Q**2
print("E in scale-invariant vars =", E_general)
print("E(center: P=0, Q=1) =", E_general.subs({P: 0, Q: 1}))
print("E(seal: P=0, Q=0)   =", E_general.subs({P: 0, Q: 0}))
print("H convention (incl. R2 const): center =", E_general.subs({P: 0, Q: 1}) - 2,
      ", seal =", -2)

print("="*70)
print("Q4: classification checks")
# constant solution
print("EOM rhs at phi'=rho'=0: phi''=", PHIPP.subs({phip: 0, rhop: 0}),
      " rho''=", RHOPP.subs({phip: 0, rhop: 0}))
# null (E=0) class: d/dr[ln rho -+ (sqrt(Z)/2) e^{phi}] = 0 propagates
null_p = sp.log(rho) - (sp.sqrt(Z)/2)*sp.exp(phi)
dnull = sp.simplify(null_p.diff(r))
# on the null branch rho'/rho = +(sqrt(Z)/2) e^{phi} phi': check it is preserved by flow
# i.e. d/dr[rho'/rho - (sqrt(Z)/2) e^{phi} phi'] = 0 on-shell AND on the branch
g = rhop/rho - (sp.sqrt(Z)/2)*sp.exp(phi)*phip
dg = onshell(g.diff(r))
# substitute the branch condition rhop = (sqrt(Z)/2) e^{phi} phip rho
dg_on = sp.simplify(dg.subs(rhop, (sp.sqrt(Z)/2)*sp.exp(phi)*phip*rho))
print("null-branch invariance: d/dr[g] on branch =", dg_on)
# E<0 forbids rho'=0: E = (Z/2)rho^2 phi'^2 - 2 e^{-2phi} rho'^2 ; at rho'=0, E>=0. trivially true.
print("At any point with rho'=0:  E = (Z/2) rho^2 phi'^2 >= 0  (so E<0 orbits never have rho'=0)")
