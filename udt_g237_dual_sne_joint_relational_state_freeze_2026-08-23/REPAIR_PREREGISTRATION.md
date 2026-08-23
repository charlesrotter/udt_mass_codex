# G237 external-review repair preregistration

Date: 2026-08-23

Trigger: fresh external `gpt-5.4` verdict
`G237_SCIENTIFIC_OR_EVIDENCE_REPAIR_REQUIRED`.

## Frozen scientific result

No state coordinate, covariance, knot, sample, residual, tolerance, resolution, or scientific
landing may change in this repair.

Pre-repair SHA-256 anchors:

| artifact | SHA-256 |
|---|---|
| `JOINT_STATE_RESULT.json` | `0407fb233158beb06fba771d78e1e2ec66e1d857858b4a094e78d294d417c951` |
| `FROZEN_PRIMARY_K12_STATE.json` | `88d3006a646f2be105a3fb15f2c4c694732b884da97f8fdeefc39323e6bbc8cf` |
| `JOINT_STATE.tsv` | `548219b37459a12c590a43568120e519fc58fa79b322c2059a7b06ba8b88c4b1` |

`INDEPENDENT_RAW_GLS.json` has pre-repair SHA-256
`725d8e57e4ab9fc927a3cc7a3a0ee49bebb8da372bf137d58acffde9accd7239`. Its numerical fields must
remain identical, but its covariance-premise label may be expanded as repair R4.

## Authorized repairs

### R1 — remove the independence overstatement

Replace “two independent SNe maps” in `LAY_REPORT.md` with wording that identifies two
de-overlapped processed releases without asserting statistical independence.

### R2 — self-contained chronology replay

Export the minimal raw Git object chain into a sealed bundle:

- commit object body;
- root tree object;
- G237 package tree object;
- committed preregistration blob content.

Add a verifier that recomputes Git object IDs, parses the tree entries, proves the commit-to-root,
root-to-package, package-to-preregistration, and preregistration-content links, and requires no live
Git repository. Keep `build_chronology_proof.py` explicitly typed as the repository-side evidence
exporter, not a sealed replay.

### R3 — command/payload alignment

Include `build_review_intake.py` in the repaired sealed payload because it is listed in
`COMMANDS.md`. Separate repository-side preparation commands from sealed replay commands.

### R4 — machine-readable covariance caveat

Change only the independent artifact’s covariance-premise label from `CHOSE_ZERO_BLOCK` to the full
production wording:

```text
CHOSE_ZERO_AFTER_EXACT_CID_DEOVERLAP__UNKNOWN_SHARED_SYSTEMATICS_OPEN
```

No numerical field may change.

## Repair certification

1. The three frozen primary artifacts retain their exact SHA-256 hashes.
2. Every numeric subtree of `INDEPENDENT_RAW_GLS.json` remains exactly equal before and after R4.
3. The self-contained chronology verifier passes in a directory with no live `.git` objects.
4. The repaired intake’s registered replay passes in an ephemeral copy.
5. Source hashes, production/independent tolerances, raw-residual gates, and mutation catches remain
   unchanged.

Maximum repair return:

```text
G237_REPAIRS_IMPLEMENTED__SCIENTIFIC_LANDING_UNCHANGED__FOLLOWUP_REVIEW_REQUIRED
```
