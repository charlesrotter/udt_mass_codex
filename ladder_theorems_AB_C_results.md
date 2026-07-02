# Ladder theorems A/B + oscillation structure C — DERIVED (claude.ai) + BLIND-VERIFIED, with one refutation-and-correction

**Date:** 2026-07-02. **Derivation:** claude.ai session (Charles's lane) — Theorems A/B exact,
Structure C a controlled O(ε) linearization (all truncations flagged at source; legal as
hypothesis development per the Taylor ruling), Lemma D explicitly NOT derived (named, route
sketched). **Blind adversarial verifier:** agent `a20e50756e94e9c98` (own CAS re-derivation with
signs + 4 IVP shots; claude.ai doc held out of repo; scripts `cascade_bv8_cas_ABC.py`,
`cascade_bv8_falsifiers.py`, tables `cascade_bv8_falsifiers_out.txt`). **Scope:** round-static
Branch-P reduction, potential-only φ-blind slices, banked cell pins; C-results are
DERIVED-AT-O(ε) only, never more.

## Theorem A (EXACT — verified): q = Z·Δφ·B⁻¹, B ≡ ∫₀^{r_s} Φ̂/ρ² dr

Pure algebra from φ' = Φ/(Zρ²); needs only q>0 (forced) and the anchor. **The q∝Z corollary is
EMERGENT, not automatic:** B depends on the sealed profile; banked data gives B(Z=8)/B(Z=1) =
1.718 at N=1 (a +72% violation of ∝Z) falling to 1.013 by N=11 — **q ∝ Z with slope
ln(1101)/B is an emergent large-N shape universality, and the deviation of q₁/q₈ from 0.125
at equal N MEASURES the shape integral's residual Z-dependence.** [Verifier-quantified.]

## Theorem B (EXACT identity — verified): U(ρ_s) = 2 − q²/(2Zρ_s²)

At any closed seal, exactly. **Asymptotic criticality (U(seal)→2=U(core)) confirmed-with-
conditions:** requires q_N/ρ_s,N → 0, not merely q decreasing (verifier sharpening); banked q_N
is non-monotone at N=1→2 in every Z=8 family and the approach is parity-interlaced — but the
trend is unambiguous: 2−U(ρ_s) falls 1.948 (N=0) → 0.0084 (N=22). **This is the derived
MECHANISM of the Stage-C ρ_s-universality: the matter's seal freedom is squeezed out at the
exact rate q_N²/(2Zρ_s²).** Falsifier F1: the identity holds rung-by-rung on all 35 banked
rungs tested (worst residual 1.7e-9, fully explained by seal-root tolerance + H-drift).

## Structure C (DERIVED-AT-O(ε); verifier-corrected) — the oscillation, the amplifier, parity

O(ε) equation (verifier's independent CAS, signs definitive): with ρ = 1+εu,
U'(1+x) = 4δ̃+4s̃₁x: **u'' − 2φ'u' + k²u = source**, k² = e^{2φ}[(Z/4)φ'² − s̃₁]; the
(Z/4)e^{2φ}φ'² term enters k² with + sign and the source with − sign; oscillatory ⟺
s̃₁ < (Z/4)φ'². Consistency window: δ̃, φ'² = O(ε) — degrades within ~one wavelength of the
seal (measured; flagged). u = e^{φ}w kills the u'-term IDENTICALLY; exact w-equation carries
k² + φ'' − φ'² (the shift is small and named).

**THE AMPLIFIER — REFUTED AS CLAIMED, CORRECTED, AND EMPIRICALLY SETTLED:** the claimed
core→seal amplitude amplification e^{Δφ} = 1101 is WRONG — the same e^{2φ} that drives
oscillation makes k ∝ e^{φ}, so the WKB envelope carries K^{−1/2} and the u-envelope is
**e^{φ/2}: amplification e^{Δφ/2} = √1101 ≈ 33.2.** Falsifier F2 (re-shot N=5 and N=15
trajectories, 17 same-parity extrema pairs, no fits): per-pair geometric mean 1.374 vs
e^{Δφ/2}-prediction 1.381 (few-% agreement, residual alternation decaying as predicted by the
offset bias) vs e^{Δφ}-prediction 1.908 (cumulative failure ×0.06). **The CMB anchor is the
ladder's amplifier as its SQUARE ROOT.** (Note for the claude.ai relay: its own Lemma-D route
formula A ∝ e^{φ}/√k already implied e^{φ/2} — the D-route was more correct than the C4
headline.) WKB validity measured: |φ'|/k ≤ 0.55 at onset, ≤ 0.05 late.

**PARITY — DERIVED at O(ε) with conditions measured to hold:** given k²>0, offset-domination
(measured |amplitude|/|offset| ≥ 4 at every extremum), and |φ'| < k, Sturm alternation transfers
through the positive e^{φ} factor and **sign(ρ_s−1) = sign(δ̃)·(−1)^N exactly** (u'(r_s)=0 is
exact, not approximate) — the Stage-B/C parity grain, derived. The twin ladder = the δ̃ → −δ̃
branch with inverted parity, a LEADING-ORDER symmetry only (the −(Z/4)e^{2φ}φ'² source part
does not flip; no exact nonlinear twin symmetry claimed). Parity checked: zero violations on
all 70 banked rungs + inverted on the 3 above-stuck scratch rungs.

**New structural fact (verifier):** the trajectory is a long one-signed ramp (no zeros for
r ≲ 0.8·r_s) with ALL N oscillations piled up near the seal — wavelength ∝ e^{−φ}. Flux at
O(ε²): Φ' = 4ε²e^{−2φ}u'² — charge accumulation quadratic in amplitude (why q_N falls),
cycle-averaged quasi-linear climb per node.

## Falsifier summary
F1 (B-identity, 35 rungs): PASS, ≤1.7e-9. F2 (envelope law): e^{Δφ} FAIL / e^{Δφ/2} PASS.
F3 (Theorem-A bracket on re-shot trajectories): PASS at 4e-10 (honestly flagged near-tautological
— tests quadrature + banked-q reproducibility, both clean).

## Lemma D — STILL OPEN (the one missing piece for full ρ_s(N) universality)
The universal sealing amplitude A_seal ≈ 0.092 across families and Z. Route (named, unproven):
double closure (φ(r_s)=0 ∧ ρ'(r_s)=0) on the two-scale averaged system with the CORRECTED
envelope A ∝ e^{φ/2} (equivalently e^{φ}/√k); family data may cancel between k and the node
condition. Dispatch owed. Until it lands: ρ_s(N)-universality = OBSERVED (blind-verified) with
mechanism DERIVED-IN-PART (A/B exact + C at O(ε)).

## Ledger
| item | tag |
|---|---|
| Theorem A; Theorem B identity | DERIVED exact (CAS ×2, blind) |
| q∝Z | EMERGENT (measured B-ratio 1.718→1.013); NOT an identity |
| asymptotic criticality | DERIVED-conditional (q_N/ρ_s→0; trend confirmed, interlaced) |
| C oscillation eq / e^{φ}-elimination / parity / twin | DERIVED-AT-O(ε), conditions named + measured |
| e^{Δφ}=1101 amplifier | **REFUTED**; corrected to e^{Δφ/2}=√1101 (F2-settled) |
| Lemma D / A_seal≈0.092 | OPEN (dispatch owed) |
| linearization status | hypothesis-development instrument (Taylor ruling); NEVER a stated nonlinear result |
