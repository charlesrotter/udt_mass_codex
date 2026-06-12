"""VERIFIER stage 1: backgrounds + blocks from scratch.
V1  own flow integration (FD-gradient validated) vs library .dat rows
V2  constant-f anchors: H_ll = l(l+1)/(2F0), G_ll = 1/F0^2 (the x2/EL
    anchor: EL coeff = 2H = l(l+1)/F0)
V3  2D finite-difference second variation of P (own 2D quadrature, incl
    phi sector) vs own analytic H at sampled states; cross-check against
    the package's printed H^(1)(M2, t=0.9) matrix
V4  G_A, G_B vs 2D direct quadrature
V5  M_out: own Dplus + own Gaunt; PSD check; compare printed eigs
"""
import numpy as np, pickle, time, sys
sys.path.insert(0, '/tmp/verify_s2')
from v_lib import *

P, F = [], []
def check(name, ok, detail=""):
    (P if ok else F).append(name)
    print(f"VCHECK {name}: {'PASS' if ok else 'FAIL'} {detail}")

t0 = time.time()
MEM = load_members()

# ---- V0: analytic gradient == FD gradient (validates fast path) ----
rng = np.random.default_rng(7)
emax = 0.0; n = 0
while n < 6:
    X = np.array([2.0, -0.6, -0.1, -0.03]) + 0.2*rng.standard_normal(4)
    if fmin_of(X) < 0.05:          # admissible states only (f > 0)
        continue
    n += 1
    emax = max(emax, np.abs(Pgrad(X) - Pgrad_fd(X)).max())
check("V0 own analytic grad(P) == own FD grad (6 admissible states)",
      emax < 1e-8, f"max dev {emax:.1e}")

# ---- V1: own background integration vs library ----
SOL = {}
print("\nV1 backgrounds (own DOP853 + own P):")
worst = 0.0
for tag, m in MEM.items():
    sol = flow(m['gamma'], m['c'])
    SOL[tag] = sol
    tstop = sol.t[-1]
    dat = m['dat']
    sel = dat[:, 0] <= m['t5pc']*1.05
    Xd = dat[sel, 2:6]
    Xr = np.array([sol.sol(t)[:4] for t in dat[sel, 0]])
    err = np.abs(Xr - Xd).max()/np.abs(Xd).max()
    worst = max(worst, err)
    print(f"  {tag}: gamma={m['gamma']} c={m['c']:.6f}  t_stop(own)="
          f"{tstop:.5f}  rel dev vs .dat (t<=5%locus) {err:.2e}")
check("V1 own re-integration matches library on trust domain (<2e-8)",
      worst < 2e-8)

# ---- V2: constant-f anchors ----
F0 = 2.5
Xc = np.array([F0, 0, 0, 0])
H0, GA0, GB0 = BLKS[0].mats(Xc)
H0, GA0 = H0[0], GA0[0]
ll = np.array([l*(l + 1) for l in range(4)])
eH = np.abs(np.diag(H0) - ll/(2*F0)).max()
eG = np.abs(GA0 - np.eye(4)/F0**2).max()
eoff = np.abs(H0 - np.diag(np.diag(H0))).max()
check("V2 constant-f: H_ll = l(l+1)/(2F0) (EL coeff 2H = l(l+1)/F0, "
      "the x2-amendment anchor), G_A = I/F0^2, H off-diag = 0",
      eH < 1e-12 and eG < 1e-12 and eoff < 1e-12,
      f"devs {eH:.1e} {eG:.1e} {eoff:.1e}")
# m=1 block at constant f: H_ll should also be l(l+1)/(2F0)
H1c = BLKS[1].mats(Xc)[0][0]
e1 = np.abs(np.diag(H1c) - np.array([2, 6, 12])/(2*F0)).max()
check("V2b constant-f m=1 block: H_ll = l(l+1)/(2F0)", e1 < 1e-12,
      f"dev {e1:.1e}")

# ---- V3: 2D FD second variation vs analytic, on-flow states ----
print("\nV3 second variation: 2D-FD vs own analytic (M2 t=0.9, M1 t=1.2):")
ok3 = True
for tag, tt in (('M2', 0.9), ('M1', 1.2)):
    X = SOL[tag].sol(tt)[:4]
    for m in range(4):
        Ha = BLKS[m].mats(X)[0][0]
        Hf = hess_fd_2d(X, m)
        dev = np.abs(Ha - Hf).max()/np.abs(Ha).max()
        ok3 &= dev < 5e-6
        print(f"  {tag} t={tt} m={m}: rel dev {dev:.2e}")
check("V3 analytic H == 2D finite-difference second variation "
      "(all m, rel < 5e-6)", ok3)

# cross-check against the PACKAGE's printed H^(1), G_A^(1) (M2, t=0.9)
Hpkg = np.array([[0.42655725, 0.1700198, 0.05879329],
                 [0.1700198, 1.31621657, 0.37756657],
                 [0.05879329, 0.37756657, 2.62834769]])
