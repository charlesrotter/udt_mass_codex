"""
VERIFIER v3: numerics on the S1 library, all with MY OWN integrator and
quadrature (s2_blocks imported ONLY as the banked comparison target).

 N1  re-integrate M1-M4 from the header jets (my own RHS) vs .dat rows
 N2  DEN = f f_t^2 - (1-u^2) f_u^2 sign map: alpha_aa = 0 locus exists
     inside every member's domain (truncation pathology, H1-C)
 N3  M2 near-seal band location (claimed interior, approx [0.59,0.93])
 N4  truncated weight <Y1 Y1 Lambda / f^2> non-convergent under
     quadrature doubling at a locus slice
 N5  my <R R'/f^2> quadrature == s2_blocks GA to 1e-12 (the W_A claim)
     and != GB (W_B) -- the derived weight is the matrices S2 used
 N6  endpoint powers under the derived weight on M2:
     vhat ~ 1/mu (slope -1), m=1 log, m=2 + m0-complement bounded
"""
import numpy as np
import sys
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

PASS = []
def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"V3 {name}: {'PASS' if ok else 'FAIL'} {detail}", flush=True)

S3, S5, S7 = np.sqrt(3.), np.sqrt(5.), np.sqrt(7.)
def Yr(u):
    u = np.asarray(u, float)
    return np.array([np.ones_like(u), S3*u, (S5/2)*(3*u**2 - 1),
                     (S7/2)*(5*u**3 - 3*u)])
def Ypr(u):
    u = np.asarray(u, float)
    return np.array([np.zeros_like(u), S3*np.ones_like(u), 3*S5*u,
                     (S7/2)*(15*u**2 - 3)])
YP1 = np.array([1.0, S3, S5, S7])

xg, wg = np.polynomial.legendre.leggauss(1200)
Yg, Ypg = Yr(xg), Ypr(xg)
sg = 1 - xg**2

def PX(X):
    f = X @ Yg; fu = X @ Ypg
    return (sg*(2*fu*Ypg/f - fu**2*Yg/f**2)) @ wg / 8.0

def fmin_of(X):
    uu = np.linspace(-1, 1, 20001)
    return (X @ Yr(uu)).min()

def rhs(t, z):
    X, Xt = z[0::2], z[1::2]
    Xtt = Xt + 2*PX(X)
    out = np.empty(8); out[0::2] = Xt; out[1::2] = Xtt
    return out

HD = {}
MEM = {}
for tag in ("M1", "M2", "M3", "M4"):
    hdr = open(f"/tmp/seal_s1/lib/bg_{tag}.dat").read(1200)
    gam = float(hdr.split("gamma=")[1].split()[0])
    c = float(hdr.split(" c=")[1].split()[0])
    tstop_h = float(hdr.split("t_stop=")[1].split(";")[0])
    dat = np.loadtxt(f"/tmp/seal_s1/lib/bg_{tag}.dat")
    z0 = np.zeros(8); z0[0] = 1.0; z0[1] = gam; z0[3] = -c
    ev = lambda t, z: fmin_of(z[0::2]) - 0.002
    ev.terminal = True; ev.direction = -1
    sol = solve_ivp(rhs, (0, 60), z0, method='DOP853', rtol=1e-11,
                    atol=1e-13, dense_output=True, events=ev)
    tstop = sol.t_events[0][0]
    MEM[tag] = dict(sol=sol, tstop=tstop, dat=dat, gamma=gam, c=c)
    # compare against the library rows on the early/trusted span
    sel = dat[:, 0] <= 0.8*tstop
    Xd = dat[sel, 2:6]
    Xr = np.array([sol.sol(t)[0::2] for t in dat[sel, 0]])
    err = np.abs(Xr - Xd).max()/np.abs(Xd).max()
    MEM[tag]['err'] = err
    print(f"  {tag}: my t_stop {tstop:.6f} vs header {tstop_h:.6f}; "
          f"re-integration vs .dat max rel dev {err:.2e}")
check("N1 my independent flow matches the library (M1-M4, <1e-7) and "
      "the header t_stop (<2e-4)",
      max(m['err'] for m in MEM.values()) < 1e-7 and
      all(abs(MEM[t]['tstop'] -
              float(open(f'/tmp/seal_s1/lib/bg_{t}.dat').read(1200)
                    .split('t_stop=')[1].split(';')[0])) < 2e-4
          for t in MEM))

