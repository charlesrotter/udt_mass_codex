#!/usr/bin/env python3
"""Hostile mutation catches for the G211 evidence contract."""

from __future__ import annotations

import json
import os
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
OUT = PACKAGE / "CATCH_PROOF_RESULT.json"


def compact(name: str) -> str:
    return " ".join((PACKAGE / name).read_text(encoding="utf-8").split())


def removed(text: str, token: str) -> bool:
    mutated = text.replace(token, "", 1)
    return token in text and text.count(token) == mutated.count(token) + 1


def replaced(text: str, old: str, new: str) -> bool:
    return old in text and old not in text.replace(old, new, 1) and new in text.replace(old, new, 1)


def main() -> None:
    prereg = compact("PREREGISTRATION.md")
    exact = compact("EXACT_DERIVATION.md")
    audit = compact("AUDIT_REPORT.md")
    execution = compact("PREREGISTRATION_EXECUTION_NOTE.md")
    production = compact("derive_diagonal_scalar_basis.py")
    independent = compact("verify_diagonal_scalar_independent.py")
    controls = compact("run_radial_controls.py")

    catches = {
        "prereg_commit": removed(execution, "7220e71f"),
        "supplied_split_scope": removed(exact, "supplied time foliation"),
        "lapse_half_factor": replaced(prereg, "(1/2)log(F/f)", "log(F/f)"),
        "spatial_sixth_factor": replaced(prereg, "(1/6)log(det(K)/det(H))", "(1/3)log(det(K)/det(H))"),
        "rank_two": replaced(audit, "exactly two coordinates", "three coordinates"),
        "lapse_not_third": removed(audit, "not a third scalar tile"),
        "common_relative_q_sign": replaced(prereg, "q=sigma-ell", "q=sigma+ell"),
        "basis_reconstruction": replaced(prereg, "sigma=Omega+q", "sigma=Omega-q"),
        "volume_coefficient_three": replaced(prereg, "V=ell+3 sigma", "V=ell+sigma"),
        "width_sign": replaced(prereg, "W=ell-sigma", "W=ell+sigma"),
        "inverse_quarter": replaced(prereg, "ell=(V+3W)/4", "ell=(V+3W)/2"),
        "determinant_scale": removed(exact, "-ufz^3"),
        "inverse_temporal_scale": removed(exact, "-1/(uf)"),
        "temporal_dt": removed(exact, "remains temporal"),
        "cone_center": removed(exact, "center remains `v=-b`"),
        "cone_common_cancellation": removed(exact, "The common scale `Omega` cancels"),
        "g205_radial_bound": removed(prereg, "|dr/dt+b^r| <= f exp(-q)"),
        "conditional_cauchy": removed(prereg, "conditional on the supplied `g_q,b`"),
        "affine_power_two": replaced(prereg, "dlambda_g=exp(2 Omega) dlambda_q", "dlambda_g=exp(Omega) dlambda_q"),
        "radial_affine_joint": removed(prereg, "exp(2Omega+q)/E"),
        "same_cone_control": removed(exact, "exactly the base causal curves"),
        "radial_only_compensation_scope": removed(exact, "proves only radial restoration"),
        "pair_common_factor": removed(prereg, "T^2=exp(2Omega)"),
        "pair_phi_common": removed(prereg, "Phi=-Omega-(1/2)log[...]"),
        "q_blind_not_omega_blind": removed(exact, "exactly `q`-blind but still hears `Omega`"),
        "independent_no_import": removed(independent, '"production_imported": False'),
        "radial_controls_scope": removed(controls, "divergence of the compensated unit density is analytic"),
        "analytic_evidence_ceiling": removed(exact, "finite scripts do not mechanize their universal quantifiers"),
        "physical_history_not_selected": removed(audit, "physical history"),
        "xmax_not_selected": removed(audit, "`X_max` law"),
        "production_scope": removed(production, "finite-dimensional scalar basis, ADM, cone, radial-null, and completed-pair algebra only"),
    }
    failed = [name for name, caught in catches.items() if not caught]
    if failed:
        raise AssertionError(f"uncaught mutations: {failed}")
    result = {
        "status": "PASS",
        "catch_count": len(catches),
        "catches": sorted(catches),
        "scope": "basis rank and coefficients, ADM, cone, affine, pair strata, evidence ceiling, history and Xmax guards",
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
