#!/usr/bin/env python3
"""Build and optionally materialize the sealed G79 review intake."""

from __future__ import annotations

import argparse
import csv
import hashlib
import shutil
import subprocess
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "26f90fc22271c682fe00ef350eac01b3113a5b9e"
PACKAGE_FILES = (
    "AUDIT_REPORT.md", "CATCH_PROOF_RESULTS.json", "DERIVATION_RESULT.json",
    "EXACT_DERIVATION.md", "INDEPENDENT_VERIFICATION.json", "LAY_REPORT.md",
    "PACKAGE_VERIFICATION.json", "PATH_EVIDENCE.npz", "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md", "REFINEMENT_ATLAS.tsv", "REVIEW_DISPATCH.md",
    "SOURCE_MANIFEST.tsv", "THERMAL_READOUT_LEDGER.tsv", "TYPE_LEDGER.tsv",
    "build_review_manifest.py", "derive_same_geometry_sne_query.py",
    "run_catch_proofs.py", "verify_package.py", "verify_same_geometry_sne_independent.py",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def frozen(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)


def rows() -> tuple[list[tuple[str, str, str]], dict[str, bytes]]:
    output: list[tuple[str, str, str]] = []
    payload: dict[str, bytes] = {}
    for name in PACKAGE_FILES:
        path = HERE / name
        assert path.is_file(), name
        relative = str(path.relative_to(ROOT))
        data = path.read_bytes()
        output.append((relative, digest(data), "G79_package"))
        payload[relative] = data
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        sources = list(csv.DictReader(stream, delimiter="\t"))
    assert len(sources) == 16
    for row in sources:
        data = frozen(row["path"])
        assert digest(data) == row["sha256"]
        output.append((row["path"], row["sha256"], f"source_{row['role']}"))
        payload[row["path"]] = data
    assert len(output) == len({item[0] for item in output}) == 36
    return output, payload


def write_manifest(output: list[tuple[str, str, str]], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "role"))
        writer.writerows(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seal", action="store_true")
    args = parser.parse_args()
    output, payload = rows()
    write_manifest(output, HERE / "REVIEW_MANIFEST.tsv")
    print("PASS: 36 unique G79 payload files; sealed intake count including manifest = 37")
    if args.seal:
        destination = Path(tempfile.mkdtemp(prefix="udt_g79_review_", dir="/tmp"))
        for relative, data in payload.items():
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        shutil.copy2(HERE / "REVIEW_MANIFEST.tsv", destination / "REVIEW_MANIFEST.tsv")
        for relative, expected, _ in output:
            assert digest((destination / relative).read_bytes()) == expected
        print(f"SEALED_INTAKE={destination}")


if __name__ == "__main__":
    main()

