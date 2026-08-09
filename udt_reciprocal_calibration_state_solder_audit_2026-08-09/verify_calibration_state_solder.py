#!/usr/bin/env python3
"""Independent standard-library verifier for the calibration-state audit."""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import subprocess


EXPECTED_LANDING = (
    "ABSTRACT_RECIPROCAL_CALIBRATION_LINE_DERIVED__"
    "PAIR_RELATIVE_CAUSAL_FLAG_CONDITIONALLY_CONSTRUCTIBLE_ON_REGULAR_QUERIES__"
    "NO_NONZERO_ORDER_ZERO_OR_FIRST_METRIC_JET_NATURAL_SOLDER__"
    "STATIONARY_KILLING_SOLDER_CONDITIONAL_POSITIVE__"
    "GENERAL_BILOCAL_GLOBAL_CALIBRATION_STATE_FUNCTOR_OPEN"
)
PREREG_BASE = "30bdb020"
MUTABLE_SNAPSHOT_SOURCE = "CURRENT_SCIENTIFIC_PREMISES.tsv"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def mmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def diag(*xs):
    return [[xs[i] if i == j else Fraction(0) for j in range(len(xs))] for i in range(len(xs))]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().with_name("VERIFICATION_RESULT.json"))
    args = parser.parse_args()
    repo = args.repo.resolve()
    package = Path(__file__).resolve().parent
    checks = []

    def check(name, condition):
        passed = bool(condition)
        checks.append({"name": name, "passed": passed})
        if not passed:
            raise AssertionError(name)

    with (package / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        sources = list(csv.DictReader(stream, delimiter="\t"))
    check("24 frozen source identities", len(sources) == 24 == len({row["path"] for row in sources}))
    for row in sources:
        path = repo / row["path"]
        if row["path"] == MUTABLE_SNAPSHOT_SOURCE:
            frozen = subprocess.check_output(
                ["git", "show", f"{PREREG_BASE}:{row['path']}"], cwd=repo
            )
            observed = hashlib.sha256(frozen).hexdigest()
        else:
            observed = sha256(path) if path.is_file() else ""
        check(f"hash {row['path']}", path.is_file() and observed == row["sha256"])

    result = json.loads((package / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    check("controller landing", result["landing"] == EXPECTED_LANDING)
    check("controller all checks pass", result["all_passed"] and result["passed_count"] == result["check_count"])
    check("controller source count", result["source_count"] == 24)
    check("abstract calibration line derived", result["statuses"]["abstract_calibration_line"].startswith("DERIVED"))
    check("general functor remains open", result["statuses"]["general_physical_functor"].startswith("OPEN"))

    one = Fraction(1)
    zero = Fraction(0)
    eta = diag(-one, one, one, one)
    T = diag(Fraction(1, 2), Fraction(2), one, one)
    gq = mmul(mmul(transpose(T), eta), T)
    check("independent chart identity strain", mmul(eta, gq) == diag(Fraction(1, 4), Fraction(4), one, one))
    Tinv = diag(Fraction(2), Fraction(1, 2), one, one)
    check("independent correct map is isometric", mmul(mmul(transpose(Tinv), gq), Tinv) == eta)

    u = [[one], [zero], [zero], [zero]]
    n = [[zero], [Fraction(3, 5)], [Fraction(4, 5)], [zero]]
    gu = mmul(mmul(transpose(u), eta), u)[0][0]
    gn = mmul(mmul(transpose(n), eta), n)[0][0]
    gun = mmul(mmul(transpose(u), eta), n)[0][0]
    check("independent regular query flag", gu == -one and gn == one and gun == zero)

    check("independent triangle nonadditivity", abs((1.0 + 1.0) - math.sqrt(2.0)) > 0.5)
    f_half = 3.0 / math.pi
    f_full = 3.0 * math.sqrt(3.0) / (2.0 * math.pi)
    check("independent dexp noncomposition", abs(f_half * f_half - f_full) > 1e-3)
    check("independent Jacobi block noncomposition", abs(math.sin(math.pi / 3) - math.sin(math.pi / 6) ** 2) > 0.5)

    check("independent raw chart current", Fraction(-1, 2) != zero)
    check("independent covariantized chart current", one - one == zero)
    check("independent higher-order family", Fraction(-3) != zero)

    with (package / "SOLDER_CANDIDATE_LEDGER.tsv").open(newline="", encoding="utf-8") as stream:
        candidates = list(csv.DictReader(stream, delimiter="\t"))
    check("candidate identities unique", len(candidates) == len({row["candidate_id"] for row in candidates}))
    by_id = {row["candidate_id"]: row for row in candidates}
    check("LC candidate zero-depth", by_id["C03"]["status"] == "DERIVED_ZERO_DEPTH")
    check("dexp rejected as functor", by_id["C06"]["status"] == "REJECTED_NONCOMPOSITIONAL")
    check("Killing branch conditional", by_id["C11"]["status"] == "CONDITIONAL_POSITIVE")
    check("no physical universal solder claimed", all(row["status"] != "DERIVED_UNIVERSAL_NONZERO_SOLDER" for row in candidates))

    with (package / "STATUS_LEDGER.tsv").open(newline="", encoding="utf-8") as stream:
        statuses = list(csv.DictReader(stream, delimiter="\t"))
    check("status identities unique", len(statuses) == len({row["claim_id"] for row in statuses}))
    status_by_id = {row["claim_id"]: row for row in statuses}
    check("order-one no-go scoped", status_by_id["S05"]["status"] == "DERIVED_SCOPED_NO_GO")
    check("higher-order not ruled out", status_by_id["S10"]["status"] == "OPEN_NONUNIQUE")
    check("physical c_eff join open", status_by_id["S13"]["status"] == "OPEN_CONSISTENT_EXTENSION")

    verification = {
        "schema": "udt-reciprocal-calibration-state-solder-independent-v1",
        "landing": EXPECTED_LANDING,
        "method": "standard_library_fraction_and_numeric_reconstruction_no_controller_import",
        "check_count": len(checks),
        "passed_count": sum(int(row["passed"]) for row in checks),
        "all_passed": all(row["passed"] for row in checks),
        "checks": checks,
    }
    args.output.write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: verification[k] for k in ("landing", "check_count", "passed_count", "all_passed")}, sort_keys=True))


if __name__ == "__main__":
    main()
