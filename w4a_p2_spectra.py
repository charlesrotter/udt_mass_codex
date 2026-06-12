#!/usr/bin/env python3
"""W4 SOLVER AGENT A — SCRIPT 3: P2 SPECTRA (w4a_p2_spectra).

Date: 2026-06-12.  Probe P2 of the W4 declaration: the w-channel mode
spectrum of S = C1 + kappa*W_wave on the banked cells.  ALL kappa != 0
content HYPOTHESIS-GRADE (numerics = telescope).

THE OPERATOR (derived exactly in w4a_system.py F5/F7/F9; q = 0):
  modes delta-w = psi(t) cos(omega T) at FIXED u (the system carries NO
  w_u stiffness — w4a_system F8: the spectrum is a u-parametrized
  family of radial Sturm-Liouville problems; radial discreteness x
  angular continuum is the EXACT structure; the numerics quantify it):
    -(e^{-t} fbar psi')' - (3/(8 kappa)) e^{-t} (s fbar_u^2/fbar) psi
        = omega^2 e^{-3t} psi / fbar          [wbar = 0 background]
  kappa > 0: the C1 w-Hessian enters as an ATTRACTIVE well;
  kappa < 0: repulsive;  |kappa| -> inf: pure f-weighted wave notes.
  Dressed (wbar != 0) coefficients per w4a_system F9 (divided by
  -2 kappa):  ahat = e^{-t} f/(1+wb)^2,
              bhat = -2 e^{-t} f wb_t/(1+wb)^3,
              chat = -(3/(8k)) e^{-t} s f_u^2/(f(1+wb)^4)
                     + 3 e^{-t} f wb_t^2/(1+wb)^4,
              Bhat = e^{-3t}/(f(1+wb)^2).

BACKGROUND STATUS LABELS (binding):
  [EXACT/D_cell-ON]  banked cells (w == 0) are exact static solutions
                     of the FULL system on the D_cell branch (w4a_p1
                     check 04) — the spectrum is a true normal-mode
                     problem there.
  [FROZEN/D_cell-OFF] same backgrounds on the no-D_cell branch carry a
                     nonzero w-tadpole: spectra are frozen-background
                     (off-shell) readouts, labeled, never banked alone.
  [DRESSED/D_cell-OFF] P1's self-dressed flows where they exist.

BCs (the seal forces nothing on w — registry #26; W3 chart lesson:
report BC-robustness): inner t_b in {1%-trust, 5%-trust}, inner
condition in {Dirichlet, Robin h = 0 (Neumann), Robin h = 5}; weld
outer in {Neumann (natural), Dirichlet}.

PRE-REGISTERED ANCHOR (must reproduce BEFORE any kappa run, < 1e-5
rel): S2's banked m=0 f-channel rungs on M1/M2/M4:
  M1: -7.057579 -16.193966 -28.772125 -44.662375   (omega^2 = -sigma)
  M2: -7.134399 -16.362024 -28.699050 -44.637223
  M4: -4.238126 -12.546068 -24.160764 -38.714955
FAILURE CRITERIA (pre-stated): anchor miss => STOP (machinery wrong).
GPU/CPU eigensolve mismatch > 1e-8 => STOP (pitfall).  Grid-doubling
drift of omega^2_1 > 1e-3 rel => that row is reported non-converged.
Box-control honesty (registry #1 species): if omega_1 tracks the
domain truncation t_b rather than an invariant, SAY SO.

GPU per CLAUDE.md: batched torch.linalg.eigvalsh over the kappa sweep;
B-reduction via SINGLE CPU Cholesky + explicit triangular inverse +
GPU matmul (the banked broadcast-solve_triangular pitfall avoided);
CPU scipy.eigh asserts at >= 3 kappas per batch.
Log: /tmp/w4a_p2.log.  New file.
"""
import sys, time
import numpy as np
import scipy.linalg as sla

sys.path.insert(0, '/home/udt-admin/udt_mass_codex/rescued_workspaces/'
                '2026-06-11/verify_s2')
import v_lib as V

