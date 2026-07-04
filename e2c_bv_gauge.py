"""BV attack #2: independently re-derive the translation-gauge diagnosis.
Build the MMS, compute J at the root v*, and check:
  - cos angle between dF/dr_p and dF/dr_sU columns (claim: -1.000000)
  - finite-difference ratio dF/dr_p vs dF/dr_sU (claim -1.0000, ~1e-4 broken)
  - sigma_min, sigma_max, cond raw (claim sigma_min~2.2e-9, cond~3.6e16)
  - energy of softest singular direction on (r_p,r_sU) vs fields (claim 0.5/0.5)
  - cond after Ruiz equilibration (claim ~1.9e7); col-only (claim ~5.7e11)
  - Tikhonov: can any lambda control the slide? (attenuation sigma^2/(sigma^2+lam))
"""
import os, math
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np, torch
torch.set_default_dtype(torch.float64)
import cell_solver_composite as C
from torch.func import jacrev

DEV = "cuda" if torch.cuda.is_available() else "cpu"
Nr, Nth, Na, KMAP = 12, 8, 192, 2.5

br = C.load_bracket("A1 m=3 Z=8"); prm = (br["Z"], 0.5, 0.1, 1)
ctx = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device=DEV)
rp0 = 0.95 * br["r_s"]

def genericize(v):
    phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = C.unpack_comp(v, ctx)
    z = ctx["cell"]["zeta"].to(DEV); mu = ctx["cell"]["mu"].to(DEV); h = ctx["ha"].to(DEV)
    phi_c = phi_c + 0.05*torch.cos(math.pi*z)
    rho_c = rho_c + 0.03*torch.sin(0.5*math.pi*(z+1.0))
    uf = uf + 0.05*(1.0-mu[None,:]**2)*mu[None,:]*torch.cos(math.pi*(z[:,None]+1.0))
    phi_a = phi_a + 0.02*torch.sin(math.pi*h)
    rho_a = rho_a + 0.01*h*(1.0-h)
    return C.pack_comp(phi_c, rho_c, uf, phi_a, rho_a, float(r_p), float(r_sU), device=DEV)

v_star = genericize(C.seed_comp(ctx, br, rp0=rp0, amp=0.8, device=DEV))
F_star = C.residual_comp(v_star, ctx, prm, br).detach()
resfn = lambda vv: C.residual_comp(vv, ctx, prm, br) - F_star
n = v_star.numel()
print(f"n={n}  root max|F(v*)|={float(resfn(v_star).abs().max()):.3e}")

# Jacobian at root
J = jacrev(resfn)(v_star).detach().cpu().numpy().astype(np.float64)
print("J shape", J.shape)

# boundary columns are the last two (r_p, r_sU) per unpack ordering
cp = J[:, n-2]; csU = J[:, n-1]
cos = float(cp @ csU / (np.linalg.norm(cp)*np.linalg.norm(csU)))
print(f"cos(dF/dr_p, dF/dr_sU) = {cos:.6f}   (claim -1.000000)")
# ratio: best-fit scalar k s.t. cp ~ k*csU
k = float(cp @ csU / (csU @ csU))
resid_frac = float(np.linalg.norm(cp - k*csU)/np.linalg.norm(cp))
print(f"cp ~ {k:.4f} * csU ; anti-collinearity residual frac = {resid_frac:.3e}  (claim k=-1.0000, ~1e-4)")

# SVD
U_, s, Vt = np.linalg.svd(J)
print(f"sigma_max={s[0]:.3e}  sigma_min={s[-1]:.3e}  raw cond={s[0]/s[-1]:.3e}  (claim ~3.6e16)")
vsoft = Vt[-1]
e_bnd = vsoft[n-2]**2 + vsoft[n-1]**2
print(f"softest dir energy on (r_p,r_sU) = {e_bnd:.4f}  on fields = {1-e_bnd:.4f}  (claim 0.5/0.5)")
print(f"   components r_p={vsoft[n-2]:.4f}  r_sU={vsoft[n-1]:.4f}")

# col-only scaling cond
cs = np.abs(J).max(0); cs[cs<1e-30]=1.0
Jc = J/cs
print(f"cond after COL-ONLY scaling = {np.linalg.cond(Jc):.3e}  (claim ~5.7e11)")

# Ruiz two-sided
dr, dc = C._ruiz_equilibrate(J)
Aeq = dr[:,None]*J*dc[None,:]
print(f"cond after RUIZ (row+col) = {np.linalg.cond(Aeq):.3e}  (claim ~1.9e7)")
sig_soft_eq = np.linalg.svd(Aeq, compute_uv=False)[-1]
print(f"equilibrated sigma_min = {sig_soft_eq:.3e}  (claim ~4.4e-7)")

# Tikhonov dilemma: attenuation of soft mode sigma^2/(sigma^2+lam), using equilibrated sigma
for lam in [1e-14, 1e-13, 1e-12, 1e-10]:
    att = sig_soft_eq**2/(sig_soft_eq**2+lam)
    print(f"   lam={lam:.0e}: soft-mode retained fraction = {att:.3e}")
