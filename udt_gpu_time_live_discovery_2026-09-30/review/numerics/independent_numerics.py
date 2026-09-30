#!/usr/bin/env python3
"""Independent CPU/metric checks of conditional NGD1 snapshots.

No import of the production solver.  Coordinate order is t,x,y,z.  The
original-metric check differentiates saved metric snapshots in time, never
substitutes an evolution RHS for a time derivative, and contracts the generic
coordinate Christoffel definition.  This is floating-point validation, not a
symbolic proof or an infinite-dimensional existence certificate.
"""
import argparse
import hashlib
import json
import math
import platform
import resource
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp


def dx(values, k, order=1):
    """Real periodic Fourier derivative; even-N Nyquist first derivative is zero."""
    n = values.shape[-1]
    modes = np.fft.rfftfreq(n, d=1.0 / n) * k
    multiplier = (1j * modes) ** order
    if n % 2 == 0 and order % 2:
        multiplier[-1] = 0
    return np.fft.irfft(np.fft.rfft(values, axis=-1) * multiplier, n=n, axis=-1)


def cpu_rhs(t, flat, n, k):
    p, v, q, w, lam = flat.reshape(5, n)
    px = dx(p, k)
    qx = dx(q, k)
    weight = np.exp(2 * p)
    acceleration_p = dx(p, k, 2) - v / t + weight * (w * w - qx * qx)
    acceleration_q = dx(q, k, 2) - w / t - 2 * (v * w - px * qx)
    lambda_velocity = t * (v * v + px * px + weight * (w * w + qx * qx))
    return np.stack((v, acceleration_p, w, acceleration_q, lambda_velocity)).ravel()


def cpu_integrate(initial, times, k, rtol=2e-12, atol=2e-13):
    n = initial.shape[-1]
    sol = solve_ivp(cpu_rhs, (float(times[0]), float(times[-1])), initial.ravel(),
                    args=(n, k), method="DOP853", t_eval=times,
                    rtol=rtol, atol=atol)
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.y.T.reshape(len(times), 5, n), int(sol.nfev)


def metric(t, state):
    """Construct g only from supplied fields, with no derivative equations."""
    p, _, q, _, lam = state
    n = p.size
    g = np.zeros((n, 4, 4))
    a = np.exp(lam / 2) / np.sqrt(t)
    b = t * np.exp(p)
    g[:, 0, 0] = -a
    g[:, 1, 1] = a
    g[:, 2, 2] = b
    g[:, 2, 3] = g[:, 3, 2] = b * q
    g[:, 3, 3] = b * q * q + t * np.exp(-p)
    return g


def coordinate_ricci(g, dg, ddg):
    """Generic Ricci from g, partial g, partial partial g, no ansatz equations.

    dg[n, derivative, row, column], ddg[n, derivative1, derivative2, row,column].
    R_bd = partial_a Gamma^a_bd - partial_d Gamma^a_ba
           + Gamma^a_ae Gamma^e_bd - Gamma^a_de Gamma^e_ba.
    """
    inv = np.linalg.inv(g)
    dinv = -np.einsum("nau,neuv,nvd->nead", inv, dg, inv)
    c = np.zeros((len(g), 4, 4, 4))
    dc = np.zeros((len(g), 4, 4, 4, 4))
    for d in range(4):
        for b in range(4):
            for j in range(4):
                c[:, d, b, j] = dg[:, b, d, j] + dg[:, j, d, b] - dg[:, d, b, j]
                for e in range(4):
                    dc[:, e, d, b, j] = (ddg[:, e, b, d, j] + ddg[:, e, j, d, b]
                                         - ddg[:, e, d, b, j])
    gamma = .5 * np.einsum("nad,ndbc->nabc", inv, c)
    dgamma = .5 * (np.einsum("nead,ndbc->neabc", dinv, c)
                   + np.einsum("nad,nedbc->neabc", inv, dc))
    ric = np.zeros_like(g)
    for b in range(4):
        for d in range(4):
            for a in range(4):
                ric[:, b, d] += dgamma[:, a, a, b, d] - dgamma[:, d, a, b, a]
                for e in range(4):
                    ric[:, b, d] += (gamma[:, a, a, e] * gamma[:, e, b, d]
                                     - gamma[:, a, d, e] * gamma[:, e, b, a])
    return ric


def frame_ricci(ric, t, state):
    """Ricci in a real Lorentz-orthonormal frame; max norm avoids signed cancellation."""
    p, _, q, _, lam = state
    a = np.exp(lam / 2) / np.sqrt(t)
    frame = np.zeros_like(ric)
    frame[:, 0, 0] = frame[:, 1, 1] = 1 / np.sqrt(a)
    frame[:, 2, 2] = np.exp(-p / 2) / np.sqrt(t)
    frame[:, 3, 2] = -q * np.exp(p / 2) / np.sqrt(t)
    frame[:, 3, 3] = np.exp(p / 2) / np.sqrt(t)
    return np.einsum("nau,nuv,nbv->nab", frame, ric, frame)


