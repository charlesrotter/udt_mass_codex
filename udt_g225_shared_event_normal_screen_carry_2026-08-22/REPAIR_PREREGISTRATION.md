# G225 repair preregistration

Date: 2026-08-22

## Trigger

Fresh external review returned `G225_ACCEPT_WITH_REPAIRS`. The bounded scientific theorem passed,
but the aggregate verifier could not find the frozen sources inside the sealed intake because its
repository-relative source resolution did not account for the intake's `frozen_sources/` prefix.

## Frozen repair R1

Make source-root resolution context aware:

- in the repository, resolve `SOURCE_MANIFEST.tsv` rows from the repository root;
- in a sealed intake containing an intake-local `frozen_sources/` directory, resolve those same
  unchanged rows from that directory;
- require containment under the selected source root and preserve exact SHA-256 checks;
- do not change any mathematical script, result payload, count, theorem wording, or premise.

Add this preregistration and the fresh review to the next intake payload. Rebuild a fresh sealed
intake and require `python3 g225_package/verify_package.py` to exit zero from the intake root without
writes.

## Maximum repair conclusion

If the fresh sealed aggregate replay passes, conclude only that the external review's packaging
defect is repaired and the already accepted bounded G225 theorem is mechanically closed. No new
scientific claim or continuation is authorized by this repair.
