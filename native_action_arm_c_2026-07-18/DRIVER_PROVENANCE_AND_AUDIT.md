# Arm C — driver provenance and mechanical audit

**Stage:** isolated adversarial Arm C only. This record checks provenance, completeness, and
reproducibility; it does not perform final cross-arm physics adjudication or canonization.

## Outer-run provenance

- Runner: OpenAI Codex CLI `0.144.5`
- Model: `gpt-5.6-sol`
- Reasoning effort: `high`
- Successful session: `019f752f-a8a3-7ec3-bac3-b4ddfbf874c1`
- Outer transcript start: `2026-07-18T08:24:44-04:00`
- Arm post-assembly gate: `2026-07-18T12:44:14Z`
- Outer transcript exit: `2026-07-18T08:44:44-04:00`, code `0`
- Prompt SHA-256: `e39220926dceaf731d176e066089c30d15f60ce31b3fbf5c7d473ba6b5d321d0`
- Successful launch-script SHA-256: `1b57d681fdd49a216bdc726e2debac2a79f0bc09c891ac6b8f4f5a8ab9624dc9`
- Successful outer-transcript SHA-256:
  `9fd7b15007125cb94a9cc621c189997065aa05cff1c733ee59d461ba9dfb5b14`

The exact pre-disclosure prompt and intake rubric were committed and pushed at `9608efe` before
Arm C saw any project material. A managed security review initially blocked API transport because
the intake contains private repository material. Charles was informed of that risk and explicitly
authorized transmission before the successful run.

The first transport attempt exited code `1` before any model response or return artifact because the
outer managed sandbox blocked the Codex API. Its complete transcript is preserved as
`PRELAUNCH_NETWORK_FAILURE_TRANSCRIPT.txt` (SHA-256
`c3ab0ff826da26dc671d0d470c0c3cd2d679e26a5b688f2ec684cafc3ee8d649`). The successful run used a
new temporary home, new empty return directory, and new ephemeral session with the identical frozen
prompt and project mounts.

## Isolation and exact exposure

The successful process ran in a fresh Bubblewrap mount namespace. The repository was not mounted.
The namespace exposed system runtime dependencies, a minimal temporary home containing only required
authentication/runtime state, one empty writable `/return`, and these read-only project inputs:

- controller;
- exact C0 and C1;
- complete immutable Stage-I Arm-A and Arm-B packages;
- complete immutable Stage-II Arm-A and Arm-B packages;
- exact A1-A6 packet and its root manifest;
- the aggregate Arm-C input manifest.

The aggregate manifest enumerates 212 input files. The aggregate manifest itself was the 213th
regular project file exposed. No project symlink was exposed. The arm verified all aggregate entries
before analysis and after artifact assembly.

Integrity anchors:

- aggregate 212-entry manifest:
  `010e7922423ab724467d94f6408425905fb872c5ccaebc5fa5941fc66080f2dc`;
- A1-A6 134-entry manifest:
  `85776969410e6dc8bee6b1aa901331dcc139e718dbdfd28c593df3f2054408b7`;
- Stage-I Arm A package manifest:
  `d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19`;
- Stage-I Arm B package manifest:
  `a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92`;
- Stage-II Arm A package manifest:
  `ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a`;
- Stage-II Arm B package manifest:
  `30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45`.

Provider connectivity existed only to run the isolated model session. Web search was disabled. No
host GPU device was exposed, and no GPU work ran.

## Returned artifact census

`ARM_C_RETURN/` contains exactly 16 regular files and no symlinks:

- the C.0-C.9 report;
- a 39-row claim matrix;
- a 16-row complete-foundation countermodel matrix;
- a 28-row smuggle list;
- the byte-identical received 212-entry input manifest;
- five original `cas_armc_*.py` scripts and five matching captured outputs;
- the CLI-captured final response.

The return contains no placeholder markers. All three TSV files are rectangular with their declared
headers. The report includes every required sector: strongest unique-action attempt, C-squared, EH,
carrier covariance, variation domain, boundary charge, and the three-part mass/virial test. Its stop
line explicitly withholds final adjudication, canonization, GPU work, further arms, and repository
reorganization.

## Independent driver verification

After the isolated process exited, the driver independently:

1. rechecked the A1-A6 manifest and all four frozen Stage-I/II package manifests from repository
   source;
2. byte-compared `RECEIVED_ARM_C_INPUT_SHA256SUMS.txt` with the committed aggregate manifest;
3. compiled every `cas_armc_*.py` with a separate temporary bytecode cache;
4. reran every script with bytecode writes disabled and compared stdout byte-for-byte with its
   captured `_out.txt`;
5. verified the three TSV schemas and row counts;
6. scanned for placeholders and required report sections;
7. checked the successful transcript bookends, exact model/session metadata, completion line, and
   exit code `0`.

Independent script results:

| Script | Driver result |
|---|---|
| `cas_armc_unique_action_weights.py` | reproduced exactly; PASS 11/11 |
| `cas_armc_carrier_covariance.py` | reproduced exactly; PASS 8/8 |
| `cas_armc_variation_domain.py` | reproduced exactly; PASS 6/6 |
| `cas_armc_boundary_charge.py` | reproduced exactly; PASS 5/5 |
| `cas_armc_mass_virial.py` | reproduced exactly; PASS 5/5 |

The driver did not alter Arm C's scientific report, matrices, scripts, outputs, or final response.
Passing this audit means the return is complete and reproducible; it is not a physics endorsement.

## Freeze boundary

This package is frozen read-only after `SHA256SUMS.txt` is generated and checked. The external hash of
that manifest is recorded in `UDT_NATIVE_ACTION_ARM_C_RETURN_2026-07-18.md`. Original Stage-I and
Stage-II packages remain unchanged and read-only.

**STOP:** final cross-arm adjudication, canonization, GPU work, further derivation arms, and repository
reorganization remain unperformed and require separate authorization.
