# O2 — the native separation-measure table (exact derivation notes)

Date 2026-08-07 | branch grok | MODE OBSERVE | Status: **LEAD / UNBANKED** (two adversarial
reviews owed per the frozen contract). Contract: `PREREGISTRATION.md`. Script: `derive_o2.py`
(exact sympy, CPU, float-free; 33 machine checks; output `run_output.txt`). Not committed.
This table CHARACTERIZES; it selects nothing (F-PIN/F-SCOPE). No measure is "the" distance.

## Ground (cited at source; no code imported)
- `udt_xmax_O1_asymptote_2026-08-07/DERIVATION_NOTES.md` (+ CONSOLIDATED): the wall = a FAMILY
  of ideal boundary points; NO finite chain of typed-invertible comparison arrows attains it;
  load-bearing quantifier = chain LENGTH, not total depth — NO budget protection (infinite
  summable-depth chains with growing non-compact twists accumulate to the wall; witnesses
  R1/R2, total budget ~0.85); the partition theorem (compact twist additive, non-compact
  strictly super-additive).
- `udt_ceff_depth_orchestra_integration_2026-08-06.md`: invariant carrier = the RATIO
  c_eff(q)/c_eff(p) = lambda_t = e^{-2(phi_q-phi_p)} = (1+z)^{-2}; lock realization
  ds^2 = -e^{-2phi}c^2 dt^2 + e^{2phi}dr^2 (+ areal transverse under the areal anchor);
  under the lock A := e^{-2phi} (so g_rr = 1/A) and 1+z = A^{-1/2}.
- `simple_metric_L_native_optical_derive_results.md` (cite only): banked d_L/X = z(z+2) for L
  — machine-verified here to be exactly d_L = (1+z)^2 r [CROSSCHECK_dL_convention_L = True].
- `udt_copresence_popt_probe_2026-08-05/DERIVATION_NOTES.md` (08-05, F-LEGACY-legal): banked
  horizon signature — L: proper = 2X FINITE, optical reach INFINITE (ell_opt ∝ phi);
  exponential A = e^{-r/X}: proper INFINITE; quadratic A=(1-r/L0)^2: proper INFINITE; the
  finite-proper family A=(1-r/X)^{1/m} finite for m > 1/2 (their exponent 1/m; our n).

## 1. The approach-class parametrization (declared up front — F-SHOP-CLASS)

The near-wall profile is FREE DATA (O1/P-opt fork); verdicts are stated as FUNCTIONS of the
class parameters, never at a tuned point. Chart: the lock radial chart; A(r) = e^{-2phi(r)},
observer normalization phi(0) = 0.
- **Class (i): power-law wall at finite areal radius R_w.** A(r) = c_0 (1 - r/R_w)^n, n > 0,
  c_0 > 0. The L-profile is the single member (n=1, c_0=1, R_w=X) — carried as one witness
  among {n = 1/2, 1, 2}, never privileged.
- **Class (ii): exponential, wall at infinite chart radius.** A(r) = e^{-r/X}.
- **Class (iii): log-corrected power laws** — ADDED, and only because completeness demands
  it: two realization rows below have KNIFE-EDGE boundary cases inside class (i) (proper at
  n = 2, optical at n = 1, both log-divergent), and a logarithmic correction
  A = c_0 (1-r/R_w)^n (-ln(1-r/R_w))^{-p} is exactly the perturbation that resolves which
  side of the edge a profile falls on. Treated only at the two edges (sec. 3d).
- Wall check (every class): delta = -1/2 ln A DIVERGES at the wall — class (i)
  [i_depth_limit_wall = oo], class (ii) [ii_depth_limit = oo], and any class-(iii) member
  (A -> 0 pointwise). The parametrization covers A -> 0 walls; a profile with A bounded away
  from 0 has no wall and is out of scope by the frozen question.

## 2. ABSTRACT rows (chain-only; unconditional; tag = ABSTRACT / chain-only)

**(a) The depth cocycle delta_t itself.** DIVERGENT at the wall in every class and every
realization — definitional: the wall IS lambda_t -> 0, delta = -(1/2) ln lambda_t -> +oo
(O1 Q1; the extractor's divergence is the wall's definition). Verdict: DIVERGENT,
unconditional. By the banked reversal the lambda_t -> oo end is the same statement at -oo.

