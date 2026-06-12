"""BLIND VERIFIER — N1 claim B2: exterior continuation.

(i)  SYMBOLIC: chi = y^{-1/6} K_nu(6 sqrt(lam) y^{1/6}) solves
     (y^{4/3} chi')' = y^{4/3} [lam y^{-5/3} + mu2/y^2] chi,
     mu2 = (nu^2 - 1)/36  — my own sympy check.
(ii) D(sigma=0) = -chi'(1)/chi(1) equals the cached static M_out
     diagonal (data: gamma + D_+(l)) to 1e-12 — mpmath, my own code.
(iii) unwalled sigma>0: Liouville-Green exponents (own integration).
(iv) walled fixed point sigma = sigma_min[interior(M_out(sigma))] for
     M1 m=0, wall-Dirichlet at y_w = 2.746 — my own interior FD solver
     + my own exterior integration. Recorded: [1.3199 5.3744 12.0669].
"""
import numpy as np, pickle
import sympy as sp
import mpmath as mp
import scipy.sparse as spr
import scipy.sparse.linalg as sla
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

mp.mp.dps = 40
PASS, FAIL = [], []
def check(label, ok, detail=""):
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label, detail, flush=True)

# ---------- (i) closed form solves the ODE ----------
y, lam, nu = sp.symbols('y lambda nu', positive=True)
mu2 = (nu**2 - 1)/36
chi = y**sp.Rational(-1, 6)*sp.besselk(nu, 6*sp.sqrt(lam)*y**sp.Rational(1, 6))
res = sp.diff(y**sp.Rational(4, 3)*sp.diff(chi, y), y) \
    - y**sp.Rational(4, 3)*(lam/y**sp.Rational(5, 3) + mu2/y**2)*chi
check("B2-i  y^{-1/6} K_nu(6 sqrt(lam) y^{1/6}) solves the exterior "
      "channel ODE (sigma=0) EXACTLY", sp.simplify(res) == 0)

# ---------- (ii) D at sigma=0 vs cached static M_out ----------
C = pickle.load(open('/tmp/nonstat_n1/cache.pkl', 'rb'))
meta, CF, MOUTC = C['meta'], C['CF'], C['MOUT']
VH = np.array([1.0, np.sqrt(3), np.sqrt(5), np.sqrt(7)])/4.0
NU_S = 3.0
def D_closed(lam_v, nu_v):
    if lam_v == 0:
        return float((1 + mp.mpf(nu_v))/6)
    t0 = 6*mp.sqrt(lam_v)
    K = mp.besselk(nu_v, t0)
    dK = mp.diff(lambda z: mp.besselk(nu_v, z), t0)
    # chi'(1) = -1/6 chi(1) + sqrt(lam) dK; D = -chi'/chi
    return float(mp.mpf(1)/6 - mp.sqrt(lam_v)*dK/K)
gam = meta['M1']['gamma']
Msc = MOUTC['M1'][0]['scr']
errs = []
for l in range(4):
    Dv = D_closed(l*(l+1), NU_S)
    errs.append(abs(gam + Dv - Msc[l, l]))
    print(f"    l={l}: my D_+ {Dv:.10f}; cached diag - gamma "
          f"{Msc[l, l]-gam:.10f}")
check("B2-ii my closed-form D_+ == cached static M_out diagonal "
      "(<= 1e-9)", max(errs) < 1e-9, f"max {max(errs):.1e}")
# and the inward integration reproduces it (the D_+ anchor, my code):
def ext_rhs(lam_v, mu2v, sig):
    def rhs(yv, z):
        chi_, dchi = z
        return [dchi, -(4/3)*dchi/yv + (lam_v*yv**(-5/3) + mu2v/yv**2
                                        - sig*yv**(2/3))*chi_]
    return rhs
errs2 = []
for lv in (2.0, 6.0, 12.0):
    yb = 80.0
    f0 = float(yb**(-1/6)*mp.besselk(3, 6*mp.sqrt(lv)*yb**(1/6)))
    d0 = float(mp.diff(lambda t: t**(-mp.mpf(1)/6)
                       * mp.besselk(3, 6*mp.sqrt(lv)*t**(mp.mpf(1)/6)), yb))
    sol = solve_ivp(ext_rhs(lv, (9-1)/36, 0.0), (yb, 1.0), [f0, d0],
                    method='DOP853', rtol=1e-12, atol=1e-300)
    Dnum = -sol.y[1, -1]/sol.y[0, -1]
    errs2.append(abs(Dnum - D_closed(lv, 3.0)))
check("B2-ii' inward integration of MY ODE reproduces closed-form D_+ "
      "(<= 1e-10; recorded claim 1e-13 at their settings)",
      max(errs2) < 1e-10, f"max {max(errs2):.1e}")

# ---------- (iii) unwalled sigma > 0: LG exponents ----------
sig = 7.057579
sol = solve_ivp(ext_rhs(0.0, 2/9, sig), (1.0, 3000.0), [1.0, 0.0],
                method='DOP853', rtol=1e-10, atol=1e-12, dense_output=True)
ys = np.geomspace(60, 2900, 3000)
ch = sol.sol(ys)[0]
loc = [i for i in range(1, len(ys)-1)
       if abs(ch[i]) >= abs(ch[i-1]) and abs(ch[i]) >= abs(ch[i+1])]
