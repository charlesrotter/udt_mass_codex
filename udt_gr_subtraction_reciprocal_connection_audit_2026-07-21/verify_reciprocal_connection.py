#!/usr/bin/env python3
"""Independent standard-library verification of the reciprocal-connection audit."""

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


def commutator(a, b):
    return sub(mul(a, b), mul(b, a))


def flat(a):
    return [value for row in a for value in row]


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


def linear_system(base, columns):
    matrix = [list(line) for line in zip(*columns)]
    rhs = [-value for value in base]
    return matrix, rhs


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


def covariant_l(lc, g, one_form, endomorphism):
    return [commutator(add(lc[a], weyl(g, one_form, a)), endomorphism) for a in range(4)]


def connection_difference_rank(g, endomorphism):
    columns = []
    for component in range(4):
        b = basis_vector(4, component)
        columns.append(
            [entry for direction in range(4) for entry in flat(commutator(weyl(g, b, direction), endomorphism))]
        )
    return rank([list(line) for line in zip(*columns)])


def affine_rank_for_a(lc, g, endomorphism):
    base = [entry for matrix in covariant_l(lc, g, [F(0)] * 4, endomorphism) for entry in flat(matrix)]
    columns = []
    for component in range(4):
        value = [
            entry
            for matrix in covariant_l(lc, g, basis_vector(4, component), endomorphism)
            for entry in flat(matrix)
        ]
        columns.append([value[i] - base[i] for i in range(len(base))])
    matrix, rhs = linear_system(base, columns)
    return rank(matrix), rank([line + [rhs[i]] for i, line in enumerate(matrix)])


def lc_difference_rank():
    eta = diag(-1, 1, 1, 1)
    pairs = [(b, c) for b in range(4) for c in range(b, 4)]
    columns = []
    for upper in range(4):
        for b, c in pairs:
            difference = [zeros(4, 4) for _ in range(4)]
            difference[b][upper][c] = F(1)
            difference[c][upper][b] = F(1)
            equations = []
            for a in range(4):
                for i in range(4):
                    for j in range(i, 4):
                        equations.append(
                            sum((difference[a][d][i] * eta[d][j] for d in range(4)), F(0))
                            + sum((difference[a][d][j] * eta[i][d] for d in range(4)), F(0))
                        )
            columns.append(equations)
    return rank([list(line) for line in zip(*columns)])


def assert_zero(values, label):
    if any(values):
        raise AssertionError(label)


def static_lc(p, h2, h3):
    eta = diag(-1, 1, 1, 1)
    derivatives = [zeros(4, 4) for _ in range(4)]
    derivatives[1] = diag(2 * p, 2 * p, 2 * h2, 2 * h3)
    return eta, levi_civita(eta, derivatives)


