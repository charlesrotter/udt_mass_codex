#!/usr/bin/env python3
"""
ns_scan_invariant.py -- GAUGE-INVARIANT re-grade of the S2/S3 flags
===================================================================
Self-audit of ns_scan_core. Driver: Claude (Opus 4.8 1M). 2026-06-13.
NEW FILE. The S2/S3 flags used a COORDINATE-DOMINANCE heuristic for "which
direction is timelike" -- the SAME heuristic the original verifier v_a3
used for C-3b (which FAILED its own >90% threshold, 2298/5098). Coordinate
dominance of a Hessian eigenvector is NOT gauge-invariant. This file
replaces it with the ONLY frame-independent question that "does T
propagate" actually means:

  The reduced second-order PDE has principal part  H_{ij} d_i d_j u  (H =
  Hessian of the reduced Lagrangian in the velocity slots, i.e. the
  inverse effective metric g_eff^{ij}). The T-Cauchy problem is
  well-posed (T is a time function / the system is hyperbolic with T
  timelike) IFF the covector dT = (1,0,0) is TIMELIKE for g_eff, i.e.
  g_eff^{TT} = H_{TT} has the sign of the timelike eigenvalue AND the
  restriction of H to the dT=0 hypersurface (the (vr,vh) block) is
  DEFINITE with the opposite sign. Equivalently, for a Lorentzian H with
  signature (-,-,+): T is timelike  <=>  the 2x2 SPATIAL block obtained
  by deleting the T row/col is NEGATIVE definite (same sign as the two
  '-' eigenvalues) AND the full det has the Lorentzian sign. This is the
  standard 'dT is a time function' test and is GAUGE-INVARIANT (it only
  uses H, the actual effective metric, not eigenvector coordinates).

So: invariant test "T PROPAGATES at this point" :=
    H Lorentzian (one + eig, two - eig)  AND  the (vr,vh) minor of H is
    negative-definite (the constant-T slice is spacelike).
'theta/r marches, NOT T' := H Lorentzian AND the (vr,vh) minor is
    INDEFINITE (the + direction lies in the spatial (r,theta) plane, so a
    constant-T slice is timelike and T is NOT a good time function).

We recompute S2 (un-eliminated full symbol N0) and S3 (eliminated reduced
symbol, all q-roots) with THIS invariant. If the T-propagating count
collapses to ~0, the F-S2/F-S3 flags were my-own-diagnostic artifacts and
the baseline holds. If a robust population survives, it is a real,
undocumented propagating-in-T region.

Log /tmp/ns_scan.log (append). HYPOTHESIS-GRADE.
"""
import time
import numpy as np
import sympy as sp

t0 = time.time()
_fh = open("/tmp/ns_scan.log", "a")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()

log("\n" + "=" * 72)
log("ns_scan_invariant -- gauge-invariant re-grade of F-S2 / F-S3")
log("=" * 72)


def classify(H):
    """H = 3x3 symmetric effective-metric (principal-symbol) matrix in
    (T,r,theta) slots. Return one of:
      'def'   : definite (elliptic, no propagation in any direction)
      'T'     : Lorentzian AND constant-T slice spacelike => T propagates
      'space' : Lorentzian AND constant-T slice timelike  => T does NOT
                propagate (the timelike axis is in the (r,theta) plane)
      'deg'   : near-degenerate, skip
    GAUGE-INVARIANT: uses only signature of H and of its (r,theta) minor.
    """
    w = np.linalg.eigvalsh(H)
    aw = np.max(np.abs(w))
    if np.min(np.abs(w)) < 1e-9 * aw:
        return 'deg'
    npos = int(np.sum(w > 0))
    nneg = int(np.sum(w < 0))
    if npos == 3 or nneg == 3:
        return 'def'
    if not ((npos == 1 and nneg == 2) or (npos == 2 and nneg == 1)):
        return 'deg'
    # Lorentzian. minor = delete T row/col -> (r,theta) block:
    minor = H[np.ix_([1, 2], [1, 2])]
    wm = np.linalg.eigvalsh(minor)
    # constant-T slice spacelike <=> minor DEFINITE with the sign of the
    # majority (the two like-sign eigenvalues). For (-,-,+): majority '-',
    # T timelike iff minor is NEG-definite. For (+,+,-): majority '+', T
    # timelike (as a 'time' for the flipped convention) iff minor POS-def.
    if npos == 1:           # (-,-,+): physical Lorentzian, time = the '+'
        return 'T' if np.all(wm < 0) else 'space'
    else:                   # (+,+,-): time = the '-' direction
        return 'T' if np.all(wm > 0) else 'space'


# =====================================================================
# S2' -- un-eliminated full-metric principal symbol N0(a=b=0), invariant
# =====================================================================
f, r, A, q, vT, vr, vh = sp.symbols('f r A q vT vr vh', real=True)
M = sp.Matrix([[-f, 0, 0], [0, 1/f, q], [0, q, A]])   # a=b=0 time row
N0 = sp.expand((sp.Matrix([vT, vr, vh]).T * M.adjugate()
                * sp.Matrix([vT, vr, vh]))[0, 0])
Hn = sp.hessian(N0, (vT, vr, vh))
F_Hn = sp.lambdify((q, f, A), Hn, 'numpy')           # constant in v
D2 = A/f - q**2
P = A*vr**2 - 2*q*vr*vh + vh**2/f
F_Q = sp.lambdify((vT, vr, vh, q, f, A), f*P - D2*vT**2, 'numpy')
F_D2 = sp.lambdify((q, f, A), D2, 'numpy')

