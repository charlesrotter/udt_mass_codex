# G264 sealed-replay packaging repair result

## Result

`EXTERNAL_ACCEPT_PACKAGING_REPAIR__PRODUCTION_SYMPY_REPLAY_NOT_RERUN_EXTERNALLY`

The sole defect reported by the first repair-only follow-up was repaired without changing the G264
science. The corrected seal now supplies a self-contained `replay_root/` containing the repaired
package, its `SOURCE_MANIFEST.tsv`, and all seven exact frozen sources at their registered
repository-relative paths.

In a fresh writable copy of the exact corrected layout, all registered commands passed:

- production derivation: 27 exact symbolic checks;
- metric-first verifier: 250 cases, 1,000 exact assertions;
- consistency replay: 12,000 exact and 6,025 numeric assertions;
- original catch proof: 18/18;
- repair catch proof: 10/10;
- package verifier: `PASS`, seven sources resolved as `live_exact` inside the seal;
- packaging catch proof: 3/3.

The packaging catch proof separately removed `SOURCE_MANIFEST.tsv`, altered one frozen source, and
removed one frozen source. The package verifier failed closed in all three altered copies.

The external reviewer accepted the packaging repair after independently verifying seal integrity,
the self-contained seven-source replay without Git, R1--R3 continuity, the unchanged landing, and
all three packaging attacks. Its isolated runtime lacked SymPy, so it did not rerun the production
symbolic script; this is retained as an explicit environment qualification. The same sealed script
had already passed 27 exact checks locally, while the external dependency-free metric-first
derivation reran successfully.

The landing, counterfamily, alpha-two thresholds, G201 conditional intersection, and all ownership
ceilings remain unchanged.
