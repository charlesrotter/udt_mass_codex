#!/usr/bin/env python3
"""Case-complete exact C08 elimination using the proven linearity in x."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import sympy as sp


sys.setrecursionlimit(1_000_000)
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SINGULAR_ROOT = Path("/tmp/udt_singular_local")
SINGULAR = SINGULAR_ROOT / "usr/bin/Singular"
LIBRARY_PATH = SINGULAR_ROOT / "usr/lib/x86_64-linux-gnu"
X, Y, Z = sp.symbols("x_ratio y_ratio z_ratio")
LABELS = ("12", "13", "23")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rows(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source_gate() -> str:
    manifest = rows(HERE / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == len({row["path"] for row in manifest}) == 116
    for row in manifest:
        blob = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob"]], cwd=ROOT,
            capture_output=True, check=True,
        ).stdout
        assert len(blob) == int(row["bytes"])
        assert digest(blob) == row["sha256"]
    manifest_hash = digest((HERE / "SOURCE_MANIFEST.tsv").read_bytes())
    assert manifest_hash == (HERE / "SOURCE_MANIFEST.sha256").read_text().strip()
    return manifest_hash


def parse_xyz(path: Path) -> sp.Poly:
    local = {str(symbol): symbol for symbol in (X, Y, Z)}
    expression = sp.sympify(path.read_text(encoding="utf-8"), locals=local)
    return sp.Poly(expression, X, Y, Z, domain=sp.QQ)


def primitive(poly: sp.Poly) -> sp.Poly:
    _content, result = poly.primitive()
    if result.LC() < 0:
        result = -result
    return result


def write_poly(path: Path, poly: sp.Poly) -> dict:
    path.write_text(str(poly.as_expr()) + "\n", encoding="utf-8")
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": digest(path.read_bytes()),
        "total_degree": poly.total_degree(),
        "terms": len(poly.terms()),
    }


def singular_expression(expression) -> str:
    return (
        str(expression)
        .replace("**", "^")
        .replace("x_ratio", "x")
        .replace("y_ratio", "y")
        .replace("z_ratio", "z")
    )


def construct():
    manifest_hash = source_gate()
    equations = []
    coefficients = []
    records = []
    for label in LABELS:
        source = HERE / f"C08_REAL_DOMAIN_NORMALIZED_B_{label}.txt"
        equation = parse_xyz(source)
        in_x = sp.Poly(equation.as_expr(), X, domain=sp.QQ.frac_field(Y, Z))
        assert in_x.degree() == 1
        a = sp.Poly(in_x.coeff_monomial(X), Y, Z, domain=sp.QQ)
        b = sp.Poly(in_x.coeff_monomial(1), Y, Z, domain=sp.QQ)
        reconstructed = sp.Poly(a.as_expr() * X + b.as_expr(), X, Y, Z, domain=sp.QQ)
        assert reconstructed == equation
        equations.append(equation)
        coefficients.append((a, b))
        records.append({
            "component": label,
            "source_sha256": digest(source.read_bytes()),
            "degree_x": 1,
            "A": write_poly(HERE / f"C08_LINEAR_A_{label}.txt", a),
            "B": write_poly(HERE / f"C08_LINEAR_B_{label}.txt", b),
            "reconstruction": "PASS_EXACT_IDENTITY",
        })

    chart_records = []
    chart_data = {}
    for owner, (a, b) in enumerate(coefficients):
        other_indices = [index for index in range(3) if index != owner]
        compatibility = []
        for other in other_indices:
            aj, bj = coefficients[other]
            polynomial = primitive(sp.Poly(
                a.as_expr() * bj.as_expr() - aj.as_expr() * b.as_expr(),
                Y, Z, domain=sp.QQ,
            ))
            compatibility.append(polynomial)
        contact = primitive(sp.Poly(
            (1 - 2 * Y**2) * b.as_expr() ** 2 - 3 * Y**2 * a.as_expr() ** 2,
            Y, Z, domain=sp.QQ,
        ))
        owner_label = LABELS[owner]
        file_records = []
        for other, polynomial in zip(other_indices, compatibility):
            name = f"C08_LINEAR_CHART_{owner_label}_COMPAT_{LABELS[other]}.txt"
            file_records.append(write_poly(HERE / name, polynomial))
        contact_record = write_poly(
            HERE / f"C08_LINEAR_CHART_{owner_label}_CONTACT.txt", contact,
        )
        chart_records.append({
            "owner": owner_label,
            "saturation_factor": records[owner]["A"],
            "compatibility": file_records,
            "contact": contact_record,
        })
        chart_data[owner_label] = (a, compatibility, contact)

    construction = {
        "schema": "udt-c08-exact-linear-elimination-construction-1.0",
        "status": "PASS_EXACT_CONSTRUCTION",
        "source_manifest_sha256": manifest_hash,
        "components": records,
        "charts": chart_records,
        "exceptional_case": {
            "equations": [f"A_{label}=0;B_{label}=0" for label in LABELS],
            "status": "REGISTERED_FOR_EXACT_CLASSIFICATION",
        },
        "coverage": "union(A_12!=0,A_13!=0,A_23!=0,all_A_zero)",
    }
    target = HERE / "C08_LINEAR_ELIMINATION_CONSTRUCTION.json"
    target.write_text(json.dumps(construction, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return coefficients, chart_data, construction


def singular_header() -> list[str]:
    return [
        'LIB "elim.lib";',
        "option(redSB);",
        "ring r=0,(z,y),dp;",
    ]


def run_singular_case(case: str, coefficients, chart_data):
    assert SINGULAR.is_file()
    lines = singular_header()
    if case in LABELS:
        owner = LABELS.index(case)
        a, compatibility, contact = chart_data[case]
        lines.append(f"poly a={singular_expression(a.as_expr())};")
        for index, polynomial in enumerate(compatibility, 1):
            lines.append(f"poly c{index}={singular_expression(polynomial.as_expr())};")
        lines.append(f"poly e={singular_expression(contact.as_expr())};")
        lines.extend((
            "ideal I=c1,c2,e;",
            "ideal S=sat(I,ideal(a))[1];",
            "ideal G=slimgb(S);",
        ))
    elif case == "all_zero":
        generators = []
        for index, (a, b) in enumerate(coefficients, 1):
            lines.append(f"poly a{index}={singular_expression(a.as_expr())};")
            lines.append(f"poly b{index}={singular_expression(b.as_expr())};")
            generators.extend((f"a{index}", f"b{index}"))
        lines.extend((
            f"ideal I={','.join(generators)};",
            "ideal G=slimgb(I);",
        ))
    else:
        raise ValueError(case)
    lines.extend((
        'print("UDT_DIM_BEGIN");',
        "dim(G);",
        'print("UDT_DIM_END");',
        'print("UDT_VDIM_BEGIN");',
        "vdim(G);",
        'print("UDT_VDIM_END");',
        'print("UDT_BASIS_BEGIN");',
        "G;",
        'print("UDT_BASIS_END");',
        "quit;",
    ))
    source = "\n".join(lines) + "\n"
    input_path = HERE / f"C08_LINEAR_{case.upper()}_INPUT.sing"
    stdout_path = HERE / f"C08_LINEAR_{case.upper()}_STDOUT.txt"
    stderr_path = HERE / f"C08_LINEAR_{case.upper()}_STDERR.txt"
    input_path.write_text(source, encoding="utf-8")
    with input_path.open("r", encoding="utf-8") as stdin, stdout_path.open("w", encoding="utf-8") as stdout, stderr_path.open("w", encoding="utf-8") as stderr:
        completed = subprocess.run(
            [str(SINGULAR), "-q"], stdin=stdin, stdout=stdout, stderr=stderr,
            env={**os.environ, "LD_LIBRARY_PATH": str(LIBRARY_PATH)},
        )
    result = {
        "schema": "udt-c08-exact-linear-elimination-case-1.0",
        "case": case,
        "returncode": completed.returncode,
        "input_sha256": digest(input_path.read_bytes()),
        "stdout_sha256": digest(stdout_path.read_bytes()),
        "stderr_sha256": digest(stderr_path.read_bytes()),
        "status": "RETURNED_REQUIRES_PARSE" if completed.returncode == 0 else "OPEN_PROCESS_ERROR",
    }
    result_path = HERE / f"C08_LINEAR_{case.upper()}_PROCESS_RESULT.json"
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return completed.returncode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--case", choices=("construct",) + LABELS + ("all_zero",), default="construct",
    )
    args = parser.parse_args()
    coefficients, chart_data, construction = construct()
    if args.case == "construct":
        print(json.dumps({
            "status": construction["status"],
            "source_manifest_sha256": construction["source_manifest_sha256"],
            "charts": len(construction["charts"]),
        }, sort_keys=True))
        return 0
    return run_singular_case(args.case, coefficients, chart_data)


if __name__ == "__main__":
    raise SystemExit(main())
