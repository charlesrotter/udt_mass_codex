#!/usr/bin/env python3
"""Exact symbolic controller for the terminal reciprocal-c pair-metric derivation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent


class Checks:
    def __init__(self) -> None:
        self.rows: list[dict[str, object]] = []

    def exact(self, name: str, actual: object, expected: object) -> None:
        passed = bool(sp.simplify(sp.sympify(actual) - sp.sympify(expected)) == 0)
        self.rows.append(
            {
                "name": name,
                "passed": passed,
                "actual": str(sp.simplify(actual)),
                "expected": str(sp.simplify(expected)),
            }
        )

    def truth(self, name: str, condition: object) -> None:
        passed = bool(condition)
        self.rows.append(
            {"name": name, "passed": passed, "actual": str(passed), "expected": "True"}
        )


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def replay_manifest(checks: Checks) -> None:
    lines = (PACKAGE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()
    checks.exact("source_manifest_column_count_header", len(lines[0].split("\t")), 3)
    for index, line in enumerate(lines[1:], start=1):
        expected, relpath, source_ref = line.split("\t")
        if source_ref == "WORKTREE":
            data = (ROOT / relpath).read_bytes()
        else:
            commit, git_path = source_ref.split(":", 1)
            import subprocess

            data = subprocess.check_output(
                ["git", "show", f"{commit}:{git_path}"], cwd=ROOT
            )
        checks.truth(
            f"source_manifest_{index:02d}_{Path(relpath).name}",
            sha256_bytes(data) == expected,
        )


def derive() -> dict[str, object]:
    checks = Checks()
    replay_manifest(checks)

    # Positive variables are used only for symbolic logarithm identities.
    T, L, sigma, phi, omega = sp.symbols("T L sigma phi omega", positive=True)
    beta = sp.symbols("beta", real=True)

    # Unique positive common-scale / reciprocal-depth decomposition.
    sigma_def = sp.sqrt(T * L)
    phi_def = sp.Rational(1, 2) * sp.log(L / T)
    checks.exact("unique_reconstruct_clock", sigma_def * sp.exp(-phi_def), T)
    checks.exact("unique_reconstruct_ruler", sigma_def * sp.exp(phi_def), L)
    checks.exact(
        "common_rescale_depth_invariant",
        sp.Rational(1, 2) * sp.log((omega * L) / (omega * T)),
        phi_def,
    )
    checks.exact(
        "common_rescale_scale_covariant", sp.sqrt((omega * T) * (omega * L)), omega * sigma_def
    )
    checks.exact("channel_exchange_depth_odd", sp.Rational(1, 2) * sp.log(T / L), -phi_def)
    checks.exact("channel_exchange_scale_even", sp.sqrt(L * T), sigma_def)

    a = sp.symbols("a", real=True)
    checks.exact(
        "reciprocal_action_adds_depth",
        sp.Rational(1, 2) * sp.log((sp.exp(a) * L) / (sp.exp(-a) * T)),
        phi_def + a,
    )
    checks.exact(
        "reciprocal_action_preserves_scale",
        sp.sqrt((sp.exp(-a) * T) * (sp.exp(a) * L)),
        sigma_def,
    )

    # Every Lorentzian pair metric with a timelike clock coordinate has a unique
    # clock / orthogonal-ruler / shift decomposition.
    h = sp.Matrix(
        [
            [-T**2, -T**2 * beta],
            [-T**2 * beta, L**2 - T**2 * beta**2],
        ]
    )
    checks.exact("pair_metric_determinant", h.det(), -(T * L) ** 2)
    checks.exact("pair_metric_clock_density", sp.sqrt(-h[0, 0]), T)
    schur = sp.simplify(h[1, 1] - h[0, 1] ** 2 / h[0, 0])
    checks.exact("pair_metric_ruler_schur", schur, L**2)
    checks.exact("pair_metric_plane_density", sp.sqrt(-h.det()), T * L)
    checks.exact("pair_metric_shift_recovery", h[0, 1] / h[0, 0], beta)
    phi_h = sp.Rational(1, 4) * sp.log(-h.det()) - sp.Rational(1, 2) * sp.log(-h[0, 0])
    checks.exact("pair_metric_terminal_depth", phi_h, phi_def)
    checks.exact(
        "pair_metric_equivalent_ratio_formula",
        sp.Rational(1, 4) * sp.log((-h.det()) / h[0, 0] ** 2),
        phi_def,
    )

    # The calibration is load-bearing. A common reparameterization changes only common scale,
    # while an independent reciprocal recalibration changes the depth and therefore changes the
    # physical query rather than acting as a gauge.
    kappa = sp.symbols("kappa", positive=True)
    R_common = sp.diag(kappa, kappa)
    h_common = sp.simplify(R_common.T * h * R_common)
    phi_common = sp.Rational(1, 4) * sp.log(-h_common.det()) - sp.Rational(1, 2) * sp.log(-h_common[0, 0])
    checks.exact("pair_parameter_common_scale_depth_invariant", phi_common, phi_def)

    R_recip = sp.diag(sp.exp(-a), sp.exp(a))
    h_recal = sp.simplify(R_recip.T * h.subs(beta, 0) * R_recip)
    phi_recal = sp.Rational(1, 4) * sp.log(-h_recal.det()) - sp.Rational(1, 2) * sp.log(-h_recal[0, 0])
    checks.exact("pair_parameter_reciprocal_recalibration_changes_depth", phi_recal, phi_def + a)

    # Pure reciprocal reduction.
    h_recip = h.subs({T: sp.exp(-phi), L: sp.exp(phi), beta: 0})
    checks.exact("pure_reciprocal_g00", h_recip[0, 0], -sp.exp(-2 * phi))
    checks.exact("pure_reciprocal_g11", h_recip[1, 1], sp.exp(2 * phi))
    checks.exact("pure_reciprocal_det", h_recip.det(), -1)
    checks.exact("pure_reciprocal_depth_recovery", phi_h.subs({T: sp.exp(-phi), L: sp.exp(phi)}), phi)

    # c_E is the fixed conversion which gives the two tape coordinates equal dimension.
    # With shift, the two coordinate-null slopes differ. Their reciprocal average removes
    # the shift and returns the ordered clock/ruler ratio.
    w_plus = T / (L - T * beta)
    w_minus = -T / (L + T * beta)
    inverse_slope_mean = sp.simplify((1 / w_plus - 1 / w_minus) / 2)
    checks.exact("two_way_inverse_slope_removes_shift", inverse_slope_mean, L / T)
    checks.exact("terminal_ceff_ratio", 1 / inverse_slope_mean, T / L)
    checks.exact(
        "terminal_ceff_depth_inverse",
        -sp.Rational(1, 2) * sp.log(T / L),
        phi_def,
    )
    checks.exact("pure_reciprocal_ceff_ratio", (T / L).subs({T: sp.exp(-phi), L: sp.exp(phi)}), sp.exp(-2 * phi))

    # Relative endpoints. Arbitrary common scales cancel from the reciprocal depth.
    sigma_p, sigma_q = sp.symbols("sigma_p sigma_q", positive=True)
    phi_p, phi_q = sp.symbols("phi_p phi_q", real=True)
    T_p, L_p = sigma_p * sp.exp(-phi_p), sigma_p * sp.exp(phi_p)
    T_q, L_q = sigma_q * sp.exp(-phi_q), sigma_q * sp.exp(phi_q)
    delta_pq = sp.Rational(1, 2) * sp.log((L_q / T_q) / (L_p / T_p))
    checks.exact("endpoint_depth_common_scale_cancels", delta_pq, phi_q - phi_p)
    checks.exact(
        "endpoint_ceff_ratio",
        (T_q / L_q) / (T_p / L_p),
        sp.exp(-2 * (phi_q - phi_p)),
    )

    # Registered complete lower-mixing witness. Screen content in the clock image changes
    # the complete pair metric before the terminal reciprocal readout.
    eta4 = sp.diag(-1, 1, 1, 1)
    J_mix = sp.Matrix(
        [
            [sp.Rational(1, 2), 0],
            [0, 2],
            [sp.Rational(1, 4), 0],
            [0, 0],
        ]
    )
    g_mix = sp.simplify(J_mix.T * eta4 * J_mix)
    checks.exact("mixing_witness_g00", g_mix[0, 0], -sp.Rational(3, 16))
    checks.exact("mixing_witness_g11", g_mix[1, 1], 4)
    checks.exact("mixing_witness_det", g_mix.det(), -sp.Rational(3, 4))
    phi_mix = sp.Rational(1, 4) * sp.log(-g_mix.det()) - sp.Rational(1, 2) * sp.log(-g_mix[0, 0])
    checks.exact("mixing_witness_terminal_depth", phi_mix, sp.Rational(1, 4) * sp.log(sp.Rational(64, 3)))
    checks.truth("mixing_witness_differs_from_quotient_log2", sp.simplify(phi_mix - sp.log(2)) != 0)

    # A second witness has angular/screen components in both pair columns and nonzero shift.
    J_orchestra = sp.Matrix(
        [
            [sp.Rational(1, 2), 0],
            [0, 2],
            [sp.Rational(1, 4), sp.Rational(1, 3)],
            [0, 0],
        ]
    )
    g_orchestra = sp.simplify(J_orchestra.T * eta4 * J_orchestra)
    checks.exact("orchestra_g00", g_orchestra[0, 0], -sp.Rational(3, 16))
    checks.exact("orchestra_g01", g_orchestra[0, 1], sp.Rational(1, 12))
    checks.exact("orchestra_g11", g_orchestra[1, 1], sp.Rational(37, 9))
    checks.exact("orchestra_det", g_orchestra.det(), -sp.Rational(7, 9))
    L2_orchestra = sp.simplify(g_orchestra[1, 1] - g_orchestra[0, 1] ** 2 / g_orchestra[0, 0])
    checks.exact("orchestra_orthogonal_ruler_square", L2_orchestra, sp.Rational(112, 27))
    phi_orchestra = sp.Rational(1, 4) * sp.log(-g_orchestra.det()) - sp.Rational(1, 2) * sp.log(-g_orchestra[0, 0])
    checks.exact(
        "orchestra_terminal_depth",
        phi_orchestra,
        sp.Rational(1, 4) * sp.log(sp.Rational(1792, 81)),
    )
    checks.truth("orchestra_differs_from_lower_mix", sp.simplify(phi_orchestra - phi_mix) != 0)

    # Endpoint Lorentz presentation changes leave the pullback pair metric invariant.
    boost = sp.Matrix(
        [
            [sp.Rational(5, 4), sp.Rational(3, 4), 0, 0],
            [sp.Rational(3, 4), sp.Rational(5, 4), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    checks.truth("rational_boost_is_lorentz", boost.T * eta4 * boost == eta4)
    checks.truth(
        "pair_metric_endpoint_frame_invariant",
        sp.simplify((boost * J_orchestra).T * eta4 * (boost * J_orchestra) - g_orchestra)
        == sp.zeros(2),
    )

    # A screen rotation is another exact presentation control.
    screen_rotation = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, -1],
            [0, 0, 1, 0],
        ]
    )
    checks.truth("screen_rotation_is_lorentz", screen_rotation.T * eta4 * screen_rotation == eta4)
    checks.truth(
        "pair_metric_screen_frame_invariant",
        sp.simplify((screen_rotation * J_orchestra).T * eta4 * (screen_rotation * J_orchestra) - g_orchestra)
        == sp.zeros(2),
    )

    # Compatible carried channel-density maps compose. This is not imposed on independently
    # rebuilt pair tapes.
    a1, a2, s1, s2 = sp.symbols("a1 a2 s1 s2", real=True)
    D1 = sp.diag(sp.exp(s1 - a1), sp.exp(s1 + a1))
    D2 = sp.diag(sp.exp(s2 - a2), sp.exp(s2 + a2))

    def diagonal_depth(matrix: sp.Matrix) -> sp.Expr:
        return sp.Rational(1, 2) * sp.log(matrix[1, 1] / matrix[0, 0])

    checks.exact("carried_density_depth_leg1", diagonal_depth(D1), a1)
    checks.exact("carried_density_depth_leg2", diagonal_depth(D2), a2)
    checks.exact("carried_density_depth_composes", diagonal_depth(D2 * D1), a1 + a2)

    # Affine development itself composes, but a log imbalance of translation coordinates
    # is neither additive nor defined on pure causal axes.
    Lambda1 = sp.Matrix([[1, 1], [0, 1]])
    Lambda2 = sp.Matrix([[1, 0], [1, 1]])
    z1 = sp.Matrix([1, 2])
    z2 = sp.Matrix([3, 4])
    Lambda12 = Lambda2 * Lambda1
    z12 = z2 + Lambda2 * z1
    x = sp.Matrix(sp.symbols("x0:2"))
    direct = sp.simplify(Lambda12 * x + z12)
    staged = sp.simplify(Lambda2 * (Lambda1 * x + z1) + z2)
    checks.truth("affine_semidirect_composition", direct == staged)

    d_translation = sp.Rational(1, 2) * sp.log(sp.Rational(2, 1))
    d_translation_sum = sp.Rational(1, 2) * sp.log(sp.Rational(4, 2))
    checks.exact("translation_same_ray_scale_invariant", d_translation_sum, d_translation)
    checks.truth("translation_log_imbalance_nonadditive", sp.simplify(d_translation_sum - 2 * d_translation) != 0)
    translation_spacelike = sp.Rational(1, 2) * sp.log(sp.oo)
    translation_timelike = sp.Rational(1, 2) * sp.log(0)
    checks.truth("translation_pure_spacelike_degenerate", translation_spacelike.is_finite is False)
    checks.truth("translation_pure_timelike_degenerate", translation_timelike.is_finite is False)

    # Fermi/normal pair-map origin is exactly calibrated; away from the origin the full
    # pullback metric is the object to evaluate. These checks encode the origin only and do
    # not assert a global Fermi chart.
    h_origin = sp.diag(-1, 1)
    phi_origin = sp.Rational(1, 4) * sp.log(-h_origin.det()) - sp.Rational(1, 2) * sp.log(-h_origin[0, 0])
    checks.exact("calibrated_pair_map_origin_depth_zero", phi_origin, 0)

    # Failure strata are algebraic, not numerical cutoffs.
    checks.exact("null_clock_boundary_g00", (-T**2).subs(T, 0), 0)
    checks.exact("degenerate_plane_boundary_det", (-(T * L) ** 2).subs(L, 0), 0)

    total = len(checks.rows)
    passed = sum(int(row["passed"]) for row in checks.rows)
    failed = [row for row in checks.rows if not row["passed"]]
    result = {
        "schema_version": 1,
        "package": PACKAGE.name,
        "base_commit": "0c010db9e594e8ef4c4512c81afd03551b36091c",
        "question_type": "METRIC_LED_TERMINAL_RECIPROCAL_READOUT",
        "landing": (
            "TERMINAL_RECIPROCAL_CE_PAIR_METRIC_DECOMPOSITION_DERIVED_ON_SUPPLIED_REGULAR_A_CALIBRATED_PAIR_METRICS__"
            "RELATIONAL_PHI_IS_THE_UNIQUE_RECIPROCAL_LOG_IMBALANCE_ONLY_WITHIN_THAT_FIXED_CALIBRATION_AND_PAIR_MAP__"
            "ANGULAR_AND_MIXING_MODULATION_ARE_STRUCTURALLY_VISIBLE_IN_SUPPLIED_PAIR_JACOBIANS_BEFORE_READOUT__"
            "NO_GENERAL_PHYSICAL_CEFF_RATIO_OR_CALIBRATION_STATE_REALIZATION_IS_DERIVED__"
            "PAIR_SURFACE_OR_COMPARISON_JACOBIAN_OWNER_ENDPOINT_SELECTION_PATH_REALIZATION_AND_XMAX_PROFILE_REMAIN_OPEN"
        ),
        "checks_total": total,
        "checks_passed": passed,
        "checks_failed": len(failed),
        "failed": failed,
        "exact_values": {
            "registered_mixing_depth": str(phi_mix),
            "registered_mixing_depth_numeric": str(sp.N(phi_mix, 16)),
            "orchestra_depth": str(phi_orchestra),
            "orchestra_depth_numeric": str(sp.N(phi_orchestra, 16)),
        },
        "rows": checks.rows,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    result = derive()
    print(json.dumps(result, indent=None if args.compact else 2, sort_keys=True))
    return 0 if result["checks_failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
