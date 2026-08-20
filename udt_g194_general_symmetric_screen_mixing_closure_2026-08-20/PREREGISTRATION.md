# G194 preregistration — arbitrary smooth symmetric `2 x 2` screen mixing

Date: 2026-08-20

## Whole question and exact bounded regime

Does G193's ordered screen factorization and family-scoped no-caustic theorem survive after the
third independent symmetric screen-mixing entry is freed?

Work on one smooth coordinate neighborhood with coordinates `(eta,z,p,w)`, an interval `I`
containing `eta=0`, and the complete coframe

\[
\begin{aligned}
\theta^0&=a(\eta)\,d\eta,\\
\theta^1&=a(\eta)\,dz,\\
\binom{\theta^p}{\theta^w}
&=a(\eta)\left[
d\binom{p}{w}+M(\eta)\binom{p}{w}(d\eta+dz)
\right],\\
M(\eta)&=
\begin{pmatrix}
A(\eta)&N(\eta)\\
N(\eta)&B(\eta)
\end{pmatrix},\\
g&=-(\theta^0)^2+(\theta^1)^2+(\theta^p)^2+(\theta^w)^2.
\end{aligned}
\]

Here `a` is arbitrary positive `C3` with `a(0)=1`; `A`, `N`, and `B` are arbitrary real `C2`
functions.  No sign, trace, determinant, commutativity, monotonicity, asymptote, relative-strength
law, or observational profile is imposed.  The G193 family is the exact `B=0` subfamily after
`A=sqrt(2) mu` and `N=nu`.

The supplied completed pair is

\[
F(\tau,\sigma)=(\eta=\tau,z=\sigma,p=w=0),
\]

with source vertex at the origin and the `+z` ruler orientation selecting the local outgoing
germ.  Classification is local on connected regular subintervals containing the vertex.

Time-dependent diagonalization may not be used to erase the induced screen connection.  The
calculation stays in the original coordinate screen and must preserve matrix order.

## Metric-led versus template-led

This is metric-led.  The metric, connection, affine ray, parallel screen, curvature tide, and
matrix Jacobi map are reconstructed from the displayed coframe.  G193 is a required regression
limit, not an assumed derivation of the answer.

## Premise and choice ledger

| Item | Status | Role |
|---|---|---|
| `c_E` | `OBSERVED`; set to one in control units | clock/ruler calibration only |
| completed-pair Dual Reciprocity | `WORKING_FOUNDATIONAL_CLARIFICATION` | acts after the full pullback |
| displayed coframe | `CHOSE_MATHEMATICAL_FUNCTION_FAMILY` | bounded extension, not general complete metric |
| `a(eta)>0`, `a(0)=1` | `free-and-explored` plus source-unit calibration | arbitrary common-scale history |
| real `A(eta),N(eta),B(eta)` | `free-and-explored` | all three symmetric screen-mixing histories |
| `C3/C2` regularity | `pinned-by-MATHEMATICAL_OPERATOR_ORDER` | sufficient metric jets and certified residuals |
| symmetric `M` | `CHOSE_BOUNDED_EXTENSION` | full symmetric tile; antisymmetric rotation omitted |
| central pair and `+z` ruler orientation | `CHOSE_QUERY` | fixes one local completed pair and outgoing germ |
| affine frequency and full matrix screen | `DERIVED_CONDITIONAL` | computed from the same metric |
| P1, G116, G189, transfer, observations, `X_max` | `OMITTED` | forbidden construction inputs |

## Whole-space and omitted-sector ledger

The arbitrary function space of positive `a` and real symmetric `M` is treated symbolically inside
the displayed family and sampled by a frozen bounded census.  Omitted are antisymmetric screen
rotation, arbitrary independent screen scale/shear beyond this coframe, spatial dependence, other
complete-coframe functions, other pair germs, singular metrics, disconnected intervals, cut loci,
topology, global completion, observer population, emission, transfer, source physics, action,
dynamics, matter, bootstrap, and `X_max`.

## Preregistered derivation gates

1. Reconstruct `g=E^T eta_4 E`; prove coframe and Lorentzian regularity for every `a>0`.
2. Pull back to the supplied pair and reconstruct its completed clock, ruler, normalized null
   germ, affine ray, and frequency.
