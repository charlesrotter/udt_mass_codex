#!/usr/bin/env python3
"""M3b Phase-3: test BOSS results against the FROZEN prediction (freeze f9c5b436).
Reads only checkpoints + assembly json; changes NOTHING frozen. Reports, per
prereg SS3: (a) feature detected? (global trials-corr p<0.01); (b) does frozen
ell=58.34 Mpc predict BOSS theta_BAO within errors across >=2 shells?;
(c) drift/tracer behavior. Also reports measured BOSS ell' and ell'/R_w.
"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CKPT = os.path.join(HERE, "boss_checkpoints")
DEG = math.pi / 180.0

# FROZEN (freeze f9c5b436 / FROZEN_PREDICTION.md) -- do NOT change
ELL = 58.34
ELL_LO, ELL_HI = 57.01, 59.70
INV_N, XEFF = 0.947, 2086.0
N = 1.0 / INV_N
RW = N * XEFF               # 2202.7 Mpc


def rz(z):
    return RW * (1.0 - (1.0 + z) ** (-2.0 / N))


def theta_pred_deg(z):
    return ELL / rz(z) / DEG


def analyze(variant):
    res = json.load(open(os.path.join(HERE, f"boss_results_{variant}.json")))
    le = res["look_elsewhere"]
    print(f"\n===== variant {variant} =====")
    print(f"shells={res['n_shells']}  global_p={le['global_p']:.4f}  "
          f"feature_detected(<0.01)={res['feature_detected']}")
    print(f"joint p={le['joint']['p']:.4f}  "
          f"local_p min={min(le['local_p']):.4f}")
    rows = []
    print(f"{'shell':22s} {'zc':>5s} {'th_obs':>7s} {'sig_c':>6s} "
          f"{'th_pred':>7s} {'ell_obs':>7s} {'localp':>6s} {'within?':>7s}")
    for r in res["per_shell"]:
        b = r["bump"]
        zc = r["zc"]
        th_obs = b["theta_b"]
        dchi2 = max(b["dchi2"], 1e-6)
        sig_c = b["sigma_b"] / math.sqrt(dchi2)   # DERIVED center err (freeze)
        th_pr = theta_pred_deg(zc)
        ell_obs = math.radians(th_obs) * rz(zc)
        within = abs(th_obs - th_pr) <= sig_c
        rows.append(dict(key=r["key"], zc=zc, th_obs=th_obs, sig_c=sig_c,
                         th_pred=th_pr, ell_obs=ell_obs,
                         local_p=r["local_p"], within=bool(within),
                         dchi2=b["dchi2"]))
        print(f"{r['key']:22s} {zc:5.3f} {th_obs:7.3f} {sig_c:6.3f} "
              f"{th_pr:7.3f} {ell_obs:7.2f} {r['local_p']:6.3f} "
              f"{str(within):>7s}")
    n_within = sum(1 for x in rows if x["within"])
    ellp = [x["ell_obs"] for x in rows]
    print(f"  shells with th_obs within DERIVED center err of frozen pred: "
          f"{n_within}/{len(rows)}")
    print(f"  BOSS ell' per shell (deg-obs * r(z)): "
          f"min={min(ellp):.1f} max={max(ellp):.1f} Mpc")
    # landing
    feat = res["feature_detected"]
    if feat and n_within >= 2:
        landing = "M3b-PASS (replication + scale-consistent)"
    elif feat:
        landing = "M3b-PARTIAL (feature at ell' != frozen ell)"
    else:
        landing = "M3b-NULL (no feature at threshold; O-D lives)"
    print(f"  LANDING [{variant}]: {landing}")
    return dict(variant=variant, global_p=le["global_p"], feature=feat,
                n_within=n_within, n_shells=len(rows), rows=rows,
                landing=landing, ellp_min=min(ellp), ellp_max=max(ellp))


if __name__ == "__main__":
    print(f"FROZEN: ell={ELL} Mpc [{ELL_LO},{ELL_HI}]  n={N:.5f}  "
          f"R_w={RW:.1f} Mpc  ell/R_w={ELL/RW:.5f}")
    out = {}
    for v in ("sys", "nosys"):
        if os.path.exists(os.path.join(HERE, f"boss_results_{v}.json")):
            out[v] = analyze(v)
    json.dump(out, open(os.path.join(HERE, "boss_prediction_test.json"), "w"),
              indent=1, default=float)
