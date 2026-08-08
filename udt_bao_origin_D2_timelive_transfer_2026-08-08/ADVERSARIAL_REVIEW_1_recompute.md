# D2 ADVERSARIAL REVIEW 1 — FULL INDEPENDENT RECOMPUTE + COMPLETENESS ATTACK

Date 2026-08-08 | reviewer: independent adversarial agent (blind recompute; derive_d2.py NOT
opened until own recompute complete) | package: `udt_bao_origin_D2_timelive_transfer_2026-08-08/`
| artifacts: `review1_recompute.py` -> `review1_output.txt` (**47/47 PASS**). No data, no BOSS,
bounded synchronous runs only. Hostile brief; kills hunted first.

## VERDICT: **SUSTAINED-AMENDED**

Every load-bearing claim reproduced independently. Five amendments owed (A1–A5 below), none
fatal; the §10 headline — anisotropy machinery real, scale-transparent, no native angular
scale, thresholds-not-scales, tracer phase forced — SURVIVES all of them.

## 1. Independent recompute (from the notes alone; 47/47)

- **Block spectrum**: charpoly factorization/radial decoupling, both disc identities, static
  roots, EXACT monotonicity dlam/d(mu²) = ±lam/√disc, product tie, K-coefficient
  1/(ρ²s²−1) + sign flip at ρs=1, immediate ellipticity at s=1/ρ — all reproduced.
- **Thresholds**: collision at λ=s/ρ at mu_c=|s−1/ρ| reproduced; eigenline eta-null EXACTLY
  at mu_c reproduced; the labeling-window/real-window COINCIDENCE adjudicated numerically
  (400 random draws, BOTH orderings ρs≷1, branch = continuous-to-1/ρ²): holds. This
  STRENGTHENS the notes (§2 states the min branch/ρs>1 case only; the coincidence is
  two-sided with mu_c = |s−1/ρ|).
- **Statistics**: K = ρ²/(2(ρ²s²−1)) re-derived by series AND checked against the exact
  branch numerically; dK/dρ closed form; deep limit 1/(2s²); Isserlis re-derived from the
  bivariate-normal MGF from scratch (Cov(k²,k²)=2C², third moments 0); coboundary
  covariance 2a⁴C² + 4a²s²k_p²C reproduced by direct moment expansion; featureless-sum
  lemma re-proven symbolically (log-slope = −E_w[g], derivative = +Var_w[g]); composition
  law reproduced.
- **Dragging**: independent null-geodesic derivation from the stationary block: drift² =
  h²/(AS(AS+h²)) ⇒ |dψ/dr| = h/(AS) + O(h³), E cancels EXACTLY (checked on the squared
  rational form), zero at h=0; coframe identities reproduced.
- **Depth law (the central new object)**: crest transport re-derived; assembly re-derived;
  and — beyond the package's own symbolics — an INDEPENDENT NUMERIC RAY-TRACE (RK4 on
  dt/dr=−1/A for A(t,r)=e^{0.13 sin t}(1−0.4r)^1.7, past-cone bisection, proper-period
  ratio) confirms d ln(1+z)/dr_s = −(A_r + A_t/A)/(2A) at three depths to <0.5%. The law is
  real, not an algebra artifact.
- **Fold + recovery**: fold ⟺ A_t=−A·A_r; static class-(i) gradient n/(2R_w q) DERIVED from
  A=q^n (derive_d2.py only asserts the form and checks positivity — gap closed here); G7
  dictionary, J recovery, all 8 static-recovery keys reproduced.

## 2. The six disclosed restatements — equivalence CONFIRMED

Five in-script disclosure blocks covering six keys (A6, B1, B6a, D3, F1a, F1b), matching §9's
count. A6/B1/F1a/F1b: the perfect-square √disc|₀ factored under s=1/ρ+w — exact, equivalent.
B6a: log-form equality — equivalent to the power-form solve (my solve concurs). D3: the
Subs-object chain rule — correct construction, honestly disclosed as replacing a WRONG earlier
Derivative-object construction; my independent algebra AND the numeric ray-trace confirm the
claim itself. No claim was weakened by any restatement.

## 3. Vacuous-key hunt

- **B6b IS VACUOUS as machine evidence** (the one real catch): it tests
  `theta_x.free_symbols == {K1,K2,g1,g2}` at the generic-abstraction layer — true by
  construction of theta_x from those very symbols. At the CHANNEL layer the crossover is
  θ_x^g = M a²/(2 s² k_p²) with a=1/ρ: free symbols {M, k_p, a, s, g} — it carries DEPTH and
  the screen ratio (recomputed, `S2_B6b_*`). See amendment A1.
- **E1 is vacuous-by-construction** (tests absence of symbols never introduced); the claim
  itself (operator carries only geometry/comparison symbols) is true by inspection of the
  audited expression list. Keep the claim, downgrade the key's evidentiary weight.
- **D4 is positivity-only** (asserted form n/(2R_w q), positivity by symbol assumptions);
  the derivation from A=q^n was not machine-checked in-script. Closed by this review.
