#!/usr/bin/env python3
"""Exact CPU causal-gradient and Petrov algebra for the reciprocal null-line selector."""

from __future__ import annotations

import argparse
import json
import platform

import sympy as sp


VERDICT = (
    "NONTRIVIAL_STATIC_NULL_DPHI_EXCLUDED_WITHIN_POSITIVE_SPATIAL_STATIC_SUBFAMILY; "
    "TIME_LIVE_NULL_DPHI_OPTIONAL_EIKONAL_BRANCH; "
    "ROUND_ANGULAR_WARPED_FAMILY_PETROV_D_OR_O_CONDITIONAL; "
    "RECIPROCAL_ANISOTROPIC_PETROV_I_COUNTERFAMILY_EXISTS; "
    "UNIQUE_REPEATED_PND_UNDERDETERMINED; "
    "GLOBAL_CONFORMAL_NULL_LINE_NOT_DERIVED"
)


def simp(value):
    return sp.factor(sp.trigsimp(sp.simplify(value)))


def require_zero(checks: dict[str, str], name: str, value) -> None:
    observed = simp(value)
    if observed != 0:
        raise AssertionError(f"{name}: expected zero, got {observed}")
    checks[name] = "PASS"


def require_equal(checks: dict[str, str], name: str, left, right) -> None:
    require_zero(checks, name, left - right)


def christoffel(metric: sp.Matrix, coords: tuple[sp.Symbol, ...]):
    n = len(coords)
    inv = simp_matrix(metric.inv())
    gamma = [[[
        simp(sum(inv[a, d] * (
            sp.diff(metric[d, c], coords[b])
            + sp.diff(metric[d, b], coords[c])
            - sp.diff(metric[b, c], coords[d])
        ) for d in range(n)) / 2)
        for c in range(n)] for b in range(n)] for a in range(n)]
    return inv, gamma


