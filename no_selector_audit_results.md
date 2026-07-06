# No-Selector Audit — does ANY native object break the three equivalent S² TARGET channels and select ONE public channel (forging q=1/3), or does the public charge stay Q=1?

**Mode:** rigorous NO-SELECTOR audit (armchair + CAS; sympy exact, NO numerical PDE solve, NO data).
Per **hypothesis discipline**, aimed HARDEST at FINDING a selector (outcome A = the exciting,
hypothesis-closing result); a clean "no selector" (outcome B) is banked as a first-class theorem.
No SM charge assignments imported; no private seal / private cell / carved boundary invoked (frame
C(b) forbidden); the value 1/3 is NOT targeted (CAS carries the structure symbolically, 1/3 appears
only as an end-of-run check).

**Driver:** Claude (Opus 4.8, 1M context), 2026-07-05.
**Status: BANKED — BLIND-VERIFIED (verifier ac28a9c57dcfd18be, 2026-07-05: OUTCOME B CONFIRMED, no native selector
found; outcome A hunted hard across the stress tensor, the backreaction/equivariance route, and the observable
space, and NOT found). The verifier independently re-derived the L4 Skyrme Hilbert stress and confirmed every
component is target-SO(3)-invariant (the load-bearing P2 term the first CAS had ASSERTED but not computed), and
independently confirmed the T1 equivariance identity =0. Two CAS demonstration gaps it flagged are now FIXED +
re-run clean: (1) the L4 Skyrme stress invariance is now COMPUTED (T4_ij for 00/01/12/22 all target-invariant);
(2) the T1 check now prints the actual 0 (via .rewrite(cos)) with a control showing the lock fixes the RELATIVE
sense. Verifier strengthening folded in: the moment-observable proof (vector moment ∫n_a ω_H1=0; 2-tensor
=(4π/3)δ_ab, traceless part 0) makes P3's exhaustiveness a DIRECT theorem — no target-indexed observable survives
on the isotropic config. Minor note added: dividing the scalar total by rank N=3 is a second (equally non-native)
route to a scalar 1/3.**
CAS: `no_selector_audit_cas.py` (sympy, exact, bounded, no solve; patched per verifier; all prints reproduced inline).

**Grounding (established, blind-verified — read, not re-litigated):**
`d1_charge_channel_projection_MAP.md` (verifier a5cf5a27f637302df): the equal-thirds partition of the
unit charge is NATIVE and TOPOLOGICAL (⟨n_a n_b⟩=δ_ab/3 = per-target-axis winding ∫n_a²dΩ=4π/3 each,
frame-invariant, whole degree-1 class), NOT the End(H1) triplet; BUT the native charge readouts
(degree (1/4π)∫ω_H1, Hopf Q_H=∫A∧dA) are scalars = the FULL sum = 1; reaching 1/3 needs a public
COUPLING to one target axis (the candidate selectors V_ab n_a n_b with V≁δ, and the easy-axis
n₃=cosΘ(r), were both flagged "not native"). The action: E=∫[(ξ/2)|∂n|² + (κ/4)F_ij²],
F_ij = n·(∂_i n×∂_j n) = ε_abc n_a ∂_i n_b ∂_j n_c (`node_H3_hopfion_solve_results.md:48`,
`angular_lagrangian_results.md`). Q_H=1 hopfion resolved (H3 outcome A); its mass is a whole-cell
response (revised-N4: cell-filling shear h_AB, `H4_N4rev_conditional_mass_response_results.md`).
Frame C(a): defect on the isotropic round cell, no private seal.

---

## 0. THE PRECISE DISTINCTION THIS AUDIT TURNS ON (kept rigorous throughout)

Two *different* rotation groups must never be conflated:

- **SPATIAL SO(3)** — rotations of ℝ³ (the cell). The hopfion is TOROIDAL in SPACE: it has a ring /
  symmetry axis, a unit vector in ℝ³. This is the axis h_AB (the induced shear) tracks.
- **TARGET SO(3)** — global rotations of the value sphere S², n_a → R_ab n_b. The equal-thirds
  partition ⟨n_a n_b⟩=δ_ab/3 lives here (over the target components n_a).

The hypothesis wants ONE TARGET channel singled out (→ 1/3). A "selector" is any NATIVE object that
breaks the **TARGET** SO(3) and pins ONE target axis in a way the PUBLIC charge observable can read.
A spatially-anisotropic object (torus axis, self-induced shear) is a selector ONLY if it feeds a
target-axis pin into the observable — otherwise it is spontaneous orientation, not selection.

