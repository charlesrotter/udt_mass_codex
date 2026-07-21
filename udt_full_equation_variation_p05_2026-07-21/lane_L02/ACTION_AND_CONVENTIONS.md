# P05-L02 action and conventions

This is a conditional post-scale comparison lane, not a selected or native UDT law.

## Premise class

- a regular four-dimensional Lorentzian metric representative and physical scale have already been
  supplied by an as-yet-open bootstrap/selection stage;
- Levi-Civita connection;
- metric-only, local, diffeomorphism-covariant bulk dynamics with at-most-second-order metric
  equations;
- unrestricted variation of all ten covariant metric components before reduction; and
- no source or carrier.

The conditional action family is

```text
S_L02[g] = integral_M sqrt(|g|) [kappa (R - 2 Lambda) + beta E4] d^4x
E4 = R_abcd R^abcd - 4 R_ab R^ab + R^2.
```

`kappa`, `Lambda`, and `beta` are symbolic and unnormalized. `Lambda=0` remains one unselected
subcase. The curvature sign convention and variation variable are exactly those registered in
`../PREREGISTRATION.md`; in particular, `h_ab = delta g_ab`.

## What the variation supplies

For the registered convention,

```text
delta S_bulk = integral_M sqrt(|g|) [-kappa (G^ab + Lambda g^ab)] h_ab d^4x
               + integral_boundary Theta.
```

Thus `G_ab + Lambda g_ab = 0` is the conditional vacuum metric bulk equation when `kappa` is
nonzero. The regular four-dimensional Euler density contributes no bulk metric equation, but its
boundary and corner content is retained.

The ungauge-fixed second-order operator is diffeomorphism-degenerate. On the explicitly diagnostic
harmonic quotient its principal factor is `kappa (g^ab xi_a xi_b)`; this is not a UDT gauge choice,
physical representative selection, or well-posedness theorem.

## Open stop

The raw EH boundary current is present. A GHY-like completion and Dirichlet data are recorded only
as a standard comparison and are not adopted. Current UDT evidence does not select the finite-cell
polarization, boundary action, corners, reference normalization, physical representative, or
equations for extra fields. Therefore this lane is formally bulk-exact inside its post-scale premise
class but not a complete differentiable UDT action.
