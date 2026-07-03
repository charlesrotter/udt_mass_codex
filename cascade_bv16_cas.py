"""bv16 blind verifier CAS: Y1 (lapse cancellation + angular reduction), Y2 (on-shell
identities), Y3(i) (off-shell MS identity from a from-scratch Einstein tensor).
All symbols built here from scratch; no repo algebra imported."""
import sympy as sp

r, th, ps, c, Z = sp.symbols('r theta psi c Z', positive=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho')(r)
Ufun = sp.Function('U')          # U(rho)
U = Ufun(rho)
Up = sp.diff(U, rho)             # U'(rho) as derivative w.r.t. rho

OK = lambda name, expr: print(f"[{name}] {'PASS' if sp.simplify(expr) == 0 else 'FAIL: ' + str(sp.simplify(expr))}")

# ================= Y1.1: sqrt(-g) = c rho^2 sin(theta) exactly =================
g4 = sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi), rho**2, rho**2*sp.sin(th)**2)
sqrtg = sp.sqrt(-g4.det())
OK("Y1.1 sqrt(-g) - c*rho^2*sin(th)", sp.powsimp(sp.simplify(sqrtg - c*rho**2*sp.sin(th))))

# ================= generic curvature machinery (from scratch) =================
def christoffel(gm, X):
    n = len(X); gi = gm.inv()
    Gam = [[[sp.simplify(sum(gi[a, d]*(sp.diff(gm[d, b], X[cc]) + sp.diff(gm[d, cc], X[b])
             - sp.diff(gm[b, cc], X[d]))/2 for d in range(n)))
             for cc in range(n)] for b in range(n)] for a in range(n)]
    return Gam

def ricci(gm, X):
    n = len(X); Gam = christoffel(gm, X)
    Ric = sp.zeros(n, n)
    for b in range(n):
        for cc in range(n):
            expr = 0
            for a in range(n):
                expr += sp.diff(Gam[a][b][cc], X[a]) - sp.diff(Gam[a][b][a], X[cc])
                for d in range(n):
                    expr += Gam[a][a][d]*Gam[d][b][cc] - Gam[a][cc][d]*Gam[d][b][a]
            Ric[b, cc] = sp.simplify(expr)
    return Ric

# ---- Y1.2: R^{(2)} of the transverse 2-metric h_AB = rho^2 * Omega_AB
h2 = sp.diag(rho**2, rho**2*sp.sin(th)**2)   # rho = rho(r) is constant on the 2-surface
X2 = [th, ps]
Ric2 = ricci(h2, X2)
R2 = sp.simplify(sum(h2.inv()[i, j]*Ric2[i, j] for i in range(2) for j in range(2)))
OK("Y1.2 R^(2) - 2/rho^2", R2 - 2/rho**2)

# ---- Y1.3: K_AB = (1/2) e^{-phi} d_r h_AB ; Kcal = K_AB K^AB - K^2
KAB = sp.Rational(1, 2)*sp.exp(-phi)*sp.diff(h2, r)
hinv = h2.inv()
Kmix = sp.simplify(hinv*KAB)                    # K^A_B
Ktr = sp.simplify(Kmix.trace())
KK = sp.simplify((Kmix*Kmix).trace())
Kcal = sp.simplify(KK - Ktr**2)
OK("Y1.3 Kcal + 2 e^{-2phi} rho'^2 / rho^2", Kcal + 2*sp.exp(-2*phi)*sp.diff(rho, r)**2/rho**2)

# ---- Y1.4: angular integral of c*sqrt(h)*[(Z/2)phi'^2 + R2 + Kcal] = 4 pi c * L_geo
sqrth = rho**2*sp.sin(th)
integrand = sqrth*(Z/2*sp.diff(phi, r)**2 + R2 + Kcal)
ang = sp.integrate(sp.integrate(integrand, (th, 0, sp.pi)), (ps, 0, 2*sp.pi))
L_geo = Z/2*rho**2*sp.diff(phi, r)**2 - 2*sp.exp(-2*phi)*sp.diff(rho, r)**2 + 2
OK("Y1.4 angular-reduced geo integrand - 4pi*L_geo", sp.simplify(ang - 4*sp.pi*L_geo))

# ---- Y1.5: EL of L_banked = L_geo - U reproduces the solver EOMs (sigma = e^{2phi}U'/4)
L = L_geo - U
EL_phi = sp.simplify(sp.diff(sp.diff(L, sp.diff(phi, r)), r) - sp.diff(L, phi))
EL_rho = sp.simplify(sp.diff(sp.diff(L, sp.diff(rho, r)), r) - sp.diff(L, rho))
phipp_solve = sp.solve(EL_phi, sp.diff(phi, r, 2))[0]
rhopp_solve = sp.solve(EL_rho, sp.diff(rho, r, 2))[0]
phipp_solver = 4*sp.diff(rho, r)**2/(sp.exp(2*phi)*Z*rho**2) - 2*sp.diff(phi, r)*sp.diff(rho, r)/rho
rhopp_solver = (2*sp.diff(phi, r)*sp.diff(rho, r) - Z/4*rho*sp.exp(2*phi)*sp.diff(phi, r)**2
                + sp.exp(2*phi)/4*Up)
