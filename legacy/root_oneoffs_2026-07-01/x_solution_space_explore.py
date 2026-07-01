#!/usr/bin/env python3
"""EXPLORE the determined static solution across the FREE dilaton ratio X (Charles's pivot 2026-06-29:
X=-2e5 is a Cassini-forced KLUGE, not derived -- R1-R3 do NOT fix |X| (branch_operator.py:85, tagged FREE);
only the sign is derived (ghost-free => negative). So OBSERVE what the metric does across X instead of forcing
the floor at the imposed value (which strangles the dilaton -- exactly the phi-angular sector of interest).

Walk an X-LADDER from the NATURAL O(1) ratio (X=-1, dilaton alive) toward the Cassini extreme (-2e5, throttled),
warm-starting each rung from the previous solution, on the determinacy-fixed + core-BC-fixed determined posing.
At each X record: did it floor? + the gauge-invariant observables + how ALIVE the dilaton is (max|phi|, profile).
OBSERVE mode -- report what is there, no targeting.

PREMISES: X = FREE/EXPLORED (the point); branch G = FREE (P is a follow-up); kap8=1, xi=kap=1 = THEORY (units);
sign(X) = DERIVED negative (ghost-free); rc=0.1 = CHOSE; matter = rigid unit hedgehog (resolved).
Category-A solver params (grid, maxit, tol). Run UNBUFFERED (python3 -u), no grep pipe. Bounded Nr=8, single process."""
import os, time
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch, numpy as np
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
import free_s2_matter as S2M
import whole_metric_3d_matter as MAT
from full3d_spectral import attach_coord_weight, Grid3D, build_metric, T, R as RR, TH, PS
from full3d_newton import inv4x4

t0 = time.time()
G = attach_coord_weight(Grid3D(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0))

def observe(u, X, Phi):
    a, b, c, d, n1, n2, n3, phi, ert, erp, etp = P1.unpack11(u, G)
    n_raw = torch.stack([n1, n2, n3], -1)
    dn = S2M.field_dn_components_exact(G, n_raw)
    g = build_metric(G, a, b, c, d, e_rt=ert, e_rp=erp, e_tp=etp); ginv = inv4x4(g)
    rho = -torch.einsum('...ma,...an->...mn', ginv, MAT.stress_tensor(g, ginv, dn, 1.0, 1.0)[0])[..., T, T]
    nrm = torch.sqrt(torch.clamp((n_raw**2).sum(-1), min=1e-300))
    wth = G.wmu / G.sth; dpl = wth[None, :, None] * G.wps[None, None, :]
    crs = torch.cross(dn[..., TH, :], dn[..., PS, :], dim=-1)
    Q_r = ((n_raw/nrm[..., None] * crs).sum(-1) * dpl).sum(dim=(1, 2)) / (4*np.pi)
    # dilaton "aliveness": max|phi|, and its radial profile (max over angles per layer)
    phi_rad = phi.abs().amax(dim=(1, 2)).cpu().numpy()
    warp = max(float(x.abs().max()) for x in (a, b, c, d))
    eoff = max(float(x.abs().max()) for x in (ert, erp, etp))
    return dict(X=X, Phi=Phi, floored=(Phi < 1e-6),
                Q=float(Q_r[2:-2].mean()), rho_max=float(rho[G.body].abs().max()),
                lapse_min=float(torch.exp(a)[G.body].min()),
                phi_absmax=float(phi.abs().max()), warp=warp, eoff=eoff,
                phi_rad=phi_rad)

# X-ladder: NATURAL O(1) ratio -> Cassini extreme. Sign DERIVED negative; magnitude EXPLORED.
Xs = [-1.0, -3.0, -10.0, -30.0, -100.0, -300.0, -1e3, -3e3, -1e4, -3e4, -1e5, -2e5]
u = P1.seed_round_native(G, p=1.0, m=1)
print("=== X SOLUTION-SPACE EXPLORATION (determined, branch G, kap8=1, Nr=8). OBSERVE across FREE X. ===", flush=True)
print(f"{'X':>9} {'Phi':>10} {'floor':>5} {'phi_absmax':>11} {'warp':>8} {'eoff':>9} {'Q':>7} {'rho_max':>9} {'lapse_min':>9}", flush=True)
rows = []
for X in Xs:
    u, hist = P1.newton_solve_p1(u, G, 1.0, 1.0, X=X, branch="G", m=1, maxit=40,
                                 tol=1e-12, determined=True, verbose=False)
    Phi = float((P1.residual_vector_p1(u, G, 1.0, 1.0, X=X, branch="G", determined=True)**2).sum())
    ob = observe(u, X, Phi)
    rows.append(ob)
    print(f"{X:>9.1f} {Phi:>10.2e} {str(ob['floored']):>5} {ob['phi_absmax']:>11.3e} {ob['warp']:>8.3f} "
          f"{ob['eoff']:>9.2e} {ob['Q']:>7.3f} {ob['rho_max']:>9.2e} {ob['lapse_min']:>9.3f}  "
          f"[t={time.time()-t0:.0f}s]", flush=True)
    torch.save({'u': u.cpu(), 'X': X, 'Phi': Phi, 'branch': 'G', 'kap8': 1.0, 'determined': True},
               f'xexplore_field_X{abs(X):.0f}.pt')

print("\n=== dilaton radial profile (max|phi| per layer, core..seal) across X ===", flush=True)
for ob in rows:
    print(f"  X={ob['X']:>9.1f}: {np.array2string(ob['phi_rad'], precision=3, max_line_width=200)}", flush=True)
print(f"\nINTERPRET (OBSERVE): does the dilaton come ALIVE (phi_absmax large, structured radial profile, localization)"
      f" at the NATURAL X~-1 and get THROTTLED (phi->0) toward the Cassini -2e5? Does any structure EMERGE as the"
      f" throttle releases? [t={time.time()-t0:.0f}s]", flush=True)
