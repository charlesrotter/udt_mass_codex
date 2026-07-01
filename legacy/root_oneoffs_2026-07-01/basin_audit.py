"""basin_audit.py — CLASSIFY-ONLY basin audit (Charles 2026-06-30: no merit gate).

Floors BOTH basins under IDENTICAL globalization from their own starts, using the
stronger step (step='glm' = Levenberg-Marquardt in galerkin coeff space, which
escapes the pure-GN nonlinear stall: verified 2.8e-3 -> 2.9e-8 in one step).

  A_pre_reconciliation : xexplore_field_X1.pt  (STALE -- floored on the PRE-seal-
      reconciliation residual, commit 80d8e37; reads Phi=3.4e5 on current code).
      Re-floored here = a compatibility/continuation test, NOT a rescue. Called
      A_pre_reconciliation until it floors under current code.
  Branch B            : galerkin_floored_X1.pt (current-residual, Phi=1.57e-5).

DISCIPLINE (binding): ALL provenance passed EXPLICITLY (no silent solver default);
manifest printed per run; CLASSIFY only -- NO 'right'/'spurious'/'physical compact
object' language. Op: run UNBUFFERED, single process, no grep pipe, no nohup.
"""
import os, json
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch, numpy as np
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
import free_s2_matter as S2M, whole_metric_3d_matter as MAT
from full3d_spectral import attach_coord_weight, Grid3D, build_metric, T, R as RR, TH, PS
from full3d_newton import inv4x4
from torch.func import jacrev

# --- frozen provenance (ALL explicit; nothing rides a silent solver default) ---
PROV = dict(X=-1.0, xi=1.0, kap=1.0, kap8=1.0, branch='G', p=1.0, wbc=30.0,
            determined=True)
GRID = dict(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0)
STEP = os.environ.get('BASIN_STEP', 'glm')      # LM-in-galerkin (the stronger step)
MAXIT = int(os.environ.get('BASIN_MAXIT', '60'))

G = attach_coord_weight(Grid3D(**GRID))
DEV = G.Dr.device


def residual(u):
    return P1.residual_vector_p1(u, G, PROV['p'], PROV['kap8'], wbc=PROV['wbc'],
                                 X=PROV['X'], xi=PROV['xi'], kap=PROV['kap'],
                                 branch=PROV['branch'], determined=PROV['determined'])


def observe(u):
    a, b, c, dd, n1, n2, n3, phi, ert, erp, etp = P1.unpack11(u, G)
    n = torch.stack([n1, n2, n3], -1)
    dn = S2M.field_dn_components_exact(G, n)
    g = build_metric(G, a, b, c, dd, e_rt=ert, e_rp=erp, e_tp=etp)
    gi = inv4x4(g)
    rho = -torch.einsum('...ma,...an->...mn', gi,
                        MAT.stress_tensor(g, gi, dn, 1.0, 1.0)[0])[..., T, T]
    nrm = torch.sqrt(torch.clamp((n ** 2).sum(-1), min=1e-300))
    wth = G.wmu / G.sth
    dpl = wth[None, :, None] * G.wps[None, None, :]
    crs = torch.cross(dn[..., TH, :], dn[..., PS, :], dim=-1)
    Q = ((n / nrm[..., None] * crs).sum(-1) * dpl).sum((1, 2)) / (4 * np.pi)
    return dict(Q=float(Q[2:-2].mean()),
                rho_max=float(rho[G.body].abs().max()),
                lapse_min=float(torch.exp(a)[G.body].min()),
                warp_max=max(float(x.abs().max()) for x in (a, b, c, dd)),
                phi_max=float(phi.abs().max()))


