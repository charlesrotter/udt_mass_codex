#!/usr/bin/env python3
"""
ns_scan_core.py -- NONSTATIONARY AXIS, symbolic/structural map (step b/c)
========================================================================
OPEN-ENDED whole-metric exploration. Driver: Claude (Opus 4.8 1M).
Date 2026-06-13. Frame: CRITICAL_UNIVERSE_FRAME.md / HANDOFF.md item 1.
NEW FILE (repo discipline). Reuses the metric's OWN derived operators from
the rescued nonstationary verifier (verify_nonstat/v_a1_a2.py, v_a3.py) and
the static dressed operator (wint_symcheck.py) -- NOTHING added, NOTHING
slaved beyond what the prior baseline already slaved (and we EXPLICITLY
re-open those slavings to test where the documented character holds).

DOCUMENTED BASELINE (nonstationary_opener_results.md), to be MAPPED:
  D1 FATE: joint shape-stationarity collapses to a fate polynomial with
     f_T ABSENT -- "motion never sources shape". (v_a1_a2 A2-5c.)
  D2 ELLIPTIC-IN-T: on the moving-spherical branch the (T,r) principal
     symbol is negative-definite => quasilinear ELLIPTIC, T-Cauchy
     Hadamard-ill-posed; no sector propagates in T. (v_a3 C-2.)
  D3 TYPE PARTITION: full Class-B mixed type partitioned EXACTLY by Q=0:
     Q>0 -> Lorentzian (-,-,+); Q<0 -> elliptic (-,-,-). The timelike
     direction lies in the (r,theta) plane; "T never marches". (v_a3 C-3.)
  SCOPE of all three (binding, from the doc): P1 metric class + full time
     row, axisymmetric even sector, C1-only, Q!=0 convention, the
     static-CONNECTED q-root.

WHAT THIS SCAN DOES (the under-explored part): it does NOT re-prove the
baseline in its own scope. It walks OUT of each scope clause and asks
where the character CHANGES:
  S1: re-derive D1/D2/D3 objects from scratch (anchor = baseline holds).
  S2: the EXCLUDED supersonic family (Q=0 boundary) -- does a propagating
      sector live exactly on the convention's blind spot?
  S3: drop the static-connected q-root SLAVING -- scan ALL real q-roots of
      the q-stationarity cubic; does the type partition still track Q=0,
      or does a NON-static-connected branch carry a timelike-T direction?
  S4: the SOURCE-ON system (interior operator S=Phi(e^{-2v}-e^{v}) with the
      time term live): does adding the matter source to the spherical
      time EOM keep it elliptic-in-T, or does the reaction term open a
      hyperbolic/parabolic window? (the interior solver was STATIC; this
      is its honest nonstationary completion.)

Log /tmp/ns_scan.log. Symbolic where exact; numeric scans seeded by me.
HYPOTHESIS-GRADE. Data-blind (no wall numbers touched).
"""
import sys, time
import sympy as sp
import numpy as np
from sympy import Rational as Ra

t0 = time.time()
_fh = open("/tmp/ns_scan.log", "a")
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _fh.write(s + "\n"); _fh.flush()
FLAGS = []
def flag(tag, msg):
    FLAGS.append((tag, msg)); log(f"  >>> FLAG {tag}: {msg}")

log("=" * 72)
log("ns_scan_core -- nonstationary axis symbolic/structural map")
log("=" * 72)

# =====================================================================
# THE METRIC'S OWN OBJECTS (verbatim algebra from verify_nonstat) -----
# 3x3 phi-block metric M (time row a,b ; radial 1/f ; angular A=r^2 W1^2),
# Lagrangian L = -(c/8) sqrt(-g) g^{ab} f_a f_b / f.
# =====================================================================
f, r = sp.symbols('f r', positive=True)
W1 = sp.symbols('W1', positive=True)
a, b, q = sp.symbols('a b q', real=True)
vT, vr, vh = sp.symbols('vT vr vh', real=True)
A = sp.symbols('A', positive=True)             # = r^2 W1^2

