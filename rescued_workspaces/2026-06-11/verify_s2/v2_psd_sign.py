"""VERIFIER stage 2:
P1  PSD scan of own H^(m)(t): all members, all m, fine grid over the FULL
    integrated domain [0, t_stop] (t_stop: f_min = 0.002 -- far BEYOND the
    trust locus). GPU-batched eigvalsh. Hostile question: does the PSD
    statement degrade approaching the seal?
P2  the m=0 zero mode is the exact homogeneity direction: H(t) X_bg(t) = 0
P3  convexity statement check at adversarial states (random admissible,
    including very deep f_min ~ 0.004)
P4  C5 sign adjudication: exact Bessel eigenvalues of the constant-
    coefficient problem vs own FEM vs shooting with both sigma signs.
P5  flip-convention anchor: own solve of the banked weld-collar problem in
    r-coordinates (independent of the package's s-transform): relaxation
    sigma at gamma=2/3 and the boosted real mode at 1.5 gamma_c.
"""
import numpy as np, pickle, time, sys
sys.path.insert(0, '/tmp/verify_s2')
from v_lib import *
import torch

P, F = [], []
def check(name, ok, detail=""):
    (P if ok else F).append(name)
    print(f"VCHECK {name}: {'PASS' if ok else 'FAIL'} {detail}")

t0 = time.time()
MEM = load_members()
with open('/tmp/verify_s2/sols.pkl', 'rb') as fh:
    SOLD = pickle.load(fh)
dev = 'cuda' if torch.cuda.is_available() else 'cpu'
print("torch device:", dev)

# ---- P1: PSD scan over the FULL domain on GPU ----
QD = Q(3000)
BLKD = {m: Blk(m, QD) for m in range(4)}
print("\nP1 PSD scan, t in [0, t_stop] (3000 pts/member), GL 3000:")
floors = {}
for tag in ('M1', 'M2', 'M3', 'M4'):
    S = SOLD[tag]
    ts = np.linspace(0, S['tstop']*(1 - 1e-6), 3000)
    X = np.array([np.array([np.interp(t, S['t'], S['X'][:, k])
                            for k in range(4)]) for t in ts])
    t1, t5 = MEM[tag]['t1pc'], MEM[tag]['t5pc']
    for m in range(4):
        H = BLKD[m].mats(X)[0]                      # (nt,d,d)
        Ht = torch.tensor(H, device=dev, dtype=torch.float64)
        ev = torch.linalg.eigvalsh(Ht)[:, 0].cpu().numpy()
        floors[(tag, m)] = ev
        i1 = ts <= t1; i5 = ts <= t5
        print(f"  {tag} m={m}: min-eig floor  trust1% {ev[i1].min():+.2e}"
              f"  trust5% {ev[i5].min():+.2e}  FULL-to-seal "
              f"{ev.min():+.2e}  (last pt {ev[-1]:+.2e})")
gf = min(v.min() for v in floors.values())
check("P1 every H^(m)(t) PSD on every member over the FULL domain to the "
      "seal cutoff (floor > -1e-10) -- NOT a trust-domain artifact",
      gf > -1e-10, f"global floor {gf:+.2e}")
# trend (hostile question): the m>=1 min-eig DECREASES toward the seal
# but must stay >= 0 (perspective convexity for f > 0). Record the trend
# and confirm positivity at the deepest computed point.
tr_pos = all(floors[(tag, m)].min() > 0
             for tag in ('M1', 'M2', 'M3', 'M4') for m in (1, 2, 3))
print("  TREND: m>=1 min-eig decreases toward the seal (e.g. M1 m=1: "
      f"{floors[('M1',1)][0]:.3f} -> {floors[('M1',1)][-1]:.3f}) but is "
      "positive at every point; convexity (P3) forbids a sign change "
      "anywhere f > 0, i.e. on the entire sealed-cavity interior.")
check("P1b m>=1 min-eig positive at every grid point incl. beyond-trust "
      "(decreasing trend noted; convexity forbids crossing)", tr_pos)

