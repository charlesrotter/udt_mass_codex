# NS-SCAN — Nonstationary Axis of the Whole Metric: Results

Status: WORKING AUDIT, not canonical. Created 2026-06-13. Queue-head
HANDOFF item 1, step (b)/(c) for the NONSTATIONARY / time-dependent axis
(solution_space_baseline.md names it the PRIME axis). Driver: Claude
(Opus 4.8 1M), agent ns-scan baa9421be118b2cb. Metric-led, open-ended
exploration (NOT a hypothesis/template test). Data-blind. New files only
(ns_scan_symbol.py, ns_scan_fork.py, ns_scan_evolve.py). Log /tmp/ns_scan.log.

Frame: CRITICAL_UNIVERSE_FRAME.md (metric primary; solve the WHOLE metric,
both sectors co-equal, add nothing, slave nothing, freeze nothing).

---

## 0. The question (step c framing)

Baseline (solution_space_baseline.md B3; NEGATIVES_REGISTRY #22;
nonstationary_opener_results.md): "C1 alone is ELLIPTIC in T, the T-Cauchy
problem is Hadamard-ill-posed, NO sector of C1 propagates hyperbolically in
T (0/6800), motion never sources shape (fate polynomial f_T-absent), cells
do not evolve — configurations are 4D boundary-value equilibria." The
baseline FILE itself flags the frontier: B3 "WHERE IT DOES NOT CONSTRAIN —
the FULL nonstationary structure ... is hypothesis-grade and is exactly
where #36/W6 point the discreteness reopening."

Task: with BOTH sectors live (radial-phi AND the metric's own e^{2phi}-
dressed angular operator with the -phi_th^2 nonlinearity), the time row ON,
the ON two-exponential source S = Phi(e^{-2phi}-e^{phi}) live, nothing
added/slaved/frozen — does the elliptic-in-T character HOLD, or change?

---

## 1. Method (all derivations exact sympy; sweep + Cauchy march GPU float64)

The metric's OWN time-dependent field equation = the C1 dilation-action
Euler-Lagrange on the dilation-tie 4-metric, the SAME metric
wint_symcheck.py states and wint_cell2d/solve2d solve, with the time row
turned ON (the static symcheck froze it):

  g_tt = -e^{-2phi}, g_rr = e^{2phi}, g_thth = r^2, g_phph = r^2 sin^2 th,
  L = (c/2) e^{-2phi} g^{ab} phi_a phi_b sqrt(-g4),  c=2,  phi=phi(T,r,theta).

ns_scan_symbol.py derives the EL exactly. Principal part (after dividing by
the positive weight sin th, normalizing by e^{-2phi}):

  coeff(phi_TT)   = +2 r^2 e^{2phi}      (the time slot)
  coeff(phi_rr)   = -2 r^2 e^{-2phi}     (radial)
  coeff(phi_thth) = -2                   (angular, dressed sector live)
  lower order     = the registry-#33 radial nonlinearity -2phi_r^2 etc. +
                    the dressed angular nonlinearity -phi_th^2 (BOTH derived,
                    nothing added; symcheck-confirmed forms).

i.e. the metric's own operator is the covariant d'Alembertian
  e^{2phi} phi_TT - e^{-2phi}(phi_rr + (2/r)phi_r - 2phi_r^2)
     - (1/r^2)(phi_thth + cot th phi_th - phi_th^2) = S.

