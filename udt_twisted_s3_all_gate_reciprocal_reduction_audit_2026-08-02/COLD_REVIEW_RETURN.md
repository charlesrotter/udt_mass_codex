# Fresh zero-context adversarial review

Date: 2026-08-02  
Reviewer: `/root/twisted_s3_cold_verifier`  
Mode: read-only; no repository edits  
Verdict: `VERIFIED` within the exact preregistered off-shell/global-cell scope

Reviewed final production script SHA-256:
`fbef0067b506b865e8bcb22db07534cd1146712b0d7869b30bd6c9a6915d75ea`.  
Reviewed final certificate SHA-256:
`876b00e7d94e249b148846d59612b4cef373430bb1b8fb2f34a1f8ee55160d67`.

## Independent reconstruction

The reviewer used the full rational stereographic metric with nested PyTorch reverse-mode automatic
differentiation, not the production Taylor-jet functions.

```text
candidate   independent determinant       exact determinant decimal
C01         -9.282447791951885e11         -9.282447791955518e11
C02         -58845.00186922464            -58845.00186922543
C03          5.151557008305059e-5          5.151557008304678e-5
C04          39755.31115572625             39755.3111557245
C08         -62755.07027165642            -62755.070271657765
```

For C02 the independent Jacobian singular values are `(1416.5767,40.1049,1.03579)`. C06 and C09
reproduce zero within numerical differentiation (`C06` residual determinant `-1.65e-40`), while C08
retains a unique-clock certificate but has exactly zero twist.

Independent implementation SHA-256:
`c182f90aaf32ab6ecb40e394f52a7e8e720206011c9d8ecfc62de99e3e7009dc`.
The preserved primary stdout SHA-256 is
`e6edb2085af4553e1a3159289581152e3c66e9a7c024d47a8983f02f284c9443`; additional stdout is
`e44394fef0695331a634f14607caac0fb3a2593e0eb762b22cdc48230cabf6de`; environment record is
`d797465a9a4177f0e1ee2b43d2c6757e6323b65d412bf47022f16d451e816b17`.

## Semantic audit

- production jet order is sufficient: metric 3-jet, Christoffel 2-jet, Ricci 1-jet, invariant first
  derivatives;
- the registered forms obey `d sigma3=-2 sigma1 wedge sigma2`, so twist is globally nonzero when
  `a` is nonzero;
- `u` has exact range `[4,11]`, the primary slice margin is strict, and `K` is timelike;
- invariant independence constrains a completely general, possibly time-dependent Killing field;
- continuity closes the critical set and missing stereographic point;
- the two contractions of `L_(AK)g` force `dA=0`;
- twist gives a smooth spacelike ruler line, and the line projectors are scale/sign independent and
  equivariant.

The reviewer required only wording/evidence repairs: display both Killing contractions; explicitly
continue over the critical/chart-complement sets; define complete as smooth global nondegenerate
complete-cell geometry rather than Lorentzian geodesic completeness; and bind final hashes. These
repairs are incorporated. No mathematical repair was required.

Maximum honest conclusion: one explicit globally smooth, strict-slice, off-shell twisted `R x S3`
configuration has a one-dimensional full Killing algebra and a metric-intrinsic smooth reciprocal
rank-two reduction. Nothing selects its profile, `lambda`, twist, physical branch, action, source,
boundary, matter, mass, or universal complete-metric reduction.
