"""Read-only fixed-edition check; NOT a pass of the stock current-input command.

The stock account verifier hardcodes the live registry filename. This harness
substitutes only its registry_rows provider in this process, after authenticating
the exact fixed-edition Git bytes against the provider's own SHA256 constant.
The remaining unmodified verifier checks the live manuscript, sidecar, source
bindings, roles and dependencies. No source file or review binding is changed.
"""
import contextlib
import csv
import datetime
import hashlib
import io
import json
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import verify_metric_kernel_account as verifier

def main():
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    t = time.monotonic()
    command = ["git", "show", verifier.account.SCIENTIFIC_SNAPSHOT
               + ":CURRENT_SCIENTIFIC_PREMISES.tsv"]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=30)
    if result.returncode:
        raise RuntimeError(result.stderr.decode())
    digest = hashlib.sha256(result.stdout).hexdigest()
    if digest != verifier.account.REGISTRY_SHA256:
        raise RuntimeError("fixed-edition registry hash mismatch")
    rows = list(csv.DictReader(io.StringIO(result.stdout.decode()), delimiter="\t"))
    original = verifier.account.registry_rows
    captured = io.StringIO()
    try:
        verifier.account.registry_rows = lambda: rows
        with contextlib.redirect_stdout(captured):
            code = verifier.main()
    finally:
        verifier.account.registry_rows = original
    print(json.dumps(dict(
        kind="authenticated_fixed_registry_input_substitution_not_stock_current_input_pass",
        started_utc=started, duration_seconds=time.monotonic()-t,
        git_command=command, git_returncode=result.returncode,
        git_stderr=result.stderr.decode(), registry_sha256=digest,
        registry_rows=len(rows), verifier_returncode=code,
        verifier_stdout=captured.getvalue(), persistent_source_writes=False,
        independence="same existing verifier, input-adapted reproducibility only")))
    return code

if __name__ == "__main__":
    raise SystemExit(main())
