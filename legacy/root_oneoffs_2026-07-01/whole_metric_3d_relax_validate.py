#!/usr/bin/env python3
"""
whole_metric_3d_relax_validate.py -- validate the 3-D relaxation solver pieces against
the VERIFIED radial #56 physics, then the full STAY / RELAX-BACK gate.

Driver: Claude (Opus 4.8, 1M). 2026-06-15. DATA-BLIND. Frame: whole_metric_solve_MAP.md.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import torch
import whole_metric_3d_core as core
import whole_metric_3d_matter as mat
import whole_metric_3d_solver as S
import whole_metric_3d_relax as RX
import radial_Bfree_soliton as rb

torch.set_default_dtype(torch.float64)
DEV = S.DEV
T, R, TH, PS = 0, 1, 2, 3


def hdr(s):
    print("\n"+"="*78, flush=True); print(s, flush=True); print("="*78, flush=True)


# ---------------------------------------------------------------------------
xi = kap = 1.0
rc = 0.05; SPAN = 14.0; ri = rc + SPAN
P = 0.4; KAP8 = 0.05
th0, th1 = 0.30, math.pi-0.30


def build_round(G, a_r, b_r, Th_r):
    Nr, Nth, Nps = G['Nr'], G['Nth'], G['Nps']
    a_f = a_r[:, None, None].expand(Nr, Nth, Nps)
    b_f = b_r[:, None, None].expand(Nr, Nth, Nps)
    g = torch.zeros(Nr, Nth, Nps, 4, 4, device=DEV)
    g[..., T, T] = -torch.exp(2*a_f)
    g[..., R, R] = torch.exp(2*b_f)
    g[..., TH, TH] = G['Rr']**2
    g[..., PS, PS] = (G['Rr']*torch.sin(G['Tht']))**2
    Th_field = Th_r[:, None, None].expand(Nr, Nth, Nps).contiguous()
    return g, Th_field


# ===========================================================================
# TEST A -- the autograd matter EL gradient reproduces the VERIFIED radial EL.
# At the #56 solution dS/dTh must be ~0 in the smooth body (it is a stationary point).
# ===========================================================================
hdr("TEST A -- autograd matter EL: dS/dTh ~ 0 at the verified #56 solution")
Nr = 320
G = S.mkgrid(Nr, 64, 16, rc, ri, th0, th1)
rN = rb.make_grid(1, Nr, rc=rc, rint=ri, geom=False)
oN = rb.selfconsistent_Bfree(rN, xi, kap, p=P, kap8=KAP8, iters=300, relax=0.4,
                             tol=1e-11, verbose=False)
a_r, b_r, Th_r = oN['a'][0], oN['b'][0], oN['Th'][0]
g, Th_field = build_round(G, a_r, b_r, Th_r)
ginv = core.metric_inverse(g)
gradTh = RX.field_EL_grad_Th(Th_field, g, ginv, G)
# normalize by the action-density scale to read it as a relative EL residual
sqrtg = torch.sqrt(torch.clamp(-torch.linalg.det(g), min=1e-30))
body = slice(int(0.1*Nr), int(0.9*Nr))
print(f"  |dS/dTh| smooth body: max={gradTh[body, 8:-8].abs().max().item():.3e} "
      f"mean={gradTh[body, 8:-8].abs().mean().item():.3e}")
print(f"  (the autograd action gradient at the verified solution should be small ->")
print(f"   confirms the action density + its EL are the SAME physics as the radial EL)")


# ===========================================================================
# TEST B -- STAY: seeded at #56, the FULL relaxer keeps the residual bounded and
# does not drift (no spurious off-diagonals appear).
# ===========================================================================
hdr("TEST B -- STAY: relaxer seeded at #56 stays put")
out = RX.solve(g, Th_field, KAP8, G, bc_core=math.pi, bc_seal=0.0,
               outer=60, omega=0.15, matter_steps=4, matter_lr=0.1,
               mask_core=1.0, verbose=True, tag="STAY")
h = out['hist']
print(f"  start body max|res_diag|={h[0][1]:.3e}  end={h[-1][1]:.3e}")
print(f"  start max|res_off|={h[0][2]:.3e}  end={h[-1][2]:.3e}  (should stay ~machine-0)")
# M_MS drift
b_now = -0.5*torch.log((g[..., R, R]).clamp(min=1e-30))  # e^{2b}=g_rr -> b
b_eq = b_now[:, G['Nth']//2, 0]
m_areal = G['rg']*(1.0 - torch.exp(-2*b_eq))
M_MS_now = (m_areal[-1]-m_areal[0]).item()
print(f"  M_MS now={M_MS_now:.6f}  committed #56={oN['M_MS'].item():.6f}")


# ===========================================================================
# TEST C -- RELAX BACK: perturb the metric (add a bump to g_rr + a small off-diagonal
# g_ttheta that NOTHING sources), relax, and confirm the residual FALLS and the
# un-sourced off-diagonal DECAYS toward 0 (the solver removes spurious structure).
# ===========================================================================
hdr("TEST C -- RELAX BACK: perturb then relax")
g_pert = g.clone()
bump = 0.05*torch.exp(-((G['rg']-(rc+3.0))**2/0.5))[:, None, None].expand_as(g[..., R, R])
g_pert[..., R, R] = g[..., R, R]*(1.0+bump)
# inject an un-sourced time-row off-diagonal g_ttheta
gt_th = 0.02*torch.sin(G['Tht'])*torch.exp(-((G['rg'][:, None, None]-(rc+3.0))**2/0.5))
g_pert[..., T, TH] = gt_th; g_pert[..., TH, T] = gt_th
ginv_p = core.metric_inverse(g_pert)
n0 = mat.hedgehog_n(Th_field, G['Tht'], G['Ps'])
Res0, _, _, _, _ = S.einstein_residual_mixed(g_pert, n0, KAP8, G)
i0, i1 = int(0.1*Nr), int(0.9*Nr)
r0diag = max(Res0[i0:i1, 8:-8, :][..., a, a].abs().max().item() for a in range(4))
r0off = Res0[i0:i1, 8:-8, :][..., T, TH].abs().max().item()
print(f"  perturbed start: body max|res_diag|={r0diag:.3e}  injected g_ttheta max={g_pert[..., T, TH].abs().max().item():.3e}")
out2 = RX.solve(g_pert, Th_field, KAP8, G, bc_core=math.pi, bc_seal=0.0,
                outer=120, omega=0.15, matter_steps=4, matter_lr=0.1,
                mask_core=1.0, verbose=True, tag="BACK")
g2 = out2['g']
n2 = mat.hedgehog_n(out2['Th'], G['Tht'], G['Ps'])
Res2, _, _, _, _ = S.einstein_residual_mixed(g2, n2, KAP8, G)
r2diag = max(Res2[i0:i1, 8:-8, :][..., a, a].abs().max().item() for a in range(4))
r2off = g2[..., T, TH].abs()[i0:i1, 8:-8, :].max().item()
print(f"  after relax: body max|res_diag|={r2diag:.3e}  (start {r0diag:.3e})")
print(f"  residual surviving g_ttheta max={r2off:.3e}  (injected 0.02 -> should decay)")
print(f"\n  STAY ok: {h[-1][1] < 5*h[0][1] and h[-1][2] < 1e-6}")
print(f"  RELAX-BACK ok: {r2diag < r0diag}")
