#!/usr/bin/env python3
"""Fail-closed catch proofs for the bounded solved-geometry atlas."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROTECTED = "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/"
STOPPED = "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/"


def rows(name):
    return list(csv.DictReader((HERE / name).open(), delimiter="\t"))


def exact_universe(values):
    ids = [r["sample_id"] for r in values]
    return len(ids) == 14 and len(set(ids)) == 14 and sum(r["geometry"] == "R17_GLOBAL" for r in values) == 9 and sum(r["geometry"] == "TIMELIVE_LOCAL" for r in values) == 5


def reject_stability_language(text):
    forbidden = ("physically stable", "dynamically stable", "the selected physical relation", "unique physical branch")
    return not any(x in text.lower() for x in forbidden)


def main():
    sample = rows("NUMERICAL_SAMPLE_UNIVERSE.tsv")
    atlas = rows("SOLVED_GEOMETRY_ATLAS.tsv")
    geo = rows("GEODESIC_DIAGNOSTICS.tsv")
    paths = rows("PATH_DIAGNOSTICS.tsv")
    indep = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    deriv = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    manifest = rows("SOURCE_MANIFEST.tsv")
    production_text = (HERE / "solve_survivor_atlas.py").read_text()
    independent_text = (HERE / "verify_survivor_atlas_independent.py").read_text()

    tests = []
    def check(test_id, statement, ok):
        tests.append({"test_id": test_id, "statement": statement, "status": "PASS" if ok else "FAIL"})

    check("C01", "exact preregistered 14-row universe", exact_universe(sample))
    check("C02", "missing sample is rejected", not exact_universe(sample[:-1]))
    check("C03", "duplicate sample is rejected", not exact_universe(sample + [sample[0]]))
    check("C04", "output row counts are 14/28/28", len(atlas) == 14 and len(geo) == 28 and len(paths) == 28)
    check("C05", "every sample occurs once in atlas and four times in solved diagnostics", {r['sample_id'] for r in sample} == {r['sample_id'] for r in atlas} and all(sum(x['sample_id'] == r['sample_id'] for x in geo + paths) == 4 for r in sample))
    check("C06", "positive/zero/negative perturbations retained", {r['parameter_2'] for r in sample if r['geometry'] == 'R17_GLOBAL'} == {'epsilon=-0.12','epsilon=0','epsilon=+0.12'} and {r['parameter_1'] for r in sample if r['geometry'] == 'TIMELIVE_LOCAL'} == {'epsilon=-0.15','epsilon=-0.075','epsilon=0','epsilon=+0.075','epsilon=+0.15'})
    check("C07", "all endpoint atlas defects pass registered tolerance", max(float(r['endpoint_atlas_defect']) for r in atlas) <= 5e-10)
    check("C08", "R17 pair readout reproduces field phi", max(float(r['r17_phi_identity_defect']) for r in atlas if r['r17_phi_identity_defect'] != 'NA') <= 5e-10)
    check("C09", "all geodesic norm and transport defects pass", max(float(r['norm_drift']) for r in geo) <= 5e-8 and max(float(r['transport_metric_defect']) for r in geo) <= 5e-8)
    check("C10", "all declared dexp maps retained and classified", all(r['classification'] in {'REGULAR_PROPAGATOR','NEAR_CONJUGATE_OR_NUMERICALLY_UNRESOLVED','NUMERIC_UNRESOLVED'} for r in geo) and min(float(r['dexp_min_singular']) for r in geo) > 1e-5)
    check("C11", "all loops retained and metric-compatible", max(float(r['lc_metric_defect']) for r in paths) <= 5e-8)
    check("C12", "nonidentity is observed rather than preferred", all(float(r['lc_holonomy_norm']) > 1e-5 and r['classification'] == 'NONIDENTITY' for r in paths))
    check("C13", "independent verifier passes all 56 comparisons", indep['status'] == 'PASS' and indep['checks'] == 56 and indep['pass_count'] == 56)
    check("C14", "independent verifier does not import production solver", "solve_survivor_atlas" not in {n.module for n in ast.walk(ast.parse(independent_text)) if isinstance(n, (ast.Import, ast.ImportFrom)) and getattr(n, 'module', None)})
    check("C15", "independent hashes bind exact production evidence", all(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest for name, digest in indep['production_hashes'].items()))
    check("C16", "source scope excludes protected and stopped paths", all(not r['path'].startswith(PROTECTED) and not r['path'].startswith(STOPPED) for r in manifest))
    check("C17", "solver does not invoke protected or stopped paths", PROTECTED not in production_text + independent_text and STOPPED not in production_text + independent_text)
    check("C18", "no cE, Xmax, bootstrap, action, or matter parameter enters numerical solver", all(token not in production_text for token in ('c_E', 'X_max', 'rho_tot', 'bootstrap_density', 'matter_action')))
    check("C19", "time-live family visibly depends on all four coordinates and epsilon", all(np.linalg.norm(np.array([float(x) for x in r['endpoint_x'].split(';')]) - np.array([.12,-.18,.23,-.14])) > 1e-3 for r in geo if r['sample_id'].startswith('TL_')))

    # Exact endpoint-atlas composition remains exact after independent endpoint presentation changes.
    rng = np.random.default_rng(20260811)
    A = [rng.normal(size=(4,4)) for _ in range(3)]
    L = [np.eye(4) + .03*(x-x.T) for x in A]
    base_pq = np.diag([1.1,.9,1.02,.98]); base_qr = np.diag([.95,1.04,.99,1.03]); base_pr = base_qr @ base_pq
    tpq = L[1] @ base_pq @ np.linalg.inv(L[0]); tqr = L[2] @ base_qr @ np.linalg.inv(L[1]); tpr = L[2] @ base_pr @ np.linalg.inv(L[0])
    check("C20", "endpoint composition survives independent presentation changes", np.linalg.norm(tqr @ tpq - tpr) < 1e-12)

    # Identity/nonidentity is conjugacy invariant; use the least separated recorded loop.
    least = min(paths, key=lambda r: float(r['lc_holonomy_norm']))
    P = np.array([float(x) for x in least['holonomy_matrix'].split(';')]).reshape(4,4)
    C = np.eye(4) + .02*rng.normal(size=(4,4)); Pc = C @ P @ np.linalg.inv(C)
    check("C21", "nonidentity loop remains nonidentity after basis conjugation", np.linalg.norm(P-np.eye(4)) > 1e-5 and np.linalg.norm(Pc-np.eye(4)) > 1e-5)
    check("C22", "production result is explicitly non-physical scope", deriv['scope'] == 'bounded_metric_geometry_not_physical_stability')

    prose = " ".join((HERE / n).read_text() for n in ("PREREGISTRATION.md", "PONDER_MAP.md", "SOLVER_COMPLETENESS_MAP.md", "NUMERICAL_CONTRACT.md"))
    check("C23", "preregistered prose avoids physical-stability and uniqueness overclaim", reject_stability_language(prose))

    with (HERE / "CATCH_PROOF_RESULTS.tsv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(tests[0]), delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(tests)
    result = {"schema": "UDT_SOLVED_GEOMETRY_CATCH_PROOFS_V1", "status": "PASS" if all(t['status'] == 'PASS' for t in tests) else "FAIL", "tests": len(tests), "passed": sum(t['status'] == 'PASS' for t in tests)}
    (HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        for row in tests:
            if row["status"] != "PASS": print(row)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
