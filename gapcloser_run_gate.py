#!/usr/bin/env python3
"""
gapcloser_run_gate.py -- VALIDATION GATE + ROBUSTNESS double-check for the gap-closer.

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  OBSERVE mode.  DATA-BLIND.

(a) GATE: from a ROUND seed (#56 soliton on the grid) the gauge-fixed nonlinear solver
    must HOLD the soliton: M_MS ~ 0.281, exterior B=1/A (a+b -> 0) recovered as a RESULT,
    Einstein body residuals stay small / converge, gauge proven non-restrictive (the
    round soliton is a fixed point of the reference-gauge solve).
(b) ROBUSTNESS: from a PERTURBED/deformed round seed the solver must RELAX BACK to the
    round soliton (same M_MS, perturbation decays) without wandering into gauge
    directions.

Reuses the validated engines (whole_metric_3d_core/matter/solver) and the gauge-fixed
Gauss-Newton (gapcloser_solver) + seed library (gapcloser_seeds).  NO physics patch:
B=1/A FREE, no seal/source injection, reference-coordinate gauge only.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, time, sys
import torch
import whole_metric_3d_solver as S
import gapcloser_seeds as seeds
import gapcloser_solver as gs

torch.set_default_dtype(torch.float64)
DEV = "cuda" if torch.cuda.is_available() else "cpu"
T, R, TH, PS = 0, 1, 2, 3


def exterior_B1A(g, G, rc, ri):
    """a+b in the exterior (unwound) region.  a = (1/2)ln(-g_tt), b=(1/2)ln(g_rr).
    B=1/A  <=>  a+b -> 0 in the exterior.  Returns mean,std of a+b on the equator far field."""
    a = 0.5*torch.log((-g[..., T, T]).clamp(min=1e-30))
    b = 0.5*torch.log((g[..., R, R]).clamp(min=1e-30))
    apb = a + b
    jeq = G['Nth']//2
    far = (G['rg'] > ri - 4.0) & (G['rg'] < ri - 0.5)
    vals = apb[far, jeq, 0]
    return vals.mean().item(), vals.std().item(), apb


def body_apb_max(g, G, rc):
    a = 0.5*torch.log((-g[..., T, T]).clamp(min=1e-30))
    b = 0.5*torch.log((g[..., R, R]).clamp(min=1e-30))
    apb = a + b
    body = (G['rg'] > rc+0.3) & (G['rg'] < rc+3.0)
    return apb[body].abs().max().item()


def run(Nr=320, Nth=24, Nps=8, p=0.4, kap8=0.05, outer=25, w_gauge=0.3):
    rc, ri = 0.05, 14.05
    th0, th1 = 0.30, math.pi-0.30
    G = S.mkgrid(Nr, Nth, Nps, rc, ri, th0, th1)
    print(f"# GAP-CLOSER GATE  grid Nr={Nr} Nth={Nth} Nps={Nps}  p={p} kap8={kap8} w_gauge={w_gauge}")
    t0 = time.time()
    g_round, Th_round, info = seeds.round_seed(G, rc, ri, p=p, kap8=kap8)
    print(f"# round #56 seed: M_MS={info['M_MS']:.6f}  ({time.time()-t0:.1f}s)")

    free = [(T,T),(R,R),(TH,TH),(PS,PS),(T,R),(T,TH),(T,PS),(R,TH),(R,PS),(TH,PS)]
    bc_core = math.pi; bc_seal = 0.0

    # reference gauge frame = the round seed coordinate frame (areal); FROZEN.
    Href, _ = gs.harmonic_gauge(g_round, G)
    Href = Href.detach()

    # ---- (a) GATE: relax the round seed itself ----
    print("\n## (a) GATE: relax ROUND seed (should HOLD)")
    out = gs.solve(g_round, Th_round, kap8, G, free, bc_core, bc_seal,
                   outer=outer, mu=1e-3, cg_iters=40, mask_core=1.0, rfreeze=1.0,
                   w_gauge=w_gauge, matter_steps=4, mr=3, mth=3, verbose=True,
                   tag="GATE", H_ref=Href)
    g_g = out['g']; Th_g = out['Th']
    n_g = S.hedgehog_field(Th_g, G)
    d = gs.body_diagnostics(g_g, n_g, kap8, G, mask_core=1.0, mth_strip=4)
    m, Rar = gs.mass_readout(g_g, G, mask_core=1.0)
    em, es, _ = exterior_B1A(g_g, G, rc, ri)
    print(f"GATE result: body diag={d['rdiag']:.3e} off={d['roff']:.3e} H_dev={d['hmax']:.3e}")
    print(f"GATE M(readout)={m:.5f}  exterior a+b mean={em:.3e} std={es:.3e}  body|a+b|max={body_apb_max(g_g,G,rc):.3e}")

    # ---- (b) ROBUSTNESS: perturb round seed, relax back ----
    print("\n## (b) ROBUSTNESS: PERTURBED seed (should RELAX BACK to round)")
    g_pert, Th_pert, lbl = seeds.seed_multipole(G, g_round, Th_round, rc, l=2, amp=0.25)
    # gauge-invariant perturbation measure: psi/theta variation of Ricci scalar
    out2 = gs.solve(g_pert, Th_pert, kap8, G, free, bc_core, bc_seal,
                    outer=outer, mu=1e-3, cg_iters=40, mask_core=1.0, rfreeze=1.0,
                    w_gauge=w_gauge, matter_steps=4, mr=3, mth=3, verbose=True,
                    tag="ROBUST", H_ref=Href)
    g_r = out2['g']; Th_r = out2['Th']
    n_r = S.hedgehog_field(Th_r, G)
    d2 = gs.body_diagnostics(g_r, n_r, kap8, G, mask_core=1.0, mth_strip=4)
    m2, _ = gs.mass_readout(g_r, G, mask_core=1.0)
    # shape measure: theta-variation of g_tt at fixed r (body), seed vs final
    def theta_var(g):
        a = 0.5*torch.log((-g[..., T, T]).clamp(min=1e-30))
        body=(G['rg']>rc+0.3)&(G['rg']<rc+2.5)
        ab=a[body][:,3:-3,0]
        return (ab.std(dim=1)/(ab.abs().mean(dim=1)+1e-12)).max().item()
    tv_seed=theta_var(g_pert); tv_final=theta_var(g_r)
    print(f"ROBUST result: body diag={d2['rdiag']:.3e} off={d2['roff']:.3e}")
    print(f"ROBUST M(readout)={m2:.5f} (gate {m:.5f})  theta-var g_tt: seed={tv_seed:.3e} -> final={tv_final:.3e}")
    print(f"\n# total {time.time()-t0:.1f}s")
    return dict(gate=out, robust=out2, m_gate=m, m_robust=m2, tv_seed=tv_seed, tv_final=tv_final)


if __name__ == "__main__":
    Nr = int(sys.argv[1]) if len(sys.argv)>1 else 320
    Nth = int(sys.argv[2]) if len(sys.argv)>2 else 24
    outer = int(sys.argv[3]) if len(sys.argv)>3 else 25
    run(Nr=Nr, Nth=Nth, outer=outer)
