"""
V1b -- follow-ups to V1's fails:
 (1) axial det re-test in the audit's own flow variables: det = c^3 (X+Y)^3
     / (64 r^8 sin^3) with X = r^2 f^2 p0r^2, Y = f p0t^2.
 (2) corrected physical reading: the q,u eliminations are the first-order
     vanishing of the DENSITIZED UPPER stress components sqrt(-g) T^{r theta},
     sqrt(-g) T^{r vphi} (exact identity), NOT of the mixed T^r_theta.
 (3) EXACT-SPHERICAL elimination in the exact-areal scheme: at p0t = 0 the
     w direction drops out of L2 entirely (flat); eliminating (a,b,q,u,v)
     -- does the corrected density equal the audit's flipped target?
 (4) the areal-scheme (q,w) degeneracy polynomial (for comparison with the
     audit's X^2+7XY-2Y^2).
 (5) w-flatness certificate: in the areal scheme at p0t=0, L2 is w-free.
"""
import sympy as sp, time
t0 = time.time()
PASS = []
def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"CHECK {name}: {'PASS' if ok else 'FAIL'} {detail}", flush=True)

c, r, st = sp.symbols('c r s_theta', positive=True)
phi0, p0r, p0t = sp.symbols('phi0 p0r p0t', real=True)
dp, dpT, dpr, dpth, dpv = sp.symbols('dp dpT dpr dpth dpv', real=True)
a, b, p, k, w, q, u, v = sp.symbols('a b p k w q u v', real=True)
eps = sp.symbols('epsilon', real=True)
f0 = sp.exp(-2*phi0)
met = [a, b, p, k, w, q, u, v]
jets = [dp, dpT, dpr, dpth, dpv]

def build(scheme, sph=False):
    phif = phi0 + eps*dp
    P0t = sp.Integer(0) if sph else p0t
    if scheme == 'audit':
        gthth = r**2*(1 + eps*(k + w))**2
        gvv = r**2*st**2*(1 + eps*(k - w))**2
    else:
        gthth = r**2*sp.exp(2*eps*(k + w))
        gvv = r**2*st**2*sp.exp(2*eps*(k - w))
    g = sp.Matrix([
        [-sp.exp(-2*phif), eps*a,           eps*b,  eps*p],
        [eps*a,            sp.exp(2*phif),  eps*q,  eps*u],
        [eps*b,            eps*q,           gthth,  eps*v],
        [eps*p,            eps*u,           eps*v,  gvv]])
    grad = sp.Matrix([eps*dpT, p0r + eps*dpr, P0t + eps*dpth, eps*dpv])
    det = g.det(); adj = g.adjugate()
    N = sp.expand((grad.T*adj*grad)[0, 0])
    L = -(c/2)*sp.exp(-2*phif)*N/det*sp.sqrt(-det)
    L1 = sp.expand(sp.diff(L, eps).subs(eps, 0))
    L2 = sp.expand(sp.powsimp(sp.expand(sp.together(
        sp.diff(L, eps, 2).subs(eps, 0))/2)))
    return g, grad, L1, L2

# ---------- (1) axial det in flow variables ----------
X, Y = sp.symbols('X Y', positive=True)
_, _, L1a, L2a = build('audit')
Hax = sp.Matrix(3, 3, lambda i, j:
                sp.diff(L2a, [p, u, v][i], [p, u, v][j])/2)
detax = sp.factor(Hax.det())
detax_XY = sp.simplify(detax.subs(p0r, sp.sqrt(X)*sp.exp(2*phi0)/r)
                       .subs(p0t, sp.sqrt(Y)*sp.exp(phi0)))
check("V1b-1 det H_axial = c^3 (X+Y)^3/(64 r^8 sin^3) EXACTLY (positive "
      "definite numerator cube; saddle block, nondegenerate everywhere "
      "except X=Y=0)",
      sp.simplify(detax_XY - c**3*(X + Y)**3/(64*r**8*st**3)) == 0,
      f"det = {sp.factor(detax_XY)}")

# ---------- (2) densitized-upper stress identity ----------
g, grad, L1, L2 = build('audit')
gi = g.adjugate()/g.det()
dphi2 = (grad.T*gi*grad)[0, 0]
Tdn = c*sp.exp(-2*(phi0 + eps*dp))*(grad*grad.T - g*dphi2/2)
Tup = gi*Tdn*gi
sq = sp.sqrt(-g.det())
for comp, fld, nm in (((1, 2), q, 'q ~ sqrt(-g) T^{r th}'),
                      ((1, 3), u, 'u ~ sqrt(-g) T^{r v}'),
                      ((0, 1), a, 'a ~ sqrt(-g) T^{T r}'),
                      ((0, 2), b, 'b ~ sqrt(-g) T^{T th}')):
    dens = sq*Tup[comp[0], comp[1]]
    d1 = sp.simplify(sp.diff(dens, eps).subs(eps, 0))
    res = sp.simplify(sp.expand(d1 - sp.diff(L2, fld)))
    check(f"V1b-2 dL2/d{fld} = delta[{nm}] exactly (first-order densitized "
          "upper stress vanishing IS the elimination)", res == 0,
          f"residual = {res}")

