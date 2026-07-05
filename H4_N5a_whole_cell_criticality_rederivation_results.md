# H4 · N5a — Whole-cell criticality RE-DERIVED off the carve: does it pin ξ? — verdict UN-ANCHORED (candidate A reduced to the gated N5d solve)

**Status: BANKED — BLIND-VERIFIED (verifier agent ad85bcc2907db3df4, 2026-07-05: OVERALL HOLDS, all 7 attack
points PASS, no revision required; it re-ran the CAS independently and found F7 §B.2 corroborates the
R-modulus gap MORE strongly than claimed — the "un-anchored" verdict is NOT premature; no native data-blind
condition pins R at armchair. Two non-blocking caveats folded in: headline scoped to "by whole-cell criticality
at armchair" (B/D remain live); "4 r_p" citation → :212.)** Armchair / CAS node (sympy algebra
checks only; NO numerical solve, NO coupled BVP, NO fully-coupled compute). Executes node N5a of
`H4_N5_whole_cell_criticality_MAP.md` §7. DATA-BLIND (no lepton masses, no z_CMB as an anchor, no fitting);
no SM/particle labels; ξ, κ, N, Q_H, Z_φ, φ_amb symbolic/free. Frame **C(a)** (one universe cell; hopfion =
localized φ-blind defect ON the ambient bulk; NO private cell / NO shared seal / NO private fold). Deriver
agent (this node). CAS: `scratchpad` sympy checks (Derrick balance; migration self-consistency) — reproduced
inline in §7.

---

## 0. One-line verdict

Requiring the WHOLE universe cell (with the resolved Q_H=1 hopfion as its scale-breaking matter content) to
close on its OWN native criticality is **ONE relation** between the cell's total mass M(ξ,κ) and its size R —
and **R is the unpinned dilatation modulus** (F7 A.4). Therefore **whole-cell criticality does NOT pin ξ AT
ARMCHAIR** (CF-N5a fires: ξ stays a free family, ℓ_hopf/ρ_c ∝ 1/√ξ). **Scope precisely: ξ is un-anchored BY
WHOLE-CELL CRITICALITY — NOT proven absolutely free.** Candidates B (whole-cell flux budget, N5b) and D (coupled
non-perturbative virial fixed point, N5d) remain LIVE anchoring channels. The negative-#75 ξ<2-vs-ξ≥2 contradiction **does NOT
transport** — it **CHANGES CHARACTER / DISSOLVES**, but NOT via the fallacy the MAP warned against ("no seal ⇒
the virial half dissolves"): BOTH halves are CONDITIONS-CHANGED objects belonging to the *round rigid-N=1
carrier*, and the hopfion (toroidal, π₃) replaces that carrier entirely; the hopfion's own virial identity is
E₂=E₄, which carries **no ξ-bound**. **Candidate A is neither revived as a bare-ξ anchor nor a re-import
(CF-N5g PASS)**: its *apparent* pinning power in E1 was ENTIRELY the carve talking; re-derived honestly on the
single cell it pins nothing about ξ. The only surviving place a ξ-scale relation could be pinned is the
**coupled non-perturbative whole-cell virial fixed point (candidate D)** — GATED to the N5d solve (CF-N5f);
un-closable at armchair (ε≫1).

---

## 1. Step 1 — the universe cell's OWN criticality, natively, NO carve

The single N=0 fundamental (the universe cell) closes on its own criticality with no insertion, no carve, no
private seal. Three equivalent native faces of the SAME condition:

- **Geometric (F7 §A.1, DERIVED, verified):** the cosmic cell sits at criticality `M/R = c²/(2G)` **exact**
  (`F7_scale_bridge_native_results.md:100`). This is F5's "matter at one critical amount."
- **Reduced-variable transversality (E1 K5, DERIVED):** at the cell's inner even fold, the on-shell
  Hamiltonian constraint gives `H = E_m − 2 = 0`, i.e. `U(ρ_c) = 2`, where `U` is the ambient N=0 potential
  (φ-blind `L_m = −U(ρ)`) and ρ_c the areal value at the fold (gauge ρ_c = 1).
- **F5 identification:** "matter exists only at ONE critical amount; departures un-form."

Premise status: this is **DERIVED (frame-closed, verified)** but F5 is graded "CLOSED-as-FRAME,
circular-by-construction" (MAP ledger) — honor that: it is a self-consistent whole-cell closure, not an
independent lever. The inner even fold used here is the **universe cell's OWN** fold (the only even fold with
H=0 that survives frame C(a) — verifier aabaa3929f5f0864f already established this in the MAP §1 pass). **No
carve is performed; nothing is migrated.**

