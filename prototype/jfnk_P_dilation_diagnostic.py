#!/usr/bin/env python3
"""
jfnk_P_dilation_diagnostic.py -- IS THE BRANCH-P STALL THE SCALE MODULUS?

Driver: Claude (Opus 4.8).  2026-06-23.  OBSERVE/PONDER mode.  DATA-BLIND.
NEW FILE; imports the immutable solver/residual verbatim.

THE PONDER (GR corpus + numerical-analysis, two agent analyses 2026-06-23):
  Branch P floored to Phi~=8.67 then STALLED (grad~=0, Phi>0 => residual in
  coker J).  The flat rho~1/r^2 on both branches = the global-monopole solid-
  angle-deficit tail, which by DERRICK (D=3) has NO stationary radius -- its
  SIZE is a flat modulus (box-controlled), UNLESS a dimensionful term lifts it.
  Branch P keeps e^{2phi}-1 (a Lambda/de-Sitter-core term; it is what breaks
  B=1/A) -- the ONE native candidate to lift the scale modulus.
  HYPOTHESIS: the stall IS the scale modulus (no scale selected => the stall is
  PHYSICS, a preconditioner would chase a gauge direction).  TEST it directly.

DECISIVE TESTS (Agent B's minimal set + SVD certification):
  (i)   ||J^T F|| / ||F||              -- is it a true critical point?
  (ii)  d = -r * d_r u (dilation gen); ||J d|| / (sigma_max ||d||)  -- is
        rescaling a NULL direction of the linearization?
  (iii) Phi(u + eps d) vs eps          -- is the solver-valley FLAT along d?
  (iv)  M_MS(u_s) for u_s = u(r/s)     -- the physics DERRICK curve: flat/
        monotone = scale-free (no particle); MINIMUM at finite s = a scale is
        SELECTED (e^{2phi}-1 lifted the modulus = localization emerges).
  (v)   dense J -> SVD: spectral gap above the ~(nU-nF) structural nulls;
        overlap |<v_i, d>| of smallest nontrivial right vectors with the
        dilation template (smoking gun); cokernel proj of F onto INTERIOR-EL
        vs BC row-blocks (obstruction on physics rows => real, build PC/refine;
        on BC/scale rows => benign, scale-freedom is physical).

Bounded: Nr=10, single process, hard caps.  No solve is delegated.
"""
import os
os.environ.setdefault('PYTORCH_NVML_BASED_CUDA_CHECK', '0')
import sys, time
import numpy as np
import torch
torch.set_default_dtype(torch.float64)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import branchGP_native_s2_coupled_OBSERVE as B
from jfnk_branch_solver import jfnk_solve, _grid

NR = 10
P = 1.0
BR = "P"
X, XI, KAP, KAP8, M = B.X_PROD, B.XI_PROD, B.KAP_PROD, B.KAP8, B.M_WIND
WBC = 30.0
t0 = time.time()
log = lambda s: print(s, flush=True)

log("=" * 72)
log(f"BRANCH-P DILATION/STALL DIAGNOSTIC  Nr={NR}  pc=jacobi")
log("=" * 72)

G = _grid(NR)
u0 = B.make_seed(G, P)

# ---- 1. Floor P to the stall (bounded) -------------------------------------
log("\n[1] flooring Branch P to the stall ...")
u, hist, tsec, capped, info = jfnk_solve(
    u0, G, P, X, XI, KAP, m=M, kap8=KAP8, branch=BR,
    pc='jacobi', maxit=12, lam0=1e-2, lsmr_maxit=300,
    eta0=1e-1, eta_min=1e-4, tol=1e-12, wall_cap=280.0, verbose=True)
torch.save(u.cpu(), "/tmp/uP_stall.pt")
Phi = hist[-1]
log(f"  floored: Phi={Phi:.4e}  newton={len(hist)-1}  t={tsec:.0f}s  capped={capped}")