**(b) Leg count of finite chains.** Every finite chain has finite leg count by construction
and NEVER attains the wall (O1 amended theorem: groupoid invertibility + the reciprocal tie
closing the singular face on mu = 0). As a separation measure ("minimum number of comparison
legs to reach"), the wall sits at NO finite value — DIVERGENT/unattained, unconditional.
HONEST CAVEAT (O1 consolidated): an INFINITE chain accumulates to the wall — the protection
is the finiteness of the chain, not any budget carried along it.

**(c) Total depth budget along a chain, Sigma_i |delta_i|.** Honestly definable
(strain-invariant per leg, endpoint-frame invariant per O1 ground). NOT wall-protective:
O1's R1/R2 witnesses accumulate to the wall with SUMMABLE total budget (< 1; witness ~0.85)
via growing non-compact twists. So against the infimum-over-chains budget functional the
wall sits at a FINITE value (bounded above by the witnesses; whether the infimum is 0 is NOT
determined here and is not claimed). Stated neutrally: this is the one ABSTRACT row where
the wall is at finite separation — the budget row and the leg-count row DISAGREE, exactly
O1's "no budget protection" in measure-table form. In SR the same functional (rapidity
budget) IS protective; the non-compact twist channel is what breaks it (O1 partition
theorem, cited not re-derived).

## 3. REALIZATION rows (exact integrals to the wall; tag = REALIZATION + stated data need)

All integrals exact (sympy keys in brackets, `run_output.txt`). Class (i) substitution
u = 1 - r/R_w (wall = u -> 0+); class (ii) wall = r -> oo.

**(a) Proper radial length** int_0^wall A^{-1/2} dr. [needs: lock realization]
- Class (i): R_w c_0^{-1/2} int_0^1 u^{-n/2} du — **FINITE iff n < 2**, value
  2R_w/(sqrt(c_0)(2-n)) [i_proper_integral_and_condition; i_proper_closed_form_nlt2].
  Witnesses: n=1/2: 4R_w/(3 sqrt(c_0)); n=1: 2R_w/sqrt(c_0); n=2: DIVERGENT
  (logarithmic boundary case) [i_proper_witness_*].
- Class (ii): int_0^oo e^{r/2X} dr = DIVERGENT [ii_proper_divergent].

**(b) Optical / Fermat path** int_0^wall dr/A. [needs: lock realization]
- Class (i): (R_w/c_0) int_0^1 u^{-n} du — **FINITE iff n < 1**, value R_w/(c_0(1-n))
  [i_optical_integral_and_condition]. Witness n=1/2: 2R_w/c_0. **n = 1 (the L member) is
  EXACTLY the boundary case: logarithmically divergent** — partial integral to u is
  -R_w ln u exactly [i_optical_n1_partial_log_rate], i.e. ell_opt = 2 R_w delta/n at c_0=1:
  optical path meters depth linearly, and depth diverges. This reproduces the banked L
  slogan ("one tick of depth, one tick of optical path") as the n=1 knife-edge of a
  continuous family — structural flag, stated neutrally. n=2: power-divergent.
- Class (ii): int_0^oo e^{r/X} dr = DIVERGENT [ii_optical_divergent].

**(c) Light travel time** int dr/c_eff. [needs: lock realization] Under the lock with
observer normalization, c_eff(r) = c A(r) (ratio identity, cited ground), so
T = ell_opt / c IDENTICALLY [travel_time_equals_optical_over_c] — same verdicts as row (b)
in every class. Not an independent row; kept for honesty of enumeration.

**(d) Class-(iii) knife-edge resolution** (why the class was added). Declared convention
A = c_0 u^n (-ln u)^{-p} (p > 0 = log-ENHANCED wall approach, A smaller near the wall;
p < 0 = log-suppressed). Substitution t = -ln u throughout.
- OPTICAL n=1 edge: integrand 1/A = c_0^{-1} u^{-1} t^{p} -> int t^{p} dt: **FINITE iff
  p < -1** (log-suppressed approach) [machine check computed as int t^{-P} dt finite iff
  P > 1, iii_optical_n1_logcorrected_t^-p, with P = -p; witnesses P=2 finite = 1/ln 2,
  P=1 divergent].
