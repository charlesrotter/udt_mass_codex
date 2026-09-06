# Commands, versions and preservation record

Date: 2026-09-06. Working directory: `/home/udt-admin/udt_mass_codex`.
Base HEAD and refreshed origin/grok: `5ef2f971805ee23383cad694c5cb058124614a5d`.
Only this candidate directory is part of the evidence change. The checkpoint's
commit identifier is the enclosing Git commit, not a scientific acceptance.

## Orientation and sources

On-disk AGENTS, LIVE/HANDOFF current blocks, current program/premise summary,
the specified CLAUDE sections, four triggered skill files, INDEX, MEMORY and
CROSS_MODEL_VERIFY were read. No fresh startup was launched: this continues the
post-restart repository session already accepted by Charles. `git status
--short --branch`, `git rev-parse HEAD origin/grok` and `git fetch origin` checked
the current state. Fetch succeeded and left the remote tracking hash equal to
HEAD. There was no resume/fork operation or new model/infrastructure audit.

The source manifest pins the exact registry, status/method files and load-bearing
G349/G351/G352 reports/derivations/adoption. Only the exact G349, G351 and G352
registry rows were queried, after the fresh premise verifier passed. Historical
pending labels in exact derivation headers do not override current registry and
audit-report acceptance. No scientific source was repaired or strengthened.

## Scientific checks actually run

```bash
python3 verify_current_scientific_premises.py
python3 --version
python3 -c 'import sympy; print(sympy.__version__)'
free -m
timeout 60s python3 udt_g349_normalized_cone_phase_extension_candidate_2026-09-06/check_exact.py
python3 udt_g349_normalized_cone_phase_extension_candidate_2026-09-06/run_checks.py
python3 udt_g349_normalized_cone_phase_extension_candidate_2026-09-06/recompute_saved.py
```

The initial exact run and initial rational recomputation returned exit 0. The
captured replays also passed; they are not independent extra evidence. The
runner records its actual Python executable, commands, separate stdout/stderr,
return codes and elapsed times in CHECK_RUNS.json. Its baseline stdout is also
saved as CHECK_RESULT.json. Its four mutant invocations are recorded there and
each has the intended AssertionError, not an import or timeout failure.

The final rational replay was captured using this read-only subprocess wrapper:

```bash
python3 -c 'import json, subprocess; command=["python3", "udt_g349_normalized_cone_phase_extension_candidate_2026-09-06/recompute_saved.py"]; p=subprocess.run(command, capture_output=True, text=True, timeout=60); print(json.dumps({"command":command,"returncode":p.returncode,"stdout":p.stdout,"stderr":p.stderr},indent=2))'
```

Its output is RECOMPUTATION_RUN.json. The premise audit's tool output is preserved
as a combined stream in PREMISE_VERIFIER_OUTPUT.txt; separate stream capture was
not available for that already-running invocation. No failure is suppressed.
Python 3.10.12, SymPy 1.13.1; exact symbolic expressions/rationals only. The
single-machine memory snapshot was 124000 MiB available. Peak process memory
was not independently measured. Each captured exact child completed in under
one second; the verifier was a separate read-only repository audit. No GPU,
grid, scientific production process, numerical tolerance or restart checkpoint
for a long solve was used.

## Closure checks

```bash
sha256sum -c udt_g349_normalized_cone_phase_extension_candidate_2026-09-06/SOURCE_SHA256SUMS
sha256sum -c udt_g349_normalized_cone_phase_extension_candidate_2026-09-06/ARTIFACT_SHA256SUMS
git diff --check
git diff --cached --check
git diff --cached --stat
git status --short --branch
```

The artifact manifest includes all package payloads except the manifest itself.
Manifests are ordinary unsigned hashes, not evidence of truth or review. Before
staging, tracked diff was empty and status contained the new candidate directory
plus the same 46 unrelated untracked entries. Preservation here means no actions
against those payloads and unchanged status entries, not a content/backup audit.
Only the named candidate directory is staged, committed and pushed on grok.
No registry, status surface, fixed-snapshot manuscript or accepted package is
part of this change. The old candidate and its independent review remain intact.

Backup completeness and pre-reboot unsaved-state disposition remain UNVERIFIED.
No ScratchDisk operation or protected-payload inspection was performed. Local
repository checks do not discharge either unverified preservation item.