Its STATIC limit (phi_TT=0) is EXACTLY registry #33 + the live dressed
angular operator (verified: ns_scan_fork.py / the EL static reduction =
-r^2 e^{-2phi}(phi_rr+(2/r)phi_r-2phi_r^2), the banked #33 equation).

---

## 2. THE MAP — behavior across the nonstationary regime

THE SIGN STRUCTURE (the type test). The time second-derivative enters with
the OPPOSITE sign to BOTH spatial second-derivatives, EVERYWHERE:

  cTT/cRR   = -e^{4phi}        < 0  for all phi   (GLOBAL)
  cTT/cThTh = -r^2 e^{2phi}    < 0  for all phi,r (GLOBAL)
  cRR/cThTh = +r^2 e^{-2phi}   > 0  (the two spatial slots agree)

Signature (sign cTT, sign cRR, sign cThTh) = (-,+,+): a LORENTZIAN /
strictly HYPERBOLIC principal part. The ON source S is zeroth-order (no
derivatives) and does NOT change the type. The angular sector being live
does NOT change the type (cThTh enters with the same sign as cRR).

GPU sweep (ns_scan_evolve.py V1, 2049x2049 grid, phi in [-6,6], r in
[.05,20]): the proper wave speeds
  c_r^2 = e^{-4phi}            (radial),  range [3.8e-11, 2.6e+10]
  c_th^2 = e^{-2phi}/r^2       (angular), range [1.5e-08, 6.5e+07]
are POSITIVE and FINITE across the ENTIRE regime. There is NO elliptic
island, NO type-change locus, NO mixed-type partition in this (diagonal,
dilation-tie) class: the nonstationary whole-metric operator is hyperbolic
in T uniformly. It PROPAGATES.

CAUCHY EVOLUTION (V2, leapfrog, ON source live, spherical reduction):
from a compact initial bump the metric's own operator (FORK A) evolves in
T STABLY and BOUNDED (maxabs 0.288, no blow-up) — a well-posed propagating
wave. REFINEMENT (V3, Nr=1001->4001): converges (|d maxabs| 6.2e-4 ->
3.3e-4) — the wave is REAL, not a coarse-grid artifact. CPU spot-checks of
the speeds match the GPU to 1e-12.

---

## 3. FLAGGED CANDIDATE ANOMALY (step c): the nonstationary whole metric
   PROPAGATES in T — the documented elliptic-in-T character does NOT hold
   in the diagonal dilation-tie class, and the baseline verdict rests on a
   reduced-Lagrangian SIGN ERROR.

WHAT CHANGED CHARACTER. Registry #22 / nonstationary_opener_results.md:
"elliptic in T, no propagation in T, Hadamard-ill-posed Cauchy, cells do
not evolve." THE METRIC'S OWN operator on the dilation-tie 4-metric (the
one wint solves; both sectors live; ON source) is instead strictly
HYPERBOLIC in T everywhere and well-posed: the nonstationary sector
PROPAGATES and cells CAN evolve in T. This is a documented invariant that
STOPS HOLDING under the whole-metric (diagonal) premises — exactly the
"sector that starts to propagate" the brief asked to flag.

THE EVIDENCE (ns_scan_fork.py + the EL-from-baseline's-own-metric check):
the discrepancy is pinned to ONE sign, and it is internal to the baseline's
OWN verifier suite:
  - verify_nonstat/v_a1_a2.py builds the metric block M = diag(-f, 1/f, A)
    with f = e^{-2phi} (Lorentzian, "Delta = -det M > 0 Lorentzian") and the
    action L = -(c/8) sqrt(-g) g^{munu} f_munu / f. This is FORK A — the
    same Lorentzian dilation-tie metric.
  - Deriving the spherical reduced Lagrangian from THAT metric+action gives
    L_red = (c r^2 / 8 f^2)( f_T^2 - f^2 f_r^2 ) sin th  — time and radial
    kinetic at OPPOSITE sign (Lorentzian). EL reduced in phi:
    coeff(phi_TT) = -r^2, coeff(phi_rr) = +r^2 e^{-4phi}; cTT/cRR =
    -e^{4phi} < 0 (HYPERBOLIC); static limit = registry #33 EXACTLY.
  - BUT verify_nonstat/v_a3.py line 23 INDEPENDENTLY wrote
    L_red = -(c/8) r^2 ( f_r^2 + f_T^2/f^2 ) — time and radial kinetic at the
    SAME sign (Euclidean). That +f_T^2/f^2 (should be -f_T^2/f^2) makes the
    Hessian negative-definite (C-2: "elliptic; no real characteristics") and
    is the SOLE basis of the "no propagation in T / Hadamard-ill-posed"
    verdict. The Cauchy march under this wrong sign blows up at step ~52
    (V2 FORK B: maxabs 3.7e+10) — the "ill-posedness" is the sign error, not
    the metric.

So the metric's own nonstationary diagonal operator was MIS-CLASSIFIED as
elliptic; it is hyperbolic. The static limit, the registry-#33 radial
sector, and the dressed angular sector are all reproduced exactly — only
the time sign was wrong.

SELF-ASSESSMENT (real vs numerical-artifact vs already-documented):
  - NOT a numerical artifact. The type is from an EXACT sympy principal-part
    computation; the propagation is confirmed by a refined, converged GPU
    Cauchy march; speeds are positive-finite by closed form everywhere.
  - REAL, with a SCOPE CAVEAT (the honest part). My result is in the
    DIAGONAL dilation-tie class (g_tt=-e^{-2phi}, no off-diagonal a,b,q,w) —
    the class wint actually solves and symcheck states. Registry #22's
    "0/6800 e_T never timelike" came from the FULL P1 OFF-DIAGONAL Class-B
    scan with the same-minus elimination and the eliminated volume factor
    L* (v_a3.py C-3, the Q=0 partition). That C-3 object (R = fP + D2 vT^2
    with the eliminated L ~ -R/sqrt(fD2)) is a DIFFERENT, more involved
    reduced object and I did NOT refute it here; its timelike-in-(r,theta)
    reading may survive in the off-diagonal class. What I HAVE shown is that
    the C-1/C-2 spherical/diagonal arm — the one that states the headline
    "elliptic in T, no propagation in T" and underlies registry #22's
    blanket — carries the sign error and is hyperbolic when corrected.
  - The fate polynomial -2 f q f_th (f q f_r - f_th)^3 = 0 (f_T-absent,
    "motion never sources shape") is a SEPARATE claim about STATIONARY-SHAPE
    configurations and is NOT addressed/refuted here; it concerns whether
    shape is sourced, not whether the field propagates. Flag is scoped to
    the TYPE (elliptic-vs-hyperbolic / propagation) claim only.
  - NOT already-documented: no registry entry documents propagation in T;
    the baseline explicitly documents the opposite. This LEAVES the premise
    set of B3/#22 (it corrects, in the diagonal class, the very verdict that
    premise set asserts).