- PROPER n=2 edge: integrand A^{-1/2} = c_0^{-1/2} u^{-1} t^{p/2} -> int t^{p/2} dt:
  **FINITE iff p < -2** [iii_edge_t^q_on_(log2,oo) with q = p/2].
Both edges are genuinely resolvable either way by log corrections — the power-law verdicts
at n=1 (optical) and n=2 (proper) are knife-edges, not class-stable facts.

**(e) Areal radius r.** [needs: lock realization + AREAL ANCHOR — chart-tagged; meaningful
only WITH the anchor (B = 1/A <=> areal transverse, canon C-2026-08-06-1)]
- Class (i): r -> R_w **FINITE** (definitional of the class) [i_areal_limit].
- Class (ii): DIVERGENT [ii_areal_limit].

**(f) Redshift z** (1+z = A^{-1/2}; ratio-invariant, cited ground — needs NO extra data
beyond the profile). DIVERGENT at the wall in EVERY class [i_redshift_limit_wall,
ii_redshift_limit] — equivalent to row 2(a): 1+z = e^{delta} exactly.

**(g) Luminosity distance d_L = (1+z)^2 r = r/A.** [needs: areal anchor + observable
convention; banked form verified: d_L/X = z(z+2) <=> d_L = (1+z)^2 r on L,
CROSSCHECK_dL_convention_L = True]
- Class (i): DIVERGENT for ALL n > 0 (r -> R_w > 0 finite, A -> 0) [i_dL_limit_wall].
- Class (ii): DIVERGENT [ii_dL_limit].

**(h) Angular-diameter distance — CONVENTION ADJUDICATED AT SOURCE.** The prereg's row list
wrote d_A = r/(1+z); the banked record has d_L = (1+z)^2 r (verified above), and the
Etherington relation d_L = (1+z)^2 d_A then FORCES **d_A = r** — the banked-consistent
convention, adopted. (d_A = r/(1+z) would give d_L = (1+z) r under Etherington, which is NOT
the banked d_L; the discrepancy in the prereg wording is flagged, not silently followed.)
- Adopted convention d_A = r: class (i) -> **FINITE limit R_w** [i_dA_limit_wall_convention_r]
  — the wall sits at finite observable angular size (an "angular-diameter horizon": an
  object of fixed proper size at the wall subtends a NONZERO minimal angle ~ size/R_w),
  while d_L and z diverge. Class (ii): DIVERGENT [ii_dA_limit_convention_r].
- Variant r/(1+z) = r sqrt(A), reported neutrally: -> 0 at the wall in BOTH classes
  [i_dA_variant_r_over_1pz_limit; ii_dA_variant_limit] (a third behavior: convergent to 0).
No convention is privileged as "the" distance; the adjudication is about matching the BANKED
record, not about physical preference (F-PIN).

**(i) Infalling observer proper time.** [needs: lock realization + a WORLDLINE POSIT — the
radial timelike geodesic of the realized metric; more structure than the pair itself, tagged]
Static metric => conserved epsilon = A c dt/dtau; radial geodesic gives
(dr/dtau)^2 = c^2(epsilon^2 - A), integrand 1/sqrt(epsilon^2 - A) -> 1/epsilon FINITE and
nonzero at the wall [i_infall_integrand_wall_limit, ii_infall_integrand_limit]. Finiteness
is therefore governed by the CHART RANGE alone: class (i) **FINITE for all n** (bounded
integrand, finite range; free fall reaches the wall in finite proper time); class (ii)
DIVERGENT (constant limiting speed dr/dtau -> c*epsilon over infinite range). A STATIC-chain
elapsed proper time is OBSTRUCTED as a pair-separation measure: it measures a duration
choice, not the pair (tagged O2-OBSTRUCTED(static-clock row), the obstruction is the row's
result).

## 4. Cross-checks against the banked record (verified, not assumed)

1. **L proper = 2X:** class-(i) n=1, c_0=1, R_w=X proper integral = 2X EXACTLY
   [CROSSCHECK_L_proper_eq_2X = True] — matches the banked copresence number (proper = 2X).
2. **L optical infinite:** n=1 optical is log-divergent with partial integral -X ln u =
   2X * delta at c_0=1 — matches the banked "ell_opt ∝ phi -> infinity" including the
   linear-in-depth RATE [i_optical_n1_partial_log_rate]. AGREES.