---

## 1. PREMISE LEDGER (chose / derived / import tags)

- Carrier (unit 3-vector n_a, |n|=1, target S²): **THEORY** (C-2026-06-14-1; blind-verified anchor).
- Action E=∫[(ξ/2)|∂n|² + (κ/4)F_ij²] (native FS L2+L4): **DERIVED** as the unique diffeo-scalar,
  target-isometry-invariant, ≤4-derivative functional (`angular_lagrangian_results.md:57-63`,
  `node_H3:48`); ξ,κ the couplings (**CHOSE** normalizations, category-A). No potential added.
- Round/isotropic S² target metric (⇒ target SO(3) isometry): **CHOSE + canonized** (C-2026-06-18-1).
- Frame C(a): one isotropic round cell, φ radial, seal/fold at fixed radius, spherical read-surface,
  matter φ-blind (n→h_AB→𝒦→φ): **THEORY** (native field equations, 2026-07-01; whole-cell canon).
- Standard degree-1 Hopf map w=2(x+iy)/(r²−1+2iz), n_∞ = north pole: **DERIVED** representative of the
  Q_H=1 class (used only to expose equivariance; conclusions are class-, not representative-, level).
- Induced shear h_AB, transverse operator L_bare (roots {1,2}, no decaying mode): **DERIVED**
  (`H4_N4rev...`, blind-verified).
- q=1/3 as a VALUE: **NOT targeted** — CAS carries the structure; 1/3 is only an end check.
- No private seal / carved boundary as selector: **EXCLUDED by construction** (frame C(b) forbidden).
- No SM charge assignment: **EXCLUDED by construction**.

---

## 2. AUDIT TARGET 1 (★ load-bearing) — the equivariance lock: spatial torus axis ↔ target axes

**The mechanism, made precise (CAS T1, exact).** For the standard degree-1 Hopf map the target
stereographic coordinate is w = 2(x+iy)/(r²−1+2iz), with n_∞ the north pole. A SPATIAL rotation
about the torus (z) axis by α sends (x+iy)→e^{iα}(x+iy) and leaves z,r fixed, so

```
w(R_z(α)·x) − e^{iα}·w(x) = 0     (sympy, exact; exp→trig rewrite → 0)
```

and w→e^{iα}w is exactly a TARGET rotation about the n_∞ (pole) axis by α. So:

> **a spatial rotation about the torus axis IS a target rotation about n_∞.**

This is the equivariance lock. It makes the hopfion invariant under the **DIAGONAL SO(2)** (rotate in
space about the torus axis AND in target about n_∞, simultaneously). Read carefully, this is a lock
of the **RELATIVE** spatial↔target orientation — it does **NOT** pin any ABSOLUTE axis.

**Does the background pin the spatial axis? (the decisive sub-question.)** No. On the round isotropic
cell (frame C(a)) the metric and the energy density depend on space only through rotation-scalars
(r² is spatial-rotation invariant — CAS T1b, exact). Therefore ANY spatially-rotated hopfion is
**energy-degenerate**: the torus axis is a **free zero-mode** (a Goldstone direction of the
spontaneously broken spatial SO(3)→SO(2), a full S² of equivalent choices). Because the torus axis is
free and it is *locked to* n_∞ by equivariance, n_∞ is free too: the pair (torus axis, n_∞) CO-ROTATES
freely at zero energy cost.

**Finding (Target 1): CO-ROTATES FREELY, no selection.** The equivariance lock ties the target axis
to the spatial axis, but the isotropic background pins NEITHER. Both the hopfion's spatial orientation
AND its locked target axis n_∞ are simultaneously free. This is **spontaneous orientation, not a native
selector**. A selector would require the background to PIN the spatial torus axis — nothing in frame
C(a) does (that would need an external spatial anisotropy = a preferred direction the round cell lacks).

---

## 3. AUDIT TARGET 2 — target-space anisotropy of the action (CAS T2, exact)

Under a finite generic SO(3) target rotation R (concrete generic axis, symbolic angle; det R=1,
RᵀR=I verified):

```
L2:  |∂_i n|²  = (∂_i n)·(∂_i n)          →  invariant   (True, exact)
L4:  F_ij = n·(∂_i n×∂_j n)               →  invariant   (True, exact)
     (F_ij)²                              →  invariant   (True, exact)
```

