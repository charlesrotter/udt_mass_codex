# G180 repair-only external follow-up request

Inspect only the corrected sealed intake. Do not continue the research.

The first fresh review returned `G180_ACCEPTED_WITH_STATED_BOUNDS` and found only replay-packaging
limitations. Verify exactly these registered repairs:

1. frozen sources now occupy their repository-relative manifest paths at the sealed intake root;
2. `UDT_READ_ONLY_REPLAY=1` standard-library independent replay runs without path repair or writes
   and reproduces 9/9 hashes,
   20,000 trials, 341,579 assertions, 1,461 turning controls, 1,461 pure-angular controls, and 118
   radial controls;
3. `UDT_READ_ONLY_REPLAY=1` catch proof runs without SymPy or writes and retains all 28 catches;
4. `verify_package.py` and `verify_sealed_intake.py` pass in place;
5. the scientific theorem, source set, premise boundary, and maximum conclusion are unchanged.

Return exactly one primary landing:

- `G180_REPAIR_ACCEPTED`;
- `G180_REPAIR_INCOMPLETE`; or
- another precisely defined repair-only result.

Do not derive or propose physics, an action, source, matter theory, `X_max`, cosmology,
radiative-transfer law, observation fit, or signalling law.
