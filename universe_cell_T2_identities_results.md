# Universe cell T2: profile-independent identities — DERIVED (claude.ai) + BLIND-VERIFIED

**Date:** 2026-07-02. **Arc:** flux-sealed universe cell; T2 was PRE-REGISTERED as the knob-free
teeth in `flux_sealed_universe_cell_miniMAP.md` §3. **Derivation:** claude.ai session (Charles's
lane), delivered 2026-07-02. **Blind verifier:** agent `ae5fd5860913a24f9` — QUESTIONS-ONLY
protocol (claimed identities held OUT of the repo in scratchpad during the run); independent
re-derivation + CAS + two bounded numeric shooting runs (residuals ≤ 1.4e-11). Scripts:
`verify_universe_bv3_q1_q4_cas.py`, `verify_universe_bv3_q5_numeric.py`,
`verify_universe_bv3_q4a_nonmonotone.py`. **Verdict: ALL CONFIRMED** (T2-A/B exactly; T2-C/D
with premise tags and sharpenings below). Regime: round-static Branch-P reduction, banked fold
pins, φ-blind autonomous ρ'-free L_m. Units c=G=1, canon per-4π normalization.

**RULING RECORDED (Charles, 2026-07-02, via the T2 doc):** the free-endpoint / BREATHING-EDGES
posture is RULED (adopted). H_tot ≡ 0 on the universe cell; the E_m(core)=2 critical closure is
no longer conditional on a driver CHOSE but on Charles's ruling. (The anchor is operated as a Δφ
statement throughout — the canon-gauge flag is treated as resolved-toward-Δφ; explicit canon
wording remains Charles's to amend.)

## T2-A — The flux law IS the untrapped condition (CONFIRMED exactly)

1 − 2m/ρ = e^{−2φ}ρ'² (Misner–Sharp, general-ρ form — the unique g_rr=e^{2φ} generalization of
the banked areal form, consistent with m'_MS = 4πρ²ρ'ε). Hence:

    Φ'(r) = 4(1 − 2m/ρ);   q = 4∫_{r_c}^{r_s} (1 − 2m/ρ) dr.

- **2m ≤ ρ EVERYWHERE is automatic** (the right side is a square): no trapped region exists in
  this static class; 2m = ρ exactly at ρ-turning spheres.
- **m(r_c) = ρ_c/2 exactly** — the inner core is born MARGINAL, matter-independently. With the
  D1 seal pin ρ'_s=0: m(r_s) = ρ_s/2 too.
- Verifier subtlety: at a GENERAL edge (ρ'_s free), m_s = (ρ_s/2)(1 − ρ'_s²) goes NEGATIVE for
  |ρ'_s| > 1 (realized in a toy run) — only the D1 pin guarantees m_s > 0.
- The public charge = 4 × the integrated untrappedness deficit. Numeric: rel. err 2.2e-8.

## T2-B — General-edge budget (CONFIRMED exactly)

    H_m(core) − H_m(seal) = q²/(2Zρ_s²) − 2ρ'_s²      (φ_s=0, ρ'_s general)

Reduces to the banked budget at ρ'_s=0. Sign note (verifier): a moving seal edge REDUCES the
matter-energy drop needed for a given q. Needs L_m autonomous + ρ'-free (banked). Numeric
residual 1e-11 at ρ'_s = 9.3.

## T2-C — H ≡ 0 (breathing edges, RULED): critical matter + charge bound

- **H_m(core) = 2 exactly** — Z-, φ_c-, ρ_c-, σ-independent (re-confirmed; does not need ρ'_s=0).
- H_m(seal) = 2 + 2ρ'_s² − q²/(2Zρ_s²). Premise-free corollary: H_m(seal) ≤ 2 + 2ρ'_s².
- **q ≤ 2ρ_s√(Z(1+ρ'_s²)) is CONDITIONED on H_m(seal) ≥ 0 — a FRESH PREMISE for general φ-blind
  matter** (D3: no universal sign). DERIVED-conditional only for the banked winding form at an
  f-mirror seal with ξ,κ > 0. Tag travels with every use of the upper bound. Saturation:
  q* = 2√Z·ρ_s at ρ'_s=0.

## T2-D — Anchor relation and the q-window (CONFIRMED, sharpened)

    Δφ = ∫ Φ/(Zρ²) dr;   SHARP lower bound  q ≥ Z·Δφ / ∫dr/ρ²   (premise-free given the pins)

- ρ_min form q ≥ ZΔφρ_min²/(r_s−r_c) is valid ONLY with ρ_min = min over the WHOLE interval:
  the verifier CONSTRUCTED an admissible non-monotone-ρ solution (interior dip below both
  endpoint values; all identities intact) — min(ρ_c, ρ_s) would be WRONG. Nothing banked forces
  monotone ρ once matter is on.
- Φ ≤ q needs NO inner pin (monotonicity alone); Φ(r_c)=0 (hence q ≥ 0, Δφ ≥ 0) needs the inner
  pin. Failure modes named: non-φ-blind matter breaks the monotonicity itself; a φ'_c≠0 core
  class shifts the integral; ρ→0 inside trivializes the bound.
- **The two-sided window** Z·Δφ/∫dr/ρ² ≤ q ≤ 2ρ_s√(Z(1+ρ'_s²)) (upper side premise-tagged):
  logically independent constraints; non-emptiness ⟺ **√Z·Δφ ≤ 2ρ_s√(1+ρ'_s²)·∫dr/ρ²**.
- **Verifier findings beyond the claims:** (i) the window condition is SCALE-INVARIANT
  (ρ_s·∫dr/ρ² is homothety-degree 0) — it constrains cell SHAPE, not size (consistent with the
  homothety: the anchor alone pins no absolute scale); (ii) **large Z closes the window** (lower
  bound ∝ Z, upper ∝ √Z): √Z ≤ 2ρ_s√(1+ρ'_s²)·(∫dr/ρ²)/Δφ is a genuine shape ceiling on Z —
  connects the D2 Z∈{1,8} fork and the standing Z=8/Route-B tension to an observable-anchored
  test.
- Scale bookkeeping: both bounds homothety-covariant (verified numerically to 8 digits).

## Use in T3 (per the pre-registration)

Per-solution acceptance identities: T2-A (MS/flux), T2-B (budget), T2-C (H_m(core)=2 under the
ruling). Frame test: the q-window — a T3 solution landing outside it = solver error; the window
EMPTY for canon shapes = the frame fails carrying the anchor (tripwire → ω≠0). The only
matter-audit with test power remains the D3 σ cross-check; TOV/ε+2p_t stay zero-power.

## Premise ledger

| item | status |
|---|---|
| MS-flux link; m=ρ/2 at turning spheres; 2m≤ρ automatic | DERIVED (CAS) |
| general-edge budget | DERIVED (L_m autonomous+ρ'-free, banked) |
| H_m(core)=2 | DERIVED under H≡0; posture now CHARLES-RULED (breathing edges) |
| H_m(seal) ≥ 0 → q upper bound | FRESH PREMISE (general matter); derived-conditional for banked winding+f-mirror+ξ,κ>0 |
| q lower bound (sharp ∫dr/ρ² form) | DERIVED (φ-blind + inner pin); whole-interval ρ_min if weakened |
| window scale-invariance; large-Z closure | DERIVED (verifier addition) |
| anchor-as-Δφ reading | Charles-operated; canon wording amendment pending |
