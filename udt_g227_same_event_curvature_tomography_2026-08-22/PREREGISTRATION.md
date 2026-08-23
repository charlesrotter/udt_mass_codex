# G227 preregistration — same-event null tidal curvature tomography

Date: 2026-08-22

Question type: `METRIC_LED`.

Terminology clarification retained with the frozen test: every occurrence of “timelike chord” in
the preregistered motivation means the explicitly `CHOSE` sectional-curvature functional
`R(E,U,E,U)`.  It does not claim ownership of a populated physical observer chord.  Likewise,
“phase germ” means an infinitesimal affine Jacobi generator/controlled short-edge jet, not an
isolated finite G226 transfer matrix.

Post-outcome type repair: the frozen phrase “common-curvature realizability” below is narrowed to
**common algebraic-curvature compatibility**.  G227 does not invoke or prove the separate local
metric-2-jet realization theorem.  The frozen candidate and numerical contract are unchanged.

## Whiteboard-pilot disclosure

Before this production preregistration, independent whiteboard agents performed small exact-rational
rank probes.  Those probes corrected an initial seven-direction guess and supplied the nine-direction
sequence below, with pilot cumulative ranks `3,6,9,12,15,16,17,18,19`.  G227 is therefore not a
blind discovery test of that sequence.  It is a preregistered production derivation, kernel proof,
held-out prediction test, hostile-catch suite, and independently implemented certification of the
pilot theorem.  This disclosure must remain attached to every evidence grade.

## Whole bounded question

At one supplied event of one supplied four-dimensional Lorentz metric, do nine fixed exact null
directions and their completed infinitesimal screen tides obey a nonidentity common-curvature
realizability condition?  Does one additional timelike sectional datum restore the algebraic
curvature mode silent to the entire null sky?

This is a local algebraic second-jet test.  It is not a field solve, history selector, branch
population rule, observational fit, or global completion.

## Frozen alternatives

- `A_NULL_RANK_19_ONE_CONSTANT_CURVATURE_KERNEL__TIMELIKE_RANK_20`
- `B_NULL_RANK_BELOW_19_OR_EXTRA_KERNEL`
- `C_NULL_RANK_20_NO_SILENT_MODE`
- `D_TIMELIKE_DATUM_FAILS_TO_RESTORE_RANK_20`

No alternative may be added after outcome inspection.

## Frozen representation

Use the Minkowski observer tetrad with signature `(-,+,+,+)` and ordered bivectors

```text
B = (01, 02, 03, 12, 13, 23).
```

Represent an algebraic curvature tensor by a symmetric `6 x 6` bivector bilinear form `Q` subject
to the single four-dimensional first-Bianchi constraint

```text
Q[01,23] - Q[02,13] + Q[03,12] = 0.
```

Eliminate `Q[03,12]`, leaving exactly 20 rational variables.  Sign conventions may alter named
components but may not alter ranks, kernel dimension, or the constant-curvature conclusion.

For every fixed rational stereographic pair `(p,q)`, define

\[
n=\frac{(2p,2q,1-p^2-q^2)}{1+p^2+q^2},\qquad k=(1,n),
\]

and the rational screen basis

```text
e1 = n cross ez,
e2 = n cross e1.
```

Normalization is not required for a rank test.  Record the three symmetric tidal entries

\[
(e_1\wedge k)^TQ(e_1\wedge k),\quad
(e_1\wedge k)^TQ(e_2\wedge k),\quad
(e_2\wedge k)^TQ(e_2\wedge k).
\]

## Frozen direction sequence

Use, in this order,

```text
(9,-1/2)
(5/4,-2/9)
(-1/7,5/3)
(-1,-1)
(4/9,-2)
(-6/7,6)
(1/6,-7/9)
(5/8,1/4)
(1,-5/6)
```

The sequence is frozen before the production implementation.  The calculation may report its
cumulative ranks but may not claim that nine directions are globally minimal.

## Frozen candidate statements

1. The nine-direction `27 x 20` null measurement map has exact rank 19.
2. Its kernel is exactly the span of the constant-curvature tensor `g wedge g`.
3. One fixed timelike sectional functional, chosen before execution and nonzero on `g wedge g`,
   raises the augmented rank to 20.
