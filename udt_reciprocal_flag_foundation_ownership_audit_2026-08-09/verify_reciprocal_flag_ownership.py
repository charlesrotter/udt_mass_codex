#!/usr/bin/env python3
"""Independent standard-library verifier for the reciprocal-flag audit.

This deliberately does not import the SymPy controller.
"""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path


EXPECTED_LANDING = (
    "FOUNDED_ABSTRACT_RECIPROCAL_CALIBRATION_SEED_DERIVED__"
    "RECIPROCAL_ROOT_CONDITIONAL_UNIQUE_UNIVERSAL_ORDER_ZERO_READOUT__"
    "COMPLETE_CAUSAL_FLAG_TRANSPORT_CALIBRATION_AND_PHYSICAL_ARROW_OPEN"
)


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


def diag(*values):
    return [[values[i] if i == j else Fraction(0) for j in range(len(values))] for i in range(len(values))]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def gram(metric, vectors):
    return mmul(mmul(transpose(vectors), metric), vectors)


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
        manifest = list(csv.DictReader(stream, delimiter="\t"))
    check("26 frozen source identities", len(manifest) == 26 == len({row["path"] for row in manifest}))
    for row in manifest:
        path = repo / row["path"]
        check(f"hash {row['path']}", path.is_file() and sha256(path) == row["sha256"])

    result = json.loads((package / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    check("controller landing", result["landing"] == EXPECTED_LANDING)
    check("controller checks all passed", result["all_passed"] and result["passed_count"] == result["check_count"])
    check("controller exact character rank", result["exact"]["abelianization_dimension"] == 3)
    check("controller exact weights", result["exact"]["exchange_weights"] == ["-1/2", "1/2", "0"])

    # Exact finite rational reconstruction at exp(t)=2.
    half = Fraction(1, 2)
    one = Fraction(1)
    zero = Fraction(0)
    D = diag(half, 2 * one, one, one)
    S = diag(half, one, one, one)
    Sinv = diag(2 * one, one, one, one)
    J = [[zero, -one, zero, zero], [one, zero, zero, zero], [zero, zero, one, zero], [zero, zero, zero, one]]
    Jinv = [[zero, one, zero, zero], [-one, zero, zero, zero], [zero, zero, one, zero], [zero, zero, zero, one]]
    check("full GL commutator reconstruction", mmul(mmul(mmul(S, J), Sinv), Jinv) == D)

    K = [[zero, one], [one, zero]]
    D2 = diag(half, 2 * one)
    eta2 = diag(-one, one)
    check("K pairing preserved", mmul(mmul(transpose(D2), K), D2) == K)
    check("K is physical anti-isometry", mmul(mmul(transpose(K), eta2), K) == [[one, zero], [zero, -one]])

    eta4 = diag(-one, one, one, one)
    A = [[half, zero, zero, zero], [zero, 2 * one, zero, zero], [Fraction(1, 4), zero, one, zero], [zero, zero, zero, one]]
    line = [[one], [zero], [zero], [zero]]
    plane = [[one, zero], [zero, one], [zero, zero], [zero, zero]]
    line_gram = gram(eta4, mmul(A, line))[0][0]
    plane_gram = gram(eta4, mmul(A, plane))
    rho1_sq = abs(line_gram) / abs(gram(eta4, line)[0][0])
    rho2_sq = abs(det2(plane_gram)) / abs(det2(gram(eta4, plane)))
    check("independent mixed clock density", rho1_sq == Fraction(3, 16))
    check("independent mixed plane density", rho2_sq == Fraction(3, 4))
    delta = 0.25 * math.log(float(rho2_sq)) - 0.5 * math.log(float(rho1_sq))
    check("independent mixed delta", abs(delta - 0.25 * math.log(64.0 / 3.0)) < 1e-15)

    # A second leg tests telescoping without sharing the controller's helper.
    B = diag(Fraction(3, 2), Fraction(5, 4), Fraction(7, 6), Fraction(9, 8))
    BA = mmul(B, A)
    Aline = mmul(A, line)
    Aplane = mmul(A, plane)
    rho1_B_sq = abs(gram(eta4, mmul(B, Aline))[0][0]) / abs(gram(eta4, Aline)[0][0])
    rho2_B_sq = abs(det2(gram(eta4, mmul(B, Aplane)))) / abs(det2(gram(eta4, Aplane)))
    rho1_BA_sq = abs(gram(eta4, mmul(BA, line))[0][0]) / abs(gram(eta4, line)[0][0])
    rho2_BA_sq = abs(det2(gram(eta4, mmul(BA, plane)))) / abs(det2(gram(eta4, plane)))
    check("independent clock telescoping", rho1_BA_sq == rho1_sq * rho1_B_sq)
    check("independent plane telescoping", rho2_BA_sq == rho2_sq * rho2_B_sq)

    # The coefficient solution is exact without a symbolic solver.
    alpha = Fraction(-1, 2)
    beta = Fraction(1, 2)
    gamma = Fraction(0)
    check("normalization", -alpha + beta == 1)
    check("exchange oddness", beta == -alpha and gamma == 0)

    # Direct elementary evaluation of the higher-jet connection witness.
    # Integral_0^1 32 t/(1+t^2)^3 dt = 6.
    integral = Fraction(8) * (one - Fraction(1, 4))
    check("higher-order connection clock factor", integral == 6)
    check("higher-order connection depth factor", -integral / 2 == -3)

    with (package / "FOUNDATION_OWNERSHIP.tsv").open(newline="", encoding="utf-8") as stream:
        ownership = list(csv.DictReader(stream, delimiter="\t"))
    check("ownership identities unique", len(ownership) == len({row["object_id"] for row in ownership}))
    by_id = {row["object_id"]: row for row in ownership}
    check("physical arrow remains open", by_id["F13"]["status"].startswith("OPEN"))
    check("flag remains conditional", by_id["F08"]["status"].startswith("CONDITIONAL"))
    check("calibration remains open", by_id["F14"]["status"].startswith("OPEN"))
    check("abstract exchange is scoped", by_id["F03"]["status"] == "DERIVED_ABSTRACT_ONLY")

    with (package / "DOWNSTREAM_REGRADE.tsv").open(newline="", encoding="utf-8") as stream:
        regrades = list(csv.DictReader(stream, delimiter="\t"))
    check("downstream regrade identities unique", len(regrades) == len({row["item_id"] for row in regrades}))
    joined = "\n".join(row["corrected_status"] for row in regrades)
    check("spectral extractor not promoted to cocycle", "STRAIN_EXTRACTOR_NOT_A_GENERAL_COCYCLE" in joined)
    check("Xmax remains unchanged", any(row["item_id"] == "R06" and "UNCHANGED" in row["corrected_status"] for row in regrades))

    verification = {
        "schema": "udt-reciprocal-flag-foundation-ownership-independent-v1",
        "landing": EXPECTED_LANDING,
        "method": "standard_library_fraction_reconstruction_no_controller_import",
        "check_count": len(checks),
        "passed_count": sum(int(row["passed"]) for row in checks),
        "all_passed": all(row["passed"] for row in checks),
        "checks": checks,
    }
    args.output.write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: verification[k] for k in ("landing", "check_count", "passed_count", "all_passed")}, sort_keys=True))


if __name__ == "__main__":
    main()
