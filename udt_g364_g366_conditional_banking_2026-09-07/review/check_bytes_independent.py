"""Read-only banking byte/scope comparison, independently of the premise guard.

No scientific formulas or author banking helper are imported. Reports to stdout;
the existing resource/capture wrapper owns output files and limits.
"""
import csv
import hashlib
import io
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = "554b0be4b369aa11aa3afa073f7b1ee954a76a87"
BANK = "udt_g364_g366_conditional_banking_2026-09-07"
CAMPAIGN = "udt_recipe_restrictiveness_campaign_2026-09-07"
NEW = {b"G364", b"G365", b"G366"}
ALLOWED = {
    "AGENTS.md", "LIVE.md", "HANDOFF.md", "CURRENT_RESEARCH_PROGRAM.md",
    "CURRENT_SCIENTIFIC_PREMISES.md", "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "INDEX.md", "MEMORY.md", "verify_current_scientific_premises.py",
    "tests/test_startup_surface.py",
}


def git(*args):
    return subprocess.run(["git", "-c", "core.preloadIndex=false", *args], cwd=ROOT, check=True,
                          capture_output=True, timeout=10).stdout


def digest(data):
    return hashlib.sha256(data).hexdigest()


def authenticate(relative):
    manifest = (ROOT / relative).read_text().splitlines()
    paths = []
    for entry in manifest:
        expected, path = entry.split(maxsplit=1)
        assert path not in paths, ("duplicate manifest path", path)
        assert digest((ROOT / path).read_bytes()) == expected, path
        paths.append(path)
    return {"entries": len(paths), "sha256": digest((ROOT / relative).read_bytes())}


current = (ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv").read_bytes()
old = git("show", BASE + ":CURRENT_SCIENTIFIC_PREMISES.tsv")
lines = current.splitlines(keepends=True)
added = [line for line in lines if line.split(b"\t", 1)[0] in NEW]
preserved = b"".join(line for line in lines if line.split(b"\t", 1)[0] not in NEW)
assert preserved == old, "old registry bytes changed"
assert len(added) == 3 and {line.split(b"\t", 1)[0] for line in added} == NEW
rows = list(csv.DictReader(io.StringIO(current.decode()), delimiter="\t"))
old_rows = list(csv.DictReader(io.StringIO(old.decode()), delimiter="\t"))
assert len(rows) == len({row["premise_id"] for row in rows}) == 349
assert len(old_rows) == 346
for row in rows:
    if row["premise_id"].encode() in NEW:
        assert row["current_status"] == (
            "BANKED_DERIVED_CONDITIONAL__VERIFIED_WITH_CAVEATS__OWNER_AUTHORIZED"
            "__NOT_PHYSICAL_ADOPTION__NOT_CANON")
        assert row["epistemic_label"] == "MIXED"
        assert row["controlling_source"] == BANK + "/BANKING_RECORD.md"

changed = git("diff", "--name-only", BASE).decode().splitlines()
assert set(changed) == ALLOWED, ("unexpected tracked change scope", changed)
fixed = {}
for path in (
    "CANON.md", "UDT_METRIC_KERNEL_DEVELOPMENT.md", "UDT_METRIC_KERNEL_COVERAGE.tsv",
    CAMPAIGN + "/CLOSURE_RECEIPT.json",
    "udt_g361_g363_conditional_banking_2026-09-07/BANKING_RECORD.md",
    "udt_shared_readout_metric_constraint_campaign_2026-09-06/step_03/CANDIDATE_ARGUMENT.md",
):
    data = (ROOT / path).read_bytes()
    assert data == git("show", BASE + ":" + path), path
    fixed[path] = digest(data)

print(json.dumps({
    "status": "PASS", "scope": "byte correspondence and exact tracked change scope only",
    "runtime_python": sys.version, "baseline": BASE,
    "observed_head": git("rev-parse", "HEAD").decode().strip(),
    "old_rows": len(old_rows), "new_rows": len(rows),
    "added_ids": sorted(item.decode() for item in NEW),
    "old_registry_sha256": digest(old), "current_registry_sha256": digest(current),
    "old_rows_byte_identical": True, "tracked_change_paths": changed,
    "source_campaign": authenticate(CAMPAIGN + "/CAMPAIGN_SHA256SUMS"),
    "stage_a": authenticate(BANK + "/review/STAGE_A_SHA256SUMS.stdout"),
    "direct_freeze": authenticate(BANK + "/DIRECT_REVIEW_SHA256SUMS.stdout"),
    "fixed_payload_sha256": fixed,
    "protected_payload_bytes": "NOT_READ", "full_premise_audit": "NOT_RUN",
    "scientific_recomputation": "NOT_RUN",
}, indent=2, sort_keys=True))
