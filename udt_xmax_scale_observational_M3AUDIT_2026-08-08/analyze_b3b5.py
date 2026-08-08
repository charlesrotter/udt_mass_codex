#!/usr/bin/env python3
"""B3 (sub-shell z-halves) + B5 (WEIGHT_ZFAIL off) analysis from cached audit
blocks. FORENSICS ONLY (contract 2d9933d1; authorize_m3 523f4aca).
Usage: analyze_b3b5.py b3|b5 [target_index ...]
Each target's result banked to audit_data/ as it completes."""
import os
import sys
import json
import numpy as np
import audit_lib as al
from analyze_b2b4 import blocks_ready


def _bins_from(th, ref):
    return float(abs(np.log(th / ref)) / np.log(al.LOG_BIN_FACTOR))


def run_b3(tracer, zlo, zhi, role):
    tag = f"{tracer}_{zlo:.2f}_{zhi:.2f}"
    out_fn = os.path.join(al.AUDIT_DATA, f"b3_{tag}.json")
    if os.path.exists(out_fn):
        return json.load(open(out_fn))
    zm = round(0.5 * (zlo + zhi), 3)
    ckj = json.load(open(os.path.join(al.CKPT_DIR, f"{tag}_sys.json")))
    ref = ckj["bump"]["theta_b"]
    halves = {}
    for a, b, name in ((zlo, zm, "lo_half"), (zm, zhi, "hi_half")):
        if not blocks_ready(tracer, a, b):
            return None
        r = al.full_shell_w(tracer, a, b, "sys")
        f = r["bump"]
        halves[name] = {"z": [a, b], "theta_b": f["theta_b"],
                        "dchi2": f["dchi2"], "A_b": f["A_b"],
                        "sigma_b": f["sigma_b"],
                        "bins_from_fullshell": _bins_from(f["theta_b"], ref)}
    rec = {"target": tag, "role": role, "theta_b_fullshell_ckpt": ref,
           "null_95th_fullshell": ckj["null_95th"], "halves": halves,
           "note": ("half-shell S/N is lower (~1/4 pair counts); persistence "
                    "in BOTH halves = sky-like; strong bump tracking ONE half "
                    "only = edge-tracking flag"),
           "prereg": [al.M3_PREREG_COMMIT, al.AUDIT_PREREG_COMMIT]}
    with open(out_fn, "w") as f:
        json.dump(rec, f, indent=1, default=float)
    return rec


def run_b5(tracer, zlo, zhi, role):
    tag = f"{tracer}_{zlo:.2f}_{zhi:.2f}"
    out_fn = os.path.join(al.AUDIT_DATA, f"b5_{tag}.json")
    if os.path.exists(out_fn):
        return json.load(open(out_fn))
    if not blocks_ready(tracer, zlo, zhi, "nozfail"):
        return None
    ckj = json.load(open(os.path.join(al.CKPT_DIR, f"{tag}_sys.json")))
    ref = ckj["bump"]
    r = al.full_shell_w(tracer, zlo, zhi, "nozfail")
    f = r["bump"]
    rec = {"target": tag, "role": role,
           "sys_ckpt": {k: ref[k] for k in ("theta_b", "dchi2", "A_b",
                                            "sigma_b")},
           "nozfail": {"theta_b": f["theta_b"], "dchi2": f["dchi2"],
                       "A_b": f["A_b"], "sigma_b": f["sigma_b"]},
           "theta_shift_pct": float((f["theta_b"] / ref["theta_b"] - 1) * 100),
           "A_shift_pct": float((f["A_b"] / ref["A_b"] - 1) * 100),
           "prereg": [al.M3_PREREG_COMMIT, al.AUDIT_PREREG_COMMIT]}
    with open(out_fn, "w") as f2:
        json.dump(rec, f2, indent=1, default=float)
    return rec


def main(which, indices=None):
    targets = al.TARGETS if indices is None else [al.TARGETS[i] for i in indices]
    for tracer, zlo, zhi, role in targets:
        fn = run_b3 if which == "b3" else run_b5
        r = fn(tracer, zlo, zhi, role)
        if r is None:
            print(f"SKIP {tracer} {zlo}-{zhi}: blocks not ready")
            continue
        if which == "b3":
            h = r["halves"]
            print(f"{r['target']:22s} full={r['theta_b_fullshell_ckpt']:.2f} "
                  f"lo: th={h['lo_half']['theta_b']:.2f} dchi2={h['lo_half']['dchi2']:.1f} "
                  f"({h['lo_half']['bins_from_fullshell']:.1f}b) | "
                  f"hi: th={h['hi_half']['theta_b']:.2f} dchi2={h['hi_half']['dchi2']:.1f} "
                  f"({h['hi_half']['bins_from_fullshell']:.1f}b)")
        else:
            print(f"{r['target']:22s} sys th={r['sys_ckpt']['theta_b']:.3f} "
                  f"nozfail th={r['nozfail']['theta_b']:.3f} "
                  f"dth={r['theta_shift_pct']:+.2f}% dA={r['A_shift_pct']:+.1f}% "
                  f"dchi2 {r['sys_ckpt']['dchi2']:.1f}->{r['nozfail']['dchi2']:.1f}")


if __name__ == "__main__":
    main(sys.argv[1], [int(a) for a in sys.argv[2:]] or None)
