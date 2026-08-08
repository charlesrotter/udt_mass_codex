# D1 — the static angular transfer function (derivation notes)

Date 2026-08-08 | branch grok | agent: D1 derivation (Fable) | MODE: OBSERVE
Contract: `PREREGISTRATION.md` (frozen). Parent: `udt_bao_origin_MAP_2026-08-08.md` §2–§4,
`udt_bao_origin_MAP_2026-08-08_D0_MATRIX.md` (debt list D1 items 1–5).
Machine check: `derive_d1.py` → `run_output.txt` (every boxed claim cites its KEY).
STATUS: **verified LEAD** — R1 SUSTAINED-AMENDED + R2 AMENDED, all amendments applied
in place; see the CONSOLIDATED section (end). Same-session reviews; external bar travels.

**SCOPE BANNER (stamps EVERY statement below): STATIC / mu = 0 stratum / lock +
areal-anchor chart.** Nothing here may be quoted unscoped (CP2; owner no-freeze ruling).
No data touched; ZERO BOSS contact; no fitted numbers — n is a free symbol throughout
(F-RETRO; machine-discharged by KEY K_FRETRO_no_float_atoms_in_derivation).

## 0. Ground and sightline geometry

Metric [THEORY, canon C-2026-08-06-1]: ds² = −A c²dt² + dr²/A + r²dΩ², with the class-(i)
profile A(r) = (1 − r/R_w)ⁿ, n a FREE symbol (declared class; prereg §1). Observer at r=0
with φ(0)=0 ⇒ A(0)=1 [THEORY, banked observer normalization] [KEY G1]. c = 1 units
(Category-A conditioning).

Derived sightline facts (all exact, native to this metric):

- **The center is regular and locally flat**: the proper-radius integrand A^(−1/2) =
  1 + n·r/(2R_w) + O(r²), so ℓ_p(r) = r + O(r²) near the observer [KEY G2].
- **Killing conservation**: t and the azimuth are cyclic in the geodesic Lagrangian ⇒
  E = A·ṫ and L = r²·(dφ/dλ) are conserved along every geodesic [KEYs G3a, G3b].
- **Only radial null geodesics reach r = 0**: the radial potential is ṙ² = E² − A·L²/r²,
  and A(0)=1 forces ṙ² → −∞ as r → 0⁺ for any L ≠ 0 — a turning point at finite radius.
  Every photon ARRIVING at the observer traveled exactly radially [KEY G5].
- **r is an affine parameter on radial nulls**: the ray (ṫ, ṙ) = (E/A, E) solves the radial
  geodesic equation exactly, so d²r/dλ² = 0 [KEY G4].
- **Redshift and the depth dictionary**: the static Killing-frequency ratio gives
  1 + z = A(r_s)^(−1/2); inverted for the class-(i) profile: r(z) = R_w[1 − (1+z)^(−2/n)],
  verified by A(r(z)) = (1+z)^(−2) [KEY G7]; dr/dz = (2R_w/n)(1+z)^(−2/n−1) > 0 —
  strictly monotone [KEYs G8a, G8b]. (Re-derives the banked D1_FORMULAS.md §1 forms;
  cited AND re-derived per contract.)

**The second-order structure demanded by T1 (shear/convergence analogs), derived exactly:**

- **Shear = 0**: the two transverse directions of a radial bundle scale identically with r
  (their ratio is r-independent; the axial rotation symmetry about each radial ray forces
  isotropic magnification) [KEY K5 — TRUE-BY-FORM (R1-V1), illustrative only; the
  substantive content is the vertex-cone argument: every arriving ray is radial (G5), so a
  beam through r=0 is a cone of radial rays whose cross-section is carried by the exact
  r²dΩ² factor — both transverse directions scale as r by construction; R1-verified].
