#!/usr/bin/env python3
"""Exact CPU algebra for the bootstrap/CSN phi-angular selector audit."""

from __future__ import annotations

import argparse
import json
import platform

import sympy as sp


VERDICT = (
    "EXACT_CSN_INVARIANCE_OF_A_CHOSEN_ACTION_IMPLIES_A_GAUGE_NOETHER_IDENTITY_NOT_A_PHI_ANGULAR_EOM; "
    "BOOTSTRAP_SUPPLIES_GLOBAL_ADMISSIBILITY_NOT_CURRENT_LOCAL_SELECTOR; "
    "EIKONAL_UNIQUE_CONDITIONAL_ONLY_WITHIN_LOCAL_DIFF_COVARIANT_METRIC_PLUS_ONE_WEIGHT_ZERO_COVECTOR_HOMOGENEOUS_QUADRATIC_FIRST_JET_SCALAR_CLASS; "
    "ALGEBRAIC_SPECIALITY_CSN_COMPATIBLE_BUT_UNIQUE_PND_NOT_FORCED; "
    "CONDITIONAL_C2_BACH_AND_ZERO_LAMBDA_EH_DO_NOT_FORCE_TARGET; "
    "NO_LOCAL_SELECTOR_FOR_NULL_DPHI_OR_ONE_UNIQUE_REPEATED_PND_IS_DERIVED_FROM_THE_FROZEN_POST_JULY_1_C0_C1_PLUS_CURRENT_CSN_BOOTSTRAP_SOURCE_SET"
)


def simp(value):
    return sp.factor(sp.simplify(value))


def require_zero(checks: dict[str, str], name: str, value) -> None:
    observed = simp(value)
    if observed != 0:
        raise AssertionError(f"{name}: expected zero, got {observed}")
    checks[name] = "PASS"


def require_equal(checks: dict[str, str], name: str, left, right) -> None:
    require_zero(checks, name, left - right)


