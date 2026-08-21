# G195 audit report — antisymmetric screen-rotation boundary

Date: 2026-08-20

## Landing

```text
ROTATION_CARRIES_COVARIANTLY__GENERAL_REAL_MATRIX_FACTORIZATION_AND_NO_CAUSTIC_CLOSE
```

Final grade after fresh external review and R1 retry:

```text
EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS
```

## Question and bounded answer

G195 activated the first antisymmetric screen-rotation function inside the exact G194 coframe
architecture.  It asked whether that function is merely screen carry, modifies the focusing law, or
breaks the ordered factorization and permits caustics.

For arbitrary positive `C3` `a(eta)` and arbitrary real `C2` `A,N,B,R`, on the supplied central
outgoing `+z` pair germ, direct metric reconstruction gives

\[
C_\eta=2\Omega,\qquad \Omega=R\begin{pmatrix}0&1\\-1&0\end{pmatrix},
\]

and

\[
T_c=\tau_0I+\frac{2S'-4S^2-4[S,\Omega]}{a^4}.
\]

The coordinate screen is not parallel when `R` is nonzero.  If

\[
O'=-2\Omega O,\qquad \widetilde S=O^TSO,
\]

then the Levi-Civita parallel screen has

\[
T_p=\tau_0I+\frac{2\widetilde S'-4\widetilde S^2}{a^4}.
\]

Thus antisymmetric rotation is lawful connection carry.  It couples to anisotropic strain through
the carried frame, but it has no independent `R'` or `R^2` curvature-focusing term.  Pure rotation
changes screen orientation and not the parallel-screen area response.

## Stronger ordered closure

The exact coordinate equation factorizes as

\[
(\partial_\eta-2M^T)(\partial_\eta+2M)Y_c=0
\]

for the full real matrix `M=S+Omega`.  With

\[
L'=-2ML,\qquad
K=\int_0^\eta L^{-1}L^{-T}\,ds,
\]

the vertex-normalized physical map is

\[
D_c=aLK.
\]

Because `L^{-1}L^{-T}` is positive definite and `det L>0`, `det D_c>0` for every
nonzero `eta` on a connected regular interval.  The parallel rotation has determinant one, so the
parallel map has the same caustic classification.

This removes the symmetry assumption from the G194 Gram proof.  The stronger theorem is still
bounded to the displayed family; it is not a statement about arbitrary complete coframes.

## Evidence gates

### Exact production

- 22/22 assertions passed.
- Direct four-dimensional metric, inverse, Christoffels, Riemann contraction, connection, and tide.
- G194 (`R=0`) and pure-rotation controls passed.
- Exact ordered and covariant factorizations passed.

### Independent replay

The verifier does not import the production module or read its artifact.  It uses Torch automatic
differentiation for metric jets and a separate Riemann/connection implementation, then SciPy DOP853
for independently written parallel-screen and ordered-representation IVPs.

| Gate | Result | Ceiling |
|---|---:|---:|
| histories | 266 | frozen 10 named + 256 seeded |
| assertions | 5,059 | exact registered count |
| maximum tide error | `1.1368683772161603e-13` | `3e-8` |
| maximum screen-connection error | `2.936618967697372e-15` | `3e-8` |
| maximum factorization error | `3.162536899026236e-11` | `3e-8` |
| maximum Wronskian error | `1.302977864492405e-11` | `3e-8` |
| minimum sampled nonvertex determinant | `2.1021706025387246e-4` | positive |

The numerical determinant census is regression evidence.  The universal bounded caustic statement
comes from the exact positive-Gram proof, not from sampling.

### External review

The first review accepted the bounded algebra and independence wording but required a frozen
package-level no-write replay result. After preregistered R1, the final fresh retry completed two
live registered replays in `775.658` and `772.465` seconds. Both exited zero; JSON identity was
exact; all 38 sealed hashes remained unchanged; and the runtime remained empty. The accepted
landing was `G195_NO_WRITE_EVIDENCE_REPAIR_ACCEPTED__BOUNDED_LANDING_RETAINED`.

### Hostile mutations

All 18 registered mutations were caught, including forced `R=0`, wrong connection sign, declaring
the coordinate screen parallel, omitting the parallel rotation, symmetrizing `M`, deleting `R'`,
deleting `R^2` or the strain-rotation commutator, reversing factor order, replacing ordered
transport by a commuting exponential, wrong Gram order, wrong affine power, and treating finite
sampling as a universal proof.

## Premise audit

| Input | Status |
|---|---|
| measured `c_E`, set to one in control units | `OBSERVED` calibration only |
| completed-pair Dual Reciprocity | `WORKING_FOUNDATIONAL_CLARIFICATION` |
| displayed coframe family | `CHOSE_MATHEMATICAL_FUNCTION_FAMILY` |
| `a,A,N,B,R` profiles | `FREE_AND_EXPLORED` |
| central pair and outgoing germ | `CHOSE_QUERY` |
| connection, tide, factorization, caustic theorem | `DERIVED_CONDITIONAL` |
| physical profiles, other germs, global completion | `OPEN` |
| P1/G116/G189, observations, transfer, `X_max` | `OMITTED` |

## Interpretation

The new degree of freedom is neither “turned off” nor fitted.  Its profile is arbitrary, but its
role in this pair response is fixed by the metric: it is connection carry that rotates the symmetric
strain seen in the parallel screen.  The activated components therefore mesh as interacting gears
at the evaluator level.  G195 does not yet derive the distance/regime dependence of their input
profiles.

## Maximum conclusion

G195 classifies arbitrary smooth real `2x2` screen mixing in the displayed time-dependent affine
coframe family and one supplied central pair germ.  It does not select a physical history, establish
the result for arbitrary complete metrics or observer pairs, derive an observational transfer law,
or establish `X_max`, dynamics, action, source, matter, mass, bootstrap, or signalling.