p = np.polyfit(np.log(ys[loc]), np.log(np.abs(ch[loc])), 1)[0]
nz = int(np.sum(np.sign(ch[1:]) != np.sign(ch[:-1])))
check("B2-iii unwalled sigma>0: oscillatory with envelope ~ y^{-5/6} "
      "(no finite-action eigenmode; continuum)", abs(p + 5/6) < 0.06
      and nz > 500, f"envelope {p:+.3f}, zeros {nz}")

# ---------- (iv) walled fixed point, M1 m=0, wall-D ----------
def interp_mat(tq, tg, M):
    out = np.empty((len(tq),) + M.shape[1:])
    for idx in np.ndindex(M.shape[1:]):
        out[(slice(None),) + idx] = np.interp(tq, tg, M[(slice(None),)+idx])
    return out

def interior_min(tag, mm, Mout, n=900):
    cf = CF[(tag, mm)]
    d = cf['d']; tb = meta[tag]['t1pc']
    t = np.linspace(0.0, tb, n + 1); h = t[1]-t[0]
    tm = 0.5*(t[:-1]+t[1:]); pm = np.exp(-tm)
    Hn = interp_mat(t, cf['t'], cf['H'])
    Gn = interp_mat(t, cf['t'], cf['GA'])
    wn = np.exp(-3*t); pn = np.exp(-t)
    ndof = (n+1)*d
    rows, cols, vals, brow, bcol, bval = [], [], [], [], [], []
    def add(i, j, M, r, c, v):
        for a in range(d):
            for b in range(d):
                if M[a, b] != 0.0:
                    r.append(i*d+a); c.append(j*d+b); v.append(M[a, b])
    I = np.eye(d)
    for i in range(n+1):
        cell = h if 0 < i < n else h/2
        add(i, i, 2*pn[i]*Hn[i]*cell, rows, cols, vals)
        add(i, i, wn[i]*Gn[i]*cell, brow, bcol, bval)
    for e in range(n):
        ke = pm[e]/h*I
        add(e, e, ke, rows, cols, vals); add(e+1, e+1, ke, rows, cols, vals)
        add(e, e+1, -ke, rows, cols, vals); add(e+1, e, -ke, rows, cols, vals)
    add(0, 0, Mout, rows, cols, vals)
    K = spr.coo_matrix((vals, (rows, cols)), shape=(ndof, ndof)).tocsc()
    B = spr.coo_matrix((bval, (brow, bcol)), shape=(ndof, ndof)).tocsc()
    T = spr.identity(ndof, format='lil'); last = n*d
    Wc = np.linalg.qr(np.column_stack([VH, np.eye(d)[:, :d-1]]))[0]
    R4 = np.column_stack([VH, Wc[:, 1:]])
    T[last:last+d, last:last+d] = R4; T = T.tocsc()
    K = (T.T @ K @ T).tocsc(); B = (T.T @ B @ T).tocsc()
    keep = np.setdiff1d(np.arange(ndof), [last])
    K = K[np.ix_(keep, keep)].tocsc(); B = B[np.ix_(keep, keep)].tocsc()
    K = (K + K.T)/2
    w = sla.eigsh(K, k=1, M=B, sigma=-2.0, which='LM',
                  return_eigenvectors=False)
    return w[0]

def D_wall(lam_v, sig_v, yw, bc='D'):
    z0 = [0.0, 1.0] if bc == 'D' else [1.0, 0.0]
    sol = solve_ivp(ext_rhs(lam_v, 2/9, sig_v), (yw, 1.0), z0,
                    method='DOP853', rtol=1e-11, atol=1e-13)
    return -sol.y[1, -1]/sol.y[0, -1]

tag, mm, yw = 'M1', 0, 2.746
m = meta[tag]
ls = [0, 1, 2, 3]
Msc = MOUTC[tag][mm]['scr']
Dst = np.array([D_closed(l*(l+1), 3.0) for l in ls])
Cg = (np.diag(m['gamma'] + Dst) - Msc)/m['c']
def mout_sig(sig_v):
    Dw = np.array([D_wall(l*(l+1), sig_v, yw, 'D') for l in ls])
    M_ = np.diag(m['gamma'] + Dw) - m['c']*Cg
    return 0.5*(M_ + M_.T)
def gfun(sig_v):
    return interior_min(tag, mm, mout_sig(sig_v)) - sig_v
sgrid = np.geomspace(0.05, 22.0, 34)
gv = np.array([gfun(s_) for s_ in sgrid])
roots = []
for i in range(len(sgrid)-1):
    a_, b_ = gv[i], gv[i+1]
    if np.isfinite(a_) and np.isfinite(b_) and a_*b_ < 0 \
       and abs(a_) < 40 and abs(b_) < 40:
        try:
            roots.append(brentq(gfun, sgrid[i], sgrid[i+1], xtol=1e-7))
        except Exception:
            pass
print("    my composite fixed points (M1 m=0 wall-D):",
      [f"{r:.4f}" for r in roots])
rec = [1.3199, 5.3744, 12.0669]
match = [min(abs(r - x)/x for r in roots) if roots else 9 for x in rec]
check("B2-iv composite walled fixed points exist (growth survives) and "
      "match recorded [1.3199 5.3744 12.0669] (<= 2%)",
      len(roots) >= 3 and max(match) < 0.02,
      f"rel devs {['%.1e' % v for v in match]}")
klow = np.sqrt(min(roots)) if roots else np.nan
print(f"    lowest composite rate k = {klow:.4f} (recorded 0.3641... "
      "wait: 1.3199 -> k = 1.1489; recorded k_comp lowest over D/N was "
      "0.3641 from wall-N)")

print()
print("PASS", len(PASS), "FAIL", len(FAIL))
if FAIL:
    print("FAILED:", FAIL)
