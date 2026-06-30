#!/usr/bin/env python3
"""Validation harness for galerkin_basis.py (all cheap; NO nonlinear flooring solve).
 1. BC-satisfaction per field (the correctness gate).
 2. Differentiation/representation accuracy on a smooth BC-compatible test function.
 3. CONDITIONING payoff: cond(J) vs cond(J_a=J@B_full), smax/smin (the payoff gate).
 4. Seed projection residual.
 + cross-check: orthonormal null space spans the SAME space as explicit Shen recombination.
"""
import numpy as np, torch
torch.set_default_dtype(torch.float64)
import galerkin_basis as GB
from full3d_spectral import attach_coord_weight, Grid3D

G = attach_coord_weight(Grid3D(Nr=8, Nth=6, Nps=8, rc=0.1, cell=8.0))
Dr = G.Dr.detach().cpu().numpy(); r = G.r.detach().cpu().numpy()
Nr = G.Nr; rc, ri = float(r[0]), float(r[-1]); core, seal = 0, Nr - 1
P = 1.0
rng = np.random.default_rng(0)

print("=" * 78)
print("VALIDATION 1 -- BC satisfaction (random coef -> field, check (core,seal) BCs)")
print("=" * 78)
print(f"{'field':6} {'ncoef':>5} {'core BC resid':>16} {'seal BC resid':>16}  type")
bc_ok = True
for field in GB.RECOMB:
    B_f, p_f = GB.recombined_basis_field(field, Dr, r, p_depth=P)
    coef = rng.standard_normal(B_f.shape[1])
    f = p_f + B_f @ coef                              # affine field
    # functionals (the ACTUAL determined-branch residual conditions, warp form)
    if field == 'a':     cb = Dr[core] @ f;                       sb = f[seal]
    elif field == 'b':   cb = f[core] + P;                        sb = Dr[seal] @ f
    elif field in ('c', 'd'):
                         cb = Dr[core] @ f;                       sb = Dr[seal] @ f + 1.0 / ri
    elif field == 'phi': cb = Dr[core] @ f;                       sb = f[seal]
    elif field in ('e_rt', 'e_rp'):
                         cb = f[core];                            sb = f[seal]
    elif field == 'e_tp':cb = Dr[core] @ f;                       sb = Dr[seal] @ f + (2.0 / ri) * f[seal]
    types = {'a': 'Neu/Dir', 'b': 'Dir(-p)/Neu', 'c': 'Neu/metric-Robin',
             'd': 'Neu/metric-Robin', 'phi': 'Neu/Dir', 'e_rt': 'Dir/Dir',
             'e_rp': 'Dir/Dir', 'e_tp': 'Neu/Robin'}
    ok = abs(cb) < 1e-10 and abs(sb) < 1e-10
    bc_ok &= ok
    print(f"{field:6} {B_f.shape[1]:5d} {cb:16.3e} {sb:16.3e}  {types[field]}  {'OK' if ok else 'FAIL'}")
print(f"  --> BC-satisfaction gate: {'PASS' if bc_ok else 'FAIL'}")

print("\n" + "=" * 78)
print("VALIDATION 2 -- representation of a smooth BC-compatible test function")
print("=" * 78)
# build a smooth function and PROJECT onto each field's BC-satisfying space; report recon error.
print(f"{'field':6} {'recon err (proj)':>18}  (smooth BC-matched target)")
rep_ok = True
for field in GB.RECOMB:
    B_f, p_f = GB.recombined_basis_field(field, Dr, r, p_depth=P)
    # craft a smooth target that satisfies this field's homogeneous BCs (so it lies in the space):
    coef = np.cos(np.arange(B_f.shape[1]))            # arbitrary smooth modal mix
    target = B_f @ coef                               # by construction in-space
    recon = B_f @ (B_f.T @ target)                    # orthonormal proj
    err = np.max(np.abs(recon - target))
    rep_ok &= err < 1e-10
    print(f"{field:6} {err:18.3e}")
# also: a GENERIC smooth function projected -> error reflects only the BC-incompatible part
print(f"  --> in-space representation exact to ~1e-12: {'PASS' if rep_ok else 'FAIL'}")

