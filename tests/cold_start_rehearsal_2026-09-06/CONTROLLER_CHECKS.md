# Production controller checks

**Controller date:** 2026-09-06
**Controller source HEAD before banking:** `12e3e5e0c50424133f15c8fde511da6302bd6e90`

These checks were executed in the production checkout after the narrow
`HANDOFF.md` repair and after the four fresh-context subjects completed.

```text
$ python3 -m pytest tests/test_startup_surface.py tests/test_guardrail_policy.py -q
82 passed in 402.42s

$ python3 verify_metric_kernel_account.py
PASS metric-kernel account: 335 rows; roles={'BOUNDARY_RESULT': 76,
'CONTROL_ONLY': 57, 'MAIN_ARGUMENT': 65, 'OUTSIDE_SCOPE': 12,
'SUPERSEDED_HISTORICAL': 2, 'SUPPORTING_LEMMA': 123}

$ python3 verify_current_scientific_premises.py
PASS: G242 through G352 startup and premise guards; PASS: 335-row premise
registry, current bounded startup route, archive integrity,
relational-depth/orchestra guards, X_max semantics, 754 historical
dispositions, and corrected DOF semantics

$ sha256sum --check tests/cold_start_rehearsal_2026-09-06/REPAIRED_SOURCE_HASHES.sha256
13 files: OK

$ git diff --check
PASS (no output)
```

Controller parsing of the four JSONL transcripts found one completed turn in
each; command counts R1/R2/R3/R4 were 12/23/25/34. No parsed subject command
used a protected path or performed checkout, fetch, pull, push, reset, clean,
add, commit, deletion, process termination, shutdown, reboot, curl, or wget.

The R2 sentinel and retained copy were byte-identical at SHA-256
`8c4cdeedb543304d8e9035d5a843ae4a87a381c048dba61b592fe1fac37de03d`.
The R3 subject JSON and retained copy were byte-identical at SHA-256
`b168bd886ab95f89111d103ef4577eb56c3c72503e555723209ba456a57b9c75`.

These passes support `COLD_ORIENTATION_READY`. They do not establish a backup
of protected or untracked workstation state, do not test a post-update Astra
deployment, and do not authorize a reboot.