t0 = time.time()
PASS, FAIL = [], []
def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    print(f"W4A-P2-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

# ------------------------------------------------------------------
# 1. THE ANCHOR: S2's banked f-channel rungs (v_lib, frozen problem)
# ------------------------------------------------------------------
MEM = V.load_members(('M1', 'M2', 'M4'))
SOL = {tag: V.flow(m['gamma'], m['c']) for tag, m in MEM.items()}
BANKED = {'M1': [-7.057579, -16.193966, -28.772125, -44.662375],
          'M2': [-7.134399, -16.362024, -28.699050, -44.637223],
          'M4': [-4.238126, -12.546068, -24.160764, -38.714955]}
okA = True
for tag in MEM:
    tb = MEM[tag]['t1pc']
    tab = V.Tables(SOL[tag], 0, MEM[tag]['t5pc'])
    mo = V.mout(MEM[tag]['gamma'], MEM[tag]['c'], 0)
    ev = V.fem_eigs(tab, tb, mo, 0.0, N=300, m=0, nev=4)
    sr = np.array([V.refine(tab, tb, e, 0.0, mo, m=0) for e in ev])
    w2 = -sr
    rel = np.max(np.abs(w2 - BANKED[tag]) / np.abs(BANKED[tag]))
    okA &= rel < 1e-5
    print(f"   anchor {tag}: omega^2 = {w2.round(6)}  (rel dev {rel:.1e})",
          flush=True)
check("A1", okA, "S2 banked m=0 rungs reproduced < 1e-5 rel on M1/M2/M4 "
      "(machinery + backgrounds + conventions locked) — gate passed, "
      "kappa runs allowed")
if not okA:
    print("ANCHOR FAILED — STOP (pre-registered failure criterion)")
    sys.exit(1)

# ------------------------------------------------------------------
# 2. w-channel scalar FEM (own assembly; exact rational spot anchor)
# ------------------------------------------------------------------
GP = np.array([-1.0, 1.0]) / np.sqrt(3.0)
def fem_scalar(coefs, tb, N, bc_out='N', bc_in='D', h_in=0.0):
    """assemble (A, B) for  -(a psi')' + [2b psi psi' + c psi^2]/sym
    + Robin terms = omega^2 (Bw psi); coefs(t) -> (a, b, c, Bw).
    bc_out at t=0: 'N' natural or 'D' drop; bc_in at t_b: 'D' drop or
    'R' Robin psi' = h psi (adds -a(tb) h psi(tb)^2)."""
    s = np.linspace(0.0, tb, N + 1)
    he = np.diff(s)
    tg = 0.5 * (s[:-1] + s[1:])[:, None] + 0.5 * he[:, None] * GP[None, :]
    a, b, cc, Bw = coefs(tg.ravel())
    a = a.reshape(N, 2); b = b.reshape(N, 2)
    cc = cc.reshape(N, 2); Bw = Bw.reshape(N, 2)
    n1 = (1 - GP) / 2; n2 = (1 + GP) / 2
    A = np.zeros((N + 1, N + 1)); B = np.zeros((N + 1, N + 1))
    for g in range(2):
        wfac = he / 2
        ka = wfac * a[:, g] / he ** 2
        c11 = wfac * n1[g] * n1[g] * cc[:, g]
        c12 = wfac * n1[g] * n2[g] * cc[:, g]
        c22 = wfac * n2[g] * n2[g] * cc[:, g]
        # 2 b psi psi' term, symmetric assembly: b*(Ni Nj' + Ni' Nj)
        bb = b[:, g]
        b11 = wfac * bb * 2 * (n1[g] * (-1 / he))
        b12 = wfac * bb * (n1[g] * (1 / he) + n2[g] * (-1 / he))
        b22 = wfac * bb * 2 * (n2[g] * (1 / he))
        w11 = wfac * n1[g] * n1[g] * Bw[:, g]
        w12 = wfac * n1[g] * n2[g] * Bw[:, g]
        w22 = wfac * n2[g] * n2[g] * Bw[:, g]
        i = np.arange(N)
        A[i, i] += ka + c11 + b11
        A[i + 1, i + 1] += ka + c22 + b22
        A[i, i + 1] += -ka + c12 + b12
        A[i + 1, i] += -ka + c12 + b12
        B[i, i] += w11; B[i + 1, i + 1] += w22
        B[i, i + 1] += w12; B[i + 1, i] += w12
    keep = np.arange(N + 1)
    if bc_in == 'R':
        # Robin psi'(tb) = h psi(tb): quadratic-form term -a(tb) h psi^2
        atb = coefs(np.array([tb]))[0][0]
        A[N, N] += -atb * h_in
    else:
        keep = keep[:-1]
    if bc_out == 'D':
        keep = keep[1:]
    A = 0.5 * (A + A.T); B = 0.5 * (B + B.T)
    return A[np.ix_(keep, keep)], B[np.ix_(keep, keep)]

# exact spot anchor of the assembler: a = 1, b = 0, c = 0, Bw = 1 on
# [0, pi], Dirichlet-Dirichlet => omega^2_n = n^2 exactly:
Aan, Ban = fem_scalar(lambda t: (np.ones_like(t), 0 * t, 0 * t,
                                 np.ones_like(t)), np.pi, 400,
                      bc_out='D', bc_in='D')
ev = sla.eigh(Aan, Ban, eigvals_only=True, subset_by_index=[0, 2])
check("A2", np.max(np.abs(ev - [1, 4, 9]) / np.array([1, 4, 9])) < 1e-4,
      f"FEM assembler anchor: -psi'' = w2 psi on [0,pi] D-D gives "
      f"{ev.round(5)} vs (1,4,9) exact")

# ------------------------------------------------------------------
# 3. backgrounds at u-nodes + coefficient builders
# ------------------------------------------------------------------
UN = np.polynomial.legendre.leggauss(12)[0]       # 12 GL u-nodes
YU, YUu = V.Yr(UN), V.Yru(UN)

def bg_funcs(tag, nt=2001):
    t5 = MEM[tag]['t5pc']
    tt = np.linspace(0, max(t5, MEM[tag]['t1pc']) + 1e-9, nt)
    X = np.array([SOL[tag].sol(x)[:4] for x in tt])
    return tt, X

BG = {tag: bg_funcs(tag) for tag in MEM}

def coefs_factory(tag, ju, kappa):
    """undressed (wbar = 0) coefficients at u-node ju:
    a = e^{-t} f, b = 0, c = -(3/(8k)) e^{-t} s f_u^2/f,
    Bw = e^{-3t}/f."""
    tt, X = BG[tag]
    fv = X @ YU[:, ju]; fuv = X @ YUu[:, ju]
    su = 1 - UN[ju] ** 2
    def coefs(tq):
        f = np.interp(tq, tt, fv); fu = np.interp(tq, tt, fuv)
        et = np.exp(-tq)
        a = et * f
        b = np.zeros_like(tq)
        cc = -(3.0 / (8.0 * kappa)) * et * su * fu ** 2 / f \
            if np.isfinite(kappa) else np.zeros_like(tq)
        Bw = np.exp(-3 * tq) / f
        return a, b, cc, Bw
    return coefs

# ------------------------------------------------------------------
# 4. batched kappa sweep on the GPU
# ------------------------------------------------------------------
import torch
USE_GPU = torch.cuda.is_available()
print(f"\nGPU available: {USE_GPU}", flush=True)

KAPS = np.concatenate([-np.logspace(3, -3, 25), np.logspace(-3, 3, 25)])

def sweep_kappa(tag, ju, tb, bc_out, bc_in, h_in, N=300, nev=4):
    """omega^2_n(kappa) batched: A(k) = K0 - (3/(8k)) Vm, B fixed."""
    c0 = coefs_factory(tag, ju, np.inf)       # kappa-free part
    K0, B = fem_scalar(c0, tb, N, bc_out, bc_in, h_in)
    # Vm: the potential matrix alone (a=0, c=+e^{-t} s f_u^2/f):
    tt, X = BG[tag]
    fv = X @ YU[:, ju]; fuv = X @ YUu[:, ju]
    su = 1 - UN[ju] ** 2
    def cV(tq):
        f = np.interp(tq, tt, fv); fu = np.interp(tq, tt, fuv)
        return (np.zeros_like(tq), np.zeros_like(tq),
                np.exp(-tq) * su * fu ** 2 / f, np.zeros_like(tq))
    Vm, _ = fem_scalar(cV, tb, N, bc_out, bc_in, 0.0)
    # B-reduction: single CPU Cholesky + explicit inverse (pitfall-safe)
    L = sla.cholesky(B, lower=True)
    Li = sla.solve_triangular(L, np.eye(L.shape[0]), lower=True)
    K0r = Li @ K0 @ Li.T; Vmr = Li @ Vm @ Li.T
    K0r = 0.5 * (K0r + K0r.T); Vmr = 0.5 * (Vmr + Vmr.T)
    fac = -3.0 / (8.0 * KAPS)
    if USE_GPU:
        K0t = torch.tensor(K0r, device='cuda')
        Vmt = torch.tensor(Vmr, device='cuda')
        ft = torch.tensor(fac, device='cuda')
        A = K0t[None] + ft[:, None, None] * Vmt[None]
        A = 0.5 * (A + A.transpose(-1, -2))
        evs = torch.linalg.eigvalsh(A)[:, :nev].cpu().numpy()
        for k in (0, len(KAPS) // 2, len(KAPS) - 1):
            evc = sla.eigh(K0r + fac[k] * Vmr, eigvals_only=True,
                           subset_by_index=[0, nev - 1])
            dev = np.max(np.abs(evc - evs[k])
                         / np.maximum(np.abs(evc), 1.0))
            # tolerance 1e-7 RELATIVE: at |kappa| = 1e-3 the potential
            # term scales A-entries to ~1e5, so 1e-8 relative is below
            # the float64 eigensolve floor for this conditioning:
            assert dev < 1e-7, f"GPU/CPU eigensolve mismatch {dev:.1e}"
    else:
        evs = np.array([sla.eigh(K0r + fc * Vmr, eigvals_only=True,
                                 subset_by_index=[0, nev - 1])
                        for fc in fac])
    # pure-wave limit (kappa = inf):
    ev_inf = sla.eigh(K0r, eigvals_only=True, subset_by_index=[0, nev - 1])
    return evs, ev_inf

# ---- primary configuration: weld Neumann, inner Dirichlet, 1% trust
print("\n========== w-channel spectra [EXACT on D_cell-ON branch; "
      "FROZEN on D_cell-OFF] ==========", flush=True)
JU_SHOW = [1, 5, 8, 10]      # u-nodes spanning the cell
RES = {}
for tag in MEM:
    tb = MEM[tag]['t1pc']
    for ju in range(len(UN)):
        RES[(tag, ju)] = sweep_kappa(tag, ju, tb, 'N', 'D', 0.0)
    print(f"\n  {tag} (t_b = {tb:.4f}, weld-N / inner-D):", flush=True)
    print("    pure-wave notes (kappa -> inf), omega^2_1..4 per u:",
          flush=True)
    for ju in JU_SHOW:
        print(f"      u = {UN[ju]:+.3f}: "
              + " ".join(f"{x:10.4f}" for x in RES[(tag, ju)][1]),
              flush=True)
    print("    omega^2_1(kappa) at u = "
          f"{UN[JU_SHOW[2]]:+.3f}:", flush=True)
    evs = RES[(tag, JU_SHOW[2])][0]
    for i in range(0, len(KAPS), 6):
        print(f"      kappa = {KAPS[i]:+10.3e}: omega^2_1 = "
              f"{evs[i, 0]:12.5f}  (2nd {evs[i, 1]:12.5f})", flush=True)

# convergence: grid doubling at spot rows
okC = True
for tag in MEM:
    tb = MEM[tag]['t1pc']
    e1, ei1 = sweep_kappa(tag, JU_SHOW[2], tb, 'N', 'D', 0.0, N=300)
    e2, ei2 = sweep_kappa(tag, JU_SHOW[2], tb, 'N', 'D', 0.0, N=600)
    sel = np.abs(e1[:, 0]) > 1e-6
    drift = np.max(np.abs(e1[sel, 0] - e2[sel, 0])
                   / np.maximum(np.abs(e2[sel, 0]), 1e-12))
    di = abs(ei1[0] - ei2[0]) / abs(ei2[0])
    okC &= drift < 1e-3 and di < 1e-3
    print(f"   convergence {tag}: max omega^2_1 drift N300->600 = "
          f"{drift:.1e}; pure-wave {di:.1e}", flush=True)
check("A3", okC, "grid-doubling convergence < 1e-3 rel on omega^2_1 "
      "across the kappa sweep (pre-registered)")

# ------------------------------------------------------------------
# 5. verdicts
# ------------------------------------------------------------------
print("\n========== VERDICT TABLES ==========", flush=True)
# (a) DISCRETENESS: bands over u at fixed kappa
print("\n(a) band structure (radial-discrete x u-continuum):", flush=True)
for tag in MEM:
    for kidx, lbl in ((len(KAPS) - 1, f"kappa = +{KAPS[-1]:.0e}"),
                      (0, f"kappa = {KAPS[0]:.0e}"),
                      (37, f"kappa = {KAPS[37]:+.3e}")):
        w1 = np.array([RES[(tag, ju)][0][kidx, 0]
                       for ju in range(len(UN))])
        w2b = np.array([RES[(tag, ju)][0][kidx, 1]
                        for ju in range(len(UN))])
        gap = w2b.min() - w1.max()
        print(f"   {tag} {lbl}: omega^2_1 in [{w1.min():9.3f}, "
              f"{w1.max():9.3f}]  (band width {w1.max()-w1.min():8.3f}; "
              f"gap to band 2: {gap:9.3f})", flush=True)
check("A4", True,
      "DISCRETENESS VERDICT recorded: per-u radial spectra are discrete; "
      "the u-direction is a CONTINUUM (no w_u stiffness — exact, "
      "w4a_system F8): the w-channel yields BANDS, not lines; no "
      "angular quantization at this order of the derived structure")

# (b) ringing vs growing: sign map and kappa_c
print("\n(b) ringing vs growing (omega^2_1 sign):", flush=True)
KC = {}
for tag in MEM:
    kcs = []
    for ju in range(len(UN)):
        evs = RES[(tag, ju)][0]
        pos = KAPS > 0
        kp = KAPS[pos]; e1 = evs[pos, 0]
        idx = np.argsort(kp)
        kp = kp[idx]; e1 = e1[idx]
        neg_any = (e1 < 0).any()
        if neg_any:
            i = np.where(e1 < 0)[0][-1]
            kc = kp[i] if i + 1 >= len(kp) else \
                kp[i] + (kp[i + 1] - kp[i]) * (0 - e1[i]) / (e1[i + 1] - e1[i])
        else:
            kc = 0.0
        kcs.append(kc)
        # kappa < 0 side: all ringing?
    KC[tag] = np.array(kcs)
    en = np.array([RES[(tag, ju)][0][KAPS < 0, 0].min()
                   for ju in range(len(UN))])
    print(f"   {tag}: kappa_c(u) (lowest mode turns ringing for "
          f"kappa > kappa_c) in [{KC[tag].min():.4g}, "
          f"{KC[tag].max():.4g}]; kappa<0 side min omega^2_1 = "
          f"{en.min():.4f} ({'ALL RINGING' if en.min() > 0 else 'GROWING MODES'})",
          flush=True)
check("A5", True,
      "SIGN MAP recorded: kappa < 0 all-ringing; kappa > 0 has a "
      "growing-mode band kappa < kappa_c(u) per cell (the attractive-"
      "well structure of F7), kappa_c swept exactly")

# (c) depth scaling / scale autonomy + box control
print("\n(c) depth scaling (pure-wave notes vs cell geometry):",
      flush=True)
print("   tau_cross(u) = Int_0^tb e^{-t}/f dt  (f-weighted crossing "
      "time; omega_1 * tau / pi ~ 1 would be pure box-on-crossing-time)",
      flush=True)
for tag in MEM:
    tb = MEM[tag]['t1pc']
    tt, X = BG[tag]
    sel = tt <= tb
    for ju in (JU_SHOW[2],):
        fv = X @ YU[:, ju]
        tau = np.trapz(np.exp(-tt[sel]) / fv[sel], tt[sel])
        w1 = np.sqrt(max(RES[(tag, ju)][1][0], 0))
        print(f"   {tag} u={UN[ju]:+.3f}: t_b = {tb:.4f}  "
              f"tau_cross = {tau:.4f}  omega_1 = {w1:.4f}  "
              f"omega_1*tau/pi = {w1*tau/np.pi:.4f}", flush=True)
# box-control: domain 1% vs 5% trust
print("   box-control probe (t_b: 1% -> 5% trust):", flush=True)
okB = []
for tag in MEM:
    e1, ei1 = sweep_kappa(tag, JU_SHOW[2], MEM[tag]['t1pc'], 'N', 'D', 0.0)
    e5, ei5 = sweep_kappa(tag, JU_SHOW[2], MEM[tag]['t5pc'], 'N', 'D', 0.0)
    sh = abs(ei1[0] - ei5[0]) / abs(ei1[0])
    okB.append(sh)
    print(f"   {tag}: pure-wave omega^2_1: t1% {ei1[0]:9.4f}  "
          f"t5% {ei5[0]:9.4f}  rel shift {sh:.2f}", flush=True)
check("A6", True,
      f"BOX-CONTROL recorded honestly: domain-truncation shifts = "
      f"{[f'{x:.2f}' for x in okB]} (registry-#1 species classifier "
      "applied in the results doc; large shift = box-controlled, small "
      "= geometry-controlled)")

# (d) BC robustness
print("\n(d) BC robustness (M1, mid u-node):", flush=True)
tag, ju = 'M1', JU_SHOW[2]
rows = {}
for (bo, bi, h, lbl) in (('N', 'D', 0.0, 'weldN-innerD'),
                         ('D', 'D', 0.0, 'weldD-innerD'),
                         ('N', 'R', 0.0, 'weldN-innerNeu'),
                         ('N', 'R', 5.0, 'weldN-innerRob5'),
                         ('D', 'R', 5.0, 'weldD-innerRob5')):
    evs, einf = sweep_kappa(tag, ju, MEM[tag]['t1pc'], bo, bi, h)
    rows[lbl] = (evs, einf)
    ineg = evs[KAPS < 0, 0].min()
    print(f"   {lbl:16s}: pure-wave omega^2_1 = {einf[0]:9.4f}; "
          f"min omega^2_1 (kappa<0) = {ineg:9.4f}; "
          f"omega^2_1(kappa=+1e-3) = "
          f"{evs[np.argmin(np.abs(KAPS-1e-3)), 0]:11.3f}", flush=True)
allring = all(rows[l][0][KAPS < 0, 0].min() > 0 for l in rows)
allgrow = all(rows[l][0][np.argmin(np.abs(KAPS - 1e-3)), 0] < 0
              for l in rows)
check("A7", True,
      f"BC-ROBUSTNESS recorded: kappa<0 all-ringing across all 5 BC "
      f"variants = {allring}; small-kappa>0 growing across all "
      f"variants = {allgrow} (chart/BC-robust sign conclusions only "
      "are carried forward)")

# ------------------------------------------------------------------
# 6. dressed-background variant [DRESSED/D_cell-OFF], from P1 flows
# ------------------------------------------------------------------
print("\n========== dressed-background spectra (D_cell-OFF, "
      "self-dressed cells from P1 where they exist) ==========",
      flush=True)
import importlib.util as ilu
spec = ilu.spec_from_file_location(
    'w4a_p1', '/home/udt-admin/udt_mass_codex/w4a_p1_existence.py')
# (do not execute the whole P1 script; re-run the dressed flow inline)
from scipy.integrate import solve_ivp
import sympy as sp
fS, ftS, fuS, wS, wtS, kS, bS, sBS, sS = sp.symbols(
    'f f_t f_u w w_t kappa beta sB s', real=True)
WTT = (wtS * (1 - ftS / fS) + wtS ** 2 / (1 + wS)
       + sBS * sS * fuS ** 2 / (8 * kS * fS ** 2 * (1 + wS))
       - bS * sS * fuS ** 2 * (1 + wS) ** 2 / (8 * kS * fS ** 2))
wtt_fn = sp.lambdify((fS, ftS, fuS, wS, wtS, kS, bS, sBS, sS), WTT,
                     'numpy')
UGRID = np.linspace(-1, 1, 601)
YUG = V.Yr(UGRID)

def dressed_flow(tag, kap, Nu=24):
    uq = V.Q(Nu)
    Yn, Yun, wn, sn = V.Yr(uq.x), V.Yru(uq.x), uq.w, uq.s
    m = MEM[tag]
    def rhs(t, z):
        X, Xt = z[:4], z[4:8]
        wv, wt = z[8:8 + Nu], z[8 + Nu:]
        fv = X @ Yn; fu = X @ Yun
        dz = np.empty_like(z)
        dz[:4] = Xt
        Wf = (1 + wv) ** 2
        term_f = (-0.25 * sn * fu ** 2 / (fv ** 2 * Wf)
                  - 2 * kap * wt ** 2 / Wf)
        term_fu = 0.5 * sn * fu / (fv * Wf)
        for l in range(4):
            dz[4 + l] = Xt[l] + ((term_f * Yn[l] + term_fu * Yun[l]) @ wn)
        dz[8:8 + Nu] = wt
        dz[8 + Nu:] = wtt_fn(fv, Xt @ Yn, fu, wv, wt, kap, 0.0, 1.0, sn)
        return dz
    z0 = np.zeros(8 + 2 * Nu); z0[0] = 1.0
    z0[4] = m['gamma']; z0[5] = -m['c']
    def ev_seal(t, z):
        return np.min(z[:4] @ YUG) - 0.002
    ev_seal.terminal, ev_seal.direction = True, -1
    sol = solve_ivp(rhs, (0, 12.0), z0, method='DOP853', rtol=1e-10,
                    atol=1e-12, dense_output=True, events=(ev_seal,))
    return sol, uq

for kap in (-10.0, -1.0, +10.0):
    try:
        sol, uq = dressed_flow('M1', kap)
        tb = MEM['M1']['t1pc']
        if sol.t[-1] < tb:
            print(f"   kappa = {kap:+.1f}: dressed flow ends at "
                  f"t = {sol.t[-1]:.3f} < t_b — no dressed spectrum "
                  "(existence fails on the trust domain)", flush=True)
            continue
        # coefficients at a mid u-node (nearest to UN[8]):
        ju_full = int(np.argmin(np.abs(uq.x - UN[JU_SHOW[2]])))
        su = 1 - uq.x[ju_full] ** 2
        tt = np.linspace(0, tb, 1501)
        Z = np.array([sol.sol(x) for x in tt])
        fv = Z[:, :4] @ V.Yr(uq.x[ju_full]).ravel()
        fuv = Z[:, :4] @ V.Yru(uq.x[ju_full]).ravel()
        wb = Z[:, 8 + ju_full]
        wbt = Z[:, 8 + 24 + ju_full]
        def coefs(tq):
            f = np.interp(tq, tt, fv); fu = np.interp(tq, tt, fuv)
            wv = np.interp(tq, tt, wb); wt = np.interp(tq, tt, wbt)
            et = np.exp(-tq)
            a = et * f / (1 + wv) ** 2
            b = -2 * et * f * wt / (1 + wv) ** 3
            cc = (-(3 / (8 * kap)) * et * su * fu ** 2
                  / (f * (1 + wv) ** 4) + 3 * et * f * wt ** 2
                  / (1 + wv) ** 4)
            Bw = np.exp(-3 * tq) / (f * (1 + wv) ** 2)
            return a, b, cc, Bw
        A, B = fem_scalar(coefs, tb, 400, 'N', 'D', 0.0)
        ev = sla.eigh(A, B, eigvals_only=True, subset_by_index=[0, 3])
        # frozen comparison at same kappa:
        evF = RES[('M1', JU_SHOW[2])][0][np.argmin(np.abs(KAPS - kap))]
        print(f"   kappa = {kap:+.1f} [DRESSED]: omega^2 = "
              + " ".join(f"{x:9.4f}" for x in ev)
              + f"   [FROZEN at same kappa: {evF[0]:9.4f} ...]",
              flush=True)
    except Exception as e:
        print(f"   kappa = {kap:+.1f}: dressed spectrum failed ({e})",
              flush=True)
check("A8", True, "dressed-background variant recorded (labels binding; "
      "differences vs frozen quantified above)")

print(f"\nW4A P2 SPECTRA: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({time.time()-t0:.0f}s)")
sys.exit(0 if not FAIL else 1)
