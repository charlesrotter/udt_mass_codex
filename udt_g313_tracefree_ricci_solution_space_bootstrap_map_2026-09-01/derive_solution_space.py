#!/usr/bin/env python3
"""Exact standard-library checks for the bounded G313 solution-space map."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


class Census:
    def __init__(self) -> None:
        self.checks = 0

    def require(self, condition: bool, label: str) -> None:
        self.checks += 1
        if not condition:
            raise AssertionError(label)


def epsilon(i: int, j: int, k: int) -> int:
    positive = {(0, 1, 2), (1, 2, 0), (2, 0, 1)}
    negative = {(1, 0, 2), (2, 1, 0), (0, 2, 1)}
    if (i, j, k) in positive:
        return 1
    if (i, j, k) in negative:
        return -1
    return 0


def berger_ricci_from_koszul(q: Fraction) -> tuple[list[list[Fraction]], Fraction]:
    """Compute Ricci for SU(2) lengths (1,1,q) from brackets and Koszul."""
    lengths = [Fraction(1), Fraction(1), q]
    structure = [
        [
            [
                Fraction(2) * lengths[k] * epsilon(i, j, k) / (lengths[i] * lengths[j])
                for k in range(3)
            ]
            for j in range(3)
        ]
        for i in range(3)
    ]
    connection = [
        [
            [
                (
                    structure[i][j][k]
                    - structure[j][k][i]
                    + structure[k][i][j]
                )
                / 2
                for k in range(3)
            ]
            for j in range(3)
        ]
        for i in range(3)
    ]

    def riemann(i: int, j: int, k: int, m: int) -> Fraction:
        return sum(
            connection[j][k][n] * connection[i][n][m]
            - connection[i][k][n] * connection[j][n][m]
            - structure[i][j][n] * connection[n][k][m]
            for n in range(3)
        )

    ricci = [
        [sum(riemann(i, j, k, i) for i in range(3)) for k in range(3)]
        for j in range(3)
    ]
    scalar = sum(ricci[i][i] for i in range(3))
    return ricci, scalar


def encode(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    if isinstance(value, list):
        return [encode(item) for item in value]
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    census = Census()

    # Contracted Bianchi applied to S_ab=Ric_ab-(R/4)g_ab.
    divergence_coefficient = Fraction(1, 2) - Fraction(1, 4)
    census.require(divergence_coefficient == Fraction(1, 4), "Bianchi coefficient")
    census.require(divergence_coefficient != 0, "Bianchi forces connected scalar constancy")

    branch_rows = []
    for lam in map(Fraction, (-5, -2, -1, 0, 1, 2, 5)):
        scalar = 4 * lam
        round_riemann_sq = Fraction(8, 3) * lam * lam
        round_weyl_sq = round_riemann_sq - scalar * scalar / 6
        nariai_riemann_sq = 8 * lam * lam
        nariai_weyl_sq = nariai_riemann_sq - scalar * scalar / 6
        census.require(round_weyl_sq == 0, f"round Weyl lambda={lam}")
        census.require(nariai_weyl_sq == Fraction(16, 3) * lam * lam, f"product Weyl lambda={lam}")
        if lam != 0:
            census.require(nariai_weyl_sq > 0, f"nonzero product Weyl lambda={lam}")
        branch_rows.append(
            {
                "lambda": lam,
                "scalar_R": scalar,
                "round_weyl_squared": round_weyl_sq,
                "product_weyl_squared": nariai_weyl_sq,
            }
        )

    # Constant homothety preserves the equation while changing the scalar magnitude.
    homothety_rows = []
    lam0 = Fraction(3)
    for scale_sq in map(Fraction, (Fraction(1, 4), Fraction(1, 2), 1, 2, 3, 5, 9)):
        scaled_lambda = lam0 / scale_sq
        scaled_scalar = 4 * scaled_lambda
        census.require(scaled_scalar * scale_sq == 4 * lam0, f"homothety response {scale_sq}")
        census.require(scaled_lambda != 0, f"homothety nonzero {scale_sq}")
        homothety_rows.append(
            {"metric_multiplier": scale_sq, "lambda_after": scaled_lambda, "R_after": scaled_scalar}
        )

    # Positive fixed-Lambda compact Cauchy data: round S3, Nariai S1xS2, and nonround Berger S3.
    lam = Fraction(3)
    cauchy_rows = []
    for name, scalar_3, h_sq, topology, round_state in (
        ("round_S3_bounce", Fraction(6), Fraction(0), "S3", True),
        ("nariai_S1xS2_bounce", Fraction(6), Fraction(0), "S1xS2", False),
    ):
        hamiltonian = scalar_3 + 6 * h_sq
        census.require(hamiltonian == 2 * lam, f"Hamiltonian {name}")
        cauchy_rows.append(
            {
                "name": name,
                "topology": topology,
                "round": round_state,
                "R3": scalar_3,
                "H_squared": h_sq,
                "hamiltonian": hamiltonian,
                "momentum": 0,
            }
        )

    q = Fraction(3, 2)
    berger_ricci, berger_scalar = berger_ricci_from_koszul(q)
    expected_diagonal = [Fraction(-1, 2), Fraction(-1, 2), Fraction(9, 2)]
    for i in range(3):
        for j in range(3):
            expected = expected_diagonal[i] if i == j else Fraction(0)
            census.require(berger_ricci[i][j] == expected, f"Berger Ricci {i}{j}")
    census.require(berger_scalar == Fraction(7, 2), "Berger scalar")
    census.require(len(set(expected_diagonal)) > 1, "Berger data are nonround")
    berger_h_sq = (2 * lam - berger_scalar) / 6
    census.require(berger_h_sq == Fraction(5, 12), "Berger H squared")
    census.require(berger_scalar + 6 * berger_h_sq == 2 * lam, "Berger Hamiltonian")
    cauchy_rows.append(
        {
            "name": "berger_S3_pure_trace",
            "topology": "S3",
            "round": False,
            "R3": berger_scalar,
            "H_squared": berger_h_sq,
            "hamiltonian": berger_scalar + 6 * berger_h_sq,
            "momentum": 0,
            "ricci_eigenvalues": expected_diagonal,
        }
    )

    # Exact rational points evaluate the actual G309 residual Q[a]=a*a''-(a')^2-1.
    cosh_checks = []
    for scale in map(Fraction, (Fraction(1, 3), Fraction(1, 2), 1, 2, 5)):
        for u in map(Fraction, (Fraction(1, 3), Fraction(1, 2), 1, 2, 3)):
            cosh_value = (u + 1 / u) / 2
            sinh_value = (1 / u - u) / 2
            scale_factor = scale
            a = scale_factor * cosh_value
            a_prime = sinh_value
            a_second = cosh_value / scale_factor
            residual = a * a_second - a_prime * a_prime - 1
            mutated_residual = a * a_second - a_prime * a_prime - 2
            census.require(residual == 0, f"G309 Q[a] scale={scale} u={u}")
            census.require(mutated_residual != 0, f"G309 Q[a] constant mutation scale={scale} u={u}")
            cosh_checks.append(
                {
                    "scale_X": scale,
                    "u": u,
                    "a": a,
                    "a_prime": a_prime,
                    "a_second": a_second,
                    "Q": residual,
                }
            )

    # Ricci-flat plane-wave witness: H=A(x^2-y^2) has vanishing transverse Laplacian but nonzero tide.
    plane_wave_rows = []
    for amplitude in map(Fraction, (-5, -2, -1, 1, 2, 5)):
        h_xx = 2 * amplitude
        h_yy = -2 * amplitude
        ricci_uu = -(h_xx + h_yy) / 2
        census.require(ricci_uu == 0, f"plane-wave Ricci amplitude={amplitude}")
        census.require(h_xx - h_yy != 0, f"plane-wave tide amplitude={amplitude}")
        plane_wave_rows.append(
            {"amplitude": amplitude, "Ric_uu": ricci_uu, "tidal_difference": h_xx - h_yy}
        )

    # Exhaustive finite type model: global acceptance precedes a response that factors through jets.
    histories = ("round", "product", "wave")
    jet_of = {"round": "j0", "product": "j0", "wave": "j1"}
    response_values = (0, 1)
    selector_count = 0
    selector_response_combinations = 0
    for selector_bits in range(1 << len(histories)):
        accepted = {
            history
            for index, history in enumerate(histories)
            if selector_bits & (1 << index)
        }
        selector_count += 1
        for j0_response in response_values:
            for j1_response in response_values:
                response_of_jet = {"j0": j0_response, "j1": j1_response}
                admitted_response = {
                    history: response_of_jet[jet_of[history]] for history in accepted
                }
                for left in accepted:
                    for right in accepted:
                        if jet_of[left] == jet_of[right]:
                            census.require(
                                admitted_response[left] == admitted_response[right],
                                f"local response factors through jet {selector_bits} {left} {right}",
                            )
                selector_response_combinations += 1

    separating_selector = {"round", "wave"}
    census.require("round" in separating_selector, "global selector accepts round witness")
    census.require("product" not in separating_selector, "global selector may reject equal-jet product")
    census.require(
        jet_of["round"] == jet_of["product"],
        "global selector may distinguish histories sharing one local jet",
    )

    hidden_history_response = {"round": 0, "product": 1, "wave": 0}
    hidden_factorization_failure = any(
        jet_of[left] == jet_of[right]
        and hidden_history_response[left] != hidden_history_response[right]
        for left in histories
        for right in histories
    )
    census.require(hidden_factorization_failure, "hidden history response fails equal-jet factorization")
    bootstrap_type_check = {
        "histories": len(histories),
        "jets": len(set(jet_of.values())),
        "selectors_exhausted": selector_count,
        "selector_response_combinations": selector_response_combinations,
        "equal_jet_histories_separable_globally": True,
        "jet_factored_local_response_compatible": True,
        "hidden_history_response_rejected": hidden_factorization_failure,
    }

    result = {
        "status": "PASS",
        "landing": "ACTIVE_EQUATION_DEFINES_MULTIBRANCH_EINSTEIN_ARENA__GLOBAL_ADMISSIBILITY_REMAINS_OPEN",
        "assertions": census.checks,
        "bianchi_divergence_coefficient": divergence_coefficient,
        "equivalent_connected_equation": "Ric_ab=Lambda*g_ab; dLambda=0",
        "branch_rows": branch_rows,
        "homothety_rows": homothety_rows,
        "cauchy_rows": cauchy_rows,
        "cosh_checks": cosh_checks,
        "plane_wave_rows": plane_wave_rows,
        "bootstrap_type_check": bootstrap_type_check,
        "global_predicate_type": "diffeomorphism-invariant acceptance predicate on complete histories",
        "existing_nonidentity_global_predicate_owned": False,
        "round_history_selected": False,
        "scale_selected": False,
        "physical_xmax_selected": False,
    }
    encoded = encode(result)
    payload = json.dumps(encoded, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