4. Once rank 19 is reached, the inferred null-visible curvature predicts every held-out null-screen
   tide exactly, because the one unresolved mode is invisible to all null screens.
5. A generic synthetic collection of 27 independent tide entries fails the eight exact left-null
   syzygies and therefore cannot arise from one algebraic curvature tensor.
6. The generic cumulative rank law is conjectured to be

   \[
   \operatorname{rank}A_N=\min(2N,10)+\min(N,9),
   \]

   corresponding to two trace-free screen entries probing ten Weyl modes and one trace entry
   probing nine trace-free-Ricci modes; scalar curvature is null-silent.  G227 may verify this law
   on its frozen sequence but may not promote finite sampling into a global genericity proof.

## Required checks

1. `Q` has 20 independent variables after symmetry and Bianchi.
2. Every frozen `k` is exactly null and every `e_A` is exactly screen-orthogonal to `k`.
3. Every tidal matrix is symmetric.
4. Report cumulative exact ranks for directions 1 through 9.
5. Verify the constant-curvature vector lies in the exact kernel.
6. Verify the exact null kernel has dimension one and is proportional to that vector.
7. Add the frozen timelike functional and report augmented exact rank.
8. Compute an exact basis for the left-null syzygies of the nine-direction map.
9. Generate seeded rational algebraic-curvature controls and reconstruct all null-visible data.
10. Predict at least four separately frozen held-out null directions not used in the rank map.
11. Reject hostile tensors that violate the Bianchi elimination, hostile arbitrary tide tables that
    violate the syzygies, and the false claim that null tides detect the constant-curvature mode.
12. Independently replay the load-bearing ranks and kernel using standard-library exact rational
    elimination with a separately written matrix builder.

## Frozen held-out directions

```text
(2/7,3/5)
(-3/4,1/8)
(7/6,-2/5)
(-5/9,-4/7)
```

## Frozen timelike datum

With `U=(1,0,0,0)` and `E=(0,1,0,0)`, use

\[
\mathcal S_U(R)=R(E,U,E,U).
\]

It is required to be nonzero on the chosen nonzero constant-curvature tensor.  If the bivector sign
convention makes its value `-1` rather than `+1`, only nonvanishing is load-bearing.

## Premise classification

- Lorentz metric/tetrad at one event: `SUPPLIED_CONDITIONAL`.
- Algebraic Riemann symmetries and first Bianchi identity: `DERIVED_METRIC_IDENTITY`.
- Null and screen construction: `DERIVED` from the supplied tetrad and frozen directions.
- Direction list and held-out list: `CHOSE_NUMERICAL_CONTROL`.
- Timelike observer chord: `CHOSE_DISCRIMINATING_CONTROL`.
- Numerical curvature values: `FREE_AND_EXPLORED`.
- Dynamics, action, source, matter, observer population, topology, global boundary, `X_max`: omitted.

## Certification contract

- Production: exact SymPy rational linear algebra and saved machine-readable results.
- Independent replay: separately implemented standard-library `Fraction` Gaussian elimination.
- Raw exact ranks, kernel vectors, syzygy count, held-out residuals, hostile catches, commands,
  hashes, and versions must be preserved.
- Aggregate verification must run without writing outside its package-owned output files.

## Falsification

Alternative A fails if the nine-null rank is not 19, if the kernel has dimension other than one,
if its generator is not proportional to `g wedge g`, if the timelike datum does not raise the rank
to 20, or if held-out null tides cannot be predicted from the inferred null-visible class.

## Maximum conclusion

At most G227 may derive an exact same-event common-curvature realizability and local tomography
theorem for a supplied completed reciprocal germ family: null directions determine 19 algebraic
curvature modes and one timelike sectional datum determines the last.  It may falsify incompatible
synthetic germ families.  It cannot generate the numerical curvature field, select a global metric
history, select or populate observer/event/path germs, derive dynamics or sources, or derive
`X_max`, transfer, observation, action, matter, bootstrap, mass, or signalling.
