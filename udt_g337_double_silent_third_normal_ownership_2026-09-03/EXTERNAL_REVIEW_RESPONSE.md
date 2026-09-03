# External Review Response: G337

## Findings

1. Packaging defect in the sealed replay path: the sealed intake builder writes frozen sources under `/sources/...` ([build_review_intake.py](/work/g337_review.aJV06P/package/build_review_intake.py:57), [build_review_intake.py](/work/g337_review.aJV06P/package/build_review_intake.py:73)), but `verify_package.py` resolves `SOURCE_MANIFEST.tsv` paths as `ROOT / relative` and falls back to `git show` when those root-relative files are absent ([verify_package.py](/work/g337_review.aJV06P/package/verify_package.py:37), [verify_package.py](/work/g337_review.aJV06P/package/verify_package.py:44)). In the copied sealed intake, the registered aggregate check therefore fails unless the reviewer manually reconstructs the expected root layout in a second writable staging directory. That is a repairable packaging/replay issue, not a mathematical refutation.
2. No mathematical defect strong enough to refute the bounded initial-third-jet ownership claim was found in the sealed evidence. The independent rederivation, the implementation-distinct verifier, and the hostile mutation suite all remain consistent with the written claim.

## Authentication

- I inspected only `/intake`, then copied the intake to `/work/g337_review.aJV06P` before running checks.
- `REVIEW_MANIFEST.sha256` matched `sha256(REVIEW_MANIFEST.tsv) = d22dd082c4158a2300de5e9dbe80472c6c0f0e968f1a5a16ca11719ca1b99f54`.
- `verify_review_intake.py` passed on the copied intake: `G337 intake PASS: 33 payloads`.
- The exact copied file set matched the sealed intake: 35 files total = 33 manifest payloads plus `REVIEW_MANIFEST.tsv` and `REVIEW_MANIFEST.sha256`.
- Regenerated outputs were byte-identical to the registered JSON:
  - `_external_DERIVATION_RESULT.json == DERIVATION_RESULT.json`
  - `_external_INDEPENDENT_VERIFICATION.json == INDEPENDENT_VERIFICATION.json`
  - `_external_CATCH_PROOF_RESULT.json == CATCH_PROOF_RESULT.json`
- `verify_package.py` failed in the straight sealed copy for the path-layout reason above, but passed unchanged after I created a second writable staging root `/work/g337_stage.M5hp4k` with the frozen sources placed where that script expects them: `G337 package PASS: 69 aggregate gates`. The staged output was byte-identical to the registered `PACKAGE_VERIFICATION_RESULT.json`.

## Mathematical Review

### 1. `s2` from `n gamma = -2K` and active ADM

With inherited Lie carry `[n,v]=0`, the preregistered identities
`q0 = (1/2)n[gamma(v,v)] = -K(v,v)`,
`s1 = (1/2)n^2[gamma(v,v)] = -F(v,v)`,
`s2 = (1/2)n^3[gamma(v,v)] = -(nF)(v,v)`
are consistent with [PREREGISTRATION.md](/work/g337_review.aJV06P/package/PREREGISTRATION.md:35) and [EXACT_DERIVATION.md](/work/g337_review.aJV06P/package/EXACT_DERIVATION.md:23).

Using
`F = nK = Ric3 + tau K - 2B - Lambda gamma`, `B = K gamma^{-1} K`,
I rederived
`nF = nRic3 + (ntau)K + tau F - 2 nB - Lambda n gamma`.
On exact double silence `K(v,v)=0` and `F(v,v)=0`; also `n gamma(v,v) = -2K(v,v)=0`. Therefore
`((ntau)K)(v,v)`, `(tau F)(v,v)`, and `(Lambda n gamma)(v,v)` vanish, leaving

```text
s2 = -(n Ric3)(v,v) + 2(nB)(v,v).
```

The inverse-metric sign is also correct:
`0 = n(gamma gamma^{-1}) = (n gamma) gamma^{-1} + gamma n(gamma^{-1})`
with `n gamma = -2K`, so
`n(gamma^{-1}) = 2 gamma^{-1} K gamma^{-1}`.
Hence

```text
nB = F gamma^{-1} K + K gamma^{-1} F + 2 K gamma^{-1} K gamma^{-1} K,
```

including the retained cubic `K` term. The sign flow here is internally consistent and matches [EXACT_DERIVATION.md](/work/g337_review.aJV06P/package/EXACT_DERIVATION.md:41).

### 2. Uncommuted Ricci variation for `h = -2K`

Starting from the standard covariant first variation

```text
(delta Ric)_ij = 1/2 (D^k D_i h_jk + D^k D_j h_ik - D^k D_k h_ij - D_i D_j tr h),
```

and substituting `h = n gamma = -2K`, `tr h = -2 tau`, I obtain

```text
(n Ric3)_ij
 = -D^k D_i K_kj - D^k D_j K_ki
   + D^k D_k K_ij + D_i D_j tau.
```

This agrees with [EXACT_DERIVATION.md](/work/g337_review.aJV06P/package/EXACT_DERIVATION.md:54). I found no evidence that the sealed derivation illegally used the momentum constraint to commute derivatives away. The independent verifier computes this formula directly rather than time-deforming the full metric, and it passed all 26 exact checks.

### 3. Complete-field ownership vs compressed-tuple ownership

