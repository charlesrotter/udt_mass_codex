#!/usr/bin/env python3
"""Independent stdlib Decimal replay of the DR2 Gaussian load-bearing value."""

from __future__ import annotations

import argparse
import hashlib
import json
from decimal import Decimal, getcontext
from pathlib import Path


getcontext().prec = 70


def sha256(path: Path) -> str:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def matrix(path: Path):
    return [
        [Decimal(token) for token in line.split()]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def solve(a, b):
    n = len(a)
    aug = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(aug[row][col]))
        if aug[pivot][col] == 0:
            raise ArithmeticError("singular matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        for j in range(col, n + 1):
            aug[col][j] /= scale
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            if factor == 0:
                continue
            for j in range(col, n + 1):
                aug[row][j] -= factor * aug[col][j]
    return [aug[i][n] for i in range(n)]


def cholesky_positive(a):
    n = len(a)
    lower = [[Decimal(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            value = a[i][j] - sum(lower[i][k] * lower[j][k] for k in range(j))
            if i == j:
                if value <= 0:
                    return False
                lower[i][j] = value.sqrt()
            else:
                lower[i][j] = value / lower[j][j]
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cov", type=Path, required=True)
    parser.add_argument("--production-json", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    production = json.loads(args.production_json.read_text(encoding="utf-8"))
    cov = matrix(args.cov)
    n = len(cov)
    assert n == 13 and all(len(row) == n for row in cov)
    assert all(cov[i][j] == cov[j][i] for i in range(n) for j in range(n))
    assert cholesky_positive(cov)
    assert sha256(args.cov) == production["cov_sha256"]

    residual = [Decimal(-30 + 5 * i) / Decimal(100) for i in range(n)]
    solution = solve(cov, residual)
    logpdf = -sum(residual[i] * solution[i] for i in range(n)) / Decimal(2)
    production_value = Decimal(str(production["gaussian_replay"]["manual_logpdf"]))
    abs_delta = abs(logpdf - production_value)
    if abs_delta > Decimal("2e-13"):
        raise AssertionError((logpdf, production_value, abs_delta))

    result = {
        "status": "PASS",
        "method": "stdlib Decimal Gaussian elimination and Cholesky; no numpy or production import",
        "precision_digits": getcontext().prec,
        "cov_sha256": sha256(args.cov),
        "logpdf": str(logpdf),
        "production_float_logpdf": str(production_value),
        "abs_delta": str(abs_delta),
        "symmetric_exact": True,
        "cholesky_positive": True,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
