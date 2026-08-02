# Replay-determinism correction

Date: 2026-08-01

The evidence package was first committed at `0f0069d`. A subsequent full repository-gate replay
passed every scientific and repository assertion but changed only pytest's reported elapsed wall
time in `REPOSITORY_TEST_STDOUT.txt` (`1.48s` to `1.46s`). Because that capture is package-hashed,
the scientifically irrelevant timing variation made `verify_package.py` fail its identity check.

This correction changes no derivation, witness, classification, premise, test outcome, or maximum
conclusion. `verify_repository_gates.py` now checks the raw pytest result and exact
`70 passed, 1 xfailed` outcome first, then normalizes only the terminal elapsed-time token to
`<elapsed>s` before saving the hashed capture. The package manifest is rebuilt after this
correction, and two consecutive gate/manifest/package replays must return the same manifest hash.
