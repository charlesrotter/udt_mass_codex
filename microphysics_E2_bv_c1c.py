"""microphysics_E2_bv_c1c.py -- BLIND VERIFIER attack 3: the C1c theta-sawtooth -- functional
obstruction vs discretization pathology.

Probes (on the representative stalled case A1Z8 W1/wall/amp0.8, from its saved .pt):
 (a) MODAL anatomy: Legendre-coefficient content of f_r(seal, theta) -- is the holdout residual
     concentrated in the top resolved modes (grid-scale) or spread (functional)?
 (b) u-SUBSYSTEM square solve at FROZEN geometry (phi, rho, r_p from the end state): unknowns u
     only; rows = f-PDE interior + core f_r + C1c. Directly tests the claimed "C1c and the f-PDE
     fight". Run at Nth = 8 and Nth = 16 (band-limited interpolation).
 (c) FULL-system re-run at Nth = 16 from the interpolated end state (bounded LM): does the
     sawtooth persist at grid scale with non-decreasing amplitude?
 (d) INDEPENDENT theta-discretization: same Legendre modal space, DIFFERENT collocation nodes
     (Chebyshev-Gauss interior mu-nodes) + exact modal quadrature -- re-run the u-subsystem.
Bounded, single process, GPU for solves w/ CPU assembly checks. NOT committed.
"""
import os, math, time
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import numpy as np
from numpy.polynomial import legendre as _leg
import torch
torch.set_default_dtype(torch.float64)
import cell_solver_composite as C
import cell_solver_f2d as F2D

DEV = "cuda" if torch.cuda.is_available() else "cpu"
LAB = "A1 m=3 Z=8"
br = C.load_bracket(LAB)
d = torch.load("E2b_A1Z8_P2_W1_wall.pt", map_location="cpu", weights_only=False)
prm = tuple(d["prm"])
Nr, Nth, Na, KMAP = d["Nr"], d["Nth"], d["Na"], d["kmap"]
ctx = C.make_ctx_comp(Nr, Nth, Na, kmap=KMAP, device="cpu")
w = d["w"].to(torch.float64)
phi_c, rho_c, uf, phi_a, rho_a, r_p, r_sU = C.unpack_comp(w, ctx)
print(f"state: {d['tag']}  r_p={float(r_p):.2f} r_sU={float(r_sU):.2f}")

# ---------------- (a) modal anatomy of the sawtooth ----------------
Q, v_cell = C.cell_fields(w, ctx, prm)
fr_seal = Q["fr"][-1, :].detach().numpy()
mu = ctx["cell"]["mu"].cpu().numpy()
S = np.zeros((Nth, Nth))
for j in range(Nth):
    ej = np.zeros(j + 1); ej[j] = 1.0
    S[:, j] = _leg.legval(mu, ej)
coef = np.linalg.solve(S, fr_seal)
print("\n(a) f_r(seal, theta_k) =", np.array2string(fr_seal, precision=3))
print("    Legendre modal coefficients c_j (j=0..%d):" % (Nth-1),
      np.array2string(coef, precision=3))
frac_top2 = (coef[-2:]**2).sum() / (coef**2).sum()
print(f"    energy fraction in top-2 modes (j={Nth-2},{Nth-1}): {frac_top2:.3f}")

# ---------------- u-subsystem machinery ----------------
def make_cell_ctx_nodes(Nr_, Nth_, device):
    return F2D.make_ctx(Nr_, Nth_, rc=0.0, device=device)

def u_subsystem_residual(u_flat, cellctx, phi_f, rho_f, rp_f, prm_):
    v_cell = torch.cat([phi_f, rho_f, u_flat, rp_f.reshape(1)])
    Q_ = F2D.fields(v_cell, cellctx, prm_)
    rows = [Q_["res_f"][1:-1].reshape(-1), Q_["fr"][0, :], Q_["fr"][-1, :]]
    return torch.cat([r.reshape(-1) for r in rows])

