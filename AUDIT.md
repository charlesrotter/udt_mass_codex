> **CONDITIONS-CHANGED (2026-07-06 macro-spine pass) — NOT a live frontier; header verdict is STALE.**
> This S116 CMB/EE dispatch was DROPPED by Charles. Its top "Current verdict" token (centrifugal-cutoff → EE peak
> ~1004) is SUPERSEDED WITHIN THIS DOC: the ★★★ TT firewall REFUTES the cutoff fix; the surviving live claim is the
> derived intrinsic-density ¼δρ/ρ term (MECHANISM DERIVED, Planck fit PENDING). CLEAN on the operator (rides the
> current native exponential-lapse metric + native radial function; no flat-j_ℓ / X=−2e5 in any surviving claim),
> but "Canonical inputs = CG §12.15.x" are from LEGACY udt_canonical_geometry (the load-bearing weld was re-derived
> natively). Read the final-state sections, not the header token.

# D-CMB-EE-PROJECTION-SPIN-1 — is the pure-metric E-mode power ℓ⁴ or gentler? (S116)

**Verdict (SUPERSEDED within this dispatch — see ★★ REOPENING below):** ~~`EE_AMPLITUDE_FRONTIER_RESOLVED__OVERSHOOT_STANDS_AS_FALSIFIABLE`~~
**Current verdict:** `EE_OVERSHOOT_REOPENED__NATIVE_RADIAL_FUNCTION_HAS_CENTRIFUGAL_CUTOFF_AT_l_max=1+z__EE_PEAK_LANDS_~1000≈PLANCK_1004__CONSISTENT_CONDITIONAL_ON_omega_drive=c/r_CMB__NOT_YET_FORCED`

> **Scope + arc:** the dispatch first resolved roadmap §S115.8 (i)/(ii)/(iii) NEGATIVE (no gentler angular power, no carrier damping, no diffusive Silk-analog) and concluded the overshoot was the prediction. Charles then directed a deeper ontology ponder, which surfaced that the projection used the **flat-space j_ℓ** (Gate-10 LCDM-isotropy reduction, not native). Redoing with the **native UDT radial function** revealed a centrifugal cutoff at ℓ_max = 1+z that the flat-Bessel/Limber projection had omitted — bringing the EE peak to ~1000 ≈ Planck 1004 and **reopening** the closed verdict. The (i)/(ii)/(iii) findings still stand for what they addressed (angular power ℓ⁴ forced; no *dissipative* damping); the cutoff is a *propagation* (non-dissipative) effect that those analyses — and my "already in the projection" dismissal in the Silk check — missed. See ★★ REOPENING.

**Charge (roadmap §S115.8 (i) / SESSION_116 §2 priority (i)):** the S115 EE-amplitude firewall FAILED — derived ð²→ℓ⁴ over-predicts the Planck EE peak ~2× (ℓ≈1900 vs 1004). Priority (i) asked: is the ℓ⁴ a *standard photon-transport* import that the **pure-metric** reframe (`project_pure_metric_polarization`: polarization = projected metric anisotropy in the observer tetrad, not a transported photon field) might replace with a **gentler derived power** (ℓ¹–ℓ²) that softens the overshoot? A gentler power must be **DERIVED**, not tuned to hit ℓ≈1004 (derivation-fitting forbidden).

## Result — the escape hatch is CLOSED; ℓ⁴ is forced by spin algebra + parity

The audit surfaced that the canon has **two** E-mode channels, and S115's amplitude calc used the angular projection consistently with both:

- **Channel A — §12.15.2 lensing-shear:** `E = ð²ψ`, `ψ = ∫W^EE δφ dr`. ð² (two angular derivatives) on the **scalar** δφ. Explicitly **in-phase** with TT (§12.15.6, even-derivative) — does **not** produce Planck's interleaving.
- **Channel B — §12.15.6a–c Route-E gravitomagnetic:** EE reads H₁ via `∂_θ h_tr = H₁ ∂_θ Y`, welded to ∂_t δφ by the rung-2 momentum constraint → **quadrature → interleaving** (the geometry that PASSED at S115).

The Planck-matching geometry is **Channel B**, so the consistent amplitude question is *what angular power does Channel B carry?* The decisive canonical fact (§12.15.6b): the Route-E source is **`δG^t_θ ∝ ∂_θ Y` — a clean transverse-vector, "leftover ≡ 0".** `∂_θ Y` is the **gradient (polar / E-parity) of a scalar harmonic**, i.e. `ð(Y)` up to normalization — **not an independent spin-1 field.** Reaching the spin-2 observable from it costs a **second ð** → total **ð² → ℓ⁴**, identical to Channel A.

### What was derived/verified (`ee_projection_spin_power.py`, sympy + numpy)

1. **Spin-raising recursion** `ð(ₛY)=√((ℓ−s)(ℓ+s+1)) ₛ₊₁Y` gives the three source-spin → spin-2 paths and their C_ℓ power factors (symbolic, exact):
   - **scalar (s=0, ð²):** `(ℓ−1)ℓ(ℓ+1)(ℓ+2) ~ ℓ⁴` — residual vs `(ℓ+2)!/(ℓ−2)!` = 0; at ℓ=2 = **24**, matching the canonical S98-007 sympy result `∫|ð²Y|²=24`.
   - **vector (s=1, ð):** `(ℓ−1)(ℓ+2) ~ ℓ²` — what a *genuine* spin-1 (curl/axial) source would give.
   - **tensor (s=2, id):** `1 ~ ℓ⁰` — what a *genuine* spatial-TT (GW h_ij) source would give.
