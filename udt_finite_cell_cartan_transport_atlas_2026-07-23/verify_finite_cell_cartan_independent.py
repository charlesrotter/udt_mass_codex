#!/usr/bin/env python3
"""Independent stdlib/Fraction verification of the finite-cell Cartan atlas.

This file does not import the SymPy production derivation.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASIS2 = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))


def zmat(n: int, m: int) -> list[list[F]]:
    return [[F(0) for _ in range(m)] for _ in range(n)]


def eye(n: int) -> list[list[F]]:
    out = zmat(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def diag(values: tuple[int, ...]) -> list[list[F]]:
    out = zmat(len(values), len(values))
    for i, value in enumerate(values):
        out[i][i] = F(value)
    return out


def add(a: list[list[F]], b: list[list[F]], scale: F = F(1)) -> list[list[F]]:
    return [[a[i][j] + scale * b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def mul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    out = zmat(len(a), len(b[0]))
    for i in range(len(a)):
        for k in range(len(b)):
            for j in range(len(b[0])):
                out[i][j] += a[i][k] * b[k][j]
    return out


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def is_zero(a: list[list[F]]) -> bool:
    return all(value == 0 for row in a for value in row)


def comm(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return add(mul(a, b), mul(b, a), F(-1))


def rank(a: list[list[F]]) -> int:
    work = [row[:] for row in a]
    rows = len(work)
    cols = len(work[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((i for i in range(pivot_row, rows) if work[i][col] != 0), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][col]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for i in range(rows):
            if i != pivot_row and work[i][col] != 0:
                factor = work[i][col]
                work[i] = [
                    work[i][j] - factor * work[pivot_row][j] for j in range(cols)
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def submatrix(a: list[list[F]], rows: tuple[int, ...], cols: tuple[int, ...]) -> list[list[F]]:
    return [[a[i][j] for j in cols] for i in rows]


def wedge_coords(x: list[F], y: list[F]) -> list[F]:
    return [x[i] * y[j] - x[j] * y[i] for i, j in BASIS2]


def matvec(a: list[list[F]], x: list[F]) -> list[F]:
    return [sum((a[i][j] * x[j] for j in range(len(x))), F(0)) for i in range(len(a))]


def induced(a: list[list[F]]) -> list[list[F]]:
    e = [[F(int(i == j)) for i in range(4)] for j in range(4)]
    cols = []
    for i, j in BASIS2:
        first = wedge_coords(matvec(a, e[i]), e[j])
        second = wedge_coords(e[i], matvec(a, e[j]))
        cols.append([first[k] + second[k] for k in range(6)])
    return [[cols[j][i] for j in range(6)] for i in range(6)]


def connection(r1: int, r2: int, r3: int, b1: int, b2: int, b3: int) -> list[list[F]]:
    return [
        [F(0), F(b1), F(b2), F(b3)],
        [F(b1), F(0), F(r3), F(-r2)],
        [F(b2), F(-r3), F(0), F(r1)],
        [F(b3), F(r2), F(-r1), F(0)],
    ]


def read_tsv(name: str) -> list[dict[str, str]]:
    with HERE.joinpath(name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_tables(
    branch: list[dict[str, str]],
    cross: list[dict[str, str]],
    blocks: list[dict[str, str]],
    transitions: list[dict[str, str]],
    status: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    ids = [row["completion_id"] for row in branch]
    expected_classes = {
        "TIMELIKE_NONNULL",
        "SPACELIKE_NONNULL",
        "NULL_INTERFACE",
        "ZERO_INTERFACE",
        "TYPE_CHANGING",
    }
    if len(ids) != 12 or len(set(ids)) != 12:
        errors.append("branch_identity_coverage")
    if not all(item.startswith(f"FC{i:02d}_") for i, item in enumerate(ids, 1)):
        errors.append("branch_order")
    pairs = [(row["completion_id"], row["causal_class"]) for row in cross]
    if len(pairs) != 60 or len(set(pairs)) != 60:
        errors.append("cross_identity_coverage")
    for item in ids:
        if {c for fc, c in pairs if fc == item} != expected_classes:
            errors.append(f"causal_coverage:{item}")
    if {row["domain"] for row in blocks} != {
        "TIMELIKE_NONNULL_DPHI",
        "SPACELIKE_NONNULL_DPHI",
        "NULL_NONNULL_DPHI",
        "ZERO_DPHI",
    }:
        errors.append("connection_domains")
    if len(transitions) != 8 or len({row["transition"] for row in transitions}) != 8:
        errors.append("transition_coverage")
    if any(row["selection"] != "NO_COMPLETE_ONSHELL_WITNESS;NO_BRANCH_SELECTED" for row in branch):
        errors.append("selection_overclaim")
    if any(row["field_witness_status"] != "UNSUPPLIED_COMPLETE_G_PHI_PROFILE" for row in cross):
        errors.append("field_witness_overclaim")
    if any(row["selection"] != "NOT_SELECTED" for row in cross):
        errors.append("cross_selection_overclaim")
    if any("KATO_AVAILABLE" not in row["geometric_transport"] for row in cross if row["causal_class"] in {"TIMELIKE_NONNULL", "SPACELIKE_NONNULL"}):
        errors.append("nonnull_kato_loss")
    if any("UNDEFINED" not in row["connection_behavior"] for row in cross if row["causal_class"] in {"NULL_INTERFACE", "ZERO_INTERFACE"}):
        errors.append("degeneration_loss")
    block_map = {row["domain"]: row for row in blocks}
    if block_map.get("SPACELIKE_NONNULL_DPHI", {}).get("interpretation") != "SYMMETRIC_PAIR_NOT_OBSERVER_BOOST_ROTATION":
        errors.append("spacelike_observer_overclaim")
    if block_map.get("NULL_NONNULL_DPHI", {}).get("sector_B") != "NILPOTENT_FILTRATION_ONLY":
        errors.append("null_semisimple_overclaim")
    transition_map = {row["transition"]: row for row in transitions}
    if transition_map.get("PHI_ZERO_NONNULL_DPHI", {}).get("maximum") != "SEAL_VALUE_ALONE_DOES_NOT_DEGENERATE_SPLIT":
        errors.append("phi_value_gradient_confusion")
    if transition_map.get("TRUE_METRIC_OR_MANIFOLD_SINGULARITY", {}).get("maximum") != "NO_THROUGH_SINGULARITY_CLAIM":
        errors.append("singularity_extension_overclaim")
    branch_map = {row["completion_id"]: row for row in branch}
    if "CRITICAL_POINT" not in branch_map.get("FC03_TWO_CAP_P0", {}).get("spacelike_or_static_persistence", ""):
        errors.append("compact_static_criticality_loss")
    if "NOT_FORCED" not in branch_map.get("FC03_TWO_CAP_P0", {}).get("timelike_persistence", ""):
        errors.append("timelive_overclaim")
    status_map = {row["id"]: row for row in status}
    if len(status_map) != len(status) or len(status) != 36:
        errors.append("status_coverage")
    required_status = {
        "S10": ("DERIVED", "not_physical_time_evolution"),
        "S15": ("OPEN", "no_native_extension_derived"),
        "S20": ("REJECTED", "physical_representative_selection"),
        "S33": ("OBSERVED", "solve_complete_metric_phi_equations"),
        "S35": ("OPEN", "not_force_or_evolution"),
        "S36": ("OPEN", "separate_bridge"),
    }
    for item, (grade, remainder) in required_status.items():
        row = status_map.get(item, {})
        if row.get("status") != grade or row.get("remaining_open") != remainder:
            errors.append(f"status_scope:{item}")
    return errors


def main() -> None:
    checks: list[dict[str, object]] = []

    def check(name: str, condition: bool, detail: object = "") -> None:
        checks.append({"name": name, "pass": bool(condition), "detail": detail})

    g = diag((-1, 1, 1, 1))
    g2 = diag((-1, -1, -1, 1, 1, 1))
    omega = connection(2, 3, 5, 7, 11, 13)
    a2 = induced(omega)
    check("independent_vector_connection_lorentz", is_zero(add(mul(transpose(omega), g), mul(g, omega))), omega)
    check("independent_bivector_connection_metric_skew", is_zero(add(mul(transpose(a2), g2), mul(g2, a2))), a2)

    pt = diag((1, 1, 1, 0, 0, 0))
    qt = add(eye(6), pt, F(-1))
    rotation = induced(connection(2, 3, 5, 0, 0, 0))
    boost = induced(connection(0, 0, 0, 1, 2, 3))
    check("independent_rotations_preserve_timelike_split", is_zero(comm(rotation, pt)))
    check("independent_boosts_mix_timelike_split", not is_zero(comm(boost, pt)))
    check("independent_timelike_cross_block_ranks", (rank(submatrix(boost, (0, 1, 2), (3, 4, 5))), rank(submatrix(boost, (3, 4, 5), (0, 1, 2)))) == (2, 2))
    check("independent_timelike_total_mix_rank", rank(boost) == 4, rank(boost))
    nabla = comm(a2, pt)
    kato = add(mul(nabla, pt), mul(nabla, qt), F(-1))
    check("independent_timelike_kato_identity", comm(kato, pt) == nabla)
    check("independent_timelike_corrected_preserves", is_zero(comm(add(a2, kato, F(-1)), pt)))
    check("independent_timelike_kato_metric_skew", is_zero(add(mul(transpose(kato), g2), mul(g2, kato))))

    ps = diag((1, 0, 0, 1, 1, 0))
    qs = add(eye(6), ps, F(-1))
    so12 = induced(connection(2, 0, 0, 0, 3, 5))
    complement = induced(connection(0, 3, 5, 2, 0, 0))
    check("independent_SO12_preserves_spacelike_split", is_zero(comm(so12, ps)))
    check("independent_SO12_complement_mixes", not is_zero(comm(complement, ps)))
    nabla_s = comm(a2, ps)
    kato_s = add(mul(nabla_s, ps), mul(nabla_s, qs), F(-1))
    check("independent_spacelike_kato_identity", comm(kato_s, ps) == nabla_s)
    check("independent_spacelike_corrected_preserves", is_zero(comm(add(a2, kato_s, F(-1)), ps)))

    null_map = [
        [F(-1), F(-1), F(0), F(0)],
        [F(1), F(1), F(0), F(0)],
        [F(0), F(0), F(0), F(0)],
        [F(0), F(0), F(0), F(0)],
    ]
    null2 = induced(null_map)
    check("independent_null_parent_rank_one", rank(null_map) == 1)
    check("independent_null_parent_nilpotent", is_zero(mul(null_map, null_map)))
    check("independent_null_Lambda2_rank_two", rank(null2) == 2, rank(null2))
    check("independent_null_Lambda2_nilpotent", is_zero(mul(null2, null2)))
    check("independent_zero_limits_nonunique", diag((1, 0, 0, 0)) != diag((0, 1, 0, 0)))

    branch = read_tsv("FINITE_CELL_CARTAN_TRANSPORT_ATLAS.tsv")
    cross = read_tsv("COMPLETION_CAUSAL_CROSS.tsv")
    blocks = read_tsv("CONNECTION_BLOCK_ATLAS.tsv")
    transitions = read_tsv("CAUSAL_TRANSITION_ATLAS.tsv")
    status = read_tsv("STATUS_LEDGER.tsv")
    check("independent_table_contract", not validate_tables(branch, cross, blocks, transitions, status), validate_tables(branch, cross, blocks, transitions, status))

    result = json.loads(HERE.joinpath("DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    check("production_all_checks_pass", result["all_checks_pass"] is True)
    check("production_check_count", result["check_count"] == 46, result["check_count"])
    check("production_count_contract", result["counts"] == {
        "causal_classes": 5,
        "complete_onshell_g_phi_branches": 0,
        "completion_causal_cross": 60,
        "completion_families": 12,
        "connection_domains": 4,
        "transition_witnesses": 8,
    }, result["counts"])
    lineage = read_tsv("SOURCE_LINEAGE.tsv")
    line_map = {row["path"]: row for row in lineage}
    check("source_lineage_exact_count", len(lineage) == 22 and len(line_map) == 22, len(lineage))
    check("source_lineage_matches_production", lineage == [
        {"path": row["path"], "sha256": row["sha256"], "bytes": str(row["bytes"])}
        for row in result["source_hashes"]
    ])
    source_ok = all(
        hashlib.sha256(ROOT.joinpath(path).read_bytes()).hexdigest() == row["sha256"]
        and len(ROOT.joinpath(path).read_bytes()) == int(row["bytes"])
        for path, row in line_map.items()
    )
    check("source_lineage_current_bytes", source_ok)

    catches: list[dict[str, object]] = []

    def catch(name: str, mutation) -> None:
        b, c, k, t, s = deepcopy(branch), deepcopy(cross), deepcopy(blocks), deepcopy(transitions), deepcopy(status)
        mutation(b, c, k, t, s)
        catches.append({"name": name, "pass": bool(validate_tables(b, c, k, t, s))})

    catch("reject_missing_completion", lambda b, c, k, t, s: b.pop())
    catch("reject_duplicate_completion", lambda b, c, k, t, s: b.__setitem__(1, deepcopy(b[0])))
    catch("reject_missing_causal_cross", lambda b, c, k, t, s: c.pop())
    catch("reject_duplicate_causal_cross", lambda b, c, k, t, s: c.__setitem__(1, deepcopy(c[0])))
    catch("reject_missing_connection_domain", lambda b, c, k, t, s: k.pop())
    catch("reject_missing_transition", lambda b, c, k, t, s: t.pop())
    catch("reject_selected_unsolved_branch", lambda b, c, k, t, s: b[0].__setitem__("selection", "SELECTED"))
    catch("reject_complete_witness_invention", lambda b, c, k, t, s: c[0].__setitem__("field_witness_status", "COMPLETE"))
    catch("reject_nonnull_kato_loss", lambda b, c, k, t, s: c[0].__setitem__("geometric_transport", "NONE"))
    null_index = next(i for i, row in enumerate(cross) if row["causal_class"] == "NULL_INTERFACE")
    catch("reject_null_semisimple_continuation", lambda b, c, k, t, s: c[null_index].__setitem__("connection_behavior", "PRESERVES"))
    zero_index = next(i for i, row in enumerate(cross) if row["causal_class"] == "ZERO_INTERFACE")
    catch("reject_zero_intrinsic_continuation", lambda b, c, k, t, s: c[zero_index].__setitem__("connection_behavior", "PRESERVES"))
    spacelike_index = next(i for i, row in enumerate(blocks) if row["domain"] == "SPACELIKE_NONNULL_DPHI")
    catch("reject_spacelike_observer_split", lambda b, c, k, t, s: k[spacelike_index].__setitem__("interpretation", "OBSERVER_BOOST_ROTATION_CARTAN"))
    null_block_index = next(i for i, row in enumerate(blocks) if row["domain"] == "NULL_NONNULL_DPHI")
    catch("reject_null_3plus3", lambda b, c, k, t, s: k[null_block_index].__setitem__("sector_B", "SEMISIMPLE_3PLUS3"))
    phi_zero_index = next(i for i, row in enumerate(transitions) if row["transition"] == "PHI_ZERO_NONNULL_DPHI")
    catch("reject_phi_zero_gradient_confusion", lambda b, c, k, t, s: t[phi_zero_index].__setitem__("maximum", "SPLIT_DEGENERATES"))
    status_index = {row["id"]: i for i, row in enumerate(status)}
    catch("reject_Kato_physical_time", lambda b, c, k, t, s: s[status_index["S10"]].__setitem__("remaining_open", "physical_time_derived"))
    catch("reject_CSN_LC_invariance", lambda b, c, k, t, s: s[status_index["S20"]].__setitem__("status", "DERIVED"))
    fc03_index = next(i for i, row in enumerate(branch) if row["completion_id"] == "FC03_TWO_CAP_P0")
    catch("reject_static_compact_nonnull_claim", lambda b, c, k, t, s: b[fc03_index].__setitem__("spacelike_or_static_persistence", "GLOBAL_NONNULL"))
    catch("reject_timelive_theorem_claim", lambda b, c, k, t, s: b[fc03_index].__setitem__("timelike_persistence", "TIMELIVE_NONNULL_FORCED"))
    singular_index = next(i for i, row in enumerate(transitions) if row["transition"] == "TRUE_METRIC_OR_MANIFOLD_SINGULARITY")
    catch("reject_singularity_extension", lambda b, c, k, t, s: t[singular_index].__setitem__("maximum", "GLOBAL_EXTENSION"))
    catch("reject_cross_branch_selection", lambda b, c, k, t, s: c[0].__setitem__("selection", "SELECTED"))
    catch("reject_complete_solution_claim", lambda b, c, k, t, s: s[status_index["S33"]].__setitem__("status", "DERIVED"))
    catch("reject_matter_import", lambda b, c, k, t, s: s[status_index["S36"]].__setitem__("status", "DERIVED"))
    check("all_exercised_catches_pass", all(row["pass"] for row in catches), catches)

    output = {
        "schema": "udt-finite-cell-Cartan-independent-1.0",
        "python": sys.version.split()[0],
        "implementation": "stdlib_Fraction_no_SymPy_no_production_import",
        "all_checks_pass": all(row["pass"] for row in checks),
        "check_count": len(checks),
        "checks": checks,
        "catch_count": len(catches),
        "all_catches_pass": all(row["pass"] for row in catches),
        "catches": catches,
    }
    HERE.joinpath("INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "all_checks_pass": output["all_checks_pass"],
        "check_count": output["check_count"],
        "all_catches_pass": output["all_catches_pass"],
        "catch_count": output["catch_count"],
    }, indent=2, sort_keys=True))
    raise SystemExit(0 if output["all_checks_pass"] and output["all_catches_pass"] else 1)


if __name__ == "__main__":
    main()
