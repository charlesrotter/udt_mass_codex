# G256 repair preregistration

Date: 2026-08-25

Fresh gpt-5.4 grade: `G256_REPAIR_REQUIRED`.

## Retained scientific landing

The reviewer found no mathematical refutation of the graph-rank, angular-tomography,
Hermite-realization, bounded owner, or solver-gate results. The scientific landing is frozen and
must not change during this repair.

## Exact finding

The original sealed intake omitted the repository-wide `verify_current_scientific_premises.py`, but
the package verifier attempted to invoke it at the intake root. Therefore one registered sealed
command failed even though the repository-local premise gate had passed before sealing.

## Preregistered repair

R1 only:

1. Remove the repository-wide verifier subprocess from the **sealed package verifier**. Its role is
   already a repository-local pre-seal gate and it is not one of the 18 scientific sources.
2. Retain exact 18-source hash and ownership checks inside the self-contained sealed verifier.
3. Distinguish the local repository premise gate from the sealed package replay in the run and
   evidence records.
4. Require the corrected sealed verifier, independent replay, and hostile controls all to exit zero.

No equation, rank, angular formula, Hermite construction, owner classification, source universe,
landing, or conclusion scope may change. The follow-up reviewer may verify only R1 and the retained
scientific landing.