2. **Parity classification (sympy):** verified `∂_θ Y` IS the gradient of the scalar harmonic (`gradient == ∂_θY` True). The canonical Route-E source is therefore the **polar/E-parity gradient = ð(scalar)**, reducible to s=0 → inherits the full ð² → **ℓ⁴**. A genuine ℓ² source would be the **axial/curl** part `∝ (1/sinθ)∂_φ Y` (B-parity) — which canon **does not produce** (`δG^t_θ` is polar only, leftover ≡ 0).
3. **Peak-location consequence** (canonical W^EE radial weight, ℓ-flat per E6 `R_const=1.21e6`, × raw Planck-TT envelope as the realistic falling source proxy):
   | source spin path | C_ℓ^EE power | peak ℓ (D_ℓ space) |
   |---|---|---|
   | scalar ð² (CANONICAL, S115) | ℓ⁴ | **2085** (overshoot) |
   | vector ð (hypothetical genuine spin-1) | ℓ² | 855 |
   | tensor (hypothetical genuine spin-2) | ℓ⁰ | 225 |
   | — Planck EE target — | — | **1004** |

   (Honest note: the hypothetical ℓ² path peaks at **855** with the raw Planck-TT envelope, *not* the "ℓ²→1004 exactly" the S115 sweep reported with a smoothed source. This does not affect the conclusion — which is about *which* power is forced — but it means even a gentle channel would not be a clean automatic fit; the envelope is source/Phase-E.)

## Why this is a DERIVATION, not an assertion (priority-(i) premise refuted)

§2's premise was that ð²→ℓ⁴ is a *standard photon-transport import* and the pure-metric reframe might give a gentler power. **That premise is false:**
- The ℓ⁴ does **not** come from photon transport. It comes from **spin algebra**: the observable is spin-2, the source is a scalar harmonic (spin-0), and spin-0 → spin-2 costs **ð²** regardless of ontology.
- The pure-metric reframe (D-CMB-NATIVE-3, S98-007) **adopted ð²** as the *correct* spin-2 mode-matching operator (replacing non-covariant operators) — it did not, and cannot, soften it.
- A gentler ℓ²/ℓ⁰ would require the polarization to be sourced by a **genuine** transverse-vector or spatial-tensor metric perturbation. The canonical CMB source is the **scalar breathing δφ** (polar, spin-0); at linear order on the spherically-symmetric static background it excites **neither** a genuine axial-vector nor a TT-tensor mode (SVT/parity decoupling; canon: `δG^t_θ` leftover ≡ 0, `K=0`, `H₂=2δφ`). "δφ rings as a gravitational wave" is about *propagation*, not about δφ being a spin-2 field.

**Disposes of priority (ii) too:** H₁ is welded to ∂_t δφ (rung-2) and lives in the polar scalar sector — it tracks the breathing and carries no independent propagation barrier/damping. The "not exhaustively closed" flag on (ii) is closed by the same parity argument.

## Net consequence for the arc

Priority (i) and (ii) are **DERIVED-NEGATIVE**: there is no gentler derived angular power, and no independent carrier damping. The ℓ⁴ EE overshoot is **forced** by {scalar breathing source} × {spin-2 polarization} × {distortionless metric, no Silk analog}. This leaves:
- **(iii)** a genuinely-*derived* dissipation in the recycling/transport sector (a Silk-analog) — the **only** remaining "fix" lever, and it would have to be a new derived mechanism, not a tuned suppression.
- **(iv)** accept + sharpen the honest falsifiable prediction — now **upgraded from "honest negative" to a DERIVED, ΛCDM-distinguishing signature**: canonical UDT forbids EE small-scale damping (ΛCDM's EE turnover at ℓ≈1004 comes from Silk-damping the *source*; UDT's distortionless metric has no such channel), so canonical UDT predicts EE power *rising* through ℓ⁴ to high ℓ, over-predicting the Planck EE peak ~2×. A clean falsifiable thing the theory forbids, and the data tests.

## ★ Re-grounding after Charles's catch (S116) — "you leaned on pre-S110 deprecated models"

**The catch is correct.** The first pass cited **§12.15.2** (ð²+W^EE lensing-shear, Channel A, S98/S105), **§12.15.6** (S105 *in-phase* TT/EE — the very result S110 overturned), and **§12.15.6a** (S106, then-hypothesis-grade source). S115's amplitude calc itself stapled the current S110+ rung-2 weld (phase/transfer) onto the pre-S110 lensing ð²/W^EE (angular power). That tangle had to be checked, not assumed harmless.

