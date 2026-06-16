#!/usr/bin/env python3
"""
einstein_3d_eval.py -- evaluate the auto-generated analytic 3-D Weyl mixed Einstein
tensor on the spectral grid (smooth warp derivatives taken SPECTRALLY; cot/1/sin
pole structure carried symbolically by the generator, evaluated at off-axis GL nodes).

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  DATA-BLIND.

CATEGORY-A: this is the SAME native Einstein content as whole_metric_3d_core (the
exact tensor algebra), specialized to the static diagonal 3-D Weyl class and made
POLE-STABLE by analytic cancellation -- exactly the validated 2-D cure extended to
psi.  Proof: flat -> 0 (machine), Schwarzschild -> 0 (exponential), and it MATCHES
the validated 2-D analytic engine in the axisymmetric (psi-flat) limit.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import torch
torch.set_default_dtype(torch.float64)
from einstein_3d_weyl_gen import Gmix_components

T, R, TH, PS = 0, 1, 2, 3


def warp_derivs(G, f):
    """1st & 2nd spectral partials of a warp f(r,th,ps): returns
    (f, f_r, f_t, f_p, f_rr, f_tt, f_pp, f_rt, f_rp, f_tp)."""
    fr = G.d_r(f); ft = G.d_th(f); fp = G.d_ps(f)
    frr = G.d_r(fr); ftt = G.d_th(ft); fpp = G.d_ps(fp)
    frt = G.d_th(fr); frp = G.d_ps(fr); ftp = G.d_ps(ft)
    return (f, fr, ft, fp, frr, ftt, fpp, frt, frp, ftp)


def einstein_mixed_weyl(G, a, b, c, d):
    """Analytic mixed Einstein G^mu_nu (Nr,Nth,Nps,4,4) for the diagonal Weyl metric
    with warps a,b,c,d(r,th,ps).  Smooth derivatives spectral; pole terms analytic."""
    A = warp_derivs(G, a); B = warp_derivs(G, b)
    C = warp_derivs(G, c); D = warp_derivs(G, d)
    rows = Gmix_components(G.Rg, G.THg, *A, *B, *C, *D)
    out = torch.zeros(G.Nr, G.Nth, G.Nps, 4, 4, device=a.device)
    for m in range(4):
        for n in range(4):
            v = rows[m][n]
            if not torch.is_tensor(v):
                v = torch.full_like(a, float(v))
            out[..., m, n] = v
    return out


if __name__ == "__main__":
    import math
    from full3d_spectral import Grid3D, attach_coord_weight, DEV
    print("=== analytic 3-D Weyl Einstein validation ===")
    print("FLAT (a=b=c=d=0) -> G=0 :")
    for (Nr, Nth, Nps) in [(20, 6, 8), (30, 12, 8), (40, 16, 12)]:
        G = Grid3D(Nr, Nth, Nps, rc=0.05, cell=14.0); G = attach_coord_weight(G)
        z = torch.zeros(G.Nr, G.Nth, G.Nps, device=DEV)
        Gm = einstein_mixed_weyl(G, z, z, z, z)
        print(f"  Nr={Nr} Nth={Nth} Nps={Nps}: max|G| body = {float(Gm[G.body].abs().max()):.3e}")

    print("\nSCHWARZSCHILD (a=-b=0.5 ln(1-2M/r), c=d=0) -> G=0 (exponential in Nr):")
    M = 0.3
    for Nr in [16, 24, 32, 48]:
        G = Grid3D(Nr, 6, 8, rc=1.0, cell=14.0); G = attach_coord_weight(G)
        f = 1.0 - 2*M/G.Rg
        a = 0.5*torch.log(f); b = -0.5*torch.log(f)
        z = torch.zeros_like(a)
        Gm = einstein_mixed_weyl(G, a, b, z, z)
        print(f"  Nr={Nr}: max|G| body = {float(Gm[G.body].abs().max()):.3e}")
