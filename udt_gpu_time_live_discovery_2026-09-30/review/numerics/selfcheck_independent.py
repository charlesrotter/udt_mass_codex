#!/usr/bin/env python3
"""Analytic controls and nonvacuum catch proofs for independent Ricci code."""
import json
from pathlib import Path
import numpy as np
from independent_numerics import (coordinate_ricci, cpu_integrate, file_hash,
                                  snapshot_ricci)


def main():
    results = {}
    # Analytic diagonal Ricci-flat power metric from homogeneous arena.
    t, u, c = 2.1, .73, 1.4
    powers = np.array([(u*u-1)/2, (u*u-1)/2, 1+u, 1-u])
    diagonal = np.array([-c, c, 1., 1.]) * t**powers
    g = np.diag(diagonal)[None]
    dg = np.zeros((1, 4, 4, 4))
    ddg = np.zeros((1, 4, 4, 4, 4))
    dg[0, 0] = np.diag(diagonal * powers / t)
    ddg[0, 0, 0] = np.diag(diagonal * powers * (powers-1) / t**2)
    r = coordinate_ricci(g, dg, ddg)
    results["exact_homogeneous_vacuum_max"] = float(abs(r).max())
    assert results["exact_homogeneous_vacuum_max"] < 2e-14

    # Nonvacuum analytic differential-geometric control.  For ds2=-dt2+
    # exp(2Ht) sum_i dxi2, direct algebra gives R_ab=3H^2 g_ab.
    # This is a control metric, not an adopted equation or cosmological input.
    H = .37
    scale = np.exp(2*H*t)
    g = np.diag([-1., scale, scale, scale])[None]
    dg.fill(0); ddg.fill(0)
    dg[0, 0] = np.diag([0., 2*H*scale, 2*H*scale, 2*H*scale])
    ddg[0, 0, 0] = np.diag([0., 4*H*H*scale, 4*H*H*scale, 4*H*H*scale])
    r = coordinate_ricci(g, dg, ddg)
    results["nonvacuum_control_max_error"] = float(abs(r-3*H*H*g).max())
    assert results["nonvacuum_control_max_error"] < 2e-14

    # Nonconstant spatial metric: R_yy=1, R_zz=sin(y)^2 for a unit two-sphere
    # product.  This detects spatial-index errors in the generic routine.
    theta = .83
    g = np.diag([-1., 1., 1., np.sin(theta)**2])[None]
    dg.fill(0); ddg.fill(0)
    dg[0, 2, 3, 3] = np.sin(2*theta)
    ddg[0, 2, 2, 3, 3] = 2*np.cos(2*theta)
    expected = np.diag([0., 0., 1., np.sin(theta)**2])[None]
    r = coordinate_ricci(g, dg, ddg)
    results["spatial_control_max_error"] = float(abs(r-expected).max())
    assert results["spatial_control_max_error"] < 2e-14

    # Exact H^2 target geodesic: exp(P)=cosh(a log t)+(u/a)sinh(a log t),
    # Q=(v/a)sinh(a log t)/exp(P), lambda=(u^2+v^2)log t+constant.
    # Includes both time-live polarizations, no spatial differentiation.
    n, k, up, vq = 16, .75, .4, .3
    a = np.hypot(up, vq)
    times = np.unique(np.r_[1., np.arange(1.25, 4.01, .25),
                            2.+.004*np.arange(-4, 5), 2.+.002*np.arange(-4, 5)])
    s = np.log(times)
    e = np.cosh(a*s) + up/a*np.sinh(a*s)
    p = np.log(e)
    v = (a*np.sinh(a*s)+up*np.cosh(a*s))/e/times
    q = (vq/a)*np.sinh(a*s)/e
    w = vq/e**2/times
    lam = a*a*s + 4*np.log(k)
    exact = np.repeat(np.stack((p,v,q,w,lam),axis=1)[:,:,None], n, axis=2)
    numerical, evaluations = cpu_integrate(exact[0], times, k)
    results["homogeneous_DOP853_max_error"] = float(abs(numerical-exact).max())
    results["homogeneous_DOP853_nfev"] = evaluations
    assert results["homogeneous_DOP853_max_error"] < 2e-11
    results["saved_metric_stencil_h004"] = snapshot_ricci(times,exact,2.,.004,k)
    results["saved_metric_stencil_h002"] = snapshot_ricci(times,exact,2.,.002,k)
    assert results["saved_metric_stencil_h004"]["orthonormal_max_abs"] < 3e-8
    assert results["saved_metric_stencil_h002"]["orthonormal_max_abs"] < 1e-7

    # A smooth off-shell lambda perturbation must not pass the Ricci check.
    corrupted = exact.copy()
    corrupted[:, 4, :] += .02*np.sin(times[:,None])
    results["off_shell_lambda_catch"] = snapshot_ricci(times,corrupted,2.,.004,k)
    assert results["off_shell_lambda_catch"]["orthonormal_max_abs"] > 1e-3
    results["PASS"] = True
    results["implementation_sha256"] = file_hash(Path(__file__).with_name("independent_numerics.py"))
    results["selfcheck_sha256"] = file_hash(__file__)
    output = Path(__file__).with_name("SELFCHECK.json")
    output.write_text(json.dumps(results, indent=2)+"\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
