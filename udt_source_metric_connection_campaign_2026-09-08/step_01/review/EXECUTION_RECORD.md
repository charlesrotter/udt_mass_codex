# SM1 reviewer execution record

Working directory for both commands:
/home/udt-admin/udt_mass_codex.

The existing capture utility was inspected before use. Its name argument
is an absolute path, so all output writes remain inside this review folder.
It refuses to overwrite prior streams/JSON. Local script creation used
apply_patch. No original evidence was changed.

Source-first independent check, before candidate exposure:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_source_metric_connection_campaign_2026-09-08/step_01/review/independent_current_check_run /home/udt-admin/udt_mass_codex python3 udt_source_metric_connection_campaign_2026-09-08/step_01/review/independent_current_check.py
```

Started2026-09-08T01:42:12.147216+00:00, exit0, timeoutfalse,
duration0.4529381820029812seconds, maxRSS48524KiB. Python3.10.12,
SymPy1.13.1;16/16 finite exact diagnostic checks. Stdout SHA256:
04d69e05121bcd9cec8a006ca756fcc896fe6955295de1824c7766a57726a2f6.
JSON SHA256:
5a6c39d8b296497677d030996483944ef5209aab7974f7e8602b61f968936792.

Direct-stage author script replay, shared-code regression only:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_source_metric_connection_campaign_2026-09-08/step_01/review/author_replay /home/udt-admin/udt_mass_codex python3 udt_source_metric_connection_campaign_2026-09-08/step_01/check_current.py
```

Started2026-09-08T01:44:25.842083+00:00, exit0, timeoutfalse,
duration0.24425932700978592seconds, maxRSS47176KiB.14/14 checks.
Both child runs enforced536870912bytes address-space and60s CPU/wall.
Both stderr streams are empty with SHA256:
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.

No failed execution occurred. Negative controls deliberately exhibit
nonzero defects and are preserved in the independent stdout. Source-first
seal and initial candidate/review are not rewritten by later clarification.
