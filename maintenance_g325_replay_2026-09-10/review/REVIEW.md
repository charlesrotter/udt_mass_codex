# Separate-context checker maintenance review

Date: 2026-09-10 UTC. Verdict: **VERIFIED-WITH-CAVEATS for the G325/G326
replay-checker maintenance only. No blocking checker defect found.**

This does not re-prove either scientific result, upgrade a registry grade, establish
full365 completion, accept a physical premise, or confer canon. The entire prior
scientific evidence/review scope remains controlling.

## Candidate, context, and exposure

Baseline independently inspected: branch `grok`, HEAD
`51f189679d4029d750e375be949f41e2f15420fa`. This reviewer did not fetch, pull,
switch branches, stage, or commit in the shared working tree; it was a pinned
bounded maintenance audit under the dispatch. Remote freshness is not an
independent reviewer claim.

Reviewer: separate agent context `/root/replay_maintenance_review`; model
**UNKNOWN**. No different-model claim. Read AGENTS and the bounded startup chain,
then solver-first, verifier-before-record, and completeness-map protocols. The
startup premise check stopped at G326 with
`AssertionError: replay_exact:DERIVATION_RESULT.json` while G325 was already
patched. That startup run is not a post-repair full365 pass.

Exposure: the work order, author diagnosis, baseline/current checker source,
registered commands, and the producers' output construction were read before
reviewer tests. The reviewer authored and ran its own checks before reading the
author's regression test implementation. The later read of the author's tests
is disclosed; this is an adversarial separate-context review, not a blind review.

Reviewed executable SHA-256 values:

| File | SHA-256 |
|---|---|
| `udt_g325_g324_homogeneous_diagonal_linear_modes_2026-09-02/verify_package.py` | `5a272422a731404c119def22d3d92c2f8baf1fc5fd2cd183db1d00a956bc01b0` |
| `udt_g326_g324_homogeneous_offdiagonal_linear_modes_2026-09-02/verify_package.py` | `8d0e15db5a75f32f6d6cd0da2b1baae3d7fa33d48061043f75fd9bf208ebba9f` |

These are the final executable candidates identified by the author. Documentation
closeout is a separate fidelity check if its wording changes after this verdict.

## Defect, repair, and surviving claim

Both original checkers compared complete parsed result dictionaries. The saved
production and independent records contain `python_version = sys.version` from
a June 22 Python 3.10.12 build; the current interpreter is the August 31 build,
also Python 3.10.12/GCC 11.4.0. Independently rerunning all three registered
producer commands for each package found exactly `python_version` different in
production/independent and no difference in the catch record.

The patch excludes only this explicitly selected top-level field in the two
artifacts that actually own it. It retains both strings and their equality flag.
It excludes no catch field and does not recursively discard a nested field with
the same name. Missing, empty, whitespace-only, and non-string provenance reject.

The scientific comparison serializes the remaining parsed JSON with sorted keys
and nonfinite numbers disabled. This distinguishes boolean, integer, and floating
point values that ordinary Python dictionary equality can conflate. All remaining
fields, including schema, status, limits, checks, arrays and extra/missing fields,
participate. Key ordering is immaterial. The intended equality is equality of
typed parsed records, not original JSON whitespace or formatting.

Both aggregate outputs now truthfully report `exact_scientific_replay: true` and
`exact_replay: false` in this environment, and schema version 2 identifies the new
report shape. Explicit gates plus refusal of optimized execution prevent assertion
removal from silently bypassing checks. G326's source hashes and canned-emitter
rejection remain intact. Root audit code still executes these gated replays and
separately checks the preserved historical aggregate JSON; it was not modified.

## Adversarial checks and results

The independently written harness uses recursive type-sensitive equality as its
oracle, without the candidate's JSON-serialization comparison. Actual package
replays themselves reuse the original scientific programs and are consequently
same-code reproducibility checks, not independent scientific proofs.

