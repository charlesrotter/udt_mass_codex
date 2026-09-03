# G337 R1 repair implementation

Date: 2026-09-03
Preregistered at commit: `0b8cfc45`

The fresh reviewer retained every bounded mathematical claim and found one replay-packaging defect.
The repair changes no equation or registered scientific output.

Implemented changes:

1. `verify_package.py` now authenticates frozen sources from either the normal repository-root
   layout or the sealed `sources/` layout before considering the historical Git fallback.
2. Both layouts enforce path containment, byte count, and SHA-256 identity.
3. `verify_review_intake.py --replay-package` now runs the aggregate verifier directly against the
   authenticated sealed layout, writes only to a temporary directory, and demands byte identity
   with the registered aggregate JSON.
4. The repair-follow-up builder runs that sealed-layout replay before reporting success.

The production, independent, and hostile outputs remain byte-identical to the fresh-review intake.
The bounded scientific landing and every premise stamp remain unchanged.
