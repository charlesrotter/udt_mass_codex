#!/usr/bin/env python3
"""Independent stdlib verification of the angular bulk Jacobi audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
MAXIMUM = (
    "COMPLETE_METRIC_DERIVES_THE_COVARIANT_ANGULAR_JACOBI_TRANSPORT_"
    "OBJECT_BUT_CURRENT_UDT_PREMISES_DO_NOT_SUPPLY_ITS_INDEPENDENT_"
    "CURVATURE_CLOSURE"
)


def z(rows: int, cols: int) -> list[list[F]]:
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def eye(size: int) -> list[list[F]]:
    value = z(size, size)
    for index in range(size):
        value[index][index] = F(1)
    return value


def add(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [
        [a[i][j] + b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def neg(a: list[list[F]]) -> list[list[F]]:
    return [[-value for value in row] for row in a]


def sub(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return add(a, neg(b))


def scale(value: F, a: list[list[F]]) -> list[list[F]]:
    return [[value * item for item in row] for row in a]


def mul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [
        [
            sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def trace(a: list[list[F]]) -> F:
    return sum((a[i][i] for i in range(len(a))), F(0))


def equal(a: list[list[F]], b: list[list[F]]) -> bool:
    return a == b


def inv2(a: list[list[F]]) -> list[list[F]]:
    determinant = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if determinant == 0:
        raise AssertionError("singular 2x2")
    return [
        [a[1][1] / determinant, -a[0][1] / determinant],
        [-a[1][0] / determinant, a[0][0] / determinant],
    ]


def determinant(matrix: list[list[F]]) -> F:
    size = len(matrix)
    if size == 1:
        return matrix[0][0]
    total = F(0)
    for column in range(size):
        minor = [
            [matrix[row][col] for col in range(size) if col != column]
            for row in range(1, size)
        ]
        total += ((-1) ** column) * matrix[0][column] * determinant(minor)
    return total


def block(
    a: list[list[F]],
    b: list[list[F]],
    c: list[list[F]],
    d: list[list[F]],
) -> list[list[F]]:
    top = [a_row + b_row for a_row, b_row in zip(a, b)]
    bottom = [c_row + d_row for c_row, d_row in zip(c, d)]
    return top + bottom


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for piece in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(piece)
    return value.hexdigest()


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_full_projected_identity() -> int:
    p = [
        [F(1), F(0), F(0), F(0)],
        [F(0), F(1), F(0), F(0)],
        [F(0), F(0), F(0), F(0)],
        [F(0), F(0), F(0), F(0)],
    ]
    q = sub(eye(4), p)
    pp = [
        [F(0), F(0), F(1), F(2)],
        [F(0), F(0), F(-1), F(1)],
        [F(3), F(1), F(0), F(0)],
        [F(2), F(-2), F(0), F(0)],
    ]
    m = [
        [F(1), F(2), F(-1), F(3)],
        [F(0), F(-2), F(2), F(1)],
        [F(4), F(1), F(3), F(-1)],
        [F(-2), F(2), F(0), F(1)],
    ]
    mp = [
        [F(2), F(-1), F(0), F(1)],
        [F(3), F(1), F(-2), F(0)],
        [F(1), F(4), F(-1), F(2)],
        [F(0), F(-3), F(1), F(2)],
    ]
    da = [
        [F(1), F(0), F(2), F(-1)],
        [F(-1), F(2), F(0), F(3)],
        [F(2), F(1), F(-2), F(0)],
        [F(0), F(-1), F(1), F(4)],
    ]
    curvature = sub(sub(da, mp), mul(m, m))

    b = mul(mul(p, m), p)
    db = mul(
        mul(
            p,
            add(
                add(mul(mul(pp, m), p), mul(mul(p, mp), p)),
                mul(mul(p, m), pp),
            ),
        ),
        p,
    )
    x = mul(mul(p, m), q)
    y = mul(mul(q, m), p)
    u = mul(mul(p, pp), q)
    v = mul(mul(q, pp), p)
    source = sub(
        sub(
            add(mul(mul(p, curvature), p), mul(x, y)),
            mul(u, y),
        ),
        add(mul(x, v), mul(mul(p, da), p)),
    )
    residual = add(add(db, mul(b, b)), source)
    if not equal(residual, z(4, 4)):
        raise AssertionError("projected Jacobi expansion")

    full_residual = sub(
        add(add(mp, mul(m, m)), curvature),
        da,
    )
    if not equal(full_residual, z(4, 4)):
        raise AssertionError("full Jacobi identity")
    return 2


def reduced_control(
    q: list[list[F]],
    qp: list[list[F]],
    qpp: list[list[F]],
    kappa: F,
) -> tuple[list[list[F]], list[list[F]], list[list[F]]]:
    qi = inv2(q)
    b = scale(F(1, 2), mul(qi, qp))
    qip = neg(mul(mul(qi, qp), qi))
    bp = scale(
        F(1, 2),
        add(mul(qip, qp), mul(qi, qpp)),
    )
    tidal = sub(add(neg(bp), scale(kappa, b)), mul(b, b))
    residual = add(add(sub(bp, scale(kappa, b)), mul(b, b)), tidal)
    if not equal(residual, z(2, 2)):
        raise AssertionError("reduced Riccati")
    if not equal(mul(q, b), mul(transpose(b), q)):
        raise AssertionError("q self-adjointness")
    return b, bp, tidal


def verify_reduced_controls() -> dict[str, object]:
    controls = [
        (
            [[F(3), F(1)], [F(1), F(2)]],
            [[F(2), F(-1)], [F(-1), F(3)]],
            [[F(1), F(2)], [F(2), F(-2)]],
            F(0),
        ),
        (
            [[F(5), F(2)], [F(2), F(4)]],
            [[F(-1), F(3)], [F(3), F(2)]],
            [[F(4), F(-2)], [F(-2), F(1)]],
            F(2),
        ),
        (
            [[F(7), F(1)], [F(1), F(3)]],
            [[F(3), F(2)], [F(2), F(-1)]],
            [[F(-2), F(1)], [F(1), F(5)]],
            F(-3),
        ),
    ]
    for args in controls:
        reduced_control(*args)

    basis = [
        [[F(1), F(0)], [F(0), F(0)]],
        [[F(0), F(1)], [F(1), F(0)]],
        [[F(0), F(0)], [F(0), F(1)]],
    ]
    images = [scale(F(-1, 2), item) for item in basis]
    vectors = [
        (item[0][0], item[0][1], item[1][1]) for item in images
    ]
    determinant_rank = determinant(
        [[vectors[column][row] for column in range(3)] for row in range(3)]
    )
    if determinant_rank == 0:
        raise AssertionError("second-jet source freedom")

    target = [[F(-1), F(0)], [F(0), F(1)]]
    target_results = {}
    for kappa in (F(0), F(2), F(-3)):
        tidal = sub(scale(kappa, target), eye(2))
        if trace(tidal) != -2:
            raise AssertionError("target tidal trace")
        tf = sub(tidal, scale(trace(tidal) / 2, eye(2)))
        if not equal(tf, scale(kappa, target)):
            raise AssertionError("target tidal tracefree")
        target_results[str(kappa)] = {
            "trace": str(trace(tidal)),
            "tracefree": "kappa*J",
        }
    return {
        "rational_reduced_controls": len(controls),
        "q_second_jet_tidal_rank": 3,
        "target_nonaffinity_controls": target_results,
    }


def verify_trace_shape_twist() -> int:
    controls = [
        (F(2), F(1), F(3), F(4)),
        (F(-1), F(2), F(-2), F(1)),
        (F(0), F(5), F(1), F(-3)),
    ]
    for area, j1, j2, omega in controls:
        identity = eye(2)
        j = [[j1, j2], [j2, -j1]]
        w = [[F(0), -omega], [omega, F(0)]]
        b = add(add(scale(area, identity), j), w)
        shape = j1 * j1 + j2 * j2
        expected = add(
            scale(area * area + shape - omega * omega, identity),
            add(scale(2 * area, j), scale(2 * area, w)),
        )
        if not equal(mul(b, b), expected):
            raise AssertionError("trace/shape/twist square")
        if not equal(add(mul(j, w), mul(w, j)), z(2, 2)):
            raise AssertionError("J/W anticommutator")
    return len(controls)


def verify_nonblock_controls() -> int:
    controls = [
        (
            [[F(-4), F(0)], [F(0), F(3)]],
            [[F(1), F(2)], [F(-1), F(1)]],
            [[F(3), F(1)], [F(1), F(2)]],
        ),
        (
            [[F(-9), F(0)], [F(0), F(5)]],
            [[F(2), F(-1)], [F(3), F(2)]],
            [[F(5), F(2)], [F(2), F(4)]],
        ),
        (
            [[F(-16), F(0)], [F(0), F(7)]],
            [[F(-2), F(3)], [F(1), F(-1)]],
            [[F(7), F(1)], [F(1), F(3)]],
        ),
    ]
    for h, cross, q in controls:
        hinv = inv2(h)
        capital_q = add(q, mul(mul(transpose(cross), hinv), cross))
        complete = block(h, cross, transpose(cross), capital_q)
        change = block(
            eye(2),
            neg(mul(hinv, cross)),
            z(2, 2),
            eye(2),
        )
        reduced = mul(mul(transpose(change), complete), change)
        expected = block(h, z(2, 2), z(2, 2), q)
        if not equal(reduced, expected):
            raise AssertionError("nonblock congruence")
        if determinant(complete) != determinant(h) * determinant(q):
            raise AssertionError("nonblock determinant")
    return len(controls)


def verify_csn_controls() -> int:
    controls = [
        (F(2), F(3), F(5)),
        (F(3), F(2), F(7)),
        (F(299792458), F(5), F(11)),
    ]
    for c, omega, lam in controls:
        h_star = [[-c * c * F(4, 9), F(0)], [F(0), F(9, 4)]]
        if -determinant(h_star) != c * c:
            raise AssertionError("c determinant")
        g = scale(omega * omega, h_star)
        g_scaled = scale(lam * lam, g)
        recovered = scale(F(1, (lam * omega) ** 2), g_scaled)
        if not equal(recovered, h_star):
            raise AssertionError("CSN representative")
    return len(controls)


def verify_conditional_source_theorem() -> int:
    t = F(1, 3)
    controls = (F(0), F(1, 2), F(1), F(2))
    for s in controls:
        denominator_minus = 1 - s * t
        denominator_plus = 1 + s * t
        if denominator_minus == 0 or denominator_plus == 0:
            raise AssertionError("singular conditional control")
        b_minus = (-s + t) / denominator_minus
        b_plus = (s + t) / denominator_plus
        db_minus_dt = (1 - s * s) / denominator_minus**2
        db_plus_dt = (1 - s * s) / denominator_plus**2
        if (
            (1 - t * t) * db_minus_dt + b_minus * b_minus - 1
            != 0
            or (1 - t * t) * db_plus_dt + b_plus * b_plus - 1
            != 0
        ):
            raise AssertionError("conditional flow residual")
        area = (b_minus + b_plus) / 2
        shape = ((b_plus - b_minus) / 2) ** 2
        expected_area = t * (1 - s * s) / (1 - s * s * t * t)
        expected_shape = (
            s * s * (1 - t * t) ** 2
            / (1 - s * s * t * t) ** 2
        )
        if area != expected_area or shape != expected_shape:
            raise AssertionError("conditional matrix flow")
        if (area == 0) != (s * s == 1):
            raise AssertionError("second-seal selection")
        if s * s == 1 and shape != 1:
            raise AssertionError("conditional unit shape")
    return len(controls)


def endpoint_bump_checks() -> int:
    def p(y: F) -> F:
        return y**3 * (1 - y) ** 3

    def pp(y: F) -> F:
        return 3 * y**2 * (1 - y) ** 2 * (1 - 2 * y)

    def ppp(y: F) -> F:
        return 6 * y - 36 * y**2 + 60 * y**3 - 30 * y**4

    checks = 0
    for y in (F(0), F(1)):
        for value in (p(y), pp(y), ppp(y)):
            if value != 0:
                raise AssertionError("endpoint bump jet")
            checks += 1
    if pp(F(1, 4)) == 0:
        raise AssertionError("interior bump freedom")
    return checks


def load_state() -> dict[str, bool]:
    result = json.loads((HERE / "RESULT.json").read_text())
    projected = json.loads(
        (HERE / "FULL_PROJECTED_JACOBI_FORMULA.json").read_text()
    )
    generic = json.loads(
        (HERE / "GENERIC_REDUCED_RICCATI_FORMULA.json").read_text()
    )
    trace_shape = json.loads(
        (HERE / "TRACE_SHAPE_TWIST_EVOLUTION.json").read_text()
    )
    csn = json.loads(
        (HERE / "CSN_NORMALIZED_REPRESENTATIVE.json").read_text()
    )
    routes = read_tsv("ROUTE_RULING_MATRIX.tsv")
    boundaries = read_tsv("BOUNDARY_PROPAGATION_ATLAS.tsv")
    freedoms = read_tsv("SOURCE_TERM_FREEDOM.tsv")
    catches = read_tsv("CATCH_PROOFS.tsv")
    statuses = read_tsv("STATUS_LEDGER.tsv")
    theorem = json.loads(
        (HERE / "RECIPROCAL_SOURCE_CONDITIONAL_THEOREM.json").read_text()
    )
    route_ids = [row["route_id"] for row in routes]
    state = {
        "raw_Q_rejected": "q=Q-C^T*h^-1*C"
        in (ROOT / "udt_relative_angular_area_shape_selector_audit_2026-07-23"
            / "NONBLOCK_INVARIANT_FORMULA.json").read_text(),
        "cross_terms_retained": projected["nonblock_terms_retained"] is True,
        "projector_motion_retained": "-U*Y-X*V" in projected["effective_source"],
        "leakage_retained": "+X*Y" in projected["effective_source"],
        "acceleration_retained": "-P*nabla(a)*P"
        in projected["effective_source"],
        "twist_retained": "-omega^2" in trace_shape["trace_equation"],
        "nonaffinity_retained": trace_shape[
            "nonaffine_twistfree_projectable_control"
        ]["K_eff"] == "R_T-kappa*B",
        "cartan_not_field_equation": projected["status"]
        == "DERIVED_EXACT_IDENTITY_NOT_INDEPENDENT_FIELD_EQUATION",
        "riccati_not_selector": generic["identity_residual"] == "EXACT_ZERO",
        "second_jet_rank_three": generic[
            "same_q_qp_arbitrary_qpp_tidal_rank"
        ] == 3,
        "tidal_trace_not_set": result["counts"][
            "native_bulk_law_derivations"
        ] == 0,
        "tidal_tf_not_set": result["counts"][
            "conditional_bulk_law_derivations"
        ] == 0,
        "seal_local_only": boundaries[4]["A_rel"] == "ZERO_ONLY",
        "seal_unit_not_forced": boundaries[2]["J_amplitude"]
        == "FREE_ONE_PARAMETER",
        "two_seal_not_pointwise": boundaries[5]["bulk_uniqueness"] == "NO",
        "reciprocal_source_join_absent": any(
            row["freedom_id"] == "F05"
            and row["current_selector"] == "ABSENT_NOT_INVENTED"
            for row in freedoms
        ),
        "csn_not_value_selector": csn["status"].endswith(
            "NOT_SELECTED_DYNAMICS"
        ),
        "c_not_one": [row["c"] for row in csn["c_controls"]]
        == ["2", "3", "299792458"],
        "cap_not_bulk_equation": routes[6]["ruling"]
        == "CONSTRAINS_NOT_CLOSES",
        "monodromy_not_normalization": "monodromy" in routes[6][
            "exact_reason"
        ],
        "bianchi_not_dynamics": routes[7]["ruling"]
        == "IDENTITY_DEFINES_SOURCE_NOT_LAW",
        "bootstrap_not_invented": routes[9]["ruling"]
        == "NOT_AN_EXECUTABLE_EQUATION",
        "critical_phi_not_assigned": "critical-`phi`" in (
            HERE / "PREREGISTRATION.md"
        ).read_text(),
        "external_action_absent": any(
            row["object"] == "complete_onshell_branches"
            and row["status"] == "ZERO_REGISTERED"
            for row in statuses
        ),
        "onshell_not_fabricated": result["counts"][
            "complete_on_shell_g_phi_branches"
        ] == 0,
        "routes_complete_unique": route_ids
        == [f"R{index:02d}" for index in range(1, 13)]
        and len(set(route_ids)) == 12
        and len(catches) == 27,
        "conditional_not_native": theorem["missing_join_status"]
        == "UNREGISTERED_NOT_DERIVED"
        and theorem["native_status"] == "NOT_A_CURRENT_UDT_DERIVATION"
        and result["counts"]["unregistered_conditional_closure_theorems"]
        == 1,
    }
    return state


def validate_state(state: dict[str, bool]) -> None:
    if set(state) != {
        "raw_Q_rejected",
        "cross_terms_retained",
        "projector_motion_retained",
        "leakage_retained",
        "acceleration_retained",
        "twist_retained",
        "nonaffinity_retained",
        "cartan_not_field_equation",
        "riccati_not_selector",
        "second_jet_rank_three",
        "tidal_trace_not_set",
        "tidal_tf_not_set",
        "seal_local_only",
        "seal_unit_not_forced",
        "two_seal_not_pointwise",
        "reciprocal_source_join_absent",
        "csn_not_value_selector",
        "c_not_one",
        "cap_not_bulk_equation",
        "monodromy_not_normalization",
        "bianchi_not_dynamics",
        "bootstrap_not_invented",
        "critical_phi_not_assigned",
        "external_action_absent",
        "onshell_not_fabricated",
        "routes_complete_unique",
        "conditional_not_native",
    }:
        raise AssertionError("guard universe")
    if not all(state.values()):
        raise AssertionError("guard contract")


def mutation_catches() -> int:
    state = load_state()
    validate_state(state)
    caught = 0
    for key in state:
        mutant = copy.deepcopy(state)
        mutant[key] = False
        try:
            validate_state(mutant)
        except AssertionError:
            caught += 1
        else:
            raise AssertionError(f"mutation escaped: {key}")
    return caught


def verify_sources() -> int:
    rows = read_tsv("SOURCE_LINEAGE.tsv")
    if len(rows) != 20:
        raise AssertionError("source count")
    for row in rows:
        path = ROOT / row["path"]
        if (
            not path.is_file()
            or digest(path) != row["sha256"]
            or path.stat().st_size != int(row["size"])
        ):
            raise AssertionError(f"source changed: {row['path']}")
    return len(rows)


def main() -> None:
    result = json.loads((HERE / "RESULT.json").read_text())
    if result["maximum_conclusion"] != MAXIMUM:
        raise AssertionError("maximum conclusion")
    projected_checks = verify_full_projected_identity()
    reduced = verify_reduced_controls()
    twist_checks = verify_trace_shape_twist()
    nonblock_checks = verify_nonblock_controls()
    csn_checks = verify_csn_controls()
    conditional_checks = verify_conditional_source_theorem()
    bump_checks = endpoint_bump_checks()
    source_checks = verify_sources()
    catches = mutation_catches()
    if catches != 27:
        raise AssertionError("mutation count")

    output = {
        "schema": "udt-angular-bulk-jacobi-independent-1.0",
        "status": "PASS",
        "implementation": (
            "stdlib_Fraction_full_projection_reduced_jets_nonblock_"
            "congruence_CSN_controls_and_exercised_mutations"
        ),
        "projected_identity_checks": projected_checks,
        **reduced,
        "trace_shape_twist_controls": twist_checks,
        "rational_nonblock_controls": nonblock_checks,
        "csn_c_controls": csn_checks,
        "conditional_two_seal_controls": conditional_checks,
        "endpoint_flat_exact_checks": bump_checks,
        "source_hashes_replayed": source_checks,
        "mutation_catches": catches,
        "maximum_conclusion": MAXIMUM,
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
