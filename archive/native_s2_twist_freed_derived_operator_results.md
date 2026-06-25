# Native S² Matter with the Radial Twist FREED — the Decisive Particle-vs-Defect Solve (DEFECT survives; φ-hair structurally caps the core)

**Mode:** OBSERVE, METRIC-LED, DATA-BLIND, EMERGENCE-LED. **NOT canon. UNVERIFIED** (no blind
verifier pass yet — record-candidate). **Driver:** Claude Opus 4.8 (1M), agent for udt_mass_codex.
**Date:** 2026-06-21. **Compute:** sympy 1.13.1 (CPU) for all EL/stress; bounded torch float64
(GPU) for the relaxation/BVP, single foreground process, N=24/400, capped iters. Nothing committed
to git; scripts in /tmp (`derive_twist.py`, `derive_g_el.py`, `derive_gravity.py`, `twist_solve.py`,
`phi_eom_sign.py` + independent EL re-derivation).

Builds on / decides the OPEN item of: `native_s2_object_derived_operator_results.md` (the rigid slice
+ its verifier revision R1 — "the rigid reading FROZE a legitimate native radial-twist DOF; its defect
verdict is SLICE-scoped"), `matter_regrade_derived_operator_results.md` (the derived scalar-tensor
operator E_munu, a(phi)=e^{phi}, e^{2phi} matter weight), `free_s2_matter.py` (the target-agnostic
S² machinery), `whole_metric_3d_matter.py` (MAT stress).

---

## 0. THE QUESTION (lay)

The rigid reading of UDT's native matter (the S² winding) said: a structureless **defect**, no body,
no size, core blows up. A blind verifier then caught that the rigid reading had **frozen** a legitimate
native freedom — a "radial twist" `g(r)` that rotates the winding's phase as you move outward, staying
exactly on the sphere (NOT the forbidden 4th-component escape). The open question: **once that frozen
twist is freed, does the native matter develop a real body (a particle), or does the twist go limp and
leave the defect intact?** Plus: with the metric's own scalar field (φ) now live, does its "hair" cap
the runaway core? This solve frees the twist + φ on the derived operator and **observes what happens.**

---

## 1. THE SOLVE (what was set up)

- **Field (on S², 3-vector, |n|²=1 exactly):** `n = (sinθ cos(mψ+g(r)), sinθ sin(mψ+g(r)), cosθ)`,
  m=1 — the degree-1 winding with a **radial twist** g(r) (the `field_n_freeaz` family of
  `free_s2_matter.py`, restricted to a purely-radial phase). This stays on S² (NO S³ escape). [The
  full 2-angle field Θ_t(r,θ) is the next stage — see HONEST STATUS; the twist is the DOF the verifier
  named as decisive.]
- **Unknowns:** A(r), B(r), φ(r), g(r) — four radial fields, **B=1/A FREE.**
- **Operator (derived, `matter_regrade`):**
  `E_munu = f G_munu + (g_munu □ − ∇_μ∇_ν)f − X f(∂_μφ ∂_νφ − ½ g_munu (∂φ)²)`, `f=e^{2φ}`,
  matter weight `S_m = ∫√−g e^{2φ}L_m`. X=−2e5, kap8=1, ξ=κ=2e-2.
- **Native matter stress (sympy-derived, `derive_twist.py`)** for the twisted field:
  ```
  L_m = [ −κm²e^{2B} − (κr² + r⁴ξ) sin²θ g'²  − r²ξ(m²+1)e^{2B} ] e^{−2B} / (2r⁴)
  T^t_t = [ −κm² − r²ξ(m²+1) − (κ/r² + ξ) r² sin²θ g'² e^{2B}·... ] ...   (rigid part + twist)
  T^t_t − T^r_r = +(κ + r²ξ) e^{−2B} sin²θ g'² / r²            ← the B=1/A break, ∝ g'²
  T^r_ψ = m(κ + r²ξ) e^{−2B} sin²θ g' / r²                      ← momentum flux, ∝ g'
  ρ_extra(twist) = +(κ + r²ξ) e^{−2B} sin²θ g'² / (2r²)  ≥ 0     ← twist STRICTLY ADDS energy
  ```
  So a live twist DOES (in principle) break B=1/A, carries momentum flux, and adds energy — exactly
  the structure the verifier predicted. The decisive question is whether the action **prefers** g'≠0.
