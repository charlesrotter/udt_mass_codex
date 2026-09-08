# Reviewer execution record

All reviewer checks use the unchanged existing shared
udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py.
The launcher prefix is exactly:

    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py

It is followed by the absolute capture stem in this review directory, the
repository cwd /home/udt-admin/udt_mass_codex, and the child command array in
the corresponding capture JSON. The runner imposes512MiB/60CPU-wall seconds,
keeps .stdout/.stderr/.json without overwrites, and records actual resources.
All hand edits use apply_patch. Simple inspection commands live in the tool
transcript; no new scientific computation or original scientific suite replay.

## Preserved reviewer runtime failure and bounded remedy

`integration_correspondence.*` preserves the initial failed read-only check:
exit1, no timeout,0.067143674s, reported maxRSS30680KiB. Registry byte/row
checks ran before the failure. Git then reported `unable to create threaded
lstat: Resource temporarily unavailable` while running `git diff --name-only`
inside the512MiB child. The same command outside that child returned the nine
expected files. This identifies an operational resource failure, not a
scientific or correspondence counterexample.

The finite diagnostic permits one same-budget retry with per-command Git index
preloading disabled, stopping on success or a repeated resource error. No config
file, scientific equation, comparison criterion or memory limit is changed.
The initial script SHA256 was
04cfdf6ad87eee4b9a1c705e032a921fd06958155026fcdbefd41e2fdb02761e.
It is exactly reconstructible from the current script by replacing this line:

    changed = subprocess.check_output(['git', '-c', 'core.preloadIndex=false', 'diff', '--name-only'], cwd=ROOT,

with its original line:

    changed = subprocess.check_output(['git', 'diff', '--name-only'], cwd=ROOT,

The original command, error and empty stdout remain unchanged. The retry has
a distinct capture stem and is not relabeled as an original passing run.
