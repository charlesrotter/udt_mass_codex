# RESULT — the native UDT equations forbid a homogeneous redshifting universe: positional dilation FORCES a center

**Date:** 2026-07-07 (PM) · **Mode:** OBSERVE/derive → blind-verified · **Author:** Claude Opus 4.8 (1M).
**Status: BANKED NEGATIVE (blind-verified), scoped by its premise set.** Data-blind (no 1101/7.004/x_c). Arose from
testing Charles's "no-preferred-frame → homogeneous universe" reframe (`archive/udt_max_distance_invariance_FRAME.md`).

> **⚠ FRAME NOTE (2026-07-07 PM-3, added after the SNe review).** This result is about the **PHYSICAL-FIELD layer** —
> whether the native equations admit a homogeneous φ-FIELD sourced on space (static). It does **NOT** refute the
> *operative* reading of UDT's redshift, which is a **FRAME-RELATION** (`1+z=e^{φ(r)}`, observer-centered;
> `udt_canonical_geometry.md` §1.4 + the shell-theorem note): every observer sees the identical isotropic law, each at
> their own `φ=0` — no preferred frame, no cosmic center. The "positional dilation FORCES a preferred CENTER /
> Copernican" reading that motivated this doc was a **category error** (over-literalizing the frame-relation as a
> physical field) and is **RETRACTED at the frame level**. The physical-field statements below stand on their own terms
> but are NOT the operative cosmology. See `archive/udt_max_distance_invariance_FRAME.md` banner.

## The result
**Within UDT's native (φ-blind-matter) frame, there is NO homogeneous, isotropic, static solution carrying positional
redshift.** Positional dilation (redshift-with-distance) is structurally incompatible with the cosmological principle:
it FORCES a preferred center. The only homogeneous static solution the equations admit is the redshift-FREE product
`R^{1,1}×S²(ρ₀)` (φ=const, ρ=const, σ=0) — no redshift, nothing to observe.

## The mechanism (one CAS-verified equation)
The native φ-equation rewrites EXACTLY as
```
(ρ²φ′)′ = (4/Z)·e^{−2φ}·ρ′²   ≥ 0     (Z>0)      [Eq-A′]
```
and it is **source-free** — matter σ enters ONLY the ρ-equation (matter is φ-blind), never Eq-A′. So `ρ²φ′` is monotone
non-decreasing and cannot be flattened by any matter content. Consequences (all blind-verified):
- **φ cannot be homogeneous while carrying redshift.** Homogeneity/constant-curvature with a redshift gradient is
  impossible; only φ=const (⇒ ρ′=0, the redshift-free cylinder) survives. Holds in BOTH branches (G: `(ρ²φ′)′=0`; P).
- **de Sitter is FORBIDDEN** (both branches). ρ=r, φ=−½ln(1−kr²) fits the B=1/A metric form but fails Eq-A′: at r→0,
  LHS=0 but RHS=4/Z>0; the required "constant" 1/Z runs r-dependent (0.008→2.3 over r=0.1–0.7 at k=1). UDT does NOT
  reduce to the de Sitter static patch — a clean place UDT DEPARTS from GR (the positive S²-curvature source in Eq-A′
  has no GR-vacuum counterpart).
- **Einstein-static (S³) is EXCLUDED, not missed** (the verifier's key check): a closed slice pins `ρ²φ′→0` at both
  poles ⇒ (monotone) `ρ²φ′≡0` ⇒ ρ′≡0 ⇒ no S³; and φ=const on it ⇒ no redshift anyway. Not a counterexample.
- **The ρ-oscillation / discrete ladder is a CENTERED-CELL artifact** — it lives off the core + seals (inhomogeneous
  boundary data); homogeneity removes them and forces ρ′=0. No homogeneous analog. (Data-blind runs: ρ monotone/
  single-hump, not multi-node.)

## Provenance / verification
- Solve: agent `acb3d2174287638fa` (from-scratch Ricci, CAS + bounded numeric, data-blind).
- **Blind adversarial verifier: agent `a1714073a41818ab5` — PASS.** Independently re-derived Eq-A′ from
  `cell_solver_universe_T3.py:79` (`code_φ'' − claimA = 0`); confirmed source-free; CLOSED the Einstein-static gap
  (excluded, not missed); confirmed de Sitter forbidden in both branches; verdict SOLID within the φ-blind frame.

## PREMISE SET (for NEGATIVES_REGISTRY — the negative loses authority if any is revised)
1. **Matter is φ-blind** (σ absent from the φ-equation) — DERIVED but **CONDITIONAL on the R1 weight + P5 shift levers,
   both tagged CHOSE** (`native_field_equations_constrained_two_player_results.md` §4,§7). **THE load-bearing premise.**
   If matter sources φ (relax R1+P5 — reopens the `e^{2φ}T` coupling previously tagged non-native import), on a closed
   slice a sign-varying source could meet `∮RHS=0` and possibly restore a homogeneous redshifting configuration.
2. **Round / isotropic** (Branch-P `h_AB=ρ²Ω`) — correct sector for an isotropic question (not a suppressed DOF);
   non-round breaks isotropy so cannot rescue a homogeneous-isotropic universe.
3. **STATIC** — genuine FRW homogeneity is TIME-DEPENDENT and lives OUTSIDE this static frame (untested door).
4. `Z>0` (Z∈{1,8} tested; result Z-independent).

## THE FORK — ⚠ SUPERSEDED (2026-07-07 PM-3, see the FRAME NOTE at top)
> **This cosmology fork is MOOT.** It rests on the physical-field reading of this doc; once UDT's redshift is read as
> the operative **FRAME-RELATION** (`1+z=e^{φ(r)}`, observer-centered — `udt_canonical_geometry.md` §1.4), there is no
> preferred frame, no cosmic center, and no Copernican problem → no centered-vs-homogeneous fork to make. Kept only as
> the record of the (now-dissolved) fork. The live forward thread is the φ-coupling / particle-emergence door
> (`udt_phi_blindness_relaxation_results.md` §3).

1. **Accept a CENTERED universe** — the equations support it; no-preferred-frame holds LOCALLY (SR boosts) not
   cosmically; PREDICTS a cosmic center → large-scale anisotropy (preferred axis / hemispherical asymmetry — ties to
   the CMB-anomaly question). Least premise-violence; keeps positional-redshift core. **[Driver's recommendation.]**
2. **Relax φ-blindness** (matter sources dilation) — could restore homogeneity but reopens a non-native import.
3. **Go time-dependent** (non-static / FRW-like) — unexplored; drifts toward expansion cosmology, against UDT's
   positional-redshift founding idea.

## Bearing on the x_max frame
The **homogeneous / no-preferred-frame reading** of `archive/udt_max_distance_invariance_FRAME.md` is **REFUTED natively** (given
φ-blindness). The **asymptotic-edge** piece survives but only in the CENTERED solution (φ→∞ at infinite proper
distance; NOT a finite de Sitter horizon). The invariant-finite-`x_max` picture is not realized. Frame → centered.
