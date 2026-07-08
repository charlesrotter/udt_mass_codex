# NEXT-SESSION DESIGN — the derived BACKGROUND (x_max done right) + the native φ-matter SOURCE, toward particle emergence

**Date:** 2026-07-07 (PM, wind-down) · **Author:** Claude Opus 4.8 (1M) with Charles. **Status: DESIGN / seamless-pickup
spec for the next session.** Data-blind (no 1101/7.004). Two threads to develop TOGETHER because they are the two halves
of the same missing setup for particle emergence: a **derived background** + **matter that couples to it**.

## 0. WHY these two together (the framing)
Particle emergence has been blocked by two things this whole project: **(i)** the matter-structure wall — φ-blind matter
DRAINS (`I_r→0`), so a cell can't carry the radial structure it needs (this killed the rung-resonance test and every
prior emergence attempt); and **(ii)** we have **never had a properly-DERIVED background** for a particle cell to embed
in — only MODEL ambients (hand-picked numbers) or a centered cell. This session unfroze both:
- **Thread A (background):** redo the `x_max`/cosmological work PROPERLY (from the observer-frame-relation), data-blind →
  the DERIVED ambient dilation field a particle cell sits in.
- **Thread B (coupling):** the native direct φ-matter source (from relaxing φ-blindness) → the RESTORING channel that can
  defeat the drain, i.e. HOW the particle's matter couples to that background's dilation.
**Together = a derived environment + matter that feels it = the setup particle emergence has always lacked.** Do A to
furnish the background; do B to test whether a cell closes in it.

---

## THREAD A — redo `x_max` PROPERLY (the derived background)

### A.1 The error to NOT repeat (this session's category error)
The earlier `x_max` work literalized *"an invariant maximum DISTANCE"* (a physical finite length) → this was a **tautology**
(the boost derivation is just `1+z=e^φ` re-coordinatized; `udt_xmax_boost_derivation_results.md`) and it spawned a
**homogeneity/Copernican rabbit hole** (over-literalizing the redshift as a physical field to be sourced;
`udt_no_homogeneous_universe_results.md` + `udt_phi_blindness_relaxation_results.md` are the PHYSICAL-FIELD layer, NOT the
operative reading). DO NOT restart there.

