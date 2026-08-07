# O3 — approach-profile classes + the conditional selection map (exact derivation notes)

Date 2026-08-07 | branch grok | MODE OBSERVE/characterize | Status: **LEAD / UNBANKED**
(two adversarial reviews owed per the frozen contract). Contract: `PREREGISTRATION.md`.
Script: `derive_o3.py` (exact sympy, CPU, float-free; 94 machine-check keys, all True;
runtime ~2 s; output `run_output.txt`). Not committed. Every selection statement below is
CONDITIONAL per branch ("IF the kernel's spatial is S_k, THEN ...") under Charles's CP2
no-pin ruling; no branch is privileged (F-PIN). No n is selected, no law stated (F-LAWHUNT).

## Ground (cited at source; every O2 cell USED here was re-derived independently in the script)

- O1 CONSOLIDATED (`udt_xmax_O1_asymptote_2026-08-07/`): wall = family of ideal boundary
  points; no finite chain attains it; load-bearing quantifier = chain LENGTH; depth-only
  budget unprotective (infinite-chain witnesses).
- O2 CONSOLIDATED (`udt_xmax_O2_measure_table_2026-08-07/DERIVATION_NOTES.md`, CONSOLIDATED
  section supersedes body): the measure table; inclusion hierarchy optical-finite =>
  proper-finite => areal/d_A-finite (profile-general, converses refuted); depth-only budget
  inf = 0 (degenerate); FULL budget (depth+twist) protective; d_A = r (Etherington-forced,
  banked-consistent); the P-opt one-way arrow + LICENSE (quoted verbatim in D3 below).
- c_eff integration (2026-08-06): lock realization ds^2 = -e^{-2phi}c^2dt^2 + e^{2phi}dr^2
  (+ areal transverse under the areal anchor); A := e^{-2phi}, g_rr = 1/A; depth
  delta = -(1/2)ln A; 1+z = e^delta = A^{-1/2}. Wall = A -> 0.
- Kernel posit (THEORY, owner posit, derivation held): x_max EXISTS and is finite in the
  kernel's spatial sense. O3 characterizes what it selects, never proves it.

## 1. Setting and the frozen family (F-SHOP-CLASS; prereg §3, no additions)

- (i)   A = c0 (1 - r/R_w)^n = c0 u^n, n > 0 (u = 1 - r/R_w; wall u -> 0+, finite chart
        radius R_w). L is the n=1 member — witness only, never privileged.