The only target tensors appearing are **δ_ab** (contracting |∂n|²) and **ε_abc** (in the triple
product F) — the UNIQUE SO(3)-invariant rank-2 and rank-3 tensors. Infinitesimally, δ(|n|²)=2n·(θ×n)=0
identically (CAS), so no linear target-anisotropy can survive. There is **no** V_ab n_a n_b term with
V≁δ_ab anywhere in L2+L4, nor in the measure √(−g)=c r² sinθ (the φ-factors cancel; target-blind), nor
in the winding 2-form ω_H1 (topological, metric-free, contributes no stress).

**Finding (Target 2): the action is manifestly target-SO(3)-invariant.** No native term carries a
target-anisotropic piece. A V_ab selector is NOT in the action; introducing one = outcome C (new
physics), not a derivation.

---

## 4. AUDIT TARGET 3 — ansatz vs physics (n_∞ is a gauge choice)

All points of the round S² are equivalent under the target SO(3) isometry; n_∞ (the value at spatial
infinity, and equivalently the toroidal-coordinate / "easy-axis" choice) merely FIXES target
coordinates by CONVENTION — a gauge/orientation choice, not a physical target-axis selection. The
charge readouts are n_∞-INDEPENDENT: the degree (1/4π)∫ω_H1 and Hopf Q_H=∫A∧dA are target-SO(3)
scalars (CAS T4: total degree = 1 independent of frame; and F, |∂n|² invariant under any R). The
per-axis shares are each 1/3 in EVERY frame (frame-invariant equality), so no frame distinguishes a
single axis. The easy-axis form n₃=cosΘ(r) that WOULD single out an axis was already flagged
"gauge/orientation choice … ansatz-dependent, not native" (`archive/n3_direction_distribution_results.md:265`).

**Finding (Target 3): n_∞ is a gauge choice; the readouts are topological and n_∞-independent.** The
ansatz does not smuggle a physical selection.

---

## 5. AUDIT TARGET 4 (★ load-bearing — scrutinized hardest) — whole-cell background coupling

**(a) radial φ-gradient — target-blind.** The matter stress is T_μν = ξ(∂_μ n_a)(∂_ν n_a) + g_μν L,
built from the δ_ab contraction (CAS T4: T_ij = Σ_a ∂_i n_a ∂_j n_a is target-SO(3) invariant). The
hedgehog gives ρ = ξ/r², p_r = −ξ/r², p_θ=p_φ=0 (`angular_lagrangian_results.md`) — a **target-scalar**
source. The φ-gradient couples to this target-scalar energy, seeing NO target axis.

**(b) fold/seal at fixed radius — isotropic in space, target-blind.** It is a spherical locus in space
(no spatial-axis pin) and enters through the target-scalar stress / geometry only. (It is also NOT a
private carved boundary — frame C(a); invoking one as a selector would be C(b), forbidden — see §6.)

**(c) flux read-surface (a sphere) — reads the SUMMED charge.** The public readout is the degree /
Hopf integral over the sphere = the target-SO(3) scalar = **1** (CAS T4). It is not a single-channel
projector.

**(d) ★ the hopfion's OWN induced shear h_AB — the most likely place a selector hides.** revised-N4:
h_AB is anisotropic/multipole in SPACE, along the hopfion's spatial torus axis; L_bare (roots {1,2})
has no decaying mode ⇒ cell-filling. Does this self-induced SPATIAL anisotropy, via equivariance, lock
a TARGET axis and select a channel for the PUBLIC charge? Three exact facts close it:

1. **The shear source is a TARGET SCALAR.** h_AB is sourced by the stress T_μν, built from the δ_ab
   contraction (CAS T4, invariant). So the source carries **no target index**: it responds to the
   spatial *distribution* of energy, not to any target direction. h_AB itself is a spatial metric
   perturbation with no target index at all.
2. **The whole (hopfion + its shear) co-rotates freely.** The shear picks out the hopfion's OWN
   spatial torus axis, which is a **free zero-mode** on the isotropic cell (§2, CAS T1b). Rotate the
   hopfion: h_AB rotates with it in space, and via equivariance n_∞ rotates too — all at zero energy
   cost. So the shear implements **spontaneous orientation**, self-choosing an axis, NOT a pinned one.
