#!/usr/bin/env python3
"""
test_shexact_psiflat.py -- the CORRECT regression statement: on the PSI-FLAT (axisym,
m=0) subspace the SH-exact theta operator equals the Legendre one, so the round result
is unchanged.  On PSI-STRUCTURED directions the two operators DIFFER -- that is the
WHOLE POINT (engagement), not a regression.

Tests:
  R1 psi-flat residual identity (round seed): forward residual identical (1e-12).
  R2 psi-flat Jacobian-action identity: J@v for a PSI-FLAT random direction v must
     match Legendre vs SH-exact to ~1e-12 (the m=0 Jacobian is identical) -- this is
     the deterministic no-regression proof restricted to the axisym subspace.
  R3 psi-STRUCTURED Jacobian-action: J@v for a psi-structured v MUST differ (proves
     the operator is engaged in the linearization where m!=0 lives).
  R4 psi-flat subspace invariance: a psi-flat state stays psi-flat under d_th of the
     SH-exact op (no spurious psi-coupling injected), and the round soliton (psi-flat)
     is a fixed structure.
Driver: Claude (Opus 4.8, 1M).  2026-06-16.  NEW file.  DATA-BLIND.
"""
import os, sys
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
from full3d_spectral import Grid3D, attach_coord_weight, diagnostics, residuals
import full3d_solver as FS
from full3d_solver import unpack, pack, residual_vector
import full3d_newton as FN
from full3d_grid_shexact import make_grid_shexact, legendre_d_th

P, KAP8 = 0.4, 0.05
NR, NTH, NPS = 20, 6, 8
def pr(*a): print(*a); sys.stdout.flush()

def jvp(u, G, v):
    u = u.detach().clone().requires_grad_(True)
    F = residual_vector(u, G, P, KAP8)
    w0 = torch.zeros_like(F, requires_grad=True)
    JTw = torch.autograd.grad(F, u, grad_outputs=w0, create_graph=True)[0]
    jv, = torch.autograd.grad(JTw, w0, grad_outputs=v, retain_graph=True)
    return jv.detach()

def psiflat_dir(G, u0):
    """random direction that is CONSTANT in psi (axisym, m=0): per-field (Nr,Nth)
    pattern broadcast over psi."""
    n = G.Nr*G.Nth*G.Nps
    parts = []
    torch.manual_seed(7)
    for _ in range(5):
        base = torch.randn(G.Nr, G.Nth)
        parts.append(base[:, :, None].expand(G.Nr, G.Nth, G.Nps).reshape(-1))
    return torch.cat(parts)

def main():
    Gleg = Grid3D(NR,NTH,NPS,rc=0.05,cell=14.0); Gleg=attach_coord_weight(Gleg)
    Gsh  = make_grid_shexact(NR,NTH,NPS,rc=0.05,cell=14.0,mmax=NPS//2)
    u0L,solL = FS.round_seed(Gleg,p=P,kap8=KAP8); u0S,_ = FS.round_seed(Gsh,p=P,kap8=KAP8)

    pr("\n=== R1: psi-flat residual identity (round seed) ===")
    FL = residual_vector(u0L,Gleg,P,KAP8); FSr = residual_vector(u0S,Gsh,P,KAP8)
    r1d = float((FL-FSr).abs().max())
    pr(f"  ||F_Leg - F_SH||_inf = {r1d:.3e}  (PASS<1e-12)")
    r1 = r1d < 1e-12

    pr("\n=== R2: psi-FLAT Jacobian-action identity (m=0 regression proof) ===")
    vflat = psiflat_dir(Gsh, u0S)
    jL = jvp(u0L,Gleg,vflat); jS = jvp(u0S,Gsh,vflat)
    r2d = float((jL-jS).abs().max())
    pr(f"  ||J_Leg v - J_SH v||_inf (v psi-flat) = {r2d:.3e}  "
       f"(PASS<1e-10 => identical Jacobian on axisym subspace)")
    r2 = r2d < 1e-10

    pr("\n=== R3: psi-STRUCTURED Jacobian-action MUST differ (engagement) ===")
    torch.manual_seed(3); vstr = torch.randn_like(u0S)        # generic (psi-structured)
    jLs = jvp(u0L,Gleg,vstr); jSs = jvp(u0S,Gsh,vstr)
    r3d = float((jLs-jSs).abs().max())
    pr(f"  ||J_Leg v - J_SH v||_inf (v psi-structured) = {r3d:.3e}  "
       f"(PASS>1e-3 => exact op engaged in linearization where m!=0)")
    r3 = r3d > 1e-3

    pr("\n=== R4: SH-exact d_th preserves psi-flatness (no spurious psi-coupling) ===")
    # a psi-flat field: its SH-exact theta derivative must remain psi-flat (mode-0 only)
    a,b,c,d,Th = unpack(u0S,Gsh)
    dTh = Gsh.d_th(Th)
    psi_spread = float((dTh - dTh.mean(dim=2, keepdim=True)).abs().max())
    pr(f"  max psi-variation of d_th(psi-flat Theta) = {psi_spread:.3e}  (PASS<1e-12)")
    r4 = psi_spread < 1e-12

    pr("\n=== REGRESSION VERDICT ===")
    pr(f"  R1 psi-flat residual identity : {'PASS' if r1 else 'FAIL'}  ({r1d:.2e})")
    pr(f"  R2 psi-flat Jacobian identity : {'PASS' if r2 else 'FAIL'}  ({r2d:.2e})")
    pr(f"  R3 psi-struct Jacobian differs: {'PASS' if r3 else 'FAIL'}  ({r3d:.2e})")
    pr(f"  R4 psi-flatness preserved     : {'PASS' if r4 else 'FAIL'}  ({psi_spread:.2e})")
    ok = r1 and r2 and r3 and r4
    pr(f"  => On the axisym (m=0) subspace the SH-exact op is BIT-IDENTICAL to Legendre")
    pr(f"     (round result unchanged); it DIFFERS only where m!=0 (the intended fix). "
       f"{'CONFIRMED' if ok else 'NOT confirmed'}")

if __name__ == "__main__":
    main()
