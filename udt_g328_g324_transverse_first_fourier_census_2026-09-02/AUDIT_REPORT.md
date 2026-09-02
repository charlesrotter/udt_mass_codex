# G328 audit report — primitive transverse Fourier census

Date: 2026-09-02
Status: `INTERNAL_VERIFIED_PENDING_EXTERNAL_REVIEW`

## Landing

```text
PRIMITIVE_TRANSVERSE_FOURIER_SECTOR_CLOSES_MODULO_PERIODIC_GAUGE
__TWO_PHYSICAL_MODE_FAMILIES__EXACT_BRANCH_CLASSIFICATION
__NO_FULL_STABILITY_CLAIM
```

## What was learned

The complete primitive Fourier eigenspace directed along a transverse compact circle closes under
the current owner-provisional bounded equation. Starting from all ten metric components, four
arbitrary periodic gauge functions, and every constraint, the quotient contains exactly two
physical second-order master amplitudes.

The anisotropic background splits their time operators. With
`nu=k/C_perp` and `zeta=3 nu T^(1/3)`, the even mode has the exact `J0,Y0` basis and the odd mode
has the exact `J3,Y3` basis. Including two real phases, the physical eigenspace has eight real
constants. The four past branches are finite, logarithmic, proportional to `T`, and proportional
to `T^-1`. All four future branches oscillate with relative `T^-1/6` envelope. No endpoint branch
was filtered.

The nonzero Fourier Bianchi identity forces `delta R=0`; this does not remove G325's homogeneous
connected-scalar mode. Exact intrinsic slice-curvature combinations are proportional to the two
gauge-invariant masters, so neither family is a coordinate artifact.

## Evidence

- frozen preregistration commit `96298482`;
- production direct four-dimensional first variation: 90 exact assertions;
- implementation-distinct Gauss--Codazzi/ADM reconstruction: 23 exact assertions;
- seven hostile mutations rejected, including omitted lapse, affine fake gauge, wrong gradient
  power, false zero-mode scalar removal, lost branch, wrong dimension, and sign-flipped
  reconstruction;
- aggregate package verifier: 71 assertions, four literal commands replayed in a clean writable
  copy from the vendored SymPy runtime, and three canned-answer substitutions rejected;
- exact current-premise verifier passed on 310 rows through G327;
- repository suite: `219 passed, 1 known xfailed`.

## Four gates

1. **Preregistered:** yes, before production at `96298482`.
2. **Full bounded space:** yes for the complete primitive `y` Fourier eigenspace on compact
   positive-time intervals; no broader spectrum claim.
3. **Independent:** yes, direct spacetime connection variation versus spatial ADM reconstruction.
4. **Premise audited:** yes; the provisional ownership of the equation and all excluded imports
   remain visible.

## Boundary

This advances the inhomogeneous census beyond G327, but it is not full linear stability. Oblique
wavevectors, multimode estimates, nonlinear coupling, and endpoint admissibility remain open, as
do physical occupancy, topology selection, scale, observations, matter/mass, history selection,
and physical `X_max`.

No UDT metric coefficient, reciprocal-kernel operator, angular-sector formula, or field equation
was modified. External adversarial review is pending.
