"""or_energy_cas.py -- D-A/D-B/D-C bookkeeping CAS (reduced radial action vs physical energy).

Metric (native constrained-two-player, round transverse h_AB = rho(r)^2 Omega_AB, c=1 canon):
    ds^2 = -e^{-2phi} dt^2 + e^{2phi} dr^2 + rho^2 dOmega^2
Native geometric action (Branch P, W_chi = 1, banked):
    S = int dt dr d2x  sqrt(h) [ (Z/2) phi'^2 + R2[h] + K_AB K^AB - K^2 + L_m ] ,  L_m = -U(rho)/rho^2*rho^2 (reduced -U)
Banked reduced radial Lagrangian (repo: universe_cell_* + cell_solver_universe_T3.py):
    L = (Z/2) rho^2 phi'^2 - 2 e^{-2phi} rho'^2 + 2 - U(rho)
Banked r-Hamiltonian:  H = (Z/2) rho^2 phi'^2 - 2 e^{-2phi} rho'^2 - 2 + U  == 0 on cells.
Banked MS:  m = (rho/2)(1 - e^{-2phi} rho'^2),  off-shell identity m' = 4 pi rho^2 rho' eps, eps = -G^t_t/8pi.
"""
import sympy as sp

r, th, ps = sp.symbols('r theta psi')
Z = sp.Symbol('Z', positive=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho', positive=True)(r)
Ufun = sp.Function('U')
U = Ufun(rho)
Up = Ufun(rho).diff(rho)            # U'(rho)
p1, p2 = phi.diff(r), phi.diff(r, 2)
q1, q2 = rho.diff(r), rho.diff(r, 2)
e2p = sp.exp(2 * phi)

OK = []
def check(name, expr):
    val = sp.simplify(expr)
    OK.append((name, val == 0 or val is sp.S.true, val))
    print(f"[{'PASS' if OK[-1][1] else 'FAIL'}] {name}" + ("" if OK[-1][1] else f"  residual={val}"))

# ---------------------------------------------------------------- geometry helpers
def christoffel(gm, xs):
    gi = gm.inv()
    n = len(xs)
    Gam = [[[sp.simplify(sum(gi[a, d] * (gm[d, b].diff(xs[c]) + gm[d, c].diff(xs[b])
             - gm[b, c].diff(xs[d])) for d in range(n)) / 2) for c in range(n)]
            for b in range(n)] for a in range(n)]
    return Gam

def ricci(gm, xs):
    n = len(xs)
    Gam = christoffel(gm, xs)
    Ric = sp.zeros(n, n)
    for b in range(n):
        for c in range(n):
            expr = 0
            for a in range(n):
                expr += Gam[a][b][c].diff(xs[a]) - Gam[a][b][a].diff(xs[c])
                for d in range(n):
                    expr += Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a]
            Ric[b, c] = sp.simplify(expr)
    return Ric

# ---------------------------------------------------------------- C1: measure / lapse bookkeeping
g4 = sp.diag(-sp.exp(-2 * phi), sp.exp(2 * phi), rho**2, rho**2 * sp.sin(th)**2)
sqrtmg = sp.sqrt(-g4.det())
sqrth = sp.sqrt((rho**2) * (rho**2 * sp.sin(th)**2))
N = sp.exp(-phi)                                     # lapse
sqrtg3 = sp.sqrt(sp.exp(2 * phi) * rho**4 * sp.sin(th)**2)  # spatial volume
SIN = {sp.sqrt(sp.sin(th)**2): sp.sin(th), sp.Abs(sp.sin(th)): sp.sin(th)}  # theta in (0,pi)
check("C1a sqrt(-g) = rho^2 sin(th) (phi-FREE)",
      sp.simplify(sp.powsimp(sqrtmg, force=True).subs(SIN) - rho**2 * sp.sin(th)))
s_, f_ = sp.symbols('s_ f_', positive=True)  # sin(theta)>0 on (0,pi); e^{phi} -> f_ > 0
check("C1b N*sqrt(g3) = sqrt(-g) (lapse e^{-phi} exactly cancels e^{+phi} radial weight)",
      sp.simplify((N * sqrtg3 - sqrtmg).subs(sp.sin(th), s_).subs(sp.exp(phi), f_)
                  .subs(sp.exp(2 * phi), f_**2).subs(sp.exp(-phi), 1 / f_)))

