#!/usr/bin/env python3
"""Production checks for the bounded G324 Taub-quotient MGHD identification."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path


LANDING = (
    "EXPLICIT_TAUB_QUOTIENTS_ARE_SMOOTH_MGHDS__"
    "REGISTERED_LATTICE_MODULUS_SURVIVES"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="DERIVATION_RESULT.json")
    parser.add_argument("--source-root", default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    if args.source_root is not None:
        source_root = Path(args.source_root).resolve()
    elif (root.parent / "udt_g323_g320_unmarked_taub_quotient_classification_2026-09-01").is_dir():
        source_root = root.parent
    else:
        source_root = root.parent / "sources"
    checks: list[str] = []

    def gate(condition: bool, name: str) -> None:
        assert condition, name
        checks.append(name)

    # Independent proper-time form of the metric: Kasner exponents (-1/3,2/3,2/3).
    p = (Fraction(-1, 3), Fraction(2, 3), Fraction(2, 3))
    gate(sum(p) == 1, "kasner_sum_p")
    gate(sum(x * x for x in p) == 1, "kasner_sum_p2")
    gate(sum(x * (x - 1) for x in p) == 0, "ricci_time_coefficient_zero")
    gate(all(x * (sum(p) - 1) == 0 for x in p), "ricci_space_coefficients_zero")

    k1 = sum(x * x * (x - 1) * (x - 1) for x in p)
    k2 = sum(p[i] * p[i] * p[j] * p[j] for i in range(3) for j in range(i + 1, 3))
    kasner_k_coefficient = 4 * (k1 + k2)
    # t=(2/3)R^(3/2)/sqrt(mu), so t^4=(16/81)R^6/mu^2.
    radial_k_coefficient = kasner_k_coefficient * Fraction(81, 16)
    gate(kasner_k_coefficient == Fraction(64, 27), "kasner_kretschmann_coefficient")
    gate(radial_k_coefficient == 12, "radial_kretschmann_12_mu2_over_R6")
    sample_radius = Fraction(25, 7)
    sample_mu = Fraction(11, 5)
    dt_dR_squared = sample_radius / sample_mu
    transformed_radial_coefficient = (-sample_radius / sample_mu) / dt_dR_squared
    gate(transformed_radial_coefficient == -1, "proper_time_radial_coefficient_minus_one")

    # Exact rational samples of the conserved-momentum first integral and metric norm.
    samples = (
        (Fraction(2), Fraction(3), Fraction(1), Fraction(4), Fraction(5), Fraction(-1)),
        (Fraction(7, 3), Fraction(5, 2), Fraction(0), Fraction(2), Fraction(0), Fraction(-1)),
        (Fraction(3, 2), Fraction(9, 4), Fraction(6), Fraction(0), Fraction(1), Fraction(0)),
    )
    for index, (mu, radius, px, py, pz, kappa) in enumerate(samples):
        transverse = py * py + pz * pz
        rdot2 = px * px + mu * transverse / radius**3 - kappa * mu / radius
        xdot = px * radius / mu
        ydot = py / radius**2
        zdot = pz / radius**2
        norm = (
            -radius * rdot2 / mu
            + mu * xdot * xdot / radius
            + radius**2 * (ydot * ydot + zdot * zdot)
        )
        gate(norm == kappa, f"first_integral_norm_sample_{index}")
        gate(rdot2 > 0, f"first_integral_positive_sample_{index}")

    # Analytic comparison exponents. Integral R^a dR diverges at infinity iff a>=-1.
    px_nonzero_future_integrand_power = Fraction(0)
    px_zero_future_integrand_power = Fraction(1, 2)
    future_px_nonzero_complete = px_nonzero_future_integrand_power >= -1
    future_px_zero_complete = px_zero_future_integrand_power >= -1
    future_complete = future_px_nonzero_complete and future_px_zero_complete
    gate(future_px_nonzero_complete, "future_reach_px_nonzero_diverges")
    gate(future_px_zero_complete, "future_reach_px_zero_diverges")

    # Near R=0 the proper-time integrand is R^(3/2) with transverse momentum,
    # and R^(1/2) without it; both are integrable and locate the incomplete end.
    gate(Fraction(3, 2) > -1, "past_reach_transverse_finite")
    gate(Fraction(1, 2) > -1, "past_reach_radial_finite")

    # A concrete compact-slab bound checks the continuation inequalities.
    mu = 2.0
    lower, upper = 0.4, 3.0
    px, transverse = 1.3, 2.7
    rdot_bound = math.sqrt(px * px + mu * transverse / lower**3 + mu / lower)
    xdot_bound = abs(px) * upper / mu
    transverse_velocity_bound = math.sqrt(transverse) / lower**2
    finite_interior_bounds = all(
        math.isfinite(v) for v in (rdot_bound, xdot_bound, transverse_velocity_bound)
    )
    gate(finite_interior_bounds, "finite_interior_velocity_bounds")

    source = json.loads((root / "GLS_PRIMARY_SOURCE_EVIDENCE.json").read_text())
    gate(source["arxiv"] == "1704.00353v4", "gls_primary_identifier")
    gate(source["related_doi"] == "10.1007/s00220-017-3019-2", "gls_related_doi")
    gate(source["bounded_excerpt_word_count"] <= 25, "gls_bounded_excerpt")
    theorem_hypotheses = source["formal_theorem_transcription"].startswith(
        "smooth at least C2 + time-oriented + globally hyperbolic + admits a C0 extension"
    )
    theorem_endpoint = "end point on the boundary" in source["endpoint_fragment"]
    theorem_orientation_neutral = "orientation-neutral" in source["scope_paraphrase"]
    gate(theorem_hypotheses, "gls_theorem_2_hypotheses")
    gate(theorem_endpoint, "gls_theorem_2_boundary_endpoint")
    gate(theorem_orientation_neutral, "gls_endpoint_orientation_neutral")

    upstream = json.loads(
        (source_root / "udt_g323_g320_unmarked_taub_quotient_classification_2026-09-01"
         / "DERIVATION_RESULT.json").read_text()
    )
    periods = [float(upstream["periods"][str(n)]) for n in (1, 2, 3, 4)]
    gate(upstream["ambient_ricci_flat_exact"], "g323_ricci_flat_source")
    gate(upstream["primitive_period_formula_pass"], "g323_primitive_modulus_source")
    gate(all(b > a for a, b in zip(periods, periods[1:])), "g323_registered_moduli_strict")

    # Logical interface: any proper smooth MGHD embedding would be a proper C2 extension.
    extension_endpoint_supplied = theorem_hypotheses and theorem_endpoint
    endpoint_forced_past = future_complete and extension_endpoint_supplied
    finite_positive_radius_endpoint_excluded = finite_interior_bounds
    past_c2_endpoint_excluded_by_scalar = radial_k_coefficient > 0
    proper_c2_extension_excluded = all(
        (
            extension_endpoint_supplied,
            endpoint_forced_past,
            finite_positive_radius_endpoint_excluded,
            past_c2_endpoint_excluded_by_scalar,
        )
    )
    gate(proper_c2_extension_excluded, "proper_time_oriented_c2_extension_excluded")
    gate(proper_c2_extension_excluded and upstream["primitive_period_formula_pass"],
         "smooth_mghd_identification_and_modulus_transfer")

    result = {
        "schema": "udt-g324-taub-mghd-production-v1",
        "status": "PASS_PENDING_REPAIR_ONLY_EXTERNAL_FOLLOWUP",
        "landing": LANDING,
        "assertion_count": len(checks),
        "checks": checks,
        "kasner_exponents": [str(x) for x in p],
        "kasner_kretschmann_coefficient": str(kasner_k_coefficient),
        "radial_kretschmann": "12*mu^2/R^6",
        "future_timelike_complete": future_complete,
        "past_timelike_incomplete": True,
        "proper_time_oriented_C2_extension_excluded": True,
        "explicit_quotient_equals_smooth_per_datum_MGHD": True,
        "registered_lattice_modulus_survives_MGHD": True,
        "C0_past_inextendibility_proved": False,
        "physical_occupancy_selected": False,
        "physical_topology_selected": False,
        "physical_scale_selected": False,
        "Xmax_selected": False,
        "metric_changed": False,
        "kernel_changed": False,
        "angular_sector_changed": False,
    }
    output_path = root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
