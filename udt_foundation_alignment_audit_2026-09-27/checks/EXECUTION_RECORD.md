# Check execution and limits

Parent baseline: `9858453171994858d85ff4c365382d67ca0c7d0c`.
This is an execution receipt written from observed tool results, not synthetic
stdout or an independently signed chronology.

## Startup, before the packet

The parent performed the ordered AGENTS startup and synchronization in this same
top-level session. Branch `grok`; HEAD and origin/grok matched the baseline;
fetch/pull succeeded with no update. The actual command
`python3 verify_current_scientific_premises.py` completed with exit 0 and PASS
for the 406-row registry, taking approximately 6 minutes 45 seconds. Its output
was returned in the session tool transcript, not captured into this later-created
packet. Do not present this receipt as a retained raw verifier log.

The preliminary parent SymPy check used `timeout 60s python3 -B` with an inline
script: Python 3.10.12, SymPy 1.13.1, eight identities, exit 0. That exploratory
script/output is in the session transcript only. The separate reviewer's retained
implementation/output supplies the inspectable new algebra checks for this packet.

## Packet construction and checks

1. `python3 udt_foundation_alignment_audit_2026-09-27/build_coverage.py`
   exited 0. It reported 406 current rows, 397 inherited rows, additions G415–G423,
   no removed ID or change in the four comparable fields, and 23 families.
   `candidate/COVERAGE_SUMMARY.json` retains the machine-readable result.
2. `python3 udt_foundation_alignment_audit_2026-09-27/check_packet.py > udt_foundation_alignment_audit_2026-09-27/checks/PACKET_CHECK_INITIAL.json 2> udt_foundation_alignment_audit_2026-09-27/checks/PACKET_CHECK_INITIAL.stderr`
   exited 0; stdout and empty stderr are retained. This validates correspondence
   of all nine current fields, exact family accounting, six rejected hostile
   variants, 48 source pins, and the 52 outside status entries.
3. `git apply --check udt_foundation_alignment_audit_2026-09-27/candidate/MAINTAINED_DOCS.patch`
   exited 0 with no output. This verifies applicability, not scientific correctness
   or a complete startup rehearsal. No patch was applied.
4. The reviewer's exact command, runtime, output and exclusions are recorded in
   `review/math/SOURCE_FIRST.md`, `INDEPENDENT_CHECK.json` and the saved script.

## Deliberate omissions

The full premise verifier is not repeated simply to create another pass count:
the exact registry and scientific inputs remain unchanged and this packet adds
no active claim or verifier integration. Any later live documentation integration
must run the checks its actual changes require. This session's same-source
startup PASS is not a future integration PASS.

No old numerical campaign is rerun, no raw registry-wide proof census is claimed,
no protected payload is read or hashed, and no unrelated untracked content identity
is asserted. The preservation check verifies outside paths/status and authorized
source bytes. No physical relocation or restoration rehearsal is performed here.
