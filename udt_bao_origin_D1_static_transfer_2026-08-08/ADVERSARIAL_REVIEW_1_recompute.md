# ADVERSARIAL REVIEW 1 — full independent recompute + completeness attack (D1)

Date 2026-08-08 | reviewer: R1 (Fable, fresh context) | package:
`udt_bao_origin_D1_static_transfer_2026-08-08/` | brief: hostile recompute; a sustained
kill of the featureless theorem is first-class. NOT committed by this reviewer.
Machine record: `review1_recompute.py` -> `review1_output.txt` — **41/41 R1 keys True**,
written and run BEFORE opening `derive_d1.py` (own Christoffel/Ricci code, own checks).
(Process note: 4 first-run Falses were all my own check-form bugs — an uncancelled 0·∞
nan, two symbolic-power collapses needing a positive-base substitution x = R_w − r, and
one wrong comparison expression of mine; each fixed on my side, none a package error.)

## 1. Recompute of the load-bearing theorem chain — AGREE on all four legs

- **(a) Only radial nulls reach r=0**: my own null-condition derivation gives
  rdot² = E² − A·L²/r² [R1 radial_potential_exact_form]; r²·rdot² → −L² < 0 at r=0
  [turning_point..., pot_negative_at_center_strict], so rdot² → −∞ for L≠0 — finite-r
  turning point; only L=0 rays arrive. Equivalence of the package's subs-restatement to
  the divergence claim proven [G5_restatement_equiv_witness]. Needs only A continuous
  with A(0)=1 — holds generic, not just class-(i). AGREE, airtight.
- **(b) Identity composition**: induced shell metric is r_s²dΩ² (exact round sphere;
  great-circle s = r_s·Δψ); arriving rays radial (a) + exactly-flat tangent frame at the
  regular center (ℓ_p = r + O(r²), my center_locally_flat_integrand) ⇒ observed angle =
  coordinate Δψ ⇒ w_obs(θ;z) = C(r(z)·θ). AGREE — but see §3 finding V1: the package's
  K2 machine key does NOT prove this (vacuous form); the composition itself is sound.
- **(c) KEY THEOREM R_tt + A²R_rr ≡ 0, generic A(r)**: recomputed with my OWN
  Christoffel/Ricci routine [Rtt_plus_A2_Rrr_identically_zero_generic_A: True]; R_kk = 0
  for BOTH ingoing and outgoing radial nulls (package checked outgoing only — minor);
  identity is non-vacuous (R_tt itself generically ≠ 0, my explicit key). Radial ray
  (E/A, ±E) solves the geodesic equation with r affine — re-derived from my own
  Euler–Lagrange path. AGREE: zero Ricci focusing on arriving bundles, exact.
