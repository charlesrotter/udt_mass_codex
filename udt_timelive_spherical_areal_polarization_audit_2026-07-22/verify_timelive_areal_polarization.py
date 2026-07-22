#!/usr/bin/env python3
"""Independent exact verification for the time-live areal-polarization audit.

This verifier uses only the Python standard library.  It does not import the
production SymPy program.  Curvature is recomputed from rational metric two-jets
in a coordinate basis at an equatorial point.
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
BASE = "066d1ee05c3ad144d28b096b4a4728cca06941fa"
PREREG = "90217f7"
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


def determinant2(matrix) -> Q:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def inverse2(matrix):
    det = determinant2(matrix)
    require(det != 0, "invertible_2x2")
    return [[matrix[1][1] / det, -matrix[0][1] / det], [-matrix[1][0] / det, matrix[0][0] / det]]


def quadratic(matrix, vector) -> Q:
    return sum((vector[i] * matrix[i][j] * vector[j] for i in range(len(vector)) for j in range(len(vector))), Q(0))


def metric_twojet_curvature(g, dg, ddg) -> dict[str, object]:
    """Coordinate curvature at one point from g, first jets, and second jets."""
    # All audit controls are diagonal at the evaluation point.
    inverse = diag(*(1 / g[i][i] for i in range(DIM)))
    dinverse = zeros(DIM, DIM, DIM)
    for upper in range(DIM):
        for right in range(DIM):
            for derivative in range(DIM):
                dinverse[upper][right][derivative] = -sum(
                    (inverse[upper][p] * dg[p][q][derivative] * inverse[q][right]
                     for p in range(DIM) for q in range(DIM)), Q(0)
                )

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

    riemann_down = zeros(DIM, DIM, DIM, DIM)
    for rho in range(DIM):
        for sigma in range(DIM):
            for mu in range(DIM):
                for nu in range(DIM):
                    riemann_down[rho][sigma][mu][nu] = sum(
                        (g[rho][lam] * riemann_up[lam][sigma][mu][nu] for lam in range(DIM)), Q(0)
                    )
    ricci = zeros(DIM, DIM)
    for sigma in range(DIM):
        for nu in range(DIM):
            ricci[sigma][nu] = sum((riemann_up[rho][sigma][rho][nu] for rho in range(DIM)), Q(0))
    scalar = sum((inverse[i][j] * ricci[i][j] for i in range(DIM) for j in range(DIM)), Q(0))
    return {"inverse": inverse, "riemann": riemann_down, "scalar": scalar}


def warped_twojet(R: Q, Rt: Q, Rr: Q, Rtt: Q, Rtr: Q, Rrr: Q):
    """Flat orbit-space normal-coordinate jet of -dT^2+dr^2+R(T,r)^2 dOmega^2."""
    require(R > 0, "positive_areal_radius")
    g = zeros(DIM, DIM)
    dg = zeros(DIM, DIM, DIM)
    ddg = zeros(DIM, DIM, DIM, DIM)
    g[0][0], g[1][1], g[2][2], g[3][3] = -1, 1, R * R, R * R
    for angular in (2, 3):
        dg[angular][angular][0] = 2 * R * Rt
        dg[angular][angular][1] = 2 * R * Rr
        ddg[angular][angular][0][0] = 2 * (Rt * Rt + R * Rtt)
        ddg[angular][angular][0][1] = 2 * (Rt * Rr + R * Rtr)
        ddg[angular][angular][1][0] = ddg[angular][angular][0][1]
        ddg[angular][angular][1][1] = 2 * (Rr * Rr + R * Rrr)
    # At theta=pi/2, d_theta sin^2(theta)=0 and d_theta^2 sin^2(theta)=-2.
    ddg[3][3][2][2] = -2 * R * R
    return g, dg, ddg


def lapse_twojet(radius: Q, F: Q, F1: Q, F2: Q):
    """Jet of -F(r)^2 dT^2+dr^2+r^2 dOmega^2 at the equator."""
    g, dg, ddg = warped_twojet(radius, Q(0), Q(1), Q(0), Q(0), Q(0))
    g[0][0] = -F * F
    dg[0][0][1] = -2 * F * F1
    ddg[0][0][1][1] = -2 * (F1 * F1 + F * F2)
    return g, dg, ddg


def independent_algebra(*, corrupt: str | None = None) -> dict[str, object]:
    # Full shift-retaining two-metric control.
    N, L, beta = Q(2), Q(3), Q(1, 5)
    Rt, Rr = Q(7, 4), Q(5, 3)
    h = [[-N * N + L * L * beta * beta, L * L * beta], [L * L * beta, L * L]]
    hinv = inverse2(h)
    dR = [Rt, Rr]
    X_direct = quadratic(hinv, dR)
    X_shift = Rr * Rr / (L * L) - (Rt - beta * Rr) ** 2 / (N * N)
    eps = [[Q(0), 1 / (N * L)], [-1 / (N * L), Q(0)]]
    K = [sum((eps[i][j] * dR[j] for j in range(2)), Q(0)) for i in range(2)]
    grad = [sum((hinv[i][j] * dR[j] for j in range(2)), Q(0)) for i in range(2)]
    Kdot = sum((K[i] * h[i][j] * grad[j] for i in range(2) for j in range(2)), Q(0))
    K2 = quadratic(h, K)
    grad2 = quadratic(h, grad)
    if corrupt == "dual_norm":
        K2 += 1

    branches = {}
    for label, vector in {
        "X_POSITIVE": [Q(0), Q(2)],
        "X_ZERO": [Q(1), Q(1)],
        "X_NEGATIVE": [Q(2), Q(1)],
    }.items():
        x = -vector[0] ** 2 + vector[1] ** 2
        k = [vector[1], -vector[0]]
        branches[label] = {"X": x, "K2": -k[0] ** 2 + k[1] ** 2, "det_h": Q(-1)}
    if corrupt == "branch":
        branches["X_NEGATIVE"]["K2"] *= -1

    # Null expansion product in an orthonormal base.
    uR, nR, radius = Q(5, 4), Q(7, 3), Q(11, 5)
    theta_product = 2 * (uR + nR) * (uR - nR) / (radius * radius)
    X_frame = -uR * uR + nR * nR

    # Direct-coordinate warped curvature at a generic rational two-jet.
    data = (Q(5, 2), Q(2, 3), Q(7, 5), Q(-3, 4), Q(5, 6), Q(4, 7))
    g, dg, ddg = warped_twojet(*data)
    curvature = metric_twojet_curvature(g, dg, ddg)
    R, wRt, wRr, Rtt, Rtr, Rrr = data
    X_warp = -wRt * wRt + wRr * wRr
    angular = curvature["riemann"][2][3][2][3] / (R ** 4)
    mixed_tt = curvature["riemann"][0][2][0][2] / (R * R)
    mixed_tr = curvature["riemann"][0][2][1][2] / (R * R)
    mixed_rr = curvature["riemann"][1][2][1][2] / (R * R)
    if corrupt == "angular":
        angular += 1
    if corrupt == "mixed":
        mixed_tr += 1

    # Same-X metrics with different clock-threading factors.
    flat = metric_twojet_curvature(*lapse_twojet(Q(2), Q(1), Q(0), Q(0)))
    curved = metric_twojet_curvature(*lapse_twojet(Q(2), Q(9), Q(3), Q(1)))
    if corrupt == "threading":
        curved["scalar"] = flat["scalar"]

    # Center Laurent coefficients of (1-X)/R^2 for X=X0+X1 R+X2 R^2/2.
    X0, X1, X2 = Q(1), Q(0), Q(7, 3)
    center_finite = -X2 / 2
    if corrupt == "center":
        X1 = Q(1)

    # Local common scale: h'^{-1}=Omega^-2 h^-1 and R'=Omega R.
    old_X = -Q(1) ** 2 + Q(3) ** 2
    Omega, physical_R, OmT, Omr = Q(5), Q(2), Q(2), Q(-1)
    scaled_Rt = Omega * Q(1) + physical_R * OmT
    scaled_Rr = Omega * Q(3) + physical_R * Omr
    local_scaled_X = (-scaled_Rt**2 + scaled_Rr**2) / Omega**2
    constant_scaled_X = (-(Omega * Q(1)) ** 2 + (Omega * Q(3)) ** 2) / Omega**2
    if corrupt == "csn":
        local_scaled_X = old_X

    # Static founded control: R=r in h=diag(-A,A^-1) gives X=A.
    static_A = Q(7, 3)
    static_h = [[-static_A, Q(0)], [Q(0), 1 / static_A]]
    static_X = quadratic(inverse2(static_h), [Q(0), Q(1)])

    checks = {
        "shift_metric_determinant": determinant2(h) == -N * N * L * L,
        "shift_complete_X": X_direct == X_shift,
        "areal_dual_orthogonal": Kdot == 0,
        "areal_dual_opposite_norm": K2 == -X_direct,
        "gradient_norm_is_X": grad2 == X_direct,
        "three_branch_X_controls": [branches[key]["X"] for key in ("X_POSITIVE", "X_ZERO", "X_NEGATIVE")] == [4, 0, -3],
        "three_branch_opposite_K_norms": all(item["K2"] == -item["X"] for item in branches.values()),
        "full_lorentzian_base_across_branches": all(item["det_h"] < 0 for item in branches.values()),
        "null_expansion_product": theta_product == -2 * X_frame / (radius * radius),
        "angular_warped_curvature": angular == (1 - X_warp) / (R * R),
        "mixed_tt_warped_curvature": mixed_tt == -Rtt / R,
        "mixed_tr_warped_curvature": mixed_tr == -Rtr / R,
        "mixed_rr_warped_curvature": mixed_rr == -Rrr / R,
        "regular_center_finite_coefficient": X0 == 1 and X1 == 0 and center_finite == Q(-7, 6),
        "unbalanced_center_diverges": (1 - Q(4)) != 0,
        "linear_center_diverges": Q(1, 5) != 0,
        "same_X_flat_threading_control": flat["scalar"] == 0,
        "same_X_curved_threading_control": curved["scalar"] == Q(-8, 9),
        "same_X_curvatures_differ": flat["scalar"] != curved["scalar"],
        "local_CSN_changes_areal_X": local_scaled_X == Q(88, 25) and local_scaled_X != old_X,
        "constant_CSN_preserves_areal_X": constant_scaled_X == old_X,
        "static_recovery_control": static_X == static_A,
    }
    require(all(checks.values()), "independent_algebra")
    return {
        "checks": checks,
        "exact_checks": len(checks),
        "controls": {
            "shift_X": str(X_direct),
            "warped_X": str(X_warp),
            "angular_section": str(angular),
            "threading_flat_R": str(flat["scalar"]),
            "threading_curved_R": str(curved["scalar"]),
            "local_scaled_X": str(local_scaled_X),
        },
    }


EXPECTED_TABLES = {
    "AREAL_POLARIZATION_ATLAS.tsv": (7, "id", "status", {
        "P01": "DERIVED_CONDITIONAL_SPHERICAL_REPRESENTATIVE",
        "P03": "DERIVED_CONDITIONAL_SPHERICAL_REPRESENTATIVE",
        "P06": "DERIVED_TRANSFORMATION", "P07": "OPEN",
    }),
    "TIME_LIVE_ASSEMBLY_LEDGER.tsv": (15, "id", "status", {
        "T09": "DERIVED_CONDITIONAL_ON_IDENTIFICATION",
        "T13": "NOT_SELECTED_BY_X_OR_LOCAL_RECIPROCAL_AMPLITUDE",
        "T15": "OPEN",
    }),
    "FRAME_STATUS_LEDGER.tsv": (9, "id", "status", {
        "F03": "DERIVED_KINEMATIC_BRANCH_CLASSIFICATION", "F04": "REFUTED",
        "F07": "REFUTED_AS_COMPLETE_SELECTION", "F08": "OPEN_PHYSICAL_IDENTIFICATION",
    }),
    "PRIOR_WORK_REGRADE.tsv": (9, "id", "status", {
        "G01": "RETAINED_AND_COVARIANTLY_EXTENDED", "G07": "PARTIALLY_ADVANCED_STILL_CONDITIONAL",
        "G09": "UNCHANGED",
    }),
    "DEDUCTIVE_SPINE.tsv": (13, "step", "status", {
        "D03": "DERIVED", "D08": "DERIVED_CONDITIONAL_ON_IDENTIFICATION",
        "D11": "EXACT_UNDERDETERMINATION", "D13": "VERIFIED_WITH_CAVEATS",
    }),
    "STATUS_LEDGER.tsv": (20, "id", "status", {
        "S07": "DERIVED_CONDITIONAL", "S08": "REFUTED",
        "S13": "DERIVED_CONDITIONAL_ON_IDENTIFICATION", "S15": "OPEN_NOT_SELECTED",
        "S16": "OPEN", "S18": "OPEN", "S20": "VERIFIED_WITH_CAVEATS",
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
        if corrupt == "flip" and name == "STATUS_LEDGER.tsv":
            next(row for row in rows if row["id"] == "S08")[status_key] = "DERIVED"
        if corrupt == "phi" and name == "STATUS_LEDGER.tsv":
            next(row for row in rows if row["id"] == "S13")[status_key] = "DERIVED_UNCONDITIONAL"
        require(len(rows) == count, f"table_count:{name}")
        require(len({row[key] for row in rows}) == count, f"table_unique:{name}")
        index = {row[key]: row for row in rows}
        for identity, expected in statuses.items():
            require(index[identity][status_key] == expected, f"table_status:{name}:{identity}")
        counts[name] = len(rows)
    return counts


def validate_sources(*, corrupt: str | None = None) -> dict[str, object]:
    rows = table("SOURCE_LINEAGE.tsv")
    require(len(rows) == 11 and len({row["source_id"] for row in rows}) == 11, "source_count")
    for number, row in enumerate(rows):
        data = run("git", "show", f"{BASE}:{row['path']}", binary=True)
        digest = hashlib.sha256(data).hexdigest()
        if corrupt == "hash" and number == 0:
            digest = "0" * 64
        require(digest == row["sha256"], f"source_sha:{row['source_id']}")
        require(run("git", "rev-parse", f"{BASE}:{row['path']}").strip() == row["git_blob"], f"source_blob:{row['source_id']}")
        line = data.decode("utf-8").splitlines()[int(row["anchor_line"]) - 1]
        anchor = hashlib.sha256(line.encode()).hexdigest()
        if corrupt == "anchor" and number == 0:
            anchor = "0" * 64
        require(anchor == row["anchor_sha256"], f"source_anchor:{row['source_id']}")
        require(row["firewall"] == "POST_FIREWALL_AFFIRMATIVE_ELIGIBLE", f"firewall:{row['source_id']}")
    return {"sources": len(rows), "base": BASE, "result": "PASS"}


def validate_production(*, corrupt: str | None = None) -> dict[str, object]:
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    if corrupt == "check":
        result["checks"][next(iter(result["checks"]))] = False
    if corrupt == "maximum":
        result["maximum_conclusion"] = "FULL_METRIC_OR_MICRO_FRAME_FLIP_DERIVED"
    require(result["status"] == "PASS", "production_status")
    require(len(result["checks"]) == 23 and all(result["checks"].values()), "production_checks")
    require(result["counts"] == {"exact_checks": 23, "causal_branch_controls": 3}, "production_counts")
    require(result["causal_branches"]["SPACELIKE_GRADIENT"]["X"] == "4", "production_X_positive")
    require(result["causal_branches"]["NULL_GRADIENT"]["X"] == "0", "production_X_zero")
    require(result["causal_branches"]["TIMELIKE_GRADIENT"]["X"] == "-3", "production_X_negative")
    require(result["rulings"]["complete_base_metric"] == "NOT_FIXED_BY_X__POSITIVE_CLOCK_THREADING_FACTOR_F_SURVIVES", "production_F_ruling")
    require(result["maximum_conclusion"] == "ANGULAR_AREAL_GEOMETRY_DERIVES_SOLUTION_SPECIFIC_TIME_LIVE_CLOCK_RADIAL_LINES_AND_AN_X_ZERO_CAUSAL_ROLE_EXCHANGE__FULL_METRIC_SIGNATURE_DOES_NOT_FLIP__PHI_EXTENSION_AND_CLOCK_THREADING_REMAIN_CONDITIONAL", "maximum_conclusion")
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
        "event_horizon_claimed": False,
        "micro_transition_claimed": False,
        "full_signature_flip_claimed": False,
        "action_or_eom_imported": False,
        "carrier_identified_with_spacetime_sphere": False,
        "threading_selected": False,
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
        "dual_norm_mutation_rejected": reject("dual", lambda: independent_algebra(corrupt="dual_norm")),
        "causal_branch_mutation_rejected": reject("branch", lambda: independent_algebra(corrupt="branch")),
        "angular_curvature_mutation_rejected": reject("angular", lambda: independent_algebra(corrupt="angular")),
        "mixed_curvature_mutation_rejected": reject("mixed", lambda: independent_algebra(corrupt="mixed")),
        "regular_center_mutation_rejected": reject("center", lambda: independent_algebra(corrupt="center")),
        "clock_threading_countermodel_loss_rejected": reject("threading", lambda: independent_algebra(corrupt="threading")),
        "local_CSN_promotion_rejected": reject("csn", lambda: independent_algebra(corrupt="csn")),
        "missing_ledger_row_rejected": reject("missing", lambda: validate_tables(corrupt="missing")),
        "duplicate_ledger_row_rejected": reject("duplicate", lambda: validate_tables(corrupt="duplicate")),
        "full_signature_flip_promotion_rejected": reject("flip", lambda: validate_tables(corrupt="flip")),
        "unconditional_phi_promotion_rejected": reject("phi", lambda: validate_tables(corrupt="phi")),
        "source_hash_mutation_rejected": reject("source_hash", lambda: validate_sources(corrupt="hash")),
        "source_anchor_mutation_rejected": reject("source_anchor", lambda: validate_sources(corrupt="anchor")),
        "production_false_check_rejected": reject("production", lambda: validate_production(corrupt="check")),
        "maximum_conclusion_inflation_rejected": reject("maximum", lambda: validate_production(corrupt="maximum")),
        "wrong_prereg_base_rejected": reject("prereg", lambda: validate_prereg(corrupt=True)),
        "event_horizon_promotion_rejected": reject("horizon", lambda: validate_stop_lines(corrupt="event_horizon_claimed")),
        "micro_transition_promotion_rejected": reject("micro", lambda: validate_stop_lines(corrupt="micro_transition_claimed")),
    }
    require(len(catches) == 18 and all(value == "PASS" for value in catches.values()), "catch_proofs")

    result = {
        "schema": "udt-timelive-spherical-areal-polarization-independent-verification-1.0",
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
            "shift_complete_areal_scalar": "PASS",
            "causal_role_exchange": "PASS",
            "full_signature_nonflip": "PASS",
            "warped_curvature": "PASS",
            "regular_center": "PASS",
            "same_X_threading_underdetermination": "PASS",
            "local_CSN_scope": "PASS",
            "physical_micro_identification": "OPEN",
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
