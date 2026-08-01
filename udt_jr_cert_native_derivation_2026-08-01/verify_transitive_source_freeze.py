#!/usr/bin/env python3
"""Read-only fail-closed verifier for the transitive evidence amendment."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "686336343878e8a9e39a4b72df08d23754243631"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tracked_under(directory: str) -> list[str]:
    output = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASE, "--", directory], cwd=ROOT, text=True
    )
    return [line for line in output.splitlines() if line]


with (HERE / "TRANSITIVE_PACKAGE_SCOPE.tsv").open(encoding="utf-8", newline="") as handle:
    packages = list(csv.DictReader(handle, delimiter="\t"))
with (HERE / "TRANSITIVE_SOURCE_INVENTORY.tsv").open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))

original = {
    line.strip()
    for line in (HERE / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
paths = [row["path"] for row in rows]
transitive = set(paths)
scoped = set().union(*(set(tracked_under(row["package_path"])) for row in packages))
expected = scoped - original
combined_lines = [line for line in (HERE / "COMBINED_SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines() if line]
snapshot = json.loads((HERE / "TRANSITIVE_FREEZE_SNAPSHOT.json").read_text(encoding="utf-8"))

assert len(packages) == 10
assert len(original) == 172
assert paths == sorted(paths) and len(paths) == len(transitive)
assert not (original & transitive)
assert transitive == expected
assert combined_lines == sorted(original | transitive)
assert len(combined_lines) == len(original) + len(transitive)
assert all(row["base"] == BASE for row in rows)
assert all(
    (ROOT / row["path"]).is_file()
    and digest(ROOT / row["path"]) == row["sha256"]
    and (ROOT / row["path"]).stat().st_size == int(row["bytes"])
    and subprocess.check_output(["git", "rev-parse", f"{BASE}:{row['path']}"], cwd=ROOT, text=True).strip()
    == row["blob"]
    for row in rows
)
assert snapshot["base"] == BASE
assert snapshot["package_count"] == 10
assert snapshot["transitive_additions"] == len(rows)
assert snapshot["combined_sources"] == len(combined_lines)
assert snapshot["package_scope_sha256"] == digest(HERE / "TRANSITIVE_PACKAGE_SCOPE.tsv")
assert snapshot["transitive_paths_sha256"] == digest(HERE / "TRANSITIVE_SOURCE_PATHS.txt")
assert snapshot["transitive_inventory_sha256"] == digest(HERE / "TRANSITIVE_SOURCE_INVENTORY.tsv")
assert snapshot["transitive_manifest_sha256"] == digest(HERE / "TRANSITIVE_SOURCE_MANIFEST.sha256")
assert snapshot["combined_paths_sha256"] == digest(HERE / "COMBINED_SOURCE_PATHS.txt")
assert "cannot broaden" in (HERE / "PREREGISTRATION_AMENDMENT.md").read_text(encoding="utf-8")
print(
    "PASS transitive amendment: "
    f"packages={len(packages)} additions={len(rows)} combined={len(combined_lines)} base={BASE}"
)
