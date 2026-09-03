# G337 repair-only external follow-up request

Act as a zero-context repair-only reviewer. Inspect only the corrected sealed intake. Do not edit
evidence files or continue the research.

Verify only preregistered G337 repair R1:

1. `verify_package.py` resolves authenticated frozen sources in the sealed `sources/` layout without
   repository access or manual root-layout reconstruction;
2. the direct `verify_review_intake.py --replay-package` command authenticates the intake, passes all
   69 aggregate gates, and reproduces the registered aggregate JSON byte-for-byte;
3. production, independent, and hostile outputs remain byte-identical to the fresh-review evidence;
4. no equation, numerical value, premise stamp, or bounded scientific landing changed; and
5. all registered checks run only in a writable ephemeral copy.

Return exactly one verdict:

- `REPAIRS_ACCEPTED__G337_BOUNDED_THIRD_JET_OWNERSHIP_RETAINED`
- `REPAIRS_INCOMPLETE__G337_BOUNDED_THIRD_JET_OWNERSHIP_RETAINED`
- `REFUTE__G337_BOUNDED_THIRD_JET_OWNERSHIP`
