#!/usr/bin/env python3
"""
whole_metric_3d_gauge_disambig.py -- THE DECISIVE GAUGE-vs-PHYSICAL disambiguation of the
near-null off-diagonal directions found by the bifurcation test (sigma_min ~ 1e-6).

Driver: Claude (Opus 4.8, 1M).  2026-06-15.  OBSERVE mode.  DATA-BLIND.
Frame: whole_metric_solve_MAP.md "#1 place to get it wrong: off-diagonals are routinely
GAUGED AWAY".  The off-diagonal Jacobian has near-null directions; a NEW solution branch
needs a null mode BEYOND the gauge orbit.  Coordinate (gauge) transformations
x^mu -> x^mu + xi^mu generate  delta g_mn = nabla_mu xi_nu + nabla_nu xi_mu , which leave
the Einstein equations INVARIANT -> EXACT null modes of J that are pure coordinate, NOT
physics.  With 4 gauge functions we EXPECT a 4-family null space.  The test:

  build the gauge subspace (the Lie-derivative directions of the round metric, restricted
  to the free off-diagonal components), PROJECT it out of the perturbation space, and
  recompute sigma_min of J on the gauge-ORTHOGONAL complement.
    * if sigma_min JUMPS UP after deflation  => the near-nulls were PURE GAUGE -> NO new
      structure (the off-diagonals are gauge artifacts; round soliton locally unique).
    * if a null mode SURVIVES deflation      => a PHYSICAL bifurcation -> NEW structure
      (a shaped/twisted type branches off the round soliton).

NUMERICS: the gauge direction delta g_mn = nabla_mu xi_nu + nabla_nu xi_mu is computed
EXACTLY by autograd: it is the linearization of the metric under the infinitesimal
diffeo, i.e. the Lie derivative L_xi g.  We compute L_xi g via the covariant formula with
Christoffels from the validated engine.  Deflation = Gram-Schmidt of the gauge basis,
then sigma_min of J restricted to the complement (matrix-free Lanczos / dense on the
small window).
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, time
import torch
import whole_metric_3d_core as core
import whole_metric_3d_matter as mat
import whole_metric_3d_solver as S
import whole_metric_3d_newton as NW
import whole_metric_3d_bifurcation as BF
import radial_Bfree_soliton as rb

torch.set_default_dtype(torch.float64)
DEV=S.DEV; T,R,TH,PS=0,1,2,3
def hdr(s): print("\n"+"="*78); print(s); print("="*78, flush=True)

xi_=kap=1.0; rc=0.05; SPAN=14.0; ri=rc+SPAN; KAP8=0.05; th0,th1=0.30,math.pi-0.30


def build_round(G,a_r,b_r,Th_r):
    Nr,Nth,Nps=G['Nr'],G['Nth'],G['Nps']
    g=torch.zeros(Nr,Nth,Nps,4,4,device=DEV)
    g[...,T,T]=-torch.exp(2*a_r[:,None,None].expand(Nr,Nth,Nps))
    g[...,R,R]=torch.exp(2*b_r[:,None,None].expand(Nr,Nth,Nps))
    g[...,TH,TH]=G['Rr']**2
    g[...,PS,PS]=(G['Rr']*torch.sin(G['Tht']))**2
    Thf=Th_r[:,None,None].expand(Nr,Nth,Nps).contiguous()
    return g,Thf


def christoffels(g, G):
    ginv=core.metric_inverse(g)
    dg=torch.zeros(*g.shape[:-2],4,4,4,device=DEV)
    dg[...,R,:,:]=S.d_dx(g,G['hr'],3); dg[...,TH,:,:]=S.d_dx(g,G['hth'],4); dg[...,PS,:,:]=S.d_dx(g,G['hps'],5)
    return core.christoffel(ginv,dg), ginv


def lie_derivative_g(g, xi_low, Gamma, G):
    """L_xi g_mn = xi^a d_a g_mn + g_an d_m xi^a + g_ma d_n xi^a
       = nabla_m xi_n + nabla_n xi_m (xi_low = xi_mu lower).  We compute via the
    covariant form: (L_xi g)_mn = nabla_m xi_n + nabla_n xi_m, with
    nabla_m xi_n = d_m xi_n - Gamma^a_mn xi_a."""
    # d_m xi_n
    dxi=torch.zeros(*xi_low.shape[:-1],4,4,device=DEV)  # dxi[...,m,n]=d_m xi_n
    dxi[...,R,:]=S.d_dx(xi_low,G['hr'],3)
    dxi[...,TH,:]=S.d_dx(xi_low,G['hth'],4)
    dxi[...,PS,:]=S.d_dx(xi_low,G['hps'],5)
    # nabla_m xi_n = d_m xi_n - Gamma^a_mn xi_a
    Gx=torch.einsum('...amn,...a->...mn',Gamma,xi_low)
    nab=dxi-Gx
    return nab+nab.transpose(-1,-2)


def gauge_basis_in_freespace(g, mask_g, G, n_xi_modes=120, seed=1):
    """Build a set of gauge directions delta g = L_xi g for random smooth xi supported in
    the free window, project each into the free-component vector space (x-coords), and
    return an orthonormal basis of the gauge subspace."""
    Gamma,ginv=christoffels(g,G)
    free_pts = mask_g.any(dim=-1)            # (Nr,Nth,Nps) where ANY comp is free
    torch.manual_seed(seed)
    vecs=[]
    Nr,Nth,Nps=G['Nr'],G['Nth'],G['Nps']
    # smooth random xi fields supported on the free region (xi lower index, 4 comps)
    for _ in range(n_xi_modes):
        xi_low=torch.zeros(Nr,Nth,Nps,4,device=DEV)
        comp=torch.randint(0,4,(1,)).item()
        # smooth bump * random low-frequency modulation over the free window
        bump=free_pts.float()
        kr=torch.randint(0,3,(1,)).item(); kth=torch.randint(0,3,(1,)).item(); kps=torch.randint(0,2,(1,)).item()
        mod=torch.cos(kr*math.pi*(G['Rr']-rc)/SPAN)*torch.cos(kth*G['Tht'])*torch.cos(kps*G['Ps'])
        xi_low[...,comp]=bump*mod
        dg=lie_derivative_g(g,xi_low,Gamma,G)   # (...,4,4)
        # restrict to the free components -> x-vector
        v=NW.x_from_g(dg, mask_g)               # picks the free symmetric comps
        nv=v.norm()
        if nv>1e-12:
            vecs.append(v/nv)
    # orthonormalize (Gram-Schmidt / QR)
    if not vecs:
        return None
    Vt=torch.stack(vecs,dim=1)   # (DOF, nmodes)
    Q,Rr=torch.linalg.qr(Vt)
    # keep columns with significant R diagonal (independent gauge dirs)
    diag=Rr.diagonal().abs()
    keep=diag>1e-9*diag.max()
    return Q[:,keep]


def J_dense(F,u0):
    n=u0.numel(); u0=u0.detach()
    cols=[]; I=torch.eye(n,device=DEV)
    for i in range(n):
        _,jv=torch.autograd.functional.jvp(F,(u0,),(I[i],),strict=False); cols.append(jv)
    return torch.stack(cols,dim=1)


# ===========================================================================
hdr("GAUGE DISAMBIGUATION of the off-diagonal near-null directions")
Nr=40; Nth=14; Nps=6
G=S.mkgrid(Nr,Nth,Nps,rc,ri,th0,th1)
offdiag=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
def windowed_mask(G,comps,lo,hi):
    m=NW.make_freemask(G,comps,rcore_freeze=1.0)
    rok=(G['rg']>=lo)&(G['rg']<=hi); keep=torch.zeros(G['Nr'],dtype=torch.bool,device=DEV); keep[rok]=True
    m[~keep,:,:,:]=False; return m

for P in [0.2,0.4,0.7,1.0]:
    rN=rb.make_grid(1,Nr,rc=rc,rint=ri,geom=False)
    o=rb.selfconsistent_Bfree(rN,xi_,kap,p=P,kap8=KAP8,iters=300,relax=0.4,tol=1e-11,verbose=False)
    a_r,b_r,Th_r=o['a'][0],o['b'][0],o['Th'][0]
    g0,Th0=build_round(G,a_r,b_r,Th_r)
    mask_g=windowed_mask(G,offdiag,rc+2.0,rc+6.0)
    mask_th=torch.zeros(G['Nr'],G['Nth'],G['Nps'],dtype=torch.bool,device=DEV)
    eqmask=mask_g.clone(); wgeom=NW.geom_weight(G)
    F,ng=BF.build_residual_fn(g0,Th0,KAP8,G,mask_g,mask_th,eqmask,wgeom)
    u0=NW.x_from_g(g0,mask_g)
    t0=time.time()
    J=J_dense(F,u0)
    JTJ=J.T@J
    ev_raw=torch.linalg.eigvalsh(JTJ).clamp(min=0).sqrt()
    # gauge subspace
    Qg=gauge_basis_in_freespace(g0,mask_g,G,n_xi_modes=200)
    ngauge=Qg.shape[1] if Qg is not None else 0
    # project JTJ onto the gauge-ORTHOGONAL complement: P = I - Qg Qg^T
    if ngauge>0:
        n=u0.numel(); I=torch.eye(n,device=DEV)
        Pm=I-Qg@Qg.T
        M=Pm@JTJ@Pm
        ev_def=torch.linalg.eigvalsh(M).clamp(min=0).sqrt()
        ev_def_sorted=ev_def.sort().values
        sig_phys=ev_def_sorted[ngauge].item()
    else:
        sig_phys=ev_raw.min().item()
    # how many raw near-null directions total? and how many does gauge explain?
    n_rawnull=int((ev_raw<1e-5*ev_raw.max()).sum())
    print(f"  p={P}: DOF={u0.numel()} sigmax={ev_raw.max().item():.2e}  raw sigma_min={ev_raw.min().item():.3e}  "
          f"raw #(near-null)={n_rawnull}  gaugedim={ngauge}  "
          f"sigma_min(gauge-orth)={sig_phys:.3e}  ({time.time()-t0:.1f}s)",flush=True)

print("\n  READ: if sigma_min(gauge-orthogonal) JUMPS UP to O(1)x sigma_max while raw was")
print("  ~1e-6 => the near-nulls were PURE GAUGE -> NO physical bifurcation, round soliton")
print("  locally unique.  If it STAYS ~0 => a physical shaped/twisted branch survives.")
