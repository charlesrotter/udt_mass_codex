#!/usr/bin/env python3
"""Exact reciprocal-toric projector, connection, and Hopf-seed control."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    phi = sp.symbols("phi", real=True)
    A, Ap, omega, omegap = sp.symbols("A Ap Omega Omega_p", positive=True, finite=True)
    u = omegap / omega

    # Mixed Hessian and dyad eigenvalues in (t, phi, xi1, xi2).
    hessian = (sp.Integer(0), -Ap / A**3, (u - 1) / A**2, (u + 1) / A**2)
    dyad = (sp.Integer(0), 1 / A**2, sp.Integer(0), sp.Integer(0))
    joint_pairs = tuple((sp.simplify(hessian[index]), sp.simplify(dyad[index])) for index in range(4))
    angular_gap = sp.simplify(hessian[3] - hessian[2])

    f = sp.simplify(sp.exp(-2 * phi) / (sp.exp(-2 * phi) + sp.exp(2 * phi)))
    one_minus_f = sp.simplify(1 - f)
    f_prime = sp.simplify(sp.diff(f, phi))
    finite_q = sp.simplify(sp.Symbol("f_minus") - sp.Symbol("f_plus"))
    minus_limit = sp.limit(f, phi, -sp.oo)
    plus_limit = sp.limit(f, phi, sp.oo)
    unit_q = sp.simplify(minus_limit - plus_limit)

    delta = sp.symbols("delta", real=True)
    quotient = (
        sp.sech(2 * phi) * sp.cos(delta),
        sp.sech(2 * phi) * sp.sin(delta),
        -sp.tanh(2 * phi),
    )
    quotient_norm = sp.simplify(sum(value**2 for value in quotient).rewrite(sp.exp))
    seal_f = sp.simplify(f.subs(phi, 0))

    round_A = sp.sech(2 * phi)
    round_omega_squared = 1 / (2 * sp.cosh(2 * phi))
    round_b_squared = sp.simplify(round_omega_squared * sp.exp(-2 * phi))
    round_c_squared = sp.simplify(round_omega_squared * sp.exp(2 * phi))
    round_limits = {
        "b2_minus": sp.limit(round_b_squared, phi, -sp.oo),
        "b2_plus": sp.limit(round_b_squared, phi, sp.oo),
        "c2_minus": sp.limit(round_c_squared, phi, -sp.oo),
        "c2_plus": sp.limit(round_c_squared, phi, sp.oo),
    }

    eta, xi1, xi2 = sp.symbols("eta xi1 xi2", real=True)
    seed = (
        sp.sin(2 * eta) * sp.cos(xi1 - xi2),
        sp.sin(2 * eta) * sp.sin(xi1 - xi2),
        sp.cos(2 * eta),
    )
    substitutions = {
        sp.sin(2 * eta): sp.sech(2 * phi),
        sp.cos(2 * eta): -sp.tanh(2 * phi),
        xi1 - xi2: delta,
    }
    seed_difference = tuple(sp.simplify(seed[index].subs(substitutions) - quotient[index]) for index in range(3))

    result = {
        "schema": "udt-reciprocal-toric-control-1.0",
        "coordinates": ["t", "phi", "xi1", "xi2"],
        "metric": "-dt^2 + A(phi)^2 dphi^2 + Omega(phi)^2[exp(-2phi)dxi1^2+exp(2phi)dxi2^2]",
        "hessian_mixed_eigenvalues": [str(value) for value in hessian],
        "dyad_mixed_eigenvalues": [str(value) for value in dyad],
        "joint_HD_eigenvalue_pairs": [[str(first), str(second)] for first, second in joint_pairs],
        "angular_hessian_eigenvalue_gap": str(angular_gap),
        "axis_recovery_condition": "Omega_p/Omega != +1 and Omega_p/Omega != -1 on the open orbit region",
        "axis_recovery_status": "GENERIC_CONDITIONAL_NOT_UNIVERSAL_FOR_ARBITRARY_POSITIVE_OMEGA",
        "projector_motif": "FOUR_LINES_FOR_H_PLUS_D_WHEN_AXIS_RECOVERY_CONDITION_HOLDS",
        "projector_orientation": "UNORIENTED_LINES_ONLY",
        "connection": f"({sp.sstr(f)}) dxi1 + ({sp.sstr(one_minus_f)}) dxi2",
        "connection_common_scale_dependence": "NONE",
        "connection_weight_selector": "OPEN_DIAGONAL_OR_ANTIDIAGONAL_ACTION_NOT_SELECTED_BY_PROJECTORS",
        "f": str(f),
        "f_prime": str(f_prime),
        "chern_simons_finite_endpoints": "4*pi^2*(f(phi_plus)-f(phi_minus))",
        "hopf_q_finite_endpoints": str(finite_q),
        "f_minus_infinity": str(minus_limit),
        "f_plus_infinity": str(plus_limit),
        "conditional_unit_q": str(unit_q),
        "periodic_phi_closed_loop_q": "0 because integral df over a single-valued periodic f vanishes",
        "periodicity_status": "SUPPLIED_GLOBAL_DATA_NOT_DERIVED_BY_LOCAL_PROJECTORS",
        "seal_equal_scale_fraction": str(seal_f),
        "reciprocity_reflection": "phi -> -phi exchanges xi1 and xi2 coefficients",
        "reflection_isometry_condition": "A(phi)^2 and Omega(phi)^2 even, with xi1<->xi2 exchange",
        "reflection_status": "CONDITIONAL_NOT_FORCED_FOR_ARBITRARY_A_OMEGA",
        "round_control_A": str(round_A),
        "round_control_Omega_squared": str(round_omega_squared),
        "round_control_b_squared": str(round_b_squared),
        "round_control_c_squared": str(round_c_squared),
        "round_control_cap_limits": {key: str(value) for key, value in round_limits.items()},
        "collapse_status": "OPPOSITE_PRIMITIVE_COLLAPSES_IN_ROUND_CONTROL; OPEN_FOR_ARBITRARY_A_OMEGA",
        "quotient_map": [str(value) for value in quotient],
        "quotient_norm_squared": str(quotient_norm),
        "hopf_seed_difference": [str(value) for value in seed_difference],
        "hopf_seed_exact_match": all(value == 0 for value in seed_difference),
        "hopfion_seed_source_sha256": digest(ROOT / "hopfion_arc_scripts_2026-07-05/fs_hopfion.py"),
        "noNull_energy_source_sha256": digest(ROOT / "noNull_energy.py"),
        "supplied_equal_weight_circle_action": True,
        "circle_action_status": "SUPPLIED_CONDITIONAL_NOT_SELECTED_BY_PROJECTORS",
        "construction_used_s2_matter_carrier": False,
        "construction_used_l2_l4_action_functional": False,
        "global_premises_for_unit_class": [
            "two periodic spatial circle directions",
            "full phi range from minus infinity to plus infinity once",
            "opposite primitive smooth circle collapses",
            "selected free diagonal or anti-diagonal circle action",
            "orientation and normalization",
        ],
        "maximum_conclusion": "CONDITIONAL_PROJECTOR_AXIS_RECOVERY_AND_UNIT_HOPF_COMPATIBILITY_WITNESS",
    }
    if quotient_norm != 1:
        raise AssertionError(f"quotient norm {quotient_norm}")
    if not result["hopf_seed_exact_match"]:
        raise AssertionError("Hopf seed mismatch")
    if unit_q != 1:
        raise AssertionError("unit Q limit")
    if seal_f != sp.Rational(1, 2):
        raise AssertionError("seal equal scale")
    if round_limits != {"b2_minus": 1, "b2_plus": 0, "c2_minus": 0, "c2_plus": 1}:
        raise AssertionError(f"round cap limits {round_limits}")
    if sp.simplify(angular_gap - 2 / A**2) != 0:
        raise AssertionError("angular gap")
    (HERE / "TORIC_CONTROL_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    rows = [
        {
            "claim_id": "T01", "object": "H+D pointwise projector axes",
            "status": "GENERIC_CONDITIONAL_FOUR_LINES",
            "basis": "joint eigenvalue pairs distinguish t,phi,xi1,xi2 when Omega'/Omega is not +/-1",
            "limit": "arbitrary positive Omega can cross a degeneracy; lines are unoriented",
        },
        {
            "claim_id": "T02", "object": "transverse angular axes",
            "status": "RECOVERED_WITHIN_CONDITIONAL_TORIC_CLASS",
            "basis": "H angular eigenvalues differ identically by 2/A^2",
            "limit": "toric diagonal reciprocal class was supplied; periodicity is not local",
        },
        {
            "claim_id": "T03", "object": "diagonal circle generator",
            "status": "OPEN",
            "basis": "projectors recover axes but do not choose weights or orientation",
            "limit": "freeness selects abs-one weights only after S3 cap completion is supplied",
        },
        {
            "claim_id": "T03A", "object": "reciprocity reflection",
            "status": "CONDITIONAL_EXCHANGE_ISOMETRY",
            "basis": "phi reversal exchanges the angular coefficients and phi=0 gives equal scales",
            "limit": "requires even A^2 and Omega^2 plus the global circle exchange",
        },
        {
            "claim_id": "T03B", "object": "periodicity and opposite caps",
            "status": "ROUND_CONTROL_EXACT_GENERAL_OPEN",
            "basis": "the round control has opposite primitive collapse limits 1/0 and 0/1",
            "limit": "local projectors do not supply periods, cap cycles, or arbitrary-profile regularity",
        },
        {
            "claim_id": "T04", "object": "finite-endpoint Hopf readout",
            "status": "CONTINUOUS_BOUNDARY_DEPENDENT",
            "basis": "Q=f(phi_minus)-f(phi_plus)",
            "limit": "not topological or integral without global cap premises",
        },
        {
            "claim_id": "T05", "object": "unit Hopf class",
            "status": "CONDITIONAL_UNIT_CLASS",
            "basis": "full reciprocal range and opposite primitive caps give f(-infinity)-f(+infinity)=1",
            "limit": "periods, action, caps, orientation, and normalization are supplied premises",
        },
        {
            "claim_id": "T06", "object": "existing Hopf seed formula",
            "status": "EXACT_SEED_LEVEL_MATCH",
            "basis": "standard Hopf coordinates with tan(eta)=exp(2phi) reproduce the code formula",
            "limit": "not equality to relaxed field; no L2+L4 action or matter emergence follows",
        },
    ]
    with (HERE / "TORIC_STATUS_LEDGER.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
