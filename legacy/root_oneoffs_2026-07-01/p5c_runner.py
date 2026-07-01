#!/usr/bin/env python3
"""
p5c_runner.py -- P5c-step-1: DECISIVE uniqueness re-run at usable resolution.

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  OBSERVE/INFRA.  DATA-BLIND.
Branch: p5c-uniqueness.  NEW FILE (reuses committed p5b_* / full3d_* as imports only).

QUESTION (the one P5c-step-1 settles): does the P5b Nr=12 PC-non-independence
(M_MS spread 9.3%, cross-gauge dM_MS 4.6%) COLLAPSE as Nr increases (=> coarse-grid
artifact, anchor resolution-robust) or PERSIST (=> real under-determination)?

ANTI-HANG (strict): SINGLE clean process per invocation; NO background+poll; NO
concurrent solves.  Hard caps per solve (Newton<=cap, LSMR<=cap).  Per-solve timing
printed so we can bail to a bounded answer.  Accept "floored to ~1e-10/1e-11".

USAGE:
  python3 p5c_runner.py solve  NR PC GAUGE [NEWTON_CAP] [LSMR_CAP]
      # ONE clean solve, saved to /tmp.  PC in {diag,rband,none}; GAUGE in {G1,G2}.
      # (G1=round-seed edges; G2=+smooth bump.  PC-independence => run two PCs, same
      #  gauge G1.  Cross-gauge => run rband on G1 and G2.)
  python3 p5c_runner.py compare NR TAG1 TAG2
      # load two saved solves (tag = "<PC>_<GAUGE>") and print field-by-field + dM_MS.

Each `solve` is a SINGLE process, one PC, hard-capped (anti-hang).  Run them
sequentially (never concurrent), then `compare`.
"""
import os, sys, time
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight, residuals, diagnostics
from full3d_solver import residual_vector, round_seed, unpack
import p5a_prime_repose as RP
import p5b_pc as PC
from p5b_loosethread import smooth_edge_bump

P, KAP8 = 0.4, 0.05
fields = ['a', 'b', 'c', 'd', 'Th']


def committed(rp, ub, G):
    u = rp.embed_vsafe(ub)
    F = residual_vector(u, G, P, KAP8); Phi = float((F*F).sum())
    out = residuals(G, unpack(u, G), P, KAP8); d = diagnostics(G, out, KAP8)
    return Phi, d


def savepath(NR, NTH, NPS, pc, gauge):
    return f"/tmp/p5c_{NR}_{NTH}_{NPS}_{pc}_{gauge}.pt"


def solve_one(NR, NTH, NPS, pc, gauge, maxit, lsmr_cap):
    print(f"\n===== SOLVE ({NR},{NTH},{NPS}) pc={pc} gauge={gauge} "
          f"newton<={maxit} lsmr<={lsmr_cap} =====", flush=True)
    G = Grid3D(NR, NTH, NPS, rc=0.05, cell=14.0); G = attach_coord_weight(G)
    u0, sol = round_seed(G, p=P, kap8=KAP8)
    edge_ref = u0 if gauge == 'G1' else smooth_edge_bump(G, u0, amp=0.1)
    rp = RP.Repose(G, p=P, m=1, edge_mode='hold', fit_deg=4); rp.set_edge_hold(edge_ref)
    ub0 = rp.extract(u0)
    F0 = residual_vector(rp.embed_vsafe(ub0), G, P, KAP8)
    print(f"  seed Phi0={float((F0*F0).sum()):.3e}  nB={rp.nB}", flush=True)
    t0 = time.time()
    ub, hist, its, wt = PC.jfnk_solve(ub0, rp, u0, KAP8, pc=pc, maxit=maxit,
                                      tol=1e-13, lsmr_maxit=lsmr_cap,
                                      lsmr_tol=1e-13, verbose=True)
    Phi, d = committed(rp, ub, G)
    print(f"  >>> FINAL pc={pc} gauge={gauge}: committed-Phi={Phi:.3e} "
          f"M_MS={d['M_MS']:.6f} tvar={d['tvar']:.4e} newton-its={len(hist)-1} "
          f"lsmr-tot={int(np.sum(its))} wall={time.time()-t0:.0f}s", flush=True)
    torch.save({'NR': NR, 'NTH': NTH, 'NPS': NPS, 'nbr': rp.nbr, 'pc': pc,
                'gauge': gauge, 'ub': ub.cpu(), 'Phi': Phi, 'M_MS': d['M_MS'],
                'tvar': d['tvar']}, savepath(NR, NTH, NPS, pc, gauge))
    print(f"  saved -> {savepath(NR,NTH,NPS,pc,gauge)}", flush=True)


def compare(NR, NTH, NPS, tag1, tag2):
    pc1, g1 = tag1.split('_'); pc2, g2 = tag2.split('_')
    A = torch.load(savepath(NR, NTH, NPS, pc1, g1))
    B = torch.load(savepath(NR, NTH, NPS, pc2, g2))
    nbr = A['nbr']
    ubA, ubB = A['ub'], B['ub']
    diff = (ubB - ubA).reshape(5, nbr, NTH, NPS)
    per = {fields[f]: float(diff[f].abs().max()) for f in range(5)}
    tot = float((ubB - ubA).abs().max())
    dM = abs(B['M_MS'] - A['M_MS']); rel = dM / max(abs(A['M_MS']), 1e-30)
    floored = A['Phi'] < 1e-9 and B['Phi'] < 1e-9
    print(f"\n===== COMPARE ({NR},{NTH},{NPS})  [{tag1}] vs [{tag2}] =====", flush=True)
    print(f"  {tag1}: Phi={A['Phi']:.3e} M_MS={A['M_MS']:.6f} tvar={A['tvar']:.4e}", flush=True)
    print(f"  {tag2}: Phi={B['Phi']:.3e} M_MS={B['M_MS']:.6f} tvar={B['tvar']:.4e}", flush=True)
    print(f"  field-by-field max|diff|={tot:.3e}  " +
          " ".join(f"{k}={v:.2e}" for k, v in per.items()), flush=True)
    print(f"  >>> dM_MS={dM:.3e} (rel {rel*100:.3f}%)  [both floored<1e-9? {floored}]",
          flush=True)


if __name__ == "__main__":
    mode = sys.argv[1]
    NR = int(sys.argv[2])
    NTH = 6 if NR == 12 else 8
    NPS = 8
    t0 = time.time()
    if mode == 'solve':
        pc = sys.argv[3]; gauge = sys.argv[4]
        maxit = int(sys.argv[5]) if len(sys.argv) > 5 else 40
        lsmr_cap = int(sys.argv[6]) if len(sys.argv) > 6 else 600
        solve_one(NR, NTH, NPS, pc, gauge, maxit, lsmr_cap)
    elif mode == 'compare':
        compare(NR, NTH, NPS, sys.argv[3], sys.argv[4])
    else:
        print("unknown mode", mode)
    print(f"=== DONE ({mode} Nr={NR}) total {time.time()-t0:.0f}s ===", flush=True)
