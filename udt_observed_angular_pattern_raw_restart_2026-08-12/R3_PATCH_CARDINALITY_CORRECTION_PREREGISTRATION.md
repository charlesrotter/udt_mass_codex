# R3 TreeCorr patch-cardinality correction — preregistration

Date: 2026-08-13  
Status: `PREREGISTERED__FAILURE_REPRODUCTION_AND_CONSTRUCTION_REPAIR_ONLY`

## Trigger and preserved evidence

The guarded R3 production run completed and atomically checkpointed the first `48/194` selections,
ending at `CMASS_North_f4_g06`, then stopped before writing the first South checkpoint. There are no
`.tmp` or `.partial` checkpoint files.

The first South `DR` call raised:

```text
RuntimeError: Cross correlation requires both catalogs use the same patches.
```

The failure is recorded in `/tmp/udt_boss_r3_checkpoints_guarded/R3_SERVICE.log` with SHA-256
`03bec6eb1310e283f07ce399afb2c0538cf558f8e7b68a8f1a0cdf54b8e68174`. The completed-cell path-list
digest is `db334ebfda4b767d47f8454f7e0194251edd475b6036a3d9c417d615c40b6675` and the pre-repair production
program SHA-256 is `7806327137fc2351693855dd9a71bfe1a3541e7b67c11478f450f6c859bcbb88`.

The service wrapper also returned success despite the Python traceback. That is an operational exit-
propagation defect, not an R3 scientific result.

## Whole bounded question

Can the already frozen HEALPix patch labels be supplied to TreeCorr without TreeCorr independently
shrinking the declared patch cardinality when one catalog lacks the largest occupied label, while
leaving every R3 selection, weight, bin, pair count, deletion, normalization, covariance formula,
rank rule, and conclusion contract unchanged?

This is an operational data-pipeline repair. It is neither metric-led nor template-led physics and
does not target a BAO feature, preferred scale, UDT response, CMB relation, or `X_max`.

## Exact diagnosed mechanism to test

The frozen code gives each complete catalog a common `patch` label array and common `npatch` value.
TreeCorr `Catalog._set_npatch`, however, replaces that value with `max(patch)+1` after loading. On the
first South selection the selected data omit the terminal label while the selected random catalog
contains it. The two independently split catalogs therefore reach the cross-correlation with unequal
cardinalities even though their labels refer to one common registered sky atlas.

The proposed category-A correction is to construct the public TreeCorr input as explicit lists of
nonempty single-patch catalogs. Every child catalog retains its original patch ID and the common full
registered `npatch`. TreeCorr publicly accepts a catalog or a list of catalogs. No point changes
patch, no empty block is invented, and no physical or statistical choice changes.

## Premise and choice ledger

| Item | Status | Ownership |
|---|---|---|
| `194` selections, four lanes, `119` analysis bins | `pinned-by-THEORY` | banked `R3_PREREGISTRATION.md` |
| NSIDE `4/8/16` nested HEALPix geometry | `pinned-by-THEORY` | banked R3 preregistration |
| selected data/random occupancy union | `pinned-by-THEORY` | banked support-typing correction |
| original integer fine-patch membership | `pinned-by-THEORY` | frozen full-random footprint atlas |
| explicit list of nonempty single-patch catalogs | `CHOSE`, category-A | representation repair; must prove semantic identity |
| completed `48` checkpoints | reusable only after validation | banked restart contract; no outcome inspection |
| shell/service exit propagation | `CHOSE`, category-A | use a wrapper with `set -o pipefail` or an equivalent direct exit-preserving launch |

No boundary, scale, source, feature, profile, cosmology, UDT parameter, or acceptance criterion is
added or removed.

## Preregistered gates

1. **Synthetic failure catch:** construct two catalogs on one common patch atlas where one lacks the
   terminal patch. The pre-repair complete-catalog path must reproduce the exact TreeCorr cardinality
   failure.
2. **Synthetic corrected replay:** the explicit single-patch-list path must complete; central integer
   pair counts and weighted sums must equal an unpatched direct TreeCorr calculation in every bin.
3. **Synthetic removal identity:** summing the saved patch-pair results must reproduce the central
   total, and literal deletion of each occupied union block must match direct subcatalog reruns.
4. **Real trigger-cell gate:** `CMASS_South_f1_g00` must complete in isolated scratch using the unchanged
   production selection logic. Its nine central components must meet the frozen R2 comparison gates.
   Only completion, shapes, finiteness, comparison residuals, and structural identities may be read;
   no covariance value, eigenvalue, rank, angular feature, or scale may be inspected.
5. **North regression gate:** the same corrected construction must reproduce one already completed
   North anchor's stored central arrays and removal identities exactly (integer) or at the existing
   frozen floating tolerances.
6. **Checkpoint gate:** all `48` completed guarded checkpoints must pass `read_cell` against the current
   unchanged cell contract before reuse. If the contract or stored semantics change, they are not
   reusable.
7. **Exit gate:** a deliberately failing short command passed through the launch wrapper must produce a
   nonzero service/shell result.
8. **Repository gate:** package checks and `python3 -m pytest tests/` must pass before banking.

## Falsification and stop conditions

Stop rather than resume if the repair changes any central count/weight, changes any registered patch
membership, cannot reproduce exact literal deletion, changes the cell contract, invalidates a stored
checkpoint, or requires a physical/statistical alteration. A South trigger-cell covariance appearance
cannot be used to select or retune the repair.

## Maximum allowed conclusion

If every gate passes:

> `VERIFIED-WITH-CAVEATS`: R3's frozen common HEALPix patch atlas can be represented to TreeCorr by
> explicit single-patch catalog lists without changing the registered estimator, and the validated
> first 48 checkpoints may be reused for a resumed production run.

This correction cannot establish or inspect an R3 covariance outcome, BAO feature, significance,
physical scale, UDT response, CMB relation, cosmology, or `X_max`.