---

## 2. Step 2 — insert the resolved hopfion as the cell's scale-breaking CONTENT (and the off-round E_ang object)

The cell's matter content is now the H3 **outcome-A** object: a stable, localized, virial-balanced **Q_H=1
toroidal π₃ hopfion**, size `ℓ_hopf ≈ 1.1√(κ/ξ)`, energy `E ∝ √(ξκ)` (`node_H3_hopfion_solve_results.md`).
It lives ON the ambient bulk (C(a)); it is **φ-blind** — the flat-space energy/size does not see φ at leading
order (`H3_...preregistration.md:61-66`).

**The round-carrier angular-energy form must NOT be reused (verifier target 4 / CF-N5g).** The E1 form

    E_ang(r) = (ξ/2)(I_θ + N²I_s) + (κN²/2) I_4θ / ρ²        [round S²-winding carrier]

is the angular energy of a **round, axially-symmetric S² (π₂) hedgehog** with a single radial profile θ(r) and
an **integer S²-winding degree N**; I_θ, I_s, I_4θ are 1-D radial moments of that round ansatz
(`microphysics_E1_composite_closure_results.md:29`). **The hopfion is a different object:** it is a π₃ map
n : R³ → S² whose invariant is the **Hopf charge Q_H** (Whitehead linking integral), NOT an S²-winding degree.
It is toroidal with linked preimages — it is **not** expressible as one radial profile times N². Reusing the
round moment form here would be a frame smuggle.

**The correct off-round angular/matter-energy object (DERIVED from the H3 FS reduction):** native L2+L4 on N=0,
φ-blind + ρ=r ⇒ exactly the flat-R³ **Faddeev–Skyrme** energy (`node_H3_..._results.md:47-48`)

    E[n] = ∫ [ (ξ/2)|∂n|²  +  (κ/4) F_ij² ] d³x ,   F_ij = n·(∂_i n × ∂_j n)
         = ξ Ê₂  +  κ Ê₄ ,       (Ê₂, Ê₄ = pure, dimensionless, topology-fixed shape integrals)

The scale-graded decomposition **(E₂, E₄)** — the L2 Dirichlet piece (dilation grade +1) and the L4 Skyrme
piece (grade −1) — is the correct object, and it **replaces** the round `(I_θ, I_s, I_4θ)` moments. The role
of "N" is taken by **Q_H**, which enters **NOT as an algebraic coefficient** but as a **topological
constraint** (Vakulenko–Kapitansky: continuum |Q|=1 ⟹ E ≥ c > 0, a lower bound guaranteeing a finite nonzero
minimizer). Ê₂, Ê₄ are ξ,κ-independent numbers (the H3 solve reports the combination Ê ≡ E/√(ξκ) ≈ 285–286;
the split is ~50/50 at balance). **This is a genuine re-derivation, not the migration renamed.**

---

## 3. Step 3 — does whole-cell closure with the hopfion as content pin (ξ, κ, N)?  **No — ξ stays a free family.**

Two things must be kept apart, and keeping them apart is the whole answer:

**(3a) The hopfion's OWN scale is set by its flat-space Derrick balance — a free family in ξ.**
Under x → λx in R³, E₂ ∝ λ⁺¹, E₄ ∝ λ⁻¹, so `E(λ) = ξÊ₂λ + κÊ₄/λ`, stationary at

    λ* = √( κÊ₄ / (ξÊ₂) )   ⇒   ℓ_hopf ∝ √(κ/ξ),   E* = 2√(ξκ Ê₂Ê₄) ∝ √(ξκ)     (§7 CAS check 1)