- **Ricci focusing = 0 — a lock-chart theorem**: for a GENERIC profile A(r) in this chart
  (g_tt·g_rr = −1), the Ricci tensor obeys R_tt + A²·R_rr = 0 identically, hence
  R_μν k^μ k^ν = 0 EXACTLY for every radial null vector k [KEYs K6a, K6b]. The A(r)
  gradient produces NO convergence/defocusing of arriving bundles at any order — this is
  native structure of the lock + areal anchor, not an approximation.
- **Consistency**: with σ = 0 and R_kk = 0 the Sachs focusing equation is solved by
  d_A = r with r affine [KEY K7 — TRUE-BY-FORM given K6b (R1-V1); the substantive machine
  content is K6a/K6b + G4]. All magnification is purely areal: d_A(z) = r(z), exact.

Consequence (the sightline geometry in one sentence): **the observed sky direction of every
source equals its angular coordinate** — arriving rays are radial (G5), the center is
locally flat (G2), so the angle between two arriving rays equals their coordinate angular
separation Δψ exactly [KEY K2 — TRUE-BY-FORM (R1-V1): a Euclidean dot-product triviality;
the actual claim rides G2 + G5, both machine-discharged, and the composition is R1-verified].
Statics additionally makes w time-independent and equalizes
travel times across a shell (equal r_s ⇒ equal Fermat length), so equal-time comparison is
automatic.

## 1. "Featureless" — precise definition and justification

**Definition.** A two-point function C on separations is FEATURELESS (scale-free) iff it is
scale-covariant: C(λs) = g(λ)·C(s) for all λ > 0 — no separation is distinguished.
Differentiating at λ = 1 gives s·C′(s) = κ·C(s), whose smooth solutions are exactly the
power laws C(s) = K·s^κ [KEY K3]. Justification: (i) any non-power-law C singles out
scales (the stationary structure of its log-slope); (ii) power laws are precisely the fixed
points of the scaling group; (iii) operationally, a "preferred angular scale" in w(θ) means
a localized departure of the log-slope d ln w/d ln θ from constancy — so CONSTANT log-slope
is the machine-checkable certificate of "no feature". This is the definition the checks use.

**Where the input lives.** The source field's correlations are taken in PROPER separation on
the shell (the induced shell metric is r_s²dΩ² — an exact round sphere; proper great-circle
separation s = r_s·Δψ at ALL angles [KEY K1 — TRUE-BY-FORM (R1-V1): an integral of a
constant; the induced-metric statement is definitional]). This is the D1F proper-ruler
REALIZATION premise [tagged]. FORK COVERED: if instead the input is declared featureless in
coordinate angle, T's angular action is the identity (§2) and the verdict below is
UNCHANGED — only the proper dictionary differs. A THIRD realization — 3-D geodesic (chord)
separation through the spatial slice — is named at §6 (R1-V4); the verdict does not ride
the realization fork on any of the three.

**Honest caveat**: on a compact sphere an exactly scale-free C cannot extend past the domain
scale (separations ≤ π radians); that compactness belongs to the INPUT's domain, and T (an
identity on the sphere, §2) neither creates nor moves it.

## 2. T1 — EXISTENCE: does T imprint any preferred angular scale? **NO (proven).**

**The transfer map, derived**: a source point on the shell at depth z (areal radius
r_s = r(z)) at angular position Ω is observed at sky position Ω — T's angular action is the
IDENTITY on the sphere (radial-only arrival G5 + flat center G2 + angle dictionary K2).
The full map on two-point statistics is therefore the identity composed with the proper
dictionary s = r_s·θ:

  **w_obs(θ; z) = C_src(s = r(z)·θ)** — exact at all θ ∈ (0, π], no small-angle expansion.

**The load-bearing statement, machine-proven (static map)**: featureless in ⇒ featureless out.
- Per shell: C = K·s^(−γ) ⇒ w_obs(θ) = K·r_s^(−γ)·θ^(−γ); log-slope ≡ −γ, exactly
  constant — NO preferred angular scale exists in the output [KEY K4].
