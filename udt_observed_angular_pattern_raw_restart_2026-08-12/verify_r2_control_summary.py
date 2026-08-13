#!/usr/bin/env python3
"""Independent checks of the load-bearing R2 control-summary statements."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "R2_CONTROL_SUMMARY.json"
OUTPUT = ROOT / "R2_CONTROL_SUMMARY_VERIFICATION.json"


def rows(name):
    with (ROOT / name).open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def quantile(values, probability):
    ordered = sorted(float(x) for x in values)
    position = (len(ordered) - 1) * probability
    lo = math.floor(position)
    hi = math.ceil(position)
    if lo == hi:
        return ordered[lo]
    return ordered[lo] * (hi - position) + ordered[hi] * (position - lo)


def close(a, b):
    return math.isclose(float(a), float(b), rel_tol=2e-14, abs_tol=2e-16)


def main():
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    summary = json.loads(SOURCE.read_text())
    controls = rows("R2_CONSISTENCY_SUMMARY.tsv")
    descriptors = rows("R2_DESCRIPTOR_ATLAS.tsv")

    expected_counts = {"RANDOM_DENSITY": 1552, "WEIGHT_LANE": 1746, "CAP": 1164}
    headline = {}
    for kind, count in expected_counts.items():
        subset = [row for row in controls if row["comparison"] == kind]
        assert len(subset) == count
        values = [float(row["rms_difference"]) for row in subset]
        observed = summary[{"RANDOM_DENSITY": "random_density", "WEIGHT_LANE": "weight_lane", "CAP": "cap"}[kind]]["rms_difference"]["overall"]
        assert observed["count"] == count
        for name, p in (("min", 0.0), ("q25", 0.25), ("median", 0.5), ("q75", 0.75), ("q90", 0.9), ("q95", 0.95), ("max", 1.0)):
            assert close(observed[name], quantile(values, p))
        headline[kind] = observed

    random_rows = [row for row in controls if row["comparison"] == "RANDOM_DENSITY"]
    paired = {}
    for row in random_rows:
        key = (row["sample"], row["cap_or_pair"], row["factor"], row["group"], row["lane_or_pair"])
        paired.setdefault(key, {})[row["ratio_or_pair"]] = float(row["rms_difference"])
    assert len(paired) == 776
    no_farther = sum(item["10-20"] <= item["5-20"] for item in paired.values())
    assert no_farther == summary["random_density_convergence"]["overall"]["ten_x_no_farther_count"] == 776

    factor_medians = {}
    for kind, summary_name in (("RANDOM_DENSITY", "random_density"), ("WEIGHT_LANE", "weight_lane"), ("CAP", "cap")):
        factor_medians[kind] = {}
        for factor in ("1", "2", "4"):
            values = [float(row["rms_difference"]) for row in controls if row["comparison"] == kind and row["factor"] == factor]
            value = quantile(values, 0.5)
            assert close(value, summary[summary_name]["rms_difference"]["by_factor"][factor]["median"])
            factor_medians[kind][factor] = value

    descriptor_fields = (
        "rms", "total_variation", "first_difference_rms", "second_difference_rms",
        "strict_max_count", "strict_min_count", "plateau_count", "zero_crossing_count",
    )
    assert len(descriptors) == summary["descriptors"]["count"] == 2328
    assert all(math.isfinite(float(row[field])) for row in descriptors for field in descriptor_fields)
    assert sum(int(row["raw_lag_degenerate"]) for row in descriptors) == summary["descriptors"]["raw_lag_degenerate_count"] == 0
    assert sum(int(row["difference_lag_degenerate"]) for row in descriptors) == summary["descriptors"]["difference_lag_degenerate_count"] == 0
    for field in descriptor_fields:
        value = quantile([row[field] for row in descriptors], 0.5)
        assert close(value, summary["descriptors"]["overall"][field]["median"])

    result = {
        "status": "PASS",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "control_row_count": len(controls),
        "descriptor_row_count": len(descriptors),
        "headline_rms_distributions_independently_recomputed": headline,
        "random_density_matched_query_count": len(paired),
        "ten_x_no_farther_count": no_farther,
        "factor_medians_independently_recomputed": factor_medians,
        "descriptor_headline_medians_independently_recomputed": True,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS: independently verified R2 control-summary headlines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