3. **Exponential proper infinite:** class (ii) proper DIVERGENT [ii_proper_divergent] —
   matches the banked exclusion integral. AGREES.
4. **Quadratic proper infinite:** n=2 proper DIVERGENT (log boundary)
   [i_proper_witness_n=2_divergent] — matches the banked A=(1-r/L0)^2 verdict. AGREES.
5. **The banked finite-proper family** A=(1-r/X)^{1/m}, finite for m > 1/2 (copresence
   review-B): their exponent is 1/m = our n; m > 1/2 <=> n < 2 — IDENTICAL to our criterion.
   AGREES.
6. **d_L convention:** banked d_L/X = z(z+2) on L is exactly (1+z)^2 r
   [CROSSCHECK_dL_convention_L = True]. AGREES; adjudication in 3(h).
No disagreement found with any banked cell.

## 5. THE TABLE (rows x classes; entries exact; F = finite, D = divergent)

| Measure (tag / data need)                     | Class (i) power, n>0        | Class (ii) exp | (iii) edges |
|-----------------------------------------------|-----------------------------|----------------|-------------|
| depth delta_t (ABSTRACT / chain)              | D (all n; definitional)     | D              | D           |
| leg count, finite chains (ABSTRACT / chain)   | wall unattained (O1)        | same           | same        |
| depth budget inf over chains (ABSTRACT/chain) | **F** (<= ~0.85; O1 no-budget-protection) | same | same |
| proper radial length (lock)                   | **F iff n < 2**: 2R_w/(sqrt(c_0)(2-n)) | D  | n=2: F iff p<-2 |
| optical / Fermat (lock)                       | **F iff n < 1**: R_w/(c_0(1-n)); n=1 log-D | D | n=1: F iff p<-1 |
| light travel time (lock)                      | = optical / c (identical)   | = optical/c    | same        |
| areal radius r (lock + areal anchor; chart)   | **F** = R_w (all n)         | D              | F = R_w     |
| redshift z (ratio-invariant; observable)      | D (all n)                   | D              | D           |
| d_L = (1+z)^2 r (areal anchor + observable)   | D (all n)                   | D              | D           |
| d_A = r (adjudicated; areal anchor + observ.) | **F** = R_w (all n)         | D              | F = R_w     |
|   [variant r/(1+z), neutral]                  | -> 0 (all n)                | -> 0           | -> 0        |
| infall geodesic proper time (lock + worldline)| **F** (all n)               | D              | F           |
| static-clock elapsed time                     | OBSTRUCTED (duration, not pair separation)  | —  | —       |

**DEGENERACY note (which measures always agree):** (1) travel time ≡ optical/c exactly, one
equivalence class. (2) z ≡ depth (1+z = e^{delta}) — the observable row IS the abstract
cocycle, divergent everywhere. (3) d_L ≡ z-class in wall behavior in both classes (r bounded
away from 0 near the wall). (4) In class (ii) ALL realization rows divergent except the
r/(1+z) variant (-> 0): near-total degeneracy — the finite/divergent SPLIT is a class-(i)
phenomenon. (5) In class (i) the split is graded by n: {areal, d_A, infall tau} finite for
ALL n; proper finite iff n<2; optical iff n<1; {depth, z, d_L} divergent for all n. Strict
inclusion: optical-finite => proper-finite => (areal/d_A/infall)-finite; never conversely.

## LANDED OUTCOME CLASS: **O2-TABLE** (completed, exact per-cell), with one
O2-OBSTRUCTED(row) entry (static-clock) and a real partial-degeneracy structure (sec. 5
note) short of O2-DEGENERATE. Falsifier discharge: F-PIN — no measure privileged; the d_A
adjudication matches the banked record only, both conventions reported. F-SHOP-CLASS — the
parametrization declared in sec. 1 before any integral; class (iii) added for stated
completeness reasons (knife-edges), not to make a wanted row finite; L appears only as
n=1 witness. F-SCOPE — no selection, no law, no kernel ruling, no x_max value. F-LEGACY —
only 08-05/08-06 banked material cited. Structurally notable cells, stated neutrally:
(A) the n=1 member sits EXACTLY on the optical knife-edge (log-divergent, rate = 2X*delta);
(B) d_A = r tends to the FINITE limit R_w at the wall in class (i) while z and d_L diverge
— a wall at finite observable angular size; (C) the abstract budget row is FINITE (O1's
no-budget-protection restated as a measure verdict) while leg-count protection holds.
LEAD / UNBANKED: two adversarial reviews owed (independent recompute + completeness attack;
F-PIN/F-SHOP-CLASS/scope + tagging honesty) before any banking. Not committed.

