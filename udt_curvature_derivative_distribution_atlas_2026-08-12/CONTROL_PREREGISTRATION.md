# Numerical-control preregistration

Date: 2026-08-12  
Parent preregistration commit: `2d50285b`

This file fixes numerical controls before any curvature-derivative outcome is evaluated.

## Production route

Production uses Torch float64 automatic differentiation through the third metric jet. Covariant
derivatives are assembled from the differentiated coordinate tensors and the Levi-Civita
connection before contraction. Calculations are sequential on CPU; no GPU or batching changes the
mathematical object.

## Independent route

The independent NumPy implementation uses:

```text
inner fourth-order curvature step: 2e-4
outer fourth-order derivative ladder: 8e-3, 4e-3, 2e-3
reporting outer step: 4e-3
```

The outer stencil differentiates the independently constructed covariant curvature tensors, then
adds the connection correction at the central point. No production derivative tensor or
classification may be imported.

If any full-tensor cross-route error exceeds `5e-3`, or the outer-ladder trend is inconsistent with
the registered tolerance, the affected row is `NUMERICALLY_UNRESOLVED`; the step may not be tuned
after looking at its ownership result.

## Rank and alignment controls

All scalar-gradient rows are normalized only by the largest singular value of the complete
seven-gradient matrix. Rank threshold:

```text
sigma_i / max(1,sigma_max) > 1e-7.
```

Any singular ratio in `(2e-8,5e-7)` makes the rank `NUMERICALLY_UNRESOLVED`. Rank-two subspaces are
compared through orthogonal/Lorentz projectors and principal angles, never by a hand-picked basis.

For each derivative Gram endomorphism:

```text
registered block residual <= 2e-6
pair/screen normalized spectral gap >= 2e-5
```

The fivefold unresolved band applies to both gates.

## Algebra diagnostic

The generated matrix-algebra dimension is computed from words in the three Gram endomorphisms,
starting from the identity and closing under left multiplication until the numerical span rank
stops changing or reaches 16. Word order is breadth-first and fixed as

```text
K_Riem, K_Ric, K_Weyl.
```

Rank threshold is `1e-8` after Frobenius normalization of each nonzero word. This diagnostic may
report reducible/irreducible-looking finite-dimensional structure but cannot by itself select a
physical `2+2` grouping.

## Stratified exact/replay anchors

The following source identities and points are frozen as readable diagnostics; they do not replace
the full 1,221-jet replay:

```text
R17_M1_N at p,q,r
R17_M0_P at p
TL_E00 at p,q,r
TL_EP20 at p
G75_AM_S01_E05:A03 at C0,CMINUS
G75_AM_S05_E20:A03 at CPLUS
G75_AM_S01_E05:A04 at C0
G75_AM_S05_E20:A04 at CPLUS
G75_AM_S21_E50:A04 at C0
A05 distinct controls C0,CMINUS,CPLUS
```

The G85 identities use the parent atlas naming convention. A missing listed identity is a hard
failure, not permission to substitute a favorable case.

## Resource and stopping contract

No scientific conclusion depends on wall-clock duration. The run may be checkpointed by exact
identity and resumed. Stop only for nonfinite tensors, memory pressure above safe workstation
headroom, a reproducible implementation failure, or explicit user interruption. Refactoring may
change computational organization but not the registered tensors, invariant family, jet universe,
or thresholds.

