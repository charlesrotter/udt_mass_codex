# Review executable commands and evidence

Working directory for all commands:
`/home/udt-admin/udt_mass_codex`.

Before candidate/author/partner code exposure, run:

```bash
python3 udt_kernel_twist_information_audit_2026-09-10/review/run_independent.py
```

This wrapper saves the exact scientific argv, output, versions, shapes, elapsed time,
exit status and 120-second CPU timeout in independent.run.json and companion stdout/stderr.
PRE_CANDIDATE_REASONING.md and CONTEXT.json precede it and record argument/exposure.

After the independent argument and candidate inspection, run:

```bash
python3 udt_kernel_twist_information_audit_2026-09-10/review/run_replays.py
```

The wrapper saves each exact argv and result separately and in REPLAY_RESULTS.json.
It runs the unmodified corrected author, optimized-mode guard, initial preserved-failure
reproduction, actual author equality-guard injection and isolated harness guards.
Every scientific child has subprocess timeout=120 and writes only under review/.

Read-only provenance checks used git status, git rev-parse HEAD, git diff --name-only,
git diff --cached --name-only, exact DictReader selections from the registry, and SHA-256
of declared source/freeze/whiteboard-manifest entries. PRESERVATION_CHECK.json records
every expected/actual digest, byte-size correspondence where declared, and the exact
shape-only R1 difference. Protected prefixes are explicitly excluded. No all-repository
hash, protected payload read, source test census, git mutation or scientific promotion
was performed. Tool transcript retains the exact read commands and preservation heredoc.

The manifest lists review evidence excluding the manifest itself. Completion records the
actual review completion clock and verdict; hashes establish byte correspondence only.
