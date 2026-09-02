# External Repair-Only Review of Sealed G321

## Scope and authentication

I treated this as a read-only repair-only follow-up review bounded by `/intake/REVIEW_SCOPE.json`.
I inspected only `/intake`, authenticated `REVIEW_MANIFEST.sha256`, `REVIEW_MANIFEST.tsv`,
`REVIEW_SCOPE.json`, and every manifest payload before relying on any evidence, then copied only
`/intake/package` to `/work/package` for replay.

Authentication results:

- detached manifest seal matched `REVIEW_MANIFEST.tsv` exactly:
  `6b09326c49976134e968c50fdcf634f985e9c0e4751aebb15dedce5e81e35d1a`;
- `REVIEW_MANIFEST.tsv` enumerated 39 authenticated payloads under `/intake`;
- every listed payload matched both recorded byte count and recorded SHA-256;
- no authentication failure occurred.

## Registered replay

In `/work/package` I ran exactly the four registered commands from
`/intake/package/REPLAY_COMMANDS.txt`:

1. `python3 -S derive_local_development.py`
2. `python3 -S verify_independent.py`
3. `python3 -S run_catch_proofs.py`
4. `python3 -S verify_package.py`

All four commands exited successfully.

The replay regenerated the five expected writable artifacts, and each matched the sealed intake
artifact byte-for-byte:

- `DEVELOPMENT_ATLAS.tsv`
- `DERIVATION_RESULT.json`
- `INDEPENDENT_VERIFICATION.json`
- `CATCH_PROOF_RESULT.json`
- `PACKAGE_VERIFICATION_RESULT.json`

I also compared the entire copied `/work/package` tree against `/intake/package` after replay.
The file set matched exactly and there were no content differences in any of the 30 package files.

## R1 assessment: hostile-mutation evidence

R1 is repaired.

Why:

- `run_catch_proofs.py` now copies the actual package into a fresh writable temporary directory for
  each hostile check (`/intake/package/run_catch_proofs.py:46-52`).
- It separately proves that an unmutated package copy passes the same aggregate verifier route
  before any attack is attempted (`/intake/package/run_catch_proofs.py:69-76`).
- All 12 preregistered attacks mutate real package artifacts, specifically
  `DEVELOPMENT_ATLAS.tsv` or `DERIVATION_RESULT.json`, rather than toy local variables
  (`/intake/package/run_catch_proofs.py:18-33`, `:79-138`).
- Each attack requires both nonzero verifier exit and the exact expected rejection substring
  (`/intake/package/run_catch_proofs.py:52-59`).
- The emitted hostile-catch result records baseline pass, 12/12 catches, and the expected rejection
  reason for every mutation (`/intake/package/CATCH_PROOF_RESULT.json`).
- The mutations are confined to temporary directories, while the only persistent write from the
  script is the result JSON in the package root (`/intake/package/run_catch_proofs.py:151-153`).
  The full-tree `/work/package` versus `/intake/package` comparison after replay showed no
  persistent evidence drift, which is consistent with the claim that evidence files are left
  unchanged outside the ephemeral attack copies.

## R2 assessment: theorem-hypothesis and report-scope evidence

R2 is repaired.

Why:

- The prior unconditional theorem-hypothesis `True` placeholders are gone from
  `derive_local_development.py`. The script now defines an explicit eight-entry
  `THEOREM_HYPOTHESIS_AUDIT` with typed `status` and nonempty `evidence` text for `H1` through
  `H8` (`/intake/package/derive_local_development.py:27-60`).
- The production result preserves that typed audit in `DERIVATION_RESULT.json`
  (`/intake/package/derive_local_development.py:266-286`,
  `/intake/package/DERIVATION_RESULT.json`).
- The script explicitly separates executable analytic/algebraic checks from the imported smooth
  harmonic PDE theorem: the principal-rank, regularity, constraint, sector, mode-separation, and
  time-reversal items remain executable, while the theorem-application boundary is stated as
  imported and not machine-proved (`/intake/package/derive_local_development.py:206-216`;
  `/intake/package/EXACT_DERIVATION.md:130-155`).
- The aggregate verifier now checks exact structured facts rather than word presence alone. It
  verifies the exact landing string, exact conditional-theorem interface status, exact hypothesis
  statuses, nonempty evidence text, exact report ownership/scope/landing stamps, and exact
  status-ledger states for wellposedness, unmarked relation, occupancy, and global history
  (`/intake/package/verify_package.py:64-75`, `:118-129`).
- The narrative texts do not claim that G321 machine-proves the imported theorem. The derivation,
  audit report, and lay report each preserve the conditional imported-theorem boundary and deny any
  machine-proof overclaim (`/intake/package/EXACT_DERIVATION.md:146-155`,
  `/intake/package/AUDIT_REPORT.md:28-32`, `/intake/package/LAY_REPORT.md:28-37`).
- The status ledger remains aligned with that bounded ownership model: standard local wellposedness
  is marked `IMPORTED_MATHEMATICAL_METHOD__CONDITIONAL`, while unmarked same-spacetime relation,
  physical occupancy, and global history remain open or unselected
  (`/intake/package/STATUS_LEDGER.tsv:7-13`).

## Bounded scientific landing

The bounded scientific landing is unchanged.

The replayed production result, the aggregate verifier, and the three narrative reports all retain
the same exact landing:

`G320_DATA_HAVE_CONDITIONAL_UNIQUE_LOCAL_MARKED_DEVELOPMENTS__REGISTERED_BREADTH_IS_ORDINARY_CAUCHY_DATA_FREEDOM_IN_BOUNDED_ARENA__NO_GLOBAL_OR_OCCUPANCY_SELECTION`

Within the repair-only scope, I found no change that broadens the scientific question, upgrades the
claim to global history or physical occupancy, removes the conditional imported-theorem caveat, or
otherwise refutes the bounded local marked-development conclusion.

## Verdict

G321_REPAIRS_ACCEPTED__CONDITIONAL_LOCAL_MARKED_UNIQUENESS_UPHELD
