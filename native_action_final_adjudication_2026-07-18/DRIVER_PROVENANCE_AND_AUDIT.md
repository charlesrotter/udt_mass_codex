# Driver provenance and audit

## Preregistration and repository state

- Final-adjudication contract: `UDT_NATIVE_ACTION_FINAL_ADJUDICATION_PREREG_2026-07-18.md`.
- Preregistration SHA-256: `b8d4bd4bb48cfcfb51bc85fb82d6fdd816b6e6585dd1600fdea3093e39dba457`.
- Preregistration commit: `177e931` (`Preregister final native-action adjudication`).
- Start commit before preregistration: `ca991f6`, synchronized with `origin/grok`.
- Frozen controller SHA-256:
  `9b7c172a395084bf9a7fede33a261de7a61ca7704c3650e9b7828f9ec814b668`.
- C0 SHA-256: `6e977717ca028cabaa198dd14a6a97b3b15740e45485d0ab735f3df0326df192`.
- C1 SHA-256: `d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0`.

The pre-existing modified JSON outputs, transfer ZIP, and scratchpad files were not opened for
editing, staged, moved, or deleted. Only the preregistration and final-adjudication artifacts are in
scope.

## Evidence and verification boundary

The driver read the exact controller and C0/C1, the complete D0-D5 and D6 reports for both arms, the
complete Arm-C report and matrices, and the prior freeze/return records. The accepted fresh isolated
Arm C is the blind adversarial verification pass over the A/B conclusions. No further arm was
launched because the user explicitly ordered a stop before further arms. The final synthesis adds no
new physical premise; it applies Arm C's accepted corrections and replays the load-bearing algebra.

The following immutable package-manifest hashes were verified internally and externally:

```text
Stage-I Arm A  d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19
Stage-I Arm B  a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92
Stage-II Arm A ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a
Stage-II Arm B 30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45
Arm C            99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f
```

## Algebra replay

- Start: `2026-07-18T13:12:26.157396+00:00`.
- Complete: `2026-07-18T13:12:31.370737+00:00`.
- Python: `3.10.12`.
- Execution: CPU only; `CUDA_VISIBLE_DEVICES` was empty for every child script.
- Package manifests: PASS 5/5.
- Source anchors: PASS 6/6.
- Script compilation and execution: PASS 24/24.
- Frozen captured stdout reproduction: byte-exact PASS 24/24.
- Frozen input mutations: none.

`run_final_algebra_replay.py` uses an explicit, preregistered script-name census for each package. It
compiles source in memory, disables bytecode generation, runs from the script's original package
directory, captures stdout/stderr, requires exit zero and empty stderr, compares stdout bytes to the
frozen output, and writes copies only inside this new package. It also verifies every entry in each
input package manifest.

## Provenance firewall audit

Every affirmative status row names a current source. Pre-2026-07-01 content is used only negatively.
Mixed-date and post-dated census/archive containers do not transfer affirmative authority to older
scientific claims. The detailed audit is `PROVENANCE_FIREWALL.tsv`.

## Repository test audit

The required full harness was run with GPU visibility disabled:

```text
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/
```

Result: 71 collected; 69 passed; one expected xfail; one failed. The failed test was
`tests/test_hygiene_header.py::test_covered_results_have_hygiene_header`, and every reported gap was
in an unchanged legacy `simple_metric_*_results.md` file outside this dispatch. The adjudication
artifacts were not named in the failure.

The same CPU suite excluding only that audit returned 68 collected, 67 passed, and one expected
xfail. This establishes that the algebra/operator/solution-space/solver-integrity lanes are green
without claiming the repository-wide hygiene gate is green. The failure is retained rather than
fixed because editing dozens of unrelated historical result headers would expand this task and
conflict with the no-reorganization stop boundary. See `REPOSITORY_TEST_AUDIT.md`.

## Completeness and imposition audit

- No displayed candidate is labeled complete-admissible.
- The exact Arm-C 0/8/5/3 countermodel census is retained candidate-by-candidate in
  `COUNTERMODEL_COMPLETENESS_FINAL.tsv`.
- Conditional C2 and EH classification premises are listed rather than naturalized.
- The round-S2 carrier remains a reopened posit; no target mass selects it.
- No boundary condition, source weight, normalization, `G`, density center/width, or `Xmax` formula is
  invented.
- The shared-static-source route is assessed symmetrically: logically possible, currently unproved.
- The current finite boundary and residual are not erased; no superseded numerical match is used as
  evidence.

## Freeze protocol

After content tests and the repository harness result are recorded, the package manifest will cover
every regular package file except `SHA256SUMS.txt` itself. The package will then be made read-only and
the manifest's external SHA-256 will be recorded in the root return record. The earlier Stage-I,
Stage-II, and Arm-C packages remain read-only and byte-identical throughout.

## Stop boundary

No canonization, GPU work, new arm, physics-branch selection, or repository reorganization was
performed.
