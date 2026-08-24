#!/usr/bin/env python3
"""Hostile semantic and implementation catches for G241."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

import numpy as np


PACKAGE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("g241_production", PACKAGE / "derive_sne_tidal_bridge.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    checks = []

    def catch(name, condition):
        assert condition, name
        checks.append(name)

    result = MODULE.derive()
    knots, theta, covariance = MODULE.load_frozen_state()
    catch("candidate_order_fixed", tuple(MODULE.CANDIDATE_DEGREES) == (2, 3, 4))
    catch("boss_outcomes_closed", result["boss_outcomes_opened"] is False)
    catch("no_angular_fit_coefficient", result["angular_fit_coefficient"] is None)
    catch("negative_landing_retained", result["selected_degree"] is None)
    catch("anchor_subtraction_exact", np.max(np.abs(MODULE.anchored_basis(np.asarray([-1.0]), 4))) == 0.0)

    diagonal = np.diag(np.diag(covariance))
    diagonal_candidate = MODULE.fit_candidate(3, knots, theta, diagonal)
    full_candidate = result["candidates"][1]
    catch("full_covariance_is_load_bearing", abs(diagonal_candidate["chi2"] - full_candidate["chi2"]) > 1.0)
    catch("monotonicity_gate_live", any(not candidate["monotone_invertible"] for candidate in result["candidates"]))
    catch("adequacy_gate_live", all(not candidate["adequate"] for candidate in result["candidates"]))

    d3 = result["candidates"][1]
    phi = knots
    decay = np.exp(-2.0 * phi)
    wrong_q_sign = decay * (
        2.0 * np.asarray(d3["knot_p"]) ** 2
        + np.asarray(d3["knot_q"])
        + 2.0 * np.asarray(d3["knot_p"])
    ) - (1.0 - decay)
    catch("tidal_q_sign_live", np.max(np.abs(wrong_q_sign - np.asarray(d3["knot_tidal_J"]))) > 1.0)

    production_text = (PACKAGE / "derive_sne_tidal_bridge.py").read_text()
    forbidden = ("P1", "G116", "G189", "X_max", "Lambda-CDM", "protected", "R5_OUTCOME", "BOSS_R5")
    catch("forbidden_construction_inputs_absent", not any(token in production_text for token in forbidden))
    catch("scale_invariance_live", all(candidate["scale_invariance_max_abs_residual"] < 1.0e-5 for candidate in result["candidates"]))

    output = {"status": "PASS", "catches": checks, "count": len(checks)}
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert rendered == (PACKAGE / "CATCH_PROOF_RESULT.json").read_text()
    else:
        (PACKAGE / "CATCH_PROOF_RESULT.json").write_text(rendered)
    print(f"PASS: {len(checks)} G241 hostile catches")


if __name__ == "__main__":
    main()
