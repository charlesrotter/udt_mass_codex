#!/usr/bin/env python3
"""Derive one preregistered dimensional SNe query on a frozen G75/G77 geometry."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "26f90fc22271c682fe00ef350eac01b3113a5b9e"
PROFILE_PATH = "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/PROFILE_ATLAS.tsv"
ENGINE_PATH = ROOT / "udt_cmb_G68_F01_F02_finite_path_jacobi_controls_2026-08-11/solve_finite_path.py"
STEP_COUNTS = (1024, 2048, 4096)
S = sp.symbols("s", real=True)


def frozen_bytes(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)


def verify_sources() -> int:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    assert len(rows) == len({row["path"] for row in rows}) == 16
    for row in rows:
        assert hashlib.sha256(frozen_bytes(row["path"])).hexdigest() == row["sha256"]
    return len(rows)


def number(text: str) -> float:
    if "/" in text:
        numerator, denominator = text.split("/", 1)
        return float(numerator) / float(denominator)
    return float(text)


def selected_profile() -> tuple[dict[str, str], tuple[float, float, float]]:
    text = frozen_bytes(PROFILE_PATH).decode("utf-8")
    rows = list(csv.DictReader(io.StringIO(text), delimiter="\t"))
    assert len(rows) == 591
    selected = next(row for row in rows if row["shape_id"] != "ZERO")
    polynomial = sp.Poly(sp.sympify(selected["q_of_s"], locals={"s": S}), S)
    coefficients = tuple(float(polynomial.nth(index)) for index in range(3))
    return selected, coefficients


def load_engine():
    spec = importlib.util.spec_from_file_location("g79_g68_engine", ENGINE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def fields(lapse_a: float, coefficients: tuple[float, float, float], x: float) -> tuple[float, ...]:
    c0, c1, c2 = coefficients
    A = 1.0 + lapse_a * x**2
    A1 = 2.0 * lapse_a * x
    A2 = 2.0 * lapse_a
    h = c0 * x**2 + c1 * x**4 + c2 * x**6
    h1 = 2.0 * c0 * x + 4.0 * c1 * x**3 + 6.0 * c2 * x**5
    h2 = 2.0 * c0 + 12.0 * c1 * x**2 + 30.0 * c2 * x**4
    return A, A1, A2, h, h1, h2


def main() -> None:
    source_count = verify_sources()
    selected, coefficients = selected_profile()
    lapse_a = number(selected["lapse_a"])
    engine = load_engine()
    profile = engine.Profile(
        profile_id=selected["profile_id"],
        family="G75_SELECTED",
        lapse_a=lapse_a,
        shape=selected["shape_id"],
        epsilon=number(selected["amplitude"]),
    )

    def profile_values(_profile, x: float) -> tuple[float, ...]:
        return fields(lapse_a, coefficients, x)

    engine.profile_values = profile_values
    integrations: dict[int, object] = {}
    endpoint_rows = []
    for step_count in STEP_COUNTS:
        controls = dict(
            method="DOP853",
            rtol=2.0e-13,
            atol=2.0e-15,
            max_step=1.0 / step_count,
        )
        solution = engine.integrate(profile, controls)
        assert solution.success and len(solution.t_events[0]) == 1
        affine, state, D = engine.endpoint_map(profile, solution)
        integrations[step_count] = solution
        endpoint_rows.append({
            "step_count": step_count,
            "affine_final": affine,
            "det_D": float(np.linalg.det(D)),
            "dA_over_R": float(math.sqrt(abs(np.linalg.det(D)))),
            "D00": float(D[0, 0]),
            "D01": float(D[0, 1]),
            "D10": float(D[1, 0]),
            "D11": float(D[1, 1]),
            "nfev": int(solution.nfev),
        })

    best_solution = integrations[STEP_COUNTS[-1]]
    summary, endpoint_state, endpoint_D = engine.endpoint_summary(profile, best_solution)
    initial = engine.initial_state(profile)
    initial_position, initial_k, _, _, _ = engine.unpack(initial)
    endpoint_position, endpoint_k, _, _, _ = engine.unpack(endpoint_state)
    initial_g, _, _ = engine.geometry(profile, initial_position)
    endpoint_g, _, _ = engine.geometry(profile, endpoint_position)
    A_receiver = fields(lapse_a, coefficients, float(initial_position[1]))[0]
    A_source = fields(lapse_a, coefficients, float(endpoint_position[1]))[0]
    omega_receiver = -float(initial_g[0] @ initial_k) / math.sqrt(A_receiver)
    omega_source = -float(endpoint_g[0] @ endpoint_k) / math.sqrt(A_source)
    one_plus_z_direct = omega_source / omega_receiver
    one_plus_z_analytic = math.sqrt(A_receiver / A_source)
    phi_pair = math.log(one_plus_z_direct)
    dA_over_R = math.sqrt(abs(float(np.linalg.det(endpoint_D))))

    a_exact = sp.Rational(selected["lapse_a"])
    exact_ratio = sp.simplify(
        sp.sqrt((1 + a_exact * sp.Rational(1, 4) ** 2) / (1 + a_exact))
    )
    exact_phi = sp.simplify(sp.log(exact_ratio))
    p1_factor = sp.simplify(1 - exact_ratio ** (-sp.Rational(2) / sp.Symbol("n", positive=True)))

    refinements = {row["step_count"]: row for row in endpoint_rows}
    dA_1024 = refinements[1024]["dA_over_R"]
    dA_2048 = refinements[2048]["dA_over_R"]
    dA_4096 = refinements[4096]["dA_over_R"]
    result = {
        "schema": "udt-cmb-g79-same-geometry-dimensional-sne-query-v1",
        "status": "PASS",
        "source_rows": source_count,
        "selection_rule": "first_PROFILE_ATLAS_data_row_with_shape_id_not_ZERO",
        "selected_profile": selected,
        "q_coefficients_c0_c1_c2": coefficients,
        "query": {
            "receiver_x": 0.25,
            "source_control_sphere_x": 1.0,
            "observer_type": "coordinate_stationary_proportional_to_stationary_Killing_field",
            "sky_direction": "outward_radial_member_of_complete_metric_orthonormal_sky",
            "frequency_normalization": "unit_receiver_measured_frequency",
            "mixing_and_angular_sectors": "LIVE",
        },
        "redshift": {
            "A_receiver": A_receiver,
            "A_source": A_source,
            "one_plus_z_direct": one_plus_z_direct,
            "one_plus_z_analytic": one_plus_z_analytic,
            "absolute_direct_analytic_difference": abs(one_plus_z_direct - one_plus_z_analytic),
            "one_plus_z_exact": sp.sstr(exact_ratio),
            "phi_pair": phi_pair,
            "phi_pair_exact": sp.sstr(exact_phi),
            "thermal_frequency_scale_ratio_conditional": 1.0 / one_plus_z_direct,
        },
        "distance": {
            "dA_over_R": dA_over_R,
            "R_power": 1,
            "physical_relation": "d_A=R*(dA_over_R)",
            "det_D_dimensionless": float(np.linalg.det(endpoint_D)),
            "P1_type_match": "CONDITIONAL_REGISTERED_MATCH_BECAUSE_FROZEN_SNE_ASSEMBLY_POSITS_dA_equals_r",
            "P1_no_fit_scale_expression": "R/R_w=[1-(1+z)^(-2/n)]/(d_A/R)",
            "P1_exact_numerator": sp.sstr(p1_factor),
        },
        "endpoint": {
            "affine_over_R": float(summary["affine_final"]),
            "coordinates": summary["endpoint_coordinates"],
            "D": summary["endpoint_D"],
            "singular_values": summary["singular_values"],
            "first_caustic_affine": summary["first_caustic_affine"],
            "classification": summary["status"],
        },
        "refinement": endpoint_rows,
        "refinement_dA_absolute_1024_2048": abs(dA_1024 - dA_2048),
        "refinement_dA_absolute_2048_4096": abs(dA_2048 - dA_4096),
        "residuals": summary["residuals"],
        "authority": {
            "maximum_conclusion": "DERIVED_CONDITIONAL_ON_ONE_FROZEN_GEOMETRY_AND_ONE_CHOSEN_STATIONARY_QUERY",
            "physical_profile_selected": False,
            "R_selected": False,
            "Xmax_identified": False,
            "SNe_fit_performed": False,
            "CMB_temperature_or_spectrum_derived": False,
        },
    }
    assert selected["profile_id"] == "G75_AM_S01_E05"
    assert selected["q_of_s"] == "s**2/20"
    assert result["endpoint"]["classification"] == "ENDPOINT_REGULAR_NO_CAUSTIC"
    assert result["residuals"]["null"] < 1.0e-9
    assert result["residuals"]["conserved_p_t"] < 1.0e-10
    assert result["residuals"]["screen_gram"] < 1.0e-8
    assert result["residuals"]["screen_ray"] < 1.0e-8
    assert result["redshift"]["absolute_direct_analytic_difference"] < 1.0e-10
    assert math.isfinite(dA_over_R) and dA_over_R > 0.0

    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    with (HERE / "REFINEMENT_ATLAS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(endpoint_rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(endpoint_rows)
    grid = np.linspace(0.0, float(summary["affine_final"]), 501)
    np.savez_compressed(
        HERE / "PATH_EVIDENCE.npz",
        affine=grid,
        state=np.asarray(best_solution.sol(grid), dtype=np.float64),
        endpoint_D=np.asarray(endpoint_D, dtype=np.float64),
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