and virial balance **E₂ = E₄** holds *identically* — it forces **no constraint on ξ** (the CAS solve of
E₂=E₄ for ξ returns the empty set: ξ unconstrained; §7). So the hopfion exists and picks its size for **every**
ξ, κ > 0. ξ is a free family at this stage. (This is H3's own conclusion `ℓ_hopf/ρ_c ∝ 1/√ξ`, f(ξ) not a
number.)

**(3b) Whole-cell criticality is ONE relation among M and R — and R is the unpinned modulus.**
The cell's criticality is `M/R = c²/(2G)` (step 1). With the hopfion as content, the cell's total mass is
`M = M_ambient + δM_hopfion`, where δM_hopfion is the hopfion's **whole-cell** gravitational response
(revised-N4 S2: the transverse operator L_bare has roots {1,2}, no decaying mode ⇒ cell-filling shear ⇒ the
mass is a whole-cell property, NOT a localizable halo — `H4_N4rev_...:16-22`). Criticality is then

    ( M_ambient + δM_hopfion(ξ,κ,…) ) / R  =  c² / (2G)          [ONE equation]

This is a **single** relation. It co-varies M and R along the critical line; **R is the dilatation modulus,
left UNPINNED by the law alone** (`F7_scale_bridge_native_results.md:107-122`, S8 pinning gap; the only thing
that would pin R is the depth anchor φ_seal = 7.004, which is z_CMB DATA — **forbidden here**). One equation,
with R free, pins **neither ξ nor κ nor N**. It does not even pin the combination ξκ (that would need a second
condition fixing R — candidate B/D, not criticality). ⇒ **CF-N5a fires: ξ un-anchored** by whole-cell
criticality. This is the pre-registered first-class scoped outcome, not a failure.

**Why E1's migration LOOKED like it pinned more — and why that power was the carve.** In the carved frame the
criticality was **migrated onto the carrier core**, forcing the *carrier's* U_eff to the critical value:
`ξ + κ/(2ρ_c²) = 2`. CAS (§7 check 2) shows this is a **self-consistent identity** that pins the **core size
ρ_c = √(κ/(2(2−ξ))) GIVEN ξ** — it does **not** pin ξ either. The ξ-value was to be pinned by the FULL carved
closure (the square residual system R1–R5), and negative #75 found that system **closes nowhere** for the
rigid carrier. Remove the carve (frame C(a)): criticality lands on the **ambient's** U, sets the **cell's own**
core size, and says **nothing** about the hopfion's scale. The hopfion just contributes δM. **The pinning
apparatus was the carve; without it, nothing pins the hopfion scale relative to the cell at armchair.**

---

## 4. CF-N5c — the negative-#75 virial identity in the NO-SEAL frame: does ξ≥2 survive?

Negative #75 (`NEGATIVES_REGISTRY.md:2129-2143`) is a two-sided contradiction for the **rigid-N=1 concentric
composite**:
- **ξ < 2 half** — the migrated core critical closure `E_ang(core) = 2 ⇔ ξ + κ/(2ρ_c²) = 2` (⇒ ξ < 2 for κ>0).
- **ξ ≥ 2 half** — the embedded-Derrick / on-shell-H≡0 **VIRIAL pointwise identity** `dens_a − dens_b = 4 − 2ξ`
  (P4/K11), whose closure needs ξ ≥ 2.

The MAP's explicit instruction: the ξ≥2 half is a **virial identity, NOT a seal BC**, so do **not** assume
seal removal dissolves it — test it on its own merits for a **frame-intrinsic residue**. Doing exactly that:

**(4a) The ξ<2 half genuinely dissolves — it WAS carve-carried.** It IS the migrated `E_ang(core)=2` (step 3
above): it exists only because the carve forced criticality onto a *private core*. Frame C(a) has no private
core ⇒ this half evaporates. (Not controversial; it is a migration artifact.)

