#!/usr/bin/env python3
"""M3b Phase-3 BOSS runner. Runs the FROZEN M3 pipeline (v_bao + look_elsewhere)
UNCHANGED against the FROZEN prediction (ell=58.34 Mpc, freeze f9c5b436, prereg
af9fa75d). F-RETRO ABSOLUTE: no frozen choice is altered in response to BOSS.

Frozen, unchanged from M3: Landy-Szalay w(theta) (v_bao.ls_w_theta_capcombine),
cap-combine ON (per-tracer floor), split-averaged RR (F=1 single random file here
-> reduces exactly to single-RR; declared), theta window [0.3,12] deg / 40 log
bins, 24-region jackknife, the cubic-null+Gaussian bump search (full window, no
seeding), 300-null look-elsewhere, GLOBAL_P_THRESHOLD=0.01, GPU spot-check under
amended-v2. Frozen 5e4 weighted-galaxy floor.

Category-A conditioning (declared BEFORE any w(theta) seen; not tuned to results):
  * backend='gpu' workhorse: BOSS random density makes the CPU tree exceed the
    anti-hang budget; the GPU counter is bin-identical to the CPU tree (M2
    equivalence test) and is validated here by the CPU-vs-GPU spot-check.
  * RAN_FACTOR=10 uniform random downsample (reduced from an initial 20 after a
    single-shell timing test showed 20x exceeds the anti-hang budget on CMASS;
    decided on THROUGHPUT, not on any assembly/verdict): RR/DR shot noise at 10x
    data stays below the 24-region jackknife variance; preserves the selection fn.
BOSS shell binning: DZ=0.05, LOWZ [0.15,0.43) CMASS [0.43,0.70), kept iff
weighted count >= 5e4 (census declared in BOSS_RESULTS.md).
"""
import argparse
import json
import os
import sys
import time
import zlib

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
M2 = os.path.join(os.path.dirname(HERE),
                  "udt_xmax_scale_observational_M2_build_2026-08-07")
sys.path.insert(0, M2)
sys.path.insert(0, HERE)
import v_bao            # noqa: E402  frozen pipeline
import look_elsewhere   # noqa: E402  frozen look-elsewhere
import boss_loader as bl  # noqa: E402

CKPT = os.path.join(HERE, "boss_checkpoints")
CAPS = ("North", "South")
DZ = 0.05
SAMPLES = {"LOWZ": (0.15, 0.43), "CMASS": (0.43, 0.70)}
FLOOR = v_bao.SHELL_MIN_WEIGHTED          # frozen 5e4
NULL_MOCKS = 300                          # frozen
GLOBAL_P = 0.01                           # frozen threshold
BACKEND = "gpu"
GPU_SPOT_SHELLS = (                       # BOSS designated CPU-vs-GPU shells
    ("CMASS", 0.53, 0.58),
    ("LOWZ", 0.30, 0.35))
_RAN_CACHE = {}


def _gal(samp, cap):
    return os.path.join(bl.BOSS_DIR, f"galaxy_DR12v5_{samp}_{cap}.fits.gz")


def _ran(samp, cap):
    return os.path.join(bl.BOSS_DIR, f"random0_DR12v5_{samp}_{cap}.fits.gz")


def _shell_edges(samp):
    zlo, zhi = SAMPLES[samp]
    e = list(np.round(np.arange(zlo, zhi + 1e-9, DZ), 3))
    if e[-1] < zhi - 1e-6:
        e.append(round(zhi, 3))
    return e


def census(use_sys=True):
    rows = []
    for samp in SAMPLES:
        edges = _shell_edges(samp)
        cats = {cap: bl.load_boss(_gal(samp, cap), use_sys=use_sys)
                for cap in CAPS}
        for a, b in zip(edges[:-1], edges[1:]):
            wsum = 0.0
            npc = []
            for cap in CAPS:
                c = cats[cap]
                m = (c.z >= a) & (c.z < b)
                wsum += float(c.w[m].sum())
                npc.append(int(m.sum()))
            rows.append({"sample": samp, "zlo": float(a), "zhi": float(b),
                         "w_sum": wsum, "n_per_cap": npc,
                         "kept": bool(wsum >= FLOOR)})
        del cats
    return rows


