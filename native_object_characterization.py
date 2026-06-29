#!/usr/bin/env python3
"""NATIVE characterization of the dense static kap8=1 object (OBSERVE, no solve, saved fields only).
Reads the object in UDT's OWN variables (NOT GR's horizon lens):
  1. DILATION well phi(r)        -- UDT's primitive; depth/shape of the positional-dilation well.
  2. REDSHIFT e^phi across cell  -- canon 1+z=e^phi (the native reading of the "lapse").
  3. WINDING DEFECT distribution -- matter energy density radial profile: LOCALIZED lump vs SPREAD
                                    scale-free defect.  Test: does public charge m(r) grow LINEARLY
                                    (global-monopole / scale-free defect) or SATURATE (localized)?
  4. AREAL law rho=r             -- canon theorem; check exp(c)~1 (areal radius = coordinate radius).
  5. PUBLIC CHARGE m(r)          -- canon Misner-Sharp mass = cell public charge (NOT 2m/R-horizon).
  6. PROPER SIZE                 -- proper radial distance int exp(b) dr; native geometric extent.
Primary = off-ON Nr=8 (floored). Frozen-off Nr=8/10 only for grid-trend hints (Nr=10 under-floored).
"""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch, numpy as np
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
import free_s2_matter as S2M
import whole_metric_3d_matter as MAT
from full3d_spectral import attach_coord_weight, Grid3D, build_metric, T, R as RR, TH, PS
from full3d_newton import inv4x4


def ang_avg(f, G):
    w = G.wmu[None, :, None] * G.wps[None, None, :]
    return (f * w).sum(dim=(1, 2)) / w.sum(dim=(1, 2))


