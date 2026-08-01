# External cold adversarial review

Date: 2026-08-01  
Models: fresh external `gpt-5.4` sessions, tool-free

## Algebra reconstruction

The Euler/Hessian reviewer returned `PASS`. It independently obtained

```text
E_p=E_lambda=E_f=E_h=0
delta^2 L = v_p'^2+v_lambda'^2+v_f'^2+v_h'^2+(1/2)v_lambda v_p
```

at `p=lambda=h=0,f=x/2`, matching the primary factor `4E0=1/2`.

The independent mode reviewer returned `PASS`: for
`[[k^2,1/4],[1/4,k^2]]`, `k=n*pi/2`, the diagonal is positive and the determinant
`k^4-1/16` is strictly positive for every `n>=1`.

## Scope audit and required repair

The separate scope reviewer returned `FAIL` on the original outcome wording. Its exact objection:

> `CONDITIONAL_F02_STATIONARY_SECTOR_WITNESS_EXISTS` overstates scope: the facts only support a
> conditional, Dirichlet-sector positivity witness, not a completed stationary solution or
> global/physical realization.

Its mandatory repair was to state the nonperiodic endpoint scope and replace the broad stationary
wording with:

```text
CONDITIONAL_NONPERIODIC_F02_DIRICHLET_HESSIAN_SECTOR_POSITIVITY_WITNESS_EXISTS
```

The repair is applied to `RESULT.json`, `AUDIT_REPORT.md`, `EXACT_DERIVATION.md`, `LAY_REPORT.md`,
and the independent verifier. The preregistration remains immutable historical evidence; the new
outcome is strictly narrower than its maximum conclusion. A separate tool-free closure pass
returned `CLOSED-PASS`.

Several earlier full-packet external attempts returned no verdict. They are harness failures, not
scientific results, and are not counted as evidence.
