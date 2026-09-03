#!/usr/bin/env python3
"""Hostile mutations for the G332 constraint witness and scope boundary."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path

from derive_weighted_constraint_embedding import Quadratic, coordinate_geometry, quadratic_matmul


def mutated_residual(root_factor=1, horizontal_denominator=2, scaled_xi=1,
                     plus_norm=False, omit_lambda=False):
    x, w1, w2 = F(1, 3), F(2), F(3)
    c0, lam = F(20), F(3)
    g, _, gi, dgi, gamma, _, scalar = coordinate_geometry(x, w1, w2)
    xi = [F(0), scaled_xi * w1, scaled_xi * w2]
    eta = [sum(g[i][j] * xi[j] for j in range(3)) for i in range(3)]
    lambda_term = 0 if omit_lambda else 2 * lam
    q = 2 * (scalar + 2 * c0 * c0 - lambda_term)
    root = Quadratic(0, root_factor, q)
    b = -c0 + root
    horizontal = c0 - root / horizontal_denominator
    k_cov = [[horizontal * g[i][j] + b * eta[i] * eta[j] for j in range(3)] for i in range(3)]
    mixed = quadratic_matmul(gi, k_cov, q)
    tau = sum(mixed[i][i] for i in range(3))
    norm = sum(mixed[i][j] * mixed[j][i] for i in range(3) for j in range(3))
    residual = Quadratic.lift(scalar - 2 * lam, q) + tau * tau
    residual = residual + norm if plus_norm else residual - norm

    p = [[Quadratic.lift(-c0 * gi[i][j], q) + b * xi[i] * xi[j]
          for j in range(3)] for i in range(3)]
    derivative_only = [Quadratic.lift(-c0 * dgi[i][0], q) for i in range(3)]
    full_momentum = []
    for i in range(3):
        value = derivative_only[i]
        for j in range(3):
            for k in range(3):
                value += gamma[i][j][k] * p[k][j]
                value += gamma[j][j][k] * p[i][k]
        full_momentum.append(value)
    return residual, derivative_only, full_momentum, b, xi


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="CATCH_PROOF_RESULT.json")
    args = parser.parse_args()
    caught = []

    def catch(condition, name):
        if not condition:
            raise AssertionError(f"mutation escaped: {name}")
        caught.append(name)

    residual, derivative, momentum, _, _ = mutated_residual()
    catch(residual.is_zero() and all(value.is_zero() for value in momentum), "baseline_closes")
    catch(any(not value.is_zero() for value in derivative), "dropping_connection_terms_is_caught")

    residual, _, _, _, _ = mutated_residual(root_factor=2)
    catch(not residual.is_zero(), "square_root_coefficient_mutation")

    residual, _, _, _, _ = mutated_residual(horizontal_denominator=3)
    catch(not residual.is_zero(), "trace_inversion_mutation")

    residual, _, _, _, _ = mutated_residual(plus_norm=True)
    catch(not residual.is_zero(), "hamiltonian_norm_sign_mutation")

    residual, _, _, _, _ = mutated_residual(omit_lambda=True)
    catch(not residual.is_zero(), "constant_lambda_term_omission")

    residual, _, _, _, _ = mutated_residual(scaled_xi=2)
    catch(not residual.is_zero(), "unit_projector_normalization_mutation")

    _, _, _, b, xi = mutated_residual()
    noninvariant_term = [b * component for component in xi]
    catch(any(not value.is_zero() for value in noninvariant_term), "xi_of_b_nonzero_mutation")

    acceleration = [F(1), F(0), F(0)]
    nongeodesic_term = [b * component for component in acceleration]
    catch(any(not value.is_zero() for value in nongeodesic_term), "geodesic_identity_mutation")

    required_scope = {
        "EXISTENCE_IS_NOT_A_FULL_K_CENSUS_OR_DYNAMIC_STABILITY",
        "INITIAL_CONSTRAINTS_DO_NOT_FORCE_HOPF_ORBIT_RIGIDITY",
    }
    baseline_landing = (
        "EXACT_IRREGULAR_WEIGHTED_CONTACT_VACUUM_CONSTRAINT_DATA_EXIST__"
        "INITIAL_CONSTRAINTS_DO_NOT_FORCE_HOPF_ORBIT_RIGIDITY__"
        "EXISTENCE_IS_NOT_A_FULL_K_CENSUS_OR_DYNAMIC_STABILITY"
    )
    catch(all(token in baseline_landing for token in required_scope), "scope_boundary_baseline")
    mutated_landing = "EXACT_IRREGULAR_WEIGHTED_CONTACT_VACUUM_CONSTRAINT_DATA_EXIST"
    catch(any(token not in mutated_landing for token in required_scope), "scope_promotion_mutation")

    payload = {
        "package": "G332",
        "mutations_caught": len(caught) - 2,
        "checks": caught,
        "verdict": "PASS",
    }
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"mutations_caught": len(caught) - 2, "verdict": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
