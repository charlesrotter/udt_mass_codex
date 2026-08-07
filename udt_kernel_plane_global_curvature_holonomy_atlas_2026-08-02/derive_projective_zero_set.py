#!/usr/bin/env python3
"""Exact full-coverage projective zero-set completion on q0 != 0."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import sympy as sp


sys.setrecursionlimit(1_000_000)
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
X, Y, Z = sp.symbols("x_ratio y_ratio z_ratio", real=True)
RATIO_VARS = (X, Y, Z)
T = sp.symbols("defined_domain_inverse")
OWNERS = ("C04", "C08", "C09", "C10")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_tsv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source_gate():
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == len({r["path"] for r in rows}) == 114
    for row in rows:
        blob = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob"]], cwd=ROOT,
            capture_output=True, check=True,
        ).stdout
        assert len(blob) == int(row["bytes"]) and digest(blob) == row["sha256"]
    assert digest((HERE / "SOURCE_MANIFEST.tsv").read_bytes()) == (HERE / "SOURCE_MANIFEST.sha256").read_text().strip()


def load_intrinsic_module():
    path = HERE / "derive_intrinsic_curvature.py"
    spec = importlib.util.spec_from_file_location("intrinsic_curvature_production", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def parse_polynomial(path, q):
    local = {str(symbol): symbol for symbol in q}
    expression = sp.sympify(path.read_text(encoding="utf-8"), locals=local)
    return sp.Poly(expression, *q, domain=sp.QQ)


def primitive(poly):
    _factor, poly = poly.clear_denoms(convert=True)
    _content, poly = poly.primitive()
    if poly.LC() < 0:
        poly = -poly
    return poly


def projectivize(poly, q):
    """Pull a sphere polynomial to q=q0*(1,x,y,z), q0^2=1/W."""
    degrees = [sum(monomial) for monomial, _coefficient in poly.terms()]
    minimum, maximum = min(degrees), max(degrees)
    parity = minimum % 2
    assert all(degree % 2 == parity for degree in degrees)
    assert (maximum-minimum) % 2 == 0
    maximum_power = (maximum-minimum)//2
    W = 1+X**2+Y**2+Z**2
    w_powers = [sp.Poly(sp.expand(W**power), *RATIO_VARS, domain=sp.QQ) for power in range(maximum_power+1)]
    terms = {}
    for monomial, coefficient in poly.terms():
        degree = sum(monomial)
        power = (degree-minimum)//2
        for w_monomial, w_coefficient in w_powers[maximum_power-power].terms():
            output_monomial = (
                monomial[1]+w_monomial[0],
                monomial[2]+w_monomial[1],
                monomial[3]+w_monomial[2],
            )
            terms[output_monomial] = terms.get(output_monomial, 0)+coefficient*w_coefficient
    result = primitive(sp.Poly.from_dict(terms, RATIO_VARS, domain=sp.QQ))

    # Exact inverse reconstruction: q0^minimum/W^maximum_power times result
    # differs only by the recorded nonzero integer normalization.
    return result, {
        "minimum_total_degree": minimum,
        "maximum_total_degree": maximum,
        "total_degree_parity": parity,
        "positive_W_power_cleared": maximum_power,
        "projective_total_degree": result.total_degree(),
        "projective_term_count": len(result.terms()),
    }


def contact_remainder(poly):
    """Reduce to x-degree < 2 in the exact contact quotient."""
    maximum_power = max(monomial[0]//2 for monomial, _coefficient in poly.terms())
    factors = {}
    for quotient_power in range(maximum_power+1):
        factors[quotient_power] = sp.Poly(
            sp.expand((3*Y**2)**quotient_power*(1-2*Y**2)**(maximum_power-quotient_power)),
            Y, domain=sp.QQ,
        )
    terms = {}
    for monomial, coefficient in poly.terms():
        x_power, y_power, z_power = monomial
        quotient_power, remainder_power = divmod(x_power, 2)
        for (factor_y_power,), factor_coefficient in factors[quotient_power].terms():
            output_monomial = (remainder_power, y_power+factor_y_power, z_power)
            terms[output_monomial] = terms.get(output_monomial, 0)+coefficient*factor_coefficient
    result = primitive(sp.Poly.from_dict(terms, RATIO_VARS, domain=sp.QQ))
    contact_leader = sp.Poly(1-2*Y**2, *RATIO_VARS, domain=sp.QQ)
    remaining_denominator_power = maximum_power
    while remaining_denominator_power:
        quotient, remainder = sp.div(result, contact_leader)
        if not remainder.is_zero:
            break
        result = primitive(quotient)
        remaining_denominator_power -= 1
    assert result.degree(X) <= 1
    return result, (1-2*Y**2)**remaining_denominator_power


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", choices=OWNERS, required=True)
    parser.add_argument("--saturate", action="store_true")
    parser.add_argument("--lex", action="store_true")
    args = parser.parse_args()
    if args.lex and not args.saturate:
        parser.error("--lex requires --saturate")
    source_gate()
    intrinsic = load_intrinsic_module()
    intrinsic.verify_sources()
    q = intrinsic.Q

    projective_polynomials = []
    contact_reduced_polynomials = []
    component_rows = []
    hashes = {}
    for label in ("12", "13", "23"):
        source = HERE / f"{args.candidate}_SPHERE_REDUCED_B_{label}.txt"
        sphere_poly = parse_polynomial(source, q)
        ratio_poly, metadata = projectivize(sphere_poly, q)
        target = HERE / f"{args.candidate}_PROJECTIVE_B_{label}.txt"
        target.write_text(str(ratio_poly.as_expr())+"\n", encoding="utf-8")
        hashes[target.name] = digest(target.read_bytes())
        projective_polynomials.append(ratio_poly)
        reduced, contact_denominator = contact_remainder(ratio_poly)
        reduced_target = HERE / f"{args.candidate}_CONTACT_REDUCED_B_{label}.txt"
        reduced_target.write_text(str(reduced.as_expr())+"\n", encoding="utf-8")
        hashes[reduced_target.name] = digest(reduced_target.read_bytes())
        contact_reduced_polynomials.append(reduced)
        component_rows.append({
            "component": label,
            "source_sha256": digest(source.read_bytes()),
            "output_sha256": hashes[target.name],
            "contact_reduced_sha256": hashes[reduced_target.name],
            "contact_reduced_degree": reduced.total_degree(),
            "contact_reduced_terms": len(reduced.terms()),
            "contact_reduced_x_degree": reduced.degree(X),
            "contact_reduction_denominator": str(contact_denominator),
            **metadata,
        })

    contact = sp.Poly(X**2-3*Y**2-2*X**2*Y**2, *RATIO_VARS, domain=sp.QQ)
    defect_poly, defect_metadata = projectivize(sp.Poly(intrinsic.DEFECT, *q, domain=sp.QQ), q)
    p_numerator, p_denominator = intrinsic.exact_p_numerator_denominator(args.candidate)
    p_numerator_sphere = intrinsic.sphere_remainder(p_numerator)
    p_denominator_sphere = intrinsic.sphere_remainder(p_denominator)
    p_numerator_ratio, p_num_metadata = projectivize(p_numerator_sphere, q)
    p_denominator_ratio, p_den_metadata = projectivize(p_denominator_sphere, q)

    saturation = {"status": "NOT_RUN", "unit_ideal": None, "basis_length": None, "zero_dimensional": None, "basis_sha256": None}
    lex_result = {"status": "NOT_RUN", "basis_length": None, "basis_sha256": None, "univariate_polynomials": []}
    if args.saturate:
        print(f"{args.candidate} exact contact-quotient saturation", flush=True)
        exclusion = sp.expand(defect_poly.as_expr()*p_numerator_ratio.as_expr()*p_denominator_ratio.as_expr())
        equations = [poly.as_expr() for poly in contact_reduced_polynomials]
        equations.extend((contact.as_expr(), 1-T*exclusion))
        basis = sp.groebner(equations, T, Z, Y, X, order="grevlex")
        unit = len(basis.polys) == 1 and basis.polys[0].as_expr() == 1
        basis_target = HERE / f"{args.candidate}_PROJECTIVE_GROEBNER_GREVLEX.txt"
        basis_target.write_text("\n".join(str(poly.as_expr()) for poly in basis.polys)+"\n", encoding="utf-8")
        saturation = {
            "status": "UNIT_IDEAL_NO_DEFINED_DOMAIN_ZERO" if unit else "NONTRIVIAL_PROJECTIVE_IDEAL",
            "unit_ideal": unit,
            "basis_length": len(basis.polys),
            "zero_dimensional": False if unit else bool(basis.is_zero_dimensional),
            "basis_sha256": digest(basis_target.read_bytes()),
        }
        if args.lex and not unit and basis.is_zero_dimensional:
            print(f"{args.candidate} exact FGLM lex conversion", flush=True)
            lex = basis.fglm(order="lex")
            lex_target = HERE / f"{args.candidate}_PROJECTIVE_GROEBNER_LEX.txt"
            lex_target.write_text("\n".join(str(poly.as_expr()) for poly in lex.polys)+"\n", encoding="utf-8")
            univariate = []
            for poly in lex.polys:
                expression = poly.as_expr()
                if expression.free_symbols <= {X}:
                    unipoly = sp.Poly(expression, X, domain=sp.QQ)
                    univariate.append({
                        "degree": unipoly.degree(),
                        "factorization": str(sp.factor(unipoly.as_expr())),
                        "real_root_count": int(unipoly.count_roots(-sp.oo, sp.oo)),
                    })
            lex_result = {
                "status": "PASS_LEX_TRIANGULATION",
                "basis_length": len(lex.polys),
                "basis_sha256": digest(lex_target.read_bytes()),
                "univariate_polynomials": univariate,
            }

    result = {
        "schema": "udt-projective-zero-set-1.0",
        "candidate_id": args.candidate,
        "status": "PASS_EXACT_PROJECTIVE_CONSTRUCTION",
        "source_manifest_sha256": (HERE / "SOURCE_MANIFEST.sha256").read_text().strip(),
        "coverage_lemma": "contact_zero AND q0_zero IMPLIES defect; therefore q0_nonzero covers all regular zeros",
        "ratio_chart": "x=q1/q0;y=q2/q0;z=q3/q0;q0^2=1/(1+x^2+y^2+z^2)",
        "components": component_rows,
        "polynomial_hashes": hashes,
        "contact": str(contact.as_expr()),
        "defect": {"expression": str(defect_poly.as_expr()), **defect_metadata},
        "P_numerator": p_num_metadata,
        "P_denominator": p_den_metadata,
        "saturation": saturation,
        "lexicographic_classification": lex_result,
        "global_real_zero_classification_complete": bool(saturation["unit_ideal"]),
    }
    target = HERE / f"{args.candidate}_PROJECTIVE_RESULT.json"
    target.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps({
        "candidate": args.candidate,
        "component_degrees": [row["projective_total_degree"] for row in component_rows],
        "component_terms": [row["projective_term_count"] for row in component_rows],
        "saturation": saturation,
        "lex": lex_result["status"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
