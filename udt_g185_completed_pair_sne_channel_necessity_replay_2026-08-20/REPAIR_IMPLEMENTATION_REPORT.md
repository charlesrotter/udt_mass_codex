# G185 sealed-replay repair implementation

## Result

`G185_SEALED_REPLAY_REPAIRED__BOUNDED_SCIENTIFIC_LANDING_UNCHANGED`

No scientific content changed. The repair made the already reviewed intake self-contained and dependency-free.

## Implemented changes

1. `build_review_intake.py` now rewrites only the sealed copy of `SOURCE_MANIFEST.tsv`. Its fourteen paths point to numbered immutable files under the intake's `sources/` directory. The repository provenance manifest and all source hashes remain unchanged.
2. `verify_sealed_intake.js` reproduces both catalog likelihoods and hostile controls using only Node.js standard-library modules.
3. The two original Python replay entrypoints detect sealed layout before importing third-party packages and delegate to the dependency-free replay. Under normal repository layout they retain their original NumPy/SciPy/SymPy implementations.
4. `verify_package.py` distinguishes repository mode from sealed mode, checks intake-relative paths, runs the dependency-free replay plus semantic catches, and reports the still-pending external repair follow-up separately from technical status.

## Sealed results

- Pantheon+: `chi2 = 1260.848088727467`, offset `22.34352850161705`, 1367 rows;
- DES-SN5YR: `chi2 = 1444.186441962819`, offset `41.70895660296941`, 1623 rows;
- all twelve stored numerical/count/control checks: PASS;
- all three hostile controls for each catalog remain more than 100 chi-square units worse;
- all fourteen sealed source hashes: PASS;
- both original entrypoints under `python3 -S`: PASS;
- complete intake before/after hash census: identical.

The small DES difference from the SciPy reference (`2.12e-7` in chi-square) is within the preregistered `3e-6` tolerance and comes from the implementation-distinct standard-library reconstruction.

## Repository regressions

- original production replay: PASS;
- original independent precision replay: PASS;
- thirteen executable catches and eleven semantic guards: PASS;
- current scientific-premise registry: PASS (170 rows; 754 historical dispositions);
- repository tests: 130 passed; 1 expected xfail.

## External closure

Fresh external repair-only gpt-5.4 review returned `G185_REPAIR_ACCEPTED`. It live-ran the sealed
Node replay and both original entrypoints under `python3 -S`, traced file and network syscalls, and
found no forbidden access or intake mutation. The conditional scientific bounds remain unchanged.