def resid_split(u):
    F = residual(u)
    J = jacrev(residual, chunk_size=128)(u).double()
    U, S, Vh = torch.linalg.svd(J, full_matrices=False)
    cco = (U.transpose(-1, -2) @ F)
    Phi = float((F * F).sum()); red = float((cco * cco).sum())
    gauge = S < 1e-3
    g_r = float((cco[gauge] ** 2).sum()); p_r = float((cco[~gauge] ** 2).sum())
    return dict(Phi=Phi, reducible=red, gauge_band=g_r, physical_band=p_r,
                gauge_frac=(g_r / red if red > 0 else float('nan')),
                physical_frac=(p_r / red if red > 0 else float('nan')),
                n_gauge=int(gauge.sum().item()))


def manifest(run_id, seed_type, start_field, u, split=True, extra=None):
    m = dict(run_id=run_id, seed_type=seed_type, start_field=start_field,
             step=STEP, grid=GRID, **PROV)
    m.update(observe(u))
    if split:
        m.update(resid_split(u))
    else:
        F = residual(u); m['Phi'] = float((F * F).sum())
    if extra:
        m.update(extra)
    print(f"--- MANIFEST [{run_id}] ---", flush=True)
    for k, v in m.items():
        print(f"    {k}: {v}", flush=True)
    return m


def floor(tag, path, seed_type):
    print("\n" + "=" * 72, flush=True)
    print(f"{tag}  (start={path}, step={STEP}, maxit={MAXIT})", flush=True)
    print("=" * 72, flush=True)
    dd = torch.load(path, map_location='cpu', weights_only=False)
    u0 = dd['u'].to(DEV)
    pre = manifest(f'{tag}_pre', seed_type, path, u0, split=False,
                   extra=dict(stored_Phi=float(dd['Phi']), phase='PRE'))
    print(f"\n>>> flooring {tag} (step={STEP}) ...", flush=True)
    u, hist = P1.newton_solve_p1(u0, G, PROV['p'], PROV['kap8'], wbc=PROV['wbc'],
                                 X=PROV['X'], xi=PROV['xi'], kap=PROV['kap'],
                                 branch=PROV['branch'], determined=PROV['determined'],
                                 step=STEP, maxit=MAXIT, verbose=True)
    print(f"\n{tag} hist (Phi per accepted iter): {[f'{h:.3e}' for h in hist]}", flush=True)
    post = manifest(f'{tag}_post', seed_type, path, u,
                    extra=dict(accepted_steps=len(hist), phase='POST',
                               hist_first=hist[0], hist_last=hist[-1]))
    out = f'{tag}_floored_glm.pt'
    torch.save(dict(u=u.cpu(), Phi=hist[-1], grid=GRID,
                    provenance=f'basin_audit glm floor of {path} under CURRENT residual',
                    **PROV), out)
    print(f"saved -> {out}", flush=True)
    return pre, post


manifests = []
for tag, path, seed in [('A_pre_reconciliation', 'xexplore_field_X1.pt', 'stale_xexplore'),
                        ('B', 'galerkin_floored_X1.pt', 'galerkin_floored')]:
    pre, post = floor(tag, path, seed)
    manifests += [pre, post]

# --- CLASSIFY (no merit judgment) ---
print("\n" + "=" * 72, flush=True)
print("CLASSIFY (no merit judgment) -- both floored under IDENTICAL glm:", flush=True)
A = [m for m in manifests if m['run_id'] == 'A_pre_reconciliation_post'][0]
B = [m for m in manifests if m['run_id'] == 'B_post'][0]
for lab, m in [('A_pre_reconciliation (re-floored)', A), ('B (re-floored)', B)]:
    print(f"  {lab:34s} Q={m['Q']:.4f} phi_max={m['phi_max']:.4f} "
          f"warp_max={m['warp_max']:.3f} rho_max={m['rho_max']:.3e} "
          f"lapse_min={m['lapse_min']:.4f} Phi={m['Phi']:.3e} "
          f"phys_frac={m.get('physical_frac', float('nan')):.3e}", flush=True)

with open('basin_audit_manifest.json', 'w') as fh:
    json.dump(manifests, fh, indent=2, default=float)
print("\nmanifest -> basin_audit_manifest.json", flush=True)
