# BI1 review execution and evidence map

All paths below are relative to repository cwd
/home/udt-admin/udt_mass_codex unless explicitly absolute. Hand-authored files
were created with apply_patch. The existing capture runner was read before
execution and used directly, without copying or changing it. An absolute name
argument makes its outputs land only in the authorized review directory.

Every capture used this exact launcher prefix:

    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py

The next arguments were, in order, the absolute capture stem, the exact cwd
above, and the child command array stored verbatim in the corresponding JSON.
Thus each full command is reconstructible without relying on shell interpolation.
The absolute capture stem for NAME is
/home/udt-admin/udt_mass_codex/udt_berger_initial_data_preservation_campaign_2026-09-08/step_01/review/NAME.
For these actual invocations NAME and child command were:

| NAME | Child command |
|---|---|
| source_first_run | python3 udt_berger_initial_data_preservation_campaign_2026-09-08/step_01/review/source_first_check.py |
| source_first_hashes | sha256sum followed by the exact 24 paths in source_first_hashes.json |
| intake_authentication | python3 udt_berger_initial_data_preservation_campaign_2026-09-08/step_01/review/authenticate_intake.py |
| candidate_comparison | python3 udt_berger_initial_data_preservation_campaign_2026-09-08/step_01/review/compare_candidate.py |
| author_regression | python3 -B udt_berger_initial_data_preservation_campaign_2026-09-08/step_01/check_bi1.py |
| mutation_probe_run | python3 udt_berger_initial_data_preservation_campaign_2026-09-08/step_01/review/mutation_probe.py |
| final_integrity | python3 udt_berger_initial_data_preservation_campaign_2026-09-08/step_01/review/final_integrity.py |

Each stem owns .stdout, .stderr and .json. The runner refuses overwrites and
limits its child to 512 MiB address-space and 60 seconds CPU/wall time. No new
scientific approximation or tolerances entered; all calculations were exact.

Chronology from saved receipts and tool transcript:

* 18:02 UTC: review dispatch read as the first command; review orientation,
  permitted source/method reads and read-only branch/hash/status inspection.
* 18:05:58 UTC: independent source-first symbolic check began.
* 18:08:56 UTC: 24-file source/argument/code/result hashes captured.
* After that capture: SOURCE_FIRST_SEAL.md written and SHA256 announced;
  no scientific conclusions sent before freeze. CANDIDATE_FREEZE.md was then
  found and opened, followed by the declared candidate/code/results/receipts.
* 18:12:06 UTC: candidate, source and parent receipt authentication captured.
* 18:13:41 UTC: saved author tensors and 18 fixtures independently compared.
* 18:14:13 UTC: original author same-code regression captured, identical stdout.
* 18:16:04 UTC: eight exact in-memory mutation probes captured, including every
  incorrect program and stream. Six rejected by author checks; two surviving
  incorrect S variants detected by the independent sealed curvature tensor.

The parent full audit was not replayed. Its receipt/streams/command were read
and hashed in intake_authentication. Source-first checks did not read the wide
registry: it was hashed only. Exact load-bearing rows were queried only after
parent audit authentication; current status strings, source paths and controls
are retained in the intake output. The old G337 derivation header is not used
to demote its current registry grade.

Initial source reads, simple file discovery, clock reads, hashes of the seal,
report-data inspection and the first author-script diff are preserved in the
tool transcript; they did not receive separate runner capture files. The
initial broad filename listing was truncated and is disclosed in REVIEW_SCOPE;
no protected payload, author code/results or whiteboard was read before seal.
All scientific checks have exact captured command arrays and raw streams.

No shared Git mutation, checkout, fetch, pull, new agent, fork/resume, model
switch, archive/GPU work, old-carrier replay or physical/canonical promotion
was performed. No post-review candidate repair was used. Original artifacts,
the pre-freeze author failure and the review's deliberate mutant failures
remain preserved, with their different evidentiary roles identified.