- **Native BCs (EMERGENCE-LED, anti-import):** core-removed inner edge r_core=0.1, seal/mirror outer
  edge R=8 (canon D3/A1), with g **natural/free** at both ends (NO imposed twist, NO Dirichlet winding
  — imposing one would be the import). φ regular; seal BC φ(R)→0.

---

## 2. THE CRUX — the g(r) EL is a PURE CONSERVATION LAW; the twist RELAXES TO TRIVIAL [DERIVED + numeric, two independent routes]

`g` enters the sphere-integrated action **only through g'** (an exact shift symmetry g→g+const —
machine-confirmed `∂L/∂g = 0` exactly, two independent sympy derivations). Therefore the g-EL is a
**pure conservation law with no restoring potential**:
```
P(r) = −(8π/3)(κ + r²ξ) e^{A−B+2φ} g'(r) = const = C ,      and  d/dr P = 0 is the entire g-EOM.
```
- **C is fixed by the boundary flux.** Native finite-cell BCs (g free/natural at core and seal — no
  externally imposed twist) give **zero flux ⇒ C=0 ⇒ g'=0 everywhere ⇒ g=const = TRIVIAL.**
- **Unbiased numeric confirmation** (`twist_solve.py`): seeded a nontrivial twist (amplitude 0.8,
  sin-bump) and relaxed the action with **free endpoints**. Twist energy collapsed
  **9.95e-2 → 2.0e-10** (six orders), g→const (max|g'|→1.4e-4). The twist is a Goldstone-flat
  direction; with no charge and no potential, free relaxation kills it.
- **The twist is a pure COST.** ρ_extra ∝ +g'² ≥ 0: any twist strictly *adds* energy and buys
  nothing (no topological charge, no potential well to settle into). Imposing a Δg=π twist by hand
  (Dirichlet) costs positive energy (7.2e-7 here) — an *imported* external winding, not a native
  preference.

> **VERDICT (calibrated, emergence-led): the native radial twist RELAXES TO TRIVIAL.** It does not
> develop on its own. Consequently **B=1/A is NOT broken by matter kinetics** (the break ∝ g'² → 0),
> **no momentum flux develops** (T^r_ψ ∝ g' → 0), and **no localized body / ρ-peak appears from the
> twist.** Freeing the verifier's decisive frozen DOF **leaves the rigid defect intact.** UDT's
> native (static, round) S² matter object is a **DEFECT, not a particle** — the rigid verdict
> SURVIVES the freeing. This is a clean, important NEGATIVE.

---

## 3. THE CORE — φ-hair has the CAPPING SIGN and structurally regulates, but is ~1/|X| WEAK at the canonical operator [DERIVED + BVP]

With the twist trivial, the matter reduces to the rigid winding PLUS the now-live φ-hair. Two findings:

- **Sign of the hair is the GOOD one (q>0), DERIVED not chosen** (`phi_eom_sign.py`, the φ field
  EQUATION solved as a radial BVP, natural core / φ(R)=0): the winding source (L_m<0) on the
  scalar-tensor operator drives **q>0**, i.e. `e^{2φ} = e^{−2q/r} → 0` at the core. The essential
  zero **beats the 1/r⁴ power pole**: the proper-measure energy density
  `~(κ/2) e^{B} r^{−2} e^{−2q/r} → 0` as r→0, so the core energy is **formally FINITE without
  excision** (analytic core tail at r=0.001: integrand 2.6e-257 at q=0.3 vs 1.0e4 at q=0). This
  CORRECTS the rigid slice's "log-divergent, excision-only" reading: the hair-cap candidate (R2) is
  REAL and has the right sign.
- **BUT the magnitude is ~1/|X| and the canonical X=−2e5 makes it negligible.** The derived hair
  charge scales `q ∝ 1/|X|`: q ≈ 1.3e-6 at X=−2e5 (1.3e-4 at X=−2e3, 1.3e-8 at X=−2e7). At
  q≈1.3e-6 and r_core=0.1, `e^{2φ}(r_core) ≈ 1.0000` — the cap, though structurally present, fires
  only at *exponentially small radii* and provides **no practical regulation at the canonical inner
  edge.** So at the derived operator's X, **finite-cell excision remains the operative core
  regulator**; the hair-cap is a true but asymptotically-weak structural feature, not a working cap.

> **CORE VERDICT:** the φ-hair caps the core *in principle* (correct sign q>0, essential zero beats
> the pole — finite energy as r→0), **overturning "excision is the ONLY native regulator."** But at
> the canonical X=−2e5 the hair is ~1/|X|-weak, so in practice finite-cell excision is still doing the
> regulating at r_core=0.1. The cap would become operative only at much smaller |X| (or much smaller
> r_core). **Honest: structurally regulated, practically still excised.**

---

## 4. B=1/A — confirmed: break is ONLY the tiny ~1/|X| φ-hair, NOT matter [DERIVED, machine-checked]

With the twist off (the native solution), `E^t_t − E^r_r` at φ=const reduces **exactly** to
`−2r(A'+B')`, which **vanishes under B=1/A** (machine-confirmed, `derive_gravity.py`). The only break
is the φ-hair terms (`X r φ'² + 4r φ'² + 2r φ'' − …`), suppressed by q∼1/|X|. So **B=1/A holds to
~1/|X|**, broken only by the scalar hair, **never by matter kinetics** (the twist that would have
broken it relaxed to zero). This matches and tightens the rigid slice's revision exactly.

---

## 5. HONEST STATUS — what is SOLVED vs DEFERRED

**SOLVED (this push):**
- The twisted-field native stress, L_m, and the g-EL — exactly (sympy, two routes).
- The decisive observation: the radial twist relaxes to trivial under native finite-cell BCs (g-EL =
  pure conservation law; unbiased relaxation; energetics all-cost). ⇒ DEFECT survives.
- The φ-hair sign (q>0, capping) DERIVED from the field equation; its 1/|X| magnitude.
- B=1/A break is hair-only, ∼1/|X|.

**DEFERRED (later stages, per scope — NOT a verdict on them):**
- **The full 2-angle on-S² field** Θ_t(r,θ) free (the polar target angle r,θ-dependent). The twist
  g(r) is the verifier's *named* decisive DOF and it's now settled; Θ_t(r,θ) is a richer deformation
  the twist result does not pre-judge. This is the honest remaining "is there ANY on-S² radial
  structure" question.
- **Off-round** (non-axisymmetric) and **time-live** (∂_t Θ ≠ 0) configurations — the
  static+round scope is explicit here; the orchestra (Principle 5) is not ruled out by this solo.
- **Full nonlinear coupled (A,B,φ,g) Newton solve** with everything live simultaneously — the g-EL
  conservation result makes this redundant for the twist (g→0 decouples it), but the φ-hair magnitude
  was read on a frozen mild metric + leading-order f; full self-consistency sharpens the number, not
  the sign.

---

## 6. PREMISE LEDGER (chose / derived)

| # | item | status |
|---|---|---|
| 1 | native L2 + cross-product L4, S² 3-vector winding | DERIVED (CANON C-2026-06-14-1) |
| 2 | radial twist ansatz `n` with ψ→ψ+g(r) (on S², no S³ escape) | CHOSE the FORM (the verifier-named DOF); |n|²=1 exact — DERIVED on-S² |
| 3 | derived scalar-tensor operator E_munu, weight e^{2φ}, X=−2e5, kap8=1, ξ=κ=2e-2 | DERIVED upstream (matter_regrade) / CHOSE healthy values |
| 4 | **native finite-cell BCs: g free/natural (no imposed twist), r_core=0.1, R=8** | **CHOSE — and this is the EMERGENCE-LED choice; imposing a twist would be the import. The g-EL conservation makes C=0 the unique native (flux-free) value** |
| 5 | g-EL = pure conservation law (∂L/∂g=0, shift symmetry) | DERIVED (two independent sympy routes) |
| 6 | twist relaxes to trivial under native BCs | DERIVED (C=0) + numeric (unbiased relaxation 1e-1→1e-10) |
| 7 | φ-hair sign q>0 (capping) | DERIVED (φ-BVP); magnitude q∼1/|X| (frozen-metric, leading-f — FLAG: full SC sharpens magnitude) |
| 8 | static, round | CHOSE (scope; 2-angle/off-round/time-live deferred) |

---

## 7. ATTACK HERE (for the blind verifier — required before banking)

1. **The g-EL conservation claim (central).** Re-derive ∂L/∂g and P(r) independently; confirm
   ∂L/∂g=0 (shift symmetry) and that the g-EOM is purely `d/dr[(κ+r²ξ)e^{A−B+2φ}g']=0`. Confirm the
   ONLY native (flux-free) solution is g=const. Hunt for any NATIVE boundary condition (not an
   imported external winding) that would force C≠0 — the claim is none exists for a phase DOF carrying
   no topological charge. **If a native C≠0 BC exists, the verdict flips to particle — attack here
   hardest.**
2. **Is g truly chargeless?** Confirm g is a phase shift on the *same* degree-1 map (π₂ class
   unchanged), so there is no winding quantization in g. (Contrast: the *azimuthal* winding mψ IS
   charged; g is the residual phase, which is not.)
3. **The twist energetics.** Confirm ρ_extra ∝ +g'² ≥ 0 (twist is all-cost) and that the unbiased
   relaxation genuinely had free endpoints (not a hidden Dirichlet pin biasing toward g=0).
4. **The hair sign + magnitude.** Re-solve the φ-BVP; confirm q>0 (capping) and q∼1/|X|. Check
   whether full self-consistency (f=e^{2φ} live, not f≈1) changes the magnitude enough to make the cap
   operative at r_core=0.1 — the leading-order read says no, but a coupled solve is the clean test.
5. **The deferred 2-angle field.** Flag that Θ_t(r,θ)-free is NOT settled by this twist result; a
   verifier should confirm the scope claim and not over-read "DEFECT" onto the full free S² field.

---

## 8. SINGLE CLEANEST STATEMENT

Freed of the rigid slice, UDT's native S² matter has exactly one new static-round on-S² radial DOF the
verifier named — the radial twist g(r). Its EL is a **pure conservation law** (exact shift symmetry,
no potential), so under native finite-cell BCs the twist **relaxes to trivial** (C=0; unbiased
relaxation 1e-1→1e-10), adding only positive energy and buying nothing. **The twist does not develop;
no body, no size, no momentum flux, no matter-kinetic B=1/A break appears — the rigid DEFECT verdict
SURVIVES the freeing.** The one genuine correction is the core: the now-live φ-hair has the **capping
sign (q>0, DERIVED from the field equation)** and structurally renders the core energy finite without
excision (essential zero beats the 1/r⁴ pole), **overturning "excision-only"** — but at the canonical
X=−2e5 the hair is ∼1/|X|-weak, so excision remains the *practical* regulator. **Static-round verdict:
DEFECT, not a particle, with a structurally-self-regulating (practically-excised) core.** Deferred and
NOT pre-judged: the full 2-angle on-S² field, off-round, and time-live — the orchestra is not ruled
out by this solo. **NOT canon; OBSERVE + bounded; UNVERIFIED.**

---

## VERIFICATION (2026-06-21) — blind adversarial pass, agent acb573f6c8c0aa96e — SUPPORTED
Independent sympy + bounded BVP (data-blind). All six attack lines reproduced:
- **B1 shift symmetry/conservation:** CONFIRMED. ∂L/∂g=0 exactly for L2 AND L4 (g via g' only; no potential);
  P(r)=−(8π/3)(κ+r²ξ)e^{A−B+2φ}g' matched to zero.
- **B2 DECISIVE BC hunt:** CONFIRMED — NO native BC forces C≠0. EOM d/dr[Wg']=0, W>0, E∝C²/(2W) minimized at C=0;
  every native finite-cell BC (free/natural, mirror-even, mirror-odd, contractible-interval/π₁-trivial, seal
  couples to the H1 m-winding not the residual phase g) forces C=0. A C≠0 state requires an EXTERNALLY IMPOSED
  Dirichlet Δg = an import. **The DEFECT verdict is NOT a smuggled slice.**
- **B3 numeric:** CONFIRMED (free BC -> g=const, E=0; imposed Δg=π holds C=0.391, E>0, does not relax).
- **B4 core cap sign:** CONFIRMED — q>0 DERIVED (L_m<0, X<0 => 2L_m/X>0); e^{−2q/r} kills any pole; q∼1/|X| weak.
- **B5 orchestra scope:** CONFIRMED solo-bounded.
- **B6 data-blind:** CONFIRMED.
**OVERALL: SUPPORTED.** 
**KEY ENHANCEMENT (verifier, records the ensemble's first instrument):** the cross term
`∂_r n · ∂_ψ n = m·sin²θ·g'` is NONZERO but enters the action only through g^{rψ} — which is 0 in the
diagonal round metric, so the twist is a flat Goldstone HERE. In an OFF-ROUND / off-diagonal-shear metric
(g_rψ≠0) this term is LINEAR in g' — a genuine SOURCE that could force g'≠0 (a nontrivial twist -> potentially
a body). **So the native matter twist comes alive precisely in the off-round shear sector — the same sector as
the derived phi-angular obstruction and the Stage-1 shear-capable engine. That off-round twist+shear coupling
is the ENSEMBLE's concrete first target.**