| Check | G325 | G326 |
|---|---:|---:|
| Helper probes against reviewer oracle | 309 passed | 352 passed |
| Copied-package hostile mutations rejected by actual main | 10/10 | 10/10 |
| Real production/independent/catch commands | 3/3 passed | 3/3 passed |
| Actual aggregate gates | 41 passed | 57 passed |
| Exact baseline checker restored in scratch | Original metadata failure reproduced | Original metadata failure reproduced |
| `-O`, `-OO`, and `PYTHONOPTIMIZE=1` | All refused | All refused |

The 661 helper probes include mutations of every scalar leaf in each saved
scientific record, integer-to-float and boolean-to-integer changes where present,
removal of each top-level scientific field, extra fields, both-sided invalid or
missing provenance, dictionary reordering, nested `python_version`, unrelated
`version`/`runtime` fields, and nonfinite values. This is concrete bounded fault
coverage, not a theorem that every conceivable corruption is detected.

The 20 actual-main mutations cover all three artifacts, extra fields,
integer-to-float assertion counts, false-to-zero result flags, missing/null/empty
provenance, and an injected `python_version` in the catch record. Each failed.
The old exact baseline source was obtained from Git and substituted only in
temporary copies; both original failures went RED at
`replay_exact:DERIVATION_RESULT.json`.

The registered G326 `--output .review_runtime/PACKAGE_VERIFICATION_RESULT.json`
command also passed; its emitted file exactly matches stdout and the original
aggregate JSON remained unchanged. All reviewer child processes were bounded at
40 seconds; the longest measured main-harness child took about 0.20 seconds.
Only CPU was used. No GPU, archive, observational, or network research occurred.

Exact reviewer entry commands, from repository root:

```text
timeout 60s python3 -B maintenance_g325_replay_2026-09-10/review/reviewer_checks.py g325
timeout 60s python3 -B maintenance_g325_replay_2026-09-10/review/reviewer_checks.py g326
timeout 60s python3 -B maintenance_g325_replay_2026-09-10/review/supplemental_checks.py
```

[G325 reviewer results](g325_reviewer_results.json) and
[G326 reviewer results](g326_reviewer_results.json) preserve every subprocess argv,
temporary cwd, return code, stdout, stderr, duration, reviewed hashes, full saved
and freshly replayed records, and before/after package hashes. The original
baseline failure text and every hostile-main failure are included. The primary
harness SHA-256 at execution was
`ba320cac9eeb4e9ad42f027b41cb0c013de86a99aad0906770464f24609997c6`.
[Supplemental results](supplemental_results.json) preserve the registered-output
command and authority-file hashes. Temporary fixtures were removed by their
scoped temporary-directory lifecycle; no original evidence was deleted.

## Preservation, omissions, and limits

Compared all 73 tracked package files against baseline Git blobs before and
after testing. The 71 original non-checker files were byte-identical; only the
two authorized verifier files differ. Independently checked that root
`verify_current_scientific_premises.py`, exact registry TSV, `CANON.md`, fixed
manuscript, and manuscript coverage TSV are byte-identical to baseline. Hashes
prove correspondence only. The protected untracked payloads were not opened,
hashed, mined, or changed by this reviewer.

No scientific algebra/geometry proof was independently reconstructed and no
original review was upgraded. No cross-version interpreter installation, generic
JSON-parser hardening, arbitrary malicious-source proof, or infrastructure
redesign was attempted. The helper is exercised at its actual JSON-dictionary
call sites with a fixed artifact-specific whitelist. G325's pre-existing lack
of G326-style source pins is not repaired or newly certified; its original
producer bytes were checked directly against the baseline for this review.

The author reported nine grouped regression tests passing. Their command/result
records were inspected after the independent checks; they add regression evidence,
not a separate scientific independence axis. The first captured full-audit
attempts used an artificial address-space cap and stopped earlier in Git history
access; those failures do not establish the unrestricted full365 outcome.

Full365 completion and any updated startup-status wording remain outside this
initial checker verdict. A timeout is an incomplete audit, not a failed scientific
theorem and not a pass. The strongest reviewed conclusion here is: the two
checkers now accept the observed runtime-only drift while preserving exact
typed comparison of the replayed scientific records and their original evidence.
