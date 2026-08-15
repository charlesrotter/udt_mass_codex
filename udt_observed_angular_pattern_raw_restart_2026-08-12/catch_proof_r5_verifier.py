#!/usr/bin/env python3
"""Prove the R5 verifier catches mutations even after output-manifest refresh."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "R5_VERIFIER_CATCH_PROOF_RESULT.json"
FILES = (
    "R2_CURVE_ATLAS.tsv",
    "R4_RELATION_ATLAS.tsv",
    "R4_VERIFICATION_RESULT.json",
    "R3_OUTPUT_MANIFEST.tsv",
    "R5_VIEW_SPECTRA.tsv",
    "R5_RANKED_SUBSPACE_OVERLAPS.tsv",
    "R5_COVARIANCE_SUBSPACE_ATLAS.tsv",
    "R5_COVARIANCE_SUBSPACE_SUMMARY.tsv",
    "R5_RESULT.json",
    "R5_OUTPUT_MANIFEST.tsv",
    "verify_r5.py",
)


def digest(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def refresh_manifest(root: Path, artifact: str):
    path = root / "R5_OUTPUT_MANIFEST.tsv"
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    target = root / artifact
    found = False
    for row in rows:
        if row["artifact"] == artifact:
            row["bytes"] = str(target.stat().st_size)
            row["sha256"] = digest(target)
            found = True
    assert found
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["artifact", "bytes", "sha256"],
                                delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def mutate_first_tsv(path: Path, field: str, delta: float):
    temp = path.with_suffix(path.suffix + ".mut")
    with path.open(newline="") as source, temp.open("w", newline="") as target:
        reader = csv.DictReader(source, delimiter="\t")
        writer = csv.DictWriter(target, fieldnames=reader.fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        first = True
        for row in reader:
            if first:
                row[field] = repr(float(row[field]) + delta)
                first = False
            writer.writerow(row)
    assert not first
    os.replace(temp, path)


def run_case(root: Path, name: str, artifact: str, mutation):
    artifact_path = root / artifact
    backup = root / f".{artifact}.backup"
    manifest_backup = root / ".R5_OUTPUT_MANIFEST.tsv.backup"
    shutil.copy2(artifact_path, backup)
    shutil.copy2(root / "R5_OUTPUT_MANIFEST.tsv", manifest_backup)
    try:
        mutation(artifact_path)
        refresh_manifest(root, artifact)
        result = subprocess.run(
            [sys.executable, str(root / "verify_r5.py")],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=240,
        )
        if result.returncode == 0:
            raise AssertionError(f"mutation escaped verifier: {name}")
        tail = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else "nonzero return"
        return {"returncode": result.returncode, "caught_by": tail[:500]}
    finally:
        os.replace(backup, artifact_path)
        os.replace(manifest_backup, root / "R5_OUTPUT_MANIFEST.tsv")
        verification = root / "R5_VERIFICATION_RESULT.json"
        if verification.exists():
            verification.unlink()


def main():
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    with tempfile.TemporaryDirectory(prefix="r5_catch_") as temp_name:
        root = Path(temp_name)
        for name in FILES:
            shutil.copy2(HERE / name, root / name)
        cases = {
            "spectrum": run_case(
                root, "spectrum", "R5_VIEW_SPECTRA.tsv",
                lambda path: mutate_first_tsv(path, "singular_value", 0.1),
            ),
            "ranked_overlap": run_case(
                root, "ranked_overlap", "R5_RANKED_SUBSPACE_OVERLAPS.tsv",
                lambda path: mutate_first_tsv(path, "projector_overlap", 0.1),
            ),
            "covariance_subspace": run_case(
                root, "covariance_subspace", "R5_COVARIANCE_SUBSPACE_ATLAS.tsv",
                lambda path: mutate_first_tsv(path, "subspace_covariance_trace", 0.1),
            ),
            "summary": run_case(
                root, "summary", "R5_COVARIANCE_SUBSPACE_SUMMARY.tsv",
                lambda path: mutate_first_tsv(path, "median", 0.1),
            ),
            "result_census": run_case(
                root, "result_census", "R5_RESULT.json",
                lambda path: path.write_text(
                    json.dumps({**json.loads(path.read_text()), "view_spectrum_row_count": 2608},
                               indent=2, sort_keys=True) + "\n"
                ),
            ),
        }
    payload = {"status": "PASS", "case_count": len(cases), "cases": cases}
    temp = OUTPUT.with_suffix(".json.tmp")
    temp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temp, OUTPUT)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
