#!/usr/bin/env python3
"""
p5b_gate12.py -- P5b GATE 1 (PC -> machine floor) + GATE 2 (PC-INDEPENDENCE at floor).

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  OBSERVE/INFRA.  DATA-BLIND.  Branch p5b-pc-floor.

GATE 1: a light PC drives the re-posed matrix-free JFNK to ~machine floor (~1e-12/1e-13)
        on the committed residual, in a sane iteration count.  Report residual history,
        inner-LSMR-iter counts, wall-time -- and the no-PC baseline (does it floor too,
        and at what Krylov cost?).
GATE 2: >=2 PC settings (incl. none) converge to the SAME fixed point, field-by-field,
        to ~machine floor.  Proves the PC changes only the path, not the fixed point.

Grid: anchor grid (12,6,8) -- where P5a' plateaued -- and a usable grid (16,8,8).
The #60 axisym-l2 perturbed seed is the off-round test (the stall case JFNK must clear
to floor, not just below the wall).

NOTE: pure JFNK here uses the CACHING allocator (fast).  The dense anchor is run in a
SEPARATE process (p5b_anchor.py) because it forces the no-cache allocator.
"""
import os, sys, time
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight, residuals, diagnostics
from full3d_solver import residual_vector, round_seed, unpack
import p5a_prime_repose as RP
import p5b_pc as PC

P, KAP8 = 0.4, 0.05
fields = ['a', 'b', 'c', 'd', 'Th']


def committed_phys(rp, ub, G, tag):
    u = rp.embed_vsafe(ub)
    F = residual_vector(u, G, P, KAP8); Phi = float((F*F).sum())
    out = residuals(G, unpack(u, G), P, KAP8); d = diagnostics(G, out, KAP8)
    print(f"  [{tag}] committed-Phi={Phi:.3e} M_MS={d['M_MS']:.6f} "
          f"tvar={d['tvar']:.4e}", flush=True)
    return Phi, d


def run_grid(NR, NTH, NPS, seed='round', pcs=('none', 'diag', 'rband'),
             maxit=80, lsmr_maxit=3000):
    print(f"\n########## GRID ({NR},{NTH},{NPS}) seed={seed} ##########", flush=True)
    G = Grid3D(NR, NTH, NPS, rc=0.05, cell=14.0); G = attach_coord_weight(G)
    u0, sol = round_seed(G, p=P, kap8=KAP8)
    rp = RP.Repose(G, p=P, m=1, edge_mode='hold', fit_deg=4); rp.set_edge_hold(u0)
    if seed == 'round':
        useed = u0
    else:  # axisym-l2 off-round perturbation (#60 stall case)
        useed = RP.axi_l2_seed(G, u0, amp=0.25, m=1)
    ub0 = rp.extract(useed)
    F0 = residual_vector(rp.embed_vsafe(ub0), G, P, KAP8)
    print(f"  seed committed-Phi0={float((F0*F0).sum()):.4e}  nB={rp.nB}", flush=True)

    sols = {}
    for pc in pcs:
        ub, hist, its, wt = PC.jfnk_solve(ub0, rp, u0, KAP8, pc=pc, maxit=maxit,
                                          tol=1e-13, lsmr_maxit=lsmr_maxit,
                                          lsmr_tol=1e-13, verbose=True)
        avg = np.mean(its) if its else 0
        print(f"  >>> JFNK[pc={pc}] FINAL reposed-Phi={hist[-1]:.4e} "
              f"newton-its={len(hist)-1} lsmr-avg={avg:.0f} lsmr-tot={int(np.sum(its))} "
              f"wall={wt:.0f}s", flush=True)
        committed_phys(rp, ub, G, f"JFNK[{pc}]")
        sols[pc] = ub

    # GATE 2: PC-independence at floor, field-by-field
    print("  --- GATE 2: PC-INDEPENDENCE (field-by-field max|diff|) ---", flush=True)
    ref = pcs[0]
    nbr = rp.nbr
    for pc in pcs[1:]:
        diff = (sols[pc] - sols[ref]).reshape(5, nbr, NTH, NPS)
        per = {fields[f]: float(diff[f].abs().max()) for f in range(5)}
        tot = float((sols[pc]-sols[ref]).abs().max())
        print(f"    |{pc} - {ref}|: max={tot:.3e}  per-field=" +
              " ".join(f"{k}={v:.2e}" for k, v in per.items()), flush=True)
    # save body solutions for cross-process anchor check
    torch.save({'nB': rp.nB, 'NR': NR, 'NTH': NTH, 'NPS': NPS,
                **{pc: sols[pc].cpu() for pc in pcs}},
               f'/tmp/p5b_sols_{NR}_{NTH}_{NPS}_{seed}.pt')
    return sols, rp, G


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if which in ('all', 'anchor'):
        run_grid(12, 6, 8, seed='round')
    if which in ('all', 'off'):
        run_grid(12, 6, 8, seed='axil2')
    if which in ('all', 'usable'):
        run_grid(16, 8, 8, seed='round')
    print("\n=== P5b GATE12 DONE ===", flush=True)