**Does the load-bearing ℓ⁴ depend on the deprecated material? — No (`ee_power_current_only.py`).** Re-derived from CURRENT-only ingredients:
- (C1) the source is the **even-parity scalar breathing δφ**;
- (C2/C3) **§12.15.6b/c (S110, current)** give the carrier source as **`δG^t_θ ∝ ∂_θ Y`** and the transverse current `∝ (∂_φL)∂_θδφ` — both even/polar;
- numerically decomposing `∂_θ Y` onto {polar gradient, axial curl} vector harmonics gives **|axial coeff| ~10⁻¹²** (machine zero) at ℓ,m = (2,0),(2,1),(3,1),(4,2) → the source is **purely polar / scalar-reducible**, NOT a genuine spin-1 field;
- (T1) Regge–Wheeler **parity decoupling** (ontology-independent): an even-parity scalar source excites no odd-parity mode → the only route to the gentler ℓ² (a genuine axial spin-1 source) is **forbidden**;
- (T2) spin algebra: scalar-reducible → spin-2 costs ð² → ℓ⁴.

So **ℓ⁴ survives the purge** — it is forced by current facts + two ontology-independent theorems, NOT inherited from the lensing construction.

**Two honest residual caveats (do not over-claim):**
- (a) The **radial weight W^EE = (r_CMB−r)/(r_CMB·r)e^{2φ₀}** that S115 used IS a pre-S110 Born-lensing kernel. It is ℓ-flat (E6) so it does **not** affect the overshoot, but it should not be presented as the current-model radial weight; the S110+ radial weight should come from the rung-2 weld and has **not** been built.
- (b) The **explicit S110+ angular construction** (rung-2 weld → H₁ angular structure → spin-2 projection) was never carried out. Parity+spin algebra make ℓ⁴ a **theorem**, not a hope — but the clean forward build in the S110+ framework is the rigorous confirmation, and is the legitimate next step if we want this airtight.

**Net:** verdict label stands (ℓ⁴ forced, no derived gentle power), but its **justification is corrected** to current-only grounds, and the radial-weight provenance + un-built forward construction are flagged.

## ★ Clean forward build in the S110+ framework (S116, Charles-directed) — closes both caveats

To retire the two residual caveats, I built the EE projection **forward from the rung-2 weld**, from scratch, without touching the deprecated lensing channel.

### Step 1 — derive the momentum constraint δG^t_θ from scratch (`weld_constraint_derive.py`, sympy)
Perturbed the canonical UDT metric `ds²=−e^{−2φ₀}dt²+e^{2φ₀}dr²+r²dΩ²` with the full even-parity RW-gauge set (H₀,H₁,H₂,K), Y(θ), e^{−iωt}; computed the linearized Einstein tensor and extracted δG^t_θ. Results:
- **Reproduces §12.15.6b independently:** at K=0, H₂=2δφ the radial operator is `−½e^{2φ₀}∂_r(e^{−2φ₀}H₁)+e^{2φ₀}∂_tδφ`, i.e. `∂_r(e^{−2φ₀}H₁)=2∂_tδφ−16πG e^{−2φ₀}δT^t_θ`. The current canonical weld is validated from first principles.
- **Coefficient of Y(θ) is exactly 0** → "clean transverse-vector ∝ ∂_θY, leftover ≡ 0" confirmed.
- **★ ℓ(ℓ+1) is ABSENT from the (t,θ) constraint** (`L` appears in no coefficient). This is precisely the thing the parity/spin-algebra shortcut cannot see — and it is verified absent. The momentum constraint is **ℓ-flat**; it carries no angular barrier that could tame the ℓ⁴. (The ℓ(ℓ+1) the S115 self-audit worried about lives in the *dynamical* breathing equation, which is **common to TT and EE** — both project the same δφ_ℓ — so it cancels in the EE/TT ratio.)
- **Refinement of the canonical weld:** the full constraint is `∂_r(e^{−2φ₀}H₁)=2∂_tδφ + ∂_tK − 16πG e^{−2φ₀}δT^t_θ`. §12.15.6b's **K=0 drops a `+∂_tK` term** (the angular-metric breathing rate) — **not** an ℓ(ℓ+1) barrier. It affects the EE amplitude **normalization**, not the ℓ-scaling. (Candidate CG §12.15.6b annotation, at Charles's tier-gate.)

### Step 2–3 — native radial weight + C_ℓ (`native_weight_cl.py`)
Built the genuinely native weight from the weld: `H₁(r)=e^{2φ₀}∫₀^r 2∂_tδφ dr'`, projected with the §12.15.6a transverse-deflection coupling `e^{2φ₀}/r²` and the §229 measure `e^{−3φ₀}` → `W^EE_native ∝ (e^{2φ₀}/r²)·H₁·e^{−3φ₀}`. Computed C_ℓ^EE = (ℓ−1)ℓ(ℓ+1)(ℓ+2)∫∫W^EE_native W^EE_native P^ℓ with the **full radial-correlation form** (finite coherence Lc~r_CMB/ℓ, **not** Limber).
- The native weight has a **genuinely different radial shape** than the lensing weight (peaks at r=9.16 Gpc vs lensing 8.89 vs W^TT 2.22) — so it is *not* the deprecated kernel in disguise.
- **R(ℓ)=C_ℓ^EE/(ℓ⁴C_ℓ^TT) is ℓ-FLAT** (log-log slope **+0.05** native, +0.02 lensing; ~24% over two decades vs the ℓ⁴ factor of ~10⁷ — negligible). Convergence-stable (N=260 vs 130, identical). **The net EE/TT ℓ-factor is ℓ⁴ regardless of the radial weight** → caveat (a) closed: the overshoot does **not** depend on the deprecated lensing W^EE.
- *Honest scope note:* the **absolute** peak numbers in this script (TT and EE both at the grid edge) are artifacts of a crude analytic source that doesn't reproduce Planck's TT turnover; they are **not** load-bearing. The load-bearing result is the **ℓ-flat R(ℓ)**; the ~2× overshoot *magnitude* (ℓ≈1900 vs 1004) is from S115 E6 with the Planck-TT source proxy.

