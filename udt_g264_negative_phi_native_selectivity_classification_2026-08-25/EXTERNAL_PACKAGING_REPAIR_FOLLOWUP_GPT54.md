# G264 external packaging-repair follow-up

## Disposition

`ACCEPT_PACKAGING_REPAIR`

## Seal integrity

- `REVIEW_SCOPE.json` SHA-256:
  `00e73b1e803f194d6d57f19350159db383e5f225687c2b51017f2dc8062ad8fe`;
- `REVIEW_MANIFEST.tsv` SHA-256:
  `9e8e80313e5dba613ca066ce142d674732b9faccc64501b16b22b18b41623273`;
- 133 total files;
- 131 manifest payloads, with zero missing, extra, hash-mismatched, or byte-mismatched files.

## Replayed evidence

From a writable ephemeral copy of the sealed `replay_root/`, the reviewer observed:

- `verify_metric_first.py`: 250 cases and 1,000 exact assertions passed;
- `verify_independent.py`: 12,000 exact and 6,025 numeric assertions passed;
- `run_catch_proofs.py`: 18/18 mutations caught;
- `verify_repair_catches.py`: 10/10 mutations caught;
- `verify_package.py`: passed with exactly seven sources resolved as sealed `live_exact` files;
- `verify_packaging_catches.py`: 3/3 attacks caught.

The reviewer also removed Git from `PATH`; `verify_package.py` still passed. No `.git` directory was
present. This independently established that source verification used only the self-contained seal.

## Continuity and scope

The R1--R3 repair-critical files and saved results were byte-identical to the earlier repaired
package. The preregistration, premise ledger, map, ownership atlas, exact derivation, lay report, and
source manifest were byte-identical to the original intake. Only the expected packaging chronology
lines changed in the status and evidence-gate documents.

The bounded G264 scientific landing and ownership ceiling are unchanged.

## Qualification

The isolated external runtime did not contain SymPy, so `derive_selectivity.py` could not be rerun
there and returned `ModuleNotFoundError`. The reviewer explicitly classified this as an environment
limitation rather than a packaging-repair defect. The production script had already passed 27 exact
symbolic checks from a fresh copy of the same seal in the local certified runtime; the external
dependency-free metric-first derivation and all packaging-specific gates reran successfully.

## Source

External Codex reviewer (`gpt-5.4`), sealed 133-file intake
`/tmp/udt_g264_packaging_repair_followup_7n1lsfnb`, completed 2026-08-26.

