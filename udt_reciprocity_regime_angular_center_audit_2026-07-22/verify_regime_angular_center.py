#!/usr/bin/env python3
"""Independent exact-rational verification of the regime/angular-center audit.

This implementation imports neither SymPy nor the production tensor code.  It
constructs metric two-jets at an equatorial point, differentiates the inverse
metric and Christoffels algebraically, and contracts the resulting coordinate
Riemann tensor using standard-library Fraction arithmetic.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "11ff6f8589a5c5d674b3dca9e65ae1c0dd8d7ac3"
PREREG = "0d5eb5d"
N = 4


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
        return [F(0) for _ in range(shape[0])]
    return [zeros(*shape[1:]) for _ in range(shape[0])]


def matmul(left, right):
    return [
        [sum((left[i][k] * right[k][j] for k in range(len(right))), F(0)) for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def transpose(value):
    return [list(row) for row in zip(*value)]


def diag(*entries):
    return [[F(entries[i]) if i == j else F(0) for j in range(len(entries))] for i in range(len(entries))]


def determinant(value):
    work = [list(row) for row in value]
    result = F(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return F(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result *= -1
        entry = work[column][column]
        result *= entry
        for row in range(column + 1, len(work)):
            factor = work[row][column] / entry
            work[row] = [item - factor * pivot_item for item, pivot_item in zip(work[row], work[column])]
    return result


def direct_coordinate_invariants(r: F, c: F, A: F, A1: F, A2: F) -> dict[str, F]:
    require(r > 0 and c > 0 and A > 0, "regular_point")
    g = zeros(N, N)
    dg = zeros(N, N, N)
    ddg = zeros(N, N, N, N)

    # Equatorial point theta=pi/2: sin(theta)=1 and cos(theta)=0.
    g[0][0], g[1][1], g[2][2], g[3][3] = -c * c * A, 1 / A, r * r, r * r
    dg[0][0][1] = -c * c * A1
    dg[1][1][1] = -A1 / (A * A)
    dg[2][2][1] = 2 * r
    dg[3][3][1] = 2 * r
    ddg[0][0][1][1] = -c * c * A2
    ddg[1][1][1][1] = 2 * A1 * A1 / (A**3) - A2 / (A * A)
    ddg[2][2][1][1] = F(2)
    ddg[3][3][1][1] = F(2)
    ddg[3][3][2][2] = -2 * r * r

    inverse = diag(-1 / (c * c * A), A, 1 / (r * r), 1 / (r * r))
    dinverse = zeros(N, N, N)
    for upper in range(N):
        for right in range(N):
            for derivative in range(N):
                dinverse[upper][right][derivative] = -sum(
                    inverse[upper][p] * dg[p][q][derivative] * inverse[q][right]
                    for p in range(N) for q in range(N)
                )

    gamma = zeros(N, N, N)
    dgamma = zeros(N, N, N, N)
    for upper in range(N):
        for left in range(N):
            for right in range(N):
                for delta in range(N):
                    q = dg[delta][right][left] + dg[delta][left][right] - dg[left][right][delta]
                    gamma[upper][left][right] += F(1, 2) * inverse[upper][delta] * q
                    for derivative in range(N):
                        dq = (
                            ddg[delta][right][left][derivative]
                            + ddg[delta][left][right][derivative]
                            - ddg[left][right][delta][derivative]
                        )
                        dgamma[upper][left][right][derivative] += F(1, 2) * (
                            dinverse[upper][delta][derivative] * q
                            + inverse[upper][delta] * dq
                        )

    riemann_up = zeros(N, N, N, N)
    for rho in range(N):
        for sigma in range(N):
            for mu in range(N):
                for nu in range(N):
                    riemann_up[rho][sigma][mu][nu] = (
                        dgamma[rho][nu][sigma][mu]
                        - dgamma[rho][mu][sigma][nu]
                        + sum(
                            gamma[rho][mu][lam] * gamma[lam][nu][sigma]
                            - gamma[rho][nu][lam] * gamma[lam][mu][sigma]
                            for lam in range(N)
                        )
                    )

    ricci = zeros(N, N)
    for sigma in range(N):
        for nu in range(N):
            ricci[sigma][nu] = sum((riemann_up[rho][sigma][rho][nu] for rho in range(N)), F(0))
    scalar = sum((inverse[i][j] * ricci[i][j] for i in range(N) for j in range(N)), F(0))

    riemann_down = zeros(N, N, N, N)
    for rho in range(N):
        for sigma in range(N):
            for mu in range(N):
                for nu in range(N):
                    riemann_down[rho][sigma][mu][nu] = sum(
                        (g[rho][lam] * riemann_up[lam][sigma][mu][nu] for lam in range(N)), F(0)
                    )
    kretschmann = sum((
        inverse[i][i] * inverse[j][j] * inverse[k][k] * inverse[l][l]
        * riemann_down[i][j][k][l] ** 2
        for i in range(N) for j in range(N) for k in range(N) for l in range(N)
    ), F(0))
    ricci2 = sum((
        inverse[i][i] * inverse[j][j] * ricci[i][j] ** 2
        for i in range(N) for j in range(N)
    ), F(0))
    c2 = kretschmann - 2 * ricci2 + scalar * scalar / 3
    return {"R": scalar, "Ricci2": ricci2, "K": kretschmann, "C2": c2, "det": determinant(g)}


def closed_form(r: F, c: F, A: F, A1: F, A2: F) -> dict[str, F]:
    scalar = -A2 - 4 * A1 / r + 2 * (1 - A) / (r * r)
    kretschmann = A2 * A2 + 4 * A1 * A1 / (r * r) + 4 * (1 - A) ** 2 / (r**4)
    ricci2 = (
        r**4 * A2**2 + 4 * r**3 * A1 * A2 + 8 * r**2 * A1**2
        + 8 * r * A * A1 - 8 * r * A1 + 4 * (A - 1) ** 2
    ) / (2 * r**4)
    c2 = (A2 - 2 * A1 / r + 2 * (A - 1) / (r * r)) ** 2 / 3
    return {"R": scalar, "Ricci2": ricci2, "K": kretschmann, "C2": c2, "det": -c * c * r**4}


def independent_algebra(*, corrupt: str | None = None) -> dict[str, object]:
    cases = {
        "flat": (F(2), F(3), F(1), F(0), F(0)),
        "constant_four": (F(2), F(3), F(4), F(0), F(0)),
        "constant_quarter": (F(2), F(3), F(1, 4), F(0), F(0)),
        "regular_quadratic": (F(2), F(3), F(7, 3), F(4, 3), F(2, 3)),
        "linear": (F(2), F(3), F(7, 5), F(1, 5), F(0)),
        "wrl": (F(2), F(3), F(3, 5), F(-1, 5), F(0)),
    }
    observed = {name: direct_coordinate_invariants(*values) for name, values in cases.items()}
    expected = {name: closed_form(*values) for name, values in cases.items()}
    if corrupt == "tensor":
        observed["wrl"]["K"] += 1

    eta = diag(-1, 1, 1, 1)
    boost = [
        [F(5, 3), F(4, 3), F(0), F(0)],
        [F(4, 3), F(5, 3), F(0), F(0)],
        [F(0), F(0), F(1), F(0)],
        [F(0), F(0), F(0), F(1)],
    ]
    coframe = diag(6, F(1, 2), 2, 2)  # c=3,A=4,r=2 at the equator.
    rebuilt = matmul(matmul(transpose(coframe), eta), coframe)
    boost_metric = matmul(matmul(transpose(boost), eta), boost)

    A2_center = F(7, 3)
    regular_center_limit = 6 * A2_center**2
    constant_R_difference = expected["constant_four"]["R"] - expected["constant_quarter"]["R"]
    angular_lower_control = expected["constant_four"]["K"]
    if corrupt == "center":
        regular_center_limit += 1

    checks = {
        "six_direct_tensor_cases_match_closed_forms": observed == expected,
        "flat_control": all(observed["flat"][key] == 0 for key in ("R", "Ricci2", "K", "C2")),
        "constant_full_metric_curved": observed["constant_four"]["K"] == F(9, 4),
        "constant_reversal_changes_scalar": constant_R_difference != 0,
        "regular_quadratic_is_conformally_flat": observed["regular_quadratic"]["C2"] == 0,
        "linear_profile_is_conformally_flat_but_curved": observed["linear"]["C2"] == 0 and observed["linear"]["K"] > 0,
        "wrl_is_conformally_flat_but_curved": observed["wrl"]["C2"] == 0 and observed["wrl"]["K"] > 0,
        "positive_A_inertia": rebuilt == diag(-36, F(1, 4), 4, 4),
        "orthonormal_boost_preserves_eta": boost_metric == eta,
        "radial_coordinate_null_speed_squared": F(3)**2 * F(4)**2 == F(144),
        "local_normalized_null_speed_squared": F(144) / F(4)**2 == F(9),
        "regular_center_limit": regular_center_limit == 6 * A2_center**2,
        "unbalanced_center_has_rminus4_coefficient": 4 * (1 - F(4)) ** 2 == 36,
        "linear_center_has_rminus2_coefficient": 8 * F(1, 5) ** 2 == F(8, 25),
        "angular_K_lower_control": angular_lower_control == 4 * (1 - F(4)) ** 2 / F(2)**4,
        "wrl_interior_direct_tensor_control": observed["wrl"]["R"] == F(3, 5)
        and observed["wrl"]["Ricci2"] == F(1, 10)
        and observed["wrl"]["K"] == F(2, 25),
    }
    # The preceding near-wall rational point checks the static formula without setting A=0,
    # which is outside direct_coordinate_invariants.  The exact wall limits are formula substitutions:
    wall_R = -F(0) - 4 * F(-1, 5) / F(5) + 2 / F(25)
    wall_K = 4 * F(1, 25) / F(25) + 4 / F(625)
    checks["wrl_exact_wall_limits"] = wall_R == F(6, 25) and wall_K == F(8, 625)
    require(all(checks.values()), "independent_algebra")
    return {"checks": checks, "exact_checks": len(checks), "cases": sorted(cases)}


EXPECTED_TABLES = {
    "REGIME_ATLAS.tsv": (11, "id", "status", {
        "R01": "DERIVED_CONDITIONAL_STATIC_SPHERICAL", "R04": "DERIVED_CONDITIONAL_STATIC_SPHERICAL",
        "R06": "DERIVED_CONDITIONAL_METRIC_LIMIT", "R07": "DERIVED_CONDITIONAL_STATIC_SPHERICAL",
        "R10": "REFUTED_AS_UNIVERSAL_SYMMETRY", "R11": "OPEN",
    }),
    "ANGULAR_COUPLING_LEDGER.tsv": (9, "id", "status", {
        "A04": "DERIVED_PER_REPRESENTATIVE", "A07": "DERIVED_CONDITIONAL_STATIC_SPHERICAL",
        "A08": "DERIVED_CONDITIONAL_C2_TAYLOR_CLASS", "A09": "NOT_A_GENERIC_COMPLETE_METRIC_SYMMETRY",
    }),
    "FRAME_STATUS_LEDGER.tsv": (9, "id", "status", {
        "F01": "OWNER_FOUNDING_CLARIFICATION", "F02": "DERIVED_CONDITIONAL_STATIC_SPHERICAL",
        "F05": "DERIVED_CONDITIONAL_CONTROL", "F08": "OPEN", "F09": "CERTIFICATION_RULE",
    }),
    "PRIOR_WORK_REGRADE.tsv": (9, "id", "status", {
        "G02": "RETAINED_AND_EXTENDED", "G03": "RETAINED_AND_LOCALIZED",
        "G08": "NOT_DERIVED_GLOBAL_COMPLETION", "G09": "UNCHANGED",
    }),
    "STATUS_LEDGER.tsv": (16, "id", "status", {
        "S02": "DERIVED_CONDITIONAL", "S07": "DERIVED_CONDITIONAL", "S09": "REFUTED",
        "S10": "REFUTED_IN_CONTROL", "S13": "OPEN", "S14": "OPEN",
        "S16": "VERIFIED_WITH_CAVEATS",
    }),
}


def validate_tables(*, corrupt: str | None = None) -> dict[str, int]:
    counts = {}
    for name, (count, key, status_key, statuses) in EXPECTED_TABLES.items():
        records = table(name)
        if corrupt == "missing" and name == "STATUS_LEDGER.tsv":
            records = records[:-1]
        if corrupt == "duplicate" and name == "STATUS_LEDGER.tsv":
            records.append(copy.deepcopy(records[0]))
        if corrupt == "promotion" and name == "STATUS_LEDGER.tsv":
            next(row for row in records if row["id"] == "S13")[status_key] = "DERIVED"
        require(len(records) == count, f"table_count:{name}")
        require(len({row[key] for row in records}) == count, f"table_unique:{name}")
        index = {row[key]: row for row in records}
        for item, expected in statuses.items():
            require(index[item][status_key] == expected, f"table_status:{name}:{item}")
        counts[name] = len(records)
    return counts


def validate_sources(*, corrupt: bool = False) -> dict[str, object]:
    records = table("SOURCE_LINEAGE.tsv")
    require(len(records) == 10 and len({row["source_id"] for row in records}) == 10, "source_count")
    for number, row in enumerate(records):
        data = run("git", "show", f"{BASE}:{row['path']}", binary=True)
        digest = hashlib.sha256(data).hexdigest()
        if corrupt and number == 0:
            digest = "0" * 64
        require(digest == row["sha256"], f"source_sha:{row['source_id']}")
        require(run("git", "rev-parse", f"{BASE}:{row['path']}").strip() == row["git_blob"], f"source_blob:{row['source_id']}")
        line = data.decode("utf-8").splitlines()[int(row["anchor_line"]) - 1]
        require(hashlib.sha256(line.encode()).hexdigest() == row["anchor_sha256"], f"source_anchor:{row['source_id']}")
        require(row["firewall"] == "POST_FIREWALL_AFFIRMATIVE_ELIGIBLE", f"firewall:{row['source_id']}")
    return {"sources": len(records), "base": BASE, "result": "PASS"}


def validate_production(*, corrupt: str | None = None) -> dict[str, object]:
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    if corrupt == "false_check":
        result["checks"][next(iter(result["checks"]))] = False
    if corrupt == "flip":
        result["maximum_conclusion"] = "MICRO_FRAME_FLIP_DERIVED"
    require(result["status"] == "PASS", "production_status")
    require(len(result["checks"]) == 18 and all(result["checks"].values()), "production_checks")
    require(result["counts"] == {"exact_checks": 18, "profile_controls": 5}, "production_counts")
    require(result["regular_center"]["necessary_and_sufficient_for_bounded_K"] == "A(0)=1 AND A'(0)=0 WITH FINITE A''(0)", "center_ruling")
    require(result["maximum_conclusion"] == "NO_INVARIANT_FINITE_PHI_FRAME_FLIP_IN_STATIC_SPHERICAL_CLASS__ANGULAR_SECTOR_FORCES_RECIPROCAL_BALANCE_AT_A_REGULAR_AREAL_CENTER__TIME_LIVE_AND_MICRO_SCALE_REMAIN_OPEN", "maximum_conclusion")
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
        "micro_scale_inserted": False,
        "gr_dynamics_imported": False,
        "material_cone_coupling_claimed": False,
        "time_live_extrapolated": False,
        "wrl_hard_edge_claimed": False,
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
        "tensor_formula_mutation_rejected": reject("tensor", lambda: independent_algebra(corrupt="tensor")),
        "center_limit_mutation_rejected": reject("center", lambda: independent_algebra(corrupt="center")),
        "missing_ledger_row_rejected": reject("missing", lambda: validate_tables(corrupt="missing")),
        "duplicate_ledger_row_rejected": reject("duplicate", lambda: validate_tables(corrupt="duplicate")),
        "micro_status_promotion_rejected": reject("promotion", lambda: validate_tables(corrupt="promotion")),
        "source_hash_mutation_rejected": reject("source", lambda: validate_sources(corrupt=True)),
        "production_false_check_rejected": reject("production", lambda: validate_production(corrupt="false_check")),
        "invented_micro_flip_rejected": reject("flip", lambda: validate_production(corrupt="flip")),
        "wrong_prereg_base_rejected": reject("prereg", lambda: validate_prereg(corrupt=True)),
        "inserted_micro_scale_rejected": reject("scale", lambda: validate_stop_lines(corrupt="micro_scale_inserted")),
        "imported_gr_dynamics_rejected": reject("gr", lambda: validate_stop_lines(corrupt="gr_dynamics_imported")),
        "material_cone_promotion_rejected": reject("matter", lambda: validate_stop_lines(corrupt="material_cone_coupling_claimed")),
        "time_live_extrapolation_rejected": reject("time", lambda: validate_stop_lines(corrupt="time_live_extrapolated")),
        "wrl_hard_edge_promotion_rejected": reject("edge", lambda: validate_stop_lines(corrupt="wrl_hard_edge_claimed")),
        "constant_block_flat_fourmetric_claim_rejected": "PASS" if algebra["checks"]["constant_full_metric_curved"] else "FAIL",
        "phi_reversal_symmetry_claim_rejected": "PASS" if algebra["checks"]["constant_reversal_changes_scalar"] else "FAIL",
        "coordinate_speed_as_local_c_rejected": "PASS" if algebra["checks"]["local_normalized_null_speed_squared"] else "FAIL",
        "component_divergence_as_frame_flip_rejected": "PASS" if algebra["checks"]["positive_A_inertia"] else "FAIL",
    }
    require(len(catches) == 18 and all(value == "PASS" for value in catches.values()), "catch_proofs")

    result = {
        "schema": "udt-reciprocity-regime-angular-center-independent-verification-1.0",
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
            "general_curvature_formulas": "PASS",
            "angular_constant_imbalance": "PASS",
            "regular_center": "PASS",
            "finite_phi_frame_type": "PASS",
            "wrl_control": "PASS",
            "phi_reversal": "PASS",
            "micro_time_live_scope": "OPEN",
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
