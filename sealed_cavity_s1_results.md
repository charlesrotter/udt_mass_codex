# Sealed Cavity — Stage S1 (Seal Control) Results

Status: working audit, not canonical. Created: 2026-06-11. Process:
one derivation agent (S1), one blind adversarial verifier (VS1: 21
independent checks; 18 PASS, 3 refutations/errata; own engine,
library re-integrated from jets at 1e-10). Ruling: SUFFICIENT FOR S2
WITH BINDING AMENDMENTS (below). New files only; backgrounds live in
/tmp/seal_s1/lib/ (not committed; reproducible from the header jets —
verifier-confirmed).

## Banked positives (verifier-confirmed)

1. CLASSIFIER CONVENTION CORRECTION: the fork-era relative cutoff
   (f_min/F) misclassifies near-threshold SAT flows (relative dip
   with absolute f_min >= 1, then ride-away — exhibits verified);
   the ABSOLUTE classifier is correct, cutoff-insensitive, and
   reproduces the banked c* = 0.206994 exactly. Bookkeeping rule
   extended: classifier convention must be stated with any c*.
2. ELL=3 TADPOLE closed form (independently re-derived, exact):
   T3(kappa) = sqrt(7)[(30k - 62k^3) - (15 - 36k^2 + 9k^4)L]/(48k^4).
3. CONVERGENCE OF THE SEAL LOCUS: c*(gamma=1) = 0.207001 / 0.158948 /
   0.141644 at ell<=1/2/3 (all verifier-reproduced to printed
   digits); seal-locus quantities (t_seal*, y_seal*, t_v,
   kappa_cross) converging under ell-extension; the c = 0.30 table
   rows reproduced to six decimals. THE IN-LAYER STATE DOES NOT
   CONVERGE (coefficient grows as (ellmax+1)^2/2); trust regions per
   background tabulated in the library headers.
4. THE BOUNDARY LAYER (verified): on-pole log law P_X =
   -(Y_X(pole)/4) ln(1/mu) + O(1); layer equation mu_tt - mu_t =
   -(N^2/2) ln(1/mu) + R, N^2 = (ellmax+1)^2 (slopes -2/-4.5/-8 at
   0.3-0.5%); finite-t touchdown with universal local exponent 1;
   layer FORM truncation-independent, coefficient divergent.
   Erratum (VS1): subleading term is mu = v*tau - (N^2/4)
   tau^2 ln(1/tau) (minus sign).
5. FORK-2 CERTIFICATION GAP CLOSED (strengthened): crossing-before-
   seal is a CONTINUITY THEOREM, truncation-free (exact slope
   identity => initial rise; IVT => a last downward f_min = 1
   crossing strictly before any seal; rise-dip-recover flows only add
   earlier crossings). Sealing-set monotonicity under ell-extension
   verified at seven c-values incl. ell<=4. The only extrapolated
   residue is sealing itself on the band (c*_inf, c*_ell3].
6. THE SEAL FLUCTUATION STRUCTURE (the S2 enabler; verifier-
   re-derived): rank-one Hessian law Hess(P) -> v v^T/(4 mu),
   v_l = Y_l(pole) = sqrt(2l+1); ALL log terms are proportional to
   v v^T (VS1 identified the exact cross-term cancellation S1
   missed); remainder O(ln 1/mu) in the vv^T direction, cross and
   complement blocks bounded (complement eigenvalues -> {0, 0.161,
   0.532}). Measure: S = int e^{-t}[(1/4) sum X_t^2 + P] dt, finite
   endpoint.
7. ADMISSIBLE BCs AT THE SEAL (verifier-confirmed per channel):
   - m=0 pole-value direction: limit-circle, sigma=0 branch
     log-divergent in C1 action => FINITE ACTION FORCES
     DIRICHLET/Friedrichs (delta-f(pole) ~ tau -> 0). Confirmed
     analytically AND by direct ODE solve (action slopes 1.159 vs
     1.152 predicted). The one forced condition.
   - m=0 complement (incl. the amplitude-homogeneity zero mode):
     regular => ONE-PARAMETER BC FAMILY per channel. (Caution for
     S2, VS1: the time-translation mode is a DIFFERENT object —
     delta-f(pole) = -v* with divergent action, excluded by the
     forced Dirichlet; do not conflate with the homogeneity mode.)
   - m=1 channels: limit-circle, BOTH branches finite-action =>
     FAMILY. Coefficient corrected by VS1: A_l1 =
     (2l+1) l(l+1)/(4D) — S1's value was HALF the true EL
     coefficient (missing factor 2; applies to every m != 0
     potential from S1's Mlm).
   - m>=2: regular => FAMILY.
   STANDING FLAG: finite action forces exactly ONE condition; every
   other channel keeps a genuine one-parameter family of admissible
   self-adjoint BCs. If S2 finds no native selector, the family is a
   physical degree of freedom of sealed cavities — a candidate home
   for discreteness. S2 scans it either way.
8. BACKGROUND LIBRARY (M1-M4; gamma = 1 at c = 1.3/2/4 x c*_3 and
   gamma = 0.5 at 2 x c*_3): verifier re-integrated M1/M2 from the
   header jets at ~1e-10 relative agreement; all shell figures and
   trust loci reproduced to printed digits; headers self-contained.

## Refutations (record)

- THE AITKEN LIMIT c*_inf = 0.1319 +- 0.0097 IS STRUCK (VS1 computed
  ell<=4 and ell<=5 itself: c*_4 = 0.132798, c*_5 = 0.127417;
  increment ratios GROW 0.360 -> 0.512 -> 0.608; the claimed central
  value is excluded by c*_5 alone). Replacement statement:
  c*_inf <= 0.119, best power-law estimate ~ 0.105-0.115, A POSITIVE
  LIMIT IS NOT ESTABLISHED (formation possibly threshold-free in the
  full-PDE limit — open). Nothing in S2 leans on c*_inf; the library
  members are comfortably supercritical.
- A_l1 factor 2 (above). Three-term-Aitken honesty note added to the
  bookkeeping rules: extrapolations from 3-term sequences with
  drifting ratios are not bankable.

## Binding amendments carried into S2

1. No use of c*_inf; residue band widened to (~0.11, 0.1416].
2. All m != 0 fluctuation potentials x2 (A_l1 = (2l+1)l(l+1)/(4D)).
3. Errata: layer subleading sign; O(ln) vv^T remainder; the
   time-translation-vs-homogeneity mode distinction at the seal.

## Verifier record

VS1: blind pass 2026-06-11; independent generic-lmax engine; 21
checks (18 PASS / 3 refutation-errata); library integrity immaculate;
ruling SUFFICIENT FOR S2 WITH AMENDMENTS. Driver note: both
load-bearing catches (the dishonest extrapolation, the factor 2)
would have propagated directly into S2's spectrum — the
verifier-before-record rule paid for itself again.
