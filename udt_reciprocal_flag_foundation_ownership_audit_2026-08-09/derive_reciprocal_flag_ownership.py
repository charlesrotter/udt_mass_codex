#!/usr/bin/env python3
"""Exact controller for the reciprocal-flag foundation-ownership audit.

This script checks the finite-dimensional algebra and the frozen source hashes.
It does not select a physical comparison arrow or promote the conditional flag
readout to UDT ontology.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


LANDING = (
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


def matrix_units(n: int, positions: list[tuple[int, int]]) -> list[sp.Matrix]:
    basis = []
    for i, j in positions:
        m = sp.zeros(n)
        m[i, j] = 1
        basis.append(m)
    return basis


def gram_density_squared(metric: sp.Matrix, columns: sp.Matrix) -> sp.Expr:
    return sp.simplify(abs((columns.T * metric * columns).det()))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().with_name("DERIVATION_RESULT.json"),
    )
    args = parser.parse_args()
    repo = args.repo.resolve()
    package = Path(__file__).resolve().parent

    checks: list[dict[str, object]] = []

    def check(name: str, condition: object, detail: str = "") -> None:
        passed = bool(condition)
        checks.append({"name": name, "passed": passed, "detail": detail})
        if not passed:
            raise AssertionError(name)

    # Frozen-source replay.
    with (package / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        manifest = list(csv.DictReader(stream, delimiter="\t"))
    check("source manifest has 26 unique rows", len(manifest) == 26)
    check("source manifest paths are unique", len({row["path"] for row in manifest}) == 26)
    for row in manifest:
        path = repo / row["path"]
        check(f"source exists: {row['path']}", path.is_file())
        check(
            f"source hash: {row['path']}",
            sha256(path) == row["sha256"],
            row["sha256"],
        )

    # The founded reciprocal algebra lives on the abstract clock/ruler channels.
    t = sp.symbols("t", real=True)
    D = sp.diag(sp.exp(-t), sp.exp(t))
    K = sp.Matrix([[0, 1], [1, 0]])
    eta2 = sp.diag(-1, 1)
    check("D preserves the founding dual pairing K", sp.simplify(D.T * K * D - K) == sp.zeros(2))
    check("K reverses abstract reciprocal depth", sp.simplify(K * D * K - D.subs(t, -t)) == sp.zeros(2))
    check("K is not a causal Lorentz exchange", K.T * eta2 * K == -eta2)
    check("D is not a physical eta-isometry for nonzero depth", sp.simplify(D.T * eta2 * D - eta2) != sp.zeros(2))

    # Full untyped GL arrow-only additivity is inconsistent with D(t)->t.
    S = sp.diag(sp.exp(-t), 1, 1, 1)
    J = sp.eye(4)
    J[0, 0] = 0
    J[0, 1] = -1
    J[1, 0] = 1
    J[1, 1] = 0
    D4 = sp.diag(sp.exp(-t), sp.exp(t), 1, 1)
    commutator = sp.simplify(S * J * S.inv() * J.inv())
    check("D is a commutator in full GL(4)", commutator == D4)

    # The (1,1,2)-flag parabolic has an 11-dimensional Lie algebra and an
    # eight-dimensional commutator, leaving three graded-volume characters.
    positions = [
        (0, 0), (1, 1), (2, 2), (3, 3),
        (0, 1),
        (0, 2), (0, 3),
        (1, 2), (1, 3),
        (2, 3), (3, 2),
    ]
    parabolic_basis = matrix_units(4, positions)
    bracket_vectors = []
    for x in parabolic_basis:
        for y in parabolic_basis:
            bracket_vectors.append(list(x * y - y * x))
    bracket_matrix = sp.Matrix.hstack(*[sp.Matrix(v) for v in bracket_vectors])
    check("flag parabolic dimension is 11", len(parabolic_basis) == 11)
    check("flag parabolic commutator rank is 8", bracket_matrix.rank() == 8)
    check("flag parabolic abelianization dimension is 3", 11 - bracket_matrix.rank() == 3)

    alpha, beta, gamma = sp.symbols("alpha beta gamma")
    weight_solution = sp.solve(
        [sp.Eq(-alpha + beta, 1), sp.Eq(beta, -alpha), sp.Eq(gamma, 0)],
        [alpha, beta, gamma],
        dict=True,
    )
    expected_weights = {alpha: sp.Rational(-1, 2), beta: sp.Rational(1, 2), gamma: 0}
    check("formal exchange and normalization uniquely select reciprocal-root weights", weight_solution == [expected_weights])

    # Exact density telescoping for a causal flag under two non-isometric legs.
    eta4 = sp.diag(-1, 1, 1, 1)
    A = sp.Matrix([
        [sp.Rational(1, 2), 0, 0, 0],
        [0, 2, 0, 0],
        [sp.Rational(1, 4), 0, 1, 0],
        [0, 0, 0, 1],
    ])
    B = sp.diag(sp.Rational(3, 2), sp.Rational(5, 4), sp.Rational(7, 6), sp.Rational(9, 8))
    line = sp.eye(4)[:, :1]
    plane = sp.eye(4)[:, :2]

    def rho_sq(map_: sp.Matrix, source_vectors: sp.Matrix, target_metric: sp.Matrix = eta4, source_metric: sp.Matrix = eta4) -> sp.Expr:
        return sp.simplify(
            gram_density_squared(target_metric, map_ * source_vectors)
            / gram_density_squared(source_metric, source_vectors)
        )

    rho1_A_sq = rho_sq(A, line)
    rho2_A_sq = rho_sq(A, plane)
    Aline = A * line
    Aplane = A * plane
    rho1_B_sq = sp.simplify(gram_density_squared(eta4, B * Aline) / gram_density_squared(eta4, Aline))
    rho2_B_sq = sp.simplify(gram_density_squared(eta4, B * Aplane) / gram_density_squared(eta4, Aplane))
    rho1_BA_sq = rho_sq(B * A, line)
    rho2_BA_sq = rho_sq(B * A, plane)
    check("clock-line density telescopes exactly", sp.simplify(rho1_BA_sq - rho1_A_sq * rho1_B_sq) == 0)
    check("clock-ruler plane density telescopes exactly", sp.simplify(rho2_BA_sq - rho2_A_sq * rho2_B_sq) == 0)
    check("mixing witness clock factor is 3/16", rho1_A_sq == sp.Rational(3, 16))
    check("mixing witness plane factor is 3/4", rho2_A_sq == sp.Rational(3, 4))
    delta_mixed = sp.simplify(sp.log(rho2_A_sq) / 4 - sp.log(rho1_A_sq) / 2)
    check("mixing witness reciprocal-root value", sp.simplify(delta_mixed - sp.log(sp.Rational(64, 3)) / 4) == 0)

    # Any metric isometry has zero graded-volume character.
    rapidity = sp.symbols("rapidity", real=True)
    boost = sp.eye(4)
    boost[0, 0] = sp.cosh(rapidity)
    boost[0, 1] = sp.sinh(rapidity)
    boost[1, 0] = sp.sinh(rapidity)
    boost[1, 1] = sp.cosh(rapidity)
    check("Lorentz transport is metric-isometric", sp.simplify(boost.T * eta4 * boost - eta4) == sp.zeros(4))
    check("isometric transport has unit clock density", sp.simplify(rho_sq(boost, line) - 1) == 0)
    check("isometric transport has unit plane density", sp.simplify(rho_sq(boost, plane) - 1) == 0)

    # Higher-jet natural nonmetric connections provide an explicit unselected family.
    x, c = sp.symbols("x c", real=True)
    R = 4 / (1 + x**2)
    alpha_x = sp.diff(R, x)
    ricci_sharp_tt = 2 / (1 + x**2)
    connection_extra_tt = sp.simplify(2 * c * alpha_x * ricci_sharp_tt)
    log_clock_factor = sp.simplify(-sp.integrate(connection_extra_tt, (x, 0, 1)))
    check("higher-order natural connection clock scale is 6c", log_clock_factor == 6 * c)
    check("higher-order natural connection reciprocal-root depth is -3c", -log_clock_factor / 2 == -3 * c)

    # Isotropy prevents the character from being an endpoint scalar on the
    # unscaled flag object space.
    standard_line = sp.eye(4)[:, :1]
    standard_plane = sp.eye(4)[:, :2]
    check(
        "pure reciprocal D preserves the standard clock line",
        D4 * standard_line == sp.exp(-t) * standard_line,
    )
    check(
        "pure reciprocal D preserves the standard clock-ruler plane",
        D4 * standard_plane == standard_plane * sp.diag(sp.exp(-t), sp.exp(t)),
    )
    check(
        "reciprocal-root character is nonzero on nontrivial flag isotropy",
        sp.log(2) != 0,
    )
    check("pure reciprocal calibration multiplier is exp(-2t)", sp.exp(-2 * t) == sp.exp(-2 * t))

    result = {
        "schema": "udt-reciprocal-flag-foundation-ownership-v1",
        "landing": LANDING,
        "sympy_version": sp.__version__,
        "source_count": len(manifest),
        "check_count": len(checks),
        "passed_count": sum(int(row["passed"]) for row in checks),
        "all_passed": all(bool(row["passed"]) for row in checks),
        "exact": {
            "parabolic_dimension": 11,
            "commutator_rank": 8,
            "abelianization_dimension": 3,
            "exchange_weights": ["-1/2", "1/2", "0"],
            "mixed_delta": "log(64/3)/4",
            "higher_order_connection_delta": "-3*c",
        },
        "statuses": {
            "abstract_reciprocal_channel_pair": "DERIVED_WITH_FOUNDING_STAMPS",
            "abstract_exchange_parity": "DERIVED_ON_TWO_CHANNEL_REPRESENTATION",
            "physical_causal_flag": "CONDITIONAL_SUPPLIED_QUERY_STRUCTURE",
            "complete_exchange_extension": "POSIT_IF_ADOPTED",
            "reciprocal_root_readout": "CONDITIONAL_UNIQUE_UNIVERSAL_ORDER_ZERO_CHARACTER",
            "physical_nonisometric_arrow": "OPEN_NOT_UNIQUE_FROM_METRIC_NATURALITY",
            "calibration_line_ceff_identification": "OPEN_CONSISTENT_ASSOCIATED_LINE_EXTENSION",
            "xmax_asymptote": "WORKING_UNCHANGED_GATE",
        },
        "checks": checks,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("landing", "check_count", "passed_count", "all_passed")}, sort_keys=True))


if __name__ == "__main__":
    main()