def solve_u_subsystem(cellctx, u0, phi_f, rho_f, rp_f, prm_, maxit=600, budget=240.0, tag=""):
    resfn = lambda uu: u_subsystem_residual(uu, cellctx, phi_f, rho_f, rp_f, prm_)
    F0 = resfn(u0)
    t0 = time.time()
    wsol, info = C.lm_qr(resfn, u0.detach().cpu().numpy(), maxit=maxit,
                         device=phi_f.device.type, time_budget=budget)
    wt = torch.as_tensor(np.asarray(wsol, dtype=float), device=phi_f.device)
    Ff = resfn(wt).detach()
    Nth_ = cellctx["Nth"]
    c1c = Ff[-Nth_:].cpu().numpy()
    print(f"  [{tag}] n={u0.numel()} seed maxF={float(F0.abs().max()):.2e} -> iters={info['iters']} "
          f"({time.time()-t0:.1f}s) end maxF={float(Ff.abs().max()):.3e} "
          f"C1c rows: {np.array2string(c1c, precision=2)}")
    return float(Ff.abs().max()), wt

print("\n(b) u-SUBSYSTEM (frozen geometry) square solve, Nth=8 then Nth=16")
dev_t = torch.device(DEV)
phi_f = phi_c.detach().to(dev_t); rho_f = rho_c.detach().to(dev_t); rp_f = r_p.detach().to(dev_t)
cell8 = make_cell_ctx_nodes(Nr, 8, DEV)
m8, u8 = solve_u_subsystem(cell8, uf.reshape(-1).detach().to(dev_t), phi_f, rho_f, rp_f, prm,
                           tag="Nth=8 from end-state u")
# band-limited interpolation of u to Nth=16
cell16 = make_cell_ctx_nodes(Nr, 16, DEV)
mu16 = cell16["mu"].cpu().numpy()
S16 = np.zeros((16, Nth))
for j in range(Nth):
    ej = np.zeros(j + 1); ej[j] = 1.0
    S16[:, j] = _leg.legval(mu16, ej)
u_end8 = u8.reshape(Nr, 8).cpu().numpy()
coefs = np.linalg.solve(S, u_end8.T)               # (Nth, Nr) modal coeffs per radius
u16 = (S16 @ coefs).T                              # (Nr, 16)
m16, u16s = solve_u_subsystem(cell16, torch.as_tensor(u16.reshape(-1), device=dev_t),
                              phi_f, rho_f, rp_f, prm, tag="Nth=16 interp")

print("\n(c) FULL system at Nth=16 from interpolated end state (bounded)")
ctx16 = C.make_ctx_comp(Nr, 16, Na, kmap=KMAP, device=DEV)
u16_full = (S16 @ np.linalg.solve(S, uf.detach().numpy().T)).T
v16 = C.pack_comp(phi_c.to(dev_t), rho_c.to(dev_t),
                  torch.as_tensor(u16_full, device=dev_t),
                  phi_a.to(dev_t), rho_a.to(dev_t), float(r_p), float(r_sU), device=DEV)
resfn16 = lambda vv: C.residual_comp(vv, ctx16, prm, br)
F0 = resfn16(v16).detach()
t0 = time.time()
wsol, info = C.lm_qr(resfn16, v16.cpu().numpy(), maxit=400, device=DEV, time_budget=420.0)
wt = torch.as_tensor(np.asarray(wsol, dtype=float), device=dev_t)
Ff = resfn16(wt).detach()
off = 2*(Nr-2) + (Nr-2)*16 + 2 + 16
c1c16 = Ff[off:off+16].cpu().numpy()
print(f"  seed maxF={float(F0.abs().max()):.2e} -> iters={info['iters']} ({time.time()-t0:.1f}s) "
      f"end maxF={float(Ff.abs().max()):.3e}  r_p -> {float(wt[-2]):.1f}")
