# G210 preregistration — spatial-volume robustness

Date: 2026-08-21

## Exact tests

1. **Unique determinant decomposition.** For positive spatial matrices `H,K`, prove

   ```text
   sigma=(1/6)log(det(K)/det(H)),
   K=exp(2 sigma) K_bar,
   det(K_bar)=det(H),
   ```

   and uniqueness. Do not call the determinant-one remainder fully classified by G207/G208.
2. **Complete local scalar algebra.** For arbitrary positive supplied `H`, lapse `f`, and shift `b`,
   derive the ADM block for

   ```text
   g_sigma,b(alpha dt+v)^2=-f alpha^2+exp(2 sigma)h_A(v+alpha b,v+alpha b),
   ```

   including determinant, signature, inverse, and temporal `dt`.
3. **Exact causal law.** Prove that spatial volume preserves the shift center and rescales every
   causal-ellipsoid width by `exp(-sigma)`. Derive the radial covector inequality and recover on
   unshifted G205

   ```text
   |dr/dt| <= f exp(-sigma).
   ```
4. **Growth-controlled global causality.** On each finite time slab, assume the exact radial speed
   envelope has divergent Osgood integral. Prove or refute that `t` remains Cauchy. Include every
   globally lower-bounded `sigma` on unshifted G205 as a corollary.
5. **Static survivor.** Prove or refute two-ended null completeness for every smooth static G205
   `sigma>=sigma_min`. Use the conserved energy and exact affine radial bound; do not infer
   timelike or spacelike completeness.
6. **Compact-time-live survivor.** Let `sigma=0` outside `|t|<T`, with a global lower bound and
   bounded `partial_t sigma` inside. Derive the exact null-energy equation and prove or refute
   global hyperbolicity and null completeness.
7. **Smooth static failure witness.** Set `sigma=-phi` on each registered G205 profile. Prove center
   smoothness and global hyperbolicity. Derive radial null

   ```text
   dr/dlambda=+-E exp(-sigma),
   dlambda/dr=exp(sigma)/E,
   ```

   and test finite affine reach through `integral exp(-phi) dr`.
8. **Completed-pair response.** Derive the full pullback before readout and classify spatially
   bearing, coordinate-static unshifted, coordinate-static shifted, Eulerian-normal, and generic
   germs. Spatial determinant change must not be equated with universal pair response.
9. **Dependency boundary.** Prove the spatial-only scale is equivalent algebraically to a common
   conformal rescaling plus a compensating lapse rescaling, hence distinct from G206 at fixed lapse.

## Certification contract

- Production: exact symbolic determinant/inverse, unique determinant split, cone, energy, radial
  null, and pair formulas.
- Independent: separate exact-rational implementation with at least 10,000 distinct positive
  spatial-matrix/scale/shift/pair cases and no production import.
- At least four 120-digit outer-tail controls covering survivor and failure integrals.
- At least 22 hostile catches spanning dimension factors, signs, determinant, causal width, energy,
  smoothness, global/affine typing, pair strata, evidence ceiling, history selection, and `X_max`.
- Saved artifacts replay byte-identically with no writes.
- Fresh external adversarial review before final banking.

## Falsification

The strongest candidate landing fails if the `1/6` determinant factor or uniqueness is wrong; if
the local determinant, inverse, temporal covector, cone center, or width is wrong; if a declared
lower-bounded static or compact-live survivor is null incomplete; if `sigma=-phi` is not smooth,
loses global hyperbolicity, or remains null complete; or if generic completed pairs fail to hear
the mode before readout.

## Scope lock

This is the complete one-dimensional local spatial-volume scalar and bounded G205 global
subclasses. It does not classify arbitrary determinant-one spatial histories, lapse freedom,
unrestricted live fields, timelike/spacelike completeness, maximal extension, physical history
selection, transfer, observations, action/source/matter, or `X_max`.
