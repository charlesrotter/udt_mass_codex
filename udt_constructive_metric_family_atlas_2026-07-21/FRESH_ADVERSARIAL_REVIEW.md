# Fresh zero-context adversarial review

Reviewer: `constructive_atlas_adversary`

Date: 2026-07-21

Verdict: `VERIFIED-WITH-CAVEATS`

## Reproduction

The reviewer performed a read-only in-memory execution of the exact builder and verifier sources,
plus a separate all-record curvature/kinematics census. The pre-correction replay returned:

- builder: 27 checks passed;
- independent verifier: 388 checks and 42 caught corruptions;
- all seven source-lineage and package-manifest hashes matched;
- metric/coframe value/first/second-jet residuals no larger than
  `2.220446049250313e-16`;
- independently recomputed Riemann, Ricci, and scalar discrepancies exactly `0.0`;
- 32/32 undeformed records flat;
- 128/128 nonzero records Ricci rank four, curvature rank six, shear rank two, twist rank one,
  and nonzero mixed curvature; and
- `dphi`: 18 timelike, 32 exactly zero, zero nonzero-near-null, and 110 spacelike.

The smallest nonzero Ricci and curvature singular values were respectively
`1.0501730840141792e-4` and `1.3849880111025433e-4`, well above the `1e-9` rank threshold. No rank
was in the uncertainty band. All four shifts were nonzero in all 128 nonzero records.

## Caveat found

Each coefficient bank uses one common amplitude `lambda` for all ten latent metric functions and
`phi`. The ten polynomial coefficient rows are linearly independent and the abstract slot chart has
rank ten, but the performed scan is not a ten-amplitude scan.

The independently computed tangent ranks under `(lambda,x0,x1,x2,x3)` were:

```text
rank 5: 112
rank 4:  16
rank 1:  28
rank 0:   4
```

The reviewer required removal of “independently adjustable,” “generic,” “ordinary,” and “normally”
interpretations. That correction is incorporated without changing the historical preregistration.

## Correction review

The reviewer then independently checked the new tangent ledger. All 160 saved tangent matrices
matched to `2.7755575615628914e-17`; the rank distribution reproduced exactly, the smallest
classified nonzero tangent singular value was `0.005108364708641407`, and no record entered the
uncertainty band.

That review requested one final wording correction and stronger catches for the five-parameter
scope. They are incorporated: the package no longer claims “complete local metric behavior,” and
the verifier rejects a parameter count of ten, a ten-amplitude parameter list, or a full-scan
interpretation. The final verifier reports 395 independent checks and 48 caught corruptions.

## Strongest permissible conclusion

In the four preregistered correlated coefficient banks, five deformation values, eight chart
points, and fixed regular split chart, all 160 records were retained; every one of the 128 nonzero
records exhibited the stated ranks, shear, twist, and mixed curvature. These are finite local metric
configurations, not dynamical solutions, evidence of genericity, or UDT physics.