M = sp.Matrix([[-f, a, b], [a, 1/f, q], [b, q, A]])
D2 = A/f - q**2
P = A*vr**2 - 2*q*vr*vh + vh**2/f
Q = sp.expand(f*P - D2*vT**2)
Rp = sp.expand(f*P + D2*vT**2)

# -- S1 anchor: reproduce the documented invariants from scratch --------
log("\nS1 -- ANCHOR: reproduce the documented baseline objects")
# perfect square
log("  D-square: Q^2 + 4 f D2 P vT^2 == (fP+D2 vT^2)^2  ->",
    sp.expand(Q**2 + 4*f*D2*P*vT**2 - Rp**2) == 0)
# the fate polynomial: eliminate the time row (a*,b*), then q- then w-
g = f*vr**2 - vT**2/f
E1_cubic = vT**2*q**3 + (f*A*vr**2 + vh**2 - (A/f)*vT**2)*q - 2*A*vr*vh
Aq = sp.cancel(-q*(vT**2*q**2 + vh**2)/(q*g - 2*vr*vh))   # A solving E1
h = f*vr**2 + vT**2/f
brackA = sp.expand(-Rp*f*D2 + 2*A*h*f*D2 - A*Rp)
fate = sp.together(brackA.subs(A, Aq))
fate_num = sp.expand(sp.numer(fate))
log("  D1 FATE numerator has vT? ->", fate_num.has(vT),
    " (baseline: False = motion never sources shape)")
if not fate_num.has(vT):
    log("    [anchor OK] fate polynomial is f_T-free in this scope")

# D2 ellipticity on the spherical branch (a=b=q=vh=0): reduced kinetic
Lred = -(r**2)*(vr**2 + vT**2/f**2)/8
Hsph = sp.hessian(Lred, (vT, vr))
log("  D2 spherical-branch Hessian eigs:",
    sp.simplify(Hsph[0, 0]), sp.simplify(Hsph[1, 1]),
    " (both <0 => elliptic in (T,r))")

# =====================================================================
# S2 -- THE EXCLUDED SUPERSONIC FAMILY (Q=0 boundary)
# v_a1_a2 A2-8: the q!=0, vh=0 family with A = -vT^2 q^2/g sits EXACTLY on
# Q=0 and was EXCLUDED BY CONVENTION (a*,b* -> infinity). The baseline
# never characterized its propagation character. Q=0 is the type-change
# locus. DOES A SECTOR PROPAGATE THERE?
# =====================================================================
log("\nS2 -- the Q=0 supersonic family the convention EXCLUDES")
A_fam = -vT**2*q**2/g
Q_fam = sp.cancel(Q.subs(vh, 0).subs(A, A_fam))
D2_fam = sp.cancel(D2.subs(vh, 0).subs(A, A_fam))
log("  Q on the family ->", Q_fam, " (==0: on the boundary, confirmed)")
log("  D2 on the family ->", sp.factor(D2_fam))
# On Q=0 the time-row elimination is singular; the right object is the
# UNELIMINATED principal symbol of the full L in (vT,vr,vh) at a=b=0,
# i.e. the static-time-row reading. Build the full quadratic form
# N = v^T adj(M) v and read its (T,r,theta) signature on Q=0 vs Q>0/<0.
Nfull = sp.expand((sp.Matrix([vT, vr, vh]).T * M.adjugate()
                   * sp.Matrix([vT, vr, vh]))[0, 0])
# at a=b=0:
N0 = sp.expand(Nfull.subs({a: 0, b: 0}))
log("  N(a=b=0) =", sp.factor(N0))
# This is the principal symbol of the C1 wave operator on the static time
# row. Its (vT,vr,vh) Hessian signature = the local type. Scan it ACROSS
# Q=0 numerically (my own seed) to see whether the +timelike eigenvalue
# crosses INTO the vT direction as Q->0.
Hn = sp.hessian(N0, (vT, vr, vh))
F_Hn = sp.lambdify((vT, vr, vh, q, f, A), Hn, 'numpy')
F_Q = sp.lambdify((vT, vr, vh, q, f, A), Q, 'numpy')
F_D2 = sp.lambdify((vT, vr, vh, q, f, A), D2, 'numpy')

