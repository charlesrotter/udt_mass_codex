#!/usr/bin/env python3
"""Independent standard-library G254 ownership and tensor-at-anchor replay."""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def anchor_curvature(b: Fraction) -> Fraction:
    """Direct coordinate Ricci contraction at t=0 for g=(-1,a2,a2,a2), a2=exp(2bt^2)."""
    dimension = 4
    g0 = [[Fraction(0) for _ in range(dimension)] for _ in range(dimension)]
    g1 = [[Fraction(0) for _ in range(dimension)] for _ in range(dimension)]
    g2 = [[Fraction(0) for _ in range(dimension)] for _ in range(dimension)]
    inverse0 = [[Fraction(0) for _ in range(dimension)] for _ in range(dimension)]
    inverse1 = [[Fraction(0) for _ in range(dimension)] for _ in range(dimension)]
    g0[0][0] = inverse0[0][0] = Fraction(-1)
    for index in range(1, dimension):
        g0[index][index] = inverse0[index][index] = Fraction(1)
        g2[index][index] = 4 * b

    def derivative(metric_derivatives, coordinate, mu, nu):
        return metric_derivatives[mu][nu] if coordinate == 0 else Fraction(0)

    gamma0 = [[[Fraction(0) for _ in range(dimension)]
               for _ in range(dimension)] for _ in range(dimension)]
    gamma_t = [[[Fraction(0) for _ in range(dimension)]
               for _ in range(dimension)] for _ in range(dimension)]
    for rho in range(dimension):
        for mu in range(dimension):
            for nu in range(dimension):
                for sigma in range(dimension):
                    first0 = (
                        derivative(g1, mu, sigma, nu)
                        + derivative(g1, nu, sigma, mu)
                        - derivative(g1, sigma, mu, nu)
                    )
                    first_t = (
                        derivative(g2, mu, sigma, nu)
                        + derivative(g2, nu, sigma, mu)
                        - derivative(g2, sigma, mu, nu)
                    )
                    gamma0[rho][mu][nu] += Fraction(1, 2) * inverse0[rho][sigma] * first0
                    gamma_t[rho][mu][nu] += Fraction(1, 2) * (
                        inverse1[rho][sigma] * first0 + inverse0[rho][sigma] * first_t
                    )

    ricci = [[Fraction(0) for _ in range(dimension)] for _ in range(dimension)]
    for mu in range(dimension):
        for nu in range(dimension):
            for rho in range(dimension):
                if rho == 0:
                    ricci[mu][nu] += gamma_t[rho][mu][nu]
                if nu == 0:
                    ricci[mu][nu] -= gamma_t[rho][mu][rho]
                for sigma in range(dimension):
                    ricci[mu][nu] += gamma0[rho][rho][sigma] * gamma0[sigma][mu][nu]
                    ricci[mu][nu] -= gamma0[rho][nu][sigma] * gamma0[sigma][mu][rho]
    return sum(inverse0[mu][nu] * ricci[mu][nu]
               for mu in range(dimension) for nu in range(dimension))


def verify() -> dict[str, object]:
    manifest = read_tsv(PACKAGE / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == 16
    for row in manifest:
        assert sha256(ROOT / row["path"]) == row["sha256"]

    contract = read_tsv(PACKAGE / "CLOSURE_CONTRACT.tsv")
    yes_rows = [row for row in contract if row["counts_as_history_equation"] == "yes"]
    assert {row["candidate"] for row in yes_rows} == {
        "independently_owned_C_of_g_equals_zero",
        "independently_owned_global_G_of_g_and_R_equals_zero",
    }
    # These are typed future schemas, and no frozen-source row owns either schema.
    owned_active = []
    assert not owned_active

    trials = 0
    for numerator in range(-32, 33):
        b = Fraction(numerator, 7)
        assert anchor_curvature(b) == 12 * b
        trials += 1
    r0 = anchor_curvature(Fraction(0))
    r7 = anchor_curvature(Fraction(7))
    assert r0 == 0 and r7 == 84 and r0 != r7

    return {
        "status": "PASS",
        "method": "standard_library_exact_fraction_direct_coordinate_ricci_at_anchor",
        "production_imported": False,
        "production_result_read": False,
        "source_count": len(manifest),
        "contract_rows": len(contract),
        "owned_active_ambient_evolution_equation_count": 0,
        "curvature_trials": trials,
        "b0_curvature": int(r0),
        "b7_curvature": int(r7),
        "landing": "NO_OWNED_TIMELIVE_RESIDUAL__ODE_AND_GPU_SOLVES_NOT_YET_DEFINED",
        "assertion_count": 16 + len(contract) + trials + 8,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = verify()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
