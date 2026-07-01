#!/usr/bin/env python3
"""Phase 3b Step 4 — SYMMETRY identification of the platonic winding ground states.
Driver: Claude (Opus 4.8, 1M). OBSERVE, DATA-BLIND. Category-A (pure analysis of a
converged state; no physics changed).

Method (rotation-invariant, basis-clean):
  energy density rho = -(ginv.Tab)[T,T] on body shells -> real spherical-harmonic
  power P(l) = sum_m |c_lm|^2 per shell (rotation-INVARIANT), mass-weighted across
  shells (same Wsh as diagnostics).  Fingerprint of the leading non-monopole l:
    only l=0                 -> spherical (m=1 control)
    even ladder, P(2) strong -> axial / toroidal
    P(3) significant         -> tetrahedral (T_d)
    P(2)~0,P(3)~0,P(4) first -> cubic / octahedral (O_h)
    first power at l=6        -> icosahedral (I_h)
  Plus the AZIMUTHAL power spectrum A(|m|)=sum_l|c_lm|^2 (which |m| carry power) as a
  second, independent witness.  Controls: m=1 (must be ~spherical) + the axisym saddle
  (must be axial, power only at |m|=0) calibrate the thresholds.
SELF-TEST (run first): feed synthetic pure-l fields; P(l) must peak at the right l.
Runs foreground/synchronous.  Usage: python3 phase3b_symmetry.py
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import json, math, glob
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
from scipy.special import sph_harm
from full3d_grid_shexact import make_grid_shexact
from full3d_spectral import residuals, T as IT
import full3d_newton as NEW
import winding_catalog_map as WC
from full3d_solver import unpack

PI = math.pi


def energy_density(G, u, p, kap8, m):
    a, b, c, d, Th = unpack(u, G)
    out = residuals(G, (a, b, c, d, Th), p, kap8, m)
    Tmix = torch.einsum('...ma,...an->...mn', out['ginv'], out['Tab'])
    rho = -Tmix[..., IT, IT]              # (Nr,Nth,Nps)
    return rho.detach().cpu().numpy()


def sh_basis(G, Lmax):
    """Precompute Y_lm*(theta,psi) on the grid; theta=polar (G.th), psi=azimuth (G.psi).
    scipy.sph_harm(m, l, azimuth, polar)."""
    th = G.th.cpu().numpy()         # polar (Nth,)
    ps = G.psi.cpu().numpy()        # azimuth (Nps,)
    TH, PS = np.meshgrid(th, ps, indexing='ij')   # (Nth,Nps)
    Y = {}
    for l in range(Lmax + 1):
        for mm in range(-l, l + 1):
            Y[(l, mm)] = np.conj(sph_harm(mm, l, PS, TH))   # (Nth,Nps)
    return Y


def power_spectrum(G, rho, Lmax):
    """Per-shell c_lm = sum_{th,ps} rho Y_lm* wmu wps; P(l)=sum_m|c_lm|^2;
    A(|m|)=sum_l|c_lm|^2.  Mass-weight across body shells (Wsh as in diagnostics).
    Returns normalized P(l)/P(0) and A(|m|)/A(0), both mass-weighted scalars per l/|m|."""
    wmu = G.wmu.cpu().numpy(); wps = G.wps.cpu().numpy()
    dO = wmu[:, None] * wps[None, :]            # (Nth,Nps), integrates to 4pi
    r = G.r.cpu().numpy()
    body = (r > 0.5) & (r < G.ri - 0.8)
    idx = np.where(body)[0]
    Y = sh_basis(G, Lmax)
    # shell weights ~ shell mass = r^2 * <rho>_angle
    meana = np.array([(rho[i] * dO).sum() / (4 * PI) for i in idx])
    shell_mass = np.clip(r[idx]**2 * meana, 0, None)
    Wsh = shell_mass / max(shell_mass.sum(), 1e-30)
    Pl = np.zeros(Lmax + 1); Am = np.zeros(Lmax + 1)
    for w, i in zip(Wsh, idx):
        clm = {}
        for l in range(Lmax + 1):
            for mm in range(-l, l + 1):
                clm[(l, mm)] = (rho[i] * Y[(l, mm)] * dO).sum()
        P0 = abs(clm[(0, 0)])**2 + 1e-300
        for l in range(Lmax + 1):
            pl = sum(abs(clm[(l, mm)])**2 for mm in range(-l, l + 1))
            Pl[l] += w * pl / P0
        for am in range(Lmax + 1):
            ampow = sum(abs(clm[(l, mm)])**2 for l in range(am, Lmax + 1)
                        for mm in (am, -am) if abs(mm) <= l)
            Am[am] += w * ampow / P0
    return Pl, Am, len(idx)


def verdict(Pl, thr=0.01):
    """Leading non-monopole l + group fingerprint."""
    lead = next((l for l in range(1, len(Pl)) if Pl[l] > thr), None)
    has = {l: (Pl[l] > thr) for l in range(len(Pl))}
    if lead is None:
        g = "spherical"
    elif lead == 2 and not has.get(3, False):
        g = "axial/toroidal (l=2 ladder)"
    elif has.get(3, False):
        g = "tetrahedral T_d (l=3 present)"
    elif lead == 4:
        g = "cubic/octahedral O_h (l=4 first, no l=2,3)"
    elif lead == 6:
        g = "icosahedral I_h (l=6 first)"
    else:
        g = f"leading l={lead} (unclassified at this resolution)"
    return lead, g


def self_test():
    """Feed synthetic pure-l angular fields; P(l) must peak at that l."""
    G = make_grid_shexact(8, 12, 12, mmax=6)
    th = G.th.cpu().numpy(); ps = G.psi.cpu().numpy()
    TH, PS = np.meshgrid(th, ps, indexing='ij')
    ok = True
    for ltest in (1, 2, 3, 4):
        field = np.real(sph_harm(0, ltest, PS, TH)) + 1.0   # +monopole offset
        rho = np.repeat(field[None, :, :], G.Nr, axis=0)
        Pl, Am, _ = power_spectrum(G, rho, 6)
        peak = int(np.argmax(Pl[1:]) + 1)
        print(f"  self-test l={ltest}: P(l)={np.round(Pl,4)} peak@{peak} {'OK' if peak==ltest else 'FAIL'}")
        ok = ok and (peak == ltest)
    # azimuthal test: cos(3 psi) -> A(3) dominant
    field = np.cos(3 * PS) * np.sin(TH)**3 + 1.0
    rho = np.repeat(field[None, :, :], G.Nr, axis=0)
    Pl, Am, _ = power_spectrum(G, rho, 6)
    apk = int(np.argmax(Am[1:]) + 1)
    print(f"  self-test cos(3psi): A(|m|)={np.round(Am,4)} peak@{apk} {'OK' if apk==3 else 'FAIL'}")
    return ok and apk == 3


def analyze_checkpoint(path, p=0.4, kap8=0.05):
    tile = json.load(open(path.replace('.pt', '.json')))
    m = tile['m']; Nr, Nth, Nps = tile['grid']
    G = make_grid_shexact(Nr, Nth, Nps, mmax=Nps // 2)
    u = torch.load(path).to(G.dev)
    rho = energy_density(G, u, p, kap8, m)
    Lmax = min(Nth - 1, Nps // 2)
    Pl, Am, nshell = power_spectrum(G, rho, Lmax)
    lead, g = verdict(Pl)
    print(f"[m={m}] grid {Nr}x{Nth}x{Nps} Lmax={Lmax} nshell={nshell} "
          f"M_MS={tile['M_MS']:.4f} psivar={tile['psivar']:.3e}")
    print(f"   P(l)/P(0) = {np.round(Pl,4)}")
    print(f"   A(|m|)/A(0)= {np.round(Am,4)}")
    print(f"   VERDICT: leading l={lead} -> {g}  [resolution Lmax={Lmax}, m<= {Nps//2}]")
    return dict(m=m, grid=[Nr, Nth, Nps], Lmax=Lmax, Pl=Pl.tolist(), Am=Am.tolist(),
                leading_l=lead, group=g, M_MS=tile['M_MS'], psivar=tile['psivar'])


if __name__ == "__main__":
    print("=== SELF-TEST (SH machinery) ===")
    st = self_test()
    print(f"SELF-TEST {'PASS' if st else 'FAIL'}")
    print("=== checkpoints (m=1 = spherical control; m>=2 = platonic) ===")
    out = []
    for path in sorted(glob.glob("/home/udt-admin/udt_mass_codex/u_plat_m*_*.pt")):
        try:
            out.append(analyze_checkpoint(path))
        except Exception as e:
            print(f"  {path}: ERROR {e}")
    json.dump(out, open("/home/udt-admin/udt_mass_codex/phase3b_symmetry_out.json", "w"), indent=1)
    print("DONE_SYMMETRY")
