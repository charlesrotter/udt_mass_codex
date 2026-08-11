#!/usr/bin/env python3
"""Fail-closed verifier for the common-query reconstruction package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    return list(csv.DictReader(path.open(), delimiter="\t"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def decreasing(values: list[float], minimum_ratio: float) -> bool:
    return all(a / b >= minimum_ratio for a, b in zip(values[:-1], values[1:]))


def verify(repo: Path, package: Path) -> dict:
    required = [
        "PREREGISTRATION.md", "PERFORMANCE_REFINEMENT_PREREGISTRATION.md",
        "IMPLEMENTATION_CORRECTION_PREREGISTRATION.md", "INDEPENDENT_VERIFIER_PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv", "FALSIFICATION_CONTRACT.tsv", "SOURCE_MANIFEST.tsv",
        "solve_common_query.py", "SCALE_DIAGNOSTICS.tsv", "LOOP_DIAGNOSTICS.tsv",
        "DERIVATION_RESULT.json", "verify_common_query_independent.py", "INDEPENDENT_VERIFICATION.json",
        "FIRST_PRODUCTION_SCALE_DIAGNOSTICS.tsv", "FIRST_PRODUCTION_LOOP_DIAGNOSTICS.tsv",
        "FIRST_PRODUCTION_DERIVATION_RESULT.json", "EXACT_DERIVATION.md", "PREMISE_AUDIT.md", "AUDIT_REPORT.md",
    ]
    for name in required:
        require((package / name).is_file(), f"missing required file {name}")

    manifest = read_tsv(package / "SOURCE_MANIFEST.tsv")
    require(len(manifest) == 12, "source manifest must retain exact 12 frozen rows")
    for row in manifest:
        path = repo / row["path"]
        require(path.is_file(), f"missing frozen source {row['path']}")
        require(sha256(path) == row["sha256"], f"frozen source hash mismatch {row['path']}")

    result = json.loads((package / "DERIVATION_RESULT.json").read_text())
    require(result["schema"] == "UDT_COMMON_QUERY_PAIR_IMMERSION_V1", "wrong production schema")
    require(result["counts"] == {"loop_rows": 6, "scale_rows": 6}, "wrong production counts")
    require(result["queries"] == ["Q1_R17_LEAF", "Q2_TL_FERMI"], "wrong frozen query universe")
    require(result["scales"] == [0.004, 0.002, 0.001], "wrong scale universe")
    require(result["loop_halfwidths"] == [0.04, 0.02, 0.01], "wrong loop universe")
    require(result["source_liveness"]["field_count"] == 11, "wrong time-live field count")
    require(result["source_liveness"]["nonzero_gradient_fields"] == 11, "a time-live field was frozen")

    scale_rows = read_tsv(package / "SCALE_DIAGNOSTICS.tsv")
    loop_rows = read_tsv(package / "LOOP_DIAGNOSTICS.tsv")
    require(len(scale_rows) == 6 and len(loop_rows) == 6, "missing or duplicate production rows")
    require({r["query_id"] for r in scale_rows} == {"Q1_R17_LEAF", "Q2_TL_FERMI"}, "scale query mismatch")
    require({r["query_id"] for r in loop_rows} == {"Q1_R17_LEAF", "Q2_TL_FERMI"}, "loop query mismatch")
    require(all(r["regular"] == "True" for r in scale_rows), "a registered pair became nonregular")
    require(max(float(r["h_reconstruction_residual"]) for r in scale_rows) < 1e-12, "pair reconstruction failed")

    grouped_scale = {q: sorted((r for r in scale_rows if r["query_id"] == q), key=lambda r: -float(r["scale"])) for q in ("Q1_R17_LEAF", "Q2_TL_FERMI")}
    r17 = grouped_scale["Q1_R17_LEAF"]
    tl = grouped_scale["Q2_TL_FERMI"]
    require(all(r["jacobi_status"] == "NOT_OWNED_BY_QUERY" and r["jacobi_residual"] == "NA" for r in r17), "Q1 Jacobi ownership regression")
    require(all(r["jacobi_status"] == "QUERY_OWNED_GEODESIC_VARIATION" for r in tl), "Q2 Jacobi ownership regression")
    require(float(r17[0]["s_ruling_acceleration_norm"]) > 1e-4, "Q1 ruling was silently treated as geodesic")
    require(float(tl[0]["s_ruling_acceleration_norm"]) < 1e-6, "Q2 Fermi ruling is not geodesic within tolerance")
    for field in ("gauss_residual", "codazzi_residual", "ricci_residual"):
        require(decreasing([float(r[field]) for r in r17], 3.0), f"Q1 {field} does not converge")
    require(decreasing([float(r["gauss_residual"]) for r in tl], 2.0), "Q2 Gauss does not converge")
    require(decreasing([float(r["ricci_residual"]) for r in tl], 3.0), "Q2 Ricci does not converge")
    for row in tl:
        scale = max(float(row["jacobi_second_derivative_norm"]), float(row["jacobi_curvature_norm"]))
        require(float(row["jacobi_residual"]) / scale < 5e-6, "Q2 Jacobi balance too large")

    grouped_loop = {q: sorted((r for r in loop_rows if r["query_id"] == q), key=lambda r: -float(r["halfwidth"])) for q in ("Q1_R17_LEAF", "Q2_TL_FERMI")}
    for query, rows in grouped_loop.items():
        require(decreasing([float(r["ambient_quadrature_8_16"]) for r in rows], 3.0), f"{query} ambient quadrature does not converge")
        require(decreasing([float(r["normal_quadrature_8_16"]) for r in rows], 2.0), f"{query} normal quadrature does not converge")
        require(decreasing([float(r["normal_curvature_residual"]) for r in rows], 3.0), f"{query} normal loop/curvature limit does not converge")
        require(decreasing([float(r["ambient_curvature_residual"]) for r in rows], 1.8), f"{query} ambient loop/curvature limit does not converge")
        require(max(float(r["ambient_metric_defect"]) for r in rows) < 1e-8, f"{query} ambient transport metric defect")

    independent_source = (package / "verify_common_query_independent.py").read_text()
    require("solve_common_query" not in independent_source, "independent verifier imports production")
    independent = json.loads((package / "INDEPENDENT_VERIFICATION.json").read_text())
    require(independent["verdict"] == "VERIFIED_WITH_CAVEATS", "independent verdict mismatch")
    require(independent["passed_gate_count"] == independent["total_gate_count"] == 16, "independent gates incomplete")

    report = (package / "AUDIT_REPORT.md").read_text()
    require("QUERY_CLASS_DEPENDENT_CHANNEL_ARCHITECTURE" in report, "landing missing")
    require("Q2 Codazzi" in report and "NUMERICALLY_UNRESOLVED" in report, "Q2 Codazzi caveat missing")
    require("selects no physical query" in (package / "EXACT_DERIVATION.md").read_text(), "scope guard missing")

    return {
        "schema": "UDT_COMMON_QUERY_FINAL_VERIFICATION_V1",
        "status": "PASS",
        "production_scale_rows": len(scale_rows),
        "production_loop_rows": len(loop_rows),
        "independent_gates": "16/16",
        "q2_codazzi": "NUMERICALLY_UNRESOLVED",
        "landing": "QUERY_CLASS_DEPENDENT_CHANNEL_ARCHITECTURE",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=HERE.parent)
    parser.add_argument("--package-dir", type=Path, default=HERE)
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()
    output = verify(args.repo_root.resolve(), args.package_dir.resolve())
    if args.write_result:
        (args.package_dir / "FINAL_VERIFICATION.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
