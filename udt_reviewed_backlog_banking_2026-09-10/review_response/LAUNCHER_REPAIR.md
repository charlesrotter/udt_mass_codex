# Supplemental replay-launcher correction

The new administrative adapter initially asserted that REPLAY_PLAN.json occurs
once in the reused runner. It occurs twice: the read and final provenance hash.
This failed before any source replay ran. The failed launch was repeated once
under capture as added_launcher_initial to preserve exact argv/stdout/stderr/
return code/time/limits. Initial adapter bytes remain in run_added_replays.initial.py.

The only change expects two occurrences for that plan filename, one for each
other replacement. Both references now consistently target the supplemental
plan. No scientific source, frozen expectation, assertion, output or original
package changed. This is new-package launcher repair, not a source-theorem repair.
