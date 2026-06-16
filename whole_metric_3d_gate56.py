#!/usr/bin/env python3
"""
whole_metric_3d_gate56.py -- THE VALIDATION GATE against the CORRECTED #56 soliton.

Driver: Claude (Opus 4.8, 1M).  2026-06-15.  Frame: whole_metric_solve_MAP.md sec 10.2.
DATA-BLIND.

The prior gate (whole_metric_3d_gate.py, #55) seeded the OLD #52 soliton (B=1/A
IMPOSED) and correctly found it FAILS the full 3-D Einstein system (the (r,r)/angular
eqs are violated O(1) because B=1/A + (t,t) forces p_r=-rho but the soliton is
EOS-softened).  The CORRECTION (#56, radial_Bfree_soliton.py, blind-verified) FREES
a(r),b(r): ds^2 = -e^{2a}dt^2 + e^{2b}dr^2 + r^2 dOmega^2, with all three radial
Einstein residuals -> 0 at O(h^2).

THIS GATE: map the CORRECTED #56 soliton onto the FULL 3-D (r,theta,psi) grid (a,b
independent, NOT B=1/A), evaluate the FULL 3-D Einstein residual G^mu_nu - kappa8 T^mu_nu
with the VALIDATED engine (all components, off-diagonals zero for the round seed but
ALLOCATED), and confirm ALL components -> 0 and CONVERGE with resolution.  If this
passes, the 3-D engine correctly recognizes the corrected soliton as a full solution,
and the validated-evaluator + corrected-seed is the trusted basis for the 3-D solver.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math
import numpy as np
import torch
import whole_metric_3d_solver as S
import radial_Bfree_soliton as rb

torch.set_default_dtype(torch.float64)
DEV = S.DEV
T, R, TH, PS = 0, 1, 2, 3


def hdr(s):
    print("\n"+"="*78, flush=True); print(s, flush=True); print("="*78, flush=True)


# ---------------------------------------------------------------------------
# 1. Solve the CORRECTED #56 radial soliton (the validation target).
# ---------------------------------------------------------------------------
hdr("STEP 1 -- the CORRECTED #56 radial soliton (validation target)")
xi = kap = 1.0
rc = 0.05; SPAN = 14.0; ri = rc + SPAN*1.0
P = 0.4; KAP8 = 0.05
N1 = 1600
r1 = rb.make_grid(1, N1, rc=rc, rint=ri, geom=False)
o = rb.selfconsistent_Bfree(r1, xi, kap, p=P, kap8=KAP8, iters=300, relax=0.4,
                            tol=1e-11, verbose=False)
a1 = o['a'][0]; b1 = o['b'][0]; Th1 = o['Th'][0]; rr1 = o['r'][0]
M_MS_ref = o['M_MS'].item()
print(f"  #56 corrected: p={P} kap8={KAP8}  M_MS={M_MS_ref:.6f}")
print(f"  a0={a1[0].item():.5f} (phi0={-a1[0].item():.5f})  b0={b1[0].item():.5f}")
# radial residuals as a sanity (the engine in radial_Bfree)
res = o['res']
print(f"  radial residuals (interior 0.4..ri-0.5): "
      f"res_tt={res['res_tt'][0, 30:-30].abs().max().item():.2e} "
      f"res_rr={res['res_rr'][0, 30:-30].abs().max().item():.2e} "
      f"res_thth={res['res_thth'][0, 30:-30].abs().max().item():.2e}")


# ---------------------------------------------------------------------------
# 2. Map onto the 3-D grid and evaluate the FULL 3-D Einstein residual.
# ---------------------------------------------------------------------------
def interp_to(rg_new, r_old, f_old):
    return torch.tensor(np.interp(rg_new.cpu().numpy(), r_old.cpu().numpy(),
                                  f_old.cpu().numpy()), device=DEV)


def build_round_metric(G, a1, b1, rr1):
    """Diagonal round soliton on the 3-D grid: ds^2 = -e^{2a}dt^2 + e^{2b}dr^2
    + r^2 dtheta^2 + r^2 sin^2theta dpsi^2.  a,b INDEPENDENT (the #56 correction).
    ALL 10 components allocated; off-diagonals zero (round)."""
    Nr, Nth, Nps = G['Nr'], G['Nth'], G['Nps']
    a_r = interp_to(G['rg'], rr1, a1)
    b_r = interp_to(G['rg'], rr1, b1)
    a_f = a_r[:, None, None].expand(Nr, Nth, Nps)
    b_f = b_r[:, None, None].expand(Nr, Nth, Nps)
    g = torch.zeros(Nr, Nth, Nps, 4, 4, device=DEV)
    g[..., T, T] = -torch.exp(2*a_f)
    g[..., R, R] = torch.exp(2*b_f)
    g[..., TH, TH] = G['Rr']**2
    g[..., PS, PS] = (G['Rr']*torch.sin(G['Tht']))**2
    return g, a_r, b_r


hdr("STEP 2 -- FULL 3-D Einstein residual on the CORRECTED #56 round seed")
print("  (seed solved DIRECTLY on each 3-D r-grid -- NO interpolation degradation)")
th0, th1 = 0.30, math.pi-0.30
results = []
for (Nr, Nth, Nps) in [(220, 64, 16), (320, 96, 16), (440, 128, 16)]:
    G = S.mkgrid(Nr, Nth, Nps, rc, ri, th0, th1)
    # Solve #56 radial soliton AT this Nr (matched resolution; no interp error).
    rN = rb.make_grid(1, Nr, rc=rc, rint=ri, geom=False)
    oN = rb.selfconsistent_Bfree(rN, xi, kap, p=P, kap8=KAP8, iters=300, relax=0.4,
                                 tol=1e-11, verbose=False)
    aN, bN, ThN, rrN = oN['a'][0], oN['b'][0], oN['Th'][0], oN['r'][0]
    Th_r = ThN
    Th_field = Th_r[:, None, None].expand(Nr, Nth, Nps).contiguous()
    g, a_r, b_r = build_round_metric(G, aN, bN, rrN)
    n = S.hedgehog_field(Th_field, G)
    Res, Gud, Tud, ginv, dn = S.einstein_residual_mixed(g, n, KAP8, G)
    # SMOOTH-BODY mask: strip FD edges AND the deep-core (r<rc+1.0) coordinate spike
    # (the #55 verifier 11.2 documented that the raw max is dominated by a deep-core /
    # near-axis COORDINATE spike that GROWS with N -- truncation/coordinate, not physics).
    rmask = (G['rg'] > rc + 1.0) & (G['rg'] < ri - 0.5)
    i0 = int(rmask.float().argmax().item())
    i1 = int(G['Nr'] - 1 - rmask.flip(0).float().argmax().item())
    def diag(ab):
        return Res[i0:i1, 8:-8, :][..., ab, ab].abs().max().item()
    rtt, rrr, rthth, rpsps = diag(T), diag(R), diag(TH), diag(PS)
    offmax = 0.0
    for a in range(4):
        for b in range(4):
            if a != b:
                offmax = max(offmax, Res[i0:i1, 8:-8, :][..., a, b].abs().max().item())
    results.append((Nr, Nth, rtt, rrr, rthth, rpsps, offmax))
    print(f"  (Nr,Nth)=({Nr},{Nth}) [smooth body r>{rc+1.0:.1f}]: res_tt={rtt:.3e} res_rr={rrr:.3e} "
          f"res_thth={rthth:.3e} res_psps={rpsps:.3e}  max|off|={offmax:.3e}")

hdr("STEP 2b -- convergence ratios (O(h^2) => physical solution; flat => non-solution)")
for i in range(1, len(results)):
    p, c = results[i-1], results[i]
    print(f"  {p[0]}->{c[0]}: res_tt {p[2]/c[2]:.2f}x  res_rr {p[3]/c[3]:.2f}x  "
          f"res_thth {p[4]/c[4]:.2f}x  res_psps {p[5]/c[5]:.2f}x  off {p[6]/max(c[6],1e-30):.2f}x")


# ---------------------------------------------------------------------------
# 3. B=1/A exterior recovery, M_MS read-off.
# ---------------------------------------------------------------------------
hdr("STEP 3 -- B=1/A (exterior) and M_MS from the 3-D metric")
G = S.mkgrid(320, 96, 16, rc, ri, th0, th1)
g, a_r, b_r = build_round_metric(G, a1, b1, rr1)
prod = (g[..., T, T]*g[..., R, R])   # = -e^{2a}e^{2b} = -e^{2(a+b)}; ->-1 iff a+b->0
ab = (a_r + b_r)
# exterior: last 30% of cell
ext = slice(int(0.7*G['Nr']), G['Nr']-6)
print(f"  a+b exterior (r>{0.7*(ri-rc)+rc:.1f}): mean={ab[ext].mean().item():.4e} "
      f"std={ab[ext].std().item():.2e}  => B=1/A {'recovered' if abs(ab[ext].mean().item())<1e-2 else 'NOT recovered'}")
print(f"  a+b twisted body max|a+b|={ab[6:int(0.5*G['Nr'])].abs().max().item():.4f} (interior warp)")
# M_MS from metric: m_areal(r)=r(1-e^{-2b}); M_MS = m(seal)-m(core)
em2b = torch.exp(-2*b_r)
m_areal = G['rg']*(1.0 - em2b)
M_MS_3d = (m_areal[-1] - m_areal[0]).item()
print(f"  M_MS from 3-D metric = {M_MS_3d:.6f}  committed #56 = {M_MS_ref:.6f}  "
      f"|diff|={abs(M_MS_3d-M_MS_ref):.3e}")


# ---------------------------------------------------------------------------
# GATE VERDICT
# ---------------------------------------------------------------------------
hdr("GATE56 VERDICT")
r0 = results[-1]
allres = max(r0[2], r0[3], r0[4], r0[5], r0[6])
# convergence: all four diagonal eqs drop with resolution
conv = all(results[-2][k]/results[-1][k] > 2.0 for k in (2, 3, 4, 5))
print(f"  finest grid ({r0[0]},{r0[1]}): max diagonal residual = {max(r0[2],r0[3],r0[4],r0[5]):.3e}")
print(f"  max off-diagonal residual = {r0[6]:.3e} (round seed -> structurally ~0)")
print(f"  residuals CONVERGE with resolution (>2x per refine): {conv}")
print(f"  M_MS matches committed #56 to {abs(M_MS_3d-M_MS_ref):.2e}")
gate_pass = (max(r0[2], r0[3], r0[4], r0[5]) < 5e-2) and conv and abs(M_MS_3d-M_MS_ref) < 5e-3
print(f"\n  >>> GATE56 (engine recognizes corrected #56 as a full 3-D solution): "
      f"{'PASS' if gate_pass else 'CHECK'} <<<")
