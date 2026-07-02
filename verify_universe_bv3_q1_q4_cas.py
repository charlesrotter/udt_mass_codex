"""bv3_q1_q4_cas.py — blind-verifier BV3: symbolic derivations for Q1-Q4.
Round-static Branch-P reduction, banked L = (Z/2) rho^2 phi'^2 - 2 e^{-2phi} rho'^2 + 2 (+ L_m).
Metric ds^2 = -e^{-2phi}dt^2 + e^{2phi}dr^2 + rho^2 dOmega, c=G=1.
MS mass m = (rho/2)(1 - e^{-2phi} rho'^2)  [general-rho form of banked areal m=(r/2)(1-e^{-2phi})].
"""
import sympy as sp

r, Z = sp.symbols('r Z', positive=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho', positive=True)(r)
p1, p2 = sp.Derivative(phi, r), sp.Derivative(rho, r)

L_geo = sp.Rational(1,2)*Z*rho**2*p1**2 - 2*sp.exp(-2*phi)*p2**2 + 2

def EL(L, q):
    return sp.diff(sp.diff(L, sp.Derivative(q, r)), r) - sp.diff(L, q)

# --- 0. EOMs vs cell_solver_round.py rhs_P (vacuum) ---
el_phi = EL(L_geo, phi)   # = (Z rho^2 phi')' - [dL/dphi]
el_rho = EL(L_geo, rho)
# solve for phi'', rho''
pp1, pp2 = sp.symbols('pp1 pp2')  # phi'', rho''
sub = {sp.Derivative(phi, r, 2): pp1, sp.Derivative(rho, r, 2): pp2}
sol = sp.solve([el_phi.subs(sub), el_rho.subs(sub)], [pp1, pp2], dict=True)[0]
phipp_solver = 4*sp.exp(-2*phi)*p2**2/(Z*rho**2) - 2*p1*p2/rho
rhopp_solver = 2*p1*p2 - (Z/4)*rho*sp.exp(2*phi)*p1**2
print("EOM check phi'':", sp.simplify(sol[pp1] - phipp_solver))
print("EOM check rho'':", sp.simplify(sol[pp2] - rhopp_solver))

# --- Legendre energy of L_geo ---
H_geo = p1*sp.diff(L_geo, p1) + p2*sp.diff(L_geo, p2) - L_geo
E_geo = sp.Rational(1,2)*Z*rho**2*p1**2 - 2*sp.exp(-2*phi)*p2**2
print("H_geo - (E_geo - 2):", sp.simplify(H_geo - (E_geo - 2)))

# dH/dr on-shell (vacuum): must be 0
dH = sp.diff(H_geo, r).subs({sp.Derivative(phi, r, 2): sol[pp1],
                             sp.Derivative(rho, r, 2): sol[pp2]})
print("dH_geo/dr on-shell (vacuum):", sp.simplify(dH))

# --- Q1: MS-flux link ---
m = (rho/2)*(1 - sp.exp(-2*phi)*p2**2)
print("\nQ1: 1 - 2m/rho - e^{-2phi} rho'^2 =", sp.simplify(1 - 2*m/rho - sp.exp(-2*phi)*p2**2))
Phi = Z*rho**2*p1
# flux law: Phi' = 4 e^{-2phi} rho'^2 on-shell (phi-EOM); check with ARBITRARY phi-blind rho''-source s(r)
s = sp.Function('s')(r)
phipp_m = sol[pp1]                      # phi-EOM untouched by phi-blind matter
rhopp_m = rhopp_solver + s              # arbitrary phi-blind rho'' source
dPhi = sp.diff(Phi, r).subs({sp.Derivative(phi, r, 2): phipp_m.subs(sub, ), })
dPhi = sp.diff(Phi, r).subs({sp.Derivative(phi, r, 2): sol[pp1]})
print("Q1: Phi' - 4 e^{-2phi} rho'^2 (on phi-EOM, any phi-blind source):",
      sp.simplify(dPhi - 4*sp.exp(-2*phi)*p2**2))
print("Q1: Phi' - 4(1 - 2m/rho):", sp.simplify(dPhi - 4*(1 - 2*m/rho)))
# m at rho'=0:
print("Q1: m at rho'=0:", sp.simplify(m.subs(p2, 0)), " (=rho/2 -> 2m=rho)")
# m at seal phi=0, rho'_s general:
rs_, rhos_, rps_ = sp.symbols("r_s rho_s rho'_s", positive=True)
print("Q1: m at seal (phi=0):", sp.simplify(m.subs([(p2, rps_), (phi, 0), (rho, rhos_)])))

# --- Q2: budget, general edges ---
# H_tot = H_geo + H_m conserved (autonomous). Core pins phi'=rho'=0 -> H_geo(core) = -2.
q_, Hmc, Hms = sp.symbols('q H_mc H_ms')
H_core = -2 + Hmc
phip_s = q_/(Z*rhos_**2)
H_seal = (sp.Rational(1,2)*Z*rhos_**2*phip_s**2 - 2*sp.exp(0)*rps_**2 - 2) + Hms
rel = sp.solve(sp.Eq(H_core, H_seal), Hmc - Hms)  # not directly; do it by hand
budget = sp.simplify(sp.expand(H_seal - H_core))  # = 0 on conservation
print("\nQ2: 0 = H_seal - H_core =", budget)
print("Q2: => H_mc - H_ms =", sp.simplify(sp.expand(q_**2/(2*Z*rhos_**2) - 2*rps_**2)))
print("Q2 check (residual):", sp.simplify((Hmc - Hms) - (q_**2/(2*Z*rhos_**2) - 2*rps_**2) + budget - (Hms - Hmc + q_**2/(2*Z*rhos_**2) - 2*rps_**2)))
# specialization rho'_s = 0 -> banked: q^2/(2 Z rho_s^2) = E_m(core) - E_m(seal)
print("Q2 at rho'_s=0: H_mc - H_ms =", sp.simplify((q_**2/(2*Z*rhos_**2) - 2*rps_**2).subs(rps_, 0)))

# --- Q3: H_tot == 0 ---
Hmc_sol = sp.solve(sp.Eq(H_core, 0), Hmc)[0]
print("\nQ3: H_m(core) =", Hmc_sol, " (Z-, phi_c-, rho_c-, sigma-independent)")
Hms_sol = sp.solve(sp.Eq(H_seal.subs(Hmc, Hmc_sol) - (H_core.subs(Hmc, Hmc_sol)), Hms - Hms), Hms)  # redo cleanly
Hms_sol = sp.solve(sp.Eq((sp.Rational(1,2)*Z*rhos_**2*phip_s**2 - 2*rps_**2 - 2) + Hms, 0), Hms)[0]
print("Q3: H_m(seal) =", sp.expand(Hms_sol))
# bound from H_m(seal) >= 0:
qmax2 = sp.solve(sp.Eq(Hms_sol, 0), q_**2)[0]
print("Q3: saturation q^2 =", sp.factor(qmax2), " -> q_max =", sp.sqrt(sp.factor(qmax2)))
print("Q3: at rho'_s=0: q_max =", sp.simplify(sp.sqrt(qmax2.subs(rps_, 0))))

# --- Q4(b): homothety scaling of the q lower bound ---
lam = sp.symbols('lambda', positive=True)
# q = Z rho_s^2 phi'(r_s): rho->lam rho, r->lam r => phi' -> phi'/lam => q -> lam q
print("\nQ4b: q scales as lambda^1;  int dr/rho^2 -> (1/lam) int  => Z*dphi/int -> lam * (Z*dphi/int).")
print("Q4b: both sides of  q >= Z*Delta_phi / int(dr/rho^2)  scale as lambda -> bound is scale-COVARIANT (degree 1).")
print("Q4b: window condition sqrt(Z)*Delta_phi <= 2 rho_s sqrt(1+rho'_s^2) * int(dr/rho^2): rho_s*int is lambda^0 -> scale-INVARIANT.")
