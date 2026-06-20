#!/usr/bin/env python3
"""
p5c_dense.py -- P5c-step-1 DENSE path: SVD-at-seed conditioning + dense-LM floor.

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  OBSERVE/INFRA.  DATA-BLIND.
Branch: p5c-uniqueness.  NEW FILE (reuses committed p5a'/full3d as imports).

WHY: the matrix-free LSMR JFNK does NOT floor at Nr>=16 inside the anti-hang
single-process budget on this contended box (inner LSMR never converges below cap;
~50 s/Newton-iter, ~20 iters needed -> ~1000 s).  The DENSE LM path
(reposed_dense_solve_fast: jacrev Jacobian + torch.linalg.lstsq) solves the inner
system EXACTLY (no Krylov cap), so it floors in far fewer Newton iters -- and lstsq
is the rank-revealing solver, so it lands on the MINIMUM-NORM point of any near-null
valley (a single well-defined readout, gauge-fixed by min-norm).  This is the right
tool to settle whether the floored M_MS is resolution-robust.

It also runs the §0 SVD-at-seed conditioning (svdvals of the dense reposed J at the
round seed) -- the direct measure of whether the non-uniqueness-causing near-null
edge mode SURVIVES at Nr>=16 (the P5b §0 prediction: it vanishes, kappa drops).

ANTI-HANG: SINGLE clean process; dense lstsq capped at maxit Newton; svdvals is
seconds.  Each invocation does ONE thing.

USAGE:
  python3 p5c_dense.py svd  NR              # conditioning of reposed J at seed
  python3 p5c_dense.py floor NR GAUGE [MAXIT]   # dense-LM floor, save M_MS (G1/G2)
  python3 p5c_dense.py cmp  NR              # load saved G1/G2 dense floors -> dM_MS
"""
import os, sys, time
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")  # dense jacrev path
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight, residuals, diagnostics
from full3d_solver import residual_vector, round_seed, unpack
import p5a_prime_repose as RP
from p5b_loosethread import smooth_edge_bump

P, KAP8 = 0.4, 0.05
fields = ['a', 'b', 'c', 'd', 'Th']


def grid(NR):
    NTH = 6 if NR == 12 else 8
    NPS = 8
    G = Grid3D(NR, NTH, NPS, rc=0.05, cell=14.0); G = attach_coord_weight(G)
    u0, sol = round_seed(G, p=P, kap8=KAP8)
    return G, u0, NTH, NPS


def svd(NR):
    G, u0, NTH, NPS = grid(NR)
    rp = RP.Repose(G, p=P, m=1, edge_mode='hold', fit_deg=4); rp.set_edge_hold(u0)
    ub0 = rp.extract(u0)
    t0 = time.time()
    J, F = RP.reposed_jacobian_jacrev(ub0, rp, KAP8)
    S = torch.linalg.svdvals(J)
    smax, smin = float(S[0]), float(S[-1])
    kap = smax / smin
    nsmall = int((S < 1e-3 * smax).sum())
    # near-null direction localization: right-singular vector of smallest SV
    U, Sv, Vh = torch.linalg.svd(J, full_matrices=False)
    v = Vh[-1].reshape(5, rp.nbr, NTH, NPS)
    perfield = {fields[f]: float((v[f]**2).sum()) for f in range(5)}  # power fraction
    tot = sum(perfield.values())
    perfield = {k: vv / tot for k, vv in perfield.items()}
    print(f"  SVD reposed-J ({NR}): nB={rp.nB} kappa={kap:.3e} smax={smax:.3e} "
          f"smin={smin:.3e} 2nd-smallest={float(S[-2]):.3e} "
          f"#SV<1e-3smax={nsmall}  ({time.time()-t0:.0f}s)", flush=True)
    print(f"    near-null dir power: " +
          " ".join(f"{k}={v*100:.0f}%" for k, v in perfield.items()) +
          f"  (Theta={perfield['Th']*100:.1f}%)", flush=True)
    return dict(NR=NR, kappa=kap, smin=smin, nsmall=nsmall, perfield=perfield)


def floor(NR, gauge, maxit):
    G, u0, NTH, NPS = grid(NR)
    edge_ref = u0 if gauge == 'G1' else smooth_edge_bump(G, u0, amp=0.1)
    rp = RP.Repose(G, p=P, m=1, edge_mode='hold', fit_deg=4); rp.set_edge_hold(edge_ref)
    ub0 = rp.extract(u0)
    t0 = time.time()
    ub, hist = RP.reposed_dense_solve_fast(ub0, rp, KAP8, maxit=maxit, tol=1e-13,
                                           verbose=True)
    u = rp.embed_vsafe(ub)
    F = residual_vector(u, G, P, KAP8); Phi = float((F*F).sum())
    out = residuals(G, unpack(u, G), P, KAP8); d = diagnostics(G, out, KAP8)
    print(f"  DENSE-FLOOR ({NR},{gauge}): committed-Phi={Phi:.3e} M_MS={d['M_MS']:.6f} "
          f"tvar={d['tvar']:.4e} newton-its={len(hist)-1} wall={time.time()-t0:.0f}s",
          flush=True)
    torch.save({'NR': NR, 'NTH': NTH, 'NPS': NPS, 'nbr': rp.nbr, 'gauge': gauge,
                'ub': ub.cpu(), 'Phi': Phi, 'M_MS': d['M_MS'], 'tvar': d['tvar']},
               f"/tmp/p5c_dense_{NR}_{gauge}.pt")


def cmp(NR):
    A = torch.load(f"/tmp/p5c_dense_{NR}_G1.pt")
    B = torch.load(f"/tmp/p5c_dense_{NR}_G2.pt")
    nbr = A['nbr']; NTH = A['NTH']; NPS = A['NPS']
    diff = (B['ub'] - A['ub']).reshape(5, nbr, NTH, NPS)
    per = {fields[f]: float(diff[f].abs().max()) for f in range(5)}
    tot = float((B['ub'] - A['ub']).abs().max())
    dM = abs(B['M_MS'] - A['M_MS']); rel = dM / max(abs(A['M_MS']), 1e-30)
    floored = A['Phi'] < 1e-9 and B['Phi'] < 1e-9
    print(f"  DENSE CROSS-GAUGE ({NR}): G1 Phi={A['Phi']:.2e} M_MS={A['M_MS']:.6f} | "
          f"G2 Phi={B['Phi']:.2e} M_MS={B['M_MS']:.6f}", flush=True)
    print(f"    field max|diff|={tot:.3e}  " +
          " ".join(f"{k}={v:.2e}" for k, v in per.items()), flush=True)
    print(f"    >>> dM_MS={dM:.3e} (rel {rel*100:.3f}%)  [both floored<1e-9? {floored}]",
          flush=True)


if __name__ == "__main__":
    mode = sys.argv[1]; NR = int(sys.argv[2])
    t0 = time.time()
    if mode == 'svd':
        svd(NR)
    elif mode == 'floor':
        gauge = sys.argv[3]; maxit = int(sys.argv[4]) if len(sys.argv) > 4 else 25
        floor(NR, gauge, maxit)
    elif mode == 'cmp':
        cmp(NR)
    print(f"=== DONE ({mode} {NR}) {time.time()-t0:.0f}s ===", flush=True)
