# D2 — the TIME-LIVE transfer function, mixing unmuted (derivation notes)

Date 2026-08-08 | branch grok | agent: D2 derivation (Fable) | MODE: OBSERVE
Contract: `PREREGISTRATION.md` (frozen). Parent: `udt_bao_origin_MAP_2026-08-08.md` (CP2a).
Machine check: `derive_d2.py` -> `run_output.txt`; **49 / 49 keys True** (45 at first
delivery; post-review: the vacuous B6b replaced by the two channel-layer keys B6b/B6c
[R1-A1] and the A-11 window-break block A11a–c added [R2-A-11]); every boxed claim cites
its KEY. STATUS: **verified LEAD** — R1 SUSTAINED-AMENDED + R2 AMENDED, ALL amendments
applied in place; see the CONSOLIDATED section (end). Same-session reviews; external bar
travels. NOT committed (owner's gate).

**SCOPE BANNER (stamps EVERY statement): TIME-LIVE / mixing ON (mu != 0, s != rho carve-out
honored) / lock + areal-anchor chart / central observer / class-(i) profile (n > 0 free
symbol) where closed forms are used / DECLARED SUB-SLICES per the ledger in §1.** No data
touched; ZERO BOSS contact; no fitted numbers (F-RETRO machine-discharged, KEY
K_FRETRO_no_float_atoms_in_derivation). NO CMB development — the X-CMB-ANISO direction is a
recorded pointer elsewhere, nothing more (F-SCOPE).

## 0. Ground (cited at source; no code imported)

- D1 CONSOLIDATED (`../udt_bao_origin_D1_static_transfer_2026-08-08/DERIVATION_NOTES.md`):
  the static map is a pure smooth rescaling (featureless in => featureless out, proven);
  window-break map-vs-window decomposition; the D2 inheritance list §9/CONSOLIDATED. The
  static limit below MUST and DOES recover it (T6', §8).
- `udt_ceff_depth_orchestra_integration_2026-08-06.md`: lambda_t is a TWO-POINT object;
  1+z = lambda_t^{-1/2} (the c_eff ratio (1+z)^{-2} = lambda_t, blind-verified); depth
  delta_t = -(1/2) log lambda_t.
- `udt_mixing_channel_lane_2026-08-06/DERIVATION_NOTES.md` (+ BLIND_VERIFICATION_FINAL):
  the arrow A = [[1/rho,0,mu],[0,rho,0],[0,0,s]]; mu = the invariant reciprocal-lock defect,
  SCOPED s != rho (on s = rho, mu is pure gauge — carve-out honored); the composition law;
  the forced coboundary form m(p,q) = a k(q) - s k(p); COUPLING-INERT verdict cited as
  SCOPE (kinematic layer), not physics.
- `udt_xmax_O1_asymptote_2026-08-07/DERIVATION_NOTES.md` CONSOLIDATED: Q3 — the mu-direction
  raises the lambda_t floor / moves away from the wall; elliptic exit before the wall.
  (Freely citable ground, 08-07; re-derived here anyway at KEYs A5–A8.)
- July time-live lane: NOT cited (nothing imported from it; the crest-transport and depth
  law in §7 are derived from scratch here, per the per-item re-derivation rule).

## 1. Declared sub-slices ledger (F-FREEZE discharge — every simplification, none silent)

| # | sub-slice | inheritance / what full generality would add |
|---|---|---|
| SS1 | ARROW LAYER per sightline: each direction n carries its own pair comparison with mixing mu(n); lambda_t taken EXACTLY (no expansion) from the 2x2 clock-screen block | exact in mu; the only expansion is O(mu^4)-truncation in STATISTICS coefficients (B1), flagged where used |
| SS2 | mixing data direction-only at leading order (mu, s vary with n, not with r along one sightline); TIME-dependent mu(t) along a sightline likewise unmodeled at this order [R1-A3b: previously unnamed — slow t-variation is composition-covered via SS7's linear accumulation, but that coverage is NAMED here, not derived beyond B7] | r-varying and t-varying mu along a sightline = the chain layer SS7; enters at next order in transverse/temporal gradients |
| SS3 | METRIC REALIZATION: stationary cross-term g_t,psi = h, LINEAR order in h for ray propagation; equatorial reduction (Category-A); h center-regularity (h -> 0 faster than S at r=0) required for a finite drift integral | O(h^2): ray-path corrections, g_tt shift (named at G1b — ORDER-consistent with the O(mu^2) arrow layer; coefficient match and frame-pair specification OPEN, see §3(ii) [R1-A2]) |
| SS4 | TIME-DEPENDENCE: A(t,r) fully generic in the DEPTH LAW (§7 — that law is EXACT, no slice beyond the SS9 chart ansatz [R2-A-4]); the slowly-varying tag applies ONLY to the no-fold conclusion (a fold needs A_t comparable to A*A_r — outside slow variation, onset condition banked) | fast time-dependence: the fold/caustic channel opens (§7, honest bound) |
| SS5 | STATISTICS: mu/k field Gaussian, statistically isotropic, power-law ("featureless" per D1 §1 definition, in the same proper/coordinate realization fork — verdict rides neither) two-point function; k_p = the observer's own value, one fixed number. GAUSSIANITY IS LOAD-BEARING on the no-feature verdicts [R1-A4]: it supplies both the quartic reduction AND the featureless-sum lemma's positive-coefficient hypothesis (third moments vanish); non-Gaussian input reopens signed cross-terms and the lemma's hypothesis fails | non-Gaussian: the pointwise-map scale-covariance argument (§3, STATED not derived) requires ALL-ORDER scale invariance of the input (the mu^2 output 2-pt function is an input 4-pt object) — STRONGER than D1 §1's two-point definition of featureless [R2-A-5]. For Gaussian input the Hermite/positive-coefficient series plus B5 covers even the un-truncated lambda_t map, so the O(mu^4) flag is safe |
| SS6 | test sources; central observer; geometric optics/eikonal; c = 1 | inherited D1 P-L7/P-L10/P-L11; back-reaction stays open (D1 §9 item 4) |
| SS7 | CHAIN LAYER: nonstationary + mixing combined handled by composition — the lane law A1*A2 = A(a1 a2, s1 s2, a1 m2 + m1 s2) re-verified [KEY B7]; O1's composition results cited for the Lorentzian-block behavior | a native PDE evolution of the profile (no such law exists per the 08-06 finding — profile = free data) |
| SS8 | spectral windows: real-spectrum window mu^2 < (s - 1/rho)^2 (near window); s != rho carve-out; the collision locus s = 1/rho excluded from the perturbative branch (exact treatment: immediately elliptic there, §2) | the far window mu > s + 1/rho and the elliptic gap: depth UNDEFINED (domain loss), not structured |
| SS9 | **[R2-A-4, LOAD-BEARING] the TIME-LIVE LOCK-FORM ANSATZ**: the derivation assumes the lock form persists time-live with a SINGLE function — ds^2 = -A(t,r)dt^2 + dr^2/A(t,r) (+ the SS3 h term): B = 1/A with the SAME time-dependent A, g_tr = 0. Canon C-2026-08-06-1's lock<=>areal-anchor equivalence (B = 1/A <=> G^t_t = G^r_r) is a STATIC statement; its time-live persistence is an ANSATZ (a choice), not cited theory. The exact depth law's FORM (§7a) and the fold condition A_t = -A*A_r (§7b) both RIDE this ansatz | inheritance = re-derivation with generic B(t,r) and g_tr != 0; the qualitative verdict (smooth law; fold as a free-data condition) plausibly survives, the EXACT forms do not |

Premise ledger (new/changed vs D1; unchanged D1 premises inherit their tags):
P-D2-1 = D1 P-L1 (lock + areal anchor chart) — THEORY (canon) for the STATIC form ONLY;
its time-live persistence is RETAGGED CHOSE (the SS9 ansatz) [R2-A-4]. P-D2-2..4 = D1
P-L2/P-L5/P-L7 inherited unchanged (declared-slice / THEORY / FREE). P-D2-5 [FLAGGED,
chose-with-theory]: the redshift reading at mu != 0 is 1+z = lambda_t^{-1/2} of the
CAUSALLY-LABELED branch — the banked extractor extended off the mu = 0 stratum (exact at
mu = 0 by F1; the labeling window is DERIVED, not chosen — §2). P-D2-6 = SS5 statistics
premise (FREE — the posed plain input; Gaussianity LOAD-BEARING per the SS5 row). P-D2-7:
time ON, mixing ON — the two D1 OFF-sectors are exactly the ones turned on here; no other
sector frozen. P-D2-8 [R2-A-10, explicit]: OFF-CENTER OBSERVERS remain un-probed — the
central-observer premise is re-inherited from D1 §9 item 5, named here as an explicit
open line, not silently carried in the banner.

## 2. The mixing block, exactly (the machinery T1' rides)

The full 3x3 strain charpoly factors as (lam - rho^2)(lam^2 - T lam + d), T = 1/rho^2 + s^2
- mu^2, d = s^2/rho^2 [KEY A1]: **the radial slot decouples exactly — mixing touches the
clock-screen block only.** Exact block structure (all machine-checked):

- Discriminant factorization: disc = ((1/rho - s)^2 - mu^2)((1/rho + s)^2 - mu^2)
  [KEY A2b] = u^2 - 4 mu^2/rho^2 with u = s^2 - mu^2 - 1/rho^2 [KEY A2a]. Real spectrum
  iff mu < |s - 1/rho| (near window) or mu > s + 1/rho; ELLIPTIC (no real depth) between.
- mu = 0 roots: {1/rho^2, s^2} — D1's static pair [KEYs A4a, A4b].
- EXACT monotonicity: d lam_min/d(mu^2) = +lam_min/sqrt(disc) > 0 and d lam_max/d(mu^2) =
  -lam_max/sqrt(disc) < 0 on the whole real window [KEYs A5a, A5b, A5c]; the product tie
  lam_min * lam_max = s^2/rho^2 is mu-INDEPENDENT [KEY A5d]. (O1 Q3 re-derived natively.)
- Perturbative coefficient: d lam_t/d(mu^2)|_0 = 1/(rho^2 s^2 - 1) for the branch continuous
  to 1/rho^2 [KEY A6] — SIGN FLIPS across rho*s = 1 (the eigenvalue-collision locus; there
  the block is IMMEDIATELY elliptic for any mu != 0: disc|_{s=1/rho} = mu^2(mu^2 - 4s^2)).
- The threshold: at mu_c = |s - 1/rho| the two eigenvalues collide at s/rho exactly
  [KEYs A7, A8], and the causally-labeled eigenline goes eta-NULL exactly there [KEY A10]:
  the window edge IS causal-labeling degeneration. The labeling condition for the min branch
  factorizes to mu < s - 1/rho exactly [KEYs A9a, A9b, A9c] — **the causal-labeling window
  and the real-spectrum near window COINCIDE, TWO-SIDED with mu_c = |s - 1/rho|** [R1-A5:
  R1 adjudicated BOTH orderings rho*s <> 1 (400 draws, branch = continuous-to-1/rho^2) —
  a strengthening, adopted]: everywhere the depth is real, the labeling is valid; both fail
  together at mu_c. (Derived, not chosen — discharges P-D2-5's window.) MACHINE-COVERAGE
  DOMAIN [R2-A-3]: the in-script keys (A6, A9b, F1a/b, B1) cover the s > 1/rho side via the
  w-parametrization; the s < 1/rho side holds for the CAUSALLY-CONTINUOUS branch (R2's
  independent implicit-differentiation check; analytic continuation of the same root) —
  stated as the branch convention, asserted-not-machine-covered on that side. GENERALITY
  NOTE [R2-A-9, wonder dialed down]: the threshold coincidence is the GENERIC
  exceptional-point behavior of an eta-pseudo-Hermitian block (the eigenvector goes neutral
  exactly where the real spectrum breaks) — structural, not a coincidence to be over-read.

## 3. T1' — EXISTENCE: what the time-live map imprints on plain input

**The anisotropy machinery is REAL — three derived channels** (none exists statically):

(i) **Per-direction depth modulation** (the direction-dependent channel named in the
contract): a direction-dependent mixing field mu(n) writes ln(1+z)(n) = ln rho -
K(rho,s)*mu(n)^2 + O(mu^4), with the transfer coefficient K = rho^2/(2(rho^2 s^2 - 1))
[KEYs B1, A6]. The map is POINTWISE per direction (each sightline's own pair comparison,
SS1) and EVEN in mu; its coefficient depends on depth only, never on angle.

(ii) **Sky remap (dragging)**: in the metric realization (g_t,psi = h, SS3) an arriving
ray with p_psi = 0 drifts at dpsi/dr = h/(A S) + O(h^3) [KEY C1; null-consistency C3;
h = 0 gives exactly zero, KEY C2] — the observed sky position is the angular coordinate
plus a smooth line-of-sight functional of h. The coframe check [KEYs G1a, G1b] ties h to
the arrow-layer mix (mix ratio h/(sqrt(A) sqrt(S)) at linear order); the metric-level
g_tt deviation is O(h^2) — ORDER-consistent with the O(mu^2) arrow layer, and no more
[R1-A2, the sharpest P-D2-5 load]: in this stationary realization, static emitters on
p_psi = 0 rays have redshift omega = E/sqrt(A) with g_tt = -A exactly — h-INDEPENDENT at
ALL orders — so the exhibited realization does NOT itself realize the arrow-layer K*mu^2
depth anisotropy; NO coefficient match is shown, and WHICH frame pair realizes the
causally-labeled-branch comparison is unspecified. Channel (i) rides the FLAGGED premise
P-D2-5 (legitimate as flagged); the coefficient match and frame specification are OPEN.

(iii) **Anisotropic radial ruler**: the per-direction z-dictionary (§7c) — the same J(z)
stretch, modulated per direction at O(mu^2).

**The statistics transfer — the load-bearing question.** All three channels are pointwise
(local in direction) with direction-independent coefficients, so the output statistics are
built from the input field's correlation function evaluated at the SAME separations:
- The quadratic channel maps a featureless C_mu(theta) = M theta^{-g} to 2 K^2 C_mu^2 —
  a PURE power law with log-slope exactly -2g, constant [KEY B3]: index doubled, NO scale.
- The coboundary channel (the lane's forced form mu(n) = k(n)/rho - s k_p): the exact
  Gaussian transfer is Cov(mu^2, mu^2) = 2 a^4 C_k^2 + 4 a^2 s^2 k_p^2 C_k (a = 1/rho)
  [KEY B4] — a TWO-POWER sum theta^{-2g} + theta^{-g}, the linear term switched on by the
  OBSERVER'S OWN mixing value k_p.
- Chains: mixing ACCUMULATES LINEARLY along a composition (m_tot = a1 m2 + m1 s2, the lane
  law re-verified [KEY B7]) — a linear pointwise accumulation of featureless per-leg fields
  stays featureless; composition acts inside the Lorentzian block, no operator on the sky
  coordinate appears.

**THE FEATURELESS-SUM LEMMA** (the master statistics statement, machine-witnessed at three
terms): any positive-coefficient finite sum of power laws has log-slope = -E_w[g] (the
weight-average of the indices) and d(log-slope)/d(ln theta) = +Var_w[g] >= 0 — the
log-slope is STRICTLY MONOTONE [KEY B5]. (The positive-coefficient hypothesis is supplied
by SS5 Gaussianity — LOAD-BEARING [R1-A4].) Consequence: NO interior extremum of the
log-slope, i.e. NO LOCALIZED FEATURE (D1 §1 definition) can appear; what CAN appear is a
smooth CROSSOVER between indices at theta_x = (K2/K1)^{1/(g2-g1)} [KEY B6a].
**AMENDED [R1-A1] — the crossover is amplitude-SET but MAP-STEERED:** at the channel layer
theta_x^g = M a^2/(2 s^2 k_p^2) with a = 1/rho [KEYs B6b, B6c] — its angular location is
set by the input amplitudes (M, the observer's own k_p) AND it CARRIES DEPTH and the
screen ratio, drifting as theta_x proportional to (1+z)^{-2/g}. This is exactly the status
D1 gave its window break — input-set location, metric/map-steered drift — and it is named
with the same first-class honesty for any later data confrontation. (The earlier
"amplitudes only / not by the map" wording was overstated; the generic-layer free-symbol
key was vacuous as machine evidence and was replaced — R1's catch.)

**T1' VERDICT (TIME-LIVE / mixing-on / declared sub-slices): the time-live map IS
anisotropy machinery — mu-modulated lambda_t writes the mu field onto the observed
redshift sky, dragging remaps the sky, both derived exactly — but the machinery is
SCALE-TRANSPARENT: a featureless mu (or k) field produces featureless anisotropy (power
laws in, power laws out; slope-monotone sums at channel mixing — Gaussian-conditional per
SS5, LOAD-BEARING [R1-A4]; non-Gaussian = stated argument only). NO preferred angular
scale arises natively (below the fold onset; declared sub-slices SS1–SS9 incl. the
time-live lock-form chart ansatz) [R2-A-8 inline conditions].**

**The honest-bounds characterization the contract demands — what WOULD have to be true of
mu's field for a scale to appear (inheritance statement, not a mechanism proposal):**
1. mu's (equivalently k's) own angular correlation must carry a localized log-slope feature
   at some scale; the map then transports it smoothly with the D1 dictionaries (its angular
   location drifting as theta(z) = s_feat/r(z)-type smooth depth-drift). The map preserves
   and transports scales; it does not make them.
2. OR the mu field's AMPLITUDE must cross the derived native thresholds: the map's only
   native non-analyticities are the elliptic/labeling threshold mu_c = |s - 1/rho| (an
   AMPLITUDE threshold — sightlines crossing it lose real depth; its sky-imprint is the
   excursion-set geometry of the mu field, which for a featureless field is itself
   scale-free [R2-A-2: this sub-claim is ASSERTED, not derived here, and rides the SS5
   Gaussian premise]) and the eigenvalue-collision locus rho*s = 1 (a DEPTH locus, not an
   angular scale). Native thresholds exist; native angular scales do not.
3. OR (radial leg, §7b) the profile's free time-dependence must realize a dictionary FOLD —
   a caustic in z-space at a metric-set depth (onset condition derived exactly, §7b, riding
   the SS9 chart ansatz); this is structure in the free profile DATA (the 08-06 finding:
   the profile is a datum), not manufactured from featureless source statistics.
4. OR [R2-A-1, the D1 window-set route, restated for completeness] a tracer's own selection
   WINDOW sets a break (D1 CONSOLIDATED: theta_break ~ Delta_l_p(bin)/r(z), window-set,
   metric-steers-the-drift) — time-live behavior derived at §7d: the break rides the now
   time-live dictionary smoothly, diverging only at the fold onset.
(F-RETRO both directions: this neither hands O-C a free feature nor kills its machinery —
the channel O-C needs EXISTS and is derived; the scale it needs is INHERITED, not native.)

## 4. T2' — the depth law of what exists

No imprinted scale exists, so (as in D1 T2) the deliverable is the depth law of the smooth
anisotropy machinery, plus the exact time-live depth dictionary:

- Transfer coefficient: K(rho, s) = rho^2/(2(rho^2 s^2 - 1)); strictly monotone in depth,
  dK/drho = -rho/(rho^2 s^2 - 1)^2 < 0 on the near window with rho*s > 1 [KEY B2a],
  saturating to K -> 1/(2 s^2) as rho -> infinity [KEY B2b]. Sign flip across rho*s = 1:
  mixing pushes z DOWN where rho*s > 1 and UP where rho*s < 1 (exact, from A6's sign).
  Featureless in depth: no critical point in rho anywhere on a window.
- THE EXACT TIME-LIVE DEPTH DICTIONARY (the time-live generalization of D1 K17, derived
  from crest transport in §7a; exact WITHIN the SS9 lock-form chart ansatz [R2-A-4]):
  d ln(1+z)/dr_s = -(A_r + A_t/A)/(2A) on the past cone [KEY D2]. Static limit:
  -A_r/(2A) exactly = D1's law [KEY F4a].
- Composition/depth behavior along time-live chains: inherited from O1 CONSOLIDATED
  (additive iff twist compact; super-additive otherwise) — smooth in leg data; no scale.

## 5. T3' — tracer-phase: non-vacuous now, and answered

Structure CAN exist time-live (inherited from the mu field, §3) — so the question D1 had
to leave vacuous is live. Derived:
- The operator is TRACER-BLIND: the complete map (lambda_t branch, K, drift rate, depth
  dictionary, class-(i) forms) carries only geometry/comparison symbols {rho, s, mu/m2, h,
  A, S, n, R_w, theta, ...} — no symbol referencing any source property exists in the
  operator [KEY E1, the D1 K14 audit re-run time-live].
- ACHROMATIC: the drift rate dpsi/dr contains no frequency symbol — E cancels exactly
  [KEY E2]; the lambda_t map acts on frames, not on spectra.
- Therefore: **any anisotropy pattern is a property of the SIGHTLINES — every tracer viewed
  through the same directions inherits the SAME pattern at the SAME sky phase.** Per-tracer
  selection windows enter as depth WEIGHTS on the same K(z) mu^2(n) pattern (amplitude,
  never phase), exactly as D1 §4(i)'s window honesty — a per-tracer window weights the
  pattern's amplitude and sets its own projection break (time-live break behavior now
  DERIVED, §7d [KEYs A11a–c], not merely echoed [R2-A-11]); it cannot move the pattern's
  angular phase. IF a pattern exists, phase-identity across tracers is FORCED at this
  layer. (Back-reaction/self-lensing P-L7 remains the named exclusion.)

## 6. T4' — amplitude(z) of the anisotropy

Fractional-depth anisotropy variance per shell (SS5, both coboundary terms, unit-variance
k, C_k = normalized correlation): Var[delta ln(1+z)](z) = K^2 (2 a^4 + 4 a^2 s^2 k_p^2)
with a = 1/rho = (1+z)^{-1} [assembled from KEYs B1, B4 at zero separation]. Exact
monotone factors, no feature in z on a window:
- the k-field weight a^2 = (1+z)^{-2} (linear channel) and a^4 = (1+z)^{-4} (quadratic
  channel) FALL with depth — deep shells' mixing anisotropy is suppressed through the
  cocycle weight a(p,q);
- K^2 RISES with depth, saturating at 1/(4 s^4) [KEYs B2a, B2b];
- net: smooth monotone-factor products; the amplitude law carries the screen ratio s as
  free data (not pinned — observe-mode); no critical depth exists on a window. The single
  non-smooth depth locus is rho*s = 1 (collision, §2) where the perturbative channel
  degenerates and the block goes elliptic — a domain edge, not an amplitude peak.

## 7. T5' — the radial imprint, time-live

**(a) The exact time-live depth dictionary (no slice beyond the SS9 chart ansatz
[R2-A-4] — the central new law).** Crest
transport in geometric optics: crest paths obey dt/dr = -1/A(t,r); the crest separation
obeys d(delta t)/dr = (A_t/A^2) delta t [KEY D1]. All sightlines of one observation event
lie on ONE past cone, so the line-of-sight integral's r_s-derivative is its integrand at
r_s; assembling (chain rule along the cone machine-checked [KEY D3]):

  1+z(r_s) = sqrt(A_obs/A_emit) * exp( -INT_0^{r_s} (A_t/A^2) dr )   (on the cone)
  **d ln(1+z)/dr_s = -(A_r + A_t/A)/(2A) |_emission   [KEY D2 — EXACT]**

Static limit: -A_r/(2A) = D1's K17 law exactly [KEY F4a].

**(b) The FOLD (caustic) channel — the one genuinely new time-live failure mode (form
rides SS9).** The dictionary folds (dz/dr_s = 0) iff A_t = -A * A_r exactly [KEY D5].
Statically this is UNSATISFIABLE on class (i): -A_r/(2A) = n/(2 R_w q) > 0 strictly on
0 < q < 1 [KEY D4 — TRUE-BY-FORM (R1-S3/R2-A-6): positivity decided by symbol
declarations, the form asserted in-script; derived from A = q^n independently by R1's
recompute; substantive machine content = D1 K17/K18 + F4a/F4b] — re-proving D1's
monotonicity. Time-live it is a CONDITION ON FREE PROFILE DATA: a fold
requires time-variation rate comparable to the static depth gradient (|A_t| ~ |A A_r|) —
outside the slowly-varying sub-slice SS4, and NOT derivable from featureless source
statistics (it is structure in A(t,r), the profile datum). IF realized, the map itself
imprints a localized z-space caustic (pileup at the extremal z) — the static
featureless-preservation theorem does NOT extend unconditionally; it extends EXACTLY
BELOW the derived onset. Honest bound, banked as the boundary of validity.

**(c) Mixing on the radial leg.** The radial strain slot is untouched by mu [KEY A1];
mixing enters the radial map only through the per-direction z-ruler. At O(mu^2) the
per-direction dictionary coefficient is 1/rho + m2*rho/(rho^2 s^2 - 1)^2 — a SUM OF
POSITIVES on the near window [KEY F6]: monotonicity is PRESERVED (slightly strengthened);
D1's no-extremum theorem carries per sightline (monotone smooth dictionary of a monotone
falling input creates no bump). Across directions the ruler varies smoothly with mu(n)^2:
an ANISOTROPIC J(z), scale-transparent by §3's pointwise argument.

**(d) The window-break re-check, time-live [R2-A-11 — prereg deliverable (iv), now
DERIVED, not asserted].** D1's break location rides theta_break = Delta_l_p(bin)/r(z)
with Delta_l_p = Delta_z/J. Time-live the dictionary rate generalizes through the exact
depth law: J_tl = dz/dl_p = (1+z) * [-(A_r + A_t/A)/(2A)] * sqrt(A) (SS9 chart) — its
static limit recovers D1 K17 exactly [KEY A11a], and theta_break = Delta_z/(J_tl * r)
contains no angular symbol [KEY A11c]: **the live map does NOT move the break beyond the
(now time-live) smooth dictionary drift, plus the smooth O(mu^2) per-direction modulation
of J [KEY F6] — EXCEPT at the fold onset, where J_tl vanishes identically [KEY A11b] and
theta_break DIVERGES** (the J -> 0 interaction R1-A3a named; there the no-feature
guarantee is already void). Map-vs-window decomposition re-checked time-live: the window
still sets the break; the metric (now with its time channel) still only steers it.

**T5' VERDICT: featureless radial input => no preferred Delta-z scale, PROVEN below the
fold onset (and at O(mu^2) in mixing; deterministic-dictionary leg — the cross-direction
statistics leg carries §3's SS5 Gaussian stamp; the law's exact form rides SS9); the fold
condition A_t = -A A_r is the exact, named boundary where this guarantee ends.**

## 8. T6' — the static-limit recovery (MANDATORY; machine-checked) — PASS

Every D2 object collapses to its D1 counterpart exactly:
- lambda_t(mu=0) = 1/rho^2 and 1+z = rho — the banked static pair [KEYs F1a, F1b, A4a,b];
- the D1 G7 dictionary r(z) = R_w(1 - (1+z)^{-2/n}) re-derived: A(r(z)) = (1+z)^{-2}
  [KEY F2];
- angular map: drift -> 0 exactly at h = 0 [KEY C2] (radial arrival G5 recovered); the
  identity map gives w_obs = K(r_s theta)^{-gamma}, log-slope exactly -gamma = D1 K4
  [KEY F3];
- depth law: -(A_r + A_t/A)/(2A) -> -A_r/(2A) = D1 K17 [KEY F4a]; class-(i)
  J(z) = (n/2R_w)(1+z)^{2/n} re-derived = D1 K18 [KEY F4b];
- anisotropy machinery OFF: every channel carries an explicit factor of mu^2 or h
  (B1/C1) — zero at the static point; the fold condition unsatisfiable [KEY D4].
NO discrepancy found; D1 recovery EXACT. (A failed recovery would have been a STOP.)

## 9. Falsifier discharge (prereg §4)

- **F-RETRO**: symbols only throughout; no E-values, no angles, no fitted numbers; machine
  key K_FRETRO confirms no float atom in any audited expression. Both steering directions
  guarded: the derived middle (machinery real / scale inherited-not-native) neither
  manufactures the owner-favorable feature nor suppresses the channel (§3 verdict + the
  honest-bounds list are the two halves).
- **F-FREEZE**: everything ON — time live (exact depth law, generic A(t,r)) and mixing on
  (exact lambda_t(mu)); every simplification is a DECLARED sub-slice with inheritance
  named (ledger §1, SS1–SS8); no silent freeze.
- **F-ONEHORSE**: O-C's row only; no statement about O-A/O-B/O-D/O-E, no comparative
  origin claims.
- **F-SCOPE**: no data contact; ZERO BOSS; no CMB development (pointer-only, banner).
- Anti-hang: pure symbolics, single process, 480 s cap; runtime ~1 min. Six first-run
  False keys were decidability/form issues (sqrt-of-perfect-square, symbolic-exponent
  cancellation, a wrong Derivative-object construction) — each restated in a machine-
  decidable EQUIVALENT form, disclosed in-script per the D1 precedent; no claim changed.
  (Both reviews independently confirmed every restatement equivalent and none weakening.)
- POST-REVIEW script touch (disclosed): the vacuous generic-layer B6b key was REPLACED by
  the channel-layer pair B6b/B6c [R1-A1] and the A-11 block (A11a–c) was ADDED [R2-A-11];
  comments relabel D4 TRUE-BY-FORM and downgrade E1's evidentiary weight. Re-run fresh:
  49/49. No pre-existing claim's check was altered.
- Cosmetic [R2-A-7]: the script's KEY names D1–D5 collide with the arc's step names
  (D1/D4 packages) — harmless in-package; rename-worthy only if excerpted.

## 10. LANDED OUTCOME (prereg §5)

**D2-T with DECLARED SUB-SLICES (= D2-PARTIAL on the tractability axis), scope-stamped:**
the time-live transfer map is DERIVED. It contains genuine ANISOTROPY MACHINERY absent
statically — per-direction depth modulation ln(1+z)(n) = ln rho - K(rho,s) mu(n)^2 (exact
block spectrum behind it), sky dragging dpsi/dr = h/(AS), an anisotropic radial ruler —
and that machinery is SCALE-TRANSPARENT: featureless mixing fields produce featureless
anisotropy (pointwise maps; index-doubling; the featureless-sum lemma: slope strictly
monotone; crossovers amplitude-set but MAP-STEERED [R1-A1]). NO preferred angular scale
arises natively (below the fold onset; declared sub-slices SS1–SS9 incl. the time-live
lock-form chart ansatz; Gaussian-conditional per SS5 — non-Gaussian = stated argument
only) [R2-A-8/R1-A4 inline conditions]. The native non-analyticities are AMPLITUDE/DEPTH
thresholds (elliptic edge mu_c = |s - 1/rho| = causal-labeling degeneration; collision
locus rho*s = 1; the radial fold A_t = -A A_r, form riding SS9), each an exact derived
onset in the comparison FIELDS — a scale appears in the view only if mu's own field
carries one (inheritance), or if the free profile data realize a fold, or through a
selection window's break (§3 route 4, §7d). T3': any existing pattern is FORCED
phase-identical across tracers (operator tracer-blind + achromatic). T6': static recovery
EXACT, 8 keys. Check count: **49/49 machine keys True** (`run_output.txt`).
Deliverables T1'–T6' all land (prereg item (iv) serviced at §7d).

STATUS: see CONSOLIDATED below (both reviews in; verified LEAD).

— D2 derivation agent, 2026-08-08.

## CONSOLIDATED (2026-08-08; post-review; supersedes §10's pre-review status)

**Reviews (both in, same session):**
- `ADVERSARIAL_REVIEW_1_recompute.md` — R1, blind full recompute + completeness attack:
  **SUSTAINED-AMENDED** (47/47 own keys, `review1_recompute.py`/`review1_output.txt`;
  independent Isserlis-from-MGF; independent null-geodesic dragging; and an INDEPENDENT
  NUMERIC RAY-TRACE of the time-live depth law — RK4 past-cone integration confirming
  d ln(1+z)/dr_s = -(A_r + A_t/A)/(2A) at three depths to <0.5%: the law is real, not an
  algebra artifact). No kill found; no scale-manufacturing channel found.
- `ADVERSARIAL_REVIEW_2_scope.md` — R2, falsifier/scope/ledger adjudication: **AMENDED**;
  NO falsifier fires (F-RETRO both directions, F-FREEZE, F-ONEHORSE, F-SCOPE all
  adjudicated DOES-NOT-FIRE); D1 debt service graded with one gap (A-11), now closed.

**Amendments applied in place (ALL of them):** R1-A1 = the crossover reworded amplitude-set
but MAP-STEERED + vacuous B6b replaced by channel-layer keys B6b/B6c (§3, §10); R1-A2 =
G1b "coherent" downgraded to order-consistent with coefficient-match + frame-pair OPEN
(§3(ii), SS3); R1-A3 = mu(t) named in SS2 + the J->0 window-break interaction treated at
§7d; R1-A4 = Gaussianity stamped LOAD-BEARING on every no-feature verdict line (SS5, §3,
§7, §10); R1-A5 = two-sided threshold coincidence adopted + D4/E1 key relabels (§2, §7b,
in-script). R2-A-1 = window-set route added to the honest-bounds list (route 4); R2-A-2 =
excursion-set sub-claim tagged asserted/Gaussian-riding; R2-A-3 = machine-coverage domain
+ branch convention stated (§2); R2-A-4 (LOAD-BEARING) = ledger line SS9 (the time-live
lock-form ANSATZ; canon equivalence statics-scoped; P-D2-1 retagged; "no slice" softened
§7a/SS4/§4); R2-A-5 = SS5 all-order scale-invariance strengthening note; R2-A-6 = KEY D4
TRUE-BY-FORM; R2-A-7 = key-name collision flagged (§9); R2-A-8 = inline conditions inside
both quotable verdict spans (§3, §10); R2-A-9 = exceptional-point generality note (§2);
R2-A-10 = off-center observers made an explicit ledger line (P-D2-8); R2-A-11 = the
window-break time-live re-check DERIVED (§7d, KEYs A11a–c).

**HEADLINE (all stamps riding):** TIME-LIVE, the transfer map grows real ANISOTROPY
MACHINERY — per-direction depth modulation ln(1+z)(n) = ln rho - K(rho,s) mu(n)^2 with the
exact block spectrum and its exceptional-point threshold behind it, sky dragging
dpsi/dr = h/(AS), an anisotropic radial ruler — and that machinery is SCALE-TRANSPARENT:
featureless mixing fields yield featureless anisotropy [Gaussian-riding (SS5); ansatz-
scoped (SS9); below the fold onset]. NO native angular scale; the map's native
non-analyticities are THRESHOLDS-NOT-SCALES (amplitude edge mu_c = causal-labeling
degeneration; depth locus rho*s = 1; the fold A_t = -A A_r — the one genuinely new
time-live failure mode of D1's featureless-preservation theorem, a condition on free
profile data). Any pattern that does exist is FORCED phase-identical across tracers
(operator tracer-blind + achromatic). Crossovers and window breaks are input/window-SET
with MAP-STEERED drift (the D1-window-break class, both legs now derived). The static
limit recovers D1 exactly (8 keys). NO data touched; no comparison to any observed
pattern made or implied (F-RETRO). [No D4/fold-caustic synthesis here — matrix step.]

**SCOPE (unquotable without it):** TIME-LIVE / mixing ON (s != rho) / SS1–SS9 declared
sub-slices incl. the SS9 lock-form chart ansatz / central observer / class-(i) n > 0 /
test sources / Gaussian statistics load-bearing on no-feature verdicts / P-D2-5 flagged
(branch extension; metric-realization coefficient match OPEN).

**Four-check line:** pre-registered (frozen contract, this directory) — YES; full-space or
bounded-slice-justified — bounded DECLARED sub-slices, every OFF/simplification ledgered
(SS1–SS9) — YES; blind-verified on the load-bearing premises — YES (R1 full recompute incl.
numeric ray-trace; R2 independent spot-derivations + falsifier adjudication); forced
premises audited — YES (P-D2-1 retag, P-D2-5 flag, SS9 named by review and applied).
Ceiling honored: **verified LEAD** (same-session reviews; the external replication bar
travels with the result).

**Inheritance list, FINAL (what D2 does NOT settle):** (1) source back-reaction/
self-lensing (SS6/P-L7); (2) off-center observers (P-D2-8, explicit); (3) generic
B(t,r)/g_tr chart generalization — the SS9 ansatz's inheritance (exact forms would
change; qualitative verdict plausibly survives, unproven); (4) non-Gaussian statistics
beyond the stated all-order argument (SS5); (5) the metric-realization frame pair +
coefficient match for channel (i) (R1-A2 — the sharpest P-D2-5 load); (6) t-/r-varying
mixing along a sightline beyond SS7's composition coverage (SS2); (7) O-E geometries and
the origin of source statistics — unowned here (F-ONEHORSE; matrix step); (8) the
fold-onset x window-break interaction beyond the derived divergence (§7d, scoped).

— consolidation by the D2 derivation agent, 2026-08-08. NOT committed (owner's gate).
