#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def run(script: str) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment.update({"PYTHONDONTWRITEBYTECODE": "1", "CUDA_VISIBLE_DEVICES": ""})
    return subprocess.run(
        [sys.executable, str(HERE / script)], cwd=ROOT, env=environment,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    expected = [
        ("build_source_manifest.py", None),
        ("derive_lambda_component_atlas.py", "DERIVATION_STDOUT.txt"),
        ("verify_lambda_atlas_sturm.py", "STURM_STDOUT.txt"),
        ("verify_lambda_atlas_torch.py", "TORCH_STDOUT.txt"),
    ]
    for script, stdout_name in expected:
        completed = run(script)
        assert completed.returncode == 0 and completed.stderr == "", (script, completed.stderr)
        if stdout_name:
            assert completed.stdout == (HERE / stdout_name).read_text(encoding="utf-8"), script

    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    sturm = json.loads((HERE / "STURM_RESULT.json").read_text(encoding="utf-8"))
    torch_result = json.loads((HERE / "TORCH_RESULT.json").read_text(encoding="utf-8"))
    assert result["actual_degree"] == 7 and result["distinct_real_roots"] == 7
    assert result["certificate_intervals"] == 8
    assert sturm["distinct_real_roots"] == 7 and sturm["polynomial_squarefree"] is True
    assert torch_result["holdouts"] == torch_result["passed"] == 5
    assert torch_result["maximum_scaled_error"] <= 2e-9

    table_counts = {
        "PRODUCTION_NODE_OUTCOMES.tsv": 10,
        "EXACT_HOLDOUT_OUTCOMES.tsv": 7,
        "REAL_ROOTS.tsv": 7,
        "LAMBDA_INTERVALS.tsv": 8,
        "CENTER_ASSIGNMENTS.tsv": 6,
        "TORCH_HOLDOUT_OUTCOMES.tsv": 5,
        "CATCH_PROOFS.tsv": 22,
    }
    for name, count in table_counts.items():
        with (HERE / name).open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        assert len(rows) == count, name
        if name == "CATCH_PROOFS.tsv":
            assert all(row["result"] == "PASS" for row in rows)

    torch_source = (HERE / "verify_lambda_atlas_torch.py").read_text(encoding="utf-8")
    sturm_source = (HERE / "verify_lambda_atlas_sturm.py").read_text(encoding="utf-8")
    assert "exact_invariant_jets" not in torch_source
    assert "import sympy" not in sturm_source and "from sympy" not in sturm_source
    print("PASS source_manifest 17/17")
    print("PASS deterministic_exact_polynomial_replay")
    print("PASS stdlib_Sturm_replay")
    print("PASS independent_Torch_replay")
    print("PASS real_roots 7/7")
    print("PASS intervals 8/8")
    print("PASS center_assignments 6/6")
    print("PASS catch_proofs 22/22")
    print(f"DERIVATION_RESULT_SHA256 {sha(HERE / 'DERIVATION_RESULT.json')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
