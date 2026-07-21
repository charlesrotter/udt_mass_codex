#!/usr/bin/env python3
"""Independent standard-library verifier for the UDT time-extendability audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def zeros(n, m):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def eye(n):
    output = zeros(n, n)
    for i in range(n):
        output[i][i] = F(1)
    return output


def transpose(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scale(c, a):
    return [[c * value for value in row] for row in a]


def mul(a, b):
    return [
        [sum((a[i][p] * b[p][j] for p in range(len(b))), F(0)) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def flat(a):
    return [value for row in a for value in row]


def matrix_equal(a, b):
    return a == b


def block_diag(a, b):
    output = zeros(len(a) + len(b), len(a[0]) + len(b[0]))
    for i in range(len(a)):
        for j in range(len(a[0])):
            output[i][j] = a[i][j]
    for i in range(len(b)):
        for j in range(len(b[0])):
            output[len(a) + i][len(a[0]) + j] = b[i][j]
    return output


def full_metric(h, c, q):
    output = zeros(4, 4)
    for i in range(2):
        for j in range(2):
            output[i][j] = h[i][j]
            output[i][j + 2] = c[i][j]
            output[j + 2][i] = c[i][j]
            output[i + 2][j + 2] = q[i][j]
    return output


def inverse(a):
    n = len(a)
    augmented = [a[i][:] + eye(n)[i] for i in range(n)]
    pivot_row = 0
    for column in range(n):
        pivot = next((r for r in range(pivot_row, n) if augmented[r][column]), None)
        if pivot is None:
            raise AssertionError("singular")
        augmented[pivot_row], augmented[pivot] = augmented[pivot], augmented[pivot_row]
        divisor = augmented[pivot_row][column]
        augmented[pivot_row] = [value / divisor for value in augmented[pivot_row]]
        for r in range(n):
            if r != pivot_row and augmented[r][column]:
                factor = augmented[r][column]
                augmented[r] = [
                    augmented[r][j] - factor * augmented[pivot_row][j] for j in range(2 * n)
                ]
        pivot_row += 1
    return [row[n:] for row in augmented]


def determinant(a):
    work = [row[:] for row in a]
    n = len(a)
    value = F(1)
    sign = 1
    for column in range(n):
        pivot = next((r for r in range(column, n) if work[r][column]), None)
        if pivot is None:
            return F(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        pivot_value = work[column][column]
        value *= pivot_value
        for r in range(column + 1, n):
            factor = work[r][column] / pivot_value
            for j in range(column, n):
                work[r][j] -= factor * work[column][j]
    return sign * value


def rank(a):
    if not a:
        return 0
    work = [row[:] for row in a]
    nrows, ncols = len(work), len(work[0])
    pivot_row = 0
    for column in range(ncols):
        pivot = next((r for r in range(pivot_row, nrows) if work[r][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        divisor = work[pivot_row][column]
        work[pivot_row] = [value / divisor for value in work[pivot_row]]
        for r in range(nrows):
            if r != pivot_row and work[r][column]:
                factor = work[r][column]
                work[r] = [work[r][j] - factor * work[pivot_row][j] for j in range(ncols)]
        pivot_row += 1
        if pivot_row == nrows:
            break
    return pivot_row


def trace(a):
    return sum((a[i][i] for i in range(len(a))), F(0))


def basis(index):
    output = zeros(4, 4)
    output[index // 4][index % 4] = F(1)
    return output


def connection_system(g, gdot, r=None, l=None):
    coefficient_columns = []
    for index in range(16):
        e = basis(index)
        pieces = [sub(add(mul(transpose(e), g), mul(g, e)), zeros(4, 4))]
        if r is not None:
            pieces.append(sub(mul(e, r), mul(r, e)))
        if l is not None:
            pieces.append(sub(mul(e, l), mul(l, e)))
        coefficient_columns.append([value for piece in pieces for value in flat(piece)])
    coefficient_rows = [list(row) for row in zip(*coefficient_columns)]
    rhs = flat(gdot)
    if r is not None:
        rhs += [F(0)] * 16
    if l is not None:
        rhs += [F(0)] * 16
    return rank(coefficient_rows), rank([row + [rhs[i]] for i, row in enumerate(coefficient_rows)])


def pair_invariant(g, l):
    return trace(mul(mul(mul(inverse(g), transpose(l)), g), l))


def matrices(k, lift):
    e = F(1, 10)
    swap = [[F(0), F(1)], [F(1), F(0)]]
    angular, cross = {
        "PLUS_IDENTITY": (eye(2), [[e, e], [e, e]]),
        "MINUS_IDENTITY": (scale(F(-1), eye(2)), [[e, e], [-e, -e]]),
        "AXIS_REFLECTION": ([[F(1), F(0)], [F(0), F(-1)]], [[e, e], [e, -e]]),
        "HOPF_EXCHANGE_LOCAL": (swap, [[e, e], [e, e]]),
    }[lift]
    h = [[F(1), -k], [-k, F(1)]]
    g = full_metric(h, cross, eye(2))
    r = block_diag(swap, angular)
    l = block_diag([[F(-1), F(0)], [F(0), F(1)]], zeros(2, 2))
    gdot = zeros(4, 4)
    gdot[0][1] = gdot[1][0] = F(-1, 10)
    return g, r, l, gdot


def validate_model(model, tables, source_override=None):
    if model["schema"] != "udt-kinematic-time-extendability-derivation-1.0":
        raise AssertionError("schema")
    if model["maximum_conclusion"] != "UDT_KINEMATIC_TIME_EXTENDABILITY_STATUS_CHARACTERIZED":
        raise AssertionError("maximum")
    if model["check_count"] != 177 or len(model["checks"]) != 177:
        raise AssertionError("check count")
    if set(model["checks"].values()) != {"PASS"}:
        raise AssertionError("derivation checks")
    required_outcomes = {
        "POINTWISE_TIME_PRESERVATION_ALLOWS_INEQUIVALENT_MU_HISTORIES",
        "ALL_REGISTERED_FROZEN_LIFTS_HAVE_KINEMATIC_TIME_EXTENSIONS",
        "METRIC_SEAL_COMPATIBILITY_ALLOWS_DOT_MU",
        "FULL_RECIPROCAL_PARALLELISM_ONLY_CONSERVES_MU",
        "FULL_RECIPROCAL_PARALLELISM_DOES_NOT_SELECT_MU_VALUE",
        "PHYSICAL_TRANSPORT_LAW_REMAINS_OPEN",
        "KINEMATIC_TIME_EXTENDABILITY_REMAINS_UNDERDETERMINED",
    }
    if not required_outcomes.issubset(model["outcomes"]):
        raise AssertionError("outcomes")
    expected_lifts = {"PLUS_IDENTITY", "MINUS_IDENTITY", "AXIS_REFLECTION", "HOPF_EXCHANGE_LOCAL"}
    if set(model["lift_results"]) != expected_lifts:
        raise AssertionError("model lifts")
    if len(model["histories"]) != 8:
        raise AssertionError("model histories")
    for lift, result in model["lift_results"].items():
        if result["status"] != "KINEMATICALLY_TIME_EXTENDABLE_MU_VALUE_OPEN":
            raise AssertionError("lift status")
        if not result["metric_seal_allows_dot_mu"] or result["full_reciprocal_parallelism_allows_dot_mu"]:
            raise AssertionError("transport effects")

    lifts, histories, hierarchy, status, completeness, sources = tables
    if len(lifts) != 4 or {row["lift"] for row in lifts} != expected_lifts:
        raise AssertionError("lift table")
    if len({row["lift"] for row in lifts}) != 4:
        raise AssertionError("duplicate lift")
    if len(histories) != 8 or len({row["history_id"] for row in histories}) != 8:
        raise AssertionError("history table")
    expected_histories = {
        f"{lift}_{history}" for lift in expected_lifts for history in ("LOWER_HISTORY", "UPPER_HISTORY")
    }
    if {row["history_id"] for row in histories} != expected_histories:
        raise AssertionError("history identities")
    if any(row["fixed_volume_status"] != "EXACT_POSITIVE_CSN_NORMALIZATION_AVAILABLE" for row in histories):
        raise AssertionError("volume promoted")
    if len(hierarchy) != 7 or {row["level"] for row in hierarchy} != {f"C0{i}" for i in range(1, 8)}:
        raise AssertionError("hierarchy")
    c04 = next(row for row in hierarchy if row["level"] == "C04")
    if c04["mu_effect"] != "DOT_MU_ZERO_ONLY" or c04["current_authority"] != "NOT_CURRENTLY_SELECTED_BY_UDT":
        raise AssertionError("full parallelism promoted")
    c06 = next(row for row in hierarchy if row["level"] == "C06")
    if c06["current_authority"] != "EXACT_BASIS_COVARIANCE_ONLY":
        raise AssertionError("moving frame promoted")
    if len(status) != 16 or {row["claim_id"] for row in status} != {f"T{i:02d}" for i in range(1, 17)}:
        raise AssertionError("status")
    by_claim = {row["claim_id"]: row for row in status}
    if by_claim["T06"]["status"] != "DERIVED_CONDITIONAL":
        raise AssertionError("conservation premise")
    if by_claim["T07"]["status"] != "NOT_DERIVED":
        raise AssertionError("value selection promoted")
    if by_claim["T12"]["status"] != "REFUTED_BOUNDED":
        raise AssertionError("frozen invalidated")
    if by_claim["T13"]["status"] != "NOT_DERIVED":
        raise AssertionError("dynamic theorem promoted")
    if by_claim["T14"]["status"] != "OPEN":
        raise AssertionError("transport selected")
    if len(completeness) != 10:
        raise AssertionError("completeness")
    dynamic = next(row for row in completeness if row["criterion"] == "dynamical_character")
    if dynamic["coverage"] != "KINEMATIC_PATHS_ONLY":
        raise AssertionError("dynamic completeness promoted")
    if len(sources) != 17 or len({row["id"] for row in sources}) != 17:
        raise AssertionError("sources")
    source_paths = {row["path"] for row in sources}
    required_sources = {
        "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
        "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md",
        "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
        "metric_cartan_holonomy_audit_2026-07-19/AUDIT_REPORT.md",
        "projective_transport_section_selector_2026-07-19/AUDIT_REPORT.md",
        "udt_premise_reset_audit_2026-07-19/AUDIT_REPORT.md",
    }
    if not required_sources.issubset(source_paths):
        raise AssertionError("source lineage")
    xmax = next(row for row in sources if row["path"] == "xmax_dynamic_observer_frame_2026-07-19/AUDIT_REPORT.md")
    if xmax["source_status"] != "CONDITIONAL_MATHEMATICS_PHYSICAL_READING_WITHDRAWN_BY_PREMISE_RESET":
        raise AssertionError("xmax authority")

    texts = {}
    for path in required_sources:
        texts[path] = (
            source_override[path]
            if source_override and path in source_override
            else (ROOT / path).read_text(encoding="utf-8")
        )
    if "derivative order and time-live degrees of freedom" not in texts["UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md"]:
        raise AssertionError("CSN semantics")
    if "No nonlocal insertion" not in texts["UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md"]:
        raise AssertionError("bootstrap semantics")
    if "connection/transport law" not in texts["UDT_SCIENTIFIC_FRONTIER_2026-07-19.md"]:
        raise AssertionError("frontier semantics")
    if "does not choose which complete metric" not in texts["metric_cartan_holonomy_audit_2026-07-19/AUDIT_REPORT.md"]:
        raise AssertionError("Cartan semantics")
    if "propagation" not in texts["projective_transport_section_selector_2026-07-19/AUDIT_REPORT.md"] or "selection" not in texts["projective_transport_section_selector_2026-07-19/AUDIT_REPORT.md"]:
        raise AssertionError("transport semantics")
    if "conditional mathematics only" not in texts["udt_premise_reset_audit_2026-07-19/AUDIT_REPORT.md"]:
        raise AssertionError("reset semantics")

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    if "conserves whichever value was initially supplied; it does not select the value" not in report:
        raise AssertionError("conservation wording")
    if "not a complete dynamical result" not in report and "not complete dynamical results" not in report:
        raise AssertionError("dynamic scope wording")
    if "No action, field equation" not in report:
        raise AssertionError("authority boundary wording")


def independent_reconstruction():
    checks = {}
    lift_rows = rows(HERE / "LIFT_TIME_EXTENDABILITY.tsv")
    expected_dimensions = {
        "PLUS_IDENTITY": 3,
        "MINUS_IDENTITY": 3,
        "AXIS_REFLECTION": 2,
        "HOPF_EXCHANGE_LOCAL": 2,
    }
    swap2 = [[F(0), F(1)], [F(1), F(0)]]
    for lift in expected_dimensions:
        endpoint_invariants = []
        for history, k0 in (("LOWER_HISTORY", F(2)), ("UPPER_HISTORY", F(3))):
            invariant_path = []
            for sval in (F(0), F(1, 2), F(1)):
                kval = k0 + sval / 10
                g, r, l, gdot = matrices(kval, lift)
                checks[f"{lift}_{history}_s{sval}_seal_involution"] = matrix_equal(mul(r, r), eye(4))
                checks[f"{lift}_{history}_s{sval}_isometry"] = matrix_equal(mul(mul(transpose(r), g), r), g)
                checks[f"{lift}_{history}_s{sval}_reciprocal_inversion"] = matrix_equal(mul(mul(r, l), r), scale(F(-1), l))
                checks[f"{lift}_{history}_s{sval}_det_negative"] = determinant(g) < 0
                h = [[F(1), -kval], [-kval, F(1)]]
                cross = [[g[i][j + 2] for j in range(2)] for i in range(2)]
                schur = sub(eye(2), mul(mul(transpose(cross), inverse(h)), cross))
                checks[f"{lift}_{history}_s{sval}_schur_positive"] = schur[0][0] > 0 and determinant(schur) > 0
                checks[f"{lift}_{history}_s{sval}_differentiated_isometry"] = matrix_equal(mul(mul(transpose(r), gdot), r), gdot)
                gamma = scale(F(1, 2), mul(inverse(g), gdot))
                checks[f"{lift}_{history}_s{sval}_metric_connection"] = matrix_equal(add(mul(transpose(gamma), g), mul(g, gamma)), gdot)
                checks[f"{lift}_{history}_s{sval}_seal_connection"] = matrix_equal(mul(gamma, r), mul(r, gamma))
                checks[f"{lift}_{history}_s{sval}_not_L_parallel"] = not matrix_equal(mul(gamma, l), mul(l, gamma))
                tr_rate = trace(mul(inverse(g), gdot))
                volume_tangent = sub(gdot, scale(tr_rate / 4, g))
                checks[f"{lift}_{history}_s{sval}_volume_trace"] = trace(mul(inverse(g), volume_tangent)) == 0
                checks[f"{lift}_{history}_s{sval}_volume_seal"] = matrix_equal(mul(mul(transpose(r), volume_tangent), r), volume_tangent)
                invariant_path.append(pair_invariant(g, l))
            checks[f"{lift}_{history}_invariant_changes"] = len(set(invariant_path)) == 3
            endpoint_invariants.append((invariant_path[0], invariant_path[-1]))
        checks[f"{lift}_two_histories_inequivalent"] = endpoint_invariants[0] != endpoint_invariants[1]

        g, r, l, gdot = matrices(F(2), lift)
        metric_rank, metric_augmented = connection_system(g, gdot)
        seal_rank, seal_augmented = connection_system(g, gdot, r)
        full_rank, full_augmented = connection_system(g, gdot, r, l)
        static_rank, static_augmented = connection_system(g, zeros(4, 4), r, l)
        checks[f"{lift}_metric_rank"] = (metric_rank, metric_augmented, 16 - metric_rank) == (10, 10, 6)
        checks[f"{lift}_seal_rank"] = (
            seal_rank,
            seal_augmented,
            16 - seal_rank,
        ) == (16 - expected_dimensions[lift], 16 - expected_dimensions[lift], expected_dimensions[lift])
        checks[f"{lift}_varying_full_inconsistent"] = (full_rank, full_augmented) == (16, 17)
        checks[f"{lift}_constant_full_consistent"] = (static_rank, static_augmented) == (16, 16)

    checks["table_dimensions_match"] = {
        row["lift"]: int(row["metric_seal_connection_dimension"]) for row in lift_rows
    } == expected_dimensions

    # Independent moving-frame reconstruction at three exact times.
    n = zeros(4, 4)
    n[0][2] = F(1, 7)
    for sval in (F(0), F(1, 2), F(1)):
        s_matrix = add(eye(4), scale(sval, n))
        s_inverse = sub(eye(4), scale(sval, n))
        g0, r0, l0, g0dot = matrices(F(2) + sval / 10, "PLUS_IDENTITY")
        g_moving = mul(mul(transpose(s_inverse), g0), s_inverse)
        r_moving = mul(mul(s_matrix, r0), s_inverse)
        l_moving = mul(mul(s_matrix, l0), s_inverse)
        g0_gamma = scale(F(1, 2), mul(inverse(g0), g0dot))
        gamma_moving = add(scale(F(-1), n), mul(mul(s_matrix, g0_gamma), s_inverse))
        g_moving_dot = add(
            add(scale(F(-1), mul(mul(transpose(n), g0), s_inverse)), mul(mul(transpose(s_inverse), g0dot), s_inverse)),
            scale(F(-1), mul(mul(transpose(s_inverse), g0), n)),
        )
        r_moving_dot = sub(mul(mul(n, r0), s_inverse), mul(mul(s_matrix, r0), n))
        l_moving_dot = sub(mul(mul(n, l0), s_inverse), mul(mul(s_matrix, l0), n))
        checks[f"moving_s{sval}_metric"] = matrix_equal(add(mul(transpose(gamma_moving), g_moving), mul(g_moving, gamma_moving)), g_moving_dot)
        checks[f"moving_s{sval}_seal"] = matrix_equal(add(r_moving_dot, sub(mul(gamma_moving, r_moving), mul(r_moving, gamma_moving))), zeros(4, 4))
        checks[f"moving_s{sval}_true_mu_not_gauge"] = not matrix_equal(add(l_moving_dot, sub(mul(gamma_moving, l_moving), mul(l_moving, gamma_moving))), zeros(4, 4))

        constant_g, constant_r, constant_l, _ = matrices(F(2), "PLUS_IDENTITY")
        constant_g_moving = mul(mul(transpose(s_inverse), constant_g), s_inverse)
        constant_r_moving = mul(mul(s_matrix, constant_r), s_inverse)
        constant_l_moving = mul(mul(s_matrix, constant_l), s_inverse)
        pure_gamma = scale(F(-1), n)
        constant_g_dot = add(
            scale(F(-1), mul(mul(transpose(n), constant_g), s_inverse)),
            scale(F(-1), mul(mul(transpose(s_inverse), constant_g), n)),
        )
        constant_r_dot = sub(mul(mul(n, constant_r), s_inverse), mul(mul(s_matrix, constant_r), n))
        constant_l_dot = sub(mul(mul(n, constant_l), s_inverse), mul(mul(s_matrix, constant_l), n))
        checks[f"pure_frame_s{sval}_metric"] = matrix_equal(add(mul(transpose(pure_gamma), constant_g_moving), mul(constant_g_moving, pure_gamma)), constant_g_dot)
        checks[f"pure_frame_s{sval}_seal"] = matrix_equal(add(constant_r_dot, sub(mul(pure_gamma, constant_r_moving), mul(constant_r_moving, pure_gamma))), zeros(4, 4))
        checks[f"pure_frame_s{sval}_reciprocity"] = matrix_equal(add(constant_l_dot, sub(mul(pure_gamma, constant_l_moving), mul(constant_l_moving, pure_gamma))), zeros(4, 4))

    if not all(checks.values()):
        failed = sorted(name for name, passed in checks.items() if not passed)
        raise AssertionError(f"independent checks failed: {failed}")
    return {name: "PASS" for name in sorted(checks)}


def rejected(label, operation):
    try:
        operation()
    except (AssertionError, KeyError, ValueError):
        return "PASS"
    raise AssertionError(f"catch did not reject: {label}")


def main():
    model = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    tables = (
        rows(HERE / "LIFT_TIME_EXTENDABILITY.tsv"),
        rows(HERE / "TIME_HISTORY_CENSUS.tsv"),
        rows(HERE / "CONNECTION_HIERARCHY.tsv"),
        rows(HERE / "STATUS_LEDGER.tsv"),
        rows(HERE / "COMPLETENESS_SCOPE.tsv"),
        rows(HERE / "SOURCE_LINEAGE.tsv"),
    )
    validate_model(model, tables)
    independent = independent_reconstruction()
    catches = {}

    def validate(m=model, t=tables, override=None):
        return validate_model(m, t, override)

    changed = copy.deepcopy(model)
    changed["checks"][next(iter(changed["checks"]))] = "FAIL"
    catches["derivation_failure"] = rejected("derivation_failure", lambda: validate(changed))
    changed = copy.deepcopy(model)
    changed["check_count"] -= 1
    catches["derivation_count"] = rejected("derivation_count", lambda: validate(changed))
    changed = copy.deepcopy(model)
    changed["outcomes"].remove("FULL_RECIPROCAL_PARALLELISM_ONLY_CONSERVES_MU")
    catches["conservation_outcome_missing"] = rejected("conservation_outcome_missing", lambda: validate(changed))
    changed = copy.deepcopy(model)
    changed["lift_results"].pop("AXIS_REFLECTION")
    catches["lift_missing"] = rejected("lift_missing", lambda: validate(changed))
    changed = copy.deepcopy(model)
    changed["histories"].pop(next(iter(changed["histories"])))
    catches["history_missing_model"] = rejected("history_missing_model", lambda: validate(changed))
    changed = copy.deepcopy(model)
    changed["lift_results"]["PLUS_IDENTITY"]["full_reciprocal_parallelism_allows_dot_mu"] = True
    catches["full_parallelism_allows_dot_mu"] = rejected("full_parallelism_allows_dot_mu", lambda: validate(changed))

    modified = list(copy.deepcopy(tables))
    modified[0] = modified[0][:-1]
    catches["lift_row_missing"] = rejected("lift_row_missing", lambda: validate(t=tuple(modified)))
    modified = list(copy.deepcopy(tables))
    modified[0].append(copy.deepcopy(modified[0][0]))
    catches["lift_row_duplicate"] = rejected("lift_row_duplicate", lambda: validate(t=tuple(modified)))
    modified = list(copy.deepcopy(tables))
    modified[1] = modified[1][:-1]
    catches["history_row_missing"] = rejected("history_row_missing", lambda: validate(t=tuple(modified)))
    modified = list(copy.deepcopy(tables))
    modified[1].append(copy.deepcopy(modified[1][0]))
    catches["history_row_duplicate"] = rejected("history_row_duplicate", lambda: validate(t=tuple(modified)))
    modified = list(copy.deepcopy(tables))
    modified[1][0]["fixed_volume_status"] = "PHYSICAL_REPRESENTATIVE_SELECTED"
    catches["CSN_gauge_promoted"] = rejected("CSN_gauge_promoted", lambda: validate(t=tuple(modified)))
    modified = list(copy.deepcopy(tables))
    next(row for row in modified[2] if row["level"] == "C04")["mu_effect"] = "MU_VALUE_SELECTED"
    catches["conservation_promoted_to_selection"] = rejected("conservation_promoted_to_selection", lambda: validate(t=tuple(modified)))
    modified = list(copy.deepcopy(tables))
    next(row for row in modified[2] if row["level"] == "C04")["current_authority"] = "SELECTED_BY_UDT"
    catches["transport_authority_promoted"] = rejected("transport_authority_promoted", lambda: validate(t=tuple(modified)))
    modified = list(copy.deepcopy(tables))
    next(row for row in modified[2] if row["level"] == "C06")["current_authority"] = "PHYSICAL_EVOLUTION"
    catches["moving_frame_promoted"] = rejected("moving_frame_promoted", lambda: validate(t=tuple(modified)))
    modified = list(copy.deepcopy(tables))
    next(row for row in modified[3] if row["claim_id"] == "T06")["status"] = "DERIVED_UNCONDITIONAL"
    catches["parallelism_premise_erased"] = rejected("parallelism_premise_erased", lambda: validate(t=tuple(modified)))
    modified = list(copy.deepcopy(tables))
    next(row for row in modified[3] if row["claim_id"] == "T07")["status"] = "DERIVED"
    catches["mu_value_promoted"] = rejected("mu_value_promoted", lambda: validate(t=tuple(modified)))
    modified = list(copy.deepcopy(tables))
    next(row for row in modified[3] if row["claim_id"] == "T12")["status"] = "CONFIRMED"
    catches["frozen_results_invalidated"] = rejected("frozen_results_invalidated", lambda: validate(t=tuple(modified)))
    modified = list(copy.deepcopy(tables))
    next(row for row in modified[3] if row["claim_id"] == "T13")["status"] = "DERIVED"
    catches["dynamic_theorem_promoted"] = rejected("dynamic_theorem_promoted", lambda: validate(t=tuple(modified)))
    modified = list(copy.deepcopy(tables))
    next(row for row in modified[3] if row["claim_id"] == "T14")["status"] = "DERIVED"
    catches["physical_transport_selected"] = rejected("physical_transport_selected", lambda: validate(t=tuple(modified)))
    modified = list(copy.deepcopy(tables))
    next(row for row in modified[4] if row["criterion"] == "dynamical_character")["coverage"] = "FULL"
    catches["dynamic_completeness_inflated"] = rejected("dynamic_completeness_inflated", lambda: validate(t=tuple(modified)))
    modified = list(copy.deepcopy(tables))
    modified[5] = [row for row in modified[5] if row["id"] != "S12"]
    catches["source_missing"] = rejected("source_missing", lambda: validate(t=tuple(modified)))
    modified = list(copy.deepcopy(tables))
    next(row for row in modified[5] if row["id"] == "S15")["source_status"] = "CURRENT_UDT_PHYSICS"
    catches["withdrawn_xmax_authority_restored"] = rejected("withdrawn_xmax_authority_restored", lambda: validate(t=tuple(modified)))

    csn_path = "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md"
    csn_corrupt = (ROOT / csn_path).read_text(encoding="utf-8").replace(
        "derivative order and time-live degrees of freedom", "time evolution selected"
    )
    catches["CSN_source_mutated"] = rejected(
        "CSN_source_mutated", lambda: validate(override={csn_path: csn_corrupt})
    )
    reset_path = "udt_premise_reset_audit_2026-07-19/AUDIT_REPORT.md"
    reset_corrupt = (ROOT / reset_path).read_text(encoding="utf-8").replace(
        "conditional mathematics only", "current observer physics"
    )
    catches["premise_reset_mutated"] = rejected(
        "premise_reset_mutated", lambda: validate(override={reset_path: reset_corrupt})
    )

    hashes = {}
    for name in (
        "AUDIT_REPORT.md",
        "COMPLETENESS_SCOPE.tsv",
        "CONNECTION_HIERARCHY.tsv",
        "DERIVATION_RESULT.json",
        "LIFT_TIME_EXTENDABILITY.tsv",
        "PREREGISTRATION.md",
        "SOURCE_LINEAGE.tsv",
        "STATUS_LEDGER.tsv",
        "TIME_HISTORY_CENSUS.tsv",
    ):
        hashes[name] = hashlib.sha256((HERE / name).read_bytes()).hexdigest()

    output = {
        "schema": "udt-kinematic-time-extendability-independent-verification-1.0",
        "result": "PASS_VERIFIED_WITH_CAVEATS",
        "maximum_conclusion": "UDT_KINEMATIC_TIME_EXTENDABILITY_STATUS_CHARACTERIZED",
        "counts": {
            "derivation_checks": 177,
            "independent_checks": len(independent),
            "catch_proofs": len(catches),
        },
        "independent_checks": independent,
        "catch_proofs": catches,
        "hashes": hashes,
        "caveats": [
            "kinematic path consistency is not an action-derived physical time evolution",
            "full reciprocal-generator parallelism is a tested premise not current selected authority",
            "complete only for registered constant real isotropic lifts and declared cross patterns",
            "no fresh external-model verifier was authorized; independent implementation is standard-library rational algebra",
        ],
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("verification=PASS_VERIFIED_WITH_CAVEATS")
    print("derivation_checks=177")
    print(f"independent_checks={len(independent)}")
    print(f"catch_proofs={len(catches)}")


if __name__ == "__main__":
    main()