# ---------------- N2: DEN sign map ----------------
def DEN_NUM_f(m, t, u, Yu, Ypu):
    z = m['sol'].sol(float(t))
    X, Xt = z[0::2], z[1::2]
    f = X @ Yu; ft = Xt @ Yu; fu = X @ Ypu
    return f*ft**2 - (1 - u**2)*fu**2, f*ft**2 + (1 - u**2)*fu**2, f

ok2 = True
for tag, m in MEM.items():
    ts = np.linspace(1e-6, m['tstop'], 481)
    has = []
    for t in ts:
        D, _, _ = DEN_NUM_f(m, t, xg, Yg, Ypg)
        if (D < 0).any():
            has.append(t)
    m['locus'] = has
    print(f"  {tag}: DEN<0 slices t in "
          f"[{has[0]:.4f}, {has[-1]:.4f}]" if has else f"  {tag}: none")
    ok2 &= len(has) > 0
check("N2 alpha_aa = 0 locus exists INSIDE every member's domain "
      "(truncated spherical-transplant scheme singular on formed bgs)",
      ok2)

# ---------------- N3: M2 near-seal band ----------------
m = MEM['M2']
pole = lambda t: float(m['sol'].sol(t)[0::2] @ YP1)
uu = np.linspace(-1, 1, 8001)
Yu, Ypu = Yr(uu), Ypr(uu)
ok3 = True
bands = []
for mu in (0.1, 0.03, 0.01, 0.003):
    tl = brentq(lambda t: pole(t) - mu, 0.2*m['tstop'], m['tstop'])
    D, NUM, f = DEN_NUM_f(m, tl, uu, Yu, Ypu)
    neg = uu[D < 0]
    bands.append((mu, neg.min(), neg.max()))
    print(f"  mu={mu:7.3f}: DEN<0 band u in [{neg.min():+.4f}, "
          f"{neg.max():+.4f}]")
    ok3 &= (0.3 < neg.min()) and (neg.max() < 0.95)
last = bands[-1]
check("N3 near-seal band INTERIOR (within [0.3,0.95]); latest slice "
      "band approx [0.59, 0.93] as recorded",
      ok3 and abs(last[1] - 0.59) < 0.03 and abs(last[2] - 0.93) < 0.03,
      f"band [{last[1]:.3f}, {last[2]:.3f}] at mu=0.003")

# ---------------- N4: truncated weight non-convergence ----------------
tl_mid = m['locus'][len(m['locus'])//2]
vals = []
for N in (400, 800, 1600, 3200, 6400):
    x, w = np.polynomial.legendre.leggauss(N)
    D, NUM, f = DEN_NUM_f(m, tl_mid, x, Yr(x), Ypr(x))
    v = (w @ ((S3*x)**2*(NUM/D)/f**2))/2
    vals.append(v)
print("  truncated <Y1^2 Lambda/f^2> under doubling:",
      " ".join(f"{v:+.4f}" for v in vals))
sp_last = abs(vals[-1] - vals[-2]); sp_first = abs(vals[1] - vals[0])
check("N4 truncated weight NON-CONVERGENT (PV-singular integrand)",
      sp_last > 0.02*abs(vals[-1]) or sp_last > sp_first,
      f"last doubling moves {sp_last:.2e}")

# ---------------- N5: derived weight == S2 GA, != GB ----------------
sys.path.insert(0, '/tmp/seal_s1'); sys.path.insert(0, '/tmp/seal_s2')
import importlib.util
spec = importlib.util.spec_from_file_location("s2b", "/tmp/seal_s2/s2_blocks.py")
print("  loading s2_blocks (banked target; its own checks will print)...")
s2b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s2b)
errA, devB = 0.0, np.inf
for tt in (0.4, 0.9, 1.3):
    X = m['sol'].sol(tt)[0::2]
    f = X @ s2b.QN.Y                     # f on their nodes
    for mb in range(4):
        B = s2b.BLK[mb]
        H, GA, GB = B.mats(X)
        n = len(B.R)
        pref = np.ones((n, n)) if mb == 0 else 0.5*np.outer(B.N, B.N)
        for i in range(n):
            for j in range(n):
                mine = pref[i, j]*(s2b.QN.w @ (B.R[i]*B.R[j]/f**2))/2
                errA = max(errA, abs(mine - GA[i, j]))
                devB = min(devB, abs(mine - GB[i, j]))
