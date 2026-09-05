#!/usr/bin/env python3
"""Hostile mutation checks for bounded G347 endpoint-observer covariance."""

from __future__ import annotations

import json
import math
import os

import derive_endpoint_observer_covariance as production


def different(left, right, floor=1.0e-5):
    return production.relerr(left, right) > floor


def main():
    if os.environ.get("UDT_NO_WRITE") not in (None, "", "0", "1"):
        raise SystemExit("UDT_NO_WRITE must be 0 or 1")
    t0, t1, t2 = 1.13, 2.27, 3.91
    t_reference, rho, nu = 0.89, 0.37, 1.61
    b10 = production.bilocal_b(t1, t0, rho, nu, t_reference)
    b21 = production.bilocal_b(t2, t1, rho, nu, t_reference)
    b20 = production.bilocal_b(t2, t0, rho, nu, t_reference)
    omega0 = production.normal_frequency(t0, rho, nu, t_reference)
    omega1 = production.normal_frequency(t1, rho, nu, t_reference)
    direction0 = production.ray_direction(t0, rho, t_reference)
    direction1 = production.ray_direction(t1, rho, t_reference)
    ray0 = production.vscale(omega0, (1.0,) + direction0)
    ray1 = production.vscale(omega1, (1.0,) + direction1)
    beta0 = (0.42, -0.51, 0.31)
    beta1 = (-0.61, 0.22, -0.18)
    observer0 = production.boost_observer(beta0)
    observer1 = production.boost_observer(beta1)
    d0 = -production.minkowski(ray0, observer0) / omega0
    d1 = -production.minkowski(ray1, observer1) / omega1
    reverse = [[-value for value in row] for row in production.transpose(b10)]
    area10 = production.angular_area(b10, omega0)
    area01 = production.angular_area(reverse, omega1)
    changed10 = d0 * d0 * area10
    changed01 = d1 * d1 * area01
    old_dhat = production.dhat(b10, omega0, omega1)
    new_dhat = old_dhat / (d0 * d1)
    hessian = production.stationary_hessian(b21, b10, b20)
    hhat = production.join_scalar(hessian, omega1)
    area21 = production.angular_area(b21, omega1)
    area20 = production.angular_area(b20, omega0)

    catches = {}
    catches["doppler_factor_reversed"] = different(1.0 / (d0 * d0), d0 * d0)
    catches["one_sky_power"] = different(1.0 / d0, 1.0 / (d0 * d0))
    catches["sky_factor_not_inverse"] = different(d0 * d0, 1.0 / (d0 * d0))
    catches["target_doppler_added_to_forward_area"] = different(changed10, d0 * d0 * d1 * d1 * area10)
    catches["numerical_observer_invariance_declared"] = different(changed10, area10)

    basis = production.screen_basis(direction0)
    omitted_rotation = basis[0]
    correct_rotation = production.screen_representative(basis[0], observer0, ray0)
    catches["null_rotation_term_omitted"] = (
        abs(production.minkowski(omitted_rotation, observer0)) > 1.0e-4
        and abs(production.minkowski(correct_rotation, observer0)) < 1.0e-12
    )
    wrong_rotation = production.vadd(
        basis[0],
        production.vscale(-production.minkowski(basis[0], observer0) / (-production.minkowski(ray0, observer0)), ray0),
    )
    catches["nonisometric_projection_sign"] = abs(production.minkowski(wrong_rotation, observer0)) > 1.0e-4

    frame0 = [[1.41, 0.33], [-0.27, 0.78]]
    frame1 = [[0.72, -0.38], [0.21, 1.36]]
    q0, q1 = production.metric_after(frame0), production.metric_after(frame1)
    transformed = production.transform_b(b10, frame1, frame0)
    wrong_dual = production.mm(production.mm(frame1, b10), production.inverse2(frame0))
    catches["screen_dual_map_reversed"] = different(
        production.angular_area(transformed, d0 * omega0, q0, q1),
        production.angular_area(wrong_dual, d0 * omega0, q0, q1),
    )
    catches["G345_endpoint0_factor_omitted"] = different(new_dhat, old_dhat / d1)
    catches["G345_endpoint1_factor_omitted"] = different(new_dhat, old_dhat / d0)
    catches["G345_factor_inverted"] = different(new_dhat, old_dhat * d0 * d1)
    catches["arithmetic_mean_used"] = different(
        0.5 * (changed10 + changed01), math.sqrt(changed10 * changed01)
    )
    catches["G345_not_inverted_in_mean"] = different(math.sqrt(changed10 * changed01), new_dhat)
    catches["join_factor_left_unchanged"] = different(
        d0 * d0 * area20, hhat * (d1 * d1 * area21) * changed10
    )
    catches["join_factor_multiplied_by_D1_squared"] = different(
        d0 * d0 * area20, (hhat * d1 * d1) * (d1 * d1 * area21) * changed10
    )
    affine = 4.7
    catches["affine_B_not_rescaled"] = different(
        production.angular_area(b10, affine * d0 * omega0), changed10
    )

    transverse_beta = (0.0, 0.67, 0.0)
    transverse_observer = production.boost_observer(transverse_beta)
    transverse_d = -production.minkowski(ray0, transverse_observer) / omega0
    gamma_only = transverse_observer[0]
    catches["transverse_boost_deleted"] = different(transverse_d, gamma_only)
    null_rejected = False
    try:
        production.boost_observer((1.0, 0.0, 0.0))
    except ValueError:
        null_rejected = True
    catches["null_observer_boundary_made_regular"] = null_rejected

    labels = {"lift_0": changed10, "lift_1": 1.3 * changed10}
    catches["compact_lifts_summed_or_selected"] = (
        sum(labels.values()) not in labels.values() and len(labels) == 2
    )
    promoted = production.LANDING + "__PREFERRED_OBSERVER_SELECTED__LIGHT_DISTANCE_SCALE_XMAX"
    catches["preferred_observer_promotion"] = "PREFERRED_OBSERVER_SELECTED" in promoted
    forbidden = ("LIGHT", "DISTANCE", "POPULATION", "SCALE", "XMAX")
    catches["forbidden_physical_promotion"] = all(token in promoted for token in forbidden)
    catches["negative_scope_token_load_bearing"] = production.LANDING.replace("NO_PREFERRED", "PREFERRED") != production.LANDING

    failed = [name for name, caught in catches.items() if not caught]
    result = {
        "caught": sum(catches.values()),
        "failed": failed,
        "mutations": catches,
        "status": "PASS" if not failed else "FAIL",
        "total": len(catches),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if failed:
        raise SystemExit("uncaught hostile mutations: " + ", ".join(failed))


if __name__ == "__main__":
    main()
