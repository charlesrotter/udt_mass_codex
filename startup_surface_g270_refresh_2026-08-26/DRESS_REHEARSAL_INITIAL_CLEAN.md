# Initial clean-clone startup rehearsal

Date: 2026-08-26
Mode: zero-context internal agent
Workspace: isolated clone under `/tmp`
Edits or research: none

## Correct orientation recovered

The rehearsal followed `AGENTS.md`, identified G268--G270 as the current closed arc, preserved the
exact qualified grades, kept `M=sech(delta)` provisional, distinguished the intrinsic completed-pair
metric from the ambient transported-screen mismatch `W`, respected protected-work boundaries, and
stopped at the MAP/PONDER gate before any automatic G271 solve.

## Defect found

`python3 verify_current_scientific_premises.py` failed in the clean clone with:

```text
G243 evidence missing: RADIAL_REPRESENTATION.npz
```

The artifact existed in the primary worktree with SHA-256
`68deaa48bb68493febb1c9d34de426a215675f917b971b1aca59f833d468600b`, but the repository-wide
`*.npz` rule ignored it and `git ls-files` confirmed that it was untracked. The local startup pass
was therefore not clone-self-contained.

## Wording cautions found

- G269 owns an independent metric evaluator, not an independently validated measurement protocol.
- R2--R5 are not wholly unresolved: they are observed/verified with caveats, while 184,300
  covariance rows and scale selection remain unresolved.
- G257 must remain an imported bounded GR comparison under `WORKING/POSIT`, not an unqualified
  native UDT parent-law derivation.

Landing: `ORIENTATION_CORRECT__FRESH_CLONE_EVIDENCE_FAILURE_FOUND`
