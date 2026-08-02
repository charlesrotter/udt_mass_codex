# Exact zero-set projective completion method

Date: 2026-08-02

## Trigger and disclosed prior observations

The defined-domain intrinsic saturation classified `C04` as having no real regular zero by an
exact sphere barrier. The preregistered, explicitly non-certifying reconnaissance then returned
antipodal cluster counts `0,6,4,6` for `C04,C08,C09,C10`. Those counts are disclosed here and are
not accepted as complete. The direct `C08` intrinsic saturation was still running when this method
was frozen.

## Exact coverage lemma

Every regular curvature zero obeys the already derived contact equation

```text
A=q0^2 q1^2-3 q0^2 q2^2-2 q1^2 q2^2=0.
```

If `q0=0`, then `A=-2 q1^2 q2^2=0`, hence `q1=0` or `q2=0`. Either case lies in the excluded
defect union `D`. Therefore every possible regular curvature zero has `q0!=0` and is covered by the
single exact ratio chart

```text
x=q1/q0, y=q2/q0, z=q3/q0,
q0^2=1/(1+x^2+y^2+z^2).
```

Antipodal sphere points map to the same ratio point; one real ratio root represents one antipodal
pair. No hemisphere or sign branch is omitted.

## Frozen construction

For each candidate, substitute `(q0,q1,q2,q3)=q0*(1,x,y,z)` into every exact sphere-reduced
curvature numerator. All surviving total degrees have one parity, so divide the common nonzero
power of `q0`, replace `q0^2` by `1/(1+x^2+y^2+z^2)`, clear only that strictly positive real
denominator, and retain the primitive integer polynomial.

The production script must prove the pulled-back polynomial agrees exactly with the sphere
representative after multiplication by its recorded positive power of
`1+x^2+y^2+z^2`. It must include the ratio contact equation

```text
x^2-3 y^2-2 x^2 y^2=0
```

and saturate away from the pulled-back defect and `P` factors. The construction may use the
reconnaissance coordinates only after the exact ideal is built, and only to identify real isolating
components—not to alter equations, order, factors, or root count.

## Certification rule

A global classification requires an exact zero-dimensional certificate plus a complete real-root
count/isolation, or another exact sign certificate. Numerical roots alone remain diagnostic. Any
positive-dimensional or unresolved algebraic component remains `OPEN_PARTIAL`.

The original stereographic and intrinsic routes remain preserved. Candidate universe, metric
profiles, defect set, and maximum conclusion are unchanged.
