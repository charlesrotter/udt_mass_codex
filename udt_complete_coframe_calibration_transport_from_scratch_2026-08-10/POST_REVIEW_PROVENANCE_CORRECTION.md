# Post-review provenance correction

Date: 2026-08-10
Scope: verifier provenance only; no mathematical formula, witness, status, or conclusion changed

The sealed external review correctly replayed the 15 source hashes against the then-current
working tree. After that review, current startup navigation and `CURRENT_SCIENTIFIC_PREMISES.tsv`
were advanced to register G57. That legitimately changes one manifest-named current file but must
not cause the exact preregistered/reviewed intake manifest to be rewritten.

Therefore `verify_calibration_transport_independent.py` now replays all 15 manifest hashes from
the preregistration commit `8425e2a2`, using `git show`, rather than comparing the historical
manifest to mutable post-result navigation. Its exact rational algebra is unchanged. This is a
fail-closed preservation correction: a changed preregistered source still fails, while a lawful
later navigation update no longer falsifies the historical intake.
