import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np, torch, math
torch.set_default_dtype(torch.float64)
import spectral_catalog_solver as S
from spectral_catalog_solver import (TGrid, unpack, pack, diagnostics, round_seed,
    residual_vector, lm_solve_dense, PI, DEV, matter_el_t as EL_committed)
from VERIF_torch_correct import matter_el_correct_t as EL_correct

G = TGrid(28, 6, rc=0.05, cell=14.0)
u0, rad = round_seed(G, p=0.4, kap8=0.05)


def legP(l, x):
    from numpy.polynomial.legendre import Legendre
    cc = np.zeros(l+1); cc[l] = 1.0
    return Legendre(cc)(x)


body = (G.R > 0.8) & (G.R < G.ri-0.8)
print("Solve each seed with COMMITTED solver (committed EL) then evaluate CORRECT EL")
print("on the committed 'relaxed' solution. Large CORRECT EL => committed null is an")
print("artifact (state is not a true solution).\n")
print(f"{'seed':>8} {'committed_Phi':>13} {'tvar':>10} {'committed_EL':>13} {'CORRECT_EL':>12}")
for kind in ['round', 'l1', 'l2', 'l3', 'l4']:
    a, b, c, d, Th = unpack(u0, G)
    a = a.clone(); b = b.clone(); c = c.clone(); d = d.clone(); Th = Th.clone()
    if kind != 'round':
        Pl = torch.tensor(legP(int(kind[1:]), G.CTH.cpu().numpy()), device=DEV)
        Th = Th + 0.30*torch.exp(-((G.R-2.0)/1.5)**2)*Pl
        Th[0, :] = PI; Th[-1, :] = 0.0
    u = pack(a, b, c, d, Th)
    for _ in range(5):
        u, rf, h = lm_solve_dense(u, G, 0.4, 0.05, maxit=12, lam0=1e-4)
    dg = diagnostics(G, rf, 0.05)
    F = residual_vector(u, G, 0.4, 0.05)[0]
    a2, b2, c2, d2, Th2 = unpack(u, G)
    el_c = EL_committed(G, Th2, a2, b2, c2, d2)
    el_corr = EL_correct(G, Th2, a2, b2, c2, d2)
    print(f"{kind:>8} {float((F**2).sum()):>13.3e} {dg['tvar']:>10.3e} "
          f"{float(el_c[body].abs().max()):>13.3e} {float(el_corr[body].abs().max()):>12.3e}")