def _ran_downsampled(samp, cap, use_sys):
    """Load a cap's random ONCE, downsample uniformly to RAN_FACTOR x total
    galaxies (Category-A), cache. use_sys does not affect randoms (weight=1)."""
    key = (samp, cap)
    if key in _RAN_CACHE:
        return _RAN_CACHE[key]
    D = bl.load_boss(_gal(samp, cap), use_sys=use_sys)
    R = bl.load_boss(_ran(samp, cap), is_random=True)
    n_tgt = bl.RAN_FACTOR * len(D)
    Rds = bl.downsample(R, n_tgt, seed=bl.RAN_SEED)
    _RAN_CACHE[key] = Rds
    del D, R
    return Rds


def _shell_cats(samp, zlo, zhi, use_sys):
    cap_pairs = []
    for cap in CAPS:
        D = bl.load_boss(_gal(samp, cap), zrange=(zlo, zhi), use_sys=use_sys)
        Rfull = _ran_downsampled(samp, cap, use_sys)
        mr = (Rfull.z >= zlo) & (Rfull.z < zhi)
        R = v_bao.Catalog(Rfull.ra[mr], Rfull.dec[mr], Rfull.z[mr],
                          Rfull.w[mr], tag="real", name=Rfull.name + "[shell]")
        cap_pairs.append((D, [R]))     # F=1 split-RR (declared)
    return cap_pairs


def run_shell(samp, zlo, zhi, variant="sys"):
    os.makedirs(CKPT, exist_ok=True)
    key = f"{samp}_{zlo:.2f}_{zhi:.2f}_{variant}"
    npz_fn = os.path.join(CKPT, key + ".npz")
    json_fn = os.path.join(CKPT, key + ".json")
    if os.path.exists(json_fn):
        return json.load(open(json_fn))
    use_sys = variant == "sys"
    v_bao.authorize_m3(v_bao.M3_PREREG_COMMIT)   # flip guard (real-data)
    cap_pairs = _shell_cats(samp, zlo, zhi, use_sys)
    t0 = time.time()
    res = v_bao.ls_w_theta_capcombine(cap_pairs, backend=BACKEND)
    t_ls = time.time() - t0
    np.savez(npz_fn, theta=res["theta"], w=res["w"], sig=res["sig"],
             cov_jk=res["cov_jk"], DD=res["counts"]["DD"],
             DR=res["counts"]["DR"], RR=res["counts"]["RR"])
    fit = v_bao.detect_bump(res["theta"], res["w"], res["sig"], refine=True)
    seed = 20260808 + zlib.crc32(key.encode()) % 100000
    null_dist = v_bao.calibrate_max_dchi2(res["sig"], n_mocks=NULL_MOCKS,
                                          seed=seed)
    n95 = float(null_dist[int(0.95 * NULL_MOCKS)])
    rec = {"key": key, "sample": samp, "z": [zlo, zhi],
           "zc": 0.5 * (zlo + zhi), "variant": variant,
           "t_ls_s": round(t_ls, 1),
           "n_data_percap": [len(p[0]) for p in cap_pairs],
           "n_ran_percap": [len(p[1][0]) for p in cap_pairs],
           "bump": {k: fit[k] for k in ("dchi2", "theta_b", "sigma_b", "A_b")},
           "local_p": v_bao.bump_pvalue(fit["dchi2"], null_dist),
           "null_95th": n95,
           "radial_trigger": bool(fit["dchi2"] > n95),
           "seed": seed, "backend": BACKEND,
           "caveat": "diagonal jackknife cov (M2); F=1 split-RR; ran x10 (Cat-A)"}
    with open(json_fn, "w") as f:
        json.dump(rec, f, indent=1, default=float)
    print(f"  {key}: t_ls={t_ls:.1f}s dchi2={fit['dchi2']:.2f} "
          f"theta_b={fit['theta_b']:.3f} local_p={rec['local_p']:.4f} "
          f"Ndat={rec['n_data_percap']} Nran={rec['n_ran_percap']}")
    return rec


