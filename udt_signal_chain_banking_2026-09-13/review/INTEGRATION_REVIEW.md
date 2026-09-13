# Direct banking integration review

**PASS WITH CAVEATS at the inspected implementation and captured attacks.**
No scientific or integration defect was found. The initial REVIEW.md and receipt
remain unchanged and keep their source-fidelity-only scope. The new full406 audit
and final current-navigation receipt are still pending this intermediate record.

The actual signal_chain_banking_guard implements an all-or-none eight-row
projection on its supplied byte string. It rejects partial/duplicate membership,
hashes each present row before removing it, and preserves every other byte.
Its current validator requires all eight, authenticates exact original398 bytes,
header/order, current406 uniqueness, exact row/claim correspondence and dependency
order. Its source gate authenticates the immutable manifest/acceptance records,
all662 current source hashes, per-package counts, named controlling members,
baseline registry bytes and exact baseline Git source membership.

Historical adaptation is centralized through ncb1_banking_guard.without_ncb1:
the new signal-chain authenticator runs before historical row removal. The
central authority helper invokes that adapter on the same raw registry snapshot,
retaining raw bytes for current-row checks; historical later-ID lists then remove
only the eight authenticated additions alongside previously authorized additions.
TI1/TI2 inherit this gate through their existing NCB1 adapter. No second current
registry read is introduced within the tested historical validators/helpers.
The full main verifier makes several separate reads by design; this review does
not assert an atomic whole-program snapshot or absence of concurrent filesystem
changes merely from per-function tests.

An independently written harness intercepts Path.open, covering read_bytes,
read_text and read_tsv, with memory-only poisoned streams. The actual first and
completed-review-pin runs each passed 198 cases: every field of all eight new
rows; individual missing/duplicate rows; all absent, old-row and header changes;
18 current/historical validators/helpers under valid-first/poisoned-second,
poisoned-first/valid-second, partial, duplicate and isolated historical-absence
conditions; 12 source candidate/final-review poisons and five acceptance poisons.
Actual rejections name SIGNAL row/scope, membership, original398, source-evidence
or acceptance-file checks. No sentinel failure is counted as an intended catch.
Current validation rejects historical absence; historical helpers allow complete
absence only at their historical scope. Independent stripping by exact IDs gives
byte-identical original398; all current406 claim rows correspond.

For the catch proof, only the central NCB1-to-signal authenticating projector was
replaced in memory by unchecked row removal. The SAME expected-rejection assertion
then went red in central, TI1, TI2 and NCB1 historical callers because poisoned
scope passed. These are four downstream manifestations of one shared gate, not
four independent authentication implementations or scientific proofs. Real code
and files were never modified by the attacks.

A further semantic membership probe retained 662 distinct entries and package
counts, replaced one source with a pretend same-package file, and temporarily
made the outer manifest digest consistent in memory. The fake file existed only
through patched read/is_file methods. The actual Git-membership check still
rejected it with SIGNAL exact baseline source membership failed. Thus the tested
membership guard is not merely an outer-hash canary. A later master continuation
WORK_ORDER pin was checked separately; its in-memory authority append is rejected.
Both stable initial review files are included in the actual 13-entry pin/fixture
set, and their values match the immutable review receipt.

The direct diff and AST comparison preserve all 14 assertions in each of the
three inherited modular guards and the old TI1/TI2/NCB1 test assertion forms.
Of 3560 central require/assert forms, only two row-count diagnostic strings
change 398 to406. This AST comparison is supplementary structure evidence, not
whole-program equivalence: the actual diff also adds authenticated projection
routes/count/navigation adapters and updates the formerly no-successor navigation
gate to Charles's explicit B/C authorization. Historical scientific assertions,
source hashes, old row values and frozen source work orders remain unchanged.

The new parent pytest implementation was read in full. Its per-field, membership,
source/acceptance and historical-boundary tests exercise real production functions.
Its read_bytes-based snapshot tests are supplemented by this review's broader
Path.open interception, which also covers the historical read_tsv API. No full
premise verifier was launched by this reviewer. Parent initial suite records
775 passed, one failure, one deselection: MEMORY451 words exceeded450. Removing
one redundant word preserves the test threshold and original failure; the next
captured suite reports778 passed, one deselected. Its omitted wrapper would repeat
the separately scheduled full verifier. Later master-authority pin and success-
message-only updates are explicitly later than that suite; final checks must own
the actual final bytes.

Navigation diffs were read: source statements remain conditional, current406 is
identified as integrated with completion gates pending, TI3/OB2 retain holds and
StageB/C are already authorized but not promoted. The master continuation work
order is read and pinned for authorization; this banking reviewer does not review
new StageB/C science. Backup/protected payload completeness stays UNVERIFIED.

All reviewer quantitative checks were serialized CPU/one-thread captures under
180seconds/2048MiB. The initial/review-pinned integration runs took0.545543/
0.543744seconds with66552/66180KiB maximum RSS; membership probe0.069251seconds,
28608KiB. Code, streams, exact commands, versions and resource records are saved.
The gate tests are distinct input implementations executing shared guard code;
source science was not re-proved or rerun. Final audit/source/navigation fidelity
will be recorded separately within the original reviewer allocation.
