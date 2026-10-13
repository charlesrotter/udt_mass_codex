# ALP1 mathematical review check freeze

Direct candidate exposure has occurred after SOURCE_FIRST.md was sealed.
This checks the supplied finite/distant family from its original null-incidence
integral, using a separately written implementation. It imports no researcher
code and does not fit or choose physical parameters. Candidate equations are
exposed; independence here is implementation/argument, not blind prediction.

Question: for the displayed metric and fixed comoving free clocks, do the
original incidence integrals reproduce the common boundary, nearby-emission
derivative, negative/positive local signs, corrected crossing and tail law?
This is a finite floating-point corroboration of an analytic argument, not
an interval proof, geometric census or native UDT result.

Pin `D=1` as free comparison units; `k` in `[-3/2,-1,0,1,3]` is diagnostic
coverage, not fitted values. Compute `s=2 sqrt(k+2)/pi`. At 45 decimal-digit
mpmath precision integrate `1/a(t)` directly with independent quadrature.
Check the infinite integral against 1 within `1e-35`. At reception `t=2s`,
solve nearby fixed-separation incidence for emissions `+/-h`, with `h=1e-7 s`
and half that value; compare its finite-difference derivative with `a(2s)`
within `1e-10` relative error and record refinement. Check local quartic
residual coefficients at `x=t/s=1e-3,5e-4` against `1+k²/6` within `2e-5`
at the finer value, retaining both outcomes. Record local signs and common-D
local coefficients without silently converting a finite check to a limit proof.

Direct tail integrals at `x=20,40,80` check the ratio of the actual `a(t)` to
`[s/(3 delta)]^(4/3)`; require last relative deviation below `0.01` and
strictly improving errors. Direct integration for `k=-1,s=1` to `t=1` checks
the corrected crossing within `1e-35`, and explicitly rejects the preserved
wrong `pi/4` expression by a discrepancy above `0.3`. All root residuals must
be below `1e-35`.

One CPU worker, one thread, 2 GiB virtual-address limit, no GPU, no wall or
CPU killing timeout. Expected below 60 total CPU seconds and 1 MiB output;
manual stop on unexpected resource growth. TPS1 capture utility, unique
`checks/finite_01` prefix, preserves stdout/stderr/receipt. No restart or
production solve is needed. On failure retain outputs, diagnose within the
same scope, and do not silently loosen thresholds. Checksums record byte
correspondence only. Analytic proof and the reviewer report own conclusions.
