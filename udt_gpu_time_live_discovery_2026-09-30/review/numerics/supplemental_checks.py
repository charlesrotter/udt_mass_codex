#!/usr/bin/env python3
"""Independent initial-data, all-snapshot constraints, refinement and clocks.

Readouts were defined in SURVEY_FREEZE.json.  Profile reconstruction and the
all-snapshot review are adverse checks added during review, not new outcome
selection.  No production-code imports.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from independent_numerics import check_constraints, file_hash


def listed_modes(terms, x, k, derivative=0):
    out = np.zeros_like(x)
    for m, amplitude, phase in terms:
        out += amplitude * (m*k)**derivative * np.cos(m*k*x + phase + derivative*np.pi/2)
    return out


def reconstruct_initial(spec, case, x):
    k = spec["k"]
    p, v, q, w = [listed_modes(case.get(name, []), x, k) for name in ("P", "V", "Q", "W")]
    px, qx = [listed_modes(case.get(name, []), x, k, 1) for name in ("P", "Q")]
    mean_momentum = np.mean(v*px + np.exp(2*p)*w*qx)
    denominator = np.mean(px*px)
    alpha = mean_momentum/denominator if denominator > 1e-24 else 0.
    v = v-alpha*px
    momentum = 2*(v*px + np.exp(2*p)*w*qx)
    coefficients = np.fft.rfft(momentum)
    frequencies = k*np.arange(len(coefficients))
    primitive = np.zeros_like(coefficients)
    primitive[1:] = coefficients[1:]/(1j*frequencies[1:])
    primitive[-1] = 0
    lam = np.fft.irfft(primitive, n=len(x))+4*np.log(.75)
    return np.stack((p,v,q,w,lam)), float(alpha)


def shifted_samples(values, k, displacement):
    """Evaluate the real trig polynomial directly, rather than FFT shifting."""
    n = values.size
    c = np.fft.rfft(values)/n
    phase = k*(np.arange(n)*2*np.pi/(k*n)+displacement)
    result = np.full(n, c[0].real)
    for m in range(1, len(c)-1):
        result += 2*(c[m].real*np.cos(m*phase)-c[m].imag*np.sin(m*phase))
    result += c[-1].real*np.cos((n//2)*phase)
    return result


def clocks(times, state, k):
    output = []
    fields = []
    for te in (1., 4., 8., 16.):
        for d in (1., 2., 4., 8.):
            if te+d > times[-1]:
                continue
            ie, io = [int(np.argmin(abs(times-t))) for t in (te,te+d)]
            assert abs(times[ie]-te)<1e-11 and abs(times[io]-te-d)<1e-11
            increment = shifted_samples(state[io,4],k,d)-state[ie,4]
            logz = (increment-np.log((te+d)/te))/4
            output.append({"te": te, "d": d, "logZ_min": float(logz.min()),
                           "logZ_max": float(logz.max()),
                           "delta_lambda_min": float(increment.min()),
                           "delta_lambda_max": float(increment.max())})
            fields.append(logz)
    return output, np.array(fields)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--pairs", nargs="*", default=[])
    args = ap.parse_args()
    package = Path(__file__).resolve().parents[2]
    report = {"source_sha256": file_hash(__file__), "runs": {}, "refinements": []}
    arrays = {}
    for name in args.runs:
        run = package/"runs"/name
        meta = json.loads((run/"metadata.json").read_text())
        data = np.load(run/"fields.npz", allow_pickle=False)
        times, x, state = data["times"], data["x"], data["state"]
        spec = meta["spec"]
        item = {"input_sha256": {str(run/"fields.npz"):file_hash(run/"fields.npz"),
                                  str(run/"metadata.json"):file_hash(run/"metadata.json")},
                "cases": []}
        readout_fields = []
        for j, case in enumerate(spec["cases"]):
            expected, alpha = reconstruct_initial(spec, case, x)
            constraint = [check_constraints(t, fields, spec["k"])
                          for t, fields in zip(times, state[:,j])]
            readouts, fields = clocks(times, state[:,j], spec["k"])
            item["cases"].append({"id":case["id"], "alpha":alpha,
                "initial_reconstruction_max_abs":float(abs(expected-state[0,j]).max()),
                "constraint_all_snapshots_max_abs":max(c["momentum_constraint_max_abs"] for c in constraint),
                "mean_momentum_all_snapshots_max_abs":max(abs(c["integrability_current_mean"]) for c in constraint),
                "readouts": readouts})
            readout_fields.append(fields)
        report["runs"][name] = item
        arrays[name] = (times, state, np.array(readout_fields))
    for pair in args.pairs:
        first, second = pair.split(":")
        ta, a, ca = arrays[first]
        tb, b, cb = arrays[second]
        assert np.max(abs(ta-tb))<1e-11
        stride = b.shape[-1]//a.shape[-1]
        assert b.shape[-1] == stride*a.shape[-1]
        report["refinements"].append({"runs":[first,second],
            "max_abs_state_difference":float(abs(a-b[...,::stride]).max()),
            "max_abs_logZ_difference":float(abs(ca-cb[...,::stride]).max())})
    Path(args.output).write_text(json.dumps(report,indent=2)+"\n")
    for name, r in report["runs"].items():
        cs=r["cases"]
        print(name, "initial",max(c["initial_reconstruction_max_abs"] for c in cs),
              "constraint",max(c["constraint_all_snapshots_max_abs"] for c in cs),
              "logZ",min(v["logZ_min"] for c in cs for v in c["readouts"]),
              max(v["logZ_max"] for c in cs for v in c["readouts"]),
              "delta_lambda_min",min(v["delta_lambda_min"] for c in cs for v in c["readouts"]))
    print(json.dumps(report["refinements"],indent=2))


if __name__ == "__main__":
    main()
