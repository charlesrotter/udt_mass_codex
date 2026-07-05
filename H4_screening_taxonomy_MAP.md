# H4 — Screening branch-taxonomy MAP: log-periodic DSI is a FROZEN-W ARTIFACT (not discreteness); N4a screening REFINED

**Status: BANKED (2026-07-05), blind-verified — a SPECULATIVE TAXONOMY MAP whose load-bearing DERIVED core is
verified; taxonomy legs tagged [SPEC]/[DERIVED].** Armchair/CAS + bounded ODE-numeric (no mass solve, no L⁻¹
response solve, no hopfion re-solve). DATA-BLIND; Z_φ symbolic; no SM labels; "force" used only where native
flux-coupling math is checked. MAP agent a7623543a23c863bc; blind adversarial verifier accd578cc50d245e0 (core
PASS; caught + corrected one headline over-reach — softened statement adopted below). Scripts:
`h4_scripts/dsi_analysis.py`, `dsi_numeric.py`, `dsi_verify_running_ambient.py`.

> **LABEL FIX (2026-07-05, revised-N4):** where this doc says "DEEP-P ambient ⇒ screened/oscillatory," the label is
> BACKWARDS — oscillatory roots need φ_amb < ½ln(32/Z_φ) = **SHALLOW**; **DEEP = clean.** Physics (running ambient
> W→0 ⇒ clean monopole recovered; artifact verdict) is UNCHANGED; only shallow/deep labels are corrected.

## ★ Headline (verified, verifier-softened)
**The log-periodic / discrete-scale-invariant (DSI) far field is a FROZEN-COEFFICIENT ARTIFACT — NOT a native
discreteness engine.** N4a's indicial analysis froze W₀=e^{−2φ_amb} as a constant (a legitimate *local* snapshot);
the true ambient RUNS and drives the screening coefficient to zero, so no persistent log-periodicity survives.
Verified two ways (self-consistency argument + direct numeric integration; the oscillation band is so thin it
**never completes even one cycle** for any physical core). **⇒ "log-periodicity = discreteness" is DEAD as a lead
— do not pursue it.** If native discreteness exists, it lives in the P-interior flux-ladder / closure machinery
(D2b), NOT in a far-field DSI.

**Verifier-softened refinement of N4a (do NOT overstate to "branch-blind clean mass"):** the clean 1/r monopole is
recovered **over the entire physical range** and **exactly** in a Branch-G / shallow (W₀<Z_φ/32) far field; on a
DEEP-P ambient the far field is clean for all physical radii (the marginal onset sits at trans-astronomical
ln r ~ 2×10²⁴, beyond any finite cell — canon: no spatial infinity). At *strict* r→∞ on the shallow log-log
attractor a **MARGINAL LOGARITHMIC (non-oscillatory) screening with non-conserved flux** (δφ~1/ln r) remains. So
**N4a's screening CONCLUSION is REFINED (log-periodic → at most marginal-logarithmic), NOT overturned; and the
far field is NOT strictly branch-blind** (residual Branch-G conserved-flux vs deep-P marginal-log distinction,
physically small).

