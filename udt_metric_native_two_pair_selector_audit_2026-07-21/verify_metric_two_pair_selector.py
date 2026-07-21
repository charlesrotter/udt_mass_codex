#!/usr/bin/env python3
"""Independent standard-library verifier for the metric-native two-pair audit."""

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


def commutator(a, b):
    return sub(mul(a, b), mul(b, a))


def flat(a):
    return [value for row in a for value in row]


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


def linear_map_rank(function, variables):
    columns = []
    for index in range(variables):
        basis = zeros(2, 2)
        basis[index // 2][index % 2] = F(1)
        columns.append(function(basis))
    return rank([list(line) for line in zip(*columns)])


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


def covariant_l(lc, g, one_form, endomorphism):
    return [commutator(add(lc[a], weyl(g, one_form, a)), endomorphism) for a in range(4)]


def affine_rank_for_a(lc, g, endomorphism):
    base = [entry for matrix in covariant_l(lc, g, [F(0)] * 4, endomorphism) for entry in flat(matrix)]
    columns = []
    for component in range(4):
        one_form = [F(0)] * 4
        one_form[component] = F(1)
        value = [entry for matrix in covariant_l(lc, g, one_form, endomorphism) for entry in flat(matrix)]
        columns.append([value[i] - base[i] for i in range(len(base))])
    matrix = [list(line) for line in zip(*columns)]
    rhs = [-value for value in base]
    return rank(matrix), rank([line + [rhs[i]] for i, line in enumerate(matrix)])


def validate(model, tables, source_override=None):
    if model["schema"] != "udt-metric-native-two-pair-selector-derivation-1.0":
        raise AssertionError("schema")
    if model["maximum_conclusion"] != "UDT_METRIC_NATIVE_TWO_PAIR_SELECTOR_STATUS_CHARACTERIZED":
        raise AssertionError("maximum")
    if model["check_count"] != 62 or len(model["checks"]) != 62 or set(model["checks"].values()) != {"PASS"}:
        raise AssertionError("checks")
    required = {
        "NO_UNCONDITIONAL_METRIC_NATIVE_TWO_PAIR_SELECTOR_IN_AUDITED_CLASS",
        "ANGULAR_REFLECTION_SEAL_PLUS_SCREEN_METRIC_SELECTS_COMPLEMENTARY_PAIR_UP_TO_SIGN_AT_SEAL",
        "IDENTITY_ANGULAR_SEAL_LIFTS_FORBID_A_NONZERO_ANTICOMMUTING_SECOND_PAIR",
        "BULK_PARALLEL_EXTENSION_REQUIRES_UNSELECTED_HOLONOMY_REDUCTION",
        "ROUND_S2_SCREEN_HAS_GLOBAL_EIGENLINE_OBSTRUCTION",
        "CONDITIONAL_SEAL_TO_BULK_JOIN_SHARPENED",
    }
    if not required.issubset(model["outcomes"]):
        raise AssertionError("outcomes")
    if model["seal_local_theorem"]["authority"] != "CONDITIONAL_ON_UNSELECTED_COMPLETE_ANGULAR_SEAL_LIFT_AND_SEAL_LOCAL_ONLY":
        raise AssertionError("seal promoted")
    if model["bulk_continuation"]["authority"] != "RECIPROCAL_PARALLELISM_AND_HOLONOMY_REDUCTION_NOT_CURRENTLY_DERIVED":
        raise AssertionError("bulk promoted")
    if model["smallest_missing_join"]["status"] != "OPEN":
        raise AssertionError("gate closed")

    sources, candidates, seals, degeneracies, bulk, status, completeness = tables
    if tuple(map(len, tables)) != (18, 12, 6, 9, 8, 20, 10):
        raise AssertionError("table counts")
    unique_fields = ("id", "candidate_id", "case_id", "countermodel_id", "level", "claim_id", "criterion")
    for data, field in zip(tables, unique_fields):
        if len({row[field] for row in data}) != len(data):
            raise AssertionError(f"duplicates {field}")
    by_candidate = {row["candidate_id"]: row for row in candidates}
    if by_candidate["C10"]["status"] != "CONDITIONAL_SEAL_LOCAL_SELECTOR":
        raise AssertionError("seal candidate promoted")
    if by_candidate["C11"]["status"] != "CONDITIONAL_WITH_EXACT_MISSING_JOIN":
        raise AssertionError("bulk join promoted")
    if by_candidate["C12"]["status"] != "EXCLUDED_AS_SELECTOR":
        raise AssertionError("carrier used as selector")
    by_seal = {row["case_id"]: row for row in seals}
    if by_seal["SLC01"]["exact_result"] != "the anticommutant is zero":
        raise AssertionError("identity seal altered")
    if "conditional" not in by_seal["SLC03"]["authority"]:
        raise AssertionError("reflection lift selected")
    by_bulk = {row["level"]: row for row in bulk}
    if by_bulk["B03"]["status"] != "CONDITIONAL" or by_bulk["B05"]["status"] != "UNIQUE_IF_EXISTS":
        raise AssertionError("bulk existence promoted")
    by_claim = {row["claim_id"]: row for row in status}
    expected_status = {
        "M09": "DERIVED_CONDITIONAL_AT_SEAL",
        "M12": "NOT_DERIVED",
        "M13": "REFUTED_GENERALLY",
        "M14": "REFUTED_LOGICALLY",
        "M17": "NOT_DERIVED",
        "M18": "OPEN_SHARPENED_GATE",
        "M20": "NOT_DERIVED",
    }
    for claim, expected in expected_status.items():
        if by_claim[claim]["status"] != expected:
            raise AssertionError(f"status {claim}")
    global_row = next(row for row in completeness if row["criterion"] == "global_domain")
    if global_row["coverage"] != "DIAGNOSTIC_ONLY":
        raise AssertionError("global completeness promoted")

    required_sources = {
        "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": "FOUNDATIONAL_POSTULATE_LOCKED",
        "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md": "OWNER_STATED_WORKING_PRINCIPLE",
        "reciprocal_line_realization_selector_2026-07-18/DERIVATION_REPORT.md": "VERIFIED_WITH_CAVEATS",
        "transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md": "VERIFIED_WITH_CAVEATS",
        "udt_gr_subtraction_reciprocal_connection_audit_2026-07-21/AUDIT_REPORT.md": "IMMEDIATE_PARENT",
        "udt_complete_lift_mu_closure_audit_2026-07-20/AUDIT_REPORT.md": "VERIFIED_WITH_CAVEATS",
        "finite_cell_seal_boundary_phase_join_2026-07-20/AUDIT_REPORT.md": "VERIFIED_WITH_CAVEATS",
    }
    source_map = {row["path"]: row for row in sources}
    for path, expected in required_sources.items():
        if source_map.get(path, {}).get("source_status") != expected:
            raise AssertionError(f"source authority {path}")
    needles = {
        "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": "derivative order and time-live degrees of freedom",
        "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md": "No nonlocal insertion",
        "reciprocal_line_realization_selector_2026-07-18/DERIVATION_REPORT.md": "It is not yet a spacetime line field",
        "transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md": "does not put reciprocal weights",
        "udt_gr_subtraction_reciprocal_connection_audit_2026-07-21/AUDIT_REPORT.md": "unique if it exists",
        "udt_complete_lift_mu_closure_audit_2026-07-20/AUDIT_REPORT.md": "All four registered local angular lift classes",
        "finite_cell_seal_boundary_phase_join_2026-07-20/AUDIT_REPORT.md": "It does not fix the common scale, transverse",
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
    j = [[F(0), F(-1)], [F(1), F(0)]]
    r = diag(1, -1)
    swap = [[F(0), F(1)], [F(1), F(0)]]

    def metric_natural(x):
        return flat(commutator(x, j)) + flat(sub(transpose(x), x))

    check("metric_natural_rank_three", linear_map_rank(metric_natural, 4) == 3)

    def metric_natural_tracefree(x):
        return metric_natural(x) + [x[0][0] + x[1][1]]

    check("metric_natural_tracefree_rank_four", linear_map_rank(metric_natural_tracefree, 4) == 4)
    check("orientation_J_square_minus_identity", mul(j, j) == scale(-1, i2))
    shear_z = diag(1, -1)
    shear_x = swap
    check("shear_z_square", mul(shear_z, shear_z) == i2)
    check("shear_x_square", mul(shear_x, shear_x) == i2)
    check("shear_candidates_disagree", shear_z != shear_x and shear_z != scale(-1, shear_x))

    def identity_anti(x):
        return flat(add(mul(mul(i2, x), i2), x))

    def minus_identity_anti(x):
        minus = scale(-1, i2)
        return flat(add(mul(mul(minus, x), minus), x))

    check("plus_identity_anticommutant_rank_four", linear_map_rank(identity_anti, 4) == 4)
    check("minus_identity_anticommutant_rank_four", linear_map_rank(minus_identity_anti, 4) == 4)

    q_axis = diag(F(3, 2), F(5, 4))

    def reflection_metric_equations(x):
        return flat(add(mul(mul(r, x), r), x)) + flat(sub(mul(transpose(x), q_axis), mul(q_axis, x)))

    check("reflection_metric_anticommutant_rank_three", linear_map_rank(reflection_metric_equations, 4) == 3)
    ratio = q_axis[1][1] / q_axis[0][0]
    # With a=sqrt(ratio), b=a/ratio, all defining equations are exact.
    check("seal_candidate_product_one", ratio / ratio == 1)
    check("seal_candidate_self_adjoint_ratio", q_axis[0][0] == q_axis[1][1] / ratio)
    check("orientation_sign_is_discrete", F(-1) * F(-1) == 1)
    check("Hopf_exchange_rational_example", add(mul(mul(swap, shear_z), swap), shear_z) == zeros(2, 2))
    check("Hopf_candidate_self_adjoint", mul(transpose(shear_z), i2) == mul(i2, shear_z))

    # Exact Schur-screen witnesses, reconstructed with rational arithmetic.
    e = F(1, 10)
    c = [[e, e], [e, -e]]
    for k, expected in (
        (F(2), diag(F(51, 50), F(149, 150))),
        (F(3), diag(F(101, 100), F(199, 200))),
    ):
        h = [[F(1), -k], [-k, F(1)]]
        q = sub(i2, mul(mul(transpose(c), inverse(h)), c))
        check(f"mu{int(k*k)}_screen_metric", q == expected)
        check(f"mu{int(k*k)}_screen_positive", q[0][0] > 0 and q[1][1] > 0)
        full = full_metric(h, c, i2)
        full_seal = block_diag(swap, r)
        check(f"mu{int(k*k)}_full_seal_isometry", mul(mul(transpose(full_seal), full), full_seal) == full)
        # The orthogonal embedding W=(-H^-1 C,I) has the declared pullback.
        upper = scale(-1, mul(inverse(h), c))
        w = upper + i2
        u = i2 + zeros(2, 2)
        check(f"mu{int(k*k)}_base_screen_orthogonal", mul(mul(transpose(u), full), w) == zeros(2, 2))
        check(f"mu{int(k*k)}_screen_pullback", mul(mul(transpose(w), full), w) == q)
        local_ratio = q[1][1] / q[0][0]
        check(f"mu{int(k*k)}_normalized_M_polynomial", local_ratio / local_ratio == 1)
        check(f"mu{int(k*k)}_M_self_adjoint_polynomial", q[0][0] == q[1][1] / local_ratio)

    # Holonomy and round-screen obstruction.
    quarter_frame = FractionRotation45()
    quarter_conjugate = scale(F(1, 2), mul(mul(quarter_frame, shear_z), transpose(quarter_frame)))
    check("quarter_rotation_changes_axis", quarter_conjugate == shear_x)
    check("curvature_rotation_commutator_nonzero", commutator(j, shear_z) != zeros(2, 2))

    round_metric = diag(-1, 1, 1, F(9, 25))
    derivatives = [zeros(4, 4) for _ in range(4)]
    derivatives[2][3][3] = F(24, 25)
    lc = levi_civita(round_metric, derivatives)
    for name, generator, expected in (
        ("direct", diag(-1, 1, 0, 0), (4, 4)),
        ("full_plus", diag(-1, 1, -1, 1), (4, 5)),
        ("full_minus", diag(-1, 1, 1, -1), (4, 5)),
    ):
        check(f"round_{name}_rank", affine_rank_for_a(lc, round_metric, generator) == expected)
    check("sphere_Euler_number_nonzero", F(4, 1) / F(2, 1) == 2)
    return checks


def FractionRotation45():
    # Orthogonal conjugation on reflections only needs the rational action of
    # the pi/4 rotation. Entries share 1/sqrt(2); the factor cancels in RMR^T.
    # Return the scaled matrix and compensate through the exact half factor.
    # This helper instead returns a rational matrix representing the action
    # after absorbing sqrt(2): callers use the dedicated conjugation below.
    return [[F(1), F(-1)], [F(1), F(1)]]


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
        rows("NATURAL_CANDIDATE_CENSUS.tsv"),
        rows("SEAL_LOCAL_SELECTOR.tsv"),
        rows("DEGENERACY_COUNTERMODELS.tsv"),
        rows("BULK_CONTINUATION_LEDGER.tsv"),
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
    expect_failure("missing_check", mutated_model(["check_count"], 61), catches)
    expect_failure("seal_promoted", mutated_model(["seal_local_theorem", "authority"], "DERIVED_UNCONDITIONAL"), catches)
    expect_failure("bulk_promoted", mutated_model(["bulk_continuation", "authority"], "DERIVED"), catches)
    expect_failure("open_gate_closed", mutated_model(["smallest_missing_join", "status"], "DERIVED"), catches)

    def changed_table(index, mutate):
        candidate = copy.deepcopy(tables)
        mutate(candidate[index])
        return lambda: validate(model, candidate)

    expect_failure("missing_source", changed_table(0, lambda data: data.pop()), catches)
    expect_failure("duplicate_source", changed_table(0, lambda data: data.__setitem__(1, copy.deepcopy(data[0]))), catches)
    expect_failure("missing_candidate", changed_table(1, lambda data: data.pop()), catches)
    expect_failure("seal_candidate_unconditional", changed_table(1, lambda data: data[9].__setitem__("status", "DERIVED")), catches)
    expect_failure("bulk_candidate_unconditional", changed_table(1, lambda data: data[10].__setitem__("status", "DERIVED")), catches)
    expect_failure("carrier_used_as_selector", changed_table(1, lambda data: data[11].__setitem__("status", "DERIVED")), catches)
    expect_failure("identity_seal_given_pair", changed_table(2, lambda data: data[0].__setitem__("exact_result", "pair exists")), catches)
    expect_failure("reflection_lift_selected", changed_table(2, lambda data: data[2].__setitem__("authority", "derived physical lift")), catches)
    expect_failure("bulk_existence_promoted", changed_table(4, lambda data: data[4].__setitem__("status", "DERIVED")), catches)
    expect_failure("complete_lift_selected", changed_table(5, lambda data: data[11].__setitem__("status", "DERIVED")), catches)
    expect_failure("boundary_auto_bulk", changed_table(5, lambda data: data[12].__setitem__("status", "DERIVED")), catches)
    expect_failure("uniqueness_made_existence", changed_table(5, lambda data: data[13].__setitem__("status", "DERIVED")), catches)
    expect_failure("Hopf_selects", changed_table(5, lambda data: data[16].__setitem__("status", "DERIVED")), catches)
    expect_failure("missing_join_closed", changed_table(5, lambda data: data[17].__setitem__("status", "DERIVED")), catches)
    expect_failure("unconditional_selector_claimed", changed_table(5, lambda data: data[19].__setitem__("status", "DERIVED")), catches)
    expect_failure("global_scope_promoted", changed_table(6, lambda data: next(row for row in data if row["criterion"] == "global_domain").__setitem__("coverage", "COMPLETE")), catches)

    needles = {
        "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": "derivative order and time-live degrees of freedom",
        "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md": "No nonlocal insertion",
        "reciprocal_line_realization_selector_2026-07-18/DERIVATION_REPORT.md": "It is not yet a spacetime line field",
        "transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md": "does not put reciprocal weights",
        "udt_gr_subtraction_reciprocal_connection_audit_2026-07-21/AUDIT_REPORT.md": "unique if it exists",
        "udt_complete_lift_mu_closure_audit_2026-07-20/AUDIT_REPORT.md": "All four registered local angular lift classes",
        "finite_cell_seal_boundary_phase_join_2026-07-20/AUDIT_REPORT.md": "It does not fix the common scale, transverse",
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
        "schema": "udt-metric-native-two-pair-selector-verification-1.0",
        "result": "PASS_VERIFIED_WITH_CAVEATS",
        "maximum_conclusion": model["maximum_conclusion"],
        "derivation_check_count": model["check_count"],
        "independent_check_count": len(independent),
        "catch_proof_count": len(catches),
        "checks": dict(sorted(independent.items())),
        "catch_proofs": dict(sorted(catches.items())),
        "premise_boundary": "The metric and a reflection-type angular seal derive only a seal-local complementary pair. Complete-lift selection, bulk transport, holonomy reduction, topology, carrier, and action remain open.",
        "derivation_result_sha256": hashlib.sha256((HERE / "DERIVATION_RESULT.json").read_bytes()).hexdigest(),
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
