#!/usr/bin/env python3
"""Fail-closed verifier for the complete local G69 package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def verify() -> dict[str, bool]:
    source = rows(HERE / "SOURCE_MANIFEST.tsv")
    cell = rows(HERE / "CELL_ATLAS.tsv")
    sensitivity = rows(HERE / "SENSITIVITY_ATLAS.tsv")
    covariance = rows(HERE / "SOURCE_DEGENERACY_ATLAS.tsv")
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
    anchor = (HERE / "OBSERVATIONAL_ANCHOR_POLICY.md").read_text(encoding="utf-8")
    builder = (HERE / "derive_identifiability_atlas.py").read_text(encoding="utf-8")
    checks = {
        "source_hashes": len(source) == 8 and all(digest(ROOT / row["path"]) == row["sha256"] for row in source),
        "cell_census": len(cell) == 315 and len({(r["profile_id"], r["endpoint_x"]) for r in cell}) == 315,
        "profile_endpoint_census": len({r["profile_id"] for r in cell}) == 21 and len({r["endpoint_x"] for r in cell}) == 15,
        "endpoint_regression": max(float(r["x1_official_relative"]) for r in cell if r["endpoint_x"] == "1.0") <= 2e-8,
        "F01_identity": max(float(r["anisotropy_log"]) for r in cell if r["family"] == "F01") <= 2e-10 and max(abs(float(r["polar_rotation"])) for r in cell if r["family"] == "F01") <= 2e-10,
        "regular_maps": min(float(r["sigma_min"]) for r in cell) > 0.0,
        "sensitivity_census": len(sensitivity) == 15 and all(r["classification"] == "FULL_RANK_OBSERVED" for r in sensitivity),
        "sensitivity_scope": "often poorly conditioned" in report and "neither a global injectivity theorem" in exact,
        "covariance_census": len(covariance) == 945,
        "covariance_gate": max(float(r["reconstruction_relative"]) for r in covariance) <= 2e-10 and min(float(r["source_min_eigenvalue"]) for r in covariance) > 0.0,
        "independent_route": independent["status"] == "PASS" and not independent["imports_production_builder"] and independent["new_ODE_solves"] == 0,
        "landing": result["primary_landing"] == "GEOMETRICALLY_SEPARATING__OBSERVATIONALLY_SOURCE_DEGENERATE",
        "no_anchor_or_solve": result["observational_anchors_used"] == 0 and result["new_ODE_solves"] == 0 and "solve_ivp" not in builder,
        "channel_scope": "scalar TT readout does not" in exact and "does not prove that full CMB data" in report,
        "anchor_policy": "held-out" in anchor and "do not add coefficients" in anchor and "none is used in\nG69" in anchor,
        "lay_scope": "original picture" in lay and "cannot identify it" in lay,
        "external_status_honest": "EXTERNAL_REVIEW_PENDING" in report,
    }
    return checks


def main() -> None:
    checks = verify()
    payload = {"schema": "udt-cmb-g69-package-v1", "checks": checks, "passed": sum(checks.values()), "total": len(checks)}
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    (HERE / "PACKAGE_VERIFICATION_STDOUT.txt").write_text(text, encoding="utf-8")
    print(text, end="")
    assert all(checks.values()), [key for key, value in checks.items() if not value]


if __name__ == "__main__":
    main()
