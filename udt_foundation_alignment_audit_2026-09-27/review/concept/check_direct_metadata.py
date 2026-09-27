"""Bounded independent correspondence check; no scientific source recertification."""
from pathlib import Path
from collections import Counter
import csv
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[3]
PACKET = ROOT / "udt_foundation_alignment_audit_2026-09-27"
OUT = Path(__file__).resolve().parent


def read_table(path):
    with path.open(newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = list(reader)
        return reader.fieldnames, rows


def keyed(rows, key):
    counts = Counter(r[key] for r in rows)
    assert all(n == 1 for n in counts.values()), counts
    return {r[key]: r for r in rows}


def command(args):
    p = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    return dict(command=args, returncode=p.returncode, stdout=p.stdout, stderr=p.stderr)


fields, current_rows = read_table(ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv")
_, candidate_rows = read_table(PACKET / "initial_candidate/REGISTRY_COVERAGE.tsv")
_, old_rows = read_table(ROOT / "udt_accepted_work_consolidation_2026-09-12/REGISTRY_COVERAGE.tsv")
_, family_rows = read_table(PACKET / "initial_candidate/FAMILY_ROUTING.tsv")
_, old_families = read_table(ROOT / "udt_accepted_work_consolidation_2026-09-12/FAMILY_MAP.tsv")
_, old_ledger = read_table(ROOT / "udt_accepted_work_consolidation_2026-09-12/SOURCE_READ_LEDGER.tsv")
_, parent_ledger = read_table(PACKET / "SOURCE_READ_LEDGER.tsv")
current, candidate, old = (keyed(rows, "premise_id") for rows in [current_rows, candidate_rows, old_rows])
assert set(candidate) == set(current)
field_mismatches = [(i, k) for i in current for k in fields if candidate[i][k] != current[i][k]]
assert not field_mismatches
mapping = {"term": "term", "epistemic_label": "epistemic_label_exact", "active_use": "active_use_exact", "controlling_source": "controlling_source_exact"}
common = sorted(set(old) & set(current))
old_mismatches = [(i, c) for i in common for c, o in mapping.items() if current[i][c] != old[i][o]]
assert not old_mismatches
added, removed = sorted(set(current) - set(old)), sorted(set(old) - set(current))
assert added == ["G" + str(i) for i in range(415, 424)] and not removed
disposition_mismatches = [i for i in old if candidate[i]["inherited_inspection_disposition"] != old[i]["inspection_disposition"]]
assert not disposition_mismatches
assignments = []
for f in family_rows:
    members = f["premise_ids"].split(";")
    assert len(members) == int(f["count"])
    assignments.extend(members)
    assert all(candidate[i]["editorial_family"] == f["family_id"] for i in members)
assert Counter(assignments) == Counter(current.keys())
old_family_by_id = keyed(old_families, "family_id")
new_family_by_id = keyed(family_rows, "family_id")
family_changes = [(i, k) for i, f in old_family_by_id.items() for k in f if new_family_by_id[i][k] != f[k]]
assert not family_changes
freeze = json.loads((PACKET / "INITIAL_FREEZE.json").read_text())
candidate_hashes = {}
freeze_mismatches = []
for name, expected in freeze["sha256"].items():
    actual = hashlib.sha256((PACKET / name).read_bytes()).hexdigest()
    candidate_hashes[name] = actual
    if actual != expected:
        freeze_mismatches.append(name)
assert not freeze_mismatches
parent_pin_mismatches = [r["path"] for r in parent_ledger if hashlib.sha256((ROOT / r["path"]).read_bytes()).hexdigest() != r["sha256"]]
assert not parent_pin_mismatches
tracked_raw = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
patch = command(["git", "apply", "--check", str(PACKET / "initial_candidate/MAINTAINED_DOCS.patch")])
assert patch["returncode"] == 0
result = {
    "utc": datetime.now(timezone.utc).isoformat(),
    "python": sys.version,
    "implementation": "Separate reviewer script; imports no parent builder/checker or scientific package.",
    "head": command(["git", "rev-parse", "HEAD"]),
    "tracked_diff": command(["git", "diff", "--name-only"]),
    "current_rows": len(current_rows), "candidate_rows": len(candidate_rows), "old_rows": len(old_rows),
    "current_field_count": len(fields), "all_current_field_mismatches": field_mismatches,
    "common_ids": len(common), "added": added, "removed": removed,
    "old_compared_field_map": mapping, "old_four_field_mismatches": old_mismatches,
    "inherited_disposition_mismatches": disposition_mismatches,
    "old_disposition_counts": dict(Counter(r["inspection_disposition"] for r in old_rows)),
    "old_source_ledger_rows": len(old_ledger),
    "old_source_parent_depth_counts": dict(Counter(r["parent_read_depth"] for r in old_ledger)),
    "old_source_reviewer_depth_counts": dict(Counter(r["reviewer_read_depth"] for r in old_ledger)),
    "family_rows": len(family_rows), "unchanged_inherited_families": len(old_families), "family_changes": family_changes,
    "unique_family_assignment_count": len(assignments),
    "parent_source_pin_count": len(parent_ledger), "parent_pin_mismatches": parent_pin_mismatches,
    "candidate_hashes": candidate_hashes, "freeze_mismatches": freeze_mismatches,
    "tracked_file_count": len(tracked_raw.rstrip(b"\0").split(b"\0")),
    "patch_read_only_check": patch,
    "limits": "Metadata correspondence only. No protected payload read. No scientific proof, full old row byte identity, all-source review, repo-wide classification or complete dependency graph claimed.",
}
(OUT / "DIRECT_METADATA_CHECKS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: result[k] for k in ["current_rows", "candidate_rows", "old_rows", "current_field_count", "common_ids", "added", "removed", "family_rows", "unchanged_inherited_families", "parent_source_pin_count", "tracked_file_count", "freeze_mismatches", "old_disposition_counts"]}, indent=2))
