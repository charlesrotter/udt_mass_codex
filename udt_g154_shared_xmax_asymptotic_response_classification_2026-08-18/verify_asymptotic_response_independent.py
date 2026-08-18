#!/usr/bin/env python3
"""Independent stdlib numerical/source replay for G154; intentionally no SymPy."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def fixed_response(q: float, ell: float, epsilon: int, x_star: float = 3.0) -> float:
    p = 1.0 / 3.0
    return epsilon * 4.0 * x_star * p * q ** (2.0 * p + ell - 1.0) / (1.0 + q ** (2.0 * p)) ** 2


def temporal_fixed_response(q: float, ell: float, epsilon: int, x_star: float = 3.0) -> float:
    p = 1.0 / 3.0
    phi = epsilon * (-p * math.log(q))
    u_phi = epsilon * p * q ** (ell - 1.0)  # T=q^-ell and q=1-tau.
    return x_star / math.cosh(phi) ** 2 * u_phi


def response_from_pair_metric(
    q: float,
    log_t: float,
    log_l: float,
    dlog_t: float,
    dlog_l: float,
    normalized_inverse_scale: float,
    x_star: float = 3.0,
) -> tuple[float, float]:
    """Recover phi and normalized response directly from T,L and their q derivatives."""
    phi = 0.5 * (log_l - log_t)
    dphi = 0.5 * (dlog_l - dlog_t)
    response = -normalized_inverse_scale * x_star / math.cosh(phi) ** 2 * dphi
    return phi, response


def spatial_pair_response(q: float, ell: float, epsilon: int, x_star: float = 3.0) -> tuple[float, float]:
    p = 1.0 / 3.0
    phi_input = epsilon * (-p * math.log(q))
    dphi = -epsilon * p / q
    log_l = -ell * math.log(q)
    dlog_l = -ell / q
    log_t = log_l - 2.0 * phi_input
    dlog_t = dlog_l - 2.0 * dphi
    return response_from_pair_metric(q, log_t, log_l, dlog_t, dlog_l, q**ell, x_star)


def temporal_pair_response(q: float, ell: float, epsilon: int, x_star: float = 3.0) -> tuple[float, float]:
    p = 1.0 / 3.0
    phi_input = epsilon * (-p * math.log(q))
    dphi = -epsilon * p / q
    log_t = -ell * math.log(q)
    dlog_t = -ell / q
    log_l = log_t + 2.0 * phi_input
    dlog_l = dlog_t + 2.0 * dphi
    return response_from_pair_metric(q, log_t, log_l, dlog_t, dlog_l, q**ell, x_star)


def oscillatory_pair_response(q: float, epsilon: int, temporal: bool, x_star: float = 3.0) -> float:
    p = 1.0 / 3.0
    amplitude = 0.5
    factor = 1.0 + amplitude * math.sin(1.0 / q)
    log_normalizer = -p * math.log(q) - math.log(factor)
    dlog_normalizer = -p / q + amplitude * math.cos(1.0 / q) / (q * q * factor)
    phi_input = epsilon * (-p * math.log(q))
    dphi = -epsilon * p / q
    if temporal:
        log_t, dlog_t = log_normalizer, dlog_normalizer
        log_l, dlog_l = log_t + 2.0 * phi_input, dlog_t + 2.0 * dphi
    else:
        log_l, dlog_l = log_normalizer, dlog_normalizer
        log_t, dlog_t = log_l - 2.0 * phi_input, dlog_l - 2.0 * dphi
    inverse_scale = q**p * factor
    _phi, response = response_from_pair_metric(
        q, log_t, log_l, dlog_t, dlog_l, inverse_scale, x_star
    )
    return response


def live_response(q: float, exponent: float, x_star: float = 3.0) -> float:
    p = 0.5
    phi = -p * math.log(q)
    x_field = x_star + q**exponent
    n_x = -exponent * q ** (exponent + p - 1.0)
    n_phi = p * q ** (p - 1.0)
    return math.tanh(phi) * n_x + x_field / math.cosh(phi) ** 2 * n_phi


def replay() -> dict[str, object]:
    checks: dict[str, bool] = {}

    # Mobius composition and reversal on a broad deterministic grid.
    max_mobius_error = 0.0
    x_star = 3.0
    for a in (-4.0, -1.0, -0.2, 0.0, 0.3, 1.5, 5.0):
        for b in (-3.0, -0.4, 0.0, 0.7, 2.0):
            xa = x_star * math.tanh(a)
            xb = x_star * math.tanh(b)
            composed = (xa + xb) / (1.0 + xa * xb / x_star**2)
            max_mobius_error = max(max_mobius_error, abs(composed - x_star * math.tanh(a + b)))
    checks["mobius_grid"] = max_mobius_error < 2.0e-13

    # The normalized chi law composes without any dimensionful X.  It remains exact alongside an
    # arbitrary nonconstant X(q)=X_star+q, so normalized composition alone cannot derive dX=0.
    max_normalized_error = 0.0
    for a in (-2.0, -0.2, 0.4, 1.7):
        for b in (-1.1, 0.0, 0.8):
            composed = (math.tanh(a) + math.tanh(b)) / (1.0 + math.tanh(a) * math.tanh(b))
            max_normalized_error = max(max_normalized_error, abs(composed - math.tanh(a + b)))
    nonconstant_scale_samples = [x_star + q for q in (0.8, 0.3, 0.1)]
    checks["normalized_composition_does_not_fix_scale"] = (
        max_normalized_error < 2.0e-13 and len(set(nonconstant_scale_samples)) == 3
    )

    # The fixed-profile common-scale exponents include a deliberately slow q^(1/6) approach.
    qs = [10.0 ** (-k) for k in (2, 4, 8, 16, 32, 60)]
    quiet = [abs(fixed_response(q, 0.5, 1)) for q in qs]
    critical = [fixed_response(q, 1.0 / 3.0, 1) for q in qs]
    divergent = [abs(fixed_response(q, 0.25, 1)) for q in qs]
    checks["fixed_quiet_trends_zero"] = quiet[-1] < 1.0e-5 and quiet[-1] < quiet[0]
    checks["fixed_critical_hits_four_X_over_three"] = abs(critical[-1] - 4.0) < 1.0e-3
    checks["fixed_divergent_grows"] = divergent[-1] > 100.0 * divergent[0]
    checks["fixed_sign_paired_witnesses"] = all(
        abs(fixed_response(q, 1.0 / 3.0, -1) + fixed_response(q, 1.0 / 3.0, 1)) < 1.0e-12
        for q in qs
    )
    checks["temporal_dual_uses_same_normalized_formula"] = all(
        math.isclose(
            fixed_response(q, ell, epsilon),
            temporal_fixed_response(q, ell, epsilon),
            rel_tol=2.0e-13,
            abs_tol=1.0e-13,
        )
        for q in qs
        for ell in (0.5, 1.0 / 3.0, 0.25)
        for epsilon in (-1, 1)
    )
    checks["responses_recovered_from_spatial_pair_metrics"] = all(
        math.isclose(
            spatial_pair_response(q, ell, epsilon)[1],
            fixed_response(q, ell, epsilon),
            rel_tol=3.0e-13,
            abs_tol=1.0e-13,
        )
        for q in qs[:-1]
        for ell in (0.5, 1.0 / 3.0, 0.25)
        for epsilon in (-1, 1)
    )
    checks["responses_recovered_from_temporal_pair_metrics"] = all(
        math.isclose(
            temporal_pair_response(q, ell, epsilon)[1],
            fixed_response(q, ell, epsilon),
            rel_tol=3.0e-13,
            abs_tol=1.0e-13,
        )
        for q in qs[:-1]
        for ell in (0.5, 1.0 / 3.0, 0.25)
        for epsilon in (-1, 1)
    )

    # Both spatial and temporal oscillatory witnesses are replayed directly from T,L.
    n_phase = 10_000_000
    q_plus = 1.0 / (math.pi / 2.0 + 2.0 * math.pi * n_phase)
    q_minus = 1.0 / (3.0 * math.pi / 2.0 + 2.0 * math.pi * n_phase)
    oscillatory = {
        mode: [oscillatory_pair_response(qv, 1, mode == "temporal") for qv in (q_plus, q_minus)]
        for mode in ("spatial", "temporal")
    }
    checks["both_oscillatory_duals_have_distinct_limits"] = all(
        abs(values[0] - 6.0) < 2.0e-4 and abs(values[1] - 2.0) < 2.0e-4
        for values in oscillatory.values()
    )

    live_quiet = [abs(live_response(q, 1.0)) for q in qs]
    live_finite = [live_response(q, 0.5) for q in qs]
    live_divergent = [abs(live_response(q, 0.25)) for q in qs]
    checks["live_quiet_trends_zero"] = live_quiet[-1] < 1.0e-5
    checks["live_finite_hits_minus_half"] = abs(live_finite[-1] + 0.5) < 1.0e-3
    checks["live_divergent_grows"] = live_divergent[-1] > 100.0 * live_divergent[0]

    # Exact cancellation is checked term by term, not merely through constant rho.
    cancellation_errors = []
    cancellation_sum_errors = []
    cancellation_terms_nonzero = []
    c = 2.0
    for q in (0.4, 0.1, 0.01, 1.0e-4):
        phi = -0.5 * math.log(q)
        dphi = -0.5 / q
        inverse_l = q**0.5
        x_field = c / math.tanh(phi)
        dx = -c * dphi / math.sinh(phi) ** 2
        n_x = -inverse_l * dx
        n_phi = -inverse_l * dphi
        term_x = math.tanh(phi) * n_x
        term_phi = x_field / math.cosh(phi) ** 2 * n_phi
        rho = x_field * math.tanh(phi)
        cancellation_errors.append(abs(rho - c))
        cancellation_sum_errors.append(abs(term_x + term_phi))
        cancellation_terms_nonzero.append(abs(term_x) > 1.0e-10 and abs(term_phi) > 1.0e-10)
    checks["cancellation_constant_rho"] = max(cancellation_errors) < 1.0e-14
    checks["cancellation_terms_nonzero_and_cancel"] = (
        max(cancellation_sum_errors) < 2.0e-14 and all(cancellation_terms_nonzero)
    )

    # Manifest hashes are independently checked from disk.
    manifest_ok = True
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8") as handle:
        next(handle)
        for line in handle:
            source, _role, expected = line.rstrip("\n").split("\t")
            payload = subprocess.run(
                ["git", "show", f"f5946fa0:{source}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout
            actual = hashlib.sha256(payload).hexdigest()
            manifest_ok = manifest_ok and actual == expected
    checks["source_manifest_hashes"] = manifest_ok

    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "implementation": "stdlib_float_and_source_hash_replay_no_sympy",
        "max_mobius_error": max_mobius_error,
        "max_normalized_composition_error": max_normalized_error,
        "nonconstant_scale_samples": nonconstant_scale_samples,
        "oscillatory_pair_metric_values": oscillatory,
        "cancellation_sum_max_error": max(cancellation_sum_errors),
        "fixed_tail": {"quiet": quiet[-1], "critical": critical[-1], "divergent": divergent[-1]},
        "live_tail": {
            "quiet": live_quiet[-1],
            "finite": live_finite[-1],
            "divergent": live_divergent[-1],
        },
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = replay()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
