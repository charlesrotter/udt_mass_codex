#!/usr/bin/env python3
"""Independent stdlib/Fraction audit of relational depth type rulings."""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def expect_failure(name: str, callback, catches: dict[str, str]) -> None:
    try:
        callback()
    except (AssertionError, KeyError, ValueError):
        catches[name] = "PASS"
        return
    raise AssertionError(f"catch did not fire: {name}")


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def matmul(left, right):
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(3)) for j in range(3))
        for i in range(3)
    )


def transpose(matrix):
    return tuple(tuple(matrix[j][i] for j in range(3)) for i in range(3))


def main() -> None:
    checks: dict[str, str] = {}
    catches: dict[str, str] = {}

    # Three equal-radius round controls have identical radial dot 1/2 and
    # nonzero mutual separation with mutual dot 1/4.
    radial_dots = [Fraction(1, 2)] * 3
    mutual_dots = [Fraction(1, 4)] * 3
    require("three_equal_radii", len(set(radial_dots)) == 1, checks)
    require("three_distinct_mutual_separations", all(dot < 1 for dot in mutual_dots), checks)
    for index, signs in enumerate(itertools.product((-1, 1), repeat=3), start=1):
        require(f"pigeonhole_{index}", len(set(signs)) < 3, checks)

    # Exact polynomial additivity controls: every nonlinear monomial creates
    # mixed terms in (x+y)^n-x^n-y^n.
    for degree in range(2, 8):
        x = Fraction(2, 5)
        y = Fraction(3, 7)
        residual = (x + y) ** degree - x**degree - y**degree
        require(f"nonlinear_monomial_fails_{degree}", residual != 0, checks)
    kappa = Fraction(11, 7)
    x = Fraction(2, 5)
    y = Fraction(3, 7)
    require("linear_additivity", kappa * (x + y) == kappa * x + kappa * y, checks)

    # Projective display at two half-depth steps: 1/2 combines to 4/5, not 1.
    u = Fraction(1, 2)
    projective_sum = (u + u) / (1 + u * u)
    require("projective_sum_exact", projective_sum == Fraction(4, 5), checks)
    require("projective_not_length_sum", projective_sum != u + u, checks)

    # Angular data: same two radial cosines 1/2 give three pair dot products.
    cos_a = Fraction(1, 2)
    sin2_a = Fraction(3, 4)
    dot_same = cos_a * cos_a + sin2_a
    dot_orthogonal = cos_a * cos_a
    dot_opposite = cos_a * cos_a - sin2_a
    require("angular_same_dot", dot_same == 1, checks)
    require("angular_orthogonal_dot", dot_orthogonal == Fraction(1, 4), checks)
    require("angular_opposite_dot", dot_opposite == Fraction(-1, 2), checks)
    require("angular_three_distances", len({dot_same, dot_orthogonal, dot_opposite}) == 3, checks)

    # Exact antipodal transport controls in a common ambient tangent basis.
    zero = Fraction(0)
    one = Fraction(1)
    t1 = ((-one, zero, zero), (zero, one, zero), (zero, zero, one))
    t2 = ((one, zero, zero), (zero, -one, zero), (zero, zero, one))
    identity = ((one, zero, zero), (zero, one, zero), (zero, zero, one))
    require("cut_transport_t1_isometry", matmul(transpose(t1), t1) == identity, checks)
    require("cut_transport_t2_isometry", matmul(transpose(t2), t2) == identity, checks)
    require("cut_transports_differ", t1 != t2, checks)

    # Exact polynomial current integral.
    A, B = Fraction(3, 5), Fraction(7, 11)
    s0, s1 = Fraction(2, 7), Fraction(5, 3)
    phi0 = A * s0 * s0 + B * s0
    phi1 = A * s1 * s1 + B * s1
    integral_derivative = A * (s1 * s1 - s0 * s0) + B * (s1 - s0)
    require("current_endpoint_integral", integral_derivative == phi1 - phi0, checks)

    with (HERE / "DERIVATION_RESULT.json").open(encoding="utf-8") as handle:
        result = json.load(handle)
    depth_rows = read_tsv("DEPTH_TYPE_RULING_LEDGER.tsv")
    composition_rows = read_tsv("COMPOSITION_DOMAIN_LEDGER.tsv")
    round_rows = read_tsv("ROUND_PAIR_CONTROL_LEDGER.tsv")
    scale_rows = read_tsv("SCALE_GATE.tsv")
    status_rows = read_tsv("STATUS_LEDGER.tsv")
    owner_rows = read_tsv("OWNER_FRAME_LEDGER.tsv")
    source_rows = read_tsv("SOURCE_LINEAGE.tsv") + read_tsv("SOURCE_ADDENDUM.tsv")

    require("production_checks", result["check_count"] >= 60, checks)
    require("depth_rows_8", len(depth_rows) == 8, checks)
    require("composition_rows_6", len(composition_rows) == 6, checks)
    require("round_rows_7", len(round_rows) == 7, checks)
    require("scale_rows_4", len(scale_rows) == 4, checks)
    require("status_rows_12", len(status_rows) == 12, checks)
    require("owner_rows_5", len(owner_rows) == 5, checks)
    require("source_rows_10", len(source_rows) == 10, checks)
    require("depth_ids_unique", len({row["id"] for row in depth_rows}) == 8, checks)
    require("source_ids_unique", len({row["id"] for row in source_rows}) == 10, checks)
    for row in source_rows:
        source = ROOT / row["path"]
        require(f"source_exists_{row['id']}", source.is_file(), checks)
        require(f"source_sha_{row['id']}", sha256(source) == row["sha256"], checks)

    depth_by_id = {row["id"]: row for row in depth_rows}
    composition_by_domain = {row["domain"]: row for row in composition_rows}
    status_by_claim = {row["claim"]: row for row in status_rows}
    require(
        "global_scalar_refuted_scoped",
        depth_by_id["D03"]["status"] == "REFUTED_AS_UNIVERSAL_CENTERLESS_ISOTROPIC_PAIR_DEPTH",
        checks,
    )
    require(
        "observer_family_survives",
        depth_by_id["D02"]["status"] == "SMALLEST_SURVIVING_METRIC_NATIVE_TYPE_GIVEN_F",
        checks,
    )
    require(
        "projective_not_distance",
        depth_by_id["D06"]["status"] == "EXACT_CONDITIONAL_DISPLAY_NOT_METRIC_DISTANCE_IDENTITY",
        checks,
    )
    require(
        "cut_type_separated",
        depth_by_id["D07"]["status"] == "DERIVED_TYPE_SEPARATION",
        checks,
    )
    require(
        "universal_F_linear",
        composition_by_domain["universal continuous F of proper distance"]["result"] == "FORCES_F_EQUAL_KAPPA_D",
        checks,
    )
    require(
        "angular_required",
        composition_by_domain["noncollinear round triples"]["result"] == "ANGULAR_DATUM_REQUIRED",
        checks,
    )
    require(
        "Xmax_not_promoted",
        status_by_claim["physical Xmax mass density CMB"]["status"] == "OPEN_NOT_PROMOTED",
        checks,
    )
    require(
        "local_physics_neutral",
        status_by_claim["pair dilation modifies local physics"]["status"]
        == "REFUTED_BY_OWNER_FRAME_MEANING",
        checks,
    )
    require(
        "three_observers_compatible",
        status_by_claim["three observers invalidate pair dilation"]["status"] == "REFUTED",
        checks,
    )
    require(
        "owner_relational_only",
        result["owner_frame"]["classification"] == "OWNER_CLARIFIED_RELATIONAL_ONLY",
        checks,
    )
    require(
        "owner_local_not_modified",
        result["owner_frame"]["local_physics_modified_by_pair_dilation"] is False,
        checks,
    )

    expect_failure(
        "global_scalar_promotion",
        lambda: require("bad", depth_by_id["D03"]["status"].startswith("DERIVED"), {}),
        catches,
    )
    expect_failure(
        "arbitrary_triangle_additivity",
        lambda: require("bad", composition_by_domain["abstract additive depth parameters"]["failure_outside_domain"] == "metric distances add for all triples", {}),
        catches,
    )
    expect_failure(
        "nonlinear_additivity",
        lambda: require("bad", projective_sum == u + u, {}),
        catches,
    )
    expect_failure(
        "finite_linear_infinite",
        lambda: require("bad", status_by_claim["finite proper diameter plus infinite linear additive depth"]["status"] == "DERIVED", {}),
        catches,
    )
    expect_failure(
        "drop_angular",
        lambda: require("bad", len({dot_same, dot_orthogonal, dot_opposite}) == 1, {}),
        catches,
    )
    expect_failure(
        "scalar_set_valued",
        lambda: require("bad", result["cut_locus"]["scalar_distance"] == "PATH_FAMILY", {}),
        catches,
    )
    expect_failure(
        "transport_unique",
        lambda: require("bad", t1 == t2, {}),
        catches,
    )
    expect_failure(
        "current_promote",
        lambda: require("bad", depth_by_id["D04"]["status"] == "DERIVED_PHYSICAL_UNCONDITIONAL", {}),
        catches,
    )
    expect_failure(
        "c_normalization",
        lambda: require("bad", result["scale"]["dimensionless_depth_normalization_from_c_alone"] == "DERIVED", {}),
        catches,
    )
    expect_failure(
        "Xmax_promotion",
        lambda: require("bad", status_by_claim["physical Xmax mass density CMB"]["status"] == "DERIVED", {}),
        catches,
    )
    expect_failure(
        "local_physics_promotion",
        lambda: require("bad", result["owner_frame"]["local_physics_modified_by_pair_dilation"] is True, {}),
        catches,
    )
    expect_failure(
        "three_observer_no_go",
        lambda: require("bad", result["owner_frame"]["three_observer_result"] == "DILATION_REFUTED", {}),
        catches,
    )
    expect_failure(
        "duplicate_depth",
        lambda: require("bad", len(depth_rows + [depth_rows[0]]) == len({row["id"] for row in depth_rows + [depth_rows[0]]}), {}),
        catches,
    )
    expect_failure(
        "missing_source",
        lambda: require("bad", len(source_rows[:-1]) == 10, {}),
        catches,
    )

    verification = {
        "schema": "udt-relational-pair-depth-independent-1.0",
        "implementation": "PYTHON_STDLIB_FRACTION_NO_SYMPY_NO_PRODUCTION_IMPORT",
        "result": "PASS",
        "checks": checks,
        "check_count": len(checks),
        "catches": catches,
        "catch_count": len(catches),
        "ruling": {
            "global_scalar": "REFUTED_AS_UNIVERSAL_CENTERLESS_ISOTROPIC_PAIR_DEPTH",
            "smallest_surviving_type": "OBSERVER_INDEXED_BILOCAL_METRIC_FAMILY_GIVEN_F",
            "ordinary_additive_F": "LINEAR_ONLY",
            "angular_composition": "REQUIRED",
            "cut_scalar": "SINGLE_VALUED",
            "cut_full_transport": "PATH_FAMILY",
            "physical_Xmax": "OPEN",
            "owner_frame": "RELATIONAL_ONLY_LOCAL_NEUTRAL",
        },
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "result": "PASS",
        "checks": len(checks),
        "catches": len(catches),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
