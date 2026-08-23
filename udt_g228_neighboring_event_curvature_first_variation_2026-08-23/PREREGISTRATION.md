# G228 preregistration — neighboring-event curvature first variation

Date: 2026-08-23

Question type: `METRIC_LED`.

Pre-outcome status: `NO_NUMERICAL_OR_SYMBOLIC_PILOT_RUN`. The tensor representation and all outcome
alternatives below are frozen before the production rank calculation.

Post-outcome repair note: fresh adversarial review found that the neighboring-tensor pullback was
written with its map direction reversed. The corrected expression below uses
`P_{p->q}^* R_q`. It also narrows the finite-phase hostile control to an actual G188 Jacobi-tide
family. `PREREGISTRATION_HASHES.tsv` preserves the original pre-outcome bytes and records this
type/evidence repair; the frozen alternatives and numerical contract are unchanged.

## Whole bounded question

At one supplied event of one supplied smooth four-dimensional Lorentz metric, classify the
first-order compatibility of supplied neighboring curvature chords. Determine whether a single
affine-null directional variation is restricted by differential Bianchi, and identify the first
frozen multidirectional subset whose assigned variations cannot be arbitrary. On the same supplied
null direction, verify the exact screen-covariant tidal and Jacobi-generator first-variation laws.

This is an infinitesimal metric-connection compatibility calculation. It is not a metric solve,
field equation, value generator, finite-history selection, or population rule.

## Frozen algebraic representation

Use signature `(-,+,+,+)`, tetrad indices `0,1,2,3`, and the G227 ordered bivectors

```text
(01, 02, 03, 12, 13, 23).
```

For each derivative index `mu`, represent

\[
D_{\mu abcd}=(\nabla_{e_\mu}R)_{abcd}
\]

by a 20-component algebraic-curvature vector with the same pair symmetries and algebraic first
Bianchi elimination used in G227. Before differential Bianchi this gives exactly `4 x 20 = 80`
rational variables.

Impose the full covariant differential Bianchi identity

\[
D_{e,ab,cd}+D_{a,be,cd}+D_{b,ea,cd}=0
\]

for every tetrad index choice. Duplicate and identically zero component equations may be generated,
but exact row reduction must report the independent rank.

## Frozen directional basis and subset census

Use the invertible rational null tetrad

\[
k=e_0+e_3,\qquad
\ell=\tfrac12(e_0-e_3),\qquad
s_1=e_1,\qquad
s_2=e_2.
\]

For every one of the 15 nonempty subsets of `(k,l,s1,s2)`, compute the exact rank of the projection
from the differential-Bianchi-compatible module to the supplied 20-component directional
derivatives in that subset. Record target dimension, image rank, and codimension. No subset may be
discarded after inspecting outcomes.

Define the first restricted subset size as the least cardinality for which at least one subset has
positive codimension. Report all subsets at that cardinality rather than selecting a favorable one.

## Frozen alternatives

- `A_ONE_DIRECTION_SURJECTIVE__FIRST_RESTRICTION_AT_TWO_DIRECTIONS`
- `B_ONE_DIRECTION_SURJECTIVE__FIRST_RESTRICTION_AT_THREE_DIRECTIONS`
- `C_ONE_DIRECTION_SURJECTIVE__FIRST_RESTRICTION_AT_FOUR_DIRECTIONS`
- `D_ONE_DIRECTION_ALREADY_RESTRICTED`
- `E_DIFFERENTIAL_BIANCHI_MODULE_NOT_DIMENSION_60_OR_OTHER_UNEXPECTED_STRUCTURE`

No alternative may be added or merged after outcome inspection.

The standard dimension-60 value for the algebraic covariant-derivative-curvature module is a
candidate to be independently reproduced, not assumed as the output.

## Neighboring-event interpretation

For a supplied short geodesic from `p` in direction `v`, use Levi-Civita parallel transport to
compare the neighboring curvature with `R_p`. The covariant first difference is typed as

\[
\Delta_v^\epsilon R=
\frac{P_{p\to q}^*R_q-R_p}{\epsilon}
\longrightarrow (\nabla_vR)_p.
\]

The finite-difference statement is interpretive. The exact production calculation acts on the
limiting tensor `D`; it does not claim finite-epsilon equality or infer `D` from isolated finite
G226 phase matrices.

## Frozen screen and phase identities

On the supplied affine null direction `k`, let `S_A` be a parallel orthonormal screen and

\[
T_{AB}=R(S_A,k,S_B,k).
\]

Here and below the curvature ordering is fixed to the G188 convention in which the Jacobi equation
has lower-left block `-T`; an overall sign change is not silent in this part of G228.

The parallel-screen identity to verify is

\[
\frac{dT_{AB}}{d\lambda}
=(\nabla_kR)(S_A,k,S_B,k).
\]

For a moving orthonormal screen `E=S C`, take

\[
T_E=C^T T C,\qquad \Omega=C^TC',\qquad \Omega^T=-\Omega.
\]

Freeze the matrix convention

\[
\mathcal D_\lambda T_E
=T_E'+[\Omega,T_E]
=C^T T' C.
\]