## Part C — the DSI verdict (the load-bearing DERIVED result)
- **Running ambient (DERIVED, CAS-exact + verified):** the ambient ODE Z_φ(r²φ_amb')'=4e^{−2φ_amb}, in t=ln r, is
  Z_φ(u_tt+u_t)=4e^{−2u}; dropping u_tt (self-consistent: u_tt/u_t=−8/(CZ_φ+8t)→0) gives **φ_amb(r) ≈
  ½ln((8/Z_φ)ln r + C)** (log-log growth; residual identically 0 on this ansatz) ⇒ **W(r)=e^{−2φ_amb} ≈
  Z_φ/(8 ln r) → 0** (W·ln r → Z_φ/8).
- **Consequence:** with W(r)→0 the perturbation operator Z_φ(r²δφ')'+8W(r)δφ=0 degenerates to the source-free
  Euler operator (roots {0,−1}); the decaying mode → real, non-oscillatory; the complex-root/oscillatory band is
  confined to a **bounded near-core skirt** r<r* (r* is core-BC-dependent, ~1–7, NOT a robust fixed number — the
  earlier illustrative 8.5/13 are IC-dependent). Flux test: Π=Z_φr²δφ' conserved (clean monopole) for W=0 and over
  all physical radii for a deep ambient; only on the strict-∞ shallow attractor does Π grow (marginal-log screening).
- **Self-consistency argument (DERIVED, sound):** genuine DSI needs W=const ⇒ φ_amb=const ⇒ e^{−2φ}=0, impossible
  — i.e. the frozen approximation that PRODUCES the DSI assumes exactly the asymptotically-constant vacuum that
  Branch-P is derived to FORBID (§6). Self-undercutting.
- **Adversarial search (verifier):** maximizing accumulated oscillation phase over ALL core ICs (φ₀, slope) at
  Z_φ=1 and 8 — the oscillation never reaches one cycle for physical cores; extra cycles only at absurd depth are
  trapped at r≈1 (the core, r*→1). **No regime with genuine asymptotic DSI exists.** Z_φ-robust (W→0 ∀Z_φ>0).

## Part A — the branch taxonomy (native; [SPEC] unless tagged) — it COLLAPSES to an INTERIOR distinction
1. **Shallow / Branch-G [DERIVED, conditional]:** source-free exterior ⇒ clean δφ=−δq/r ⇒ a public/far-field mass
   (conserved dilation flux δQ_φ=∫√h Z_φ δφ' d²x on a bulk read-surface; δm=δM=−δq; flux=Z_φ×charge).
2. **Deep / Branch-P [DERIVED-revised]:** the N4a "screened ⇒ no clean mass" reading is CORRECTED by Part C — the
   deep-P object is a **cored monopole**: the same clean public far-field mass over all physical radii, dressed by a
   bounded near-core skirt (+ a physically-moot marginal-log tail at strict ∞). It is NOT a mass-less/internal object.
3. **Pure-G flux conduit [DERIVED conduit; FORCE NOT ESTABLISHED]:** from D2b (E1: G carries MS geometric mass with
   φ≡const & ZERO dilation charge; E4: "G can CARRY flux between P-structures but cannot terminate/close it") — a
   G-interstitial conducts a conserved flux (Φ=Z_φρ²φ' exactly constant in G) between P-terminals. Native
   flux-carrier CONFIRMED; but **no two-body interaction energy is derived**, so "force" is NOT established (do not
   call it a force). A standalone massless pure-G object cannot self-close (E4) — the conduit is interstitial.
4. **Genuine split? [SPEC → collapses]:** the naive 3-way far-field split (mass-bearing G / screened-internal deep-P
   / massless-carrier pure-G) does NOT hold: the screened-internal leg is a frozen artifact (Part C), the
   massless-carrier leg is not a standalone object (E4). What genuinely DERIVES is a **2-way INTERIOR distinction**
   (NOT the sole distinction — see the residual far-field note above): **active-P interior** (𝒦≠0 sources φ; the
   native φ-angular coupling + the whole emergence machinery — anchor Δφ, seal charge, flux ladder, quantization
   closures, D2b T-G2 — are ON) vs **dead/slaved-G interior** (φ source-free/const; holds MS-massed φ-inert matter,
   conducts flux, but NO emergence machinery). Both interiors present ~the same far-field monopole.

## Part B — parameters (Z_φ symbolic)
| quantity | form | Z_φ=1 | Z_φ=8 |
|---|---|---|---|
| critical depth (frozen) | φ_amb^crit = ½ln(32/Z_φ) | 1.7329 | 0.6931 |
| frozen indicial roots | s = −½ ± √(Z_φ−32W₀)/(2√Z_φ) → {0,−1} as W₀→0 | — | — |
| frozen "DSI" ω (near-core ONLY) | ω = √(32W₀−Z_φ)/(2√Z_φ) | — | — |
| **running ambient** | φ_amb(r) ≈ ½ln((8/Z_φ)ln r + C) | — | — |
| **running coeff (→0)** | W(r) ≈ Z_φ/(8 ln r) | — | — |
All Z_φ-robust: W→0 ∀Z_φ>0 ⇒ the DSI-artifact verdict holds for both Route A (Z_φ free) and Route B (Z_φ=8).

## Provenance / discipline
No SM categories/labels; no GR import; Z_φ symbolic; "force" rated NOT-established. DERIVED: the artifact verdict,
the running-ambient asymptotic, W→0, the critical-depth/ω formulae, the interior active-P/dead-G distinction (D2b).
[SPEC/analogy, wait on the G/P switch + a bounded interior solve]: any richer particle-type taxonomy; the deep-P
mass SIGN (rides CF1/CF2, still open); the physical role of the near-core skirt.

## Implication for the NEXT step (the G/P switch for the hopfion — Charles's option 1)
1. **De-prioritize "clean far-field mass" as the switch DRIVER** — the far-field monopole is *nearly* branch-blind
   (both G and deep-P present a clean public mass over physical radii; only a marginal-log residual distinguishes
   them at strict ∞). The G/P switch barely changes the EXISTENCE of a public mass; it changes the INTERIOR.
2. **Re-aim the switch at the INTERIOR question it actually governs:** does the hopfion's core sit in an
   **active-P interior** (finite angular geometry breaks the depth-shift ⇒ 𝒦-source + emergence machinery ON) or a
   **dead-G interior**? The hopfion's n:S²→S² winding / finite toroidal angular geometry is exactly candidate-switch
   (2)/(3) of the §10 two-player doc — the most promising native trigger to prove.
3. **Drop the "log-periodicity = discreteness" branch of the hunch;** re-point the discreteness search at the
   P-interior flux-ladder / closure machinery (D2b).
4. **One cheap owed object (bounded, anti-hang-safe, NOT the mass solve):** the variable-coefficient near-core skirt
   δφ solve on the running background — characterizes where interior structure imprints on the field.
