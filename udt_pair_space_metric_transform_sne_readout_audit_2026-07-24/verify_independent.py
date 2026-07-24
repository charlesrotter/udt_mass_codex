#!/usr/bin/env python3
"""Independent algebra and direct-solve SNe verification."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(checks: dict[str, str], name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_inputs() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    catalog = np.genfromtxt(
        ROOT / "Data" / "Pantheon+SH0ES.dat",
        names=True,
        dtype=None,
        encoding=None,
    )
    z_all = np.asarray(catalog["zHD"], dtype=float)
    magnitude_all = np.asarray(catalog["m_b_corr"], dtype=float)
    calibrator = np.asarray(catalog["IS_CALIBRATOR"], dtype=int)
    selected = np.flatnonzero((calibrator == 0) & (z_all > 0.01))
    covariance_path = ROOT / "Data" / "Pantheon+SH0ES_STAT+SYS.cov"
    covariance_all = np.loadtxt(covariance_path, skiprows=1).reshape(1701, 1701)
    covariance_all = 0.5 * (covariance_all + covariance_all.T)
    return (
        z_all[selected],
        magnitude_all[selected],
        covariance_all[np.ix_(selected, selected)],
    )


def direct_scores(
    z: np.ndarray, magnitude: np.ndarray, covariance: np.ndarray
) -> dict[str, dict[str, float | int]]:
    u = 1.0 + z
    candidates = {
        "WRL_AREAL_OPTICAL": z * (z + 2.0),
        "PROJECTIVE_AREAL_J1": u**2 * (u**2 - 1.0) / (u**2 + 1.0),
    }
    ones = np.ones_like(z)
    solved_ones = np.linalg.solve(covariance, ones)
    result: dict[str, dict[str, float | int]] = {}
    for name, shape in candidates.items():
        difference = magnitude - 5.0 * np.log10(shape)
        solved_difference = np.linalg.solve(covariance, difference)
        offset = float((ones @ solved_difference) / (ones @ solved_ones))
        residual = difference - offset
        solved_residual = np.linalg.solve(covariance, residual)
        chi2 = float(residual @ solved_residual)
        result[name] = {
            "N": len(z),
            "offset": offset,
            "chi2": chi2,
            "dof": len(z) - 1,
            "chi2_dof": chi2 / (len(z) - 1),
            "rms_mag": float(np.sqrt(np.mean(residual**2))),
        }
    return result


def profile_values(name: str, value: float) -> float:
    if name == "PROJECTIVE_TANH":
        return math.tanh(value)
    if name == "WRL_PROPER_EXPONENTIAL":
        return 1.0 - math.exp(-value)
    if name == "B19_ROUND":
        return 2.0 / math.pi * math.atan(math.sinh(2.0 * value))
    raise KeyError(name)


def validate_status_override(kind: str) -> None:
    state = {
        "selected_profile": "NONE",
        "proper_equals_areal": False,
        "score_missing_join": False,
        "shape_parameter_count": 0,
        "pell_included": False,
        "physical_Xmax": "OPEN",
        "B19_clock_solder": "OPEN",
        "FC12_profile": "OPEN",
        "BAO_CMB_BH": "OPEN_OUT_OF_SCOPE",
    }
    if kind:
        mutations: dict[str, object] = {
            "select": ("selected_profile", "WRL"),
            "conflate": ("proper_equals_areal", True),
            "missing_join": ("score_missing_join", True),
            "retune": ("shape_parameter_count", 1),
            "pell": ("pell_included", True),
            "xmax": ("physical_Xmax", "DERIVED"),
            "b19": ("B19_clock_solder", "DERIVED"),
            "fc12": ("FC12_profile", "SELECTED"),
            "cosmology": ("BAO_CMB_BH", "EXPLAINED"),
        }
        key, value = mutations[kind]
        state[str(key)] = value
    if state != {
        "selected_profile": "NONE",
        "proper_equals_areal": False,
        "score_missing_join": False,
        "shape_parameter_count": 0,
        "pell_included": False,
        "physical_Xmax": "OPEN",
        "B19_clock_solder": "OPEN",
        "FC12_profile": "OPEN",
        "BAO_CMB_BH": "OPEN_OUT_OF_SCOPE",
    }:
        raise AssertionError(f"status firewall rejected {kind}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="INDEPENDENT_VERIFICATION.json")
    args = parser.parse_args()
    checks: dict[str, str] = {}

    names = [
        "PROJECTIVE_TANH",
        "WRL_PROPER_EXPONENTIAL",
        "B19_ROUND",
    ]
    samples = [0.0, 1e-6, 0.02, 0.2, 1.0, 4.0, 12.0]
    for name in names:
        values = [profile_values(name, value) for value in samples]
        require(checks, f"{name}_origin", values[0] == 0.0)
        require(
            checks,
            f"{name}_strict_increase",
            all(right > left for left, right in zip(values, values[1:])),
        )
        require(checks, f"{name}_bounded", all(0.0 <= value < 1.0 for value in values))
        for left in [0.01, 0.1, 0.7, 2.3]:
            for right in [0.02, 0.4, 1.1, 3.2]:
                require(
                    checks,
                    f"{name}_subadd_{left}_{right}",
                    profile_values(name, left + right)
                    <= profile_values(name, left)
                    + profile_values(name, right)
                    + 2e-15,
                )
        require(
            checks,
            f"{name}_non_path_length",
            2 * profile_values(name, 0.5) > profile_values(name, 1.0),
        )

    # Check the three closed composition laws without SymPy.
    pairs = [(0.03, 0.11), (0.2, 0.7), (1.1, 2.4)]
    for first, second in pairs:
        y1 = math.tanh(first)
        y2 = math.tanh(second)
        require(
            checks,
            f"tanh_comp_{first}",
            abs((y1 + y2) / (1 + y1 * y2) - math.tanh(first + second))
            < 2e-15,
        )
        y1 = 1 - math.exp(-first)
        y2 = 1 - math.exp(-second)
        require(
            checks,
            f"exp_comp_{first}",
            abs(y1 + y2 - y1 * y2 - (1 - math.exp(-(first + second))))
            < 2e-15,
        )
        y1 = profile_values("B19_ROUND", first)
        y2 = profile_values("B19_ROUND", second)
        a1 = math.tan(math.pi * y1 / 2)
        a2 = math.tan(math.pi * y2 / 2)
        combined = 2 / math.pi * math.atan(
            a1 * math.sqrt(1 + a2 * a2)
            + a2 * math.sqrt(1 + a1 * a1)
        )
        require(
            checks,
            f"round_comp_{first}",
            abs(combined - profile_values("B19_ROUND", first + second))
            < 3e-15,
        )

    z, magnitude, covariance = load_inputs()
    scores = direct_scores(z, magnitude, covariance)
    registered = {
        "WRL_AREAL_OPTICAL": (0.9098574003059215, 0.1581642243395007),
        "PROJECTIVE_AREAL_J1": (2.166501637078457, 0.30740259169961603),
    }
    for name, expected in registered.items():
        require(checks, f"{name}_N", scores[name]["N"] == 1580)
        require(
            checks,
            f"{name}_chi2",
            abs(float(scores[name]["chi2_dof"]) - expected[0]) < 3e-11,
        )
        require(
            checks,
            f"{name}_rms",
            abs(float(scores[name]["rms_mag"]) - expected[1]) < 3e-14,
        )

    production = json.loads((HERE / "SNE_RESULT.json").read_text(encoding="utf-8"))
    for name in registered:
        require(
            checks,
            f"{name}_cross_method_chi2",
            abs(
                float(scores[name]["chi2_dof"])
                - float(production["scores"][name]["chi2_dof"])
            )
            < 3e-11,
        )
        require(
            checks,
            f"{name}_cross_method_rms",
            abs(
                float(scores[name]["rms_mag"])
                - float(production["scores"][name]["rms_mag"])
            )
            < 3e-14,
        )

    dispositions = {
        row["candidate"]: row for row in read_tsv(HERE / "READOUT_DISPOSITION.tsv")
    }
    require(checks, "readout_disposition_count", len(dispositions) == 8)
    require(
        checks,
        "only_two_sne_evaluable",
        sum(row["SNe_status"].startswith("EVALUABLE") for row in dispositions.values())
        == 2,
    )
    require(
        checks,
        "wrl_proper_not_scored",
        dispositions["WRL_PROPER_PAIR_TRANSFORM"]["SNe_status"]
        == "NOT_EVALUABLE_AS_PAIR_PROFILE",
    )
    require(
        checks,
        "pell_prohibited",
        dispositions["RETIRED_P_ELL"]["SNe_status"] == "PROHIBITED",
    )

    source_rows = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    require(checks, "source_count", len(source_rows) == 23)
    for row in source_rows:
        digest = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        require(checks, f"source_{row['path']}", digest == row["sha256"])

    catches: dict[str, str] = {}
    for kind in [
        "select",
        "conflate",
        "missing_join",
        "retune",
        "pell",
        "xmax",
        "b19",
        "fc12",
        "cosmology",
    ]:
        try:
            validate_status_override(kind)
        except AssertionError:
            catches[kind] = "PASS_REJECTED"
        else:
            raise AssertionError(f"catch survived: {kind}")
    validate_status_override("")

    result = {
        "schema": "udt-pair-space-independent-verification-1.0",
        "result": "PASS",
        "method": "stdlib_profile_algebra_plus_numpy_direct_solve",
        "check_count": len(checks),
        "checks": checks,
        "catch_count": len(catches),
        "catches": catches,
        "SNe_scores": scores,
        "ruling": {
            "valid_pair_transforms": 3,
            "selected_profile": "NONE",
            "SNe_evaluable_registered_readouts": 2,
            "SNe_pair_profile_selection": False,
            "global_Xmax": "OPEN",
        },
    }
    (HERE / args.output).write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
