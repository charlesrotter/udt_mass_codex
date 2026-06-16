#!/usr/bin/env python3
"""
gapcloser_axisym_gate.py -- GATE + ROBUSTNESS for the axisymmetric gap-closer.

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  OBSERVE mode.  DATA-BLIND.

(a) GATE: relax the ROUND #56 seed; must HOLD (M_MS~0.281, exterior B=1/A recovered,
    body residuals stay small / down).
(b) ROBUSTNESS: perturb the round seed (l=2 conformal multipole); must RELAX BACK
    (theta-shape of the metric decays, M_MS returns).

The inner body r<rc+rfreeze is regularity-excised (anchored to the round radial seed);
the FREE region is the outer body + all theta -- where shaped/multipole/ring types would
live.  proper-volume weighting + axis excision.  B=1/A FREE.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, time, sys
import torch
import gapcloser_axisym as ax
import radial_Bfree_soliton as rb

torch.set_default_dtype(torch.float64)
DEV = ax.DEV
T, R, TH, PS = 0, 1, 2, 3


def round_seed(G, rc, ri, p=0.4, kap8=0.05):
    rN = rb.make_grid(1, G['Nr'], rc=rc, rint=ri, geom=False)
    o = rb.selfconsistent_Bfree(rN, 1.0, 1.0, p=p, kap8=kap8, iters=300, relax=0.4,
                                tol=1e-11, verbose=False)
    a_r, b_r, Th_r = o['a'][0], o['b'][0], o['Th'][0]
    Nr, Nth = G['Nr'], G['Nth']
    a = a_r[:, None].expand(Nr, Nth).contiguous()
    b = b_r[:, None].expand(Nr, Nth).contiguous()
    c = torch.zeros(Nr, Nth, device=DEV)
    d = torch.zeros(Nr, Nth, device=DEV)
    Th = Th_r[:, None].expand(Nr, Nth).contiguous()
    return a, b, c, d, Th, o['M_MS'].item()


def body_envelope(G, rc, width=1.5):
    rcen = rc + 2.0
    return torch.exp(-((G['rg'][:, None].expand(G['Nr'], G['Nth']) - rcen)/width)**2)


def perturb_multipole(a, b, c, d, G, rc, l=2, amp=0.25):
    """l-th Legendre theta shaping of the metric functions, localized in the body.
    Genuine axisymmetric deformation of the round seed; the solver then relaxes it."""
    env = body_envelope(G, rc)
    ct = torch.cos(G['Tht'][..., 0])
    Pl = {1: ct, 2: 0.5*(3*ct**2-1), 3: 0.5*(5*ct**3-3*ct),
          4: 0.125*(35*ct**4-30*ct**2+3)}[l]
    mod = amp*env*Pl
    return a - 0.5*mod, b.clone(), c + mod, d + mod, None


def exterior_B1A(a, b, G, ri):
    apb = a + b
    jeq = G['Nth']//2
    far = (G['rg'] > ri-4.0) & (G['rg'] < ri-0.5)
    v = apb[far, jeq]
    return v.mean().item(), v.std().item()


def M_MS_readout(b, G, rc):
    """Misner-Sharp mass from g_rr=e^{2b} on the equator: e^{-2b}=1-m/r => m=r(1-e^{-2b}).
    M_MS = m(outer)-m(core).  Equator (jeq) -- in the round case theta-independent."""
    jeq = G['Nth']//2
    m = G['rg']*(1.0 - torch.exp(-2*b[:, jeq]))
    return (m[-3] - m[0]).item()


def theta_shape(a, G, rc):
    """gauge-ish shape measure: theta-variation of a (=ln lapse) in the body, max over r."""
    body = (G['rg'] > rc+1.2) & (G['rg'] < rc+4.0)
    ab = a[body][:, 3:-3]
    return (ab.std(dim=1)/(ab.abs().mean(dim=1)+1e-9)).max().item()


def run(Nr=400, Nth=24, outer=30, rfreeze=1.0, p=0.4, kap8=0.05):
    rc, ri = 0.05, 14.05
    G = ax.mkgrid(Nr, Nth, rc, ri, th0=0.30, th1=math.pi-0.30)
    print(f"# AXISYM GAP-CLOSER GATE  Nr={Nr} Nth={Nth} rfreeze={rfreeze} p={p} kap8={kap8}")
    t0 = time.time()
    a0, b0, c0, d0, Th0, M0 = round_seed(G, rc, ri, p=p, kap8=kap8)
    print(f"# round #56 seed: M_MS={M0:.6f}  ({time.time()-t0:.1f}s)")

    # ---- (a) GATE ----
    print("\n## (a) GATE: relax ROUND seed")
    a, b, c, d, Th, hist = ax.metric_lm_solve(a0, b0, c0, d0, Th0, G, kap8,
                                              outer=outer, rfreeze=rfreeze, mr=2, mth=2,
                                              verbose=True, tag="GATE", w_matter=0.0)
    em, es = exterior_B1A(a, b, G, ri)
    MMS = M_MS_readout(b, G, rc)
    print(f"GATE: M_MS(readout)={MMS:.5f} (seed {M0:.5f})  exterior a+b mean={em:.3e} std={es:.3e}")
    print(f"GATE: theta-shape(a) seed={theta_shape(a0,G,rc):.3e} -> final={theta_shape(a,G,rc):.3e}")
    print(f"GATE: final Phi={hist[-1][2]:.3e} max|F|={hist[-1][3]:.3e}")

    # ---- (b) ROBUSTNESS ----
    print("\n## (b) ROBUSTNESS: PERTURBED (l=2) seed -> relax back")
    ap, bp, cp, dp, _ = perturb_multipole(a0, b0, c0, d0, G, rc, l=2, amp=0.25)
    tv_seed = theta_shape(ap, G, rc)
    a2, b2, c2, d2, Th2, hist2 = ax.metric_lm_solve(ap, bp, cp, dp, Th0.clone(), G, kap8,
                                                    outer=outer, rfreeze=rfreeze, mr=2, mth=2,
                                                    verbose=True, tag="ROBUST", w_matter=0.0)
    MMS2 = M_MS_readout(b2, G, rc)
    tv_final = theta_shape(a2, G, rc)
    # also c-d-theta shape (the genuine warp)
    cd_seed = (cp[(G['rg']>rc+1.2)&(G['rg']<rc+4.0)]).abs().max().item()
    cd_final = (c2[(G['rg']>rc+1.2)&(G['rg']<rc+4.0)]).abs().max().item()
    print(f"ROBUST: M_MS(readout)={MMS2:.5f} (gate {MMS:.5f})")
    print(f"ROBUST: theta-shape(a) seed={tv_seed:.3e} -> final={tv_final:.3e}")
    print(f"ROBUST: |c| body seed={cd_seed:.3e} -> final={cd_final:.3e}")
    print(f"ROBUST: final Phi={hist2[-1][2]:.3e}")
    print(f"\n# total {time.time()-t0:.1f}s")
    return dict(MMS=MMS, MMS2=MMS2, tv_seed=tv_seed, tv_final=tv_final,
                cd_seed=cd_seed, cd_final=cd_final, hist=hist, hist2=hist2)


if __name__ == "__main__":
    Nr = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    Nth = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    outer = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    run(Nr=Nr, Nth=Nth, outer=outer)