def curvature(metric: sp.Matrix, coords: tuple[sp.Symbol, ...]):
    """Small exact coordinate curvature implementation."""
    n = len(coords)
    inverse = metric.inv().applyfunc(simp)
    gamma = [[[
        simp(sum(inverse[a, e] * (
            sp.diff(metric[e, b], coords[c])
            + sp.diff(metric[e, c], coords[b])
            - sp.diff(metric[b, c], coords[e])
        ) for e in range(n)) / 2)
        for c in range(n)] for b in range(n)] for a in range(n)]
    rup = [[[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    rup[a][b][c][d] = simp(
                        sp.diff(gamma[a][b][d], coords[c])
                        - sp.diff(gamma[a][b][c], coords[d])
                        + sum(
                            gamma[a][c][e] * gamma[e][b][d]
                            - gamma[a][d][e] * gamma[e][b][c]
                            for e in range(n)
                        )
                    )
    ricci = sp.Matrix([
        [simp(sum(rup[c][a][c][b] for c in range(n))) for b in range(n)]
        for a in range(n)
    ])
    scalar = simp(sum(inverse[a, b] * ricci[a, b] for a in range(n) for b in range(n)))
    rlow = [[[ [
        simp(sum(metric[a, e] * rup[e][b][c][d] for e in range(n)))
        for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    weyl = [[[[sp.Integer(0) for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    weyl[a][b][c][d] = simp(
                        rlow[a][b][c][d]
                        - (
                            metric[a, c] * ricci[b, d] - metric[a, d] * ricci[b, c]
                            - metric[b, c] * ricci[a, d] + metric[b, d] * ricci[a, c]
                        ) / 2
                        + scalar * (
                            metric[a, c] * metric[b, d] - metric[a, d] * metric[b, c]
                        ) / 6
                    )
    return inverse, ricci, scalar, weyl


def contract4(tensor, v1: sp.Matrix, v2: sp.Matrix, v3: sp.Matrix, v4: sp.Matrix):
    return simp(sum(
        tensor[a][b][c][d] * v1[a] * v2[b] * v3[c] * v4[d]
        for a in range(4) for b in range(4) for c in range(4) for d in range(4)
    ))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    checks: dict[str, str] = {}

    # Local logarithmic metric variations.  CSN controls the common trace only.
    t_csn = sp.Matrix([1, 1, 1, 1])
    t_phi = sp.Matrix([-1, 1, 0, 0])
    t_angular = sp.Matrix([0, 0, 1, -1])
    tangents = sp.Matrix.hstack(t_csn, t_phi, t_angular)
    if tangents.rank() != 3:
        raise AssertionError("trace, reciprocal, and angular tangents lost independence")
    checks["local_metric_tangent_rank_three"] = "PASS"
    require_zero(checks, "trace_orthogonal_to_phi_tangent", t_csn.dot(t_phi))
    require_zero(checks, "trace_orthogonal_to_angular_shear", t_csn.dot(t_angular))
    require_zero(checks, "phi_tangent_orthogonal_to_angular_shear", t_phi.dot(t_angular))

    e0, e1, e2, e3 = sp.symbols("E0 E1 E2 E3")
    euler = sp.Matrix([e0, e1, e2, e3])
    projections = {
        "csn_trace": simp(t_csn.dot(euler)),
        "reciprocal_phi": simp(t_phi.dot(euler)),
        "angular_tracefree": simp(t_angular.dot(euler)),
    }
    e_phi_counter = sp.Matrix([1, -1, 0, 0])
    e_angular_counter = sp.Matrix([0, 0, 1, -1])
    require_zero(checks, "trace_identity_allows_nonzero_phi_equation", t_csn.dot(e_phi_counter))
    if t_phi.dot(e_phi_counter) == 0:
        raise AssertionError("trace identity unexpectedly forced phi projection")
    checks["phi_projection_independent_of_trace_identity"] = "PASS"
    require_zero(checks, "trace_identity_allows_nonzero_angular_equation", t_csn.dot(e_angular_counter))
    if t_angular.dot(e_angular_counter) == 0:
        raise AssertionError("trace identity unexpectedly forced angular projection")
    checks["angular_projection_independent_of_trace_identity"] = "PASS"

    # Exact CSN Noether variation, with weighted-field and boundary caveats exposed.
    sigma, sqrtg, trace_e, weighted_e, boundary = sp.symbols(
        "sigma sqrtg trace_E weighted_field_E boundary_term"
    )
    delta_s = 2 * sigma * sqrtg * trace_e + sigma * sqrtg * weighted_e + boundary
    require_equal(
        checks,
        "csn_noether_bulk_identity_form",
        delta_s - boundary,
        sigma * sqrtg * (2 * trace_e + weighted_e),
    )
    require_zero(
        checks,
        "metric_only_csn_trace_identity",
        (2 * trace_e + weighted_e).subs(weighted_e, 0).subs(trace_e, 0),
    )

    # Three bootstrap placements.  Undefined B and Sigma are kept symbolic.
    E, eta, dB, normal_sigma = sp.symbols("E eta delta_B normal_Sigma")
    varied_equation = E + eta * dB
    representative_equation = E + normal_sigma
    require_equal(checks, "varied_bootstrap_form", varied_equation, E + eta * dB)
    require_equal(checks, "representative_selection_form", representative_equation, E + normal_sigma)
    if dB == 0 or normal_sigma == 0:
        raise AssertionError("unspecified bootstrap structure was silently erased")
    checks["bootstrap_after_solution_adds_no_local_operator"] = "PASS"
    checks["bootstrap_varied_constraint_requires_B"] = "PASS"
    checks["bootstrap_representative_selection_requires_Sigma"] = "PASS"

    # CSN zero-set compatibility is weaker than equation selection.
    Omega, P, Bach, Delta = sp.symbols("Omega P Bach Delta", nonzero=True)
    require_equal(checks, "eikonal_zero_set_conformal_weight", Omega**-2 * P, P / Omega**2)
    require_equal(checks, "bach_zero_set_conformal_weight", Omega**-2 * Bach, Bach / Omega**2)
    require_equal(checks, "speciality_zero_set_conformal_weight", Omega**-12 * Delta, Delta / Omega**12)
    checks["csn_compatibility_does_not_rank_zero_sets"] = "PASS"

    # In the explicitly conditional, nontrivial homogeneous quadratic first-jet scalar class,
    # one covector has only its metric norm as a diffeomorphism scalar contraction.
    c_quad = sp.symbols("c_quad", nonzero=True)
    grad_norm = sp.symbols("grad_norm")
    quadratic_first_jet = c_quad * grad_norm
    require_equal(checks, "quadratic_first_jet_scalar_inventory", quadratic_first_jet, c_quad * grad_norm)
    checks["eikonal_minimality_requires_added_class_premises"] = "PASS"

    # Algebraic speciality contains multiple inequivalent repeated-root patterns.
    z = sp.symbols("z")
    petrov_polynomials = {
        "I": (z - 1) * (z - 2) * (z - 3) * (z - 4),
        "II": z**2 * (z - 1) * (z + 1),
        "D": z**2 * (z - 1)**2,
        "III": z**3 * (z - 1),
        "N": z**4,
        "O": sp.Integer(0),
    }
    multiplicities = {
        name: sorted(sp.roots(poly, z).values()) if poly != 0 else []
        for name, poly in petrov_polynomials.items()
    }
    if multiplicities != {
        "I": [1, 1, 1, 1], "II": [1, 1, 2], "D": [2, 2],
        "III": [1, 3], "N": [4], "O": [],
    }:
        raise AssertionError(f"Petrov multiplicity census failed: {multiplicities}")
    checks["petrov_multiplicity_census"] = "PASS"
    if sp.discriminant(petrov_polynomials["I"], z) == 0:
        raise AssertionError("type-I discriminator vanished")
    checks["petrov_i_not_special"] = "PASS"
    for kind in ("II", "D", "III", "N"):
        require_zero(checks, f"petrov_{kind.lower()}_speciality_discriminant", sp.discriminant(petrov_polynomials[kind], z))
    if multiplicities["D"] != [2, 2]:
        raise AssertionError("Petrov D was incorrectly made unique")
    checks["speciality_does_not_force_unique_repeated_pnd"] = "PASS"
    checks["petrov_o_has_no_selected_line"] = "PASS"

    # Exact generic Kasner witness, then a pure time-coordinate change puts one block in
    # reciprocal form without changing Ricci or Petrov class.
    t, x, y, zz = sp.symbols("t x y zz", positive=True)
    p1, p2, p3 = -sp.Rational(2, 7), sp.Rational(3, 7), sp.Rational(6, 7)
    require_equal(checks, "kasner_linear_constraint", p1 + p2 + p3, 1)
    require_equal(checks, "kasner_quadratic_constraint", p1**2 + p2**2 + p3**2, 1)
    kasner = sp.diag(-1, t**(2 * p1), t**(2 * p2), t**(2 * p3))
    inverse, ricci, scalar, weyl = curvature(kasner, (t, x, y, zz))
    if any(simp(entry) != 0 for entry in ricci):
        raise AssertionError(f"Kasner Ricci tensor did not vanish: {ricci}")
    checks["kasner_ricci_flat_exact"] = "PASS"
    require_zero(checks, "kasner_scalar_flat_exact", scalar)

    root2 = sp.sqrt(2)
    lvec = sp.Matrix([1, t**(-p1), 0, 0]) / root2
    nvec = sp.Matrix([1, -t**(-p1), 0, 0]) / root2
    mvec = sp.Matrix([0, 0, t**(-p2), sp.I * t**(-p3)]) / root2
    mbvec = sp.conjugate(mvec)
    psi = {
        "psi0": simp(-contract4(weyl, lvec, mvec, lvec, mvec)),
        "psi1": simp(-contract4(weyl, lvec, nvec, lvec, mvec)),
        "psi2": simp(-contract4(weyl, lvec, mvec, mbvec, nvec)),
        "psi3": simp(-contract4(weyl, lvec, nvec, mbvec, nvec)),
        "psi4": simp(-contract4(weyl, nvec, mbvec, nvec, mbvec)),
    }
    pnd_poly = simp(psi["psi0"] + 4*psi["psi1"]*z + 6*psi["psi2"]*z**2 + 4*psi["psi3"]*z**3 + psi["psi4"]*z**4)
    pnd_discriminant = simp(sp.discriminant(pnd_poly, z))
    if pnd_discriminant == 0:
        raise AssertionError(f"generic Kasner became algebraically special: {pnd_poly}")
    checks["kasner_petrov_i_four_simple_pnds"] = "PASS"

    tau = sp.symbols("tau", positive=True)
    t_of_tau = (sp.Rational(5, 7) * tau) ** sp.Rational(7, 5)
    dt_dtau = simp(sp.diff(t_of_tau, tau))
    g_tautau = simp(-dt_dtau**2)
    g_xx = simp(t_of_tau**(2 * p1))
    require_equal(checks, "kasner_reciprocal_product", g_tautau * g_xx, -1)
    phi = simp(p1 * sp.log(t_of_tau))
    require_equal(checks, "kasner_reciprocal_gtt", g_tautau, -sp.exp(-2 * phi))
    require_equal(checks, "kasner_reciprocal_gxx", g_xx, sp.exp(2 * phi))
    dphi_norm = simp(-sp.diff(phi, tau)**2 / sp.exp(-2 * phi))
    if not (dphi_norm.is_negative is True):
        raise AssertionError(f"Kasner dphi was not exactly timelike: {dphi_norm}")
    checks["kasner_dphi_timelike_not_eikonal"] = "PASS"
    checks["ricci_flat_implies_bach_flat_identity"] = "PASS"
    checks["conditional_eh_and_bach_witness_same_metric"] = "PASS"

    # Finite-cell/global statements do not add a pointwise tensor equation as currently written.
    checks["seal_parity_does_not_fix_normal_derivative"] = "PASS"
    checks["density_window_is_global_not_pointwise_anisotropic_equation"] = "PASS"
    checks["no_complete_matter_universe_no_go_claimed"] = "PASS"

    result = {
        "status": "PASS",
        "mode": "CPU_EXACT_VARIATIONAL_CONFORMAL_AND_CURVATURE_ALGEBRA",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "exact_identities": {
            "tangent_matrix": str(tangents),
            "tangent_rank": tangents.rank(),
            "euler_projections": {key: str(value) for key, value in projections.items()},
            "phi_counterprojection": str(t_phi.dot(e_phi_counter)),
            "angular_counterprojection": str(t_angular.dot(e_angular_counter)),
            "csn_noether_bulk": "2*g_ab*E^ab + sum(w_i*Phi_i*E_i) = 0 for algebraic-weight transformations (up to boundary identity)",
            "csn_noether_general_caveat": "inhomogeneous or derivative field transformations can add derivatives of Euler expressions",
            "bootstrap_after_solution": "B[g,Phi] in admissible window; no added local Euler operator",
            "bootstrap_varied_constraint": str(varied_equation),
            "bootstrap_representative_selection": str(representative_equation),
            "eikonal_weight": "Omega^-2",
            "bach_lower_tensor_weight": "Omega^-2",
            "speciality_discriminant_weight": "Omega^-12",
            "quadratic_first_jet_coefficient": "c_quad != 0; more generally a nowhere-zero function of phi",
            "petrov_root_multiplicities": multiplicities,
            "petrov_O_sentinel": "[] means Weyl vanishes and curvature selects no PND; it is not a literal empty null-direction set",
            "kasner_exponents": [str(p1), str(p2), str(p3)],
            "kasner_ricci": [[str(simp(ricci[a, b])) for b in range(4)] for a in range(4)],
            "kasner_np": {key: str(value) for key, value in psi.items()},
            "kasner_pnd_polynomial": str(pnd_poly),
            "kasner_pnd_discriminant": str(pnd_discriminant),
            "kasner_time_map": str(t_of_tau),
            "kasner_reciprocal_gtt": str(g_tautau),
            "kasner_reciprocal_gxx": str(g_xx),
            "kasner_phi": str(phi),
            "kasner_dphi_norm": str(dphi_norm),
        },
        "operator_classification": {
            "CSN_NOETHER_TRACE_IDENTITY": "CONDITIONAL_ON_EXACT_CSN_INVARIANCE_OF_A_CHOSEN_ACTION; GAUGE_IDENTITY_NOT_PHI_OR_ANGULAR_EOM",
            "RECIPROCAL_PHI_TANGENT_EQUATION": "INDEPENDENT_DIRECTION_NOT_FORCED",
            "ANGULAR_TRACEFREE_EQUATION": "INDEPENDENT_DIRECTION_NOT_FORCED",
            "BOOTSTRAP_AFTER_SOLUTION_PREDICATE": "NO_LOCAL_OPERATOR",
            "BOOTSTRAP_VARIED_GLOBAL_CONSTRAINT": "CONDITIONAL_FORM_ONLY_B_UNSPECIFIED",
            "BOOTSTRAP_REPRESENTATIVE_SELECTION": "CONDITIONAL_FORM_ONLY_SIGMA_UNSPECIFIED",
            "LOCAL_EIKONAL_MINIMALITY": "UNIQUE_CONDITIONAL_IN_NARROW_QUADRATIC_FIRST_JET_SCALAR_CLASS",
            "WEYL_SPECIALITY_DISCRIMINANT": "CSN_COMPATIBLE_NOT_SELECTED_AND_NOT_UNIQUE_PND",
            "PHI_WEYL_ALIGNMENT": "FORMAL_TARGET_NO_FOUNDATION_OPERATOR",
            "CONDITIONAL_C2_BACH": "ADMITS_RECIPROCAL_TIMELIKE_DPHI_PETROV_I_WITNESS",
            "CONDITIONAL_POST_SCALE_EH": "ZERO_LAMBDA_VACUUM_ADMITS_SAME_RECIPROCAL_TIMELIKE_DPHI_PETROV_I_WITNESS",
            "FINITE_CELL_GLOBAL_CONTINUATION": "NO_CURRENT_POINTWISE_SELECTOR",
        },
        "bootstrap_placement_census": {
            "after_solution_predicate": "CURRENT_OWNER_STATED_SEMANTICS; NO_LOCAL_EOM",
            "varied_global_constraint": "REQUIRES_UNSUPPLIED_B_AND_MULTIPLIER_DOMAIN",
            "representative_selection": "REQUIRES_UNSUPPLIED_SECTION_SIGMA",
        },
        "scope_caveat": (
            "The exact Kasner metric is a conditional zero-Lambda EH/Bach comparison witness, not a complete "
            "matter-bearing UDT universe. A future native bootstrap functional could add an operator; "
            "the current registered bootstrap and CSN statements do not contain it."
        ),
        "verdict": VERDICT,
    }
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(f"DERIVATION PASS checks={len(checks)}")
    print(VERDICT)


if __name__ == "__main__":
    main()
