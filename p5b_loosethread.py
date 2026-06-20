#!/usr/bin/env python3
"""
p5b_loosethread.py -- P5b LOOSE THREAD (the decisive gate the P5a' verifier left open):
floor TWO regular edge gauges at Nr=12, 24, 40 and measure whether the cross-gauge
dM_MS spread SHRINKS with Nr.

Driver: Claude (Opus 4.8, 1M).  2026-06-20.  OBSERVE/INFRA.  DATA-BLIND.  Branch p5b-pc-floor.

WHY IT MATTERS (P5a' + verifier): the P5a' "solution-manifold" finding (two regular edge
gauges -> physically distinct floored M_MS, dM_MS~5% at Nr=12) was RULED a coarse-Nr edge
artifact by the verifier (the angular residual is Nth-independent + Nr-convergent in the
interior).  But the verifier could NOT cleanly measure the Nr-DEPENDENCE of the spread
(reposed_dense_solve_fast did not floor at Nr>=16 with a perturbed gauge).  THE RULING
RESTS ON THIS LOOSE THREAD: if the spread SHRINKS with Nr, the artifact ruling holds and
the anchor is resolution-robust; if it does NOT shrink, the manifold question reopens.

THE TWO REGULAR EDGE GAUGES (both smooth/regular; only the unconstrained edge DOF differ):
  G1 = round-seed edges (the #56 radial soliton's edge rows).
  G2 = round-seed edges PERTURBED by a smooth bump on the edge rows (a different but
       equally regular gauge representative).  We use a small smooth radial bump so the
       gauge is genuinely different yet still smooth/regular (NOT random noise, which
       would not be a fair "regular gauge").

We floor BOTH gauges with the P5b PC'd JFNK (the tool the verifier lacked), then compare
the committed-residual physics (M_MS, tvar) at Nr=12, 24, 40.

DISCIPLINE: the edge gauge is the declared 'hold' from p5a'; the perturbation is on the
UNCONSTRAINED edge DOF only (not a physical-DOF freeze).  Both gauges floor the SAME
committed residual; the question is whether the floored PHYSICS depends on the gauge and
whether that dependence vanishes with resolution.  DATA-BLIND.
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


def smooth_edge_bump(G, u0, amp=0.1):
    """Return a copy of u0 with a SMOOTH radial bump added to the EDGE rows only
    (rows {0,1,2,Nr-3,Nr-2,Nr-1}) of the metric warps a,b,c,d -- a different but
    regular edge-gauge representative.  Theta edges are left at BC values (pinned
    anyway).  The bump is a low-order smooth function of r, so the gauge stays
    regular (NOT noise)."""
    Nr = G.Nr
    a, b, c, d, Th = unpack(u0.clone(), G)
    rn = (G.r - G.r.min())/(G.r.max() - G.r.min())          # in [0,1]
    bump = amp*torch.sin(np.pi*rn)                            # smooth, 0 at both ends
    bump = bump[:, None, None]
    edge = torch.zeros(Nr, dtype=torch.bool, device=G.r.device)
    edge[:3] = True; edge[Nr-3:] = True
    em = edge[:, None, None]
    for f in (a, b, c, d):
        f += em*bump
    from full3d_solver import pack
    return pack(a, b, c, d, Th)


def floor_gauge(G, u0, edge_ref, kap8, pc='rband', maxit=120, lsmr_maxit=4000):
    """Floor the committed residual under the 'hold' re-pose with edges held at
    edge_ref, using the PC'd JFNK.  Returns floored committed-Phi + diagnostics."""
    rp = RP.Repose(G, p=P, m=1, edge_mode='hold', fit_deg=4)
    rp.set_edge_hold(edge_ref)
    ub0 = rp.extract(u0)              # body seed from the round soliton (same for both)
    ub, hist, its, wt = PC.jfnk_solve(ub0, rp, u0, kap8, pc=pc, maxit=maxit,
                                      tol=1e-13, lsmr_maxit=lsmr_maxit, lsmr_tol=1e-13,
                                      verbose=False)
    u = rp.embed_vsafe(ub)
    F = residual_vector(u, G, P, kap8); Phi = float((F*F).sum())
    out = residuals(G, unpack(u, G), P, kap8); d = diagnostics(G, out, kap8)
    return Phi, d, len(hist)-1, int(np.sum(its)), wt


if __name__ == "__main__":
    grids = [int(x) for x in (sys.argv[1].split(',') if len(sys.argv) > 1 else
                              ['12', '24', '40'])]
    pc = sys.argv[2] if len(sys.argv) > 2 else 'rband'
    print(f"=== P5b LOOSE THREAD: cross-gauge dM_MS spread vs Nr (pc={pc}) ===", flush=True)
    print("    G1 = round-seed edges ; G2 = round-seed edges + smooth bump", flush=True)
    rows = []
    for NR in grids:
        NTH, NPS = 8, 8
        G = Grid3D(NR, NTH, NPS, rc=0.05, cell=14.0); G = attach_coord_weight(G)
        u0, sol = round_seed(G, p=P, kap8=KAP8)
        eg2 = smooth_edge_bump(G, u0, amp=0.1)
        t0 = time.time()
        Phi1, d1, n1, l1, w1 = floor_gauge(G, u0, u0, KAP8, pc=pc)
        Phi2, d2, n2, l2, w2 = floor_gauge(G, u0, eg2, KAP8, pc=pc)
        dM = abs(d1['M_MS'] - d2['M_MS'])
        relM = dM/max(abs(d1['M_MS']), 1e-30)
        dtv = abs(d1['tvar'] - d2['tvar'])
        print(f"\nNr={NR} (Nth,Nps={NTH},{NPS}):", flush=True)
        print(f"  G1: Phi={Phi1:.2e} (newton {n1}, lsmr-tot {l1}) M_MS={d1['M_MS']:.6f} tvar={d1['tvar']:.4e}", flush=True)
        print(f"  G2: Phi={Phi2:.2e} (newton {n2}, lsmr-tot {l2}) M_MS={d2['M_MS']:.6f} tvar={d2['tvar']:.4e}", flush=True)
        print(f"  >>> cross-gauge dM_MS={dM:.3e} (rel {relM*100:.3f}%) dtvar={dtv:.3e}  "
              f"[both floored? {Phi1<1e-9 and Phi2<1e-9}]  ({time.time()-t0:.0f}s)", flush=True)
        rows.append((NR, Phi1, Phi2, d1['M_MS'], d2['M_MS'], dM, relM, dtv))
    print("\n=== SPREAD-vs-Nr SUMMARY ===", flush=True)
    print("  Nr   floored?      dM_MS        rel%       dtvar", flush=True)
    for (NR, P1, P2, M1, M2, dM, relM, dtv) in rows:
        fl = "yes" if (P1 < 1e-9 and P2 < 1e-9) else f"NO(P={max(P1,P2):.1e})"
        print(f"  {NR:<4} {fl:<12} {dM:.3e}    {relM*100:7.3f}   {dtv:.3e}", flush=True)
    if len(rows) >= 2:
        shrink = all(rows[i+1][5] < rows[i][5] for i in range(len(rows)-1))
        print(f"\n  SPREAD SHRINKS MONOTONICALLY WITH Nr: {shrink}", flush=True)
        print(f"  (Nr={rows[0][0]} dM={rows[0][5]:.3e} -> Nr={rows[-1][0]} dM={rows[-1][5]:.3e}, "
              f"ratio {rows[0][5]/max(rows[-1][5],1e-30):.1f}x)", flush=True)
    print("\n=== LOOSE THREAD DONE ===", flush=True)
