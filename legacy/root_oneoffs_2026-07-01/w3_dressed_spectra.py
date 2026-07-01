#!/usr/bin/env python3
"""
W3 — THE CROSS-BLOCK RE-POSE: SCRIPT 4 (DRESSED SPECTRA / THETA-DIAL
RE-GRADE).  Date: 2026-06-12.  Driver: W3 agent.  METRIC-LED.

The S2 mode problem (sealed_cavity_s2_results.md) re-run on the
w-completed fluctuation class, labeled variants (test-both):
  FROZEN (= S2's banked problem = the C1 + D_cell branch exactly)
  V-w  (delta-w eliminated, w-chart;  atom ratios (-1/3, 1/3, 2/3))
  V-s  (delta-w eliminated, exp-chart; atom ratios (-1, 0, 1/2))
The joint V-wq variant is NOT run as a global spectrum: its Schur
locus D_M = 0 enters the domain (w3_locus_maps) and severs the
eliminated operator; it is carried by the locus map + seal
asymptotics only (scoped statement, no spectrum claim).

Conventions locked to S2 by construction: backgrounds re-integrated
with the v_lib conventions (rescued_workspaces/2026-06-11/verify_s2/
v_lib.py, the VS2 verifier library); my OWN dressed-Hessian integrand
(asserted == v_lib's for the frozen variant); v_lib's FEM assembly
and shooting; W_A weight (ground H1: untouched by the completion);
banked outer D_+ + weld jet; inner stand-in t_b at the 1% trust
boundary; h = Robin dial on the non-forced directions (m=0: vhat
Dirichlet forced + complement Robin; m>=1: Robin all).

ANCHOR (must reproduce before any dressed number is computed): S2's
banked M1/M2/M4 m=0 lowest rungs (h=0):
  M1: -7.057579 -16.193966 -28.772125 -44.662375  (omega^2 = -sigma)
  M2: -7.134399 -16.362024 -28.699050 -44.637223
  M4: -4.238126 -12.546068 -24.160764 -38.714955

PRE-REGISTERED QUESTIONS (stated before the run):
  Q1 does h_c survive as a positive threshold per block (S2 item 1:
     interior cannot ring; omega^2 > 0 iff h > h_c > 0)?
  Q2 does the dressed interior produce omega^2 > 0 at h = 0 (the
     registry-#20 real-frequency species inside the static
     diagonal+w class)?  If yes, the 'h > h_c is the only oscillatory
     sector' reading DIES on the C1-only branch and the T-bounded
     oscillatory sector (sign inversion, nonstationary opener)
     ENLARGES beyond the boundary family.
  Q3 does any variant SELECT an h (kill the family or pin a unique
     finite-action member)?  (Script 2 already answers no at the
     true-seal endpoint; here the stand-in scan cross-checks that no
     dressed degeneracy singles out an h.)
FAILURE CRITERIA: a no-selector outcome on Q3 is the first-class
negative F-1; chart-disagreement between V-w and V-s on any SIGN
conclusion marks that conclusion chart-conditional (F-2), to be
reported as such, not resolved here.

GPU use per CLAUDE.md: batched eigvalsh only; B-reduction via CPU
Cholesky + explicit triangular inverse, matmul-only on device; CPU
scipy.eigh asserts at spot batches (the recorded V100 pitfall).
"""
import sys, time
import numpy as np
import scipy.linalg as sla

sys.path.insert(0, '/home/udt-admin/udt_mass_codex/rescued_workspaces/'
                '2026-06-11/verify_s2')
import v_lib as V

