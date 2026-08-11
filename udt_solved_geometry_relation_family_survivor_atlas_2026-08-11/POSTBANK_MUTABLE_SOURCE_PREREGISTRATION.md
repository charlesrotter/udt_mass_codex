# Post-bank mutable-source replay preregistration

Date: 2026-08-11

## Observed issue

The original external-review source manifest correctly froze the pre-result
`CURRENT_SCIENTIFIC_PREMISES.tsv`. Banking G63 then necessarily adds the G63 row to that live
registry. The historical manifest must not be rewritten to follow the mutable navigation file, but
the corrected verifier must also remain replayable from the final repository.

The exact frozen repository source snapshot is commit
`4046b46279e87121e1c84373cafa3068d5b50354`. At that commit the registry SHA-256 is the manifest
value `051e27b985867d9ee5728b6c353a4bd3edbadb9d80841fe0068d6cc21e642f50`.

## Preregistered repair

- preserve `SOURCE_MANIFEST.tsv` and `REVIEWED_INTAKE_SHA256SUMS.tsv` byte-identically;
- add an explicit source-snapshot commit record;
- in a Git repository, resolve all `22` frozen sources from that exact commit rather than from the
  mutable working tree;
- in a sealed intake, resolve all `22` sources from the existing `sources/` transport layout;
- accept exactly one complete layout and reject absent, partial, mixed, wrong-commit, hash-mismatched,
  protected-atlas, or stopped-draft inputs;
- keep the original preregistration verifier as historical pre-result evidence;
- change no solver, sample, threshold, output, classification, or scientific landing.

This correction addresses provenance replay only. It cannot strengthen or weaken the bounded
scientific result.