- Finite z-bin — CORRECTED per R1-V2: the SAME-SHELL superposition (any weights) preserves
  the power law [KEY K8], but the binned w(θ) of a finite-depth window is NOT a pure power
  law: cross-shell pairs contribute ξ(√(Δℓ² + r̄²θ²)) terms, and the exact binned kernel
  carries a smooth BREAK at θ_break ≈ W/r̄ (W = the proper half-width of the bin window;
  R1's top-hat witness: log-slope → 1−γ at r̄θ ≪ W, → −γ at r̄θ ≫ W) [R1 ATTACK_* keys].
  The break scale is WINDOW-SET: the binned kernel's free symbols are exactly {r̄θ, W} —
  no metric symbol enters except through the smooth dictionaries — so it is imported by the
  tracer's selection window, present identically in flat space, and is NOT a scale
  manufactured by T from featureless input. THE MAP adds no scale; the OBSERVATION WINDOW
  does add one, and the metric controls only its smooth depth-drift (θ_break(z) ≈
  Δℓ_p(bin)/r(z), with Δℓ_p(bin) = Δz_bin/J(z) for a fixed-Δz window) — first-class
  derived structure of map-plus-window, named for any later data confrontation.
- Full 3-D projection (Limber-type, local-flatness premise P-L12): for a 3-D power-law
  ξ(σ) = σ^(−γ), the line-of-sight integral of ξ(√(Δ² + (r̄θ)²)) scales EXACTLY as
  (r̄θ)^(1−γ) (substitution Δ = r̄θ·u; convergence for γ > 1) ⇒ w(θ) ∝ θ^(1−γ) — a pure
  power law in the INFINITE-UNIFORM-LOS limit only (the finite-window case is the bullet
  above) [KEY K8b, re-scoped per R1-V2].
- γ depth-dependence (R2-A2): if γ drifted smoothly in z, the binned w(θ) would not be a
  pure power law, but its log-slope would vary SMOOTHLY (broadband) — no localized scale
  appears; the no-localized-scale verdict survives, "pure power law preserved" does not.
- No second-order leak: the only candidate distortions — shear and A′-driven convergence —
  are both exactly ZERO on arriving bundles (K5, K6b); there is no channel by which the
  A(r) gradient can write angular structure onto the sky for the central observer.

**T1 VERDICT (STATIC / mu=0 / lock chart): the static transfer map is a pure smooth
rescaling — it imprints NO preferred angular scale on any featureless input.** An angular
feature at ANY scale (degree-scale included) CANNOT be manufactured by the static comparison
map from statistically plain matter [R2-A3 wording]. (Scoped: this does NOT kill O-C —
D2's time-live layer is owed regardless; CP2.)

## 3. T2 — the depth law of the rescaling (the honest T2 content)

No scale is imprinted, so there is no "drift of an imprinted scale" to derive; the exact
depth-dependence of the smooth rescaling is the deliverable [prereg T2]:

- Magnification law: a proper separation s at depth z is seen at **θ(z; s) = s / r(z)**
  = s / (R_w[1 − (1+z)^(−2/n)]) — angle-per-proper-length μ(z) = 1/r(z).
- Strictly monotone: dθ/dz = −s·(dr/dz)/r² < 0 for every n > 0 — the rescaling has no
  critical point in z; the depth law is itself featureless in z [KEYs K10a, K10b; the
  r(z) > 0 leg rides the calculus lemma (1+z)^(2/n) > 1 for z > 0 (value 1 at z = 0 +
  strictly positive derivative) — KEYs K10lemma_a, K10lemma_b, K10c].
- High-z limit: θ → s/R_w — the class-(i) minimal-angle floor (finite d_A = R_w at the
  wall), re-derived via the q = (1+z)^(−2/n) → 0 substitution with the exponent-sign step
  machine-checked [KEYs K9a, K9b]; n stays a free symbol throughout.

## 4. T3 — cross-tracer: is T tracer-blind? **YES at this layer (derived).**

- **Achromatic**: null paths depend on the impact parameter b = L/E only — the overall
  frequency scale cancels from the orbit equation, so propagation is identical for photons
  of any energy/spectral origin [KEY K13].
- **Free-symbol audit**: the complete static map — angular action (identity, Δψ) plus depth
  dictionary z(r_s) = (1−r_s/R_w)^(−n/2) − 1 — contains ONLY geometry symbols
  {Δψ, r_s, R_w, n}. No parameter referencing any source property EXISTS in T; T is one
  fixed operator applied to whatever field is there [KEY K14].
- Channels by which tracer physics COULD enter, named honestly: (i) the tracer's own
  selection window p(r_s) enters the §2 bin projection — it multiplies weights, never the
  operator, so it cannot make T tracer-dependent; but per R1-V2 the window DOES set the §2
  projection break θ_break ≈ W/r̄ (window-set, not map-made — a per-tracer window gives a
  per-tracer break location, honestly a tracer-dependent feature of map-PLUS-window, not
  of T); (ii) source self-gravity/back-reaction
  (lensing by the clustered field itself) is excluded by the test-source premise P-L7 —
  a D2+/beyond-static inheritance; (iii) non-gravitational propagation (absorption,
  dispersion) is outside metric optics — outside this arc's map entirely.
- **Honest limit (D0 debt item 3)**: the sharp O-C signature "identical pattern AND phase
  across tracers" is VACUOUS at the static layer — T generates no pattern here, so there is
  no T-generated pattern whose phase could be compared. What IS derived: the OPERATOR is
  tracer-blind. Whether a time-live T generates a pattern (whose tracer-universality would
  then follow from operator-blindness) is D2's question — inheritance, not answered here.

## 5. T4 — amplitude vs depth (exact)

- **T is value-preserving at fixed proper separation**: w_obs(θ = s/r_s; z) = C(s),
  independent of depth — the map relabels separations, it does not attenuate correlation
  amplitudes [KEY K16]. (Position statistics; no surface-brightness/Tolman factor enters
  a correlation of number counts.)
- At FIXED ANGLE the amplitude falls as **w(θ; z) ∝ r(z)^(−γ)** — purely because a fixed θ
  probes a larger proper separation at larger depth; strictly monotone fall, no feature in
  z [KEYs K15a, K15b, K15c]. Finite-bin projection multiplies by z-smooth weights and adds
  no structure beyond the §2 window break (R1-V2), which is window-set, not map-made.

## 6. T5 — the radial (line-of-sight) imprint

Re-derived from the metric (proper radial element dℓ_p = A^(−1/2)dr, realization premise;
depth δ = −½ln A), for GENERIC A(r) — the banked D1_FORMULAS.md §4 identities:

  **dz/dℓ_p = −A′/(2A) = dδ/dr = (1+z)·dδ/dℓ_p** [KEYs K17a, K17b]

Class-(i) closed form at depth z: **J(z) ≡ dz/dℓ_p = (n/2R_w)(1+z)^(2/n)** — strictly
GROWING with depth for every n > 0 [KEYs K18a, K18b].

- **Locally** (separations ≪ the depth scale): Δz = J(z)·Δℓ_p — a pure rescaling; power-law
  radial input ⇒ constant log-slope in Δz: featureless preserved [KEY K19].
- **Finite separations, exactly**: the observed radial correlation is
  w(z₂) = C_r(ℓ_p(z₂) − ℓ_p(z₁)) with ℓ_p(r) = (2R_w/(2−n))[1 − (1−r/R_w)^((2−n)/2)]
  (n ≠ 2; wall value 2R_w/(2−n) for n < 2 — D1F §5 re-derived) [KEYs K20a, K20b].
  **No-extremum theorem**: dw/dz₂ = C_r′·(1/J(z₂)) — a fixed-sign product (C_r′ < 0 for a
  falling featureless input, 1/J > 0), so the monotone reparametrization can NEVER create a
  local extremum: no bump, no peak, no preferred Δz scale [KEYs K21a, K21b].
- **The single smooth departure the radial map carries**: the separation dictionary's
  log-slope bends away from 1 at second order, d lnΔℓ_p/d lnΔz = 1 − Δz/(n(1+z₁)) + O(Δz²)
  — the only scale in the bend is **n·(1+z₁), the depth/shape scale itself** [KEY K22]:
  a broadband distortion at separations comparable to the depth, never a localized feature.
- **The legs are asymmetric, exactly**: the ANGULAR dictionary is linear at ALL separations
  (log-slope ≡ 1, zero curvature at every order [KEY K23]); the RADIAL dictionary is linear
  only locally, with the depth-scale bend above. This derived asymmetry is first-class
  observe-mode structure of the static map. REALIZATION CAVEAT (R1-V4): K23's "linear at
  all orders" holds on the great-circle proper ruler; a third natural realization — 3-D
  geodesic (chord) separation through the spatial slice — makes the shell dictionary
  nonlinear at all orders (already 2·r_s·sin(θ/2) in FLAT space), so the linearity is
  realization-dependent. Verdict robust on that ruler too: the chord nonlinearity exists
  identically in flat space (not a metric imprint), is smooth and broadband, and the
  no-extremum argument extends (a monotone smooth dictionary of a monotone falling input
  creates no bump).

**T5 VERDICT (STATIC / mu=0 / lock chart): featureless radial input ⇒ NO preferred Δz
scale out; the static radial imprint is the growing stretch J(z) plus a depth-scale
broadband bend — no feature.**

## 7. Premise ledger (every ON/OFF choice; F-FREEZE discharge)

| # | premise | tag |
|---|---|---|
| P-L1 | metric = lock + areal anchor chart | THEORY (canon C-2026-08-06-1) |
| P-L2 | profile class (i): A = (1−r/R_w)ⁿ, n FREE symbol **with n > 0** (R1-V3: every monotonicity/positivity key rides sympy positive-symbol declarations; for n < 0 the profile grows with depth and the redshift dictionary inverts — outside this slice) | declared-slice (prereg §1; class declaration + declared domain restriction) |
| P-L3 | STATIC — all time dependence OFF | declared-slice (CP2a; D2 owed regardless) |
| P-L4 | mu = 0 stratum | declared-slice (banked static kinematic inertness cited as SCOPE, not physics) |
| P-L5 | observer at r = 0, φ(0) = 0 ⇒ A(0) = 1 | THEORY (banked observer normalization) |
| P-L6 | redshift 1+z = A^(−1/2) | THEORY (banked ratio identity; used via G7) |
| P-L7 | sources are TEST structures (no self-lensing/back-reaction on the metric) | FREE — declared; inheritance beyond static |
| P-L8 | source field statistically homogeneous + isotropic per shell, AND statistically homogeneous across depth (single index γ; used by K8/K8b) [R2-A2] | FREE — the posed "plain input" (the question's own subject); a z-drifting γ gives a smoothly varying log-slope — broadband, still no localized scale (§2) |
| P-L9 | featureless ≔ scale-free ≔ power law, in PROPER separation | definition (§1, justified); realization = D1F proper-ruler tag; coordinate-angle fork covered, verdict unchanged |
| P-L10 | geometric optics (photons on null geodesics; eikonal limit) | Category-A technique (soundness: achromaticity K13) |
| P-L11 | c = 1; equatorial-plane reduction in geodesic checks | Category-A conditioning (spherical symmetry makes it lossless) |
| P-L12 | 3-D projection step uses local flatness (separations ≪ depth scale) | scoped premise; the per-shell statement carries ALL separations without it |

No other sector was frozen. OFF sectors are exactly P-L3 and P-L4, both declared-slice.

## 8. Falsifier discharge (prereg §3)

- **F-RETRO**: n free symbol everywhere; no E-value, no angle number, no fitted parameter
  appears anywhere in script or notes; machine key K_FRETRO_no_float_atoms confirms no
  float literal enters any audited expression. The derivation's outputs are symbols and
  exact rationals only. No drift direction was targeted: the T1/T5 results are
  featureless-preserving — neither toward nor away from any known pattern.
- **F-FREEZE**: ledger §7 complete; the two OFF sectors are the declared slice.
- **F-ONEHORSE**: this package contains no statement about O-A/O-B/O-D/O-E and no
  comparative origin claims. (Matrix consequences belong to the arc, not to D1.)
- **F-SCOPE**: no data contact; zero BOSS contact of any kind; no cosmology numbers.

## 9. What the static slice CANNOT answer (D2's inheritance, named)

1. Time-live modulation of the view — the clock→screen mixing channel entering λ_t
   (un-tabled for this question; MAP §3). Whether a LIVE T generates any pattern at all.
2. mu beyond the static stratum — its static kinematic inertness is scope, not a prior.
3. The cross-tracer PHASE question (vacuous here, §4) — meaningful only if D2 generates
   a pattern; operator-blindness (K14-style audit) must be re-derived there.
4. Source back-reaction / self-lensing (P-L7) — clustered matter perturbing the metric.
5. Off-center observers (the r = 0 normalization is THEORY here, but anisotropic viewing
   from off-center is a genuinely un-probed static direction — named, not owed by contract).
6. Oscillating-profile geometries (O-E) — outside the declared class-(i) family (D4's own
   class declaration; F-SHOP-CLASS analog).
7. Anything about WHERE source statistics come from — T maps statistics, it does not
   generate them (O-B/D3 territory).

## 10. LANDED OUTCOME (prereg §4)

**D1-T (STATIC / mu = 0 stratum / lock chart) — the static transfer map is DERIVED, and it
is a pure smooth rescaling: featureless in ⇒ featureless out, proven and machine-checked on
both the angular leg (exact, all separations) and the radial leg (locally exact + the
no-extremum theorem at finite separations).** [R2-A1 wording: scope inside the bold span.]
Static-scoped, first-class: the static comparison map does NOT manufacture angular or
radial features from plain matter. Deliverables T1–T5 all land (T2 as the rescaling's depth
law, per contract). Check count, honest split (R1-V1): **44 / 44 keys True machine-run**
(`run_output.txt`), of which FOUR (K1, K2, K5, K7) are TRUE-BY-FORM/illustrative —
substantive machine coverage is 40 keys; the four underlying claims are independently
verified by R1's blind recompute (41/41 of R1's own keys, own Ricci code, both ray
orientations, K22 by a stronger route).

STATUS: see CONSOLIDATED below (both reviews in; verified LEAD).

## LAB-LOG (process disclosure for the reviews; Category-A conditioning only)

- Reproduce: `timeout 480 python3 -u derive_d1.py` (CPU; ~3–5 min, the generic-A(r) Ricci
  block dominates; single process per the anti-hang rule).
- First run attempt hung in `sympy.limit` (gruntz) on expressions with SYMBOLIC exponents
  (G5-type limits with free n). Amendment (technique, not physics): three limit claims were
  restated in machine-decidable equivalent form — G5 via r²·ṙ² → −L² at r=0 (expand+subs);
  K9 via the q = (1+z)^(−2/n) substitution with the exponent-sign step its own key; K20b via
  0^(m/2) = 0 under m > 0. K10b/K15c positivity was routed through the K10lemma calculus
  proof (monotone-from-1) because sympy's assumption engine cannot decide (1+z)^(2/n) > 1
  directly. K22's series was assembled from the exact Taylor coefficients of dℓ_p/dz
  (fundamental theorem) instead of `series` on the unevaluated ratio (speed only).
  Every restatement PROVES the same mathematical claim; none weakens a check. The failed
  first attempt's five False keys were all decidability/form issues of this kind, repaired
  as above — no claim was changed to make a check pass.

## CONSOLIDATED (2026-08-08; post-review; supersedes §10's pre-review status)

**Reviews (both in, same session):**
- `ADVERSARIAL_REVIEW_1_recompute.md` — R1, blind full recompute + completeness attack:
  **SUSTAINED-AMENDED** (41/41 own keys; own Christoffel/Ricci code; both ray orientations;
  K22 by direct series on the exact ℓ_p(z)). No kill found.
- `ADVERSARIAL_REVIEW_2_scope.md` — R2, falsifier/scope/ledger adjudication: **AMENDED**;
  NO falsifier fires (F-RETRO, F-FREEZE, F-ONEHORSE, F-SCOPE all adjudicated DOES-NOT-FIRE);
  debt service graded DELIVERED 5/5.

**Amendments applied in place (all of them):** R1-V2/R2 = the §2 finite-bin correction +
§4(i) + §5 echo (the window-break statement, R1's exact characterization); R1-V1 = K1/K2/
K5/K7 relabeled TRUE-BY-FORM where cited + the §10 machine-vs-claim coverage split;
R1-V3 = P-L2 n > 0 domain restriction; R1-V4 = the 3-D chord realization fork named at §6
(pointer at §1); R2-A1 = scope inside the §10 bold span + the §2 "(static map)" headline;
R2-A2 = P-L8 extended (single γ across depth) + the §2 γ-drift sentence; R2-A3 = the
"ANY scale" verdict wording.

**HEADLINE RESULT (with the V2 refinement as its sharpest honest form):**
THE MAP: the static transfer map is a pure smooth rescaling — featureless in ⇒ featureless
out, PROVEN (angular leg exact at all separations; radial leg locally exact + the
no-extremum theorem; zero shear; zero radial-null Ricci focusing — the generic-A(r)
lock-chart theorem R_tt + A²R_rr ≡ 0). THE MAP + WINDOW: any finite observation window
adds a smooth projection BREAK at θ_break ≈ Δℓ_p(bin)/r(z) — window-set (present
identically in flat space, free symbols {r̄θ, W} only), with the metric controlling only
its smooth depth-drift through the dictionaries r(z) and J(z). That distinction — the map
adds no scale; the window adds one whose drift the metric steers — is the honest bridge to
any future data contact. NO DATA TOUCHED here; no comparison to any observed pattern made
or implied (F-RETRO).

**SCOPE (unquotable without it):** STATIC / mu = 0 stratum / lock + areal-anchor chart /
central observer / n > 0 / test sources. A static featureless verdict is NOT a verdict on
O-C (CP2): D2 owns time-live.

**Four-check line:** pre-registered (frozen contract, this directory) — YES; full-space or
bounded-slice-justified — bounded slice, DECLARED (CP2a) with every OFF sector ledgered;
blind-verified on the load-bearing premise — YES (R1 full recompute; R2 independent
spot-derivations); forced premises audited — YES (ledger P-L1–P-L12 + reviews' V3/A2
additions). Ceiling honored: **verified LEAD** (same-session reviews; the external
replication bar travels with the result).

**D2 inheritance (restated from §9):** (1) time-live modulation of the view — the
clock→screen mixing channel entering λ_t; whether a LIVE T generates any pattern at all;
(2) mu beyond the static stratum (inertness = scope, not prior); (3) the cross-tracer
PHASE question (vacuous at the static layer; re-derive operator-blindness time-live);
(4) source back-reaction/self-lensing; (5) off-center observers (un-probed static
direction, named); (6) oscillating-profile geometries (O-E/D4, own class declaration);
(7) the origin of source statistics (O-B/D3). Plus, from the reviews: the window-break's
map-vs-window decomposition should be RE-CHECKED under a time-live T (does the live map
move the break beyond the smooth dictionary drift?).

— consolidation by the D1 derivation agent, 2026-08-08. NOT committed (owner's gate).
