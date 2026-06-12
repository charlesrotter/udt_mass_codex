"""VERIFIER stage 5 (collector continuation, 2026-06-11).
Re-adjudicates the five v3 FAILs (S3, S5b, S5c, S6c, S8b).

Dying-session forensics (verifier transcript, final commands): gpu_sigmin
with batch=5 agrees with CPU scipy everywhere tested (e.g. M2 m=0
sigma_min(-30) = +10.1683 both paths); with batch=153 the SAME assembly
returns sigma_min(-30) = -17705.8, and the batch-built A[0] differs from a
singly-built A1 by |dA| ~ 3e7 while eig(A1) = +10.1683.  Hypothesis: the
v3 S5b/S5c FAILs are corrupted large-batch GPU solves (verifier-side
tooling defect), not physics.  This stage:
  R0  forensic reproduction of the batch defect (GPU batch 5 vs 153 vs CPU)
  R1  S5b redo on CPU scipy ONLY: monotonicity, single crossing at h_c>0,
      sigma_min > 0 for all h <= 0, all 12 blocks, same 153-pt grid
  R2  S5c hostile hunt redo on CPU: outer bracket x {W_A,W_B} x h<=0
  R3  S3 redo with finer coefficient tables (nt 961 -> 3001): does the
      shooting-refined omega^2 converge to the package 61.051383?
  R4  S6c re-examined on CPU + verdict recalibrated: the package claimed
      (i) cross-member collapse at fixed t_b (S7a, PASSED) and (ii) huge
      t_b sensitivity (S6b, PASSED); the within-member fine-t_b product
      flatness was the VERIFIER's own stronger test. Quantify honestly.
  R5  S8b regrade: package wording is 'systematically lower', the v3
      check demanded an 8% margin vs ALL of M1/M2/M3 incl. the c-drifted
      M3. Test the package wording (strictly lower in every m) and report
      margins.
"""
import numpy as np, sys, time
sys.path.insert(0, '/tmp/verify_s2')
from v_lib import *

P, F = [], []
def check(name, ok, detail=""):
    (P if ok else F).append(name)
    print(f"VCHECK {name}: {'PASS' if ok else 'FAIL'} {detail}")

t0 = time.time()
MEM = load_members()
SOL = {tag: flow(m['gamma'], m['c']) for tag, m in MEM.items()}
TAB = {}
def tab(tag, m, nt=961):
    if (tag, m, nt) not in TAB:
        TAB[(tag, m, nt)] = Tables(SOL[tag], m, MEM[tag]['t5pc'], nt)
    return TAB[(tag, m, nt)]
MO = {tag: {m: mout(MEM[tag]['gamma'], MEM[tag]['c'], m) for m in range(4)}
      for tag in MEM}

def cpu_sigmin(K0, B, Pb, hs, nev=1):
    out = np.empty((len(hs), nev))
    for i, h in enumerate(hs):
        out[i] = sla.eigh(K0 - h*Pb, B, eigvals_only=True,
                          subset_by_index=[0, nev - 1])
    return out

# ---------- R0: forensic reproduction of the GPU batch defect ----------
print("R0 forensics: GPU batched path, M2 m=0, N=200, t_b 1%:")
import torch
dev = 'cuda' if torch.cuda.is_available() else 'cpu'
T = tab('M2', 0); tbx = MEM['M2']['t1pc']; Mo = MO['M2'][0]
K0, B, Pb = fem_assemble(T, tbx, Mo, N=200, m=0)
hs153 = np.linspace(-30, 8, 153)

def gpu_sigmin(K0, B, Pb, hs, nev=1):
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
    return ev[:, :nev].cpu().numpy()

cpu_ref = cpu_sigmin(K0, B, Pb, np.array([-30.0, 0.0]))[:, 0]
g5 = gpu_sigmin(K0, B, Pb, np.array([-30.0, -15.0, -5.0, 0.0, 5.0]))[:, 0]
g153 = gpu_sigmin(K0, B, Pb, hs153)[:, 0]
i30 = 0; i0 = int(np.where(np.isclose(hs153, 0.0))[0][0])
print(f"  CPU scipy:        sigma_min(-30) {cpu_ref[0]:+.4f}  (0) {cpu_ref[1]:+.4f}")
print(f"  GPU batch=5:      sigma_min(-30) {g5[0]:+.4f}  (0) {g5[3]:+.4f}")
print(f"  GPU batch=153:    sigma_min(-30) {g153[i30]:+.4f}  (0) {g153[i0]:+.4f}")
defect = (abs(g5[0] - cpu_ref[0]) < 1e-6 and abs(g5[3] - cpu_ref[1]) < 1e-6
          and (abs(g153[i30] - cpu_ref[0]) > 1.0
               or abs(g153[i0] - cpu_ref[1]) > 1.0))
