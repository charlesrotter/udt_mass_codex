#!/usr/bin/env python3
"""Certify G258 R1 exact historical-source resolution and scientific non-regression."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
PREREGISTRATION_COMMIT = "a9f96360"
EXPECTED_PREMISE_HASH = "83b00d923de6163fa17c6f336b73baa977f8588e6ab2fd98c57ce17e1e78f441"
SCIENTIFIC_HASHES = {
    "DERIVATION_RESULT.json": "f048aa41a51a652d910a85615db6b85dd32c5c05b7e24671824b322fefa81f0f",
    "NODE_ATLAS.tsv": "0bd9ed882d4dd457bfa610388c002548f99c4bda797998d0f261d43c779a57fb",
    "ADJACENT_CHANGE_ATLAS.tsv": "2829d5e7743cd6f742ed0e453a1d63a969c3e3f223b74ddc969324f8d7853137",
    "INDEPENDENT_VERIFICATION.json": "0531af669d4ec8e76a2184100a84b81235b53444a0dc2731f269679b1e45c67c",
    "CATCH_PROOF_RESULT.json": "4ea15776159277c682fc47064c51d954f548cf4fbfedad1b40c816056a5f20cb",
}


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def make_writable(root: Path) -> None:
    for path in root.rglob("*"):
        path.chmod(0o755 if path.is_dir() else 0o644)
    root.chmod(0o755)


def main() -> None:
    verifier_text = (ROOT / "verify_package.py").read_text()
    builder_text = (ROOT / "build_review_intake.py").read_text()
    forbidden = ('startswith("G258', "splitlines(keepends=True)")
    assert all(token not in verifier_text for token in forbidden)
    assert all(token not in builder_text for token in forbidden)

    current_source = REPO / "CURRENT_SCIENTIFIC_PREMISES.tsv"
    if sha256_path(current_source) == EXPECTED_PREMISE_HASH:
        historical = current_source.read_bytes()
    else:
        completed = subprocess.run(
            ["git", "show", f"{PREREGISTRATION_COMMIT}:CURRENT_SCIENTIFIC_PREMISES.tsv"],
            cwd=REPO,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        historical = completed.stdout
    assert sha256_bytes(historical) == EXPECTED_PREMISE_HASH

    for name, expected in SCIENTIFIC_HASHES.items():
        assert sha256_path(ROOT / name) == expected, name

    built = subprocess.run(
        [sys.executable, str(ROOT / "build_review_intake.py")],
        cwd=REPO,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    values = dict(line.split("=", 1) for line in built.stdout.splitlines() if "=" in line)
    intake = Path(values["INTAKE"])
    try:
        with (intake / "REVIEW_MANIFEST.tsv").open(newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        for row in rows:
            assert sha256_path(intake / row["path"]) == row["sha256"], row["path"]

        sealed_package = intake / ROOT.name
        strict = subprocess.run(
            [sys.executable, "verify_package.py"],
            cwd=sealed_package,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert strict.returncode == 0, strict.stderr

        make_writable(intake)
        premise = intake / "CURRENT_SCIENTIFIC_PREMISES.tsv"
        premise.write_bytes(premise.read_bytes() + b"\n")
        mutated = subprocess.run(
            [sys.executable, "verify_package.py"],
            cwd=sealed_package,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert mutated.returncode != 0
    finally:
        if intake.exists():
            make_writable(intake)
            shutil.rmtree(intake)

    followup = ROOT / "EXTERNAL_REPAIR_FOLLOWUP_GPT54.md"
    followup_status = (
        "ACCEPTED"
        if followup.is_file() and followup.read_text().startswith("REPAIRS_ACCEPTED\n")
        else "OPEN"
    )
    result = {
        "status": "PASS",
        "repair": "R1_EXACT_HISTORICAL_SOURCE_RESOLUTION",
        "historical_source_sha256": EXPECTED_PREMISE_HASH,
        "scientific_artifacts_byte_identical": len(SCIENTIFIC_HASHES),
        "sealed_manifest_strict": True,
        "one_byte_mutation_rejected": True,
        "row_synthesis_absent": True,
        "scientific_landing": "UNCHANGED",
        "external_repair_followup": followup_status,
    }
    (ROOT / "REPAIR_CERTIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS: G258 R1 exact historical source, strict seal, one-byte catch, 5 unchanged artifacts")


if __name__ == "__main__":
    main()
