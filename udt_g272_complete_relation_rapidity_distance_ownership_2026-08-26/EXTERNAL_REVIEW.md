# G272 external adversarial review

Reviewer: external Codex `gpt-5.4`

Date: 2026-08-26

Sealed intake: `/tmp/udt_g272_review_bimn7dnu`

`REVIEW_SCOPE.json` SHA-256:
`a9c31956c95bb0af42a154d49f3903b2ef48b91438abbbccdf4916a6b8d0d7a8`

`REVIEW_MANIFEST.tsv` SHA-256:
`a8b15b533e0a4653a89e5a745e40d72667ef0956b1322a8c0d956f542a4a3d0e`

Raw response SHA-256:
`e38e02236779de57c7927514409698c7edc69d5f6c209bad2389bf799f1f4fd7`

## Landing

`ACCEPT_BOUNDED_G272_LEAD`

Repairs: none.

## Strongest surviving bounded conclusion

The reviewer found that

```text
Gamma_PT >= 1
```

is correctly derived from

```text
Gamma_PT - 1 = ((r - 1)^2 + r^2 ||W||^2)/(2r),
```

that `eta_PT=arcosh(Gamma_PT)` is correctly typed as the nonnegative transported rapidity, and that

```text
rho_PT = tanh(eta_PT) = sqrt(1 - M_PT^2)
```

is exactly the norm of the full transported-frame spatial state `(v_parallel,v_perp)`.

The reviewer accepted the `W=0` planar/radial control, affine invariance, reversal-even magnitude,
same-`delta`/different-`W` separator argument, and bounded G271 first-jet join on their stated scope.
The signed coordinate `chi=tanh(delta)` survives only as the exact oriented planar stratum, not as
the complete nonradial state.

The profile

```text
Delta phi = artanh(x/X)
```

follows exactly only after the separately labelled `CONDITIONAL_DISTANCE_ATTACHMENT` `x/X=chi`.
The reviewer agreed that `c_E` alone does not furnish the missing length scale by dimensional type
and found no promotion of transported-frame coordinates into local signal velocity, conventional
distance, selected history, or `X_max`.

Manifest verification and the registered no-write replay passed. The reviewer judged the production
checks, independent verification, mutation catches, and source freeze nonvacuous.
