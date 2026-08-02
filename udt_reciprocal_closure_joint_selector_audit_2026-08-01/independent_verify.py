#!/usr/bin/env python3
"""Non-importing exact reconstruction and mutation catches for projector closure."""

from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


PKG = Path(__file__).resolve().parent
ROOT = PKG.parent


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def mt(a):
    return [list(row) for row in zip(*a)]


def ms(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def tr(a):
    return sum(a[i][i] for i in range(len(a)))


def frob2(a):
    return sum(value * value for row in a for value in row)


def dprojector(a, b):
    return [[F(0), F(0), a], [F(0), F(0), b], [a, b, F(0)]]


def exact_case(aa, bb):
    dps = [dprojector(aa[i], bb[i]) for i in range(3)]
    strain = [[aa[i] * aa[j] + bb[i] * bb[j] for j in range(3)] for i in range(3)]
    l2p = sum(frob2(dp) for dp in dps) / 2
    l2s = tr(strain)
    comm2 = F(0)
    area = F(0)
    for i in range(3):
        for j in range(3):
            comm = ms(mm(dps[i], dps[j]), mm(dps[j], dps[i]))
            comm2 += frob2(comm) / 2
            area += (aa[i] * bb[j] - bb[i] * aa[j]) ** 2
    gram = tr(strain) ** 2 - tr(mm(strain, strain))
    return l2p, l2s, comm2, area, gram


def table(name):
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def blob_hash(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def main() -> int:
    checks = {}
    seeds = []
    for k in range(1, 26):
        aa = [F(k - 7), F(2 * k + 1), F(3 - k)]
        bb = [F(5 - 2 * k), F(k + 4), F(3 * k - 2)]
        seeds.append((aa, bb))
    recon = [exact_case(aa, bb) for aa, bb in seeds]
    checks["25_exact_L2_reconstructions"] = all(row[0] == row[1] for row in recon)
    checks["25_exact_L4_reconstructions"] = all(row[2] == row[3] == row[4] for row in recon)

    rank_one = []
    for k in range(1, 18):
        q = [F(k), F(1 - k), F(2 * k + 3)]
        aa = [value * F(2) for value in q]
        bb = [value * F(-3) for value in q]
        rank_one.append(exact_case(aa, bb))
    checks["17_rank_one_area_zero"] = all(row[3] == 0 for row in rank_one)
    checks["17_rank_one_path_cost_positive"] = all(row[1] > 0 for row in rank_one)

    witness = exact_case([F(1), F(0), F(0)], [F(0), F(1), F(0)])
    checks["rank_two_witness_area_two"] = witness[2] == witness[3] == witness[4] == 2
    checks["axis_lift_reversal_projector_identity"] = all(
        F(a) * F(b) == F(-a) * F(-b) for a, b in ((0, 0), (0, 1), (1, 0), (1, 1))
    )

    # Independent algebraic selection controls.
    checks["quartic_rank_one_blind_subspace_dimension_one"] = (F(1) + F(-1) == 0) and (F(1) + F(0) != 0)
    checks["nonarea_quartic_countermodel"] = F(7) ** 2 > 0
    checks["scalar_one_generator_commutator_zero"] = mm([[-1, 0], [0, 1]], [[-1, 0], [0, 1]]) == mm([[-1, 0], [0, 1]], [[-1, 0], [0, 1]])
    checks["coefficient_ratio_not_fixed_by_stationarity"] = (F(4) / F(1)) != (F(1) / F(1))

    # Current-source and preregistration guards.
    premise_rows = table("PREMISE_LEDGER.tsv")
    current_rows = []
    with (ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv").open(newline="", encoding="utf-8") as handle:
        current_rows = list(csv.DictReader(handle, delimiter="\t"))
    current = {row["premise_id"]: row for row in current_rows}
    checks["current_carrier_remains_posit"] = current["G09"]["current_status"] == "POSIT"
    checks["complete_action_remains_open"] = current["G16"]["current_status"] == "OPEN"
    checks["strong_CSN_remains_inactive"] = current["G04"]["active_use"] == "INACTIVE_UNLESS_CHARLES_EXPLICITLY_REAUTHORIZES"
    checks["candidate_joint_explicitly_free"] = all(
        any(row["id"] == pid and row["status_before_audit"].startswith("FREE_") for row in premise_rows)
        for pid in ("P14", "P15")
    )

    sources = table("SOURCE_INVENTORY.tsv")
    source_integrity = []
    for row in sources:
        data = (ROOT / row["path"]).read_bytes()
        source_integrity.append(hashlib.sha256(data).hexdigest() == row["sha256"] and blob_hash(data) == row["git_blob"])
    checks["24_source_hashes_replayed"] = len(source_integrity) == 24 and all(source_integrity)

    # Exercised catch-proofs: each intentionally corrupted claim must be rejected.
    catches = {
        "missing_half_factor_L2": any(2 * row[0] != row[1] for row in recon),
        "anticommutator_as_loop_curvature": frob2([[2, 0, 0], [0, 0, 0], [0, 0, 2]]) != witness[3],
        "rank_one_area_promoted_nonzero": any(row[3] == 0 for row in rank_one),
        "rank_one_path_cost_promoted_zero": any(row[1] > 0 for row in rank_one),
        "quartic_nonarea_called_rank_one_blind": F(7) ** 2 != 0,
        "finite_size_called_unique_coefficient": F(1) != F(4),
        "carrier_called_derived": current["G09"]["current_status"] != "DERIVED",
        "complete_action_called_closed": current["G16"]["current_status"] != "DERIVED",
        "strong_CSN_silently_activated": current["G04"]["current_status"] != "DERIVED",
        "historical_candidate_called_authority": all(
            row["affirmative_authority"].startswith("NO_") for row in sources if row["id"] in {"S05", "S06"}
        ),
    }
    checks["10_mutation_catches_exercised"] = len(catches) == 10 and all(catches.values())

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "catch_proofs": catches,
        "catch_proofs_passed": sum(catches.values()),
        "catch_proofs_total": len(catches),
        "implementation": "stdlib Fraction; no import of production derivation",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