**(4b) The ξ≥2 half is a REAL virial identity — but it is the ROUND rigid-N=1 carrier's virial identity, a
CONDITIONS-CHANGED object that does NOT transport to the toroidal hopfion.** Tested on its own merits:
- The identity `dens_a − dens_b = 4 − 2ξ` (P3/P4) rides on the constant **"4"**, which is the **round radial
  boundary term** `4 r_p` in the reduced 1-D geometry (`microphysics_E1_...:212`, `ξ∫(I_θ+N²I_s) = 4r_p +
  κN²∫I_4r + τ`). That "4" and the resulting ξ-bound are **specific to the round S²-winding reduction + the
  concentric embedded geometry**. They are properties of the RIGID-N=1 carrier, which the hopfion **replaces**.
- **The hopfion's OWN virial identity is E₂ = E₄** (the FS Derrick balance, §3a; H3-verified numerically to
  ~1%). CAS (§7 check 1): E₂=E₄ holds identically at λ* and forces **no ξ-bound** (empty solve). There is
  **no "4−2ξ" and no ξ≥2** for the toroidal object; the balance is satisfiable for every ξ, κ > 0 and merely
  **sets the size** λ*.

**⇒ CF-N5c VERDICT: the ξ<2-vs-ξ≥2 contradiction does NOT transport — it CHANGES CHARACTER (dissolves), but
via the CARRIER SWAP, decisively NOT via the "no seal ⇒ it dissolves" fallacy.** The honest chain: (i) the
ξ<2 half was carve-carried and evaporates; (ii) the ξ≥2 half is a genuine virial identity but the **wrong
object's** virial identity (round rigid-N=1, tied to the round radial "4"); (iii) the correct object (π₃
hopfion) has virial identity E₂=E₄, which carries **no ξ-bound at all**. So neither half survives as a
frame-intrinsic ξ-constraint. **Negative #75 is itself CONDITIONS-CHANGED by the hopfion reframe** (it is
scoped rigid-N=1 concentric; the reframe swaps both the carrier AND the frame) and loses blocking authority
for the C(a) hopfion until re-graded. It remains fully in force *within its own premise set* (round-static,
concentric, rigid-N=1 carrier).

**One honest residue flag (points to candidate D, gated).** The E₂=E₄ balance carrying no ξ-bound is the
**flat-space** identity. With gravity ON **non-perturbatively** (ε≫1, revised-N4 S6), the cell-filling shear
energy MODIFIES the Derrick balance (candidate D): the coupled fixed point *could* pin ℓ_hopf/ρ_c hence ξ. But
that is **not** a "ξ≥2 residue of #75" — it is a NEW, whole-cell, coupled condition, un-closable at armchair
(CF-N5f) and forbidden to close perturbatively (ε≫1). At armchair the correct statement is: **no virial
ξ-residue survives seal removal; a possible coupled-gravity virial residue is GATED, not derivable here.**

---

## 5. CF-N5g — self-audit: single cosmic cell, no re-import

Line-by-line the derivation stays on the ONE cosmic cell:
- **Step 1** uses the universe cell's OWN inner even fold (`U(ρ_c)=2` on the ambient potential). No carve.
- **Step 2** uses the flat-R³ FS hopfion energy on the bulk, φ-blind, no private cell / no private φ-well.
- **Step 3** uses the GLOBAL criticality `c²=2GM/R` with δM = the whole-cell hopfion response. No shared seal;
  no `H_cell(r_p)=H_amb(r_p)` matching; no migrated `E_ang(core)=2`.
- **Step 4** uses the hopfion's flat-R³ Derrick balance E₂=E₄. No seal, no concentric geometry, no "4 r_p".

Nowhere is a shared seal, private inner fold, or carved particle cell reintroduced. **CF-N5g PASS.** And
crucially: candidate A **re-derived** on the single cell does **not** reproduce the migration's pin — it shows
the pin evaporates. So candidate A is a **genuine re-derivation whose verdict is "no ξ-anchor,"** NOT the
concentric migration re-labelled (which would be the smuggle). The re-derivation *refutes* the migration as an
anchor rather than renaming it.

---

## 6. What is DERIVED vs OPEN vs REFUTED (and candidate A's fate)

**DERIVED (armchair, CAS-checked, C(a)-clean):**
- Whole-cell criticality with the hopfion as content is **ONE relation** (M vs R) with R the unpinned modulus
  ⇒ **ξ un-anchored** (CF-N5a). ξ remains a free family; `ℓ_hopf/ρ_c ∝ 1/√ξ` reported honestly (heir of H4-CF4).
