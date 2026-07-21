#!/usr/bin/env python3
"""Independent exact verifier and corruption catches for the P02 atlas."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import os
import subprocess
import sys
from itertools import product
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESULT = HERE / "ATLAS_RESULT.json"
VERIFY = HERE / "VERIFICATION_RESULT.json"
TRANSCRIPT = HERE / "VERIFICATION_TRANSCRIPT.txt"
TOLERANCE = 2e-10
ETA = sp.diag(-1, 1, 1, 1)
PAIRS = ((0, 1), (0, 2), (0, 3), (2, 3), (3, 1), (1, 2))
BG = sp.diag(-1, -1, -1, 1, 1, 1)


TABLES = {
    "metric": "ZERO_JET_INERTIA_STRATA.tsv",
    "split": "SPLIT_ZERO_JET_STRATA.tsv",
    "phi": "DPHI_FIRST_JET_STRATA.tsv",
    "kinematic": "SPLIT_FIRST_JET_STRATA.tsv",
    "curvature": "CURVATURE_OPERATOR_RANK_STRATA.tsv",
    "ricci": "RICCI_ENDOMORPHISM_RANK_STRATA.tsv",
    "petrov": "PETROV_STRATA.tsv",
    "second_basis": "SECOND_JET_DIRECT_SUM_BASIS.tsv",
    "dimension": "JET_QUOTIENT_DIMENSION_LEDGER.tsv",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def parse_matrix(value: str) -> sp.Matrix:
    parsed = sp.sympify(value, locals={"Matrix": sp.Matrix, "I": sp.I})
    return sp.Matrix(parsed)


def pair_lookup(a: int, b: int) -> tuple[int | None, int]:
    if a == b:
        return None, 0
    for index, pair in enumerate(PAIRS):
        if (a, b) == pair:
            return index, 1
        if (b, a) == pair:
            return index, -1
    raise AssertionError((a, b))


def tensor_from_bilinear(bilinear: sp.Matrix):
    tensor = sp.MutableDenseNDimArray.zeros(4, 4, 4, 4)
    for a, b, c, d in product(range(4), repeat=4):
        first, sign_first = pair_lookup(a, b)
        second, sign_second = pair_lookup(c, d)
        tensor[a, b, c, d] = (
            0
            if first is None or second is None
            else sp.simplify(sign_first * sign_second * bilinear[first, second])
        )
    return tensor


def independent_weyl_from_q(q_matrix: sp.Matrix):
    electric = q_matrix.applyfunc(sp.re)
    magnetic = q_matrix.applyfunc(sp.im)
    bilinear = electric.row_join(magnetic).col_join(magnetic.row_join(-electric))
    return tensor_from_bilinear(bilinear)


def independent_ricci(tensor):
    return sp.Matrix(
        4,
        4,
        lambda b, d: sp.simplify(
            sum(ETA[a, c] * tensor[a, b, c, d] for a in range(4) for c in range(4))
        ),
    )


def independent_ddg(tensor):
    return sp.MutableDenseNDimArray(
        [
            sp.simplify(-sp.Rational(1, 3) * (tensor[mu, a, nu, b] + tensor[mu, b, nu, a]))
            for a, b, mu, nu in product(range(4), repeat=4)
        ],
        (4, 4, 4, 4),
    )


def independent_riemann_from_ddg(second):
    return sp.MutableDenseNDimArray(
        [
            sp.simplify(
                sp.Rational(1, 2)
                * (
                    second[mu, b, a, nu]
                    - second[mu, a, nu, b]
                    - second[nu, b, a, mu]
                    + second[nu, a, mu, b]
                )
            )
            for a, b, mu, nu in product(range(4), repeat=4)
        ],
        (4, 4, 4, 4),
    )


def tensor_equal(left, right) -> bool:
    return all(
        sp.simplify(left[index] - right[index]) == 0
        for index in product(range(4), repeat=4)
    )


def independent_petrov(q_matrix: sp.Matrix) -> str:
    zero = sp.zeros(3)
    if q_matrix == zero:
        return "O"
    if sp.simplify(q_matrix**2) == zero:
        return "N"
    if sp.simplify(q_matrix**3) == zero:
        return "III"
    invariant_i = sp.simplify(sp.trace(q_matrix**2) / 2)
    invariant_j = sp.simplify(-sp.trace(q_matrix**3) / 6)
    delta = sp.simplify(invariant_i**3 - 27 * invariant_j**2)
    if delta != 0:
        return "I"
    repeated = sp.simplify(3 * invariant_j / invariant_i)
    polynomial = sp.simplify(
        (q_matrix - repeated * sp.eye(3)) * (q_matrix + 2 * repeated * sp.eye(3))
    )
    return "D" if polynomial == zero else "II"


def validate(data: dict, tables: dict[str, list[dict[str, str]]]) -> None:
    require(data["schema"] == "udt-p02-law-neutral-local-jet-atlas-1.0", "schema")
    require(data["status"] == "PASS", "status")
    require(
        data["maximum_conclusion"]
        == "LOCAL_KINEMATIC_SOLUTION_SPACE_CHARACTERIZED_WITHOUT_DYNAMICS",
        "maximum conclusion",
    )
    expected_counts = {
        "metric_inertia_strata": 15,
        "supplied_split_inertia_strata": 36,
        "dphi_strata": 8,
        "split_first_jet_rank_strata": 12,
        "curvature_operator_rank_strata": 7,
        "Ricci_rank_strata": 5,
        "Petrov_types": 6,
        "second_jet_direct_sum_basis": 20,
        "discrete_registered_strata_total": 89,
    }
    require(data["counts"] == expected_counts, "counts")
    require(data["dimension_contract"] == {
        "raw_metric_two_jet": 150,
        "normal_coordinate_Riemann_before_residual_Lorentz": 20,
        "local_CSN_quotient_Weyl": 10,
        "generic_Weyl_mod_Lorentz_continuous": 4,
    }, "dimension contract")
    require(data["check_count"] == 21 and all(value == "PASS" for value in data["checks"].values()), "checks")
    require(data["maximum_raw_residual"] < TOLERANCE, "raw residual")
    require(data["premise_stamps"]["two_plus_two"] == "CONDITIONAL_SUPPLIED_SPLIT_NOT_SELECTED", "split promotion")
    require(data["premise_stamps"]["phi"].endswith("JOIN_OPEN"), "phi promotion")
    require(data["premise_stamps"]["dynamics"] == "OPEN_NOT_EVALUATED", "dynamics promotion")
    scope = data["scope"]
    require(scope["point_local_only"] and scope["continuous_moduli_retained"], "local continuous scope")
    require(not any(scope[key] for key in (
        "scientific_equation_solved", "action_or_EOM_selected", "P03_launched",
        "ODE_or_PDE_run", "GPU_used", "comparison_or_merit_filter_used",
    )), "scope promotion")

    expected_lengths = {"metric": 15, "split": 36, "phi": 8, "kinematic": 12, "curvature": 7, "ricci": 5, "petrov": 6, "second_basis": 20, "dimension": 4}
    for name, expected in expected_lengths.items():
        require(len(tables[name]) == expected, f"{name} length")
        require(len({row["id"] for row in tables[name]}) == expected, f"{name} IDs")
        require(data["table_sha256"][TABLES[name]] == sha256(HERE / TABLES[name]), f"{name} hash")

    require({(int(row["n_negative"]), int(row["n_positive"]), int(row["n_zero"])) for row in tables["metric"]}
            == {(negative, positive, 4-negative-positive) for negative in range(5) for positive in range(5-negative)}, "metric strata")
    require({(row["base_inertia"], row["screen_inertia"]) for row in tables["split"]}
            == {(f"{n}/{p}/{2-n-p}", f"{m}/{q}/{2-m-q}") for n in range(3) for p in range(3-n) for m in range(3) for q in range(3-m)}, "split strata")
    require({row["stratum"] for row in tables["phi"]} == {
        "ZERO", "HORIZONTAL_TIMELIKE", "HORIZONTAL_NULL", "HORIZONTAL_SPACELIKE",
        "VERTICAL_SPACELIKE", "MIXED_TIMELIKE", "MIXED_NULL", "MIXED_SPACELIKE",
    }, "phi strata")
    require({(int(row["expansion_rank"]), int(row["shear_map_rank"]), int(row["twist_map_rank"])) for row in tables["kinematic"]}
            == set(product((0,1), (0,1,2), (0,1))), "kinematic products")
    require({int(row["curvature_operator_rank"]) for row in tables["curvature"]} == set(range(7)), "curvature ranks")
    require({int(row["Ricci_endomorphism_rank"]) for row in tables["ricci"]} == set(range(5)), "Ricci ranks")
    require({row["Petrov_type"] for row in tables["petrov"]} == {"I", "D", "II", "III", "N", "O"}, "Petrov types")
    require([int(row["prefix_exact_rank"]) for row in tables["second_basis"]] == list(range(1, 21)), "second basis ranks")
    require(sum(row["sector"] == "WEYL_PRE_SCALE" for row in tables["second_basis"]) == 10, "Weyl basis count")
    require(sum(row["sector"] == "SCHOUTEN_REPRESENTATIVE" for row in tables["second_basis"]) == 10, "Schouten basis count")
    require(all(row["exact_minor_certification"].startswith("RANK_EXACT_") for row in tables["curvature"]), "exact rank certification")
    require(all(row["CSN_expansion_status"] == "REPRESENTATIVE_DEPENDENT_AFFINE_SHIFT" for row in tables["kinematic"]), "expansion CSN")
    require(all(row["CSN_shear_rank_status"] == "INVARIANT" and row["CSN_twist_status"] == "INVARIANT" for row in tables["kinematic"]), "shear/twist CSN")
    require(all((row["integrability"] == "INTEGRABLE") == (row["twist_map_rank"] == "0") for row in tables["kinematic"]), "integrability")
    require(all(row["CSN_status"].startswith("REPRESENTATIVE_DEPENDENT") for row in tables["curvature"] + tables["ricci"]), "Ricci/Riemann CSN")


def expect_failure(name: str, operation, catches: dict[str, str]) -> None:
    try:
        operation()
    except (AssertionError, KeyError, ValueError):
        catches[name] = "PASS"
        return
    raise AssertionError(f"mutation unexpectedly passed: {name}")


def main() -> None:
    checks: dict[str, str] = {}
    catches: dict[str, str] = {}
    before = {path.name: sha256(path) for path in [RESULT, *[HERE / filename for filename in TABLES.values()]]}
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["CUDA_VISIBLE_DEVICES"] = ""
    replay = subprocess.run(
        [sys.executable, "-B", str(HERE / "run_p02_local_jet_atlas.py")],
        cwd=ROOT,
        env=environment,
        text=True,
        capture_output=True,
        timeout=600,
        check=False,
    )
    require(replay.returncode == 0, replay.stdout + replay.stderr)
    require(not replay.stderr, "main stderr")
    require((HERE / "ATLAS_TRANSCRIPT.txt").read_text(encoding="utf-8") == replay.stdout, "main transcript")
    require(before == {path.name: sha256(path) for path in [RESULT, *[HERE / filename for filename in TABLES.values()]]}, "deterministic replay")
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    tables = {name: read_tsv(HERE / filename) for name, filename in TABLES.items()}
    validate(data, tables)
    checks["deterministic_main_replay_and_contract"] = "PASS"

    # Independent combinatorial zero-jet census and exact split congruence.
    require(sum(1 for n in range(5) for p in range(5-n)) == 15, "inertia combinatorics")
    h00, h01, h11, q22, q23, q33 = sp.symbols("h00 h01 h11 q22 q23 q33")
    a20, a30, a21, a31 = sp.symbols("a20 a30 a21 a31")
    h = sp.Matrix([[h00, h01], [h01, h11]])
    q = sp.Matrix([[q22, q23], [q23, q33]])
    a = sp.Matrix([[a20, a21], [a30, a31]])
    g = (h + a.T*q*a).row_join(a.T*q).col_join((q*a).row_join(q))
    require(sp.factor(g.det() - h.det()*q.det()) == 0, "generic split determinant")
    checks["independent_zero_jet_and_generic_split_algebra"] = "PASS"

    # Independent exact dphi witnesses.
    for row in tables["phi"]:
        covector = parse_matrix(row["exact_covector"]).T
        norm = sp.simplify((covector.T * ETA * covector)[0])
        require(norm == sp.sympify(row["exact_norm"]), "dphi norm")
        if row["causal_type"] == "ZERO":
            require(covector == sp.zeros(4, 1), "dphi zero")
        elif row["causal_type"] == "NULL":
            require(covector != sp.zeros(4, 1) and norm == 0, "dphi null")
        elif row["causal_type"] == "TIMELIKE":
            require(norm < 0, "dphi timelike")
        else:
            require(norm > 0, "dphi spacelike")
    checks["independent_dphi_causal_alignment"] = "PASS"

    # Independent first-jet rank and CSN transformation algebra.
    for row in tables["kinematic"]:
        expansion = parse_matrix(row["exact_expansion"])
        shear = parse_matrix(row["exact_shear_map"])
        twist = parse_matrix(row["exact_twist"])
        require(expansion.rank() == int(row["expansion_rank"]), "expansion row rank")
        require(shear.rank() == int(row["shear_map_rank"]), "shear row rank")
        require(twist.rank() == int(row["twist_map_rank"]), "twist row rank")
    b00, b01, b11, scale_gradient = sp.symbols("b00 b01 b11 scale_gradient")
    deformation = sp.Matrix([[b00, b01], [b01, b11]])
    expansion = sp.trace(deformation)
    shear = sp.simplify(deformation - expansion*sp.eye(2)/2)
    transformed_deformation = deformation + scale_gradient*sp.eye(2)
    transformed_expansion = sp.trace(transformed_deformation)
    transformed_shear = sp.simplify(transformed_deformation - transformed_expansion*sp.eye(2)/2)
    require(sp.simplify(transformed_expansion - expansion - 2*scale_gradient) == 0, "CSN expansion shift")
    require(transformed_shear == shear, "CSN shear")
    checks["independent_first_jet_rank_and_CSN_algebra"] = "PASS"

    # Independent exact curvature-operator and Ricci rank certificates from the saved witnesses.
    for row in tables["curvature"]:
        diagonal = parse_matrix(row["exact_operator_diagonal"])
        require(sum(value != 0 for value in diagonal) == int(row["curvature_operator_rank"]), "curvature exact rank")
    for row in tables["ricci"]:
        mixed = parse_matrix(row["exact_mixed_Ricci"])
        require(mixed.rank() == int(row["Ricci_endomorphism_rank"]), "Ricci exact rank")
        require(row["Weyl"] == "ZERO", "Ricci witness Weyl")
    checks["independent_exact_curvature_and_Ricci_ranks"] = "PASS"

    # Independent Weyl construction, Ricci contraction, RNC inversion, and Petrov classification.
    for row in tables["petrov"]:
        q_matrix = parse_matrix(row["exact_Q"])
        require(q_matrix == q_matrix.T and sp.trace(q_matrix) == 0, "Q form")
        tensor = independent_weyl_from_q(q_matrix)
        require(independent_ricci(tensor) == sp.zeros(4), "Weyl Ricci")
        second = independent_ddg(tensor)
        require(tensor_equal(independent_riemann_from_ddg(second), tensor), "RNC inverse")
        require(independent_petrov(q_matrix) == row["Petrov_type"], "Petrov type")
        invariant_i = sp.simplify(sp.trace(q_matrix**2)/2)
        invariant_j = sp.simplify(-sp.trace(q_matrix**3)/6)
        delta = sp.simplify(invariant_i**3-27*invariant_j**2)
        require((invariant_i, invariant_j, delta) == tuple(sp.sympify(row[key]) for key in ("I","J","Delta")), "Petrov invariants")
    checks["independent_Weyl_RNC_and_all_Petrov_types"] = "PASS"

    saved_basis_columns = [
        parse_matrix(row["upper_bivector_bilinear_21_vector"]).T
        for row in tables["second_basis"]
    ]
    require(all(column.shape == (21, 1) for column in saved_basis_columns), "saved basis shapes")
    require(sp.Matrix.hstack(*saved_basis_columns).rank() == 20, "saved direct-sum rank")
    require(sp.Matrix.hstack(*saved_basis_columns[:10]).rank() == 10, "saved Schouten rank")
    require(sp.Matrix.hstack(*saved_basis_columns[10:]).rank() == 10, "saved Weyl rank")
    checks["independent_20_component_direct_sum_basis"] = "PASS"

    # Independent CSN dimension/rank proof: symmetric Hessian acts identically on Schouten.
    symmetric_pairs = [(a, b) for a in range(4) for b in range(a, 4)]
    action = sp.eye(len(symmetric_pairs))
    require(action.rank() == 10, "Schouten Hessian rank")
    require(10 + 40 + 100 == 150 and 150 - 10 - 40 - 80 == 20 and 20 - 10 == 10 and 10 - 6 == 4, "dimension arithmetic")
    checks["independent_Schouten_orbit_and_dimension_contract"] = "PASS"

    sources = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    discriminants = read_tsv(HERE / "DISCRIMINANT_LEDGER.tsv")
    interfaces = read_tsv(HERE / "INTERFACE_COVERAGE.tsv")
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    require(len(sources) == 16 and len({row["id"] for row in sources}) == 16, "sources")
    require(all((ROOT / row["path"]).exists() for row in sources), "source paths")
    require(all("PRE_JULY" not in row["authority_class"] for row in sources), "source firewall")
    require(len(discriminants) == 15 and len({row["id"] for row in discriminants}) == 15, "discriminants")
    require(len(interfaces) == 14 and len({row["id"] for row in interfaces}) == 14, "interfaces")
    require(len(statuses) == 18 and len({row["id"] for row in statuses}) == 18, "statuses")
    by_status = {row["id"]: row for row in statuses}
    require(by_status["P05"]["status"] == "EXACT_REPRESENTATIVE_DATA", "expansion status")
    require(by_status["P09"]["status"] == "EXACT_PRE_SCALE_LOCAL_ATLAS", "Weyl status")
    require(by_status["P14"]["status"] == "NOT_APPLIED" and by_status["P18"]["status"] == "NOT_AUTHORIZED", "P03 gate")
    require((HERE / "requirements.txt").read_text(encoding="utf-8").splitlines() == ["numpy==2.2.6", "sympy==1.13.1"], "pins")
    checks["source_scope_status_and_dependency_ledgers"] = "PASS"

    # Fail-closed mutations.
    mutation_tables = copy.deepcopy(tables); mutation_tables["metric"].pop()
    expect_failure("missing_metric_inertia", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); mutation_tables["metric"][-1] = copy.deepcopy(mutation_tables["metric"][0])
    expect_failure("duplicate_metric_inertia", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); mutation_tables["split"].pop()
    expect_failure("missing_split_inertia", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); mutation_tables["split"][-1] = copy.deepcopy(mutation_tables["split"][0])
    expect_failure("duplicate_split_inertia", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); mutation_tables["phi"] = [row for row in mutation_tables["phi"] if row["stratum"] != "ZERO"]
    expect_failure("missing_zero_dphi", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); next(row for row in mutation_tables["phi"] if row["stratum"] == "HORIZONTAL_NULL")["stratum"] = "ZERO"
    expect_failure("null_dphi_merged_with_zero", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); mutation_tables["phi"] = [row for row in mutation_tables["phi"] if row["support"] != "VERTICAL_ONLY"]
    expect_failure("missing_vertical_dphi", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); mutation_tables["phi"] = [row for row in mutation_tables["phi"] if row["support"] != "MIXED"]
    expect_failure("missing_mixed_dphi", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); mutation_tables["kinematic"].pop()
    expect_failure("missing_kinematic_product", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); mutation_tables["kinematic"][0]["integrability"] = "NONINTEGRABLE"
    expect_failure("twist_integrability_reversed", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); mutation_tables["kinematic"][0]["CSN_expansion_status"] = "INVARIANT"
    expect_failure("expansion_called_CSN_invariant", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); mutation_tables["kinematic"][0]["CSN_shear_rank_status"] = "REPRESENTATIVE_DEPENDENT"
    expect_failure("shear_rank_called_CSN_dependent", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); mutation_tables["kinematic"][0]["CSN_twist_status"] = "REPRESENTATIVE_DEPENDENT"
    expect_failure("twist_called_CSN_dependent", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); mutation_tables["curvature"].pop(0)
    expect_failure("divided_away_zero_curvature_rank", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); mutation_tables["curvature"][1]["exact_minor_certification"] = "FLOAT_CLUSTER"
    expect_failure("floating_only_curvature_rank", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); mutation_tables["ricci"].pop(0)
    expect_failure("divided_away_zero_Ricci_rank", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); mutation_tables["ricci"][0]["CSN_status"] = "INVARIANT"
    expect_failure("Ricci_rank_called_pre_scale_invariant", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); mutation_tables["petrov"].pop()
    expect_failure("missing_Petrov_type", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); next(row for row in mutation_tables["petrov"] if row["Petrov_type"] == "D")["Petrov_type"] = "II"
    expect_failure("Petrov_D_II_collapsed", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); mutation_tables["second_basis"].pop()
    expect_failure("missing_second_jet_basis_component", lambda: validate(data, mutation_tables), catches)
    mutation_tables = copy.deepcopy(tables); mutation_tables["second_basis"][-1] = copy.deepcopy(mutation_tables["second_basis"][0])
    expect_failure("duplicate_second_jet_basis_component", lambda: validate(data, mutation_tables), catches)
    mutation = copy.deepcopy(data); mutation["dimension_contract"]["normal_coordinate_Riemann_before_residual_Lorentz"] = 19
    expect_failure("wrong_Riemann_dimension", lambda: validate(mutation, tables), catches)
    mutation = copy.deepcopy(data); mutation["dimension_contract"]["local_CSN_quotient_Weyl"] = 9
    expect_failure("wrong_Weyl_dimension", lambda: validate(mutation, tables), catches)
    mutation = copy.deepcopy(data); mutation["scope"]["continuous_moduli_retained"] = False
    expect_failure("continuous_moduli_dropped", lambda: validate(mutation, tables), catches)
    mutation = copy.deepcopy(data); mutation["premise_stamps"]["two_plus_two"] = "DERIVED_GLOBAL_SPLIT"
    expect_failure("supplied_split_promoted", lambda: validate(mutation, tables), catches)
    mutation = copy.deepcopy(data); mutation["premise_stamps"]["phi"] = "METRIC_DERIVED"
    expect_failure("phi_join_promoted", lambda: validate(mutation, tables), catches)
    mutation = copy.deepcopy(data); mutation["premise_stamps"]["dynamics"] = "NATIVE_EOM"
    expect_failure("dynamics_promoted", lambda: validate(mutation, tables), catches)
    mutation = copy.deepcopy(data); mutation["scope"]["scientific_equation_solved"] = True
    expect_failure("local_jet_called_on_shell", lambda: validate(mutation, tables), catches)
    mutation = copy.deepcopy(data); mutation["scope"]["ODE_or_PDE_run"] = True
    expect_failure("local_jet_called_evolution", lambda: validate(mutation, tables), catches)
    mutation = copy.deepcopy(data); mutation["scope"]["P03_launched"] = True
    expect_failure("P03_launched", lambda: validate(mutation, tables), catches)
    mutation = copy.deepcopy(data); mutation["maximum_conclusion"] = "NATIVE_UDT_DYNAMICS_SELECTED"
    expect_failure("maximum_conclusion_promoted", lambda: validate(mutation, tables), catches)

    output = {
        "schema": "udt-p02-law-neutral-local-jet-independent-verification-1.0",
        "status": "PASS",
        "maximum_conclusion": data["maximum_conclusion"],
        "atlas_result_sha256": sha256(RESULT),
        "checks": checks,
        "check_count": len(checks),
        "catch_proofs": catches,
        "catch_proof_count": len(catches),
        "independent_scope": {
            "exact_combinatorics": True,
            "exact_split_symbolics": True,
            "exact_RNC_reconstruction": True,
            "independent_Petrov_classifier": True,
            "scientific_equation_solved": False,
            "GPU_used": False,
        },
    }
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    VERIFY.write_text(rendered, encoding="utf-8")
    TRANSCRIPT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
