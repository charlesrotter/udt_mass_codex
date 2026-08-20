# G193 preregistration — noncommuting transverse-mixing extension

Date: 2026-08-20

## Whole question and exact bounded regime

Does G192's exact screen factorization and family-scoped no-caustic result survive after one
independent transverse-mixing channel is activated, including histories that cannot be reduced by
one constant screen rotation?

Work on one smooth coordinate neighborhood with coordinates `(eta,z,p,w)`, an interval `I`
containing `eta=0`, and the complete coframe

\[
\begin{aligned}
\theta^0&=a(\eta)\,d\eta,\\
\theta^1&=a(\eta)\,dz,\\
\binom{\theta^p}{\theta^w}
&=a(\eta)\left[
d\binom{p}{w}
+M(\eta)\binom{p}{w}(d\eta+dz)
\right],\\
M(\eta)&=
\begin{pmatrix}
A(\eta)&\nu(\eta)\\
\nu(\eta)&0
\end{pmatrix},
\qquad A(\eta)=\sqrt2\,\mu(\eta),\\
g&=-(\theta^0)^2+(\theta^1)^2+(\theta^p)^2+(\theta^w)^2.
\end{aligned}
\]

Here `a` is arbitrary positive `C3` with `a(0)=1`; `mu` and `nu` are arbitrary real `C2`
functions.  No sign, monotonicity, asymptote, relative-strength law, or observational profile is
imposed.  At `nu=0` the family reduces exactly to G192 in its `(p,w)` screen.

The supplied completed pair is

\[
F(\tau,\sigma)=(\eta=\tau,z=\sigma,p=w=0),
\]

with source vertex at the origin and the `+z` ruler orientation selecting the local outgoing
germ.  The classification is local on connected regular subintervals containing the vertex.

For varying `A/nu`, matrices `M(eta_1)` and `M(eta_2)` may fail to commute.  Such controls are
required in the census.  A time-dependent diagonalization may not be used to delete the induced
screen connection.

## Metric-led versus template-led

This is metric-led.  The metric, connection, affine ray, parallel screen, curvature tide, and
matrix Jacobi map will be reconstructed from the displayed coframe.  G192 is a required limit, not
a source for assuming the enlarged answer.

## Premise and choice ledger

| Item | Status | Role |
|---|---|---|
| `c_E` | `OBSERVED`; set to one in control units | clock/ruler calibration only |
| completed-pair Dual Reciprocity | `WORKING_FOUNDATIONAL_CLARIFICATION` | acts after the full pullback |
| displayed coframe | `CHOSE_MATHEMATICAL_FUNCTION_FAMILY` | bounded extension, not general complete metric |
| `a(eta)>0`, `a(0)=1` | `free-and-explored` plus source-unit calibration | arbitrary common-scale history |
| real `mu(eta)` | `free-and-explored` | G192 mixing history |
| real `nu(eta)` | `free-and-explored` | one independent cross-screen mixing history |
| `C3/C2/C2` regularity | `pinned-by-MATHEMATICAL_OPERATOR_ORDER` | sufficient metric jets and certified residuals |
| symmetric two-channel `M` | `CHOSE_BOUNDED_EXTENSION` | minimal noncommuting tile; antisymmetric rotation remains omitted |
| central pair and `+z` ruler orientation | `CHOSE_QUERY` | fixes one local completed pair and outgoing germ |
| affine frequency and full matrix screen | `DERIVED_CONDITIONAL` | computed from the same metric |
| P1, G116, G189, transfer, observations, `X_max` | `OMITTED` | forbidden construction inputs |

## Whole-space and omitted-sector ledger

The full function space of positive `a` and real `mu,nu` is represented symbolically inside the
displayed family and sampled by a frozen bounded census.  Omitted are the third independent
symmetric screen-mixing component, antisymmetric screen rotation, arbitrary screen scale/shear,
spatial dependence, other complete-coframe functions, other pair germs, singular metrics,
disconnected intervals, cut loci, topology, global completion, observer population, emission,
transfer, source physics, action, dynamics, matter, bootstrap, and `X_max`.