OK("Y1.5a EL phi'' - solver phi''", phipp_solve - phipp_solver)
OK("Y1.5b EL rho'' - solver rho''", rhopp_solve - rhopp_solver)

# ================= Y2 =================
H = (Z/2*rho**2*sp.diff(phi, r)**2 - 2*sp.exp(-2*phi)*sp.diff(rho, r)**2 - 2 + U)
# (i) L = H + 4 - 2U identically
OK("Y2.i L - (H + 4 - 2U)", L - (H + 4 - 2*U))
# H is the Legendre transform of L (sanity)
Hleg = (sp.diff(phi, r)*sp.diff(L, sp.diff(phi, r)) + sp.diff(rho, r)*sp.diff(L, sp.diff(rho, r)) - L)
OK("Y2.i' H - Legendre(L)", H - Hleg)
# (ii) boundary identity ON-SHELL: Z rho^2 phi'^2 - 4 e^{-2phi} rho'^2 = d/dr[-4 e^{-2phi} rho rho'] + rho U'
lhs = Z*rho**2*sp.diff(phi, r)**2 - 4*sp.exp(-2*phi)*sp.diff(rho, r)**2
rhs_expr = sp.diff(-4*sp.exp(-2*phi)*rho*sp.diff(rho, r), r) + rho*Up
diff_expr = sp.simplify(lhs - rhs_expr)
# substitute the rho EOM only:
diff_onshell = sp.simplify(diff_expr.subs(sp.diff(rho, r, 2), rhopp_solver))
OK("Y2.ii boundary identity (rho-EOM only)", diff_onshell)
# does it need the phi EOM too? check off-shell residual
print("[Y2.ii off-shell residual =", sp.simplify(diff_expr), "] (nonzero => genuinely on-shell identity)")
# chain: L = (1/2)(lhs) + 2 - U  =>  int L = [-2 e^{-2phi} rho rho'] + int(2 - U + rho U'/2)
OK("Y2.ii' L - [(1/2)lhs + 2 - U]", L - (lhs/2 + 2 - U))
# (iii) m_MS at folds: m = rho/2 (1 - e^{-2phi} rho'^2); rho'=0 => m = rho/2  (algebraic)
mMS = rho/2*(1 - sp.exp(-2*phi)*sp.diff(rho, r)**2)
OK("Y2.iii m_MS|_{rho'=0} - rho/2", mMS.subs(sp.diff(rho, r), 0) - rho/2)
# on-shell H conservation: dH/dr = 0 using both EOMs (supports H==0 propagation)
dH = sp.diff(H, r).subs({sp.diff(phi, r, 2): phipp_solver, sp.diff(rho, r, 2): rhopp_solver})
OK("Y2.extra dH/dr on-shell", dH)

# ================= Y3(i): Einstein tensor from scratch, OFF-SHELL =================
c1 = sp.Integer(1)  # c = 1 (banked units)
g4u = sp.diag(-sp.exp(-2*phi), sp.exp(2*phi), rho**2, rho**2*sp.sin(th)**2)
X4 = [sp.Symbol('t'), r, th, ps]
Ric4 = ricci(g4u, X4)
g4i = g4u.inv()
Rs = sp.simplify(sum(g4i[i, j]*Ric4[i, j] for i in range(4) for j in range(4)))
# mixed G^t_t = g^{tt} (R_tt - R/2 g_tt)
Gtt_mixed = sp.simplify(g4i[0, 0]*(Ric4[0, 0] - Rs/2*g4u[0, 0]))
eps = -Gtt_mixed/(8*sp.pi)
print("[Y3.i] eps*8*pi*rho^2 =", sp.simplify(8*sp.pi*rho**2*eps))
ident = sp.simplify(sp.diff(mMS, r) - 4*sp.pi*rho**2*sp.diff(rho, r)*eps)
OK("Y3.i m'_MS - 4 pi rho^2 rho' eps (OFF-SHELL)", ident)
# on-shell eps (substitute rho'' from the rho EOM) for numeric use:
eps_on = sp.simplify((8*sp.pi*rho**2*eps).subs(sp.diff(rho, r, 2), rhopp_solver))
print("[Y3.i] 8*pi*rho^2*eps ON-SHELL =", eps_on)
