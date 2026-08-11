#!/usr/bin/env python3
"""Fail-closed semantic and census verification for G75."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    shapes = table("SHAPE_ATLAS.tsv")
    profiles = table("PROFILE_ATLAS.tsv")
    checks = {
        "production_pass": result["status"] == "PASS",
        "independent_pass": independent["status"] == "PASS",
        "shape_count": len(shapes) == result["shape_count"] == 49,
        "profile_count": len(profiles) == result["profile_count"] == 591,
        "unique_shapes": len({row["shape_id"] for row in shapes}) == 49,
        "unique_profiles": len({row["profile_id"] for row in profiles}) == 591,
        "behavior_counts": Counter(row["behavior_class"] for row in shapes) == Counter(result["behavior_counts"]),
        "all_center_smooth": all(row["center_status"] == "CENTER_C_INFINITY" for row in profiles),
        "all_signature_regular": all(row["signature_status"] == "LORENTZ_REGULAR_ALL_X" for row in profiles),
        "all_unselected": all(row["physical_status"] == "CHOSE_CONTROL_NOT_SELECTED" for row in profiles),
        "scale_symbolic": result["scale_status"] == "R_POSITIVE_SYMBOLIC_NOT_SELECTED",
        "physical_owner_open": result["physical_owner"] == "OPEN_NO_OWNER",
        "no_G74_repair": result["original_G74_blocked_profiles_repaired"] is False,
        "three_zero_controls": sum(row["shape_id"] == "ZERO" for row in profiles) == 3,
        "588_nonzero_controls": sum(row["shape_id"] != "ZERO" for row in profiles) == 588,
        "analogs_present": set(result["new_even_analog_shape_ids"]) == {"persistent_even", "endpoint_taper_even", "sign_change_even"},
    }
    assert all(checks.values()), [name for name, value in checks.items() if not value]
    payload = {
        "schema": "udt-cmb-g75-package-verification-v1",
        "status": "PASS",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "protected_draft_read": False,
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
