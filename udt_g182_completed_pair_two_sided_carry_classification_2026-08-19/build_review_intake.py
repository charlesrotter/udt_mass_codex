#!/usr/bin/env python3
"""Build a sealed G182 review intake containing only declared package evidence and sources."""

import csv
import hashlib
import json
from pathlib import Path
import shutil
import tempfile


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
EXCLUDE = {"build_review_intake.py", "VERIFICATION_RESULT.json"}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run():
    destination = Path(tempfile.mkdtemp(prefix="udt_g182_review_", dir="/tmp"))
    package_target = destination / ROOT.name
    package_target.mkdir()

    copied = []
    for source in sorted(ROOT.iterdir()):
        if not source.is_file() or source.name in EXCLUDE or source.name.startswith("EXTERNAL_"):
            continue
        target = package_target / source.name
        shutil.copy2(source, target)
        copied.append(target)

    with (ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        source = REPO / row["path"]
        if sha256(source) != row["sha256"]:
            raise SystemExit(f"source hash mismatch: {row['path']}")
        target = destination / "sources" / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)

    records = []
    for path in sorted(copied):
        records.append({"path": str(path.relative_to(destination)), "sha256": sha256(path), "bytes": path.stat().st_size})
    tree_material = "".join(f"{item['sha256']}  {item['path']}\n" for item in records).encode()
    scope = {
        "audit": "G182",
        "permission": "fresh read-only adversarial review; no edits or research continuation",
        "payload_file_count": len(records),
        "total_file_count_including_scope": len(records) + 1,
        "tree_digest_sha256": hashlib.sha256(tree_material).hexdigest(),
        "files": records,
    }
    scope_path = destination / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"intake": str(destination), "scope_sha256": sha256(scope_path), **{key: scope[key] for key in ("payload_file_count", "total_file_count_including_scope", "tree_digest_sha256")}}, sort_keys=True))


if __name__ == "__main__":
    run()