The retained formula for `s2` depends on `Ric3`, `K`, `F`, and especially spatial derivatives of `K` through the Ricci variation term. Those are part of the smooth complete initial fields `(gamma,K)` and their spatial jets, so the initial inherited third jet is fixed by the complete fields plus the active conditional equation. That is an initial-data ownership statement only; it is not a finite-time, observer-time, persistence, or stability theorem. This boundary is stated consistently in [PREREGISTRATION.md](/work/g337_review.aJV06P/package/PREREGISTRATION.md:64), [EXACT_DERIVATION.md](/work/g337_review.aJV06P/package/EXACT_DERIVATION.md:67), and [PREMISE_LEDGER.tsv](/work/g337_review.aJV06P/package/PREMISE_LEDGER.tsv:15).

The compressed pointwise tuple `(R,b,C,Lambda,mu)` does not contain those spatial jets, so tuple ownership is not forced.

### 4. Exact unequal-weight twin attack

The sealed package provides two unequal-weight controls per branch with the same pointwise tuple:

```text
R = 319/200, mu = 16/25, |b| = 1, C = -7b/25,
Lambda = R/2 - 2 b^2 mu + 3 b^2 mu^2 = 7463/10000.
```

The two geometries
`(w1,w2,x) = (1/4,1/2,1438/1919)` and `(1/3,1/2,4071/6157)`
have distinct invariant `|dR|^2` values
`663665041/48000000` and `8714316107/1296000000`,
so they are not the same spatial germ in disguise.

For `b=-1`, the independent verifier rederived
`s2 = -11982281327/699840000` and `-207122235829/18895680000`.
For `b=+1`, it rederived the sign-reversed pair.
Thus both exact twin pairs share `(R,b,C,Lambda,mu)` branchwise, satisfy `q0=s1=0`, remain invariantly distinct through `|dR|^2`, and still give different `s2`. That defeats pointwise-tuple ownership exactly as claimed.

### 5. Equal-weight reduction and both strict roots

Using G332/G336,
`C = b(1-2mu)` on first-order silence and
`Lambda = R/2 - 2b^2 mu + 3b^2 mu^2`
([udt_g332.../EXACT_DERIVATION.md](/work/g337_review.aJV06P/sources/udt_g332_weighted_contact_vacuum_constraint_embedding_2026-09-03/EXACT_DERIVATION.md:107), [udt_g336.../EXACT_DERIVATION.md](/work/g337_review.aJV06P/sources/udt_g336_silent_direction_second_normal_response_2026-09-03/EXACT_DERIVATION.md:115)).

On the equal-weight control `w1=w2=719/1600`, `R=319/200` is constant and the double-silent condition forces `b^2=1`, so the two strict roots are `b=±1`. I checked the homogeneous reduction used by the hostile suite:

- `k_h = -b mu`
- `k_v = b(1-mu)`
- `tau = b(1-3mu)`
- `Ric_h = (R-2)/2`
- `Ric_v = 2`
- `(nRic3)_h = 4b`
- `(nRic3)_v = -8b`

and the full third response combines to
`s2 = 8 b mu`, giving
`s2 = -128/25` for `b=-1` and `s2 = +128/25` for `b=+1`.
I found no basis for a universal preferred sign or a universal nonzero claim beyond this control, and the sealed package does not overclaim either point.

### 6. Finite boost pair matrix and terminal `Phi`

For fixed finite boost `z`, the package’s third pair-metric jet

```text
2 s2 [[sinh(z)^2, sinh(z)cosh(z)],
      [sinh(z)cosh(z), cosh(z)^2]]
```

and terminal scalar third jet
`n^3 Phi / 2 = s2 sinh(z)^2`
are consistent with the inherited-pair structure from G333/G334/G336 and with the 30 registered fixed-boost controls in `DERIVATION_RESULT.json`. At zero boost, terminal `Phi` is blind while the full pair matrix can still carry nonzero third response. The sealed package keeps that distinction.

## Check Replay

- `derive_double_silent_third_response.py`: passed, 149 checks.
- `verify_double_silent_third_response_independent.py`: passed, 26 checks, no production import/result read.
- `run_catch_proofs.py`: passed, 17 of 17 hostile mutations caught.
- `verify_package.py`: failed in the straight sealed copy for source-path-layout reasons; passed unchanged in a second writable staging root that restored the root-relative frozen-source layout expected by the script.

## Premise Audit

- The premise ledger and live premise registry consistently mark Universal Reciprocity/DDR and the G312 arena as owner-adopted provisional, not derived or canonized.
- I found no use of topology, matter, mass, source, action, observation, scale, `X_max`, physical germ population, history selection, stability, or canon as mathematical inputs to the bounded third-jet claim.
- The maximum supported conclusion remains the initial inherited third normal jet only, not explicit evolution, persistence, or stability.

## Conclusion

The bounded G337 mathematical landing survives fresh adversarial rederivation and replay. The only defect I found is implementation/package-level: the sealed intake’s source layout is not directly compatible with the registered aggregate verifier and requires a repair so the copied intake can replay that gate without reconstructing a repo-like root. That defect is real but does not refute the underlying bounded third-jet ownership result.

ACCEPT_WITH_REPAIRS__G337_BOUNDED_THIRD_JET_OWNERSHIP_RETAINED
