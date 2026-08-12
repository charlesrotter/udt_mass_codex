# G81 exact derivation — screen-basis covariance of reverse Jacobi reciprocity

## Scope

This is a geometric statement for a fixed regular null segment and its mathematical reverse. It
does not choose that segment, its metric profile, its endpoint, or a physical observable.

Let `D_fwd` map receiver screen-angle seeds to source transverse separation. Let `D_rev` map source
screen-angle seeds to receiver transverse separation. With receiver frequency normalized to one
and source frequency `Z`, the Wronskian pairing gives, in the carried unrotated screens,

```text
D_rev = Z transpose(D_fwd).
```

Now rotate the reverse source seed basis by the orthogonal matrix `A` and independently rotate the
receiver projection basis by the orthogonal matrix `B`. Coordinate columns transform on the right
by `transpose(A)` and output rows transform on the left by `B`, so

```text
D_rev_AB = B D_rev transpose(A)
         = Z B transpose(D_fwd) transpose(A).
```

This is basis covariance, not a new physical effect. It does not permit diagonalizing `D_fwd`: the
complete off-diagonal map must transform.

Taking determinants and using `det(A)=det(B)=1` gives

```text
sqrt(abs(det(D_rev_AB))) = Z sqrt(abs(det(D_fwd))).
```

The endpoint frequency reversal independently gives `Z_rev=1/Z` and therefore
`phi_rev=-phi_fwd` for `phi=log(Z)`.

## Exact nonradial frame

In receiver orthonormal-triad coordinates, G81 fixes

```text
n  = (12,3,4)/13
s1 = (0,4,-3)/5
s2 = (-25,36,48)/65.
```

Direct dot products give unit norms, pairwise orthogonality, and `s1 cross s2 = n`. Hence C1 is a
genuine three-directional ray with a complete oriented screen, not a radial control relabelled.

## Observed finite-control values

At the finest registered production step:

- C0 matrix covariance residual: `1.0086332137876813e-14`.
- C1 matrix covariance residual: `3.931585029333395e-15`.
- C1 forward off-diagonal norm: `1.1801666864663825e-3`.
- C1 endpoint moved from `(theta,psi)=(pi/2,0)` to approximately
  `(1.7493671390260097,0.23079074045919012)`.

The separate direct-Christoffel neighboring-ray calculation obtained C0/C1 rotated covariance
residuals `1.3498538204686179e-8` and `1.1585881402639625e-8`, respectively.

## Maximum conclusion

`DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS`.

The derivation is a control-scoped representation of generic Jacobi/Wronskian reciprocity. It is
not a UDT-specific selector, future signal, physical endpoint, `Xmax` relation, source law, action,
matter result, or CMB prediction.
