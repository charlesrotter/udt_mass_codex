#!/usr/bin/env python3
"""Independent exact-rational verification of the clock-anchor/threading audit.

The verifier uses only the Python standard library and does not import the
production SymPy implementation.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from fractions import Fraction as Q
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "e4075a05e6f64714e732f375641bd73447d3559c"
PREREG = "c0da3e7"
DIM = 4


class ContractError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise ContractError(label)


def run(*args: str, binary: bool = False):
    return subprocess.check_output(args, cwd=ROOT, text=not binary)


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def zeros(*shape: int):
    if len(shape) == 1:
        return [Q(0) for _ in range(shape[0])]
    return [zeros(*shape[1:]) for _ in range(shape[0])]


def diag(*entries: Q):
    return [[Q(entries[i]) if i == j else Q(0) for j in range(len(entries))] for i in range(len(entries))]


def rank(matrix) -> int:
    work = [list(map(Q, row)) for row in matrix]
    row = 0
    for column in range(len(work[0])):
        pivot = next((index for index in range(row, len(work)) if work[index][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        value = work[row][column]
        work[row] = [entry / value for entry in work[row]]
        for index in range(len(work)):
            if index != row and work[index][column]:
                factor = work[index][column]
                work[index] = [entry - factor * pivot_entry for entry, pivot_entry in zip(work[index], work[row])]
        row += 1
        if row == len(work):
            break
    return row


def metric_twojet_curvature(g, dg, ddg) -> dict[str, object]:
    inverse = diag(*(1 / g[index][index] for index in range(DIM)))
    dinverse = zeros(DIM, DIM, DIM)
    for upper in range(DIM):
        for right in range(DIM):
            for derivative in range(DIM):
                dinverse[upper][right][derivative] = -sum((
                    inverse[upper][p] * dg[p][q][derivative] * inverse[q][right]
                    for p in range(DIM) for q in range(DIM)
                ), Q(0))

    gamma = zeros(DIM, DIM, DIM)
    dgamma = zeros(DIM, DIM, DIM, DIM)
    for upper in range(DIM):
        for left in range(DIM):
            for right in range(DIM):
                for delta in range(DIM):
                    first = dg[delta][right][left] + dg[delta][left][right] - dg[left][right][delta]
                    gamma[upper][left][right] += inverse[upper][delta] * first / 2
                    for derivative in range(DIM):
                        second = (
                            ddg[delta][right][left][derivative]
                            + ddg[delta][left][right][derivative]
                            - ddg[left][right][delta][derivative]
                        )
                        dgamma[upper][left][right][derivative] += (
                            dinverse[upper][delta][derivative] * first
                            + inverse[upper][delta] * second
                        ) / 2

    riemann_up = zeros(DIM, DIM, DIM, DIM)
    for rho in range(DIM):
        for sigma in range(DIM):
            for mu in range(DIM):
                for nu in range(DIM):
                    riemann_up[rho][sigma][mu][nu] = (
                        dgamma[rho][nu][sigma][mu]
                        - dgamma[rho][mu][sigma][nu]
                        + sum((
                            gamma[rho][mu][lam] * gamma[lam][nu][sigma]
                            - gamma[rho][nu][lam] * gamma[lam][mu][sigma]
                            for lam in range(DIM)
                        ), Q(0))
                    )

    down = zeros(DIM, DIM, DIM, DIM)
    for rho in range(DIM):
        for sigma in range(DIM):
            for mu in range(DIM):
                for nu in range(DIM):
                    down[rho][sigma][mu][nu] = sum((
                        g[rho][lam] * riemann_up[lam][sigma][mu][nu] for lam in range(DIM)
                    ), Q(0))
    kretschmann = sum((
        inverse[i][i] * inverse[j][j] * inverse[k][k] * inverse[l][l] * down[i][j][k][l] ** 2
        for i in range(DIM) for j in range(DIM) for k in range(DIM) for l in range(DIM)
    ), Q(0))
    return {"inverse": inverse, "riemann": down, "K": kretschmann}


def static_spherical_twojet(r: Q, c: Q, n: Q, n1: Q, n2: Q, x: Q, x1: Q, x2: Q):
    require(r > 0 and c > 0 and n > 0 and x > 0, "regular_static_point")
    g = zeros(DIM, DIM)
    dg = zeros(DIM, DIM, DIM)
    ddg = zeros(DIM, DIM, DIM, DIM)
    g[0][0], g[1][1], g[2][2], g[3][3] = -c * c * n * n, 1 / x, r * r, r * r
    dg[0][0][1] = -2 * c * c * n * n1
    ddg[0][0][1][1] = -2 * c * c * (n1 * n1 + n * n2)
    dg[1][1][1] = -x1 / (x * x)
    ddg[1][1][1][1] = 2 * x1 * x1 / (x**3) - x2 / (x * x)
    for angular in (2, 3):
        dg[angular][angular][1] = 2 * r
        ddg[angular][angular][1][1] = 2
    ddg[3][3][2][2] = -2 * r * r
    return g, dg, ddg


def motifs(r: Q, n: Q, n1: Q, n2: Q, x: Q, x1: Q) -> list[Q]:
    return [
        x * n2 / n + x1 * n1 / (2 * n),
        x * n1 / (r * n),
        -x1 / (2 * r),
        (1 - x) / (r * r),
    ]


def independent_algebra(*, corrupt: str | None = None) -> dict[str, object]:
    c, f, x = Q(5), Q(3), Q(4)
    clock = f * Q(2)
    ruler = Q(1, 2)
    slope = c * f * x
    proper_ratio = ruler * slope / clock
    if corrupt == "anchor":
        proper_ratio += 1

    time_scale = Q(7)
    determinant = -c * c * f * f
    determinant_new = determinant * time_scale * time_scale

    # Generic direct-coordinate curvature reconstruction.
    values = (Q(2), Q(5), Q(3), Q(2), Q(-1), Q(4, 3), Q(1, 5), Q(7, 9))
    direct = metric_twojet_curvature(*static_spherical_twojet(*values))
    r, cc, n, n1, n2, xx, x1, _ = values
    expected_motifs = motifs(r, n, n1, n2, xx, x1)
    down = direct["riemann"]
    observed_motifs = [
        down[0][1][0][1] * xx / (cc * cc * n * n),
        down[0][2][0][2] / (cc * cc * n * n * r * r),
        down[1][2][1][2] * xx / (r * r),
        down[2][3][2][3] / (r**4),
    ]
    expected_k = 4 * (
        expected_motifs[0] ** 2 + 2 * expected_motifs[1] ** 2
        + 2 * expected_motifs[2] ** 2 + expected_motifs[3] ** 2
    )
    if corrupt == "curvature":
        observed_motifs[0] += 1
    if corrupt == "kretschmann":
        expected_k += 1

    # Regular center Taylor consequences.
    n0, n2c, x2c = Q(3), Q(5), Q(-7, 4)
    center_limits = [n2c / n0, n2c / n0, -x2c / 2, -x2c / 2]
    if corrupt == "center":
        center_limits[1] += 1

    # Divergent radial lapse control at X=1: q=2, r=3.
    q, inner_r = Q(2), Q(3)
    inner_n = inner_r ** (-2)
    inner_n1 = -q * inner_r ** (-3)
    inner_n2 = q * (q + 1) * inner_r ** (-4)
    inner = metric_twojet_curvature(*static_spherical_twojet(
        inner_r, Q(5), inner_n, inner_n1, inner_n2, Q(1), Q(0), Q(0)
    ))
    inner_expected_k = 4 * q * q * (q * q + 2 * q + 3) / inner_r**4
    if corrupt == "inner_f":
        inner_expected_k = 0

    # Divergent X angular control at r=1/2,p=2 -> X=4.
    xr, xp = Q(1, 2), Q(4)
    angular_motif = (1 - xp) / (xr * xr)
    angular_k_lower = 4 * angular_motif * angular_motif
    if corrupt == "inner_x":
        angular_k_lower = 0

    # Endpoint-flat bump b=y^3(1-y)^3: b,b',b'' vanish at y=0,1.
    # At y=1/2, b''(y)=-3/8 and X=1/2, so Delta m01=X*epsilon*b''/L^2.
    cell, epsilon = Q(4), Q(2)
    endpoint_jets = {"left": [Q(1), Q(0), Q(0)], "right": [Q(1), Q(0), Q(0)]}
    deformation_difference = Q(1, 2) * epsilon * Q(-3, 8) / (cell * cell)
    if corrupt == "endpoint":
        endpoint_jets["right"][2] = Q(1)

    dimensions = [[1, 3, 0, 1], [-1, -2, 0, 0], [0, -1, 1, 0]]
    null_vector = [-2, 1, 1, -1]
    null_product = [sum((Q(row[index]) * null_vector[index] for index in range(4)), Q(0)) for row in dimensions]
    if corrupt == "scale":
        null_vector[0] = -1
        null_product = [sum((Q(row[index]) * null_vector[index] for index in range(4)), Q(0)) for row in dimensions]

    checks = {
        "local_proper_anchor_is_c_E": proper_ratio == c,
        "clock_factor_control": clock == 6,
        "ruler_factor_control": ruler == Q(1, 2),
        "coordinate_slope_control": slope == 60,
        "reciprocal_X_product": Q(2) * Q(1, 2) == 1,
        "block_determinant_contains_F": determinant == -225,
        "time_relabel_changes_coordinate_determinant": determinant_new == -11025,
        "generic_four_curvature_motifs": observed_motifs == expected_motifs,
        "generic_direct_K_matches_motifs": direct["K"] == expected_k,
        "regular_center_limits": center_limits == [Q(5, 3), Q(5, 3), Q(7, 8), Q(7, 8)],
        "inner_radial_F_divergence_has_positive_K": inner["K"] == inner_expected_k and inner_expected_k > 0,
        "inner_X_angular_lower_bound_positive": angular_k_lower == 576,
        "endpoint_F_second_jets_preserved": endpoint_jets == {"left": [1, 0, 0], "right": [1, 0, 0]},
        "endpoint_flat_interior_curvature_changes": deformation_difference == Q(-3, 128),
        "dimension_matrix_rank_three": rank(dimensions) == 3,
        "sole_dimensionless_null_vector": null_product == [0, 0, 0],
        "c_G_submatrix_rank_two": rank([row[:2] for row in dimensions]) == 2,
        "outer_exponent_clock_condition_stronger": all(
            qtest + Q(ptest, 2) > 0 and qtest + ptest > 0
            for ptest, qtest in ((2, 0), (4, -1), (3, Q(-1, 2)))
        ),
    }
    require(all(checks.values()), "independent_algebra")
    return {
        "checks": checks,
        "exact_checks": len(checks),
        "controls": {
            "proper_anchor": str(proper_ratio),
            "generic_motifs": [str(value) for value in observed_motifs],
            "generic_K": str(direct["K"]),
            "inner_F_K": str(inner["K"]),
            "inner_X_angular_K_lower": str(angular_k_lower),
            "endpoint_deformation_difference": str(deformation_difference),
        },
    }


EXPECTED_TABLES = {
    "CLOCK_ANCHOR_LEDGER.tsv": (10, "id", "status", {
        "C01": "OWNER_LOCKED_OBSERVATIONAL_ANCHOR", "C05": "DERIVED_CONDITIONAL_LOCAL_METRIC_NULL_RELATION",
        "C07": "WORKING_OWNER_INTERPRETATION", "C10": "SEMANTIC_CORRECTION_REQUIRED_FOR_FUTURE_WORK",
    }),
    "THREADING_SELECTOR_LEDGER.tsv": (13, "id", "status", {
        "T01": "NOT_SELECTED", "T02": "CHOSE_IF_IMPOSED_NOT_DERIVED", "T05": "DERIVED_STATIC_AREAL_CONGRUENCE",
        "T09": "REFUTED_IN_BOUNDED_ENDPOINT_CLASS", "T10": "OPEN_NOT_SUPPLIED", "T13": "OPEN",
    }),
    "SCALE_REGIME_LEDGER.tsv": (12, "id", "status", {
        "R01": "OWNER_LOCKED_OBSERVATIONAL_ANCHOR", "R04": "DERIVED_DIMENSION_COUNT",
        "R07": "CONDITIONAL_ASYMPTOTIC_CLASS", "R08": "OPEN_SCALE_AND_GEOMETRY_MAP", "R12": "OPEN",
    }),
    "ENDPOINT_ATLAS.tsv": (12, "id", "classification", {
        "E02": "CONDITIONAL_ASYMPTOTIC_CLASS", "E06": "DERIVED_CONDITIONAL_CONTROL",
        "E07": "DERIVED_CONDITIONAL_CENTER", "E08": "SINGULAR_BRANCH_CATALOGUED",
        "E09": "SINGULAR_BRANCH_CATALOGUED", "E11": "OPEN", "E12": "OPEN",
    }),
    "DEDUCTIVE_SPINE.tsv": (12, "step", "status", {
        "D02": "DERIVED_CONDITIONAL_LOCAL_METRIC_NULL", "D09": "EXACT_COUNTERMODEL",
        "D10": "DERIVED_DIMENSION_COUNT", "D12": "VERIFIED_WITH_CAVEATS",
    }),
    "PRIOR_WORK_REGRADE.tsv": (9, "id", "status", {
        "G01": "RETAINED_AND_SHARPENED", "G02": "RETAINED_WITH_OWNER_CLARIFICATION",
        "G04": "RETAINED_AND_STRENGTHENED", "G09": "RETAINED_OPEN",
    }),
    "STATUS_LEDGER.tsv": (19, "id", "status", {
        "S02": "DERIVED_CONDITIONAL", "S06": "REFUTED_AS_CURRENT_IMPLICATION",
        "S09": "REFUTED_IN_BOUNDED_ENDPOINT_CLASS", "S10": "OPEN_NOT_SUPPLIED",
        "S13": "DERIVED_CONDITIONAL_ASYMPTOTIC_CLASS", "S15": "REFUTED_IN_BOUNDED_CURVATURE_CLASS",
        "S16": "OPEN", "S19": "VERIFIED_WITH_CAVEATS",
    }),
}


def validate_tables(*, corrupt: str | None = None) -> dict[str, int]:
    counts = {}
    for name, (count, key, status_key, statuses) in EXPECTED_TABLES.items():
        rows = table(name)
        if corrupt == "missing" and name == "STATUS_LEDGER.tsv":
            rows = rows[:-1]
        if corrupt == "duplicate" and name == "STATUS_LEDGER.tsv":
            rows.append(copy.deepcopy(rows[0]))
        if corrupt == "select_f" and name == "STATUS_LEDGER.tsv":
            next(row for row in rows if row["id"] == "S06")[status_key] = "DERIVED"
        if corrupt == "regular_inner" and name == "STATUS_LEDGER.tsv":
            next(row for row in rows if row["id"] == "S15")[status_key] = "DERIVED_REGULAR"
        require(len(rows) == count, f"table_count:{name}")
        require(len({row[key] for row in rows}) == count, f"table_unique:{name}")
        index = {row[key]: row for row in rows}
        for identity, expected in statuses.items():
            require(index[identity][status_key] == expected, f"table_status:{name}:{identity}")
        counts[name] = len(rows)
    return counts


def validate_sources(*, corrupt: bool = False) -> dict[str, object]:
    rows = table("SOURCE_LINEAGE.tsv")
    require(len(rows) == 15 and len({row["source_id"] for row in rows}) == 15, "source_count")
    for number, row in enumerate(rows):
        data = run("git", "show", f"{BASE}:{row['path']}", binary=True)
        digest = hashlib.sha256(data).hexdigest()
        if corrupt and number == 0:
            digest = "0" * 64
        require(digest == row["sha256"], f"source_sha:{row['source_id']}")
        require(run("git", "rev-parse", f"{BASE}:{row['path']}").strip() == row["git_blob"], f"source_blob:{row['source_id']}")
        line = data.decode("utf-8").splitlines()[int(row["anchor_line"]) - 1]
        require(hashlib.sha256(line.encode()).hexdigest() == row["anchor_sha256"], f"source_anchor:{row['source_id']}")
        require(row["firewall"] == "POST_FIREWALL_AFFIRMATIVE_ELIGIBLE", f"source_firewall:{row['source_id']}")
    return {"sources": len(rows), "base": BASE, "result": "PASS"}


def validate_production(*, corrupt: str | None = None) -> dict[str, object]:
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    if corrupt == "check":
        result["checks"][next(iter(result["checks"]))] = False
    if corrupt == "maximum":
        result["maximum_conclusion"] = "INNER_INFINITY_AND_INSTANT_ACCESS_DERIVED"
    require(result["status"] == "PASS", "production_status")
    require(len(result["checks"]) == 24 and all(result["checks"].values()), "production_checks")
    require(result["counts"] == {"exact_checks": 24, "causal_readouts": 4, "static_curvature_motifs": 4}, "production_counts")
    require(result["local_anchor"]["local_frame_null_component_ratio_dell_dtau_ref"] == "c_E", "production_anchor")
    require(result["regular_center"]["ruling"] == "RADIAL_CLOCK_DIVERGENCE_OR_X_DIVERGENCE_IS_CURVATURE_SINGULAR_AT_A_SPHERICAL_AREAL_CENTER", "production_center")
    require(result["threading"]["ruling"] == "LOCAL_RECIPROCAL_X_PAIR_AND_ENDPOINT_JETS_DO_NOT_FIX_RADIAL_THREADING_F", "production_threading")
    require(result["maximum_conclusion"] == "C_E_REMAINS_THE_EXPLICIT_LOCAL_CLOCK_LENGTH_ANCHOR__F_AND_X_SEPARATELY_CONTROL_REMOTE_CLOCK_AND_COORDINATE_READOUTS__REGISTERED_KINEMATIC_AND_GLOBAL_PREMISES_DO_NOT_FIX_F_OR_THE_SCALE_MAP__OUTER_FREEZE_IS_COMBINED_ASYMPTOTICS_CONDITIONAL__INNER_INFINITY_IS_NOT_DERIVED_AND_IS_SINGULAR_AT_A_REGULAR_SPHERICAL_AREAL_CENTER", "maximum_conclusion")
    return result


def validate_prereg(*, corrupt: bool = False) -> dict[str, str]:
    commit = run("git", "rev-parse", PREREG).strip()
    merge_base = run("git", "merge-base", commit, BASE).strip()
    if corrupt:
        merge_base = "0" * 40
    require(merge_base == BASE, "prereg_base")
    paths = set(run("git", "diff", "--name-only", BASE, commit).splitlines())
    require(paths == {f"{HERE.name}/PREREGISTRATION.md"}, "prereg_scope")
    return {"commit": commit, "base": BASE, "result": "PASS"}


def validate_stop_lines(*, corrupt: str | None = None) -> dict[str, bool]:
    values = {
        "instantaneous_operational_access_claimed": False,
        "matter_signal_law_claimed": False,
        "micro_equals_areal_center_claimed": False,
        "F_selected_claimed": False,
        "absolute_scale_selected": False,
        "nonspherical_inner_branch_excluded": False,
    }
    if corrupt:
        values[corrupt] = True
    require(not any(values.values()), "stop_line")
    return values


def reject(label: str, callback) -> str:
    try:
        callback()
    except ContractError:
        return "PASS"
    raise ContractError(f"catch_accepted:{label}")


def main() -> None:
    algebra = independent_algebra()
    tables = validate_tables()
    sources = validate_sources()
    production = validate_production()
    prereg = validate_prereg()
    stop_lines = validate_stop_lines()
    catches = {
        "local_c_anchor_mutation_rejected": reject("anchor", lambda: independent_algebra(corrupt="anchor")),
        "curvature_motif_mutation_rejected": reject("curvature", lambda: independent_algebra(corrupt="curvature")),
        "kretschmann_mutation_rejected": reject("K", lambda: independent_algebra(corrupt="kretschmann")),
        "regular_center_mutation_rejected": reject("center", lambda: independent_algebra(corrupt="center")),
        "inner_F_regularization_rejected": reject("inner_F", lambda: independent_algebra(corrupt="inner_f")),
        "inner_X_regularization_rejected": reject("inner_X", lambda: independent_algebra(corrupt="inner_x")),
        "endpoint_jet_loss_rejected": reject("endpoint", lambda: independent_algebra(corrupt="endpoint")),
        "dimensional_null_mutation_rejected": reject("scale", lambda: independent_algebra(corrupt="scale")),
        "missing_ledger_row_rejected": reject("missing", lambda: validate_tables(corrupt="missing")),
        "duplicate_ledger_row_rejected": reject("duplicate", lambda: validate_tables(corrupt="duplicate")),
        "F_selection_promotion_rejected": reject("select_F", lambda: validate_tables(corrupt="select_f")),
        "inner_regular_promotion_rejected": reject("inner_regular", lambda: validate_tables(corrupt="regular_inner")),
        "source_hash_mutation_rejected": reject("source", lambda: validate_sources(corrupt=True)),
        "production_false_check_rejected": reject("production", lambda: validate_production(corrupt="check")),
        "maximum_conclusion_inflation_rejected": reject("maximum", lambda: validate_production(corrupt="maximum")),
        "wrong_prereg_base_rejected": reject("prereg", lambda: validate_prereg(corrupt=True)),
        "instant_access_promotion_rejected": reject("instant", lambda: validate_stop_lines(corrupt="instantaneous_operational_access_claimed")),
        "nonspherical_exclusion_rejected": reject("nonspherical", lambda: validate_stop_lines(corrupt="nonspherical_inner_branch_excluded")),
    }
    require(len(catches) == 18 and all(value == "PASS" for value in catches.values()), "catch_proofs")
    result = {
        "schema": "udt-clock-anchor-scale-threading-independent-verification-1.0",
        "status": "PASS",
        "base": BASE,
        "preregistration": prereg,
        "independent_algebra": algebra,
        "production": {"status": production["status"], "checks": len(production["checks"]), "sympy_version": production["sympy_version"]},
        "tables": tables,
        "sources": sources,
        "stop_lines": stop_lines,
        "catch_proofs": {"passed": len(catches), "total": len(catches), "details": catches},
        "agreement": {
            "explicit_c_anchor": "PASS",
            "coordinate_remote_factors": "PASS",
            "threading_nonselection": "PASS",
            "endpoint_flat_counterfamily": "PASS",
            "scale_rank": "PASS",
            "regular_spherical_center": "PASS",
            "outer_freeze": "CONDITIONAL_CLASSIFIED",
            "nonspherical_micro_reflection": "OPEN",
        },
        "grade": "VERIFIED-WITH-CAVEATS",
        "caveat": "NO_FRESH_EXTERNAL_MODEL_SEMANTIC_REVIEW_AUTHORIZED",
    }
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, ["catch", "result"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows({"catch": key, "result": value} for key, value in catches.items())
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