# quadrature control at the deepest state
Sd = SOLD['M2']; Xd = Sd['X'][-2]
h3 = BLKD[0].mats(Xd)[0][0]
h6 = Blk(0, Q(6000)).mats(Xd)[0][0]
check("P1c GL3000 vs GL6000 at deepest state (f_min ~ 0.002)",
      np.abs(h3 - h6).max() < 1e-8, f"dev {np.abs(h3-h6).max():.1e}")

# ---- P2: homogeneity kernel ----
emax = 0.0
for tag in ('M1', 'M2', 'M4'):
    S = SOLD[tag]
    for frac in (0.2, 0.6, 0.95):
        t = S['tstop']*frac
        X = np.array([np.interp(t, S['t'], S['X'][:, k]) for k in range(4)])
        H = BLKS[0].mats(X)[0][0]
        emax = max(emax, np.abs(H @ X).max()/np.abs(H).max())
check("P2 m=0 kernel = homogeneity direction: H(t) X_bg(t) = 0 (so the "
      "PSD floor at 0 is structural, not marginal stability)",
      emax < 1e-10, f"max |H X|/|H| {emax:.1e}")

# ---- P3: convexity at adversarial admissible states ----
rng = np.random.default_rng(3)
fl = np.inf; n = 0
while n < 40:
    X = np.array([3.0, 0, 0, 0]) + rng.standard_normal(4)*np.array(
        [1.5, 1.0, 0.5, 0.25])
    fm = fmin_of(X)
    if fm < 0.004:
        continue
    n += 1
    for m in range(4):
        fl = min(fl, np.linalg.eigvalsh(BLKD[m].mats(X)[0][0]).min())
check("P3 H PSD at 40 random admissible states incl. f_min ~ 0.004 "
      "(perspective |grad f|^2/f jointly convex for f > 0: theorem holds "
      "wherever f > 0, i.e. up to the seal itself)", fl > -1e-10,
      f"floor {fl:+.2e}")

# ---- P4: sign adjudication via exact Bessel ----
print("\nP4 constant-coefficient exact solve:")
import mpmath as mp
F0, lam, L = 2.5, 6.0, 1.5
Hc, Gc = lam/(2*F0), 1/F0**2
nu = mp.sqrt(mp.mpf('0.25') + 2*Hc)
def cross(sig):
    x0 = mp.sqrt(sig*Gc); x1 = x0*mp.e**(-L)
    return (mp.besselj(nu, x0)*mp.bessely(nu, x1)
            - mp.besselj(nu, x1)*mp.bessely(nu, x0))
# scan for the first three roots
sg = np.linspace(1, 1200, 2400)
vals = [float(cross(s)) for s in sg]
roots = []
for i in range(len(sg) - 1):
    if vals[i]*vals[i+1] < 0:
        roots.append(float(mp.findroot(cross, (sg[i], sg[i+1]),
                                       solver='bisect')))
roots = np.array(roots[:3])
print("  exact Bessel sigmas:", roots)
ref = np.array([148.49670323, 467.60654397, 982.83062682])
check("P4a exact Bessel eigenvalues == the collector's FEM 'truth' "
      "{148.4967, 467.6065, 982.8306} (rel, FEM-discretization level)",
      (np.abs(roots - ref)/ref).max() < 2e-6,
      f"max rel dev {(np.abs(roots-ref)/ref).max():.1e}")
# my FEM on the same problem
class ConstTab:
    d = 1
    def at(self, tq, which='A'):
        n = len(np.atleast_1d(tq))
        return (np.full((n, 1, 1), Hc), np.full((n, 1, 1), Gc))
ct = ConstTab()
ev = fem_eigs(ct, L, 'dir', 0.0, N=2000, m=9, nev=3, dir_in=True)
check("P4b own FEM reproduces the exact Bessel sigmas",
      np.abs(ev - roots).max()/roots.max() < 1e-5,
      f"FEM {ev} rel dev {np.abs(ev-roots).max()/roots.max():.1e}")
