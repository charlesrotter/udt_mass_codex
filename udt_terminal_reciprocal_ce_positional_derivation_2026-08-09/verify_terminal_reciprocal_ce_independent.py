#!/usr/bin/env python3
"""Independent standard-library verification of the load-bearing finite claims."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent


def det2(g: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> Fraction:
    return g[0][0] * g[1][1] - g[0][1] * g[1][0]


def gram2(
    c0: tuple[Fraction, Fraction, Fraction, Fraction],
    c1: tuple[Fraction, Fraction, Fraction, Fraction],
) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    signs = (-1, 1, 1, 1)

    def dot(a: tuple[Fraction, ...], b: tuple[Fraction, ...]) -> Fraction:
        return sum(Fraction(s) * x * y for s, x, y in zip(signs, a, b))

    return ((dot(c0, c0), dot(c0, c1)), (dot(c1, c0), dot(c1, c1)))


def terminal_depth(g: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> float:
    return 0.25 * math.log(float(-det2(g))) - 0.5 * math.log(float(-g[0][0]))


def main() -> int:
    rows: list[dict[str, object]] = []

    def check(name: str, condition: bool, detail: object = "") -> None:
        rows.append({"name": name, "passed": bool(condition), "detail": str(detail)})

    # Frozen source replay uses independent parsing and hashlib.
    manifest = (PACKAGE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()
    check("manifest_header", manifest[0].split("\t") == ["sha256", "path", "source_ref"])
    check("manifest_member_count", len(manifest) - 1 == 20, len(manifest) - 1)
    for index, line in enumerate(manifest[1:], start=1):
        digest, relpath, source_ref = line.split("\t")
        if source_ref == "WORKTREE":
            data = (ROOT / relpath).read_bytes()
        else:
            commit, git_path = source_ref.split(":", 1)
            data = subprocess.check_output(["git", "show", f"{commit}:{git_path}"], cwd=ROOT)
        check(f"manifest_{index:02d}", hashlib.sha256(data).hexdigest() == digest, relpath)

    # Rational complete-pair witnesses, independently implemented.
    mix = gram2(
        (Fraction(1, 2), Fraction(0), Fraction(1, 4), Fraction(0)),
        (Fraction(0), Fraction(2), Fraction(0), Fraction(0)),
    )
    check("mix_g00", mix[0][0] == Fraction(-3, 16), mix)
    check("mix_g01", mix[0][1] == 0, mix)
    check("mix_g11", mix[1][1] == 4, mix)
    check("mix_det", det2(mix) == Fraction(-3, 4), det2(mix))
    mix_expected = 0.25 * math.log(64.0 / 3.0)
    check("mix_depth", abs(terminal_depth(mix) - mix_expected) < 1e-14, terminal_depth(mix))
    check("mix_not_quotient", abs(terminal_depth(mix) - math.log(2.0)) > 1e-3)

    orchestra = gram2(
        (Fraction(1, 2), Fraction(0), Fraction(1, 4), Fraction(0)),
        (Fraction(0), Fraction(2), Fraction(1, 3), Fraction(0)),
    )
    check("orchestra_g00", orchestra[0][0] == Fraction(-3, 16), orchestra)
    check("orchestra_g01", orchestra[0][1] == Fraction(1, 12), orchestra)
    check("orchestra_g11", orchestra[1][1] == Fraction(37, 9), orchestra)
    check("orchestra_det", det2(orchestra) == Fraction(-7, 9), det2(orchestra))
    schur = orchestra[1][1] - orchestra[0][1] * orchestra[1][0] / orchestra[0][0]
    check("orchestra_schur", schur == Fraction(112, 27), schur)
    orchestra_expected = 0.25 * math.log(1792.0 / 81.0)
    check(
        "orchestra_depth",
        abs(terminal_depth(orchestra) - orchestra_expected) < 1e-14,
        terminal_depth(orchestra),
    )

    # Numerical property sweep is only an algebra sanity check, not solution-space sampling.
    for i, (clock, ruler, shift) in enumerate(
        [
            (0.5, 2.0, 0.0),
            (0.8, 1.3, 0.2),
            (3.0, 0.25, -0.1),
            (1.0e-4, 9.0, 2.0),
        ],
        start=1,
    ):
        g00 = -(clock * clock)
        g01 = -(clock * clock) * shift
        g11 = ruler * ruler - clock * clock * shift * shift
        determinant = g00 * g11 - g01 * g01
        recovered_clock = math.sqrt(-g00)
        recovered_ruler = math.sqrt(g11 - g01 * g01 / g00)
        depth_a = 0.5 * math.log(recovered_ruler / recovered_clock)
        depth_b = 0.25 * math.log(-determinant) - 0.5 * math.log(-g00)
        check(f"sweep_{i}_clock", abs(recovered_clock - clock) < 1e-12)
        check(f"sweep_{i}_ruler", abs(recovered_ruler - ruler) < 1e-12)
        check(f"sweep_{i}_depth", abs(depth_a - depth_b) < 1e-12)
        inv_plus = ruler / clock - shift
        inv_minus = ruler / clock + shift
        check(f"sweep_{i}_two_way", abs(0.5 * (inv_plus + inv_minus) - ruler / clock) < 1e-12)

    # Common scale cancels; reciprocal scaling adds.
    for i, (clock, ruler, scale, depth) in enumerate(
        [(0.5, 2.0, 7.0, 0.3), (1.2, 0.7, 0.2, -1.1)], start=1
    ):
        original = 0.5 * math.log(ruler / clock)
        common = 0.5 * math.log((scale * ruler) / (scale * clock))
        reciprocal = 0.5 * math.log((math.exp(depth) * ruler) / (math.exp(-depth) * clock))
        check(f"scale_{i}_common", abs(common - original) < 1e-13)
        check(f"scale_{i}_reciprocal", abs(reciprocal - (original + depth)) < 1e-13)

    # Translation imbalance cannot be an additive depth.
    d1 = 0.5 * math.log(2.0 / 1.0)
    d2 = 0.5 * math.log(2.0 / 1.0)
    dsum = 0.5 * math.log(4.0 / 2.0)
    check("translation_nonadditive", abs(dsum - (d1 + d2)) > 1e-3, (d1, d2, dsum))

    passed = sum(int(row["passed"]) for row in rows)
    result = {
        "implementation": "independent_python_stdlib_no_sympy_import",
        "checks_total": len(rows),
        "checks_passed": passed,
        "checks_failed": len(rows) - passed,
        "rows": rows,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if passed == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
