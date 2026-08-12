# Fresh sealed adversarial review

Date: 2026-08-12

Reviewer: external Codex `gpt-5.4`, high reasoning, ephemeral, web disabled, read-only

Session: `019ff72a-3858-7df1-9964-f6d29629b996`

Sealed intake: 26 files

`REVIEW_SCOPE.json` SHA-256:
`de5ad3b367c4cbd49cdc35f211213481e42c2d4a72b3636f0046d74da9b27a98`

Raw final-message SHA-256:
`3652fc9d486bc31f10e33d3168a2cfca0d63d10f77a0373ae9f18a322a4b6bf9`

## Verdict

```text
ACCEPT__VERIFIED_WITH_CAVEATS
```

The reviewer independently re-expressed the load-bearing algebra and replayed it on 200 fresh
rational samples. It reproduced:

- the tangent/screen split conditional on a supplied timelike immersion;
- the exact complete-coframe pullback;
- `C=S+Z Y^-1` on the invertible-`Y` stratum;
- the `PSD(2)` image and three-class inertia atlas;
- the calibrated terminal formulas; and
- the curvature-atlas regrade as a narrowing of role rather than a rewrite.

Its clean replay returned:

```text
200/200 direct pullbacks,
200/200 reduced Gram identities,
200/200 pair-coordinate covariance checks,
200/200 screen-frame covariance checks,
40/40 encountered terminal reconstructions,
all three inertia classes represented.
```

## Binding caveats

1. The result does not derive a physical realization. `F` remains a supplied regular timelike
   immersion. This caveat concerns realization ownership, not the already derived terminal
   reciprocal-`c_E` readout on a supplied relation.
2. The package's stdlib `Fraction` replay is implementation-independent in its matrix arithmetic
   but not fully hermetic, because it reopens the production JSON at the end. The package verifier
   is primarily an administrative/status/manifest gate. The reviewer's separate 200-sample replay
   is the fresh load-bearing algebra check.

Neither caveat changes the bounded landing.

## Reviewer final return

> `ACCEPT__VERIFIED_WITH_CAVEATS`
>
> The load-bearing finite-dimensional algebra is correct within the sealed scope. I independently
> re-expressed it and replayed it on 200 fresh rational samples: the tangent/screen split from a
> supplied timelike immersion, the exact pullback identity, the reduced object `C=S+ZY^-1`, the
> `PSD(2)` image of `C^TqC`, the three-class inertia atlas, and the calibrated terminal formulas all
> check out as stated. The curvature regrade is also mathematically sound as a narrowing of role,
> not a rewrite of the earlier ambient atlases.
>
> The caveats are strict. First, this does not solve the physical selector problem; it assumes the
> selector as a supplied regular timelike immersion `F`, and the package is valid only if that
> conditionality is never weakened. Second, the “independent” JSON is not fully hermetic: the
> independent script reopens and asserts the production JSON, and the package verifier is largely
> a manifest/status gate. The internal result supports consistency, but it is not by itself a
> clean-room proof.
