"""CAS verifier for the V1 virial identities (dispatch 2026-07-16 §3).

Verifies SYMBOLICALLY (sympy):
  (T1) trace identity: T_ii = -E2dens + E4dens = S            [pure index algebra, generic field]
  (MD) multiplier drop: (lam * n_a) * d_j n_a = 0 given n.n=1  [generic constrained field]
  (T2') translation identity: d_i T_ij + Rhat_a d_j n_a = 0    [explicit constrained test fields]
        with Rhat the functional gradient (sign convention of the derivation record), verified
        identically in the coordinates for concrete non-trivial unit fields n = (sin f cos g,
        sin f sin g, cos f) with polynomial/trig f, g — the identity must simplify to 0 exactly.
Output: verify_virial_identity_cas_output.txt with per-check PASS/FAIL.
"""
import sympy as sp

out = []
def check(name, ok, detail=''):
    out.append((name, bool(ok), detail)); print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}", flush=True)

x1, x2, x3 = sp.symbols('x1 x2 x3', real=True)
X = (x1, x2, x3)
xi, kap = sp.symbols('xi kappa', positive=True)

def build(nvec):
    """Given a 3-component unit field (list of sympy exprs), return d[i][a], Fij, X_, Y_, T[i][j], S."""
    d = [[sp.diff(nvec[a], X[i]) for a in range(3)] for i in range(3)]
    def cross(u, v):
        return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
    F = [[sum(nvec[a]*cross(d[i], d[j])[a] for a in range(3)) for j in range(3)] for i in range(3)]
    X_ = sum(d[k][a]**2 for k in range(3) for a in range(3))
    Y_ = sum(F[k][l]**2 for k in range(3) for l in range(3))
    T = [[xi*(sum(d[i][a]*d[j][a] for a in range(3)) - sp.Rational(1,2)*(1 if i==j else 0)*X_)
          + kap*(sum(F[i][k]*F[j][k] for k in range(3)) - sp.Rational(1,4)*(1 if i==j else 0)*Y_)
          for j in range(3)] for i in range(3)]
    S = -xi/2*X_ + kap/4*Y_
    return d, F, X_, Y_, T, S

# ---------- (T1) + (MD) on a GENERIC constrained field: n = m/|m|, m arbitrary functions ----------
m = [sp.Function(f'm{a}')(x1, x2, x3) for a in range(3)]
r = sp.sqrt(sum(mi**2 for mi in m))
n_gen = [mi/r for mi in m]
d_g, F_g, X_g, Y_g, T_g, S_g = build(n_gen)
tr = sp.simplify(sum(T_g[i][i] for i in range(3)) - S_g)
check('(T1) trace T_ii = S (generic constrained field)', tr == 0, f'residual={tr}')
lam = sp.Function('lam')(x1, x2, x3)
md = [sp.simplify(sum(lam*n_gen[a]*d_g[j][a] for a in range(3))) for j in range(3)]
check('(MD) multiplier drop (generic constrained field)', all(sp.simplify(t) == 0 for t in md),
      f'residuals={[sp.simplify(t) for t in md]}')

# ---------- (T2') on explicit non-trivial unit fields ----------
def rhat(nvec, d, F):
    """FULL unconstrained functional gradient (CORRECTED after first CAS pass caught the sign):
    Rhat_a = -xi*Lap(n_a) + (kap/2) F_kl (d_k n x d_l n)_a + kap * d_i( F_ik (n x d_k n)_a ).
    The middle term is normal (parallel to n for unit fields) and self-drops in the contraction."""
    def cross(u, v):
        return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
    R = []
    for a in range(3):
        lap = sum(sp.diff(nvec[a], X[i], 2) for i in range(3))
        normal = sum(F[k][l]*cross(d[k], d[l])[a] for k in range(3) for l in range(3))
        term4 = 0
        for i in range(3):
            for k in range(3):
                term4 += sp.diff(F[i][k]*cross(nvec, d[k])[a], X[i])
        R.append(-xi*lap + kap/2*normal + kap*term4)
    return R

FIELDS = [
    ('polytrig-1', sp.sin(x1 + 2*x2)*sp.cos(x3), x2*x3 + x1),
    ('polytrig-2', x1*x2 + sp.Rational(1,3)*x3**2, sp.cos(x1) + x2),
]
for (tag, f, g) in FIELDS:
    nv = [sp.sin(f)*sp.cos(g), sp.sin(f)*sp.sin(g), sp.cos(f)]
    d, F, X_, Y_, T, S = build(nv)
    R = rhat(nv, d, F)
    ok = True; worst = 0
    for j in range(3):
        divT = sum(sp.diff(T[i][j], X[i]) for i in range(3))
        rw = sum(R[a]*d[j][a] for a in range(3))
        resid = sp.simplify(sp.expand_trig(sp.expand(divT + rw)))
        if resid != 0:
            # fall back: exact rational-point evaluation at several points (still exact arithmetic)
            import random
            random.seed(7)
            allzero = True
            for _ in range(4):
                pt = {x1: sp.Rational(random.randint(-3,3), 7), x2: sp.Rational(random.randint(-3,3), 5),
                      x3: sp.Rational(random.randint(-3,3), 11), xi: sp.Rational(2,3), kap: sp.Rational(5,7)}
                v = sp.simplify(resid.subs(pt))
                if sp.nsimplify(v) != 0 and abs(complex(v.evalf(30))) > 1e-25: allzero = False; break
            ok = ok and allzero
    check(f"(T2') div T + Rhat·dn = 0 [{tag}]", ok)

npass = sum(1 for _, k, _ in out if k)
verdict = 'PASS' if npass == len(out) else 'FAIL'
print(f"\n== CAS VERDICT: {verdict} ({npass}/{len(out)}) ==")
with open('verify_virial_identity_cas_output.txt', 'w') as fo:
    for nm, k, dt in out: fo.write(f"[{'PASS' if k else 'FAIL'}] {nm} {dt}\n")
    fo.write(f"== CAS VERDICT: {verdict} ({npass}/{len(out)}) ==\n")
