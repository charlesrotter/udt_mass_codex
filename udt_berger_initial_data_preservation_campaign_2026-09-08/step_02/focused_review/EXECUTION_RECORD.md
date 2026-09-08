# Focused review execution record

User instruction overrides normal synchronization/audit startup: first read
FOCUSED_REVIEW_DISPATCH, no Git mutation/sync, no duplicate premise audit, no
agents/fork/resume, write only this directory. No permissions were re-requested.
No broader campaign work or scientific promotion was performed.

The actual tool transcript records initial dispatch/source reads, git status
and HEAD, the three exact registry-row queries after reading the direct parent
audit, source/BI1 inspection, file creation and subsequent exposure. Initial
read-only inspection stdout/stderr were returned in that transcript, not
separately captured as local files. The first explicit UTC observation was
18:48:54 on 2026-09-08, together with local shell/parent process names. No
host-wide process-state claim is made.

Source-first scientific check ran at 18:52:12.242900 UTC, passed unchanged.
First authentication attempt at 18:53:08.589906 failed because git status
returned 128 under the cap. The original script and all its capture files
were copied to authenticate_sources_initial_failure.* before the routine
capture script removed that redundant status invocation. The successful
authentication at 18:53:34.008981 verified HEAD/branch directly, source pins,
the direct parent audit and BI1 evidence. Initial status remained available
in the tool transcript. There was no mathematical candidate/check alteration.

SOURCE_FIRST_SEAL.json was created 18:53:53.322226 UTC. It hashes the argument,
independent code and successful exact output, source hashes, authentication
and wrapper. Only then was EXPOSURE_START.json written and BI2 freeze,
candidate and entire original review opened. No campaign log or whiteboard
content was needed. All original-review calculations were inspected after
that seal. The fresh exposed comparison ran at 18:56:06.121479 UTC, passed.

Scientific/authentication capture launcher commands, each from repository root:

    python3 -B udt_berger_initial_data_preservation_campaign_2026-09-08/step_02/focused_review/run_check.py source_first_check
    python3 -B udt_berger_initial_data_preservation_campaign_2026-09-08/step_02/focused_review/run_check.py authenticate_sources
    python3 -B udt_berger_initial_data_preservation_campaign_2026-09-08/step_02/focused_review/run_check.py exposed_comparison

The authentication launcher was used twice with the preserved script change
described above. Each child receipt contains exact argv, cwd, UTC start,
duration, return code, timeout, limits, thread environment and measured child
RSS. The wrapper saves separate raw streams and uses Python -B to avoid
bytecode writes. Every authored output is in this review directory.

git_status_diagnostic.json later captured the precise failure:
`fatal: unable to create threaded lstat: Resource temporarily unavailable`.
The bounded runtime-only command
`git --no-optional-locks -c core.preloadIndex=false status --short --branch`
succeeded with empty stderr. It changes no Git configuration and disables
optional index locks. This resolves the read-only status-capture issue, not
a scientific defect. The diagnostic command and complete streams are saved.

Two small inspection errors remain in the tool transcript: attempting to
parse the initially empty failed authentication stdout produced JSONDecodeError;
querying the absolute-path EXPOSED_HASHES with a relative key produced KeyError.
The latter query was repeated with resolved absolute paths. Neither ran or
altered a scientific check, source, candidate or seal. They were not silently
counted as passes. No independent mathematical run failed and no source-first
argument or scientific executable was changed after seal.

Final integrity is run with the same wrapper and records source, candidate,
prior-review and source-first payload correspondence. A final SHA256 manifest
records all focused-review artifacts except itself. Those checks show byte
preservation, not science or independence. Parent audit and all reused original
checks remain prior evidence, never independently rerun claims.
