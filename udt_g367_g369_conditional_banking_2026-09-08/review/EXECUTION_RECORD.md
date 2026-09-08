# Banking fidelity review execution record

Reviewer `/root/sm_banking_fidelity`,2026-09-08 UTC. Cwd for all commands:
/home/udt-admin/udt_mass_codex. Source-first requirements and code pins precede
new author-guard exposure. All owned artifacts are under this review directory.
Original sources/targets were read-only. The full no-shortcuts, completeness-map
and verifier-before-record protocols plus CROSS_MODEL_VERIFY informed scope,
preservation, exposure and proportional checks; they provide no science premise.

Read-only startup used git status, git rev-parse HEAD and the bounded documents
in source-first order. No git synchronization/mutation was performed by this
pinned delegate. Full349 execution belongs to main session17654; its receipt
was read, not replayed. Exact rows were queried after the reported PASS.
Main's corrected timestamp is observed before04:33:18UTC, not its earlier
informal04:36 estimate; no exact finish instant or separate streams was claimed.

The inspected capture helper is
udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py,
SHA2568ff5469ace76bdfc84188915242abbf3baff35516f9ee3f9ba4b1cbfeb2573ef.
It refuses output overwrite and supplies512MiB AS/60s CPU/60s wall limits.
Python3.10.12 standard library is used by the independent checker; no SymPy,
numerical array library, author verifier or scientific implementation import.
All three runs were sequential in this reviewer context. No resources increased.

## First independent run — retained execution failure

Exact command:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_g367_g369_conditional_banking_2026-09-08/review/independent_fidelity_initial /home/udt-admin/udt_mass_codex python3 -B udt_g367_g369_conditional_banking_2026-09-08/review/check_fidelity_bytes.py
```

Start04:41:04.605425UTC; return1;0.058692046seconds; max RSS30916KiB;
no timeout. Registry assertions completed before git archive returned128
because default Git mmap exceeded the inherited512MiB address-space cap.
stdout empty. Failure preserved in independent_fidelity_initial.stderr/.json.
This was not a source/row mismatch and did not justify raising the cap.

## Unchanged-checker retry with smaller invocation-only Git mapping windows

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=core.packedGitLimit GIT_CONFIG_VALUE_0=32m GIT_CONFIG_KEY_1=core.packedGitWindowSize GIT_CONFIG_VALUE_1=1m python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_g367_g369_conditional_banking_2026-09-08/review/independent_fidelity_retry /home/udt-admin/udt_mass_codex python3 -B udt_g367_g369_conditional_banking_2026-09-08/review/check_fidelity_bytes.py
```

Start04:41:44.731349UTC; return0;0.077710624seconds; RSS23420KiB;
empty stderr, no timeout.199 byte/schema/history assertions pass. Git config
is supplied only through this invocation's environment, with no config-file
write. All original checker source bytes and numerical/resource caps unchanged.
Independent output SHA256ee7949c28edb68a82c1524db279a421e65a50018116a8ade5303ffe8dd1351d0.

## Author focused guard replay

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=core.packedGitLimit GIT_CONFIG_VALUE_0=32m GIT_CONFIG_KEY_1=core.packedGitWindowSize GIT_CONFIG_VALUE_1=1m python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_g367_g369_conditional_banking_2026-09-08/review/author_guard_replay /home/udt-admin/udt_mass_codex python3 -B udt_g367_g369_conditional_banking_2026-09-08/check_banking.py
```

Start04:42:15.117923UTC; return0;0.525664074seconds; RSS58560KiB;
empty stderr/no timeout. Five banking guards plus startup pass; all six
temporary-fixture mutants reject for the matching reasons. Output SHA256
23ec24261432583d5a5c8b74cec94ca8762e28d7957a03a18d96e11e8b42d4a3;
cmp against ../banking_checks_initial.stdout returned0. This is shared-code
regression, not new scientific verification. Temporary fixtures do not touch
maintained targets or original sources.

## Other correspondence checks and target pins

Before target exposure, sha256sum authenticated all nine original scientific
candidate/result/review files and the349 registry pin. A scoped git diff
against baseline for the original campaign/CANON/manuscript/coverage was empty.
Filtering original SHA256SUMS to its own package and sha256sum --check --quiet
passed all87 entries. Initial SM2 stderr and repaired stdout match their
original reviewer counterparts by cmp.

After target exposure, independent git-show/sha256sum against baseline yielded:

```text
LIVE.md 3464562486cf150ad0be7c00073fc27647c1c0c0c1efc30850264146877bb147
HANDOFF.md 2d77d4c52a316b1116012f2d67519c5299d31d4528c0b70848d6e589ae06b9a7
CURRENT_RESEARCH_PROGRAM.md ffad8d015c5c3d9f3b202430c4ab903cfd4232619032680e0e216e635adf680a
```

These match the historical three control entries in original SHA256SUMS;
they are not expected hashes for updated live text. Exact maintained targets
at direct-review completion,04:43UTC:

```text
AGENTS.md 0a6f34e40575d0a909410d3473f9487a364d62b05f849bb8137ecdd0bb0739df
LIVE.md 12e7123b24e4147fe6423f839a4135f863725416066a182897b2c46dc8539ee7
HANDOFF.md c97a0fc65ff15c47fb0c2f652bfcd46e23193ee94a11e90da5c4319e193c9d94
CURRENT_RESEARCH_PROGRAM.md f3c4054d46a1660058f08afacfc0407cecb25ef610b0adf56d56eac0d97ae9cd
CURRENT_SCIENTIFIC_PREMISES.md 6620766d87c13510f2e62ff6400205ce2e1681ad6353ed429cbcce0c9fae3672
INDEX.md bdd7705f7a33289c1c6b757315c0dd768802f62755eeb6547f3171c1a8d39f74
MEMORY.md f0d034ba9e23b02fc7795b104f54b48067b96557355e25735b64094c98138d4d
../WORK_ORDER.md b614f90be74d2d15715f5e15023adf780abfc1aaf504bb034a9b3eb90a0c0ac6
../EXECUTION_RECORD.md 41c7b6c50e45c2b1afcbdd1f3147b961bd9d2507cd27a81282c23f166abdc942
```

These current surfaces still report integration IN PROGRESS. Later completion
wording is a main-context action, not silently covered as these exact bytes.
Final repeated git rev-parse HEAD remained the declared baseline. Full352
audit, publication, original scientific replays, host-wide process/backup
checks and the next reconstructibility science were not performed here.
