#!/usr/bin/env python3
"""Fail-closed artifact and algebra verifier for the F01/F02 Jacobi control package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


PACKAGE_NAME = "udt_cmb_F01_F02_observer_sky_jacobi_controls_2026-08-11"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify(package: Path, source_root: Path) -> dict:
    checks: dict[str, bool] = {}

    source_rows = rows(package / "SOURCE_MANIFEST.tsv")
    require(len(source_rows) == 7, "source universe must contain exactly seven frozen rows")
    for row in source_rows:
        require(sha256(source_root / row["path"]) == row["sha256"], f"source hash changed: {row['path']}")
    checks["J01_source_hashes"] = True

    controls = rows(package / "LOCAL_CONTROL_ATLAS.tsv")
    require([r["family"] for r in controls] == ["F01", "F02"], "control universe missing, duplicate, or reordered")
    require(len({r["query_status"] for r in controls}) == 1 and controls[0]["query_status"] == "IDENTICAL_QSKY", "query mismatch")
    require(controls[1]["psi_tidal"].startswith("h0*N/"), "F02 mixing tidal term removed")
    require(all(r["physical_status"] == "CONTROL_NOT_SELECTED" for r in controls), "control promoted to physical")
    checks["J02_identical_query"] = True
    checks["J03_complete_F02"] = True
    checks["J10_no_control_selection"] = True

    result = json.loads((package / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    require(result["primary_landing"] == "LOCAL_SKY_MAP_GEOMETRY_DISTINGUISHES_F01_F02_WITH_PROFILE_REMAINDER", "landing changed")
    require(result["F01_induced_limit"] == [["0", "0"], ["0", "0"]], "F01 round result mutated")
    require(result["generator_norm"] == "0", "query generator is not null")
    require(result["frame_gram_before_equator"] == [["-1", "0", "0", "0"], ["0", "1", "0", "0"], ["0", "0", "1", "0"], ["0", "0", "0", "1"]], "query frame is not orthonormal")
    require(result["F02_tidal_matrix_equator"][0] == ["0", "0"] and result["F02_tidal_matrix_equator"][1][0] == "0", "F02 screen matrix structure changed")
    require(result["antisymmetric"] == "0" and result["shear_cross"] == "0", "screen symmetry/rotation failure")
    require(result["weak_mixing_linear"] == "0" and result["weak_mixing_cubic"] == "0", "weak-mixing parity changed")
    require("no finite CMB angular map" in result["maximum_conclusion"] and "no finite" not in result["primary_landing"], "scope promotion")
    checks["J04_round_limit"] = True
    checks["J05_query_type"] = True
    checks["J06_screen_symmetry"] = True
    checks["J07_local_scope"] = True

    r, A0, A1, A2, h0, h1, h2 = sp.symbols("r A0 A1 A2 h0 h1 h2", real=True)
    local = {x.name: x for x in (r, A0, A1, A2, h0, h1, h2)}
    tau = sp.sympify(result["F02_tidal_matrix_equator"][1][1], locals=local)
    N = sp.sympify(result["mixing_polynomial_N"], locals=local)
    expected_tau = h0 * N / (4 * A0 * (A0 * r**2 + h0**2) ** 2)
    require(sp.factor(tau - expected_tau) == 0, "F02 exact factorization failed")
    require(sp.factor(tau.subs({h0: 0})) == 0, "h0=0 special sublocus lost")
    checks["exact_factorization"] = True

    subloci = rows(package / "SPECIAL_SUBLOCUS_ATLAS.tsv")
    expected_subloci = {"ROUND_F01", "MIXING_ZERO_AT_EVENT", "NONZERO_MIX_CANCELLATION", "GENERIC_MIXING", "WEAK_MIXING", "POSITIVE_CONTROL", "NEGATIVE_CONTROL"}
    require({r["sublocus"] for r in subloci} == expected_subloci and len(subloci) == len(expected_subloci), "special sublocus discarded or duplicated")
    checks["J12_complete_subloci"] = True

    projection = {r["historical_freedom"]: r for r in rows(package / "PROJECTION_FREEDOM_LEDGER.tsv")}
    require(projection["TT_power"]["status_after_control"] == "OPEN", "TT power inferred without source")
    require(projection["affine_offset"]["status_after_control"] == "NOT_OWNED_BY_THIS_QUERY", "offset silently assigned to screen map")
    checks["J08_source_ownership"] = True

    premise = {r["item"]: r for r in rows(package / "PREMISE_LEDGER.tsv")}
    require(premise["c_eff_pair"]["not_owned"] == "local propagation speed", "observer/local c_eff guard lost")
    require(premise["X_max"]["not_owned"] == "local wall or boundary", "Xmax local-wall regression")
    checks["J09_observer_local_guard"] = True

    independent = json.loads((package / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    require(independent["passed"] == independent["total"] == 6 and all(independent["checks"].values()), "independent checks failed")
    require(independent["method"].startswith("direct fully-lowered Riemann") and "production" not in independent["method"], "independence method invalid")
    checks["J11_independence"] = True

    exact = (package / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    require("does not select the\nremote comparison surface" in exact, "finite endpoint scope lost")
    require("not being promoted to a local material signal trajectory" in exact, "co-present signal guard lost")
    require("mode-ladder offset is boundary/operator phase data" in exact, "offset ownership lost")
    checks["semantic_guards"] = True

    return {"checks": checks, "passed": len(checks), "total": len(checks)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path)
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()
    source_root = (args.source_root or Path(__file__).resolve().parents[1]).resolve()
    package = (args.package or source_root / PACKAGE_NAME).resolve()
    result = verify(package, source_root)
    (package / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
