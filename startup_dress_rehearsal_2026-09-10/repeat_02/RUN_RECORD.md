# Repeat startup rehearsal — full premise verifier

Working directory: `/home/udt-admin/udt_mass_codex`

Observed HEAD and local origin/grok: `ec7a095e21a061e7ce9a076f2c615f10263798ed`.
Parent reports completing the ordered Git synchronization at 17:16:28 UTC on 2026-09-10 (corrected from the dispatch's approximate 17:14); this scoped reviewer independently inspected status, refs, and recent log without repeating Git writes.

Python version: Python 3.10.12.

Question: does the mandatory full premise-registry regression verifier complete successfully against the current working tree during this rehearsal?
No scientific model or physical choices are introduced. Existing verifier configuration is pinned by the repository's startup method, not by a new scientific premise.
Controls: one full invocation, `timeout --signal=KILL 600s`, no added memory cap. Observed shell data-segment, resident-memory, virtual-memory and CPU-time limits are unlimited. No GPU work is requested. The full process memory peak is recorded by `/usr/bin/time -v`.
Maximum conclusion: an observed regression result; no scientific promotion, runtime-capacity reset, or independent mathematical verification.

Exact command:

```bash
/usr/bin/time -v -o /tmp/udt_startup_repeat02.mXNfQr/full365.time.txt timeout --signal=KILL 600s python3 verify_current_scientific_premises.py > /tmp/udt_startup_repeat02.mXNfQr/full365.stdout.txt 2> /tmp/udt_startup_repeat02.mXNfQr/full365.stderr.txt
```

The captured shell exit code is returned by the execution tool. No artificial memory cap is set by this command.

## Observed result

Owning execution session: `15717`; final execution-tool exit code: `0`.
The final `/usr/bin/time` record independently reports exit status `0`.
The verifier reports PASS for its 365-row registry and stated startup/premise guards through G382.
Elapsed wall time: `6:47.46` (`407.46` seconds); user time `401.10` seconds; system time `6.80` seconds.
Maximum resident set size: `105600` KiB. Stderr is empty. No timeout occurred.
The output files initially had modification time `2026-09-10 17:17:45.827636403 UTC`; this is file metadata, not a separately instrumented process-start timestamp.

| Output | SHA-256 |
|---|---|
| `full365.stdout.txt` | `cdd907acf2487c1548aa7852ee738a83d75d95adae81b030ef77e396198538ec` |
| `full365.stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `full365.time.txt` | `e3946cb912189e4543980021ad4b9203953b7e0e37b37efd6fa9b2a551cd8d64` |

Live state was obtained from the owning execution session. A separate `ps` search returned no matching process during execution; that did not establish termination or absence, and the session continued to report running. Completion claims above use the final session result and saved timing.
