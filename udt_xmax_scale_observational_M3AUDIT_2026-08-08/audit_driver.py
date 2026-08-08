#!/usr/bin/env python3
"""M3-AUDIT heavy-compute driver (contract 2d9933d1). Stages:
  blocks-sys      : region-blocked counts, frozen 'sys' weights, all 9 targets
                    (serves B2 + B4; also the reproduction check vs checkpoints)
  blocks-nozfail  : same with WEIGHT_ZFAIL off (B5)
  halves-sys      : half-shell blocks, 'sys' (B3)
Tasks = (target, cap); priority order = outliers, thread control, remaining.
Modest CPU parallelism (4 workers, whole cap-units per worker, Category-A —
same allowance as the M3 runner); every count piece banked to its own npz as
it completes (resumable). Progress appended to audit_data/driver_log.txt.
"""
import sys
import time
import multiprocessing as mp

import audit_lib as al


def _log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(al.AUDIT_DATA + "/driver_log.txt", "a") as f:
        f.write(line + "\n")


def _task(args):
    tracer, zlo, zhi, cap, variant = args
    t0 = time.time()
    al.compute_cap_blocks(tracer, zlo, zhi, cap, variant, log=_log)
    _log(f"UNIT DONE {al.unit_key(variant, tracer, zlo, zhi, cap)} "
         f"({time.time() - t0:.0f}s)")
    return args


def tasks_for(stage):
    out = []
    for tracer, zlo, zhi, _role in al.TARGETS:
        if stage == "blocks-sys":
            spans, variant = [(zlo, zhi)], "sys"
        elif stage == "blocks-nozfail":
            spans, variant = [(zlo, zhi)], "nozfail"
        elif stage == "halves-sys":
            zm = round(0.5 * (zlo + zhi), 3)
            spans, variant = [(zlo, zm), (zm, zhi)], "sys"
        else:
            raise ValueError(stage)
        for a, b in spans:
            for cap in al.CAPS:
                out.append((tracer, a, b, cap, variant))
    return out


def main(stage, workers=4):
    ts = tasks_for(stage)
    _log(f"STAGE {stage}: {len(ts)} cap-units, workers={workers}")
    with mp.Pool(workers) as pool:
        for done in pool.imap(_task, ts):
            pass
    _log(f"STAGE {stage} COMPLETE")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 4)
