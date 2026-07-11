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
    # spectral (FFT, open BC via zero-pad) solve of Laplacian u = rho4
    u = C.poisson_solve_open(rho4, L)
    # ACTUAL Poisson residual against the 7-point FD Laplacian, INTERIOR ONLY (torch.roll wraps at the
    # extracted-region boundary; the physical residual is the interior, away from the box faces).
    res = fd_laplacian(u) - rho4
    b = 6                                                 # exclude a boundary layer
    interior = torch.zeros_like(res, dtype=torch.bool); interior[b:-b, b:-b, b:-b] = True
    res_rel = float(res[interior].norm() / rho4.norm())
    res_rel_full = float(res.norm() / rho4.norm())
    # grad u by FD central diff
    gu = torch.stack([C._dc(u, a, h) for a in range(3)], 0)   # (3,N,N,N)
    # INDEPENDENT nested-surface flux via lat-lon spherical quadrature + trilinear interp
    nth, nph = 48, 96
    th = (torch.arange(nth, device=dev) + 0.5) * np.pi / nth
    ph = (torch.arange(nph, device=dev)) * 2*np.pi / nph
    TH, PH = torch.meshgrid(th, ph, indexing='ij')
    rhat = torch.stack([torch.sin(TH)*torch.cos(PH), torch.sin(TH)*torch.sin(PH), torch.cos(TH)], 0)  # (3,nth,nph)
    dOmega = (np.pi/nth) * (2*np.pi/nph) * torch.sin(TH)      # (nth,nph)
    def surf_flux(R):
        pts = R * rhat                                        # (3,nth,nph) cartesian
        # grid_sample expects coords in [-1,1], order (x=dim2? ) -> build (1,1,nth,nph,3) with (z,y,x)
        gc = torch.stack([pts[2]/L, pts[1]/L, pts[0]/L], -1)[None, None]   # (1,1,nth,nph,3)
        gu_s = Fn.grid_sample(gu[None], gc, align_corners=True, padding_mode='border')[0, :, 0]  # (3,nth,nph)
        gdotr = (gu_s * rhat).sum(0)                          # grad u . rhat
        return float((gdotr * dOmega).sum() * R**2)          # oint grad u.dS
    Rs = np.linspace(2.5, 5.5, 7)
    flux = [surf_flux(float(R)) for R in Rs]
    MN_surf = [2*f for f in flux]
    # best read radius = just outside the compact source (r_tex~2.5), before finite-box image drift
    ib = int(np.argmin([abs(R - 3.0) for R in Rs]))
    return dict(tag=tag, res_rel=res_rel, res_rel_full=res_rel_full, E4=E4, twoE4=2*E4,
                Rs=[float(x) for x in Rs], surf_flux=flux, MN_surface=MN_surf,
                MN_best=MN_surf[ib], R_best=float(Rs[ib]), MN_best_over_2E4=MN_surf[ib]/(2*E4),
                MN_surface_limit=MN_surf[-1], MN_over_2E4=MN_surf[-1]/(2*E4))

print("=== Phase C REDO: actual Poisson residual + INDEPENDENT nested-surface flux ===")
r = phaseC(rho4, L, N, h)
print(f"  Poisson FD residual ||lap_FD(u)-rho4||/||rho4|| = {r['res_rel']:.3e}")
print(f"  E4(volume)={E4:.3f}  2E4={2*E4:.3f}")
print(f"  R -> INDEPENDENT surface flux oint grad u.dS  (should -> E4={E4:.2f}); M_N=2*flux -> 2E4:")
for R, f, m in zip(r['Rs'], r['surf_flux'], r['MN_surface']):
    print(f"    R={R:.2f}  surf_flux={f:.3f} (E4={E4:.2f})  M_N=2*flux={m:.3f} (2E4={2*E4:.2f})")
print(f"  M_N(surface)/2E4 = {r['MN_over_2E4']:.4f}  (independent surface vs volume agreement)")

# grid refinement of the surface-flux limit (subsample -> re-evaluate)
print("  grid refinement of surface-flux M_N (subsample factor 2):")
n2 = n[:, ::2, ::2, ::2].contiguous(); n2 = n2/n2.norm(dim=0, keepdim=True); h2 = h*2; N2 = n2.shape[1]
mf2 = C.matter_fields(n2, h2, xi, k4); r2 = phaseC(mf2['rho4'], L, N2, h2)
print(f"    N={N}: M_N={r['MN_surface_limit']:.3f} res={r['res_rel']:.2e} ; N={N2}: M_N={r2['MN_surface_limit']:.3f} res={r2['res_rel']:.2e}")

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
       'phaseC_refine': {'N_fine': N, 'MN_fine': r['MN_surface_limit'], 'res_fine': r['res_rel'],
                         'N_coarse': N2, 'MN_coarse': r2['MN_surface_limit'], 'res_coarse': r2['res_rel']},
       'axisymmetry_fourier': frac, 'E2': E2, 'E4': E4}
json.dump(out, open('hopfion_static_mass_phaseC_redo_out.json', 'w'), indent=1)
print("saved hopfion_static_mass_phaseC_redo_out.json")
