#!/usr/bin/env python3
"""B2 (drop-one-region theta_b stability) + B4 (per-cap NGC vs SGC) from the
cached audit blocks, per target; plus the reproduction check of the
reassembled full-shell w(theta) against the M3 checkpoint. FORENSICS ONLY
(contract 2d9933d1; machinery under authorize_m3 523f4aca).
Usage: analyze_b2b4.py [target_index ...] (default: all with complete blocks)
"""
import os
import sys
import json
import numpy as np
import audit_lib as al


def blocks_ready(tracer, zlo, zhi, variant="sys"):
    for cap in al.CAPS:
        key = al.unit_key(variant, tracer, zlo, zhi, cap)
        if not os.path.exists(os.path.join(al.BLOCKS_DIR, key + "_META.json")):
            return False
    return True


def run_target(tracer, zlo, zhi, role):
    tag = f"{tracer}_{zlo:.2f}_{zhi:.2f}"
    out_fn = os.path.join(al.AUDIT_DATA, f"b2b4_{tag}.json")
    if os.path.exists(out_fn):
        return json.load(open(out_fn))
    # reproduction check vs the M3 checkpoint (sys)
    ck = np.load(os.path.join(al.CKPT_DIR, f"{tag}_sys.npz"))
    res = al.assemble_union(tracer, zlo, zhi, "sys")
    good = np.isfinite(ck["w"]) & np.isfinite(res["w"])
    repro = {"max_abs_dw": float(np.max(np.abs(res["w"][good] - ck["w"][good]))),
             "max_abs_dsig": float(np.max(np.abs(res["sig"][good] -
                                                 ck["sig"][good]))),
             "n_finite_bins": int(good.sum())}
    b2 = al.b2_drop_one(tracer, zlo, zhi, "sys")
    ckj = json.load(open(os.path.join(al.CKPT_DIR, f"{tag}_sys.json")))
    null95 = ckj["null_95th"]
    th_full = b2["full"]["theta_b"]
    ths = np.array([r["theta_b"] for r in b2["regions"]])
    dcs = np.array([r["dchi2"] for r in b2["regions"]])
    bins_moved = np.abs(np.log(ths / th_full)) / np.log(al.LOG_BIN_FACTOR)
    b2_sum = {"theta_b_full_refit": th_full,
              "theta_b_checkpoint": ckj["bump"]["theta_b"],
              "null_95th": null95,
              "max_bins_moved": float(bins_moved.max()),
              "n_regions_moved_gt_1bin": int((bins_moved > 1).sum()),
              "regions_moved_gt_1bin": [
                  {"region": int(k), "theta_b": float(ths[k]),
                   "bins": float(bins_moved[k]), "dchi2": float(dcs[k])}
                  for k in np.flatnonzero(bins_moved > 1)],
              "min_dchi2": float(dcs.min()),
              "n_regions_dchi2_below_null95": int((dcs < null95).sum()),
              "theta_b_spread_bins_p5_p95": [
                  float(np.percentile(bins_moved, 5)),
                  float(np.percentile(bins_moved, 95))]}
    b4 = al.b4_per_cap(tracer, zlo, zhi, "sys")
    b4_sum = {}
    for cap in al.CAPS:
        f = b4[cap]["bump"]
        b4_sum[cap] = {"theta_b": f["theta_b"], "dchi2": f["dchi2"],
                       "A_b": f["A_b"], "sigma_b": f["sigma_b"]}
    for cap in al.CAPS:
        b4_sum[cap]["bins_from_full"] = float(
            abs(np.log(b4_sum[cap]["theta_b"] / th_full)) /
            np.log(al.LOG_BIN_FACTOR))
    rec = {"target": tag, "role": role, "repro_check": repro,
           "B2": b2_sum, "B4": b4_sum,
           "B2_regions_full": b2["regions"],
           "prereg": [al.M3_PREREG_COMMIT, al.AUDIT_PREREG_COMMIT]}
    with open(out_fn, "w") as f:
        json.dump(rec, f, indent=1, default=float)
    return rec


def main(indices=None):
    targets = al.TARGETS if indices is None else [al.TARGETS[i] for i in indices]
    for tracer, zlo, zhi, role in targets:
        if not blocks_ready(tracer, zlo, zhi):
            print(f"SKIP {tracer} {zlo}-{zhi}: blocks not ready")
            continue
        r = run_target(tracer, zlo, zhi, role)
        print(f"{r['target']:22s} repro dw={r['repro_check']['max_abs_dw']:.2e} "
              f"B2 maxmove={r['B2']['max_bins_moved']:.2f}bins "
              f"(n>1bin={r['B2']['n_regions_moved_gt_1bin']}) "
              f"minDchi2={r['B2']['min_dchi2']:.1f} vs null95={r['B2']['null_95th']:.1f} | "
              f"B4 NGC th={r['B4']['NGC']['theta_b']:.2f} ({r['B4']['NGC']['bins_from_full']:.1f}b) "
              f"SGC th={r['B4']['SGC']['theta_b']:.2f} ({r['B4']['SGC']['bins_from_full']:.1f}b)")


if __name__ == "__main__":
    idx = [int(a) for a in sys.argv[1:]] or None
    main(idx)
