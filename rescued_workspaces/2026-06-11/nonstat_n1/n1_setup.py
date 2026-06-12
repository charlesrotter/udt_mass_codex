"""
NONSTATIONARY SECTOR, AGENT N1 -- script 1: SPOT-VALIDATION + CACHE.

Reuse license per task: re-import the verified S2 stack (s2_blocks runs
its own B1-B8 battery on import: backgrounds re-integrated from S1
header jets, Hessian vs banked P_hess, m=1 vs S1 Mlm x2 amendment, PSD
theorem scan, smooth-collar weld anchor, G PD, M_out PSD, quadrature
doubling), then:
  N1-S1  my own vector-P1 FEM (independent assembly, returns
         eigenVECTORS) reproduces the recorded production ladders
         (results_main.pkl 'ladder', 4 rungs x 4 blocks x M1/M2/M4)
  N1-S2  shooting refinement reproduces the .md headline value
         sigma(M1,m=0,rung1) = 7.057579
  N1-S3  eigenvector sanity: u^T A u / u^T B u == sigma
Then dump a self-contained cache (coefficient tables, backgrounds,
M_out, modes) for the downstream N1 scripts.
Conventions: s2_anchors.py frozen header. omega^2 = -sigma; under the
same-minus dynamics (ensembles record) sigma > 0 modes evolve as
exp(+-sqrt(sigma) T): GROWTH RATE = sqrt(sigma) in weld-time units.
"""
import numpy as np, pickle, sys, time
import scipy.linalg as sla
sys.path.insert(0, '/tmp/seal_s1'); sys.path.insert(0, '/tmp/seal_s2')

PASSN = []
def checkN(name, ok, detail=""):
    PASSN.append((name, bool(ok)))
    print(f"CHECK {name}: {'PASS' if ok else 'FAIL'} {detail}")

t0 = time.time()
print("=== importing verified S2 stack (runs S2's own B-battery) ===")
from s2_blocks import MEM, BLK, LBLK, Xof, MOUT, PASS as PASS_S2
from s2_solve import coeffs   # verified coefficient tables (481-pt)
nS2 = sum(1 for _, ok in PASS_S2 if ok)
checkN("N1-S0 S2 block battery re-ran clean on import",
       nS2 == len(PASS_S2), f"{nS2}/{len(PASS_S2)}; wall {time.time()-t0:.0f}s")

VH = np.array([1.0, np.sqrt(3), np.sqrt(5), np.sqrt(7)])/4.0
WC = sla.qr(np.column_stack([VH, np.eye(4)[:, :3]]))[0][:, 1:]