# ---------------------------------------------------------------- C2: R^(2) of the round 2-sphere of radius rho
RHO = sp.Symbol('RHO', positive=True)
h2 = sp.diag(RHO**2, RHO**2 * sp.sin(th)**2)
Ric2 = ricci(h2, [th, ps])
R2 = sp.simplify(sum(h2.inv()[i, i] * Ric2[i, i] for i in range(2)))
check("C2 R^(2)[rho^2 Omega] = 2/rho^2", R2 - 2 / RHO**2)

# ---------------------------------------------------------------- C3: extrinsic invariants
hAB = sp.diag(rho**2, rho**2 * sp.sin(th)**2)
KAB = sp.Rational(1, 2) * sp.exp(-phi) * hAB.diff(r)
Kmix = sp.simplify(hAB.inv() * KAB)                  # K^A_B
K = sp.trace(Kmix)
KK = sp.trace(Kmix * Kmix)                           # K_AB K^AB
scrK = sp.simplify(KK - K**2)
check("C3 scrK = -2 e^{-2phi} rho'^2 / rho^2", scrK + 2 * sp.exp(-2 * phi) * q1**2 / rho**2)

# ---------------------------------------------------------------- C4: angular reduction of the action (per-4pi)
# bracket = (Z/2) phi'^2 + R2 + 1*scrK + L_m,   L_m reduced = -U(rho)/rho^2 (so sqrt(h)*L_m -> -U per-4pi)
bracket_geo = (Z / 2) * p1**2 + 2 / rho**2 + scrK
red_geo = sp.simplify(sp.integrate(rho**2 * sp.sin(th) * bracket_geo, (th, 0, sp.pi),
                                   (ps, 0, 2 * sp.pi)) / (4 * sp.pi))
L_banked = (Z / 2) * rho**2 * p1**2 - 2 * sp.exp(-2 * phi) * q1**2 + 2 - U
check("C4 per-4pi reduced geometric integrand = banked L + U (i.e. banked L = geo - U)",
      red_geo - (L_banked + U))

# ---------------------------------------------------------------- C5/C6: EL equations = banked/solver EOMs
L = L_banked
EL_phi = sp.diff(sp.diff(L, p1), r) - sp.diff(L, phi)
EL_rho = sp.diff(sp.diff(L, q1), r) - sp.diff(L, rho)
# solver rhs (cell_solver_universe_T3.py):
phipp_solver = 4 * q1**2 / (e2p * Z * rho**2) - 2 * p1 * q1 / rho
sigma = (e2p / 4) * Up
rhopp_solver = 2 * p1 * q1 - (Z / 4) * rho * e2p * p1**2 + sigma
sol = sp.solve([EL_phi, EL_rho], [p2, q2], dict=True)[0]
check("C5 EL_phi of banked L  =>  solver phi''", sp.simplify(sol[p2] - phipp_solver))
check("C6 EL_rho of banked L  =>  solver rho'' (sigma = e^{2phi} U'/4, D3)",
      sp.simplify(sol[q2] - rhopp_solver))

# ---------------------------------------------------------------- C7/C8: r-Hamiltonian, conservation, L-H
H = sp.simplify(p1 * sp.diff(L, p1) + q1 * sp.diff(L, q1) - L)
H_banked = (Z / 2) * rho**2 * p1**2 - 2 * sp.exp(-2 * phi) * q1**2 - 2 + U
check("C7a H (r-Legendre of banked L) = banked H", H - H_banked)
dH = sp.simplify(H.diff(r).subs({q2: sol[q2], p2: sol[p2]}))
check("C7b dH/dr = 0 on the EL equations (autonomy)", dH)
check("C8 L - H = 4 - 2U  (so ON-SHELL with H==0:  L = 4 - 2U pointwise)", sp.simplify(L - H) - (4 - 2 * U))

