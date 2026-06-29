#!/usr/bin/env python3
"""PONDER (option 3): characterize the EXISTING saved kap8=1 fields for DIRECT horizon signatures,
BEFORE committing days to an Nr=12 solve. NO solve -- pure diagnostics on saved fields (seconds).

A forming horizon would show as: (i) lapse N=exp(a) dipping toward 0 (infinite-redshift surface);
(ii) radial metric g_rr=exp(2b) blowing up (throat); (iii) compactness 2m/R_areal -> 1 (black-hole
bound), m = Misner-Sharp mass; (iv) a region of LARGE / GROWING curvature (Ricci scalar). We report
the RADIAL PROFILE (angle-averaged) of each + min/max over the body, for:
  - off-ON Nr=8  (fully-floored TRUE-physics anchor)
  - frozen-off Nr=8 and Nr=10  (matched grid-pair: does any signature GROW with refinement?)

This CHARACTERIZES the geometry; it does NOT filter for "horizon" (observe, not target).
"""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch, numpy as np
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
from full3d_spectral import attach_coord_weight, Grid3D, build_metric, einstein_mixed, T, R as RR, TH, PS


def ang_avg(f, G):
    """angle-average a (Nr,Nth,Nps) field over the sphere using the GL theta + uniform phi weights."""
    w = G.wmu[None, :, None] * G.wps[None, None, :]          # sin(th) dth dps
    return (f * w).sum(dim=(1, 2)) / w.sum(dim=(1, 2))


def characterize(path, Nr):
    G = attach_coord_weight(Grid3D(Nr=Nr, Nth=6, Nps=8, rc=0.1, cell=8.0))
    d = torch.load(path, map_location='cpu', weights_only=False)
    u = d['u'].to(G.dev); Xfin = float(d['Xfin'])
    a, b, c, dd, n1, n2, n3, phi, ert, erp, etp = P1.unpack11(u, G)
    r = G.Rg                                                  # areal coordinate r (Nr,Nth,Nps)
    lapse = torch.exp(a)                                      # N = exp(a);  g_tt = -N^2
    grr = torch.exp(2 * b)                                    # radial metric
    R_areal = torch.exp(c) * r                                # sqrt(g_thth) = areal radius
    # Misner-Sharp mass in the spherically-reduced sense: 2m/R = 1 - g^{rr} (d_r R_areal)^2
    # (g^{rr} = exp(-2b); horizon/throat where this -> 1, i.e. d_r R_areal -> 0 in proper length)
    dR = G.d_r(R_areal)
    compactness = 1.0 - torch.exp(-2 * b) * dR**2             # = 2m/R_areal
    # Ricci scalar from the mixed Einstein: G^mu_mu = -R  =>  R = -trace
    g = build_metric(G, a, b, c, dd, e_rt=ert, e_rp=erp, e_tp=etp)
    Gmix = einstein_mixed(G, g)[0]                            # (...,4,4) G^mu_nu (tuple: Gmix,Gmn,ginv,Gamma)
    Ricci = -(Gmix[..., T, T] + Gmix[..., RR, RR] + Gmix[..., TH, TH] + Gmix[..., PS, PS])
    bod = G.body
    rad = ang_avg(r, G).cpu().numpy()
    print(f"\n=== {path}  (Nr={Nr}, Xfin={Xfin:.2e}) ===")
    print(f"  warp max|a,b,c,d|     = {max(float(x.abs().max()) for x in (a,b,c,dd)):.4f}")
    print(f"  lapse N=exp(a):  min(body)={float(lapse[bod].min()):.4f}  max={float(lapse[bod].max()):.4f}   (horizon if ->0)")
    print(f"  g_rr=exp(2b):    max(body)={float(grr[bod].max()):.4f}                       (throat if ->inf)")
    print(f"  compactness 2m/R: max(body)={float(compactness[bod].max()):.4f} min={float(compactness[bod].min()):.4f}  (horizon if ->1)")
    print(f"  Ricci scalar:    max|R|(body)={float(Ricci[bod].abs().max()):.4e}            (singularity if diverges)")
    # angle-averaged radial profiles
    lap_p = ang_avg(lapse, G).cpu().numpy()
    grr_p = ang_avg(grr, G).cpu().numpy()
    cmp_p = ang_avg(compactness, G).cpu().numpy()
    ric_p = ang_avg(Ricci.abs(), G).cpu().numpy()
    print("   r        lapse     g_rr      2m/R      |Ricci|")
    for i in range(Nr):
        print(f"   {rad[i]:6.3f}  {lap_p[i]:8.4f}  {grr_p[i]:8.3f}  {cmp_p[i]:8.4f}  {ric_p[i]:.3e}")
    return dict(r=rad, lapse=lap_p, grr=grr_p, comp=cmp_p, ricci=ric_p,
                comp_max=float(compactness[bod].max()), lap_min=float(lapse[bod].min()),
                ric_max=float(Ricci[bod].abs().max()))


print("###### HORIZON-SIGNATURE CHARACTERIZATION (existing saved fields, no solve) ######")
on8 = characterize('solved_fields_nr8_G_kap8_1.pt', 8)
off8 = characterize('control_offdiagOFF_cold_nr8_G_kap8_1.pt', 8)
off10 = characterize('control_offdiagOFF_cold_nr10_G_kap8_1.pt', 10)

print("\n###### GRID-TREND of the signatures (frozen-off matched pair Nr=8 -> Nr=10) ######")
print(f"  compactness 2m/R max:   Nr=8 {off8['comp_max']:.4f}  ->  Nr=10 {off10['comp_max']:.4f}   (x{off10['comp_max']/off8['comp_max']:.2f})")
print(f"  lapse min:              Nr=8 {off8['lap_min']:.4f}  ->  Nr=10 {off10['lap_min']:.4f}")
print(f"  |Ricci| max:            Nr=8 {off8['ric_max']:.3e}  ->  Nr=10 {off10['ric_max']:.3e}   (x{off10['ric_max']/off8['ric_max']:.2f})")
print(f"  TRUE-physics anchor (off-ON Nr=8): 2m/R max={on8['comp_max']:.4f}, lapse min={on8['lap_min']:.4f}, |Ricci| max={on8['ric_max']:.3e}")
print("\n  READ: compactness ~1 / lapse ->0 / Ricci growing fast with grid => horizon hypothesis ALIVE.")
print("        compactness <<1 / lapse O(1) / Ricci mild+stable           => warp-creep is benign, Nr=12 likely just confirms a plateau.")