def characterize(path, Nr):
    G = attach_coord_weight(Grid3D(Nr=Nr, Nth=6, Nps=8, rc=0.1, cell=8.0))
    d = torch.load(path, map_location='cpu', weights_only=False)
    u = d['u'].to(G.dev); Xfin = float(d['Xfin'])
    a, b, c, dd, n1, n2, n3, phi, ert, erp, etp = P1.unpack11(u, G)
    r = G.Rg
    n_raw = torch.stack([n1, n2, n3], dim=-1)
    dn = S2M.field_dn_components_exact(G, n_raw)
    g = build_metric(G, a, b, c, dd, e_rt=ert, e_rp=erp, e_tp=etp); ginv = inv4x4(g)
    Tab, _, _, _ = MAT.stress_tensor(g, ginv, dn, 1.0, 1.0)
    rho = -torch.einsum('...ma,...an->...mn', ginv, Tab)[..., T, T]      # matter energy density

    R_areal = torch.exp(c) * r
    dR = G.d_r(R_areal)
    m_of_r = 0.5 * R_areal * (1.0 - torch.exp(-2 * b) * dR**2)           # Misner-Sharp = public charge

    # radial profiles (angle-averaged)
    rad   = ang_avg(r, G).cpu().numpy()
    phi_p = ang_avg(phi, G).cpu().numpy()
    a_p   = ang_avg(a, G).cpu().numpy()
    b_p   = ang_avg(b, G).cpu().numpy()
    c_p   = ang_avg(c, G).cpu().numpy()
    ezp   = ang_avg(torch.exp(phi), G).cpu().numpy()                     # redshift factor e^phi
    rho_p = ang_avg(rho, G).cpu().numpy()
    m_p   = ang_avg(m_of_r, G).cpu().numpy()
    # CLEAN energy-charge (no noisy d_r): dE/dr = int rho*sqrt(det g_spatial) dth dps; E(<r)=cumsum.
    # (replaces the spectral-ringing-contaminated Misner-Sharp m(r); see verifier a9efe4b 2026-06-29.)
    gs = g[..., 1:, 1:]                                                  # spatial 3x3 (exact, incl off-diag)
    sqrtg = torch.sqrt(torch.clamp(torch.linalg.det(gs), min=0.0))
    dEdr = ((rho * sqrtg) * (G.wmu[None, :, None] * G.wps[None, None, :])).sum(dim=(1, 2))  # (Nr,)
    Ecum = np.cumsum((dEdr * G.wr).cpu().numpy())
    eshell = (dEdr * G.wr).cpu().numpy()
    # proper radial distance core->seal
    Lproper = float((ang_avg(torch.exp(b), G) * G.wr).sum()) if hasattr(G, 'wr') else None

    print(f"\n=== {path}  (Nr={Nr}, Xfin={Xfin:.2e}) ===")
    print(f"  DILATION phi:  range [{phi_p.min():.4f}, {phi_p.max():.4f}]   (deepest |phi|={np.abs(phi_p).max():.4f})")
    print(f"  REDSHIFT e^phi: core={ezp[0]:.4f}  seal={ezp[-1]:.4f}  ratio(core/seal)={ezp[0]/ezp[-1]:.4f}")
    print(f"  AREAL exp(c):  range [{np.exp(c_p).min():.4f}, {np.exp(c_p).max():.4f}]   (rho=r holds if ~1)")
    print(f"  PUBLIC CHARGE m(r): m(seal)={m_p[-1]:.4f}   m(mid)={m_p[Nr//2]:.4f}")
    print(f"  proper radial distance core->seal = {Lproper}")
    print("   r        phi       e^phi     a(lapse)  b(g_rr/2) exp(c)    rho_mat   m(r)      E/shell")
    for i in range(Nr):
        print(f"   {rad[i]:6.3f}  {phi_p[i]:8.4f}  {ezp[i]:8.4f}  {a_p[i]:8.4f}  {b_p[i]:8.4f}  "
              f"{np.exp(c_p[i]):8.4f}  {rho_p[i]:8.4f}  {m_p[i]:8.4f}  {eshell[i]:.3e}")
    # CLEAN scale-free-defect test: is E(<r)/r CONSTANT (E ~ k*r, scale-free defect) or FALLING
    # (core-concentrated)?  Plus: does E(<r) SATURATE (localized lump)?  Interior shells only.
    sl = slice(1, Nr - 1)
    EoverR = Ecum[sl] / rad[sl]
    print(f"  CLEAN energy-charge E(<r): inner={Ecum[sl][0]:.2f} outer={Ecum[sl][-1]:.2f} "
          f"(rising => not localized); E/r drift {EoverR[0]:.1f} -> {EoverR[-1]:.1f} "
          f"(CONSTANT => scale-free defect; FALLING => core-concentrated)")
    return dict(rad=rad, Ecum=Ecum, EoverR=EoverR, rho=rho_p, phi=phi_p)


print("###### NATIVE CHARACTERIZATION (UDT variables; no GR horizon lens) ######")
on8  = characterize('solved_fields_nr8_G_kap8_1.pt', 8)
off8 = characterize('control_offdiagOFF_cold_nr8_G_kap8_1.pt', 8)
off10= characterize('control_offdiagOFF_cold_nr10_G_kap8_1.pt', 10)

print("\n###### NATIVE GRID-TREND (frozen-off matched pair; Nr=10 UNDER-FLOORED, soft) ######")
print(f"  dilation depth max|phi|:   Nr=8 {np.abs(off8['phi']).max():.4f}  ->  Nr=10 {np.abs(off10['phi']).max():.4f}")
print(f"  TRUE-physics anchor (off-ON Nr=8): max|phi| = {np.abs(on8['phi']).max():.4f}")
print("\n  READ (Nr=8, scoped): gentle-phi + core-concentrated winding (E/r FALLS, not constant) => a")
print("    CORE-CONCENTRATED WINDING DEFECT -- NOT a forming horizon, NOT a localized lump, and NOT a clean")
print("    scale-free monopole (E/r not constant). Quantitative defect law + grid-stability OPEN (phi may")
print("    deepen ~6x on the soft Nr=10; needs a properly-floored finer grid).")