### Net: both caveats retired
- (a) The native weld-derived weight gives the same ℓ⁴ overshoot → the conclusion never depended on the lensing import.
- (b) The projection is now constructed forward in the S110+ framework (weld → H₁ → spin-2 ð²), and the symbolic derivation confirms the weld carries **no ℓ(ℓ+1)** — so the parity/spin-algebra ℓ⁴ is **airtight**, not a shortcut hiding a missed radial ℓ-factor.

**The clean forward build CONFIRMS ℓ⁴ rather than surfacing an escape.** Priority (i) is closed on current S110+ grounds: there is no derived gentler power; the ~2× EE overshoot is a genuine, DERIVED, ΛCDM-distinguishing falsifiable prediction.

## ★ Priority (iii) — is there a derived Silk-analog dissipation? (S116) — NEGATIVE

To move the EE peak, a damping must be **scale-dependent (diffusive, ∝k², kills high ℓ)** *and* act on the EE/carrier channel; a scale-independent friction is just a normalization. Verified the carrier wave operator on the canonical metric (`silk_analog_check.py`, sympy) against the three damping classes:
- **(A) friction (∂_t A):** the static-metric carrier operator has **zero** first-order ∂_t coefficient (verified) — time-translation symmetry forbids it; and friction is scale-independent anyway (can't move the peak).
- **(B) mass/screening (μ²=π/3):** present in the reservoir scalar, but the KG dispersion ω²=c²(k²+μ²) gives group velocity →0 at **low k** → suppresses **long wavelengths (low ℓ)** — wrong direction.
- **(C) diffusion (k²-loss, the only Silk-analog):** the carrier operator is **DISTORTIONLESS** — verified the tortoise reduction `dr*=e^{2φ₀}dr` sends it to `F_{r*r*}+(ω²/c²)F − e^{−2φ₀}(L/r²)F=0`, principal part dispersionless with constant ω²/c² (lossless Heaviside R/L=G/C line) → no k²-diffusion. The only route to one — a two-way carrier↔matter opacity — is O(ε²) via the exchange identity (one-way at linear order; transverse currents vanish statically → no mean-free-path), not the canonical linear observable.

The sole ℓ-structure is the centrifugal ℓ(ℓ+1) barrier — the standard projection geometry already inside the ð²→ℓ⁴ accounting, **high-pass**, not a small-scale loss. (Note: this directly verifies the doc "distortionless" label for the **even-parity EE carrier**, whereas CG §11.10 D-TRANSPORT-WAVE-2 had derived it for the odd-parity sector.) **No derived Silk-analog → the overshoot cannot be fixed by a derived transport dissipation.** Consistent with C1 ("no metric damping to invent") and the Gate-10 discipline that the only damping is INPUT-class cell-scatter (source-side, which E6 ruled out as the EE lever).

## Frontier resolved — (i)+(ii)+(iii) all NEGATIVE → (iv)
All three "fix" levers for the EE-amplitude overshoot are now closed by derivation:
- **(i)** angular power ℓ⁴ — forced (parity + spin algebra; airtight via the from-scratch weld, no ℓ(ℓ+1)).
- **(ii)** carrier independent barrier/damping — none (distortionless; same parity sector as the breathing).
- **(iii)** derived diffusive Silk-analog — none (distortionless operator; screening wrong-way; opacity O(ε²)).

⇒ **(iv) is the genuine outcome:** the ~2× EE overshoot is a **derived, ΛCDM-distinguishing, falsifiable prediction** — UDT's distortionless metric *forbids* small-scale EE damping, so canonical UDT predicts EE power rising through ℓ⁴ and over-predicting the Planck EE peak ~2× (ℓ≈1900 vs 1004), whereas ΛCDM's EE turnover at ℓ≈1004 comes from Silk-damping its source. A clean thing the theory forbids, that the data tests.

## ★★ REOPENING (S116, Charles-directed ponder) — the native radial function caps the overshoot

**My "frontier resolved / overshoot is the prediction" verdict was premature.** Charles pushed to re-examine the EE ontology, then caught that my projection used `j_ℓ(kr)` — the **flat-space (LCDM-isotropy) radial function**, Gate-10-flagged (B-1), not native. Redoing with the **native UDT radial function** (regular solution of `(1/r²)(r²e^{−2φ₀}u′)′ + [ω²e^{2φ₀}/c² − ℓ(ℓ+1)/r²]u = 0`, of which j_ℓ is the φ₀=0 limit) changes the answer.

**The native radial function carries a centrifugal cutoff the flat-Bessel/Limber projection omitted.** A boundary-sourced mode driven at ω can only *propagate* where `ω²e^{2φ₀}/c² > ℓ(ℓ+1)/r²`, i.e. `ℓ < ℓ_max(r) = (ω/c)e^{φ₀(r)}r`; above it the centrifugal barrier makes the response evanescent. With the recycling drive `ω_drive = c/r_CMB` (cycle = light-crossing, AR §1.6.8):
$$\ell_{\max}(r_{\rm CMB}) = e^{\phi_0(r_{\rm CMB})} = 1+z = 1101.$$
- **Direct native ODE (`native_radial_cutoff.py`, no Bessel):** the boundary shell goes allowed→forbidden right at ℓ_max — ℓ=1004 ALLOWED (oscillatory), ℓ=1101 FORBIDDEN (evanescent). Validated, not assumed.
- **EE = ℓ⁴ × (field capped at ℓ_max) peaks at ℓ≈1000** (vs Planck **1004**); TT peaks low (the BAO source scale). The ℓ⁴ growth slams into the metric's own angular cutoff.
- **Robustness (`native_cutoff_robustness.py`):** convergent (T1: 956–1020); **source-width-independent** (T2: 956 at every width → not a source fit); and (T3) **EE peak ≈ 0.9·ℓ_max at all ω_drive** → the peak *tracks the native cutoff*.

**So the S115 ~2× overshoot (ℓ≈1900) was the flat-Bessel/Limber omission of the metric's own radial cutoff** — exactly "a small part of the model doing the wrong thing, not what the metric is really doing" (Charles's intuition, vindicated). The native projection puts the EE peak at the metric scale **1+z ≈ Planck's 1004.**