- All other keys are substantive and correct.

## 4. Amendments owed (SUSTAINED-AMENDED)

**A1 (B6b + §3 wording).** "whose free symbols are the input AMPLITUDES only" and "set …
not by the map" are OVERSTATED. The coboundary crossover angle is amplitude-SET but
map-STEERED: θ_x(z) ∝ ((1+z)^{-2} M/(2s²k_p²))^{1/g} — its angular location DRIFTS with
depth through a²=(1+z)^{-2} and carries s. This is exactly the status D1 gave its window
break (window-set location, metric-steered drift) and should be stated with D1's honesty —
first-class map-plus-input structure, nameable for any later data confrontation. (The notes'
own C_k(θ_x) ~ (sρk_p)² line half-discloses this; the headline sentence contradicts it.)

**A2 (G1b prose / the P-D2-5 load, sharpened).** "the metric-level redshift shift is O(h²) —
coherent with the O(mu²) arrow layer" claims too much. G1b establishes only the COFRAME g_tt
deviation order. In the stationary realization itself, for STATIC emitters on p_ψ=0 rays the
observed redshift is ω=E/√A with g_tt=−A exactly h-INDEPENDENT at ALL orders — so the
realization exhibited does not (yet) realize the arrow-layer K·mu² anisotropy at all; no
coefficient match is shown, and which frame pair realizes the causally-labeled-branch
comparison is unspecified. This is the sharpest form of the package's own P-D2-5 review
directive: the channel-(i) coefficient K rides P-D2-5 (banked-lane extraction, exact at mu=0,
window derived) — legitimate as a FLAGGED premise, but the "coherent" cross-check should be
downgraded to "order-consistent; coefficient match and frame specification OPEN."

**A3 (completeness).** (a) Contract deliverable (iv) (map-vs-window re-checked time-live) is
only partially assembled: the pieces exist (time-live dictionary §4, per-direction J §7c) but
the D1-CONSOLIDATED question "does the live map move the break beyond smooth dictionary
drift?" is never answered as such, and the window break's behavior NEAR THE FOLD ONSET
(J→0 ⇒ θ_break = Δz_bin/(J·r) → ∞) is untreated. (b) Time-dependent mixing mu(t) along a
sightline is in no ledger row (SS2 covers direction-only; SS7 composition covers piecewise
legs — slow t-variation is arguably composition-covered, but it is not NAMED). Ledger lines
owed, not new machinery.

**A4 (Gaussian conditionality on the verdict line).** B5's no-feature conclusion needs its
POSITIVE-COEFFICIENT hypothesis, which Gaussianity supplies (third moments vanish; both
channel coefficients positive). Non-Gaussian featureless input reopens signed cross-terms
(Cov(k²,k) ≠ 0) and the lemma's hypothesis fails — the notes DO declare this (SS5, §3
"stated"), but the T1'/§10 verdict lines should carry the stamp "Gaussian-conditional (SS5);
non-Gaussian = stated argument only."

**A5 (minor).** §2's labeling statement is min-branch/ρs>1-scoped where the two-sided
mu_c = |s−1/ρ| coincidence holds (verified here) — state it two-sided; D4/E1 key weights per
§3 above; A9b is one algebraic link of a prose chain (chain confirmed here numerically).

## 5. Consistency adjudications the brief demanded

- **Featureless standard vs D1**: CONSISTENT. D1's window break is also a monotone-log-slope
  crossover, named a break and attributed to the window; D2 applies the same standard
  (no interior log-slope extremum = no localized feature; crossovers real, attributed to
  amplitudes/observer data) and itself names the analogy. A monotone-slope crossover CAN
  look like a break in binned data — true of BOTH packages equally; with amendment A1 the
  treatment is symmetric. The exact surviving statement is "no log-slope extremum" (no bump),
  which is the right standard for a BAO-like localized feature.
- **D2 fold vs D4 caustics**: SAME mathematical object. Static limit of D2's fold condition
  (A_t=0) gives A_r=0 — exactly D4's J=0 caustic locus, reachable statically only OUTSIDE
  class (i) (D4's supercritical nm>1 sign-changing profiles), which is precisely D2's D4-key
  scoping. The two packages are mutually consistent; D2 adds the time channel
  (A_t = −A·A_r with A_r ≠ 0). Checked (`S5_fold_static_limit_is_Ar_zero`).

## 6. What was hunted and NOT found

No smuggled float/fitted number (F-RETRO scan concurs); no silent freeze beyond the SS
ledger; no branch error in the extraction (branch forced by static recovery + continuity on
the near window); no channel found that MANUFACTURES rather than transports a scale — the
crossover (A1) is the closest candidate and it is input-data-set with map-steered drift,
D1-window-break class, not a native scale.

— ADVERSARIAL REVIEW 1, 2026-08-08. VERDICT: **SUSTAINED-AMENDED** (A1–A5). Not committed.
