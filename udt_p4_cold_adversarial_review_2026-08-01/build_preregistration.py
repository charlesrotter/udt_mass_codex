#!/usr/bin/env python3
"""Freeze the P4 cold-review units and exact source bytes before outcome work."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "2e93a621aeeee0a0844543068363d0ba94094357"
SUMMARY = ROOT / "P4_ARC_SUMMARY_2026-07-31.md"
SUGGESTION = ROOT / "P4_COLD_ADVERSARIAL_REVIEW_SUGGESTION_2026-08-01.md"

CONTROLS = [
    "AGENTS.md", "LIVE.md", "HANDOFF.md", "CURRENT_SCIENTIFIC_PREMISES.md",
    "CURRENT_SCIENTIFIC_PREMISES.tsv", "CANON.md", "NEGATIVES_REGISTRY.md",
    "ROADMAP_LINEAR_TIME_2026-07-31.md", "INFLIGHT_STATE.md",
    "P4_ARC_SUMMARY_2026-07-31.md", "P4_COLD_ADVERSARIAL_REVIEW_SUGGESTION_2026-08-01.md",
    "SCOPING_MAP_seam_constants_from_metric_2026-07-31.md",
    "PONDER_MATH_ELEGANCE_2026-07-31.md", "PONDER_100KLY_VIEW_2026-07-31.md",
]

QUESTIONS = [
    ("Q1", "Does the inverse-problem domain follow from the metric and registered premises, or silently choose an alphabet, pairing, posture, census, or variation rule?"),
    ("Q2", "Do static, time-live, and angular-live response spaces embed exactly, without a formal-family to fixed-realized-metric quantifier change?"),
    ("Q3", "Do mass branches and stability results survive their complete premise stacks, without conditional definitions being narrated as physical mass?"),
    ("Q4", "Is the real-character versus compact-circle integer distinction a theorem of the admitted domain rather than an artifact of chosen topology or transition class?"),
    ("Q5", "Does A3 exhaust its stated torus, full-sphere, and fine-detail layers without steering toward integers?"),
    ("Q6", "Are coordinate/projected reading forks shape-neutral through A2, and where do they first become physically distinguishable?"),
    ("Q7", "Which P4 claims are independent, which share one derivation or implementation, and which require different-method recomputation?"),
    ("Q8", "Does nuclear scoping remain separated into banked structural theorems, textbook/SEMF reimplementation, and conditional identifications?"),
]


def run(*args: str) -> str:
    return subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=True).stdout


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_summary() -> list[dict[str, str]]:
    pattern = re.compile(r"^\| (\d+) \| `([^`]+)` \| ([^|]+?) \| (.+) \|$", re.MULTILINE)
    rows = [
        {"unit_id": f"P4-{int(i):02d}", "package": package.rstrip("/"),
         "bank_commit": commit.strip(), "verbatim_headline_bundle": verdict.strip(),
         "unit_kind": "PACKAGE_HEADLINE_BUNDLE"}
        for i, package, commit, verdict in pattern.findall(SUMMARY.read_text())
    ]
    assert len(rows) == 29
    assert [r["unit_id"] for r in rows] == [f"P4-{i:02d}" for i in range(29)]
    assert all((ROOT / r["package"]).is_dir() for r in rows)
    return rows


def tracked_map() -> dict[str, str]:
    entries = {}
    for line in run("git", "ls-files", "-s").splitlines():
        meta, path = line.split("\t", 1)
        entries[path] = meta.split()[1]
    return entries


def role(path: str) -> str:
    name = Path(path).name
    if name == "PREREGISTRATION.md": return "PREREGISTRATION"
    if "VERIFIER" in name: return "VERIFIER"
    if name.endswith((".py", ".sh")): return "EXECUTABLE"
    if name.endswith((".json", ".tsv", ".csv", ".npz", ".log", ".txt")): return "MACHINE_OR_RAW_EVIDENCE"
    if name in {"AUDIT_REPORT.md", "EXACT_DERIVATION.md", "DECISION_SURFACE_UPDATE.md"}: return "LOAD_BEARING_REPORT"
    if path in CONTROLS: return "CONTROL_OR_CROSS_CUTTING"
    return "PACKAGE_RECORD"


def main() -> None:
    units = parse_summary()
    with (HERE / "FROZEN_REVIEW_UNITS.tsv").open("w", newline="") as fh:
        fields = ["unit_id", "package", "bank_commit", "unit_kind", "verbatim_headline_bundle"]
        writer = csv.DictWriter(fh, fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(units)
        for qid, question in QUESTIONS:
            writer.writerow({"unit_id": qid, "package": SUGGESTION.name, "bank_commit": BASE[:7],
                             "unit_kind": "CROSS_CUTTING_QUESTION",
                             "verbatim_headline_bundle": question})

    tracked = tracked_map()
    selected = set(CONTROLS)
    for unit in units:
        prefix = unit["package"] + "/"
        selected.update(p for p in tracked if p.startswith(prefix))
    assert all(p in tracked and (ROOT / p).is_file() for p in selected)

    inventory = []
    package_by_prefix = [(u["package"] + "/", u["unit_id"]) for u in units]
    for path in sorted(selected):
        unit_id = next((uid for prefix, uid in package_by_prefix if path.startswith(prefix)), "CONTROL")
        full = ROOT / path
        inventory.append({"unit_id": unit_id, "path": path, "git_blob": tracked[path],
                          "sha256": sha(full), "size_bytes": full.stat().st_size,
                          "role": role(path)})
    with (HERE / "SOURCE_INVENTORY.tsv").open("w", newline="") as fh:
        fields = ["unit_id", "path", "git_blob", "sha256", "size_bytes", "role"]
        writer = csv.DictWriter(fh, fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(inventory)
    (HERE / "SOURCE_MANIFEST.sha256").write_text(
        "".join(f"{row['sha256']}  ../{row['path']}\n" for row in inventory))

    snapshot = {
        "base": BASE,
        "package_units": len(units),
        "cross_cutting_units": len(QUESTIONS),
        "total_units": len(units) + len(QUESTIONS),
        "source_paths": len(inventory),
        "frozen_review_units_sha256": sha(HERE / "FROZEN_REVIEW_UNITS.tsv"),
        "source_inventory_sha256": sha(HERE / "SOURCE_INVENTORY.tsv"),
        "source_manifest_sha256": sha(HERE / "SOURCE_MANIFEST.sha256"),
        "summary_sha256": sha(SUMMARY),
        "suggestion_sha256": sha(SUGGESTION),
    }
    (HERE / "PREREG_SNAPSHOT.json").write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n")
    print(json.dumps(snapshot, sort_keys=True))


if __name__ == "__main__":
    main()

