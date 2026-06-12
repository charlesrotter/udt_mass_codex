"""BLIND VERIFIER — N1 claim B4: saturation landscape, M2 m=0 paths.

My own re-implementation: own FD mode (B-normalized), own GL quadrature
for P(X) = (1/8) Int (1-u^2) f_u^2/f du, own path assembly
  E(a) = sum wq e^{-t} [ (1/4)|Xt + a u'|^2 + P(X + a u) ]
  dE(a) = E(a) - lin*a + (1/4)(u0.Mo.u0) a^2 - E(0)
Recorded (corrected run): a<0: corner f_min=0.012 at a=-0.432,
located (t,u)=(0.13,+1) [weld-side pole], dE=+0.353 rising, no turning
point, T(path)=2.0 (~5.3 e-folds). a>0: no corner by a=60, kappa falls.
"""
import numpy as np, pickle
import scipy.sparse as spr
import scipy.sparse.linalg as sla

C = pickle.load(open('/tmp/nonstat_n1/cache.pkl', 'rb'))
meta, CF, MOUTC, fine = C['meta'], C['CF'], C['MOUT'], C['fine']
VH = np.array([1.0, np.sqrt(3), np.sqrt(5), np.sqrt(7)])/4.0
S3, S5, S7 = np.sqrt(3.0), np.sqrt(5.0), np.sqrt(7.0)

PASS, FAIL = [], []
def check(label, ok, detail=""):
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label, detail, flush=True)

# ---- my own harmonics + GL quadrature ----
NGL = 1000
ux, wgl = np.polynomial.legendre.leggauss(NGL)
Y = np.array([np.ones_like(ux), S3*ux, (S5/2)*(3*ux**2 - 1),
              (S7/2)*(5*ux**3 - 3*ux)])
Yp = np.array([np.zeros_like(ux), S3*np.ones_like(ux), 3*S5*ux,
               (S7/2)*(15*ux**2 - 3)])
s2 = 1 - ux**2
# orthonormality sanity
M = 0.5*(Y*wgl) @ Y.T
assert np.allclose(M, np.eye(4), atol=1e-12)

def P_of(X):
    f = X @ Y; fu = X @ Yp
    fc = np.maximum(f, 1e-300)
    return (wgl @ (s2*fu**2/fc))/8.0

def gradP(X):
    f = X @ Y; fu = X @ Yp
    fc = np.maximum(f, 1e-300)
    return (s2*(2*fu*Yp/fc - fu**2*Y/fc**2)) @ wgl/8.0

def fmin_of(X, ugrid=np.linspace(-1, 1, 4001)):
    Yg = np.array([np.ones_like(ugrid), S3*ugrid, (S5/2)*(3*ugrid**2-1),
                   (S7/2)*(5*ugrid**3 - 3*ugrid)])
    f = X @ Yg
    i = np.argmin(f)
    return f[i], ugrid[i]

# ---- my own mode (FD solver from v_b1 logic) ----
def interp_mat(tq, tg, Mm):
    out = np.empty((len(tq),) + Mm.shape[1:])
    for idx in np.ndindex(Mm.shape[1:]):
        out[(slice(None),)+idx] = np.interp(tq, tg, Mm[(slice(None),)+idx])
    return out