3. Derive a parallel orthonormal screen directly.  Do not infer it from G193.
4. Reconstruct the full self-adjoint `2 x 2` tidal matrix, retaining every derivative, square,
   and cross term from `A,N,B`.
5. Test the ordered matrix factorization directly against the reconstructed tide without assuming
   commutativity.
6. Solve or exactly characterize the vertex-normalized matrix Jacobi IVP with
   `D(0)=0`, `dD/dlambda(0)=I`.
7. Classify every determinant-zero/caustic class admitted by this family.  A no-caustic claim
   requires an exact definiteness proof, not a finite census.
8. Characterize cross response and polar rotation without selecting a sign or magnitude.
9. Recover G193 at `B=0`, G192 at `B=N=0`, and the conformal G190 limit at `A=N=B=0`.
10. Independently replay diagonal, scalar, commuting, genuinely noncommuting, rank-changing,
    signed, zero-crossing, and frequency-turning histories without importing production code or
    reading production output.

## Frozen independent census

The independent replay will contain these named classes plus 256 seeded random histories:

- `g193_limit`: `B=0`, nonconstant signed `A,N`;
- `g192_limit`: `B=N=0`, nonconstant signed `A`;
- `conformal_limit`: `A=N=B=0`;
- `scalar_trace`: `A=B` and `N=0`;
- `diagonal_unequal`: nonconstant unequal `A,B` with `N=0`;
- `constant_full_rank`: constant nonzero `A,N,B`;
- `noncommuting_rotating_axes`: varying eigendirections with an explicit nonzero commutator;
- `rank_transition`: `det M` crosses zero;
- `signed_triple_crossing`: all three entries change sign;
- `frequency_turn`: positive nonmonotone `a`;
- `near_singular_regular`: positive `a` with a small registered lower bound.

Random histories use seed `1940820`, bounded polynomial/trigonometric coefficients, and a positive
exponential representation for `a`.  They are characterized rather than filtered.  Numerical
residual ceilings are `2e-8` for independently reconstructed curvature/Jacobi quantities and
`2e-10` for algebraic/frame identities.  Exact symbolic claims must vanish identically.

## Preregistered hostile mutations

At minimum the catches must detect: deleted `B'`; deleted `B^2`; deleted either diagonal `N^2`;
deleted `N(A+B)` off-diagonal cross term; forced `B=0`; forced trace-free or scalar `M`; reversed
factor order; replaced ordered evolution by commuting exponentials; dropped the outer `L` action;
wrong affine power; transposed one ordered factor; and a non-positive or unsigned Gram integrand.

## Outcome classes

- `GENERAL_SYMMETRIC_MATRIX_FACTORIZATION_AND_NO_CAUSTIC_CLOSE`;
- `FACTORIZATION_SURVIVES__CAUSTIC_CLASSES_EXIST`;
- `FACTORIZATION_FAILS__NO_CAUSTIC_BY_DIFFERENT_IDENTITY`;
- `GENERAL_SYMMETRIC_EXTENSION_ADMITS_CAUSTICS`;
- `TYPE_OR_REGULARITY_FAILURE`;
- or a more precise bounded result forced by the derivation.

## Certification and falsification contract

The result fails if coframe regularity, affine-null property, frequency identity, screen
orthonormality/parallelism, tide self-adjointness, Jacobi residual, affine vertex normalization,
G193/G192/G190 limits, or independent replay exceeds its gate.  Every new structural guard must
be mutation catch-proved.  No retuning follows observed outcomes.

Banking requires a production reconstruction, a separately implemented frozen-census replay,
hostile catches, premise audit, full repository tests, `git diff --check`, and fresh adversarial
review.

## Maximum conclusion

At most G194 may classify frequency, full matrix screen response, ordered factorization, and
caustics for arbitrary smooth symmetric `2 x 2 M` in this supplied coframe family and one central
pair germ.  It cannot select a physical metric history or observer population, establish a theorem
for arbitrary complete coframes or antisymmetric rotation, derive radiative transfer or
observations, or establish `X_max`, dynamics, action, source, matter, mass, bootstrap, or
signalling.
