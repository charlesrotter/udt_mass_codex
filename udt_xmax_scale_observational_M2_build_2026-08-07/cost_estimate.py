#!/usr/bin/env python3
"""Deterministic generator for the `four_file_m3` section of
vbao_outputs/m3_cost_estimate.json (B2 amendment: every shipped number
regenerable by shipped code).

Inputs (all shipped/measured): the base per-shell rows (written by
v_bao.estimate_full_cost, 1-random-file convention), per-cap dec extents
(schema-level read, F-PEEK legal), and the measured GPU throughput /
cull reference from smoke_outputs/gpu_timing_LRG_NGC.json (frozen rounded
values restated below).

DR-COUNTING FIX (verifier item 5, <=5% nit): the shipped section counted DR
once in the GPU evals (343 = 1 + 18 + 18^2) but twice in the CPU pairs
(361 = 1 + 2*18 + 18^2). Both pipelines compute DR ONCE (a single D->R
ordered count), so the consistent factor is 343 for BOTH. Both totals are
kept below for the audit trail; the conclusion (GPU brute ~3.6-3.8x slower
than the CPU tree for the 4-file run) is unchanged.
"""
import json
import os

import numpy as np

import v_bao

HERE = os.path.dirname(os.path.abspath(__file__))
FN = os.path.join(HERE, "vbao_outputs", "m3_cost_estimate.json")

# frozen assumption constants (stated provenance)
THR_GPU = 4.5e8    # evals/s, rounded from measured 4.44-4.58e8 (timing smoke)
THR_CPU = 2.0e8    # in-window pairs/s, conservative vs measured ~2.5e8 (M2)
RANF = 18.0        # 4 random files ~ 18x data (M1 recon)
F_CULL_REF, EXT_REF = 0.42, 89.1   # measured dec-cull @ LRG NGC dec extent
F_ONCE = 1.0 + RANF + RANF ** 2          # DD + DR(once) + RR = 343
F_TWICE = 1.0 + 2.0 * RANF + RANF ** 2   # legacy shipped CPU convention = 361
F_BASE_1FILE = 25.0                      # base rows: (1 + 2*4 + 16), nr=4n


def dec_extents():
    from astropy.io import fits
    out = {}
    for tracer in v_bao.TRACER_ZRANGE:
        for cap in ("NGC", "SGC"):
            f = os.path.join(v_bao.DATA_DIR,
                             f"{tracer}_{cap}_clustering.dat.fits")
            with fits.open(f, memmap=True) as h:
                dec = np.asarray(h[1].data["DEC"], float)
            out[f"{tracer}_{cap}"] = float(dec.max() - dec.min())
    return out


def generate(write=True):
    est = json.load(open(FN))
    ext = dec_extents()
    rows, tg, tc_once, tc_twice = [], 0.0, 0.0, 0.0
    for r in est["rows"]:
        N = r["N"]
        f_cull = min(1.0, F_CULL_REF * EXT_REF / ext[f"{r['tracer']}_{r['cap']}"])
        evals = F_ONCE * N * N * f_cull
        t_gpu = evals / THR_GPU
        pairs_once = r["pairs"] * F_ONCE / F_BASE_1FILE
        pairs_twice = r["pairs"] * F_TWICE / F_BASE_1FILE
        t_cpu = pairs_once / THR_CPU
        tg += t_gpu
        tc_once += t_cpu
        tc_twice += pairs_twice / THR_CPU
        rows.append({**{k: r[k] for k in ("tracer", "cap", "z", "N")},
                     "f_cull": f_cull, "gpu_evals": evals, "t_gpu_s": t_gpu,
                     "cpu_inwindow_pairs_4file": pairs_once,
                     "t_cpu_s": t_cpu})
    worst_g = max(rows, key=lambda x: x["t_gpu_s"])
    worst_c = max(rows, key=lambda x: x["t_cpu_s"])
    section = {
        "generator": "cost_estimate.py (B2; deterministic)",
        "assumes": {"ran_factor_4files": RANF,
                    "gpu_evals_per_s_measured": THR_GPU,
                    "gpu_cull_ref": [F_CULL_REF, EXT_REF],
                    "cpu_pairs_per_s": THR_CPU,
                    "dr_counting": "ONCE on both backends (factor 343)",
                    "dec_extents_deg": ext},
        "rows": rows,
        "total_gpu_hr": tg / 3600.0,
        "total_cpu_hr": tc_once / 3600.0,
        "total_cpu_hr_legacy_DR_twice": tc_twice / 3600.0,
        "dr_fix_note": ("shipped v1 counted DR twice on CPU (361) vs once on "
                        "GPU (343); corrected to once/once. Legacy CPU total "
                        "kept for the audit trail; conclusion unchanged."),
        "worst_shell_gpu": {k: worst_g[k]
                            for k in ("tracer", "cap", "z", "N", "t_gpu_s")},
        "worst_shell_cpu": {k: worst_c[k]
                            for k in ("tracer", "cap", "z", "N", "t_cpu_s")},
        "honest_conclusion": (
            "For the FOUR-file run the brute GPU backend (dec-cull only, "
            "f_cull 0.42-0.68) is SLOWER in total than the CPU dual-tree, "
            "which pays only in-window pairs (about 4 percent of all): GPU "
            "{:.0f} GPU-hr vs CPU {:.0f} CPU-hr (DR-once, both). Bounded "
            "options for the M3 gate: (a) CPU tree for RR (dominant) + GPU "
            "DD/DR; (b) 2D (dec+RA) GPU block culling (est. 4-5x); (c) "
            "per-cap RR reuse across shells (exact in expectation under "
            "shuffled-z randoms; needs explicit prereg); (d) 1-random-file "
            "default (3.2 CPU-hr) + a 4-file spot-check shell."
        ).format(tg / 3600.0, tc_once / 3600.0)}
    est["four_file_m3"] = section
    if write:
        json.dump(est, open(FN, "w"), indent=1, default=float)
    return section


if __name__ == "__main__":
    s = generate()
    print("4-file totals: GPU %.1f hr | CPU (DR-once) %.1f hr | "
          "CPU legacy (DR-twice) %.1f hr"
          % (s["total_gpu_hr"], s["total_cpu_hr"],
             s["total_cpu_hr_legacy_DR_twice"]))
    print("worst GPU shell:", s["worst_shell_gpu"])
    print("worst CPU shell:", s["worst_shell_cpu"])
