# External final-adjudication verifier

This verifier is deliberately outside the frozen
`native_action_final_adjudication_2026-07-18/` package. It validates the
immutable Stage-I, Stage-II, Arm-C, and final-adjudication packages; copies the
24 load-bearing CAS scripts into a caller-supplied external work directory;
runs only those copies; compares their standard output byte-for-byte with the
frozen outputs; and then confirms that every package has the same complete
per-file state as it had before execution.

It does not write to, chmod, import as a Python package, or execute a script in
any frozen package. The only writes are copied scripts and run artifacts below
the external `--work-root`, plus the optional JSON file named by `--report`.

The clean-environment dependency lock is `requirements-verifier.txt`. Both
SymPy and its runtime dependency are exactly pinned:

```text
sympy==1.13.1
mpmath==1.3.0
```

The recorded run used a new virtual environment and a new work root under
`/tmp`, with user-site packages disabled and CUDA visibility empty. No GPU code
is imported or executed.

Example invocation from the clean environment:

```bash
PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= \
  /tmp/VERIFIER_VENV/bin/python -I -B verify_frozen_adjudication.py \
  --repo /home/udt-admin/udt_mass_codex \
  --work-root /tmp/VERIFIER_WORK \
  --report /home/udt-admin/udt_mass_codex/native_action_external_verifier_2026-07-18/VERIFY_RESULT.json
```

The verifier fails closed unless both its own interpreter and every copied CAS
run are isolated, the virtual environment excludes system and user site
packages, and the repository is absent from the verifier's import path. It
also fails on a package-manifest mismatch, unlisted or missing
package file, writable frozen file, script-inventory mismatch, dependency or
environment mismatch, nonzero script exit, any standard error, any stdout
difference, failed catch-proof probe, or any pre/post package-state difference.
