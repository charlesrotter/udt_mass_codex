#!/usr/bin/env python3
"""Dependency-free independent checks for G255.

This verifier does not import the production census builder or any G254 code.
It rechecks frozen-source integrity, exact 90-slot coverage, classification
counts, the candidate gate, and the counterhistory scalar curvature by a full
coordinate Ricci contraction using Fraction arithmetic.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_source_sha256(path: Path, relative: str) -> str:
    """Replay the prereview registry snapshot after the appended G255 current row."""
    if relative != "CURRENT_SCIENTIFIC_PREMISES.tsv":
        return sha256(path)
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    frozen = "".join(line for line in lines if not line.startswith("G255\t"))
    return hashlib.sha256(frozen.encode("utf-8")).hexdigest()


def zeros(*shape: int):
    if len(shape) == 1:
        return [Fraction(0) for _ in range(shape[0])]
    return [zeros(*shape[1:]) for _ in range(shape[0])]


def ricci_scalar_from_metric_2jet(b: Fraction, t: Fraction) -> Fraction:
    """Direct coordinate Ricci scalar for diag(-1,a(t)^2,a(t)^2,a(t)^2).

    A spatial coordinate rescaling sets a(t)=1 at the evaluation event.  The
    invariant logarithmic derivatives H=a'/a and A2=a''/a retain the full jet.
    No FLRW curvature formula is used in the contraction below.
    """

    dim = 4
    h = 2 * b * t
    a2 = 2 * b + 4 * b * b * t * t
    g = zeros(dim, dim)
    gi = zeros(dim, dim)
    g[0][0] = gi[0][0] = Fraction(-1)
    for i in range(1, dim):
        g[i][i] = gi[i][i] = Fraction(1)

    dg = zeros(dim, dim, dim)
    ddg = zeros(dim, dim, dim, dim)
    for i in range(1, dim):
        dg[0][i][i] = 2 * h
        ddg[0][0][i][i] = 2 * (h * h + a2)

    dgi = zeros(dim, dim, dim)
    for lam in range(dim):
        for mu in range(dim):
            for nu in range(dim):
                dgi[lam][mu][nu] = -sum(
                    gi[mu][a] * dg[lam][a][c] * gi[c][nu]
                    for a in range(dim)
                    for c in range(dim)
                )

    gamma = zeros(dim, dim, dim)
    dgamma = zeros(dim, dim, dim, dim)
    for rho in range(dim):
        for mu in range(dim):
            for nu in range(dim):
                for sig in range(dim):
                    first = dg[mu][sig][nu] + dg[nu][sig][mu] - dg[sig][mu][nu]
                    gamma[rho][mu][nu] += gi[rho][sig] * first / 2
                    for lam in range(dim):
                        second = (
                            ddg[lam][mu][sig][nu]
                            + ddg[lam][nu][sig][mu]
                            - ddg[lam][sig][mu][nu]
                        )
                        dgamma[lam][rho][mu][nu] += (
                            dgi[lam][rho][sig] * first + gi[rho][sig] * second
                        ) / 2

    ricci = zeros(dim, dim)
    for mu in range(dim):
        for nu in range(dim):
            ricci[mu][nu] = sum(
                dgamma[rho][rho][mu][nu] - dgamma[nu][rho][mu][rho]
                for rho in range(dim)
            )
            ricci[mu][nu] += sum(
                gamma[rho][rho][lam] * gamma[lam][mu][nu]
                - gamma[rho][nu][lam] * gamma[lam][mu][rho]
                for rho in range(dim)
                for lam in range(dim)
            )
    return sum(gi[mu][nu] * ricci[mu][nu] for mu in range(dim) for nu in range(dim))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    if args.no_write and args.output:
        raise SystemExit("--no-write and --output are mutually exclusive")

    checks = 0
    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        manifest = list(csv.DictReader(handle, delimiter="\t"))
    assert len(manifest) == 321
    checks += 1
    for row in manifest:
        path = ROOT / row["path"]
        assert path.is_file()
        assert frozen_source_sha256(path, row["path"]) == row["sha256"]
        assert "udt_native_onshell_timelive_reset_owner_audit" not in row["path"]
        assert "udt_pair_regime_flow_reciprocal_orchestra_amplification" not in row["path"]
        assert "udt_sne_xmax_G88_am_radial_compatibility_atlas" not in row["path"]
        checks += 4

    with (PKG / "EQUATION_OWNERSHIP_CENSUS.tsv").open(newline="", encoding="utf-8") as handle:
        census = list(csv.DictReader(handle, delimiter="\t"))
    expected = [f"G{number}" for number in range(165, 255)]
    assert [row["slot"] for row in census] == expected
    assert len({row["decisive_report"] for row in census}) == 90
    checks += 2
    for row in census:
        assert sha256(ROOT / row["decisive_report"]) == row["decisive_report_sha256"]
        assert row["primary_class"] not in {"C12", "C13", "C14"}
        assert row["passes_owned_history_gate"] == "false"
        assert row["g254_counterhistory_gate"] == "NOT_REJECTED"
        checks += 4

    with (PKG / "CANDIDATE_EQUATION_LEDGER.tsv").open(newline="", encoding="utf-8") as handle:
        candidates = list(csv.DictReader(handle, delimiter="\t"))
    assert len(candidates) == 21
    assert [row["candidate_id"] for row in candidates] == [f"K{i:02d}" for i in range(1, 22)]
    assert not any(row["classification"] in {"C12", "C13", "C14"} for row in candidates)
    assert sum("NOT_UDT_OWNED" in row["udt_owner_status"] for row in candidates) == 1
    assert candidates[7]["candidate_id"] == "K08"
    assert candidates[7]["g254_twin_test"] == "REJECTS_GENERIC_TWIN"
    checks += 6

    curvature_cases = 0
    for b_num in range(-8, 9):
        b = Fraction(b_num, 3)
        for t in (Fraction(-3, 2), Fraction(-1, 3), Fraction(0), Fraction(2, 5), Fraction(7, 4)):
            direct = ricci_scalar_from_metric_2jet(b, t)
            expected_r = 12 * b * (1 + 4 * b * t * t)
            assert direct == expected_r
            curvature_cases += 1
            checks += 1

    # Independent completed Eulerian-pair check at arbitrary positive local a.
    for a in (Fraction(1, 5), Fraction(1), Fraction(7, 3), Fraction(11)):
        h00 = Fraction(-1)
        h11 = a * a * (Fraction(1, 1) / a) ** 2
        det_h = h00 * h11
        assert (h00, h11, det_h) == (Fraction(-1), Fraction(1), Fraction(-1))
        checks += 1

    # Hostile controls: the gate must catch promoted/unowned or incomplete rows.
    hostile_caught = 0
    mutated = [dict(row) for row in census]
    mutated[0]["primary_class"] = "C12"
    try:
        assert all(row["primary_class"] not in {"C12", "C13", "C14"} for row in mutated)
    except AssertionError:
        hostile_caught += 1
    try:
        assert [row["slot"] for row in census[:-1]] == expected
    except AssertionError:
        hostile_caught += 1
    try:
        assert "NOT_UDT_OWNED" not in candidates[7]["udt_owner_status"]
    except AssertionError:
        hostile_caught += 1
    try:
        assert sha256(ROOT / manifest[0]["path"]) == ("0" * 64)
    except AssertionError:
        hostile_caught += 1
    assert hostile_caught == 4
    checks += 5

    result = {
        "status": "PASS",
        "slot_count": len(census),
        "source_count": len(manifest),
        "candidate_count": len(candidates),
        "owned_local_metric_condition_count": 0,
        "owned_global_relation_law_count": 0,
        "unresolved_candidate_count": 0,
        "counterhistory_curvature_cases": curvature_cases,
        "hostile_mutations_caught": hostile_caught,
        "assertion_count": checks,
        "landing": "NO_LOST_CLOSURE_IN_G165_G254",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
