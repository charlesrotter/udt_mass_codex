"""bv2_a_reduction.py — BLIND VERIFIER: independent reduction of the native action
on the round cell h = rho(r)^2 Omega, metric ds^2 = -e^{-2phi}c^2 dt^2 + e^{2phi}dr^2 + rho^2 dOmega^2.
Checks: reduced L form; EOMs vs cell_solver_round.py rhs_P/rhs_G; H, E, Phi definitions.
"""
import sympy as sp

r = sp.symbols('r', positive=True)
Z = sp.symbols('Z', positive=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho', positive=True)(r)
th = sp.symbols('theta', positive=True)

# ---- transverse geometry for h_AB = rho^2 * Omega_AB (unit 2-sphere Omega) ----
# Omega_AB = diag(1, sin^2 th)
Om = sp.diag(1, sp.sin(th)**2)
h = rho**2 * Om
hinv = h.inv()
# K_AB = (1/2) e^{-phi} d_r h_AB
K = sp.Rational(1,2)*sp.exp(-phi)*sp.diff(h, r)
Kmix = sp.simplify(hinv*K)                       # K^A_B
trK = sp.simplify(Kmix.trace())
KK = sp.simplify((Kmix*Kmix).trace())            # K_AB K^AB
calK = sp.simplify(KK - trK**2)
print("K^A_B =", Kmix)
print("K =", sp.simplify(trK), "   K_ABK^AB =", KK)
print("calK =", calK, "  expect -2 e^{-2phi} rho'^2/rho^2:",
      sp.simplify(calK + 2*sp.exp(-2*phi)*sp.diff(rho,r)**2/rho**2) == 0)

R2 = 2/rho**2                                    # intrinsic curvature of sphere radius rho
sqh = rho**2*sp.sin(th)                          # sqrt(det h)

# ---- reduced Lagrangian per 4pi (integrate sin th over sphere /4pi -> factor 1) ----
phip = sp.diff(phi, r); rhop = sp.diff(rho, r)
for name, W in [('P', sp.Integer(1)), ('G', sp.exp(2*phi))]:
    Ldens = sqh*(sp.Rational(1,2)*Z*phip**2 + R2 + W*calK)
    Lred = sp.simplify(sp.integrate(Ldens, (th, 0, sp.pi))/(4*sp.pi)*2)  # int sin = 2; /4pi*2pi(psi)=...
    # careful: full angular integral = int_0^pi dth int_0^{2pi} dpsi -> 2pi * int sin th dth = 4pi
    Lred = sp.simplify(Ldens/sp.sin(th))         # per-(4pi/(4pi)) = density with sin stripped
    print(f"\nBranch {name}: L_red =", sp.expand(Lred))

# Branch P explicitly:
L_P = sp.Rational(1,2)*Z*rho**2*phip**2 - 2*sp.exp(-2*phi)*rhop**2 + 2
Ldens_P = sqh*(sp.Rational(1,2)*Z*phip**2 + R2 + calK)
print("\nCLAIM L_P = (Z/2)rho^2 phi'^2 - 2 e^{-2phi} rho'^2 + 2 :",
      sp.simplify(Ldens_P/sp.sin(th) - L_P) == 0)

# ---- EOMs from L_P vs solver ----
def EL(L, q):
    return sp.diff(sp.diff(L, sp.diff(q, r)), r) - sp.diff(L, q)

el_phi = sp.expand(EL(L_P, phi))
el_rho = sp.expand(EL(L_P, rho))
phipp = sp.diff(phi, r, 2); rhopp = sp.diff(rho, r, 2)
sol = sp.solve([el_phi, el_rho], [phipp, rhopp], dict=True)[0]
phipp_P = sp.simplify(sol[phipp]); rhopp_P = sp.simplify(sol[rhopp])
print("\nP phi'' =", phipp_P)
print("P rho'' =", rhopp_P)
solver_phipp = 4*sp.exp(-2*phi)*rhop**2/(Z*rho**2) - 2*phip*rhop/rho
solver_rhopp = 2*phip*rhop - Z/4*rho*sp.exp(2*phi)*phip**2
print("matches solver rhs_P:",
      sp.simplify(phipp_P - solver_phipp) == 0, sp.simplify(rhopp_P - solver_rhopp) == 0)

L_G = sp.Rational(1,2)*Z*rho**2*phip**2 - 2*rhop**2 + 2
sol = sp.solve([sp.expand(EL(L_G, phi)), sp.expand(EL(L_G, rho))], [phipp, rhopp], dict=True)[0]
print("G phi'' =", sp.simplify(sol[phipp]), "  G rho'' =", sp.simplify(sol[rhopp]))
print("matches solver rhs_G:",
      sp.simplify(sol[phipp] - (-2*phip*rhop/rho)) == 0,
      sp.simplify(sol[rhopp] - (-Z/4*rho*phip**2)) == 0)

# ---- momenta / H / E / Phi ----
pi_phi = sp.diff(L_P, phip); pi_rho = sp.diff(L_P, rhop)
H = sp.simplify(phip*pi_phi + rhop*pi_rho - L_P)
E = sp.Rational(1,2)*Z*rho**2*phip**2 - 2*sp.exp(-2*phi)*rhop**2
print("\npi_phi =", pi_phi, "  pi_rho =", pi_rho)
print("H = E - 2 :", sp.simplify(H - (E - 2)) == 0)

# dH/dr on-shell (vacuum P) == 0
dH = sp.diff(H, r).subs({phipp: phipp_P, rhopp: rhopp_P})
print("dH/dr on-shell (vacuum P) == 0 :", sp.simplify(dH) == 0)

# dPhi/dr on-shell:
Phi = Z*rho**2*phip
dPhi = sp.simplify(sp.diff(Phi, r).subs({phipp: phipp_P}))
print("dPhi/dr on-shell =", dPhi, " (expect 4 e^{-2phi} rho'^2; Phi NOT conserved in P)")
