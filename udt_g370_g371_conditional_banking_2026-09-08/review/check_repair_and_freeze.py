"""Post-exposure integration-repair replay, with no maintained-file writes."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
PKG = ROOT / "udt_g370_g371_conditional_banking_2026-09-08"
BASE = "6eea4b90c59e5fd873d793c073b55ecab67d1992"
VERIFIER = "verify_current_scientific_premises.py"


def sha(data):
    return hashlib.sha256(data).hexdigest()


pins = {}
with (PKG / "INTEGRATION_FREEZE.tsv").open() as stream:
    for row in csv.DictReader(stream, delimiter="\t"):
        actual = sha((ROOT / row["path"]).read_bytes())
        assert actual == row["sha256"], "freeze mismatch: " + row["path"]
        pins[row["path"]] = actual

baseline = subprocess.check_output(["git", "show", BASE + ":" + VERIFIER], cwd=ROOT)
with tempfile.TemporaryDirectory(prefix="udt-rt-repair-review-") as directory:
    fixture = Path(directory)
    (fixture / VERIFIER).write_bytes(baseline)
    command = ["git", "apply", "--recount", str(PKG / "INITIAL_VERIFIER_DIFF.patch")]
    applied = subprocess.run(command, cwd=fixture, capture_output=True)
    assert applied.returncode == 0, applied.stderr.decode()
    initial = (fixture / VERIFIER).read_text()

current = (ROOT / VERIFIER).read_text()
fixed = initial
edits = []
variants = [("initial", initial, "current route lacks 352-row: CURRENT_RESEARCH_PROGRAM.md")]
for name in ("CURRENT_RESEARCH_PROGRAM.md", "CURRENT_SCIENTIFIC_PREMISES.md"):
    before = f'        "{name}": (\n            "352-row",'
    after = before.replace('"352-row"', '"354-row"')
    assert fixed.count(before) == 1, "repair context must be unique: " + name
    fixed = fixed.replace(before, after, 1)
    edits.append({"control": name, "before": "352-row", "after": "354-row"})
    if name == "CURRENT_RESEARCH_PROGRAM.md":
        variants.append(("first_count_only", fixed,
                         "current route lacks 352-row: CURRENT_SCIENTIFIC_PREMISES.md"))
assert fixed == current, "repaired verifier has additional changes beyond two current count tokens"
variants.append(("both_current_counts_repaired", fixed, None))

replays = {}
for name, source, expected in variants:
    namespace = {"__name__": "bounded_repair_review", "__file__": str(ROOT / VERIFIER)}
    exec(compile(source, str(ROOT / VERIFIER), "exec"), namespace)
    try:
        namespace["validate_startup_surface"](ROOT)
    except (SystemExit, AssertionError, RuntimeError) as error:
        observed = str(error)
        assert expected is not None and expected in observed, (name, expected, observed)
    else:
        observed = "PASS"
        assert expected is None, "false pass: " + name
    replays[name] = observed

failed = json.loads((PKG / "banking_checks_initial.json").read_text())
passed = json.loads((PKG / "banking_checks_repaired.json").read_text())
assert failed["returncode"] == 1 and not failed["timeout"]
assert (PKG / "banking_checks_initial.stderr").read_text().strip() == replays["initial"]
assert passed["returncode"] == 0 and not passed["timeout"]

print(json.dumps({
    "status": "PASS", "meaning": "exact two-token integration repair and frozen-target correspondence; shared startup-guard replay only",
    "frozen_targets": pins, "reconstruct_command_in_temporary_fixture": command,
    "git_apply_stdout": applied.stdout.decode(), "git_apply_stderr": applied.stderr.decode(),
    "initial_reconstructed_verifier_sha256": sha(initial.encode()),
    "repaired_verifier_sha256": sha(current.encode()), "exact_changes": edits,
    "actual_rejection_and_success_replays": replays,
    "original_failed_and_repaired_receipts_preserved": True,
}, indent=2, sort_keys=True))
