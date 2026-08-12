#!/usr/bin/env python3
"""Independent scalar proof and stratified solver replay for G83."""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DERIVE_PATH = HERE / "derive_endpoint_asymptote_atlas.py"
RADUA_CONTROLS = dict(method="Radau", rtol=1.0e-10, atol=1.0e-12, max_step=1.0 / 400.0)
COMPARISON_TOLERANCE = 1.0e-7


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def exact_scalar_checks() -> dict[str, object]:
    x, xr, A_s = sp.symbols("x xr A_s", positive=True)
    A = 1 - x**2 / 4
    # Prove the registered 0<x<2 primitive without depending on SymPy's Piecewise presentation.
    primitive = 2 * sp.asin(x / 2)
    assert sp.simplify(sp.diff(primitive, x) - 1 / sp.sqrt(A)) == 0
    assert primitive.subs(x, 0) == 0
    xs = 2 * sp.sqrt(1 - A_s)
    A_r = 1 - xr**2 / 4
    assert sp.simplify(A.subs(x, xs) - A_s) == 0
    phi = sp.log(A_r / A_s) / 2
    c_ratio = A_s / A_r
    assert sp.limit(phi, A_s, 0, dir="+") == sp.oo
    assert sp.limit(c_ratio, A_s, 0, dir="+") == 0
    proper = 2 * (sp.asin(xs / 2) - sp.asin(xr / 2))
    proper_limit = sp.simplify(sp.limit(proper, A_s, 0, dir="+"))
    assert sp.simplify(proper_limit - (sp.pi - 2 * sp.asin(xr / 2))) == 0
    assert sp.simplify(sp.diff(proper_limit, xr)) != 0
    return {
        "A_source_identity": True,
        "phi_limit": "POSITIVE_INFINITY",
        "c_eff_ratio_limit": "ZERO",
        "proper_limit_over_R": str(proper_limit),
        "proper_limit_receiver_derivative": str(sp.simplify(sp.diff(proper_limit, xr))),
        "receiver_dependent": True,
    }


def choose_stratified(profiles) -> list:
    am = [profile for profile in profiles if profile.lapse_name == "AM"]
    selected = [next(profile for profile in am if profile.shape_id == "ZERO")]
    behaviors = sorted({profile.behavior_class for profile in am if profile.shape_id != "ZERO"})
    for behavior in behaviors:
        candidates = [
            profile for profile in am
            if profile.behavior_class == behavior and math.isclose(profile.amplitude, 1.0)
        ]
        selected.append(sorted(candidates, key=lambda profile: profile.profile_id)[0])
    assert len({profile.profile_id for profile in selected}) == len(selected)
    return selected


def replay_radau(derive, path_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    profiles = derive.load_profiles()
    by_id = {profile.profile_id: profile for profile in profiles}
    registered = {(row["profile_id"], int(row["approach_power"])): row for row in path_rows}
    engine = derive.import_engine()

    def patched_profile_values(engine_profile, x: float):
        return derive.metric_profile_values(by_id[engine_profile.profile_id], x)

    engine.profile_values = patched_profile_values
    engine.START_X = derive.RECEIVER_X
    engine.S_CAP = derive.AFFINE_CAP
    rows: list[dict[str, object]] = []
    for profile in choose_stratified(profiles):
        engine_profile = derive.make_engine_profile(engine, profile)
        for power in derive.APPROACH_POWERS:
            target = 2.0 * math.sqrt(1.0 - 2.0 ** (-power))
            event = derive.endpoint_event_factory(target)
            solution = solve_ivp(
                engine.full_rhs(engine_profile),
                (0.0, derive.AFFINE_CAP),
                engine.initial_state(engine_profile),
                events=(event, engine.turning_event),
                dense_output=True,
                **RADUA_CONTROLS,
            )
            endpoint = len(solution.t_events[0]) > 0
            final_s = float(solution.t_events[0][0]) if endpoint else float(solution.t[-1])
            state = np.asarray(solution.sol(final_s), dtype=np.float64)
            D, _, _, _ = engine.screen_objects(engine_profile, state)
            reference = registered[(profile.profile_id, power)]
            affine_difference = abs(final_s - float(reference["affine_final"]))
            det_difference = abs(float(np.linalg.det(D)) - float(reference["endpoint_det_D"]))
            endpoint_match = endpoint == (reference["endpoint_reached"].lower() == "true")
            passed = bool(endpoint_match and affine_difference <= COMPARISON_TOLERANCE and det_difference <= COMPARISON_TOLERANCE)
            rows.append(
                {
                    "profile_id": profile.profile_id,
                    "behavior_class": profile.behavior_class,
                    "approach_power": power,
                    "endpoint_match": endpoint_match,
                    "affine_absolute_difference": affine_difference,
                    "det_D_absolute_difference": det_difference,
                    "passed": passed,
                    "radau_nfev": int(solution.nfev),
                }
            )
            print(f"Radau {profile.profile_id} p={power} pass={passed}", flush=True)
    return rows


def main() -> None:
    derive = load_module("g83_derive_verify", DERIVE_PATH)
    assert derive.verify_sources() == 14
    strict = read_tsv(HERE / "STRICT_DOMAIN_ATLAS.tsv")
    recenter = read_tsv(HERE / "RECENTERED_ENDPOINT_LIMIT_ATLAS.tsv")
    paths = read_tsv(HERE / "CONTINUED_PATH_ATLAS.tsv")
    families = read_tsv(HERE / "LAPSE_FAMILY_CONTINUATION.tsv")
    assert len(strict) == 591 and len({row["profile_id"] for row in strict}) == 591
    assert all(row["finite_positive_lapse"] == "true" for row in strict)
    assert all(math.isfinite(float(row["phi_receiver_to_x_1"])) for row in strict)
    assert len(recenter) == 12
    assert len(paths) == 591 and len({(row["profile_id"], row["approach_power"]) for row in paths}) == 591
    allowed = {
        "ENDPOINT_REGULAR_NO_CAUSTIC", "ENDPOINT_AFTER_CAUSTIC", "TURNING_NO_ENDPOINT",
        "AFFINE_CAP_NO_ENDPOINT", "SOLVER_FAILURE", "NUMERIC_NONFINITE_OR_SIGNATURE_FAILURE",
    }
    assert {row["status"] for row in paths} <= allowed
    assert {row["lapse_name"] for row in families} == {"AM", "A0", "AP"}
    certified = [row for row in paths if row["numerically_certified"].lower() == "true"]
    for row in certified:
        for field in ("null_residual", "screen_gram_residual", "screen_ray_residual", "p_t_residual", "p_psi_residual"):
            assert float(row[field]) <= derive.RESIDUAL_TOLERANCE
    scalar = exact_scalar_checks()
    radau = replay_radau(derive, paths)
    with (HERE / "INDEPENDENT_RADAU_REPLAY.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(radau[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(radau)
    status_counts = Counter(row["status"] for row in paths)
    payload = {
        "schema": "UDT_CMB_G83_INDEPENDENT_VERIFICATION_V1",
        "all_passed": all(row["passed"] for row in radau),
        "source_hashes_passed": True,
        "exact_scalar_checks": scalar,
        "strict_rows": len(strict),
        "path_rows": len(paths),
        "certified_rows": len(certified),
        "status_counts": dict(sorted(status_counts.items())),
        "radau_rows": len(radau),
        "radau_passed": sum(bool(row["passed"]) for row in radau),
        "radau_profile_ids": sorted({str(row["profile_id"]) for row in radau}),
        "maximum_conclusion": "independent verification of the bounded G83 candidate atlas only; physical X_max remains open",
    }
    assert payload["all_passed"]
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