# ---------------------------------------------------------------- C9: boundary-term identity for the on-shell L
# On shell L = sum psi' pi_psi (H=0):  L = Z rho^2 phi'^2 - 4 e^{-2phi} rho'^2  ("2T").
# Claim: 2T = d/dr[ -4 e^{-2phi} rho rho' ] + rho U'(rho)   on the EL equations.
twoT = Z * rho**2 * p1**2 - 4 * sp.exp(-2 * phi) * q1**2
bdy = -4 * sp.exp(-2 * phi) * rho * q1
resid = sp.simplify((twoT - bdy.diff(r) - rho * Up).subs({q2: sol[q2], p2: sol[p2]}))
check("C9 2T = (-4 e^{-2phi} rho rho')' + rho U'  on-shell", resid)

# ---------------------------------------------------------------- C10: OFF-SHELL Misner-Sharp identity via G^t_t
Ric4 = ricci(g4, [sp.Symbol('t'), r, th, ps])
gi4 = g4.inv()
Rs4 = sp.simplify(sum(gi4[i, i] * Ric4[i, i] for i in range(4)))
Gtt_mix = sp.simplify(gi4[0, 0] * (Ric4[0, 0] - sp.Rational(1, 2) * g4[0, 0] * Rs4))  # G^t_t
eps = -Gtt_mix / (8 * sp.pi)
m = (rho / 2) * (1 - sp.exp(-2 * phi) * q1**2)
check("C10 OFF-SHELL: m'_MS - 4 pi rho^2 rho' eps == 0 (pure metric identity, no EOM used)",
      sp.simplify(m.diff(r) - 4 * sp.pi * rho**2 * q1 * eps))

# ---------------------------------------------------------------- C11: constant-cylinder anchor for the eps sign
eps_cyl = sp.simplify(eps.subs({p2: 0, q2: 0, p1: 0, q1: 0}))
check("C11 constant cylinder: eps = 1/(8 pi rho^2) > 0 (banked D3 anchor reproduced)",
      eps_cyl - 1 / (8 * sp.pi * rho**2))

# ---------------------------------------------------------------- C12: eps on-shell in field terms (for numerics)
eps_onshell = sp.simplify(eps.subs({q2: sol[q2], p2: sol[p2]}))
print("\n eps (on the EL equations, BEFORE using H=0):")
sp.pprint(sp.simplify(8 * sp.pi * rho**2 * eps_onshell))
# with the H==0 constraint eliminate (Z/2) rho^2 phi'^2 = 2 - U + 2 e^{-2phi} rho'^2:
eps_H = sp.simplify(eps_onshell.subs(Z, (2 - U + 2 * sp.exp(-2 * phi) * q1**2) * 2 / (rho**2 * p1**2)))
target = (3 + sp.exp(-2 * phi) * q1**2 - 2 * rho * sp.exp(-2 * phi) * p1 * q1 - U - (rho / 2) * Up) / (8 * sp.pi * rho**2)
check("C12 on-shell+H=0:  8 pi rho^2 eps = 3 + e^{-2phi}rho'^2 - 2 rho e^{-2phi} phi' rho' - U - (rho/2)U'",
      sp.simplify(eps_H - target))

# ---------------------------------------------------------------- C13: odd-fold convention cross-check (repo wins)
Ltilde = L.subs(phi, -phi)   # phi -> -phi with derivatives implied
Ltilde = (Z / 2) * rho**2 * p1**2 - 2 * sp.exp(2 * phi) * q1**2 + 2 - U
check("C13 Ltilde - L = -4 sinh(2phi) rho'^2 (banked odd-fold bulk-asymmetry reproduced)",
      sp.simplify(sp.expand(((Ltilde - L) + 4 * sp.sinh(2 * phi) * q1**2).rewrite(sp.exp))))

# ---------------------------------------------------------------- C14: m' is NOT proportional to L (different functionals)
# structural: on-shell m' carries an overall factor rho' (via the eps identity); L on-shell = 4-2U has none.
mp_onshell = sp.simplify(m.diff(r).subs({q2: sol[q2], p2: sol[p2]}))
check("C14 m'(on-shell) has overall factor rho' (m'|_{rho'=0} = 0), while L|_{H=0}=4-2U does not",
      sp.simplify(mp_onshell.subs(q1, 0)))

print("\nSUMMARY:", sum(1 for _, ok, _ in OK if ok), "/", len(OK), "PASS")
