#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def run(script: str) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, str(HERE / script)],
        cwd=ROOT,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    source = run("build_source_manifest.py")
    assert source.returncode == 0 and source.stderr == "", source.stderr
    production = run("derive_deformation_neighborhood.py")
    assert production.returncode == 0 and production.stderr == "", production.stderr
    independent = run("verify_deformation_neighborhood_independent.py")
    assert independent.returncode == 0 and independent.stderr == "", independent.stderr
    assert production.stdout == (HERE / "DERIVATION_STDOUT.txt").read_text(encoding="utf-8")
    assert independent.stdout == (HERE / "INDEPENDENT_STDOUT.txt").read_text(encoding="utf-8")

    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert result["base_count"] == 6
    assert result["axis_ids"] == [f"A0{i}" for i in range(1, 7)]
    assert result["stratum_ids"] == [f"S0{i}" for i in range(1, 8)]
    assert result["all_gate_open_neighborhoods"] is True
    assert result["explicit_joint_radius_certified"] is False

    with (HERE / "OPENNESS_GATE_OUTCOMES.tsv").open(newline="", encoding="utf-8") as handle:
        open_rows = list(csv.DictReader(handle, delimiter="\t"))
    with (HERE / "DEFORMATION_AXIS_OUTCOMES.tsv").open(newline="", encoding="utf-8") as handle:
        axis_rows = list(csv.DictReader(handle, delimiter="\t"))
    with (HERE / "DEGENERATION_STRATUM_OUTCOMES.tsv").open(newline="", encoding="utf-8") as handle:
        stratum_rows = list(csv.DictReader(handle, delimiter="\t"))
    with (HERE / "CATCH_PROOFS.tsv").open(newline="", encoding="utf-8") as handle:
        catches = list(csv.DictReader(handle, delimiter="\t"))
    assert len(open_rows) == 6 and all(row["status"] == "OPEN_AROUND_ALL_SIX_BASES" for row in open_rows)
    assert [row["axis_id"] for row in axis_rows] == [f"A0{i}" for i in range(1, 7)]
    assert [row["stratum_id"] for row in stratum_rows] == [f"S0{i}" for i in range(1, 8)]
    assert len(catches) == 22 and all(row["result"] == "PASS" for row in catches)

    verifier_source = (HERE / "verify_deformation_neighborhood_independent.py").read_text(encoding="utf-8")
    forbidden_import = re.compile(
        r"^\s*(?:import\s+derive_deformation_neighborhood\b|"
        r"from\s+derive_deformation_neighborhood\s+import\b)",
        re.MULTILINE,
    )
    assert forbidden_import.search(verifier_source) is None
    print("PASS source_manifest 17/17")
    print("PASS deterministic_production_replay")
    print("PASS independent_replay")
    print("PASS all_gate_open_centers 6/6")
    print("PASS deformation_axes 6/6")
    print("PASS degeneration_strata 7/7")
    print("PASS catch_proofs 22/22")
    print(f"DERIVATION_RESULT_SHA256 {sha(HERE / 'DERIVATION_RESULT.json')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
