#!/usr/bin/env python3
"""Complete outcome-blind aggregation of the preregistered R2 controls."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "R2_CONTROL_SUMMARY.json"
Q = (0.0, 0.25, 0.5, 0.75, 0.9, 0.95, 1.0)
QN = ("min", "q25", "median", "q75", "q90", "q95", "max")


def read(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def stats(values) -> dict:
    x = np.asarray(list(values), dtype=np.float64)
    assert x.size and np.all(np.isfinite(x))
    return {"count": int(x.size), **{k: float(v) for k, v in zip(QN, np.quantile(x, Q))}}


def grouped(rows, field: str, keys: tuple[str, ...]) -> dict:
    groups = defaultdict(list)
    for row in rows:
        groups["|".join(row[k] for k in keys)].append(float(row[field]))
    return {key: stats(groups[key]) for key in sorted(groups)}


def comparison_summary(rows: list[dict[str, str]], kind: str, group_axes: tuple[tuple[str, ...], ...]) -> dict:
    subset = [row for row in rows if row["comparison"] == kind]
    out = {}
    for field in ("max_abs_difference", "rms_difference"):
        out[field] = {"overall": stats(float(row[field]) for row in subset)}
        for keys in group_axes:
            out[field]["by_" + "_".join(keys)] = grouped(subset, field, keys)
    return out


def convergence(rows: list[dict[str, str]]) -> dict:
    random_rows = [row for row in rows if row["comparison"] == "RANDOM_DENSITY"]
    values = {}
    for row in random_rows:
        key = (row["sample"], row["cap_or_pair"], row["factor"], row["group"], row["lane_or_pair"])
        values.setdefault(key, {})[row["ratio_or_pair"]] = float(row["rms_difference"])
    flags = []
    for key, item in sorted(values.items()):
        assert set(item) == {"5-20", "10-20"}
        flags.append((key, item["10-20"] <= item["5-20"]))

    def summarize_flags(chosen) -> dict:
        chosen = list(chosen)
        passed = sum(flag for _, flag in chosen)
        return {"count": len(chosen), "ten_x_no_farther_count": int(passed), "fraction": passed / len(chosen)}

    out = {"overall": summarize_flags(flags)}
    axes = {"sample": 0, "cap": 1, "factor": 2, "lane": 4}
    for name, index in axes.items():
        grouped_flags = defaultdict(list)
        for key, flag in flags:
            grouped_flags[key[index]].append((key, flag))
        out["by_" + name] = {k: summarize_flags(grouped_flags[k]) for k in sorted(grouped_flags)}
    return out


def descriptor_summary(rows: list[dict[str, str]]) -> dict:
    fields = (
        "rms", "total_variation", "first_difference_rms", "second_difference_rms",
        "strict_max_count", "strict_min_count", "plateau_count", "zero_crossing_count",
    )
    parsed = []
    for row in rows:
        item = dict(row)
        for field in fields:
            item[field] = float(row[field])
        parsed.append(item)

    def block(subset) -> dict:
        subset = list(subset)
        return {field: stats(row[field] for row in subset) for field in fields}

    out = {
        "count": len(parsed),
        "all_selected_fields_finite": bool(all(np.isfinite(row[field]) for row in parsed for field in fields)),
        "raw_lag_degenerate_count": sum(int(row["raw_lag_degenerate"]) for row in parsed),
        "difference_lag_degenerate_count": sum(int(row["difference_lag_degenerate"]) for row in parsed),
        "overall": block(parsed),
    }
    for name in ("sample", "factor"):
        groups = defaultdict(list)
        for row in parsed:
            groups[row[name]].append(row)
        out["by_" + name] = {key: block(groups[key]) for key in sorted(groups)}
    return out


def main() -> int:
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    controls = read("R2_CONSISTENCY_SUMMARY.tsv")
    descriptors = read("R2_DESCRIPTOR_ATLAS.tsv")
    assert len(controls) == 4462 and len(descriptors) == 2328
    result = {
        "status": "OBSERVED__OUTCOME_BLIND_CONTROL_SUMMARY__NO_SIGNIFICANCE_CLAIM",
        "random_density": comparison_summary(
            controls, "RANDOM_DENSITY", (("ratio_or_pair",), ("sample",), ("factor",))
        ),
        "weight_lane": comparison_summary(
            controls, "WEIGHT_LANE", (("lane_or_pair",), ("sample",), ("factor",))
        ),
        "cap": comparison_summary(
            controls, "CAP", (("sample",), ("factor",), ("lane_or_pair",))
        ),
        "random_density_convergence": convergence(controls),
        "descriptors": descriptor_summary(descriptors),
        "forbidden_inference": "No feature, scale, significance, BAO, UDT, CMB, or X_max inference.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS: wrote complete outcome-blind R2 control summary")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
