#!/usr/bin/env python3
"""Hostile-mutation catch proof for every load-bearing R4 verifier surface."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
CELL_ROOT = Path("/media/udt-admin/ScratchDisk/Data/UDT_BOSS_R3_2026-08-14/R3_COVARIANCE_CELLS")
FILES = (
    "R2_CURVE_ATLAS.tsv",
    "R4_RELATION_ATLAS.tsv",
    "R4_CROSS_LAG_ATLAS.npz",
    "R4_CAP_COVARIANCE_ATLAS.tsv",
    "R4_SUMMARY.tsv",
    "R4_RESULT.json",
    "R4_OUTPUT_MANIFEST.tsv",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_tsv(path: Path):
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader), list(reader.fieldnames or [])


def write_tsv(path: Path, rows: list[dict], fields: list[str]):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def refresh_manifest(root: Path, artifact: str):
    path = root / "R4_OUTPUT_MANIFEST.tsv"
    rows, fields = read_tsv(path)
    target = root / artifact
    found = False
    for row in rows:
        if row["artifact"] == artifact:
            row["bytes"] = str(target.stat().st_size)
            row["sha256"] = sha256(target)
            found = True
    assert found
    write_tsv(path, rows, fields)


def clone_case(parent: Path, name: str) -> Path:
    root = parent / name
    root.mkdir()
    for file_name in FILES:
        shutil.copy2(HERE / file_name, root / file_name)
    return root


def mutate_relation(root: Path):
    path = root / "R4_RELATION_ATLAS.tsv"
    rows, fields = read_tsv(path)
    rows[0]["raw_rms_difference"] = str(float(rows[0]["raw_rms_difference"]) + 0.1)
    write_tsv(path, rows, fields); refresh_manifest(root, path.name)


def mutate_lag(root: Path):
    path = root / "R4_CROSS_LAG_ATLAS.npz"
    with np.load(path, allow_pickle=False) as handle:
        arrays = {key: handle[key].copy() for key in handle.files}
    arrays["raw_centered_cross_correlation"][0, 0] += 0.1
    np.savez_compressed(path, **arrays); refresh_manifest(root, path.name)


def mutate_cap(root: Path):
    path = root / "R4_CAP_COVARIANCE_ATLAS.tsv"
    rows, fields = read_tsv(path)
    rows[0]["difference_rms"] = str(float(rows[0]["difference_rms"]) + 0.1)
    write_tsv(path, rows, fields); refresh_manifest(root, path.name)


def mutate_summary(root: Path):
    path = root / "R4_SUMMARY.tsv"
    rows, fields = read_tsv(path)
    rows[0]["median"] = str(float(rows[0]["median"]) + 0.1)
    write_tsv(path, rows, fields); refresh_manifest(root, path.name)


def mutate_result(root: Path):
    path = root / "R4_RESULT.json"
    payload = json.loads(path.read_text())
    payload["relation_count"] += 1
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    refresh_manifest(root, path.name)


def main():
    cases = {
        "relation_descriptor": (mutate_relation, "relation 0/raw_rms_difference"),
        "cross_lag": (mutate_lag, "raw cross-lag replay mismatch"),
        "cap_descriptor": (mutate_cap, "difference_rms"),
        "summary": (mutate_summary, "summary"),
        "result_census": (mutate_result, "relation_count"),
    }
    results = {}
    with tempfile.TemporaryDirectory(prefix="udt_r4_catch_") as tmp_name:
        parent = Path(tmp_name)
        for name, (mutator, expected_text) in cases.items():
            root = clone_case(parent, name)
            mutator(root)
            command = [
                "python3", str(HERE / "verify_r4.py"),
                "--package-dir", str(root),
                "--r3-cells", str(CELL_ROOT),
                "--output", str(root / "verification.json"),
            ]
            completed = subprocess.run(command, text=True, capture_output=True, check=False)
            transcript = completed.stdout + completed.stderr
            if completed.returncode == 0 or expected_text not in transcript:
                raise AssertionError(
                    f"catch proof failed for {name}: rc={completed.returncode}, expected={expected_text!r}"
                )
            results[name] = {"returncode": completed.returncode, "caught_by": expected_text}
    payload = {"status": "PASS", "case_count": len(results), "cases": results}
    out = HERE / "R4_VERIFIER_CATCH_PROOF_RESULT.json"
    if out.exists():
        raise FileExistsError(out)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