Gpkg = np.array([[0.17829872, 0.05731375, 0.01587453],
                 [0.05731375, 0.19526931, 0.06584077],
                 [0.01587453, 0.06584077, 0.19928512]])
X9 = SOL['M2'].sol(0.9)[:4]
H1, GA1, _ = BLKS[1].mats(X9)
dH = np.abs(H1[0] - Hpkg).max(); dG = np.abs(GA1[0] - Gpkg).max()
check("V3b own H^(1),G_A^(1)(M2,t=0.9) == package assembled values",
      dH < 1e-6 and dG < 1e-6, f"max dev H {dH:.1e} G {dG:.1e}")

# ---- V4: G_A/G_B vs direct 2D quadrature at a state ----
def G_2d(X, m, p, nu=800, nphi=256):
    x, w = np.polynomial.legendre.leggauss(nu)
    phi = np.linspace(0, 2*np.pi, nphi, endpoint=False)
    B = Blk(m, Q(nu))
    if m == 0:
        Rl = Yr(x); cosf = np.ones_like(phi)
    else:
        Rl = B.R; cosf = np.sqrt(2)*np.cos(m*phi)
    f = (X @ Yr(x))[:, None] + 0*phi[None, :]
    d = len(LBLK[m]); G = np.empty((d, d))
    for i in range(d):
        for j in range(d):
            integ = (Rl[i][:, None]*cosf)*(Rl[j][:, None]*cosf)/f**p
            G[i, j] = 0.5*(w @ integ).mean()
    return G
g2 = G_2d(X9, 1, 2); g3 = G_2d(X9, 1, 3)
_, GA1x, GB1x = BLKS[1].mats(X9)
dv = max(np.abs(g2 - GA1x[0]).max(), np.abs(g3 - GB1x[0]).max())
check("V4 G_A, G_B == direct 2D quadrature (M2 t=0.9 m=1)", dv < 1e-9,
      f"max dev {dv:.1e}")

# ---- V5: D_+ and M_out ----
print("\nV5 D_+ (own mpmath):")
dps = {l: Dplus(l*(l + 1), NU_S) for l in range(4)}
dpu = {l: Dplus(l*(l + 1), NU_U) for l in range(4)}
print("  scr  : " + " ".join(f"{dps[l]:.6f}" for l in range(4)))
print("  unscr: " + " ".join(f"{dpu[l]:.6f}" for l in range(4)))
check("V5a screened D_+ == banked 0.666667/1.739812/2.745646/3.747460",
      max(abs(dps[0] - 2/3), abs(dps[1] - 1.739812),
          abs(dps[2] - 2.745646), abs(dps[3] - 3.747460)) < 2e-6)
print("  NOTE task prompt cited 'screened 3.7777 at ell=3'; 3.777706 is "
      "the UNSCREENED value; screened is 3.747460. Package used screened "
      "(scanned both) -- prompt typo, not a package error.")
MO = {}
okp = True
for tag, m in MEM.items():
    MO[tag] = {}
    for mm in range(4):
        M = mout(m['gamma'], m['c'], mm)
        MO[tag][mm] = M
        ev = np.linalg.eigvalsh(M)
        okp &= ev[0] > 0
        if mm == 0:
            print(f"  {tag} m=0 M_out eigs {np.round(ev, 4)}")
check("V5b own M_out PSD for every member/block (banked scr D_+)", okp)
# compare against package pickle
with open('/tmp/seal_s2/blocks.pkl', 'rb') as fh:
    bp = pickle.load(fh)
dmax = max(np.abs(MO[tag][mm] - bp['MOUT'][tag][mm]['scr']).max()
           for tag in MEM for mm in range(4))
check("V5c own M_out == package blocks.pkl (all members/blocks)",
      dmax < 1e-6, f"max dev {dmax:.1e}")
# bracket scan of outer condition PSD status
okb = True
for tag, m in MEM.items():
    for mm in range(4):
        for sc, nu, z in ((2.0, NU_S, False), (0.5, NU_S, False),
                          (1.0, NU_U, False), (1.0, NU_S, True)):
            ev = np.linalg.eigvalsh(mout(m['gamma'], m['c'], mm, sc, nu, z))
            okb &= ev[0] > -1e-12
check("V5d M_out stays PSD over the scanned bracket [0.5x,2x,unscr,D+=0]",
      okb)

with open('/tmp/verify_s2/sols.pkl', 'wb') as fh:
    pickle.dump({tag: dict(t=np.linspace(0, SOL[tag].t[-1], 4001),
                           X=np.array([SOL[tag].sol(t)[:4] for t in
                                       np.linspace(0, SOL[tag].t[-1], 4001)]),
                           tstop=SOL[tag].t[-1]) for tag in MEM}, fh)
print(f"\nV1 STAGE: PASS {len(P)}/{len(P)+len(F)}  wall {time.time()-t0:.0f}s")
if F: print("FAILS:", F)
