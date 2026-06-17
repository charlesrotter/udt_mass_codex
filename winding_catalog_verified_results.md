# Winding Catalog — VERIFIED verdict (platonic ground states) — 2026-06-16

**Push:** Phase 3 of the fix-static-then-eigenvalue sequence (Charles 2026-06-16).
**Mode:** OBSERVE, DATA-BLIND (L=sqrt(kappa/xi)=1; no wall numbers).
**Status:** this doc is the VERIFIER-VALIDATED record. It OVERTURNS the stability claim
in winding_catalog_map_results.md (the first-pass build) — see "THE REVERSAL" below.
**Driver:** Claude (Opus 4.8, 1M), agent-fanned. Build agent a218fb0584ec4b080;
verifier agent ae8549549893f5bcd (its scripts run by the driver after it stalled).
**Tools (verified this session):** full3d_newton.py (Phase-2, category-A), full3d_grid_shexact.py
(SH-exact theta, regression-clean), sh_theta_operator.py. Audit scripts (committed):
verify_winding_hessian_2026-06-16.py (+ .log), verify_winding_platonic_2026-06-16.py,
winding_catalog_map.py.

## HEADLINE (regime-stamped)
UDT carries a DISCRETE catalog of topologically-protected winding (charge) sectors — m=1,2,3
all converge as distinct types. m=1 is the round, STABLE hedgehog. For m>=2 the AXISYMMETRIC
soliton is UNSTABLE to non-axisymmetric ("platonic") symmetry-breaking; the TRUE ground states
are NON-AXISYMMETRIC and substantially LIGHTER. This MATCHES the flat-space Skyrme/large-N-QCD
soliton structure (multi-solitons go platonic) — the UDT angular sector landing on QCD's own
classical face — now extended from static counting (N=3, q=1/3) toward the binding/shaping
DYNAMICS. Regime: p=0.4, kap8=0.05, grids Nr16-18 x Nth6-8 x Nps8; masses INTERIM (one grid,
not deep-floored for the platonic states). NOT YET banked: the platonic SYMMETRY per charge,
binding energies, grid convergence — that is the explicit Phase-3b follow-up.

## THE REVERSAL (why the first-pass stability claim is REFUTED)
winding_catalog_map_results.md claimed "NO psi-breaking negative mode in any sector — UDT does
NOT go platonic (opposite of Skyrme)." That claim was an ARTIFACT of TWO method bugs:
1. SIGN-BROKEN STABILITY PROBE: its finite-difference "secondvar" reported NEGATIVE (downhill)
   curvature even for m=1 — the round hedgehog that is DEFINITIONALLY the stable ground state.
   A probe that flags the known-stable state as unstable is invalid. (The raw m2_deep.json
   samples are ODD in amplitude => it measured a GRADIENT/non-stationarity, not a curvature.)
2. INEXACT THETA OPERATOR: the first pass used the Legendre theta operator, which is spectrally
   INEXACT for psi-dependent (m!=0) fields — it cannot represent the platonic downhill direction,
   so it artificially PINNED the soliton at the axisymmetric saddle and its relax-test "decayed
   back to axisym." On the SH-EXACT grid the pinning disappears (see below).
Per the project's hypothesis-discipline (aim verifiers hardest at hypothesis-CONFIRMING results),
this confirming claim was distrusted, re-tested, and overturned BEFORE banking.

## THE VERIFIED EVIDENCE
### A. Sign-calibrated energy-Hessian (verify_winding_hessian_2026-06-16.py)
Autograd FULL Hessian of the matter action wrt nodal Theta at the converged soliton (fixed
metric), restricted to the psi-BREAKING subspace; m=1 used as the sign-calibration anchor.
| m | Phi (converged) | lowest psi-break eigenvalue | n_neg (psi-break) | reading |
|---|---|---|---|---|
| 1 | 3.0e-12 | ~0 (−8e-14, i.e. machine zero) | **0** | STABLE — calibration PASS |
| 2 | 2.7e-15 | −223.6 | **30** | platonic-UNSTABLE |
| 3 | 5.2e-9  | −151.0 | **37** | platonic-UNSTABLE |
m=1 n_neg=0 (full_min eigenvalue +0.55, positive-definite) validates the sign convention; m=2,3
carry many strongly-negative psi-breaking modes => the axisymmetric m>=2 solitons are saddles.

