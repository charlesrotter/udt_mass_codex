# G334 sealed-extra repair implementation

Date: 2026-09-03

The preregistered packaging repair changes no scientific formula, output, classification, premise,
or boundary.

- `verify_review_intake.py` now compares the complete regular-file set against the manifest plus
  its two seal files and rejects every unmanifested extra.
- `verify_package.py` invokes all child replays with `python3 -B -S`, preventing local bytecode
  cache creation.
- registered command documentation now uses the same no-bytecode mode.
- `verify_sealed_replay_repair.py` independently tests exact fresh file count, hostile-extra
  rejection, and byte-for-byte immutability across an in-place aggregate replay.

After the first repair-only follow-up, R3 makes the evidence type distinction explicit:

- the repaired **fresh-review product** built by `build_review_intake.py` contains 43 files;
- the separately sealed **repair-follow-up product** built by
  `build_repair_followup_intake.py` contains 46 files because it carries three follow-up-only
  artifacts;
- `verify_sealed_replay_repair.py` now exercises both products independently, including exact
  file-set verification, no-bytecode replay, byte immutability, hostile-extra rejection, and all
  103 retained scientific gates;
- its registered result deliberately records fixed counts and classifications rather than either
  product's manifest digest. This avoids an impossible self-referential requirement in which a
  manifest would need to hash a result that itself contains that manifest's hash.

The accepted scientific landing remains unchanged.
