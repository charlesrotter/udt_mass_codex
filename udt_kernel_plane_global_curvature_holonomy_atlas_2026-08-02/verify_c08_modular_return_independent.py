#!/usr/bin/env python3
"""Independent exact verification of the saved C08 modular basis."""

from __future__ import annotations

import hashlib
import json
import os
import re
import resource
import subprocess
from itertools import combinations
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SINGULAR_ROOT = Path("/tmp/udt_singular_local")
SINGULAR = SINGULAR_ROOT / "usr/bin/Singular"
SINGULAR_LIB = SINGULAR_ROOT / "usr/lib/x86_64-linux-gnu"
POLY_KERNELS = tuple(
    SINGULAR_ROOT / "usr/libexec/x86_64-linux-gnu/singular/MOD" / name
    for name in (
        "p_Procs_FieldGeneral.so", "p_Procs_FieldIndep.so",
        "p_Procs_FieldQ.so", "p_Procs_FieldZp.so",
    )
)
Z, Y = sp.symbols("z y")
ORDER = "grevlex"
EXPECTED_PRODUCTION_STDOUT_SHA256 = "a785441f0bb6fc5bb8f631861a84336660f8508e729780a6e40459868070479b"
EXPECTED_PRODUCTION_STDERR_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
EXPECTED_PROCESS_RESULT_SHA256 = "139b9789d31ba2ad903d8d770644d5483374ba9cc0f6dc2860f6ce67fd8cbb62"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def environment() -> dict[str, str]:
    result = dict(os.environ)
    result["LD_LIBRARY_PATH"] = str(SINGULAR_LIB)
    result["LD_PRELOAD"] = ":".join(map(str, POLY_KERNELS))
    return result


def committed_clean(path: Path) -> str:
    relative = str(path.relative_to(ROOT))
    blob = subprocess.run(
        ["git", "rev-parse", f"HEAD:{relative}"], cwd=ROOT,
        text=True, capture_output=True, check=True,
    ).stdout.strip()
    content = subprocess.run(
        ["git", "cat-file", "blob", blob], cwd=ROOT,
        capture_output=True, check=True,
    ).stdout
    assert content == path.read_bytes(), relative
    return blob


def parse_expression(text: str) -> sp.Expr:
    return sp.sympify(text.replace("^", "**"), locals={"z": Z, "y": Y})


def parse_basis() -> list[sp.Poly]:
    stdout = (HERE / "C08_MODULAR_ALL_ZERO_STDOUT.txt").read_text()
    body = stdout.split("UDT_BASIS_BEGIN", 1)[1].split("UDT_BASIS_END", 1)[0]
    rows = re.findall(r"^G\[(\d+)\]=(.*)$", body, re.MULTILINE)
    assert [int(index) for index, _ in rows] == list(range(1, len(rows) + 1))
    return [sp.Poly(parse_expression(text), Z, Y, domain=sp.QQ) for _, text in rows]


def parse_inputs() -> list[sp.Poly]:
    result = []
    for label in ("12", "13", "23"):
        for prefix in ("A", "B"):
            path = HERE / f"C08_LINEAR_{prefix}_{label}.txt"
            text = path.read_text().strip().replace("**", "^")
            text = text.replace("z_ratio", "z").replace("y_ratio", "y")
            result.append(sp.Poly(parse_expression(text), Z, Y, domain=sp.QQ))
    return result


def leading(poly: sp.Poly) -> tuple[tuple[int, int], sp.Rational]:
    monomial, coefficient = poly.terms(order=ORDER)[0]
    return monomial, coefficient


def monomial(exponents: tuple[int, int]) -> sp.Expr:
    return Z ** exponents[0] * Y ** exponents[1]


def s_polynomial(left: sp.Poly, right: sp.Poly) -> sp.Expr:
    lm_left, lc_left = leading(left)
    lm_right, lc_right = leading(right)
    common = tuple(max(a, b) for a, b in zip(lm_left, lm_right))
    left_factor = tuple(a - b for a, b in zip(common, lm_left))
    right_factor = tuple(a - b for a, b in zip(common, lm_right))
    return sp.expand(monomial(left_factor) * left.as_expr() / lc_left - monomial(right_factor) * right.as_expr() / lc_right)


def reduce_exact(poly: sp.Expr, basis: list[sp.Poly]) -> sp.Poly:
    _quotients, remainder = sp.reduced(
        poly, [entry.as_expr() for entry in basis], Z, Y,
        order=ORDER, domain=sp.QQ,
    )
    return sp.Poly(remainder, Z, Y, domain=sp.QQ)


