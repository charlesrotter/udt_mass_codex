# Whole-Metric Solution-Space Map — Open-Ended Scan (queue-head, 2026-06-13)

Status: working deliverable, NOT canonical (pending Charles). Driver:
Claude (Opus 4.8). Executes HANDOFF item 1 (Charles, 2026-06-13): broadly
re-solve the whole-metric solution space to find UNDOCUMENTED/anomalous
regions, in three steps — (a) state the documented baseline, (b) scan the
four under-explored axes, (c) flag + blind-verify each anomaly.

Method: agent-heavy. Baseline doc `solution_space_baseline.md`. Four
parallel scan agents (both phi + angular sectors LIVE, metric's own
derived operators, ADD/SLAVE/FREEZE nothing; GPU V100 torch float64 for
sweeps). Two flagged anomalies put through independent HOSTILE
default-refute blind verifiers. No mass-matching; no interior retreat; no
invention. Data-blind throughout.

Scan docs: ns_scan_results.md, ens_scan_results.md, ext_scan_results.md,
sf_scan_results.md. Verifier docs: ns_scan_verifier_results.md
(agent a9cfcd85385bff920), ens_scan_verifier_results.md (agent
a8a374f52ac4d3199).

================================================================
## THE HEADLINE (one genuine, blind-verified, undocumented region)

**THE NONSTATIONARY DIAGONAL SECTOR PROPAGATES HYPERBOLICALLY IN T.** The
banked theorem-grade negative #22 ("no sector propagates hyperbolically in
T; cells do not evolve"; nonstationary_opener_results.md) rests, in that
clause, on a SINGLE SIGN ERROR in its own verifier script (v_a3.py ~line
23 wrote the time-kinetic term as +f_T^2/f^2 — Euclidean/elliptic — where
the Lorentzian dilation-tie metric g_tt=-e^{-2phi}, g_rr=+e^{2phi} gives
-f_T^2/f^2 — hyperbolic). Independently re-derived from scratch by the
blind verifier:

- principal part of the metric's OWN field equation has signature (-,+,+),
  STRICTLY HYPERBOLIC in T uniformly; cTT/cRR = -e^{4phi} < 0 everywhere;
  wave speeds c_r^2=e^{-4phi}, c_theta^2=e^{-2phi}/r^2 positive-finite
  across phi in [-6,6], r in [.05,20].
- HIGH-k DISCRIMINATOR (the decisive test the verifier added, since an
  ill-posed Cauchy problem looks bounded at coarse resolution): with the
  CORRECTED sign the march stays bounded (maxabs ~1 at k=50); with v_a3's
  sign it blows up ~1e60 with growth RISING in k — i.e. the original
  "Hadamard ill-posedness" WAS the sign error.
- the wave is PHYSICAL not gauge: the Ricci scalar carries real
  phi_TT / phi_T^2 terms.

**This is a real character-change of documented behavior** — exactly the
kind of region the scan was commissioned to find. The diagonal class does
NOT cell-evolve into an elliptic dead end; it carries genuine hyperbolic
dynamics.

### What SURVIVES the correction (the negative is AMENDED, not voided)

The blind verifier independently reproduced two legs that the sign fix
does NOT touch:

1. LEG (b) — "MOTION NEVER SOURCES SHAPE." The fate-polynomial numerator
   2 f q v_h (f q v_r - v_h)^3 is f_T-FREE (re-derived from scratch,
   matches the banked polynomial). Even with T now propagating, C1 ALONE
   sources no SHAPED matter. The metric evolves; it does not thereby make
   structure.
2. THE OFF-DIAGONAL CLASS-B Q-PARTITION (the "0/6800 e_T never timelike"
   object) used R = fP + D2·v_T^2 with the CORRECT +D2 f_T^2 sign already;
   the diagonal sign error never touched it. Reproduced 7997/7997.
   CAVEAT the verifier surfaced (secondary, real): the "0/6800 / e_T never
   timelike" WORDING is metric-definition-sensitive — the verifier's own
   scan gives ~12.5% e_T-dominated, and v_a3's OWN C-3b check already
   FAILED in the original suite (45%, not the claimed >90%). The Class-B
   partition stands as a result; its strongest verbal claim is softer than
   recorded. Flagged for the off-diagonal frontier below.

### Registry action (mandated CONDITIONS-CHANGED mechanism; reversible)

#22 is flagged CONDITIONS-CHANGED on the clauses "no sector propagates
hyperbolically in T" and "cells do not evolve" (REFUTED in the diagonal
dilation-tie class via the v_a3 sign error), and the #5 elliptic lineage /
B3 propagation clause inherit it. #22's fate-polynomial leg ("motion never
sources shape") and the Class-B Q-partition STAND. Per the maintenance
rule the flag loses blocking authority on the propagation clause until
re-graded; it does NOT touch the no-shaped-matter conclusion. Nothing
canonical without Charles.

================================================================
## THE MAP — by axis