### B. SH-exact platonic re-solve (verify_winding_platonic_2026-06-16.py)
On the SH-exact grid the m=2 BASE solve (from the analytic seed) spontaneously FALLS OFF the
round shape to a non-axisymmetric state:
  [m=2] base SH-exact: Phi 4.25e1 -> 1.2e-8,  M_MS = 13.40,  psivar = 0.297 (strongly non-axisym).
vs the AXISYMMETRIC m=2 saddle (Legendre-pinned): M_MS ~= 59. So the platonic ground state is
~4x LIGHTER than the axisym saddle. (Probe sweep injecting cos2psi onto the base converges to
nearby non-axisym states of slightly HIGHER mass, dM~+2.5 — consistent with the base being the
lower platonic branch. Full sweep + m=3 platonic state = Phase-3b.)

## CORRECTED MASS PICTURE (INTERIM — one grid, not deep-floored)
| sector | state | M_MS | note |
|---|---|---|---|
| m=1 | round, STABLE | ~0.298 | solid (Hessian-stable; #56 radial ~0.281, grid-dependent) |
| m=2 | axisym (saddle) | ~59 | UPPER BOUND only (30 neg modes) |
| m=2 | platonic (ground) | ~13.4 | INTERIM; the true ground state (psivar 0.30) |
| m=3 | axisym (saddle) | ~1024 | under-converged AND a saddle — DISCARD as a mass |
| m=3 | platonic (ground) | TBD | Phase-3b (Hessian says it exists; n_neg=37) |
The earlier "200x super-linear m=1->m=2" was a SADDLE artifact. The ground-state ratio
m=1->m=2 is ~0.30 -> ~13.4 ~= 45x — still strongly super-linear (gravitational self-binding,
absent in flat Skyrme), but far less extreme. Bank no ratio until deep-floored + grid-converged.

## CATEGORY-A / discipline
All solves category-A (full3d_newton value-equivalent to the committed residual to 1.4e-14;
B=1/A free, maxB1A 0.19-5.1; SH-exact grid regression-clean on the round). No injected term,
no tuning, no linearization-as-result. winding_catalog_map.py works around a latent NameError in
full3d_spectral.matter_action's return (dead code) — does not alter physics. The first pass's
secondvar probe is RETIRED (sign-broken); use the autograd Hessian (verify_winding_hessian...).

## COMPLETENESS-MAP IMPACT (the ten criteria)
- crit-6 (topological sector): m=1,2,3 converge as distinct protected types — COVERED (existence).
- crit-8 (branch/bifurcation = CATALOG): a discrete winding catalog EXISTS; AND within m>=2 there
  is a bifurcation axisym-saddle -> platonic-ground. The catalog is NOT a continuum here. Partial:
  the platonic branch masses/symmetries unmapped (Phase-3b).
- crit-9 (stability spectrum): m=1 stable; m>=2 axisym unstable (calibration-valid Hessian). The
  platonic ground states' OWN stability is the next check.
- DROPPED: deep-floor + grid convergence for platonic masses; the platonic SYMMETRY per charge
  (toroidal? tetrahedral? cubic?); binding energies; the FULL coupled (gravitational) Hessian
  (here the Hessian is matter-sector at fixed metric — a strong but not complete stability test).

## STANDING-QUESTION ANSWERS (push: winding catalog + platonic)
1. COVERS: existence of a discrete winding catalog (crit-6/8) + the axisym-vs-platonic stability
   bifurcation for m=2,3 (crit-9). DROPS: platonic masses/symmetries/binding; full coupled Hessian.
2. Dropped hosting structure? YES — the platonic branch (its symmetry IS the candidate baryon
   geometry) is unmapped => flagged, the Phase-3b target.
3. REGIME: p=0.4, kap8=0.05, Nr16-18 x Nth6-8 x Nps8; masses interim.
4. Category-A? YES (value-equiv 1.4e-14; B=1/A free; SH-exact regression-clean). No category-B.
5. Tooling next: deep-floor + grid-converge the platonic states on the SH-exact grid; identify
   the symmetry group per charge; compute binding; the full coupled-Hessian stability of the
   platonic ground states.
6. ONE tile: the platonic ground-state MAP (symmetry/mass/binding per charge) is still BLANK;
   newly filled = the catalog EXISTS + m>=2 ground states are platonic (verifier-validated).

## NOTE for the record
winding_catalog_map_results.md (first pass) is SUPERSEDED on its stability/no-platonic claim by
THIS doc. Its existence/convergence observations (sectors converge; m=2 axisym M~59; super-linear
axisym masses) stand only as the AXISYM-SADDLE branch, re-labeled here as upper bounds.