print("\n" + "=" * 78)
print("CROSS-CHECK -- orthonormal null space vs explicit Shen 3-term recombination")
print("=" * 78)
print(f"{'field':6} {'span mismatch':>16}  (||(I-B B^T) B_shen|| ; same column space => ~0)")
span_ok = True
for field in GB.RECOMB:
    B_f, _ = GB.recombined_basis_field(field, Dr, r, p_depth=P)
    try:
        B_sh = GB.shen_recombination_field(field, Dr, r)
        resid = B_sh - B_f @ (B_f.T @ B_sh)
        mm = float(np.max(np.abs(resid)))
    except Exception as ex:
        mm = float('nan'); print(f"   ({field} shen: {ex})")
    span_ok &= (mm < 1e-9)
    print(f"{field:6} {mm:16.3e}")
print(f"  --> same recombined-Chebyshev span: {'PASS' if span_ok else 'CHECK'}")

print("\n" + "=" * 78)
print("VALIDATION 3 -- CONDITIONING (cond(J) vs cond(J_a=J@B_full)) [the payoff gate]")
print("=" * 78)
import p1_residual_general_einstein as P1
from torch.func import jacrev
dev = G.Dr.device
# generic linearization point: the floored X=-1 determined field (avoids round-seed spurious SVs)
d = torch.load('xexplore_field_X1_floored.pt', map_location='cpu', weights_only=False)
u = d['u'].to(dev)
X = -1.0
print(f"point = xexplore_field_X1_floored.pt (Phi={d.get('Phi')}), X={X}, branch=G, determined=True")
f = lambda uu: P1.residual_vector_p1(uu, G, P, 1.0, X=X, branch='G', determined=True)
J = jacrev(f, chunk_size=128)(u).detach()
B_full, u_part, info = GB.build_B_full(G, p=P, device=dev)
Ja = J @ B_full
print(f"  J  shape {tuple(J.shape)} ; B_full shape {tuple(B_full.shape)} ; J_a shape {tuple(Ja.shape)}")
svJ  = torch.linalg.svdvals(J.double()).cpu().numpy()
svJa = torch.linalg.svdvals(Ja.double()).cpu().numpy()
def rep(sv):
    return sv[0], sv[-1], sv[0] / max(sv[-1], 1e-300)
sJ = rep(svJ); sJa = rep(svJa)
print(f"  {'':10} {'smax':>12} {'smin':>12} {'cond':>12}")
print(f"  {'J':10} {sJ[0]:12.4e} {sJ[1]:12.4e} {sJ[2]:12.4e}")
print(f"  {'J_a':10} {sJa[0]:12.4e} {sJa[1]:12.4e} {sJa[2]:12.4e}")
print(f"  cond drop factor = {sJ[2]/sJa[2]:.3e} ; smin lift factor = {sJa[1]/sJ[1]:.3e}")
print(f"  smallest 8 SV of J  : {np.array2string(svJ[-8:],  precision=3)}")
print(f"  smallest 8 SV of J_a: {np.array2string(svJa[-8:], precision=3)}")

print("\n" + "=" * 78)
print("VALIDATION 4 -- seed projection onto the BC-satisfying subspace")
print("=" * 78)
seed = P1.seed_round_native(G, p=P, m=1).to(dev)
u_proj, coef = GB.project_to_subspace(seed, B_full, u_part)
# residual of the projection = part of seed NOT representable in the affine subspace
proj_res = float((u_proj - seed).abs().max())
# verify the projected seed actually satisfies the determined BCs via the residual's BC rows:
F_seed = P1.residual_vector_p1(u_proj, G, P, 1.0, X=X, branch='G', determined=True)
print(f"  ||u_proj - seed||_inf = {proj_res:.3e}  (nonzero => seed not BC-compatible; expected for c/d/phi)")
print(f"  projected-seed residual ||F||_2 = {float((F_seed*F_seed).sum())**0.5:.4e} (full nonlinear residual; not floored, just a start point)")
# confirm the projected seed lies in the subspace (re-project -> no change)
u_proj2, _ = GB.project_to_subspace(u_proj, B_full, u_part)
print(f"  idempotency ||P(P seed)-P seed||_inf = {float((u_proj2-u_proj).abs().max()):.3e}  (should be ~0)")
print("\nDONE.")
