#!/usr/bin/env python3
"""Independent semantic/numerical replay of the attributed corrected-atlas readout."""

from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
ATLAS = ROOT / "corrected_full_atlas_certified.json"
READOUT = ROOT / "attributed_readout.json"
EXPECTED_ATLAS = "042138fb73cc9f3bef4faf97fc0357f2a2f079daced5e39d6532c4a6f770dfbb"
EXPECTED_READOUT = "1d733a82beaa66cdefd61f1f2a3a702a6cb18f2cd70ae5c8ada025c87dbba156"
PEAKS = np.asarray([220.6, 538.1, 809.8, 1147.8, 1446.8, 1779.0, 2075.0])
TROUGHS = np.asarray([416.3, 675.5, 1001.1, 1290.0, 1623.8, 1919.0, 2241.0])


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fit(values: np.ndarray) -> tuple[float, float, float]:
    matrix = np.vstack((values, np.ones(7))).T
    scale, offset = np.linalg.solve(matrix.T @ matrix, matrix.T @ PEAKS)
    residual = np.max(np.abs((scale * values + offset - PEAKS) / PEAKS))
    return float(scale), float(offset), float(residual)


def replay(atlas: dict[str, object]) -> dict[str, object]:
    morphology: Counter[str] = Counter()
    line_counts: Counter[str] = Counter()
    residuals: dict[str, list[float]] = defaultdict(list)
    crowding: dict[str, list[int]] = defaultdict(list)
    conventions = 0
    spectral = [row for row in atlas["rows"] if float(row["hbar"]) > 0.0]
    for row in spectral:
        positive = {
            "mminus": np.asarray(row["omega_mminus"]),
            "m0": np.asarray(row["omega_m0"]),
            "mplus": np.asarray(row["omega_mplus"]),
        }
        row_conventions = ("POSITIVE_ONLY", "ZERO_INCLUDED") if row["wall"] == "N" else ("POSITIVE_ONLY",)
        for convention in row_conventions:
            conventions += 1
            compared = {name: values[:7] for name, values in positive.items()}
            if convention == "ZERO_INCLUDED":
                compared["m0"] = np.r_[0.0, positive["m0"][:6]]
            fitted = {name: fit(values) for name, values in compared.items()}
            for name, (_, _, residual) in fitted.items():
                residuals[name].append(residual)
                line_counts[name] += int(residual <= 0.031)
            scale, offset, _ = fitted["m0"]
            ell0 = scale * compared["m0"] + offset
            ellm = scale * compared["mminus"] + offset
            ellp = scale * compared["mplus"] + offset
            left, right = TROUGHS[:-1], TROUGHS[1:]
            basin = np.minimum(PEAKS[1:] - left, right - PEAKS[1:])
            displacement = np.maximum(np.abs(ellm[1:] - ell0[1:]), np.abs(ellp[1:] - ell0[1:]))
            half_split = 0.5 * np.abs(ellp[1:] - ellm[1:])
            if np.all(basin - displacement >= 0.0):
                morphology["FULL_CENTERED_MULTIPLET_CONTAINMENT"] += 1
            elif np.all(basin - half_split >= 0.0):
                morphology["SPLITTING_ONLY"] += 1
            else:
                morphology["BASIN_MISMATCH"] += 1
            all_lines = np.concatenate(tuple(positive.values()))
            for name, (anchor_scale, anchor_offset, _) in fitted.items():
                projected = anchor_scale * all_lines + anchor_offset
                crowding[name].extend(int(np.count_nonzero((projected >= lo) & (projected <= hi))) for lo, hi in zip(left, right))
    return {
        "spectral_identities": len(spectral),
        "convention_rows": conventions,
        "historical_pairing_morphology_counts": dict(morphology),
        "standalone_historical_3p1_line_counts": dict(line_counts),
        "residual_extrema": {name: (min(vals), max(vals)) for name, vals in residuals.items()},
        "crowding_extrema": {name: (min(vals), max(vals)) for name, vals in crowding.items()},
    }