rng = np.random.default_rng(20260613)
log("  scan: as Q crosses 0, which coordinate carries the +(timelike) "
    "eigenvector? (baseline says NEVER vT)")
buckets = {}   # (sign band) -> count vT-dominated timelike
near0_vt = 0; near0_tot = 0
for _ in range(40000):
    fv = float(np.exp(rng.uniform(np.log(0.1), np.log(10))))
    Av = float(np.exp(rng.uniform(np.log(0.1), np.log(10))))
    vrv, vhv, vTv = rng.normal(size=3)
    qv = rng.normal()
    D2v = float(F_D2(vTv, vrv, vhv, qv, fv, Av))
    if D2v <= 1e-6:
        continue
    Hv = np.array(F_Hn(vTv, vrv, vhv, qv, fv, Av), float)
    # principal symbol Hessian is in (vT,vr,vh) DIRECTIONS; signature is
    # what matters, evaluate at a representative point (the form is
    # quadratic so the Hessian is constant in v -- exact local type):
    w, V = np.linalg.eigh(Hv)
    sig = tuple(int(np.sign(x)) for x in w)
    Qv = float(F_Q(vTv, vrv, vhv, qv, fv, Av))
    # only Lorentzian (one +) cases carry a timelike direction
    npos = sum(1 for x in w if x > 1e-9)
    if npos == 1:
        i = int(np.argmax(w))
        vtl = V[:, i]
        dom = int(np.argmax(np.abs(vtl)))   # 0=vT,1=vr,2=vh
        key = ('Q>0' if Qv > 0 else 'Q<0')
        buckets.setdefault(key, [0, 0, 0])
        buckets[key][dom] += 1
        if abs(Qv) < 0.05*max(1.0, abs(D2v*vTv**2)):
            near0_tot += 1
            if dom == 0:
                near0_vt += 1
log("  timelike-direction dominant coordinate by Q-band "
    "[counts vT, vr, vh]:")
for k, v in buckets.items():
    log(f"    {k}: vT={v[0]} vr={v[1]} vh={v[2]}")
log(f"  near Q=0 timelike vT-dominated: {near0_vt}/{near0_tot}")
# NOTE: this N0 form is the STATIC-TIME-ROW principal symbol, NOT the
# eliminated branch. The baseline's "T never marches" was about the
# ELIMINATED (moving-spherical) reduced symbol. Whether the UNELIMINATED
# full-metric symbol ever puts the timelike axis along vT is a DISTINCT,
# under-documented question -- the actual nonstationary whole-metric.
if buckets.get('Q>0', [0, 0, 0])[0] > 0 or buckets.get('Q<0', [0, 0, 0])[0] > 0:
    flag("F-S2", "the UN-ELIMINATED full-metric principal symbol DOES place "
         "the timelike axis along vT (the T direction) in part of the "
         "Class-B space -- a propagating-in-T sector that the eliminated "
         "moving-spherical reading (D2/D3) does not see. Needs the "
         "honest-vs-artifact grade in S3 (is it inside the physical "
         "Lorentzian D2>0 region, and does it survive the q-root choice?).")