fwd = lambda uu: B.residual_vec(uu, G, P, X, XI, KAP, m=M, kap8=KAP8, branch=BR, wbc=WBC)
F = fwd(u).detach()
nU = u.numel(); nF = F.numel()
log(f"  nU={nU} nF={nF}  ||F||={float(F.norm()):.4e}")

# ---- 2. dilation generator d = -r * d_r u (per field) ----------------------
a, b, c, d4, phi, gtw = B.unpack6(u)
rcol = G.r.view(-1, 1, 1)
dfields = [-(rcol * G.d_r(f)) for f in (a, b, c, d4, phi, gtw)]
dvec = torch.stack(dfields, 0).reshape(-1).detach()
dvec_u = dvec / dvec.norm()

# ---- 3. dense J (reuse the immutable jacrev helper) ------------------------
log("\n[3] forming dense Jacobian (jacrev) ...")
tj = time.time()
J, F2 = B.jac_jacrev(u, G, P, X, XI, KAP, M, KAP8, BR, WBC, chunk_size=128)
J = J.reshape(nF, nU)
log(f"  J shape={tuple(J.shape)}  formed in {time.time()-tj:.0f}s")

# (i) critical point
g = J.t() @ F
sigmax_est = float(torch.linalg.matrix_norm(J, ord=2))
log(f"\n(i)  CRITICAL POINT:  ||J^T F||={float(g.norm()):.4e}  "
    f"||J^T F||/||F||={float(g.norm()/F.norm()):.4e}  "
    f"||J^T F||/(sigma_max||F||)={float(g.norm()/(sigmax_est*F.norm())):.4e}")

# (ii) dilation null?
Jd = J @ dvec
log(f"(ii) DILATION NULL:  ||J d||/(sigma_max ||d||)={float(Jd.norm()/(sigmax_est*dvec.norm())):.4e}  "
    f"(small => rescaling is a null direction of J)")

# (iii) solver-valley flatness along d (linear)
log("(iii) SOLVER-VALLEY Phi(u+eps*d_unit):")
for eps in [-2e-1, -1e-1, -3e-2, 0.0, 3e-2, 1e-1, 2e-1]:
    Pe = float((fwd(u + eps * dvec_u.reshape(u.shape)) ** 2).sum())
    log(f"     eps={eps:+.2e}  Phi={Pe:.4e}")

# ---- 4. physics DERRICK curve: M_MS(u_s), u_s = u(r/s) ----------------------
log("\n(iv) DERRICK curve  E(s)=M_MS(u(r/s))  (flat/monotone=scale-free; min=scale SELECTED):")
rgrid = G.r
def dilate(u_in, s):
    a_, b_, c_, d_, p_, t_ = B.unpack6(u_in)
    out = []
    rq = (rgrid / s).clamp(min=float(rgrid.min()), max=float(rgrid.max()))
    # linear interp along r for each (th,ps) column
    idx = torch.searchsorted(rgrid.contiguous(), rq.contiguous()).clamp(1, len(rgrid) - 1)
    r0 = rgrid[idx - 1]; r1 = rgrid[idx]
    w = ((rq - r0) / (r1 - r0)).view(-1, 1, 1)
    for f in (a_, b_, c_, d_, p_, t_):
        f0 = f[idx - 1]; f1 = f[idx]
        out.append((1 - w) * f0 + w * f1)
    return torch.stack(out, 0)
for s in [0.6, 0.75, 0.87, 1.0, 1.15, 1.33, 1.55, 1.8]:
    us = dilate(u, s)
    dg = B.diagnose(us, G, X, XI, KAP, m=M, kap8=KAP8, branch=BR)
    Ps = float((fwd(us) ** 2).sum())
    log(f"     s={s:.2f}  M_MS={dg['M_MS']:.4e}  phi_min={dg['phi_min']:+.3e}  "
        f"AB={dg['AB']:.3e}  Phi={Ps:.3e}")

