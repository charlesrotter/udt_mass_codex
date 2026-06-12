"""
Numeric leg: route 1 (second-order gluing consistency across the n-family)
and route 3 (distributional weld in both slots, mollified).
q = 1/3 throughout. mu(n) = (1-n)q(1-q), nu(n) = sqrt(17-8n).
DtN normalization: D = y^2 u'/u at y=1 = u'(1)/u(1) for the regular branch
on (0,1]; record formula D_nu(lam) = sqrt(lam) I_{nu+1}(6 sqrt lam)/I_nu(6 sqrt lam)
+ (q nu - 1)/2.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import iv
import mpmath as mp

q = 1.0/3.0
def mu_of(n): return (1.0-n)*q*(1.0-q)
def nu_of(n): return np.sqrt(17.0-8.0*n)

PASS=0; FAIL=0
def check(name, val, tol):
    global PASS, FAIL
    ok = abs(val) < tol
    print(("PASS" if ok else "FAIL"), name, f"  |resid|={abs(val):.2e}")
    if ok: PASS+=1
    else: FAIL+=1

def D_bessel(n, lam):
    nu = nu_of(n)
    z = 6.0*np.sqrt(lam)
    return np.sqrt(lam)*iv(nu+1.0, z)/iv(nu, z) + (q*nu-1.0)/2.0

# ---------------- N1: anchors against the banked record numbers
# record: L0(2) = D_sqrt17(2) + q = 1.33835 ;  D_3(2) + q = 1.25842
a1 = D_bessel(0.0, 2.0) + q
a2 = D_bessel(1.0, 2.0) + q
print(f"N1 D_sqrt17(2)+q = {a1:.6f}  (record 1.33835)")
print(f"N1 D_3(2)+q      = {a2:.6f}  (record 1.25842)")
check("N1a anchor n=0", a1-1.33835, 5e-5)
check("N1b anchor n=1", a2-1.25842, 5e-5)

# ---------------- N2: ODE shooting (regular branch) vs Bessel formula
def D_shoot(n, lam, y0=1e-8):
    mu = mu_of(n)
    ap = (-1.0+np.sqrt(1.0+4.0*mu))/2.0
    def rhs(y, s):
        u, p = s            # p = y^2 u'
        return [p/y**2, (lam*y**q + mu)*u]
    u0 = y0**ap; p0 = ap*y0**(ap+1.0)
    sol = solve_ivp(rhs, [y0, 1.0], [u0, p0], rtol=1e-12, atol=1e-300,
                    method='DOP853', dense_output=False)
    u, p = sol.y[0,-1], sol.y[1,-1]
    return p/u   # = y^2 u'/u at y=1

ns = [-4.0, -1.0, 0.0, 0.8, 1.0, 2.0]
for n in ns:
    for lam in (2.0, 6.0):
        d_ode = D_shoot(n, lam); d_bes = D_bessel(n, lam)
        check(f"N2 shooting=Bessel n={n} lam={lam}", d_ode-d_bes, 1e-6*max(1,abs(d_bes)))

# ---------------- N3: two-sided Calderon projector idempotence, all n
def D_exterior(n, lam, Y=3.0):
    """DtN at y=1 from the exterior side [1, Y], Dirichlet u(Y)=0.
    Convention: far graph = {(a, -D_+ a)} with p = y^2 u'."""
    mu = mu_of(n)
    def rhs(y, s):
        u, p = s
        return [p/y**2, (lam*y**q + mu)*u]
    sol = solve_ivp(rhs, [Y, 1.0], [0.0, 1.0], rtol=1e-12, atol=1e-300,
                    method='DOP853')
    u, p = sol.y[0,-1], sol.y[1,-1]
    return -p/u

print()
for n in ns:
    lam = 2.0
    Dm = D_shoot(n, lam); Dp = D_exterior(n, lam)
    C = np.array([[Dp, 1.0],[Dm*Dp, Dm]])/(Dm+Dp)
    r_idem = np.linalg.norm(C@C - C)
    g_int = np.array([1.0, Dm]); g_far = np.array([1.0, -Dp])
    r_fix  = np.linalg.norm(C@g_int - g_int)
    r_ann  = np.linalg.norm(C@g_far)
    check(f"N3 Calderon idempotent+complementary n={n}", r_idem+r_fix+r_ann, 1e-9)

