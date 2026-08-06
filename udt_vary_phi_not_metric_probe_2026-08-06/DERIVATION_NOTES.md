# Derivation notes — vary phi (metric from phi) vs vary metric freely

Mode: OBSERVE. Exact sympy (sympy 1.13.1, CPU, float-free). Status: UNBANKED LEADS.
c set =1 (premise: constant reference c_E scales only g_tt, irrelevant to vacuum structure).
Metric (R-areal, reciprocal lock, canon): ds^2 = -e^{-2phi(r)}dt^2 + e^{2phi(r)}dr^2 + r^2 dOmega^2.
phi(r) the ONLY field; r the fixed areal radius.

## Q1 — free-metric Einstein tensor (the wall)  [script q1_einstein.py; EXACT]

Mixed Einstein components G^mu_nu[phi, phi', phi'']:

    G^t_t = G^r_r = e^{-2phi} ( -2 r phi' - e^{2phi} + 1 ) / r^2
    G^th_th = G^ph_ph = e^{-2phi} ( 2 r phi'^2 - r phi'' - 2 phi' ) / r

KEY STRUCTURAL FACT (load-bearing): **G^t_t is IDENTICALLY EQUAL to G^r_r** on this ansatz.
(General static metric g_tt=-e^{2a}, g_rr=e^{2b}: G^t_t - G^r_r = 2(-a'-b')e^{-2b}/r, i.e.
proportional to (a'+b'); reciprocal lock a=-phi, b=+phi forces a'+b'=0 -> equal. Verified
q4_projection.py.)

Free-metric variation of int R sqrt(-g) demands G_{mu nu}=0. Independent content:
G^t_t = 0  =>  -2 r phi' - e^{2phi} + 1 = 0. dsolve gives (q2_phivar.py):
    -phi + (1/2)ln r + (1/2)ln(e^{2phi}-1) = C1
    <=>  e^{-2phi} = 1 - k/r   (k = integration const)  =  Schwarzschild / GR vacuum.
The angular component G^th_th=0 is then satisfied (Bianchi). So free-g forces the RIGID
one-parameter GR vacuum e^{-2phi}=1-k/r. THIS IS THE COLLAPSE WALL — confirmed.

## Q2 — phi-variation (the unblock candidate)  [q2_phivar.py; EXACT]

Reciprocal lock makes the volume element phi-free:
    sqrt(-g) = sqrt( e^{-2phi} * e^{2phi} * r^2 * r^2 sin^2 th ) = r^2 sin(theta).
Radial action integrand (drop constant 4pi, sin th, t-length):
    L(phi,phi',phi'') = R * r^2 = 2( -2 r^2 phi'^2 + 4 r phi' + r^2 phi'' + e^{2phi} - 1 ) e^{-2phi}.

Full Euler-Lagrange (2nd-order): E[phi] = dL/dphi - d/dr(dL/dphi') + d^2/dr^2(dL/dphi'').

    ============================================
    E[phi]  =  0   IDENTICALLY  (for EVERY phi(r))
    ============================================

The reduced EH action on the reciprocal-lock slice is a NULL LAGRANGIAN (total derivative);
its phi-variation vanishes identically. This is NOT G=0 re-labelled and NOT a nontrivial law
-- it is VACUOUS. Not a machinery artifact: the SAME EL code on two INDEPENDENT metric
functions a(r),b(r) returns the correct NONZERO Einstein equations (control, q3_verify.py).

WHY (mechanism, exact): the constrained phi-variation is the projection of delta S/delta g
onto d g/d phi. With d g_tt/d phi = -2 g_tt, d g_rr/d phi = +2 g_rr, the projection is
proportional to (G^r_r - G^t_t) -- exactly the combination the reciprocal lock annihilates
(Q1 fact). Hence 0. The lock aligns the field direction with the flat direction of S.

### Q2(a) distinct from Einstein? YES it differs from G=0 -- but by being EMPTY, not weaker-
and-nonvacuous. It is neither Einstein-in-disguise nor a genuine new law: it is 0=0.

### Q2(b) profile admission (EXACT):
 - L-profile c_eff=c_E(1-r/X), i.e. e^{-2phi}=1-r/X:  solves E[phi]? YES (trivially -- ALL
   phi do). Solves G=0? NO: G^t_t = -2/(X r) != 0 (exact). So G=0 FORBIDS it.
 - Schwarzschild e^{-2phi}=1-k/r: solves E[phi]? YES (trivially). Solves G=0? YES.
 - Any other profile (e.g. e^{-2phi}=1-(r/X)^2): solves E[phi] trivially; solves G=0 only if
   =1-k/r. So E "admits profiles G=0 forbids" -- but VACUOUSLY (it admits everything).

## Q3 — honest characterization

Effective source on an E-solution (take L-profile): T^mu_nu = G^mu_nu/(8 pi G/c^4);
G^t_t = -2/(X r) != 0 -> INTRINSIC nonzero effective stress-energy, not imposed. But it is
NOT SELECTED by the phi-law, because there is no phi-law: E[phi]=0 constrains nothing.
Determination: with the EH reference scalar, phi-variation gives ZERO equations for one field
-> the metric is COMPLETELY UNDETERMINED by this variation (orchestra flag, maximal): another
sector / a different (native) action must supply the phi-equation.

## Falsifier check
 - F-TRIVIAL: FIRES against reading this as UNBLOCK -- E[phi] is vacuous/auto-satisfied.
 - F-STEER: the owner-favorable read would call "admits L-profile G=0 forbids" an UNBLOCK;
   honest reading refuses it -- admission is vacuous (admits ALL), not a genuine weaker law.
 - F-IMPORT: EH used reference-only; g[phi] native. OK.
 - F-SCOPE: static/radial/EH-reference; no native action, no physics, no mass. Held.

## VERDICT (scoped, UNBANKED)
UNDERDETERMINED (degenerate extreme). On the static reciprocal-lock class, varying phi with
the EH REFERENCE scalar yields the IDENTICALLY-VACUOUS equation E[phi]=0 -- it escapes
Lovelock's forced-Einstein (it is NOT G=0) but escapes into VACUITY, not into a new law; the
EH scalar supplies NO phi-equation on this slice. Free-metric collapse to GR (e^{-2phi}=1-k/r)
is CONFIRMED the wall. Load-bearing step: reciprocal lock forces G^t_t = G^r_r, and phi-
variation projects onto exactly (G^r_r - G^t_t) = 0. Whether a DIFFERENT (native) action gives
a nonvacuous phi-law is the open door this leaves -- EH-reference does not.

## CONSOLIDATED (2026-08-06): NULL-CONFIRMED, RE-DERIVATION of banked 07-01; frame aliveness UNDETERMINED

Two adversarial reviews. `ADVERSARIAL_REVIEW_1_nulllagrangian.md` = NULL-CONFIRMED (independent
recompute: E[phi]≡0 exact; mechanism E[phi]=-2sqrt(-g)(A G^t_t + B G^r_r) = -2sqrt(-g)(G^r_r-G^t_t)
on the lock; profile-admission exact and VACUOUS — the probe's refusal of UNBLOCK is correct).
`ADVERSARIAL_REVIEW_2_interpretation.md` = RE-DERIVATION-ONLY + DEFER-RISK.

**What is CONFIRMED (exact, both):** varying phi with the EH scalar on the reciprocal lock gives
0=0 for every phi. The lock aligns the phi-direction with the flat (null) direction of the EH action.

**What this is NOT:** NOT new physics. Review 2 proved L = R·r^2 is exactly the total derivative of
the boundary term the **2026-07-01 native-field-equations work already banked** ("EH empty / phi-blind";
L - dB = 0, verified). New only in FRAMING (the Lovelock / vary-phi / projection lens), not in result.

**Frame status (honest):** the STRUCTURAL escape (constrained phi-variation != G=0, so not
Lovelock-forced) is real; but the one action tried produced ZERO law, so CONSTRUCTIVE aliveness is
UNDETERMINED. "EH is the wrong action" is a HYPOTHESIS, not a demonstrated status.

**Boundary term (driver F-STEER caught, both reviews):** the boundary term is nontrivial — it is the
Misner-Sharp mass F = 2r^2 e^{-2phi}phi' + 4m(r) (the edge energy; GHY-type) — BUT it fixes only
boundary DATA; it does NOT impose a profile-selecting phi-condition or a bulk law. "The physics is in
the boundary" was over-credited; credit the POINTER, not a mechanism.

**Narrow refinement (R1):** the null locus is {a+b=0} ∪ {b=0}; strictly the vacuity is the reciprocal
lock (a+b=0) OR b=0, and generic single-function ansätze ARE non-null (probe's core Q3 holds). Add
"reciprocal-lock-specific" to the scope stamp.

**DEFER-RISK (R2, forward):** concluding "so we need a different native action" quietly re-commits to
the ACTION-FIRST program that the law-order audit (LIVE.md) left OPEN vs response-first, and risks the
unfalsifiable "just find the right action." Do NOT charge into action-hunting as if obvious.

**Deep structural fact (reasoned, not a claim):** the reciprocal lock makes sqrt(-g) depth-independent
(clock e^{-phi} x ruler e^{phi} = 1) — so any PURE-CURVATURE (metric-only) volume action is depth-blind
on the lock. A native law that SEES depth must come from either the boundary (edge energy — data, per
above), an EXPLICIT phi-field term (native iff from positional dilation, not bolted on), or the
RELATIONAL/comparison structure (phi+orchestra strain — how depth is actually defined, NON-volume).
The last is the natural response-first home. Fork for Charles; nothing selected. Nothing banks;
four-check N/A (re-derivation + reviews; no new bankable result).