def validate(payload: dict[str, object], expected: dict[str, object]) -> list[str]:
    errors: list[str] = []
    rows = payload.get("rows", [])
    if len(rows) != 630:
        errors.append("row count")
    if sum(row.get("neumann_mode_convention") == "ZERO_INCLUDED" for row in rows) != 210:
        errors.append("conventions")
    if any(set(row.get("standalone_families", {})) != {"mminus", "m0", "mplus"} for row in rows):
        errors.append("families")
    if any("no physical multiplet" not in row.get("historical_pairing_diagnostic", {}).get("pairing_caveat", "") for row in rows):
        errors.append("pairing caveat")
    if any(len(counts) != 6 for row in rows for counts in row.get("all_24_positive_line_crowding_by_anchor", {}).values()):
        errors.append("crowding")
    source = payload.get("source", {})
    if "Planck Collaboration" not in source.get("citation", "") or len(source.get("peaks", [])) != 7:
        errors.append("source")
    summary = payload.get("summary", {})
    for name in ("spectral_identities", "convention_rows", "historical_pairing_morphology_counts", "standalone_historical_3p1_line_counts"):
        if summary.get(name) != expected[name]:
            errors.append(name)
    return errors


def main() -> None:
    keys: dict[str, bool] = {}
    keys["ARV1_input_hashes"] = digest(ATLAS) == EXPECTED_ATLAS and digest(READOUT) == EXPECTED_READOUT
    atlas = json.loads(ATLAS.read_text())
    payload = json.loads(READOUT.read_text())
    expected = replay(atlas)
    errors = validate(payload, expected)
    keys["ARV2_independent_counts"] = not errors
    keys["ARV3_no_full_centered_rows"] = expected["historical_pairing_morphology_counts"] == {
        "SPLITTING_ONLY": 503, "BASIN_MISMATCH": 127
    }
    keys["ARV4_standalone_line_counts"] = expected["standalone_historical_3p1_line_counts"] == {
        "mminus": 63, "m0": 4, "mplus": 78
    }
    reported_residuals = payload["summary"]["standalone_max_abs_fractional_residual"]
    keys["ARV5_residual_extrema"] = all(
        abs(expected["residual_extrema"][name][0] - reported_residuals[name]["minimum"]) < 2.0e-12
        and abs(expected["residual_extrema"][name][1] - reported_residuals[name]["maximum"]) < 2.0e-12
        for name in ("mminus", "m0", "mplus")
    )
    reported_crowd = payload["summary"]["line_crowding_counts_per_trough_basin"]
    keys["ARV6_crowding_extrema"] = all(
        expected["crowding_extrema"][name][0] == reported_crowd[name]["minimum"]
        and expected["crowding_extrema"][name][1] == reported_crowd[name]["maximum"]
        for name in ("mminus", "m0", "mplus")
    )

    mutations: list[tuple[str, dict[str, object]]] = []
    missing = copy.deepcopy(payload); missing["rows"].pop(); mutations.append(("missing", missing))
    convention = copy.deepcopy(payload); convention["rows"][0]["neumann_mode_convention"] = "ZERO_INCLUDED"; mutations.append(("convention", convention))
    family = copy.deepcopy(payload); family["rows"][0]["standalone_families"].pop("mplus"); mutations.append(("family", family))
    caveat = copy.deepcopy(payload); caveat["rows"][0]["historical_pairing_diagnostic"]["pairing_caveat"] = ""; mutations.append(("caveat", caveat))
    crowd = copy.deepcopy(payload); crowd["rows"][0]["all_24_positive_line_crowding_by_anchor"]["m0"].pop(); mutations.append(("crowd", crowd))
    source = copy.deepcopy(payload); source["source"]["citation"] = ""; mutations.append(("source", source))
    summary = copy.deepcopy(payload); summary["summary"]["convention_rows"] = 629; mutations.append(("summary", summary))
    catches = {name: bool(validate(mutated, expected)) for name, mutated in mutations}
    keys["ARV7_all_mutation_catches"] = len(catches) == 7 and all(catches.values())

    for name, value in keys.items():
        print(f"KEY {name}: {value}")
    result = {
        "keys": keys,
        "independent_replay": expected,
        "base_errors": errors,
        "mutation_catches": catches,
    }
    output = ROOT / "attributed_verification_result.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(expected, indent=2, sort_keys=True))
    print(f"WROTE {output} SHA256 {digest(output)}")
    if not all(keys.values()):
        raise SystemExit("attributed verification failed")


if __name__ == "__main__":
    main()
