#!/usr/bin/env python3
"""Exact symbolic and rational atlas for the preregistered pair reachability map."""

from __future__ import annotations

import csv
import itertools
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent


def symbolic_derivation() -> dict[str, str]:
    t, ell = sp.symbols("t ell", positive=True)
    b, p, m, n = sp.symbols("b p m n", real=True)
    A, L2, db = sp.symbols("A L2 db", real=True)

    h0 = sp.Matrix([[-t, -t * b], [-t * b, ell - t * b**2]])
    gram = sp.Matrix([[p, p * b + m], [p * b + m, p * b**2 + 2 * b * m + n]])
    shear_inverse = sp.Matrix([[1, -b], [0, 1]])
    h0_shift = sp.simplify(shear_inverse.T * h0 * shear_inverse)
    gram_shift = sp.simplify(shear_inverse.T * gram * shear_inverse)
    h_shift = sp.simplify(h0_shift + gram_shift)

    det_h = sp.factor(h_shift.det())
    clock2 = sp.factor(-h_shift[0, 0])
    beta_shift = sp.factor(h_shift[0, 1] / h_shift[0, 0])
    ruler2 = sp.factor(h_shift[1, 1] - h_shift[0, 1] ** 2 / h_shift[0, 0])

    inverse_gram = sp.Matrix(
        [[t - A, -A * db], [-A * db, L2 - ell - A * db**2]]
    )
    inverse_det = sp.factor(inverse_gram.det())
    target_h = sp.Matrix([[-A, -A * db], [-A * db, L2 - A * db**2]])
    reconstructed_h = sp.simplify(sp.diag(-t, ell) + inverse_gram)
    r00, r01, r10, r11 = sp.symbols("r00 r01 r10 r11", real=True)
    pair_change = sp.Matrix([[r00, r01], [r10, r11]])
    pair_congruence = sp.simplify(
        (pair_change.T * h_shift * pair_change).det()
        - pair_change.det() ** 2 * h_shift.det()
    )
    q00, q01, q10, q11 = sp.symbols("q00 q01 q10 q11", real=True)
    c00, c01, c10, c11 = sp.symbols("c00 c01 c10 c11", real=True)
    screen_coframe = sp.Matrix([[q00, q01], [q10, q11]])
    relative_displacement = sp.Matrix([[c00, c01], [c10, c11]])
    screen_rotation = sp.Matrix([[0, -1], [1, 0]])
    screen_gram = (screen_coframe * relative_displacement).T * (
        screen_coframe * relative_displacement
    )
    rotated_screen_gram = (
        screen_rotation * screen_coframe * relative_displacement
    ).T * (screen_rotation * screen_coframe * relative_displacement)

    checks = {
        "base_shear": h0_shift == sp.diag(-t, ell),
        "gram_shear": gram_shift == sp.Matrix([[p, m], [m, n]]),
        "completed_form": h_shift == sp.Matrix([[p - t, m], [m, ell + n]]),
        "determinant": sp.simplify(det_h - ((p - t) * (ell + n) - m**2)) == 0,
        "clock": sp.simplify(clock2 - (t - p)) == 0,
        "beta": sp.simplify(beta_shift + m / (t - p)) == 0,
        "ruler": sp.simplify(ruler2 - (ell + n + m**2 / (t - p))) == 0,
        "inverse_det": sp.simplify(
            inverse_det - ((t - A) * (L2 - ell) - A * t * db**2)
        ) == 0,
        "inverse_reconstruction": reconstructed_h == target_h,
        "target_det": sp.simplify(target_h.det() + A * L2) == 0,
        "pair_congruence_determinant": pair_congruence == 0,
        "screen_rotation_gram": sp.simplify(rotated_screen_gram - screen_gram) == sp.zeros(2),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    return {
        "checks": str(sum(checks.values())),
        "det_h": str(det_h),
        "T_pair_squared": str(clock2),
        "beta_pair_minus_beta0": str(beta_shift),
        "L_pair_squared": str(ruler2),
        "inverse_gram_det": str(inverse_det),
        "target_det": str(sp.factor(target_h.det())),
    }


def fstr(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def determinant2(matrix: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> Fraction:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def gram_rank(p: Fraction, m: Fraction, n: Fraction) -> int:
    if p == 0 and m == 0 and n == 0:
        return 0
    return 1 if p * n == m * m else 2


def signature_label(det_h: Fraction) -> str:
    if det_h < 0:
        return "LORENTZIAN"
    if det_h == 0:
        return "DEGENERATE"
    return "POSITIVE_DEFINITE"


def rational_atlas() -> tuple[list[dict[str, str]], dict[str, int]]:
    # Mathematical verification controls only; no physical values are assigned.
    t, ell, b = Fraction(4), Fraction(9), Fraction(2, 3)
    entries = [Fraction(-2), Fraction(-1), Fraction(-1, 2), Fraction(0),
               Fraction(1, 2), Fraction(1), Fraction(2)]
    grams: set[tuple[Fraction, Fraction, Fraction]] = set()
    for a, c, d, e in itertools.product(entries, repeat=4):
        p = a * a + c * c
        m = a * d + c * e
        n = d * d + e * e
        grams.add((p, m, n))

    # Exact controls for all three completed signatures outside the terminal chart.
    grams.update(
        {
            (Fraction(4), Fraction(0), Fraction(1)),
            (Fraction(4), Fraction(2), Fraction(4)),
            (Fraction(5), Fraction(0), Fraction(7)),
            (Fraction(5), Fraction(4), Fraction(7)),
            (Fraction(5), Fraction(5), Fraction(7)),
        }
    )

    rows: list[dict[str, str]] = []
    for index, (p, m, n) in enumerate(sorted(grams), start=1):
        assert p >= 0 and n >= 0 and m * m <= p * n
        h_shift = ((p - t, m), (m, ell + n))
        det_h = determinant2(h_shift)
        sig = signature_label(det_h)
        terminal = p < t
        row = {
            "case_id": f"P{index:04d}",
            "p": fstr(p),
            "m": fstr(m),
            "n": fstr(n),
            "gram_rank": str(gram_rank(p, m, n)),
            "det_h": fstr(det_h),
            "signature": sig,
            "a_calibrated_terminal": str(terminal).lower(),
        }
        if terminal:
            A = t - p
            db = -m / A
            L2 = ell + n + m * m / A
            inverse = ((t - A, -A * db), (-A * db, L2 - ell - A * db * db))
            assert inverse == ((p, m), (m, n))
            assert (t - A) * (L2 - ell) >= A * t * db * db
            assert A > 0 and L2 >= ell
            assert det_h == -A * L2
            row.update({"T2": fstr(A), "L2": fstr(L2), "delta_beta": fstr(db)})
        else:
            row.update({"T2": "", "L2": "", "delta_beta": ""})
        rows.append(row)

    counts: dict[str, int] = {}
    for row in rows:
        keys = [
            f"signature_{row['signature']}",
            f"gram_rank_{row['gram_rank']}",
            f"terminal_{row['a_calibrated_terminal']}",
        ]
        for key in keys:
            counts[key] = counts.get(key, 0) + 1
    required = [
        "signature_LORENTZIAN", "signature_DEGENERATE", "signature_POSITIVE_DEFINITE",
        "gram_rank_0", "gram_rank_1", "gram_rank_2", "terminal_true", "terminal_false",
    ]
    assert len(rows) >= 250 and all(counts.get(k, 0) > 0 for k in required), counts
    return rows, counts


def write_outputs() -> None:
    symbolic = symbolic_derivation()
    rows, counts = rational_atlas()
    atlas_path = ROOT / "RATIONAL_ATLAS.tsv"
    with atlas_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    result = {
        "status": "EXACT_SYMBOLIC_AND_RATIONAL_ATLAS_COMPLETE",
        "symbolic": symbolic,
        "rational_case_count": len(rows),
        "counts": counts,
        "maximum_conclusion": (
            "EXACT_ZERO_ORDER_REACHABILITY_CLASSIFICATION_FOR_ALL_PSD_GRAM_ADDITIONS_"
            "TO_ONE_FIXED_SYMBOLIC_A_CALIBRATED_BASE_PAIR_METRIC"
        ),
    }
    (ROOT / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    write_outputs()