# ---- 5. SVD certification --------------------------------------------------
log("\n[5] SVD of J ...")
ts = time.time()
U, S, Vh = torch.linalg.svd(J, full_matrices=False)   # U:(nF,k) S:(k,) Vh:(k,nU), k=nF
log(f"  SVD in {time.time()-ts:.0f}s  sigma_max={float(S[0]):.3e}  sigma_min={float(S[-1]):.3e}")
Snp = S.cpu().numpy()
log("  smallest 18 singular values: " + " ".join(f"{x:.2e}" for x in Snp[-18:]))
# structural-null count proxy: nU-nF would be right-null; J has nF rows so up to nF nonzero.
# gap finder among the smallest nonzero:
ratios = Snp[:-1] / np.clip(Snp[1:], 1e-300, None)
log(f"  largest small-end gap ratio among smallest 40: "
    f"{float(np.max(ratios[-40:])):.2e} at idx {int(np.argmax(ratios[-40:]))} from bottom")

# right-vector overlap with dilation template (smallest nontrivial modes)
V = Vh.t()  # (nU, k) columns = right vectors
ovl = (V.t() @ dvec_u).abs()   # |<v_i, d_unit>| for each i
ovl_np = ovl.cpu().numpy()
# report the modes with the LARGEST dilation overlap and their sigma
order = np.argsort(-ovl_np)[:8]
log("  modes with largest |<v_i, d_dilation>|  (sigma_i, overlap):")
for i in order:
    log(f"     mode {i:4d}  sigma={Snp[i]:.3e}  |<v,d>|={ovl_np[i]:.3f}")
# also: overlap of d with the smallest-sigma subspace as a whole
ksmall = 60
proj_small = float((V[:, -ksmall:].t() @ dvec_u).norm())
log(f"  ||proj of d onto smallest-{ksmall} right-subspace|| = {proj_small:.4f}  (1=fully in null)")

# (v) cokernel projection of F onto INTERIOR-EL vs BC row blocks
nbody = int(G.body.sum()); nbc = G.Nth * G.Nps
nINT = 9 * nbody  # 7 Einstein + elphi + elg
log(f"\n(v) COKERNEL obstruction localization (nbody={nbody} nbc={nbc} nINT={nINT}):")
# small-sigma left vectors:
eps_sv = 1e-6 * float(S[0])
mask_small = S < eps_sv
nsmall = int(mask_small.sum())
Usmall = U[:, mask_small]            # (nF, nsmall) cokernel-ish
cF = Usmall.t() @ F                  # projections
PcokF = Usmall @ cF
frac_coker = float((PcokF.norm() / F.norm()) ** 2)
log(f"  #sigma<1e-6 sigma_max = {nsmall};  ||P_coker F||^2/||F||^2 = {frac_coker:.4f}")
# how is P_coker F distributed across row blocks?
pc = PcokF
e_int = float((pc[:nINT] ** 2).sum()); e_bc = float((pc[nINT:] ** 2).sum())
tot = e_int + e_bc + 1e-300
log(f"  P_coker F energy: INTERIOR-EL={e_int/tot:.3f}   BC-rows={e_bc/tot:.3f}")
# finer: per interior block (which equation carries it)
names = ["E_TT","E_RR","E_THTH","E_PSPS","E_RTH","E_RPS","E_THPS","EL_phi","EL_gtw"]
log("  interior-block share of P_coker F:")
for k, nm in enumerate(names):
    seg = pc[k*nbody:(k+1)*nbody]
    log(f"     {nm:8s} {float((seg**2).sum())/tot:.3f}")
# also raw F distribution (where the residual lives, regardless of coker)
log("  raw ||F||^2 share by interior block:")
for k, nm in enumerate(names):
    seg = F[k*nbody:(k+1)*nbody]
    log(f"     {nm:8s} {float((seg**2).sum())/float((F**2).sum()):.3f}")
log(f"  raw ||F||^2 BC-rows share: {float((F[nINT:]**2).sum())/float((F**2).sum()):.3f}")

log(f"\n=== DIAGNOSTIC DONE  total={time.time()-t0:.0f}s ===")