### Axis 1 — NONSTATIONARY / time-dependent  [ANOMALY CONFIRMED, scoped]
Documented baseline: elliptic-in-T, Hadamard-ill-posed, cells don't
evolve, motion never sources shape (#22). FOUND: the diagonal class is in
fact strictly HYPERBOLIC in T (sign-error correction, blind-verified). The
no-shaped-matter leg survives. NET: the dynamical CHARACTER of the
diagonal class is overturned (propagates); the matter-sourcing conclusion
is not. This is the scan's one genuine undocumented region.

### Axis 2 — MULTI-CELL / ensemble  [baseline holds; one chart lesson]
Documented baseline: like cells repel statically, flipped-sector dynamics
accelerate them together; single-cell compactness is a continuum (#33).
The scan's "single-centre ANISOTROPIC metric / no faithful two-centre
chart" claim was PARTIALLY-CONFIRMED then DOWNGRADED by the verifier: the
exact arithmetic survives (g^rr=e^{-2phi} dressed, g^thth=1/r^2 bare; the
naive isotropic-cylindrical chart genuinely is NOT the metric's operator,
which correctly explains a prior two-centre non-convergence) — BUT "bare
1/r^2 angular" is just the ordinary AREAL-RADIUS convention (identical in
Schwarzschild / any static spherical metric), a GAUGE statement, not a
UDT-specific anisotropy; a single cell HAS an isotropic conformally-flat
chart. "No faithful two-centre chart exists" is NOT proven — only that one
naive chart fails. The native welded-radial-chain object holds within
scope (angular dead at shared welds, compactness stays a continuum). REAL
OPEN OBJECT: the genuine finite-separation two-centre field in a
bispherical / Brill-Lindquist-isotropic chart (the GR-corpus "mine",
charter principle 4) — never solved.

### Axis 3 — EXTERIOR / medium  [baseline holds; method gap exposed]
Documented baseline: formation threshold c*=chat·gamma^2 (chat=0.498912),
formed depth diverges at threshold; linear-binding window shut. Sourceless
exterior closes cleanly (36/36, lobes relax to round). The ON-source
existence fold (Phi_c~0.19) is REAL but NOT exterior-special — the
interior control folds EARLIER (Phi_c~0.011-0.025); this is the already-
banked both-sided "formed depth diverges at threshold," not a new region.
The decisive angular test (does the #36 "pure-damping-about-round" gap go
NEGATIVE on a gradient-carrying medium -> a shaped type born in the
medium?) is UNRESOLVED: the symmetrized FD-Jacobian eigen-reading is an
ARTIFACT because the e^{-2phi}-weighted box is NOT self-adjoint in the
naive inner product (~18000 spurious negatives on a positive control). No
bankable exterior anomaly; the test needs the correct measure-weighted
self-adjoint generalized eigenproblem.

### Axis 4 — STRONG-FIELD / off-diagonal  [baseline holds in reach; frontier flagged]
Documented baseline: interior damps every angular shape to round,
Jacobian non-singular (no bifurcation), in the weak-ish trust window.
PROBE 1 (scalar deep core, exp(-2v)~3000, full nonlinear, NO
linearization): a raw Jacobian min|eig| turnover LOOKED like an
approaching bifurcation but was PROSECUTED and REFUTED as a grid/BC
artifact — the symmetric angular-restricted gap stays sign-definite. B1
(pure angular damping) holds into strong field, diagonal class. PROBE 2
(off-diagonal/shear ell=1, kappa->0.999, exact symbolic Hessian): CLEAN
NEGATIVE — shape stiffness grows faster than the phi-angular cross-block;
no off-diagonal type born. EXTENDS fork_tests #3 into strong field.

================================================================
## THE MAP-LEVEL FINDING (where the undocumented territory actually is)

The diagonal class is now largely CLOSED and well-understood: it
propagates hyperbolically in T (Axis 1), it damps angular shape to round
even at strong field (Axis 4 Probe 1), it sources no shape (Axis 1 leg b),
and its single-cell compactness is a continuum (Axis 2/3). The genuine
undocumented territory of the whole-metric solution space is CONCENTRATED
IN THE OFF-DIAGONAL / FULL-ROW ANGULAR SECTOR, and three independent axes
converge on it:

- Axis 4: the decisive off-diagonal-ON, self-consistent strong-field solve
  was NOT reached; the banked angular_completeness_results.md already shows
  that carrying the full off-diagonal row LIVE flips the centrifugal term
  to ATTRACTIVE and yields real-frequency oscillation CANDIDATES at
  ell>=2-3.
- Axis 3: the gradient-medium angular-gap test stalled on the SAME
  technical object — the e^{-2phi}-weighted box's non-self-adjointness;
  it needs the correct measure-weighted generalized eigenproblem (which is
  also how the off-diagonal row must be posed).
- Axis 1: the surviving Class-B partition's strongest verbal claim
  ("e_T never timelike") is itself off-diagonal and now shown soft
  (~12.5% e_T-dominated; original C-3b already failed) — the off-diagonal
  time/angular row is exactly where the record is least settled.

CONCLUSION: the metric's undocumented behavior lives in the OFF-DIAGONAL
ANGULAR ROW (the full, measure-weighted, self-adjoint angular operator
with the time/shear couplings live), NOT in the diagonal class the program
has been mapping. That is one coherent region, reached from three sides,
where (i) the centrifugal sign is reported to flip attractive, (ii) the
gap test is unresolved for lack of the right eigenproblem, and (iii) the
banked "no timelike T" claim is softest. It is the natural next scan.

## Caretaking
ORPHAN FILES (disowned by the completing scan agents; timestamps
16:06-16:07; likely partial artifacts of the first, rejected agent
launch): ns_scan_core.py, ns_scan_invariant.py, sf_scan_symcheck.py. NOT
load-bearing for any result above. Flagged for Charles before any
cleanup/commit (charter: inspect before deleting what you did not create).
