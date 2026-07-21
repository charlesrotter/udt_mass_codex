#!/usr/bin/env python3
"""Independent standard-library verifier for the complete-seal selector audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(name):
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def zeros(n, m):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def eye(n):
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def diag(*values):
    out = zeros(len(values), len(values))
    for i, value in enumerate(values):
        out[i][i] = F(value)
    return out


def transpose(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scale(c, a):
    return [[F(c) * value for value in row] for row in a]


def mul(a, b):
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def block_diag(a, b):
    out = zeros(len(a) + len(b), len(a[0]) + len(b[0]))
    for i in range(len(a)):
        for j in range(len(a[0])):
            out[i][j] = a[i][j]
    for i in range(len(b)):
        for j in range(len(b[0])):
            out[len(a) + i][len(a[0]) + j] = b[i][j]
    return out


def full_metric(h, c, q):
    out = zeros(4, 4)
    for i in range(2):
        for j in range(2):
            out[i][j] = h[i][j]
            out[i][j + 2] = c[i][j]
            out[j + 2][i] = c[i][j]
            out[i + 2][j + 2] = q[i][j]
    return out


def rank(a):
    if not a:
        return 0
    work = [line[:] for line in a]
    nrows, ncols = len(work), len(work[0])
    row = 0
    for column in range(ncols):
        pivot = next((r for r in range(row, nrows) if work[r][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        divisor = work[row][column]
        work[row] = [value / divisor for value in work[row]]
        for r in range(nrows):
            if r != row and work[r][column]:
                factor = work[r][column]
                work[r] = [work[r][j] - factor * work[row][j] for j in range(ncols)]
        row += 1
        if row == nrows:
            break
    return row


def determinant(a):
    work = [line[:] for line in a]
    value = F(1)
    sign = 1
    for column in range(len(work)):
        pivot = next((r for r in range(column, len(work)) if work[r][column]), None)
        if pivot is None:
            return F(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        pivot_value = work[column][column]
        value *= pivot_value
        for r in range(column + 1, len(work)):
            factor = work[r][column] / pivot_value
            for j in range(column, len(work)):
                work[r][j] -= factor * work[column][j]
    return sign * value


def inverse(a):
    n = len(a)
    work = [a[i][:] + eye(n)[i] for i in range(n)]
    row = 0
    for column in range(n):
        pivot = next((r for r in range(row, n) if work[r][column]), None)
        if pivot is None:
            raise AssertionError("singular")
        work[row], work[pivot] = work[pivot], work[row]
        divisor = work[row][column]
        work[row] = [value / divisor for value in work[row]]
        for r in range(n):
            if r != row and work[r][column]:
                factor = work[r][column]
                work[r] = [work[r][j] - factor * work[row][j] for j in range(2 * n)]
        row += 1
    return [line[n:] for line in work]


def validate(model, tables, source_override=None):
    if model["schema"] != "udt-complete-seal-fixed-set-selector-derivation-1.0":
        raise AssertionError("schema")
    if model["maximum_conclusion"] != "UDT_COMPLETE_SEAL_FIXED_SET_SELECTOR_STATUS_CHARACTERIZED":
        raise AssertionError("maximum")
    if model["check_count"] != 117 or len(model["checks"]) != 117 or set(model["checks"].values()) != {"PASS"}:
        raise AssertionError("checks")
    required = {
        "COMPLETE_LIFT_REMAINS_OPEN_BECAUSE_SEAL_POINTWISE_ACTION_IS_UNDERDETERMINED",
        "PLUS_IDENTITY_SELECTED_ONLY_IF_POINTWISE_CODIMENSION_ONE_METRIC_MIRROR_IS_ADDED",
        "CURRENT_ODD_PHI_FOLD_DOES_NOT_SUPPLY_ORDINARY_POINTWISE_METRIC_MIRROR",
        "ORIENTATION_PRESERVATION_IS_NOT_DERIVED_AND_WOULD_LEAVE_TWO_REFLECTION_LIFTS",
        "REFLECTION_SEAL_TWO_PAIR_ROUTE_REMAINS_CONDITIONAL_ON_EXTRA_ANGULAR_IDENTIFICATION",
    }
    if not required.issubset(model["outcomes"]):
        raise AssertionError("outcomes")
    if model["conditional_rulings"]["current_static_phi_odd_fold"] != "NO_COMPLETE_LIFT_SELECTION":
        raise AssertionError("current fold promoted")
    if model["two_pair_consequence"]["selection"] != "OPEN; the desired second pair cannot be used to select its own lift":
        raise AssertionError("circular selection")
    if model["smallest_missing_join"]["status"] != "OPEN":
        raise AssertionError("gate closed")

    sources, lifts, interpretations, jets, witnesses, status, completeness = tables
    if tuple(map(len, tables)) != (14, 4, 9, 4, 8, 18, 10):
        raise AssertionError("table counts")
    keys = ("id", "lift", "interpretation_id", "lift", "witness_id", "claim_id", "criterion")
    for data, key in zip(tables, keys):
        if len({row[key] for row in data}) != len(data):
            raise AssertionError(f"duplicates {key}")
    by_lift = {row["lift"]: row for row in lifts}
    expected = {
        "PLUS_IDENTITY": ("-1", "3", "1", "NO"),
        "MINUS_IDENTITY": ("-1", "1", "3", "NO"),
        "AXIS_REFLECTION": ("+1", "2", "2", "YES_CONDITIONAL"),
        "HOPF_EXCHANGE_LOCAL": ("+1", "2", "2", "YES_CONDITIONAL"),
    }
    for lift, values in expected.items():
        row = by_lift[lift]
        if (row["full_determinant"], row["fixed_dimension"], row["anti_fixed_dimension"], row["seal_local_second_pair"]) != values:
            raise AssertionError(f"lift {lift}")
    by_interpretation = {row["interpretation_id"]: row for row in interpretations}
    if by_interpretation["I01"]["result"] != "CONDITIONAL_SELECTION_ONLY":
        raise AssertionError("ordinary mirror promoted")
    if by_interpretation["I08"]["eligible_lifts"] != "ALL_FOUR" or by_interpretation["I08"]["result"] != "NO_SELECTION":
        raise AssertionError("scalar fold promoted")
    if by_interpretation["I09"]["result"] != "FORBIDDEN_SELECTOR":
        raise AssertionError("two-pair circularity")
    by_claim = {row["claim_id"]: row for row in status}
    expected_status = {
        "F02": "NOT_DERIVED",
        "F03": "REFUTED_AS_CURRENT_INFERENCE",
        "F04": "DERIVED_CONDITIONAL",
        "F07": "NOT_DERIVED",
        "F12": "NOT_DERIVED",
        "F13": "FORBIDDEN_CIRCULARITY",
        "F14": "NOT_DERIVED",
        "F16": "OPEN_SHARPENED_GATE",
        "F18": "NOT_DERIVED_AND_EXCLUDED",
    }
    for claim, expected_value in expected_status.items():
        if by_claim[claim]["status"] != expected_value:
            raise AssertionError(f"status {claim}")
    global_row = next(row for row in completeness if row["criterion"] == "angular_global_data")
    if global_row["coverage"] != "NOT_COVERED":
        raise AssertionError("global scope promoted")

    required_sources = {
        "UDT_NATIVE_ACTION_COLD_PACKET.md": "BINDING_FOUNDATION_PACKET",
        "finite_cell_seal_boundary_phase_join_2026-07-20/AUDIT_REPORT.md": "VERIFIED_WITH_CAVEATS",
        "udt_clock_ruler_soldering_selector_audit_2026-07-20/AUDIT_REPORT.md": "VERIFIED_WITH_CAVEATS",
        "udt_complete_lift_mu_closure_audit_2026-07-20/AUDIT_REPORT.md": "VERIFIED_WITH_CAVEATS",
        "udt_metric_native_two_pair_selector_audit_2026-07-21/AUDIT_REPORT.md": "IMMEDIATE_PARENT",
    }
    source_map = {row["path"]: row for row in sources}
    for path, source_status in required_sources.items():
        if source_map.get(path, {}).get("source_status") != source_status:
            raise AssertionError(f"source authority {path}")
    needles = {
        "UDT_NATIVE_ACTION_COLD_PACKET.md": "The spatial-depth mirror makes `phi` odd at the",
        "finite_cell_seal_boundary_phase_join_2026-07-20/AUDIT_REPORT.md": "Current UDT does not supply that premise",
        "udt_clock_ruler_soldering_selector_audit_2026-07-20/AUDIT_REPORT.md": "the complete angular/normal/time-on lift",
        "udt_complete_lift_mu_closure_audit_2026-07-20/AUDIT_REPORT.md": "All four registered local angular lift classes",
        "udt_metric_native_two_pair_selector_audit_2026-07-21/AUDIT_REPORT.md": "the complete angular seal lift is not selected",
        "transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md": "does not put reciprocal weights",
        "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md": "does not derive two periodic",
        "LIVE.md": "no torus lattice, collapse cycles",
    }
    for path, needle in needles.items():
        text = source_override[path] if source_override and path in source_override else (ROOT / path).read_text(encoding="utf-8")
        if needle not in text:
            raise AssertionError(f"source semantics {path}")


def independent_algebra():
    checks = {}

    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        checks[name] = "PASS"

    i2 = eye(2)
    swap = [[F(0), F(1)], [F(1), F(0)]]
    axis = diag(1, -1)
    base = diag(1, -1)
    eta = diag(-1, 1, 1, 1)
    lifts = {
        "PLUS_IDENTITY": i2,
        "MINUS_IDENTITY": scale(-1, i2),
        "AXIS_REFLECTION": axis,
        "HOPF_EXCHANGE_LOCAL": swap,
    }
    expected = {
        "PLUS_IDENTITY": (3, 1, F(-1), 2, 1),
        "MINUS_IDENTITY": (1, 3, F(-1), 0, 3),
        "AXIS_REFLECTION": (2, 2, F(1), 1, 2),
        "HOPF_EXCHANGE_LOCAL": (2, 2, F(1), 1, 2),
    }
    lift_data = {}
    for name, angular in lifts.items():
        seal = block_diag(base, angular)
        fixed = 4 - rank(sub(seal, eye(4)))
        anti = 4 - rank(add(seal, eye(4)))
        spatial = block_diag([[-F(1)]], angular)
        spatial_fixed = 3 - rank(sub(spatial, eye(3)))
        spatial_anti = 3 - rank(add(spatial, eye(3)))
        check(f"{name}_involution", mul(seal, seal) == eye(4))
        check(f"{name}_eta_isometry", mul(mul(transpose(seal), eta), seal) == eta)
        check(f"{name}_fixed", fixed == expected[name][0])
        check(f"{name}_anti", anti == expected[name][1])
        check(f"{name}_determinant", determinant(seal) == expected[name][2])
        check(f"{name}_det_from_anti", determinant(seal) == (-1) ** anti)
        check(f"{name}_spatial_fixed", spatial_fixed == expected[name][3])
        check(f"{name}_spatial_anti", spatial_anti == expected[name][4])
        check(f"{name}_time_fixed", seal[0][0] == 1)
        check(f"{name}_radial_reversed", seal[1][1] == -1)
        lift_data[name] = (fixed, anti)

    # Exact 45-degree conjugacy with the common sqrt(2) factor cancelled.
    q = [[F(1), F(-1)], [F(1), F(1)]]
    conjugate = scale(F(1, 2), mul(mul(transpose(q), swap), q))
    check("axis_Hopf_local_conjugacy", conjugate == axis)
    check("codim_one_unique", [name for name, value in lift_data.items() if value[1] == 1] == ["PLUS_IDENTITY"])
    check("orientation_preserving_two", {name for name, angular in lifts.items() if determinant(block_diag(base, angular)) == 1} == {"AXIS_REFLECTION", "HOPF_EXCHANGE_LOCAL"})
    check("orientation_reversing_two", {name for name, angular in lifts.items() if determinant(block_diag(base, angular)) == -1} == {"PLUS_IDENTITY", "MINUS_IDENTITY"})

    # Symmetric metric-jet parity dimensions.
    for name, (fixed, anti) in lift_data.items():
        signs = [F(1)] * fixed + [F(-1)] * anti
        even = odd = 0
        for i in range(4):
            for j in range(i, 4):
                if signs[i] * signs[j] == 1:
                    even += 1
                else:
                    odd += 1
        check(f"{name}_jet_even", even == fixed * (fixed + 1) // 2 + anti * (anti + 1) // 2)
        check(f"{name}_jet_odd", odd == fixed * anti)
        check(f"{name}_jet_complete", even + odd == 10)

    # Odd scalar slope versus ordinary even tangential metric.
    check("ordinary_even_linear_jet_forces_zero", F(1) != -F(1))
    check("odd_phi_value_zero", F(0) == 0)
    check("odd_phi_slope_can_be_nonzero", F(1) != 0)

    # Eight exact nonzero-cross witnesses.
    e = F(1, 10)
    cross = {
        "PLUS_IDENTITY": [[e, e], [e, e]],
        "MINUS_IDENTITY": [[e, e], [-e, -e]],
        "AXIS_REFLECTION": [[e, e], [e, -e]],
        "HOPF_EXCHANGE_LOCAL": [[e, e], [e, e]],
    }
    expected_det = {
        ("PLUS_IDENTITY", 2): F(-78, 25),
        ("PLUS_IDENTITY", 3): F(-204, 25),
        ("MINUS_IDENTITY", 2): F(-74, 25),
        ("MINUS_IDENTITY", 3): F(-198, 25),
        ("AXIS_REFLECTION", 2): F(-7599, 2500),
        ("AXIS_REFLECTION", 3): F(-20099, 2500),
        ("HOPF_EXCHANGE_LOCAL", 2): F(-78, 25),
        ("HOPF_EXCHANGE_LOCAL", 3): F(-204, 25),
    }
    for name, angular in lifts.items():
        seal = block_diag(swap, angular)
        for k in (2, 3):
            h = [[F(1), F(-k)], [F(-k), F(1)]]
            metric = full_metric(h, cross[name], i2)
            schur = sub(i2, mul(mul(transpose(cross[name]), inverse(h)), cross[name]))
            check(f"{name}_mu{k*k}_isometry", mul(mul(transpose(seal), metric), seal) == metric)
            check(f"{name}_mu{k*k}_determinant", determinant(metric) == expected_det[(name, k)])
            check(f"{name}_mu{k*k}_screen_positive", schur[0][0] > 0 and determinant(schur) > 0)
            check(f"{name}_mu{k*k}_fixed_unchanged", 4 - rank(sub(seal, eye(4))) == expected[name][0])
            check(f"{name}_mu{k*k}_anti_unchanged", 4 - rank(add(seal, eye(4))) == expected[name][1])

    mirror = diag(1, -1, 1, 1)
    check("orientation_reversing_isometry", mul(mul(transpose(mirror), eta), mirror) == eta)
    check("orientation_reversing_isometry_det", determinant(mirror) == -1)
    return checks


def expect_failure(name, function, catches):
    try:
        function()
    except (AssertionError, KeyError, StopIteration):
        catches[name] = "PASS"
        return
    raise AssertionError(f"catch did not fire: {name}")


def main():
    model = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    tables = (
        rows("SOURCE_LINEAGE.tsv"),
        rows("COMPLETE_LIFT_CLASSIFICATION.tsv"),
        rows("INTERPRETATION_SELECTOR.tsv"),
        rows("FIRST_JET_PARITY.tsv"),
        rows("NONZERO_CROSS_WITNESSES.tsv"),
        rows("STATUS_LEDGER.tsv"),
        rows("COMPLETENESS_SCOPE.tsv"),
    )
    validate(model, tables)
    independent = independent_algebra()
    catches = {}

    def mutated_model(path, value):
        candidate = copy.deepcopy(model)
        target = candidate
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        return lambda: validate(candidate, tables)

    expect_failure("wrong_schema", mutated_model(["schema"], "wrong"), catches)
    expect_failure("missing_check", mutated_model(["check_count"], 116), catches)
    expect_failure("current_fold_selects_lift", mutated_model(["conditional_rulings", "current_static_phi_odd_fold"], "PLUS_IDENTITY"), catches)
    expect_failure("two_pair_circular_selection", mutated_model(["two_pair_consequence", "selection"], "REFLECTION_SELECTED"), catches)
    expect_failure("open_gate_closed", mutated_model(["smallest_missing_join", "status"], "DERIVED"), catches)

    def changed_table(index, mutate):
        candidate = copy.deepcopy(tables)
        mutate(candidate[index])
        return lambda: validate(model, candidate)

    expect_failure("missing_source", changed_table(0, lambda data: data.pop()), catches)
    expect_failure("duplicate_source", changed_table(0, lambda data: data.__setitem__(1, copy.deepcopy(data[0]))), catches)
    expect_failure("missing_lift", changed_table(1, lambda data: data.pop()), catches)
    expect_failure("plus_identity_second_pair", changed_table(1, lambda data: data[0].__setitem__("seal_local_second_pair", "YES")), catches)
    expect_failure("ordinary_mirror_unconditional", changed_table(2, lambda data: data[0].__setitem__("result", "DERIVED")), catches)
    expect_failure("scalar_fold_selects", changed_table(2, lambda data: data[7].__setitem__("eligible_lifts", "PLUS_IDENTITY")), catches)
    expect_failure("desired_pair_selects", changed_table(2, lambda data: data[8].__setitem__("result", "DERIVED")), catches)
    expect_failure("full_involution_promoted", changed_table(5, lambda data: data[1].__setitem__("status", "DERIVED")), catches)
    expect_failure("mirror_word_promoted", changed_table(5, lambda data: data[2].__setitem__("status", "DERIVED")), catches)
    expect_failure("orientation_law_promoted", changed_table(5, lambda data: data[6].__setitem__("status", "DERIVED")), catches)
    expect_failure("scalar_fold_lift_promoted", changed_table(5, lambda data: data[11].__setitem__("status", "DERIVED")), catches)
    expect_failure("circularity_removed", changed_table(5, lambda data: data[12].__setitem__("status", "DERIVED")), catches)
    expect_failure("boundary_two_pair_promoted", changed_table(5, lambda data: data[13].__setitem__("status", "DERIVED")), catches)
    expect_failure("complete_lift_closed", changed_table(5, lambda data: data[15].__setitem__("status", "DERIVED")), catches)
    expect_failure("Hopf_selector_promoted", changed_table(5, lambda data: data[17].__setitem__("status", "DERIVED")), catches)
    expect_failure("global_scope_promoted", changed_table(6, lambda data: next(row for row in data if row["criterion"] == "angular_global_data").__setitem__("coverage", "COMPLETE")), catches)

    needles = {
        "UDT_NATIVE_ACTION_COLD_PACKET.md": "The spatial-depth mirror makes `phi` odd at the",
        "finite_cell_seal_boundary_phase_join_2026-07-20/AUDIT_REPORT.md": "Current UDT does not supply that premise",
        "udt_clock_ruler_soldering_selector_audit_2026-07-20/AUDIT_REPORT.md": "the complete angular/normal/time-on lift",
        "udt_complete_lift_mu_closure_audit_2026-07-20/AUDIT_REPORT.md": "All four registered local angular lift classes",
        "udt_metric_native_two_pair_selector_audit_2026-07-21/AUDIT_REPORT.md": "the complete angular seal lift is not selected",
        "transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md": "does not put reciprocal weights",
        "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md": "does not derive two periodic",
        "LIVE.md": "no torus lattice, collapse cycles",
    }
    for path, needle in needles.items():
        source = (ROOT / path).read_text(encoding="utf-8")
        expect_failure(
            f"source_semantics_removed_{Path(path).name}",
            lambda path=path, needle=needle, source=source: validate(
                model, tables, {path: source.replace(needle, "REMOVED", 1)}
            ),
            catches,
        )

    output = {
        "schema": "udt-complete-seal-fixed-set-selector-verification-1.0",
        "result": "PASS_VERIFIED_WITH_CAVEATS",
        "maximum_conclusion": model["maximum_conclusion"],
        "derivation_check_count": model["check_count"],
        "independent_check_count": len(independent),
        "catch_proof_count": len(catches),
        "checks": dict(sorted(independent.items())),
        "catch_proofs": dict(sorted(catches.items())),
        "premise_boundary": "Current UDT fixes scalar fold parity only. Every complete lift selection remains conditional on an unprovided pointwise, orientation, or angular-identification premise.",
        "derivation_result_sha256": hashlib.sha256((HERE / "DERIVATION_RESULT.json").read_bytes()).hexdigest(),
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
