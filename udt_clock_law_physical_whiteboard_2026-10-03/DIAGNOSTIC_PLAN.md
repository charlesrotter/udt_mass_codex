# CPW1 finite representation diagnostic

Initial capture failed at exact structural matrix equality for the deliberately
wrong affine scaling; the correct-scaling residual passed. Freeze one diagnostic:
load only the initial script through that assertion, print computed/expected
wrong residuals and their componentwise expanded difference, and evaluate one
nonzero derivative control. No expression, null vector or equation changes.
Same capture2GiB/oneBLAS/no timeout; one finite algebra family, no search.

Check whether expression-tree form rather than polynomial value caused failure.
No omitted metric terms or asymptotic sector will be added; this control was
explicitly pointwise conformal-flat. No numerical tolerance is involved. A
canonicalization repair may use exact expanded differences only if they vanish
and the wrong-scaling countercontrol remains nonzero. Otherwise return the
actual algebra defect. The original failed source/output/freeze remain fixed.
The full repaired script, not this prefix diagnostic, must check remaining claims.
