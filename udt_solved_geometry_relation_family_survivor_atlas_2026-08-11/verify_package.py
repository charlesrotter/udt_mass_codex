#!/usr/bin/env python3
"""Read-only final verifier for the solved-geometry survivor-atlas package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def table(name):
    return list(csv.DictReader((HERE / name).open(), delimiter="\t"))


def digest(name):
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


required = {
    "PREREGISTRATION.md", "PONDER_MAP.md", "PREMISE_LEDGER.tsv", "SOLVER_COMPLETENESS_MAP.md",
    "SURVIVOR_AXES.tsv", "WITNESS_UNIVERSE.tsv", "FALSIFICATION_CONTRACT.tsv",
    "SOURCE_MANIFEST.tsv", "NUMERICAL_CONTRACT.md", "NUMERICAL_SAMPLE_UNIVERSE.tsv",
    "solve_survivor_atlas.py", "SOLVED_GEOMETRY_ATLAS.tsv", "GEODESIC_DIAGNOSTICS.tsv",
    "PATH_DIAGNOSTICS.tsv", "DERIVATION_RESULT.json", "verify_survivor_atlas_independent.py",
    "INDEPENDENT_COMPARISON.tsv", "INDEPENDENT_VERIFICATION.json", "run_catch_proofs.py",
    "CATCH_PROOF_RESULTS.tsv", "CATCH_PROOF_RESULT.json", "SURVIVOR_CLASSIFICATION.tsv",
    "EXACT_METHOD_AND_LIMITS.md", "AUDIT_REPORT.md", "NEXT_STEP.md",
}
assert all((HERE / name).is_file() for name in required), sorted(name for name in required if not (HERE/name).is_file())

# Freeze and verify cited sources.
sources = table("SOURCE_MANIFEST.tsv")
assert len(sources) == len({r["path"] for r in sources}) == 22
for row in sources:
    p = ROOT / row["path"]
    assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == row["sha256"], row["path"]
    assert "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02" not in row["path"]
    assert "udt_native_onshell_timelive_reset_owner_audit_2026-08-10" not in row["path"]

samples = table("NUMERICAL_SAMPLE_UNIVERSE.tsv")
atlas = table("SOLVED_GEOMETRY_ATLAS.tsv")
geo = table("GEODESIC_DIAGNOSTICS.tsv")
paths = table("PATH_DIAGNOSTICS.tsv")
classes = table("SURVIVOR_CLASSIFICATION.tsv")
indep_rows = table("INDEPENDENT_COMPARISON.tsv")
assert (len(samples), len(atlas), len(geo), len(paths), len(classes), len(indep_rows)) == (14,14,28,28,7,56)
assert len({r["sample_id"] for r in samples}) == 14
assert all(r["endpoint_family"] == "REGULAR" for r in atlas)
assert all(r["classification"] == "REGULAR_PROPAGATOR" for r in geo)
assert all(r["classification"] == "NONIDENTITY" for r in paths)
assert all(r["pass"] == "TRUE" for r in indep_rows)

deriv = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
indep = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
catch = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
assert deriv["counts"] == {"samples":14,"geodesics":28,"paths":28}
assert deriv["scope"] == "bounded_metric_geometry_not_physical_stability"
assert indep["status"] == "PASS" and indep["checks"] == indep["pass_count"] == 56
assert catch["status"] == "PASS" and catch["tests"] == catch["passed"] == 23
assert all(digest(name) == value for name,value in indep["production_hashes"].items())
assert indep["maxima"]["geodesic_endpoint_diff"] <= 2e-4
assert indep["maxima"]["holonomy_matrix_diff"] <= 3e-4
assert indep["maxima"]["normal_angle_diff"] <= 3e-4

report = (HERE / "AUDIT_REPORT.md").read_text()
for required_text in (
    "MULTIPLE_GEOMETRIC_SURVIVOR_FAMILIES", "14/14", "28/28", "18/18", "56/56",
    "geometric persistence, not physical or dynamical stability", "not a universal selection",
):
    assert required_text in report, required_text
for forbidden in ("unique physical branch", "dynamically stable branch", "complete UDT solution space"):
    assert forbidden not in report.lower(), forbidden

summary = {
    "status":"PASS",
    "sources":22,
    "samples":14,
    "geodesics":28,
    "paths":28,
    "independent_checks":56,
    "catch_proofs":23,
    "landing":"MULTIPLE_GEOMETRIC_SURVIVOR_FAMILIES",
    "key_hashes":{
        "atlas":digest("SOLVED_GEOMETRY_ATLAS.tsv"),
        "geodesics":digest("GEODESIC_DIAGNOSTICS.tsv"),
        "paths":digest("PATH_DIAGNOSTICS.tsv"),
        "independent":digest("INDEPENDENT_VERIFICATION.json"),
    },
}
print(json.dumps(summary, indent=2, sort_keys=True))