# ---------------- my own vector-P1 FEM with eigenvectors ----------------
def fem_vec(tag, mm, tb, h_in, Mout, N=400, nev=8, neumann0=False):
    """independent assembly (same weak form as S2's, written fresh);
    returns (sigmas, modes) with modes[k] = (N+1, d) nodal values in the
    ORIGINAL channel basis, B-normalized."""
    cf = coeffs(tag, mm); d = cf.d
    s = np.linspace(0.0, tb, N + 1)
    ndof = (N + 1)*d
    K = np.zeros((ndof, ndof)); B = np.zeros((ndof, ndof))
    for e in range(N):
        he = s[e+1] - s[e]; tm = 0.5*(s[e] + s[e+1])
        Hm, Gm = cf.at(tm, 'A')
        pm = np.exp(-tm); qm = 2*np.exp(-tm)*Hm; wm = np.exp(-3*tm)*Gm
        i0 = e*d
        I = np.eye(d)
        Ke = np.zeros((2*d, 2*d)); Be = np.zeros((2*d, 2*d))
        Ke[:d, :d] += pm/he*I + qm*he/3; Ke[d:, d:] += pm/he*I + qm*he/3
        Ke[:d, d:] += -pm/he*I + qm*he/6; Ke[d:, :d] += -pm/he*I + qm*he/6
        Be[:d, :d] += wm*he/3; Be[d:, d:] += wm*he/3
        Be[:d, d:] += wm*he/6; Be[d:, :d] += wm*he/6
        K[i0:i0+2*d, i0:i0+2*d] += Ke; B[i0:i0+2*d, i0:i0+2*d] += Be
    if not neumann0:
        K[:d, :d] += Mout          # weld Robin (natural)
    last = N*d
    drop = []
    Tm = np.eye(ndof)
    if mm == 0:
        R4 = np.column_stack([VH, WC])
        Tm[last:last+d, last:last+d] = R4
        K = Tm.T @ K @ Tm; B = Tm.T @ B @ Tm
        drop = [last]              # forced vhat Dirichlet at the stand-in
        K[last+1:last+d, last+1:last+d] += -np.exp(-tb)*h_in*np.eye(d-1)
    else:
        K[last:last+d, last:last+d] += -np.exp(-tb)*h_in*np.eye(d)
    keep = np.setdiff1d(np.arange(ndof), drop)
    K = 0.5*(K + K.T)
    w, V = sla.eigh(K[np.ix_(keep, keep)], B[np.ix_(keep, keep)],
                    subset_by_index=[0, nev-1])
    modes = []
    for k in range(nev):
        full = np.zeros(ndof); full[keep] = V[:, k]
        full = Tm @ full           # back to original channel basis
        u = full.reshape(N+1, d)
        # sign convention: positive vhat-projected value at midpoint
        mid = u[N//2] @ (VH if mm == 0 else np.ones(d)/np.sqrt(d))
        if mid < 0: u = -u
        modes.append(u)
    return w, np.array(modes), s

# ---------------- N1-S1: reproduce the production ladders ----------------
R = pickle.load(open('/tmp/seal_s2/results_main.pkl', 'rb'))
print("\n=== N1-S1: my FEM vs production ladders (h=0, banked scr D_+) ===")
worst = 0.0
CACHE_MODES = {}
for tag in ('M1', 'M2', 'M4'):
    tb = MEM[tag]['t1pc']
    for mm in range(4):
        Mo = MOUT[tag][mm]['M']['scr']
        w, modes, sgrid = fem_vec(tag, mm, tb, 0.0, Mo)
        ref = np.array(R[(tag, mm, 'ladder')])
        dev = np.abs(w[:4] - ref)/np.abs(ref)
        worst = max(worst, dev.max())
        CACHE_MODES[(tag, mm)] = dict(sig=w, modes=modes, sgrid=sgrid)
        print(f"  {tag} m={mm}: sig {np.round(w[:4],5)} | rel dev vs pkl "
              f"{dev.max():.1e}")
checkN("N1-S1 independent FEM reproduces all 48 production rungs "
       "(<= 5e-3 rel; FEM-discretization level)", worst < 5e-3,
       f"worst {worst:.1e}")

# ---------------- N1-S2: shooting spot-check of the headline -------------
from s2_solve import refine
sr = refine('M1', 0, MEM['M1']['t1pc'], 7.06, 0.0, MOUT['M1'][0]['M']['scr'])
checkN("N1-S2 shooting reproduces recorded sigma = 7.057579 (M1 m=0)",
       abs(sr - 7.057579) < 2e-5, f"got {sr:.6f}")

# ---------------- N1-S3: Rayleigh-quotient consistency -------------------
# rebuild u^T A u and u^T B u by direct quadrature on the mode (trapz on
# the FEM grid) and compare to sigma -- guards index/transform errors.
def rayleigh(tag, mm, k=0, h_in=0.0):
    cf = coeffs(tag, mm); d = cf.d
    dd = CACHE_MODES[(tag, mm)]
    u = dd['modes'][k]; s = dd['sgrid']; sig = dd['sig'][k]
    du = np.gradient(u, s, axis=0)
    Anum = 0.0; Bnum = 0.0
    for i, t in enumerate(s):
        Hm, Gm = cf.at(t, 'A')
        wq = (s[1]-s[0]) * (0.5 if i in (0, len(s)-1) else 1.0)
        Anum += wq*np.exp(-t)*(du[i] @ du[i] + 2*u[i] @ Hm @ u[i])
        Bnum += wq*np.exp(-3*t)*(u[i] @ Gm @ u[i])
    Mo = MOUT[tag][mm]['M']['scr']
    Anum += u[0] @ Mo @ u[0]
    return Anum/Bnum, sig
rq, sig = rayleigh('M2', 0)
checkN("N1-S3 Rayleigh quotient (incl. M_out boundary term) == sigma "
       "(M2 m=0 rung 1, <=1%)", abs(rq/sig - 1) < 1e-2,
       f"RQ {rq:.4f} vs sigma {sig:.4f}")

# ---------------- pure-Neumann (no-flux) soft modes, all members ----------
print("\n=== no-flux (pure-Neumann weld) m=0 spectra: the flux-frozen "
      "scaling sector ===")
NOFLUX = {}
for tag in ('M1', 'M2', 'M4'):
    tb = MEM[tag]['t1pc']
    w, modes, sgrid = fem_vec(tag, 0, tb, 0.0, None, neumann0=True)
    NOFLUX[tag] = dict(sig=w, modes=modes, sgrid=sgrid)
    print(f"  {tag} m=0 Neumann-weld sigma: {np.round(w[:4], 5)}")

# ---------------- cache for downstream scripts ----------------------------
fine = {}
for tag in ('M1', 'M2', 'M4'):
    m = MEM[tag]
    tg = np.linspace(0, m['t5pc'], 1201)
    X = np.array([Xof(m, t) for t in tg])
    Xt = np.array([m['sol'].sol(t)[1::2] for t in tg])
    fine[tag] = dict(t=tg, X=X, Xt=Xt)
CF = {}
for tag in ('M1', 'M2', 'M4'):
    for mm in range(4):
        c = coeffs(tag, mm)
        CF[(tag, mm)] = dict(t=c.t, H=c.H, GA=c.GA, GB=c.GB, d=c.d)
meta = {t: {k: v for k, v in MEM[t].items() if k not in ('sol', 'dat')}
        for t in ('M1', 'M2', 'M4')}
MOUTC = {t: {mm: MOUT[t][mm]['M'] for mm in range(4)} for t in
         ('M1', 'M2', 'M4')}
GAUNT = {(t, mm): BLK[mm].gaunt() for t in ('M1',) for mm in range(4)}
with open('/tmp/nonstat_n1/cache.pkl', 'wb') as fh:
    pickle.dump(dict(meta=meta, fine=fine, CF=CF, MOUT=MOUTC,
                     MODES=CACHE_MODES, NOFLUX=NOFLUX, VH=VH, WC=WC,
                     GAUNT=GAUNT, LBLK=LBLK), fh)
n = sum(1 for _, ok in PASSN if ok)
print(f"\nN1-SETUP PASS {n}/{len(PASSN)}; wall {time.time()-t0:.0f}s")
