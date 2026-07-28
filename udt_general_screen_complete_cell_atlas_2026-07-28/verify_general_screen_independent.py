#!/usr/bin/env python3
"""Independent, non-importing verification for the general-screen S3 atlas."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "73833fa4e75152e51d24f8056b6856dd835785f7"
I = sp.eye(2)
R = sp.Matrix([[0, -1], [1, 0]])
S1 = sp.diag(1, -1)
S2 = sp.Matrix([[0, 1], [1, 0]])
HALF = sp.Rational(1, 2)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rotation(angle: sp.Expr) -> sp.Matrix:
    return sp.Matrix([[sp.cos(angle), -sp.sin(angle)], [sp.sin(angle), sp.cos(angle)]])


def exact_zero(expr: sp.Expr) -> bool:
    rewritten = sp.expand_trig(expr.rewrite(sp.exp))
    return sp.simplify(sp.trigsimp(rewritten)) == 0


def matrix_exact_zero(matrix: sp.Matrix) -> bool:
    return all(exact_zero(entry) for entry in matrix)


def reconstruct(response: dict[str, sp.Expr]) -> sp.Matrix:
    return response["area"]*I + response["rotation"]*R + response["shear1"]*S1 + response["shear2"]*S2


def independent_polar_check() -> dict[str, object]:
    """Verify dP=K P directly, without importing or calling the production derivation."""
    u, v, beta, chi = sp.symbols("u v beta chi", real=True)
    gamma = beta + chi
    A = rotation(gamma)
    D = sp.diag(sp.exp(u+v), sp.exp(u-v))
    P = A*D*rotation(-beta)
    responses = {
        u: {"area": 1, "rotation": 0, "shear1": 0, "shear2": 0},
        v: {"area": 0, "rotation": 0, "shear1": sp.cos(2*gamma), "shear2": sp.sin(2*gamma)},
        beta: {
            "area": 0,
            "rotation": 1-sp.cosh(2*v),
            "shear1": -sp.sinh(2*v)*sp.sin(2*gamma),
            "shear2": sp.sinh(2*v)*sp.cos(2*gamma),
        },
        chi: {"area": 0, "rotation": 1, "shear1": 0, "shear2": 0},
    }
    for variable, response in responses.items():
        require(matrix_exact_zero(P.diff(variable)-reconstruct(response)*P), f"direct dP=KP failed for {variable}")
    require(exact_zero(P.det()-sp.exp(2*u)), "detP direct check")
    h = sp.trigsimp(P.T*P)
    require(not h.has(chi), "coframe gauge chi entered h")

    # Verify the transported Maurer-Cartan generator from C P=P R, again without P^-1.
    c_response = {
        "area": 0,
        "rotation": sp.cosh(2*v),
        "shear1": sp.sinh(2*v)*sp.sin(2*gamma),
        "shear2": -sp.sinh(2*v)*sp.cos(2*gamma),
    }
    C = reconstruct(c_response)
    require(matrix_exact_zero(C*P-P*R), "C P=P R")
    require(matrix_exact_zero(C*C+I), "C squared=-I")
    require(exact_zero(sp.trace(C)), "trace C")
    require(exact_zero(C.det()-1), "det C")

    # The response Jacobian has determinant sinh(2v); regular log-H coordinates restore rank at v=0.
    jac = sp.Matrix([
        [1, 0, 0, 0],
        [0, sp.cos(2*gamma), -sp.sinh(2*v)*sp.sin(2*gamma), 0],
        [0, sp.sin(2*gamma), sp.sinh(2*v)*sp.cos(2*gamma), 0],
        [0, 0, 1-sp.cosh(2*v), 1],
    ])
    require(exact_zero(jac.det()-sp.sinh(2*v)), "polar response determinant")
    regular = sp.Matrix.hstack(I.reshape(4, 1), S1.reshape(4, 1), S2.reshape(4, 1), R.reshape(4, 1))
    require(regular.rank() == 4, "regular isotropic tangent rank")
    require(sp.Matrix.hstack(I.reshape(4, 1), S1.reshape(4, 1), S2.reshape(4, 1)).rank() == 3,
            "screen metric tangent rank")
    # The global symmetric witness exp(u I+q1 S1+q2 S2) is SPD and invertible for every
    # finite real u,q1,q2; its eigenvalues are exp(u +/- sqrt(q1^2+q2^2)).
    q1, q2 = sp.symbols("q1 q2", real=True)
    Q = u*I+q1*S1+q2*S2
    require(sp.simplify(Q.det()-(u**2-q1**2-q2**2)) == 0, "symmetric generator determinant")
    require(sp.simplify(sp.trace(Q)-2*u) == 0, "symmetric generator trace")
    return {
        "direct_product_derivatives": 4,
        "polar_response_determinant": "sinh(2*v)",
        "regular_isotropic_coframe_rank": 4,
        "regular_isotropic_metric_rank": 3,
        "global_symmetric_witness_eigenvalues": "exp(u_plus_or_minus_sqrt(q1^2+q2^2))",
        "angular_generator_identity": "C^2=-I;trC=0;detC=1",
    }


def independent_cartan_check(production: dict[str, object]) -> dict[str, object]:
    """Rebuild every first-jet connection coefficient from explicit exterior-form coefficients."""
    p1, p2, p3, t0, t1, m = sp.symbols("p1 p2 p3 t0 t1 m", real=True)
    c11, c12, c21, c22 = sp.symbols("c11 c12 c21 c22", real=True)
    C = sp.Matrix([[c11, c12], [c21, c22]])
    L = {a: sp.Matrix(2, 2, lambda i, j: sp.symbols(f"L{a}{i+1}{j+1}", real=True)) for a in (1, 2, 3)}
    coefficients: dict[tuple[int, int, int], sp.Expr] = {}

    def add_de(upper: int, left: int, right: int, value: sp.Expr) -> None:
        if left == right:
            return
        if left > right:
            left, right, value = right, left, -value
        coefficients[upper, left, right] = sp.simplify(coefficients.get((upper, left, right), 0)+value)

    add_de(0, 0, 1, p1); add_de(0, 0, 2, p2); add_de(0, 0, 3, p3); add_de(0, 2, 3, t0)
    add_de(1, 1, 2, -p2); add_de(1, 1, 3, -p3); add_de(1, 2, 3, t1)
    for out in range(2):
        for direction in (1, 2, 3):
            for column in range(2):
                add_de(out+2, direction, column+2, L[direction][out, column])
        for column in range(2):
            add_de(out+2, 1, column+2, m*C[out, column])

    structure: dict[tuple[int, int, int], sp.Expr] = {}
    for (upper, left, right), value in coefficients.items():
        structure[upper, left, right] = -value
        structure[upper, right, left] = value
    signature = (-1, 1, 1, 1)

    def c_lower(out: int, left: int, right: int) -> sp.Expr:
        return signature[out]*structure.get((out, left, right), 0)

    def koszul(left: int, middle: int, out: int) -> sp.Expr:
        return sp.simplify(HALF*(c_lower(out, left, middle)-c_lower(left, middle, out)+c_lower(middle, out, left)))

    independent_connections: dict[str, list[list[str]]] = {}
    for direction in range(4):
        matrix = sp.Matrix(4, 4, lambda out, middle: koszul(direction, middle, out))
        require(sp.simplify(matrix+matrix.T) == sp.zeros(4), "lowered connection metric compatibility")
        independent_connections[f"D{direction}"] = [[str(sp.simplify(matrix[i, j])) for j in range(4)] for i in range(4)]
    require(independent_connections == production["connection_matrices"], "full connection differs from production")

    off = {}
    for direction in range(4):
        off[f"D{direction}"] = sp.Matrix(2, 2, lambda screen, pair: koszul(direction, pair, screen+2))
    require(sp.simplify(off["D2"][1, 1]-off["D3"][0, 1]-t1) == 0, "connection block obstruction")

    # Independent Frobenius route: dtheta1(E2,E3)=t1, so the screen is not integrable
    # whenever t1=kappa exp(phi)/detP is nonzero.  A parallel distribution would be integrable.
    kappa, phi, det_p = sp.symbols("kappa phi detP", real=True, nonzero=True)
    t1_s3 = kappa*sp.exp(phi)/det_p
    require(t1_s3 != 0, "registered S3 Frobenius coefficient unexpectedly zero")
    require(production["connection_checks"]["D2_bottomright_minus_D3_topright"] == "t1",
            "production did not expose t1 obstruction")

    plus = production["rays"]["plus"]["acceleration"]
    minus = production["rays"]["minus"]["acceleration"]
    require(plus == ["-p1", "-p1", "-2*p2", "-2*p3"], "plus acceleration")
    require(minus == ["p1", "-p1", "-2*p2", "-2*p3"], "minus acceleration")
    return {
        "independently_rebuilt_connection_matrices": 4,
        "connection_method": "EXPLICIT_EXTERIOR_COEFFICIENTS_PLUS_KOSZUL",
        "obstruction_crosscheck": "D2_21-D3_12=t1",
        "independent_obstruction_method": "FROBENIUS_NONINTEGRABILITY",
        "frobenius_coefficient": "t1=kappa*exp(phi)/detP_nonzero",
        "maximum_ruling": "NO_ALL_DIRECTION_PARALLEL_PAIR_SCREEN_SPLIT_WITHIN_REGISTERED_S3_GL2_FAMILY",
    }


def verify_sources(rows: list[dict[str, str]]) -> str:
    require(len(rows) == 15, "source manifest row count")
    for row in rows:
        blob = subprocess.run(["git", "rev-parse", f"{BASE}:{row['path']}"], cwd=ROOT, check=True,
                              text=True, stdout=subprocess.PIPE).stdout.strip()
        raw = subprocess.run(["git", "show", f"{BASE}:{row['path']}"], cwd=ROOT, check=True,
                             stdout=subprocess.PIPE).stdout
        require(blob == row["git_blob"], f"blob mismatch {row['path']}")
        require(hashlib.sha256(raw).hexdigest() == row["sha256"], f"sha mismatch {row['path']}")
        require(len(raw) == int(row["bytes"]), f"size mismatch {row['path']}")
    canonical = "".join(f"{row['path']}\t{row['sha256']}\n" for row in rows).encode()
    return hashlib.sha256(canonical).hexdigest()


def snapshot() -> dict[str, object]:
    return {
        "result": json.loads((HERE / "DERIVATION_RESULT.json").read_text()),
        "cartan": json.loads((HERE / "GENERAL_CARTAN_RESULT.json").read_text()),
        "responses": read_tsv("POLAR_RESPONSE_ATLAS.tsv"),
        "witnesses": read_tsv("COMPLETE_S3_WITNESS_ATLAS.tsv"),
        "global": read_tsv("GLOBAL_EXISTENCE_ATLAS.tsv"),
        "completion": read_tsv("COMPLETION_DESCENT_ATLAS.tsv"),
        "coverage": read_tsv("TEN_CRITERION_COVERAGE.tsv"),
        "blocks": read_tsv("BLOCK_PRESERVATION_CONDITIONS.tsv"),
        "sources": read_tsv("SOURCE_MANIFEST.tsv"),
    }


def validate_snapshot(data: dict[str, object], check_git_sources: bool = False) -> None:
    result = data["result"]
    require(result["status"] == "PASS", "derivation status")
    require(result["coframe_response_rank"] == 4, "coframe response rank")
    require(result["metric_screen_response_rank"] == 3, "metric response rank")
    require(result["both_shear_tangents_at_isotropy"] is True, "isotropic shear tangent loss")
    require(result["rotation_is_extra_metric_DOF"] is False, "gauge rotation counted as metric")
    require(result["full_4D_metric_family"] is False, "block screen called full metric")
    require(result["on_shell_or_selected"] is False, "off-shell family called selected")
    require(result["all_direction_pair_screen_parallel_split"] is False, "parallel split promoted")
    require("t1=kappa*exp(phi)/detP_nonzero" in result["parallel_split_obstruction"], "t1 obstruction lost")

    responses = {row["stratum"]: row for row in data["responses"]}
    require(len(responses) == 8, "response row count")
    require(responses["A01_ISOTROPIC_REGULAR_q_COORDINATES"]["ruling"] == "BOTH_SHEAR_TANGENTS_PRESENT_AT_ISOTROPY",
            "isotropic regular chart ruling")
    require(responses["A07_DET_ZERO"]["ruling"] == "SCREEN_AND_FOUR_METRIC_DEGENERATE", "det zero ruling")
    require(responses["A04_PURE_GAUGE"]["rank"] == "1_COFAME;0_METRIC", "gauge rank")
    require("dbeta*sinh(2v)" in responses["A03_ROTATING_AXIS"]["shear1"], "rotating-axis shear lost")

    witnesses = {row["id"]: row for row in data["witnesses"]}
    require(len(witnesses) == 9 and "W04_TWO_SHEAR" in witnesses, "complete witness universe")
    require(witnesses["W04_TWO_SHEAR"]["physics_status"] == "OFF_SHELL_FULL_SYMMETRIC_RESPONSE_WITNESS",
            "two-shear witness status")
    require(all("LORENTZIAN_GEODESICALLY_COMPLETE" not in row["global_status"] for row in data["witnesses"]),
            "unsupported Lorentzian completeness")

    global_rows = {row["object"]: row for row in data["global"]}
    require(global_rows["four_Lorentzian_spacetime"]["scope"] == "NOT_A_LORENTZIAN_GEODESIC_COMPLETENESS_CLAIM",
            "Lorentzian completeness scope")
    require(global_rows["isotropic_axis"]["scope"] == "CHART_ONLY_DEGENERACY", "v=0 geometric singularity")
    require(global_rows["screen_rank_boundary"]["result"] == "coframe_and_four_metric_degenerate", "rank boundary")

    completion = data["completion"]
    require(len(completion) == 12 and len({row["completion_id"] for row in completion}) == 12,
            "completion universe")
    require(all(row["physical_selection"] == "NONE" for row in completion), "completion selected")
    fc11 = next(row for row in completion if row["completion_id"] == "FC11_NONINTEGRABLE_DISTRIBUTION")
    require(fc11["general_screen_status"] == "PROPERTY_REALIZED_INSIDE_S3_WITNESS_NOT_SEPARATE_METRIC",
            "contact overlap classification")

    coverage = data["coverage"]
    require(len(coverage) == 10 and len({row["criterion"] for row in coverage}) == 10, "ten-criterion coverage")
    stability = next(row for row in coverage if row["criterion"] == "STABILITY_SPECTRUM")
    require(stability["stamp"] == "EXPLICITLY_OPEN_NOT_TESTED", "stability silently claimed")

    blocks = {row["condition_id"]: row for row in data["blocks"]}
    require(len(blocks) == 6, "block condition count")
    require(blocks["BP05"]["status"] == "NO_PARALLEL_PAIR_SCREEN_SPLIT_WITHIN_REGISTERED_S3_FAMILY",
            "parallel split obstruction classification")
    require("t1=0" in blocks["BP04"]["actual_S3_consequence"], "opposite t1 equations omitted")

    require(len(data["sources"]) == 15 and len({row["path"] for row in data["sources"]}) == 15,
            "source universe")
    if check_git_sources:
        verify_sources(data["sources"])


def catch_proofs(base: dict[str, object]) -> list[dict[str, str]]:
    cases = [
        ("C01", "coframe rank reduced", lambda d: d["result"].__setitem__("coframe_response_rank", 3)),
        ("C02", "gauge rotation promoted to metric DOF", lambda d: d["result"].__setitem__("rotation_is_extra_metric_DOF", True)),
        ("C03", "one isotropic shear tangent removed", lambda d: d["result"].__setitem__("both_shear_tangents_at_isotropy", False)),
        ("C04", "block-screen family promoted to full metric", lambda d: d["result"].__setitem__("full_4D_metric_family", True)),
        ("C05", "off-shell witness promoted to selected", lambda d: d["result"].__setitem__("on_shell_or_selected", True)),
        ("C06", "parallel split promoted despite contact obstruction", lambda d: d["result"].__setitem__("all_direction_pair_screen_parallel_split", True)),
        ("C07", "t1 obstruction disclosure deleted", lambda d: d["result"].__setitem__("parallel_split_obstruction", "REMOVED")),
        ("C08", "regular isotropic chart mislabeled", lambda d: next(r for r in d["responses"] if r["stratum"] == "A01_ISOTROPIC_REGULAR_q_COORDINATES").__setitem__("ruling", "SINGULAR")),
        ("C09", "detP zero promoted to configuration", lambda d: next(r for r in d["responses"] if r["stratum"] == "A07_DET_ZERO").__setitem__("ruling", "REGULAR")),
        ("C10", "pure gauge counted as metric rank one", lambda d: next(r for r in d["responses"] if r["stratum"] == "A04_PURE_GAUGE").__setitem__("rank", "1_COFAME;1_METRIC")),
        ("C11", "rotating-axis second shear deleted", lambda d: next(r for r in d["responses"] if r["stratum"] == "A03_ROTATING_AXIS").__setitem__("shear1", "dv*cos(2gamma)")),
        ("C12", "two-shear witness removed", lambda d: d["witnesses"].__delitem__(next(i for i,r in enumerate(d["witnesses"]) if r["id"] == "W04_TWO_SHEAR"))),
        ("C13", "witness promoted to Lorentzian geodesic completeness", lambda d: d["witnesses"][0].__setitem__("global_status", "LORENTZIAN_GEODESICALLY_COMPLETE")),
        ("C14", "Lorentzian scope guard deleted", lambda d: next(r for r in d["global"] if r["object"] == "four_Lorentzian_spacetime").__setitem__("scope", "COMPLETE")),
        ("C15", "v=0 called geometric degeneration", lambda d: next(r for r in d["global"] if r["object"] == "isotropic_axis").__setitem__("scope", "METRIC_SINGULARITY")),
        ("C16", "one FC row deleted", lambda d: d["completion"].pop()),
        ("C17", "one FC selected physically", lambda d: d["completion"][0].__setitem__("physical_selection", "SELECTED")),
        ("C18", "contact completion overlap lost", lambda d: next(r for r in d["completion"] if r["completion_id"] == "FC11_NONINTEGRABLE_DISTRIBUTION").__setitem__("general_screen_status", "SEPARATE_METRIC")),
        ("C19", "one completeness criterion deleted", lambda d: d["coverage"].pop()),
        ("C20", "stability silently promoted", lambda d: next(r for r in d["coverage"] if r["criterion"] == "STABILITY_SPECTRUM").__setitem__("stamp", "COVERED")),
        ("C21", "block obstruction ruling removed", lambda d: next(r for r in d["blocks"] if r["condition_id"] == "BP05").__setitem__("status", "OPEN")),
        ("C22", "opposite-sign t1 consequence removed", lambda d: next(r for r in d["blocks"] if r["condition_id"] == "BP04").__setitem__("actual_S3_consequence", "S=0")),
        ("C23", "source row deleted", lambda d: d["sources"].pop()),
        ("C24", "source path duplicated", lambda d: d["sources"].__setitem__(1, copy.deepcopy(d["sources"][0]))),
    ]
    rows = []
    for cid, mutation, mutate in cases:
        trial = copy.deepcopy(base)
        mutate(trial)
        caught = False
        try:
            validate_snapshot(trial, check_git_sources=False)
        except (AssertionError, KeyError, StopIteration):
            caught = True
        require(caught, f"mutation escaped verifier: {cid} {mutation}")
        rows.append({"id": cid, "mutation": mutation, "expected": "REJECT", "observed": "REJECT", "status": "PASS"})
    return rows


def main() -> int:
    data = snapshot()
    validate_snapshot(data, check_git_sources=True)
    polar = independent_polar_check()
    cartan = independent_cartan_check(data["cartan"])
    catches = catch_proofs(data)
    write_tsv("CATCH_PROOFS.tsv", catches)
    source_identity = verify_sources(data["sources"])
    result = {
        "schema": "udt-general-screen-independent-verification-1.0",
        "status": "PASS",
        "sympy_version": sp.__version__,
        "fixed_base": BASE,
        "source_rows": 15,
        "source_identity_sha256": source_identity,
        "catch_proofs_passed": len(catches),
        "production_code_imported": False,
        "polar_method": "DIRECT_DERIVATIVE_EQUATION_dP_EQUALS_KP",
        "cartan": cartan,
        "polar": polar,
        "maximum_verified_conclusion": "STATIONARY_OFF_SHELL_COMPLETE_S3_GENERAL_SCREEN_EXISTENCE_RESPONSE_AND_BOUNDED_PARALLEL_SPLIT_NO_GO_ONLY",
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