**Honest status — CONSISTENT, not FORCED (labeling asymmetry: under-claim).** The whole result rests on one physical claim: **ω_drive = c/r_CMB** (the EE-relevant driving frequency = the recycling cycle = light-crossing time). That is canonically motivated (AR §1.6.8 τ≈r_CMB/c) but the recycling rate carries an input piece (f), and identifying the *projection* driving frequency with the recycling cycle needs a real derivation. Open threads before this can be called forced:
1. **Derive ω_drive = c/r_CMB** for the EE projection (not just assert the recycling cycle).
2. **Confirm broadband washing:** ω=c/r_CMB also brings coherent Δℓ≈3 ("cavity ringing") oscillations into T_ℓ, which are NOT observed; a broadband recycling drive P(ω) (input, S108) should wash those while preserving the ℓ_max *envelope* cutoff. Verify the comb spacing stays Δℓ≈297 (BAO source) and the Δℓ≈3 ringing is suppressed.
3. **Verify the firewall survives** the native projection: do the EE interleaving (positions) + TE (10 flips) still hold with the cutoff? (Cutoff is common to TT/EE so positions should survive; verify.)
4. This is all scalar-sector (BB-safe).

**Net: the EE-amplitude question is REOPENED, not closed. There is a derived candidate — the native radial cutoff at ℓ_max = 1+z — that brings the EE peak to ~1000 ≈ observed, conditional on ω_drive = c/r_CMB.** The prior "overshoot is the falsifiable prediction" verdict is withdrawn pending the four threads above.

## ★★★ TT FIREWALL CROSS-CHECK (S116) — the native-cutoff EE fix is REFUTED; overshoot stands

Before deriving ω_drive = c/r_CMB I ran the cross-channel firewall on it (`tt_crosscheck_cutoff.py`), because the cutoff ℓ_max = (ω/c)e^{φ₀(r_CMB)}r_CMB is **common to TT and EE** (same breathing field, same ω). Result — **decisive negative:**
- **ω = c/r_CMB** (ℓ_max=1101, the value that puts EE at ~1000): TT power above ℓ=1101 is **exactly 0.000**; above ℓ=1500, 0.000. TT **dies at the cutoff** — flatly contradicting Planck TT, which has real acoustic power out to ℓ~2000.
- **ω = 2.3 c/r_CMB** (ℓ_max≈2532, the value TT needs): TT survives to ℓ=1500-2000 (D_ℓ 0.27/0.13 ✓), but then EE = ℓ⁴ × (cap at 2532) **overshoots again** (~2250).

**A common cutoff cannot simultaneously cap EE at ~1004 and let TT run to ~2500.** The carrier (EE) and the scalar breathing (TT) share the cutoff because the rung-2 weld ties H₁'s radial structure to δφ's, so EE and TT cannot have different ℓ_max. The EE≈1000 match (the REOPENING above) was **real arithmetic but physically inconsistent with TT** — obtained by an ω that kills the observed TT high-ℓ power.

