# Conditional banking integration implementation note

Agent context: /root/conditional_banking_integration. Runtime model is not independently
attested; this is implementation and regression work, not the fresh fidelity review.
Authorized baseline: c92588ad31f3fd79868378e6e3a318af2de1235f, grok.

Only assigned repository files edited:

- CURRENT_SCIENTIFIC_PREMISES.tsv: four added rows G353--G356; existing 335 rows untouched.
- verify_current_scientific_premises.py: 339-row current count, corresponding startup
  frontier/record route, minimal historical replay row-removal updates, and a bounded
  conditional-banking scope/evidence guard. No old package code changed.
- tests/test_startup_surface.py: fixture routing/count maintenance and banking mutation
  tests. No solver, scientific candidate, campaign evidence, manuscript, sidecar, canon,
  protected payload, external disk, deployment or git configuration changed.

All original four candidate arguments and REVIEW_RECORD.md files were read in full,
alongside their precise machine review verdicts. Original pending/UNPROMOTED language
stays frozen; the new owner-authorized BANKING_RECORD.md supplies only the later banking
disposition and incorporates all reviewed limits.

The evidence guard authenticates all 350 original campaign manifest payloads against
its fixed manifest hash, checks reviewed argument correspondence and preserved verdict/
model limits, and authenticates the 32 unique four-step source paths at the exact Git
snapshot. It compares current scientific dependency bytes with those frozen sources,
except the intentionally extended registry. Removing exactly the four new rows must
recover byte-for-byte the historical 335-row registry. Hashes establish correspondence,
not scientific truth, review independence or trusted chronology. No archived helper is
executed. This is not another independent recomputation of the scientific arguments.

Historical replay updates: generic legacy_later_rows adds G353--G356; manual G303,
G304, G305 and G306 frozen-registry filters do likewise; the G351 ephemeral replay
removes G353--G356 along with G352 before its own G351 exclusion. G352's five frozen
source derivations are unaffected and need no special copy. No frozen package file or
old scientific row was weakened to permit the integration.

## Verification so far

Command, constrained to 512 MiB address space and 60 seconds CPU/wall:

    env PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 prlimit --as=536870912 --cpu=60 -- timeout 60s python3 -B -m pytest --noconftest -q tests/test_startup_surface.py -k 'conditional_banking and not next_gate'

Actual result: exit 0, 29 passed, 79 deselected in 0.42s. These include actual
grade/source/active/open/forbidden/independence mutation rejection for all four rows,
an old-row rewrite, changed frozen argument, changed scientific dependency, physical-
adoption wording mutation, and positive full frozen-evidence authentication.

The first same bounded command omitted --noconftest and failed before collection:
tests/conftest.py imported unrelated torch, whose libtorch_cuda.so could not map
under the 512 MiB cap. Exit 4; no test or scientific failure occurred. --noconftest
excludes those unrelated global solver fixtures for these self-contained registry
tests; no fixture file or resource cap changed. Plugin autoload was also disabled.

`git diff --check` passed after these edits. After the parent supplied the maintained
startup documents, the same bounded pytest command was run with the selection:

    -k 'not test_full_foundational_premise_verifier_is_in_pytest'

Actual result: exit 1; 106 passed, 1 failed, 1 deselected in 1.54s. The only failure
was the existing readable-bounds guard: the new CURRENT_RESEARCH_PROGRAM.md table
row had 306 characters against the established 220-character line limit. All source
and scientific-scope regression checks passed. The parent was asked to shorten that
documentation row; no guard was relaxed and no scientific source changed. Exact
combined tool output and command are preserved in STARTUP_TEST_INITIAL_TOOL_RESULT.json;
stdout/stderr were not separately captured by that unified execution interface.

The post-edit full scientific premise audit remains the parent's closure gate; no
duplicate full audit was run by this agent.

After the parent shortened that one table row, the isolated readability regression
passed (exit 0; 1 passed, 107 deselected in 0.14s). The owner-requested final aggregate
then passed with the same full startup-minus-audit selection (exit 0; 107 passed,
1 deselected in 1.47s), under the unchanged 512 MiB/60-second limits. Exact captures
are READABILITY_REPAIR_TOOL_RESULT.json and STARTUP_TEST_FINAL_TOOL_RESULT.json.
The original targeted pass and prior global-conftest collection failure are retained
verbatim from the tool transcript in their explicitly labeled machine records.

Final `git diff --check` passed. Assigned files were frozen before the parent's clean
21:30 UTC post-edit audit began; their hashes are FROZEN_INTEGRATION_FILES_SHA256SUMS.
No subsequent repository edit was made by this agent. Diff size: TSV +4/-0 lines;
verifier +167/-24 lines; tests +106/-5 lines. IMPLEMENTATION_DIFF.patch records the
complete assigned diff from c92588ad. No commits were made by this agent.

## Preserved operational diagnostics and scope limits

The parent startup audit was still running when the first registry-only patch landed
at filesystem mtime 2026-09-06 17:19:58.789978301 -0400 (21:19:58 UTC). The pause
message arrived just afterward. Only the four new rows were present at that point;
the verifier/tests remained untouched. Parent was notified immediately, then explicitly
instructed continuation without rollback and excluded that snapshot-overlapped audit
from all banking gates. Parent later reported it exited 1 at the old 335-row guard.
This is an observed integration timing issue, not adverse scientific evidence. A clean
post-edit audit is required for banking closure.

A scratch-to-repository apply_patch conversion initially retained unified-diff numbered
hunk headers; apply_patch rejected it without changing the target. Normalizing the hunk
headers to its supported format then applied the exact prepared change. No source or
mathematical correction resulted. Scratch files remain in this new /tmp directory.

The fixed-edition account updater rejects the changed live registry hash even when the
manuscript/335-row sidecar remain byte-identical. This is reported to parent as an
intentional current-vs-fixed-edition limitation. Neither updater, manuscript nor sidecar
was edited; parent will verify the unchanged edition against its frozen registry.
