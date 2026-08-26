# G271 external adversarial review

Reviewer: external Codex `gpt-5.4`

Date: 2026-08-26

Sealed intake: `/tmp/udt_g271_review_hwb1isn4`

`REVIEW_SCOPE.json` SHA-256:
`95650992a267e695e259ff699d319adb4256c36e5cff7be11bc6d8028dc40985`

Raw response SHA-256:
`e2eb9b17173c5f6409b28536e3348f61880f12af77db01d345c67266b8340a94`

## Landing

`ACCEPT_WITH_REPAIRS`

## Accepted scientific findings

The reviewer accepted all load-bearing algebra and the bounded landing:

1. `nabla_X U=-g(X,U)a` and `a_hat_r=-exp(-phi) phi_prime` are correct on the
   supplied primary static family.
2. For parallel-transported `E_I`, the exact evaluator
   `dW_I/dlambda=omega g(a,E_I)` has the stated sign and type.
3. The local affine-normalized depth and screen formulas follow in the written equatorial
   representative.
4. The Pythagorean split, exact radial and quiet strata, equatorial out-of-plane control, leading
   `sech(delta)-M_PT` gap, affine invariance, and reversal qualification are sound.
5. The finite-path integral is an evaluator on a supplied profile and branch, not a field equation
   or history selector.
6. `W` is consistently typed as transported endpoint-clock mismatch, not Jacobi area or holonomy.
7. The result is bounded metric geometry, not dynamics, history, distance, or `X_max` selection.
8. Production, independent verification, and mutation catches are nonvacuous; all three local
   no-write replays passed.

## Requested repairs

### R1 — alleged sealed-source defect

The reviewer stated that `verify_package.py` resolves manifest sources outside the intake because it
uses `ROOT.parent`. This factual premise is incorrect: in the sealed replay `ROOT` is the copied G271
package and `ROOT.parent` is exactly the sealed intake root. All five manifest sources were copied
under that root. The repair ledger records the direct containment proof and adds an executable
`Path.is_relative_to(SCOPE_ROOT)` guard so the intended boundary is mechanically explicit.

### R2 — arbitrary-germ coverage wording

The reviewer correctly noted that the calculation was written in an equatorial representative
while one evidence line said all regular local incidence angles. The repair adds the exact spherical
`SO(3)` isometry reduction from an arbitrary finite-radius null germ to that representative and
qualifies the coverage as modulo metric isometry.

## Strongest conclusion accepted by the reviewer

On the supplied arbitrary smooth regular primary static reciprocal family, the local
affine-normalized direct depth jet and transported-screen jet are exact longitudinal and transverse
projections of the single metric first jet `exp(-phi) phi_prime`, with exact radial and quiet strata
and the leading local gap

```text
sech(delta) - M_PT = (1/2) w_1^2 lambda^2 + O(lambda^3).
```

Finite-path values remain conditional on a supplied profile and branch. No history, distance, or
`X_max` selection follows.
