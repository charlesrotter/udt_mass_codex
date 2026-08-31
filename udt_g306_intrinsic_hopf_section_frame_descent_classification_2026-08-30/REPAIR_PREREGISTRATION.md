# G306 external-review repair preregistration

Date: 2026-08-30
Status: `PREREGISTERED_BEFORE_REPAIRS`
Trigger: fresh external review verdict `REPAIRABLE_DEFECTS`

## Frozen repair scope

R1. Separate repository-only gates from the self-contained sealed replay. `COMMANDS.md` must state
which commands require the repository environment and which commands are required inside a sealed
intake. The fresh follow-up intake must contain every file used by every sealed command. It must not
claim that the repository-wide premise verifier or full pytest suite can be rerun from the bounded
intake. Their already recorded counts remain repository regression evidence only and will be rerun
in the repository before the follow-up intake is built.

R2. Make `verify_package.py` resolve every `SOURCE_MANIFEST.tsv` row in exactly one of two allowed
layouts: repository root or sealed `frozen_sources/`. It must reject missing and ambiguous matches,
and it must verify the same 15 registered source hashes in both layouts.

R3. Remove the unsealed SymPy dependency from the production derivation. Replace it with an exact,
standard-library-only implementation of the same preregistered algebra and geometry. The repaired
production replay must retain the exact landing, 172 production assertions, candidate census, and
all registered output fields. The independent verifier must remain implementation-distinct and
must not import production code.

R4. Rerun production, independent, hostile, package, premise-registry, and full repository gates;
build a fresh repair-only sealed intake; and prove that all sealed commands run from a writable
ephemeral copy using `python3 -S` and only sealed dependencies.

## Frozen scientific landing

These are evidence-portability repairs only. They may not alter the bounded scientific result:

`ROUND_S3_METRIC_INTRINSICALLY_DEFINES_TWO_ORIENTED_HOPF_CONGRUENCE_FAMILIES__ISOTROPY_SELECTS_NO_PHYSICAL_MEMBER__SUPPLIED_GEOMETRIC_MEMBER_HAS_FRAME_INDEPENDENT_SCALE_BLIND_NORMALIZED_HELICITY__RAW_COMPONENT_HOPF_NUMBER_FAILS_FULL_LOCAL_FRAME_DESCENT__FIELD_QUERY_POPULATION_TARGET_ACTION_DYNAMICS_HISTORY_MAGNITUDE_MASS_AND_XMAX_REMAIN_OPEN`

No repair may select a field/query population, individual Hopf member, fixed physical target,
orientation, dynamics, action, history, magnitude, mass, scale, or physical `X_max`; modify the
metric or reciprocal kernel; or export the theorem outside the positive G305 standard round `S3`
completion.

## Acceptance contract

1. The self-contained sealed command list contains no unavailable repository asset or dependency.
2. The package verifier passes unchanged in the repository layout and in a copied sealed layout,
   while rejecting missing and ambiguous source resolutions.
3. The repaired production script runs under `python3 -S`, reports exactly 172 assertions, and
   reproduces the frozen landing and output fields without SymPy or another external dependency.
4. The independent standard-library replay remains separate, retains 22,237 checks, and reproduces
   both chiralities and the normalized Hopf result within its registered tolerance.
5. All 17 hostile direct mutations remain caught; the premise registry and full repository suite
   pass with the previously registered single expected xfail.
6. A fresh external repair-only reviewer verifies R1--R4 and confirms that the scientific landing
   did not change.
