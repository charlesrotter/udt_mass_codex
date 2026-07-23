# Second post-commit adversarial audit preregistration

Date: 2026-07-23

Audited tip: `ec2498cf4abba68eafdd74538f3f526f98899e7d`

Mode: reproducibility and source-lineage correction only

## Findings registered before correction

### R1 — manifested rehearsal output is volatile

In a fresh local clone at the audited tip:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -s rehearse_startup_zero_state.py
```

passes all 16 checks but changes:

- `ZERO_STATE_REHEARSAL_RESULT.json`;
- `ZERO_CONTEXT_REHEARSAL_OUTPUT.md`.

The only causes are embedded volatile Git metadata: the current `HEAD` and
pre-run worktree status. Replaying the documented command then makes
`sha256sum --check MANIFEST.sha256` fail on exactly those two files.

### R2 — strongest absolute-scale source omitted from lineage

`C15` is correctly `OPEN`, but its cited source is the matter coefficient
inventory. The load-bearing global result is stronger and more direct:

```text
scale_breaking_closure_census_2026-07-20/STATUS_LEDGER.tsv
```

In particular, `S04` proves that measured `c_E` and `G_obs` supply mass per
length but no absolute length, `S14` finds no noncircular scale breaker in the
audited foundation, `S15` leaves physical `Xmax` and unconditional mass open,
and `S16` gives the scoped dimensional theorem. This source was not included
in the checkpoint's 25-path source lineage.

## Authorized correction

- Preserve every prior preregistration, status correction, evidence package,
  and historical source table unchanged.
- Add an append-only source-universe addition naming the scale-breaking status
  ledger.
- Change only the `C15` evidence pointer and its exact source bindings.
- Regenerate source lineage with 26 paths and update verification counts.
- Remove volatile `HEAD` and worktree-status fields from manifested rehearsal
  outputs. Replace them with stable statements that volatile Git metadata is
  deliberately checked by repository gates rather than embedded in the
  rehearsal artifact.
- Add a stable check that `AGENTS.md` requires branch `grok`.
- Require the documented rehearsal command, run from a fresh clean clone, to
  leave the clone clean and preserve the package manifest.
- Update only this checkpoint's scripts, method/command/audit documentation,
  generated outputs, manifest, and repository gate as necessary.

## Prohibited work

- No scientific status, scope, open seam, equation, derivation, numerical
  result, research artifact, frozen package, registry, `LIVE.md`, `HANDOFF.md`,
  `INDEX.md`, `README.md`, `AGENTS.md`, `MEMORY.md`, `CANON.md`, script outside
  this checkpoint, data, artifact path, or repository organization may change.
- No solve, GPU work, canonization, action/carrier adoption, or follow-on
  scientific derivation.

## Verification contract

1. The source universe must contain 26 unique identities and paths: the
   historical 25 plus exactly one append-only scale-breaking ledger.
2. `C15` remains `OPEN`; its evidence path must be the scale-breaking status
   ledger.
3. Exact bindings must verify `S04=REFUTED_BY_DIMENSION_AND_RANK`,
   `S14=NOT_FOUND_IN_AUDITED_CURRENT_FOUNDATION`, and `S15=OPEN`.
4. No manifested rehearsal output may contain `head`,
   `worktree_status`, or a commit-specific hash.
5. The rehearsal must pass 17 checks, including the stable `grok` instruction.
6. A fresh-clone rehearsal replay must leave zero dirty paths and preserve
   every package-manifest hash.
7. Existing 15 independent checks and 20 catches must be retained or
   strengthened; add catches for a missing source addition, loss of the scale
   binding, and reintroduction of volatile rehearsal metadata.
8. All prior scientific packages, six frozen manifests, current paths, links,
   frontier targets, tests, and original dirty-checkout metadata gates must
   pass unchanged.

## Maximum conclusion

`SECOND_PASS_REPRODUCIBILITY_AND_SOURCE_LINEAGE_CORRECTION_VERIFIED_WITH_NO_NEW_PHYSICS`
