"""
BLIND ADVERSARIAL VERIFIER (written from scratch, no existing scripts consulted).

Claim under test:
  S = int d^4x sqrt(-g) [ f(phi) R + L_matter ],  f = c0^4 e^{-8phi}/(16 pi G).
  Metric g = diag(-e^{-2phi} c0^2, e^{2phi}, r^2, r^2 sin^2 th).
  Field eq (vacuum): f G_{mn} + (g_{mn} Box - nabla_m nabla_n) f = 0.

  (a) E_{mn} = (g_{mn} Box - nabla_m nabla_n) f is NONZERO in vacuum.
  (b) Schwarzschild phi = -1/2 ln(1 - rs/r) FAILS the full vacuum eq.
  (c) flat phi=0 SOLVES it.
  (d) reduced-action EL agrees with covariant.
"""
import sympy as sp

t, r, th, ph = sp.symbols('t r theta phi_ang', real=True)
rs, c0, G = sp.symbols('r_s c0 G', positive=True)
phi = sp.Function('phi', real=True)(r)

coords = [t, r, th, ph]

# Metric (lower)
gtt = -sp.exp(-2*phi)*c0**2
grr = sp.exp(2*phi)
gthth = r**2
gphph = r**2*sp.sin(th)**2
g = sp.diag(gtt, grr, gthth, gphph)
ginv = g.inv()

n = 4

def d(expr, i):
    return sp.diff(expr, coords[i])

# Christoffel symbols Gamma^a_{bc}
Gamma = [[[sp.S(0)]*n for _ in range(n)] for _ in range(n)]
for a in range(n):
    for b in range(n):
        for c in range(n):
            s = sp.S(0)
            for dd in range(n):
                s += ginv[a, dd]*(d(g[dd, b], c) + d(g[dd, c], b) - d(g[b, c], dd))
            Gamma[a][b][c] = sp.simplify(s/2)

# Ricci tensor R_{bc} = d_a G^a_bc - d_c G^a_ba + G^a_ad G^d_bc - G^a_cd G^d_ba
Ric = sp.zeros(n, n)
for b in range(n):
    for c in range(n):
        s = sp.S(0)
        for a in range(n):
            s += d(Gamma[a][b][c], a) - d(Gamma[a][b][a], c)
            for dd in range(n):
                s += Gamma[a][a][dd]*Gamma[dd][b][c] - Gamma[a][c][dd]*Gamma[dd][b][a]
        Ric[b, c] = sp.simplify(s)

# Ricci scalar
Rscalar = sp.simplify(sum(ginv[i, j]*Ric[i, j] for i in range(n) for j in range(n)))

# Einstein tensor lower then mixed G^a_b
Glow = Ric - sp.Rational(1, 2)*g*Rscalar
Gmix = sp.simplify(ginv*Glow)

print("==== PART 1: Einstein tensor (mixed G^mu_nu) ====")
print("G^t_t =", sp.simplify(Gmix[0, 0]))
print("G^r_r =", sp.simplify(Gmix[1, 1]))
print("G^th_th =", sp.simplify(Gmix[2, 2]))
print("G^t_t - G^r_r =", sp.simplify(Gmix[0, 0] - Gmix[1, 1]))

# ===== PART 2: f, covariant Hessian, Box, E mixed =====
f = c0**4*sp.exp(-8*phi)/(16*sp.pi*G)
df = [d(f, i) for i in range(n)]

# Hessian_{mn} = d_m d_n f - Gamma^l_{mn} d_l f
Hess = sp.zeros(n, n)
for m in range(n):
    for nn in range(n):
        s = d(df[nn], m)
        for l in range(n):
            s -= Gamma[l][m][nn]*df[l]
        Hess[m, nn] = sp.simplify(s)

Boxf = sp.simplify(sum(ginv[i, j]*Hess[i, j] for i in range(n) for j in range(n)))

# E^mu_nu = delta^mu_nu Box f - g^{mu l} Hess_{l nu}
Emix = sp.zeros(n, n)
for mu in range(n):
    for nu in range(n):
        s = (Boxf if mu == nu else sp.S(0))
        for l in range(n):
            s -= ginv[mu, l]*Hess[l, nu]
        Emix[mu, nu] = sp.simplify(s)

print("\n==== PART 2: f-Hessian sector ====")
print("Box f =", Boxf)
print("E^t_t =", Emix[0, 0])
print("E^r_r =", Emix[1, 1])
print("E^th_th =", Emix[2, 2])
nonzero_E = any(Emix[i, i] != 0 for i in range(n))
print("E nonzero (symbolic, general phi)?", nonzero_E)

# ===== PART 3: full vacuum eq, substitute Schwarzschild =====
EQ = sp.simplify(f*Gmix + Emix)

phi_schw = sp.Rational(-1, 2)*sp.log(1 - rs/r)
subs_schw = {phi: phi_schw,
             sp.Derivative(phi, r): sp.diff(phi_schw, r),
             sp.Derivative(phi, r, r): sp.diff(phi_schw, r, r)}

# Robust substitution: replace the Function and its derivatives.
def sub_profile(expr, profile):
    expr = expr.subs(sp.Derivative(phi, (r, 2)), sp.diff(profile, r, 2))
    expr = expr.subs(sp.Derivative(phi, r), sp.diff(profile, r))
    expr = expr.subs(phi, profile)
    return sp.simplify(expr)

print("\n==== PART 3: Schwarzschild phi = -1/2 ln(1-rs/r) ====")
EQ_schw = [sub_profile(EQ[i, i], phi_schw) for i in range(3)]
print("EQ^t_t (schw) =", EQ_schw[0])
print("EQ^r_r (schw) =", EQ_schw[1])
print("EQ^th_th (schw) =", EQ_schw[2])
schw_fails = any(e != 0 for e in EQ_schw)
print("Schwarzschild FAILS full vacuum eq?", schw_fails)

