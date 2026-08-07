#!/usr/bin/env python3
"""Derive the preregistered kernel-plane curvature on the global quaternion sphere.

This is the append-only intrinsic route authorized by
PREREGISTRATION_METHOD_REFINEMENT.md.  It does not replace the preserved
stereographic attempt.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
Q0, Q1, Q2, Q3 = sp.symbols("q0 q1 q2 q3", real=True)
Q = (Q0, Q1, Q2, Q3)
T = sp.symbols("defect_inverse")
OWNERS = ("C04", "C08", "C09", "C10")


def read_tsv(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_sources() -> int:
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == len({row["path"] for row in rows}) == 114
    for row in rows:
        content = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob"]],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        assert len(content) == int(row["bytes"])
        assert digest(content) == row["sha256"]
    manifest_digest = digest((HERE / "SOURCE_MANIFEST.tsv").read_bytes())
    assert manifest_digest == (HERE / "SOURCE_MANIFEST.sha256").read_text().strip()
    return len(rows)


def directional(vector, expression):
    return sp.expand(sum(vector[i] * sp.diff(expression, Q[i]) for i in range(4)))


X1 = (-Q1, Q0, Q3, -Q2)
X2 = (-Q2, -Q3, Q0, Q1)
X3 = (-Q3, Q2, -Q1, Q0)
X = (X1, X2, X3)


F12 = sp.expand(Q0 * Q1**2 + 3 * Q0 * Q2**2 + 2 * Q1 * Q2 * Q3)
F13 = sp.expand(Q0**2 * Q1 + 3 * Q0 * Q2 * Q3 - 2 * Q1 * Q2**2)
F23 = sp.expand(3 * Q0**2 * Q2 - Q0 * Q1 * Q3 + 2 * Q1**2 * Q2)
DEFECT = sp.expand(F12**2 + F13**2 + F23**2)
SPHERE = Q0**2 + Q1**2 + Q2**2 + Q3**2 - 1
CONTACT_A = sp.expand(Q0**2 * Q1**2 - 3 * Q0**2 * Q2**2 - 2 * Q1**2 * Q2**2)


DETA = (
    sp.expand(directional(X1, F23) - directional(X2, F13)),
    sp.expand(-directional(X3, F13) + 2 * F23),
    sp.expand(-directional(X3, F23) - 2 * F13),
)


def primitive_integer_polynomial(expression):
    numerator, denominator = sp.fraction(sp.cancel(expression))
    poly = sp.Poly(numerator, *Q, domain=sp.QQ)
    denominator_factor, poly = poly.clear_denoms(convert=True)
    content, poly = poly.primitive()
    if poly.LC() < 0:
        poly = -poly
    return poly, sp.factor(denominator), int(denominator_factor), int(content)


def sphere_remainder(expression):
    """Return the exact q0-degree<2 representative modulo the sphere ideal."""
    coefficient_field = sp.QQ.frac_field(Q1, Q2, Q3)
    dividend = sp.Poly(expression, Q0, domain=coefficient_field)
    divisor = sp.Poly(SPHERE, Q0, domain=coefficient_field)
    quotient, remainder = sp.div(dividend, divisor)
    remainder_poly = sp.Poly(sp.cancel(remainder.as_expr()), *Q, domain=sp.QQ)
    # Independent exact reconstruction in the coefficient field.
    assert sp.expand(dividend.as_expr() - quotient.as_expr() * divisor.as_expr() - remainder.as_expr()) == 0
    return remainder_poly


def profile(candidate_id: str):
    u = 3 + Q0**2 + 2 * Q1**2 + 4 * Q2**2 + 8 * Q3**2
    v = 1 + sp.Rational(1, 10) * (Q0**2 + 3 * Q1**2 + 7 * Q2**2 + 9 * Q3**2)
    r = 1 + sp.Rational(1, 10) * (2 * Q0**2 + 5 * Q1**2 + 11 * Q2**2 + 13 * Q3**2)
    b = sp.Rational(1, 10) * (
        Q0 * Q1 + 2 * Q0 * Q2 + 3 * Q0 * Q3 + 5 * Q1 * Q2
        + 7 * Q1 * Q3 + 11 * Q2 * Q3
    )
    if candidate_id == "C04":
        return u, v, sp.S.One, sp.S.Zero
    area = {"C08": v, "C09": v / u, "C10": u * v}[candidate_id]
    return u, area, r, b


def exact_p_numerator_denominator(candidate_id: str):
    """Return exact polynomial N,D with P=u*S=N/D.

    Keeping the registered positive profile denominators factored avoids the
    large rational cancellations that defeated the first generic expansion.
    No factor is dropped.
    """
    u, area, r, b = profile(candidate_id)
    v_numerator = 10 + Q0**2 + 3 * Q1**2 + 7 * Q2**2 + 9 * Q3**2
    if candidate_id == "C04":
        assert sp.expand(10 * area - v_numerator) == 0
        assert r == 1 and b == 0
        numerator = sp.expand(
            10 * u**2 * F12**2
            + u * v_numerator * (F13**2 + F23**2)
        )
        denominator = sp.Integer(10)
    else:
        r_numerator = 10 + 2 * Q0**2 + 5 * Q1**2 + 11 * Q2**2 + 13 * Q3**2
        b_numerator = (
            Q0 * Q1 + 2 * Q0 * Q2 + 3 * Q0 * Q3 + 5 * Q1 * Q2
            + 7 * Q1 * Q3 + 11 * Q2 * Q3
        )
        shear = sp.expand(b_numerator * F13 - r_numerator * F23)
        weight = {"C08": u, "C09": sp.S.One, "C10": u**2}[candidate_id]
        expected_area = {"C08": v_numerator / 10, "C09": v_numerator / (10 * u), "C10": u * v_numerator / 10}[candidate_id]
        assert sp.cancel(area - expected_area) == 0
        assert sp.expand(10 * r - r_numerator) == 0
        assert sp.expand(10 * b - b_numerator) == 0
        numerator = sp.expand(
            1000 * r_numerator**2 * u**2 * F12**2
            + weight * v_numerator * r_numerator**2 * shear**2
            + 10000 * weight * v_numerator * F13**2
        )
        denominator = sp.expand(1000 * r_numerator**2)

    # The assertions above prove the registered profile substitutions exactly.
    # N/D then follows by literal common-denominator arithmetic; retaining N and
    # D separately is what prevents a gratuitous rational-expression blow-up.
    return numerator, denominator


def chart_equivalence_proof():
    """Prove the preregistered intrinsic d(eta) equals its chart derivative."""
    x, y, z = sp.symbols("x y z", real=True)
    rho2 = x**2 + y**2 + z**2
    den = 1 + rho2
    chart_q = ((1 - rho2) / den, 2 * x / den, 2 * y / den, 2 * z / den)
    substitutions = dict(zip(Q, chart_q))
    d2 = den**2
    sigmas = (
        sp.Matrix((
            2 * (x**2 - y**2 - z**2 + 1) / d2,
            4 * (x * y + z) / d2,
            4 * (x * z - y) / d2,
        )),
        sp.Matrix((
            4 * (x * y - z) / d2,
            -2 * (x**2 - y**2 + z**2 - 1) / d2,
            4 * (x + y * z) / d2,
        )),
        sp.Matrix((
            4 * (x * z + y) / d2,
            -4 * (x - y * z) / d2,
            -2 * (x**2 + y**2 - z**2 - 1) / d2,
        )),
    )
    f13 = sp.cancel(F13.subs(substitutions))
    f23 = sp.cancel(F23.subs(substitutions))
    eta = sp.Matrix([sp.cancel(v) for v in f13 * sigmas[0] + f23 * sigmas[1]])
    direct = (
        sp.cancel(sp.diff(eta[1], x) - sp.diff(eta[0], y)),
        sp.cancel(sp.diff(eta[2], x) - sp.diff(eta[0], z)),
        sp.cancel(sp.diff(eta[2], y) - sp.diff(eta[1], z)),
    )
    coordinate_pairs = ((0, 1), (0, 2), (1, 2))
    coframe_pairs = ((0, 1), (0, 2), (1, 2))
    pulled = []
    for coordinate_a, coordinate_b in coordinate_pairs:
        component = 0
        for coefficient, (frame_i, frame_j) in zip(DETA, coframe_pairs):
            wedge = (
                sigmas[frame_i][coordinate_a] * sigmas[frame_j][coordinate_b]
                - sigmas[frame_i][coordinate_b] * sigmas[frame_j][coordinate_a]
            )
            component += coefficient.subs(substitutions) * wedge
        pulled.append(sp.cancel(component))
    differences = [sp.cancel(a - b) for a, b in zip(direct, pulled)]
    assert differences == [0, 0, 0]

    # The coframe/vector duality and Maurer-Cartan signs are also exact on S^3.
    gram = sp.Matrix(X) * sp.Matrix(X).T
    expected_gram = (SPHERE + 1) * sp.eye(3)
    assert all(sp.expand(v) == 0 for v in (gram - expected_gram))
    brackets = []
    for first, second in ((X1, X2), (X2, X3), (X3, X1)):
        bracket = tuple(
            sp.expand(directional(first, second[i]) - directional(second, first[i]))
            for i in range(4)
        )
        brackets.append(bracket)
    assert all(sp.expand(brackets[0][i] - 2 * X3[i]) == 0 for i in range(4))
    assert all(sp.expand(brackets[1][i] - 2 * X1[i]) == 0 for i in range(4))
    assert all(sp.expand(brackets[2][i] - 2 * X2[i]) == 0 for i in range(4))
    contact_obstruction = sp.expand(F13 * DETA[2] - F23 * DETA[1])
    assert sp.expand(contact_obstruction - 2 * CONTACT_A * (SPHERE + 1)) == 0
    result = {
        "schema": "udt-intrinsic-chart-equivalence-1.0",
        "status": "PASS_EXACT_IDENTITY",
        "chart_deta_minus_intrinsic_pullback": ["0", "0", "0"],
        "coframe_duality_mod_sphere": "PASS",
        "maurer_cartan_brackets": ["[X1,X2]=2X3", "[X2,X3]=2X1", "[X3,X1]=2X2"],
        "maurer_cartan_forms": [
            "d sigma1=-2 sigma2 wedge sigma3",
            "d sigma2=-2 sigma3 wedge sigma1",
            "d sigma3=-2 sigma1 wedge sigma2",
        ],
        "contact_obstruction": "eta wedge d eta=2*A*(q0^2+q1^2+q2^2+q3^2)*volume",
        "unit_sphere_contact_stratum": str(CONTACT_A),
    }
    target = HERE / "COFRAME_CHART_EQUIVALENCE.json"
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def derive_candidate(candidate_id: str, saturate: bool):
    numerator, p_denominator = exact_p_numerator_denominator(candidate_id)
    d_numerator = tuple(directional(vector, numerator) for vector in X)
    d_denominator = tuple(directional(vector, p_denominator) for vector in X)
    # For P=N/D, D^2 B is the following exact polynomial triple.
    derivative_numerators = tuple(
        sp.expand(d_numerator[i] * p_denominator - numerator * d_denominator[i])
        for i in range(3)
    )
    B = (
        sp.expand(
            2 * numerator * p_denominator * DETA[0]
            - (derivative_numerators[0] * F23 - derivative_numerators[1] * F13)
        ),
        sp.expand(2 * numerator * p_denominator * DETA[1] + derivative_numerators[2] * F13),
        sp.expand(2 * numerator * p_denominator * DETA[2] + derivative_numerators[2] * F23),
    )

    polynomial_rows = []
    polynomials = []
    reduced_polynomials = []
    polynomial_hashes = {}
    for label, expression in zip(("12", "13", "23"), B):
        poly, component_denominator, clear_factor, content = primitive_integer_polynomial(expression)
        polynomials.append(poly)
        target = HERE / f"{candidate_id}_INTRINSIC_B_{label}.txt"
        target.write_text(str(poly.as_expr()) + "\n", encoding="utf-8")
        polynomial_hashes[target.name] = digest(target.read_bytes())
        reduced = sphere_remainder(poly.as_expr())
        _factor, reduced = reduced.clear_denoms(convert=True)
        _content, reduced = reduced.primitive()
        if reduced.LC() < 0:
            reduced = -reduced
        reduced_polynomials.append(reduced)
        reduced_target = HERE / f"{candidate_id}_SPHERE_REDUCED_B_{label}.txt"
        reduced_target.write_text(str(reduced.as_expr()) + "\n", encoding="utf-8")
        polynomial_hashes[reduced_target.name] = digest(reduced_target.read_bytes())
        polynomial_rows.append({
            "component": label,
            "total_degree": poly.total_degree(),
            "term_count": len(poly.terms()),
            "cleared_denominator": str(component_denominator),
            "integer_clear_factor": clear_factor,
            "primitive_content": content,
            "sha256": polynomial_hashes[target.name],
            "sphere_reduced_total_degree": reduced.total_degree(),
            "sphere_reduced_term_count": len(reduced.terms()),
            "sphere_reduced_sha256": polynomial_hashes[reduced_target.name],
        })

    common_gcd = sp.gcd(sp.gcd(polynomials[0], polynomials[1]), polynomials[2])
    saturation = {
        "status": "NOT_RUN",
        "unit_ideal": None,
        "basis_length": None,
        "basis_sha256": None,
    }
    if saturate:
        numerator_reduced = sphere_remainder(numerator).as_expr()
        denominator_reduced = sphere_remainder(p_denominator).as_expr()
        equations = [poly.as_expr() for poly in reduced_polynomials]
        equations.extend((CONTACT_A, SPHERE))
        equations.append(1 - T * DEFECT * numerator_reduced * denominator_reduced)
        basis = sp.groebner(equations, T, Q3, Q2, Q1, Q0, order="grevlex")
        unit = len(basis.polys) == 1 and basis.polys[0].as_expr() == 1
        basis_text = "\n".join(str(poly.as_expr()) for poly in basis.polys) + "\n"
        basis_target = HERE / f"{candidate_id}_SATURATED_GROEBNER_BASIS.txt"
        basis_target.write_text(basis_text, encoding="utf-8")
        saturation = {
            "status": "UNIT_IDEAL_EMPTY_COMPLEX_ON_DEFINED_DOMAIN" if unit else "NONTRIVIAL_DEFINED_DOMAIN_IDEAL_REQUIRES_REAL_CLASSIFICATION",
            "unit_ideal": unit,
            "basis_length": len(basis.polys),
            "basis_sha256": digest(basis_target.read_bytes()),
        }

    result = {
        "schema": "udt-intrinsic-global-curvature-candidate-1.0",
        "candidate_id": candidate_id,
        "status": "PASS_EXACT_POLYNOMIAL_DERIVATION",
        "sympy_version": sp.__version__,
        "source_manifest_sha256": (HERE / "SOURCE_MANIFEST.sha256").read_text().strip(),
        "sphere_constraint": str(SPHERE),
        "defect_exclusion": str(DEFECT),
        "connection": "omega=-a*(f13*sigma1+f23*sigma2)/sqrt(P); P=u*S",
        "curvature": "Omega=-a*(2*P*deta-dP_wedge_eta)/(2*P^(3/2))",
        "polynomials": polynomial_rows,
        "polynomial_hashes": polynomial_hashes,
        "common_gcd": str(common_gcd.as_expr()),
        "cleared_denominators_nonzero_on_sphere": "PROVED_FROM_POSITIVE_u_V_r",
        "P_exact_factored_denominator": str(p_denominator),
        "P_exact_numerator_sha256": digest((str(numerator) + "\n").encode()),
        "contact_zero_necessary_on_regular_domain": str(CONTACT_A),
        "saturation_domain": "sphere AND defect!=0 AND P_numerator!=0 AND P_denominator!=0",
        "saturation": saturation,
        "global_regular_zero_set_complete": bool(saturation["unit_ideal"]),
    }
    target = HERE / f"{candidate_id}_INTRINSIC_RESULT.json"
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", choices=OWNERS + ("all",), default="all")
    parser.add_argument("--saturate", action="store_true")
    args = parser.parse_args()
    source_count = verify_sources()
    proof = chart_equivalence_proof()
    candidates = OWNERS if args.candidate == "all" else (args.candidate,)
    results = []
    for candidate_id in candidates:
        print(f"derive {candidate_id}", flush=True)
        results.append(derive_candidate(candidate_id, args.saturate))
        print(
            json.dumps({
                "candidate": candidate_id,
                "degrees": [row["total_degree"] for row in results[-1]["polynomials"]],
                "terms": [row["term_count"] for row in results[-1]["polynomials"]],
                "saturation": results[-1]["saturation"]["status"],
            }, sort_keys=True),
            flush=True,
        )
    print(json.dumps({
        "status": "PASS",
        "frozen_sources": source_count,
        "chart_equivalence": proof["status"],
        "candidates": list(candidates),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
