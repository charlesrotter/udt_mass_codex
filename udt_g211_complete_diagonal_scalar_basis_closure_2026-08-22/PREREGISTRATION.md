# G211 preregistration — complete diagonal-scalar basis closure

Date: 2026-08-22

## Exact tests

1. **Unique supplied-split scalar coordinates.** For positive reference lapse `f`, positive
   reference spatial metric `H`, positive lapse `F`, and positive spatial metric `K`, prove

   ```text
   ell=(1/2)log(F/f),
   sigma=(1/6)log(det(K)/det(H)),
   K=exp(2 sigma) K_bar,
   det(K_bar)=det(H),
   ```

   with uniqueness after the references and split are supplied.
2. **Rank-two basis closure.** Define

   ```text
   Omega=ell,
   q=sigma-ell.
   ```

   Prove `ell=Omega`, `sigma=Omega+q` and

   ```text
   g_ell,sigma,b=exp(2 Omega)[-f dt^2+exp(2q)h_A(dx+b dt,dx+b dt)].
   ```

   The transformation must have rank two. A lapse-only path must lie in this plane rather than
   produce a third diagonal scalar.
3. **Volume/cone coordinates.** Derive

   ```text
   V=ell+3 sigma,
   W=ell-sigma,
   ell=(V+3W)/4,
   sigma=(V-W)/4,
   ```

   where `exp(V)` is the square-root determinant ratio and `exp(W)` is the common causal-width
   factor.
4. **Complete local ADM algebra.** For arbitrary positive supplied `H` and supplied shift `b`,
   derive determinant, inverse, Lorentz signature, and temporal `dt` for both scalar modes.
5. **Causal separation.** Prove the causal center remains `-b`, all widths scale by
   `exp(ell-sigma)=exp(-q)`, and the common factor `Omega` cancels from the cone. On G205 recover

   ```text
   |dr/dt+b^r| <= f exp(-q).
   ```
6. **Causal/global transfer.** Prove `g_ell,sigma,b` and the relative metric `g_q,b` have the same
   unparametrized causal curves. Any Cauchy theorem must be conditional on the supplied `g_q,b`.
7. **Null-affine composition.** Prove for corresponding null affine parameters

   ```text
   dlambda_g=exp(2 Omega) dlambda_q.
   ```

   On static radial unshifted G205 derive

   ```text
   dr/dlambda=E exp[-(ell+sigma)],
   dlambda/dr=exp(ell+sigma)/E=exp(2Omega+q)/E.
   ```

   Register exact same-cone/different-affine controls without promoting them to physical histories.
8. **Completed-pair response.** Derive the full pullback and

   ```text
   T^2=exp(2Omega)[f alpha0^2-exp(2q)h_A(v0+alpha0 b,v0+alpha0 b)],
   Phi=-Omega-(1/2)log[...].
   ```

   Classify common-scale response, relative-mode response, generic response, and exact blind strata.
9. **Ownership ceiling.** Reject lapse, common scale, relative mode, profile, history, or `X_max`
   selection. The diagonal basis is conditional on a supplied calibrated split.

## Certification contract

- Production: exact symbolic scalar maps, determinant/inverse, cone, affine, and pair formulas.
- Independent: separate exact-rational implementation with at least 10,000 distinct positive
  lapse/spatial/shift/pair cases and no production import.
- Four 120-digit G205 radial controls separating common-scale and relative-mode affine effects.
- At least 25 hostile catches spanning rank, coefficients, determinant, inverse, cone, affine,
  pair strata, evidence ceiling, history selection, and `X_max`.
- Saved artifacts replay byte-identically with no writes.
- Fresh external adversarial review before final banking.

## Candidate landing and falsification

Candidate maximum:

```text
COMPLETE_LOCAL_DIAGONAL_SCALAR_SECTOR_HAS_RANK_TWO_AFTER_SUPPLIED_1PLUS3_REFERENCE
__COMMON_SCALE_AND_RELATIVE_SPATIAL_VOLUME_FORM_AN_EXACT_BASIS
__LAPSE_ONLY_IS_NOT_A_THIRD_TILE
__CAUSAL_CONES_DEPEND_ONLY_ON_RELATIVE_MODE_WHILE_NULL_AFFINE_AND_COMPLETED_DEPTH_HEAR_COMMON_SCALE
__NO_PHYSICAL_SCALAR_HISTORY_OR_XMAX_SELECTION
```

It fails if the scalar map is not bijective; if lapse-only supplies a third local diagonal mode; if
the determinant, inverse, cone width, affine weight, or completed-pair formula is wrong; or if the
same-cone controls cannot separate affine behavior.

## Scope lock

This is a complete local scalar-basis theorem only after the `1+3` reference and pair germ are
supplied. It does not classify arbitrary determinant-one spatial histories, unrestricted live null
completeness, timelike/spacelike completeness, maximal extension, foliation ownership, physical
history, transfer, observations, action/source/matter, or `X_max`.
