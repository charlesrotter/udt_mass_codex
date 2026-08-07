#!/usr/bin/env python3
"""Exact Singular replay of the C08 projective contact ideal."""

from __future__ import annotations

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
VARS = (X, Y, Z)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source_gate():
    manifest = rows(HERE / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == len({row["path"] for row in manifest}) == 114
    for row in manifest:
        blob = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob"]], cwd=ROOT,
            capture_output=True, check=True,
        ).stdout
        assert len(blob) == int(row["bytes"]) and digest(blob) == row["sha256"]
    assert digest((HERE / "SOURCE_MANIFEST.tsv").read_bytes()) == (HERE / "SOURCE_MANIFEST.sha256").read_text().strip()


def parse(path):
    local = {str(symbol): symbol for symbol in VARS}
    return sp.Poly(sp.sympify(path.read_text(encoding="utf-8"), locals=local), *VARS, domain=sp.QQ)


def singular_expression(expression):
    return str(expression).replace("**", "^").replace("x_ratio", "x").replace("y_ratio", "y").replace("z_ratio", "z")


def main():
    source_gate()
    assert SINGULAR.is_file()
    version = subprocess.run(
        [str(SINGULAR), "--version"], capture_output=True, check=True, text=True,
        env={**os.environ, "LD_LIBRARY_PATH": str(LIBRARY_PATH)},
    ).stdout.splitlines()[0]

    expected_g = sp.Poly(
        42*Y**4+46*Y**2*Z**2-42*Y**2-23*Z**2-12,
        Y, Z, domain=sp.QQ,
    )
    normalized = []
    factor_records = []
    for label, expected_y_power in (("12", 1), ("13", 2), ("23", 2)):
        source = HERE / f"C08_CONTACT_REDUCED_B_{label}.txt"
        polynomial = parse(source)
        in_x = sp.Poly(polynomial.as_expr(), X)
        coefficient = sp.Poly(in_x.coeff_monomial(X), Y, Z, domain=sp.QQ)
        constant = sp.Poly(in_x.coeff_monomial(1), Y, Z, domain=sp.QQ)
        common = sp.gcd(coefficient, constant)
        expected = sp.Poly(Y**expected_y_power, Y, Z, domain=sp.QQ)*expected_g
        ratio = sp.cancel(common.as_expr()/expected.as_expr())
        assert ratio.is_Rational and ratio != 0
        common_xyz = sp.Poly(common.as_expr(), *VARS, domain=sp.QQ)
        quotient, remainder = sp.div(polynomial, common_xyz)
        assert remainder.is_zero
        _content, quotient = quotient.primitive()
        normalized.append(quotient)
        target = HERE / f"C08_REAL_DOMAIN_NORMALIZED_B_{label}.txt"
        target.write_text(str(quotient.as_expr())+"\n", encoding="utf-8")
        factor_records.append({
            "component": label,
            "removed_factor": str(sp.factor(common.as_expr())),
            "expected_factor_ratio": str(ratio),
            "source_sha256": digest(source.read_bytes()),
            "normalized_sha256": digest(target.read_bytes()),
            "normalized_degree": quotient.total_degree(),
            "normalized_terms": len(quotient.terms()),
        })

    # On real contact points away from D, y!=0 and 0<y^2<1/2. Writing a=y^2,
    # G=42a(a-1)-12+23(2a-1)z^2 proves G<0. Thus no real zero is removed.
    contact = X**2-3*Y**2-2*X**2*Y**2
    source_lines = [
        "option(redSB);",
        "ring r=0,(z,y,x),dp;",
    ]
    for index, polynomial in enumerate(normalized, 1):
        source_lines.append(f"poly f{index}={singular_expression(polynomial.as_expr())};")
    source_lines.extend((
        f"poly contact={singular_expression(contact)};",
        "ideal I=f1,f2,f3,contact;",
        "ideal G=std(I);",
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
    singular_source = "\n".join(source_lines)+"\n"
    input_target = HERE / "C08_SINGULAR_PROJECTIVE_INPUT.sing"
    input_target.write_text(singular_source, encoding="utf-8")
    completed = subprocess.run(
        [str(SINGULAR), "-q"], input=singular_source, capture_output=True, text=True,
        env={**os.environ, "LD_LIBRARY_PATH": str(LIBRARY_PATH)}, check=True,
    )
    stdout_target = HERE / "C08_SINGULAR_PROJECTIVE_STDOUT.txt"
    stderr_target = HERE / "C08_SINGULAR_PROJECTIVE_STDERR.txt"
    stdout_target.write_text(completed.stdout, encoding="utf-8")
    stderr_target.write_text(completed.stderr, encoding="utf-8")

    def between(start, end):
        return completed.stdout.split(start, 1)[1].split(end, 1)[0].strip()

    dimension = int(between("UDT_DIM_BEGIN", "UDT_DIM_END"))
    vector_dimension = int(between("UDT_VDIM_BEGIN", "UDT_VDIM_END"))
    basis_text = between("UDT_BASIS_BEGIN", "UDT_BASIS_END")
    basis_target = HERE / "C08_SINGULAR_PROJECTIVE_BASIS.txt"
    basis_target.write_text(basis_text+"\n", encoding="utf-8")
    result = {
        "schema": "udt-singular-projective-c08-1.0",
        "status": "PASS_EXACT_ZERO_DIMENSIONAL_BASIS" if dimension == 0 else "OPEN_POSITIVE_DIMENSIONAL",
        "singular_version": version,
        "source_manifest_sha256": (HERE / "SOURCE_MANIFEST.sha256").read_text().strip(),
        "coverage": "all regular zeros have q0!=0 by contact lemma",
        "real_domain_factor_proof": "y!=0; a=y^2 in (0,1/2); G=42a(a-1)-12+23(2a-1)z^2<0",
        "removed_factors": factor_records,
        "dimension": dimension,
        "vector_space_dimension": vector_dimension,
        "input_sha256": digest(input_target.read_bytes()),
        "stdout_sha256": digest(stdout_target.read_bytes()),
        "stderr_sha256": digest(stderr_target.read_bytes()),
        "basis_sha256": digest(basis_target.read_bytes()),
    }
    (HERE / "C08_SINGULAR_PROJECTIVE_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
