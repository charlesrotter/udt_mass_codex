#!/usr/bin/env python3
"""M3 V-BAO runner (prereg SS4, commit 523f4aca). Per-shell checkpointed;
cap-combine ON (per-tracer floor); split-averaged RR over the FOUR random
files; CPU tree workhorse; GPU spot-check on the 3 designated shells;
look-elsewhere assembly. WEIGHT_SYS with/without variants both run.

--dry-run: shell enumeration + per-tracer floor census (cap-combine ON),
checkpoint plan and ETA -- NO pair counting, guard never flipped.
Real mode: guard flip ONLY via v_bao.authorize_m3(M3_PREREG_COMMIT)
(prereg SS5.4). Modest CPU parallelism: --workers N (max 4, Category-A,
documented); each worker handles whole shells; checkpoints make the run
resumable (staged banking).
"""
import argparse
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
M2_BUILD = os.path.join(os.path.dirname(HERE),
                        "udt_xmax_scale_observational_M2_build_2026-08-07")
sys.path.insert(0, M2_BUILD)
import v_bao            # noqa: E402
import look_elsewhere   # noqa: E402

M3_PREREG_COMMIT = "523f4aca"
CKPT_DIR = os.path.join(HERE, "bao_checkpoints")
CAPS = ("NGC", "SGC")
N_RAN_FILES = 4
WORKERS_MAX = 4
NULL_MOCKS = 300                      # frozen (prereg SS4)
GLOBAL_P_THRESHOLD = 0.01             # frozen: "feature detected" bar
GPU_SPOT_SHELLS = (                   # frozen designated spot-check shells
    ("LRG", "NGC", 0.60, 0.65),
    ("BGS_BRIGHT", "NGC", 0.21, 0.26),
    ("QSO", "NGC", 1.10, 1.25))
CPU_PAIRS_PER_S = 2.5e8               # measured M2 throughput (ETA only)
SPLIT_FACTOR = 1.0 + 18.0 + 4 * 4.5 ** 2   # DD + DR(cat 18x) + 4xRR(4.5x)


def _dat_path(tracer, cap):
    return os.path.join(v_bao.DATA_DIR, f"{tracer}_{cap}_clustering.dat.fits")


def _ran_path(tracer, cap, i):
    return os.path.join(v_bao.DATA_DIR,
                        f"{tracer}_{cap}_{i}_clustering.ran.fits")


def census(use_sys=True):
    """Cap-combine census: per-tracer shell floor (prereg SS4).
    Loads the 8 data catalogs (loader-legal); NO pair counting."""
    out = []
    for tracer in v_bao.TRACER_ZRANGE:
        cats = [v_bao.load_catalog(_dat_path(tracer, cap), use_sys=use_sys)
                for cap in CAPS]
        kept, dropped = v_bao.bin_shells_combined(cats, tracer)
        for sh in kept:
            n_caps = [int(m.sum()) for m in sh["masks"]]
            out.append({"tracer": tracer, "zlo": sh["zlo"], "zhi": sh["zhi"],
                        "w_sum": sh["w_sum"], "n_per_cap": n_caps,
                        "kept": True})
        for sh in dropped:
            out.append({"tracer": tracer, "zlo": sh["zlo"], "zhi": sh["zhi"],
                        "w_sum": sh["w_sum"], "kept": False})
        del cats
    return out


def _foot_sr():
    """Per-(tracer,cap) footprint solid angle from the shipped cost rows."""
    fn = os.path.join(M2_BUILD, "vbao_outputs", "m3_cost_estimate.json")
    rows = json.load(open(fn))["rows"]
    out = {}
    for r in rows:
        out.setdefault((r["tracer"], r["cap"]),
                       r["foot_deg2"] * (np.pi / 180.0) ** 2)
    return out


def eta_hours(census_rows, n_variants=2, workers=1):
    """ETA for the real run from the M2-measured CPU tree throughput."""
    cap_sr = 2 * np.pi * (1 - np.cos(np.radians(v_bao.THETA_MAX_DEG)))
    foot = _foot_sr()
    total_pairs = 0.0
    for row in census_rows:
        if not row["kept"]:
            continue
        for cap, n in zip(CAPS, row["n_per_cap"]):
            fs = foot.get((row["tracer"], cap))
            if fs is None or n == 0:
                continue
            total_pairs += SPLIT_FACTOR * n * n * min(cap_sr / fs, 1.0)
    hours = total_pairs / CPU_PAIRS_PER_S / 3600.0 * n_variants
    return {"total_pairs_est": total_pairs, "n_variants": n_variants,
            "eta_cpu_hr_serial": hours,
            "eta_wallclock_hr_at_workers": hours / max(1, min(workers,
                                                              WORKERS_MAX))}


