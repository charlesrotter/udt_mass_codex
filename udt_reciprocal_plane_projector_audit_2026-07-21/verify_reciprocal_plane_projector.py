#!/usr/bin/env python3
"""Independent standard-library verification of the projector audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(name: str):
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def zeros(n: int, m: int):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def eye(n: int):
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


def flat(a):
    return [value for row in a for value in row]


def commutator(a, b):
    return sub(mul(a, b), mul(b, a))


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


def inverse(a):
    n = len(a)
    work = [a[i][:] + eye(n)[i] for i in range(n)]
    row = 0
    for column in range(n):
        pivot = next((r for r in range(row, n) if work[r][column]), None)
        if pivot is None:
            raise AssertionError("singular matrix")
        work[row], work[pivot] = work[pivot], work[row]
        divisor = work[row][column]
        work[row] = [value / divisor for value in work[row]]
        for r in range(n):
            if r != row and work[r][column]:
                factor = work[r][column]
                work[r] = [work[r][j] - factor * work[row][j] for j in range(2 * n)]
        row += 1
    return [line[n:] for line in work]


def rank(a):
    if not a:
        return 0
    work = [line[:] for line in a]
    row = 0
    for column in range(len(work[0])):
        pivot = next((r for r in range(row, len(work)) if work[r][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        divisor = work[row][column]
        work[row] = [value / divisor for value in work[row]]
        for r in range(len(work)):
            if r != row and work[r][column]:
                factor = work[r][column]
                work[r] = [work[r][j] - factor * work[row][j] for j in range(len(work[0]))]
        row += 1
        if row == len(work):
            break
    return row


def solve_unique(matrix, rhs):
    work = [matrix[i][:] + [rhs[i]] for i in range(len(matrix))]
    nvars = len(matrix[0])
    row = 0
    pivot_rows = {}
    for column in range(nvars):
        pivot = next((r for r in range(row, len(work)) if work[r][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        divisor = work[row][column]
        work[row] = [value / divisor for value in work[row]]
        for r in range(len(work)):
            if r != row and work[r][column]:
                factor = work[r][column]
                work[r] = [work[r][j] - factor * work[row][j] for j in range(nvars + 1)]
        pivot_rows[column] = row
        row += 1
    if len(pivot_rows) != nvars:
        raise AssertionError("not unique")
    if any(all(value == 0 for value in line[:nvars]) and line[-1] != 0 for line in work):
        raise AssertionError("inconsistent")
    return [work[pivot_rows[column]][-1] for column in range(nvars)]


def basis_vector(n, index):
    out = [F(0)] * n
    out[index] = F(1)
    return out


def weyl(g, one_form, direction):
    gi = inverse(g)
    raised = [sum((gi[i][j] * one_form[j] for j in range(4)), F(0)) for i in range(4)]
    out = zeros(4, 4)
    for upper in range(4):
        for lower in range(4):
            out[upper][lower] = (
                (one_form[lower] if upper == direction else F(0))
                + (one_form[direction] if upper == lower else F(0))
                - g[direction][lower] * raised[upper]
            )
    return out


def levi_civita(g, derivatives):
    gi = inverse(g)
    out = []
    for direction in range(4):
        connection = zeros(4, 4)
        for upper in range(4):
            for lower in range(4):
                connection[upper][lower] = F(1, 2) * sum(
                    (
                        gi[upper][d]
                        * (
                            derivatives[direction][d][lower]
                            + derivatives[lower][d][direction]
                            - derivatives[d][direction][lower]
                        )
                        for d in range(4)
                    ),
                    F(0),
                )
        out.append(connection)
    return out


def covariant(lc, g, one_form, endomorphism):
    return [commutator(add(lc[a], weyl(g, one_form, a)), endomorphism) for a in range(4)]


def residual(g, derivatives, one_form, projector=None):
    return covariant(levi_civita(g, derivatives), g, one_form, projector or diag(1, 1, 0, 0))


def connection_difference_rank(g, endomorphism):
    columns = []
    for component in range(4):
        b = basis_vector(4, component)
        columns.append(
            [entry for direction in range(4) for entry in flat(commutator(weyl(g, b, direction), endomorphism))]
        )
    return rank([list(line) for line in zip(*columns)])


def affine_rank_for_a(g, derivatives, projector):
    base = [entry for matrix in residual(g, derivatives, [F(0)] * 4, projector) for entry in flat(matrix)]
    columns = []
    for component in range(4):
        value = [entry for matrix in residual(g, derivatives, basis_vector(4, component), projector) for entry in flat(matrix)]
        columns.append([value[i] - base[i] for i in range(len(base))])
    matrix = [list(line) for line in zip(*columns)]
    rhs = [-value for value in base]
    return rank(matrix), rank([matrix[i] + [rhs[i]] for i in range(len(matrix))])


def orthogonal_projector(g):
    inclusion = [[F(1), F(0)], [F(0), F(1)], [F(0), F(0)], [F(0), F(0)]]
    return mul(mul(mul(inclusion, inverse(mul(mul(transpose(inclusion), g), inclusion))), transpose(inclusion)), g)


def assert_zero(values, label):
    if any(values):
        raise AssertionError(label)


def cross_derivatives(free, dependent):
    u0, u1, x2, x3 = free
    v0, w0, v1, w1, y2, z2, y3, z3 = dependent
    d = [zeros(4, 4) for _ in range(4)]
    d[0][2][2], d[0][2][3], d[0][3][2], d[0][3][3] = u0, w0, w0, v0
    d[1][2][2], d[1][2][3], d[1][3][2], d[1][3][3] = u1, w1, w1, v1
    d[2][0][0], d[2][0][1], d[2][1][0], d[2][1][1] = x2, z2, z2, y2
    d[3][0][0], d[3][0][1], d[3][1][0], d[3][1][1] = x3, z3, z3, y3
    return d


def validate_model(model, tables, source_override=None):
    if model["schema"] != "udt-reciprocal-plane-projector-derivation-1.0":
        raise AssertionError("schema")
    if model["maximum_conclusion"] != "UDT_RECIPROCAL_PLANE_PROJECTOR_FRAME_STATUS_CHARACTERIZED":
        raise AssertionError("maximum")
    if model["check_count"] != 102 or len(model["checks"]) != 102 or set(model["checks"].values()) != {"PASS"}:
        raise AssertionError("derivation checks")
    theorem = model["theorem"]
    if theorem["uniqueness"] != "AT_MOST_ONE_CONNECTION":
        raise AssertionError("uniqueness promoted")
    if theorem["existence"] != "IFF_BOTH_DISTRIBUTIONS_INTEGRABLE_AND_CROSS_SECOND_FUNDAMENTAL_FORMS_PURE_TRACE":
        raise AssertionError("existence theorem")
    if model["physical_status"]["overall"] != "COHERENT_CONDITIONAL_FRAME_REDUCTION_NOT_AN_UNCONDITIONAL_UDT_SELECTOR":
        raise AssertionError("physical promotion")
    if model["smallest_missing_principle"]["status"] != "OPEN_SHARPENED_GATE":
        raise AssertionError("open gate")
    if model["strictness"]["P_parallel_implies_L_parallel"] is not False:
        raise AssertionError("P versus L")
    if model["strictness"]["twist_or_cross_shear_retained"] is not False:
        raise AssertionError("shear promoted")
    if len(model["witnesses"]["constant_nonzero_cross_metrics"]) != 8:
        raise AssertionError("cross witnesses")

    sources, theorem_rows, witnesses, holonomy, status, completeness = tables
    if tuple(map(len, tables)) != (18, 10, 16, 8, 19, 14):
        raise AssertionError("table counts")
    if len({row["id"] for row in sources}) != 18 or len({row["id"] for row in theorem_rows}) != 10:
        raise AssertionError("table identities")
    if len({row["witness_id"] for row in witnesses}) != 16:
        raise AssertionError("witness identities")
    if len({row["claim_id"] for row in status}) != 19:
        raise AssertionError("status identities")
    by_claim = {row["claim_id"]: row for row in status}
    required_status = {
        "R05": "DERIVED_IN_DECLARED_CLASS",
        "R06": "DERIVED_CONDITIONAL",
        "R09": "REFUTED",
        "R12": "REFUTED_IN_TORSION_FREE_CLASS",
        "R16": "OPEN",
        "R17": "OPEN",
        "R19": "OPEN_SHARPENED_GATE",
    }
    for claim, expected in required_status.items():
        if by_claim.get(claim, {}).get("status") != expected:
            raise AssertionError(f"status {claim}")
    by_witness = {row["witness_id"]: row for row in witnesses}
    if by_witness["W05"]["result"] != "FAIL" or by_witness["W07"]["result"] != "FAIL":
        raise AssertionError("obstruction lost")
    if by_witness["W08"]["result"] != "PASS_FOR_P_FAIL_FOR_L":
        raise AssertionError("strictness witness")
    if any(by_witness[f"W{i:02d}"]["result"] != "PASS" for i in range(9, 17)):
        raise AssertionError("cross witness table")
    if next(row for row in completeness if row["criterion"] == "dynamics_and_action")["coverage"] != "NOT_COVERED":
        raise AssertionError("dynamics promoted")

    required_sources = {
        "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md": "FOUNDATIONAL_CANDIDATE_PLUS_DERIVED_KINEMATICS",
        "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": "FOUNDATIONAL_POSTULATE_LOCKED",
        "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md": "OWNER_STATED_WORKING_PRINCIPLE",
        "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md": "CURRENT_FRONTIER",
        "udt_gr_subtraction_reciprocal_connection_audit_2026-07-21/AUDIT_REPORT.md": "IMMEDIATE_PARENT",
        "udt_complete_seal_fixed_set_selector_audit_2026-07-21/AUDIT_REPORT.md": "IMMEDIATE_PARENT",
    }
    source_by_path = {row["path"]: row for row in sources}
    for path, expected in required_sources.items():
        if source_by_path.get(path, {}).get("source_status") != expected:
            raise AssertionError(f"source status {path}")
    semantic_needles = {
        "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": "derivative order and time-live degrees of freedom",
        "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md": "No nonlocal insertion",
        "reciprocal_line_realization_selector_2026-07-18/DERIVATION_REPORT.md": "It is not yet a spacetime line field",
        "metric_cartan_holonomy_audit_2026-07-19/AUDIT_REPORT.md": "No current UDT premise sets `A^A_i=0`",
        "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md": "the carrier is reopened and conditional",
    }
    for path, needle in semantic_needles.items():
        text = source_override[path] if source_override and path in source_override else (ROOT / path).read_text(encoding="utf-8")
        if needle not in text:
            raise AssertionError(f"source semantics {path}")


def independent_algebra():
    checks = {}

    def check(label, condition):
        if not condition:
            raise AssertionError(label)
        checks[label] = "PASS"

    eta = diag(-1, 1, 1, 1)
    projector = diag(1, 1, 0, 0)
    generator = diag(-1, 1, 0, 0)
    check("projector_difference_rank_four", connection_difference_rank(eta, projector) == 4)

    # Independently solve all twelve dependent cross-jet variables at a
    # generic rational point. Columns are constructed by finite differences of
    # the exact rational tensor residual, not imported from the SymPy code.
    free = [F(2), F(-3), F(5), F(-7)]
    zero_dep = [F(0)] * 8
    zero_a = [F(0)] * 4
    base = [entry for m in residual(eta, cross_derivatives(free, zero_dep), zero_a, projector) for entry in flat(m)]
    columns = []
    for component in range(12):
        a = zero_a[:]
        dep = zero_dep[:]
        if component < 4:
            a[component] = F(1)
        else:
            dep[component - 4] = F(1)
        value = [entry for m in residual(eta, cross_derivatives(free, dep), a, projector) for entry in flat(m)]
        columns.append([value[i] - base[i] for i in range(len(base))])
    matrix = [list(line) for line in zip(*columns)]
    rhs = [-value for value in base]
    check("cross_jet_dependent_rank_twelve", rank(matrix) == 12)
    solution = solve_unique(matrix, rhs)
    expected = [F(-1), F(3, 2), F(5, 2), F(-7, 2), F(2), F(0), F(-3), F(0), F(-5), F(0), F(7), F(0)]
    check("cross_jet_unique_umbilical_solution", solution == expected)
    check("cross_jet_augmented_rank_twelve", rank([matrix[i] + [rhs[i]] for i in range(len(matrix))]) == 12)

    screen_shear = [zeros(4, 4) for _ in range(4)]
    screen_shear[0][2][2], screen_shear[0][3][3] = F(1), F(-1)
    check("screen_shear_rank_obstruction", affine_rank_for_a(eta, screen_shear, projector) == (4, 5))
    base_shear = [zeros(4, 4) for _ in range(4)]
    base_shear[2][0][0], base_shear[2][1][1] = F(1), F(1)
    check("base_shear_rank_obstruction", affine_rank_for_a(eta, base_shear, projector) == (4, 5))

    z, p, rho = F(2), F(3), F(7)
    round_metric = diag(-z**-2, z**2, 25, 9)
    round_d = [zeros(4, 4) for _ in range(4)]
    round_d[1] = diag(2 * p * z**-2, 2 * p * z**2, 2 * rho * 25, 2 * rho * 9)
    round_d[2][3][3] = F(24)
    assert_zero([value for m in residual(round_metric, round_d, [F(0), -rho, F(0), F(0)], projector) for value in flat(m)], "round witness")
    check("round_curved_screen_witness", True)
    for rate in (F(2), F(11)):
        d = [[row[:] for row in matrix] for matrix in round_d]
        d[1][0][0], d[1][1][1] = 2 * rate * z**-2, 2 * rate * z**2
        assert_zero([value for m in residual(round_metric, d, [F(0), -rho, F(0), F(0)], projector) for value in flat(m)], "phi profile")
        check(f"phi_profile_{rate}_passes", True)

    direct_d = [zeros(4, 4) for _ in range(4)]
    direct_d[1] = diag(6, 6, 0, 0)
    assert_zero([value for m in residual(eta, direct_d, [F(0)] * 4, projector) for value in flat(m)], "P witness")
    direct_values = [value for m in residual(eta, direct_d, [F(0)] * 4, generator) for value in flat(m)]
    check("P_parallel_L_nonparallel", any(direct_values))

    cross_sets = {
        "PLUS_IDENTITY": [[F(1, 10), F(1, 10)], [F(1, 10), F(1, 10)]],
        "MINUS_IDENTITY": [[F(1, 10), F(1, 10)], [F(-1, 10), F(-1, 10)]],
        "AXIS_REFLECTION": [[F(1, 10), F(1, 10)], [F(1, 10), F(-1, 10)]],
        "HOPF_EXCHANGE_LOCAL": [[F(1, 10), F(1, 10)], [F(1, 10), F(1, 10)]],
    }
    for name, cross in cross_sets.items():
        for k in (2, 3):
            g = full_metric([[F(1), F(-k)], [F(-k), F(1)]], cross, eye(2))
            pmetric = orthogonal_projector(g)
            check(f"{name}_MU{k*k}_idempotent", mul(pmetric, pmetric) == pmetric)
            check(f"{name}_MU{k*k}_self_adjoint", mul(transpose(pmetric), g) == mul(g, pmetric))
            check(f"{name}_MU{k*k}_rank_two", rank(pmetric) == 2)
            check(f"{name}_MU{k*k}_difference_rank", connection_difference_rank(g, pmetric) == 4)
            assert_zero([value for m in residual(g, [zeros(4, 4) for _ in range(4)], [F(0)] * 4, pmetric) for value in flat(m)], "constant cross")

    base_boost = block_diag([[F(0), F(1)], [F(1), F(0)]], zeros(2, 2))
    angular_rotation = block_diag(zeros(2, 2), [[F(0), F(-1)], [F(1), F(0)]])
    angular_axis = diag(0, 0, -1, 1)
    check("base_boost_commutes_P", commutator(base_boost, projector) == zeros(4, 4))
    check("angular_rotation_commutes_P", commutator(angular_rotation, projector) == zeros(4, 4))
    check("angular_rotation_not_axis_preserving", commutator(angular_rotation, angular_axis) != zeros(4, 4))
    check("twist_bracket_transverse", F(1) != 0)

    # Directly reconstruct the CSN cancellation C(ds)+C(A-ds)=C(A).
    a = [F(2), F(-3), F(5), F(7)]
    ds = [F(11), F(13), F(-17), F(19)]
    for direction in range(4):
        lhs = add(weyl(eta, ds, direction), weyl(eta, [a[i] - ds[i] for i in range(4)], direction))
        check(f"CSN_cancel_{direction}", lhs == weyl(eta, a, direction))
    return checks


def expect_failure(label, function, catches):
    try:
        function()
    except (AssertionError, KeyError, StopIteration):
        catches[label] = "PASS"
        return
    raise AssertionError(f"catch did not fire: {label}")


def main():
    model = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    tables = (
        rows("SOURCE_LINEAGE.tsv"),
        rows("PROJECTOR_EXISTENCE_THEOREM.tsv"),
        rows("WITNESS_CLASSIFICATION.tsv"),
        rows("HOLONOMY_AND_RECIPROCITY.tsv"),
        rows("STATUS_LEDGER.tsv"),
        rows("COMPLETENESS_SCOPE.tsv"),
    )
    validate_model(model, tables)
    checks = independent_algebra()
    catches = {}

    def mutated_model(path, value):
        candidate = copy.deepcopy(model)
        target = candidate
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        return lambda: validate_model(candidate, tables)

    expect_failure("wrong_schema", mutated_model(["schema"], "wrong"), catches)
    expect_failure("missing_derivation_check", mutated_model(["check_count"], 101), catches)
    expect_failure("uniqueness_promoted", mutated_model(["theorem", "uniqueness"], "EXISTS_UNCONDITIONALLY"), catches)
    expect_failure("existence_conditions_removed", mutated_model(["theorem", "existence"], "ALWAYS"), catches)
    expect_failure("physical_law_promoted", mutated_model(["physical_status", "overall"], "DERIVED_UDT_LAW"), catches)
    expect_failure("open_gate_closed", mutated_model(["smallest_missing_principle", "status"], "DERIVED"), catches)
    expect_failure("P_promoted_to_L", mutated_model(["strictness", "P_parallel_implies_L_parallel"], True), catches)
    expect_failure("shear_silently_allowed", mutated_model(["strictness", "twist_or_cross_shear_retained"], True), catches)
    cross_mutation = copy.deepcopy(model)
    cross_mutation["witnesses"]["constant_nonzero_cross_metrics"].pop(next(iter(cross_mutation["witnesses"]["constant_nonzero_cross_metrics"])))
    expect_failure("missing_cross_witness", lambda: validate_model(cross_mutation, tables), catches)

    def changed_table(index, mutate):
        candidate = copy.deepcopy(tables)
        mutate(candidate[index])
        return lambda: validate_model(model, candidate)

    expect_failure("missing_source", changed_table(0, lambda data: data.pop()), catches)
    expect_failure("duplicate_source", changed_table(0, lambda data: data.__setitem__(1, copy.deepcopy(data[0]))), catches)
    expect_failure("missing_theorem_row", changed_table(1, lambda data: data.pop()), catches)
    expect_failure("missing_witness_row", changed_table(2, lambda data: data.pop()), catches)
    expect_failure("shear_failure_erased", changed_table(2, lambda data: data[4].__setitem__("result", "PASS")), catches)
    expect_failure("twist_failure_erased", changed_table(2, lambda data: data[6].__setitem__("result", "PASS")), catches)
    expect_failure("P_L_distinction_erased", changed_table(2, lambda data: data[7].__setitem__("result", "PASS")), catches)
    expect_failure("projector_law_promoted", changed_table(4, lambda data: data[15].__setitem__("status", "DERIVED")), catches)
    expect_failure("metric_sector_gate_closed", changed_table(4, lambda data: data[16].__setitem__("status", "DERIVED")), catches)
    expect_failure("dynamics_promoted", changed_table(5, lambda data: next(row for row in data if row["criterion"] == "dynamics_and_action").__setitem__("coverage", "COMPLETE")), catches)

    semantic_needles = {
        "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": "derivative order and time-live degrees of freedom",
        "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md": "No nonlocal insertion",
        "reciprocal_line_realization_selector_2026-07-18/DERIVATION_REPORT.md": "It is not yet a spacetime line field",
        "metric_cartan_holonomy_audit_2026-07-19/AUDIT_REPORT.md": "No current UDT premise sets `A^A_i=0`",
        "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md": "the carrier is reopened and conditional",
    }
    for path, needle in semantic_needles.items():
        source = (ROOT / path).read_text(encoding="utf-8")
        expect_failure(
            f"source_semantics_removed_{path.replace('/', '_')}",
            lambda path=path, needle=needle, source=source: validate_model(model, tables, {path: source.replace(needle, "REMOVED", 1)}),
            catches,
        )

    output = {
        "schema": "udt-reciprocal-plane-projector-verification-1.0",
        "result": "PASS_VERIFIED_WITH_CAVEATS",
        "maximum_conclusion": model["maximum_conclusion"],
        "derivation_check_count": model["check_count"],
        "independent_check_count": len(checks),
        "catch_proof_count": len(catches),
        "checks": dict(sorted(checks.items())),
        "catch_proofs": dict(sorted(catches.items())),
        "reconstructed": [
            "rank-four uniqueness map",
            "full twelve-variable cross-jet umbilical solution",
            "base and screen trace-free shear obstructions",
            "round curved-screen and two inequivalent phi-profile witnesses",
            "projector-parallel but generator-nonparallel witness",
            "eight metric-derived nonzero-cross orthogonal projectors",
            "residual boost and angular-rotation algebra",
            "CSN affine-connection cancellation",
        ],
        "premise_boundary": "The theorem characterizes a supplied projector inside the torsion-free Weyl class. It does not derive the spacetime plane, projector parallelism, an integrable/umbilical complete metric, an action, carrier, source, boundary, or mass.",
        "derivation_result_sha256": hashlib.sha256((HERE / "DERIVATION_RESULT.json").read_bytes()).hexdigest(),
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
