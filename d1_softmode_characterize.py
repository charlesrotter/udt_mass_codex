#!/usr/bin/env python3
"""D1 soft-mode CHARACTERIZATION (derive what the near-null direction IS, do not impose a gauge).
Per Charles: derive the path, don't assert. The determined-posing Jacobian has 2 near-null directions
(smin~1e-4) dominated by off-diagonal warps (e_rp/e_rt/e_tp) + matter angular (n1,n2). Question: is each
a GENUINE SYMMETRY of the action (benign gauge orbit -> no imposition needed, LM damping handles it), a
NEAR-DEPENDENT derived BC (re-derive it), or a real physical soft mode?
Test 1 (decisive): perturb u along the soft singular vector v; if gauge-INVARIANT observables (winding Q,
rho_max, lapse min, max warp) do NOT move while the field DOES -> it is a pure gauge/symmetry orbit.
Test 2 (identify): overlap the MATTER part of v with the hedgehog's ROTATION generators omega x n (derived
from the matter action's SO(3) invariance). High overlap -> the matter soft mode IS the rotation symmetry.
Category-A diagnosis; OBSERVE not target. Run UNBUFFERED (python3 -u), no grep pipe."""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import torch, numpy as np
torch.set_default_dtype(torch.float64)
import p1_residual_general_einstein as P1
import free_s2_matter as S2M
import whole_metric_3d_matter as MAT
from full3d_spectral import attach_coord_weight, Grid3D, build_metric, T, R as RR, TH, PS
from full3d_newton import inv4x4
from torch.func import jacrev

G = attach_coord_weight(Grid3D(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0))
FIELDS = ['a', 'b', 'c', 'd', 'n1', 'n2', 'n3', 'phi', 'e_rt', 'e_rp', 'e_tp']
f = lambda uu: P1.residual_vector_p1(uu, G, 1.0, 1.0, X=-2e5, branch='G', determined=True)

def observables(u):
    a, b, c, d, n1, n2, n3, phi, ert, erp, etp = P1.unpack11(u, G)
    n_raw = torch.stack([n1, n2, n3], -1)
    dn = S2M.field_dn_components_exact(G, n_raw)
    g = build_metric(G, a, b, c, d, e_rt=ert, e_rp=erp, e_tp=etp); ginv = inv4x4(g)
    rho = -torch.einsum('...ma,...an->...mn', ginv, MAT.stress_tensor(g, ginv, dn, 1.0, 1.0)[0])[..., T, T]
    nrm = torch.sqrt(torch.clamp((n_raw**2).sum(-1), min=1e-300))
    wth = G.wmu / G.sth; dpl = wth[None, :, None] * G.wps[None, None, :]
    crs = torch.cross(dn[..., TH, :], dn[..., PS, :], dim=-1)
    Q_r = ((n_raw/nrm[..., None] * crs).sum(-1) * dpl).sum(dim=(1, 2)) / (4*np.pi)
    warp = max(float(x.abs().max()) for x in (a, b, c, d))
    return dict(Q=float(Q_r[2:-2].mean()), rho_max=float(rho[G.body].abs().max()),
                lapse_min=float(torch.exp(a)[G.body].min()), warp=warp)

def rot_generators(u):
    """Derived hedgehog rotation generators: delta n = omega_k x n (matter-action SO(3) invariance)."""
    a, b, c, d, n1, n2, n3, phi, ert, erp, etp = P1.unpack11(u, G)
    n = torch.stack([n1, n2, n3], -1)
    gens = []
    for k in range(3):
        e = torch.zeros(3, device=n.device); e[k] = 1.0
        dnrot = torch.cross(e.view(1, 1, 1, 3).expand_as(n), n, dim=-1)  # omega_k x n
        gv = torch.zeros(11, G.Nr, G.Nth, G.Nps, device=n.device)
        gv[4] = dnrot[..., 0]; gv[5] = dnrot[..., 1]; gv[6] = dnrot[..., 2]
        gens.append(gv.reshape(-1))
    return gens

d = torch.load('solved_fields_nr8_G_kap8_1.pt', map_location='cpu', weights_only=False)
u = d['u'].to(G.Dr.device)
J = jacrev(f, chunk_size=128)(u).double()
U, S, Vh = torch.linalg.svd(J, full_matrices=False)
sv = S.cpu().numpy()
base = observables(u)
print(f"BASE observables: {base}", flush=True)
print(f"smin SVs: {np.array2string(sv[-3:], precision=3)}", flush=True)
gens = rot_generators(u)
gens = [g/ (g.norm()+1e-30) for g in gens]

for k in (1, 2):
    v = Vh[-k]
    v = v / v.norm()
    # Test 2: overlap of v with the derived rotation generators (matter SO(3) symmetry)
    ov = [abs(float(torch.dot(v, g))) for g in gens]
    matter_frac = float((P1.unpack11(v, G)[4]**2 + P1.unpack11(v, G)[5]**2 + P1.unpack11(v, G)[6]**2).sum())
    print(f"\n=== soft mode #{k} (SV={sv[-k]:.3e}) ===", flush=True)
    print(f"  matter energy frac = {matter_frac:.2f}; |overlap with rotation gens omega_k x n| = "
          f"[{ov[0]:.2f},{ov[1]:.2f},{ov[2]:.2f}]  (rot-subspace overlap = {np.sqrt(sum(o*o for o in ov)):.2f})", flush=True)
    # Test 1: perturb along v, watch gauge-invariant observables vs field change
    print("  perturb u -> u+eps*v  (field DOES change; do the INVARIANTS move?)", flush=True)
    for eps in (0.05, 0.2, 0.5):
        ob = observables(u + eps * v)
        dF = float(((f(u + eps*v) - f(u))**2).sum().sqrt())
        print(f"    eps={eps:.2f}: dQ={ob['Q']-base['Q']:+.4f} d(rho_max)={ob['rho_max']-base['rho_max']:+.3e} "
              f"d(lapse_min)={ob['lapse_min']-base['lapse_min']:+.4f} d(warp)={ob['warp']-base['warp']:+.4f} "
              f"|dResidual|={dF:.3e}", flush=True)
print("\nINTERPRET: invariants ~unchanged while |dResidual| small => GAUGE/SYMMETRY orbit (benign, no imposition;"
      " LM damping handles it). High rotation-gen overlap => the matter mode IS the derived SO(3) rotation symmetry.", flush=True)