## CONSOLIDATED (2026-08-07, both reviews in): O2-TABLE SUSTAINED — AMENDED (no cell broken)

Files: ADVERSARIAL_REVIEW_1_cells.md (SUSTAINED-AMENDED; every cell independently reproduced, own
scripts, probe code never opened) + ADVERSARIAL_REVIEW_2_neutrality.md (AMENDED; all cells hand-
recomputed; F-PIN does not fire; F-SHOP-CLASS discharged). Amendments applied here; this section
supersedes the corresponding entries above.

**AMENDED/NEW TABLE ENTRIES:**
- **Depth-budget row (R1 settles the infimum): inf = 0 EXACTLY — the depth-only budget is
  DEGENERATE for the wall** (and globally at the abstract layer: any depth target at arbitrarily
  small budget; greedy chains reach lambda_t ~ 5e-22 at total budget 1e-3, every truncation regular
  and timelike-labeled). The prior "F <= ~0.85" materially understated.
- **NEW ROW (R1's completeness find): the FULL budget Sigma(|delta_i| + |w_i|) — depth PLUS twist —
  IS PROTECTIVE:** delta_comp <= full budget (operator-norm subadditivity; 0/200 numerical
  violations); the wall is DIVERGENT against the full budget. **This refines O1's "no budget
  protection": the depth-only budget is degenerate because the twist channel rides free; charge for
  twists and the SR-like budget functional EXISTS.** (Neutral structural fact; no selection.)
- **NEW CLASS (ii'):** power-decay walls at infinite radius (A ~ r^-alpha): all class-(ii) entries
  generalize EXCEPT the r/(1+z) variant (diverges/finite/0 for alpha</=/>2) — the "-> 0" was
  exponential-specific; tagged member-specific (R2 A3 + R1 B).
- Radial paths PROVEN length-minimizing (proper/optical rows are true distances, not path
  artifacts). Inclusion chain STRENGTHENED to profile-general (any A -> 0), converses refuted at
  witnesses. Leg-count cell now carries the infinite-chain caveat explicitly (R2 A4a). Infall
  proviso e^2 > sup A stated; c_0-vs-phi(0) cosmetic flag noted (verdicts unaffected). Parallax
  distance flagged as a candidate future row (non-blocking).
- **P-opt: the exact ONE-WAY arrow (R1):** within pure class (i) at c_0=1, P-opt <=> n=1 <=> the
  optical knife-edge (kappa = 2X); but knife-edge does NOT imply P-opt (class-(iii) counterexample),
  and P-opt is global while edge-status is asymptotic. "P-opt IS the knife-edge" was a loose gloss —
  the arrow direction is now stated. **LICENSE (R2 A2, verbatim duty):** this observation LOCATES
  P-opt in the class family and recovers its exact rate; it does NOT derive P-opt, does NOT upgrade
  its posit status, and edge-status is measure-relative (n=2 is the proper edge; every n is some
  functional's threshold) and not class-stable (log corrections move it) — selection content ZERO
  until a measure is chosen, which is Charles's guarded CP2 choice.
- "Angular-diameter horizon" DEMOTED from a coinage to an annotation (R2 A1): the neutral statement
  is "d_A = r -> R_w finite at the wall, all n, class (i)."

**STATUS: verified LEAD** (same-session reviews; external bar travels). Four-check: preregistered;
bounded scope stated; every load-bearing cell blind-verified by two independent recomputes;
premises/tags audited. **HANDOFF:** O3 is gated BEHIND Charles's CP2 ruling (the separation-type
choice, now ripe — the decision aid is in ADVERSARIAL_REVIEW_2 §5 verbatim); all O3 selection is
conditional on that ruling + the kernel posit; F-LAWHUNT remains in force.