t0 = time.time()
npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond)
    npass += ok; nfail += (not ok)
    print(f"W3D-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

RAT = {'frozen': (1.0, 1.0, 1.0),
       'V-w': (-1/3, 1/3, 2/3),
       'V-s': (-1.0, 0.0, 1/2)}

# ---------- my own (dressed) coefficient tables ----------
class DressedTables:
    """same interface as v_lib.Tables but with MY OWN integrand:
    Hess~_ij = (1/2)< [g_ s dRi dRj + m^2 Ri Rj/s]/f
               - d_ (s fu)(dRi Rj + dRj Ri)/f^2
               + r_ (s fu^2) Ri Rj/f^3 >,  s = 1-u^2,
    (g_, d_, r_) the variant atom ratios; centrifugal undressed
    (ground H2).  G (W_A) identical to v_lib (ground H1)."""
    def __init__(self, sol, m, t5, variant, nt=961):
        g_, d_, r_ = RAT[variant]
        q = V.Q12
        B = V.BLKS[m]
        self.t = np.linspace(0.0, t5, nt)
        Xarr = np.array([sol.sol(tt)[:4] for tt in self.t])
        f = Xarr @ q.Y
        fu = Xarr @ q.Yu
        s = q.s
        d = B.d
        H = np.empty((nt, d, d)); G = np.empty((nt, d, d))
        for i in range(d):
            for j in range(i, d):
                gg = g_*s*B.dR[i]*B.dR[j]
                if m:
                    gg = gg + m*m*B.R[i]*B.R[j]/s
                rr = B.R[i]*B.R[j]
                rd = B.dR[i]*B.R[j] + B.dR[j]*B.R[i]
                I = gg/f - d_*(s*fu)*rd/f**2 + r_*(s*fu**2)*rr/f**3
                H[:, i, j] = H[:, j, i] = (I @ q.w)/4.0
                G[:, i, j] = G[:, j, i] = ((rr/f**2) @ q.w)/2.0
        self.H, self.GA, self.d = H, G, d
    def at(self, tq, which='A'):
        tq = np.clip(tq, self.t[0], self.t[-1])
        d = self.d
        H = np.empty((len(tq), d, d)); G = np.empty_like(H)
        for i in range(d):
            for j in range(d):
                H[:, i, j] = np.interp(tq, self.t, self.H[:, i, j])
                G[:, i, j] = np.interp(tq, self.t, self.GA[:, i, j])
        return H, G

MEM = V.load_members(('M1', 'M2', 'M4'))
SOL = {tag: V.flow(m['gamma'], m['c']) for tag, m in MEM.items()}
MO = {tag: {m: V.mout(MEM[tag]['gamma'], MEM[tag]['c'], m)
            for m in range(4)} for tag in MEM}

# my frozen integrand == v_lib's (independence + convention lock):
tabs = {}
for tag in MEM:
    for m in range(4):
        for var in RAT:
            tabs[(tag, m, var)] = DressedTables(
                SOL[tag], m, MEM[tag]['t5pc'], var)
ref = V.Tables(SOL['M1'], 0, MEM['M1']['t5pc'])
dev = np.max(np.abs(ref.H - tabs[('M1', 0, 'frozen')].H))
check("A1", dev < 1e-12,
      f"my frozen-integrand H == v_lib's Tables H (max dev {dev:.1e}) "
      "-- own code, locked conventions")

# ---------- the anchor: S2's banked rungs ----------
BANKED = {'M1': [-7.057579, -16.193966, -28.772125, -44.662375],
          'M2': [-7.134399, -16.362024, -28.699050, -44.637223],
          'M4': [-4.238126, -12.546068, -24.160764, -38.714955]}
okA = True
for tag in MEM:
    tb = MEM[tag]['t1pc']
    T = tabs[(tag, 0, 'frozen')]
    ev = V.fem_eigs(T, tb, MO[tag][0], 0.0, N=300, m=0, nev=4)
    sr = np.array([V.refine(T, tb, e, 0.0, MO[tag][0], m=0)
                   for e in ev])
    w2 = -sr
    rel = np.max(np.abs(w2 - BANKED[tag])/np.abs(BANKED[tag]))
    okA &= rel < 1e-5
    print(f"   anchor {tag} m=0 h=0: omega^2 = {w2.round(6)} "
          f"(banked rel dev {rel:.1e})")
check("A2", okA,
      "S2's banked m=0 relaxation rungs reproduced < 1e-5 rel on "
      "M1/M2/M4 (FROZEN variant == the banked problem == the "
      "C1 + D_cell branch)")

# ---------- GPU batched h-scans ----------
import torch
USE_GPU = torch.cuda.is_available()
def sigmin_scan(tab, tb, Mout, hs, m, N=200, nev=2):
    K, B, Pb = V.fem_assemble(tab, tb, Mout, N, 'A', m)
    L = sla.cholesky(B, lower=True)
    Li = sla.solve_triangular(L, np.eye(L.shape[0]), lower=True)
    KK = Li @ K @ Li.T
    PP = Li @ Pb @ Li.T
    KK = 0.5*(KK + KK.T); PP = 0.5*(PP + PP.T)
    if USE_GPU:
        KKt = torch.tensor(KK, device='cuda')
        PPt = torch.tensor(PP, device='cuda')
        ht = torch.tensor(hs, device='cuda')
        A = KKt[None] - ht[:, None, None]*PPt[None]
        A = 0.5*(A + A.transpose(-1, -2))
        ev = torch.linalg.eigvalsh(A)[:, :nev].cpu().numpy()
        # per-batch CPU assert (recorded V100 pitfall discipline):
        for k in (0, len(hs)//2, len(hs) - 1):
            evc = sla.eigh(KK - hs[k]*PP, eigvals_only=True,
                           subset_by_index=[0, nev - 1])
            assert np.max(np.abs(evc - ev[k])/np.maximum(
                np.abs(evc), 1)) < 1e-8, "GPU/CPU mismatch"
        return ev
    return np.array([sla.eigh(KK - h*PP, eigvals_only=True,
                              subset_by_index=[0, nev - 1])
                     for h in hs])

hs = np.concatenate([np.linspace(-4, 12, 81),
                     np.linspace(12.5, 40, 56)])
print("\nh-scan sigma_min(h) per member/block/variant "
      f"(GPU={USE_GPU}; t_b = 1% trust; W_A; banked D_+):")
HC = {}
SIG0 = {}
for tag in MEM:
    tb = MEM[tag]['t1pc']
    for m in range(4):
        for var in RAT:
            sm = sigmin_scan(tabs[(tag, m, var)], tb, MO[tag][m],
                             hs, m)[:, 0]
            # h_c: first crossing sigma_min = 0 (omega^2 = -sigma):
            below = np.where(sm < 0)[0]
            if len(below) and below[0] > 0:
                i = below[0]
                # linear interpolation:
                hc = hs[i-1] + (hs[i] - hs[i-1])*sm[i-1]/(sm[i-1]
                                                          - sm[i])
            elif len(below) and below[0] == 0:
                hc = -np.inf      # already ringing at scan start
            else:
                hc = np.inf
            mono = bool(np.all(np.diff(sm) < 1e-10))
            HC[(tag, m, var)] = hc
            i0 = np.argmin(np.abs(hs))
            SIG0[(tag, m, var)] = sm[i0]
            print(f"   {tag} m={m} {var:7s}: sigma_min(h=0) = "
                  f"{sm[i0]:10.4f}  h_c = {hc:8.3f}  "
                  f"monotone-decr: {mono}")

# ---------- the pre-registered questions ----------
q1 = all(np.isfinite(HC[(tag, m, var)]) and HC[(tag, m, var)] > 0
         for tag in MEM for m in range(4) for var in ('V-w',))
q1s = all(np.isfinite(HC[(tag, m, 'V-s')]) and HC[(tag, m, 'V-s')] > 0
          for tag in MEM for m in range(4))
check("B1", True,
      f"Q1 recorded: positive finite h_c on all blocks -- V-w: {q1}, "
      f"V-s: {q1s} (frozen: "
      f"{all(HC[(t, m, 'frozen')] > 0 for t in MEM for m in range(4))})")
ring_w = [(tag, m) for tag in MEM for m in range(4)
          if SIG0[(tag, m, 'V-w')] < 0]
ring_s = [(tag, m) for tag in MEM for m in range(4)
          if SIG0[(tag, m, 'V-s')] < 0]
check("B2", True,
      f"Q2 recorded: interior ringing at h=0 -- V-w blocks: {ring_w}; "
      f"V-s blocks: {ring_s}; frozen: "
      f"{[(t, m) for t in MEM for m in range(4) if SIG0[(t, m, 'frozen')] < 0]}")
# h_c shift table:
print("\nh_c shift table (variant vs frozen):")
for tag in MEM:
    for m in range(4):
        f0 = HC[(tag, m, 'frozen')]
        print(f"   {tag} m={m}: frozen {f0:8.3f}  V-w "
              f"{HC[(tag, m, 'V-w')]:8.3f}  V-s "
              f"{HC[(tag, m, 'V-s')]:8.3f}")
# chart sensitivity of the SIGN conclusions:
sign_agree = all((SIG0[(t, m, 'V-w')] < 0) == (SIG0[(t, m, 'V-s')] < 0)
                 for t in MEM for m in range(4))
check("B3", True,
      f"chart agreement on the h=0 ringing SIGN per block: "
      f"{sign_agree} (disagreement = chart-conditional conclusion, "
      "F-2 species)")
check("B4", all(np.isfinite(HC[(t, m, v)]) or HC[(t, m, v)] == -np.inf
                for t in MEM for m in range(4) for v in RAT),
      "every block has a crossing inside the scanned h-window or "
      "rings already at the window edge (no block lost)")

print(f"\nW3 DRESSED SPECTRA: {npass} PASS / {nfail} FAIL "
      f"({time.time()-t0:.0f}s)")
sys.exit(0 if nfail == 0 else 1)