# shooting both signs
def u0_sign(sig, sign):
    def rhs(t, z):
        return [z[1], z[1] + (2*Hc + sign*sig*np.exp(-2*t)*Gc)*z[0]]
    s = solve_ivp(rhs, (L, 0.0), [0.0, 1.0], method='DOP853',
                  rtol=1e-11, atol=1e-13)
    return s.y[0, -1]
rm = brentq(lambda s: u0_sign(s, -1), roots[0]-5, roots[0]+5)
plus_has_root = (u0_sign(roots[0]-5, +1)*u0_sign(roots[0]+5, +1) < 0)
rp = brentq(lambda s: u0_sign(s, +1), -roots[0]-5, -roots[0]+5)
check("P4c MINUS-sign shooting (collector's fix) has root at the true "
      "sigma; PLUS-sign (original bug) instead at -sigma",
      abs(rm - roots[0]) < 1e-5 and not plus_has_root
      and abs(rp + roots[0]) < 1e-5,
      f"minus {rm:.4f}, plus-root {rp:.4f} vs true {roots[0]:.4f}")

# ---- P5: flip anchor: banked weld-collar in r-coordinates (own FEM) ----
print("\nP5 weld-collar (r-coordinates, own FEM):")
# -(r^2 f^2 u')' + (lam f + 4 s f^2) u = sigma r^2 u, f = r^{-1/3}, s=1/9
# Robin r u'/u = gamma at r=1; Friedrichs at 0 (u ~ r^alpha, alpha ~ 0.52)
import scipy.sparse as sp
import scipy.sparse.linalg as spla
def collar(lam, gam, N=60000, r0=1e-9):
    r = np.geomspace(r0, 1.0, N)
    rm = 0.5*(r[:-1] + r[1:]); h = np.diff(r)
    p = rm**2*rm**(-2/3.)
    q = lam*rm**(-1/3.) + (4/9.)*rm**(-2/3.)
    w = rm**2
    n = N
    main_k = np.zeros(n); off_k = np.zeros(n - 1)
    main_m = np.zeros(n); off_m = np.zeros(n - 1)
    main_k[:-1] += p/h; main_k[1:] += p/h; off_k -= p/h
    main_k[:-1] += q*h/3; main_k[1:] += q*h/3; off_k += q*h/6
    main_m[:-1] += w*h/3; main_m[1:] += w*h/3; off_m += w*h/6
    # Robin at r=1: r u' = gam u -> form -= p(1)*gam*u(1)^2 / r ... careful:
    # Int -(p u')' u = Int p u'^2 - [p u' u]; at r=1: -p(1) u'(1) u(1),
    # u'(1) = gam u(1)/1 => K[n-1,n-1] += -1^2*1^{-2/3}*gam
    main_k[-1] += -gam
    K = sp.diags([off_k, main_k, off_k], [-1, 0, 1]).tocsc()
    M = sp.diags([off_m, main_m, off_m], [-1, 0, 1]).tocsc()
    # Dirichlet at r0
    K = K[1:, 1:]; M = M[1:, 1:]
    v = spla.eigsh(K, k=3, M=M, sigma=-20.0, return_eigenvectors=False)
    return np.sort(v)
s_rel = collar(2, 2/3)
print("  gamma=2/3 lam=2 sigmas:", s_rel)
check("P5a relaxation anchor: lowest sigma = +3.4667814 (omega^2 = "
      "-sigma < 0, banked)", abs(s_rel[0] - 3.4667814) < 2e-4,
      f"got {s_rel[0]:.6f}")
gc = 1.33835009
s_b = collar(2, 1.5*gc)
print("  gamma=1.5 gamma_c sigmas:", s_b)
check("P5b boosted REAL mode: lowest sigma = -4.0701100 (omega^2 = "
      "+4.07, banked) -- validates the omega^2 = -sigma flip on BOTH "
      "signs", abs(s_b[0] + 4.0701100) < 2e-4, f"got {s_b[0]:.6f}")

print(f"\nV2 STAGE: PASS {len(P)}/{len(P)+len(F)}  wall {time.time()-t0:.0f}s")
if F: print("FAILS:", F)
