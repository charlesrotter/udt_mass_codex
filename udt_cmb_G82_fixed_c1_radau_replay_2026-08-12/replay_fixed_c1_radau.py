#!/usr/bin/env python3
"""Preregistered Radau replay of the exact frozen G81 C1 neighboring-ray control."""

from __future__ import annotations

import importlib.util
import json
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
G81 = ROOT / "udt_cmb_G81_nonradial_screen_covariance_2026-08-12"
PARENT_PATH = G81 / "verify_nonradial_neighboring_rays.py"
RTOL = 5.0e-11
ATOL = 5.0e-13
MAX_STEP = 1.0 / 512.0
METHOD = "Radau"
GATE = 2.0e-4


def load_parent():
    spec = importlib.util.spec_from_file_location("g81_neighboring", PARENT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def relative(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.linalg.norm(left - right) / max(1.0, np.linalg.norm(left), np.linalg.norm(right)))


def main() -> None:
    parent = load_parent()
    assert parent.DELTAS == (1.0e-4, 5.0e-5)
    assert len(parent.CONTROLS) == 2
    c1 = parent.CONTROLS[1]
    assert c1 == (
        "C1_FULL_ANGULAR",
        (12.0 / 13.0, 3.0 / 13.0, 4.0 / 13.0),
        (0.0, 4.0 / 5.0, -3.0 / 5.0),
        (-5.0 / 13.0, 36.0 / 65.0, 48.0 / 65.0),
    )

    def integrate_radau(
        position: np.ndarray,
        tangent: np.ndarray,
        screen: np.ndarray | None,
        *,
        target_x: float | None = None,
        direction: float = 0.0,
        affine_end: float | None = None,
    ) -> object:
        state0 = (
            np.concatenate((position, tangent))
            if screen is None
            else np.concatenate((position, tangent, screen.ravel()))
        )

        def rhs(_affine: float, state: np.ndarray) -> np.ndarray:
            p, k = state[:4], state[4:8]
            gamma = parent.connection(p)
            dk = -np.einsum("rmn,m,n->r", gamma, k, k)
            if screen is None:
                return np.concatenate((k, dk))
            frame = state[8:16].reshape(2, 4)
            dframe = -np.einsum("rmn,m,an->ar", gamma, k, frame)
            return np.concatenate((k, dk, dframe.ravel()))

        events = None
        if target_x is not None:
            def event(_affine: float, state: np.ndarray) -> float:
                return float(state[1] - target_x)
            event.terminal = True
            event.direction = direction
            events = event
        return solve_ivp(
            rhs,
            (0.0, 10.0 if affine_end is None else affine_end),
            state0,
            events=events,
            dense_output=True,
            method=METHOD,
            rtol=RTOL,
            atol=ATOL,
            max_step=MAX_STEP,
        )

    parent.integrate = integrate_radau
    production = json.loads((G81 / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    frozen_dop853 = json.loads((G81 / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    assert production["controls"][1]["control_id"] == "C1_FULL_ANGULAR"
    assert frozen_dop853["controls"][1]["control_id"] == "C1_FULL_ANGULAR"

    result = parent.run_control(c1, production["controls"][1])
    old = frozen_dop853["controls"][1]
    matrix_keys = ("forward_fine_D", "reverse_fine_D", "rotated_fine_D")
    dop853_relative = {
        key: relative(np.asarray(result[key]), np.asarray(old[key])) for key in matrix_keys
    }
    coarse_fine_max = max(
        result["forward_coarse_fine_relative"],
        result["reverse_coarse_fine_relative"],
        result["rotated_coarse_fine_relative"],
    )
    extra_gates = {
        "radau_not_dop853": METHOD == "Radau",
        "coarse_fine": coarse_fine_max < GATE,
        "dop853_matrix_agreement": max(dop853_relative.values()) < GATE,
        "all_frozen_g81_gates": all(result["gates"].values()),
    }
    status = "PASS" if result["status"] == "PASS" and all(extra_gates.values()) else "FAIL"
    payload = {
        "schema": "udt-cmb-g82-fixed-c1-radau-replay-v1",
        "status": status,
        "maximum_conclusion_if_pass": "G81_C1_SCREEN_COVARIANCE_SURVIVES_ONE_FIXED_NON_DOP853_RADAU_REPLAY",
        "scientific_maximum_unchanged": "DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS",
        "method": {
            "integrator": METHOD,
            "rtol": RTOL,
            "atol": ATOL,
            "max_step": MAX_STEP,
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "shared_with_g81": "metric, Christoffels, query, endpoint, rotations, finite-difference and projection implementation",
        "changed_from_g81": "integrator family only: Radau instead of DOP853",
        "gate": GATE,
        "coarse_fine_max_relative": coarse_fine_max,
        "radau_vs_dop853_matrix_relative": dop853_relative,
        "extra_gates": extra_gates,
        "control": result,
        "authority_boundary": (
            "one-control integrator-family replay only; no selector, physical profile, endpoint, scale, Xmax, "
            "SNe/CMB observable, cmb_temp, source, action, matter, bootstrap closure, signalling law, or future signal"
        ),
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    (HERE / "DERIVATION_RESULT.json").write_text(rendered, encoding="utf-8")
    (HERE / "DERIVATION_STDOUT.txt").write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if status != "PASS":
        raise SystemExit("G82 preregistered Radau gate failed")


if __name__ == "__main__":
    main()
