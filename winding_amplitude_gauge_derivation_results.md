# Does the winding AMPLITUDE have native dynamics, or is |n|=1 fixing a pure gauge mode? — derivation

**Driver:** Claude (Opus 4.8, 1M). **Date:** 2026-06-29. **Mode:** DERIVE (native, Principle 1). DATA-BLIND.
**Status:** RESOLVED at the level the action can resolve it; blind-verified CONFIRMED. The remaining piece is a
canon-level modeling decision for Charles (layer-B), NOT a numerics question.

## Why this was asked
The D1 fix (re-pose the underdetermined static solve as a DETERMINED system) needs a decision on the defect
CORE: the gravitating-global-monopole literature regularizes its core by letting the scalar AMPLITUDE vanish
(profile h→0); our solver holds |n|=1. The question — instead of choosing by fiat — is whether UDT's own
action gives the winding amplitude any dynamics (so the metric/action decides). Charles's framing: "let the
metric tell us directly / determine it from the GR corpus + positional dilation."

## Result — TWO LAYERS

### LAYER-A (airtight, blind-verified by independent sympy): the amplitude is an EXACT gauge null direction.
The physical matter field is `nhat = n/|n|` (a unit S² 3-vector; `free_s2_matter.py:76-120`). Writing the raw
field `n = A(x)·u` with `|u|=1` and `A=|n|` an independent positive field:
- `nhat` and its tangential derivative `d nhat = dn/|n| − n(n·dn)/|n|³` (the code's `proj()`) are **pointwise
  invariant under any local rescaling n→λ(x)n** — symbolically exact.
- Hence `L2 = -(ξ/2) g^{mn} d_m nhat·d_n nhat` and the area-form `L4` (`whole_metric_3d_matter.py:80-87`) are
  **identically independent of A and ∂_μA**: `∂L/∂A ≡ 0`, `∂L/∂(∂_μA) ≡ 0` (sympy, 1D and 2D). The amplitude
  has **no equation of motion** — it is an exact null/gauge direction the action does not depend on.
- **The e^{2φ} positional-dilation weight gives the amplitude NO dynamics** (the answer to Q2): `e^{2φ}` is a
  φ-only coefficient (φ a separate field) multiplying an A-free Lagrangian; nothing anywhere (matter EL,
  gravity source −κ8·f·T, φ-EOM, X-kinetic) pairs e^{2φ} or φ with |n|. It re-weights *where the direction
  field's gradient energy concentrates*, but is structurally incapable of being an amplitude potential V(|n|).
- The `wbc·(|n|²−1)` residual row is a **pure gauge-fix** (removes the null direction so the Newton Jacobian
  is non-singular there), not a physical Lagrange condition — it never enters T or any field equation.

**So the metric/action DID tell us directly (Q1): UDT-as-derived has no amplitude DOF; a vanishing-amplitude
core-regularizing profile is NOT available natively.** The degree-1 S² hedgehog `n=x/r` core is a genuine
TOPOLOGICAL singularity (Barriola–Vilenkin): the metric warp / φ-profile / areal coordinate can make the
ENERGY integral finite, but **cannot make `nhat` continuous at r=0** — that is a property of the map, not the
measure. Getting the profile path requires **importing a linear-σ / Mexican-hat V(|n|)** — an SM-Higgs-type
Category-B mechanism import, forbidden by the purity discipline unless forced.

### LAYER-B (the genuinely open part, blind-verified): the unit-field posit is NOT derived.
- F2-1 (`F2_matter_action_forcedness_results.md:232`) labels "field = unit 3-vector" as an **upstream POSIT,
  not re-opened**. No record derives that matter MUST be a nonlinear-σ (unit) model vs a linear-σ (amplitude +
  V) model. F2's "forbidden V(n)" is a **direction** potential (constant by SO(3)-transitivity on the *unit*
  sphere) — it does **NOT** forbid an amplitude potential V(|n|).
- **Honest canon correction (chose-or-derived):** unit-ness has been attributed to canon **C-2026-06-14-1**,
  but that canon's actual proposition is "B=1/A sourced by the angular sector" (`CANON.md:116-165`) — it merely
  *uses* a unit field. **There is no canon entry whose proposition is "matter must be unit."** So unit-ness is
  an embedded, never-independently-derived premise mis-tagged as canon-derived. This is a FREE/CHOSE, not a
  DERIVED — surfaced for Charles's premise ledger.
- Scope note: an **S³/π₃ (Skyrme)** carrier WOULD regularize the core with a profile Θ(r)→0 while keeping
  |n|=1 (no amplitude needed) — but S³ is itself undecided/not derived; it widens the same open fork, it does
  not give a native S²-carrier regularization.

## IMPLICATION for the D1 fix (the principled default)
- **Layer-A forecloses the "native profile" path** — so the D1 fix proceeds on the **RIGID / intrinsic-S²
  singular-core path**: re-pose as a DETERMINED square system (PDE residual at all interior nodes + sufficient
  endpoint BCs, rows==unknowns, one residual S(u)=0), with origin regularity imposed on the **direction** field
  per its tensor/vector parity (Boyd) + a finite-core (rc-regularized) inner treatment. The vanishing-amplitude
  treatment is NOT used (it would be an import).
- **This does NOT require Charles to resolve layer-B to proceed** — the rigid path is what UDT-as-derived gives,
  and the alternative is a gated import the purity default disfavors. Layer-B (re-open unit-ness to a linear-σ
  with a real amplitude DOF?) is a genuine **canon-level decision** flagged for Charles, but it is not a blocker.

## Verifiers (verifier-before-record)
- **Derivation:** agent `a803da6bfa9baf8a9`, 2026-06-29 (sympy + code + records).
- **Blind adversarial:** agent `a12f170075b15e875`, 2026-06-29 — **CONFIRMED**. Independent sympy reproduced
  the exact A-independence of L2/L4/area-form; confirmed e^{2φ} never couples to |n|; confirmed the constraint
  is a gauge-fix; scrutinized layer-B hardest and upheld it (unit-ness = upstream posit, F2's V(n) is direction-
  only); found the C-2026-06-14-1 attribution loose (strengthens "genuinely open"); confirmed no native S²-core
  regularization route exists (topological, not measure).
