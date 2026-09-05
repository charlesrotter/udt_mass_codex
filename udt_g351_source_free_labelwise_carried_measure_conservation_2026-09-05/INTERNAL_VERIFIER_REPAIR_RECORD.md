# G351 internal aggregate-verifier repair record

Date: 2026-09-05

The first aggregate replay returned 23/26. Its only failures were the three exact-phrase checks
frozen in `INTERNAL_VERIFIER_REPAIR_PREREGISTRATION.md`. Production, independent arithmetic,
hostile catches, frozen hashes, no-write replay, exact landing, and the other 23 aggregate checks
all passed.

After changing only those three phrase matchers, the registered no-write aggregate replay returned
26/26. Saving the aggregate landing added one self-consistency assertion, after which the final
pre-R1 aggregate replay returned 27/27. Production remained 56,316/56,316, independent verification
remained 11,115/11,115, and hostile catches remained 10/10. The replay changed no package bytes and
emitted no bytecode.

No scientific statement, premise, calculation result, frozen input, or exact landing changed in
this mechanical repair. The later scientific R1 narrowing is recorded separately.