# Also report the pure-Einstein pieces for context
print("  -- diagnostic: G^mu_nu under schw (should be the GR Schw, nonzero offdiag cancel?)")
for i, lbl in enumerate(['tt', 'rr', 'thth']):
    print("    f*G^%s =" % lbl, sub_profile((f*Gmix)[i, i], phi_schw),
          " ; E^%s =" % lbl, sub_profile(Emix[i, i], phi_schw))

# ===== PART 4: flat phi=0 =====
print("\n==== PART 4: flat phi = 0 ====")
EQ_flat = [sub_profile(EQ[i, i], sp.S(0)) for i in range(3)]
print("EQ^t_t (flat) =", EQ_flat[0])
print("EQ^r_r (flat) =", EQ_flat[1])
print("EQ^th_th (flat) =", EQ_flat[2])
flat_solves = all(e == 0 for e in EQ_flat)
print("Flat space SOLVES full vacuum eq?", flat_solves)

# ===== PART 5: reduced-action cross-check =====
print("\n==== PART 5: reduced-action EL cross-check ====")
N = sp.Function('N')(r)
L = sp.Function('L')(r)
# metric diag(-N, L, r^2, r^2 sin^2)
gR = sp.diag(-N, L, r**2, r**2*sp.sin(th)**2)
gRinv = gR.inv()
sqrtmg = sp.sqrt(-gR.det())  # = sqrt(N L r^4 sin^2) = r^2 sin th sqrt(N L)
sqrtmg = sp.simplify(sqrtmg)

# Ricci scalar for this metric (recompute generally in N,L)
GammaR = [[[sp.S(0)]*n for _ in range(n)] for _ in range(n)]
for a in range(n):
    for b in range(n):
        for c in range(n):
            s = sp.S(0)
            for dd in range(n):
                s += gRinv[a, dd]*(d(gR[dd, b], c)+d(gR[dd, c], b)-d(gR[b, c], dd))
            GammaR[a][b][c] = sp.simplify(s/2)
RicR = sp.zeros(n, n)
for b in range(n):
    for c in range(n):
        s = sp.S(0)
        for a in range(n):
            s += d(GammaR[a][b][c], a)-d(GammaR[a][b][a], c)
            for dd in range(n):
                s += GammaR[a][a][dd]*GammaR[dd][b][c]-GammaR[a][c][dd]*GammaR[dd][b][a]
        RicR[b, c] = sp.simplify(s)
RscalR = sp.simplify(sum(gRinv[i, j]*RicR[i, j] for i in range(n) for j in range(n)))

fR = N**4/(16*sp.pi*G)
# Lagrangian density (drop overall sin th, harmless constant for EL in r)
Lag = sp.simplify(sqrtmg*fR*RscalR / sp.sin(th))

# Euler-Lagrange w.r.t. a field q(r) up to 2nd derivative:
# EL = dLag/dq - d/dr(dLag/dq') + d^2/dr^2(dLag/dq'')
def euler_lagrange(Lag, q):
    qp = sp.diff(q, r)
    qpp = sp.diff(q, r, r)
    dq = sp.diff(Lag, q)
    dqp = sp.diff(Lag, qp)
    dqpp = sp.diff(Lag, qpp)
    EL = dq - sp.diff(dqp, r) + sp.diff(dqpp, r, r)
    return sp.simplify(EL)

EL_N = euler_lagrange(Lag, N)
EL_L = euler_lagrange(Lag, L)

# Schwarzschild: N = (1-rs/r) c0^2, L = 1/(1-rs/r)
Nsch = (1 - rs/r)*c0**2
Lsch = 1/(1 - rs/r)

def sub_NL(expr, Nval, Lval):
    e = expr
    e = e.subs(sp.Derivative(N, (r, 2)), sp.diff(Nval, r, 2))
    e = e.subs(sp.Derivative(L, (r, 2)), sp.diff(Lval, r, 2))
    e = e.subs(sp.Derivative(N, r), sp.diff(Nval, r))
    e = e.subs(sp.Derivative(L, r), sp.diff(Lval, r))
    e = e.subs(N, Nval).subs(L, Lval)
    return sp.simplify(e)

EL_N_sch = sub_NL(EL_N, Nsch, Lsch)
EL_L_sch = sub_NL(EL_L, Nsch, Lsch)
print("Reduced EL_N (schw) =", EL_N_sch)
print("Reduced EL_L (schw) =", EL_L_sch)

# Flat: N = c0^2, L = 1
EL_N_flat = sub_NL(EL_N, c0**2, sp.S(1))
EL_L_flat = sub_NL(EL_L, c0**2, sp.S(1))
print("Reduced EL_N (flat) =", EL_N_flat)
print("Reduced EL_L (flat) =", EL_L_flat)

reduced_schw_fails = (EL_N_sch != 0) or (EL_L_sch != 0)
reduced_flat_solves = (EL_N_flat == 0) and (EL_L_flat == 0)

print("\n==== SUMMARY ====")
print("(a) E nonzero in vacuum:        ", "PASS" if nonzero_E else "FAIL")
print("(b) Schwarzschild fails:        ", "PASS" if schw_fails else "FAIL")
print("(c) flat solves:                ", "PASS" if flat_solves else "FAIL")
print("(d) reduced agrees (schw fails & flat solves): ",
      "PASS" if (reduced_schw_fails and reduced_flat_solves and schw_fails and flat_solves) else "FAIL")