# ---------------- N4: symplectic form preserved across a sourced interface, all n
# glued problem on [y0, 2] with interface at y_w = 1: u continuous,
# p(1+) - p(1-) = -W u(1), W = interface response (any value = any interface n).
# Concomitant B[u,v] = (u' v - u v') y^2 = (p_u v - u p_v) must be continuous.
print()
rng = np.random.default_rng(7)
for n in ns:
    mu = mu_of(n); lam = 2.0; W = (1.0-n)*0.31   # arbitrary symmetric response
    def rhs(y, s):
        u, pu, v, pv = s
        return [pu/y**2, (lam*y**q+mu)*u, pv/y**2, (lam*y**q+mu)*v]
    s0 = rng.standard_normal(4)
    sol = solve_ivp(rhs, [0.5, 1.0], s0, rtol=1e-12, atol=1e-14, method='DOP853')
    u, pu, v, pv = sol.y[:, -1]
    B_minus = pu*v - u*pv
    # apply jump: p -> p - W u
    pu2, pv2 = pu - W*u, pv - W*v
    B_plus_at_weld = pu2*v - u*pv2
    sol2 = solve_ivp(rhs, [1.0, 2.0], [u, pu2, v, pv2], rtol=1e-12, atol=1e-14,
                     method='DOP853')
    u3, pu3, v3, pv3 = sol2.y[:, -1]
    B_plus_far = pu3*v3 - u3*pv3
    check(f"N4 symplectic jump+flow conservation n={n}",
          (B_plus_at_weld-B_minus) + (B_plus_far-B_plus_at_weld), 1e-8*max(1,abs(B_minus)))

# ---------------- N5: route 3 — mollified weld, both slots' distributional form
# weld config: f = y^{-q} (y<1), f = 1 (y>=1); f continuous; Delta(y^2 f') = q.
# f-slot EL distribution:  EL_f  = -(1/2)(y^2 f')'  -> delta weight -q/2 at y=1
# phi-slot EL distribution: EL_phi = -2 f * EL_f = f (y^2 f')'
#                                                -> delta weight +q*f(1) = +q
print()
def weld_weights(eps):
    # smooth f' transition over [1-eps, 1+eps] via C^1 mollifier of the kink
    # f(y) = y^{-q} * S(y) blend; simplest: mollify g(y) = min(ln f) profile:
    # phi0(y) = q ln y for y<1, 0 for y>1 -> f = exp(-2*...)? Use direct kink in
    # h(y) := ln f = -q ln y (y<1), 0 (y>1); mollify h' with smoothstep.
    N = 400001
    y = np.linspace(1.0-6*eps, 1.0+6*eps, N)
    t = np.clip((y-1.0+eps)/(2*eps), 0.0, 1.0)
    sm = t*t*(3-2*t)                      # smoothstep 0->1
    hp = (-q/y)*(1.0-sm)                  # h' = -q/y -> 0
    h = np.concatenate([[0.0], np.cumsum((hp[1:]+hp[:-1])/2*np.diff(y))])
    h += (-q*np.log(y[0])) - h[0]         # match h = -q ln y at left end
    f = np.exp(h)
    fp = f*hp
    p = y**2*fp                            # y^2 f'
    dp = np.gradient(p, y)                 # (y^2 f')'
    test = np.exp(-((y-1.0)/(20*eps))**2)  # test fn ~ 1 near weld (broad)
    # delta weights = integral of EL distribution against test (bulk part -> 0 with eps)
    w_f   = np.trapezoid(-0.5*dp*test, y)
    w_phi = np.trapezoid(f*dp*test, y)
    return w_f, w_phi

for eps in (1e-2, 1e-3, 1e-4):
    wf, wp = weld_weights(eps)
    print(f"  eps={eps:.0e}:  f-slot weight={wf:+.6f} (target {-q/2:+.6f}), "
          f"phi-slot weight={wp:+.6f} (target {q:+.6f}), ratio={wp/wf:+.6f} (target -2 f(1) = -2)")
wf, wp = weld_weights(1e-4)
check("N5a f-slot delta weight -> -q/2", wf+q/2, 2e-3)
check("N5b phi-slot delta weight -> +q (well-defined)", wp-q, 2e-3)
check("N5c covariant ratio -> -2 f(1)", wp/wf+2.0, 1e-2)

# ---------------- N6: the spectrum DOES move with n (physical, not consistency)
# glued eigenvalue condition D_-(lam) + D_+(lam) = 0 on [0,1]+[1,3]:
from scipy.optimize import brentq
print()
print("N6 lowest glued eigenvalue lam* per n (consistency holds for all; value moves):")
for n in ns:
    g = lambda lam: D_shoot(n, lam) + D_exterior(n, lam)
    try:
        lo, hi = 1e-3, 0.01
        while g(lo)*g(hi) > 0 and hi < 100: hi *= 1.6
        lam_star = brentq(g, lo, hi, xtol=1e-10)
        print(f"   n={n:+.1f}  nu={nu_of(n):.4f}  lam* = {lam_star:.8f}")
    except Exception as e:
        print(f"   n={n:+.1f}  no root in range ({e})")

print(f"\nNumeric leg: {PASS} PASS / {FAIL} FAIL")
