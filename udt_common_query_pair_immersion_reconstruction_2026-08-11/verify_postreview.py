#!/usr/bin/env python3
"""Fail-closed verification of the external-review adjudication layer."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SEALED_COMMIT = "7cce1745"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def verify_payload(payload: dict, source: str) -> None:
    require(payload["schema"] == "UDT_COMMON_QUERY_EXTERNAL_REVIEW_CLOSURE_V1", "wrong closure schema")
    require(payload["verdict"] == "VERIFIED_WITH_CAVEATS", "verdict was promoted or demoted")
    require("solve_common_query" not in source, "closure verifier imports production")
    require("verify_common_query_independent" not in source, "closure verifier imports prior verifier")
    require("LOOP_DIAGNOSTICS" not in source, "closure verifier reads production loop rows")
    require("orthogonal_polar" not in source, "closure verifier uses production polar projection")

    codazzi = payload["codazzi"]
    require(codazzi["status"] == "NUMERICALLY_UNRESOLVED", "Codazzi caveat was silently promoted")
    rows = codazzi["rows"]
    require([r["scale"] for r in rows] == [0.008, 0.004, 0.002, 0.001], "wrong Codazzi scale universe")
    require(all(r["classification_residual"] < 5e-6 for r in rows), "Codazzi residual exceeded bounded small-residual gate")
    require(max(r["formulation_disagreement"] for r in rows) < 1e-9, "Codazzi formulations disagree")
    tail = [rows[-2]["classification_residual"], rows[-1]["classification_residual"]]
    stable = tail[0] / max(tail[1], 1e-30) >= 1.5 or max(tail) / max(min(tail), 1e-30) <= 1.5
    require(not stable, "saved Codazzi status contradicts preregistered stability gate")
    require(abs(rows[-1]["classification_residual"] - codazzi["curvature_step_control"]["classification_residual"]) < 2e-6,
            "Codazzi curvature-step control failed")

    loop = payload["normal_loop"]
    require(loop["status"] == "INDEPENDENTLY_REGENERATED", "normal loop was not independently regenerated")
    require(loop["quadrature_32_64"] < 1e-8, "normal loop quadrature gate failed")
    require(loop["loop_norm_64"] > 1e-7, "normal loop became numerically trivial")
    require(loop["generator_relative_difference"] < 2e-3, "loop/generator gate failed")
    require(loop["production_relative_difference"] < 2e-3, "independent/production loop gate failed")
    U = np_array(loop["loop_matrices"]["64"])
    loop_norm = matrix_norm(U - np_eye(2))
    require(abs(loop_norm - loop["loop_norm_64"]) < 1e-15, "reported loop norm does not match raw matrix")


def np_array(value):
    import numpy as np
    return np.array(value, dtype=float)


def np_eye(size: int):
    import numpy as np
    return np.eye(size)


def matrix_norm(value) -> float:
    import numpy as np
    return float(np.linalg.norm(value))


def verify_sealed_manifest() -> int:
    rows = list(csv.DictReader((HERE / "REVIEW_MANIFEST.tsv").open(), delimiter="\t"))
    require(len(rows) == 37, "sealed review manifest row count changed")
    for row in rows:
        data = subprocess.check_output(["git", "show", f"{SEALED_COMMIT}:{row['path']}"], cwd=REPO)
        require(sha256_bytes(data) == row["sha256"], f"sealed hash mismatch at {row['path']}")
    return len(rows)


def verify_postreview_manifest() -> int:
    manifest_path = HERE / "POSTREVIEW_MANIFEST.tsv"
    require(manifest_path.is_file(), "post-review manifest missing")
    rows = list(csv.DictReader(manifest_path.open(), delimiter="\t"))
    excluded = {manifest_path.name, "POSTREVIEW_VERIFICATION.json"}
    expected = sorted(p for p in HERE.iterdir() if p.is_file() and p.name not in excluded)
    require([r["path"] for r in rows] == [str(p.relative_to(REPO)) for p in expected],
            "post-review manifest path universe mismatch")
    for row, path in zip(rows, expected):
        require(sha256(path) == row["sha256"], f"post-review hash mismatch at {row['path']}")
    return len(rows)


def catch_proofs(payload: dict, source: str) -> dict:
    results = {}

    promoted = copy.deepcopy(payload)
    promoted["codazzi"]["status"] = "INDEPENDENTLY_CERTIFIED"
    try:
        verify_payload(promoted, source)
        results["codazzi_promotion"] = "FAILED_TO_REJECT"
    except AssertionError:
        results["codazzi_promotion"] = "REJECTED"

    changed_loop = copy.deepcopy(payload)
    changed_loop["normal_loop"]["loop_norm_64"] *= 1.1
    try:
        verify_payload(changed_loop, source)
        results["loop_norm_mutation"] = "FAILED_TO_REJECT"
    except AssertionError:
        results["loop_norm_mutation"] = "REJECTED"

    lost_loop = copy.deepcopy(payload)
    lost_loop["normal_loop"]["status"] = "NUMERICALLY_UNRESOLVED"
    try:
        verify_payload(lost_loop, source)
        results["lost_independent_loop"] = "FAILED_TO_REJECT"
    except AssertionError:
        results["lost_independent_loop"] = "REJECTED"

    contaminated = source + "\nimport solve_common_query\n"
    try:
        verify_payload(payload, contaminated)
        results["production_import"] = "FAILED_TO_REJECT"
    except AssertionError:
        results["production_import"] = "REJECTED"

    require(set(results.values()) == {"REJECTED"}, "one or more catch proofs failed")
    return results


def main() -> None:
    payload = json.loads((HERE / "EXTERNAL_REVIEW_CLOSURE_VERIFICATION.json").read_text())
    source = (HERE / "verify_external_review_closure.py").read_text()
    verify_payload(payload, source)
    sealed_rows = verify_sealed_manifest()
    catches = catch_proofs(payload, source)
    review = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text()
    require(review.startswith("VERIFIED_WITH_CAVEATS"), "external verdict missing")
    report = (HERE / "AUDIT_REPORT.md").read_text()
    require("EXTERNALLY REVIEWED — VERIFIED WITH CAVEATS" in report, "audit report not adjudicated")
    require("NUMERICALLY_UNRESOLVED" in report, "Codazzi caveat missing from report")
    result = {
        "schema": "UDT_COMMON_QUERY_POSTREVIEW_VERIFICATION_V1",
        "status": "PASS",
        "sealed_manifest_rows_replayed_at_commit": sealed_rows,
        "sealed_commit": SEALED_COMMIT,
        "external_verdict": "VERIFIED_WITH_CAVEATS",
        "landing": "QUERY_CLASS_DEPENDENT_CHANNEL_ARCHITECTURE",
        "q2_codazzi": "NUMERICALLY_UNRESOLVED",
        "q2_normal_loop": "INDEPENDENTLY_REGENERATED",
        "catch_proofs": catches,
        "hashes": {
            "closure_script": sha256(HERE / "verify_external_review_closure.py"),
            "closure_result": sha256(HERE / "EXTERNAL_REVIEW_CLOSURE_VERIFICATION.json"),
            "sealed_review_manifest": sha256(HERE / "REVIEW_MANIFEST.tsv"),
        },
    }
    (HERE / "POSTREVIEW_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    result["postreview_manifest_rows"] = verify_postreview_manifest()
    (HERE / "POSTREVIEW_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
