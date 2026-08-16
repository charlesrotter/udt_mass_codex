#!/usr/bin/env python3
"""Exact finite-dimensional checks for the bounded G118 synthesis."""

from __future__ import annotations

import csv
import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rectangular_tsv(name: str) -> bool:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle, delimiter="\t"))
    return bool(rows) and all(len(row) == len(rows[0]) for row in rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    hashes = {
        row["path"]: sha256(ROOT / row["path"]) == row["sha256"]
        for row in source_rows
    }

    Z, n, R, transfer, a, theta = sp.symbols(
        "Z n R transfer a theta", positive=True, finite=True
    )
    lambda_a = n * (1 - Z ** (-sp.Rational(2, 1) / n))
    p1 = Z**2 * lambda_a
    quotient = sp.sqrt(Z) * lambda_a
    general = Z ** sp.Rational(3, 2) * quotient
    transparent = Z ** sp.Rational(3, 2) * R / sp.sqrt(1 / Z)
    rotation = sp.Matrix(
        [[sp.cos(theta), -sp.sin(theta)], [sp.sin(theta), sp.cos(theta)]]
    )
    reflection = sp.diag(1, -1)

    checks = {
        "all_16_source_hashes": len(source_rows) == 16 and all(hashes.values()),
        "dependency_tsv_rectangular": rectangular_tsv("DEPENDENCY_MAP.tsv"),
        "scaffolding_tsv_rectangular": rectangular_tsv("SCAFFOLDING_LEDGER.tsv"),
        "category_tsv_rectangular": rectangular_tsv("CATEGORY_ERROR_LEDGER.tsv"),
        "orthogonal_screen_determinant": sp.simplify((R * rotation).det() - R**2) == 0,
        "orientation_reversing_absolute_determinant": sp.simplify(
            sp.Abs((R * reflection).det()) - R**2
        ) == 0,
        "hostile_signed_determinant_rejected": sp.simplify(
            (R * reflection).det() - R**2
        ) != 0,
        "p1_sqrt_Z_retyping": sp.simplify(general - p1) == 0,
        "transparent_transfer_returns_Z2R": sp.simplify(transparent - Z**2 * R) == 0,
        "interface_fiber_invariant": sp.simplify(
            (a * R) / sp.sqrt(a**2 * transfer) - R / sp.sqrt(transfer)
        ) == 0,
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "source_hashes": hashes,
        "scope": (
            "finite-dimensional synthesis checks only; does not prove the proposed "
            "finite-radius time-live spherical Jacobi theorem"
        ),
    }
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_result:
        (HERE / "VERIFICATION_RESULT.json").write_text(output, encoding="utf-8")
    print(output, end="")
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
