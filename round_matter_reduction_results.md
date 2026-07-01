# Round S² Winding Matter — reduction + why rigid collapses + the free-field solver (Class A)

**Date:** 2026-07-01. **Provenance:** derivation by Charles (in-session); driver CAS-confirmed
(`verify_matter_reduction.py` — every claim TRUE); blind-verify owed on the eventual discreteness FINDING,
not on this reduction. **Status:** matter reduction DERIVED+verified; the free-field 2-D eigenproblem is the
next build. Frozen model = `discreteness_preregistration.md` (Class A: closed topological cell modes).

## The winding carrier
`n = (sin f(r,θ) cos Nψ, sin f(r,θ) sin Nψ, cos f(r,θ))`, degree N, `f(r,0)=0, f(r,π)=π`. Rigid hedgehog = `f=θ`.
Derivative norms (CAS): `|∂_r n|²=f_r²`, `|∂_θ n|²=f_θ²`, `|∂_ψ n|²=N²sin²f`; area norms
`|∂_θ n×∂_ψ n|²=N²f_θ²sin²f`, `|∂_r n×∂_ψ n|²=N²f_r²sin²f`.

## Reduced matter Lagrangian (round, per 4π; matter uses the UNDILATED radial channel ḡ^{rr}=1, transverse ḡ^{θθ}=1/ρ²)
    L_m = -(ξ/2)(ρ² I_r + I_θ + N² I_s) - (κN²/2)(I_4r + I_4θ/ρ²)
with `I_r=½∫sinθ f_r²dθ`, `I_θ=½∫sinθ f_θ²dθ`, `I_s=½∫(sin²f/sinθ)dθ`, `I_4θ=½∫(sin²f/sinθ)f_θ²dθ`,
`I_4r=½∫(sin²f/sinθ)f_r²dθ`. Rigid `f=θ` → `I_r=0, I_θ=1, I_s=1, I_4r=0, I_4θ=1` → `L_m=-(ξ/2)(1+N²)-κN²/(2ρ²)`.

## The ρ-source (CAS-confirmed)
    ρ''_matter = (e^{2φ}/4)( ξ ρ I_r  −  κ N² I_4θ / ρ³ )
- `+ξρI_r` = OUTWARD (stabilizing) — present ONLY if the matter develops RADIAL structure `I_r>0`.
- `−κN²I_4θ/ρ³` = INWARD (collapsing).
- **Rigid hedgehog has `I_r=0`** → only the inward term → **the round cell COLLAPSES (verified numerically).**
  This is NOT a sign bug; rigid round winding is simply too constrained to make a stable cell.
- Balance (where a finite size can EMERGE, not be imposed): **ρ⁴ ~ κN²I_4θ/(ξI_r).**

## Matter field equation (f must be SOLVED, not prescribed)
    ∂_r(A f_r) + ∂_θ(B f_θ) − (N²sin f cos f/sinθ)(ξ + κ f_r² + κ f_θ²/ρ²) = 0
    A = ξρ²sinθ + κN²sin²f/sinθ ,   B = ξsinθ + κN²sin²f/(ρ²sinθ)
⇒ a **2-D finite-domain problem in (r,θ)** coupling `f(r,θ)` to the 1-D geometry `φ(r), ρ(r)`.

## NEXT BUILD (Class A, minimally-free field) — the honest test
Solve the coupled system on a FINITE MIRRORED radial domain:
- fields: `φ(r), ρ(r)` (1-D) + `f(r,θ)` (2-D), fixed `Z_φ, ξ, κ, N`;
- angular pole BCs `f(r,0)=0, f(r,π)=π`;
- radial MIRROR seal BCs (`φ'=ρ'=0`, and the appropriate `f`-mirror) at the seals — unless testing the charged
  Class-B seal;
- **do NOT insert `I_r` by hand — let the BVP decide if `f` develops radial structure `I_r>0`.**
- Look for ISOLATED cell lengths where `φ, ρ, f` close simultaneously (the mirror-seal conditions). Unlabeled.

**Acceptance (pre-registered):** fixed `Z_φ, ξ, κ, N`, no per-solution retuning, no particle labels.
- If it STILL collapses with free `f(r,θ)` → rigid-round collapse was not an artifact; record the scoped negative
  ("round winding, even minimally free, does not stabilize finite cells") and go to the next-freer sector / off-round.
- If ISOLATED finite modes appear → the FIRST real discreteness signal (still Class A: closed modes, `q=0`, NOT
  particle charge).

## Scope / premises
Rigid-round collapse is verified but SCOPED to rigid purely-angular matter. `L_2` is source-free ONLY under the
rigid reduction (`I_r=0`); a free `f(r,θ)` reactivates the `ξρ²I_r` channel. Not yet tested: free profile (this
build), radial/off-round matter modes, seal/core stabilization. `ξ=κ=1` are the repo "units"; `N` fixed per run.

## VERIFIER
- CAS (driver, `verify_matter_reduction.py`): n-derivative + area norms; reduced L2/L4; rigid limit; ρ-source
  `e^{2φ}/4(ξρI_r−κN²I_4θ/ρ³)`. ALL confirmed. Blind-adversarial owed on the DISCRETENESS finding (next build).
