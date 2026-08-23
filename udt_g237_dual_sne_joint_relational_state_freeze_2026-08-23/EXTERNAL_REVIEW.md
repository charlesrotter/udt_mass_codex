# G237 fresh external adversarial review

Date: 2026-08-23

Reviewer: external Codex `gpt-5.4`, high reasoning, web disabled, sealed ephemeral intake.

Intake: `/tmp/udt_g237_review_dignag7a`

`REVIEW_SCOPE.json` SHA-256:

```text
8e6ab4424f74464ba20d05a5d4043851d7cb68cc88455e3165066c62cb70c397
```

## Verdict

```text
G237_SCIENTIFIC_OR_EVIDENCE_REPAIR_REQUIRED
```

The reviewer verified the 40-payload seal and reproduced the tree digest. It accepted the
scientific core: the estimator algebra, direct raw simultaneous GLS, all four raw adequacy gates,
cross-route tolerances, 56 output rows, immutable `K=12` freeze, and absence of a hidden P1,
`X_max`, Lambda-CDM, optimizer, smoothing, monotonicity, or held-out-outcome fit.

It found no scientific, type, source-provenance, or hidden-fit failure. It required:

1. replace “two independent SNe maps” in `LAY_REPORT.md`, because statistical independence is not
   derived;
2. make the chronology proof independently replayable from the sealed intake without live Git
   objects.

It optionally recommended including `build_review_intake.py` when that script appears in the
command registry and mirroring the full covariance caveat in the independent machine artifact.

The reviewer explicitly accepted carrying the frozen state without refitting into a separately
typed held-out query, while retaining a separate source/operator audit for BAO or CMB.

## Error classification returned

- scientific error: no;
- statistical error: one wording overstatement only;
- type error: no;
- source-provenance error: no;
- scaffolding error: yes, chronology replay packaging;
- evidence-contract error: yes, chronology replay packaging.