For screen position `y` and screen-covariant velocity `v=y'+\Omega y`, freeze the first-order
Jacobi generator

\[
\frac d{d\lambda}
\begin{pmatrix}y\\v\end{pmatrix}
=
\begin{pmatrix}
-\Omega&I_2\\
-T_E&-\Omega
\end{pmatrix}
\begin{pmatrix}y\\v\end{pmatrix}.
\]

The production must verify equivalence to the parallel-screen generator and verify Hamiltonian
symplecticity for symmetric `T_E` and skew `Omega`. These are gauge-covariance identities, not an
independent screen coefficient or a promotion of G225 transport.

## Required exact checks

1. Rebuild the 20-component algebraic-curvature basis without importing the G227 production
   measurement matrix.
2. Construct the `80` raw derivative variables and the full differential-Bianchi equation matrix.
3. Report its exact row rank and compatible-module dimension.
4. Compute all 15 frozen subset projection ranks and codimensions.
5. Compute the first restricted subset size or report that the one-direction map is already
   restricted.
6. Produce exact left-null syzygies for every restricted frozen subset.
7. Generate seeded rational compatible derivative-curvature controls and verify every reported
   syzygy exactly.
8. Apply at least one deterministic incompatible one-entry perturbation to each restricted subset
   class and require rejection when the chosen entry lies outside the image.
9. Demonstrate that an explicitly constructed within-image perturbation is accepted, preventing
   the false claim that any change is incompatible.
10. Verify the parallel-screen curvature derivative identity by tensor multilinearity and parallel
    carry assumptions.
11. Verify the moving-screen commutator identity with exact rational orthogonal controls and a
    separately checked symbolic derivation.
12. Verify the moving-screen Jacobi generator, its symplecticity, and its equivalence to the
    parallel-screen phase under the corresponding time-dependent phase change.
13. Independently rebuild the differential-Bianchi matrix and projection census using only the
    Python standard library `Fraction` and separately written row reduction.

## Structural hostile controls

At minimum the package must catch:

- deleting one independently selected differential-Bianchi pivot equation;
- replacing the differential cyclic sum by an algebraic first-Bianchi duplicate;
- falsely declaring an isolated one-direction variation incompatible;
- calling one isolated finite G226 matrix a curvature derivative; the catch must use two smooth
  admissible G188 Jacobi-tide histories with the same finite full phase and different initial tide
  derivatives, not merely two unrestricted Hamiltonian paths;
- omitting the screen commutator term for a noncommuting tide and rotation;
- reversing the commutator sign;
- using a nonsymmetric tide or nonskew screen connection while claiming symplecticity;
- deleting either diagonal `-Omega` block from the moving Jacobi generator;
- promoting a supplied derivative value into a generated history value.

## Premise and completeness ledger

- Event, tetrad, curvature value, derivative values, null direction, and local screen gauge:
  `SUPPLIED_CONDITIONAL` / `FREE_AND_EXPLORED`.
- Null-tetrad ordering: `CHOSE_NUMERICAL_CONTROL`.
- Levi-Civita metricity, curvature symmetries, algebraic Bianchi, differential Bianchi, quotient
  screen connection, and Jacobi equation: `DERIVED_METRIC_IDENTITIES` or existing
  `DERIVED_CONDITIONAL` evaluators.
- Metric dimension/signature: `pinned-by-THEORY` to the declared four-dimensional Lorentz arena.
- No boundary condition, numerical profile, source, action, matter sector, topology, observer
  population, branch selector, or asymptotic scale is introduced.
- Coverage: one event, first curvature derivative, and one supplied local null tetrad. Dropped:
  finite separation, higher jets, cuts/caustics beyond full-phase typing, topology, global overlap,
  dynamics, stability, sources, and all observational applications.

## Certification contract

- Production arithmetic: exact SymPy rationals.
- Independent arithmetic and matrix builder: Python standard-library `Fraction` only.
- Preserve exact matrices or their canonical hashes, ranks, codimensions, syzygy counts, seeded
  controls, hostile catches, commands, versions, and a SHA-256 evidence manifest.
- Preregister this contract in git before executing the production or independent calculation.
- A result may be banked only after an adversarial fresh-context review and a no-write aggregate
  replay.

## Falsification

The selected alternative is falsified if production and independent builders disagree on the
differential-Bianchi rank, any subset projection rank, first restricted subset size, or syzygy
codimension; if a reported syzygy fails on a compatible seeded control; if the frozen incompatible
perturbation is accepted; or if the moving-screen identities fail in the declared convention.

## Maximum conclusion

At most G228 may derive the local first-order compatibility class of a supplied neighboring-event
curvature tile and the exact gauge-covariant screen/Jacobi representation of that supplied first
variation. It may distinguish one-chain bookkeeping from genuinely multidirectional metric
compatibility. It cannot generate curvature values, select a metric history, select or populate
observers or null branches, derive a finite path from an endpoint pair, promote G225 into selected
transport, or derive dynamics, action, source, matter, bootstrap, boundary, `X_max`, transfer,
observation, mass, or signalling.
