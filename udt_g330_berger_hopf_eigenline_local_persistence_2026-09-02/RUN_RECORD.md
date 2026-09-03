# G330 run record

Date: 2026-09-02
Preregistration: `add519ae`
Device: CPU
Arithmetic: exact Python `Fraction` and exact Laurent-polynomial algebra

## Commands

```bash
python3 -S derive_berger_hopf.py --output DERIVATION_RESULT.json
python3 -S verify_berger_hopf_independent.py --output INDEPENDENT_VERIFICATION.json
python3 -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json
```

## Results

- production: 39/39 exact assertions;
- independent: 40/40 exact assertions, no production import or result read;
- hostile: 8/8 direct mutations rejected.
- aggregate: 145/145 package, source, provenance, and byte-exact replay gates.

The first hostile run exposed one incorrect mutation anchor in the catch harness. The anchor was
repaired before any verdict was banked; no scientific formula or expected result changed.

Fresh external review retained the bounded scientific landing and requested three repairs. Those
repairs were preregistered at `4d9b1cd8`; local corrected replay and repair-only external follow-up
are required before final banking.

## Corrected sealed replay

The corrected 47-file intake authenticated 45 manifest payloads. From one fresh writable copy, all
four registered commands passed:

- production: 39/39;
- independent: 40/40;
- hostile: 8/8 caught;
- aggregate: 169/169.

The four generated JSON artifacts were byte-identical to the package outputs. Repair-only external
follow-up accepted R1 and R2 and retained the landing. R3 required only explicit
`isometry-extension consequence` language in three summary records; completion was preregistered at
`c739be6c`.

The R3-completed 50-file intake authenticated 48 manifest payloads. All four commands then passed
from one fresh writable copy: 39/39 production, 40/40 independent, 8/8 hostile catches, and 178/178
aggregate gates. Final R3-completion-only external review authenticated that intake, repeated all
four commands, accepted R3, found no scientific regression, and retained the bounded landing.
The closed package then passed 181/181 aggregate gates, including the returned acceptance and its
exact transmission record.

During final banking, adding G330 to the live premise registry and startup guide correctly changed
two current-source hashes. The replay/intake resolver was therefore completed so sealed intakes
continue to use their immutable `sources/` tree and live-repository replays or intake rebuilds use
exact `add519ae` blobs for reviewed sources that have since advanced. The reviewed manifest was not
rewritten.