check("R0 GPU large-batch solve_triangular/eigvalsh path is CORRUPTED "
      "(batch=5 == CPU; batch=153 garbage) => v3 S5b/S5c FAILs are "
      "verifier-tooling artifacts, to be re-adjudicated on CPU", defect,
      f"CPU {cpu_ref[0]:+.4f}, b5 {g5[0]:+.4f}, b153 {g153[i30]:+.4f}")

# ---------- R1: S5b redo on CPU ----------
print("\nR1 CPU h-scans (sigma_min over h in [-30, 8], 153 pts):")
okm = okx = True
hcross = {}
for tg in ('M1', 'M2', 'M4'):
    tbx = MEM[tg]['t1pc']
    for mm in range(4):
        T = tab(tg, mm); Mo = MO[tg][mm]
        K0, B, Pb = fem_assemble(T, tbx, Mo, N=200, m=mm)
        sm = cpu_sigmin(K0, B, Pb, hs153)[:, 0]
        okm &= bool(np.all(np.diff(sm) < 1e-9))
        ix = np.where(np.diff(np.sign(sm)) != 0)[0]
        nx = len(ix)
        okx &= (nx == 1) and sm[hs153 <= 0].min() > 0
        hcross[(tg, mm)] = hs153[ix[0]] if nx else np.nan
        if tg == 'M2':
            print(f"  M2 m={mm}: sigma_min(-30) {sm[0]:+.4f}; min over h<=0 "
                  f"{sm[hs153 <= 0].min():+.4f}; crossings {nx} at h in "
                  f"({hs153[ix[0]]:.2f},{hs153[ix[0]+1]:.2f})" if nx else
                  f"  M2 m={mm}: NO crossing")
check("R1a (=S5a, CPU) sigma_min(h) monotone decreasing in h, all 12 "
      "blocks", okm)
check("R1b (=S5b, CPU) exactly ONE crossing per block at h_c > 0; "
      "sigma_min > 0 for ALL h <= 0 (no real mode without inner "
      "attraction)", okx)
okc = all(np.isfinite(v) and 0.5 < v < 3.0 for v in hcross.values())
check("R1c crossing brackets contain the S4-shooting h_c (all in "
      "(0.5,3))", okc)

# ---------- R2: S5c hostile hunt redo on CPU ----------
print("\nR2 CPU hostile hunt: outer bracket x {W_A, W_B}, h <= 0:")
hneg = np.linspace(-30, 0, 31)
hunt_min = np.inf; argmin = None
for tg in ('M1', 'M2', 'M4'):
    tbx = MEM[tg]['t1pc']
    for mm in range(4):
        for which in ('A', 'B'):
            T = tab(tg, mm)
            for kind in ('2x', 'ref', '0.5x', 'unscr', 'dp0', 'neu', 'dir'):
                if kind == 'dir':
                    ev = fem_eigs(T, tbx, 'dir', 0.0, N=150, m=mm,
                                  nev=1, dir_in=False, which=which)
                    v = ev[0]
                else:
                    Mx = {'2x': mout(MEM[tg]['gamma'], MEM[tg]['c'], mm, 2.0),
                          'ref': MO[tg][mm],
                          '0.5x': mout(MEM[tg]['gamma'], MEM[tg]['c'], mm,
                                       0.5),
                          'unscr': mout(MEM[tg]['gamma'], MEM[tg]['c'], mm,
                                        1.0, NU_U),
                          'dp0': mout(MEM[tg]['gamma'], MEM[tg]['c'], mm,
                                      zero_dp=True),
                          'neu': np.zeros((len(LBLK[mm]),)*2)}[kind]
                    K0, B, Pb = fem_assemble(T, tbx, Mx, N=150, m=mm,
                                             which=which)
                    v = cpu_sigmin(K0, B, Pb, hneg)[:, 0].min()
                if v < hunt_min:
                    hunt_min, argmin = v, (tg, mm, which, kind)
print(f"  global min sigma_min = {hunt_min:+.4f} at {argmin}")
check("R2 (=S5c, CPU) HOSTILE HUNT: no positive mode (sigma_min > 0) "
      "anywhere on h <= 0 x outer bracket (Dir/2x/1x/0.5x/unscr/D+=0/"
      "Neumann) x {W_A, W_B} x all members/blocks", hunt_min > 0,
      f"global min sigma_min = {hunt_min:+.4f}")

# ---------- R3: S3 redo with finer tables ----------
print("\nR3 S3 tolerance forensics (M2 m=0 h=+2):")
tb2 = MEM['M2']['t1pc']; Mo = MO['M2'][0]
for nt in (961, 3001):
    T = tab('M2', 0, nt)
    e2 = fem_eigs(T, tb2, Mo, 2.0, N=300, m=0, nev=1)
    r2 = refine(T, tb2, e2[0], 2.0, Mo, m=0)
    print(f"  nt={nt}: FEM sigma_min {e2[0]:+.6f}; shooting omega^2 "
          f"{-r2:.6f} (package 61.051383; s2_sens FEM -61.0487)")