## Preregistered derivation gates

1. Reconstruct `g=E^T eta_4 E`; prove coframe and Lorentzian regularity for every `a>0`.
2. Pull back to the supplied pair and reconstruct its completed clock, ruler, and normalized null
   germs.
3. Derive the selected central affine ray, `lambda(eta)`, frequency, and frequency-contraction law.
4. Derive a parallel orthonormal screen without assuming the coordinate screen stays parallel.
5. Reconstruct the full self-adjoint `2 x 2` tidal matrix, retaining every `a`, `mu`, `nu`
   derivative and quadratic cross term that survives.
6. Test any matrix factorization directly against the reconstructed tide.  Do not infer it by
   analogy with G192.
7. Solve or exactly characterize the vertex-normalized matrix Jacobi IVP with
   `D(0)=0`, `dD/dlambda(0)=I`.
8. Classify every determinant-zero/caustic class admitted by this family.  Do not exclude one by
   an acceptance criterion.
9. Characterize cross response and screen-axis rotation without assigning a preferred sign.
10. Recover G192 at `nu=0`, G190 at `mu=nu=0`, and the appropriate static complete-coframe controls
    at `a=1`.
11. Independently replay commuting, genuinely noncommuting, rank-changing, signed, zero-crossing,
    and frequency-turning histories without importing production code or reading its output.

## Frozen independent census

The independent replay will contain these named classes plus 256 seeded random histories:

- `g192_limit`: `nu=0`, nonconstant signed `mu`;
- `conformal_limit`: `mu=nu=0`;
- `constant_full_rank`: constant nonzero `mu,nu`;
- `noncommuting_rotating_axes`: nonconstant `mu/nu` with an explicit nonzero matrix commutator;
- `rank_transition`: `nu` crosses zero;
- `signed_double_crossing`: both mixing functions change sign;
- `frequency_turn`: positive nonmonotone `a`;
- `near_singular_regular`: positive `a` with a small registered lower bound.

Random histories use seed `1930820`, bounded polynomial/trigonometric coefficients, and a positive
exponential representation for `a`; they are characterized rather than retained or discarded by
screen behavior.  Numerical residual ceilings are `2e-8` for independently reconstructed
curvature/Jacobi quantities and `2e-10` for algebraic/frame identities.  Exact symbolic claims must
vanish identically.

## Outcome classes

- `MATRIX_FACTORIZATION_AND_NO_CAUSTIC_SURVIVE_IN_DECLARED_FAMILY`;
- `FACTORIZATION_SURVIVES__CAUSTIC_CLASSES_EXIST`;
- `FACTORIZATION_FAILS__NO_CAUSTIC_BY_DIFFERENT_IDENTITY`;
- `NONCOMMUTING_EXTENSION_ADMITS_CAUSTICS`;
- `TYPE_OR_REGULARITY_FAILURE`;
- or a more precise bounded result forced by the derivation.

## Certification and falsification contract

The result fails if the coframe regularity, affine-null property, frequency identity, screen
orthonormality/parallelism, tide self-adjointness, Jacobi residual, affine vertex normalization,
G192/G190 limits, or independent replay exceeds its registered gate.  Any claimed factorization
must be catch-proved by a mutation that breaks its derivative order or matrix order.  Any claimed
no-caustic result requires an exact sign/definiteness proof, not a finite numerical census.

Banking requires production reconstruction, a separately implemented frozen-census replay,
hostile catches, premise audit, full repository tests, `git diff --check`, and fresh adversarial
review.  No retuning follows observed outcomes.

## Maximum conclusion

At most G193 may classify frequency, full matrix screen response, factorization, and caustics for
this supplied three-function complete-coframe family and one pair germ.  It cannot select a
physical metric history or observer population, establish a theorem for arbitrary complete
coframes, derive radiative transfer or observations, or establish `X_max`, dynamics, action,
source, matter, mass, bootstrap, or signalling.
