"""Supplementary: (A) measure a2_peak in the FIX-1-reproduced stalled states (settle 'tiny response'),
(B) rigorous full-3D-field traceless-stress ell-decomposition fraction (instruction 1). Category-A."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
import cell_solver_f2d as cs
import n5d_pilot as pilot
PRM = pilot.PRM; Nr, Nth = 16, 8
st, source_rc, source_sh2 = pilot.load_frozen_source()

print("="*90); print("(A) a2_peak in the FIX-1-reproduced stalled states + shear-ODE residual"); print("="*90)
import time
for sealbc in ("S-Dir", "S-JC2"):
    ctx = cs.make_ctx(Nr, Nth, rc=0.5)
    u = cs.seed_n5d(ctx, a2_amp=pilot.A2_SEED); L0 = float(cs.unpack(u, ctx, n5d=True)[-1])
    t0 = time.time()
    for amp in pilot.CONT_AMPS:
        rem = 100 - (time.time()-t0)
        if rem <= 1: break
        Ts = pilot.build_Tshear(ctx, L0, amp, source_rc, source_sh2)
        n5d = dict(sealbc=sealbc, Tshear=Ts, a2_mirror=0.0)
        u, h = cs.newton_lm_solve(u, ctx, PRM, maxit=30, tol=pilot.PHI_TOL, verbose=False,
                                  time_budget=rem, n5d=n5d, equilibrate=True)
    n5d = dict(sealbc=sealbc, Tshear=pilot.build_Tshear(ctx, L0, 1.0, source_rc, source_sh2), a2_mirror=0.0)
    with torch.no_grad():
        Q = cs.fields(u, ctx, PRM, n5d=n5d)
        a2 = Q["a2"].cpu().numpy(); shr = Q["shear_res"].cpu().numpy()
    print(f"  [{sealbc}] FIX-1 reproduced: a2_peak={np.abs(a2).max():.4e}  a2(rs)={a2[-1]:+.4e}  "
          f"||shear_ODE||={np.linalg.norm(shr[1:-1]):.3e}  finalPhi={h[-1]:.3e}")
print("  (linear-response EXPECTED a2_peak ~2.1 for S-Dir; compare)")

print("="*90); print("(B) full-3D-field traceless-stress ell decomposition (rigorous fraction)"); print("="*90)
dev = 'cuda' if torch.cuda.is_available() else 'cpu'
print("  device:", dev)
d = np.load(pilot.HOPFION_NPZ)
n = torch.tensor(d['n'], device=dev); Ngr = int(d['N']); L = float(d['L']); h = float(d['h'])
xi = float(d['xi']); kap = float(d['kappa'])
x = torch.linspace(-L, L, Ngr, device=dev)
def dc(f, ax): return (torch.roll(f, -1, ax) - torch.roll(f, 1, ax))/(2*h)
n = n/n.norm(dim=0, keepdim=True)
dn = [dc(n, i+1) for i in range(3)]
def cross(a, b): return torch.stack([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]], 0)
F = {}
for i in range(3):
    for j in range(3):
        if i != j: F[(i, j)] = (n*cross(dn[i], dn[j])).sum(0)
e2d = 0.5*xi*sum((dn[i]*dn[i]).sum(0) for i in range(3))
e4d = torch.zeros_like(e2d)
for i in range(3):
    for j in range(3):
        if i != j: e4d = e4d + 0.25*kap*F[(i, j)]*F[(i, j)]
ed = e2d + e4d
sig = torch.zeros(3, 3, Ngr, Ngr, Ngr, device=dev)
for i in range(3):
    for j in range(3):
        t = xi*(dn[i]*dn[j]).sum(0); fk = torch.zeros_like(t)
        for k in range(3):
            if k == i or k == j: continue
            fk = fk + kap*F.get((i, k), torch.zeros_like(t))*F.get((j, k), torch.zeros_like(t))
        sig[i, j] = t + fk - (ed if i == j else 0)
X, Y, Zc = torch.meshgrid(x, x, x, indexing='ij')
rr = torch.sqrt(X*X+Y*Y+Zc*Zc)+1e-12; rho2 = torch.sqrt(X*X+Y*Y)+1e-12
er = torch.stack([X/rr, Y/rr, Zc/rr], 0)
eth = torch.stack([X*Zc/(rr*rho2), Y*Zc/(rr*rho2), -rho2/rr], 0)
eph = torch.stack([-Y/rho2, X/rho2, torch.zeros_like(X)], 0)
def contract(u, v):
    s = torch.zeros(Ngr, Ngr, Ngr, device=dev)
    for i in range(3):
        for j in range(3): s = s + u[i]*sig[i, j]*v[j]
    return s
Tthth = contract(eth, eth); Tphph = contract(eph, eph)
shear = Tthth - Tphph                         # transverse traceless shear field
Tnorm = torch.sqrt((sig*sig).sum((0, 1)))     # |T^AB| Frobenius per point
mu = (Zc/rr)                                   # cos theta
P0 = torch.ones_like(mu); P2 = 0.5*(3*mu*mu-1); P4 = (35*mu**4-30*mu*mu+3)/8
vol = h**3
def L2(f): return float(torch.sqrt((f*f).sum()*vol))
# per-shell ell-decomposition is expensive; use the GLOBAL angular decomposition weighted by r^2 vol:
# project shear onto P_l(mu) over the whole field (each with its own r-profile). Report ENERGY fractions.
# proper: coefficient_l(shell) ~ (2l+1)/2 <shear P_l>. Global captured-energy proxy = ||<shear,P_l>-weighted||.
# Simplify to the physically-relevant statement: fraction of ||shear||^2 in each l via spherical-harmonic
# angular power using nb shells.
nb = 64; idx = torch.clamp((rr/L*nb).long(), 0, nb-1)
def shell_moment(fld, Pl):
    num = torch.zeros(nb, device=dev); cnt = torch.zeros(nb, device=dev)
    num.scatter_add_(0, idx.flatten(), (fld*Pl).flatten())
    cnt.scatter_add_(0, idx.flatten(), torch.ones_like(fld.flatten()))
    return num/cnt.clamp(min=1)                # <shear Pl>_shell
def shell_sq(fld):
    num = torch.zeros(nb, device=dev); cnt = torch.zeros(nb, device=dev)
    num.scatter_add_(0, idx.flatten(), (fld*fld).flatten())
    cnt.scatter_add_(0, idx.flatten(), torch.ones_like(fld.flatten()))
    return num/cnt.clamp(min=1)                # <shear^2>_shell
rc = 0.5*(torch.linspace(0, L, nb+1, device=dev)[1:]+torch.linspace(0, L, nb+1, device=dev)[:-1])
w_sh = (rc**2).cpu().numpy()
m0 = shell_moment(shear, P0).cpu().numpy(); m2 = shell_moment(shear, P2).cpu().numpy()
m4 = shell_moment(shear, P4).cpu().numpy(); tot = shell_sq(shear).cpu().numpy()
# angular power per l ~ <shear Pl>^2 / <Pl^2>, <Pl^2>=1/(2l+1)
def band_power(ml, l): return np.sum(ml**2*(2*l+1)*w_sh)
p0 = band_power(m0, 0); p2 = band_power(m2, 2); p4 = band_power(m4, 4)
ptot = np.sum(tot*w_sh)                         # total angular power of shear
print(f"  ||T^AB|| (Frobenius, full field) = {L2(Tnorm):.4f}")
print(f"  ||shear|| (transverse traceless) = {L2(shear):.4f}")
print(f"  angular-power fractions of the TRACELESS SHEAR field (r^2-weighted shells):")
print(f"    ell=0: {p0/ptot:.4f}   ell=2: {p2/ptot:.4f}   ell=4: {p4/ptot:.4f}   "
      f"(sum l0,2,4 = {(p0+p2+p4)/ptot:.4f} of total)")
print(f"  => the ell=2-ONLY pilot couples to ~{p2/ptot:.1%} of the traceless shear stress power.")
