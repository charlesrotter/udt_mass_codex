# P16 DECISION NOTE — does spinning matter (ω≠0) source the depth field φ? (Fork-3b)

**Mode: armchair/CAS-symbolic decision note, data-blind, NO solve. A FRAMING note, not a result.**
Deriver agent aba0399ef8316c9ce (CAS-checked); driver sign-correction folded in (see §4).
Answers the P16 fork raised in `node23_precompute_map.md` Q2b, per Charles's order (P16 before the F4 test).

## Verdict: **C — NATIVELY UNDECIDED** (documented lean → A; do NOT bank as A or B)

The native action does NOT fix whether spinning matter sources φ. That single unforced choice IS the answer.

## 1. What "φ-blind" precisely means (STEP 1)
φ-blindness is NOT a naive δS_m/δφ at fixed metric (that object is nonzero — the raw L2 contains
g^{rr}Θ′²=e^{−2φ}Θ′², φ-dependent). The derived statement (`native_field_equations_constrained_two_player_results.md:71-77`)
is: **matter couples to the BARE / undilated inverse metric ḡ^{mn}** (channel-correction), which strips the
e^{±2φ} depth-weights (radial channel e^{−2φ}Θ′² → Θ′²; angular already weight-0; measure √−g=c√h φ-free,
:91). Then the channel-corrected S_m contains no φ ⇒ δS_m/δφ=0; matter sources φ only INDIRECTLY via
geometry n→h_AB→𝒦→φ, and only in Branch P. **The sole justification for channel-correction is exact
depth-shift symmetry φ→φ+λ — a Branch-G/vacuum property. The particle lives in Branch P, where that
symmetry is BROKEN** (:117-124). Conditional on the R1+P5 shift levers (tagged CHOSE, :151).

## 2. With ω≠0 (STEP 2)
Turning on the spin (χ=Nψ+ωt) adds to X exactly **−ω²e^{+2φ}sin²Θ/c²** (the time channel g^{tt}G_tt;
CAS-confirmed). It carries the OPPOSITE depth-weight (e^{+2φ}, shift factor e^{+2λ}) vs the static radial
term (e^{−2φ}). Everything hinges on **whether channel-correction extends to the time channel**:
- **extends ⇒ A (φ-blind survives):** ḡ^{tt}=−1/c², ω-term → −ω²sin²Θ/c², φ-free; and an internal phase
  rotation does not change h_AB, so the only derived matter→φ channel (indirect via 𝒦) is ω-independent.
  Spin then binds through the metric/ρ (frame-drag) sector.
- **does not extend ⇒ B (φ-blind breaks):** matter couples to the physical g^{tt}=−e^{+2φ}/c² in Branch P,
  adding a φ-source; the Branch-P φ-player equation becomes
  **Z_φ(r²φ′)′ = 4e^{−2φ} + (ξ/c²)e^{+2φ}ω²sin²Θ·(√h/√ĥ)** (+L4, O(j) analogs) — the founding depth×spin coupling.

## 3. Why C, not A or B (STEP 3)
The exact missing ingredient: **a native derivation of the matter–φ coupling WEIGHT in Branch P** — whether
channel-correction (justified by a symmetry Branch P breaks) still forces bare-channel coupling once
absolute φ is physical. R1 leaves the relevant weights FREE (:154). The action is silent. It must NOT be
closed by (i) importing GR's g^{tt} minimal coupling (silently selects B — trigger-#6 forbidden), nor by
(ii) assuming channel-correction trivially transplants (silently selects A). **Lean → A is a consistency
lean, NOT a derivation** (the consistent non-import extension of the derived static rule channel-corrects
the time channel too; B requires an ad-hoc asymmetric coupling). The `native_dilation_weight_derivation:408-416`
obstruction is about the φ-field's OWN kinetic term (Flavor III), not the matter coupling; per-channel bare
correction is fine for both signs — so it neither forces B nor cleanly forces A. (P16 = UNDERDETERMINED,
not forbidden — re-grade already banked.)

## 4. DRIVER SIGN-CORRECTION (folded in — the P16 note's "depth-enhanced" narrative is backwards)
The P16 note characterized the B-branch φ-source (∝ e^{+2φ}) as "depth-ENHANCED — spin reaching the deep
core." **This is backwards for the particle cell.** From the Branch-P flux law: the φ-equation source
+4e^{−2φ}>0 ⇒ (ρ²φ′)′>0 ⇒ ρ²φ′ increases from 0 at the core even fold ⇒ φ′>0 ⇒ φ increases outward to
φ(seal)=0 ⇒ **φ_core < 0.** Hence e^{+2φ} is SMALL (suppressed) at the core and →1 at the seal. So the
B-branch φ-source (∝e^{+2φ}sin²Θ) is ALSO outer-shell-weighted (suppressed at the core wall) — exactly like
the Q3 Θ-binding (∝e^{2φ}). **Consequence: branch B does NOT reach the deep core better than branch A; in
BOTH branches the ω-help is outer-shell.** The two agents used opposite φ-core sign conventions; the
CAS-checked Q3 one (φ_core<0, e^{−2φ_c}≈1.2×10⁶) is correct. (Empirically confirmable on the saved E2 φ(r)
— to be checked at F4 setup.) This removes the main physics motivation to prefer branch B; the make-or-break
in BOTH branches is whether outer-shell binding can INDIRECTLY relieve the core stiffness (= the F4 test).

## 5. Consequence / next step
P16 is natively UNDECIDED ⇒ per Charles's pre-authorization, run the bounded NODE-3 F4 test in BOTH
branches (φ-blind = channel-corrected ω-term −ω²sin²Θ/c²; raw = physical −ω²e^{+2φ}sin²Θ/c²). Saved real
E2 φ(r) fields exist (E2b_*.pt). Test spec (Charles): 1-D only; saved real φ(r) (not flat toy); Nr≤16–24;
Jacobi/Derrick ONLY; output = F4 classification {stabilizer works / too weak-depth-suppressed / no
restoring term}; NO nonlinear solve; no labels/masses/data. Nail sign(φ_core) empirically as setup.

## Premise tags
- φ-blind = channel-corrected δS_m/δφ=0: DERIVED conditional on R1+P5 (CHOSE).
- channel-correction grounded in exact shift symmetry: THEORY (Branch-G) — does NOT transplant to Branch P by derivation.
- ω-term −ω²e^{+2φ}sin²Θ/c², opposite depth-weight: DERIVED (CAS).
- matter time-coupling weight in Branch P: FREE/UNDERIVED (the deciding object; R1-free).
- φ_core<0 ⇒ both branches' ω-help outer-shell: DERIVED (flux law; driver §4; empirically confirmable).
- "lean A": consistency lean, NOT a derivation — do not bank.
