# G185 sealed-replay packaging repair preregistration

## Trigger

The first fresh external review returned `G185_REPAIR_REQUIRED` after independently confirming the bounded science. The only failed gate was sealed self-replay.

## Frozen scientific surface

The following are immutable during this repair:

- all source bytes and registered source SHA-256 values;
- the completed-pair derivation and its premise stamps;
- the frozen `n = 1.0559332414320268` calibration;
- Pantheon+ and DES row cuts and covariance semantics;
- the production and independent reference results;
- the three hostile controls;
- the preregistered landing and its conditional scope.

No fitting, retuning, new physics, changed transfer law, changed observer query, changed screen rule, or changed tolerance is permitted.

## Authorized implementation repair

1. The intake builder will rewrite only the manifest paths in the sealed copy so each row resolves to its numbered immutable file under `sources/`. Roles and source SHA-256 values remain unchanged.
2. A dependency-free Node.js sealed replay will be added. It will read only those sealed source copies and independently perform:
   - Pantheon+ parsing, release cut, covariance symmetrization, Cholesky profiling, and all four channel models;
   - DES table parsing, packed precision reconstruction, Schur-complement marginalization, profiling, and all four channel models.
3. The sealed package verifier will detect the sealed layout and run that dependency-free replay instead of requiring NumPy, SciPy, or SymPy. Repository-mode verification will retain the existing production, independent-Python, and catch-proof replays.
4. The sealed replay may be implementation-derived from the external reviewer's scratch-only Node recomputation, whose pre-adoption SHA-256 is `0ae691b8390e377fdf03c8ee2ae98f427db74d50c6cca965bf456ab0d0160add`.

## Preregistered gates

The repaired intake passes only if all of the following hold:

1. every manifest path is relative to the intake and remains inside its `sources/` directory;
2. every sealed source hash matches the unchanged registered SHA-256;
3. the sealed verifier succeeds without importing NumPy, SciPy, or SymPy and without repository, `/media`, network, or authentication access;
4. the sealed replay reproduces both stored production results within the already registered independent tolerances;
5. every hostile control remains worse than the full-channel result;
6. a before/after hash census proves the default verifier does not modify the intake;
7. repository-mode production, independent verification, catch proofs, tests, and premise-registry verification still pass;
8. a fresh repair-only external review accepts the repaired packaging while retaining the bounded scientific landing.

## Falsification

Any changed scientific value outside registered tolerance, any source-byte change, any path escape, any undeclared dependency, any intake mutation, or any failed repository regression rejects the repair.

## Maximum conclusion

At most: `G185_SEALED_REPLAY_REPAIRED__BOUNDED_SCIENTIFIC_LANDING_UNCHANGED`, subject to fresh external repair-only acceptance.