3. **Even a spontaneously-chosen axis does NOT change the observable.** The public charge readout is a
   target-SO(3) SCALAR (degree, Hopf = 1). Choosing a direction n_∞ leaves that scalar = 1 — it never
   becomes 1/3. To read 1/3 you need a readout that PROJECTS onto one target axis
   ((1/4π)∫n_a(∂n×∂n)_a for a single fixed a — CAS T4 gives 1/3 per axis, sum 1). The shear coupling,
   being target-scalar, supplies a SCALAR (summed) response — it does NOT implement a single-target-axis
   projector in the observable.

**Finding (Target 4d): SPONTANEOUS ORIENTATION, not selection.** The self-induced shear is the nearest
thing to a selector — it is genuinely anisotropic in space and locked to n_∞ by equivariance — but it
is target-blind (scalar source, no target index), freely orientable (zero-cost), and it never enters
the target-scalar charge observable. The public charge stays the **summed Q=1**.

---

## 6. AUDIT TARGETS 5 & 6 — forbidden-move checks

**5. No private seal / private cell / carved boundary invoked (frame C(b) forbidden).** Every step
used the PUBLIC isotropic round cell (frame C(a)): the seal is a spherical locus at fixed radius
entering only through target-scalar stress/geometry; no Dirichlet wall at finite r was invoked (that
localizing wall = the retired private seal, explicitly avoided in revised-N4 too). No selection rests
on a carved boundary. **PASS.**

**6. No SM charge assignment imported.** No quark/lepton charge, no color/gauge label, no 1/3 as an
input. The number 1/3 appears only as an end-of-run CAS check of the equal-thirds partition. **PASS.**

---

## 7. OUTCOME — **B: NO SELECTOR under the current action + frame C(a)**

The audit lands on **B**. Every candidate selector location was checked; the nearest miss (the
self-induced shear, Target 4d) fails for a precise reason. Evidence: CAS T1 (equivariance lock exact),
T1b (torus axis is a free zero-mode), T2 (action manifestly target-SO(3)-invariant, no V_ab), T3
(n_∞ a gauge choice; readouts n_∞-independent), T4 (stress/shear source is a target scalar; public
readout = scalar 1; single-channel needs a hand-fixed axis).

### 7.1 NO-SELECTOR THEOREM (stated precisely, with premise set)

> **Premises (P):** (P1) the native hopfion action E=∫[(ξ/2)∂_i n_a ∂_i n_a + (κ/4)(ε_abc n_a ∂_i n_b
> ∂_j n_c)²], which is invariant under the global TARGET rotation group SO(3): n_a→R_ab n_b, R∈SO(3)
> (CAS T2, exact); (P2) the isotropic round cell background, frame C(a) — φ radial, seal a spherical
> locus at fixed radius, spherical read-surface — all target-blind, coupling to matter only through
> the TARGET-SCALAR stress T_μν[n]=ξ(∂_μ n_a)(∂_ν n_a)+g_μν L (CAS T4); (P3) the public charge
> observables — degree (1/4π)∫ω_H1 and Hopf Q_H=∫A∧dA — are target-SO(3)-invariant SCALARS.
>
> **Claim:** Under P1–P3 no native object breaks the target SO(3) to select a single target axis; the
> public charge readout is the SUMMED **Q = 1**. The equal-thirds partition ⟨n_a n_b⟩=δ_ab/3 is real
> and internal, but its three shares are related by the UNBROKEN target SO(3) and no native field
> couples to a single share. The hopfion's spatial torus axis (and its self-induced shear h_AB) is a
> FREE zero-mode on the isotropic cell; by Hopf equivariance a spatial rotation about the torus axis
> equals a target rotation about n_∞ (CAS T1), so the spatial axis and n_∞ CO-ROTATE freely at zero
> energy cost — spontaneous orientation, not selection. Because the shear source is a target scalar and
> the charge observable is a target scalar, every orientation yields the same public charge = 1.
> Therefore **q = 1/3 is NOT forced; the native public charge is q = 1.**

This is a CLEAN negative: the equal-thirds ARITHMETIC is native (confirmed, unchanged), but no native
PROJECTOR makes one share public. It is the same failure mode the parent D1 MAP reached, here promoted
to a theorem by exhibiting the selector-absence structurally (equivariance + target-scalar coupling)
rather than by enumerating failed readouts.

### 7.2 What would OVERTURN it (what a future selector must supply)

A selector must introduce a **TARGET-indexed** object that couples anisotropically — in the ACTION or
in the OBSERVABLE — that is DERIVED (not posited) from the metric:

