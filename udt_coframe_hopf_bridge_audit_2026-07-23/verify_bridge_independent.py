#!/usr/bin/env python3
"""Independent rational verifier for the coframe-to-Hopf bridge audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED_ROW_DIGESTS = {
    "subgroups": "65caf621a881e77e12ef5ee3c41501f51a4fd75f6bc6474aab7ff7e88bff1fb6",
    "dependencies": "98dbd4a1b31213c29c176b28a1e038bcefb3063784b607abdb3c7c080be4af30",
    "statuses": "06f03faf2f76a772b6d26d12cbd97ec4fcdb2da720c0faa2e28bf8e605f5c3cd",
}
EXPECTED_MAXIMUM = (
    "EXACT_CONDITIONAL_CHART_LEVEL_ANGULAR_CHARACTER_TO_HOPF_WEIGHT_"
    "AND_LATITUDE_CROSSWALK_IDENTIFIED__FRAME_INDEPENDENT_KINEMATIC_"
    "LAW_NATIVE_CARRIER_AND_HOPFION_EMERGENCE_REMAIN_OPEN"
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def verify_sources() -> int:
    records = []
    for line in (HERE / "SOURCE_MANIFEST.sha256").read_text().splitlines():
        expected, relative = line.split("  ", 1)
        path = ROOT / relative
        if not path.is_file() or digest(path) != expected:
            raise AssertionError(f"source mismatch: {relative}")
        records.append(relative)
    if len(records) != 25 or len(set(records)) != 25:
        raise AssertionError("source identity/count mismatch")
    return len(records)


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def row_digest(records: list[dict[str, str]]) -> str:
    payload = json.dumps(
        records, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def mm(left, right):
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def madd(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def inv2(matrix):
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return [
        [matrix[1][1] / determinant, -matrix[0][1] / determinant],
        [-matrix[1][0] / determinant, matrix[0][0] / determinant],
    ]


def neg(matrix):
    return [[-item for item in row] for row in matrix]


def coframe(a, d, s):
    ds = mm(d, s)
    return [
        [a[0][0], a[0][1], F(0), F(0)],
        [a[1][0], a[1][1], F(0), F(0)],
        [ds[0][0], ds[0][1], d[0][0], d[0][1]],
        [ds[1][0], ds[1][1], d[1][0], d[1][1]],
    ]


def independent_algebra() -> dict[str, object]:
    # Different exact-rational anchors and no import of the production code.
    a1 = [[F(2), F(1)], [F(0), F(3)]]
    a2 = [[F(5), F(-2)], [F(0), F(7)]]
    d1 = [[F(3), F(2)], [F(0), F(4)]]
    d2 = [[F(7), F(1)], [F(0), F(5)]]
    s1 = [[F(1), F(2)], [F(-1), F(3)]]
    s2 = [[F(2), F(-1)], [F(4), F(1)]]
    s12 = madd(mm(mm(inv2(d2), s1), a2), s2)
    direct = mm(coframe(a1, d1, s1), coframe(a2, d2, s2))
    predicted = coframe(mm(a1, a2), mm(d1, d2), s12)
    if direct != predicted:
        raise AssertionError("independent complete product failed")

    inverse_s1 = neg(mm(mm(d1, s1), inv2(a1)))
    identity = mm(coframe(a1, d1, s1), coframe(inv2(a1), inv2(d1), inverse_s1))
    expected_identity = [
        [F(int(i == j)) for j in range(4)] for i in range(4)
    ]
    if identity != expected_identity:
        raise AssertionError("independent inverse failed")

    # Diagonal characters multiply even when shear is present.
    if mm(d1, d2)[0][0] != d1[0][0] * d2[0][0]:
        raise AssertionError("first angular diagonal character failed")
    if mm(d1, d2)[1][1] != d1[1][1] * d2[1][1]:
        raise AssertionError("second angular diagonal character failed")

    # A reciprocal diagonal subgroup is not normal under upper shear.
    shear = [[F(1), F(1)], [F(0), F(1)]]
    reciprocal = [[F(1, 2), F(0)], [F(0), F(2)]]
    conjugate = mm(mm(shear, reciprocal), inv2(shear))
    if conjugate[0][1] != F(3, 2):
        raise AssertionError("nonnormal diagonal-subgroup witness failed")

    def compose(left, right):
        return left * right / (
            left * right + (1 - left) * (1 - right)
        )

    # Odds 4 and 9 multiply to 36.
    weight1, weight2, weight12 = F(1, 5), F(1, 10), F(1, 37)
    if compose(weight1, weight2) != weight12:
        raise AssertionError("independent logistic composition failed")
    if compose(weight1, F(1, 2)) != weight1:
        raise AssertionError("independent identity failed")
    if compose(weight1, 1 - weight1) != F(1, 2):
        raise AssertionError("independent inverse failed")

    z1, z2, z12 = F(-3, 5), F(-4, 5), F(-35, 37)
    if (z1 + z2) / (1 + z1 * z2) != z12:
        raise AssertionError("independent latitude composition failed")

    # A rational point on S2 lifts to a metric-null direction.
    n = (F(12, 25), F(16, 25), F(-15, 25))
    if sum(item * item for item in n) != 1:
        raise AssertionError("independent quotient sphere check failed")
    if -F(1) + sum(item * item for item in n) != 0:
        raise AssertionError("independent null lift failed")

    # Same separate Q values, different composed Q values.
    qa = compose(F(3, 4), F(3, 4)) - compose(F(1, 4), F(1, 4))
    qb = compose(F(3, 4), F(2, 3)) - compose(F(1, 4), F(1, 6))
    if qa != F(4, 5) or qb != F(89, 112) or qa == qb:
        raise AssertionError("independent charge-composition catch failed")

    return {
        "complete_group_product_anchors": 1,
        "complete_group_inverse_anchors": 1,
        "diagonal_character_checks": 2,
        "nonnormal_conjugate_off_diagonal": str(conjugate[0][1]),
        "logistic_weight_anchor": str(weight12),
        "latitude_anchor": str(z12),
        "null_section_anchor": [str(item) for item in n],
        "finite_readout_composites": [str(qa), str(qb)],
    }


def validate_records(result, subgroups, dependencies, statuses) -> None:
    if result["schema"] != "udt-coframe-hopf-bridge-audit-v1":
        raise AssertionError("result schema")
    if result["source_count"] != 25:
        raise AssertionError("source count")
    if result["counts"] != {
        "registered_candidates": 8,
        "bridge_dependencies": 11,
        "status_rows": 14,
        "native_carrier_bridges_derived": 0,
        "exact_conditional_seed_bridges": 1,
        "independent_additive_chart_depth_characters": 2,
    }:
        raise AssertionError("result counts")
    if len(subgroups) != 8 or len({row["candidate"] for row in subgroups}) != 8:
        raise AssertionError("subgroup census")
    if len(dependencies) != 11 or len({row["object"] for row in dependencies}) != 11:
        raise AssertionError("dependency matrix")
    if len(statuses) != 14 or len({row["id"] for row in statuses}) != 14:
        raise AssertionError("status ledger")
    if any(
        row["status"] in {"DERIVED", "DERIVED_CONDITIONAL"}
        for row in statuses
        if row["id"] == "S14"
    ):
        raise AssertionError("native bridge promoted")
    by_status = {row["id"]: row for row in statuses}
    if by_status["S02"]["status"] != "OPEN":
        raise AssertionError("ownership promoted")
    if by_status["S06"]["status"] != "OPEN":
        raise AssertionError("phase promoted")
    if by_status["S12"]["status"] != "POSIT":
        raise AssertionError("carrier promoted")
    observed_row_digests = {
        "subgroups": row_digest(subgroups),
        "dependencies": row_digest(dependencies),
        "statuses": row_digest(statuses),
    }
    if observed_row_digests != EXPECTED_ROW_DIGESTS:
        raise AssertionError("semantic row contract")
    if result["maximum_conclusion"] != EXPECTED_MAXIMUM:
        raise AssertionError("bounded maximum")
    algebra = result["algebra"]
    if algebra["reciprocal_angular_subgroup"][
        "diagonal_subset_is_normal_in_upper_triangular_group"
    ]:
        raise AssertionError("nonnormality lost")
    if algebra["conditional_toric_composition"][
        "phase_delta_composition"
    ] != "NOT_PRESENT_IN_POINTWISE_COFRAME_GROUP":
        raise AssertionError("phase invented")
    if algebra["finite_endpoint_readout"][
        "pointwise_group_law_is_hopf_charge_homomorphism"
    ]:
        raise AssertionError("charge homomorphism invented")


def expect_failure(identifier, callback):
    try:
        callback()
    except (AssertionError, KeyError):
        return {
            "catch_id": identifier,
            "result": "PASS",
            "scope": "RECORD_INTEGRITY_MUTATION",
        }
    raise AssertionError(f"mutation passed: {identifier}")


def mutation_catches(result, subgroups, dependencies, statuses):
    catches = []

    def mutated(mutator):
        r = copy.deepcopy(result)
        s = copy.deepcopy(subgroups)
        d = copy.deepcopy(dependencies)
        t = copy.deepcopy(statuses)
        mutator(r, s, d, t)
        validate_records(r, s, d, t)

    mutations = (
        ("M01_SOURCE_COUNT", lambda r, s, d, t: r.__setitem__("source_count", 24)),
        ("M02_DROP_SUBGROUP", lambda r, s, d, t: s.pop()),
        ("M03_DUPLICATE_DEPENDENCY", lambda r, s, d, t: d.append(copy.deepcopy(d[0]))),
        ("M04_DROP_STATUS", lambda r, s, d, t: t.pop()),
        (
            "M05_PROMOTE_NATIVE_BRIDGE",
            lambda r, s, d, t: next(row for row in t if row["id"] == "S14").__setitem__("status", "DERIVED"),
        ),
        (
            "M06_PROMOTE_OWNERSHIP",
            lambda r, s, d, t: next(row for row in t if row["id"] == "S02").__setitem__("status", "DERIVED"),
        ),
        (
            "M07_PROMOTE_PHASE",
            lambda r, s, d, t: next(row for row in t if row["id"] == "S06").__setitem__("status", "DERIVED"),
        ),
        (
            "M08_PROMOTE_CARRIER",
            lambda r, s, d, t: next(row for row in t if row["id"] == "S12").__setitem__("status", "DERIVED"),
        ),
        (
            "M09_FALSE_NORMALITY",
            lambda r, s, d, t: r["algebra"]["reciprocal_angular_subgroup"].__setitem__(
                "diagonal_subset_is_normal_in_upper_triangular_group", True
            ),
        ),
        (
            "M10_INVENT_PHASE",
            lambda r, s, d, t: r["algebra"]["conditional_toric_composition"].__setitem__(
                "phase_delta_composition", "DERIVED_ADDITION"
            ),
        ),
        (
            "M11_FALSE_CHARGE_HOMOMORPHISM",
            lambda r, s, d, t: r["algebra"]["finite_endpoint_readout"].__setitem__(
                "pointwise_group_law_is_hopf_charge_homomorphism", True
            ),
        ),
        (
            "M12_OVERCLAIM_MAXIMUM",
            lambda r, s, d, t: r.__setitem__(
                "maximum_conclusion", "NATIVE_HOPFION_EMERGENCE_DERIVED"
            ),
        ),
        (
            "M13_FALSE_SUBGROUP_NORMALITY_TEXT",
            lambda r, s, d, t: next(
                row
                for row in s
                if row["candidate"] == "POSITIVE_DIAGONAL_ANGULAR_SUBSET"
            ).__setitem__("invariance", "NORMAL_UNDER_ANGULAR_SHEAR"),
        ),
        (
            "M14_PROMOTE_SCALAR_ANGULAR_OWNERSHIP",
            lambda r, s, d, t: next(
                row
                for row in d
                if row["object"]
                == "identification of positional scalar phi with angular depth"
            ).__setitem__("ruling", "DERIVED"),
        ),
        (
            "M15_DEMOTE_NONNORMALITY_STATUS",
            lambda r, s, d, t: next(
                row for row in t if row["id"] == "S04"
            ).__setitem__("status", "OPEN"),
        ),
        (
            "M16_INVENT_PHYSICAL_DESCENT",
            lambda r, s, d, t: next(
                row
                for row in d
                if row["object"]
                == "descent of chart multiplication to physical coframe/metric classes"
            ).__setitem__("metric_or_group_supply", "DERIVED"),
        ),
    )
    for identifier, mutator in mutations:
        catches.append(expect_failure(identifier, lambda m=mutator: mutated(m)))
    return catches


def main() -> None:
    source_count = verify_sources()
    result = json.loads((HERE / "RESULT.json").read_text())
    subgroups = rows("SUBGROUP_CENSUS.tsv")
    dependencies = rows("BRIDGE_DEPENDENCY_MATRIX.tsv")
    statuses = rows("STATUS_LEDGER.tsv")
    validate_records(result, subgroups, dependencies, statuses)
    algebra = independent_algebra()
    catches = mutation_catches(result, subgroups, dependencies, statuses)
    with (HERE / "CATCH_PROOFS.tsv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("catch_id", "result", "scope"),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(catches)
    output = {
        "schema": "udt-coframe-hopf-bridge-independent-v1",
        "status": "PASS",
        "sources_checked": source_count,
        "independent_algebra": algebra,
        "record_counts": {
            "subgroups": len(subgroups),
            "dependencies": len(dependencies),
            "statuses": len(statuses),
        },
        "mutation_catches": {"passed": len(catches), "total": len(catches)},
        "result_sha256": digest(HERE / "RESULT.json"),
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
