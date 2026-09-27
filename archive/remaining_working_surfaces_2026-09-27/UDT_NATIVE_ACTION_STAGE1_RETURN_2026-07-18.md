# UDT Native-Action Stage-I Return — 2026-07-18

**Status:** ARM A AND ARM B COMPLETE, MECHANICALLY CHECKED, FROZEN, AND HASHED

**Stop line:** Stage II, Arm C, independent physics adjudication, cross-arm convergence analysis, and
GPU work have not been launched. These packages are returned to Charles for audit.

## Exact cold inputs

Both arms began with exactly the following byte-identical C0/C1 files and no other project material:

```text
6e977717ca028cabaa198dd14a6a97b3b15740e45485d0ab735f3df0326df192  UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md
d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0  UDT_NATIVE_ACTION_COLD_PACKET.md
```

The repository, controller dispatch, Stage-II archive, LIVE/HANDOFF, other arm, and host GPU devices
were absent from each arm's separate Bubblewrap mount namespace. The two sessions shared no work
directory, conversation, output, or transcript. Web use was disabled; network access existed only
for the model provider.

## Frozen package returns

### Arm A

- Package: `native_action_stage1_2026-07-18/arm_A/`
- Model/session: `gpt-5.6-sol` / `019f72f1-8a16-7862-9573-d051361ae85f`
- D0–D5 SHA-256: `22804ff3c744b8857481908cd4cb7bc8775c67a158de58cf570c0fea924e4ddb`
- Files covered by package manifest: 29
- CAS bundle: 11 scripts and 11 captured outputs
- External SHA-256 of `arm_A/SHA256SUMS.txt`:
  `d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19`

Arm A's D0 preserves a disclosed operational deviation: its final self-check used a freshly created
`/tmp_check_output` in the namespace's private empty tmpfs. That file contained only output from the
arm's own scripts and could not expose host, repository, Stage-II, or other-arm content. The driver
classified it as noncontaminating but audit-visible; the cold output was not edited.

### Arm B

- Package: `native_action_stage1_2026-07-18/arm_B/`
- Model/session: `gpt-5.4` / `019f72f1-db2a-7ed0-9eac-b861d4f320ec`
- D0–D5 SHA-256: `07f9519049d0993d35dbbc68f86ffe1f7da1339e1eb888dbdfe90a75ac34ba68`
- Files covered by package manifest: 15
- CAS bundle: 4 scripts and 4 captured outputs
- External SHA-256 of `arm_B/SHA256SUMS.txt`:
  `a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92`

A proposed cross-provider Arm B launch was rejected before execution because third-party packet
transfer lacked explicit approval. No packet bytes were sent and no external session was created.
The separately isolated `gpt-5.4` arm was preregistered as the approved-provider fallback before its
successful launch.

## Mechanical freeze gate

For each arm, the driver verified:

- D0 through D5 exist once, in order, with D1 MAP before D2;
- D0 has the exact input hashes, completion timestamp, initial inventory, and exposure declaration;
- every CAS script has a nonempty matching captured-output file;
- every script compiles, exits zero on rerun, and reproduces its captured output byte-for-byte;
- D3 states what every script does and does not verify;
- no prohibited controller/repository/Stage-II context appears in the arm-authored output;
- the successful outer terminal transcript and the earlier no-model-output network-preflight failure
  transcript are complete and preserved;
- `sha256sum -c SHA256SUMS.txt` passes for every manifested file.

The per-arm `DRIVER_PROVENANCE_AND_AUDIT.md` files hold the exact mechanical record. The manifests
cover every package file except themselves; the manifest hashes above are recorded externally here.
The package directories were made read-only after this freeze.

## Audit boundary

No Stage-I physics conclusion is banked here. The driver has not built an A-versus-B agreement table,
translated a conclusion, selected a branch, or treated agreement as evidence. Those operations belong
after Charles audits these immutable cold packages and separately authorizes any next stage.
