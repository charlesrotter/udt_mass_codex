# D2a — The G/P switch criterion applied to the solved N=0 fundamental interiors

**Date:** 2026-07-04. **Contract:** `microphysics_D2_two_regime_MAP.md` Q1 ("where is G, where is
P, inside the solved universe?"), approved by Charles 2026-07-04. **Mode:** OBSERVE — CAS/algebra
on the blind-verified E0 tables only (`microphysics_E0_ambient_tables.md`/`.json`, verifier agent
aaa9ca9e751d1f6fb); NO new solves. **Script:** `d2a_switch_criterion_interior.py` (CAS anchors +
dense-profile analysis, all four brackets). **Status: PROVISIONAL — not verifier-passed, not
committed.** Data-blind (no observational numbers touched).

---

## 1. The criterion's operational content (extracted, cited)

From `gp_switch_criterion_results.md`:

- Only 𝒦 = K_ABK^AB − K², K_AB = ½e^{−φ}∂_r h_AB, breaks the constant depth-shift φ→φ+λ
  (Result 1, :21-31).
- The moved invariant is the aspect ratio χ = L_radial/√(A/4π), L_radial = ∫e^φ dr; χ→e^λχ
  (Result 2, :33-38).
- **P iff (N1) √A pinned ∧ (N2) radial interval pinned ∧ (N3) 𝒦≠0**; blind-verifier refinement:
  N2 is diffeo-meaningful only via N3 ("r-dependent transverse geometry supplies physical anchors
  for the endpoints"), minimal content **N1∧N3** (Result 3, :40-58).
- P is a genuine **bulk** equation with local source −2𝒦 in the φ-EL (Result 4 Task 3, :67-69);
  bulk-P made UNCONDITIONAL by `native_geometric_action_results.md` (:117-121).
- Regime map: "G governs the bulk wherever χ is NOT a fixed observable"; "P governs the INTERIOR
  of a cell that pins χ … NOT the whole finite domain automatically — **only where χ is pinned
  and 𝒦≠0**"; "the cell wall / seal is where χ becomes pinned" (Result 5, :78-83).
- Branch G's equation form: (r²φ')' = 0, Coulomb
  (`native_field_equations_constrained_two_player_results.md`:107-110).

Reduced to the solved round-static slice (h_AB = ρ(r)²Ω_AB, CAS-verified in the script):

    𝒦 = −2 e^{−2φ} (ρ'/ρ)²          (≤ 0; zero iff ρ'=0)
    d/dr [Zρ²φ'] = 4e^{−2φ}ρ'² = −2ρ²𝒦     (the T3 φ-EOM, cell_solver_universe_T3.py:79)

So the E0 column `pi_phi_qflux` = Zρ²φ' is exactly the ACCUMULATED shift-breaking source, and
Q(r)/q is the fraction of the cell's φ-charge sourced inside radius r. **Corollary (algebra):**
in Branch G, (r²φ')'=0 plus core regularity forces φ'≡0 — a regular-cored G region is exactly
φ-flat. Every nonzero φ' anywhere in these interiors is therefore 100% P-sourced.

---

## 2. ADJUDICATION — is the criterion pointwise/regional or cell-global?

**Honest answer: it is a HYBRID, and the strict classification unit is the CELL.**

1. **The classified transformation is a GLOBAL constant shift.** φ→φ+λ with λ constant
   (Results 1-3 throughout). "Symmetry or redundancy?" for a constant shift is a property of a
   DOMAIN with its pinned observables, not of a point: one cannot restrict a constant shift to a
   sub-region without changing the transformation. N1 (√A pinned) and N2 (interval pinned) are
   domain-boundary conditions. **The criterion as derived classifies whole cells bounded by
   pinning data; it does not define a pointwise regime field "G(r) vs P(r)."** Asking "is the
   plateau G-governed?" in the strict shift-redundancy sense is category-mismatched as posed.

2. **But the criterion has a derived POINTWISE ingredient.** Task 3 (:67-69) establishes the
   breaking as a bulk density (φ-EL source −2𝒦), and Result 5's where-clause ("only where χ is
   pinned and 𝒦≠0", :81-82) is explicitly regional in 𝒦. So a REGIONAL reading is supportable in
   exactly this form: *given* a pinned cell, the P physics acts where 𝒦≠0, with local strength
   −2𝒦; where 𝒦=0 the branches coincide and the shift is locally inert.

3. **Sub-cells would need their own pinning surfaces — and the anchors exist everywhere 𝒦≠0.**
   Per the verifier refinement (:56-58), endpoint anchors are supplied by r-dependent transverse
   geometry. In all four fundamentals ρ is STRICTLY monotone on the open interior (E0 fold map:
   interior ρ'=0 zeros NONE at graduated floors to 1e-10; script: zero sign changes,
   ρ''(0)=σ(core)>0 so the fold zeros are isolated). So every ρ-level-set is a diffeo-invariant
   anchor surface, any sub-interval [ρ_a,ρ_b] is pinnable, and each such sub-cell has 𝒦≠0
   ⇒ **every anchorable sub-region classifies P.** The core/seal folds are the only TURNING
   surfaces, but not the only anchors; there is no interior surface where χ UN-pins (that would
   need 𝒦≡0 on an open interval, i.e. ρ'≡0 — excluded by the fold map).

4. **What the criterion CANNOT do (sharpening it would need):** it is BINARY. It has no derived
   notion of "approximately G" / "effectively G where the source is small." Any graded reading
   (e.g. an ε = local source fraction with a controlled G-limit) would be a NEW perturbative
   derivation, not this criterion. We do not force one.

---

## 3. The whole-cell classification (strict reading): ALL FOUR INTERIORS ARE P — one cell each

Per bracket: **N1** — √A pinned: ρ_c, ρ_s are turning values (diffeo-invariant scalars); ρ_c=1 is
the slice normalization (CHOSE, WLOG under the T3 homothety covariance) and ρ_s/ρ_c is DERIVED by
the seal root. The homothety freedom does NOT rescue the shift: under r→sr, ρ→sρ both L_radial
and √A scale by s, so χ is homothety-invariant while the shift still moves it (χ→e^λχ) — the
rigidity N1 carries survives family-wide (CAS note in script). **N2** — [0, r_s] pinned by the
two fold anchors (𝒦≠0 between them supplies the diffeo-invariant endpoints per :56-58). **N3** —
𝒦≠0 a.e.: min|ρ'| in the open interior 2.3e-14–8.9e-14 only AT the fold approach; zero
sign-changes; σ(core)>0 makes the fold zeros isolated. N1∧N2∧N3 hold ⇒ **Branch P, the entire
interior, every bracket.** No interior pinning surface exists to cut a sub-cell out, and no
interior interval un-pins χ. The plateau-is-G question, posed strictly, is answered: **there is
no G anywhere inside the solved universe cell; G exists only beyond the seal** (beyond-CMB,
PONDER-tag, banked).

χ per bracket (for the record; the criterion doc leaves the transverse surface for √A
unspecified when ρ varies — a convention gap, flagged, not load-bearing):
| bracket | L_radial | χ(ρ_c) | χ(ρ_s) |
|---|---|---|---|
| A1 m=3 Z=8 | 3.5637 | 3.5637 | 1.5759 |
| A1 m=3 Z=1 | 2.6164 | 2.6164 | 1.9212 |
| A3 Z=8 | 4.4839 | 4.4839 | 1.8520 |
| A3 Z=1 | 3.4337 | 3.4337 | 2.5379 |

---

## 4. The regional reading (defensible, Task-3 form): P everywhere, but SEAL-CONCENTRATED

The local breaking density |𝒦| and the accumulated source Q(r)/q (x = r/r_s):

| bracket | \|𝒦\| st1 (x≈0.17) | \|𝒦\| max (at x) | max/plateau | Q/q at x=0.5 | x at Q/q=50% | x at 99% |
|---|---|---|---|---|---|---|
| A1 m=3 Z=8 | 5.3e-06 | 0.708 (0.9939) | 1.3e+05 | 7.5e-04 | 0.9935 | 0.9987 |
| A1 m=3 Z=1 | 5.8e-07 | 0.183 (0.9981) | 3.2e+05 | 7.4e-04 | 0.9968 | 0.9996 |
| A3 Z=8 | 3.4e-06 | 0.473 (0.9942) | 1.4e+05 | 6.9e-04 | 0.9939 | 0.9989 |
| A3 Z=1 | 3.7e-07 | 0.096 (0.9979) | 2.6e+05 | 8.2e-04 | 0.9964 | 0.9995 |

Family-universal layout: the inner HALF of the cell sources <0.1% of the φ-charge; 99% of q is
sourced in the last ~0.04–0.14% of the radius (VERIFIER-CORRECTED from '~0.1–0.4%' — the doc's own table 1−x99 = 0.0004–0.0014; the result is ~3x STRONGER than the original prose); the breaking density spans 5–6 decades between
plateau and wall. **So the honest regional statement is: one P cell whose P-source support is a
thin seal-wall shell; the plateau is weak-P (quantitatively near-Coulomb), not G.**

**Why the plateau LOOKS G-shaped, and why that is not G-governance:** a regular-cored G region
would be exactly φ-flat (φ'≡0, Sec. 1 corollary). The plateau's φ' is small (≤1.2e-3 at x≤0.5)
but nonzero — and the flux identity shows it is 100% accumulated P-source (Q reconstruction
matches the extracted flux column to ≤1.1e-3 rel on the dense grid). Near-flatness is what a
weakly-sourced P region with the Coulomb mode killed by core regularity looks like. The MAP's
suspicion "χ not locally pinned" in the plateau fails on the derivation's own anchor rule:
ρ is strictly monotone there, so anchors exist and sub-regions pin.

---

## 5. Consequence for the architecture table (D2 MAP)

Under BOTH defensible readings the answer to Q1 is the MAP's flagged first-class outcome: **the
whole interior is P.**

- **A1 (P-particle in G-governed ambient region): the Q1 premise is FALSE for the solved
  interior.** There is no G-governed region inside the universe cell to host a G|P weight-jump
  seal. A1 as an *embedded-particle* architecture is killed cleanly. (Scope honesty: the G|P
  JC1/JC2 machinery itself is untouched — its natural home is the universe's OWN seal / the
  beyond-CMB exterior, not an interior particle wall. If any architecture ever places a cell
  at/outside the seal, A1's machinery revives there. Flag for the ponder, not a recommendation.)
- **A0 (P-pocket in P-ambient): the MEDIUM CATEGORY is vindicated** — E2's composite put its seal
  in a medium that is natively P, the right medium after all. This says nothing about A0's
  P|P-continuity CHOSE or its optimizer-gated existence question (E2c/D3, unchanged).
- **A2 (P-core | G-layer | P-universe): NO SUPPORT.** An interior G-layer would require an open
  interval with χ un-pinned, i.e. ρ'≡0 (𝒦≡0) on that interval — excluded by the blind-verified
  fold map (no interior turning points, all four brackets). The nested-alternation reading has no
  purchase inside a fundamental.
- **Refinement the regional reading ADDS for the ponder:** the P-ambient is not uniform — it is a
  5–6-decade weak-P plateau walled by a thin strong-P shell holding >99% of the source. Where a
  particle pocket sits in THAT structure (deep plateau vs wall vicinity) is a real, now
  quantified, dimension of the A0 problem that the E2 composite's uniform-ambient picture did not
  see.

---

## 6. Premise ledger (chose or derived) — everything used

| item | tag |
|---|---|
| Criterion N1∧N2∧N3 (minimal N1∧N3); χ; bulk-P source −2𝒦 | DERIVED (gp_switch doc, blind-verified; bulk-P unconditional per native_geometric_action) |
| 𝒦 = −2e^{−2φ}(ρ'/ρ)² on the round slice; flux identity d(Zρ²φ')/dr = −2ρ²𝒦 | DERIVED (CAS in script, from the banked T3 EOM) |
| G-branch form (r²φ')'=0; regular core ⇒ φ'≡0 | DERIVED (field-eq doc :110 + elementary algebra) |
| E0 profiles, fold map (no interior turning points), gates | EXTRACTED (blind-verified E0 tables; all inherited provenance tags apply) |
| ρ_c = 1 | CHOSE (slice normalization, WLOG under homothety; χ-rigidity shown homothety-invariant, so not load-bearing for the verdict) |
| √A-surface convention for χ (ρ_c vs ρ_s) | CHOSE (criterion doc leaves it unspecified for varying ρ; both reported; not load-bearing) |
| "plateau" = x≤0.5; stations = even sixths; percentile levels {1,10,50,90,99}% | CHOSE (reporting conventions, Category-A) |
| Q-reconstruction trapezoid on the dense grid | Category-A numerics (cross-check only; ≤1.1e-3 rel vs the exact solver flux column) |
| Adjudication "criterion = hybrid; strict unit = cell; regional via Task-3 𝒦-density + ρ-level-set anchors" | DERIVED-from-cited-lines (Sec. 2 cites); the BINARY-no-graded-G limitation stated honestly |
| Any "effectively-G plateau" notion | NOT USED — would need a NEW perturbative sharpening (named in Sec. 2.4) |
| Beyond-CMB is natively G | PONDER-tag (banked, underived) — used only for scoping remarks, not the verdict |

**Forks encountered not covered by the MAP: none that block.** The one interpretive fork (strict
cell-global vs Task-3 regional) is resolved by carrying BOTH readings to the same Q1 verdict; the
χ-surface convention gap is flagged as a sharpening item for the criterion doc, not a blocker.

**Status: PROVISIONAL until verifier-before-record.** Suggested attack surface for the blind
verifier: (a) re-derive the flux identity independently; (b) attack the "anchors exist everywhere
ρ'≠0" step (is a ρ-level-set a legitimate N2 pin under the criterion's own wording?); (c) attempt
to construct an interior sub-region where the shift IS absorbable despite pinned parent-cell data;
(d) recompute the percentile table from the JSON independently.

---
## VERIFIER RECORD (blind adversarial pass — agent a9cfb0141acd701ee, 2026-07-04): ALL ATTACKS HOLD
Own algebra chain 64/64 from the source-doc action forms; every table entry independently
reproduced from the E0 JSON (own integration). The ρ-level-set-as-N2-pin extension adjudicated
LEGITIMATE (diffeo-invariant surfaces; the shift moves L_radial between them; the only undoing
move changes observable areas) — and nothing rides on it: both readings give the same all-P
verdict. The one correction (the 99%-sourcing prose, ~3x stronger) applied inline above.
A1/A2 kill scoping confirmed under both readings; JC1/JC2-untouched caveat correct. SAFE TO BANK.
