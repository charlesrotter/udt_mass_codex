"""sweep_E2b_A3Z1_anatomy.py -- residual ANATOMY on the phase-2 saved end states (recompute-on-
saved; observation only). For each .pt: where in (r, theta) the f-PDE residual mass sits, the
C1c f_r(r_p, theta) profile, cell rho/phi ODE radial residual profile, H_cell(r) profile, and the
u(r,theta) shape -- the diagnosis data for the pre-committed failure reading. CPU recompute =
the end-to-end independent-device check (bracket-2/3 note: expect mismatch ONLY on e^{2phi}-
OVERFLOW states, H_cell >~ 1e15 with POSITIVE phi excursions; the underflow direction was clean
18/18 in bracket 3 -- do not read a clean match as surprising, nor an overflow mismatch as a bug)."""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import sys, glob, json
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
REPO = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, REPO)
import cell_solver_composite as C
import cell_solver_f2d as F2D

br = C.load_bracket("A3 Z=1")
out = {}
for pt in sorted(glob.glob(os.path.join(REPO, "E2b_A3Z1_P2*.pt"))):
    d = torch.load(pt, weights_only=False)
    w, prm = d["w"], tuple(d["prm"])
    ctx = C.make_ctx_comp(d["Nr"], d["Nth"], d["Na"], kmap=d["kmap"], device="cpu")
    v = w.clone()
    F = C.residual_comp(v, ctx, prm, br)
    Q, v_cell = C.cell_fields(v, ctx, prm)
    Hc = F2D.H_of_r(v_cell, ctx["cell"], prm)
    phi_c, rho_c, uf, phi_a, rho_a, rp, rsU = C.unpack_comp(v, ctx)
    Nr, Nth, Na = d["Nr"], d["Nth"], d["Na"]
    mu = ctx["cell"]["mu"].numpy()          # collocation mu = cos(theta) nodes
    zeta = ctx["cell"]["zeta"].numpy()
    resf = Q["res_f"].detach().numpy()      # (Nr, Nth) f-PDE residual
    fr_seal = Q["fr"][-1, :].detach().numpy()
    rec = dict(tag=d["tag"], prm=list(prm), rp=float(rp), rsU=float(rsU),
               maxF=float(F.abs().max()),
               fPDE_max=float(np.abs(resf[1:-1]).max()),
               fPDE_argmax_r_frac=float(zeta[np.unravel_index(np.abs(resf[1:-1]).argmax(), resf[1:-1].shape)[0] + 1] / 2 + 0.5),
               fPDE_theta_profile_maxoverr=[float(x) for x in np.abs(resf[1:-1]).max(axis=0)],
               C1c_fr_seal=[float(x) for x in fr_seal],
               mu_nodes=[float(x) for x in mu],
               u_seal=[float(x) for x in uf[-1].detach().numpy()],
               u_core=[float(x) for x in uf[0].detach().numpy()],
               max_u=float(uf.abs().max()),
               H_cell_profile=[float(x) for x in Hc.detach().numpy()],
               phi_cell_range=[float(phi_c.min()), float(phi_c.max())],
               rho_cell_range=[float(rho_c.min()), float(rho_c.max())],
               phi_amb_range=[float(phi_a.min()), float(phi_a.max())],
               rho_amb_range=[float(rho_a.min()), float(rho_a.max())],
               cell_phiODE_prof_absmax_by_r=[float(x) for x in Q["phi_ode"].abs().detach().numpy()],
               )
    out[os.path.basename(pt)] = rec
    print(f"{d['tag']:34s} maxF={rec['maxF']:.2e} fPDEmax={rec['fPDE_max']:.2e} "
          f"max|u|={rec['max_u']:.3f} rp={rec['rp']:.1f} rsU={rec['rsU']:.1f}")
with open(os.path.join(REPO, "microphysics_E2b_A3Z1_anatomy.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("anatomy saved")
