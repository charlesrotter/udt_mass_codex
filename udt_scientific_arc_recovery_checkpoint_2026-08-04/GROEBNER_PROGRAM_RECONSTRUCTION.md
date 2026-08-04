# Gröbner program reconstruction

## What problem generated the polynomials

The source was a stationary, off-shell, complete `R x S3` metric ensemble—not a matter action or
field equation. A metric-derived timelike line `T` and spacelike ruler line `n` define a Lorentzian
plane `E=span(T,n)`. In its metric-anchored frame the program formed

```text
omega_E = g(n,nabla T),
Omega_E = d omega_E.
```

Previous exact work showed nonzero point samples and branch-dependent curvature components. The
global atlas was intended to decide where `Omega_E` vanishes or becomes singular across the full
registered domain and how its finite-loop integrals behave. That would tell us whether local
projector/connection motifs persist globally. It would not select a physical branch or derive an
action, source, carrier, mass or bootstrap law.

## Why the algebra became large

The calculation substituted the complete chosen metric/coframe profiles into the Cartan connection,
formed the curvature two-form, changed to a stereographic/projective chart on `S3` minus the defect
graph, cleared only proved-nonzero denominators, and retained exact polynomial numerators. Global
zero-set completeness then required saturation away from the defect and exact real-root
classification. These operations convert compact geometric formulas into large nonlinear
polynomial ideals.

This was a representation-growth problem arising from a direct exact expansion of a bounded metric
object. It was not evidence that the underlying geometry was physically wrong or intrinsically
incoherent.

## Exact narrowing

The atlas froze four curvature owners `C04,C08,C09,C10` and two twist-scaling controls. C04 acquired
an exact sphere barrier excluding regular real zeros. For C08, reconnaissance suggested six
antipodal clusters but was explicitly non-certifying.

The first direct three-variable rational Gröbner attempt returned no basis after 24 hours 19 minutes
and about 65 GB RSS. Inspection then exposed an exact simplification:

```text
f_i(x,y,z)=A_i(y,z)x+B_i(y,z),
(1-2y^2)x^2-3y^2=0.
```

This split the problem into three `A_i != 0` charts and one exceptional case
`A_1=A_2=A_3=B_1=B_2=B_3=0`. The expensive later jobs focused only on that exceptional bivariate
ideal. They were not repeated attacks on the full original system.

## What returned

- Exact modular rational computation returned a nine-element candidate Gröbner basis in about ten
  seconds, with `verifyGB=1`, all six source reductions zero, algebraic dimension zero and quotient
  staircase count 124.
- An independent SymPy implementation verified all Buchberger reductions, all source reductions,
  the leading monomials and the 124 staircase count. This establishes that the returned object is a
  Gröbner basis containing the source ideal in the recorded direction.
- Exact rational reverse containment remained unproved. A 30-minute lift, a two-hour transformation
  run and a four-hour continuation returned no transformation certificate.
- A finite-field transformation at prime 32003 exactly reproduced the candidate basis and dimension,
  but the first characteristic-zero inference was correctly withdrawn because an inhomogeneous
  special fiber need not bound the rational fiber without a flatness/homogeneous certificate.
- The corrected homogeneous unsaturated route returned multiplicity 640 rather than the required
  124. That is retained algebraic closure/infinity data. Its exhaustive independent replay did not
  finish in one hour.

## What remains open

1. Rational reverse containment for the exceptional C08 bivariate ideal.
2. The three `A_i != 0` C08 charts.
3. Complete rigorous real-root isolation and reconstruction.
4. Global C08 classification and the uncompleted C09/C10 classifications.
5. The final curvature/finite-loop atlas report from the tracked source record.

The untracked raw paths in this directory remain user-owned and unread by this checkpoint.

## Scientific grade and future use

The correct status is `OPEN_SIDE_CERTIFICATE_WITH_STRONG_PARTIAL_EXACT_ALGEBRA`.

The work remains worth resuming if a future native-law or branch decision makes this exact curvature
zero set load-bearing. It should then use sparse/factorized chart elimination, local rank and branch
continuation before global expansion. It should not be resumed merely to make a computer finish a
hard problem.

Runtime and RAM ceilings protect the workstation and characterize implementations. They are never
scientific acceptance criteria. A stopped computation says `INCOMPLETE-COMPUTATION`, not “no
solution,” “no closure,” or “UDT failed.”

