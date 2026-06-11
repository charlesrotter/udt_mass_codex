# The Angular Completeness Audit — Results (THE ANGULAR FLIP)

Status: working audit, not canonical. Created: 2026-06-11.
Charles-ordered (his two directives shaped the result: "all
contributions discovered?" and "evaluated COMBINED SIMULTANEOUSLY,
not individually"). Process: one derivation agent (27/27 exact jets +
gauge + M2 numerics), one blind adversarial verifier (VAA: 46 checks,
44 PASS, 2 hostile probes that found real scheme-dependence; zero
refutations of the recomputed algebra; the gauge argument REPLACED by
a stronger mechanism). Metric-led. Data-blind. New files only.

## Headline (verifier-ruled): THE ANGULAR FLIP SURVIVES

Eliminating ALL couplable metric components SIMULTANEOUSLY (time row
a,b,p; g_rtheta = q; sphere-shape anisotropy w; axial u,v; k = 0 by
canon — the joint elimination, not the per-component one) gives, on
spherical backgrounds, EXACTLY:

L2_corr = -(c/2) sin(th) [ r^2 dpT^2
          + f0^2 r^2 (dpr^2 - 8 phi0_r dp dpr + 8 phi0_r^2 dp^2)
          - f0 dpth^2 - f0 dpv^2/sin^2(th) ]

Three signs flip: the banked time flip (W_A) AND BOTH ANGULAR
GRADIENT TERMS. The centrifugal term enters the corrected operator
with REVERSED (attractive) sign. Verifier-confirmed exact,
parameterization-safe at spherical, and GAUGE-PROTECTED by a stronger
argument than the audit's: regular chart-preserving gauge vectors DO
exist in every ell >= 1 channel (the audit's nonexistence claim is
refuted), but none are null directions — the symmetry breaking equals
exactly the Lie drag of the background densitized stress, with no
Einstein row to absorb it. No flipped term is gauge-removable.
Physical reading (amended): the eliminations impose first-order
vanishing of the DENSITIZED UPPER stress components
delta[sqrt(-g) T^{r theta}] = delta[sqrt(-g) T^{r phi}] = 0 — the
exact angular analogs of the algebraic weld.

## THE SPECTRAL CONSEQUENCE (verifier's decisive test)

The banked silence record IS genuinely conditional on the diagonal
metric class in its ell >= 1 channels:
- ell = 1: the flip only relocates relaxation rates (no real modes on
  every tested collar domain) — the banked ell = 1 conclusions
  survive in content.
- ell >= 2-3: REAL-FREQUENCY OSCILLATION CANDIDATES APPEAR — finitely
  many per channel (1 -> 6 as ell -> 6): A DISCRETE REAL-FREQUENCY
  LADDER PRODUCED BY THE ATTRACTIVE ANGULAR TERM, which the diagonal
  class structurally cannot produce. Computed on collar test domains;
  formed-cavity versions await the corrected-class backgrounds (the
  PDE run).
- ell = 0: identical operators up to overall sign — the W_A/measure-
  fork record is untouched (verified exact on arbitrary formed
  backgrounds in the enlarged scheme).
- The dpv flip is the strongest member: corrected/in-scheme = -1
  EXACTLY, background- and scheme-uniform, sourced entirely by the
  (u,v) elimination.

CALIBRATION (binding): these are CANDIDATES on test domains, not a
banked spectrum. The formed-background flip maps are SCHEME-
CONDITIONAL and off-shell (the q,w tadpoles mean the second variation
is taken off-shell in those directions on diagonal-class formed
backgrounds) — only spherical statements are bankable now; the
corrected-class spectrum on SELF-CONSISTENT backgrounds (q, w on) is
the decisive computation, owned by the full-PDE run.

## The completed table (verifier-amended)

