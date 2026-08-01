# F01 second-wall inverse-stability audit

Date: 2026-08-01  
Preregistration commit: `1e6130f`  
Mode: CPU-only, exact algebra plus outward interval certification

Evidence grade: **`VERIFIED-WITH-CAVEATS`**. The cold mathematical status is `PASS` after the
transparently registered finite-`beta` repair; the historical caveat is retained because that
repair and the distinct-method cold evidence were required after the initial primary result.

## Result first

`TWO_PARAMETER_CONDITIONAL_STABILITY_THRESHOLD_SURFACE_DERIVED`

Within the declared trace-aligned two-parameter wall-Hessian slice, the missing response is not one
number but a coordinated pair:

- enough effective angular-trace response `tau` to remove the existing field negative direction;
- then enough direct constant-lambda/mu wall curvature `eta` to remove the negative direction that
  otherwise migrates into the joint field-plus-modulus block.

Below the exact `tau` crossing, no `eta` can repair the form. At the crossing, no finite `eta` can
repair it because the field zero mode couples nontrivially to lambda/mu. Above the crossing, the
joint form is nonnegative exactly when `eta` lies at or above the derived surface. Both owned `p`
endpoint domains have a nonempty conditional stabilizing region in this restricted slice.

This does **not** select either response and does not cover the complete wall Hessian.

## Certified numerical landmarks

| `p` domain | `t_critical=tau_critical/tau_infinity` | R06-end representative `eta_mu,critical` |
|---|---:|---:|
| Dirichlet | `[0.4417740924, 0.4423464119]` | `[2.0655163719, 2.1039263946]` |
| free right | `[0.5541992847, 0.5549826638]` | `[3.4930656692, 3.5377848970]` |

The representative `mu` values use `a_F=a_Fprime=2`; the invariant audit coordinate is `nu=k mu`.
The exact full table has two crossing rows and eight preregistered above-crossing samples in
`THRESHOLD_SURFACE.tsv`.

## Interpretation

This makes the earlier R05/R06 split more precise. Free angular traces leave the original field
instability. Fully pinning the angular trace makes the field slice positive, but the joint
lambda/mu direction becomes negative. The two effects are coupled: the first response transfers
the location of the negative mode, while a second independent response is needed to remove it.

That is useful progress for the working stability hypothesis because a future native global-local
closure law now has a quantitative target. It is not evidence that such a law exists, nor permission
to invent one. The action/boundary bridge remains open and the bridge audit's no-map result is
unchanged.

## Verification

- 135 source files are frozen from base `46c7637` by path, blob, bytes, and SHA-256.
- Fifteen exact SymPy controls pass, including the finite-`beta` angular elimination, both response
  boundary problems, and an independent symbolic Sherman-Morrison identity.
- Nested 80/100-digit outward interval runs certify the signs and thresholds.
- A separately coded 80-digit adaptive midpoint reconstruction lies inside every load-bearing
  enclosure. It is an internal same-formula reconstruction, not the independent evidence gate.
- Fourteen exercised semantic/schema mutations are rejected. Formula-level confidence does not
  rest on those catches: the cold audit separately reconstructs the response, raw quadratic form,
  and index changes.
- The fresh cold adversarial derivation uses independent DOP853 shooting boundary-value solves,
  direct/Green overlaps, and a finite-element raw-form inertia calculation. It neither imports nor
  executes the primary code. Its original verdict and repair requests are preserved in
  `COLD_REVIEW.md` and `COLD_RESULT.json`; the registered repair and same-context closure remain
  explicit layers.
- The cold verifier checks 135/135 source identities, both BVPs, direct/Green `n`, direct/formula
  `m`, both FEM inertia transitions, and 25/25 repaired-primary comparisons.
- Six hard-frozen manifests remain unchanged: 127 members and 133 package paths.
- Current-premise guards pass; repository tests remain `70 passed, 1 xfailed`.

## Four evidence gates

1. **Preregistered:** yes, commit `1e6130f`, before inspecting threshold values.
2. **Full or bounded:** complete for the unique root, both owned endpoint domains, and all frozen
   nodes in the declared two-parameter slice; explicitly not the full wall-Hessian or global space.
3. **Independent:** yes. The cold DOP853/FEM reconstruction reproduces `m`, `n`, both crossings,
   all eight thresholds, and the `1 -> 0 -> 0` field-inertia sequence (index one, zero crossing,
   then index zero). The primary adaptive midpoint reconstruction is only a same-formula regression
   check and is not credited as this gate.
4. **Premises:** every imported, conditional, explored, and open item is carried in
   `PREMISE_LEDGER.tsv`.

## Maximum conclusion

An exact conditional inverse threshold surface has been derived for one trace-aligned effective
wall-Hessian slice. It states what a future law would have to supply. It selects no wall response,
boundary, action, carrier, source, bootstrap law, matter branch, mass, or time-persistent state.