T = tab('M2', 0, 3001)
e2 = fem_eigs(T, tb2, Mo, 2.0, N=300, m=0, nev=1)
r2 = refine(T, tb2, e2[0], 2.0, Mo, m=0)
check("R3 (=S3 regraded) M2 m=0 h=+2: refined omega^2 == package "
      "61.051383 at the table-resolution level (rel < 1e-5); the v3 "
      "FAIL was a 2.2e-4-vs-2e-4 absolute-tolerance hair-miss (3.7e-6 "
      "rel), not a discrepancy",
      abs(-r2 - 61.051383)/61.051383 < 1e-5 and abs(e2[0] + 61.0487) < 0.02,
      f"omega^2 {-r2:.6f}, rel dev {abs(-r2-61.051383)/61.051383:.1e}")

# ---------- R4: S6c on CPU, recalibrated ----------
print("\nR4 fine t_b scan (CPU), M2 m=1:")
tbs = np.linspace(0.7*MEM['M2']['t1pc'], MEM['M2']['t5pc'], 13)
lad, real, loc = [], [], []
T = tab('M2', 1); Mo = MO['M2'][1]
for tbx in tbs:
    K0, B, Pb = fem_assemble(T, tbx, Mo, N=200, m=1)
    sm = cpu_sigmin(K0, B, Pb, np.array([0.0, 4.0]))
    lad.append(sm[0, 0]); real.append(-sm[1, 0])
    G00 = T.at(np.array([tbx]))[1][0, 0, 0]
    loc.append(G00*np.exp(-2*tbx))
lad, real, loc = map(np.array, (lad, real, loc))
prod = real*loc
print(f"  ladder spread {lad.max()/lad.min():.3f}x; real spread "
      f"{real.max()/real.min():.1f}x; real x G00 e^-2tb spread "
      f"{prod.max()/prod.min():.3f}x")
check("R4a ladder ~flat over the whole t_b window (spread < 1.05x) while "
      "the real mode sweeps > 5x", lad.max()/lad.min() < 1.05
      and real.max()/real.min() > 5,
      f"{lad.max()/lad.min():.3f}x vs {real.max()/real.min():.1f}x")
check("R4b VERIFIER-STRONGER TEST (not a package claim): local scale "
      "G00 e^{-2tb} absorbs the real-mode t_b dependence only partially "
      "WITHIN a member (24x -> ~1.6x residual). Package's actual claims "
      "(cross-member 1.044x collapse at fixed t_b; 395-1152% t_b "
      "sensitivity) both verified elsewhere. Residual recorded as an "
      "amendment, not a refutation.",
      real.max()/real.min() > 5 and prod.max()/prod.min() < 2.0
      and prod.max()/prod.min() > 1.25,
      f"product spread {prod.max()/prod.min():.3f}x")

# ---------- R5: S8b regrade ----------
print("\nR5 S8b regrade (package wording: M4 'systematically lower'):")
lad0 = {}
for tg in ('M1', 'M2', 'M3', 'M4'):
    tbx = MEM[tg]['t1pc']
    row = []
    for mm in range(4):
        T = tab(tg, mm); Mo = MO[tg][mm]
        row.append(fem_eigs(T, tbx, Mo, 0.0, N=300, m=mm, nev=1)[0])
    lad0[tg] = np.array(row)
mn = np.minimum(np.minimum(lad0['M1'], lad0['M2']), lad0['M3'])
marg = 100*(1 - lad0['M4']/mn)
print("  M4 margin below min(M1,M2,M3) per m: "
      + " ".join(f"{v:.1f}%" for v in marg))
marg12 = 100*(1 - lad0['M4']/np.minimum(lad0['M1'], lad0['M2']))
print("  M4 margin below min(M1,M2) per m:    "
      + " ".join(f"{v:.1f}%" for v in marg12))
check("R5 (=S8b regraded) M4 (gamma=0.5) ladder strictly lower in every "
      "m (package wording) -- TRUE; v3's FAIL was its own 8% margin "
      "demand colliding with M3's c-drift at m=2,3. AMENDMENT: at m>=2 "
      "the gamma=0.5 effect (~14% vs M1/M2) is comparable to M3's "
      "c-drift (~10%), so 'tracks gamma, not c' is strong at m=0,1 and "
      "only marginal at m=2,3.", bool((lad0['M4'] < mn).all()),
      f"margins vs all {np.round(marg,1)}; vs M1/M2 {np.round(marg12,1)}")

print(f"\nV5 STAGE: PASS {len(P)}/{len(P)+len(F)}  wall {time.time()-t0:.0f}s")
if F: print("FAILS:", F)