# ---------- (3)+(5) exact-spherical areal-scheme elimination ----------
gs, grads, L1s, L2s = build('areal', sph=True)
check("V1b-5 w-FLATNESS: in the exact-areal scheme at p0t=0, L2 is "
      "completely w-independent (w is a quadratic-flat direction of the "
      "spherical second variation)", sp.simplify(sp.diff(L2s, w)) == 0)
elim5 = [a, b, q, u, v]
sol5 = sp.solve([sp.diff(L2s, s) for s in elim5], elim5, dict=True)[0]
L2c5 = sp.expand(sp.powsimp(sp.cancel(sp.together(L2s.subs(sol5)))))
for s in (p, k, w):
    L2c5 = L2c5.subs(s, 0)
target = sp.expand(-(c/2)*st*(r**2*dpT**2
                              + f0**2*r**2*(dpr**2 - 8*p0r*dp*dpr
                                            + 8*p0r**2*dp**2)
                              - f0*dpth**2 - f0*dpv**2/st**2))
check("V1b-3 EXACT-SPHERICAL corrected density in the canon-true areal "
      "scheme = the audit's flipped target (q-elimination alone carries "
      "the dpth flip; w flat and sourceless)",
      sp.simplify(L2c5 - target) == 0,
      f"residual = {sp.simplify(L2c5 - target)}")

# also: audit-scheme exact-spherical (w coupled-but-decoupled) for parity
ga, grada, L1a2, L2a2 = build('audit', sph=True)
sol6 = sp.solve([sp.diff(L2a2, s) for s in [a, b, q, w, u, v]],
                [a, b, q, w, u, v], dict=True)[0]
L2c6 = sp.expand(sp.powsimp(sp.cancel(sp.together(L2a2.subs(sol6)))))
for s in (p, k):
    L2c6 = L2c6.subs(s, 0)
check("V1b-3' audit-scheme exact-spherical elimination agrees (schemes "
      "coincide AT spherical; they diverge only in the formed maps and "
      "in the p0t->0 LIMIT of the formed maps)",
      sp.simplify(L2c6 - target) == 0)

# ---------- (4) areal-scheme (q,w) degeneracy polynomial ----------
_, _, L1e, L2e = build('areal')
Hqq = sp.diff(L2e, q, 2)/2; Hww = sp.diff(L2e, w, 2)/2
Hqw = sp.diff(L2e, q, w)/2
detqw_e = sp.factor(sp.simplify(Hqq*Hww - Hqw**2))
d_XY = sp.simplify(detqw_e.subs(p0r, sp.sqrt(X)*sp.exp(2*phi0)/r)
                   .subs(p0t, sp.sqrt(Y)*sp.exp(phi0)))
print(f"  areal-scheme det H_qw = {sp.factor(d_XY)}")
print(f"  alpha_ww(areal) in XY = "
      f"{sp.simplify((Hww).subs(p0r, sp.sqrt(X)*sp.exp(2*phi0)/r).subs(p0t, sp.sqrt(Y)*sp.exp(phi0)))}")
print(f"  alpha_qq in XY = "
      f"{sp.simplify((Hqq).subs(p0r, sp.sqrt(X)*sp.exp(2*phi0)/r).subs(p0t, sp.sqrt(Y)*sp.exp(phi0)))}")
print(f"  alpha_qw in XY = "
      f"{sp.simplify((Hqw).subs(p0r, sp.sqrt(X)*sp.exp(2*phi0)/r).subs(p0t, sp.sqrt(Y)*sp.exp(phi0)))}")
# formed corrected dpth ratio in the areal scheme, in XY variables
elim = [a, b, q, w, u, v]
sol_e = sp.solve([sp.diff(L2e, s) for s in elim], elim, dict=True)[0]
L2ce = sp.expand(sp.powsimp(sp.cancel(sp.together(L2e.subs(sol_e)))))
for s in (p, k):
    L2ce = L2ce.subs(s, 0)
L2dp = L2e
for s in met:
    L2dp = L2dp.subs(s, 0)
rth_e = sp.simplify(sp.diff(L2ce, dpth, 2)/sp.diff(L2dp, dpth, 2))
rth_e_XY = sp.simplify(rth_e.subs(p0r, sp.sqrt(X)*sp.exp(2*phi0)/r)
                       .subs(p0t, sp.sqrt(Y)*sp.exp(phi0)))
print(f"  AREAL formed dpth flip ratio = {sp.factor(rth_e_XY)}")
print(f"  AUDIT formed dpth flip ratio = "
      f"{sp.factor(-(X - Y)*(X + 2*Y)/(X**2 + 7*X*Y - 2*Y**2))}")
lim_e = sp.limit(rth_e_XY, Y, 0, '+')
check("V1b-4 the areal-scheme formed dpth map does NOT tend to -1 as "
      "Y->0 (discontinuous spherical limit: the formed maps are "
      "scheme-dependent and off-shell -- only the PDE run settles them)",
      sp.simplify(lim_e + 1) != 0, f"limit Y->0+: {lim_e}")

n = sum(1 for _, ok in PASS if ok)
print(f"\nV1b TOTAL: {n}/{len(PASS)} PASS   ({time.time()-t0:.1f}s)")
for nm, ok in PASS:
    if not ok:
        print("  FAIL:", nm)