- The round S²-winding `E_ang` moment form does **NOT** transport to the toroidal π₃ hopfion; the correct
  object is the FS **(E₂, E₄)** scale-graded functional; **Q_H replaces N as a topological constraint (VK
  bound), not an algebraic N² coefficient.**
- The hopfion's virial identity is **E₂ = E₄**, ξ-unconstrained (sets the size λ* ∝ √(κ/ξ) only).
- Negative #75's contradiction does **NOT transport** to the C(a) hopfion (CF-N5c: dissolves via carrier swap;
  #75 is CONDITIONS-CHANGED by the reframe — flag it in the registry, re-grade under C(a)).

**OPEN / GATED (cannot be closed at armchair):**
- Whether the **coupled non-perturbative whole-cell virial fixed point** (candidate D) pins ℓ_hopf/ρ_c hence ξ.
  This is the **only** surviving place a ξ-scale relation could live. It needs the N5d solve; ε≫1 forbids a
  perturbative close (CF-N5f). **This is where candidate A's anchoring question is REDUCED to.**
- Candidate **B** (whole-cell dilation-flux budget closure) — a separate whole-cell condition (N5b); may pin a
  (ξ, Z_φ) combination (CF-N5e). Not settled here; cross-check against A/D owed.

**REFUTED / pre-registered failures confirmed:**
- **Candidate A as a bare-ξ anchor at armchair** — REFUTED: its apparent pin was carve-artifact; on the single
  cell criticality is one relation absorbed by the free modulus. (Not a re-import; a genuine re-derivation with
  a null-anchor verdict.)
- **Candidate C** (active-P onset threshold) — stays a pre-registered clean failure (CF-N5b): no reachable
  dead-G (revised-N4 S4) + φ-blind scale.
- **Candidate E** (cosmic absolute / z_CMB) — OUT (data + F7 §B insufficient).

**Candidate A's fate:** **NOT revived** as an armchair ξ-anchor; **NOT a re-import** (CF-N5g PASS); **REDUCED
to the gated N5d solve** (its only surviving anchoring channel is the coupled non-perturbative virial fixed
point, candidate D). The MAP's provisional read — "A and B are the two live whole-cell-consistent candidates,
possibly the same condition seen two ways; the anchor, if any, needs the gated solve" — is **confirmed and
sharpened**: A *by itself* (criticality) does not anchor; the anchoring content it was hoped to carry lives in
D (coupled virial) and possibly B (flux), both un-closable at armchair.

---

## 7. CAS checks (sympy; algebra only, no solve)

**Check 1 — FS hopfion Derrick balance (the correct off-round virial identity).** `E(λ)=ξÊ₂λ+κÊ₄/λ`:
- `λ* = √(κÊ₄)/(√(ξÊ₂))` = √(κÊ₄/(ξÊ₂)) ⇒ ℓ_hopf ∝ √(κ/ξ).
- `E₂(λ*) = E₄(λ*) = √(Ê₂Ê₄ κξ)` ⇒ virial `E₂−E₄ = 0` identically.
- `E(λ*) = 2√(Ê₂Ê₄ κξ)` ∝ √(ξκ).
- **Solve E₂=E₄ for ξ → ∅ (empty): the virial identity forces NO ξ-constraint.**