- a target-space potential V_ab n_a n_b with V≁δ_ab, derived natively (would break P1); OR
- a background that is itself **target-charged** (carries a target-vector/tensor), coupling to one n_a
  (would break P2's target-blindness); OR
- a native single-target-axis PROJECTOR in the public charge readout — a charge functional returning
  ∫n_a(∂n×∂n)_a for one fixed a WITHOUT an imported anisotropy (would break P3's scalar character).

Any of these that is genuinely DERIVED = outcome A (hypothesis closes, q=1/3 forged). Any that is
merely ADDED = outcome C (new physics, not a derivation). The audit finds NONE of the three natively
under the current action + frame C(a).

---

## 8. FOR THE VERIFIER / ATTACK SURFACE (where a selector was most nearly found)

Attack the CONFIRMING (selector-found) readings hardest — hypothesis discipline.

1. **★ Target 4d — the induced shear (nearest miss).** The strongest selector candidate: h_AB IS
   spatially anisotropic and IS locked to n_∞ by equivariance. My close rests on THREE claims — attack
   each: (a) is the shear source REALLY a target scalar? Re-derive T_μν from L2+L4 and confirm the
   δ_ab contraction leaves no residual target-vector piece (e.g. does the Skyrme F_ij² term, or a
   φ-coupling in the whole-cell equations, generate a target-indexed stress component?). If ANY stress
   component carries a free target index, P2 breaks and a selector may exist. (b) Is the torus axis
   truly a FREE zero-mode, or does the whole-cell backreaction (h_AB cell-filling, revised-N4) generate
   a self-energy that PINS the spatial axis? A pinned spatial axis + equivariance ⇒ pinned n_∞ ⇒ a
   selector (outcome A). I claim the isotropy of the cell keeps it free — check the backreacted energy
   is still spatial-rotation invariant. (c) Does the charge observable REALLY stay scalar under the
   backreaction? Confirm the Hopf/degree integral is unchanged by h_AB (h_AB has no target index).
2. **★ Target 1 — the equivariance direction.** I used ONE representative Hopf map. Attack: is the
   spatial-axis↔target-axis lock representative-independent (a class property), and does it hold for
   the ACTUAL resolved toroidal hopfion (⟨ρ⟩=1.28 core ring), not just the rational map? Confirm the
   lock is the diagonal SO(2) of the config's symmetry group, and that it pins RELATIVE not ABSOLUTE
   orientation.
3. **Target 2 — hidden anisotropy in the measure or φ-coupling.** I checked L2+L4 and √(−g). Attack:
   does the geometric coupling n→h_AB→𝒦→φ (matter φ-blind) introduce a target-anisotropic effective
   term at second order (e.g. via h_AB feeding back into the n-equation)? Confirm the feedback stays
   target-SO(3)-invariant (h_AB target-scalar ⇒ it should).
4. **The single-channel readout (Target 3/4c).** I claim ∫n_a(∂n×∂n)_a for fixed a (=1/3) is the ONLY
   way to 1/3 and requires a hand-fixed axis. Attack: is there a native charge functional (a flux
   through one coordinate 2-cell, a per-generator holonomy, a projected Whitehead integral) that
   returns 1/3 WITHOUT an imported anisotropy? If yes, P3 breaks and outcome flips to A.
5. **Anti-targeting / data-blind audit.** Confirm the CAS carries the structure symbolically and 1/3
   enters only as an end check; confirm no lepton/hadron number anywhere; confirm no private
   seal/cell/boundary and no SM charge assignment was used as a selector.

---

## 9. BOTTOM LINE

Under the current native action (FS L2+L4, manifestly target-SO(3)-invariant) and frame C(a) (one
isotropic cosmic cell, no private seal), **NO native object breaks the three equivalent target
channels to select one public channel.** The equal-thirds partition is real and internal; the public
charge readout remains the **summed Q = 1**. q=1/3 is NOT forged — it remains UNFORCED. The nearest
miss is the hopfion's self-induced shear (spatially anisotropic, equivariance-locked to n_∞), which
fails as a selector because its source is a target scalar, its axis is a free zero-mode, and it never
enters the target-scalar charge observable: it is spontaneous orientation, not selection. **OUTCOME B —
a no-selector theorem (premise set §7.1), overturnable only by a natively-derived target-indexed
anisotropic coupling (§7.2), which does not exist under the current action + frame.** DRAFT — owes a
blind verifier.
