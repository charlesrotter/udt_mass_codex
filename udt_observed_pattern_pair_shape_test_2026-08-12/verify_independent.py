#!/usr/bin/env python3
"""Independent Decimal/closed-2x2 replay; imports no production code or NumPy."""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, getcontext
from pathlib import Path


getcontext().prec = 70
N = Decimal("1.0559332414320268")
Z_USED = tuple(Decimal(x) for x in ("0.510", "0.706", "0.934", "1.321", "1.484", "2.330"))


def data_rows(path: Path):
    rows = []
    numeric_index = 0
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        z, value, kind = line.split()
        rows.append((numeric_index, Decimal(z), Decimal(value), kind))
        numeric_index += 1
    return rows


def matrix(path: Path):
    return [[Decimal(x) for x in line.split()] for line in path.read_text().splitlines() if line.strip()]


def f_values(z: Decimal):
    u = Decimal(1) + z
    f0 = z + z * z / Decimal(2)
    f1 = N / Decimal(2) * ((Decimal(2) / N * u.ln()).exp() - Decimal(1))
    return f0, f1


def profile(y0, y1, c00, c01, c11, f):
    determinant = c00 * c11 - c01 * c01
    i00, i01, i11 = c11 / determinant, -c01 / determinant, c00 / determinant
    ivy0 = i00 * y0 + i01 * y1
    ivy1 = i01 * y0 + i11 * y1
    numerator = f * ivy0 + ivy1
    denominator = f * f * i00 + Decimal(2) * f * i01 + i11
    amplitude = numerator / denominator
    r0, r1 = y0 - amplitude * f, y1 - amplitude
    chi2 = r0 * (i00 * r0 + i01 * r1) + r1 * (i01 * r0 + i11 * r1)
    return amplitude, chi2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mean", type=Path, required=True)
    parser.add_argument("--cov", type=Path, required=True)
    parser.add_argument("--production", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows, cov = data_rows(args.mean), matrix(args.cov)
    production = json.loads(args.production.read_text())
    totals = {"C0": Decimal(0), "C1": Decimal(0)}
    maximum_row_delta = Decimal(0)
    exact_rows = []
    for z in Z_USED:
        dm = next(row for row in rows if row[1] == z and row[3] == "DM_over_rs")
        dh = next(row for row in rows if row[1] == z and row[3] == "DH_over_rs")
        c00, c01, c11 = cov[dm[0]][dm[0]], cov[dm[0]][dh[0]], cov[dh[0]][dh[0]]
        for name, f in zip(("C0", "C1"), f_values(z)):
            amplitude, chi2 = profile(dm[2], dh[2], c00, c01, c11, f)
            totals[name] += chi2
            prod_row = next(x for x in production["controls"][name] if Decimal(str(x["z"])) == z)
            delta = abs(chi2 - Decimal(str(prod_row["chi2"])))
            maximum_row_delta = max(maximum_row_delta, delta)
            exact_rows.append(
                {
                    "control": name,
                    "z": str(z),
                    "observed_DM": str(dm[2]),
                    "observed_DH": str(dh[2]),
                    "F": str(f),
                    "amplitude": str(amplitude),
                    "chi2": str(chi2),
                }
            )

    total_deltas = {
        name: abs(value - Decimal(str(production["totals"][name]["chi2"])))
        for name, value in totals.items()
    }
    assert maximum_row_delta < Decimal("1e-12")
    assert max(total_deltas.values()) < Decimal("1e-12")
    result = {
        "status": "PASS",
        "method": "stdlib Decimal closed 2x2 inverse and analytic profile; no NumPy or production import",
        "precision_digits": getcontext().prec,
        "totals": {key: str(value) for key, value in totals.items()},
        "total_abs_deltas": {key: str(value) for key, value in total_deltas.items()},
        "maximum_row_abs_delta": str(maximum_row_delta),
        "rows": exact_rows,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "totals", "maximum_row_abs_delta")}))


if __name__ == "__main__":
    main()
