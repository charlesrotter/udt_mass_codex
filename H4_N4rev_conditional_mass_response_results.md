# H4 · N4-revised — conditional mass-response solve: OUTCOME D (box-control, DERIVED cause); interior active-P; positive-mass SIGN lean; NON-PERTURBATIVE

**Status: BANKED, blind-verified (2026-07-05). Outcome D (tool-limited = the pre-registered BOX-CONTROL sub-outcome)
— HONEST, with a DERIVED structural cause, not a budget dodge.** The Charles-authorized revised N4 (corrected
N4a-screened operator + G/P-switch interior check, run as a φ_amb siting-depth sweep, frame C(a)). Solver agent
ab253bf77f0e47b76; blind adversarial verifier af9da9e9dc08b8016 (all 7 targets PASS as scoped; caught 2 mandatory
caveats + a labeling slip). DATA-BLIND; Z_φ ∈ {1,8} explicit; no ξ-anchor claim. Scripts:
`h4_scripts/op_derive2.py`, `ell2_derive.py`, `extract_stress_rtheta.py`, `n4rev_pipeline_GREENBUG.py` (BUGGY —
see caveat 1), `n4rev_diagnose.py`.

## What the solve found (verified)
- **S1 — operators (PASS).** Monopole: **Z_φ(r²δφ')' + 8e^{−2φ_amb}δφ = Σ** (the +8e^{−2φ_amb} = ∂/∂φ of the
  Branch-P source 4e^{−2φ}, ADDITIVE screening, re-confirms N4a). Transverse/shear: **e^{−2φ_amb}·L_bare**,
  L_bare[f]=r²f''−2rf'+2f, roots **{1,2}** — e^{−2φ_amb} a frozen MULTIPLICATIVE prefactor, NOT additive
  screening (additive shear screening arises only from φ_amb'(r)≠0 = the N2-owed running correction).
- **★ S2 — box-control is INTRINSIC + STRUCTURAL (PASS, load-bearing).** L_bare's roots {1,2} both grow ⇒ the
  transverse operator has **NO decaying homogeneous mode**. A compact hopfion stress therefore sources a shear
  that is **CELL-FILLING, not a localized halo** (fractional δh/h∝1/r decays, but absolute shear grows; the
  induced O(amp²) monopole source carries a 1/r² tail, r²Σ̂→const). A localizing shear would require a Dirichlet
  wall at finite r = the retired PRIVATE SEAL (frame C(b), FORBIDDEN). ⇒ **the hopfion's mass is inherently a
  WHOLE-CELL property, not a cleanly-separable localized quantity** — consistent with the finite-cell canon and
  N4a's "the real fork is INTERIOR." This is the derived cause of the pre-registered box-control D.
- **S3 — no read-surface-independent δq at any finite frozen depth (PASS).** The screened far-field exponent
  s₊=−½+√(Z_φ−32e^{−2φ₀})/(2√Z_φ) > −1 in the real-root regime ⇒ −r·δφ∼r^{1+s₊} GROWS (no clean 1/r plateau; δq
  drifts with read radius, no plateau). The sub-critical sign-flips are the frozen-W **DSI oscillation artifact**
  (already killed by the taxonomy MAP), NOT physical zero-crossings. A clean δq recovers only as W₀→0 = the
  RUNNING ambient. ⇒ the frozen-const sweep cannot yield a clean δq(φ_amb) CURVE.
- **S4 — interior ACTIVE-P, no reachable DEAD-G (PASS).** The interior source Σ(r)≠0 (real localized stress) ⇒
  max|δφ'|_interior ≠ 0 in EVERY case ⇒ any apparent far-field δq=0 is a **FLUX-NEUTRAL ACTIVE-P** point, never
  dead-G. **The isolated hopfion (frame C(a)) is always interior-active-P; a genuine dead-G is NOT reachable.**
  Discharges the G/P-switch MAP's δq=0-branch interior-φ' check.
- **★ S5 — positive-mass SIGN lean (PASS-WITH-CAVEAT).** ∫Σ̂ dr > 0 (near-core positive lump dominant; the
  negative 1/r² tail is convergent + sub-dominant, does not flip the sign) ⇒ near-core δq<0 ⇒ **δm = −δq > 0**.
  The SIGN is coupling-independent (sign of the bilinear source over the core) and read-surface-robust in the
  clean regime; it corroborates N4's "CF1 leans positive" + N2's positive-energy plausibility. **NEGATIVE MASS
  (the pre-registered prime risk) is DISFAVORED.** CAVEAT: because ε≫1 (S6) the sign is only the LEADING-ORDER
  term's sign — a genuine **LEAN, not a certified physical mass sign**.
- **★ S6 — NON-PERTURBATIVE (PASS).** ε ≈ 10–15/W₀ ≫ 1 for ALL physical siting depths (peak transverse stress
  O(45), not small). ⇒ the entire O(amp²) linear reduction (N4 Phase A ½⟨T,L⁻¹T⟩, N2) is **out of validity for
  the real hopfion MAGNITUDE**; the mass magnitude needs a NON-PERTURBATIVE fully-coupled solve. (The sign, a
  leading-order property, survives as a lean.)

## Conditional-region partition (the requested deliverable — it COLLAPSES honestly)
No clean read-surface-independent δq(φ_amb) curve exists under the frozen ambient (S2+S3), so the region partition
collapses: the whole φ₀ axis is **D** (box-control / frozen-W artifact) for the MAGNITUDE; the only robust
statements are **positive-mass SIGN + interior ACTIVE-P everywhere**, and **NO dead-G / no negative-mass region is
reachable** by the isolated hopfion. (The apparent shallow-band sign-flips are the dead DSI artifact, not physics.)

## Caveats recorded (verifier-mandated)
1. **Green's-function BUG (category-A numerics, NOT a physics smuggle):** `n4rev_pipeline_GREENBUG.py`'s
   `green_response` does NOT invert L_bare (L_bare[green]=r⁴(5T+2rT')≠−r⁴T; interior residual 15.5). It inflates
   the MAGNITUDE ~8× (∫Ŝ=103 vs correct ~13). **The SIGN survives** a correct L_bare BVP (residual 0.03; ∫Ŝ>0,
   +13…+25, near-core lump dominant in every outer-BC choice). Magnitude figures from the scratchpad are
   UNRELIABLE (already non-banked under D); any future magnitude solve MUST use a correct L_bare inverse.
2. **Sign under non-perturbativity:** the +mass sign is leading-order; state it as a LEAN, never a certified sign.
3. **Labeling fix (non-load-bearing):** N4a / the taxonomy MAP wrote "deep ⇒ screened/oscillatory" — BACKWARDS.
   Complex (oscillatory) roots occur for W₀>Z_φ/32 ⇔ e^{−2φ_amb}>Z_φ/32 ⇔ **φ_amb < ½ln(32/Z_φ) = SHALLOW**. So
   **SHALLOW (small φ_amb, strong screening) = oscillatory; DEEP (large φ_amb) = clean.** The running ambient
   DEEPENS outward (φ_amb≈½ln((8/Z_φ)ln r) grows) ⇒ clean recovered at large r — physics unchanged, only the
   shallow/deep labels in N4a + taxonomy are corrected.

## Bottom line + the next tool
Revised N4 = **D (box-control), with the DERIVED cause: the native transverse operator L_bare (roots 1,2) admits
NO decaying shear mode ⇒ the hopfion's geometric response is cell-filling ⇒ its mass is a whole-cell property, not
a separable localized halo.** Robust physics: **interior ACTIVE-P everywhere (no reachable dead-G); a
coupling-independent POSITIVE-mass sign lean (negative-mass disfavored); the backreaction is NON-PERTURBATIVE
(ε≫1).** This reinforces — does not overturn — N4a / the taxonomy MAP / the G/P-switch MAP.
**NEXT TOOL (precise):** a NON-PERTURBATIVE, fully-coupled (φ + transverse h_AB) solve on the resolved hopfion
source with the TRUE running ambient φ_amb(r)≈½ln((8/Z_φ)ln r) — NOT a flat box, NOT a Dirichlet wall, NOT another
perturbative L⁻¹ contraction — reading δq on a bulk read-surface in the running background (a correct L_bare
inverse for any residual linear step). **Implication for N5:** the original "anchor φ_amb from the response curve"
is UNDERCUT (no clean perturbative curve exists); N5 must either drive the non-perturbative solve or reframe the
anchor around the whole-cell criticality (E_ang(core)=2), since the mass is a whole-cell property.
