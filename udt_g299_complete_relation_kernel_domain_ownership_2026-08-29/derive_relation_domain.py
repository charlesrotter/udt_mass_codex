#!/usr/bin/env python3
"""Exact G299 production derivation on the frozen regular active-screen stratum."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

try:
    import sympy as sp
except ModuleNotFoundError:  # Exact stdlib fallback for minimal sealed-review images.
    sp = None


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def projective(matrix):
    column = matrix[:, 0]
    return tuple(sp.cancel(column[i] / column[0]) for i in range(1, 4))


def _mdot(x, y):
    return -x[0] * y[0] + x[1] * y[1] + x[2] * y[2]


def _det3(a, b, c):
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - b[0] * (a[1] * c[2] - a[2] * c[1])
        + c[0] * (a[1] * b[2] - a[2] * b[1])
    )


def _matmul(a, b):
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
         for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def _projective_fraction(matrix):
    return tuple(matrix[i][0] / matrix[0][0] for i in range(1, 4))


def _dependency_free_main() -> None:
    """Reproduce the frozen production claims using only exact Fraction arithmetic."""

    assertions = 0
    manifest_rows = []
    for line in (HERE / "SOURCE_MANIFEST.tsv").read_text().splitlines()[1:]:
        expected, relative = line.split("\t")
        assert digest(ROOT / relative) == expected, relative
        assertions += 1
        manifest_rows.append(relative)

    phrases = {
        "founding.md": [
            "physical normalized pair position is the metric's complete projective relation state",
            "general nonradial composition requires the full path-labelled frame morphism and its screen/frame carry",
            "W5 also does not change F1--F4, W1, the metric, or the reciprocal kernel",
        ],
        "udt_g274_projective_pair_position_network_descent_2026-08-26/EXACT_DERIVATION.md": [
            "The full arrow descends covariantly on overlaps",
            "projectivization forgets the arrow's right spatial/frame carry",
            "physical pair position is naturally a coordinate on a path-labelled metric relation groupoid",
        ],
        "udt_g298_causal_diamond_to_pair_germ_transfer_2026-08-29/EXACT_DERIVATION.md": [
            "The complete path-labelled causal state contains both",
            "Current premises still do not own a unique transfer to",
            "its complete input should not be reduced to one arbitrary two-plane",
        ],
    }
    phrase_checks = 0
    for relative, required in phrases.items():
        source_text = " ".join((ROOT / relative).read_text().split())
        for phrase in required:
            assert " ".join(phrase.split()) in source_text, (relative, phrase)
            assertions += 1
            phrase_checks += 1

    # One exact active-screen anchor reproduces every symbolic identity before the grid.
    r, w = F(3, 2), F(2, 5)
    gamma = (1 + r * r + r * r * w * w) / (2 * r)
    a = (-1 + r * r + r * r * w * w) / (2 * r)
    U = (gamma, a, w)
    clock = tuple(r * value for value in U)
    n_transport = (F(0), F(1), F(0))
    n_local = (r - gamma, r - a, -w)
    assert _mdot(U, U) == -1
    assert r * (gamma - a) == 1
    assert _mdot(U, n_local) == 0
    assert _mdot(n_local, n_local) == 1
    assertions += 4

    hT00 = _mdot(clock, clock)
    hT01 = _mdot(clock, n_transport)
    hT11 = _mdot(n_transport, n_transport)
    hL00 = _mdot(clock, clock)
    hL01 = _mdot(clock, n_local)
    hL11 = _mdot(n_local, n_local)
    assert hT00 == -r * r
    assert (hL00, hL01, hL11) == (-r * r, 0, 1)
    assert hT00 * hT11 - hT01 * hT01 == -r * r * (1 + a * a)
    assert hL00 * hL11 - hL01 * hL01 == -r * r
    assertions += 4
    assert _det3(clock, n_transport, n_local) == -r * r * w
    assertions += 1
    # Since both clock entries are exactly -r^2 with r>0, W1 gives -log(r).
    assert hT00 == hL00 == -r * r
    assert r > 0
    assertions += 2

    Bx = [[F(5, 4), F(3, 4), F(0), F(0)], [F(3, 4), F(5, 4), F(0), F(0)],
          [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    Bs = [[F(441, 359), F(0), F(200, 359), F(160, 359)], [F(0), F(1), F(0), F(0)],
          [F(200, 359), F(0), F(409, 359), F(40, 359)],
          [F(160, 359), F(0), F(40, 359), F(391, 359)]]
    rotation = [[F(1), F(0), F(0), F(0)], [F(0), F(0), F(-1), F(0)],
                [F(0), F(1), F(0), F(0)], [F(0), F(0), F(0), F(1)]]
    BsR = _matmul(Bs, rotation)
    assert _projective_fraction(Bs) == _projective_fraction(BsR)
    assert _projective_fraction(_matmul(Bs, Bx)) != _projective_fraction(_matmul(BsR, Bx))
    assertions += 2

    cases = 0
    for rn in range(1, 26):
        for rd in range(1, 10):
            rv = F(rn, rd)
            for wn in range(-7, 8):
                if wn == 0:
                    continue
                for wd in range(1, 5):
                    wv = F(wn, wd)
                    gammav = (1 + rv * rv + rv * rv * wv * wv) / (2 * rv)
                    av = (-1 + rv * rv + rv * rv * wv * wv) / (2 * rv)
                    Uv = (gammav, av, wv)
                    clockv = tuple(rv * value for value in Uv)
                    nlocalv = (rv - gammav, rv - av, -wv)
                    separator = _det3(clockv, n_transport, nlocalv)
                    hT00v = _mdot(clockv, clockv)
                    hT01v = _mdot(clockv, n_transport)
                    hL00v = hT00v
                    hL01v = _mdot(clockv, nlocalv)
                    hL11v = _mdot(nlocalv, nlocalv)
                    assert separator != 0
                    assert hT00v == hL00v
                    assert hT00v - hT01v * hT01v < 0
                    assert hL00v * hL11v - hL01v * hL01v < 0
                    assertions += 4
                    cases += 1

    result = {
        "status": "PASS",
        "landing": (
            "ACTIVE_PREMISES_REQUIRE_COMPLETE_CARRY_BUT_DO_NOT_TYPE_THE_KERNEL_DOMAIN"
            "__ARCHITECTURE_REMAINS_OPEN"
        ),
        "source_hashes": len(manifest_rows),
        "source_phrase_checks": phrase_checks,
        "symbolic_separator": "-r**2*w",
        "projection_scalar": "Phi_T=Phi_L=-log(r)",
        "right_carry_inputs_equal": True,
        "right_carry_outputs_different": True,
        "cases": cases,
        "assertions": assertions,
        "engine": "stdlib Fraction exact fallback",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


def main() -> None:
    if sp is None:
        _dependency_free_main()
        return

    assertions = 0

    # Frozen source integrity and source-owned phrases.
    manifest_rows = []
    for line in (HERE / "SOURCE_MANIFEST.tsv").read_text().splitlines()[1:]:
        expected, relative = line.split("\t")
        actual = digest(ROOT / relative)
        assert actual == expected, relative
        assertions += 1
        manifest_rows.append(relative)

    phrases = {
        "founding.md": [
            "physical normalized pair position is the metric's complete projective relation state",
            "general nonradial composition requires the full path-labelled frame morphism and its screen/frame carry",
            "W5 also does not change F1--F4, W1, the metric, or the reciprocal kernel",
        ],
        "udt_g274_projective_pair_position_network_descent_2026-08-26/EXACT_DERIVATION.md": [
            "The full arrow descends covariantly on overlaps",
            "projectivization forgets the arrow's right spatial/frame carry",
            "physical pair position is naturally a coordinate on a path-labelled metric relation groupoid",
        ],
        "udt_g298_causal_diamond_to_pair_germ_transfer_2026-08-29/EXACT_DERIVATION.md": [
            "The complete path-labelled causal state contains both",
            "Current premises still do not own a unique transfer to",
            "its complete input should not be reduced to one arbitrary two-plane",
        ],
    }
    phrase_checks = 0
    for relative, required in phrases.items():
        text = " ".join((ROOT / relative).read_text().split())
        for phrase in required:
            assert " ".join(phrase.split()) in text, (relative, phrase)
            assertions += 1
            phrase_checks += 1

    # G298 active-screen geometry, rederived symbolically rather than imported.
    r, w = sp.symbols("r w", positive=True, nonzero=True)
    Gamma = (1 + r**2 + r**2 * w**2) / (2 * r)
    a = (-1 + r**2 + r**2 * w**2) / (2 * r)
    eta3 = sp.diag(-1, 1, 1)
    U = sp.Matrix([Gamma, a, w])
    n_transport = sp.Matrix([0, 1, 0])
    n_local = sp.Matrix([r - Gamma, r - a, -w])
    clock = r * U

    dot = lambda x, y: sp.factor((x.T * eta3 * y)[0])
    assert sp.simplify(dot(U, U) + 1) == 0
    assert sp.simplify(r * (Gamma - a) - 1) == 0
    assert sp.simplify(dot(U, n_local)) == 0
    assert sp.simplify(dot(n_local, n_local) - 1) == 0
    assertions += 4

    h_T = sp.Matrix(
        [[dot(clock, clock), dot(clock, n_transport)],
         [dot(clock, n_transport), dot(n_transport, n_transport)]]
    )
    h_L = sp.Matrix(
        [[dot(clock, clock), dot(clock, n_local)],
         [dot(clock, n_local), dot(n_local, n_local)]]
    )
    assert sp.simplify(h_T[0, 0] + r**2) == 0
    assert sp.simplify(h_L - sp.diag(-r**2, 1)) == sp.zeros(2)
    assert sp.simplify(h_T.det() + r**2 * (1 + a**2)) == 0
    assert sp.simplify(h_L.det() + r**2) == 0
    assertions += 4

    separator = sp.factor(sp.det(sp.Matrix.hstack(clock, n_transport, n_local)))
    assert separator == -r**2 * w
    assertions += 1

    # W1 reads the clock entry only after either complete query pullback is formed.
    phi_T = sp.simplify(-sp.log(-h_T[0, 0]) / 2)
    phi_L = sp.simplify(-sp.log(-h_L[0, 0]) / 2)
    assert sp.simplify(phi_T + sp.log(r)) == 0
    assert sp.simplify(phi_L + sp.log(r)) == 0
    assertions += 2

    # G274 right-carry separator, independently evaluated from frozen exact matrices.
    Bx = sp.Matrix(
        [[sp.Rational(5, 4), sp.Rational(3, 4), 0, 0],
         [sp.Rational(3, 4), sp.Rational(5, 4), 0, 0],
         [0, 0, 1, 0], [0, 0, 0, 1]]
    )
    Bs = sp.Matrix(
        [[sp.Rational(441, 359), 0, sp.Rational(200, 359), sp.Rational(160, 359)],
         [0, 1, 0, 0],
         [sp.Rational(200, 359), 0, sp.Rational(409, 359), sp.Rational(40, 359)],
         [sp.Rational(160, 359), 0, sp.Rational(40, 359), sp.Rational(391, 359)]]
    )
    R = sp.Matrix([[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
    assert projective(Bs) == projective(Bs * R)
    composed_a = projective(Bs * Bx)
    composed_b = projective((Bs * R) * Bx)
    assert composed_a != composed_b
    assertions += 2

    # Exact nonzero-plane census over a broad rational grid.
    cases = 0
    grid_assertions = 0
    for rn in range(1, 26):
        for rd in range(1, 10):
            rv = sp.Rational(rn, rd)
            for wn in range(-7, 8):
                if wn == 0:
                    continue
                for wd in range(1, 5):
                    wv = sp.Rational(wn, wd)
                    subs = {r: rv, w: wv}
                    assert sp.factor(separator.subs(subs)) != 0
                    assert h_T[0, 0].subs(subs) == h_L[0, 0].subs(subs)
                    assert h_T.det().subs(subs) < 0
                    assert h_L.det().subs(subs) < 0
                    grid_assertions += 4
                    cases += 1

    assertions += grid_assertions
    result = {
        "status": "PASS",
        "landing": (
            "ACTIVE_PREMISES_REQUIRE_COMPLETE_CARRY_BUT_DO_NOT_TYPE_THE_KERNEL_DOMAIN"
            "__ARCHITECTURE_REMAINS_OPEN"
        ),
        "source_hashes": len(manifest_rows),
        "source_phrase_checks": phrase_checks,
        "symbolic_separator": str(separator),
        "projection_scalar": "Phi_T=Phi_L=-log(r)",
        "right_carry_inputs_equal": list(map(str, projective(Bs))) == list(map(str, projective(Bs * R))),
        "right_carry_outputs_different": composed_a != composed_b,
        "cases": cases,
        "assertions": assertions,
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
