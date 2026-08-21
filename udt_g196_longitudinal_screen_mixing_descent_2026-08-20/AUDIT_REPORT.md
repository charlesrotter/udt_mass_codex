# G196 audit report — longitudinal screen-mixing descent

Date: 2026-08-21

## Landing

```text
NULL_DIRECTIONAL_DESCENT__FACTORIZATION_AND_NO_CAUSTIC_SURVIVE
```

Current grade:

```text
EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS
```

## What was asked

G196 made the G195 screen-mixing matrix genuinely two-variable: `M=M(eta,z)`. It then rebuilt the
full four-dimensional metric, connection, curvature, and Jacobi map for the same supplied central
outgoing pair. The question was whether spatial gradients add a new independent response, break
the ordered factorization, or create caustics.

## Bounded answer

They do not in this declared family and germ. The metric selects the derivative along the pair's
own outgoing null direction,

\[
D_+=\partial_\eta+\partial_z.
\]

The exact connection and tide are

\[
C_s=2\Omega,
\qquad
T_c=\tau_0I+a^{-4}\left(2D_+S-4S^2-4[S,\Omega]\right).
\]

The coordinate Jacobi operator remains

\[
(D_+-2M^T)(D_++2M)Y=0,
\]

and therefore retains the ordered positive-Gram representation

\[
D=aLK,
\quad L'=-2\bar M L,
\quad K=\int L^{-1}L^{-T}ds.
\]

Consequently `det D>0` at every nonvertex point of a connected regular outgoing-ray interval.

## Evidence

### Exact production

- 17/17 exact assertions passed.
- The script constructs the full metric, inverse, Christoffels, Riemann contraction, connection,
  and tide directly in SymPy.
- Pair pullback, affine ray, frequency, screen connection, directional tide, both factorizations,
  the G195 limit, pure rotation, and positive-Gram template all passed.

### Independent metric-side replay and formula-level IVP regression

The verifier does not import the production script or read its output. It independently reconstructs
second metric jets with Torch `float64` and builds Riemann, the screen connection, and the central
tide by separate index contractions. Its interval Jacobi comparison has a narrower evidence type:
the direct second-order and ordered `L,K` IVPs both use the same separately coded
`candidate_matrices(...)` coefficients. Their agreement is therefore formula-level regression, not
an independent metric-to-Jacobi derivation.

| Gate | Result | Ceiling |
|---|---:|---:|
| histories | 204 | 12 named + 192 seeded |
| assertions | 5,313 | exact frozen count |
| maximum tide error | `8.881784197001252e-16` | `3e-8` |
| maximum connection error | `2.220446049250313e-16` | `3e-8` |
| maximum factorization error | `1.5420713317393364e-11` | `3e-8` |
| minimum sampled nonvertex determinant | `1.7099989610881957e-4` | positive |
| same-ray alias error | `5.551115123125783e-17` | `3e-10` |
| off-ray alias difference | `0.04032` | greater than `1e-4` |

The determinant census is regression evidence. The universal bounded sign result comes from the
exact Gram proof.

### Hostile mutations

All 9/9 frozen mutations were caught: dropping `partial_z`, reversing the null derivative, forcing
symmetry, reversing factor order, assuming commuting transport, reversing the connection sign,
using finite samples as a proof, promoting one-ray equality to global equality, and treating
rotation as independent focusing.

## Premise audit

| Input | Status |
|---|---|
| measured `c_E`, set to one in control units | `OBSERVED` calibration only |
| completed-pair Dual Reciprocity | `WORKING_FOUNDATIONAL_CLARIFICATION` |
| displayed `a(eta),M(eta,z)` coframe | `CHOSE_MATHEMATICAL_FUNCTION_FAMILY` |
| functions `a,A,N,B,R` | `FREE_AND_EXPLORED` |
| central pair and outgoing null germ | `CHOSE_QUERY` |
| connection, tide, factorization, sign theorem | `DERIVED_CONDITIONAL` |
| physical profiles, other directions, transverse dependence, global completion | `OPEN` |
| P1/G116/G189, observations, transfer, source, `X_max` | `OMITTED` |

## Interpretation

This is a real interlocking constraint, not a fitted melody. Once the full metric and pair germ are
supplied, time and longitudinal variation do not enter as two independently adjustable effects.
They collapse into the derivative along that pair's null direction. Yet one ray cannot reconstruct
off-ray field structure; a network of differently directed pairs is the natural adjacent test.

## Maximum conclusion

G196 proves longitudinal directional descent, ordered factorization, and no nonvertex caustic for
one spatially extended affine complete-coframe family and supplied central outgoing germ. It does
not yet prove arbitrary-direction or arbitrary-coframe closure, select physical functions or
observers, derive a global spacetime, or supply observational physics.
