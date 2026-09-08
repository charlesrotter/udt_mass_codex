# Actual command and version record

Cwd /home/udt-admin/udt_mass_codex, branch grok. Observed Python3.10.12 and
git2.34.1 via `python3 --version` and `git --version`. No solver, model or
configuration change. Git writes use the environment's normal escalation;
no force, stash, clean, reset or protected-path staging.

The required startup commands were executed in this order:

    git status --short --branch
    git checkout grok
    git fetch origin
    git pull --ff-only origin grok
    git status --short --branch
    git log -8 --oneline

Both full premise checks ran this exact child command in the cwd above:

    python3 -B verify_current_scientific_premises.py

The parent inline Python wrapper used subprocess.run(capture_output=True,
timeout=900), resource.setrlimit(RLIMIT_AS,(2147483648,2147483648)) and
RLIMIT_CPU(900,900) in preexec_fn. The shell set OPENBLAS_NUM_THREADS,
OMP_NUM_THREADS,MKL_NUM_THREADS,NUMEXPR_NUM_THREADS to1 and
PYTHONDONTWRITEBYTECODE to1. The prebank wrapper used text=True; the postbank
wrapper captured bytes then decoded them and retained TimeoutExpired streams
if needed. Each prints actual command/cwd/start/duration/RSS/limits/returncode
and stdout/stderr as JSON to the tool. Exact emitted JSON and separate stream
files are preserved as prebank_361.* and, after completion, postbank_363.*.
These are actual tool-captured receipts, not another invocation of the audit.

Focused parent invocation (one librarythread, bytecode disabled):

    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_g379_g380_conditional_banking_2026-09-08/focused_initial /home/udt-admin/udt_mass_codex python3 -B /home/udt-admin/udt_mass_codex/udt_g379_g380_conditional_banking_2026-09-08/check_banking.py

The existing capture utility was read fully and reused unchanged; its receipt
owns exact512MiB/60CPU-wall limits and actual results. Reviewer capture commands
and versions belong to review/*.json and the complete review report. A replay
of shared code is reproducibility, not a different implementation or proof.

Small read-only correspondence additionally used sha256sum --check --quiet on
the source149 and planning14 manifests, and an explicit Python/Git comparison
of the registry minus ONLY G379/G380 against b1dda672's registry. They passed.
Git diff --check passed for the tracked integration. Later actual publication
commands/results are recorded only after they occur, in PUBLICATION_RECEIPT.md.
