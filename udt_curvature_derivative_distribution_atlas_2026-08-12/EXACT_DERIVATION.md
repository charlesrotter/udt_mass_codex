# Exact objects and contraction conventions

This package evaluates local metric concomitants on supplied third-order metric jets. Indices are
raised and lowered with the supplied Lorentz metric `g`; the connection is its Levi-Civita
connection.

## Scalar-gradient distribution

The declared scalar family is

```text
R,
tr[(g^-1 Ric)^2],
tr[(g^-1 Ric)^3],
C_ab^cd C_cd^ab,
(*C)_ab^cd C_cd^ab,
C_ab^cd C_cd^ef C_ef^ab,
(*C)_ab^cd C_cd^ef C_ef^ab.
```

The last four are real representatives proportional to the real and imaginary parts of the usual
self-dual Weyl traces. Constant proportionality factors do not alter the span. For each scalar
`I_A`, form the covector `dI_A` and metric-raised vector `grad(I_A)`. Their unweighted span is

```text
D_SPI = span{grad(I_A)}.
```

No scalar combination or preferred gradient is selected. A rank-two span is compared with the
registered pair and screen projectors only after its rank and Lorentz signature are determined.

## Curvature-derivative Gram tensors

The three symmetric covariant tensors are

```text
K_Riem_ab = (nabla_a R_cdef)(nabla_b R^cdef),
K_Ric_ab  = (nabla_a Ric_cd)(nabla_b Ric^cd),
K_Weyl_ab = (nabla_a C_cdef)(nabla_b C^cdef).
```

Each is converted to the endomorphism `g^-1 K`. Registered-split ownership requires both:

1. pair/screen block preservation below the frozen residual; and
2. disjoint pair and screen spectra above the frozen gap.

A simple four-eigenvector frame alone is not counted as ownership because it still permits several
inequivalent groupings into two planes.

The completion layer diagonalizes each mixed endomorphism and records its four complex
eigenvalues, numerical rank, clustered algebraic/geometric multiplicities, Jordan defect, and the
real invariant subspace belonging to each spectral block. If four simple real eigenlines survive,
all six unordered two-line sums are retained as intrinsic candidate two-planes. If a repeated
scalar eigenspace survives, the whole repeated block is intrinsic but arbitrary subplanes inside
it are not. Complex-conjugate eigenlines are joined into their real invariant plane.

## Production derivative

Production differentiates the coordinate tensors with automatic differentiation and then applies
the connection corrections. For example,

```text
nabla_a Ric_bc = partial_a Ric_bc
                 - Gamma^f_ab Ric_fc
                 - Gamma^f_ac Ric_bf,
```

and the same correction is applied to all four covariant indices of Riemann and Weyl. The full
tensor identities are checked after this assembly.

## Independent derivative

The independent implementation reconstructs metric connection and curvature through fourth-order
finite differences with inner step `2e-4`. It then differentiates the independently reconstructed
curvature using outer steps `8e-3`, `4e-3`, and `2e-3`, reporting the `4e-3` tensor. It independently
applies all connection corrections and contractions.

The independent route never imports a production derivative tensor or production classification.
The saved arrays allow full-tensor rather than scalar-only comparison.

The independent spectral layer uses SciPy eigensystem, nullspace, QR, and assignment algorithms
rather than the production NumPy SVD/eigensystem path. It compares unordered eigenvalue sets and
unordered spectral/projector sets, so no favorable eigenvector ordering is assumed.
