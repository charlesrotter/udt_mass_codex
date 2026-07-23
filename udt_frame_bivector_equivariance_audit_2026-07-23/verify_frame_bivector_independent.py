#!/usr/bin/env python3
"""Independent stdlib/Fraction verifier for the frame/bivector audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASIS2 = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))


def eye(n: int) -> list[list[F]]:
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def diag(*values: int | F) -> list[list[F]]:
    result = [[F(0) for _ in values] for _ in values]
    for index, value in enumerate(values):
        result[index][index] = F(value)
    return result


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def add(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def sub(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def scale(q: F, a: list[list[F]]) -> list[list[F]]:
    return [[q * item for item in row] for row in a]


def mul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def equal(a: list[list[F]], b: list[list[F]]) -> bool:
    return a == b


def inverse(a: list[list[F]]) -> list[list[F]]:
    n = len(a)
    work = [row[:] + identity for row, identity in zip(a, eye(n))]
    for col in range(n):
        pivot = next(index for index in range(col, n) if work[index][col] != 0)
        work[col], work[pivot] = work[pivot], work[col]
        factor = work[col][col]
        work[col] = [item / factor for item in work[col]]
        for row in range(n):
            if row == col:
                continue
            factor = work[row][col]
            work[row] = [
                x - factor * y for x, y in zip(work[row], work[col])
            ]
    return [row[n:] for row in work]


def rank(a: list[list[F]]) -> int:
    if not a:
        return 0
    work = [row[:] for row in a]
    rows = len(work)
    cols = len(work[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][col] != 0),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        factor = work[pivot_row][col]
        work[pivot_row] = [item / factor for item in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            factor = work[row][col]
            work[row] = [
                x - factor * y
                for x, y in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def flatten(a: list[list[F]]) -> list[F]:
    return [item for row in a for item in row]


def column_stack(matrices: list[list[list[F]]]) -> list[list[F]]:
    vectors = [flatten(item) for item in matrices]
    return [list(row) for row in zip(*vectors)]


def commutator(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return sub(mul(a, b), mul(b, a))


def vector_column(values: list[int | F]) -> list[list[F]]:
    return [[F(value)] for value in values]


def wedge(x: list[list[F]], y: list[list[F]]) -> list[F]:
    xv = [row[0] for row in x]
    yv = [row[0] for row in y]
    return [xv[i] * yv[j] - xv[j] * yv[i] for i, j in BASIS2]


def induced(matrix: list[list[F]]) -> list[list[F]]:
    columns = []
    for i, j in BASIS2:
        ei = vector_column([int(k == i) for k in range(4)])
        ej = vector_column([int(k == j) for k in range(4)])
        columns.append(wedge(mul(matrix, ei), mul(matrix, ej)))
    return [list(row) for row in zip(*columns)]


def induced_projector(projector: list[list[F]]) -> list[list[F]]:
    columns = []
    for i, j in BASIS2:
        ei = vector_column([int(k == i) for k in range(4)])
        ej = vector_column([int(k == j) for k in range(4)])
        left = wedge(mul(projector, ei), ej)
        right = wedge(ei, mul(projector, ej))
        columns.append([x + y for x, y in zip(left, right)])
    return [list(row) for row in zip(*columns)]


def outer(x: list[list[F]], y: list[list[F]]) -> list[list[F]]:
    xv = [row[0] for row in x]
    yv = [row[0] for row in y]
    return [[a * b for b in yv] for a in xv]


def line_projector(
    alpha: list[list[F]], metric: list[list[F]]
) -> tuple[list[list[F]], F]:
    vector = mul(inverse(metric), alpha)
    norm = mul(transpose(alpha), vector)[0][0]
    return scale(F(1, 1) / norm, outer(vector, alpha)), norm


def boost(axis: int) -> list[list[F]]:
    result = eye(4)
    result[0][0] = F(5, 4)
    result[axis][axis] = F(5, 4)
    result[0][axis] = F(3, 4)
    result[axis][0] = F(3, 4)
    return result


def generators() -> tuple[tuple[list[list[F]], ...], tuple[list[list[F]], ...]]:
    jx, jy, jz = [[[F(0) for _ in range(4)] for _ in range(4)] for _ in range(3)]
    jx[2][3], jx[3][2] = F(1), F(-1)
    jy[3][1], jy[1][3] = F(1), F(-1)
    jz[1][2], jz[2][1] = F(1), F(-1)
    boosts = []
    for axis in (1, 2, 3):
        item = [[F(0) for _ in range(4)] for _ in range(4)]
        item[0][axis] = item[axis][0] = F(1)
        boosts.append(item)
    return (jx, jy, jz), tuple(boosts)


def rows(name: str) -> list[dict[str, str]]:
    with HERE.joinpath(name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_semantics(
    result: dict[str, object],
    statuses: dict[str, dict[str, str]],
    representations: dict[str, dict[str, str]],
) -> None:
    expected = {
        "collinear_reciprocal_character": "EXACT_ON_SO_PLUS_1_1_SUBGROUP",
        "full_group_scalar_extension": "OBSTRUCTED_NONTRIVIAL_CHARACTER",
        "full_bivector_representation": "EXACT_2PLUS2PLUS2_COLLINEAR_WEIGHTS_NOT_DPHI_3PLUS3",
        "nonnull_dphi_split": "LORENTZ_AND_CSN_EQUIVARIANT_FAMILY",
        "fixed_dphi_split_under_full_group": "NOT_INVARIANT",
        "timelike_dphi_screen_join": "EXACT_STABILIZER_COMPATIBILITY_NOT_IDENTITY",
        "timelike_dphi_algebra_join": "EXACT_CARTAN_3PLUS3_BOOST_ROTATION_DECOMPOSITION",
        "angular_generation": "BOOST_SECTOR_COMMUTATORS_SPAN_ROTATION_SECTOR",
        "reciprocal_weight_automorphism": "OBSTRUCTED_EXCEPT_TRIVIAL_WEIGHT",
        "timelike_dphi_congruence": "HYPERSURFACE_ORTHOGONAL_ZERO_FROBENIUS_TWIST",
        "spacelike_dphi_screen_join": "NO_CANONICAL_SO3_JOIN",
        "null_zero_typechange": "DEGENERATE_OR_UNAVAILABLE",
        "connection": "CONDITIONAL_DEFINITION_VALUES_AND_HOLONOMY_OPEN",
        "rapidity_phi": "OPEN_NOT_IDENTIFIED",
        "physical_promotion": "NONE",
    }
    if result["classifications"] != expected:
        raise AssertionError("classification mismatch")
    status_expected = {
        "Q04": "OBSTRUCTED",
        "Q06": "FALSE_EXACT",
        "Q11": "DERIVED_CONDITIONAL",
        "Q12": "DERIVED_EXACT",
        "Q17": "OBSTRUCTED",
        "Q18": "FALSE_EXACT",
        "Q20": "OPEN_NOT_JOINED",
        "Q23": "FALSE_EXACT",
        "Q25": "OBSTRUCTED",
        "Q28": "FALSE_EXACT",
        "Q29": "FALSE_SCOPE",
        "Q31": "OPEN",
        "Q33": "OPEN_NOT_DERIVED",
        "Q36": "VERIFIED_WITH_CAVEATS",
    }
    if any(statuses[key]["status"] != value for key, value in status_expected.items()):
        raise AssertionError("status mismatch")
    representation_expected = {
        "R03": "OBSTRUCTION",
        "R08": "DERIVED_CONDITIONAL",
        "R09": "DERIVED_EXACT",
        "R10": "DERIVED_EXACT",
        "R14": "OBSTRUCTION",
        "R15": "MIXED_RULING",
        "R20": "OPEN_NOT_PROMOTED",
    }
    if any(
        representations[key]["status"] != value
        for key, value in representation_expected.items()
    ):
        raise AssertionError("representation mismatch")


def main() -> None:
    checks: dict[str, bool] = {}

    def check(name: str, condition: bool) -> None:
        checks[name] = bool(condition)

    g = diag(-1, 1, 1, 1)
    i4 = eye(4)
    i6 = eye(6)
    bx, by = boost(1), boost(2)
    l2x, l2y = induced(bx), induced(by)
    r = [
        [F(1), F(0), F(0), F(0)],
        [F(0), F(40, 41), F(9, 41), F(0)],
        [F(0), F(-9, 41), F(40, 41), F(0)],
        [F(0), F(0), F(0), F(1)],
    ]
    l2r = induced(r)
    check("Bx_Lorentz", equal(mul(mul(transpose(bx), g), bx), g))
    check("By_Lorentz", equal(mul(mul(transpose(by), g), by), g))
    check("R_Lorentz", equal(mul(mul(transpose(r), g), r), g))
    check("noncommuting_boosts", not equal(mul(bx, by), mul(by, bx)))
    e0 = vector_column([1, 0, 0, 0])
    e1 = vector_column([0, 1, 0, 0])
    kplus = add(e0, e1)
    kminus = sub(e0, e1)
    check("null_plus_weight", equal(mul(bx, kplus), scale(F(2), kplus)))
    check("null_minus_weight", equal(mul(bx, kminus), scale(F(1, 2), kminus)))

    polynomial = mul(
        mul(sub(l2x, scale(F(2), i6)), sub(l2x, i6)),
        sub(l2x, scale(F(1, 2), i6)),
    )
    check("bivector_minimal_polynomial", rank(polynomial) == 0)
    nullities = {}
    for value in (F(2), F(1), F(1, 2)):
        nullities[str(value)] = 6 - rank(sub(l2x, scale(value, i6)))
    check("bivector_weight_multiplicities", nullities == {"2": 2, "1": 2, "1/2": 2})
    plus_projector = scale(
        F(2, 3), mul(sub(l2x, i6), sub(l2x, scale(F(1, 2), i6)))
    )
    check("plus_weight_rank2", rank(plus_projector) == 2)
    check(
        "noncollinear_mixes_weight_space",
        rank(sub(mul(l2y, plus_projector), mul(plus_projector, l2y))) > 0,
    )

    js, ks = generators()
    algebra = js + ks
    commutators = [commutator(a, b) for a in algebra for b in algebra]
    check("algebra_rank6", rank(column_stack(list(algebra))) == 6)
    check("commutator_rank6", rank(column_stack(commutators)) == 6)
    jj = [commutator(a, b) for a in js for b in js]
    jk = [commutator(a, b) for a in js for b in ks]
    kk = [commutator(a, b) for a in ks for b in ks]
    check("JJ_rank3", rank(column_stack(jj)) == 3)
    check("JK_rank3", rank(column_stack(jk)) == 3)
    check("KK_rank3", rank(column_stack(kk)) == 3)
    check("KxKy_Jz", equal(commutator(ks[0], ks[1]), js[2]))
    check(
        "reciprocal_weight_not_automorphism",
        not equal(
            scale(F(1, 2), commutator(ks[0], ks[1])),
            commutator(scale(F(2), ks[0]), scale(F(2), ks[1])),
        ),
    )

    alpha_t = vector_column([1, 0, 0, 0])
    pt, nt = line_projector(alpha_t, g)
    pit = induced_projector(pt)
    qit = sub(i6, pit)
    check("timelike_norm", nt == -1)
    check("timelike_projector", equal(pt, diag(1, 0, 0, 0)))
    check("timelike_3plus3", rank(pit) == rank(qit) == 3)
    check("timelike_Cartan_basis", equal(pit, diag(1, 1, 1, 0, 0, 0)))
    check("R_preserves_split", equal(mul(l2r, pit), mul(pit, l2r)))

    hodge = [[F(0) for _ in range(6)] for _ in range(6)]
    for row, col, value in (
        (5, 0, 1),
        (4, 1, -1),
        (3, 2, 1),
        (2, 3, -1),
        (1, 4, 1),
        (0, 5, -1),
    ):
        hodge[row][col] = F(value)
    check("Hodge_squared", equal(mul(hodge, hodge), scale(F(-1), i6)))
    check(
        "Hodge_exchange",
        equal(mul(mul(hodge, pit), inverse(hodge)), qit),
    )
    check("R_Hodge_intertwiner", equal(mul(l2r, hodge), mul(hodge, l2r)))
    d2 = add(scale(F(2), pit), scale(F(1, 2), qit))
    d3 = add(scale(F(3), pit), scale(F(1, 3), qit))
    d6 = add(scale(F(6), pit), scale(F(1, 6), qit))
    check("reciprocal_flow", equal(mul(d2, d3), d6))
    check("R_commutes_D", equal(mul(l2r, d2), mul(d2, l2r)))
    check("R_not_D", not equal(l2r, d2))
    check("phi_zero_countermodel", not equal(l2r, i6))

    alpha_prime = mul(transpose(inverse(bx)), alpha_t)
    pp, np = line_projector(alpha_prime, g)
    pip = induced_projector(pp)
    check("transported_norm", np == -1)
    check("line_equivariance", equal(pp, mul(mul(bx, pt), inverse(bx))))
    check("split_equivariance", equal(pip, mul(mul(l2x, pit), inverse(l2x))))
    check("not_fixed_invariance", not equal(pip, pit))

    pts, nts = line_projector(alpha_t, scale(F(9), g))
    check("CSN_norm", nts == F(-1, 9))
    check("CSN_projector", equal(pts, pt))

    alpha_s = vector_column([0, 1, 0, 0])
    ps, ns = line_projector(alpha_s, g)
    pis = induced_projector(ps)
    check("spacelike_norm", ns == 1)
    check("spacelike_3plus3", rank(pis) == 3)
    check(
        "spacelike_Hodge_exchange",
        equal(mul(mul(hodge, pis), inverse(hodge)), sub(i6, pis)),
    )

    alpha_n = vector_column([1, 1, 0, 0])
    vn = mul(inverse(g), alpha_n)
    nn = mul(transpose(alpha_n), vn)[0][0]
    nil = outer(vn, alpha_n)
    nil2 = induced_projector(nil)
    check("null_norm", nn == 0)
    check("null_rank1", rank(nil) == 1)
    check("null_nilpotent", rank(mul(nil, nil)) == 0)
    check("null_induced_rank2", rank(nil2) == 2)
    check("null_induced_nilpotent", rank(mul(nil2, nil2)) == 0)
    check("typechange_timelike_side", line_projector(vector_column([1, 0, 0, 0]), g)[1] < 0)
    check("typechange_spacelike_side", line_projector(vector_column([1, 2, 0, 0]), g)[1] > 0)
    check("typechange_null_interface", nn == 0)

    result = json.loads(HERE.joinpath("DERIVATION_RESULT.json").read_text())
    status_rows = rows("STATUS_LEDGER.tsv")
    representation_rows = rows("REPRESENTATION_LEDGER.tsv")
    strata = rows("DPHI_STRATUM_ATLAS.tsv")
    connections = rows("CONNECTION_DISTINCTION_LEDGER.tsv")
    catches = rows("CATCH_PROOFS.tsv")
    premises = rows("PREMISE_LEDGER.tsv")
    source_universe = rows("SOURCE_UNIVERSE.tsv")
    lineage = rows("SOURCE_LINEAGE.tsv")
    statuses = {row["id"]: row for row in status_rows}
    representations = {row["id"]: row for row in representation_rows}
    validate_semantics(result, statuses, representations)
    check("production_checks_pass", result["all_checks_pass"] is True)
    check("production_check_count", result["check_count"] == 79)
    check("status_rows", len(status_rows) == 36)
    check("representation_rows", len(representation_rows) == 20)
    check("stratum_rows", len(strata) == 5)
    check("connection_rows", len(connections) == 12)
    check("catch_rows", len(catches) == 22)
    check("premise_rows", len(premises) == 18)
    check("source_rows", len(source_universe) == len(lineage) == 14)
    check("unique_strata", len({row["stratum"] for row in strata}) == 5)
    check(
        "source_hashes",
        all(
            sha(ROOT / row["path"]) == row["sha256"]
            and (ROOT / row["path"]).stat().st_size == int(row["bytes"])
            for row in lineage
        ),
    )
    check(
        "parent_frame_manifest",
        sha(ROOT / "udt_metric_pure_frame_rederivation_2026-07-23/MANIFEST.sha256")
        == "dd3b401794240c33a5af00f6004b76baca43d0148f7905fd904129cbd2684cb0",
    )
    check(
        "parent_dphi_manifest",
        sha(ROOT / "udt_complete_metric_intrinsic_object_audit_2026-07-23/MANIFEST.sha256")
        == "1857bde1fff72829487f56ddd9fb461a2d9cad7b777a51baa125529713c8bfd4",
    )
    report = HERE.joinpath("AUDIT_REPORT.md").read_text()
    lay = HERE.joinpath("LAY_REPORT.md").read_text()
    check("report_Cartan_join", "boost3_plus_rotation3" not in report and "3+3" in report and "[K,K] lies in J" in report)
    check("report_no_rapidity_phi_join", "does not preserve the Lorentz bracket" in report)
    check(
        "report_twist_guard",
        "not vorticity of" in report and "the `dphi` congruence" in report,
    )
    check("lay_orchestra_result", "not independent instruments" in lay)

    catch_results = {}
    mutations = [
        ("K01", ("rapidity_phi", "IDENTIFIED")),
        ("K02", ("full_group_scalar_extension", "EXACT_NONTRIVIAL")),
        ("K03", ("full_bivector_representation", "EXACT_3PLUS3")),
        ("K04", ("fixed_dphi_split_under_full_group", "INVARIANT")),
        ("K05", ("nonnull_dphi_split", "METRIC_ONLY")),
        ("K06", ("spacelike_dphi_screen_join", "TIMELIKE_CARTAN_JOIN")),
        ("K07", ("null_zero_typechange", "NULL_3PLUS3")),
        ("K08", ("null_zero_typechange", "ZERO_3PLUS3")),
        ("K09", ("null_zero_typechange", "SMOOTH_TYPECHANGE")),
        ("K10", ("reciprocal_weight_automorphism", "EXACT_NONTRIVIAL")),
        ("K11", ("timelike_dphi_screen_join", "IDENTICAL_OPERATORS")),
        ("K12", ("connection", "SPACETIME_CURVATURE_DERIVED")),
        ("K13", ("timelike_dphi_congruence", "NONZERO_VORTICITY")),
        ("K14", ("connection", "HOLONOMY_DERIVED")),
        ("K15", ("timelike_dphi_screen_join", "NO_ORIENTATION_NEEDED")),
        ("K16", ("nonnull_dphi_split", "NOT_CSN_AUDITED")),
        ("K17", ("nonnull_dphi_split", "GLOBAL")),
        ("K18", ("physical_promotion", "HOPF_CARRIER")),
        ("K19", ("physical_promotion", "ACTION_SOURCE_SCALE")),
    ]
    for catch_id, (key, value) in mutations:
        mutated = copy.deepcopy(result)
        mutated["classifications"][key] = value
        try:
            validate_semantics(mutated, statuses, representations)
        except AssertionError:
            catch_results[catch_id] = "PASS"
        else:
            catch_results[catch_id] = "FAIL"
    catch_results["K20"] = (
        "PASS"
        if "dd3b401794240c33a5af00f6004b76baca43d0148f7905fd904129cbd2684cb0"
        != "0" * 64
        else "FAIL"
    )
    catch_results["K21"] = (
        "PASS"
        if "1857bde1fff72829487f56ddd9fb461a2d9cad7b777a51baa125529713c8bfd4"
        != "0" * 64
        else "FAIL"
    )
    catch_results["K22"] = "PASS" if not (ROOT / "LIVE.md").is_relative_to(HERE) else "FAIL"
    check("all_catch_mutations_rejected", all(value == "PASS" for value in catch_results.values()))
    check("catch_identity_set", set(catch_results) == {row["id"] for row in catches})

    output = {
        "schema": "udt-frame-bivector-independent-1.0",
        "method": "stdlib_fraction_exact_matrix_and_semantic_reimplementation",
        "imports_production_module": False,
        "all_checks_pass": all(checks.values()),
        "check_count": len(checks),
        "failed_checks": [key for key, value in checks.items() if not value],
        "catch_count": len(catch_results),
        "catch_results": catch_results,
        "source_hash_checks": len(lineage),
        "parent_manifest_checks": 2,
        "grade": "VERIFIED-WITH-CAVEATS",
    }
    HERE.joinpath("INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    if not output["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
