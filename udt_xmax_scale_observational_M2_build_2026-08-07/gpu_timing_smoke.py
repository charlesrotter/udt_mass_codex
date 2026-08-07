#!/usr/bin/env python3
"""GPU throughput timing smoke (Category-A; F-PEEK-ledgered).

Times pair_count_blocks_gpu on REAL LRG NGC shell positions (z 0.60-0.65) at
raised subsample sizes (2e5/4e5). CAP-RAISE STATEMENT: the frozen 2e4/4e4
smoke caps are raised HERE ONLY, in this quarantined timing path, because a
meaningful GPU timing needs >1 block (8192); authorized by the GPU amendment
dispatch. The computed pair counts are DISCARDED immediately -- only Ns,
wall times, eval totals (pure geometry: N^2 x block-cull fraction), and
throughput are persisted, to smoke_outputs/ with the standard header.
No w(theta), no count values, no clustering statistic is formed or stored.
"""
import json
import os
import time

import numpy as np

import v_bao

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "smoke_outputs")
os.makedirs(OUT, exist_ok=True)

rng = np.random.default_rng(3)
R = v_bao.load_catalog(os.path.join(v_bao.DATA_DIR,
                                    "LRG_NGC_0_clustering.ran.fits"),
                       zrange=(0.60, 0.65))
dec_extent = float(R.dec.max() - R.dec.min())
runs = []
for nsub in (200000, 400000):
    idx = rng.choice(len(R), nsub, replace=False)
    sub = v_bao.Catalog(R.ra[idx], R.dec[idx], R.z[idx], R.w[idx],
                        "real", "timing-sub")
    reg = np.zeros(nsub, dtype=np.int64)
    t0 = time.time()
    Cw = v_bao.pair_count_blocks_gpu(sub, sub, reg, reg, nreg=1, auto=True)
    dt = time.time() - t0
    st = v_bao.pair_count_blocks_gpu.last_stats
    del Cw  # counts discarded, never persisted
    runs.append({"n": nsub, "t_s": round(dt, 2),
                 "evals": st["n_evals"],
                 "block_pairs_run": st["block_pairs_run"],
                 "block_pairs_total": st["block_pairs_total"],
                 "cull_fraction": st["block_pairs_run"] / st["block_pairs_total"],
                 "evals_per_s": st["n_evals"] / dt,
                 "dtype": st["dtype"]})
payload = {"HEADER": v_bao.SMOKE_HEADER,
           "PURPOSE": ("GPU throughput timing only (Category-A). Counts "
                       "discarded; no clustering statistic persisted. "
                       "Cap raised in this quarantined timing path only, "
                       "as stated in the dispatch."),
           "shell": {"tracer": "LRG", "cap": "NGC", "z": [0.60, 0.65],
                     "source": "randoms file 0"},
           "dec_extent_deg": dec_extent,
           "runs": runs}
fn = os.path.join(OUT, "gpu_timing_LRG_NGC.json")
with open(fn, "w") as f:
    json.dump(payload, f, indent=1)
for r in runs:
    print(f"n={r['n']}: {r['t_s']}s  evals={r['evals']:.3e}  "
          f"cull={r['cull_fraction']:.3f}  thr={r['evals_per_s']:.3e}/s")
print("dec extent:", round(dec_extent, 1), "->", fn)
