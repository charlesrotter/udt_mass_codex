#!/usr/bin/env python3
"""Exact symbolic G201 phi-jet amplitude classification."""

import json
import sympy as sp


def main() -> None:
    r = sp.symbols("r", positive=True)
    alpha = sp.symbols("alpha", positive=True)
    delta = sp.symbols("Delta", real=True)
    phi_value, p, q = sp.symbols("phi p q", real=True)
    phi = sp.Function("phi")(r)
    f = sp.exp(-2 * phi)
    angmom = r * sp.sin(alpha)

    tide_parallel = sp.simplify(
        angmom**2 * (r * sp.diff(f, r, 2) - sp.diff(f, r)) / (2 * r**3)
    )
    tide_perp = sp.simplify(
        angmom**2 * (r * sp.diff(f, r) - 2 * f + 2) / (2 * r**4)
    )
    amplitude_parallel = sp.simplify(r**2 * tide_parallel / sp.sin(alpha) ** 2)
    amplitude_perp = sp.simplify(r**2 * tide_perp / sp.sin(alpha) ** 2)

    jet_subs = {
        sp.diff(phi, r): p / r,
        sp.diff(phi, r, 2): q / r**2,
        phi: phi_value,
    }
    # xreplace is simultaneous: replacing phi before its derivatives would spuriously zero them.
    a_parallel = sp.simplify(amplitude_parallel.xreplace(jet_subs))
    a_perp = sp.simplify(amplitude_perp.xreplace(jet_subs))
    expected_parallel = sp.exp(-2 * phi_value) * (2 * p**2 - q + p)
    expected_perp = 1 - sp.exp(-2 * phi_value) * (1 + p)

    assertions = [
        sp.simplify(a_parallel - expected_parallel) == 0,
        sp.simplify(a_perp - expected_perp) == 0,
    ]

    # Flat-overlap and live-jet controls at the same value phi=0.
    flat_overlap = [sp.simplify(expr.subs({phi_value: 0, p: 0, q: 0}))
                    for expr in (a_parallel, a_perp)]
    phi_zero_live_jet = [sp.simplify(expr.subs({phi_value: 0, p: 1, q: 0}))
                         for expr in (a_parallel, a_perp)]
    assertions.extend(value == 0 for value in flat_overlap)
    assertions.extend(value != 0 for value in phi_zero_live_jet)

    # At every supplied phi, local jets can cancel both angular modes.
    cancel_p = sp.exp(2 * phi_value) - 1
    cancel_q = 2 * cancel_p**2 + cancel_p
    cancellation = [sp.simplify(expr.subs({p: cancel_p, q: cancel_q}))
                    for expr in (a_parallel, a_perp)]
    assertions.extend(value == 0 for value in cancellation)

    # The cancellation jets integrate exactly to f=1+C r^2.
    constant = sp.symbols("C", real=True)
    f_family = 1 + constant * r**2
    family_tides = [
        sp.simplify(angmom**2 * (r * sp.diff(f_family, r, 2)
                    - sp.diff(f_family, r)) / (2 * r**3)),
        sp.simplify(angmom**2 * (r * sp.diff(f_family, r)
                    - 2 * f_family + 2) / (2 * r**4)),
    ]
    assertions.extend(value == 0 for value in family_tides)
    family_p = sp.simplify(-r * sp.diff(f_family, r) / (2 * f_family))
    family_q = sp.simplify(r**2 * (
        sp.diff(f_family, r)**2 - f_family * sp.diff(f_family, r, 2)
    ) / (2 * f_family**2))
    assertions.append(sp.simplify(family_p - (1 / f_family - 1)) == 0)
    assertions.append(sp.simplify(family_q - (2 * family_p**2 + family_p)) == 0)

    # Constant-jet subclasses illustrate, but do not define, asymptotic behavior.
    constant_profile = [sp.simplify(expr.subs({p: 0, q: 0}))
                        for expr in (a_parallel, a_perp)]
    positive_limits = [sp.limit(expr, phi_value, sp.oo) for expr in constant_profile]
    negative_limits = [sp.limit(expr, phi_value, -sp.oo) for expr in constant_profile]
    assertions.extend([
        positive_limits == [0, 1],
        negative_limits[0] == 0,
        negative_limits[1] == -sp.oo,
    ])

    # A diagnostic of the founded reciprocal block, not a new physical score.
    reciprocal_contrast = sp.cosh(2 * delta) - 1
    assertions.extend([
        reciprocal_contrast.subs(delta, 0) == 0,
        sp.simplify(reciprocal_contrast.subs(delta, -delta) - reciprocal_contrast) == 0,
        sp.simplify(reciprocal_contrast - 2 * sp.sinh(delta) ** 2) == 0,
        sp.limit(reciprocal_contrast, delta, sp.oo) == sp.oo,
        sp.limit(reciprocal_contrast, delta, -sp.oo) == sp.oo,
    ])

    payload = {
        "landing": (
            "TWO_SIDED_RECIPROCAL_MAGNITUDE__ANGULAR_VOLUME_IS_PHI_JET_DEPENDENT"
            "__NO_LOCKSTEP_LOUDNESS_FORCED"
        ),
        "all_pass": all(bool(item) for item in assertions),
        "assertions": len(assertions),
        "passed": sum(bool(item) for item in assertions),
        "dimensionless_angular_amplitudes": {
            "parallel": str(a_parallel),
            "perpendicular": str(a_perp),
        },
        "flat_overlap_phi_p_q_zero": [str(value) for value in flat_overlap],
        "phi_zero_live_jet_p1_q0": [str(value) for value in phi_zero_live_jet],
        "arbitrary_phi_cancellation_jets": {
            "p": str(cancel_p),
            "q": str(cancel_q),
            "amplitudes": [str(value) for value in cancellation],
        },
        "exact_smooth_zero_tide_family": {
            "f": str(f_family),
            "tides": [str(value) for value in family_tides],
        },
        "constant_phi_subclass": {
            "amplitudes": [str(value) for value in constant_profile],
            "positive_extreme_limits": [str(value) for value in positive_limits],
            "negative_extreme_limits": [str(value) for value in negative_limits],
        },
        "reciprocal_block_contrast_diagnostic": str(reciprocal_contrast),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