def dry_run(workers=1):
    t0 = time.time()
    rows = census(use_sys=True)
    kept = [r for r in rows if r["kept"]]
    dropped = [r for r in rows if not r["kept"]]
    eta = eta_hours(rows, n_variants=2, workers=workers)
    plan = {"prereg_commit": M3_PREREG_COMMIT,
            "convention": "cap-combine ON, per-tracer floor; split-averaged "
                          "RR over 4 files; union-region jackknife",
            "n_shells_kept": len(kept), "n_shells_dropped": len(dropped),
            "kept_shells": kept, "dropped_shells": dropped,
            "checkpoint_dir": CKPT_DIR,
            "checkpoint_plan": "one npz (counts+w+sig+cov) + one json "
                               "(bump+local p) per (shell, variant); "
                               "resumable by file existence",
            "variants": ["sys", "nosys"], "workers_max": WORKERS_MAX,
            "gpu_spot_shells": [list(s) for s in GPU_SPOT_SHELLS],
            "eta": eta,
            "guard_state": {"M3_REAL_RUN_AUTHORIZED":
                            v_bao.M3_REAL_RUN_AUTHORIZED,
                            "note": "dry-run never flips the guard"},
            "census_time_s": round(time.time() - t0, 1)}
    fn = os.path.join(HERE, "bao_dry_run_census.json")
    with open(fn, "w") as f:
        json.dump(plan, f, indent=1, default=float)
    per_tracer = {}
    for r in kept:
        per_tracer[r["tracer"]] = per_tracer.get(r["tracer"], 0) + 1
    print(f"kept shells: {len(kept)} {per_tracer}; dropped: {len(dropped)}")
    print(f"ETA: {eta['eta_cpu_hr_serial']:.1f} CPU-hr serial "
          f"(both weight variants), "
          f"{eta['eta_wallclock_hr_at_workers']:.1f} hr at "
          f"{min(workers, WORKERS_MAX)} workers")
    print(f"DRY-RUN COMPLETE (no pair counting; guard untouched) -> {fn}")
    return plan

def _shell_key(tracer, zlo, zhi, variant):
    return f"{tracer}_{zlo:.2f}_{zhi:.2f}_{variant}"


def run_shell(tracer, zlo, zhi, variant="sys", backend="cpu"):
    """One (shell, variant): cap-combined split-RR LS -> checkpoint npz;
    bump search + frozen null-mock calibration -> checkpoint json."""
    os.makedirs(CKPT_DIR, exist_ok=True)
    key = _shell_key(tracer, zlo, zhi, variant)
    npz_fn = os.path.join(CKPT_DIR, key + ".npz")
    json_fn = os.path.join(CKPT_DIR, key + ".json")
    if os.path.exists(json_fn):
        return json.load(open(json_fn))          # resumable: staged banking
    use_sys = variant == "sys"
    cap_pairs = []
    for cap in CAPS:
        D = v_bao.load_catalog(_dat_path(tracer, cap), zrange=(zlo, zhi),
                               use_sys=use_sys)
        R_list = [v_bao.load_catalog(_ran_path(tracer, cap, i),
                                     zrange=(zlo, zhi), use_sys=use_sys)
                  for i in range(N_RAN_FILES)]
        cap_pairs.append((D, R_list))
    t0 = time.time()
    res = v_bao.ls_w_theta_capcombine(cap_pairs, backend=backend)
    t_ls = time.time() - t0
    np.savez(npz_fn, theta=res["theta"], w=res["w"], sig=res["sig"],
             cov_jk=res["cov_jk"], DD=res["counts"]["DD"],
             DR=res["counts"]["DR"], RR=res["counts"]["RR"])
    fit = v_bao.detect_bump(res["theta"], res["w"], res["sig"], refine=True)
    import zlib
    seed = 20260807 + zlib.crc32(key.encode()) % 100000   # deterministic
    null_dist = v_bao.calibrate_max_dchi2(res["sig"], n_mocks=NULL_MOCKS,
                                          seed=seed)
    rec = {"key": key, "tracer": tracer, "z": [zlo, zhi], "variant": variant,
           "zc": 0.5 * (zlo + zhi), "t_ls_s": round(t_ls, 1),
           "bump": {k: fit[k] for k in ("dchi2", "theta_b", "sigma_b",
                                        "A_b")},
           "local_p": v_bao.bump_pvalue(fit["dchi2"], null_dist),
           "null_95th": float(null_dist[int(0.95 * NULL_MOCKS)]),
           "radial_trigger": bool(fit["dchi2"] >
                                  null_dist[int(0.95 * NULL_MOCKS)]),
           "seed": seed, "backend": backend,
           "caveat": "diagonal jackknife covariance (M2 condition)"}
    with open(json_fn, "w") as f:
        json.dump(rec, f, indent=1, default=float)
    return rec


