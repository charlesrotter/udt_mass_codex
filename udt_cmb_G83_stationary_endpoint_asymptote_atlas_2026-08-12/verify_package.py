#!/usr/bin/env python3
"""Fail-closed verification of the banked G83 package."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ALLOWED_STATUSES = {
    "ENDPOINT_REGULAR_NO_CAUSTIC", "ENDPOINT_AFTER_CAUSTIC", "TURNING_NO_ENDPOINT",
    "AFFINE_CAP_NO_ENDPOINT", "SOLVER_FAILURE", "NUMERIC_NONFINITE_OR_SIGNATURE_FAILURE",
}
EXPECTED_COUNTS = {
    "ENDPOINT_REGULAR_NO_CAUSTIC": 516,
    "TURNING_NO_ENDPOINT": 18,
    "AFFINE_CAP_NO_ENDPOINT": 57,
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def validate_source_manifest() -> None:
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == 14
    for row in rows:
        path = ROOT / row["path"]
        assert path.is_file() and digest(path) == row["sha256"]


def validate_strict(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 591
    assert len({row["profile_id"] for row in rows}) == 591
    assert all(row["finite_positive_lapse"] == "true" for row in rows)
    assert all(float(row["min_A_on_0_1"]) > 0.0 for row in rows)
    assert all(math.isfinite(float(row["phi_receiver_to_x_1"])) for row in rows)
    assert {row["strict_domain_asymptote_status"] for row in rows} == {
        "NO_INFINITE_STATIONARY_DEPTH_ON_REGISTERED_DOMAIN"
    }


def validate_paths(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 591
    identities = [(row["profile_id"], row["approach_power"]) for row in rows]
    assert len(set(identities)) == 591
    assert {row["status"] for row in rows} <= ALLOWED_STATUSES
    assert Counter(row["status"] for row in rows) == Counter(EXPECTED_COUNTS)
    assert Counter(row["approach_power"] for row in rows) == Counter({"4": 197, "8": 197, "12": 197})
    reached = [row for row in rows if row["endpoint_reached"].lower() == "true"]
    assert len(reached) == 516
    assert all(row["numerically_certified"].lower() == "true" for row in reached)
    assert all(row["caustic_sign_change_sampled"].lower() == "false" for row in reached)
    for row in reached:
        for field in ("null_residual", "screen_gram_residual", "screen_ray_residual", "p_t_residual", "p_psi_residual"):
            assert float(row[field]) <= 1.0e-7
    unreached = [row for row in rows if row["endpoint_reached"].lower() != "true"]
    assert len(unreached) == 75
    assert all(row["numerically_certified"].lower() != "true" for row in unreached)


def validate_recenter(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 12
    assert len({(row["receiver_x"], row["approach_power"]) for row in rows}) == 12
    limits_by_receiver: dict[str, set[str]] = {}
    for row in rows:
        limits_by_receiver.setdefault(row["receiver_x"], set()).add(row["proper_limit_over_R"])
        assert float(row["A_source"]) > 0.0
        assert float(row["c_eff_source_over_receiver"]) > 0.0
        assert row["ownership"] == "FREE_AND_EXPLORED_CONTINUATION_NOT_X_MAX"
    assert all(len(values) == 1 for values in limits_by_receiver.values())
    assert len({next(iter(values)) for values in limits_by_receiver.values()}) == 4


def validate_independent() -> None:
    payload = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    assert payload["all_passed"] is True
    assert payload["source_hashes_passed"] is True
    assert payload["radau_rows"] == payload["radau_passed"] == 18
    assert payload["exact_scalar_checks"]["phi_limit"] == "POSITIVE_INFINITY"
    assert payload["exact_scalar_checks"]["c_eff_ratio_limit"] == "ZERO"
    assert payload["exact_scalar_checks"]["receiver_dependent"] is True


def validate_semantics() -> None:
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert "no physical profile" in result["maximum_conclusion"]
    ledger = {row["claim"]: row for row in read_tsv(HERE / "STATUS_LEDGER.tsv")}
    assert ledger["AM_lapse_selects_physical_X_max"]["status"] == "OPEN"
    assert ledger["physical_X_max_value"]["status"] == "OPEN"
    assert ledger["physical_CMB_conclusion"]["status"] == "OPEN"


def main() -> None:
    validate_source_manifest()
    validate_strict(read_tsv(HERE / "STRICT_DOMAIN_ATLAS.tsv"))
    validate_paths(read_tsv(HERE / "CONTINUED_PATH_ATLAS.tsv"))
    validate_recenter(read_tsv(HERE / "RECENTERED_ENDPOINT_LIMIT_ATLAS.tsv"))
    validate_independent()
    validate_semantics()
    payload = {
        "schema": "UDT_CMB_G83_PACKAGE_VERIFICATION_V1",
        "all_passed": True,
        "source_rows": 14,
        "strict_rows": 591,
        "path_rows": 591,
        "status_counts": EXPECTED_COUNTS,
        "reached_and_certified": 516,
        "independent_radau_rows": 18,
        "physical_X_max_status": "OPEN",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
