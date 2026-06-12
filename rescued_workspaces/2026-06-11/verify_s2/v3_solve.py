"""VERIFIER stage 3: the mode problem, recomputed from scratch.
S1  grid convergence + FEM-vs-own-shooting (M2 m=1 reference)
S2  ladder spot entries (5+) vs package, shooting-refined
S3  the C6 incident number: M2 m=0 h=+2 (convention pinned)
S4  h_c table (12 blocks) via own FEM bracket + own shooting at sigma=0
S5  GPU h-scan: monotonicity of sigma_min(h), single crossing, Dirichlet
    limit as h -> -inf; BOTH weights; hostile positive-mode hunt over the
    outer-condition bracket at h <= 0
S6  t_b stand-in sensitivity: ladder vs real modes (1% vs 5% + fine scan)
S7  collapse diagnostic: omega^2(h=4) x G00(t_b) e^{-2 t_b} across members
    (+ stability of the collapse at h=6 and m=0: is the inference robust?)
S8  c-independence / gamma-tracking of the ladder (incl. M3) -- exact %
S9  W_B parallel: same sign structure, ~20% stiffer ladder
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
dev = 'cuda' if torch.cuda.is_available() else 'cpu'
GPU_SOLVES = [0]

SOL = {tag: flow(m['gamma'], m['c']) for tag, m in MEM.items()}
TAB = {}
def tab(tag, m):
    if (tag, m) not in TAB:
        TAB[(tag, m)] = Tables(SOL[tag], m, MEM[tag]['t5pc'])
    return TAB[(tag, m)]
MO = {tag: {m: mout(MEM[tag]['gamma'], MEM[tag]['c'], m) for m in range(4)}
      for tag in MEM}

def gpu_sigmin(K0, B, Pb, hs, nev=1):
    """batched generalized eigh over h-grid; returns (len(hs), nev)."""
    Kt = torch.tensor(K0, device=dev, dtype=torch.float64)
    Bt = torch.tensor(B, device=dev, dtype=torch.float64)
    Pt = torch.tensor(Pb, device=dev, dtype=torch.float64)
    ht = torch.tensor(np.asarray(hs), device=dev, dtype=torch.float64)
    Ks = Kt[None] - ht[:, None, None]*Pt[None]
    L = torch.linalg.cholesky(Bt)
    Y = torch.linalg.solve_triangular(L[None], Ks, upper=False)
    A = torch.linalg.solve_triangular(
        L[None], Y.transpose(-1, -2), upper=False).transpose(-1, -2)
    A = 0.5*(A + A.transpose(-1, -2))
    ev = torch.linalg.eigvalsh(A)
    GPU_SOLVES[0] += len(hs)
    return ev[:, :nev].cpu().numpy()

# ---------- S1: convergence + FEM-vs-shooting ----------
print("S1 convergence (M2 m=1, h=0, banked scr, t_b 1%):")
tg, mm = 'M2', 1
tb = MEM[tg]['t1pc']; T = tab(tg, mm); Mo = MO[tg][mm]
for N in (150, 300, 600):
    ev = fem_eigs(T, tb, Mo, 0.0, N=N, m=mm, nev=4)
    print(f"  N={N}: {ev}")
ev3 = fem_eigs(T, tb, Mo, 0.0, N=300, m=mm, nev=3)
sr = [refine(T, tb, e, 0.0, Mo, m=mm) for e in ev3]
print(f"  own shooting-refined: {np.array(sr)}")
pk = [15.4327163, 28.2136726, 44.4018865]   # package shooting
check("S1 own shooting == package shooting (M2 m=1 lowest 3, <1e-5 rel)",
      max(abs(np.array(sr) - pk)/np.abs(pk)) < 1e-5,
      f"max rel {max(abs(np.array(sr)-pk)/np.abs(pk)):.1e}")
check("S1b own FEM N=300 vs own shooting < 2e-3 rel",
      max(abs(ev3 - np.array(sr))/np.abs(sr)) < 2e-3)

# ---------- S2: ladder spot entries ----------
print("\nS2 ladder spot entries (h=0, W_A, banked scr, t_b 1%):")
SPOTS = [('M2', 0, [7.134399, 16.362024, 28.699050, 44.637223]),
         ('M2', 1, [15.432716, 28.213673, 44.401887, 86.108506]),
         ('M4', 0, [4.238126, 12.546068, 24.160764, 38.714955]),
         ('M1', 3, [44.488525, 148.906794, 323.013850, 569.504587]),
         ('M3', 1, [14.297171, 26.506067, 42.719972, 81.465808])]
okl = True; wd = 0.0
for tg, mm, ref in SPOTS:
    T = tab(tg, mm); tbx = MEM[tg]['t1pc']; Mo = MO[tg][mm]
    ev = fem_eigs(T, tbx, Mo, 0.0, N=400, m=mm, nev=5)
    got = [refine(T, tbx, e, 0.0, Mo, m=mm) for e in ev[:4]]
    rel = max(abs(np.array(got) - ref)/np.abs(ref))
    wd = max(wd, rel); okl &= rel < 2e-5
    print(f"  {tg} m={mm}: own {np.round(got,6)}  (max rel dev {rel:.1e})")
check("S2 ladder: 20 entries across 5 blocks reproduce the package table "
      "(omega^2 = -sigma; all NEGATIVE omega^2)", okl, f"worst {wd:.1e}")

# ---------- S3: the incident number ----------
T = tab('M2', 0); tb2 = MEM['M2']['t1pc']; Mo = MO['M2'][0]
e2 = fem_eigs(T, tb2, Mo, 2.0, N=300, m=0, nev=3)
r2 = refine(T, tb2, e2[0], 2.0, Mo, m=0)
print(f"\nS3 M2 m=0 h=+2: FEM sigma_min = {e2[0]:.4f}; shooting-refined "
      f"sigma = {r2:.6f} => omega^2 = {-r2:.6f} (REAL mode, h > h_c)")
check("S3 M2 m=0 h=+2: sigma_min = -61.0487 (FEM, the s2_sens adapted "
      "number) and refined omega^2 = +61.051383 -- convention: quoted "
      "value is sigma, omega^2 = -sigma > 0",
      abs(e2[0] + 61.0487) < 0.02 and abs(-r2 - 61.051383) < 2e-4,
      f"FEM {e2[0]:.4f}, refined omega^2 {-r2:.6f}")

# ---------- S4: h_c table ----------
print("\nS4 h_c (sigma_min = 0 crossing), own FEM N=300 + own shooting:")
HCP = {'M1': [1.12074, 1.46347, 1.88106, 2.33170],
       'M2': [1.19430, 1.62723, 2.15566, 2.73562],
       'M4': [1.07609, 1.56420, 2.10390, 2.67363]}
okh = True; whd = 0.0
for tg in ('M1', 'M2', 'M4'):
    tbx = MEM[tg]['t1pc']
    row = []
    for mm in range(4):
        T = tab(tg, mm); Mo = MO[tg][mm]
        fmin1 = lambda h: fem_eigs(T, tbx, Mo, h, N=300, m=mm, nev=1)[0]
        hc = brentq(fmin1, 0.5, 4.0, xtol=2e-5)
        hcs = brentq(lambda h: shoot_det(T, tbx, 0.0, h, Mo, m=mm),
                     hc - 0.1, hc + 0.1, xtol=1e-7)
        row.append((hc, hcs))
        d = abs(hcs - HCP[tg][mm])
        whd = max(whd, d); okh &= d < 5e-4
    print(f"  {tg}: " + "  ".join(f"m={mm}:{r[0]:.5f}/{r[1]:.5f}"
                                  for mm, r in enumerate(row)))
check("S4 all 12 h_c reproduce the package (shooting, <5e-4)", okh,
      f"worst {whd:.1e}")

# ---------- S5: GPU h-scans, monotonicity, hostile hunt ----------
print("\nS5 GPU h-scans (sigma_min over h in [-30, 8], 153 pts):")
hs = np.linspace(-30, 8, 153)
okm = True; okx = True
for tg in ('M1', 'M2', 'M4'):
    tbx = MEM[tg]['t1pc']
    for mm in range(4):
        T = tab(tg, mm); Mo = MO[tg][mm]
        K0, B, Pb = fem_assemble(T, tbx, Mo, N=200, m=mm)
        sm = gpu_sigmin(K0, B, Pb, hs)[:, 0]
        dif = np.diff(sm)
        okm &= np.all(dif < 1e-9)
        nx = int(np.sum(np.diff(np.sign(sm)) != 0))
        okx &= (nx == 1) and sm[hs <= 0].min() > 0
        # Dirichlet limit
        evD = fem_eigs(T, tbx, Mo, 0.0, N=200, m=mm, nev=1, dir_in=True)[0]
        if tg == 'M2':
            print(f"  M2 m={mm}: sigma_min(-30) {sm[0]:+.4f} vs Dirichlet "
                  f"{evD:+.4f}; crossings {nx}; min over h<=0 "
                  f"{sm[hs<=0].min():+.4f}")
check("S5a sigma_min(h) strictly monotone decreasing in h, all 12 blocks "
      "(boundary-form monotonicity)", okm)
check("S5b exactly ONE sigma_min crossing per block, at h_c > 0; "
      "sigma_min > 0 for all h <= 0 (no real mode without inner "
      "attraction)", okx)
# hostile hunt: outer-condition bracket x both weights at h in [-30, 0]
print("  hostile hunt: outer bracket x {W_A, W_B}, h <= 0, all blocks:")
hneg = np.linspace(-30, 0, 31)
hunt_min = np.inf
for tg in ('M1', 'M2', 'M4'):
    tbx = MEM[tg]['t1pc']
    for mm in range(4):
        for which in ('A', 'B'):
            T = tab(tg, mm)
            for kind in ('2x', 'ref', '0.5x', 'unscr', 'dp0', 'neu', 'dir'):
                if kind == 'dir':
                    ev = fem_eigs(T, tbx, 'dir', 0.0, N=150, m=mm,
                                  nev=1, dir_in=False, which=which)
                    hunt_min = min(hunt_min, ev[0]); continue
                Mx = {'2x': mout(MEM[tg]['gamma'], MEM[tg]['c'], mm, 2.0),
                      'ref': MO[tg][mm],
                      '0.5x': mout(MEM[tg]['gamma'], MEM[tg]['c'], mm, 0.5),
                      'unscr': mout(MEM[tg]['gamma'], MEM[tg]['c'], mm,
                                    1.0, NU_U),
                      'dp0': mout(MEM[tg]['gamma'], MEM[tg]['c'], mm,
                                  zero_dp=True),
                      'neu': np.zeros((len(LBLK[mm]),)*2)}[kind]
                K0, B, Pb = fem_assemble(T, tbx, Mx, N=150, m=mm,
                                         which=which)
                sm = gpu_sigmin(K0, B, Pb, hneg)[:, 0]
                hunt_min = min(hunt_min, sm.min())
check("S5c HOSTILE HUNT: no positive mode (sigma_min > 0) anywhere on "
      "h <= 0 x outer bracket (Dir/2x/1x/0.5x/unscr/D+=0/Neumann) x "
      "{W_A, W_B} x all members/blocks", hunt_min > 0,
      f"global min sigma_min = {hunt_min:+.4f}")

# ---------- S6: t_b sensitivity ----------
print("\nS6 t_b stand-in sensitivity:")
for tg in ('M1', 'M2', 'M4'):
    for mm in (0, 1):
        T = tab(tg, mm); Mo = MO[tg][mm]
        l1 = fem_eigs(T, MEM[tg]['t1pc'], Mo, 0.0, N=300, m=mm, nev=1)[0]
        l5 = fem_eigs(T, MEM[tg]['t5pc'], Mo, 0.0, N=300, m=mm, nev=1)[0]
        r1 = -fem_eigs(T, MEM[tg]['t1pc'], Mo, 4.0, N=300, m=mm, nev=1)[0]
        r5 = -fem_eigs(T, MEM[tg]['t5pc'], Mo, 4.0, N=300, m=mm, nev=1)[0]
        print(f"  {tg} m={mm}: ladder h=0: {l1:+.4f} -> {l5:+.4f} "
              f"({100*abs(l5/l1-1):.1f}%) | real h=4: {r1:.1f} -> {r5:.1f} "
              f"({100*abs(r5/r1-1):.0f}%)")
T = tab('M2', 0); Mo = MO['M2'][0]
l1 = fem_eigs(T, MEM['M2']['t1pc'], Mo, 0.0, N=300, m=0, nev=1)[0]
l5 = fem_eigs(T, MEM['M2']['t5pc'], Mo, 0.0, N=300, m=0, nev=1)[0]
check("S6a ladder t_b sensitivity small but M2 m=0 = 2.3% (report says "
      "'1-2%'; verifier: the honest statement is '<= 2.3%')",
      abs(l5/l1 - 1) < 0.03, f"M2 m=0 shift {100*abs(l5/l1-1):.2f}%")
sens = []
for tg in ('M1', 'M2', 'M4'):
    for mm in (0, 1):
        T = tab(tg, mm); Mo = MO[tg][mm]
        r1 = -fem_eigs(T, MEM[tg]['t1pc'], Mo, 4.0, N=300, m=mm, nev=1)[0]
        r5 = -fem_eigs(T, MEM[tg]['t5pc'], Mo, 4.0, N=300, m=mm, nev=1)[0]
        sens.append(100*(r5/r1 - 1))
check("S6b real-mode t_b sensitivity 395-1152% (reproduced)",
      min(sens) > 380 and max(sens) < 1170,
      f"range {min(sens):.0f}% .. {max(sens):.0f}%")
# fine t_b scan (GPU) on M2: ladder smooth in t_b, real mode ~ local scale
tbs = np.linspace(0.7*MEM['M2']['t1pc'], MEM['M2']['t5pc'], 13)
lad, real, loc = [], [], []
for tbx in tbs:
    T = tab('M2', 1); Mo = MO['M2'][1]
    K0, B, Pb = fem_assemble(T, tbx, Mo, N=200, m=1)
    sm = gpu_sigmin(K0, B, Pb, np.array([0.0, 4.0]))
    lad.append(sm[0, 0]); real.append(-sm[1, 0])
    G00 = T.at(np.array([tbx]))[1][0, 0, 0]
    loc.append(G00*np.exp(-2*tbx))
lad, real, loc = map(np.array, (lad, real, loc))
prod = real*loc
print("  M2 m=1 fine t_b scan: ladder spread "
      f"{lad.max()/lad.min():.3f}x; real-mode spread "
      f"{real.max()/real.min():.1f}x; real x G00 e^-2tb spread "
      f"{prod.max()/prod.min():.3f}x")
check("S6c fine t_b scan: ladder ~flat; real mode tracks the LOCAL "
      "boundary scale 1/(G00 e^{-2tb}) over the whole trust window",
      lad.max()/lad.min() < 1.05 and real.max()/real.min() > 5
      and prod.max()/prod.min() < 1.25)

# ---------- S7: collapse diagnostic across members ----------
print("\nS7 collapse under local boundary scale:")
for hh, mm in ((4.0, 1), (6.0, 1), (4.0, 0)):
    vals = []
    for tg in ('M1', 'M2', 'M4'):
        tbx = MEM[tg]['t1pc']
        T = tab(tg, mm); Mo = MO[tg][mm]
        e = fem_eigs(T, tbx, Mo, hh, N=300, m=mm, nev=1)[0]
        sr = refine(T, tbx, e, hh, Mo, m=mm)
        w2 = -sr if np.isfinite(sr) else -e
        G00 = T.at(np.array([tbx]))[1][0, 0, 0]
        vals.append(w2*G00*np.exp(-2*tbx))
    v = np.array(vals)
    print(f"  h={hh} m={mm}: omega^2 x G00(tb)e^-2tb = "
          + " ".join(f"{x:.4f}" for x in v)
          + f"  (spread {v.max()/v.min():.3f}x)")
    if hh == 4.0 and mm == 1:
        check("S7a m=1 h=4 collapse {9.787, 9.999, 9.574}, spread 1.044x "
              "(reproduced)", np.abs(v - [9.787, 9.999, 9.574]).max() < 0.02
              and abs(v.max()/v.min() - 1.044) < 0.01,
              f"got {np.round(v,3)}")

# ---------- S8: c-independence / gamma tracking ----------
print("\nS8 ladder vs c (gamma=1: M1/M2/M3) and vs gamma (M4):")
lad0 = {}
for tg in ('M1', 'M2', 'M3', 'M4'):
    tbx = MEM[tg]['t1pc']
    row = []
    for mm in range(4):
        T = tab(tg, mm); Mo = MO[tg][mm]
        row.append(fem_eigs(T, tbx, Mo, 0.0, N=300, m=mm, nev=1)[0])
    lad0[tg] = np.array(row)
    print(f"  {tg} (gamma={MEM[tg]['gamma']}, c={MEM[tg]['c']:.4f}): "
          + " ".join(f"{v:+.4f}" for v in row))
sp12 = np.abs(lad0['M2']/lad0['M1'] - 1).max()
sp13 = np.abs(lad0['M3']/lad0['M1'] - 1).max()
g4 = (lad0['M4'] < 0.92*np.minimum(lad0['M1'], np.minimum(lad0['M2'],
                                                          lad0['M3']))).all()
print(f"  M2/M1 max dev {100*sp12:.1f}%; M3/M1 max dev {100*sp13:.1f}%")
check("S8a c-independence claim: M1 vs M2 within 2.5% -- TRUE; but "
      "M1 vs M3 deviates up to ~10% (report's 'M1/M2/M3 within 2-3%' "
      "OVERSTATES; M3 has the thin trust region)", sp12 < 0.025
      and 0.05 < sp13 < 0.12, f"M3 dev {100*sp13:.1f}%")
check("S8b gamma-tracking: M4 (gamma=0.5) ladder systematically lower "
      "in every m", bool(g4))

# ---------- S9: W_B parallel ----------
rowB = []
tbx = MEM['M2']['t1pc']
for mm in range(4):
    T = tab('M2', mm); Mo = MO['M2'][mm]
    rowB.append(fem_eigs(T, tbx, Mo, 0.0, N=300, m=mm, nev=1,
                         which='B')[0])
rowB = np.array(rowB)
print(f"\nS9 W_B ladder (M2 h=0): " + " ".join(f"{v:+.4f}" for v in rowB))
ratio = rowB/lad0['M2']
check("S9 W_B: same sign structure, ladder ~20% stiffer "
      "(package: +8.6349 +18.7718 +33.6658 +52.3369)",
      np.abs(rowB - [8.6349, 18.7718, 33.6658, 52.3369]).max() < 0.02
      and np.all((ratio > 1.15) & (ratio < 1.30)),
      f"ratios {np.round(ratio,3)}")
# pure-Neumann soft mode
T = tab('M2', 0)
ev = fem_eigs(T, tbx, np.zeros((4, 4)), 0.0, N=300, m=0, nev=1)[0]
check("S9b pure-Neumann outer soft mode +0.1586 (M2 m=0, h=0) -- "
      "positive only via the outer condition", abs(ev - 0.1586) < 0.003,
      f"got {ev:+.4f}")

print(f"\nV3 STAGE: PASS {len(P)}/{len(P)+len(F)}  wall {time.time()-t0:.0f}s"
      f"  GPU batched eigensolves: {GPU_SOLVES[0]}")
if F: print("FAILS:", F)