def gpu_spot_check(variant="sys"):
    """CPU-vs-GPU bin-identity on designated BOSS shells (amended-v2 criterion:
    per-cell rel<=1e-8 AND small-cell whole-pair census==0 AND total rel<=1e-9).
    Validates the GPU workhorse. Uses the actual shell catalogs (North cap)."""
    v_bao.authorize_m3(v_bao.M3_PREREG_COMMIT)
    out = []
    for samp, zlo, zhi in GPU_SPOT_SHELLS:
        D = bl.load_boss(_gal(samp, "North"), zrange=(zlo, zhi))
        Rfull = _ran_downsampled(samp, "North", True)
        mr = (Rfull.z >= zlo) & (Rfull.z < zhi)
        R = v_bao.Catalog(Rfull.ra[mr], Rfull.dec[mr], Rfull.z[mr],
                          Rfull.w[mr], tag="real", name="R")
        rm = v_bao.make_region_map(R.ra, R.dec, R.w)
        regD = v_bao.apply_region_map(rm, D.ra, D.dec)
        regR = v_bao.apply_region_map(rm, R.ra, R.dec)
        for name, args in (("DD", (D, D, regD, regD, 24, True)),
                           ("DR", (D, R, regD, regR, 24, False))):
            cpu = v_bao.pair_count_blocks(*args)
            gpu = v_bao.pair_count_blocks_gpu(*args)
            d = np.abs(cpu - gpu)
            mrel = float((d / np.maximum(cpu, 1.0)).max())
            tot = float(abs(cpu.sum() - gpu.sum()) / max(cpu.sum(), 1.0))
            nsp = int(((cpu <= 1e8) & (d > 0.5)).sum())
            ok = (mrel < 1e-8) and (nsp == 0) and (tot < 1e-9)
            out.append({"shell": [samp, "North", zlo, zhi], "count": name,
                        "max_abs_diff": float(d.max()), "max_rel_diff": mrel,
                        "total_rel_diff": tot, "n_smallcell_wholepair": nsp,
                        "ok": bool(ok),
                        "bound": "rel<=1e-8 & smallcell-wholepair==0 & total<=1e-9"})
            print(f"  spot {samp} {name}: mrel={mrel:.2e} tot={tot:.2e} "
                  f"nsp={nsp} ok={ok}")
            if not ok:
                raise RuntimeError(f"GPU spot-check FAILED {samp} {name}")
    return out


def assembly(variant="sys"):
    recs = []
    for fn in sorted(os.listdir(CKPT)):
        if fn.endswith(f"_{variant}.json"):
            recs.append(json.load(open(os.path.join(CKPT, fn))))
    w_list, sig_list, z_list = [], [], []
    for r in recs:
        d = np.load(os.path.join(CKPT, r["key"] + ".npz"))
        w_list.append(d["w"])
        sig_list.append(d["sig"])
        z_list.append(r["zc"])
    le = look_elsewhere.analyze_shells(w_list, sig_list, np.array(z_list),
                                       n_mocks=NULL_MOCKS, seed=20260808)
    res = {"prereg_commit": "af9fa75d", "freeze_commit": "f9c5b436",
           "variant": variant, "n_shells": len(recs), "per_shell": recs,
           "look_elsewhere": le,
           "feature_detected": bool(le["global_p"] < GLOBAL_P),
           "threshold": GLOBAL_P,
           "radial_leg_triggered_shells": [r["key"] for r in recs
                                           if r.get("radial_trigger")],
           "caveat": "diagonal jackknife cov; F=1 split-RR; ran x10 (Cat-A); "
                     "GPU workhorse (Cat-A, spot-checked)"}
    with open(os.path.join(HERE, f"boss_results_{variant}.json"), "w") as f:
        json.dump(res, f, indent=1, default=float)
    print(f"[{variant}] shells={len(recs)} global_p={le['global_p']:.4f} "
          f"feature={res['feature_detected']}")
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--census", action="store_true")
    ap.add_argument("--spot", action="store_true")
    ap.add_argument("--variant", default="both")
    args = ap.parse_args()
    if args.census:
        rows = census(use_sys=True)
        kept = [r for r in rows if r["kept"]]
        print(json.dumps({"kept": len(kept), "rows": rows}, indent=1))
        json.dump(rows, open(os.path.join(HERE, "boss_census.json"), "w"),
                  indent=1)
        return
    variants = ("sys", "nosys") if args.variant == "both" else (args.variant,)
    rows = [r for r in census(use_sys=True) if r["kept"]]
    for v in variants:
        print(f"=== variant {v} ({len(rows)} shells) ===")
        for r in rows:
            run_shell(r["sample"], r["zlo"], r["zhi"], variant=v)
    if args.spot:
        print("=== GPU spot-check ===")
        spot = gpu_spot_check()
    else:
        spot = None
    for v in variants:
        res = assembly(variant=v)
        if spot is not None:
            res["gpu_spot_check"] = spot
            json.dump(res, open(os.path.join(HERE,
                      f"boss_results_{v}.json"), "w"), indent=1, default=float)


if __name__ == "__main__":
    main()
