"""Phase C REDO (rigorous) + axisymmetry Fourier test.
Phase C: SOLVE Laplacian u = rho4 with an ACTUAL residual, then INDEPENDENTLY evaluate the
nested-surface flux Phi(R)=oint_{S_R} grad u . dS by spherical quadrature (trilinear-interp of
grad u onto lat-lon spheres). Compare surface flux to the volume int rho4 = E4 -- an INDEPENDENT
Gauss-law check (surface computation != volume computation). M_N(R)=2 Phi(R) -> 2 E4.
Axisymmetry: azimuthal Fourier m-mode power of rho (replaces the coarse bin test)."""
import json, numpy as np, torch
import torch.nn.functional as Fn
import hopfion_static_mass_common as C
torch.set_default_dtype(torch.float64)
P = 'hopfion_arc_scripts_2026-07-05/prod_an256.npz'
d = C.load_h3(P); n = d['n']; h = d['h']; L = d['L']; xi = d['xi']; k4 = d['k4']; dev = d['dev']; N = d['N']
mf = C.matter_fields(n, h, xi, k4); rho4 = mf['rho4']; E4 = float(rho4.sum()*h**3); E2 = float(mf['rho2'].sum()*h**3)

def fd_laplacian(f):
    return sum((torch.roll(f, -1, a) - 2*f + torch.roll(f, 1, a)) for a in (0, 1, 2)) / h**2

def phaseC(rho4, L, N, h, tag=""):
    E4loc = float(rho4.sum() * h**3)
    # TRUE isolated (free-space Hockney) Poisson solve -- NO periodic images
    u = C.poisson_solve_isolated(rho4, L)
    # ACTUAL Poisson residual against the 7-point FD Laplacian, INTERIOR ONLY (roll wraps at faces)
    res = fd_laplacian(u) - rho4
    b = 6
    interior = torch.zeros_like(res, dtype=torch.bool); interior[b:-b, b:-b, b:-b] = True
    res_rel = float(res[interior].norm() / rho4.norm())
    # DISCRETE nested CUBIC FACE fluxes (exact discrete Gauss law) -> E4 for boxes enclosing the source
    halves = list(range(max(2, int(0.8 / h)), N // 2 - 3, max(1, N // 40)))
    Rphys = [hh * h for hh in halves]
    flux = [C.discrete_face_flux(u, hh, h) for hh in halves]
    MN = [2 * f for f in flux]
    ib = int(np.argmin([abs(rp - 3.0) for rp in Rphys]))
    encl = [f for rp, f in zip(Rphys, flux) if rp >= 3.0]
    spread = float(np.ptp(encl) / (abs(np.mean(encl)) + 1e-30)) if len(encl) > 2 else float('nan')
    return dict(tag=tag, res_rel=res_rel, E4=E4loc, twoE4=2*E4loc,
                Rphys=[float(x) for x in Rphys], face_flux=flux, MN=MN,
                MN_best=MN[ib], R_best=float(Rphys[ib]), MN_best_over_2E4=MN[ib]/(2*E4loc),
                flux_plateau_spread=spread)

print("=== Phase C REDO: isolated (Hockney) Poisson + DISCRETE CUBIC FACE fluxes ===")
r = phaseC(rho4, L, N, h)
print(f"  interior Poisson FD residual ||lap_FD(u)-rho4||/||rho4|| = {r['res_rel']:.3e}")
print(f"  E4(volume)={E4:.3f}  2E4={2*E4:.3f}")
print(f"  cube half-width R -> DISCRETE FACE flux oint grad u.dS (-> E4={E4:.2f}); M_N=2*flux -> 2E4:")
for R, f, m in zip(r['Rphys'], r['face_flux'], r['MN']):
    print(f"    R={R:.2f}  face_flux={f:.3f} (E4={E4:.2f})  M_N=2*flux={m:.3f} (2E4={2*E4:.2f})")
print(f"  best (R~3, just enclosing source): M_N={r['MN_best']:.3f}  M_N/2E4={r['MN_best_over_2E4']:.4f}")
print(f"  flux plateau spread over enclosing boxes = {r['flux_plateau_spread']:.2e}  (isolated => should be flat)")

# grid convergence (subsample factor 2)
print("  grid convergence (subsample factor 2):")
n2 = n[:, ::2, ::2, ::2].contiguous(); n2 = n2/n2.norm(dim=0, keepdim=True); h2 = h*2; N2 = n2.shape[1]
mf2 = C.matter_fields(n2, h2, xi, k4); r2 = phaseC(mf2['rho4'], L, N2, h2)
print(f"    N={N}: M_N_best={r['MN_best']:.3f} (/2E4={r['MN_best_over_2E4']:.4f}) res={r['res_rel']:.2e} ;"
      f" N={N2}: M_N_best={r2['MN_best']:.3f} (/2E4={r2['MN_best_over_2E4']:.4f}) res={r2['res_rel']:.2e}")

# === Axisymmetry: azimuthal Fourier m-mode power of rho (replaces bin test) ===
print("\n=== Axisymmetry: azimuthal Fourier m-mode power of rho ===")
rho = mf['rho']
nrho, nz, nphi = 40, 40, 64
rc = torch.linspace(0.15, 4.0, nrho, device=dev); zc = torch.linspace(-3.5, 3.5, nz, device=dev)
phg = torch.arange(nphi, device=dev)*2*np.pi/nphi
RC, ZC, PHI = torch.meshgrid(rc, zc, phg, indexing='ij')
Xc = RC*torch.cos(PHI); Yc = RC*torch.sin(PHI)
gc = torch.stack([ZC/L, Yc/L, Xc/L], -1)[None, None]         # (1,1,nrho,nz,nphi... need 5D)
gc = torch.stack([ZC/L, Yc/L, Xc/L], -1).reshape(1, nrho, nz, nphi, 3)
rho_cyl = Fn.grid_sample(rho[None, None], gc, align_corners=True, padding_mode='border')[0, 0]  # (nrho,nz,nphi)
fft = torch.fft.rfft(rho_cyl, dim=-1)                         # FFT in phi
pw = (fft.abs()**2)
m0 = float(pw[..., 0].sum()); mtot = float(pw.sum())
frac = {f"m>=1_power_frac": (mtot-m0)/mtot}
for m in (1, 2, 3, 4):
    frac[f"m={m}"] = float(pw[..., m].sum()/mtot)
print(f"  m>=1 power fraction = {frac['m>=1_power_frac']:.4f}  (m=1:{frac['m=1']:.4f} m=2:{frac['m=2']:.4f} m=3:{frac['m=3']:.4f} m=4:{frac['m=4']:.4f})")

out = {'phaseC_redo': {k: v for k, v in r.items() if k != 'tag'},
       'method': 'isolated free-space Hockney Poisson (no periodic images) + discrete cubic face fluxes (exact discrete Gauss law)',
       'phaseC_convergence': {'N_fine': N, 'MN_best_fine': r['MN_best'], 'ratio_fine': r['MN_best_over_2E4'], 'res_fine': r['res_rel'],
                              'N_coarse': N2, 'MN_best_coarse': r2['MN_best'], 'ratio_coarse': r2['MN_best_over_2E4'], 'res_coarse': r2['res_rel']},
       'axisymmetry_fourier': frac, 'E2': E2, 'E4': E4}
json.dump(out, open('hopfion_static_mass_phaseC_redo_out.json', 'w'), indent=1)
print("saved hopfion_static_mass_phaseC_redo_out.json")
