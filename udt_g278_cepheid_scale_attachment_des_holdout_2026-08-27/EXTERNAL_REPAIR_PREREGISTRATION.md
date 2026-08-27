# G278 external-review repair preregistration

Date: 2026-08-27

External verdict: `ACCEPT-WITH-REPAIRS`

Raw response SHA-256:
`33f115f9820fa8f536da4216d0fd04268cdb12c8439dbbfbca48eb015ac14178`

The reviewer independently reproduced every load-bearing numerical result and retained the bounded
scientific landing unchanged. The following repairs are packaging-only and are frozen before any
repair implementation.

## R1 — make the sealed intake directly replayable

Change only `build_review_intake.py` so every `SOURCE_MANIFEST.tsv` payload is copied to the same
intake-root-relative path already consumed by the production, independent, and package verifiers.
Copy the additional G275--G277 contextual sources into their repository-shaped intake-relative
paths as well. The package scripts and scientific artifacts remain unchanged.

Acceptance:

1. an intake-shaped replay runs without manually rearranging sealed files;
2. all ten source hashes pass from the intake root;
3. production, independent, hostile, diagnostic, and package replays reproduce the accepted values.

## R2 — add a detached manifest seal

After writing `REVIEW_MANIFEST.tsv`, write `REVIEW_MANIFEST.sha256` containing its exact SHA-256 and
basename. Report the detached-seal hash and total physical file count separately. This is an outer
seal; it is not inserted into the payload manifest and no impossible self-hash is attempted.

Acceptance:

1. `sha256sum -c REVIEW_MANIFEST.sha256` passes inside the sealed intake;
2. all payload rows still match exact bytes and hashes;
3. the follow-up authorization identifies both the manifest hash and detached-seal hash.

## R3 — make the registered sealed command surface exact

Remove `python3 verify_current_scientific_premises.py` from the sealed package's `COMMANDS.md`, because
that repository-wide startup/premise audit requires the full repository and is not an intake replay.
Continue to run it locally as a separate repository banking gate. Add an explicit sentence making
that distinction.

Acceptance:

1. every command advertised as a sealed-package replay is present and runnable in the intake;
2. the repository premise audit still passes locally;
3. no scientific artifact, number, model choice, or landing changes.

## No-change contract

These repairs may not:

- refit or recompute a preferred resolution;
- alter observational masks, covariance routes, tolerances, or results;
- change the metric, kernel, state, transfer law, angular sector, history, `X_max`, or CMB model;
- introduce `P1`, an LCDM distance, a DES offset, or any observational retuning;
- touch protected or unrelated work.

## Follow-up gate

The repaired package remains `ACCEPT-WITH-REPAIRS` until a fresh sealed repair-only follow-up verifies
R1--R3 and retains `SCALE_ATTACHMENT_RESOLUTION_OR_SUBSET_SENSITIVE` unchanged.
