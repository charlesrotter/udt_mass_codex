# G308 external-review repair preregistration

Date: 2026-08-31
Parent evidence commit: `56e0d75e`
External verdict: `G308_REPAIRABLE_DEFECTS`

No repair may change the bounded G308 scientific question or landing. A repair that changes the
metric, reciprocal kernel, member census, physical-population boundary, or global chirality result
is a scientific regression and must stop closure.

## R1 — sealed-source path portability

Repair `verify_package.py` so every source-manifest path is resolved uniquely from exactly one of:

1. the repository sibling layout `ROOT / relative`; or
2. the sealed layout `ROOT / frozen_sources / relative`.

Missing and ambiguous layouts must both fail. The verifier must pass unchanged in the repository
and in a freshly rebuilt sealed intake without symlinks or manual staging.

## R2 — method-distinct chirality verification

Add an independent verifier that does not import production code and does not reconstruct the
candidates with the production outer-product ansatz. It must instead use:

- fixed canonical opposite-chirality complex blocks;
- random `SO(4)` conjugation built from Givens rotations;
- the four-dimensional Hodge-star split to classify chirality;
- group-orbit flow `q(s)=cos(s)q+sin(s)Jq` for global closed fibers;
- an orthogonal parity conjugation and the warped-product connection identities.

It must verify both global members, `O(4)` exchange, `SO(4)` nonexchange, pair-reversal chirality
preservation, connected-stratum separation, causal equivalence, normalized time carry, and the
slice-geodesic/four-dimensional-geodesic distinction. Any contradiction reopens the scientific
landing.

## R3 — evidence-language regrade

Regrade the existing randomized verifier as a non-importing constructive cross-check, not a fully
independent derivation. Count the new Hodge/group-orbit implementation as the method-distinct
independent gate. Preserve both results and report both check counts separately.

## R4 — repair portability and hostile gates

Add a standard-library portability verifier covering repository-only, sealed-only, missing, and
ambiguous source layouts. Extend package verification and the review intake to include all repair
evidence. Rebuild the intake and replay every registered command in a fresh writable copy.

## Acceptance contract

Repairs pass only if:

1. production outputs and the exact G308 landing are unchanged;
2. repository and sealed package verification both pass without layout shims;
3. missing and ambiguous source layouts are rejected;
4. the Hodge/group-orbit verifier passes independently of production code and the outer-product
   candidate construction;
5. all existing exact, randomized, hostile, premise, and repository regression gates still pass;
6. a repair-only external reviewer accepts R1--R4 without a scientific regression.

Until item 6, the package remains `EXTERNAL_REVIEW_REPAIR_PENDING`.