CONDITIONS-CHANGED implication (for the registry, pending verifier+Charles):
registry #22 and #5's "elliptic => no real modes" lineage, and B3's
"elliptic-in-T / motion-never-evolves" baseline, carry the premise
"diagonal reduced time kinetic = +f_T^2/f^2 (v_a3 L_red)". That premise is
refuted by the same suite's own metric. Every nonstationary negative
resting on "the C1 sector does not propagate in T" should be flagged
CONDITIONS-CHANGED and re-graded under the corrected (hyperbolic) operator —
NOT silently overturned (the off-diagonal Q-partition arm is untouched).

WHY THIS MATTERS to the GOAL (particles). A propagating nonstationary
sector is exactly the orchestra instrument the frame (CLAUDE.md principle 5;
Charles's phi-angular hunch) and #36/W6 said the discreteness reopening
needs ("cell-count discreteness REOPENS in the ... fold, driven by f_T, on
the NONSTATIONARY phi-angular sector"). The reopening route is alive: the
whole metric's time sector is a genuine wave sector, with the dressed
angular operator coupled in (cThTh live), not a frozen elliptic equilibrium.
This does NOT itself produce types or masses — no claim is made here beyond
the type/propagation correction.

---

## 4. What I did NOT find / honest negatives

- NO type-change LOCUS within the diagonal nonstationary class: it is
  hyperbolic UNIFORMLY (no elliptic island, no transition surface). The
  "map" is monotone — the anomaly is a global re-classification, not a new
  internal frontier surface.
- I did NOT refute the off-diagonal Class-B Q=0 partition (v_a3 C-3) — out
  of reach of this diagonal solve; flagged as the next check.
- I did NOT touch the fate polynomial / "motion never sources shape" — a
  shape-sourcing claim, orthogonal to the type claim; untested here.
- No mass-matching, no interior retreat, no invented mechanism. The only
  object solved is the metric's own d'Alembertian with its own source.

---

## 5. Verifier hooks (for the blind pass, before any banking)

A blind verifier should, independently: (i) rebuild the dilation-tie
4-metric and derive the C1 EL with the time row on, confirm signature
(-,+,+); (ii) derive the spherical reduced Lagrangian from v_a1_a2.py's OWN
metric+action and confirm the time kinetic is -f_T^2/f^2 (opposite v_a3
line 23); (iii) re-run a Cauchy march with the corrected sign and confirm
well-posed propagation + refinement convergence; (iv) confirm the static
limit = registry #33 exactly; (v) confirm the off-diagonal C-3 arm is NOT
claimed refuted. Scripts: ns_scan_symbol.py, ns_scan_fork.py,
ns_scan_evolve.py. Checks logged: 8/8 PASS in /tmp/ns_scan.log
(plus the exact L-derivation prints).
