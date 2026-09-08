"""Independent banking correspondence check; no author-validator imports.

Written after the source-first seal and before new bank/row/guard exposure.
This checks bytes, IDs and retained execution records, not scientific truth.
"""
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[2]
BASE = "7b6ce629636c5ce3acee9f0e7427660b60857cc2"
SOURCE = "udt_source_metric_connection_campaign_2026-09-08"
NEW = {"G367", "G368", "G369"}
REGISTRY = "CURRENT_SCIENTIFIC_PREMISES.tsv"
BANK_RECORD = "udt_g367_g369_conditional_banking_2026-09-08/BANKING_RECORD.md"
checks = {}


def require(name, condition):
    checks[name] = bool(condition)
    if not condition:
        raise AssertionError(name)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def registry_check(current, original):
    lines = current.splitlines(keepends=True)
    old_lines = original.splitlines(keepends=True)
    rows = list(csv.DictReader(io.StringIO(current.decode()), delimiter="\t"))
    old_rows = list(csv.DictReader(io.StringIO(original.decode()), delimiter="\t"))
    ids = [row["premise_id"] for row in rows]
    require("baseline_349_rows", len(old_rows) == 349)
    require("current_352_unique_rows", len(ids) == len(set(ids)) == 352)
    require("new_ids_only", set(ids) - {r["premise_id"] for r in old_rows} == NEW)
    retained = b"".join(line for line in lines
                        if line.split(b"\t", 1)[0].decode() not in NEW)
    require("all_old_registry_bytes_preserved", retained == b"".join(old_lines))
    selected = [row for row in rows if row["premise_id"] in NEW]
    require("new_rows_well_formed", all(None not in row and None not in row.values()
                                       and all(row.values()) for row in selected))
    require("new_rows_bank_source", all(row["controlling_source"] == BANK_RECORD
                                       for row in selected))
    require("new_rows_conditional", all("BANKED_DERIVED_CONDITIONAL" in row["current_status"]
                                       for row in selected))
    return {row["premise_id"]: hashlib.sha256(
        next(line for line in lines if line.startswith(row["premise_id"].encode()+b"\t"))
    ).hexdigest() for row in selected}


old_registry = git("show", BASE + ":" + REGISTRY)
new_registry = (ROOT / REGISTRY).read_bytes()
row_pins = registry_check(new_registry, old_registry)
targets = [SOURCE, "CANON.md", "UDT_METRIC_KERNEL_DEVELOPMENT.md",
           "UDT_METRIC_KERNEL_COVERAGE.tsv"]
archive = git("archive", "--format=tar", BASE, "--", *targets)
preserved = []
with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
    for item in tar:
        if item.isfile():
            baseline_data = tar.extractfile(item).read()
            require("baseline_bytes:" + item.name,
                    (ROOT / item.name).read_bytes() == baseline_data)
            preserved.append(item.name)

manifest_count = 0
for line in (ROOT / SOURCE / "SHA256SUMS").read_text().splitlines():
    expected, relative = line.split(maxsplit=1)
    if relative.startswith(SOURCE + "/"):
        require("manifest:" + relative,
                hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected)
        manifest_count += 1

source_count = 0
with (ROOT / SOURCE / "SOURCE_LEDGER.tsv").open() as stream:
    for row in csv.DictReader(stream, delimiter="\t"):
        require("source_ledger:" + row["path"],
                hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"])
        source_count += 1

step = ROOT / SOURCE / "step_02"
original_run = json.loads((step / "author_checks_initial.json").read_text())
repaired_run = json.loads((step / "author_checks_repaired.json").read_text())
require("SM2_original_failure_retained", original_run["returncode"] == 1
        and not original_run["timeout"]
        and b"AssertionError: second_stabilizer_constraint" in
        (step / "author_checks_initial.stderr").read_bytes())
require("SM2_repaired_success_retained", repaired_run["returncode"] == 0
        and not repaired_run["timeout"])
require("SM2_failure_replay_bytes", (step / "author_checks_initial.stderr").read_bytes()
        == (step / "review/author_initial_replay.stderr").read_bytes())
require("SM2_repaired_replay_bytes", (step / "author_checks_repaired.stdout").read_bytes()
        == (step / "review/author_repaired_replay.stdout").read_bytes())

print(json.dumps({
    "status": "PASS", "meaning": "byte correspondence and registry integration only",
    "baseline": BASE, "current_head": git("rev-parse", "HEAD").decode().strip(),
    "original_registry_sha256": hashlib.sha256(old_registry).hexdigest(),
    "current_registry_sha256": hashlib.sha256(new_registry).hexdigest(),
    "new_row_sha256": row_pins, "baseline_preserved_file_count": len(preserved),
    "original_package_manifest_count": manifest_count,
    "controlling_source_ledger_count": source_count,
    "checks_passed": len(checks), "checks": checks,
}, indent=2, sort_keys=True))