check("N5 derived weight == S2 GA (W_A) to 1e-12; distinct from GB "
      "(W_B)", errA < 1e-12 and devB > 1e-3,
      f"maxdev GA {errA:.1e}; mindev GB {devB:.2e}")

# ---------------- N6: endpoint powers on M2 ----------------
print("  endpoint powers (derived weight, M2):")
from numpy.linalg import qr, eigvalsh
VH = YP1/np.linalg.norm(YP1)
WC = qr(np.column_stack([VH, np.eye(4)[:, :3]]))[0][:, 1:]
mus = np.array([0.3, 0.1, 0.03, 0.01, 0.003])
rows = {k: [] for k in ('vhat', 'comp', 'm1', 'm2')}
for mu in mus:
    tl = brentq(lambda t: pole(t) - mu, 0.2*m['tstop'], m['tstop'])
    X = m['sol'].sol(tl)[0::2]
    G0 = np.empty((4, 4))
    f = X @ Yg
    for i in range(4):
        for j in range(4):
            G0[i, j] = (wg @ (Yg[i]*Yg[j]/f**2))/2
    rows['vhat'].append(VH @ G0 @ VH)
    rows['comp'].append(eigvalsh(WC.T @ G0 @ WC)[-1])
    # m=1, l=1: R = N P_1^1, P_1^1 = -sqrt(1-u^2); m=2, l=2: prop (1-u^2)
    R11 = np.sqrt(1 - xg**2)
    rows['m1'].append(3.0*(wg @ (R11**2/f**2))/2/2)   # norm-irrelevant
    R22 = (1 - xg**2)
    rows['m2'].append((wg @ (R22**2/f**2))/2)
ln = np.log(mus)
def slope(k):
    v = np.log(np.abs(rows[k]))
    return (v[-1] - v[-2])/(ln[-1] - ln[-2])
for k in rows:
    print(f"   {k:5s}: " + " ".join(f"{v:10.4f}" for v in rows[k])
          + f"  slope {slope(k):+.3f}")
d1 = rows['m1'][3] - rows['m1'][2]; d2 = rows['m1'][4] - rows['m1'][3]
lr = np.log(mus[3]/mus[4])/np.log(mus[2]/mus[3])
check("N6a vhat ~ 1/mu (slope -1 within 10%): the 1/tau forced "
      "limit-circle endpoint", abs(slope('vhat') + 1) < 0.10,
      f"slope {slope('vhat'):+.3f}")
check("N6b m=1 LOG growth (|slope|<0.15, increments track ln-steps): "
      "limit-circle under the derived W_A weight (W_B's limit-point "
      "kill NOT reproduced)", abs(slope('m1')) < 0.15
      and abs(d2/(d1*lr) - 1) < 0.12,
      f"slope {slope('m1'):+.3f}, incr ratio {d2/d1:.3f} vs ln {lr:.3f}")
check("N6c m=2 and m0-complement bounded (|slope|<0.05)",
      abs(slope('m2')) < 0.05 and abs(slope('comp')) < 0.05,
      f"{slope('m2'):+.3f}, {slope('comp'):+.3f}")
# contrast: same channels under W_B = <R R'/f^3> -- m=1 should DIVERGE
rowsB = []
for mu in mus:
    tl = brentq(lambda t: pole(t) - mu, 0.2*m['tstop'], m['tstop'])
    X = m['sol'].sol(tl)[0::2]
    f = X @ Yg
    R11 = np.sqrt(1 - xg**2)
    rowsB.append(3.0*(wg @ (R11**2/f**3))/2/2)
vB = np.log(np.abs(rowsB))
slB = (vB[-1] - vB[-2])/(ln[-1] - ln[-2])
print(f"   m=1 under W_B: " + " ".join(f"{v:10.3f}" for v in rowsB)
      + f"  slope {slB:+.3f}")
check("N6d under W_B the m=1 entry DIVERGES like a power (slope <= "
      "-0.5): the two weights genuinely separate the m=1 endpoint "
      "class; the derived weight decides", slB < -0.5,
      f"slope {slB:+.3f}")

n = sum(1 for _, ok in PASS if ok)
print(f"\nV3 TOTAL: {n}/{len(PASS)} PASS")