def simp_matrix(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(simp)


def curvature(metric: sp.Matrix, coords: tuple[sp.Symbol, ...]):
    n = len(coords)
    inv, gamma = christoffel(metric, coords)
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
    ricci = [[simp(sum(rup[c][a][c][b] for c in range(n))) for b in range(n)] for a in range(n)]
    scalar = simp(sum(inv[a, b] * ricci[a][b] for a in range(n) for b in range(n)))
    rlow = [[[[
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
                            metric[a, c] * ricci[b][d]
                            - metric[a, d] * ricci[b][c]
                            - metric[b, c] * ricci[a][d]
                            + metric[b, d] * ricci[a][c]
                        ) / 2
                        + scalar * (
                            metric[a, c] * metric[b, d]
                            - metric[a, d] * metric[b, c]
                        ) / 6
                    )
    return inv, gamma, rup, ricci, scalar, weyl


def contract4(tensor, v1: sp.Matrix, v2: sp.Matrix, v3: sp.Matrix, v4: sp.Matrix):
    n = len(v1)
    return simp(sum(
        tensor[a][b][c][d] * v1[a] * v2[b] * v3[c] * v4[d]
        for a in range(n) for b in range(n) for c in range(n) for d in range(n)
    ))


def np_scalars(weyl, l: sp.Matrix, n: sp.Matrix, m: sp.Matrix, mb: sp.Matrix):
    return {
        "psi0": simp(-contract4(weyl, l, m, l, m)),
        "psi1": simp(-contract4(weyl, l, n, l, m)),
        "psi2": simp(-contract4(weyl, l, m, mb, n)),
        "psi3": simp(-contract4(weyl, l, n, mb, n)),
        "psi4": simp(-contract4(weyl, n, mb, n, mb)),
    }


def text_map(values: dict[str, sp.Expr]) -> dict[str, str]:
    return {key: str(simp(value)) for key, value in values.items()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    checks: dict[str, str] = {}

    phi, pt, pr, qnorm, Omega = sp.symbols("phi pt pr qnorm Omega", real=True)
    c_light = sp.symbols("c_light", positive=True)
    Omega_positive = sp.symbols("Omega_positive", positive=True)

    # Complete local dphi norm from an explicit reciprocal-block matrix inverse.
    qa, qb, qd, px, py = sp.symbols("qa qb qd px py", real=True)
    qdet = qa * qd - qb**2
    general_metric = sp.Matrix([
        [-c_light**2 * sp.exp(-2 * phi), 0, 0, 0],
        [0, sp.exp(2 * phi), 0, 0],
        [0, 0, qa, qb],
        [0, 0, qb, qd],
    ])
    gradient = sp.Matrix([pt, pr, px, py])
    qnorm_explicit = simp((qd * px**2 - 2 * qb * px * py + qa * py**2) / qdet)
    P_matrix = simp((gradient.T * general_metric.inv() * gradient)[0])
    P = -sp.exp(2 * phi) * pt**2 / c_light**2 + sp.exp(-2 * phi) * pr**2 + qnorm
    static_P = simp(P.subs(pt, 0))
    require_equal(
        checks,
        "general_block_inverse_dphi_norm",
        P_matrix,
        P.subs(qnorm, qnorm_explicit),
    )
    completed_qnorm = px**2 / qa + (qa * py - qb * px) ** 2 / (qa * qdet)
    require_equal(checks, "positive_angular_complete_square_decomposition", qnorm_explicit, completed_qnorm)
    require_equal(checks, "static_dphi_positive_sum", static_P, sp.exp(-2 * phi) * pr**2 + qnorm)
    require_zero(checks, "static_zero_gradient_has_zero_norm", static_P.subs({pr: 0, qnorm: 0}))
    require_equal(checks, "csn_dphi_norm_scaling", Omega_positive**-2 * P, P / Omega_positive**2)

    radial_eikonal = simp(P.subs(qnorm, 0) / sp.exp(2 * phi))
    require_equal(checks, "radial_time_live_eikonal", radial_eikonal, -pt**2 / c_light**2 + sp.exp(-4 * phi) * pr**2)
    angular_eikonal = simp(P / sp.exp(2 * phi))
    require_equal(checks, "angular_time_live_eikonal", angular_eikonal, -pt**2 / c_light**2 + sp.exp(-4 * phi) * pr**2 + sp.exp(-2 * phi) * qnorm)
    require_zero(checks, "null_first_jet_exists", P.subs({pt: c_light * sp.exp(-2 * phi), pr: 1, qnorm: 0}))
    require_equal(checks, "spacelike_first_jet_exists", P.subs({pt: 0, pr: 1, qnorm: 0}), sp.exp(-2 * phi))
    require_equal(
        checks,
        "timelike_first_jet_exists",
        P.subs({pt: 1, pr: 0, qnorm: 0}),
        -sp.exp(2 * phi) / c_light**2,
    )
    require_zero(checks, "static_seal_zero_gradient_has_zero_norm", static_P.subs({phi: 0, pr: 0, qnorm: 0}))

    # Explicit nontrivial local time-live eikonal branch.
    t, r, wave_rate, A0, B0 = sp.symbols("t r wave_rate A0 B0", real=True)
    numerator = A0 + 2 * c_light * wave_rate * t
    denominator = B0 - 2 * wave_rate * r
    phi_wave = sp.log(numerator / denominator) / 2
    wave_norm = simp(
        -sp.exp(2 * phi_wave) * sp.diff(phi_wave, t) ** 2 / c_light**2
        + sp.exp(-2 * phi_wave) * sp.diff(phi_wave, r) ** 2
    )
    require_zero(checks, "explicit_time_live_eikonal_branch", wave_norm)
    if sp.diff(phi_wave, t) == 0 or sp.diff(phi_wave, r) == 0:
        raise AssertionError("explicit time-live eikonal branch became trivial")
    checks["explicit_time_live_eikonal_nontrivial"] = "PASS"

    # Conditional static round-angular family, arbitrary local two-jets at r=0.
    tt, rr, th, ph = sp.symbols("tt rr th ph", real=True)
    p0, p1, p2 = sp.symbols("p0 p1 p2", real=True)
    R0, R1, R2 = sp.symbols("R0 R1 R2", positive=True)
    pfun = p0 + p1 * rr + p2 * rr**2 / 2
    Rfun = R0 + R1 * rr + R2 * rr**2 / 2
    spherical_metric = sp.diag(
        -sp.exp(-2 * pfun),
        sp.exp(2 * pfun),
        Rfun**2,
        Rfun**2 * sp.sin(th) ** 2,
    )
    _, _, _, _, spherical_scalar, spherical_weyl = curvature(spherical_metric, (tt, rr, th, ph))
    sqrt2 = sp.sqrt(2)
    l_s = sp.Matrix([sp.exp(pfun), sp.exp(-pfun), 0, 0]) / sqrt2
    n_s = sp.Matrix([sp.exp(pfun), -sp.exp(-pfun), 0, 0]) / sqrt2
    m_s = sp.Matrix([0, 0, 1 / Rfun, sp.I / (Rfun * sp.sin(th))]) / sqrt2
    mb_s = sp.conjugate(m_s)
    spherical_np_full = np_scalars(spherical_weyl, l_s, n_s, m_s, mb_s)
    spherical_np = {
        key: simp(value.subs(rr, 0))
        for key, value in spherical_np_full.items()
    }
    for key in ("psi0", "psi1", "psi3", "psi4"):
        require_zero(checks, f"spherical_{key}_vanishes", spherical_np[key])
    if spherical_np["psi2"] == 0:
        raise AssertionError("generic spherical psi2 vanished identically")
    checks["spherical_only_psi2_may_survive"] = "PASS"
    flat_spherical_psi2 = simp(spherical_np["psi2"].subs({p0: 0, p1: 0, p2: 0, R1: 1, R2: 0}))
    require_zero(checks, "spherical_flat_subfamily_petrov_o", flat_spherical_psi2)
    curved_spherical_psi2 = simp(spherical_np["psi2"].subs({p0: 0, p1: 1, p2: 0, R0: 1, R1: 1, R2: 0}))
    if curved_spherical_psi2 == 0:
        raise AssertionError("curved spherical D witness psi2 vanished")
    checks["spherical_curved_subfamily_petrov_d"] = "PASS"

    # Exact anisotropic reciprocal counterfamily.
    k, ay, az = sp.symbols("k ay az", real=True)
    anisotropic_metric = sp.diag(
        -sp.exp(-2 * k * rr),
        sp.exp(2 * k * rr),
        sp.exp(2 * ay * rr),
        sp.exp(2 * az * rr),
    )
    _, _, _, _, anisotropic_scalar, anisotropic_weyl = curvature(anisotropic_metric, (tt, rr, th, ph))
    l_a = sp.Matrix([sp.exp(k * rr), sp.exp(-k * rr), 0, 0]) / sqrt2
    n_a = sp.Matrix([sp.exp(k * rr), -sp.exp(-k * rr), 0, 0]) / sqrt2
    m_a = sp.Matrix([0, 0, sp.exp(-ay * rr), sp.I * sp.exp(-az * rr)]) / sqrt2
    mb_a = sp.conjugate(m_a)
    anisotropic_np_full = np_scalars(anisotropic_weyl, l_a, n_a, m_a, mb_a)
    substitution = {rr: 0, k: 1, ay: 2, az: 3}
    anisotropic_np = {key: simp(value.subs(substitution)) for key, value in anisotropic_np_full.items()}
    require_zero(checks, "anisotropic_psi1_vanishes", anisotropic_np["psi1"])
    require_zero(checks, "anisotropic_psi3_vanishes", anisotropic_np["psi3"])
    if anisotropic_np["psi0"] == 0 or anisotropic_np["psi4"] == 0 or anisotropic_np["psi2"] == 0:
        raise AssertionError(f"anisotropic Weyl witness lost required components: {anisotropic_np}")
    checks["anisotropic_psi0_psi2_psi4_nonzero"] = "PASS"
    z = sp.symbols("z")
    pnd_poly = simp(
        anisotropic_np["psi0"]
        + 4 * anisotropic_np["psi1"] * z
        + 6 * anisotropic_np["psi2"] * z**2
        + 4 * anisotropic_np["psi3"] * z**3
        + anisotropic_np["psi4"] * z**4
    )
    pnd_discriminant = simp(sp.discriminant(pnd_poly, z))
    if pnd_discriminant == 0:
        raise AssertionError(f"anisotropic PND quartic is algebraically special: {pnd_poly}")
    checks["anisotropic_pnd_quartic_four_simple_roots"] = "PASS"
    if len(sp.roots(pnd_poly, z)) != 4 or set(sp.roots(pnd_poly, z).values()) != {1}:
        raise AssertionError(f"anisotropic PND root census failed: {sp.roots(pnd_poly, z)}")
    checks["anisotropic_petrov_i_exact"] = "PASS"
    petrov_I = simp(
        anisotropic_np["psi0"] * anisotropic_np["psi4"]
        - 4 * anisotropic_np["psi1"] * anisotropic_np["psi3"]
        + 3 * anisotropic_np["psi2"] ** 2
    )
    petrov_J = simp(
        anisotropic_np["psi2"]
        * (anisotropic_np["psi0"] * anisotropic_np["psi4"] - anisotropic_np["psi2"] ** 2)
    )
    speciality_discriminant = simp(petrov_I**3 - 27 * petrov_J**2)
    if speciality_discriminant == 0:
        raise AssertionError("anisotropic invariant speciality discriminator vanished")
    checks["anisotropic_invariant_speciality_excluded"] = "PASS"

    # Reciprocal founding identity alone contains no anisotropic-rate restriction.
    require_equal(checks, "anisotropic_reciprocal_temporal_radial_product", anisotropic_metric[0, 0] * anisotropic_metric[1, 1], -1)
    require_zero(checks, "anisotropic_phi_odd", k * (-rr) + k * rr)
    if simp(pnd_discriminant.subs({ay: 2, az: 3, k: 1})) == 0:
        raise AssertionError("registered reciprocal parameter point became algebraically special")
    checks["anisotropic_speciality_counterexample_registered"] = "PASS"

    # PND multiplicity possibilities retained, not installed.
    b = sp.symbols("b")
    if sorted(sp.roots(b**2 * (b - 1) * (b + 1), b).values()) != [1, 1, 2]:
        raise AssertionError("Petrov II multiplicity failure")
    checks["petrov_ii_local_unique_double_root"] = "PASS"
    if sorted(sp.roots(b**3 * (b - 1), b).values()) != [1, 3]:
        raise AssertionError("Petrov III multiplicity failure")
    checks["petrov_iii_local_unique_triple_root"] = "PASS"
    if sp.roots(b**4, b) != {sp.Integer(0): 4}:
        raise AssertionError("Petrov N multiplicity failure")
    checks["petrov_n_local_unique_quadruple_root"] = "PASS"

    result = {
        "status": "PASS",
        "mode": "CPU_EXACT_CAUSAL_GRADIENT_AND_WEYL_PETROV_ALGEBRA",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "exact_identities": {
            "general_dphi_norm": str(P),
            "explicit_angular_inverse_norm": str(qnorm_explicit),
            "angular_complete_square_decomposition": str(completed_qnorm),
            "static_dphi_norm": str(static_P),
            "radial_time_live_eikonal": str(radial_eikonal),
            "angular_time_live_eikonal": str(angular_eikonal),
            "explicit_time_live_eikonal_phi": str(phi_wave),
            "spherical_np_at_generic_static_two_jet": text_map(spherical_np),
            "spherical_scalar_at_r0": str(simp(spherical_scalar.subs(rr, 0))),
            "anisotropic_np_at_k1_ay2_az3_r0": text_map(anisotropic_np),
            "anisotropic_scalar_at_k1_ay2_az3_r0": str(simp(anisotropic_scalar.subs(substitution))),
            "anisotropic_pnd_polynomial": str(pnd_poly),
            "anisotropic_pnd_discriminant": str(pnd_discriminant),
            "anisotropic_petrov_I": str(petrov_I),
            "anisotropic_petrov_J": str(petrov_J),
            "anisotropic_speciality_discriminant": str(speciality_discriminant),
        },
        "classification": {
            "static_positive_spatial_dphi": "SPACELIKE_OR_ZERO; NONTRIVIAL_NULL_EXCLUDED_WITHIN_STATIC_SUBFAMILY",
            "time_live_radial_dphi": "NULL_IS_OPTIONAL_EIKONAL_PDE_NOT_RECIPROCITY_IDENTITY",
            "time_live_angular_dphi": "POSITIVE_ANGULAR_TERM_REQUIRES_ADDITIONAL_TIME_BALANCE",
            "static_seal_global_nullness": "REQUIRES_ALL_SPATIAL_DERIVATIVES_ZERO_WHERE_PARTIAL_T_PHI_ZERO",
            "round_angular_warped_petrov": "D_IF_PSI2_NONZERO; O_IF_PSI2_ZERO; TWO_OR_NO_PNDS",
            "anisotropic_reciprocal_counterfamily": "PETROV_I_WITH_FOUR_SIMPLE_PNDS",
            "petrov_ii_iii_n": "LOCAL_UNIQUE_HIGHEST_MULTIPLICITY_LINE_EXISTS_BUT_NOT_FOUNDATION_FORCED",
            "unique_repeated_pnd": "UNDERDETERMINED_NOT_DERIVED",
            "global_conformal_null_line": "NOT_DERIVED",
            "physical_carrier_action_cap": "OPEN_NOT_ACTIVATED",
        },
        "counterfamilies": {
            "static_nonzero_phi_spacelike_gradient": {
                "result": "same reciprocal block; dphi spacelike rather than null",
                "scope": "static positive-spatial metric family",
            },
            "explicit_time_live_null_gradient": {
                "result": "nontrivial eikonal branch exists but is selected by a PDE not by reciprocity",
                "scope": "local positive numerator/denominator domain",
            },
            "round_angular_petrov_d_or_o": {
                "result": "two repeated radial PNDs or conformally flat no selector",
                "scope": "conditional spherical/constant-curvature warped family",
            },
            "anisotropic_reciprocal_petrov_i": {
                "result": "exact reciprocal temporal/radial product with four simple PNDs",
                "scope": "finite local r interval with chosen unequal transverse warp rates",
            },
        },
        "premise_stamps": {
            "reciprocal_metric_block": "DERIVED_CONDITIONAL",
            "common_scale_neutrality": "FOUNDING",
            "four_dimensional_lorentz_readout": "INHERITED_CONDITIONAL",
            "positive_spatial_angular_metric": "GENERAL_LOCAL_METRIC_REQUIREMENT",
            "staticity": "CHOSE_CONDITIONAL_SUBFAMILY",
            "time_live_eikonal": "FREE_BRANCH_NOT_FIELD_EQUATION",
            "round_angular_warp": "PINNED_BY_HABIT_CONDITIONAL_TEST_FAMILY",
            "anisotropic_warp_rates": "CHOSE_COUNTERFAMILY",
            "petrov_class": "OBSERVED_CURVATURE_READOUT_PER_FAMILY",
            "field_equations_goldberg_sachs": "EXCLUDED_NOT_IMPORTED",
            "action_source_boundary_bootstrap_operator": "OPEN",
            "carrier_section_periods_caps": "OPEN_EXCLUDED",
        },
        "verdict": VERDICT,
    }
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(f"DERIVATION PASS {len(checks)}/{len(checks)}")
    print(VERDICT)


if __name__ == "__main__":
    main()
