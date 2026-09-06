# Additive read-only replay adapter

This is packaging/reproducibility work only, not scientific repair, another independent review
axis or a change to the frozen mathematical checks. All 41 original review files and their archived
copies remain unchanged. Their frozen checksum validations each exited 0 after this replay.

The original stage_b_independent_artifacts.py hardcodes its original review scratch and repository
paths. The original stage_b_replays.py also writes child evidence into that original scratch.
Those originals are historical execution records; do not directly execute stage_b_replays.py when
a read-only replay is required.

portable_saved_artifact_replay.py takes explicit --review-dir and --candidate-dir arguments,
authenticates the two reused scripts against the review's frozen checksum manifest, and replaces
exactly their two path-binding lines in memory. It neither edits source nor writes evidence.
Python bytecode writing is disabled. The --show-path-diff option displays the precise adaptation
without executing the comparison. The actual inspected PORTABLE_PATH_ONLY.diff changes only the
review directory; the candidate-directory argument for this run equals the historical candidate
location. On a relocated checkout that binding also changes. No check or mathematical expression
is edited or replaced.

The independent comparison then runs the ARCHIVED stage_a_tensor.py and reads AUTHOR_RESULT.json
and WITNESS_INPUTS.json from the supplied candidate directory. It does not need the original
/tmp/udt-curvature-review-qassiP directory. The original scratch was not removed or renamed to
demonstrate absence; lack of that dependency follows from the inspected path replacement and the
actual execution using archived inputs. No filesystem-isolation or sandboxing claim is made.

The one comparison replay ran from /tmp with this exact command:

    timeout 60s /usr/bin/time -v python3 -B /tmp/udt-curvature-portable-zChlAj/portable_saved_artifact_replay.py --review-dir /home/udt-admin/udt_mass_codex/udt_g313_curvature_phase_current_candidate_2026-09-06/review_2026-09-06 --candidate-dir /home/udt-admin/udt_mass_codex/udt_g313_curvature_phase_current_candidate_2026-09-06 > /tmp/udt-curvature-portable-zChlAj/PORTABLE_REPLAY.stdout 2> /tmp/udt-curvature-portable-zChlAj/PORTABLE_REPLAY.stderr

Actual child exit: 0. Start 2026-09-06T19:12:17.953744+00:00; finish
2026-09-06T19:12:23.875113+00:00. /usr/bin/time wall 6.07 seconds; max RSS 52,540 KiB.
Python 3.10.12 / SymPy 1.13.1 as in the frozen review environment. Separate stdout/stderr are
preserved under NEW filenames. JSON comparison with the archived independent-comparison output
passed after excluding only start_utc and finish_utc; all checks, tensor-mutant differences and
saved-witness values are identical.

Portable use after this additive launcher is archived inside the candidate package:

    python3 -B PATH_TO_LAUNCHER/portable_saved_artifact_replay.py --review-dir PATH_TO_CANDIDATE/review_2026-09-06 --candidate-dir PATH_TO_CANDIDATE

That invocation writes its result to stdout only. The caller may capture it to a NEW output path.
Do not redirect over an archived result file. Files in this additive package are enumerated and
hashed by PORTABILITY_SHA256SUMS, excluding the checksum manifest itself. The original Stage A and
Stage B verdict and independence limitations remain unchanged.
