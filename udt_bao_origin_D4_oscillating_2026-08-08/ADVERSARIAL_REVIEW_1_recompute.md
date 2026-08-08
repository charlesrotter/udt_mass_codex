# ADVERSARIAL REVIEW 1 — D4 full independent recompute + completeness attack

Date 2026-08-08 | branch grok | reviewer: R1 (Fable, fresh context) | HOSTILE brief.
Protocol: PREREGISTRATION.md + DERIVATION_NOTES.md + run_output.txt read FIRST; my own
recompute (`review1_recompute.py` → `review1_output.txt`, **39/39 True**) built and run
BEFORE opening `derive_d4.py`; then line-by-line source diff + vacuous-key hunt.
No data, ZERO BOSS contact, bounded synchronous CPU runs only. NOT committed.

## 1. Independent recompute (own Ricci code, Schwarzschild-anchored) — all reproduced

- **Generic-A backbone:** R_tt + A²R_rr ≡ 0 and radial-null R_kk = 0 for arbitrary A(r)
  [S1, S2]; lock form, radial-null geodesic with r affine, b-only orbit equation
  [S3, S4, S5]. d_A = r is a chart fact riding zero focusing + the D1 vertex argument
  (cited-not-recomputed here; inherited ground, previously reviewed). CONFIRMED.
- **P1:** anchor pin A(0)−1 = ε·cos φ₀ with X_m(0) = 0 verified at GENERAL m (the package
  machine-checks only the areal representative; claim correct) [P1_anchor_pin]; ε < 1
  bound with the fewer-than-one-cycle caveat as disclosed; ripple bound −½ln(1−ε), depth
  still divergent; X_m closed form by differentiation, nm = 1 log form, edge-X-is-depth
  (proper n=2, optical n=1 = O2's knife edges, confirmed against the O2 package)
  [P1_Xm_*]; the exact B6a criterion reproduced symbol-for-symbol; the trichotomy limits
  (u^q → 0 / const / u^(−g) → ∞) + phase divergence at and above the edge (infinitely many
  sign sweeps ⇒ supercritical breaks monotonicity for EVERY ε > 0) [P1_B7_*]; the areal
  sufficient bound n·λ·(1−ε) ≥ 2πR_wε re-derived from worst-case |sin| ≤ 1, u ≤ 1
  (sufficient-only, as stated); the O2 comparison squeeze [P1_B9]. ALL CONFIRMED.
- **Caustics admitted-not-forbidden:** checked against the banked set — D1's monotonicity
  is premise P-L2 (declared-slice, D1 ledger line confirmed by inspection), NOT a banked
  verdict; A > 0, wall, and measure verdicts hold in the supercritical cells. SUSTAINED.
- **P2:** dictionary inversion ρ₁ = (R_w u/n)·osc and the residual law
  Δμ = (5/ln10)(ε/n)[u/(1−u)]·osc [P2_C1, C2]; equal spacing in ξ_m = (1+z)^(−2(1−nm)/n),
  ln(1+z) exactly at nm = 1, z-affine cell m = 1/2 + 1/n ⇒ only (optical, n=2) among the
  natural m (m=0 root n=−2 outside n>0) [P2_C3*]; envelope strictly falling, wall rate
  (1+z)^(−2/n) verified as a genuine LIMIT (package key C4b checks only the algebraic
  identity; the limit holds), low-z pin cancellation verified at GENERAL m (package
  checks the linearized areal form; the full general-m limit gives the same
  2πR_w/λ constant) [P2_C4*]; anti-phase lock (identity); the oscillating-Jacobian
  eps-leg + transport leg (total (ε/n)(osc − R_w u osc′)) and the loudness ratio r·Φ′
  with the π/2 phase advance [P2_C7*]; cycle spacing and λ_p = λ(1+z)^(1−2m) [P2_C8*];
  the projection scaling identity and the γ=2 exponentially-localized witness
  (∫cos/(l²+r̄θ²) = (π/r̄θ)e^(−2π·r̄θ/λ_p)) [P2_C9*]; symbol audit clean. ALL CONFIRMED.
- Reviewer honesty note: 4 of my first-pass keys failed as MY OWN decidability/form bugs
  (solve-form comparison; (R_w−r) sign undecidable outside a positive variable; an
  unevaluated-integral comparison). All four resolved FOR the package. This independently
  corroborates the LAB-LOG's account of the three B1 restatements as genuine sympy
  decidability walls, not claim-weakening: I hit the identical wall on C7.

## 2. Source diff + vacuous-key hunt (after recompute)

No vacuous keys that carry load. Honest labeling confirmed: C5/C6 and the C7b+C7b2
composition are BY-FORM and declared so both inline and in §7; B1c/B1d are thin log
identities but their content (edge X ∝ depth) is real and re-verified; B6b verifies the
bound's algebra (the domination argument is elementary and I re-derived it); C11's float
scan covers the AUDITED list only, as its text states (source inspection: no float
enters any physics expression). No key asserts more than its check + labeled composition.

## 3. Completeness attack — findings (none fatal)

- **A1 (the sharpest): the θ_osc "metric-set" claim needs one ledger line.** The
  distinction vs D1's window-set break IS real — the localized kernel's scale symbol λ_p
  is the metric's own, its drift law (1+z)^(1−2m) is metric-set, and D1's break carried
  only window symbols {r̄θ, W} — but the feature's VISIBILITY is window-conditional: the
  oscillatory window component requires the projection bin to span ≳ one λ_p cycle (and
  the C9b witness integrates an effectively infinite line of sight). Amplitude
  window-conditional; LOCATION and drift metric-set. Not an artifact of the binning
  channel (a binning artifact could not carry λ), but the visibility premise is
  currently unledgered. AMENDMENT: add the window-width condition to §3b + ledger.
- A2: admitted behaviors not characterized and not named in §6: (i) multiple
  incommensurate λ's — actually covered at O(ε) by linearity of every P2 law
  (superposition), worth one sentence; (ii) amplitude-modulated ε(r) envelopes —
  genuinely outside P-D3 and outside §6.3's named exclusions. AMENDMENT: name both.
- A3 (cosmetic): C3a's "residual periodic in ξ_m" — strictly the oscillatory factor is
  periodic; the residual is envelope × periodic. "Equal cycle spacing in ξ_m" (as in the
  run-output text) is the exact statement.
- A4: angular-sector oscillation is NOT a gap: in the lock + areal-anchor chart the full
  spherically-symmetric freedom IS A(r) (g_θθ = r² by the anchor); only angular-DEPENDENT
  oscillation escapes, and §6.3 names it. Attack fails.
- A5: overreach hunt at O(ε): none found — P-D11 scopes per-law; B6a/trichotomy/fold
  statements are exact-level; C4c's calibration-degeneracy honestly stated; the phase pin
  is correctly "forced GIVEN c₀ = 1, else absorbed by c₀-renormalization" (one parameter
  combination lost either way — counting verified).

## 4. VERDICT: **SUSTAINED-AMENDED**

Every boxed claim reproduced independently (39/39); no kill found; the trichotomy ↔ O2
correspondence, the anchor pin, the ε < 1 bound, the supercritical break-for-every-ε,
the residual/periodicity/envelope laws, the anti-phase lock, the loudness hierarchy, and
the λ_p drift law all stand. Amendments required before banking (clarificatory, no
result changes): (1) ledger the window-width visibility condition on θ_osc (§3.A1);
(2) name incommensurate-λ superposition + ε(r)-envelope forms in §6 (§3.A2); (3) the
C3a periodic-factor phrasing (§3.A3). D4-ADMIT+IMPRINT stands as a LEAD pending R2.