log("\nS2' -- un-eliminated symbol, GAUGE-INVARIANT type:")
rng = np.random.default_rng(20260613)
cnt = {'def': 0, 'T': 0, 'space': 0, 'deg': 0}
cntD2pos = {'def': 0, 'T': 0, 'space': 0, 'deg': 0}
for _ in range(60000):
    fv = float(np.exp(rng.uniform(np.log(0.1), np.log(10))))
    Av = float(np.exp(rng.uniform(np.log(0.1), np.log(10))))
    qv = rng.normal() * 2
    H = np.array(F_Hn(qv, fv, Av), float)
    c = classify(H)
    cnt[c] += 1
    if float(F_D2(qv, fv, Av)) > 1e-6:
        cntD2pos[c] += 1
log("  all samples:", cnt)
log("  D2>0 (physical) samples:", cntD2pos)
log("  -> the un-eliminated symbol type is set by (f,A,q) ALONE (the "
    "Hessian of N0 is v-independent); 'T' = T genuinely propagates.")

# =====================================================================
# S3' -- eliminated reduced symbol, ALL real q-roots, invariant test
# =====================================================================
log("\nS3' -- eliminated reduced symbol, all real q-roots, invariant type:")
fL, AL, qS, vTs, vrs, vhs = sp.symbols('fL AL qS vTs vrs vhs', real=True)
D2L = AL/fL - qS**2
PL = AL*vrs**2 - 2*qS*vrs*vhs + vhs**2/fL
RL = fL*PL + D2L*vTs**2
LB = -RL/sp.sqrt(fL*D2L)
H3 = sp.hessian(LB, (vTs, vrs, vhs))
gq = [sp.diff(sp.diff(LB, qS), v) for v in (vTs, vrs, vhs)]
hqq = sp.diff(LB, qS, 2)
F_H3 = sp.lambdify((vTs, vrs, vhs, qS, fL, AL), H3, 'numpy')
F_gq = sp.lambdify((vTs, vrs, vhs, qS, fL, AL), gq, 'numpy')
F_hqq = sp.lambdify((vTs, vrs, vhs, qS, fL, AL), hqq, 'numpy')
F_QL = sp.lambdify((vTs, vrs, vhs, qS, fL, AL), fL*PL - D2L*vTs**2, 'numpy')


def qroot_static(fv, Av, vrv, vhv, vTv):
    c3 = vTv**2
    c1 = fv*Av*vrv**2 + vhv**2 - (Av/fv)*vTv**2
    c0 = -2*Av*vrv*vhv
    if c3 < 1e-300:
        return [(-c0/c1, True)] if c1 != 0 else []
    rts = np.roots([c3, 0.0, c1, c0])
    out = []
    qstat = 2*Av*vrv*vhv/(fv*Av*vrv**2 + vhv**2)
    reals = [z.real for z in rts if abs(z.imag) < 1e-9*max(1.0, abs(z))]
    if not reals:
        return []
    conn = min(reals, key=lambda z: abs(z - qstat))
    return [(z, abs(z - conn) < 1e-12) for z in reals]


rng2 = np.random.default_rng(777)
stat = {'def': 0, 'T': 0, 'space': 0, 'deg': 0}
nonstat = {'def': 0, 'T': 0, 'space': 0, 'deg': 0}
examplesT = []
for _ in range(20000):
    fv = float(np.exp(rng2.uniform(np.log(0.1), np.log(10))))
    Av = float(np.exp(rng2.uniform(np.log(0.1), np.log(10))))
    vrv, vhv, vTv = rng2.normal(size=3)
    for qv, is_static in qroot_static(fv, Av, vrv, vhv, vTv):
        if Av/fv - qv**2 <= 1e-8:
            continue
        try:
            Hvv = np.array(F_H3(vTv, vrv, vhv, qv, fv, Av), float)
            gvec = np.array(F_gq(vTv, vrv, vhv, qv, fv, Av), float)
            hq = float(F_hqq(vTv, vrv, vhv, qv, fv, Av))
        except Exception:
            continue
        if not np.isfinite(hq) or abs(hq) < 1e-10:
            continue
        Heff = Hvv - np.outer(gvec, gvec)/hq
        if not np.all(np.isfinite(Heff)):
            continue
        c = classify(0.5*(Heff+Heff.T))
        (stat if is_static else nonstat)[c] += 1
        if c == 'T' and not is_static and len(examplesT) < 6:
            examplesT.append(dict(f=fv, A=Av, q=float(qv), vT=vTv,
                                  vr=vrv, vh=vhv,
                                  Q=float(F_QL(vTv, vrv, vhv, qv, fv, Av))))
log("  STATIC-connected root  :", stat)
log("  NON-static-connected   :", nonstat)
if examplesT:
    log("  examples of invariant T-propagation on non-static roots:")
    for e in examplesT:
        log("    ", e)

log("\n  VERDICT criteria:")
log("   - if S2'/S3' 'T' counts are ~0 => F-S2/F-S3 were coordinate-"
    "dominance ARTIFACTS; baseline (elliptic-in-T / T-never-marches) HOLDS.")
log("   - if a robust 'T' population survives in the physical (D2>0) "
    "region => a genuine undocumented propagating-in-T sector.")
log(f"\nns_scan_invariant done ({time.time()-t0:.0f}s)")
_fh.close()