print(f"  C1c rows (Nth=16): {np.array2string(c1c16, precision=2)}")
sgn = np.sign(c1c16); alt = np.all(sgn[:-1] * sgn[1:] <= 0)
print(f"  node-to-node alternating: {alt}   max|C1c|={np.abs(c1c16).max():.3e} "
      f"(Nth=8 floor was ~1.1e-2)")

print("\n(d) INDEPENDENT theta-discretization (Chebyshev-Gauss interior mu-nodes, same modal space)")
def make_cheb_cell_ctx(Nr_, Nth_, device):
    """Clone of F2D.make_ctx but theta collocation at Chebyshev-Gauss mu-nodes (interior, no
    poles) with EXACT modal quadrature weights for the P_j basis (integral of the Lagrange
    interpolant in mu)."""
    zeta, Dz = F2D._cheb(Nr_)
    Dz2 = Dz @ Dz
    ccw = F2D._cc_weights(Nr_)
    k = np.arange(Nth_)
    mu_ = np.cos((2*k + 1) * np.pi / (2*Nth_))[::-1].copy()   # ascending
    th_ = np.arccos(mu_)[::-1].copy(); th_ = np.sort(th_)
    mu_s = np.cos(th_)                                        # theta ascending
    S_ = np.zeros((Nth_, Nth_)); dSth = np.zeros((Nth_, Nth_)); dSthth = np.zeros((Nth_, Nth_))
    sth = np.sqrt(1.0 - mu_s**2); cth = mu_s
    for j in range(Nth_):
        ej = np.zeros(j + 1); ej[j] = 1.0
        dej = _leg.legder(ej); d2ej = _leg.legder(ej, 2)
        S_[:, j] = _leg.legval(mu_s, ej)
        dSth[:, j] = -sth * _leg.legval(mu_s, dej)
        dSthth[:, j] = -cth * _leg.legval(mu_s, dej) + sth**2 * _leg.legval(mu_s, d2ej)
    Sinv = np.linalg.inv(S_)
    # exact quadrature in mu for polynomials of deg < Nth: w = integral of Lagrange basis
    # via modal route: int P_j dmu = 2*delta_{j0}; w^T = e0^T * 2 * Sinv  (since g = S c, int g = 2 c_0)
    w_ = 2.0 * Sinv[0, :]
    tt = lambda a: torch.as_tensor(np.asarray(a), dtype=torch.float64, device=device)
    return dict(Nr=Nr_, Nth=Nth_, rc=0.0, device=device,
                zeta=tt(zeta), Dz=tt(Dz), Dz2=tt(Dz2), ccw=tt(ccw),
                th=tt(th_), mu=tt(mu_s), w=tt(w_),
                DthT=tt((dSth @ Sinv).T), Dth2T=tt((dSthth @ Sinv).T),
                s=tt(np.sin(th_)), c=tt(np.cos(th_)), s2=tt(1.0 - mu_s**2))

cheb8 = make_cheb_cell_ctx(Nr, 8, DEV)
# sanity: quadrature weights integrate P_0 to 2, P_2 to 0
wq = cheb8["w"].cpu().numpy(); muq = cheb8["mu"].cpu().numpy()
print(f"  quad sanity: sum w = {wq.sum():.12f} (2 exact); int P2 = {np.sum(wq*0.5*(3*muq**2-1)):+.2e}")
# interpolate end-state u onto the Chebyshev-Gauss theta nodes
Sc = np.zeros((8, Nth))
for j in range(Nth):
    ej = np.zeros(j + 1); ej[j] = 1.0
    Sc[:, j] = _leg.legval(muq, ej)
u_cheb = (Sc @ np.linalg.solve(S, uf.detach().numpy().T)).T
mC, _ = solve_u_subsystem(cheb8, torch.as_tensor(u_cheb.reshape(-1), device=dev_t),
                          phi_f, rho_f, rp_f, prm, tag="Cheb-Gauss Nth=8")
print(f"\nsummary: u-subsystem floors GL8={m8:.3e} GL16={m16:.3e} ChebGauss8={mC:.3e}")
print("DONE (bv_c1c)")
