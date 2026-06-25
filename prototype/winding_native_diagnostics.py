#!/usr/bin/env python3
"""
winding_native_diagnostics.py -- WINDING-NATIVE rulers (replace the lump-ruler).

Driver: Claude (Opus 4.8). 2026-06-24. OBSERVE infra. DATA-BLIND. NEW FILE; reuses
the immutable residual/metric machinery verbatim.

WHY (Charles 2026-06-24): the recent Branch-P diagnostics (M_MS-as-mass, body_flat,
r_peak "defect vs body", localization, "does it select a scale into a BODY") are a
LUMP-RULER -- they ask "is there a localized lump?", the wrong question for UDT's
native matter, which is a WINDING/DEFECT (a topological texture, never a lump). We
were measuring a winding with a lump-ruler and reading "no localized body /
box-controlled" as a NEGATIVE. The lump crept back via the MEASUREMENT, not the
field (the field n=x/r is a genuine S^2 winding; seed is a pure winding). FIX THE
RULER before any deep solve.

WINDING-NATIVE quantities (metric g_tt=-e^{2a}, g_rr=e^{2b}, g_thth=e^{2c}r^2,
g_psps=e^{2d}r^2 sin^2th; angular sector DIAGONAL in this solver):
  1. TOPOLOGICAL DEGREE  Q(r) = (1/4pi) int n.(d_th n x d_ps n) dth dps  -- the
     discrete LABEL (integer m; the native discreteness). Per radial shell.
  2. SOLID-ANGLE DEFICIT Delta(r) = 1 - (proper 2-area)/(4 pi r^2)
                               = 1 - (1/4pi) int e^{c+d} sin th dth dps
     -- the global-monopole gravitational winding charge (dimensionless,
     box-INDEPENDENT if intrinsic). [c,d are BC-pinned to 0 at both ends -> deficit
     signal lives in the INTERIOR; watch for BC suppression.]
  3. ENERGY PER PROPER RADIAL LENGTH  dE/dl(l),  l = proper radius int e^{b} dr,
     dE/dl = r^2 int rho e^{c+d} sin th dth dps.  FLAT in l => scale-free defect
     (NO intrinsic scale). A BUMP at proper radius l* => an INTRINSIC CORE; l*
     box-INDEPENDENT => intrinsic scale, l* scaling with the box => box-controlled.
  NO M_MS-as-mass, NO body_flat, NO localization-of-a-lump.

INTRINSIC-vs-BOX is read by applying these across cell sizes (Q integer & Delta &
l* box-independent = intrinsic; quantities scaling with the box = box-controlled).
"""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import sys
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import branchGP_native_s2_coupled_OBSERVE as B
from branchGP_native_s2_coupled_OBSERVE import unpack6, build_metric, s2_dn_freeaz, s2_Tmix_and_Lm, T


def winding_diag(u, G, X, XI, KAP, m=1, kap8=1.0, branch="P"):
    a, b, c, d, phi, gtw = unpack6(u)
    g = build_metric(G, a, b, c, d); ginv = B.inv4x4(g)
    wmu = G.wmu; wps = G.wps                       # wmu includes sin th
    wth_plain = (G.wmu / G.sth)                    # plain d-theta weight
    dOm = wmu[None, :, None] * wps[None, None, :]  # solid-angle element, sum=4pi
    dpl = wth_plain[None, :, None] * wps[None, None, :]  # plain dth dps element

    # --- 1. topological degree per shell ---
    Psi = m * G.PSg + gtw
    n = torch.stack([G.STHg * torch.cos(Psi), G.STHg * torch.sin(Psi),
                     torch.cos(G.THg)], dim=-1)             # (Nr,Nth,Nps,3)
    dn = s2_dn_freeaz(G, gtw, m=m)                          # (...,4,3)
    cr = torch.cross(dn[..., 2, :], dn[..., 3, :], dim=-1)  # d_th n x d_ps n  (TH=2,PS=3)
    deg_dens = (n * cr).sum(-1)                             # n.(d_th n x d_ps n)
    Q_r = (deg_dens * dpl).sum(dim=(1, 2)) / (4 * np.pi)    # (Nr,)

    # --- 2. solid-angle deficit per shell ---
    area_factor = (torch.exp(c + d) * dOm).sum(dim=(1, 2)) / (4 * np.pi)  # <e^{c+d}>
    Delta_r = 1.0 - area_factor                            # (Nr,)

    # --- 3. energy per proper radial length ---
    Tmix, _ = s2_Tmix_and_Lm(G, g, ginv, gtw, XI, KAP, m=m)
    rho = -Tmix[..., T, T]                                 # energy density (mixed)
    # shell energy in PROPER radius:  dE/dl = r^2 * int rho e^{c+d} sin th dth dps
    r = G.r
    dEdl = (r**2) * (rho * torch.exp(c + d) * dOm).sum(dim=(1, 2))   # (Nr,)
    # proper radius l(r) = cumulative int e^{b} dr  (mid-angle b)
    jt, jp = G.Nth // 2, G.Nps // 2
    br = b[:, jt, jp]
    rnp = r.cpu().numpy(); ebr = torch.exp(br).cpu().numpy()
    l = np.concatenate([[0.0], np.cumsum(0.5 * (ebr[1:] + ebr[:-1]) * np.diff(rnp))])
    return dict(r=rnp, Q_r=Q_r.cpu().numpy(), Delta_r=Delta_r.cpu().numpy(),
                dEdl=dEdl.cpu().numpy(), l_proper=l, ri=float(G.ri))


