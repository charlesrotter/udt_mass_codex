# External Adversarial Review of G321

## Scope and procedure

I treated this as a fresh bounded review of the sealed intake only. I authenticated
`REVIEW_MANIFEST.sha256`, `REVIEW_MANIFEST.tsv`, `REVIEW_SCOPE.json`, and all 33 manifest payloads
before relying on the package. The detached seal matched the manifest SHA-256 exactly, and every
listed payload matched both its byte count and SHA-256.

I then copied only `/intake/package` to a writable work directory and ran exactly the four
registered commands from `REPLAY_COMMANDS.txt`:

- `python3 -S derive_local_development.py`
- `python3 -S verify_independent.py`
- `python3 -S run_catch_proofs.py`
- `python3 -S verify_package.py`

All four commands passed. The five regenerated artifacts were byte-identical to the sealed
artifacts in `/intake/package`:

- `DEVELOPMENT_ATLAS.tsv`
- `DERIVATION_RESULT.json`
- `INDEPENDENT_VERIFICATION.json`
- `CATCH_PROOF_RESULT.json`
- `PACKAGE_VERIFICATION_RESULT.json`

## Main findings

### 1. The hostile-mutation evidence is materially overstated because most checks are vacuous or circular.

The package presents `run_catch_proofs.py` as evidence that 12 registered mutations are rejected,
but the implementation does not mutate the actual derivation, replay outputs, or report text in a
substantive way.

- `R1` through `R6` are toy tautology checks on hand-written numbers and tuples, not attacks on the
  package computations or claims (`/intake/package/run_catch_proofs.py:18`, `:23`, `:27`, `:31`,
  `:43`, `:48`).
- `R7` through `R12` are circular: they read `DERIVATION_RESULT.json` and confirm that the file
  already contains the desired booleans or strings, rather than independently probing whether the
  derivation, scripts, or narrative would fail under those mutations
  (`/intake/package/run_catch_proofs.py:54`, `:58`, `:65`, `:71`, `:78`, `:84`, `:90`).

This does not refute the G321 landing, but it does mean the claimed hostile-check support is weaker
than advertised. The repair is straightforward: mutate actual result fields, derivation text, or
implementation paths and assert that the verifier fails for the mutated package.

### 2. The executable theorem-hypothesis audit is weaker than the narrative claim.

The report states that every exposed hypothesis of the imported local theorem passes, but the
executable checks do not fully substantiate that claim.

- In `derive_local_development.py`, several nonnumerical theorem hypotheses are marked as passing by
  unconditional `True` checks rather than by explicit verification
  (`/intake/package/derive_local_development.py:179`-`:182`).
- The same script then records
  `registered_controls_meet_smooth_local_theorem_hypotheses: True` in the result JSON
  (`/intake/package/derive_local_development.py:232`-`:248`).
- The aggregate verifier only checks for the presence of the words `conditional` and `global` in
  three markdown files, which is not a meaningful semantic audit of theorem scope or caveats
  (`/intake/package/verify_package.py:78`-`:81`).

Again, this is repairable rather than fatal, because the mathematical source chain itself does most
of the real work. But the package should not present the current executable layer as a complete
machine-checked audit of theorem applicability.

## Scientific assessment

Despite those support-evidence defects, the bounded scientific landing itself remains intact.

- G303 explicitly derives `S_ab=0 => Ric_ab = Lambda g_ab` with `dLambda=0`, derives the spacelike
  constraints `H=2 Lambda`, `M=0`, and distinguishes the raw rank-nine trace-free symbol from the
  Bianchi-completed fixed-sector rank-ten metric-wave system
  (`/intake/sources/udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/EXACT_DERIVATION.md:36`,
  `:75`, `:117`).
- G315 gives the required spacelike data interface, treats lapse/shift as gauge, writes the ADM
  evolution system with the `-Lambda gamma_ij` term, and keeps local well-posedness explicitly
  imported and conditional
  (`/intake/sources/udt_g315_conditional_cauchy_characteristic_data_interface_2026-09-01/EXACT_DERIVATION.md:36`,
  `:91`, `:111`, `:117`).
- G319 supplies the regular `B != 0` reconstruction and shows that the registered family gives
  smooth lawful constraint data in the bounded slice
  (`/intake/sources/udt_g319_ratio_free_noncmc_constraint_descent_2026-09-01/EXACT_DERIVATION.md:120`,
  `:165`, `:217`).
- G320 supplies the intrinsic invariant `Q_R` and the `n^2` mode separation needed to distinguish
  marked developments without overclaiming an unmarked global quotient
  (`/intake/sources/udt_g320_g319_physical_initial_geometry_quotient_audit_2026-09-01/EXACT_DERIVATION.md:35`,
  `:76`, `:115`, `:122`).
- G321 itself keeps the core uniqueness step conditional on the imported harmonic theorem, treats
  the unit-lapse zero-shift calculation only as an interface check, distinguishes time-reversed sign
  branches, and explicitly leaves unmarked/global classification open
  (`/intake/package/EXACT_DERIVATION.md:121`, `:138`, `:141`, `:162`, `:196`, `:201`).

On that record, I do not find a scientific refutation of the bounded claim:

For each fixed complete G320 datum in the declared smooth marked `T^3` slice, the package
correctly applies the already-imported conditional local well-posedness interface to support one
local marked metric development up to diffeomorphism, while keeping global history, physical
occupancy, and unmarked same-spacetime classification outside scope.

## Verdict

The package should not receive the cleanest acceptance grade because its hostile-mutation and
executable theorem-audit layers overstate how much has been independently stress-tested. But those
defects are repairable and do not presently overturn the bounded mathematical landing.

G321_REPAIRABLE_DEFECTS__BOUNDED_LANDING_RETAINED
