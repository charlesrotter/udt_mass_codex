#!/usr/bin/env python3
"""
gapcloser_axisym_search.py -- THE DISCONNECTED-TYPE SEARCH (axisymmetric).

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  OBSERVE mode.  DATA-BLIND.

Seed MANY qualitatively-different axisymmetric shapes -- multipole (l=1..4),
prolate/oblate, two-center-on-axis, ring/toroidal, large-amplitude -- relax each with
the gauge-fixed nonlinear solver, and CLASSIFY the endpoint:
  * round family  (relaxes back: shape -> 0, M_MS -> round, Phi -> floor)
  * disconnected stable type  (Phi -> floor BUT a GAUGE-INVARIANT shape persists and/or
    M_MS differs at the same charge).
For any candidate we report (i) final Phi (genuine Einstein solution?), (ii) the
gauge-invariant Ricci theta-variation (round=0), (iii) M_MS.

CLASSIFICATION is GAUGE-INVARIANT: the metric functions a,b,c,d can carry pure-gauge
theta-distortion even on a perfectly round geometry (the diagonal-axisymmetric gauge
leaves a residual theta-reparametrization freedom).  The decisive measure is the
theta-variation of the RICCI SCALAR (a true scalar) in the CLEAN interior -- nonzero =>
a genuinely non-round geometry; ~0 => round (regardless of the coordinate shape).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, time, sys
import torch
import gapcloser_axisym as ax
import gapcloser_axisym_gate as gt
import whole_metric_3d_core as core

torch.set_default_dtype(torch.float64)
DEV = ax.DEV
rc, ri = 0.05, 14.05


def ricci_tvar(a, b, c, d, G, r_lo=1.0, r_hi=2.5, edge=6):
    """GAUGE-INVARIANT shape: theta-variation of the Ricci SCALAR in the BODY band where
    R is substantial (r in [rc+r_lo, rc+r_hi]).  Measured RELATIVE to the body-mean |R|
    (a single scale, not pointwise -- avoids the meaningless std/mean blow-up where R~0
    in the exterior).  Round geometry => ~0 (FD floor ~0.005); a genuine non-round shape
    => O(0.1-1)."""
    g = ax.metric_from_abcd(a, b, c, d, G); ginv = core.metric_inverse(g)
    dg = torch.zeros(*g.shape[:-2], 4, 4, 4, device=g.device)
    dg[..., 1, :, :] = ax.d_dx_rt(g, G['hr'], 3); dg[..., 2, :, :] = ax.d_dx_rt(g, G['hth'], 4)
    Gam = core.christoffel(ginv, dg)
    dGam = torch.zeros(*Gam.shape[:-3], 4, 4, 4, 4, device=g.device)
    dGam[..., 1, :, :, :] = ax.d_dx_rt(Gam, G['hr'], 3); dGam[..., 2, :, :, :] = ax.d_dx_rt(Gam, G['hth'], 4)
    _, _, Rs = core.einstein(g, ginv, Gam, dGam)
    body = (G['rg'] > rc+r_lo) & (G['rg'] < rc+r_hi)
    Rb = Rs[body, edge:-edge, 0]
    scale = Rb.abs().mean() + 1e-30
    return (Rb.std(dim=1).max() / scale).item()


def envelope(G, width=1.5):
    rcen = rc + 2.0
    return torch.exp(-((G['rg'][:, None].expand(G['Nr'], G['Nth']) - rcen)/width)**2)


def seeds(a0, b0, c0, d0, Th0, G):
    """Library of qualitatively-different axisymmetric seeds (deformations of round)."""
    env = envelope(G)
    ct = torch.cos(G['Tht'][..., 0]); st = torch.sin(G['Tht'][..., 0])
    out = []
    # multipoles l=1..4 (conformal theta shaping of c,d and counter-shaping of a)
    for l in (1, 2, 3, 4):
        Pl = {1: ct, 2: 0.5*(3*ct**2-1), 3: 0.5*(5*ct**3-3*ct),
              4: 0.125*(35*ct**4-30*ct**2+3)}[l]
        mod = 0.3*env*Pl
        out.append((f"multipole_l{l}", a0-0.5*mod, b0.clone(), c0+mod, d0+mod, Th0.clone()))
    # prolate/oblate: c vs d opposite (genuine spatial quadrupole)
    q = 0.4*env*(ct**2-1.0/3)
    out.append(("prolate_oblate", a0.clone(), b0.clone(), c0+q, d0-q, Th0.clone()))
    # two-center on axis: deepen lapse at both poles
    two = (torch.exp(-((ct-1)/0.5)**2) + torch.exp(-((ct+1)/0.5)**2))
    out.append(("two_center", a0-0.5*0.5*env*two, b0+0.3*0.5*env*two, c0.clone(), d0.clone(),
                Th0*(1+0.2*0.5*env*two)))
    # ring/toroidal: concentrate on equator
    ring = st**4
    out.append(("ring", a0-0.5*0.5*env*ring, b0+0.3*0.5*env*ring, c0.clone(), d0.clone(),
                Th0*(1+0.2*0.5*env*ring)))
    # large amplitude: deepen the whole core well
    envw = envelope(G, width=2.5)
    out.append(("large_amp", a0-0.6*envw, b0+0.6*envw, c0.clone(), d0.clone(), Th0.clone()))
    return out


def classify(name, a, b, c, d, G, Phi, tvar, MMS, M_round, tvar_round, tol_phi):
    solved = Phi < tol_phi
    round_like = (tvar < 3*tvar_round + 1e-3) and (abs(MMS-M_round) < 0.01)
    if not solved:
        return "UNCONVERGED"
    return "ROUND (relaxed back)" if round_like else "DISCONNECTED CANDIDATE"


def run(Nr=160, Nth=24, blocks=8, per=15, rfreeze=1.0):
    G = ax.mkgrid(Nr, Nth, rc, ri, th0=0.30, th1=math.pi-0.30)
    print(f"# AXISYM DISCONNECTED-TYPE SEARCH  Nr={Nr} Nth={Nth} blocks={blocks}x{per} rfreeze={rfreeze}")
    t0 = time.time()
    a0, b0, c0, d0, Th0, M0 = gt.round_seed(G, rc, ri)
    tvar0 = ricci_tvar(a0, b0, c0, d0, G)
    M_round = gt.M_MS_readout(b0, G, rc)
    print(f"# round #56: M_MS={M0:.5f} (readout {M_round:.5f})  Ricci tvar(round)={tvar0:.4f}  ({time.time()-t0:.0f}s)")
    # the gate floor (relax the round seed itself a few blocks) as the Phi tolerance
    print("\n## library search")
    results = []
    for (name, a, b, c, d, Th) in seeds(a0, b0, c0, d0, Th0, G):
        ts = time.time()
        for blk in range(blocks):
            a, b, c, d, Th = ax.metric_lm_solve(a, b, c, d, Th, G, 0.05, outer=per,
                                                cg_iters=40, mu0=1e-3, rfreeze=rfreeze,
                                                verbose=False)[:5]
        g = ax.metric_from_abcd(a, b, c, d, G)
        Res, _, _ = ax.residual_mixed_rt(a, b, c, d, Th, G, 0.05)
        mask, w = ax.make_mask_weight(G, g, rfreeze=rfreeze)
        Phi = ((torch.sqrt(w)[..., None]*Res[..., 0, [0,1,2,3], [0,1,2,3]])**2).sum().item() \
            if False else None
        # recompute Phi consistently with the solver objective
        sw = torch.sqrt(w)
        comps = [Res[..., 0, i, i] for i in range(4)]
        Phi = sum((sw*cc).pow(2).sum().item() for cc in comps)
        tv = ricci_tvar(a, b, c, d, G)
        MMS = gt.M_MS_readout(b, G, rc)
        results.append((name, Phi, tv, MMS, time.time()-ts))
        print(f"  {name:16s}: Phi={Phi:.3e} Ricci_tvar={tv:.4f} M_MS={MMS:.5f} ({time.time()-ts:.0f}s)", flush=True)
    # classify (tol_phi = 10x the round floor estimate)
    print("\n## CLASSIFICATION")
    tol_phi = 5e-3
    for (name, Phi, tv, MMS, dt) in results:
        verdict = classify(name, None, None, None, None, G, Phi, tv, MMS, M_round, tvar0, tol_phi)
        print(f"  {name:16s}: {verdict}  (Phi={Phi:.2e} tvar={tv:.3f} dM={MMS-M_round:+.4f})")
    print(f"\n# total {time.time()-t0:.0f}s")
    return results


if __name__ == "__main__":
    Nr = int(sys.argv[1]) if len(sys.argv) > 1 else 160
    Nth = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    blocks = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    run(Nr=Nr, Nth=Nth, blocks=blocks)