def sympy_checks(inputs: list[sp.Poly], basis: list[sp.Poly]) -> dict[str, object]:
    s_failures = []
    for left_index, right_index in combinations(range(len(basis)), 2):
        remainder = reduce_exact(s_polynomial(basis[left_index], basis[right_index]), basis)
        if not remainder.is_zero:
            s_failures.append([left_index + 1, right_index + 1])
    input_failures = []
    for index, entry in enumerate(inputs, 1):
        if not reduce_exact(entry.as_expr(), basis).is_zero:
            input_failures.append(index)

    leading_monomials = [leading(entry)[0] for entry in basis]
    pure_z = min(monom[0] for monom in leading_monomials if monom[1] == 0)
    pure_y = min(monom[1] for monom in leading_monomials if monom[0] == 0)
    standard = []
    for z_degree in range(pure_z):
        for y_degree in range(pure_y):
            if not any(z_degree >= a and y_degree >= b for a, b in leading_monomials):
                standard.append([z_degree, y_degree])

    dropped = basis[:-1]
    mutation_input_failures = sum(
        not reduce_exact(entry.as_expr(), dropped).is_zero for entry in inputs
    )
    mutation_s_failures = sum(
        not reduce_exact(s_polynomial(dropped[i], dropped[j]), dropped).is_zero
        for i, j in combinations(range(len(dropped)), 2)
    )
    return {
        "basis_size": len(basis),
        "buchberger_pairs": len(basis) * (len(basis) - 1) // 2,
        "buchberger_failures": s_failures,
        "input_reduction_failures": input_failures,
        "leading_monomials": [list(item) for item in leading_monomials],
        "pure_power_bounds": {"z": pure_z, "y": pure_y},
        "standard_monomial_count": len(standard),
        "mutation": {
            "operation": "DROP_LAST_BASIS_ELEMENT",
            "input_reduction_failures": mutation_input_failures,
            "buchberger_failures": mutation_s_failures,
            "caught": mutation_input_failures + mutation_s_failures > 0,
        },
    }


def singular_expression(poly: sp.Poly) -> str:
    return str(poly.as_expr()).replace("**", "^")


def build_singular_source(inputs: list[sp.Poly], basis: list[sp.Poly]) -> Path:
    lines = ["option(redSB);", "ring r=0,(z,y),dp;"]
    for index, entry in enumerate(inputs, 1):
        lines.append(f"poly i{index}={singular_expression(entry)};")
    for index, entry in enumerate(basis, 1):
        lines.append(f"poly g{index}={singular_expression(entry)};")
    lines.extend((
        "ideal I=i1,i2,i3,i4,i5,i6;",
        "ideal G=g1,g2,g3,g4,g5,g6,g7,g8,g9;",
        'print("UDT_IND_VERIFYGB_BEGIN");',
        'int verified=system("verifyGB",G);',
        "verified;",
        'print("UDT_IND_VERIFYGB_END");',
        "int reduction_failures=0;",
        "for (int i=1; i<=size(I); i++) { if (reduce(I[i],G,1)!=0) { reduction_failures++; } }",
        'print("UDT_IND_INPUT_REDUCTIONS_BEGIN");',
        "reduction_failures;",
        'print("UDT_IND_INPUT_REDUCTIONS_END");',
        'print("UDT_IND_LIFT_BEGIN");',
        "matrix T=lift(I,G);",
        "matrix D=matrix(I)*T-matrix(G);",
        "int lift_failures=0;",
        "for (int i=1; i<=nrows(D); i++) { for (int j=1; j<=ncols(D); j++) { if (D[i,j]!=0) { lift_failures++; } } }",
        "lift_failures;",
        'print("UDT_IND_LIFT_END");',
        'print("UDT_IND_DIM_BEGIN");', "dim(G);", 'print("UDT_IND_DIM_END");',
        'print("UDT_IND_VDIM_BEGIN");', "vdim(G);", 'print("UDT_IND_VDIM_END");',
        'print("UDT_IND_SIZE_BEGIN");', "size(G);", 'print("UDT_IND_SIZE_END");',
        "quit;",
    ))
    target = HERE / "C08_MODULAR_INDEPENDENT_LIFT_INPUT.sing"
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target


def bounded_child() -> None:
    limit = 48 * 1024**3
    resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    os.setsid()


def marker(text: str, name: str) -> str | None:
    start = f"UDT_IND_{name}_BEGIN"
    end = f"UDT_IND_{name}_END"
    if start not in text or end not in text:
        return None
    values = [line.strip() for line in text.split(start, 1)[1].split(end, 1)[0].splitlines() if line.strip()]
    return values[-1] if values else None


