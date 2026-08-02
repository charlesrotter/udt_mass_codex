#!/usr/bin/env python3
"""Independent Koszul/frame verification for the Cartan production audit."""

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
ETA = (-1, 1, 1, 1)
PAIRS = tuple((i, j) for i in range(4) for j in range(i + 1, 4))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_source_manifest() -> dict[str, object]:
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == 29
    assert len({row["path"] for row in rows}) == 29
    for row in rows:
        path = ROOT / row["path"]
        assert path.is_file()
        assert sha256(path) == row["sha256"]
        assert path.stat().st_size == int(row["bytes"])
        blob = subprocess.run(
            ["git", "rev-parse", f"HEAD:{row['path']}"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        assert blob == row["git_blob"]
    return {"rows": len(rows), "manifest_sha256": sha256(HERE / "SOURCE_MANIFEST.tsv")}


def independent_koszul_curvature() -> dict[str, object]:
    p1, p2, p3, s1, s2, s3, m, t = sp.symbols("p1 p2 p3 s1 s2 s3 m t", real=True)
    p = (p1, p2, p3)
    s = (s1, s2, s3)
    variables = p + s
    deriv = {
        (direction, variable): sp.Symbol(f"K_E{direction}_{variable}", real=True)
        for direction in (1, 2, 3)
        for variable in variables
    }

    # dtheta^a=A^a_bc theta^b wedge theta^c, frozen independently from the source formula.
    A: dict[tuple[int, int, int], sp.Expr] = {}
    for index, value in enumerate(p, start=1):
        A[(0, 0, index)] = value
    A[(1, 1, 2)] = -p2
    A[(1, 1, 3)] = -p3
    A[(1, 2, 3)] = t
    A[(2, 1, 2)] = s1 / 2
    A[(2, 1, 3)] = -m
    A[(2, 2, 3)] = -s3 / 2
    A[(3, 1, 2)] = m
    A[(3, 1, 3)] = s1 / 2
    A[(3, 2, 3)] = s2 / 2

    def aval(a: int, b: int, c: int) -> sp.Expr:
        if b == c:
            return sp.Integer(0)
        if b < c:
            return A.get((a, b, c), sp.Integer(0))
        return -A.get((a, c, b), sp.Integer(0))

    # [E_b,E_c]^a=-A^a_bc.
    def structure(a: int, b: int, c: int) -> sp.Expr:
        return -aval(a, b, c)

    # Exact-scalar commutator closure, derived without exterior-form code.
    closure: dict[sp.Symbol, sp.Expr] = {}
    for field in (p, s):
        for i, j in ((1, 2), (1, 3), (2, 3)):
            rhs = deriv[(j, field[i - 1])]
            rhs += sum(structure(k, i, j) * field[k - 1] for k in (1, 2, 3))
            closure[deriv[(i, field[j - 1])]] = sp.factor(rhs)

    def frame_derivative(direction: int, expression: sp.Expr) -> sp.Expr:
        if direction == 0:
            return sp.Integer(0)
        value = sum(
            sp.diff(expression, variable) * deriv[(direction, variable)]
            for variable in variables
        )
        value += sp.diff(expression, m) * (-m * p[direction - 1])
        value += sp.diff(expression, t) * (t * (p[direction - 1] - s[direction - 1]))
        return sp.factor(sp.expand(value).subs(closure))

    # Koszul: Gamma^a_ij for nabla_{E_i} E_j.
    gamma: dict[tuple[int, int, int], sp.Expr] = {}
    for a in range(4):
        for i in range(4):
            for j in range(4):
                value = (
                    structure(a, i, j)
                    - ETA[a] * ETA[i] * structure(i, j, a)
                    + ETA[a] * ETA[j] * structure(j, a, i)
                ) / 2
                gamma[(a, i, j)] = sp.factor(value)

    # Independent zero-torsion and metric-compatibility checks.
    for a in range(4):
        for i, j in PAIRS:
            assert sp.simplify(
                gamma[(a, i, j)] - gamma[(a, j, i)] - structure(a, i, j)
            ) == 0
    for i in range(4):
        for a in range(4):
            for b in range(4):
                assert sp.simplify(
                    ETA[a] * gamma[(a, i, b)] + ETA[b] * gamma[(b, i, a)]
                ) == 0

    curvature: dict[tuple[int, int, int, int], sp.Expr] = {}
    for a in range(4):
        for b in range(4):
            for c, d in PAIRS:
                value = frame_derivative(c, gamma[(a, d, b)])
                value -= frame_derivative(d, gamma[(a, c, b)])
                value += sum(
                    gamma[(e, d, b)] * gamma[(a, c, e)]
                    - gamma[(e, c, b)] * gamma[(a, d, e)]
                    - structure(e, c, d) * gamma[(a, e, b)]
                    for e in range(4)
                )
                curvature[(a, b, c, d)] = sp.factor(sp.expand(value).subs(closure))

    nonzero_lower_pairs: set[tuple[int, int]] = set()
    bilinear_rows = 0
    alternating_rows = 0
    symmetric_rows = 0
    for a, b in PAIRS:
        for i, j in PAIRS:
            expression = sp.expand(ETA[a] * curvature[(a, b, i, j)])
            if expression != 0:
                nonzero_lower_pairs.add((a, b))
            if i == 0:
                continue
            forward = expression.coeff(p[i - 1] * s[j - 1])
            reverse = expression.coeff(p[j - 1] * s[i - 1])
            alternating = sp.simplify((forward - reverse) / 2)
            symmetric = sp.simplify((forward + reverse) / 2)
            if alternating != 0 or symmetric != 0:
                bilinear_rows += 1
            alternating_rows += int(alternating != 0)
            symmetric_rows += int(symmetric != 0)

    return {
        "nonzero_curvature_lower_pairs": len(nonzero_lower_pairs),
        "rows_with_p_sigma_bilinears": bilinear_rows,
        "rows_with_nonzero_alternating_projection": alternating_rows,
        "rows_with_nonzero_symmetric_projection": symmetric_rows,
        "torsion": "ZERO_EXACT",
        "metric_compatibility": "PASS_EXACT",
    }


def semantic_checks(
    result: dict[str, object], objects: list[dict[str, str]], branches: list[dict[str, str]]
) -> None:
    affine = result["affine_response"]
    assert affine == {
        "coefficient_dimension": 6,
        "quotient_rank": 1,
        "universally_exact_kernel_dimension": 5,
    }
    logs = result["cartan_contact_reconstruction"]
    assert logs["fixed_coefficient"] == 1
    assert logs["minus_dphi_wedge_dlogt1"] == "dphi_wedge_dsigma"
    assert logs["m_role"] == "NOT_LOAD_BEARING_FIXED_MAURER_CARTAN_PRESENTATION_ONLY"
    assert result["maximum_grade"] == (
        "SPLIT_RELATIVE_DIFFERENTIAL_PRODUCTION_ONLY__PRIMITIVE_AND_NATURALITY_OPEN"
    )
    assert len(objects) == 10
    object_map = {row["object"]: row for row in objects}
    assert len(object_map) == 10
    assert object_map["minus_dphi_wedge_dlog_abs_t1"]["presentation"] == (
        "REGISTERED_SPLIT_RELATIVE_O2_AND_ORIENTATION_SAFE"
    )
    assert object_map["lambda_from_phi_log_t1"]["production"] == (
        "AVAILABLE_PRIMITIVE_NOT_SELECTED_CONNECTION"
    )
    assert object_map["dlog_abs_m"]["production"] == (
        "NOT_LOAD_BEARING_GAUGE_SEPARATION_CAN_MIX_WITH_SKEW_L1"
    )
    assert object_map["Levi_Civita_connection_scalar_one_form"]["exactness"] == "NOT_TENSOR"
    assert len(branches) == 10
    branch_map = {row["branch"]: row for row in branches}
    assert len(branch_map) == 10
    assert branch_map["FC07_MAPPING_TORUS_ALL_EIGHT"]["pullback_rank"] == "0"
    assert branch_map["S3_GENERAL_SCREEN_DEGENERATE"]["pullback_rank"] == "UNDEFINED"
    assert branch_map["S3_GENERAL_SCREEN_FUNCTIONAL_DEPENDENCE"]["pullback_rank"] == "0"
    assert branch_map["S3_GENERAL_SCREEN_FORMAL_FREE"]["pullback_rank"] == "1"


def catches(
    result: dict[str, object], objects: list[dict[str, str]], branches: list[dict[str, str]]
) -> list[dict[str, str]]:
    mutations = []

    def register(catch_id: str, name: str, mutate) -> None:
        r = copy.deepcopy(result)
        o = copy.deepcopy(objects)
        b = copy.deepcopy(branches)
        mutate(r, o, b)
        caught = False
        try:
            semantic_checks(r, o, b)
        except (AssertionError, KeyError):
            caught = True
        assert caught, f"uncaught semantic mutation: {name}"
        mutations.append({"catch_id": catch_id, "mutation": name, "result": "PASS_CAUGHT"})

    register("C01", "quotient_rank_promoted", lambda r, o, b: r["affine_response"].update(quotient_rank=2))
    register("C02", "exact_kernel_reduced", lambda r, o, b: r["affine_response"].update(universally_exact_kernel_dimension=4))
    register("C03", "fixed_coefficient_changed", lambda r, o, b: r["cartan_contact_reconstruction"].update(fixed_coefficient=2))
    register("C04", "observer_natural_promotion", lambda r, o, b: r.update(maximum_grade="OBSERVER_NATURAL_FIXED_COEFFICIENT_PRODUCTION_DERIVED_IN_BOUNDED_UNIVERSE"))
    register("C05", "split_stamp_removed", lambda r, o, b: next(x for x in o if x["object"] == "minus_dphi_wedge_dlog_abs_t1").update(presentation="OBSERVER_NATURAL"))
    register("C06", "primitive_promoted_to_connection", lambda r, o, b: next(x for x in o if x["object"] == "lambda_from_phi_log_t1").update(production="SELECTED_CONNECTION"))
    register("C07", "connection_promoted_to_tensor", lambda r, o, b: next(x for x in o if x["object"] == "Levi_Civita_connection_scalar_one_form").update(exactness="TENSOR"))
    register("C08", "FC07_rank_promoted", lambda r, o, b: next(x for x in b if x["branch"] == "FC07_MAPPING_TORUS_ALL_EIGHT").update(pullback_rank="1"))
    register("C09", "functional_dependence_rank_promoted", lambda r, o, b: next(x for x in b if x["branch"] == "S3_GENERAL_SCREEN_FUNCTIONAL_DEPENDENCE").update(pullback_rank="1"))
    register("C10", "degenerate_metric_called_rank_one", lambda r, o, b: next(x for x in b if x["branch"] == "S3_GENERAL_SCREEN_DEGENERATE").update(pullback_rank="1"))
    register("C11", "complete_S3_witness_removed", lambda r, o, b: b.pop(0))
    return mutations


def main() -> None:
    source = verify_source_manifest()
    with (HERE / "DERIVATION_RESULT.json").open(encoding="utf-8") as handle:
        result = json.load(handle)
    objects = read_tsv(HERE / "OBJECT_PRODUCTION_LEDGER.tsv")
    branches = read_tsv(HERE / "BRANCH_PULLBACK_RANK_ATLAS.tsv")
    semantic_checks(result, objects, branches)

    # Independent coefficient-space calculation.
    coefficient_matrix = sp.Matrix([[0, 0, -1, 0, 1, 0]])
    assert coefficient_matrix.rank() == 1
    assert len(coefficient_matrix.nullspace()) == 5
    jacobian = sp.Matrix([[1, 0], [1, -1]])
    assert jacobian.det() == -1

    # Complete S3 constructive witness: at (0,0,1,0) in unit S3 subset R4,
    # dx1 and dx2 are independent tangent covectors; P=exp(x2/2)I is global and invertible.
    witness = {
        "domain": "unit_S3_in_R4",
        "phi": "x1",
        "sigma": "x2",
        "P": "exp(x2/2)_I",
        "check_point": "(0,0,1,0)",
        "dphi_wedge_dsigma": "NONZERO_ON_TANGENT_E1_E2",
        "detP": "exp(x2)_POSITIVE",
    }

    independent_curvature = independent_koszul_curvature()
    production_curvature = result["complete_S3_isotropic_curvature_control"]
    assert independent_curvature["nonzero_curvature_lower_pairs"] == production_curvature["nonzero_curvature_slots"]
    for key in (
        "rows_with_p_sigma_bilinears",
        "rows_with_nonzero_alternating_projection",
        "rows_with_nonzero_symmetric_projection",
    ):
        assert independent_curvature[key] == production_curvature[key]

    catch_rows = catches(result, objects, branches)
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["catch_id", "mutation", "result"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(catch_rows)

    independent = {
        "schema": "udt-complete-cell-cartan-alternating-independent-verification-1.0",
        "status": "PASS_VERIFIED_WITH_CAVEATS_NO_FRESH_BLIND_MODEL",
        "source_manifest": source,
        "affine_rank": 1,
        "exact_kernel_dimension": 5,
        "cartan_contact_jacobian_determinant": -1,
        "complete_S3_witness": witness,
        "koszul_curvature": independent_curvature,
        "semantic_catch_proofs": len(catch_rows),
        "production_code_imported": False,
        "fresh_blind_adversarial_model": False,
    }
    with (HERE / "INDEPENDENT_RESULT.json").open("w", encoding="utf-8") as handle:
        json.dump(independent, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(independent, sort_keys=True))


if __name__ == "__main__":
    main()
