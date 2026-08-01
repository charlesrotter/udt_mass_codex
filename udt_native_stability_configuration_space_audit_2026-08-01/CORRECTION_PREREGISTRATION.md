# Cold-review correction preregistration

Date: 2026-08-01  
Trigger: fresh cold adversarial review, before result banking

## Defect

The primary exact-control implementation and prose instantiated `alpha1(x,y)=x-y` as a scalar while
calling `alpha1` a response one-form. That is type-imprecise and cannot serve as the registered
one-form pullback counterexample.

## Exact correction

Replace the example by

```text
C1 = R2,  C0 = R,  i(a)=(a,a),  alpha1=dx-dy.
```

Then

```text
i*alpha1 = da-da = 0,
```

while `alpha1` is a nonzero ambient covector at every point. The forward implication remains:
`alpha1=0` implies `i*alpha1=0`; the converse fails.

Update only the exact-control construction, its independent verifier, and explanatory prose or
generated hashes that depend on those bytes. Preserve the preregistered outcome labels, frozen base,
source universe, premise grades, and conclusion ceiling. If the corrected one-form control fails, or
if the remainder of the cold review finds an outcome-level conflict, stop rather than preserve the
current result.