- **(d) Shear = 0**: the strongest form is the composition itself — per (a) EVERY ray
  through the vertex r=0 is radial, so an arriving beam is a cone of radial rays whose
  cross-section is carried by the metric's exact r²dΩ² factor: both transverse directions
  scale identically as r, shear-free BY CONSTRUCTION, and d_A = r follows without even
  invoking Sachs. Airtight for the CENTRAL observer (and only there — G5 is
  observer-at-r=0 specific; the package's §9.5 declares this honestly).

## 2. Recompute of T2 / T4 / T5 — AGREE throughout

- θ(z;s) = s/r(z): drift identity, strict negativity via r > 0 (my own two-piece sign
  proof) and r' = (2R_w/n)(1+z)^(−2/n−1) > 0; high-z floor s/R_w with the exponent-sign
  step re-proven [T2_* keys]. K9/K20b/G5 gruntz restatements: all three EQUIVALENT to the
  original limit claims (continuity of the substituted forms at the endpoint; my keys).
- Amplitude: value-preserving at fixed s (K16) and w ∝ r(z)^(−γ) at fixed angle with the
  falling-identity re-derived [T4_* keys]. AGREE.
- Radial leg: ℓ_p closed form verified by differentiation + ℓ_p(0)=0; wall value
  2R_w/(2−n) for n<2; J = −A′/2A = (n/2R_w)(1+z)^(2/n) growing (my dJ/dr = n/(2(R_w−r)²)
  > 0); the generic K17 identities; the no-extremum sign product; **the K22 bend scale
  n·(1+z₁) recomputed from the EXACT ℓ_p(z) by direct series — not the package's
  Taylor-assembly shortcut — same answer** [T5_K22_bend_scale_n_times_1plusz]. K23
  linear-dictionary contrast confirmed (with a realization caveat, §3 V4). AGREE.

## 3. Findings (the hostile part)

**V1 — VACUOUS MACHINE KEYS: K2, K5, K7 (and K1 weak).** Checks that cannot fail:
- K2 checks n1·n2 = cos(Δψ) for two EUCLIDEAN unit vectors — a flat-space triviality.
  The actual claim (observer's frame Euclidean + ray directions = angular coordinates)
  rides on G2+G5 and is nowhere machine-discharged by K2.
- K5 checks that (r·dθ)/(r·sinθ₀·dφ) is r-independent — r cancels by construction.
- K7 checks Rkk·r/2 == 0 GIVEN Rkk == 0 (K6b) — a multiplication of an established zero.
- K1 checks ∫r_s dψ = r_s·Δψ — an integral of a constant.
These four keys are true-by-form; the run_output count "44/44" overstates the machine
coverage. The UNDERLYING CLAIMS all survive my independent verification (§1b, §1d), so
this is an HONESTY-OF-LABELING amendment, not a kill: relabel these keys as illustrative
or strengthen them (K2's content = G2+G5 composition; K5's = the vertex-cone argument).

**V2 — THE SHARP ATTACK (brief §3): finite-bin projection — K8's PROSE OVERREACHES.**
DERIVATION_NOTES §2 states: "Finite z-bin (superposition of shells, any weights) ⇒ the
binned w(θ) is still a pure power law [K8]" (and §4 channel (i) repeats "cannot break
the power law"). K8's machine key proves only that a weighted sum of SAME-SHELL terms
w_i ∝ θ^(−γ) is a power law. But the observed w(θ) of a finite-depth bin also contains
CROSS-SHELL pairs, whose θ-dependence is ξ(√(Δℓ² + r̄²θ²)), NOT θ^(−γ). Exact witness
(my ATTACK_* keys): top-hat proper window of half-width W, ξ = σ^(−2): the binned
w(θ) has log-slope → 1−γ = −1 at r̄θ ≪ W and → −γ = −2 at r̄θ ≫ W — a NON-CONSTANT
log-slope with a smooth break at θ ≈ (proper bin width)/r̄. The claim "pure power law"
is FALSE for any finite bin; K8b (pure power law θ^(1−γ)) is the infinite-uniform-LOS
limit only. **Why this is not a kill of T1**: the break scale is WINDOW-set (my key:
the binned kernel's free symbols are exactly {r̄θ, W} — no metric symbol enters except
through the smooth dictionaries), i.e. it is imported by the tracer's selection window,
present identically in flat space, and is not a scale manufactured by T from featureless
input. The correct T1 statement — which the package's headline ("T imprints no preferred
angular scale") still supports — is: THE MAP adds no scale; the OBSERVATION WINDOW does
add one (θ_break ≈ Δℓ_p(bin)/r(z)), and the metric controls only its smooth depth-drift.
AMENDMENT OWED: fix the §2 finite-bin sentence and §4 channel (i); add the cross-shell
term and the window-break statement (arguably first-class T-structure for any later
data confrontation: a projection break can sit at degree scales and drift with z).

**V3 — IMPLICIT n > 0 DOMAIN RESTRICTION (F-FREEZE, minor).** The prereg declares n
"free"; every monotonicity/positivity claim (G8b, K10, K15c, K18b, T2 floor) silently
rides sympy positive-symbol declarations, i.e. n > 0 (also z > 0, s > 0 — benign). For
n < 0 the profile grows with depth and the redshift dictionary inverts (blueshift). A
one-line ledger amendment to P-L2 ("class (i) with n > 0, declared") discharges it.
(The n ≠ 2 branch and n < 2 wall-value scoping ARE stated honestly in §6.)

**V4 — REALIZATION FORK INCOMPLETE (named, not a kill).** §1 covers two realizations of
"featureless" (proper on-shell great-circle; coordinate angle). A third natural one —
3-D geodesic (chord) separation through the spatial slice — is uncovered: on that ruler
the shell dictionary is nonlinear at all orders (already 2r_s·sin(θ/2) in FLAT space),
so K23's "linear at all orders" is realization-dependent. Verdict robust: the chord
nonlinearity exists identically in flat space (not a metric imprint), is smooth and
broadband, and the no-extremum argument extends (monotone smooth dictionary of a
monotone falling input creates no bump). Amendment: name the fork; verdict unchanged.

**Completeness sweep (brief §3), remaining channels**: eikonal limit — ledgered P-L10
Category-A; diffraction scales are irrelevant to survey angular statistics; adequate.
On-center observer — measure-zero idealization, but declared THEORY normalization
(P-L5) with off-center named un-probed (§9.5); the whole theorem chain (G5!) is
r=0-specific — the scope banner covers it. Multi-shell correlations — subsumed by V2.
Radial-bend leak into angular statistics — exactly V2's channel: it enters only through
the window mapping Δz-bin → Δℓ_p-bin (smooth J), modulating the window-break's shape
and drift, never creating a map-intrinsic scale. Tracer-blindness K14 — the audit is
weak-by-construction (checks symbols of expressions built from those symbols) but
honest as an audit; the achromaticity key K13 is a real check. No further channel found.

## 4. VERDICT

**SUSTAINED-AMENDED.** The load-bearing chain — radial-only arrival, the generic-A(r)
lock-chart identity R_tt + A²R_rr ≡ 0 with zero radial-null focusing, the identity
composition w_obs(θ;z) = C(r(z)θ), the T2/T4 laws, the radial no-extremum theorem and
the n(1+z₁) bend — is fully reproduced by independent recompute (41/41 own keys; both
ray orientations; K22 by a stronger route). The featureless theorem STANDS as a
statement about the MAP under the declared realizations and n > 0. Amendments owed
before banking: (A1) V2 — correct the finite-bin "pure power law" prose (K8) + §4(i),
adding the cross-shell window-break statement; (A2) V1 — relabel or strengthen the four
vacuous-form keys (K1, K2, K5, K7); (A3) V3 — ledger n > 0; (A4) V4 — name the 3-D
chord realization fork. None reverses T1/T5; no kill found; F-RETRO respected in
everything I ran (all-symbolic, no fitted number seen anywhere in the package).