**Check 2 — the round migration pin is self-consistent ⇒ pins core size, not ξ.** `ξ + κ/(2ρ_c²) = 2` ⇒
`ρ_c = √(κ/(2(2−ξ)))`; back-substituting gives `U_eff(ρ_c) = 2` **identically** ⇒ the closure fixes ρ_c
**given** ξ, it does not pin ξ. (The ξ-value came only from the full carved closure — which #75 killed.)

**Check 3 — the round rigid virial residue `4−2ξ` rides on the "4"** = the round radial boundary term `4 r_p`
(`microphysics_E1_...:212`); it is carrier-specific (round S²-winding, concentric) and does not belong to the
toroidal hopfion. (Structural, not a solve.)

(Reproducible sympy in the session scratchpad; all three are elementary and were re-run clean.)

---

## 8. Premise ledger (chose / derived / theory / habit)

| Premise | Tag | Note |
|---|---|---|
| Universe cell closes on its own criticality `c²=2GM/R` / `U(ρ_c)=2` | **DERIVED (frame-closed, verified)** | F5/F7; honor its "circular-by-construction" grade — a closure, not an independent lever |
| Frame C(a): no private seal / cell / fold for the hopfion | **THEORY/CHOSE — Charles-ruled (N3)** | violation = C(b) = STOP |
| Hopfion = H3 outcome-A Q_H=1 toroidal π₃ FS soliton, φ-blind | **DERIVED (H3, blind-verified A)** | size ℓ_hopf∝√(κ/ξ), E∝√(ξκ) |
| Round `E_ang` moment form applies to the hopfion | **REFUTED — does not transport** | correct object = FS (E₂,E₄); Q_H replaces N as a topological constraint, not a coefficient |
| Hopfion gravitational mass is a WHOLE-CELL response (δM not a localized halo) | **DERIVED (revised-N4 S2, blind-verified)** | makes criticality a global M/R statement |
| R = dilatation modulus, unpinned by the law alone (data-blind) | **DERIVED (F7 A.4 / S8 gap)** | the reason one criticality relation cannot pin ξ; the depth anchor that would pin R is z_CMB DATA (forbidden) |
| ξ = L2, κ = L4; existence derived, VALUE free | **existence DERIVED / value FREE (data-blind gauge)** | the object to (not) anchor |
| Backreaction NON-PERTURBATIVE (ε≫1) | **DERIVED (revised-N4 S6)** | forbids perturbative CLOSURE of candidate D; frames only |
| Negative #75 (rigid-N=1 concentric contradiction) | **CONDITIONS-CHANGED by the reframe** | carrier swap (round→toroidal) + frame swap (carve→C(a)); re-grade in NEGATIVES_REGISTRY; in force only within its own premise set |
| Z_φ fork (Route A free / Route B=8) | **CHOSE / OPEN** | bites candidate B (flux), not A at armchair |
| CAS grids / sympy assumptions (positivity) | **Category-A conditioning** | soundness, not physics |

---

## 9. For the verifier (attack surface, named)

Aim hardest where a confirmation-of-hypothesis smuggle is most likely (hypothesis-discipline):
1. **★ Is candidate A genuinely re-derived, or the migration renamed (CF-N5g)?** Check §3/§5: is "one
   criticality relation + free R ⇒ ξ un-anchored" clean, or does it silently need the carve to even state δM?
   (I claim δM is the whole-cell response, revised-N4 S2 — no seal needed. Attack that.)
2. **★ The CF-N5c call.** Did I honestly test the ξ≥2 virial half on its own merits, or did I lazily invoke
   "no seal ⇒ dissolves"? Verify §4b: is the "4−2ξ" really carrier-specific (round radial "4 r_p"), and does
   the hopfion's E₂=E₄ really carry no ξ-bound (CAS check 1)? If the ξ≥2 half has a frame-intrinsic residue I
   missed, CF-N5c changes.
3. **Off-round object.** Is the FS (E₂,E₄) decomposition the right replacement for the round moments, and is
   "Q_H as constraint not coefficient" correct? A round-form assumption anywhere is a smuggle.
4. **Non-perturbativity gate.** Confirm no step CLOSES the anchor perturbatively; candidate D stays gated.
5. **Modulus claim.** Is R genuinely unpinned data-blind (F7 A.4), or did I over-read the pinning gap to
   manufacture "un-anchored"? If a data-blind condition pins R, criticality would pin ξκ (CF-N5e).
6. **Freshness.** #75 and the `E_ang(core)=2` margin note are treated as needing-re-grade, not in-force —
   confirm I did not lean on CONDITIONS-CHANGED work as current support.

---

## 10. LAB-LOG
- (this node) armchair/CAS only; sympy checks 1–3 re-run clean; NO solve, NO BVP. NOT committed
  (verifier-before-record). Owes a blind adversarial verifier pass before any banking or registry edit.
