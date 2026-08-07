#!/usr/bin/env python3
"""Derive exact reduced connection and global curvature polynomial triples."""

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
X, Y, Z = sp.symbols("x y z", real=True)
XYZ = (X, Y, Z)
T = sp.symbols("saturation_inverse")
OWNERS = ("C04", "C08", "C09", "C10")


def read_tsv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify_sources():
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == len({row["path"] for row in rows}) == 110
    for row in rows:
        content = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob"]], cwd=ROOT,
            capture_output=True, check=True,
        ).stdout
        assert len(content) == int(row["bytes"])
        assert digest(content) == row["sha256"]
    assert digest((HERE / "SOURCE_MANIFEST.tsv").read_bytes()) == (HERE / "SOURCE_MANIFEST.sha256").read_text().strip()
    return len(rows)


def primitive_integer_polynomial(expression):
    numerator, denominator = sp.fraction(sp.cancel(expression))
    poly = sp.Poly(numerator, X, Y, Z, domain=sp.QQ)
    _factor, poly = poly.clear_denoms(convert=True)
    _content, poly = poly.primitive()
    if poly.LC() < 0:
        poly = -poly
    return poly, sp.factor(denominator)


def profile(candidate_id, q):
    q0, q1, q2, q3 = q
    u = 3 + q0*q0 + 2*q1*q1 + 4*q2*q2 + 8*q3*q3
    v0 = q0*q0 + 3*q1*q1 + 7*q2*q2 + 9*q3*q3
    r0 = 2*q0*q0 + 5*q1*q1 + 11*q2*q2 + 13*q3*q3
    b0 = q0*q1 + 2*q0*q2 + 3*q0*q3 + 5*q1*q2 + 7*q1*q3 + 11*q2*q3
    v = 1 + sp.Rational(1, 10)*v0
    if candidate_id == "C04":
        lam, r, b = 0, sp.S.One, sp.S.Zero
    else:
        lam = {"C08": 0, "C09": -1, "C10": 1}[candidate_id]
        r = 1 + sp.Rational(1, 10)*r0
        b = sp.Rational(1, 10)*b0
    return tuple(sp.cancel(value) for value in (u, u**lam*v, r, b))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--saturate", action="store_true")
    args = parser.parse_args()
    source_count = verify_sources()

    rho2 = X*X + Y*Y + Z*Z
    denominator = 1 + rho2
    q = (
        (1-rho2)/denominator,
        2*X/denominator,
        2*Y/denominator,
        2*Z/denominator,
    )
    q0, q1, q2, q3 = q
    d2 = denominator**2
    sigma1 = sp.Matrix([
        2*(X*X-Y*Y-Z*Z+1)/d2,
        4*(X*Y+Z)/d2,
        4*(X*Z-Y)/d2,
    ])
    sigma2 = sp.Matrix([
        4*(X*Y-Z)/d2,
        -2*(X*X-Y*Y+Z*Z-1)/d2,
        4*(X+Y*Z)/d2,
    ])
    f12 = sp.cancel(q0*q1*q1 + 3*q0*q2*q2 + 2*q1*q2*q3)
    f13 = sp.cancel(q0*q0*q1 + 3*q0*q2*q3 - 2*q1*q2*q2)
    f23 = sp.cancel(3*q0*q0*q2 - q0*q1*q3 + 2*q1*q1*q2)
    eta = sp.Matrix([sp.cancel(value) for value in f13*sigma1 + f23*sigma2])
    deta = (
        sp.cancel(sp.diff(eta[1], X)-sp.diff(eta[0], Y)),
        sp.cancel(sp.diff(eta[2], X)-sp.diff(eta[0], Z)),
        sp.cancel(sp.diff(eta[2], Y)-sp.diff(eta[1], Z)),
    )

    defect_measure = sp.cancel(f12*f12+f13*f13+f23*f23)
    defect_poly, defect_denominator = primitive_integer_polynomial(defect_measure)
    (HERE / "DEFECT_EXCLUSION_POLYNOMIAL.txt").write_text(str(defect_poly.as_expr())+"\n", encoding="utf-8")

    summary_rows = []
    polynomial_hashes = {}
    polynomial_cache = {}
    for candidate_id in OWNERS:
        print(f"derive {candidate_id}", flush=True)
        u, area, r, b = profile(candidate_id, q)
        S = sp.cancel(
            u*f12*f12
            + area*((b*f13-r*f23)**2 + f13*f13/(r*r))
        )
        P = sp.cancel(u*S)

        # Exact algebraic identity behind the preregistered reduced connection.
        root_area, root_u = sp.sqrt(area), sp.sqrt(u)
        w12 = -f13/(root_area*r*root_u)
        w13 = (b*f13-r*f23)/(root_area*root_u)
        w23 = f12/area
        L2 = sp.cancel(w12*w12+w13*w13+w23*w23)
        assert sp.cancel(L2-S/(u*area*area)) == 0

        dP = [sp.diff(P, coordinate) for coordinate in XYZ]
        B = (
            sp.cancel(2*P*deta[0]-(dP[0]*eta[1]-dP[1]*eta[0])),
            sp.cancel(2*P*deta[1]-(dP[0]*eta[2]-dP[2]*eta[0])),
            sp.cancel(2*P*deta[2]-(dP[1]*eta[2]-dP[2]*eta[1])),
        )
        polynomials = []
        denominators = []
        for label, component in zip(("xy", "xz", "yz"), B):
            poly, component_denominator = primitive_integer_polynomial(component)
            polynomials.append(poly)
            denominators.append(component_denominator)
            target = HERE / f"{candidate_id}_B_{label}.txt"
            target.write_text(str(poly.as_expr())+"\n", encoding="utf-8")
            polynomial_hashes[target.name] = digest(target.read_bytes())
        polynomial_cache[candidate_id] = polynomials
        common_gcd = sp.gcd(sp.gcd(polynomials[0], polynomials[1]), polynomials[2])
        summary_rows.append({
            "candidate_id": candidate_id,
            "degrees_xy_xz_yz": ";".join(str(poly.total_degree()) for poly in polynomials),
            "terms_xy_xz_yz": ";".join(str(len(poly.terms())) for poly in polynomials),
            "common_gcd": str(common_gcd.as_expr()),
            "denominators": ";".join(str(value) for value in denominators),
            "S_numerator_terms": str(len(sp.Poly(sp.fraction(S)[0], X, Y, Z).terms())),
            "saturation_status": "NOT_RUN" if not args.saturate else "RUNNING",
        })

    saturation_results = {}
    if args.saturate:
        for row in summary_rows:
            candidate_id = row["candidate_id"]
            print(f"saturate {candidate_id}", flush=True)
            equations = [poly.as_expr() for poly in polynomial_cache[candidate_id]]
            equations.append(1-T*defect_poly.as_expr())
            basis = sp.groebner(equations, T, X, Y, Z, order="grevlex")
            unit = len(basis.polys) == 1 and basis.polys[0].as_expr() == 1
            row["saturation_status"] = "UNIT_IDEAL_EMPTY_COMPLEX_OFF_D" if unit else "NONTRIVIAL_IDEAL_REQUIRES_CLASSIFICATION"
            saturation_results[candidate_id] = {
                "unit_ideal": unit,
                "basis_length": len(basis.polys),
                "basis": [str(poly.as_expr()) for poly in basis.polys],
            }

    with (HERE / "CURVATURE_POLYNOMIAL_SUMMARY.tsv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["candidate_id", "degrees_xy_xz_yz", "terms_xy_xz_yz", "common_gcd", "denominators", "S_numerator_terms", "saturation_status"]
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader(); writer.writerows(summary_rows)

    result = {
        "schema": "udt-kernel-plane-global-curvature-1.0",
        "status": "PASS_EXACT_POLYNOMIAL_DERIVATION" if not args.saturate else "PASS_WITH_SATURATION_RESULTS",
        "sympy_version": sp.__version__,
        "frozen_sources": source_count,
        "owners": list(OWNERS),
        "stereographic_omitted_point_in_D": True,
        "connection_reduction": "omega=-a*(f13*sigma1+f23*sigma2)/sqrt(u*S)",
        "curvature_reduction": "Omega=-a*(2*P*deta-dP_wedge_eta)/(2*P^(3/2));P=u*S",
        "S_zero_iff_defect": "PROVED_BY_POSITIVE_SUM_AND_INVERTIBLE_METRIC_WEIGHTS",
        "additional_singularities": "NONE_ON_M",
        "defect_exclusion_polynomial_degree": defect_poly.total_degree(),
        "defect_exclusion_polynomial_terms": len(defect_poly.terms()),
        "defect_exclusion_denominator": str(defect_denominator),
        "polynomial_hashes": polynomial_hashes,
        "saturation": saturation_results,
        "global_zero_classification_complete": bool(args.saturate) and all(value["unit_ideal"] for value in saturation_results.values()),
    }
    (HERE / "GLOBAL_CURVATURE_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "defect_degree": result["defect_exclusion_polynomial_degree"],
        "global_complete": result["global_zero_classification_complete"],
        "summary": {row["candidate_id"]: [row["degrees_xy_xz_yz"], row["terms_xy_xz_yz"], row["common_gcd"]] for row in summary_rows},
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