def stencil_weights(derivative):
    offsets = np.arange(-4., 5.)
    target = np.zeros(9)
    target[derivative] = math.factorial(derivative)
    return np.linalg.solve(offsets[None, :] ** np.arange(9)[:, None], target)


def snapshot_ricci(times, states, center, h, k):
    wanted = center + h * np.arange(-4, 5)
    ids = np.array([np.argmin(abs(times - t)) for t in wanted])
    if np.max(abs(times[ids] - wanted)) > 5e-10:
        raise ValueError(f"Missing 9-point stencil center={center}, h={h}")
    metrics = np.stack([metric(float(times[j]), states[j]) for j in ids])
    dtg = np.einsum("s,snij->nij", stencil_weights(1) / h, metrics)
    dttg = np.einsum("s,snij->nij", stencil_weights(2) / h**2, metrics)
    g = metrics[4]
    # The spatial derivative routine has its data axis last.
    dgx = dx(np.moveaxis(g, 0, -1), k).transpose(2, 0, 1)
    dxxg = dx(np.moveaxis(g, 0, -1), k, 2).transpose(2, 0, 1)
    dtxg = dx(np.moveaxis(dtg, 0, -1), k).transpose(2, 0, 1)
    dg = np.zeros((len(g), 4, 4, 4))
    ddg = np.zeros((len(g), 4, 4, 4, 4))
    dg[:, 0] = dtg
    dg[:, 1] = dgx
    ddg[:, 0, 0] = dttg
    ddg[:, 0, 1] = ddg[:, 1, 0] = dtxg
    ddg[:, 1, 1] = dxxg
    ric = coordinate_ricci(g, dg, ddg)
    frame = frame_ricci(ric, center, states[ids[4]])
    # Supplementary dimensionless residual: local time-coordinate scale times
    # lapse.  Prevents a growing metric scale hiding absolute frame residuals.
    proper_time_scale_squared = center**1.5 * np.exp(states[ids[4], 4] / 2)
    return {"coordinate_max_abs": float(np.max(abs(ric))),
            "orthonormal_max_abs": float(np.max(abs(frame))),
            "proper_time_scaled_max_abs": float(np.max(abs(frame)
                * proper_time_scale_squared[:, None, None])),
            "ricci_symmetry_max": float(np.max(abs(ric - ric.transpose(0, 2, 1)))),
            "metric_determinant_max_error": float(np.max(abs(np.linalg.det(g)
                + np.exp(states[ids[4], 4]) * center))),
            "temporal_stencil": ids.tolist()}


def check_constraints(t, state, k):
    p, v, q, w, lam = state
    current = 2 * t * (v * dx(p, k) + np.exp(2 * p) * w * dx(q, k))
    error = dx(lam, k) - current
    return {"momentum_constraint_max_abs": float(np.max(abs(error))),
            "integrability_current_mean": float(np.mean(current))}


def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for part in iter(lambda: f.read(1 << 20), b""):
            h.update(part)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshots")
    parser.add_argument("metadata")
    parser.add_argument("--output", required=True)
    parser.add_argument("--cases", default="all")
    parser.add_argument("--centers", default="2,3")
    parser.add_argument("--steps", default=".004,.002")
    parser.add_argument("--cpu", action="store_true")
    args = parser.parse_args()
    start = time.monotonic()
    meta = json.loads(Path(args.metadata).read_text())
    data = np.load(args.snapshots, allow_pickle=False)
    times = data["times"]
    state = data["state"]
    if state.ndim == 3:
        state = state[:, None]
    k = float(meta.get("spec", meta)["k"])
    selected = list(range(state.shape[1])) if args.cases == "all" else list(map(int, args.cases.split(",")))
    report = {"implementation": "fresh NumPy rFFT/SciPy DOP853 and generic coordinate Christoffel/Ricci",
              "production_solver_imported": False,
              "source_sha256": file_hash(__file__),
              "input_sha256": {args.snapshots: file_hash(args.snapshots), args.metadata: file_hash(args.metadata)},
              "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
              "shape": list(state.shape), "k": k, "cases": []}
    for case in selected:
        saved = state[:, case]
        item = {"case_index": case, "initial_constraint": check_constraints(times[0], saved[0], k),
                "final_constraint": check_constraints(times[-1], saved[-1], k), "original_metric_ricci": []}
        if args.cpu:
            independent, nfev = cpu_integrate(saved[0], times, k)
            differences = np.max(abs(independent - saved), axis=(0, 2))
            item["cpu_comparison"] = {"method": "DOP853", "rtol": 2e-12, "atol": 2e-13,
                                       "nfev": nfev, "max_abs_by_component": differences.tolist(),
                                       "max_abs": float(differences.max())}
        for center in map(float, args.centers.split(",")):
            for h in map(float, args.steps.split(",")):
                item["original_metric_ricci"].append({"center": center, "h": h,
                    **snapshot_ricci(times, saved, center, h, k)})
        report["cases"].append(item)
    report["elapsed_seconds"] = time.monotonic() - start
    report["peak_rss_kib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