- (ii)  A = e^{-r/X} (wall at infinite chart radius).
- (ii') A = (1 + r/X)^{-alpha}, alpha > 0 — **exact representative declared here**: regular
        at r=0 with A(0)=1 (matches observer normalization phi(0)=0), ~ (r/X)^{-alpha}
        asymptotically. (The (r0/r)^{-alpha} form is singular at r=0; not used.)
- (iii) A = c0 u^n (-ln u)^{-p} at the class-(i) knife edges (p>0 = log-enhanced wall,
        A smaller near the wall; O2's declared convention kept).
- Essential-singularity walls A ~ e^{-1/(R_w - r)}: NOTED-ONLY coverage limit (outside the
  frozen family); entries below are hand-checks, every key tagged `ESS_*`.
- Window reparametrizations used throughout the script (so open ranges are exact, no
  Piecewise): q = (2-n)/2 > 0 encodes n < 2; w = 1-n > 0 encodes n < 1; g > 0 = generic gap.

## 2. THE LOAD-BEARING DISTINCTION: distance-role vs rapidity-role branches

Within the frozen family, some rows CAN carry a finite wall value while others necessarily
diverge — SR's structure (CP1): the bounded speed variable vs the divergent rapidity. WHICH
role the kernel's "spatial" plays is Charles's open choice (CP2 no-pin); the split below
classifies the ROWS, it does not assign the KERNEL. Divergence of a depth-like row is therefore
NOT a failure of the posit; it is the gamma-asymptote statement itself (CP1). The two roles:

- **DISTANCE ROLE (can host "x_max finite"):** a branch where the wall CAN sit at finite
  separation for some family member. Found: **S1, S2, S3, S7** (each with its own surviving
  subfamily, §3), plus **S4 in exactly one genuine member** ((ii'), alpha=2 — §3, a
  surprise). The posit is a live selection statement only on these branches.
- **RAPIDITY ROLE (necessarily divergent; the asymptote statement):** **S6** (z ≡ depth:
  divergent in every class, definitionally — its divergence IS CP1), **S5** (d_L: divergent
  in every class; d_L's divergence is depth-driven (the (1+z)^2 factor; the exact identity
  ln d_L = 2*delta + ln r [S5_lndL_identity_2delta_plus_lnr]) — near the wall
  d_L = R_w e^{2delta}(1+o(1)), so the row plays the rapidity role), **S8** (the FULL budget:
  divergent at the wall, O2 consolidated — and this divergence is exactly wall-PROTECTION,
  the SR-like reading: the wall is unreachable AND infinitely costly; the gamma-asymptote
  reading needs NO finite value in this branch), and **S9b** (leg count: the wall sits at
  no finite value; O1's finite-chain theorem; infinite-chain caveat travels).
- **DEGENERATE (fails both roles):** **S9a** (depth-only budget: inf = 0 exactly, O2
  consolidated — the wall at ZERO separation from everything; trivially "finite" but with
  zero selection content; obstruction-grade as a spatial-distance candidate) and **S4 in
  all other members** (value -> 0 at the wall non-monotonically: the wall at zero
  separation, the measure non-injective — §3).

So: IF the kernel's spatial sense is S1/S2/S3/S7 (or the single genuine S4 member), the
posit selects (§3); IF it is S5/S6/S8/S9b, the posit is unsatisfiable in the frozen family
and the honest statement is the modus tollens of §3 — while S6 and S8 are exactly where the
wall behaves like SR's c. The pair (finite distance-role value, divergent rapidity-role
value) is the gamma-asymptote structure, now split cleanly across the O2 rows.

## 3. D1 — THE CONDITIONAL SELECTION MAP (branch x class; keys in brackets; F=finite, D=divergent)

Question per cell: does the wall sit at finite S_k-separation for this family member?
"Posit satisfiable" = some member admits it; "surviving subfamily" = exactly which.

| Branch (tag/data need) | (i) power n>0 | (ii) exp | (ii') (1+r/X)^-a | (iii) edges | ESS (hand-check) |
|---|---|---|---|---|---|
| S1 proper (lock) | F iff n<2, = 2R_w/(sqrt(c0)(2-n)) [S1_i_*] | D [S1_ii_divergent] | D (all a) [S1_iiprime_*] | n=2 edge: F iff p<-2 [S1_iii_edge_*] | D [ESS_exp_*, ESS_harmonic_divergent] |
| S2 optical ≡ c·travel (lock) | F iff n<1, = R_w/(c0(1-n)); n=1 log-D [S2_i_*] | D [S2_ii_divergent] | D (all a) [S2_iiprime_*] | n=1 edge: F iff p<-1 [S2_iii_edge_*] | D (same comparison) |
| S3 areal ≡ d_A=r (lock+areal anchor) | F = R_w (all n) [S3_i_*] | D [S3_ii_*] | D (all a) [S3_iiprime_*] | F = R_w [S3_iii_*] | **F = R_w** [ESS_S3_*] |
| S4 r/(1+z) = r·sqrt(A) (variant) | ->0 NON-MONOTONE [S4_i_*] | ->0 non-mono [S4_ii_*] | a<2: D mono; **a=2: F=X MONOTONE**; a>2: ->0 non-mono [S4_iiprime_*] | ->0 non-mono [S4_iii_*] | ->0 [ESS_S4_*] |
| S5 d_L = (1+z)^2 r (anchor+observable) | D (all n) [S5_i_divergent] | D [S5_ii_*] | D (all a) [S5_iiprime_*] | D [S5_iii_*] | D [ESS_S5_divergent] |
| S6 z ≡ depth delta (ratio-invariant) | D (all n) [S6_i_divergent] | D [S6_ii_*] | D (all a) [S6_iiprime_*] | D [S6_iii_*] | D [ESS_S6_divergent] |
| S7 infall proper time (lock+worldline POSIT; proviso eps^2 > sup A) | F (all n) [S7_i_*] | D [S7_ii_*] | D (all a) [S7_iiprime_*] | F [bounded integrand, finite range] | **F** [ESS_S7_*] |
| S8 FULL budget (ABSTRACT/chain) | D — profile-independent (O2 CONSOLIDATED, cited) | same | same | same | same |
| S9a depth-only budget (ABSTRACT) | inf = 0 (degenerate; O2 CONSOLIDATED, cited) | same | same | same | same |
| S9b leg count (ABSTRACT) | wall unattained by finite chains (O1, cited) | same | same | same | same |

Per-branch selection statements (each conditional, uniform ink — F-PIN):

- **IF spatial = S1 (proper):** satisfiable. Surviving subfamily: class (i) with n < 2
  (incl. n=1); class (iii) at the n=2 edge iff p < -2 (log-suppressed); (ii), (ii'),
  essential walls EXCLUDED. [S1_* keys]
- **IF spatial = S2 (optical/travel-time):** satisfiable. Surviving: class (i) with n < 1;
  class (iii) at the n=1 edge iff p < -1; (ii), (ii'), essential EXCLUDED. **n=1 (the
  P-opt member) is excluded — it sits exactly on the log-divergent knife edge**
  [S2_i_n1_logdivergent], with the exact rate ell_opt = 2 R_w delta/n (at c0=1)
  [S2_i_n1_rate_ell_eq_2Rw_delta] — the banked "one tick of depth, one tick of optical
  path." P-opt LICENSE attached in §5 verbatim.
- **IF spatial = S3 (areal/d_A):** satisfiable. Surviving: ALL finite-chart-radius walls —
  class (i) every n, class (iii) every p, AND the essential walls (noted-only class:
  hand-check tag). (ii)/(ii') EXCLUDED. This is the least selective distance branch: it
  reads only the chart location of the wall, not the profile.
- **IF spatial = S4 (r/(1+z)):** SATISFIABLE ONLY DEGENERATELY in classes (i), (ii),
  (ii' a>2), (iii), essential: the measure tends to 0 at the wall NON-MONOTONICALLY
  (interior max at u = n/(n+2) in (i) [S4_i_interior_max_*]; at r = 2X in (ii); at
  r = 2X/(a-2) in (ii' a>2) [S4_iiprime_critpoint_*]) — the wall then sits at ZERO
  separation, equal to the observer's own value, and the measure is non-injective:
  obstruction-grade as a distance in those members (O3-OBSTRUCTED(S4-cell) grade, stated
  per-cell, not for the branch). **THE SURPRISE: the single GENUINE member is (ii')
  alpha = 2** — r/(1+z) = rX/(X+r) is monotone increasing [S4_iiprime_alpha2_monotone]
  with finite wall value X [S4_iiprime_alpha2_wall_value_X]: an INFINITE-chart-radius wall
  at finite S4-separation. (a<2: monotone divergent — posit fails; a=2 is the knife edge.)
  Under S4 the posit selects EXACTLY {(ii'), alpha=2} — an anti-exclusion cell: see §5.
- **IF spatial = S5 (d_L):** UNSATISFIABLE in the frozen family (divergent in every class
  and member). Modus tollens: IF the kernel's spatial is d_L, THEN the finiteness posit is
  unsatisfiable against A->0 walls in the frozen family. d_L's divergence is depth-driven
  (the (1+z)^2 factor; ln d_L = 2*delta + ln r).
- **IF spatial = S6 (z/depth):** UNSATISFIABLE, definitionally (the wall IS delta -> oo).
  This branch's divergence is not a defect: it is the CP1 gamma-asymptote statement itself
  (infinite rapidity). A kernel that reads "spatial" as z cannot also posit finiteness; the
  modus tollens is the outcome: IF spatial = z, THEN the finiteness posit is unsatisfiable —
  an outcome, not a failure; under CP1 this divergence is the asymptote statement itself.
- **IF spatial = S7 (infall proper time; worldline posit + proviso eps^2 > sup A):**
  satisfiable. Surviving: all finite-chart-radius walls (class (i) every n — exact witness
  c*tau = 2R_w(sqrt(1+h^2)-h) at n=1, c0=1, eps^2=1+h^2 [S7_i_finite_exact_witness_n1];
  class (iii); essential, hand-check tag); (ii)/(ii') EXCLUDED (integrand >= 1/eps over an
  infinite range [S7_comparison_*, S7_ii_*, S7_iiprime_*]). Verdict-pattern IDENTICAL to S3
  (see §5c). The worldline-posit tag travels: this branch imports more structure than the
  pair itself.
- **IF spatial = S8 (full budget):** UNSATISFIABLE — the wall is DIVERGENT against the full
  budget Sigma(|delta_i|+|w_i|) (O2 consolidated; profile-independent, so this holds in
  every class). BOTH READINGS STATED HONESTLY: (reading 1) as a finiteness posit, S8 fails
  — "x_max finite in S8" is false at every A->0 wall; (reading 2) this failure is exactly
  the SR-LIKE PROTECTION — S8 is the one refined functional against which the wall is both
  unreachable (finite chains, O1) and infinitely costly (divergent budget), i.e. the branch
  where the wall behaves most like SR's c. Reading 2 is available regardless of whether S8
  is adopted as the kernel's spatial; adopted as spatial, S8 renders the posit unsatisfiable —
  an outcome, not a failure.
- **IF spatial = S9a (depth-only budget):** DEGENERATE, not merely unsatisfiable: inf = 0
  (O2 consolidated) — every point, including the wall, at zero separation. As a spatial
  candidate this row is obstruction-grade (O3-OBSTRUCTED(S9a) as a selection question:
  "finite" is trivially true and selects nothing; the row is not a distance).
- **IF spatial = S9b (leg count):** UNSATISFIABLE for finite chains (the wall is unattained
  at every finite count — O1 theorem; the protection is chain finiteness). Infinite-chain
  caveat travels verbatim: an infinite chain accumulates to the wall. Rapidity-role.

## 4. D2 — THE APPROACH-PROFILE CLASS (the gamma-asymptote's SHAPE, per distance branch)

For each branch S_k where the wall sits at finite S_k, the depth delta (equivalently
1+z = e^delta) as a function of REMAINING separation sigma_k := S_k(wall) - S_k(r), r -> wall.
CLASS ONLY: exponents/coefficients as functions of (n, measure); no n selected (F-LAWHUNT).

### 4a. Class (i) interior members: LOGARITHMIC depth / POWER-LAW redshift

Every surviving class-(i) cell has the SAME shape with a measure-dependent coefficient:
  **delta = kappa · ln(1/sigma_k) + const + o(1),   i.e.   1+z ∝ sigma_k^(-kappa)**,
derived exactly (the residual delta - kappa·ln(1/sigma) is u-INDEPENDENT — checked by
d/du = 0, an exact statement, not merely asymptotic, for S1/S2/S3):

| Branch | surviving range | sigma_k(u) exact | **kappa(n, measure)** | const (exact) | key |
|---|---|---|---|---|---|
| S3 areal | all n | R_w·u | **n/2** | (n/2)ln R_w - (1/2)ln c0 | D2_S3_kappa_n_over_2_const_exact |
| S1 proper | n<2 | 2R_w u^{(2-n)/2}/(sqrt(c0)(2-n)) | **n/(2-n)** | u-free (script) | D2_S1_kappa_n_over_2mn_const_exact |
| S2 optical | n<1 | R_w u^{1-n}/(c0(1-n)) | **n/(2(1-n))** | u-free (script) | D2_S2_kappa_n_over_2_1mn_const_exact |
| S7 infall | all n | ~ (R_w/(c·eps))·u (leading) | **n/2** (same as areal) | + (n/2)ln(R_w/eps) shift | D2_S7_sigma_over_u_limit_Rw_over_eps |

- S7 derivation: sigma7/u -> R_w/eps (L'Hopital on the exact integral; integrand -> 1/eps),
  so ln sigma7 = ln u + O(1) and the areal coefficient transfers: kappa_infall = n/2.
  UNITS CONVENTION (R1 A6, cosmetic): the script and table set c = 1 and suppress the
  -(1/2)ln c0 term of the S7 constant; with units restored, sigma7/u -> R_w/(c·eps) and the
  shift is (n/2)ln(R_w/(c·eps)). Verdicts and kappa unaffected.
- **General-m unification (structural, not a new row):** any measure with radial integrand
  A^{-m} (m=0 areal-like, m=1/2 proper, m=1 optical) is finite iff n·m < 1 and has
  kappa = n/(2(1-n·m)), i.e. **1/kappa = 2/n - 2m: linear in the A-weight m with slope
  exactly -2** [D2_general_m_kappa_const_exact, D2_general_m_reciprocal_kappa_linear].
  Corollary (n-FREE cross-branch spacing): 1/kappa_areal - 1/kappa_proper = 1 and
  1/kappa_proper - 1/kappa_optical = 1 for EVERY n [D2_reciprocal_kappa_spacing_*].
  The three distance coefficients are one arithmetic progression in reciprocal — a
  cross-measure invariant of the power-law family, independent of the free profile data.
- kappa is NOT pinned by any branch: within each surviving window kappa sweeps all of
  (0, oo) [D3_kappa_S1/S2/S3_range_0_to_oo]. The CLASS (log-depth/power-redshift) is the
  content; the coefficient stays free with the profile (F-LAWHUNT discharged).

### 4b. Class (iii) log corrections: the class is STABLE for interior members (log-log shift)

For A = c0 u^n(-ln u)^{-p} with n INTERIOR to the window (finiteness unchanged — power
dominates log; witness key D2_iii_interior_proper_finite_witness_n1_p2):
  **delta = kappa·ln(1/sigma) + (kappa/n)·p·ln ln(1/sigma) + const + o(1)** —
same leading kappa, plus a log-log term with coefficient (kappa/n)·p per measure:
areal p/2; proper p/(2-n); optical p/(2(1-n)). Derivation chain, machine-checked:
- areal: exact substitution; residual after both terms -> 0 [D2_iii_S3_loglog_coeff_*].
- proper: remaining length ~ u^{1-n/2}(-ln u)^{p/2}/(1-n/2) via L'Hopital — the derivative
  ratio reduces EXACTLY to 1/(q - p/(2t)) -> 1/q [D2_iii_S1_lhopital_reduction_*,
  D2_iii_S1_lhopital_limit_*]; inverting the log gives the stated pair of coefficients;
  witness inversion limit (n=1, p=2): the residual CONVERGES — against the member's actual
  exact remaining length sigma1 = 2 e^{-t/2}(t+2) the constant is **ln 8** (R1-adjudicated
  [R1_ADJ_actual_sigma_residual_eq_log8]); the script key
  [D2_iii_S1_inversion_witness_const_eq_log4] takes the residual w.r.t. the LEADING FORM of
  ln(1/sigma), L(t) = t/2 - ln t, which gives ln 4 (difference exactly ln 2). The load-bearing
  content (convergence; kappa = 1; ln-ln coefficient 2) holds either way (R1 A1).
  Optical: same algebra with w = 1-n.

### 4c. The EDGE members change the class: POWER-LAW depth / exp-of-power redshift

The only (iii) members that are finite AT a knife edge (proper n=2 with p<-2; optical n=1
with p<-1) approach the wall in a genuinely HARDER class:
- proper edge n=2, p<-2: remaining ell ∝ t^{(p+2)/2} (t = -ln u), delta ~ t, so
  **delta ∝ (1/ell)^{2/|p+2|}** — power-law depth divergence in remaining proper length;
  1+z ~ exp(C/ell^{2/|p+2|}). Witnesses p=-4 (delta·ell -> const) and p=-3 (delta·ell^2 ->
  const; exponent 2/|p+2| = 2) [D2_edge_proper_pm4_*, D2_edge_proper_pm3_*].
- optical edge n=1, p<-1: sigma_opt ∝ t^{p+1}, delta ~ t/2, so **delta ∝
  (1/sigma_opt)^{1/|p+1|}**; witness p=-2 (delta·sigma -> 1/2) [D2_edge_optical_pm2_*].
So the gamma-asymptote's shape is CLASS-DEPENDENT: logarithmic depth generically, but the
edge-rescued members escape to power-law depth. No member falls SOFTER than logarithmic.

### 4d. Essential walls (noted-only, hand-check tag): the harder class already at S3

A = e^{-1/s} (s = R_w - r): delta = 1/(2s) EXACTLY [ESS_D2_delta_eq_1_over_2sigma3_exact],
so on the areal branch **delta = 1/(2 sigma3)** — power-law depth with NO logarithmic
regime at all; 1+z = e^{1/(2 sigma3)}. On S7: sigma7 ~ s/(c·eps) near the wall
[ESS_S7_integrand_wall_limit_1_over_eps], so delta ~ 1/(2 c eps sigma7) — same class.
(S1/S2 are divergent here, so no profile is owed on those branches.)

### 4e. The S4 genuine member: an EXACT profile, not asymptotic

For (ii') alpha=2 under S4: sigma4 = X - r/(1+z) = X^2/(X+r) and the relation
  **(1+z)·sigma4 = X exactly, for ALL r** [D2_S4_alpha2_exact_identity_1pz_times_sigma4_eq_X]
i.e. delta = ln(1/sigma4) + ln X with kappa = 1 EXACTLY everywhere (not just near-wall) —
the only cell in the map where the approach profile is globally exact. Reported neutrally:
a structural curiosity of this one member, selected by no branch unconditionally;
conditionally under S4 it is the unique genuine survivor (§3).

## 5. D3 — CROSS-BRANCH STRUCTURE

### 5a. BRANCH-ROBUST statements (checked per branch, not asserted blanket)

- **R-1 (qualified, NOT blanket — F-STEER attacked):** "the finiteness posit excludes
  infinite-chart-radius walls (ii)/(ii')" holds on **S1, S2, S3, S7** — every lock/monotone
  distance branch [S1_ii/iiprime_*, S2_ii/iiprime_*, S3_ii/iiprime_*, S7_ii/iiprime_*].
  **It BREAKS on S4**: (a) the genuine member (ii') alpha=2 puts an infinite-radius wall at
  finite monotone S4-separation X [S4_iiprime_alpha2_*]; (b) in the degenerate cells the
  wall's S4-value 0 is "finite" vacuously. The honest robust statement is therefore:
  **"IF the kernel's spatial is any of S1/S2/S3/S7, the posit forces a finite-chart-radius
  wall; the r/(1+z) variant is the one shortlist branch on which an infinite-radius wall
  can carry the posit."** Stated at the same temperature as the exclusions (F-STEER).
- **R-2 (robust across every surviving branch x member, scoped to the frozen family):**
  the depth divergence is NEVER slower than logarithmic in remaining distance — interior
  members are exactly logarithmic (power-law 1+z); edge-rescued and essential members are
  power-law in depth (exp-of-power 1+z). "Softer-than-log" does not occur in the family.
- **R-3 (robust):** the rapidity-role rows {S5, S6, S8} reject the posit in EVERY class —
  their per-branch modus tollens is class-independent (S6/S8 definitionally/abstractly; S5
  via the depth-carrier identity in every class checked).

### 5b. BRANCH-SENSITIVE statements

- **The n=1 member (P-opt): survives S1 (n=1<2), S3, S7; DIES on S2** (exactly the
  log-divergent optical knife edge; rate ell_opt = 2R_w·delta/n at c0=1). Per the O2
  verbatim duty, the LICENSE travels wherever n=1 is named: "this observation LOCATES
  P-opt in the class family and recovers its exact rate; it does NOT derive P-opt, does
  NOT upgrade its posit status, and edge-status is measure-relative (n=2 is the proper
  edge; every n is some functional's threshold) and not class-stable (log corrections move
  it) — selection content ZERO until a measure is chosen, which is Charles's guarded CP2
  choice." (O2 CONSOLIDATED, quoted.) Stated with equal temperature both ways (F-STEER):
  the optical branch excluding n=1 is exactly as conditional as the (ii)-exclusions that
  flatter the kernel; neither is savored.
- **The surviving n-window is branch-graded:** S2 selects n<1 (strictest); S1 selects n<2;
  S3/S7 select all n (least selective). The kernel posit's selective POWER depends
  entirely on which branch Charles later adopts.
- **Essential-wall membership is branch-sensitive:** excluded by S1/S2 (divergent),
  admitted by S3/S7 (finite radius, bounded integrand) — hand-check tag travels.
- **kappa itself:** the approach coefficient differs per branch at the same member
  (1/kappa spacing exactly 1 — §4a): the same wall approach "looks" n/2-logarithmic
  areally, n/(2-n) in proper meters, n/(2(1-n)) optically.

### 5c. The selection LATTICE (joint demands; O2 inclusion hierarchy as selector)

Within the frozen family (profile-general inclusion re-verified at the class level:
optical-finite => proper-finite => areal/infall-finite; converses refuted by the n-windows):
- **{S2} == {S1,S2,S3,S7} (maximal joint demand):** demanding optical-finiteness alone
  already implies all four — surviving family: class (i) n<1 (any interior p-correction),
  plus the optical-edge members {n=1, p<-1}; everything else out. Jointly satisfiable
  (witness n=1/2: all four finite [D3_joint_witness_nhalf_*]).
- **{S1} (+S3,S7 implied):** class (i) n<2 (any interior p), plus proper-edge {n=2, p<-2}.
- **{S3} or {S7} or {S3,S7} (minimal demand):** any finite-chart-radius wall — all n, all
  p, essential walls included. S3 and S7 are VERDICT-DEGENERATE across the entire family
  (identical in/out pattern) AND approach-class-degenerate (both kappa = n/2, differing
  only in the constant): at the wall the infall branch is asymptotically the areal branch
  (the worldline posit buys no new selection). A degeneracy pair, stated as a finding.
- **S4-genuine is an ISOLATED atom:** {(ii') alpha=2} is excluded by every other distance
  branch [D3_S4gen_excluded_*], so demanding S4-finiteness (genuine, monotone) JOINTLY
  with any of S1/S2/S3/S7 is UNSATISFIABLE in the frozen family. The lattice is a chain
  (S2 => S1 => S3==S7) plus one incompatible off-chain atom (S4-genuine) plus the
  never-satisfiable rapidity rows (S5, S6, S8, S9b) and the degenerate S9a.

## 6. Falsifier discharge (prereg §6)

- **F-LAWHUNT (primary): discharged.** Every D2 statement is a CLASS with (n, p, alpha)
  free; kappa shown to sweep (0,oo) in every branch — nothing pins n, no profile is called
  "the law," the free-data status of the profile is restated at each use.
- **F-STEER: discharged, both directions named.** Kernel-favorable hazard (blanket
  infinite-radius exclusion): NOT granted — the S4 break is reported at headline level
  (§5a R-1). L-unfavorable hazard (optical excludes n=1): stated with the O2 license
  verbatim, same ink as the favorable cells (§5b).
- **F-PIN: discharged.** All nine branches carried; per-branch conditionals uniformly
  phrased; the S4 obstruction-grade cells and S9a degeneracy are graded by the same
  standard (zero-separation degeneracy) — no branch privileged; Charles can adopt any.
- **F-SHOP-CLASS: discharged.** No family additions. The (ii') representative was FIXED
  (declared §1) not added; general-m is a unification of existing rows, not a new row;
  essential walls remain noted-only with every key tagged ESS_/hand-check.
- **F-SCOPE: discharged.** No x_max value, no cosmology numbers, no mass, no law.
- **F-LEGACY: discharged.** Citations only to O1/O2 (2026-08-07), the c_eff integration
  (2026-08-06), and O2's own 08-05 cross-checks (cited through O2, not re-opened).

## 7. LANDED OUTCOME CLASS: **O3-MAP**

The selection map (§3) and approach-class table (§4) completed for every branch, including
the per-branch unsatisfiability entries (S5, S6, S8, S9b modus tollens) — with per-CELL
obstruction grades inside S4 (non-monotone members: zero-separation degeneracy) and the
S9a row (degenerate inf = 0), neither of which obstructs its whole branch question, so
O3-OBSTRUCTED is not the landing; branches do NOT collapse (the n-windows differ per
branch), so O3-DEGENERATE is not the landing either — though two real partial degeneracies
are findings: {S3 == S7} (verdict- and class-degenerate) and {S5 ~ S6} (depth-carrier).

**SURPRISES (deliverable-grade, none sanded off):** (1) the S4/(ii') alpha=2 member — an
infinite-chart-radius wall at finite monotone S4-separation with an EXACT kappa=1 profile
(1+z)·sigma4 = X — breaking the blanket infinite-radius exclusion; (2) the reciprocal-kappa
arithmetic progression (1/kappa spacing exactly 1 across areal/proper/optical at every n);
(3) edge-rescued and essential members escape the logarithmic class UPWARD only (power-law
depth); (4) S3/S7 full degeneracy — the infall worldline posit adds no selection power.

**STATUS: LEAD / UNBANKED — two independent adversarial reviews owed** (R1 = full
independent recompute + completeness attack; R2 = F-LAWHUNT/F-STEER/F-PIN neutrality +
tagging honesty) before consolidation; nothing banks without both reviews + Charles.
Machine record: `derive_o3.py` (94 keys, all True) -> `run_output.txt`.

## CONSOLIDATED (2026-08-07, both reviews in): O3-MAP SUSTAINED — AMENDED

Files: `ADVERSARIAL_REVIEW_1_recompute.md` (SUSTAINED-AMENDED; full independent recompute, 108
checks, own scripts, probe code unopened until after — NO KILL; amendments A1-A6 + one
strengthening) + `ADVERSARIAL_REVIEW_2_neutrality.md` (AMENDED A1-A7; no falsifier fired;
F-LAWHUNT/F-PIN/F-STEER do not fire; all leaned-on cells hand-confirmed). The four R2 rhetoric
fixes (R2 A1-A4), R2 A5, R1 A1 and R1 A6 are applied IN PLACE above; the remaining amendments
are applied HERE and this section supersedes the corresponding entries above.

**APPLIED AMENDMENTS (compact):**
- **R1 A2 — class-(iii) cells are WALL-LOCAL (scope tag on the whole (iii) column, D1 §3):**
  the frozen (iii) profile A = c0 u^n(-ln u)^{-p} is SINGULAR at the observer end r=0 (A(0)=oo
  for p>0; A(0)=0 for p<0, so phi(0)=0 cannot hold), and for the surviving edge-rescued members
  the separation integrals diverge at the OBSERVER end — O2 computed them on (log2, oo), i.e.
  wall-local, and that tag now travels: (a) S1/S2 (iii)-edge cells mean "finite separation-
  to-wall from any interior r0>0", not "from the observer"; (b) the S7 x (iii) proviso
  eps^2 > sup A is UNSATISFIABLE from r=0 for p>0 — that cell is restated WALL-LOCAL;
  (c) the S4 x (iii) literal "wall at zero separation equal to the observer's own value" fails
  for p>2 — the honest degenerate content is "S4-value -> 0 at the wall (wall-locally
  monotone)". ONE scope tag; no cell verdict flips.
- **R1 A3 + R2 A7 — honest key-count statement:** "94 machine-check keys, all True" overstates
  what the machine verified. Five keys are hardcoded-True definitional placeholders (chart
  location by class construction: S3_ii, S3_iiprime, S3_iii, ESS_S3, D3_S4gen_excluded_S3);
  S2_i_n1_rate is a hand-substituted tautology (t = t); S7_comparison checks an algebraic
  rearrangement, not the inequality; the reciprocal-kappa spacing keys are arithmetic of
  already-derived kappas; two cells were keyless (S7 x (iii); S2 x ESS). None hides a wrong
  cell — BOTH reviews' independent keys cover every one of them and all pass (R1: 108 checks;
  R2: hand recomputes). Also recorded: `run_output.txt` carries NO language scan; R2 ran an
  independent scan (superlatives/selection language/scope/legacy/floats) — clean. R2 A7b: the
  §3 branch tags (areal-anchor chart tag on S3/S5; the S7 worldline posit + proviso) travel
  into every D2 row. R2 A7c: the S4-genuine wall value X is TAIL-GENERAL within (ii') (any
  A ~ (r/X)^{-2} gives r·sqrt(A) -> X); the monotonicity/injectivity statement is for the
  declared regular representative.
- **R1 A4 — the d_L gloss is finite-R_w-scoped:** "near the wall d_L = R_w e^{2delta}(1+o(1))"
  holds only for finite-chart-radius classes ((i)/(iii)/ESS); in (ii)/(ii'), d_L = r·e^{2delta}
  with r -> oo. Divergence verdicts unaffected.
- **R1 A5 (+ its duty) — the S4/alpha=2 genuine atom is ITSELF a KNIFE-EDGE, not class-stable:**
  log-corrected neighbors A = (1+r/X)^{-2} ln(e+r/X)^{nu} destroy genuineness either way
  (nu>0: monotone divergent; nu<0: degenerate ->0) — exactly the fragility for which O2's
  license demoted n=1's edge status. The atom survives as an in-family fact (a tag, not a new
  member; F-SHOP-CLASS respected), but headline SURPRISE (1) in §7 must NOT be read as
  class-stable; it carries the same license-style tag as n=1.
- **R1 strengthening (reported, no change owed):** R-1's exclusion of (ii)/(ii') on S1/S2/S7 is
  PROFILE-GENERAL, not merely family-internal — any A -> 0 wall at infinite chart radius has
  integrand >= 1 (S1, S2) or bounded below via 1/eps (S7) eventually, over an infinite range;
  matches the O2 inclusion hierarchy's profile-generality. (S3 is definitional.)
- **R2 A6 — outcome tagging corrected:** the S4 cells do not obstruct the S4 branch question
  (one genuine member exists); the S9a row IS obstruction-grade as a whole branch question (§3)
  and is carried as row-grade **O3-OBSTRUCTED(S9a) INSIDE the O3-MAP landing**. The landed
  outcome class is **O3-MAP** with that row grade.

**STATUS: verified LEAD** (same-session reviews; external bar travels). Four-check:
preregistered; bounded scope stated; every load-bearing cell blind-verified by two independent
recomputes; premises/tags audited.

**HANDOFF:** the structure lane (O1-O3) is COMPLETE as verified leads. Per Charles's CP1
scale-lane ruling, the profile-family output now feeds the observational lane (the M2 validator
build) — with EVERY selection statement conditional on a future branch adoption (the CP2 no-pin
standing: Charles free to adopt any row afterward) + the kernel posit. F-LAWHUNT remains in
force: no n selected, no law stated.
