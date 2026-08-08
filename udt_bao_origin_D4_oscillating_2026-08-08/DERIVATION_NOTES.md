# D4 — O-E's oscillating-solution question (derivation notes)

Date 2026-08-08 | branch grok | agent: D4 derivation (Fable) | MODE: OBSERVE
Contract: `PREREGISTRATION.md` (frozen). Parent: `udt_bao_origin_MAP_2026-08-08.md` §2 O-E + §5 D4.
Machine check: `derive_d4.py` → `run_output.txt` — **56/56 keys True**; every boxed claim cites its KEY.
STATUS: **verified LEAD** — R1 SUSTAINED-AMENDED + R2 AMENDED, all amendments applied in
place; see the CONSOLIDATED section (end). Same-session reviews; external bar travels.
NOT committed (owner's gate).

**SCOPE BANNER (stamps EVERY statement): STATIC profile / mu = 0 stratum / lock + areal-anchor
chart / central observer / n > 0 / spherically symmetric r-only oscillation (the declared class) /
test sources.** The time-live oscillation is NAMED INHERITANCE (D2/D4b), not silently dropped
(F-FREEZE). No data; ZERO BOSS contact; (ε, λ, φ₀, n) free symbols throughout (F-RETRO;
machine-discharged by KEY C11_FRETRO_no_float_atoms).

## 0. Ground + THE OBJECT + the osc-form declaration

Ground (cited AND re-derived where used): canon C-2026-08-06-1 (lock + areal anchor);
the 08-06 session-close INFERENCE "the depth profile = FREE boundary/initial data" (P1's
kinematic-freedom baseline — an inference, labeled, not a theorem); D1 CONSOLIDATED
(`udt_bao_origin_D1_static_transfer_2026-08-08/`) — dictionaries re-derived here (C0, C7a),
generic-A theorems re-proven here (Block A); O1/O2/O3 CONSOLIDATED (wall structure, measure
table, approach classes — the constraint set P1 tests against).

**THE OBJECT:** A(r) = A_bg(r)·[1 + ε·osc(r)], A_bg = (1 − r/R_w)ⁿ (class (i), c₀=1, n > 0
free). ε ≥ 0 WLOG (φ₀ → φ₀+π flips sign).

**OSC-FORM DECLARATION (the P2(a) fork carried whole, not sliced):** osc = cos(Φ(r)),
Φ = 2π·X_m(r)/λ + φ₀, where X_m is the radial measure of weight m built on the BACKGROUND
profile: dX_m/dr = A_bg^(−m). The three natural members: **m = 0 (areal, X₀ = r), m = 1/2
(proper length), m = 1 (optical/Fermat path)** — exactly O2's measure rows. "Periodic in which
variable" (P2(a)) is answered as a FUNCTION of m; no m is privileged (the same no-pin posture
as O3's branches). Closed form [KEY B1a]: X_m = R_w(1−u^(1−nm))/(1−nm) with u = 1−r/R_w;
at the knife-edge nm = 1: X = R_w·ln(1/u) [B1b], which IS the depth up to a constant —
proper n=2: ℓ_p = R_w·δ [B1c]; optical n=1: ℓ_opt = 2R_w·δ, the banked O2 rate re-derived
[B1d]. CONVENTION TAG: the argument uses the background measure (chose — declared; using the
full-A measure differs at O(ε), i.e. a reparametrization inside the same class).

## 1. The generic-A backbone (which D1 conclusions survive AUTOMATICALLY)

The contract's directed check: R_tt + A²R_rr ≡ 0 is GENERIC-A. Re-proven from scratch with
A a generic function (own Christoffel/Ricci code, Schwarzschild soundness anchor [A0]):

SURVIVE FOR ANY A(r) — oscillating included, no monotonicity used anywhere:
- the lock form g_tt·g_rr = −1 (the oscillation cannot break the lock) [A_lock];
- radial nulls exact geodesics with r affine [A1]; null condition [A3];
- **R_tt + A²R_rr ≡ 0 [A2a] ⇒ radial-null Ricci focusing R_kk = 0 exactly [A2b]**: the
  oscillating gradient produces ZERO convergence/defocusing on arriving bundles at any ε —
  with the vertex-cone/shear argument (D1, geometric, A-independent) this gives **d_A = r and
  d_L = (1+z)²r EXACTLY for the oscillating profile**;
- achromaticity: the orbit equation carries b = L/E only [A6a, A6b] — propagation is
  tracer/spectrum-blind for oscillating A;
- the Jacobian identity J ≡ dz/dℓ_p = −A′/(2A) = δ′(r) (D1 K17) [C7a].

USED MONOTONICITY IN D1 (must be re-derived; regime-split below): the single-valued
dictionary r(z) and dr/dz > 0 (G8); θ(z;s) strictly falling (K10); the fixed-angle amplitude
fall (K15); J growing (K18); the radial no-extremum theorem (K21). None of these is generic-A;
all become CONDITIONAL on the monotone regime of §2.

## 2. P1 — ADMISSIBILITY against the banked constraint set

**(a) Lock + areal anchor:** form-preserved identically [A_lock]; the oscillation lives in A.
**(b) Observer regularity A(0) = 1 [banked anchor]: a REAL restriction — the phase is pinned.**
A(0) − 1 = ε·cos(φ₀) exactly [B2] (every X_m(0) = 0), so admissibility demands cos(φ₀) = 0:
osc = ±sin(2πX_m/λ) [pinned representative checked, B2b] — or a c₀-renormalization absorbing
one parameter combination. The oscillation family loses EXACTLY ONE parameter combination to
the banked anchor; (ε, λ) stay free. (This pin later CANCELS the low-z envelope divergence —
§3b — a derived structural link, not a coincidence.)
**(c) A > 0 on (0, R_w): the amplitude bound.** The factor 1+ε·osc is linear in osc [B3a],
minimum 1−ε at osc = −1 [B3b]: **admissible iff ε < 1** (necessary whenever osc attains −1 in
range, i.e. whenever ≳ one full cycle fits; for fewer cycles the bound relaxes to
ε·max(−osc) < 1). Exact, free-symbol.
**(d) The A → 0 wall survives:** (1−ε)A_bg ≤ A ≤ (1+ε)A_bg pointwise [B3b, B4a] ⇒ A → 0 at
R_w [B4b]; depth ripple |δ_osc − δ_bg| = |−½ln(1+ε·osc)| ≤ −½ln(1−ε) bounded [B5a, B5b];
δ still diverges [B5c]. **O1's asymptote/wall theorem is NOT violated.**
**(e) O2 measure verdicts survive:** every integrand A^(−m) is squeezed by
(1±ε)^(−m)·A_bg^(−m) [B9a, B9b] ⇒ comparison test: **every finite/divergent cell of the O2
table keeps its verdict** (finite values shift within the two-sided bound). No banked measure
verdict is violated.
**(f) O3 approach class:** where the oscillation FREEZES (below), δ = κ·ln(1/σ) + const + o(1)
holds with the SAME κ and a shifted const [B10 + B5a]; at the knife-edge cells the const term
gains a bounded log-periodic decoration (osc periodic in depth itself, B1c/B1d); no class is
softened (R-2's never-softer-than-log stands — the ripple is bounded).

**(g) THE WALL-INTERACTION TRICHOTOMY (die/freeze/compress — the P1 centerpiece).**
The regime question is exactly the sign of J = δ′(r), derived exactly [B6a]:

  δ′ = [n(1+ε·osc) − ε·R_w·u·osc′] / [2·R_w·u·(1+ε·osc)]  —  z(r) monotone ⇔ numerator > 0.

For the m-parametrized oscillation the competing term scales as (2πεR_w/λ)·u^(1−nm)
(osc′ = ∓(2π/λ)A_bg^(−m)·sin-type). Trichotomy in the exponent 1−nm [B7a–B7e]:

| cell | argument measure at wall | oscillation near the wall | monotonicity |
|---|---|---|---|
| SUBCRITICAL nm<1 (areal all n; proper n<2; optical n<1) | FINITE (O2's finite cells) | **FREEZES**: finitely many cycles; competing term → 0 [B7a, B6c] | holds near wall ALWAYS; global condition = an interior amplitude bound (areal sufficient form: n·λ·(1−ε) ≥ 2πR_w·ε [B6b]) |
| CRITICAL nm=1 (proper n=2; optical n=1 — O2's knife edges) | log-divergent | **RIDES with depth**: X = R_w·ln(1/u) ∝ δ [B1c, B1d]: infinitely many cycles, equally spaced in depth — a log-periodic decoration | holds iff a finite amplitude threshold (term → const [B7b]; cycles infinite [B7d]) |
| SUPERCRITICAL nm>1 (proper n>2; optical n>1 — O2's divergent cells) | power-divergent | **COMPRESSES**: cycles accumulate at the wall faster than depth | **BREAKS for EVERY ε > 0**: the term is unbounded [B7c] and sweeps sign over infinitely many cycles [B7e] ⇒ δ′ < 0 on infinitely many intervals accumulating at the wall |

In measure language: a fixed areal wavelength STRETCHES to proper wavelength λ(1+z) → ∞ at the
wall; a fixed proper wavelength COMPRESSES areally as λ·(1+z)^(−1)... — the exact local law is
λ_p = λ·(1+z)^(1−2m) [C8b]. The trichotomy is exactly O2's finiteness table read as an
oscillation-fate table — a derived correspondence, not an analogy.

**(h) The supercritical cells: NOT forbidden — qualitatively restructured ("redshift
caustics").** A > 0, the wall, and all measure verdicts still hold there; what fails is
single-valuedness of z(r): the same z is reached at multiple r ("shell-crossing" in redshift
space), and at each J = 0 point the observed density dN/dz ∝ 1/|J| develops an integrable
fold-caustic spike. No banked verdict is violated (monotone z was never banked; D1's
monotonicity was a declared class premise P-L2, and D4 carries its own class declaration).

**P1 VERDICT: D4-ADMITTED (KINEMATIC — against the banked constraint set only; no native law
is banked, so no dynamical admissibility is claimed or claimable here [R2-A1]), with exact
restrictions** — (i) one phase combination pinned by the
banked anchor [B2]; (ii) amplitude ε < 1 [B3]; (iii) the trichotomy: in supercritical
parametrization×background cells any admitted oscillation necessarily produces non-monotone
z(r) near the wall (caustics) — a characterization, not a prohibition. **No banked verdict
(O1 asymptote, O2 table, O3 classes, lock, anchor, wall) is violated ⇒ D4-RESTRICTED is NOT
the landing; the restrictions are first-class structure INSIDE admission.**

## 3. P2 — THE IMPRINT TRANSFER (monotone regime; exact O(ε) laws; free symbols)

**(a) THE HUBBLE-RESIDUAL LAW (the centerpiece).** With d_L = (1+z)²r exact (generic-A optics,
§1) the oscillation enters ONLY through the dictionary r(z). Exact first-order inversion at
fixed z [C1]: r(z) = r_bg(z) + ε·(R_w·u/n)·osc(r_bg) + O(ε²), u = (1+z)^(−2/n). Hence [C2]:

  **Δμ(z) = (5/ln10)·(ε/n) · [u/(1−u)] · osc(r_bg(z)) + O(ε²),   u = (1+z)^(−2/n).**

- **PERIODICITY VARIABLE (P2(a)'s frozen question, answered exactly):** the residual is an
  ENVELOPE times an oscillation with **EQUAL CYCLE SPACING in ξ_m = (1+z)^(−2(1−nm)/n)**
  [C3a; R1-3 wording — envelope × equal-spaced oscillation, not a "periodic residual"] —
  ξ_m is the oscillation's own
  argument measure pulled through the depth dictionary. Per parametrization: areal →
  (1+z)^(−2/n) [C3b]; proper → (1+z)^(−(2−n)/n); optical → (1+z)^(−2(1−n)/n).
  **ln(1+z)-periodicity occurs EXACTLY at the O2 knife-edges nm = 1** (proper n=2, optical
  n=1) [C3c]. **Periodicity in z itself occurs at exactly ONE natural cell: optical
  parametrization on the n = 2 background** [C3d, C3f]; proper never [C3e]; areal never
  (exponent −2/n ≠ 1 for n > 0). A residual search must therefore scan the ONE-PARAMETER
  family of variables ξ_p = (1+z)^(−p), p > 0, plus the ln(1+z) edge — NOT assume
  z-periodicity; which p responds measures nm through p = 2(1−nm)/n.
- **THE ENVELOPE (parametrization-INDEPENDENT — same for every m):** amplitude ∝ u/(1−u),
  strictly falling in z [C4a], dying at the wall at the exact rate (1+z)^(−2/n) [C4b]: an
  oscillating-geometry residual MUST fade with redshift at a rate tied to the same n as the
  distance law. At z → 0 the banked phase pin (osc(0)=0, §2b) exactly cancels the 1/(1−u)
  divergence: the residual tends to the finite constant (5/ln10)·(ε/n)·(2πR_w/λ)
  [C4c] — absorbed by calibration (degenerate with an offset in M), honest limit stated.
- The radial cycle spacing in z [C8]: Δz_cyc = λ·(n/2R_w)·(1+z)^(1+2/n−2m) — growing with
  depth for every m ≤ 1/2; constant exactly at the (optical, n=2) cell.

**(b) THE ANGULAR / w(θ) IMPRINT.** Three exact statements, sharpest honest split:
- **Per shell: STILL FEATURELESS.** The angular action stays the identity (generic-A optics,
  §1): w_obs(θ; z) = C_src(r(z)·θ) with r(z) merely a (now oscillation-shifted) number per
  shell — log-slope ≡ −γ, no angular scale [C6, BY-FORM on the §1 backbone]. D1's per-shell
  theorem survives verbatim.
- **The rescaling's depth-drift now oscillates:** θ(z; s) = s/r(z) inherits the modulation
  θ = θ_bg·[1 − ε·(u/(n(1−u)))·osc + O(ε²)], EXACTLY ANTI-PHASED with the Hubble residual
  (δθ/θ = −δd_L/d_L at fixed z [C5, BY-FORM]) — a derived cross-observable phase lock:
  where the Hubble diagram reads far, standard angles read small, cycle by cycle.
- **A localized ANGULAR SCALE APPEARS at O(ε) through the map+window channel** (the D1
  distinction sharpened): the finite-bin projection weight in proper length is
  p(ℓ) ∝ p_z(z)·(dz/dℓ_p)⁻¹-normalized with the OSCILLATING Jacobian (below), so the window
  autocorrelation gains an oscillatory component at proper wavelength λ_p(z̄); the projection
  kernel then factors as λ_p^(1−γ)·f(r̄θ/λ_p) [scaling identity C9a], with f genuinely
  localized (γ=2 witness: f ∝ e^(−2π·r̄θ/λ_p) [C9b]) ⇒ **an angular preferred scale at**

    **θ_osc(z) = λ_p(z)/r(z),  λ_p(z) = λ·(1+z)^(1−2m)**  [C8b]

  i.e. areal: θ_osc = λ(1+z)/r(z); proper: θ_osc = λ/r(z); optical: θ_osc = λ/((1+z)r(z)).
  The DRIFT LAW of the induced angular scale reads out the parametrization m. Contrast with
  D1: there the window break was window-set (free symbols {r̄θ, W} only, present in flat
  space); HERE the new kernel symbol λ_p is GEOMETRY-set (the metric's own oscillation) —
  this is a scale the map+window manufactures from featureless input at O(ε). Per-shell w(θ)
  remains featureless; the scale lives strictly in the depth-projection channel.
  **VISIBILITY CONDITION (R1-1, ledgered P-D12):** the θ_osc feature exists only where the
  projection window spans ≥ one λ_p cycle (proper bin width W ≥ λ_p(z̄)); a narrower window
  cannot resolve the oscillatory component of the radial weight, and the kernel reverts to
  D1's window-set break alone.
**(c) TRACER-UNIVERSALITY + PHASE COHERENCE (derived, not assumed):**
- The full map (angular identity + oscillating dictionaries) carries ONLY the symbols
  {z, n, R_w, λ, ε, m, osc-value} — machine free-symbol audit [C10]; no source property
  exists in the operator; propagation achromatic [A6b]. ⇒ **every tracer at the same z
  inherits the SAME modulation with the SAME phase** — tracer-dependence can enter only
  through per-tracer selection WINDOWS (window-set, as in D1 §4(i)), never through the map.
- Phase coherence across the sky: the declared class is r-only (spherically symmetric about
  the central observer) ⇒ at fixed z the phase is IDENTICAL in every direction — an
  isotropic, z-locked pattern [class-tagged: an angular-dependent oscillation is outside
  this class declaration, named]. Phase coherence across z-shells: the phase advances
  deterministically as Φ(z) = 2πX_m(z)/λ + φ₀ — fully coherent, no stochastic component.
**(d) THE RADIAL / Δz IMPRINT (the oscillating Jacobian, exact):**
- J(r) = δ′(r) exactly [C7a, B6a]. First order along the dictionary [C7b, C7b2 + BY-FORM
  chain rule]: the observed density of a mean-uniform-in-ℓ_p test field [tagged posit,
  P-L8-analog] is modulated as δ(dN/dz)/(dN/dz) = (ε/n)·[R_w·u·osc′ − osc](r_bg(z)) + O(ε²).
- **THE LOUDNESS HIERARCHY [C7d]:** the ratio of the dN/dz modulation amplitude to the
  distance-modulation amplitude is EXACTLY r·Φ′ (= 2πr/λ areal) — the number of radians of
  oscillation phase across the depth. A many-cycle oscillation is parametrically LOUDEST in
  the radial 1-point channel (dN/dz), quietest in the Hubble diagram; the derivative factor
  also advances the radial phase by π/2 against the distance channels in the rapid limit.
- The radial two-point function: in the monotone regime the no-extremum argument survives
  (dw/dz₂ = C′·(1/J), fixed-sign product, J > 0) — featureless radial input still gives no
  bump in the CORRELATION; the oscillation lives in the 1-point function and the Δz
  dictionary. In the caustic regime dN/dz develops fold spikes at J = 0 (§2h).

**(e) MAP §2 O-E SIGNATURE SUPERSESSIONS (R2-A3, recorded):** the MAP's provisional O-E
signature list is superseded where this derivation sharpened it: **signature (iii)**
("oscillatory residuals in the SNe Hubble diagram at the corresponding spacing") — the
spacing is EQUAL IN ξ_m = (1+z)^(−2(1−nm)/n), generically NOT in z; any future SNe-residual
preregistration must scan the ξ_p = (1+z)^(−p) family plus the ln(1+z) edge, not assume
z-periodicity. **Signature (ii)** ("an optics component") — only PARTIALLY delivered here:
the achromatic propagation and the d_L/θ modulations are derived, but surface-brightness/
image-level optics of background light was not derived in this package — named open.

## 4. Premise ledger (every choice; F-FREEZE discharge)

| # | premise | tag |
|---|---|---|
| P-D1 | metric = lock + areal anchor chart | THEORY (canon C-2026-08-06-1) |
| P-D2 | background class (i): A_bg = (1−r/R_w)ⁿ, n > 0 free | declared-slice (prereg §1; O2/O3 family) |
| P-D3 | oscillation class: multiplicative, r-only, osc = cos(2πX_m/λ+φ₀), m ∈ {0, ½, 1} carried | declared-slice (the D4 class declaration; F-SHOP-CLASS analog); additive/angular/time-dependent forms OUT, named |
| P-D4 | argument built on BACKGROUND measure | CHOSE (declared §0; full-A measure = O(ε) reparametrization in-class) |
| P-D5 | STATIC; mu = 0 stratum | declared-slice (F-FREEZE; D2/D4b inheritance) |
| P-D6 | observer at r=0, A(0)=1 | THEORY (banked anchor) — actively load-bearing here (phase pin) |
| P-D7 | 1+z = A^(−1/2) | THEORY (banked ratio identity; re-derived C0) |
| P-D8 | test sources; geometric optics; c=1 | FREE-declared / Category-A (as D1 P-L7/P-L10/P-L11) |
| P-D9 | featureless input = power law in proper separation (for §3b/§3d statements) | definition (D1 §1, cited) |
| P-D10 | mean-uniform-in-ℓ_p test field (for the dN/dz law only) | FREE — tagged posit (D1 P-L8 analog) |
| P-D11 | O(ε) laws first-order; exact statements labeled exact | scope — VALIDITY DOMAIN (R2-A2): the O(ε) remainder carries Ξ′, so the relative error of the first-order laws is ~ ε·2πR_w·u/(n·λ); it reaches O(1) exactly at B6b-bound saturation — "ε small" ALONE is not the validity domain for many-cycle combs (ε·R_w/λ small is). The exact statements (lock, A2a/A2b, B6a criterion, the trichotomy) are untouched by this |
| P-D12 | θ_osc visibility: projection window spans ≥ one λ_p cycle (W ≥ λ_p(z̄)) | scope condition (R1-1) on the §3b angular-scale statement only |

## 5. Falsifier discharge (prereg §3)

- **F-RETRO (primary):** (ε, λ, φ₀, n, m) symbolic everywhere; no 150 Mpc, no observed angle,
  no fitted n in any load-bearing step; machine scan: zero float atoms in audited expressions
  [C11]. No derived law was compared to any observed number in this package.
- **F-TEMPLATE (posing audit):** every question ran admit-and-characterize: P1 asked what the
  banked constraints DO to the object (result: pin + bound + trichotomy); P2 asked what an
  admitted object imprints (result: signature laws as functions of free symbols). At no point
  was any (ε, λ, m, n) chosen to make any known pattern appear; the closest hazard — the
  angular-scale finding in §3b — was DERIVED from the Jacobian channel with its location left
  symbolic, and its D1-contrast (geometry-set vs window-set) stated both ways. No re-declaration
  was needed; the make-BAO framing was never entered.
- **F-FREEZE:** ledger §4 complete; static/mu=0 are the declared slice; the time-live
  oscillation is named inheritance (§6).
- **F-ONEHORSE guard:** O-E's row only; no statement about O-A/O-B/O-C/O-D; the O-C-adjacent
  D1 theorems are cited as GROUND, not adjudicated against O-E.
- **F-SCOPE:** no data, ZERO BOSS contact, no verdicts on other origins, no accrual dynamics
  (the "matter aligns along it" step remains O-E's own inheritance, underived).

## 6. What the static slice CANNOT answer (named inheritance)

1. TIME-LIVE oscillation (D2/D4b): a standing wave vs a static profile; whether the
   clock→screen mixing channel (λ_t) carries or damps it; phase evolution.
2. Whether any NATIVE LAW admits/selects such a profile — none is banked; the admissibility
   here is kinematic, scoped to the banked constraint set (the 08-06 free-profile INFERENCE
   is the baseline and is itself labeled unproven).
3. Angular-dependent or non-multiplicative oscillations (outside P-D3's class).
4. Matter accrual along the structure (O-E's own inheritance; out of scope by contract).
5. Source back-reaction; off-center observers (the phase-coherence signature is
   central-observer-scoped).
6. The full nonlinear (all orders in ε) observable laws; the caustic-regime statistics
   beyond the fold-spike characterization.
7. (R1-2) Multi-wavelength content: an INCOMMENSURATE superposition of oscillations IS
   covered at O(ε) — the laws superpose linearly, each component carrying its own
   (ε_i, λ_i, m_i) laws — but nonlinear cross-terms are not. GENUINELY OUTSIDE P-D3:
   ε(r)-envelope forms (amplitude varying with depth) — uncovered, named.

## 7. LANDED OUTCOME (prereg §4): **D4-ADMIT+IMPRINT**

**P1: ADMITTED (KINEMATIC — against the banked constraint set only; no native law is banked,
so no dynamical admissibility is claimed [R2-A1]) with exact restrictions** — phase pinned by
the banked anchor (cos φ₀ = 0);
amplitude ε < 1; monotonicity criterion exact [B6a] with the wall-interaction TRICHOTOMY
(freeze / log-periodic ride / compress-with-caustics) mapping one-to-one onto O2's
finiteness table; NO banked verdict violated (O1/O2/O3/lock/anchor/wall all survive, some
with derived decorations). **P2: the imprint laws delivered as free-symbol functions** —
residual law + parametrization-independent envelope + the periodicity-variable answer
(ξ_m = (1+z)^(−2(1−nm)/n); ln(1+z) exactly at the O2 knife-edges; z-periodicity at exactly
one natural cell (optical, n=2)); the map+window angular scale θ_osc = λ(1+z)^(1−2m)/r(z)
(geometry-set, unlike D1's window-set break) with per-shell featurelessness intact; derived
tracer-universality + full phase coherence (z-locked, isotropic); the oscillating Jacobian
with the loudness hierarchy (radial 1-point channel louder than the Hubble diagram by
exactly r·Φ′) and the anti-phase lock between angular and distance channels.

Check count: **56/56 keys True** (`run_output.txt`), of which C5/C6 and the C7b+C7b2
composition are BY-FORM/composition steps (labeled inline); the load-bearing machine content
is Blocks A (generic-A backbone, own Ricci code, Schwarzschild-anchored), B (P1), C (P2).

STATUS: **LEAD / UNBANKED — two independent adversarial reviews owed** (R1 full blind
recompute + completeness attack; R2 falsifier/scope/posing-audit adjudication) before any
banking; verified-LEAD ceiling after that (same-session; external bar travels). NOT committed
(agent contract: do not commit).

## LAB-LOG (process disclosure; Category-A conditioning only)

- Reproduce: `timeout 480 python3 -u derive_d4.py` (CPU, ~1–2 min; single process).
- First run: 53/56 — three keys (B1a/B1c/B1d) failed as DECIDABILITY-of-form issues only:
  sympy cannot combine (u^n)^(−m) → u^(−nm) or log(1/u) → −log(u) when u = 1−r/R_w has
  unknown sign. Restated in the positive variable uu = 1−r/R_w with the chain rule
  dX/dr = dX/du·(−1/R_w) applied explicitly — the same mathematical claims, now decidable
  (the D1 precedent: restatements PROVE the same claim, none weakens a check; no claim was
  changed to make a check pass). Second run: 56/56.
- Limits with symbolic exponents were routed through positive substitution variables
  (uu, q, g) from the start (the D1 gruntz-hang scar, applied prospectively); C4c's
  low-z limit was restated via x = r_bg/R_w → 0⁺ (no symbolic exponent enters).

## CONSOLIDATED (2026-08-08; post-review; supersedes the §7 pre-review status)

**Reviews (both in, same session):**
- `ADVERSARIAL_REVIEW_1_recompute.md` — R1, blind full recompute + completeness attack:
  **SUSTAINED-AMENDED** (39/39 own keys; everything reproduced; the metric-set-vs-window-set
  distinction AFFIRMED as real). No kill found.
- `ADVERSARIAL_REVIEW_2_scope.md` — R2, falsifier/scope/posing adjudication: **AMENDED**;
  NO falsifier fired (F-RETRO, F-TEMPLATE, F-FREEZE, F-ONEHORSE, F-SCOPE all DOES-NOT-FIRE).

**Amendments applied in place (all of them):** R2-A1 = both verdict lines carry the KINEMATIC
ceiling inline (§2, §7); R2-A2 = P-D11 validity-domain wording (relative error
~ ε·2πR_w·u/(n·λ), O(1) at B6b saturation; exact statements untouched); R2-A3 = the MAP §2
O-E signature supersessions recorded (§3e: signature (iii) → ξ_m spacing, not z; signature
(ii) optics component PARTIAL, named); R1-1 = the θ_osc visibility condition (§3b + ledger
P-D12: window ≥ one λ_p cycle); R1-2 = §6 items 7 (incommensurate multi-λ = O(ε)
superposition, stated; ε(r)-envelopes genuinely outside P-D3, named uncovered); R1-3 = the
§3a wording (envelope × equal-cycle-spacing in ξ_m, not "periodic residual").

**HEADLINE RESULT:** the oscillating depth-profile component is **ADMITTED-KINEMATIC with
exact restrictions** (phase pinned by the banked anchor; ε < 1; the exact monotonicity
criterion B6a) and its wall interaction is a derived TRICHOTOMY (freeze / log-periodic ride /
compress-with-redshift-caustics) mapping one-to-one onto O2's finiteness table — no banked
verdict (O1/O2/O3/lock/anchor/wall) is violated. The imprint laws, all free-symbol: the
Hubble residual = the parametrization-independent fading envelope (5/ln10)(ε/n)·u/(1−u)
times an oscillation with **equal cycle spacing in ξ_m = (1+z)^(−2(1−nm)/n)** (ln(1+z)
exactly at the O2 knife-edges; z-spacing at exactly one natural cell (optical, n=2)); a
**METRIC-SET localized angular scale θ_osc(z) = λ(1+z)^(1−2m)/r(z) in the map+window channel**
(affirmed real by R1; visibility condition attached: window ≥ one λ_p cycle) while per-shell
w(θ) stays featureless; and the OVER-CONSTRAINED signature set — the exact anti-phase lock
δθ/θ = −δd_L/d_L plus the loudness hierarchy (dN/dz louder than Δμ by exactly r·Φ′, phase-
advanced π/2) plus tracer-universal, isotropic, z-locked phase coherence — one geometry, many
mutually-locked channels. NO DATA TOUCHED; no comparison to any observed pattern (F-RETRO).

**SCOPE (unquotable without it):** STATIC / mu = 0 / lock + areal-anchor chart / central
observer / n > 0 / r-only multiplicative oscillation class / test sources / O(ε) laws inside
the P-D11 validity domain.

**Four-check line:** pre-registered (frozen contract, this directory) — YES; full-space or
bounded-slice-justified — bounded slice, DECLARED (class + static, every choice ledgered) —
YES; blind-verified on the load-bearing premise — YES (R1 full recompute, 39/39 own keys; R2
independent adjudication); forced premises audited — YES (ledger P-D1–P-D12 + reviews).
Ceiling honored: **verified LEAD** (same-session reviews; the external replication bar
travels with the result).

**Inheritance (open, named):** caustic-regime statistics beyond the fold-spike
characterization; the time-live oscillation (D2/D4b — standing wave vs static profile;
the λ_t mixing channel); accrual dynamics (O-E's own step, underived by contract);
ε(r)-envelope forms (outside P-D3). No D2/fold synthesis here — that is the matrix step.

— consolidation by the D4 derivation agent, 2026-08-08. NOT committed (owner's gate).