**Verdict flip — honest record.** This dispatch went: (1) "overshoot is the falsifiable prediction" → (2) Charles ponder + the j_ℓ catch → "REOPENED, native cutoff lands EE at 1+z≈1004" → (3) **TT firewall → the cutoff fix is REFUTED; the overshoot stands.** The firewall (Charles's keystone — *always cross-check the other channel*) is the arbiter, and it killed a fix that looked clean in the EE channel alone. **Net current state: the ~2× EE overshoot stands, now stress-tested against its single most promising fix.** The native radial cutoff is real metric physics, but it is common to both channels and TT pins it high (≥2500), so it cannot tame EE. Lesson banked: the EE-channel-only "fix" that died on the TT cross-check is exactly why Phase D (fit-one-predict-two) is the keystone.

**What would still be needed to revive a fix:** a mechanism that gives the EE/carrier channel a genuinely *lower* effective cutoff than the TT/scalar channel — but the weld ties them, so this looks closed at canonical content. Absent that, the overshoot is the honest, ΛCDM-distinguishing prediction (now firewall-hardened).

## ★★★★ PONDER 2 (S116, Charles: "modify the base model for TT — close but missing something")

**The strongest candidate yet — a missing TERM in the base temperature model, not a patch.** The overshoot is one ratio: TT reads the *potential* (δT/T=−δφ, Sachs-Wolfe redshift), EE reads the *tidal field* of that potential (ð²→ℓ²). Potential vs its Laplacian = ℓ²; in power, ℓ⁴ — the whole gap.

But ΛCDM's temperature is `δT/T = ¼δ_γ + Φ + v·n̂`: the SW **Φ** only dominates the plateau (ℓ<30); at the acoustic peaks TT is the **intrinsic photon density ¼δ_γ**, not the potential. **UDT's model kept only the Φ (redshift) piece and dropped the ¼δ_γ analog.** In the recycling ontology that analog is forced: a denser re-emergence region is intrinsically *hotter*, so the temperature carries an **intrinsic emission term δT ∝ δρ ~ ∇²δφ** (the density of the breathing). The complete model:
$$\frac{\delta T}{T} = \underbrace{-\delta\phi}_{\text{SW redshift (have it)}} + \underbrace{c\,\delta\rho\sim\nabla^2\delta\phi}_{\text{intrinsic re-emergence temp (MISSING)}}.$$
The intrinsic piece is itself a Laplacian/tidal object carrying ℓ² — the **same** ℓ² EE carries.

**Numerical confirmation (`tt_density_term.py`, native radial-correlation, NO flat Bessel):**
- EE/TT with **TT=potential** (current): log-log slope **+4.04** → the ℓ⁴ overshoot.
- EE/TT with **TT=density** (the peak-dominant term): slope **+0.04** → **flat. The overshoot collapses ℓ⁴ → ℓ⁰.**

**Refinement the numbers force:** TT=density *alone* is too **blue** (0.998 of power above ℓ=1000 vs Planck 0.222), just as TT=potential alone is too red. So the answer is **both terms** (SW + intrinsic), ΛCDM-style: −δφ dominates the plateau (ℓ≲tens), c·δρ dominates the peaks. At the peaks (where EE maxes, ℓ~1000) TT is density-dominated → **EE/TT flat → no overshoot.** The absolute peak locations in the script are grid-edge artifacts of a crude analytic source (NOT load-bearing); the load-bearing result is the **slope +4.04 → +0.04**.

**Why this is the catch Charles was pointing at, and why it's different from the failed candidates:**
- It **modifies the source/base-model** (adds the physically-required intrinsic-temperature term), not a band-aid on the projection. So it **survives the firewall by construction**: TT and EE come from the *same* field, both tidal at the peaks → the common-cutoff conflict that killed the native-cutoff candidate doesn't arise.
- It fixes **two** standing problems with one term: the EE overshoot **and** the long-standing "TT falloff shape wrong in detail" (bare-SW TT is ℓ⁴-too-red; the density term supplies the acoustic high-ℓ power TT is observed to have).
- It's **required, not invented** — the recycling ontology (CMB = re-emergence of recycled matter as radiation) demands an intrinsic emission-temperature ∝ density; the ΛCDM analog (¼δ_γ) is standard. The current −δφ-only model is the truncation.
- **Locks respected:** δρ = density of the *breathing oscillation* (∇²δφ, gravity-driven), NOT the static matter map; the oscillator still makes the comb. Not matter-as-source.

**Honest status — CONSISTENT + structurally confirmed, NOT yet FORCED (and I've twice been wrong this dispatch, so: under-claim).** What remains:
1. **Derive the coefficient c** of the intrinsic δT∝δρ term from the recycling emission physics (the temperature-density relation of re-emergence) — currently asserted by analogy, not derived.
2. **Verify complete TT = −δφ + c·δρ matches Planck TT** (plateau + acoustic peaks + falloff) with a *realistic* source/comb — the crude-source numerics here can't assess absolute shape.
3. **Verify EE lands at ℓ≈1004 with the right amplitude** under the complete model, and that the interleaving/TE firewall survives.
4. Reconcile with the canonical amplitude AR §1.6.10 (δT/T=0.038(δρ/ρ)(L/r_CMB)² is the *SW* piece, scale²-suppressed; the intrinsic piece is un-suppressed and dominates at small L/high ℓ — consistent, but the canonical record currently has only the SW piece).

**This reopens the EE frontier on the most promising footing of the dispatch: the overshoot is plausibly an artifact of an incomplete TT base model (SW-only), and the physically-required intrinsic-density term collapses it — fixing TT's shape at the same time.**

## ★★★★★ DERIVE c (S116) — Ponder 2 confirmed from the metric + blackbody (DERIVED, not fitted)

Charles: "derive the coefficient c." Two ingredients, both canonical:

**(A) The temperature–density relation is Stefan-Boltzmann (the blackbody UDT already derived).** ρ_γ ∝ T⁴ ⟹ δρ_γ/ρ_γ = 4 δT/T ⟹ **δT/T (intrinsic) = ¼ δρ_γ/ρ_γ. c = ¼** — not a free parameter.

**(B) δρ(δφ) from the metric's own Einstein tensor (`derive_intrinsic_coeff.py` + `density_angular_test.py`, sympy).** For the UDT breathing metric, `ρ = −G^t_t/(8πG)`. Linearizing in δφ (with the **angular** dependence φ(t,r,θ) kept — the critical step):
$$\delta\rho = -\frac{1}{8\pi G r^2}\,\partial_\theta^2\delta\phi \;+\; \frac{e^{-2\phi_0}}{4\pi G r}\,\partial_r\delta\phi \;+\;(\dots)\delta\phi.$$
The angular-Laplacian coefficient is **−1/(8πG r²) ≠ 0** (sympy-verified) → for a mode Y_ℓm, the angular piece gives **δρ → +ℓ(ℓ+1)/(8πG r²)·δφ**, i.e. at the acoustic scales **δρ ~ ℓ(ℓ+1)δφ**. (My first pass used φ(t,r), no angle, and wrongly got coefficient 0 — caught and corrected.)

**Chain closes, end to end:**
- δρ ~ ℓ(ℓ+1)δφ (from G^t_t — DERIVED) ⟹ TT_intrinsic = ¼δρ/ρ ~ ¼ℓ(ℓ+1)δφ ⟹ C_ℓ^TT,int ~ [ℓ(ℓ+1)]²|δφ|².
- EE = ð²(velocity) ~ ℓ(ℓ+1)·v ⟹ C_ℓ^EE ~ [ℓ(ℓ+1)]²ω²|δφ|².
- **EE/TT,int ~ ω² — FLAT.** The ℓ⁴ overshoot collapses. (This is exactly the [ℓ(ℓ+1)]² factor `tt_density_term.py` used to measure slope +4.04 → +0.04; now derived, not assumed.)

**So the complete temperature is `δT/T = −δφ + ¼(δρ/ρ)`, both terms derived** — the SW redshift (had it) + the intrinsic re-emergence temperature (Stefan-Boltzmann ¼ × the metric's δρ~ℓ(ℓ+1)δφ). The intrinsic piece dominates at the acoustic scales (ℓ²-enhanced), so TT traces the breathing density there and EE/TT is flat → **no ℓ⁴ overshoot.** This is the ΛCDM `Φ + ¼δ_γ` structure, *derived from the UDT metric + its blackbody* rather than imported.

**Status — MECHANISM DERIVED; quantitative match PENDING.**
- DERIVED: δρ carries ℓ(ℓ+1) (metric G^t_t, sympy); c = ¼ (Stefan-Boltzmann, the blackbody); EE/TT flat (the slope collapse).
- The one not-fully-forced link: **δρ_γ/ρ_γ = δρ/ρ** (re-emerged radiation contrast tracks the breathing/matter density contrast). Physically motivated (radiation re-emerges in proportion to local dissolution), so c = ¼·η with the tracking efficiency η~1; η<1 only if recycling thermalization washes the small-scale contrast (a source-side effect, separate question). The ℓ² (the overshoot-fixer) is independent of η.
- PENDING (#2): does complete TT = −δφ + ¼δρ/ρ match Planck TT (plateau + peaks + falloff) and land EE at ℓ≈1004 with the right amplitude, under a *realistic* source? The mechanism is derived; the full data match needs the realistic-source projection.
- **Canonical-record implication (at Charles's tier-gate):** AR §1.6.2's `δT/T = −δφ` is **incomplete** — it is the SW piece only and is *sub-dominant at the acoustic peaks*; the dominant intrinsic ¼δρ/ρ term (derived here from G^t_t + blackbody) is missing. Candidate canonical-record edit.

**This survived the metric's own test** (the angular Laplacian had to be non-zero, and it is) — the strongest footing of the dispatch. The overshoot is an artifact of the truncated (SW-only) temperature model; the metric's full δT/T, with the Stefan-Boltzmann intrinsic term it already implies, removes it.

## #2 — complete model vs Planck (`complete_model_vs_planck.py`): overshoot fix CONFIRMED, peak-separation NOT yet

Built the thin-shell forward model of the complete `δT/T = −δφ + ¼δρ/ρ` (TT) + `ð²(velocity)` (EE), one source, source tuned to TT then EE predicted. Honest results:
- **The overshoot is killed — confirmed quantitatively.** EE/TT log-log slope on ℓ∈[300,1500] = **−0.00** (vs +4 for the SW-only model), with a realistic source and the **derived** background `B = 8πGr²ρ₀ = 1.0000` (the deep-boundary limit e^{2φ₀}·e^{−2φ₀}=1, robust). So the derived intrinsic-temperature term takes EE/TT from ℓ⁴ to flat with no tuning. **This is the session's core result, now validated on a realistic source.**
- **B=1 ⟹ the SW term is sub-dominant for ℓ≥2** (transition ℓ(ℓ+1)=4B → ℓ≈2). So TT ≈ ¼Δ (traces the density) at all observable ℓ; the SW −δφ is only an ℓ≈2 correction.
- **What did NOT pan out:** the hoped "SW boosts TT at low ℓ → TT peaks low, EE peaks high" structural separation **fails** because B=1 makes the SW boost negligible above ℓ=2. In this toy, TT and EE both trace the density and peak together — the **TT-220 / EE-1004 separation is not explained by the intrinsic term alone.** It requires either (a) the velocity transfer **ω(ℓ) rising** with ℓ (the S115 root-gap, still unresolved), or (b) the **acoustic comb** (BAO source + oscillator dynamics) that boosts TT's first peak — neither is in this smooth-source thin-shell toy.
- **The TT-vs-Planck shape fit is crude** (smooth source, no comb) — not a real peak-by-peak match yet.

**Net of #2:** the derived intrinsic-temperature term **definitively kills the ℓ⁴ overshoot** (EE/TT flat, validated) — that part of Charles's "missing term" diagnosis is confirmed and quantitative. But "flat EE/TT" is the *ballpark*, not Planck's exact EE/TT(ℓ) (a mild rise + interleaved peaks). The **remaining residual — the exact TT/EE peak positions and the mild EE/TT rise — is set by the velocity transfer ω(ℓ) + the comb**, which is the full forward model (a bigger build), not settled here. So: overshoot **fixed** (mechanism derived + validated); full peak-by-peak Planck match **still open**, now isolated to ω(ℓ) + comb rather than a factor-of-ℓ⁴ structural error.

## Full forward model assembled (`full_forward_firewall.py`) — structure falls out; residual = a MILD transfer

Assembled all derived/forced pieces into one strict firewall (fit TT → predict EE+TE, no refit): TT = intrinsic-temperature-dominated envelope × oscillator comb (BAO Δℓ≈300); EE = same envelope × **interleaved** comb (forced sin² midpoints) × flat transfer, amplitude = one input ε; TE = forced cross.

Honest results:
- **Comb positions ~work:** model TT peaks [537, 827, 1123, 1421, 1720] line up with Planck [540, 810, 1130, 1450, 1750] at spacing ~300 (BAO). **But the crude fit MISSED the first peak (220)** — a *rising* envelope suppressed it. **This is a fit failure (envelope shape), not structural** — the comb is present; a proper fit (envelope declining from ℓ~220) is needed and wasn't achieved in this coordinate-scan pass.
- **Interleaving + overshoot-removal fall out** with no new freedom (EE sin² midpoints; finite EE from the intrinsic term).
- **EE envelope residual — and it points somewhere physical:** the flat-transfer EE peaks at **1570** (mildly high vs Planck 1004). The data require the EE/TT envelope ratio to **fall** ~ℓ^−0.42 → a **mild falling velocity transfer ω(ℓ)~ℓ^−0.21**. This is the **same direction and rough magnitude S115's careful analysis already found** (keeping the dropped ℓ(ℓ+1): "transfer mildly falls, 23–42%"). So the residual is a *physically-pointed-to* mild transfer, **not a free fudge**.

**Net of the full build:** with the derived intrinsic-temperature term doing the heavy lifting (ℓ⁴→ℓ⁰), the CMB **structure** (comb spacing, interleaving, overshoot-removal) falls out of the derived/forced pieces, and the **EE envelope residual is a MILD transfer ω(ℓ)~ℓ^−0.2** — exactly what S115's ℓ(ℓ+1)-careful transfer analysis indicated. **What was NOT achieved:** a proper quantitative Planck fit (the crude scan got the TT envelope shape wrong / missed the first peak). So the model is *assembled and coherent*, not yet *fit*.

### Session arc summary (this dispatch)
1. (i)/(ii)/(iii) — no gentler angular power, no carrier damping, no diffusive Silk-analog → "overshoot is the prediction."
2. Ponder + native-radial-cutoff candidate → **refuted by the TT firewall** (common cutoff).
3. **Ponder 2 → the real fix:** the base TT model was truncated to Sachs-Wolfe; the metric's own G^t_t + its blackbody supply the missing **intrinsic-temperature term δT/T = −δφ + ¼δρ/ρ** (c=¼ derived; δρ carries ℓ(ℓ+1) from G^t_t). This **collapses the ℓ⁴ overshoot to ℓ⁰** (validated). The "EE failure" was a **TT base-model truncation**, not an EE problem.
4. Full forward model: structure falls out; EE-envelope residual = a **mild derived transfer ω(ℓ)~ℓ^−0.2** (consistent with S115), + a proper fit still owed.

**Canonical implication (tier-gate):** AR §1.6.2 `δT/T = −δφ` is incomplete (SW-only, sub-dominant at the peaks); the dominant intrinsic ¼δρ/ρ term (derived from G^t_t + blackbody) is missing. Candidate canonical-record edit + a model-lock memory update so the next instance doesn't regress to SW-only TT.

## Gates
Gate 5/8/10 token scan (NAME tokens, string-stripped): **hits=[]**. The only borrowed machinery is the Limber radial reduction (`# SCAFFOLDING`-flagged, E6-established ℓ-flat, cancels in the EE/TT ratio). Theory Rules 2/4/5 clean: full nonlinear φ₀ profile; no imported physics; static metric, scalar source. No fitting (the ℓ² peak was *reported* at 855, not tuned to 1004).

## Files
- `ee_projection_spin_power.py` — spin recursion + parity test + peak-location table + gate scan.
- Canonical inputs (verbatim, not re-derived): CG §12.15.2 (ð²+W^EE), §12.15.6/6a/6b/6c (in-phase scalar channel + Route-E + rung-2 weld + current), §12.4 (ð² machinery), §11.10 (carrier).
- Predecessor: `dispatch_D_CMB_EE_AMPLITUDE_RUNG2_1/AUDIT.md` §E6 (radial R(ℓ) ℓ-flat — the radial half; this dispatch closes the angular half).
