# G195 preregistration — antisymmetric screen-rotation boundary

Date: 2026-08-20

## Whole question and exact bounded regime

Does G194's parallel-screen factorization and no-nonvertex-caustic theorem survive when the first
omitted antisymmetric screen-rotation channel is activated inside the same complete-coframe family?

Work on one smooth coordinate neighborhood with coordinates `(eta,z,p,w)`, an interval `I`
containing `eta=0`, and

\[
\theta^0=a\,d\eta,\qquad \theta^1=a\,dz,\qquad
\theta_{\rm screen}=a[dX+M(\eta)X(d\eta+dz)],
\]

where

\[
X=\binom pw,\qquad
M=\begin{pmatrix}A&N+R\\N-R&B\end{pmatrix}=S+R J,
\qquad J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]

Here `a` is arbitrary positive `C3` with `a(0)=1`; `A,N,B,R` are arbitrary real `C2`
functions. No sign, trace, determinant, commutativity, monotonicity, asymptote, relative-strength
law, or observational profile is imposed. G194 is the exact `R=0` subfamily.

The supplied completed pair is

\[
F(\tau,\sigma)=(\eta=\tau,z=\sigma,p=w=0),
\]

with source vertex at the origin and `+z` ruler orientation. Classification is local on connected
regular subintervals containing the vertex.

The coordinate screen may not be declared parallel. Any screen rotation must be reconstructed
from the Levi-Civita connection, and all matrix order must be retained.

## Metric-led versus template-led

This is metric-led. The metric, connection, affine ray, coordinate-screen connection, parallel
screen, curvature tide, and Jacobi map are reconstructed from the displayed coframe. G194 is a
regression limit, not an imported formula for the answer.

## Premise and choice ledger

| Item | Status | Role |
|---|---|---|
| `c_E` | `OBSERVED`; one in control units | clock/ruler calibration only |
| completed-pair Dual Reciprocity | `WORKING_FOUNDATIONAL_CLARIFICATION` | after full pullback |
| displayed coframe | `CHOSE_MATHEMATICAL_FUNCTION_FAMILY` | bounded extension, not all complete coframes |
| `a>0`, `a(0)=1` | `free-and-explored` plus source calibration | common-scale function |
| real `A,N,B,R` | `free-and-explored` | symmetric mixing plus rotation |
| `C3/C2` | `pinned-by-MATHEMATICAL_OPERATOR_ORDER` | metric jets and certified residuals |
| central pair and `+z` | `CHOSE_QUERY` | one completed pair and outgoing germ |
| P1, G116, G189, transfer, observations, `X_max` | `OMITTED` | forbidden construction inputs |

## Whole-space and omitted-sector ledger

The arbitrary function space of positive `a` and real `A,N,B,R` is treated symbolically inside the
displayed family and sampled by a frozen census. Omitted are independent screen coframe factors
beyond this family, spatial dependence, other complete-coframe functions, other pair germs,
singular metrics, disconnected intervals, cut loci, topology, global completion, observer
population, transfer, source physics, action, dynamics, matter, bootstrap, and `X_max`.

## Preregistered derivation gates

1. Reconstruct `g=E^T eta_4 E`, its exact inverse, determinant, and central pair pullback.
2. Reconstruct the normalized null germ, affine ray, and frequency directly.
3. Compute the coordinate-screen connection along the ray. Construct a parallel orthonormal screen
   from that connection without assuming rotation is gauge-trivial in the Jacobi map.
4. Reconstruct the full curvature tide first in the coordinate screen and then in the parallel
   screen. The physical parallel-screen tide must be self-adjoint.
5. Derive the exact parallel-screen Jacobi equation and preserve all derivative, quadratic,
   commutator, and rotation terms.
6. Test every lawful ordered first-order factorization suggested by the exact connection. Do not
   force the G194 factorization if its hypotheses fail.
7. Derive the Wronskian law and classify determinant-zero/caustic behavior. A universal no-caustic
   statement requires an exact proof; a caustic claim requires an exact witness or independently
   certified sign-changing root.
8. Recover G194 at `R=0`, plus pure-rotation and constant-rotation controls.
9. Independently replay metric-jet/Riemann spot checks and separately coded matrix IVPs without
   importing production code or reading production artifacts.

## Frozen independent census

Use these named histories plus 256 seeded random histories:

- `g194_limit`: noncommuting symmetric `S`, `R=0`;
- `pure_constant_rotation`: `S=0`, constant nonzero `R`;
- `pure_variable_rotation`: `S=0`, sign-changing `R`;
- `isotropic_plus_rotation`: `S=sI`, variable `R`;
- `anisotropic_constant_rotation`: unequal diagonal `S` and constant `R`;
- `fully_noncommuting`: all four entries variable;
- `rotation_zero_crossing`: `R` changes sign;
- `rank_transition`: `det M` changes sign;
- `frequency_turn`: positive nonmonotone `a`;
- `near_singular_regular`: positive `a` with a small registered lower bound.

Random histories use seed `1950820`, bounded polynomial/trigonometric coefficients, and a positive
exponential representation for `a`. Histories are characterized, never filtered. Numerical
ceilings are `3e-8` for independent curvature/Jacobi quantities and `3e-10` for algebraic/frame
identities. Exact symbolic claims must vanish identically.

## Preregistered hostile mutations

At minimum catch: forced `R=0`; deleted `R'`; reversed the sign of the screen connection; declared
the coordinate screen parallel; omitted parallel-screen rotation; symmetrized `M` before metric
reconstruction; replaced ordered transport by a commuting exponential; reversed factor order;
dropped a quadratic `R` contribution; dropped an `S-RJ` cross term; used a non-self-adjoint
parallel tide; wrong affine power; and promoted finite sampling into a universal caustic theorem.

## Outcome classes

- `ROTATION_CARRIES_COVARIANTLY__G194_FACTORIZATION_AND_NO_CAUSTIC_SURVIVE`;
- `ROTATION_MODIFIES_FACTORIZATION__NO_CAUSTIC_BY_NEW_IDENTITY`;
- `ROTATION_MODIFIES_FACTORIZATION__CAUSTIC_CLASSES_EXIST`;
- `ANTISYMMETRIC_ROTATION_BREAKS_ORDERED_CLOSURE`;
- `TYPE_OR_REGULARITY_FAILURE`;
- or a more precise bounded result forced by the derivation.

## Certification and falsification contract

The result fails if coframe regularity, affine-null property, frequency, screen orthonormality,
parallel transport, tide self-adjointness, Jacobi residual, affine vertex normalization, G194
limit, or independent replay exceeds its gate. Every new structural guard must be mutation-catch
proved. No retuning follows outcomes.

Banking requires exact production reconstruction, an independent frozen-census replay, hostile
catches, current premise audit, full repository tests, `git diff --check`, and fresh adversarial
review.

## Maximum conclusion

At most G195 may classify the rotation-carry, parallel-screen Jacobi structure, ordered
factorization, and caustics for arbitrary smooth `a,A,N,B,R` in this supplied coframe family and
one central pair. It cannot select a physical metric profile or observer population, establish a
theorem for arbitrary complete coframes or other germs, derive transfer or observations, or
establish `X_max`, dynamics, action, source, matter, mass, bootstrap, or signalling.
