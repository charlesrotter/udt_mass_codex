# Command provenance clarification

The automatic capture `<stem>.json` is the authority for exact child argv,
working directory, start, duration, exit/timeout and resource limits. Each
capture was invoked from the repository root with prefix

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py

followed by the absolute review output stem, absolute repository cwd, and
the exact child argv saved in that capture JSON. The inspected wrapper sets
512MiB AS/60s CPU and a60s subprocess wall timeout. Its source is snapshotted.

The sealed manual `source_first_block_focused.command.json` and
`source_first_scalar.command.json` normalized the child script to an absolute
path; the actual invocation used the relative path shown in the automatic
JSONs. Both resolve to the same script. These sidecars must not be quoted as
literal argv. Their original bytes remain sealed. This is an evidence-record
precision issue, not a changed calculation or a source repair.

The initial timeout launch returned a PTY/session identifier which was not
retained in the model's displayed result. Its wrapper still completed and
saved the authoritative60.005965651s timeout receipt and separate streams.
A subsequent process-list command saw only its sandbox namespace and is not
used as a host-wide process claim. No complete raw tool/CLI transcript is
claimed. The substantive commands, streams, code and result receipts are local.
