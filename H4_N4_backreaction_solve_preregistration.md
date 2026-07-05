# H4 · N4 — Backreaction / mass / pinning solve: PRE-REGISTRATION (frozen BEFORE compute, under frame C(a))

**Mode:** pre-registration / frozen falsification contract. NO compute yet (armchair). Charles-authorized
2026-07-06 (N3 ruling below).

**VERIFIER RECORD — blind adversarial verifier ac1c5b1af227688b5 (2026-07-06): SOUND in frame, NO FAIL on any of
8 targets.** Confirmed (incl. an independent sympy re-check of √h𝒦 = −½e^{−2φ}(a'b'−s'²)/√h, bilinear-in-velocities
⇒ finite-amplitude): second-order necessity correctly enforced (outcome B gated to O(amp²)-and-beyond; linear
artifact forbidden); the frozen-H3-source approximation is valid at leading order (field response enters δq only
at O(ε³), one order below); all four outcomes genuinely open (C negative-mass has real teeth via phase1_geon,
"positive energy ⇒ positive mass" explicitly refuted — NOT pre-decided); frame C(a) honored (no sealed-cell); no
GR import; box-control → D. **Four method-completeness revisions APPLIED** (none touch a decision or open fork):
(T1) explicit O(amp²) bookkeeping in Step 2 [keep both (δh^(1))² and δh^(2)]; (T2) the O(ε³) fixed-source
justification + non-small-ε fallback must re-solve δn, in Step 1; (T4) a resolution floor on dE/dr_hopf to
separate a genuine "float" from a below-resolution force (D), in Step 4; (T7) quantify interior-ℓ≥2 smallness
relative to the O(amp²) δq + the ℓ≥2→ℓ=0 back-projection check, in Step 5. Verifier-flagged CF3 as the
throughput-limited-risk deliverable (subleading pinning force; H3's ~1% precision could swamp it) — recorded.
**The pre-registration is now blind-verified; the N4 SOLVE remains gated behind Charles's explicit go for compute.** Builds on the
blind-verified N1 (`H4_N1_offround_transverse_equation_results.md`) and N2 (`H4_N2_farfield_reduction_results.md`)
and the frame `H4_backreaction_mass_MAP.md`. DATA-BLIND: no particle labels, no masses, no observational data,
no GR minimal-coupling (G=8πT FORBIDDEN as a source law; GR only as far-field reference, lane #2).

## N3 RULING (Charles, 2026-07-06) — the frame N4 is frozen under
- **Frame C(a) CONFIRMED.** The hopfion is a localized perturbation on the selected N=0 bulk. Mass is read on a
  Gaussian/read-surface satisfying **ℓ_hopf ≪ r ≪ r_fold**. **NO private seal, NO particle-owned boundary, NO G|P
  mini-cell** unless later FORCED by derivation.
- **Mass reading:** use the native far-field φ-monopole / flux reading from N2; **report BOTH** the geometric mass
  and the flux/charge mass, noting they coincide at leading order up to Z_φ; **keep Z_φ the open normalization
  fork**; **keep CF1 OPEN** — net flux may still be zero or negative until the N4 solve.

## The question (frozen)
On the numerically-resolved Q_H=1 hopfion (H3 = outcome A), does the backreaction — its stress deforming the
transverse geometry h_AB, hence the curvature 𝒦, hence sourcing φ (Branch-P −2𝒦 channel, N1) — produce:
1. a NONZERO net far-field monopole δq (a mass)? [CF1] — and of what SIGN [CF2, +mass vs −mass]?
2. a self-φ-well that PINS the hopfion (a restoring force → localized particle) or leaves it FLOATING (bulk) or
   runs it to the core/fold (core-pinned, re-opens H1's premise)? [CF3, the bulk-vs-core verdict]
3. consistency of the ledgered form (φ=φ(r) longitudinal, block-diagonal, no shift) with a genuinely toroidal
   source — or does the source force interior angular-φ / radial-shift beyond scope? [FORM-break check]

## What N1+N2 already fixed (frozen inputs, do NOT re-derive)
- **Backreaction channel (N1):** matter is φ-blind (δS_m/δφ=0); reaches φ ONLY via n→h_AB→𝒦→φ; Branch-P source
  ∂_r(√h Z_φ φ') = −2√h 𝒦, with 𝒦 = −2 det(K^A_B), K_AB = ½e^{−φ}∂_r h_AB. Transverse equation E^{AB} = −T^{AB}
  (R^(2) contributes zero local stress; π^{AB} = the JC2 momentum). Survives off-round (CF5 does not trip).
- **Far-field reduction (N2):** the mass is a pure MONOPOLE in φ, δφ = −δq/r (1/r native from ρ=r area growth);
  multipoles live in the transverse SHEAR δh_AB (no ℓ(ℓ+1) tower — a native GR-departure). Read-surface reads
  δm = δM = −δq at O(1/r) (geometric = Coulomb; sub-leading −q²/r is the native nonlinear departure), conserved
  flux δQ_φ = 4πZ_φ δq. **The read-surface value is radius-INDEPENDENT** (flux conservation) — so a
  read-surface-radius dependence in the solve would signal box-control (a numerical failure, not physics).
- **CF1 is intrinsically FINITE-AMPLITUDE (N2):** at linear order the shape source δ(√h𝒦) is an exact total
  r-derivative (integrates to 0 over compact support); the net δq is **O(amplitude²)**. ⇒ N4 must compute the
  backreaction to SECOND order in the perturbation amplitude (or finite-amplitude directly) — a first-order/linear
  solve returns δq=0 spuriously and must NOT be reported as CF1.

## Frozen method (the solve design — falsification contract)
**Inputs:** the resolved H3 hopfion field n(x) (blind-verified outcome A; its ~1% precision caveats are
NON-GATING here — they do not affect the sign of the backreaction) and its transverse stress
T^{AB} = (2/√h) δS_m/δh_AB, computed from the resolved field on the ρ=r Euclidean slice. Do NOT re-solve the
hopfion (anti-hang: reuse the saved H3 field).

**Step 1 — transverse response.** Solve E^{AB} = −T^{AB} (N1) for the geometry deformation δh_AB sourced by the
fixed hopfion stress, as a bounded perturbation on the N=0 round ambient (h_amb = r²Ω, φ_amb from the Branch-P
cell). Solve for the linear response δh^(1) (~O(ε)) AND the second-order δh^(2) (~O(ε²)). Check the perturbative
smallness parameter ε ≡ (hopfion stress / ambient curvature scale). **Fixed-source justification (verifier T2,
record it):** matter is φ-blind, so the hopfion field n responds only to δh (not δφ); the field response is
δn ~ O(ε), and its back-effect on T feeds δh at O(ε²), entering the *bilinear* δq (below) only at **O(ε³)** — one
order below the leading O(ε²) δq. So the frozen H3 field is a valid fixed source for the leading CF1 sign+magnitude
**provided ε is small** (the Step-1 check). **If ε is NOT small,** the fixed-source approximation is invalid: fall
back to a bounded coupled relaxation that **re-solves (or bounds) the field response δn** as well (anti-hang
limits), or report outcome D.
**Step 2 — φ-source and flux (O(amp²) bookkeeping, verifier T1).** Form δ𝒦 = −2 δ(det K^A_B)[δh_AB] and **expand
√h 𝒦 to O(amp²), retaining BOTH the bilinear (δh^(1))² term (the dominant shear contribution — N2: the linear
shape-piece is a total r-derivative that integrates to zero, so the leading net flux is this bilinear) AND the
genuine second-order δh^(2) contribution.** A computation that keeps only linear δh returns δq=0 spuriously and is
FORBIDDEN (the LINEAR-ORDER ARTIFACT clean failure). Integrate the net flux δq = −(1/2πZ_φ)∫ δ(√h 𝒦) d³x
(equivalently solve the monopole ODE d/dr[Z_φ δφ' A]=−2∫√h δ𝒦 d²x and read the 1/r coefficient). This is the CF1
quantity.
**Step 3 — read the masses.** δm = −δq (geometric = Coulomb, N2); flux δQ_φ = 4πZ_φ δq. Report BOTH; keep Z_φ
symbolic. Confirm read-surface-radius independence (else box-control). Sign of δm = CF2.
**Step 4 — pinning force (CF3; SUBLEADING — the throughput-limited-risk deliverable).** Compute the total energy
E_tot(r_hopf) = hopfion energy + backreaction (self-φ-well) energy as a function of the hopfion's radial position
r_hopf in the cell. The hopfion couples to the ambient transverse geometry h_amb (it is NOT blind to h_amb — only
to φ), and the sourced δφ-well sits in the φ_amb(r_hopf) gradient — so the force is NOT identically zero by
φ-blindness. **BUT (verifier T4, load-bearing): in the clean-bulk C(a) limit ℓ_hopf ≪ r_hopf the hopfion sits in a
locally-flat patch, so its LEADING energy is position-INDEPENDENT; the entire pinning force is SUBLEADING**
(O((ℓ_hopf/r)²) ambient curvature + the φ_amb gradient acting on an O(ε²) well). The force is
−dE_tot/dr_hopf: FLAT ⇒ floats (bulk); a MINIMUM ⇒ self-traps (pinned at that r); monotone-inward ⇒ runs to
core/fold (re-opens H1). Use unbiased evaluation at ≥3 positions (never a biased blend toward a chosen endpoint —
the ANTI-HANG stability rule). **Require a RESOLUTION FLOOR: quantify the numerical noise on dE_tot/dr_hopf (from
the H3 field's ~1% precision and the grid) and declare "float"/CF3-bulk ONLY if |dE/dr_hopf| is resolved to be
below a genuine-force threshold; a below-resolution force is outcome D (tool-limited), NOT a physics "float".**
**Step 5 — FORM-break check (N1/N2 scope; verifier T7).** Verify the interior φ-angular ℓ≥2 excitation is small
(or allow φ=φ(r,x)); check whether the toroidal source forces a radial shift g_{rA}≠0. **Quantify "small"
RELATIVE TO the O(amp²) δq it could contaminate** (not merely far-field decay), AND **check the second-order
ℓ≥2 × ℓ≥2 → ℓ=0 back-projection** of any dropped interior angular-φ onto the monopole δq being measured (a dropped
ℓ≥2 φ can feed the ℓ=0 flux at O(amp²)). If the ledgered form breaks or the back-projection is non-negligible, N4
is SCOPED to the perturbative regime and the form-extension is flagged for a later node — do NOT silently inherit
form-generality.

**ANTI-HANG (binding):** reuse the saved H3 field (no hopfion re-solve); bound the grid (Nr ≤ 16–24 for any
coupled step) and iterations; ONE clean foreground process at a time; NEVER background-poll a solve; the
perturbative/finite-amplitude response is the cheap path — prefer it; a bounded honest partial beats a hang. The
pinning test uses unbiased kicks + persistence (never a field blended toward a chosen endpoint).

## Frozen outcomes
- **A — definite localized massive particle:** δq ≠ 0, δm > 0 (positive mass), read-surface-independent, and the
  self-well gives a restoring force (floats or self-traps but does not run away). ⇒ the hopfion gravitates as a
  positive-mass localized object; H4's core question answered.
- **B — massless / inert:** δq = 0 (CF1 trips) at second order and beyond ⇒ the hopfion carries no far-field mass;
  redirect (is the mass a different native invariant? does an ensemble differ?). SCOPED, not a metric verdict.
- **C — negative mass:** δm < 0 (CF2). Pre-registered PRIME RISK (the phase1_geon single bare mode gave
  m/A² ≈ −0.905). A negative result indicts the SINGLE-OBJECT frame FIRST (ensemble? the L4 term's role?), the
  solver second, the metric last — NEVER a mechanism.
- **D — tool-limited:** box-control (read-surface-radius dependence), non-convergence, or the FORM-break making
  the perturbative solve invalid without a coupled solve that exceeds budget. Not a physics verdict.

## Clean failures (pre-registered, frozen)
- CF1 (δq=0 exact) — allowed OUTPUT (outcome B); must be computed at O(amp²), not linear.
- CF2 (δq<0, negative mass) — outcome C; prime risk; indict single-object frame first.
- CF3 (no restoring force / runaway) — float = bulk verdict (scoped); runaway = core-pinned (re-opens H1).
- FORM-break (toroidal source forces interior angular-φ or radial shift beyond the ledgered form) — scope N4 to
  perturbative, flag the extension; do NOT report a form-general verdict.
- BOX-CONTROL (mass depends on read-surface radius) — outcome D; N2 proved the flux is radius-independent, so any
  dependence is numerical.
- LINEAR-ORDER ARTIFACT (reporting the spurious linear δq=0 as CF1) — forbidden; second order mandatory.
- GR-IMPORT tripwire (mass read from G=8πT or Schwarzschild adopted as source) — STOP; native flux only.

## Premise ledger (chose / derived / theory / habit)
| Premise | Tag |
|---|---|
| Frame C(a) (read-surface in bulk, no private seal) | **CHOSE — Charles-RULED (N3)** |
| Resolved H3 hopfion field as the fixed source | DERIVED (H3 outcome A, blind-verified); ~1% caveats NON-GATING |
| Backreaction channel −2𝒦, transverse eq E^{AB}=−T^{AB} | DERIVED (N1, blind-verified) |
| Monopole-in-φ / mass=δm=−δq up to Z_φ / radius-independent | DERIVED (N2, blind-verified) |
| Second-order (finite-amplitude) computation of δq | DERIVED-necessity (N2) — method requirement, category-A |
| Z_φ value | **FREE / OPEN FORK** (Route A free / Route B=8) — kept symbolic |
| ρ=r reduction, φ-blind matter | DERIVED (conditional on R1+P5 CHOSE, per N1) |
| Ledgered metric FORM (φ longitudinal, block-diagonal, no shift) | **CHOSE** — audited in Step 5 (FORM-break check) |
| Perturbative smallness | to be CHECKED in Step 1 (not assumed) |
| Pinning via E_tot(r_hopf) unbiased ≥3-position test | method (anti-hang stability rule), category-A |

## Discipline
No labels/masses/data/fitting; no GR minimal coupling; Z_φ kept open; CF1 and CF2 genuinely open (the solve may
return massless or negative — pre-registered, not to be retrofitted); H3 precision caveats separate + NON-gating;
no private seal / no sealed-cell revival (frame C(a), Charles-ruled). No nonlinear solve until THIS
pre-registration is blind-verified. If a verifier finds the method smuggles a linear-order δq, a GR mass, or a
private seal, this pre-registration is revised before any solve.