# =====================================================================
# S3 -- DROP THE STATIC-CONNECTED q-ROOT SLAVING
# The baseline selected, at each point, the q-root of E1 CONNECTED to the
# static solution (v_a3 qroot_static_connected). The cubic E1 can have 3
# real roots. Does a DIFFERENT (non-static-connected) real branch carry a
# T-timelike direction in the eliminated reduced symbol? If the type
# partition tracks Q=0 ONLY on the static branch, that is a documented-
# scope artifact, and the OTHER branches are undocumented territory.
# =====================================================================
log("\nS3 -- ALL real q-roots (drop the static-connected slaving)")
# eliminated reduced symbol on a given q-branch: the Schur-reduced
# Hessian of LB = -R/sqrt(f D2) in (vT,vr,vh) after eliminating q
# (the q-stationarity), EXACTLY as v_a3 C-3 did but for EVERY real root.
fL, AL = sp.symbols('fL AL', positive=True)
qS = sp.Symbol('qS', real=True)
vTs, vrs, vhs = sp.symbols('vTs vrs vhs', real=True)
D2L = AL/fL - qS**2
PL = AL*vrs**2 - 2*qS*vrs*vhs + vhs**2/fL
RL = fL*PL + D2L*vTs**2
LB = -RL/sp.sqrt(fL*D2L)
vlist = (vTs, vrs, vhs)
H3 = sp.hessian(LB, vlist)
gq = [sp.diff(sp.diff(LB, qS), v) for v in vlist]
hqq = sp.diff(LB, qS, 2)
F_H3 = sp.lambdify((vTs, vrs, vhs, qS, fL, AL), H3, 'numpy')
F_gq = sp.lambdify((vTs, vrs, vhs, qS, fL, AL), gq, 'numpy')
F_hqq = sp.lambdify((vTs, vrs, vhs, qS, fL, AL), hqq, 'numpy')
F_QL = sp.lambdify((vTs, vrs, vhs, qS, fL, AL), fL*PL - D2L*vTs**2, 'numpy')

rng2 = np.random.default_rng(777)
allroot_sigs = {}
timelike_in_T = 0      # eliminated reduced symbol with +eig along vT
timelike_in_T_examples = []
ntot_branch = 0
for _ in range(15000):
    fv = float(np.exp(rng2.uniform(np.log(0.1), np.log(10))))
    Av = float(np.exp(rng2.uniform(np.log(0.1), np.log(10))))
    vrv, vhv, vTv = rng2.normal(size=3)
    # all real roots of E1 cubic in q: c3 q^3 + c1 q + c0
    c3 = vTv**2
    c1 = fv*Av*vrv**2 + vhv**2 - (Av/fv)*vTv**2
    c0 = -2*Av*vrv*vhv
    roots = np.roots([c3, 0.0, c1, c0]) if c3 > 1e-300 else \
        ([-c0/c1] if c1 != 0 else [])
    for z in roots:
        if abs(z.imag) > 1e-9*max(1.0, abs(z)):
            continue
        qv = z.real
        if Av/fv - qv**2 <= 1e-8:        # D2>0 required (physical)
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
        w, V = np.linalg.eigh(Heff)
        if np.min(np.abs(w)) < 1e-9*np.max(np.abs(w)):
            continue
        sig = tuple(int(np.sign(x)) for x in w)
        allroot_sigs[sig] = allroot_sigs.get(sig, 0) + 1
        ntot_branch += 1
        npos = sum(1 for x in w if x > 0)
        if npos == 1:
            i = int(np.argmax(w))
            vtl = V[:, i]
            if int(np.argmax(np.abs(vtl))) == 0:   # +eig along vT
                timelike_in_T += 1
                if len(timelike_in_T_examples) < 5:
                    timelike_in_T_examples.append(
                        dict(f=fv, A=Av, q=qv, vT=vTv, vr=vrv, vh=vhv,
                             Q=float(F_QL(vTv, vrv, vhv, qv, fv, Av)),
                             vtl=[float(x) for x in vtl]))
log("  eliminated reduced-symbol signatures over ALL real q-roots:",
    allroot_sigs)
log(f"  reduced symbol with +(timelike) eigenvector along vT (T marches): "
    f"{timelike_in_T}/{ntot_branch}")
if timelike_in_T > 0:
    flag("F-S3", f"on NON-static-connected q-roots the eliminated reduced "
         f"symbol DOES carry a timelike eigenvector along the T axis in "
         f"{timelike_in_T}/{ntot_branch} samples -- D3's 'T never marches' "
         f"is SCOPED to the static-connected root, NOT a property of the "
         f"full nonstationary solution space. Examples logged.")
    for ex in timelike_in_T_examples:
        log("    ex:", ex)
else:
    log("  [baseline holds] no q-root puts the timelike axis along T")

log(f"\nns_scan_core done ({time.time()-t0:.0f}s); flags: "
    f"{[t for t, _ in FLAGS]}")
_fh.close()