def singular_checks(inputs: list[sp.Poly], basis: list[sp.Poly]) -> dict[str, object]:
    source = build_singular_source(inputs, basis)
    stdout_path = HERE / "C08_MODULAR_INDEPENDENT_LIFT_STDOUT.txt"
    stderr_path = HERE / "C08_MODULAR_INDEPENDENT_LIFT_STDERR.txt"
    try:
        completed = subprocess.run(
            [str(SINGULAR), "-q", "--no-rc", "--cpus=1", "--threads=1"],
            stdin=source.open("rb"), capture_output=True, env=environment(),
            timeout=1800, check=False, preexec_fn=bounded_child,
        )
        stdout_path.write_bytes(completed.stdout)
        stderr_path.write_bytes(completed.stderr)
        stdout = completed.stdout.decode("utf-8", errors="replace")
        stderr = completed.stderr.decode("utf-8", errors="replace")
        combined = stdout + stderr
        return {
            "returncode": completed.returncode,
            "timed_out": False,
            "input_sha256": digest(source),
            "stdout_sha256": digest(stdout_path),
            "stderr_sha256": digest(stderr_path),
            "internal_error": "? ERROR" in combined or "error occurred" in combined,
            "verifygb": marker(stdout, "VERIFYGB"),
            "input_reduction_failures": marker(stdout, "INPUT_REDUCTIONS"),
            "lift_identity_failures": marker(stdout, "LIFT"),
            "dimension": marker(stdout, "DIM"),
            "quotient_dimension": marker(stdout, "VDIM"),
            "basis_size": marker(stdout, "SIZE"),
        }
    except subprocess.TimeoutExpired as exc:
        stdout_path.write_bytes(exc.stdout or b"")
        stderr_path.write_bytes(exc.stderr or b"")
        return {
            "returncode": None,
            "timed_out": True,
            "input_sha256": digest(source),
            "stdout_sha256": digest(stdout_path),
            "stderr_sha256": digest(stderr_path),
        }


def main() -> int:
    for name in (
        "C08_MODULAR_ALL_ZERO_INPUT.sing", "C08_MODULAR_PREPARATION.json",
        "C08_LINEAR_A_12.txt", "C08_LINEAR_B_12.txt",
        "C08_LINEAR_A_13.txt", "C08_LINEAR_B_13.txt",
        "C08_LINEAR_A_23.txt", "C08_LINEAR_B_23.txt",
    ):
        committed_clean(HERE / name)
    process_record = json.loads((HERE / "C08_MODULAR_PROCESS_RESULT.json").read_text())
    assert digest(HERE / "C08_MODULAR_PROCESS_RESULT.json") == EXPECTED_PROCESS_RESULT_SHA256
    stdout_path = HERE / "C08_MODULAR_ALL_ZERO_STDOUT.txt"
    stderr_path = HERE / "C08_MODULAR_ALL_ZERO_STDERR.txt"
    assert digest(stdout_path) == process_record["stdout_sha256"] == EXPECTED_PRODUCTION_STDOUT_SHA256
    assert digest(stderr_path) == process_record["stderr_sha256"] == EXPECTED_PRODUCTION_STDERR_SHA256

    inputs = parse_inputs()
    basis = parse_basis()
    sympy_result = sympy_checks(inputs, basis)
    singular_result = singular_checks(inputs, basis)
    primary_pass = (
        not sympy_result["buchberger_failures"]
        and not sympy_result["input_reduction_failures"]
        and sympy_result["standard_monomial_count"] == 124
        and sympy_result["mutation"]["caught"]
        and singular_result.get("returncode") == 0
        and not singular_result.get("internal_error")
        and singular_result.get("verifygb") == "1"
        and singular_result.get("input_reduction_failures") == "0"
        and singular_result.get("lift_identity_failures") == "0"
        and singular_result.get("dimension") == "0"
        and singular_result.get("quotient_dimension") == "124"
        and singular_result.get("basis_size") == "9"
    )
    result = {
        "schema": "udt-c08-modular-independent-verification-1.0",
        "status": "PASS_EXACT_INDEPENDENT_ALGEBRA_PENDING_COLD_REVIEW" if primary_pass else "REFUTED_OR_OPEN",
        "production_stdout_sha256": digest(stdout_path),
        "production_stderr_sha256": digest(stderr_path),
        "sympy": sympy_result,
        "singular_lift": singular_result,
    }
    target = HERE / "C08_MODULAR_INDEPENDENT_VERIFICATION.json"
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0 if primary_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