### A.2 The CORRECT frame to start from — the observer FRAME-RELATION
UDT's redshift is a **FRAME-RELATION**, exactly like relativistic frame dependence (canonical SNe work,
`udt_canonical_geometry.md` §1.4 + the shell-theorem note at §1, line 148):
- `1 + z = e^{φ(r)}`, `d_L = r·e^{φ(r)} = r(1+z)` (static reciprocity, ONE `(1+z)`, not FLRW's `(1+z)²`), `D_A = r`.
- Every observer sits at their **own** `φ=0` (locally Minkowski); the boundary-mass growth arrives isotropically and
  **cancels** (Newtonian shell theorem) → **no preferred frame, NO cosmic center, NO Copernican problem.**
- The "boundary" is the `φ→∞` **asymptotic edge** (infinite redshift), observer-relative — NOT a finite invariant length.
This is empirically successful ALREADY: Pantheon+ 1701 SNe = **0.166 mag RMS (1.08× ΛCDM), ZERO free cosmological params**.

### A.3 What to DERIVE (data-blind, no 1101/7.004)
1. **The native `φ(r)` profile FORM — the D-POLY-1 gap.** The old work derived the cubic's COEFFICIENTS
   `(3/2, cos(π/5), 2/3)` from the angular Diophantine triple `(j,ℓ,|κ|)=(1/2,1,3)` + `μ_g=πμ/13`, but the cubic
   **FORM itself is an ansatz, not derived** (D-POLY-1, `udt_canonical_geometry.md` §12.7). DERIVE the form from the
   metric's constraint structure (Branch-C imposes no scalar equation on φ; is there a native selector?).
2. **The asymptotic-edge structure** at `φ→∞` (observer-relative; the earlier quartic-lapse/infinite-proper-distance
   characterization was profile-specific to the cell cosine and is SUBSUMED — redo it on the operative profile).
3. **Reconcile** our native cell `φ(r)` (the round-cell cosine, `e^{−φ/2}=A cos(kr)`) with the SNe cubic near the edge —
   are they the same object at different scales, or different?
4. **The depth anchor natively** — this is the STANDING GOAL: derive why the universe sits at its depth (the thing the
   old work fits as `φ(r*)=ln(1101)`), WITHOUT fitting. Ties to the Misner–Sharp marginal relation `c²≈2GM/r*` (= our
   native `x_max=2GM/c²` marginal edge, `udt_canonical_geometry.md` §10.4).

### A.4 Grab / don't-grab from the old corpus
- **GRAB (helps the frame, no anchor smuggled):** the frame-relation reading (§1.4); `d_L=r(1+z)` reciprocity; the
  Misner–Sharp marginal relation; the angular-sector derivations (`μ`, the Diophantine triple, the pentagonal algebra)
  that are genuinely native.
- **DO NOT GRAB:** the polynomial ansatz treated as-if-derived (D-POLY-1 open); the **1101/7.004 anchor**; the **BAO/CMB
  scaffolding** (poorly scaffolded — rides the polynomial ansatz + the 1101 anchor; Charles's flag).
- **CMB origin is DEFERRED** (Charles: set it aside for now).

### A.5 Deliverable of Thread A
A DERIVED, data-blind, observer-frame ambient dilation field `φ(r)` (form + asymptotic edge) = **the background a particle
cell embeds in.** Output ratios, not absolute scales (scale-free; the depth is the standing derivation).

---

## THREAD B — the native direct φ-matter SOURCE (particle emergence)

### B.1 What was unfrozen (this session, blind-verified — `udt_phi_blindness_relaxation_results.md`)
The native two-player action, varied w.r.t. φ, gives the DIRECT matter source in the dilation equation:
```
Z(ρ²φ′)′ = 4e^{−2φ}ρ′²  +  α·ξ·e^{αφ}·ρ²·I_r        (I_r = ½∫sinθ f_r²dθ ≥ 0 ; ξ=1)
```
- **φ-blindness ≡ α=0** and is a **CHOSE lever, NOT forced** — its only justification is the depth-shift symmetry, which is
  **BROKEN in Branch P** (where the particle cell lives; `gp_switch_criterion_results.md`). So relaxing it is legitimate-native.
- **The RESTORING channel:** with α≠0, `I_r` sources φ → feeds `e^{2φ}` in the ρ-source → can **SUPPORT `I_r` instead of
  draining it** — the exact thing the matter-structure wall lacked. Open ONLY for α≠0.
- Bonus: a **matter-based L-selector** (cell size set by matter `I_r`, not only boundary data) — bears on the long-open
  L-selection question.

### B.2 The `α` question (OWED derivation — do NOT pick by outcome)
- `α=0` = φ-blind (Branch-P CHOSE). `α=−2` = matter contracts with the PHYSICAL metric (import-tagged as "GR minimal
  coupling", BUT **re-adjudicate**: the shift symmetry that justified stripping the weight is broken in Branch P, so
  `α=−2` may be the honest covariant coupling, not an import — `p16_phi_sourcing_decision_note.md`). Other `α` = FREE;
  no native principle fixes it yet (p16 verdict **C**).
- **TASK:** DERIVE a native principle that fixes `α` in the broken-shift Branch-P regime (an open derivation, not
  forbidden), OR characterize the physics **across `α<0`** (all α<0 open the restoring channel). Never pick `α` because
  it gives the desired answer (imposition trap).
- Sign fact (derived): only **α<0** makes the matter source oppose the geometric one (the restoring / non-monotone regime).

### B.3 The test — does the restoring channel defeat the drain?
The coupled **`(f, φ, ρ)` solve**: with the direct source ON (α<0), does a cell CLOSE with `I_r>0` **supported** (not
drained to 0)? This is the matter-structure wall's escape and the core particle-emergence test.
- **ANTI-HANG (binding):** bound the grid (Nr≤16/24), cap iters, ONE clean process, NEVER background-poll a solve.
- Observe-not-target: the particle is the goal but let it EMERGE; don't sculpt a lump. Data-blind. Verifier-before-record.

### B.4 Deliverable of Thread B
Verdict (blind-verified) on whether matter-sourcing-φ (α<0) lets a cell carry `I_r>0` — i.e. whether the particle-emergence
door the φ-coupling opened actually leads somewhere, or the drain wins anyway.

---

## HOW A + B CONNECT (the payoff)
The derived background (A) is what a particle cell embeds in and couples to; the direct source (B) is HOW the cell's matter
feels that background's dilation. The whole-project goal — **does a particle CELL emerge** — is tested by putting a
matter-coupled cell (B) into the derived background (A) and seeing whether it closes with structure supported. Neither half
is enough alone; that's why this session's cosmology detour (A, done wrong) and the φ-coupling unlock (B) belong together
next session, done right.

## Records / provenance to read first (next session)
`udt_phi_blindness_relaxation_results.md` (B: the source, forced-vs-chose, restoring channel — blind-verified),
`udt_canonical_geometry.md` §1.4/§10.4/§12.7 (A: frame-relation, Misner–Sharp, the polynomial + D-POLY-1),
`udt_max_distance_invariance_FRAME.md` banner (the corrected frame; the error not to repeat), `gp_switch_criterion_results.md`
(shift broken in Branch P), `p16_phi_sourcing_decision_note.md` (the α-weight adjudication, verdict C).
NEGATIVES_REGISTRY: the "no homogeneous universe" entries are PHYSICAL-FIELD-layer, NOT blockers on the frame-relation.
