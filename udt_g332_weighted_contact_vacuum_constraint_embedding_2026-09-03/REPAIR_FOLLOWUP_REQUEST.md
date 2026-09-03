# G332 repair-only external follow-up request

## Role

Act as a zero-context repair-only reviewer. Inspect only the corrected sealed intake. Do not edit
evidence files or continue the research.

## Frozen scope

Verify only preregistered repairs R1 and R2 in `REPAIR_PREREGISTRATION.md` and confirm that the
bounded G332 scientific landing is unchanged. The fresh review is already recorded in
`EXTERNAL_REVIEW_RESPONSE.md`.

## Required checks

1. Authenticate the scope, manifest, detached seal, and every manifest payload.
2. In one writable ephemeral copy, run all four commands in `REPLAY_COMMANDS.txt` literally.
3. Confirm `verify_package.py` resolves all 12 source rows within the sealed `sources/` subtree,
   verifies their byte counts and SHA-256 hashes, and does not require repository access.
4. Confirm all three generated JSON artifacts reproduce byte-for-byte.
5. Confirm the derivation consistently distinguishes contravariant `P^ij` and `xi^i xi^j` from
   the covariant unindexed `K` and `xi_flat tensor xi_flat`.
6. Confirm that no equation, coefficient, branch, metric, provenance stamp, or scientific landing
   changed.

## Forbidden expansion

Do not reopen the G331 geometry, choose a weight, classify all extrinsic curvatures, analyze
evolution or stability, select occupancy, or introduce matter, mass, observation, scale,
`X_max`, an action, source, or canon claim.

## Allowed verdicts

```text
REPAIRS_ACCEPTED__G332_BOUNDED_SCIENTIFIC_LANDING_RETAINED
REPAIRS_INCOMPLETE__G332_BOUNDED_SCIENTIFIC_LANDING_RETAINED
REFUTE__G332_WEIGHTED_CONSTRAINT_EMBEDDING
```