def mode_mine(tag, mm=0, n=1600):
    cf = CF[(tag, mm)]
    d = cf['d']; tb = meta[tag]['t1pc']
    t = np.linspace(0.0, tb, n+1); h = t[1]-t[0]
    tm = 0.5*(t[:-1]+t[1:]); pm = np.exp(-tm)
    Hn = interp_mat(t, cf['t'], cf['H']); Gn = interp_mat(t, cf['t'], cf['GA'])
    wn = np.exp(-3*t); pn = np.exp(-t)
    ndof = (n+1)*d
    rows, cols, vals, brow, bcol, bval = [], [], [], [], [], []
    def add(i, j, Mm, r, c, v):
        for a in range(d):
            for b in range(d):
                if Mm[a, b] != 0.0:
                    r.append(i*d+a); c.append(j*d+b); v.append(Mm[a, b])
    I = np.eye(d)
    for i in range(n+1):
        cell = h if 0 < i < n else h/2
        add(i, i, 2*pn[i]*Hn[i]*cell, rows, cols, vals)
        add(i, i, wn[i]*Gn[i]*cell, brow, bcol, bval)
    for e in range(n):
        ke = pm[e]/h*I
        add(e, e, ke, rows, cols, vals); add(e+1, e+1, ke, rows, cols, vals)
        add(e, e+1, -ke, rows, cols, vals); add(e+1, e, -ke, rows, cols, vals)
    add(0, 0, MOUTC[tag][mm]['scr'], rows, cols, vals)
    K = spr.coo_matrix((vals, (rows, cols)), shape=(ndof, ndof)).tocsc()
    B = spr.coo_matrix((bval, (brow, bcol)), shape=(ndof, ndof)).tocsc()
    T = spr.identity(ndof, format='lil'); last = n*d
    Wc = np.linalg.qr(np.column_stack([VH, np.eye(4)[:, :3]]))[0]
    R4 = np.column_stack([VH, Wc[:, 1:]])
    T[last:last+d, last:last+d] = R4; T = T.tocsc()
    K = (T.T @ K @ T).tocsc(); B2 = (T.T @ B @ T).tocsc()
    keep = np.setdiff1d(np.arange(ndof), [last])
    Kk = K[np.ix_(keep, keep)].tocsc(); Bk = B2[np.ix_(keep, keep)].tocsc()
    Kk = (Kk + Kk.T)/2
    w, V = sla.eigsh(Kk, k=2, M=Bk, sigma=-2.0, which='LM')
    o = np.argsort(w); w = w[o]; V = V[:, o]
    full = np.zeros(ndof); full[keep] = V[:, 0]
    full = np.asarray((T @ full)).ravel()
    u = full.reshape(n+1, d)
    if u[n//2] @ VH < 0:
        u = -u
    return w[0], u, t

sig, u, t = mode_mine('M2')
print(f"    my M2 m=0 sigma_1 = {sig:.5f} (rec 7.1344)")
h = t[1]-t[0]
wq = np.full(len(t), h); wq[0] *= 0.5; wq[-1] *= 0.5
ft = fine['M2']['t']
X = np.array([np.interp(t, ft, fine['M2']['X'][:, j]) for j in range(4)]).T
Xt = np.array([np.interp(t, ft, fine['M2']['Xt'][:, j]) for j in range(4)]).T
du = np.gradient(u, t, axis=0)
Mo = MOUTC['M2'][0]['scr']
bnd = 0.25*(u[0] @ Mo @ u[0])

def E_K_fmin(a):
    Xa = X + a*u; Xta = Xt + a*du
    E = K = 0.0
    fmins = np.empty(len(t)); umins = np.empty(len(t))
    for i in range(len(t)):
        E += wq[i]*np.exp(-t[i])*(0.25*(Xta[i] @ Xta[i]) + P_of(Xa[i]))
        fpath = np.maximum(Xa[i] @ Y, 1e-9)
        upath = u[i] @ Y
        K += wq[i]*np.exp(-3*t[i])*0.5*(wgl @ (upath**2/fpath**2))/4.0
        fmins[i], umins[i] = fmin_of(Xa[i])
    i0 = np.argmin(fmins)
    return E, K, fmins[i0], t[i0], umins[i0]

E0 = E_K_fmin(0.0)[0]
lin = sum(wq[i]*np.exp(-t[i])*(0.5*(Xt[i] @ du[i]) + gradP(X[i]) @ u[i])
          for i in range(len(t)))
# consistency: E''(0) == sigma/2 (B-norm = 1)
hh = 0.01
Ep = E_K_fmin(+hh)[0]; Em = E_K_fmin(-hh)[0]
Epp = (Ep - 2*E0 + Em)/hh**2 + 2*bnd
check("B4-0 quadratic consistency E''(0) (incl. boundary) == sigma/2",
      abs(Epp/(sig/2) - 1) < 0.02, f"E''={Epp:.4f} vs sigma/2={sig/2:.4f}")
K0 = E_K_fmin(0.0)[1]
check("B4-0b K(0) == 1/4 (B-normalized mode)", abs(K0 - 0.25) < 0.005,
      f"K0={K0:.5f}")

# ---- a < 0 deepening path ----
print("\n    a<0 path:")
tr = []
a = 0.0
hit = False
while a > -60:
    da = -min(0.4, max(0.02, abs(a)*0.12))
    E, K, fm, tmin, umin = E_K_fmin(a + da)
    if fm < 0.012:
        lo, hi = a, a + da
        for _ in range(40):
            mid = 0.5*(lo + hi)
            if E_K_fmin(mid)[2] > 0.012:
                lo = mid
            else:
                hi = mid
        a = lo
        E, K, fm, tmin, umin = E_K_fmin(a)
        tr.append((a, E - lin*a + bnd*a*a - E0, K, fm, tmin, umin))
        hit = True
        break
    a += da
    tr.append((a, E - lin*a + bnd*a*a - E0, K, fm, tmin, umin))
aa = np.array([x[0] for x in tr]); dE = np.array([x[1] for x in tr])
KK = np.array([x[2] for x in tr])
turned = bool(np.any(dE < -1e-9))
mono = bool(np.all(np.diff(dE) > 0))
Tt = abs(np.trapezoid(np.sqrt(KK/np.maximum(dE, 1e-12)), aa))
print(f"    corner: {hit} at a={aa[-1]:+.3f} (rec -0.432); f_min "
      f"{tr[-1][3]:.4f} at t={tr[-1][4]:.3f} (rec 0.13), u={tr[-1][5]:+.2f}"
      f" (rec +1); dE_end {dE[-1]:+.4f} (rec +0.353); turned {turned}; "
      f"T(path) {Tt:.3f} (rec 2.00; {Tt*np.sqrt(sig):.1f} e-folds)")
check("B4-1 a<0: corner (f->0) at finite a ~ -0.43, at the WELD-side "
      "pole (t ~ 0.13, u = +1), E rising monotone, NO turning point, "
      "finite path time", hit and (not turned) and mono
      and abs(aa[-1] + 0.432) < 0.03 and abs(tr[-1][4] - 0.13) < 0.04
      and tr[-1][5] > 0.97 and abs(dE[-1] - 0.353) < 0.04
      and abs(Tt - 2.0) < 0.15)

# ---- a > 0 inflation direction (shorter scan, to a=20) ----
print("\n    a>0 path (to a=20):")
avals = [0.5, 2.0, 5.0, 10.0, 20.0]
dEs = []; fms = []
for av in avals:
    E, K, fm, tmin, umin = E_K_fmin(av)
    dEs.append(E - lin*av + bnd*av*av - E0); fms.append(fm)
kap0 = S3*abs(X[-1, 1])/X[-1, 0]
Xe = X + 20.0*u
kape = S3*abs(Xe[-1, 1])/Xe[-1, 0]
print(f"    dE: {[f'{v:+.2f}' for v in dEs]}; f_min: "
      f"{[f'{v:.2f}' for v in fms]}; kappa(tb) {kap0:.3f} -> {kape:.3f}")
check("B4-2 a>0: no corner (f_min rising), dE rising (no turning "
      "point), kappa decreasing (spheroidalizing inflation escape)",
      all(np.diff(dEs) > 0) and all(np.diff(fms) > 0) and fms[0] > 0.012
      and kape < kap0)

print()
print("PASS", len(PASS), "FAIL", len(FAIL))
if FAIL:
    print("FAILED:", FAIL)