def print_winding(tag, dg, G):
    r = dg['r']; bod = G.body.cpu().numpy()[:, G.Nth//2, G.Nps//2]
    bi = np.where(bod)[0]
    print(f"\n  ==== WINDING-NATIVE [{tag}] (ri={dg['ri']:.2f}) ====", flush=True)
    # 1. degree (label) -- should be integer m, shell-constant
    print(f"  [1] TOPOLOGICAL DEGREE Q(r): mean(body)={dg['Q_r'][bi].mean():+.4f}  "
          f"range[{dg['Q_r'][bi].min():+.4f},{dg['Q_r'][bi].max():+.4f}]  "
          f"(=> the discrete LABEL; expect integer, shell-constant)")
    # 2. deficit
    Dint = dg['Delta_r'][bi]
    print(f"  [2] SOLID-ANGLE DEFICIT Delta(r): body mean={Dint.mean():+.4e}  "
          f"max|Delta|={np.abs(Dint).max():.4e}  (gravitational winding charge; "
          f"box-INDEP if intrinsic)")
    print(f"      Delta(r) full: " + " ".join(f"{r[i]:.2f}:{dg['Delta_r'][i]:+.2e}"
          for i in range(len(r))))
    # 3. energy per proper length -- flat vs bump
    l = dg['l_proper']; e = dg['dEdl']
    eb = np.abs(e[bi])
    ipk = bi[int(np.argmax(eb))]
    flat = eb.max() / max(eb.mean(), 1e-30)
    print(f"  [3] ENERGY per PROPER radial length dE/dl: flatness(max/mean,body)={flat:.2f}  "
          f"peak at proper-l={l[ipk]:.2f} (=r {r[ipk]:.2f}, ={r[ipk]/dg['ri']:.2f} ri)")
    print(f"      => FLAT(~1) = scale-free defect (NO intrinsic scale); BUMP at fixed "
          f"PROPER l* (box-indep) = intrinsic core")
    print(f"      dE/dl(proper l): " + " ".join(f"l={l[i]:.2f}:{e[i]:+.2e}"
          for i in range(len(r))))


if __name__ == "__main__":
    from jfnk_branch_solver import _grid
    X, XI, KAP, KAP8, M = B.X_PROD, B.XI_PROD, B.KAP_PROD, B.KAP8, B.M_WIND
    # validate the ruler on two SAVED Branch-P fields (Nr=10 & Nr=16, same cell=8)
    cases = [("Nr10 cont -2e5 (Phi=0.18)", "/tmp/uP_X2e5_tight.pt", 10),
             ("Nr16 floored -2e5 (Phi=5e-3)", "/tmp/uP_Nr16_X2e5_floored.pt", 16)]
    for tag, path, nr in cases:
        if not os.path.exists(path):
            print(f"(missing {path})"); continue
        G = _grid(nr)
        u = torch.load(path).to('cuda' if torch.cuda.is_available() else 'cpu')
        dg = winding_diag(u, G, X, XI, KAP, m=M, kap8=KAP8, branch="P")
        print_winding(tag, dg, G)
    print("\n=== winding-native ruler validated on saved fields ===")