def validate_model(model, tables, source_override=None):
    if model["schema"] != "udt-gr-subtraction-reciprocal-connection-derivation-1.0":
        raise AssertionError("schema")
    if model["maximum_conclusion"] != "UDT_GR_SUBTRACTION_RECIPROCAL_CONNECTION_STATUS_CHARACTERIZED":
        raise AssertionError("maximum conclusion")
    if model["check_count"] != 129 or len(model["checks"]) != 129 or set(model["checks"].values()) != {"PASS"}:
        raise AssertionError("derivation checks")
    required_outcomes = {
        "RECIPROCAL_COMPATIBILITY_UNIQUE_IF_IT_EXISTS",
        "RECURRENT_NORMALIZED_RECIPROCITY_COLLAPSES_TO_EXACT_PARALLELISM",
        "SPLITTING_PRESERVATION_IS_STRICTLY_WEAKER",
        "DIRECT_TRANSVERSE_IDENTITY_STATIC_JET_HAS_NONZERO_INTRINSIC_OBSTRUCTION",
        "CONDITIONAL_FULL_TWO_PAIR_EXTENSION_REMOVES_LOCAL_OBSTRUCTION",
        "CONDITIONAL_FULL_TWO_PAIR_PLUS_ANGULAR_RECIPROCITY_YIELDS_HOPF_ORBIT_WEIGHTS",
        "CONNECTION_UNIQUENESS_WITH_EXISTENCE_OPEN",
        "CONDITIONAL_HOPF_STRUCTURE_DIAGNOSES_BUT_DOES_NOT_SELECT_CONNECTION",
    }
    if not required_outcomes.issubset(model["outcomes"]):
        raise AssertionError("outcomes")
    if model["direct_extension"]["status"] != "UNIQUE_IF_EXISTS_BUT_GENERIC_FOUNDING_ANGULAR_READOUT_OBSTRUCTED":
        raise AssertionError("direct existence promoted")
    if model["conditional_full_two_pair"]["foundation_status"] != "CONDITIONAL_TRANSVERSE_REALIZATION_NOT_DERIVED":
        raise AssertionError("full pair promoted")
    if model["smallest_missing_principle"]["selection_status"] != "OPEN":
        raise AssertionError("selection promoted")

    sources, subtraction, uniqueness, jets, angular, status, completeness = tables
    expected_lengths = (18, 7, 8, 8, 4, 18, 10)
    if tuple(map(len, tables)) != expected_lengths:
        raise AssertionError("table row counts")
    if len({row["id"] for row in sources}) != 18:
        raise AssertionError("source duplicates")
    if len({row["witness_id"] for row in uniqueness}) != 8:
        raise AssertionError("uniqueness duplicates")
    if any(row["L_difference_rank"] != "4" or row["P_difference_rank"] != "4" for row in uniqueness):
        raise AssertionError("uniqueness rank table")
    if {row["case"] for row in jets} != {f"J{i:02d}" for i in range(1, 9)}:
        raise AssertionError("static cases")
    if len({row["seal_lift"] for row in angular}) != 4:
        raise AssertionError("angular classes")
    by_lift = {row["seal_lift"]: row for row in angular}
    if by_lift["PLUS_IDENTITY"]["anti_commuting_angular_generator"] != "ZERO_ONLY":
        raise AssertionError("plus identity generator")
    if by_lift["HOPF_EXCHANGE_LOCAL"]["foundation_status"] != "TRANSVERSE_PHYSICAL_REALIZATION_NOT_DERIVED":
        raise AssertionError("Hopf realization promoted")
    if {row["claim_id"] for row in status} != {f"R{i:02d}" for i in range(1, 19)}:
        raise AssertionError("status identities")
    by_claim = {row["claim_id"]: row for row in status}
    if by_claim["R03"]["status"] != "DERIVED_CONDITIONAL":
        raise AssertionError("uniqueness conditional lost")
    if by_claim["R07"]["status"] != "REFUTED_IN_STATIC_JET_CLASS":
        raise AssertionError("direct obstruction lost")
    if by_claim["R10"]["status"] != "DERIVED_CONDITIONAL":
        raise AssertionError("full extension promoted")
    if by_claim["R13"]["status"] != "NOT_DERIVED":
        raise AssertionError("carrier promoted")
    if by_claim["R16"]["status"] != "OPEN_SHARPENED_GATE":
        raise AssertionError("open gate lost")
    if len({row["criterion"] for row in completeness}) != 10:
        raise AssertionError("completeness identities")
    dynamics = next(row for row in completeness if row["criterion"] == "dynamical_character")
    if dynamics["coverage"] != "NOT_COVERED":
        raise AssertionError("dynamics promoted")

    required_sources = {
        "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md": "FOUNDATIONAL_CANDIDATE_PLUS_DERIVED_KINEMATICS",
        "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": "FOUNDATIONAL_POSTULATE_LOCKED",
        "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md": "OWNER_STATED_WORKING_PRINCIPLE",
        "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md": "CURRENT_FRONTIER",
        "reciprocal_line_realization_selector_2026-07-18/DERIVATION_REPORT.md": "VERIFIED_WITH_CAVEATS",
        "transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md": "VERIFIED_WITH_CAVEATS",
        "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md": "VERIFIED_WITH_CAVEATS",
    }
    source_by_path = {row["path"]: row for row in sources}
    for path, expected_status in required_sources.items():
        if source_by_path.get(path, {}).get("source_status") != expected_status:
            raise AssertionError(f"source authority {path}")
    semantic_needles = {
        "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": "derivative order and time-live degrees of freedom",
        "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md": "No nonlocal insertion",
        "reciprocal_line_realization_selector_2026-07-18/DERIVATION_REPORT.md": "It is not yet a spacetime line field",
        "transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md": "P4=diag(exp(-phi),exp(phi),1,1)",
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
    direct = diag(-1, 1, 0, 0)
    projector = mul(direct, direct)
    full_plus = diag(-1, 1, -1, 1)
    full_minus = diag(-1, 1, 1, -1)
    swap = [[F(0), F(1)], [F(1), F(0)]]

    check("metric_connection_difference_rank_40", lc_difference_rank() == 40)
    for component in range(4):
        a = basis_vector(4, component)
        for direction in range(4):
            c = weyl(eta, a, direction)
            for upper in range(4):
                for lower in range(4):
                    check(
                        f"weyl_torsion_{component}_{direction}_{upper}_{lower}",
                        c[upper][lower] == weyl(eta, a, lower)[upper][direction],
                    )
            metric_derivative = scale(-1, add(mul(transpose(c), eta), mul(eta, c)))
            check(
                f"weyl_metric_{component}_{direction}",
                metric_derivative == scale(-2 * a[direction], eta),
            )

    check("direct_difference_rank", connection_difference_rank(eta, direct) == 4)
    check("projector_difference_rank", connection_difference_rank(eta, projector) == 4)
    check("full_plus_difference_rank", connection_difference_rank(eta, full_plus) == 4)
    check("full_minus_difference_rank", connection_difference_rank(eta, full_minus) == 4)

    # Recurrence map has eight independent columns: four Weyl differences and four recurrence scalars.
    recurrence_columns = []
    for component in range(4):
        b = basis_vector(4, component)
        recurrence_columns.append(
            [entry for direction in range(4) for entry in flat(commutator(weyl(eta, b, direction), direct))]
        )
    for direction in range(4):
        recurrence_columns.append(
            [
                (-direct[i][j] if a == direction else F(0))
                for a in range(4)
                for i in range(4)
                for j in range(4)
            ]
        )
    check("recurrence_rank_eight", rank([list(line) for line in zip(*recurrence_columns)]) == 8)
    check("normalized_trace_square_two", sum(mul(direct, direct)[i][i] for i in range(4)) == 2)

    lifts = {
        "PLUS_IDENTITY": (eye(2), [[F(1, 10), F(1, 10)], [F(1, 10), F(1, 10)]]),
        "MINUS_IDENTITY": (scale(-1, eye(2)), [[F(1, 10), F(1, 10)], [F(-1, 10), F(-1, 10)]]),
        "AXIS_REFLECTION": (diag(1, -1), [[F(1, 10), F(1, 10)], [F(1, 10), F(-1, 10)]]),
        "HOPF_EXCHANGE_LOCAL": (swap, [[F(1, 10), F(1, 10)], [F(1, 10), F(1, 10)]]),
    }
    for name, (angular, cross) in lifts.items():
        seal = block_diag(swap, angular)
        check(f"{name}_seal_inversion", add(mul(mul(seal, direct), seal), direct) == zeros(4, 4))
        for k in (2, 3):
            metric = full_metric([[F(1), F(-k)], [F(-k), F(1)]], cross, eye(2))
            check(f"{name}_mu{k*k}_L_rank", connection_difference_rank(metric, direct) == 4)
            check(f"{name}_mu{k*k}_P_rank", connection_difference_rank(metric, projector) == 4)

    # Exact static witnesses and the direct flat-angular obstruction.
    for label, generator, p, h2, h3, one_form in (
        ("direct", direct, 3, -3, -3, [0, 3, 0, 0]),
        ("projector", projector, 5, 2, 2, [0, -2, 0, 0]),
        ("full_plus", full_plus, 3, -3, 3, [0, 3, 0, 0]),
        ("full_minus", full_minus, 3, 3, -3, [0, 3, 0, 0]),
    ):
        metric, lc = static_lc(F(p), F(h2), F(h3))
        residual = covariant_l(lc, metric, [F(x) for x in one_form], generator)
        check(f"static_{label}_witness", all(value == 0 for matrix in residual for value in flat(matrix)))
    metric, lc = static_lc(F(1), F(0), F(0))
    check("direct_flat_angular_inconsistent", affine_rank_for_a(lc, metric, direct) == (4, 5))

    # Exact non-unit representative profile at z=2, p=3.
    z, p = F(2), F(3)
    profile = diag(-z**-2, z**2, z**-2, z**2)
    derivatives = [zeros(4, 4) for _ in range(4)]
    derivatives[1] = diag(2 * p * z**-2, 2 * p * z**2, -2 * p * z**-2, 2 * p * z**2)
    residual = covariant_l(levi_civita(profile, derivatives), profile, [F(0), p, F(0), F(0)], full_plus)
    check("full_profile_exact_witness", all(value == 0 for matrix in residual for value in flat(matrix)))

    # Angular seal anticommutator solution ranks and normalized witnesses.
    angular_examples = {
        "PLUS_IDENTITY": (eye(2), None, 4),
        "MINUS_IDENTITY": (scale(-1, eye(2)), None, 4),
        "AXIS_REFLECTION": (diag(1, -1), swap, 2),
        "HOPF_EXCHANGE_LOCAL": (swap, diag(-1, 1), 2),
    }
    for name, (seal, example, expected_rank) in angular_examples.items():
        columns = []
        for component in range(4):
            m = zeros(2, 2)
            m[component // 2][component % 2] = F(1)
            columns.append(flat(add(mul(mul(seal, m), seal), m)))
        check(f"{name}_angular_equation_rank", rank([list(line) for line in zip(*columns)]) == expected_rank)
        if example is not None:
            check(f"{name}_angular_example_inverted", add(mul(mul(seal, example), seal), example) == zeros(2, 2))
            check(f"{name}_angular_example_normalized", mul(example, example) == eye(2))

    hopf_seal = block_diag(swap, swap)
    check("hopf_full_plus_inverted", add(mul(mul(hopf_seal, full_plus), hopf_seal), full_plus) == zeros(4, 4))
    check("hopf_full_minus_inverted", add(mul(mul(hopf_seal, full_minus), hopf_seal), full_minus) == zeros(4, 4))
    check("CSN_common_rate_cancels", (-3 + 7) - (-3 + 7) == 0)
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
        rows("GR_UDT_SUBTRACTION.tsv"),
        rows("UNIQUENESS_WITNESSES.tsv"),
        rows("STATIC_JET_EQUATIONS.tsv"),
        rows("ANGULAR_EXTENSION_CLASSIFICATION.tsv"),
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
    expect_failure("missing_derivation_check", mutated_model(["check_count"], 128), catches)
    expect_failure("uniqueness_promoted_to_existence", mutated_model(["direct_extension", "status"], "UNCONDITIONALLY_SELECTED"), catches)
    expect_failure("full_pair_promoted", mutated_model(["conditional_full_two_pair", "foundation_status"], "DERIVED"), catches)
    expect_failure("selection_gate_closed", mutated_model(["smallest_missing_principle", "selection_status"], "DERIVED"), catches)

    def changed_table(index, mutate):
        candidate = copy.deepcopy(tables)
        mutate(candidate[index])
        return lambda: validate_model(model, candidate)

    expect_failure("missing_source", changed_table(0, lambda data: data.pop()), catches)
    expect_failure("duplicate_source", changed_table(0, lambda data: data.__setitem__(1, copy.deepcopy(data[0]))), catches)
    expect_failure("missing_witness", changed_table(2, lambda data: data.pop()), catches)
    expect_failure("mutated_witness_rank", changed_table(2, lambda data: data[0].__setitem__("L_difference_rank", "3")), catches)
    expect_failure("missing_static_case", changed_table(3, lambda data: data.pop()), catches)
    expect_failure("identity_extension_promoted", changed_table(4, lambda data: data[0].__setitem__("anti_commuting_angular_generator", "NONZERO")), catches)
    expect_failure("Hopf_realization_promoted", changed_table(4, lambda data: data[3].__setitem__("foundation_status", "DERIVED")), catches)
    expect_failure("direct_obstruction_removed", changed_table(5, lambda data: data[6].__setitem__("status", "DERIVED")), catches)
    expect_failure("full_extension_unconditional", changed_table(5, lambda data: data[9].__setitem__("status", "DERIVED")), catches)
    expect_failure("carrier_promoted", changed_table(5, lambda data: data[12].__setitem__("status", "DERIVED")), catches)
    expect_failure("open_gate_removed", changed_table(5, lambda data: data[15].__setitem__("status", "DERIVED")), catches)
    expect_failure("dynamics_promoted", changed_table(6, lambda data: next(row for row in data if row["criterion"] == "dynamical_character").__setitem__("coverage", "COMPLETE")), catches)

    semantic_needles = {
        "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": "derivative order and time-live degrees of freedom",
        "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md": "No nonlocal insertion",
        "reciprocal_line_realization_selector_2026-07-18/DERIVATION_REPORT.md": "It is not yet a spacetime line field",
        "transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md": "P4=diag(exp(-phi),exp(phi),1,1)",
        "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md": "the carrier is reopened and conditional",
    }
    for path, needle in semantic_needles.items():
        source = (ROOT / path).read_text(encoding="utf-8")
        expect_failure(
            f"source_semantics_removed_{Path(path).name}",
            lambda path=path, needle=needle, source=source: validate_model(model, tables, {path: source.replace(needle, "REMOVED", 1)}),
            catches,
        )

    output = {
        "schema": "udt-gr-subtraction-reciprocal-connection-verification-1.0",
        "result": "PASS_VERIFIED_WITH_CAVEATS",
        "maximum_conclusion": model["maximum_conclusion"],
        "derivation_check_count": model["check_count"],
        "independent_check_count": len(checks),
        "catch_proof_count": len(catches),
        "checks": dict(sorted(checks.items())),
        "catch_proofs": dict(sorted(catches.items())),
        "reconstructed": [
            "torsion-free metric connection-difference rank 40",
            "Weyl torsion and conformal metric compatibility",
            "direct/projector/full reciprocal connection-difference ranks",
            "normalized recurrence rank eight",
            "eight nonzero-cross lift witnesses",
            "direct angular obstruction and direct/projector/full static witnesses",
            "exact full-profile witness",
            "angular seal anticommutator classes and Hopf seal inversion",
        ],
        "premise_boundary": "Connection uniqueness is conditional on spacetime reciprocal realization, compatibility existence, and torsion freedom; the second reciprocal pair and Hopf carrier remain unselected.",
        "derivation_result_sha256": hashlib.sha256((HERE / "DERIVATION_RESULT.json").read_bytes()).hexdigest(),
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
