#!/usr/bin/env python3
"""Independent Torch replay of every reciprocal-background Bach component."""
from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import torch
from torch.func import jacfwd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DTYPE = torch.float64
torch.set_default_dtype(DTYPE)
torch.set_num_threads(1)


def load_parent():
    path = ROOT / "c2_reciprocal_transverse_twist_jacobi_2026-07-20/verify_twist_jacobi.py"
    spec = importlib.util.spec_from_file_location("independent_parent_twist_tensor", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def polynomial(r, coefficients):
    return sum(coefficients[index] * r**index for index in range(coefficients.numel()))


def derivative(function, r, order):
    result = function
    for _ in range(order):
        result = jacfwd(result)
    return result(r)


def formula_bach(r, coefficients):
    pfun = lambda x: polynomial(x, coefficients)
    p0, a, b, c, d = [derivative(pfun, r, order) for order in range(5)]
    zero = r * 0
    b00 = (20 * a**4 - 56 * a**2 * b + 18 * a * c + 11 * b**2 - 2 * d) * torch.exp(-6 * p0) / 6
    b11 = (-4 * a**4 + 8 * a**2 * b - 2 * a * c + b**2) * torch.exp(-2 * p0) / 6
    b22 = (12 * a**4 - 32 * a**2 * b + 10 * a * c + 5 * b**2 - d) * torch.exp(-4 * p0) / 6
    return torch.stack((
        torch.stack((b00, zero, zero, zero)),
        torch.stack((zero, b11, zero, zero)),
        torch.stack((zero, zero, b22, zero)),
        torch.stack((zero, zero, zero, b22)),
    ))


def scaled_error(observed, expected):
    scale = torch.maximum(torch.tensor(1e-10), torch.maximum(torch.abs(observed), torch.abs(expected)))
    return float(torch.abs(observed - expected) / scale)


PROFILES = [
    ("P1", [0, 1/3, 1/5, -1/7], [-1/3, 1/5, 2/3]),
    ("P2", [0, -1/4, 2/7, 0, 1/13], [-2/5, 1/7, 3/5]),
    ("P3", [1/6], [-1/2, 1/4]),
]


def main():
    parent = load_parent()
    epsilon = torch.tensor(0.0)
    ucoeff = torch.tensor([0.0])
    records = []
    for name, raw_coefficients, raw_points in PROFILES:
        coefficients = torch.tensor(raw_coefficients)
        for raw_r in raw_points:
            r = torch.tensor(raw_r)
            observed = parent.bach_point(r, epsilon, coefficients, ucoeff)
            expected = formula_bach(r, coefficients)
            for a in range(4):
                for b in range(4):
                    records.append({
                        "profile": name,
                        "r": raw_r,
                        "component": f"B_{a}{b}",
                        "direct": float(observed[a, b]),
                        "formula": float(expected[a, b]),
                        "absolute_error": float(torch.abs(observed[a, b] - expected[a, b])),
                        "scaled_error": scaled_error(observed[a, b], expected[a, b]),
                    })

    nonzero = [row for row in records if abs(row["formula"]) > 1e-10]
    zero = [row for row in records if abs(row["formula"]) <= 1e-10]
    max_relative = max(row["scaled_error"] for row in nonzero)
    max_zero_absolute = max(row["absolute_error"] for row in zero)
    transverse_nonzero = max(abs(row["formula"]) for row in records if row["component"] in {"B_22", "B_33"})
    constant_control = max(
        max(abs(row["direct"]), abs(row["formula"]))
        for row in records if row["profile"] == "P3"
    )
    checks = {
        "all_registered_profiles": len(records) == 8 * 16,
        "all_nonzero_components_match": max_relative <= 1e-8,
        "all_zero_components_match": max_zero_absolute <= 1e-9,
        "transverse_bach_component_exercised": transverse_nonzero > 1e-6,
        "constant_profile_zero_control": constant_control <= 1e-9,
        "cpu_only": epsilon.device.type == "cpu",
    }
    if not all(checks.values()):
        raise AssertionError({
            "checks": checks,
            "max_relative": max_relative,
            "max_zero_absolute": max_zero_absolute,
            "constant_control": constant_control,
        })

    fields = list(records[0])
    with (HERE / "VERIFICATION_POINTS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    result = {
        "schema": "udt-c2-coupled-reciprocal-background-bach-verification-1.0",
        "result": "PASS",
        "checks": checks,
        "counts": {"profile_points": 8, "component_records": len(records), "nonzero_records": len(nonzero)},
        "maxima": {
            "nonzero_scaled_error": max_relative,
            "zero_absolute_error": max_zero_absolute,
            "transverse_component_witness": transverse_nonzero,
            "constant_profile_absolute": constant_control,
        },
        "compute": {
            "method": "independent banked Torch forward-AD full coordinate Bach tensor",
            "source": "c2_reciprocal_transverse_twist_jacobi_2026-07-20/verify_twist_jacobi.py",
            "dtype": "float64",
            "cpu_only": True,
        },
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", **result["counts"], **result["maxima"]}, sort_keys=True))


if __name__ == "__main__":
    main()
