# G304 repair-only follow-up request

Verify only the two repairs preregistered in `REPAIR_PREREGISTRATION.md`:

1. `verify_package.py` must resolve all 14 exact source-manifest hashes in both the live repository
   layout and the sealed `frozen_sources` layout, while rejecting zero or multiple matches.
2. `COMMANDS.md` must distinguish sealed-intake replays from the repository-only premise and diff
   gates, and must no longer imply that an absent file is runnable inside the intake.

Run the dependency-free independent, hostile, and package checks in a writable ephemeral copy.
SymPy is not sealed; do not install it or rerun the production derivation. Confirm that the landing,
65 production assertions, 55 independent assertions, 10 hostile checks, eight domain rows, 14
source hashes, and all scientific scope statements are unchanged.

Return exactly one:

- `REPAIRS_VERIFIED`
- `REPAIRS_INCOMPLETE`

Do not edit evidence files, continue the research, change the scientific question, or inspect
anything outside the sealed intake.
