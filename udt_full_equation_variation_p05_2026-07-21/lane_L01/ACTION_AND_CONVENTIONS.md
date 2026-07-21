# P05-L01 action and conventions

This is a conditional mathematical lane, not a selected or native UDT law.

## Premise class

- regular four-dimensional Lorentzian metric;
- Levi-Civita connection;
- metric-only, local, parity-even curvature-square bulk inventory;
- exact pre-scale Common-Scale Neutrality;
- unrestricted variation of all ten covariant metric components before reduction; and
- no source or carrier.

The conditional action family is

```text
S_L01[g] = integral_M sqrt(|g|) [alpha C_abcd C^abcd + beta E4] d^4x
E4 = R_abcd R^abcd - 4 R_ab R^ab + R^2.
```

`alpha` and `beta` are symbolic and unnormalized. The curvature sign convention and variation
variable are exactly those registered in `../PREREGISTRATION.md`; in particular,
`h_ab = delta g_ab`.

## What the variation supplies

For the registered convention,

```text
delta S_bulk = integral_M sqrt(|g|) (-2 alpha B^ab) h_ab d^4x
               + integral_boundary Theta,
B_ab = (nabla^c nabla^d + 1/2 R^cd) C_acbd.
```

Thus `B_ab = 0` is the conditional metric bulk equation when `alpha` is nonzero. The regular
four-dimensional Euler density contributes no bulk metric equation, but its boundary and corner
content is not erased.

The ungauge-fixed fourth-order operator is degenerate under diffeomorphisms and Weyl rescalings. On
the explicitly diagnostic de Donder-plus-trace quotient its principal factor is
`alpha (g^ab xi_a xi_b)^2`; this is not a UDT gauge choice or a well-posedness theorem.

## Open stop

The raw boundary current contains independent `h` and `nabla h` channels. Current UDT evidence does
not select their allowed polarization, a finite-cell boundary action, corner terms, orientation
normalization, or equations for any independent `phi`, coframe, projector, multiplier, bridge, or
connection field. Therefore this lane is bulk-exact but not a complete differentiable action.