- Tadpole row (twice-independent: jets + covariant stress route):
  k-refusal (known); q = g_rtheta tadpole (known, formed-only); NEW
  w-TADPOLE T_w = (c/4) f_theta^2 sin(th)/f (formed-only; global
  magnitude 3.8-4.5% of the k-refusal on M2's trust regions;
  pointwise up to ~0.5 at the trust edge). Zero tadpoles: a, b, p,
  u, v everywhere; q, w spherically. No missed components (the
  static/stationary class has 10 = 2 tied + 8 fields).
- AXIAL SECTOR: certified consistent exclusion AT m = 0 ONLY (no
  kinetic terms at any order; nondegenerate saddle, det =
  c^3(X+Y)^3/(64 r^8 sin^3) exactly; eliminates to zero). At m != 0,
  u and v MUST be carried — their elimination IS the dpv flip. p
  (g_Tphi fluctuation) is droppable always (fully decoupled,
  axisymmetric backgrounds).
- Degeneracy locus: det H_qw = 0 on X^2 + 7XY - 2Y^2 = 0
  (Y/X = (7+sqrt57)/4), entered inside M2's 5% trust region (not the
  1%); PLUS a scheme-dependent twin locus (Y = 3X in the canon-true
  areal scheme, also entered): q, w must be FIELDS in the PDE run, on
  three independent grounds.
- THE FIRST PHI-ANGULAR OPERATOR COUPLING: dpr x dpth cross terms
  prop. phi0_r phi0_theta on formed backgrounds — Charles's standing
  hunch, now an operator entry. Verifier flag: in the canon-true
  scheme, w's dynamics first enters at cubic order or on formed/
  q,w-on backgrounds — exactly where the hunch lives.

## The bundle/unification row (verifier: sound as graded)

The metric contains the U(1) the typed nodes need: A_phi = g_Tphi/f0
has the exact U(1) transformation law under xi^T = chi(phi); flux =
winding. But the carrier is the STATIONARY lifting (outside the
static class), flux quantization needs T-periodicity (an import), the
lambda = 1/2 doublet needs a T-frequency-charged probe, and the U(1)
direction is action-costly inside matter (flat only where
grad phi0 = 0). VERDICT: typed nodes and Galerkin amplitudes are
DISJOINT structures today; ONE bridge candidate named
(g_Tphi-as-connection; stationary or C-3 nonstationary lifting
required); the corpus's P2 postulate is RELOCATED, not derived.

## Registry consequences (applied in this commit)

The silence-record entries (#1, #2, #3, #5 and the S2 narrowing) gain
an explicit premise: DIAGONAL METRIC CLASS — their ell >= 1 channels
are CONDITIONS-CHANGED pending the corrected-class re-grade on
self-consistent backgrounds. Their ell = 0 content and all
time-sector results (W_A, measure fork) are unaffected. Blocking
authority over the discreteness program: suspended for ell >= 2
channels specifically.

## Full-PDE required-content list (final, verifier-amended)

1. Backgrounds: f + q + w simultaneously (k = 0 canon); the
   parameterization choice matters off-spherical — use the canon-true
   areal scheme and carry q, w as fields (never algebraic
   elimination).
2. Fluctuations: full even sector; at m != 0 include u, v
   (algebraic); p droppable; axial droppable at m = 0 only.
3. FIRST PHYSICS TARGET after validation: the corrected-class
   spectrum on self-consistent formed backgrounds — are the ell >= 2
   real-frequency candidates real cavity modes? (The native-
   discreteness question, live again, in the static sector.)
4. m != 0 backgrounds for ensembles phase.
5. The jet table needs re-derivation on q,w-on backgrounds (the
   current table's background class excludes exactly what the run
   produces).

## Verifier record

VAA: blind pass 2026-06-11; exact 4x4 adjugate route, covariant
stress cross-validation, joint linear-solve elimination, own spectral
test; 46 checks; the headline CONFIRMED with amendments (densitized-
stress reading; gauge mechanism replaced; scheme-conditionality of
formed maps; axial m != 0 correction). Driver note: the headline
finding exists because Charles demanded simultaneous evaluation — the
per-component audits could never have seen a three-sign joint flip.