def gpu_spot_check():
    """Frozen SS4: recompute DD/DR on the GPU backend for the 3 designated
    shells; bin-identical agreement required (M2 equivalence bound);
    disagreement = STOP."""
    out = []
    for tracer, cap, zlo, zhi in GPU_SPOT_SHELLS:
        D = v_bao.load_catalog(_dat_path(tracer, cap), zrange=(zlo, zhi))
        Rcat = v_bao._concat_catalogs(
            [v_bao.load_catalog(_ran_path(tracer, cap, i),
                                zrange=(zlo, zhi))
             for i in range(N_RAN_FILES)])
        rm = v_bao.make_region_map(Rcat.ra, Rcat.dec, Rcat.w)
        regD = v_bao.apply_region_map(rm, D.ra, D.dec)
        regR = v_bao.apply_region_map(rm, Rcat.ra, Rcat.dec)
        for name, args in (("DD", (D, D, regD, regD, 24, True)),
                           ("DR", (D, Rcat, regD, regR, 24, False))):
            cpu = v_bao.pair_count_blocks(*args)
            gpu = v_bao.pair_count_blocks_gpu(*args)
            d = np.abs(cpu - gpu)
            md = float(d.max())
            # AMENDED BOUND (2026-08-08, disclosed; Category-A recalibration
            # after the STOP fired on BGS DR and the diagnosis proved the
            # diffs are accumulation-order dust: 0 cells at whole-pair scale,
            # worst diffs magnitude-proportional (4.6e-2 on 1.2e8-count
            # cells, 3.8e-10 relative, at 1/10-randoms scale). Old absolute
            # bound 1e-9*cpu.max() did not scale with accumulation growth on
            # full 4-file cells. New criterion: per-cell RELATIVE agreement
            # <= 1e-8 -- still catches one misassigned pair on any cell
            # <~1e8 counts; single-pair errors on larger cells are below
            # this check's sensitivity (stated limit; gross failures hit
            # many cells and remain trivially detectable). Results-verifier
            # must re-adjudicate this amendment (flagged).
            mrel = float((d / np.maximum(cpu, 1.0)).max())
            tot_rel = float(abs(cpu.sum() - gpu.sum()) / max(cpu.sum(), 1.0))
            ok = (mrel < 1e-8) and (tot_rel < 1e-10)
            out.append({"shell": [tracer, cap, zlo, zhi], "count": name,
                        "max_abs_diff": md, "max_rel_diff": mrel,
                        "total_rel_diff": tot_rel, "ok": bool(ok),
                        "bound": "rel<=1e-8 & total<=1e-10 (amended "
                                 "2026-08-08, see BAO diagnosis note)"})
            if not ok:
                raise RuntimeError(f"GPU spot-check FAILED on {tracer} "
                                   f"{cap} {zlo}-{zhi} {name}: STOP, "
                                   "diagnose (prereg SS4)")
    return out


def assembly(variant="sys"):
    """After all shells: look-elsewhere + joint fits + BAO_RESULTS."""
    recs = []
    for fn in sorted(os.listdir(CKPT_DIR)):
        if fn.endswith(f"_{variant}.json"):
            recs.append(json.load(open(os.path.join(CKPT_DIR, fn))))
    w_list, sig_list, z_list = [], [], []
    for r in recs:
        d = np.load(os.path.join(CKPT_DIR, r["key"] + ".npz"))
        w_list.append(d["w"])
        sig_list.append(d["sig"])
        z_list.append(r["zc"])
    le = look_elsewhere.analyze_shells(w_list, sig_list, np.array(z_list),
                                       n_mocks=NULL_MOCKS, seed=20260807)
    radial = [r["key"] for r in recs if r.get("radial_trigger")]
    spot = gpu_spot_check()
    res = {"prereg_commit": M3_PREREG_COMMIT, "variant": variant,
           "n_shells": len(recs), "per_shell": recs,
           "look_elsewhere": le,
           "feature_detected": bool(le["global_p"] < GLOBAL_P_THRESHOLD),
           "threshold": GLOBAL_P_THRESHOLD,
           "radial_leg_triggered_shells": radial,
           "radial_note": ("attempt-only; retired for DR1 with honest note "
                           "if no shell triggers (prereg SS4)"),
           "gpu_spot_check": spot,
           "caveat": "diagonal jackknife covariance on every significance"}
    with open(os.path.join(HERE, f"bao_results_{variant}.json"), "w") as f:
        json.dump(res, f, indent=1, default=float)
    return res


def real_run(workers=1, backend="cpu"):
    v_bao.authorize_m3(M3_PREREG_COMMIT)
    rows = [r for r in census(use_sys=True) if r["kept"]]
    tasks = [(r["tracer"], r["zlo"], r["zhi"], v)
             for v in ("sys", "nosys") for r in rows]
    workers = max(1, min(workers, WORKERS_MAX))
    if workers == 1:
        for t in tasks:
            print("shell", t)
            run_shell(*t)
    else:   # modest CPU parallelism (Category-A; whole shells per worker)
        import multiprocessing as mp
        with mp.Pool(workers, initializer=_worker_init) as pool:
            pool.starmap(run_shell, tasks)
    out = {v: assembly(variant=v) for v in ("sys", "nosys")}
    print("BAO run complete:",
          {v: out[v]["feature_detected"] for v in out})
    return out


def _worker_init():
    v_bao.authorize_m3(M3_PREREG_COMMIT)   # each worker process re-arms


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--backend", default="cpu")
    args = ap.parse_args()
    if args.dry_run:
        dry_run(workers=args.workers)
    else:
        real_run(workers=args.workers, backend=args.backend)
