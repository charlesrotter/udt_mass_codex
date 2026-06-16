#!/usr/bin/env python3
"""
whole_metric_3d_persist.py -- NONLINEAR PERSISTENCE TEST: seed finite-amplitude 3-D
configurations (shaped, lobed, off-axis, rotating g_tpsi, multi-center) and relax with
UNCONDITIONALLY-STABLE gradient descent on the geometry-weighted squared Einstein
residual ||F||^2, core/axis/seal frozen.  Report what PERSISTS.

Driver: Claude (Opus 4.8, 1M).  2026-06-15.  OBSERVE mode.  DATA-BLIND.
Frame: whole_metric_solve_MAP.md realization (A) exploration step.

WHY GRADIENT DESCENT (not Newton): the global residual-Newton is ill-conditioned (the
coordinate spike + the off-diagonal sector is linearly near-null on the round background --
300 near-null directions, only 69 gauge: diagnosed & committed).  Newton chases those.
Gradient descent on phi(u)=||F(u)||^2 is MONOTONE (can only decrease the residual; cannot
blow up) -- the robust honest tool to ask the binary question: does a NON-ROUND seed
RELAX to a distinct persistent solution, or does it DECAY back to the round soliton (or
fail to lower its residual = not a solution)?  We use Adam (adaptive, stable) on phi with
the validated residual + matter action; core/axis/seal frozen.

OUTPUT per seed: does ||F|| reach the round-soliton floor?  do the off-diagonals /
non-axisymmetric shape SURVIVE (a new type) or DECAY to the round soliton?  M_MS, the
multipole content, angular momentum (g_tpsi), node count.
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
import math, time
import torch
import whole_metric_3d_core as core
import whole_metric_3d_matter as mat
import whole_metric_3d_solver as S
import whole_metric_3d_newton as NW
import radial_Bfree_soliton as rb

torch.set_default_dtype(torch.float64)
DEV=S.DEV; T,R,TH,PS=0,1,2,3
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


def residual_norm_full(g, Th, G, kap8, bmask, wgeom):
    """phi = sum over body of geometry-weighted (Einstein residual^2 + matter EL^2)."""
    n=mat.hedgehog_n(Th,G['Tht'],G['Ps'])
    Res=NW.residual_of_g(g,n,kap8,G)
    Rsym=0.5*(Res+Res.transpose(-1,-2))
    einstein_sq=(Rsym**2).sum(dim=(-1,-2))*wgeom
    # matter EL term: dS/dTh
    Thl=Th.requires_grad_(True)
    ginv=core.metric_inverse(g)
    nn=mat.hedgehog_n(Thl,G['Tht'],G['Ps'])
    dn=torch.zeros(*nn.shape[:-1],4,4,device=DEV)
    dn[...,R,:]=S.d_dx(nn,G['hr'],3); dn[...,TH,:]=S.d_dx(nn,G['hth'],4); dn[...,PS,:]=S.d_dx(nn,G['hps'],5)
    Gmn=mat.field_metric(dn); Lf,_,_,_=mat.lagrangian(ginv,Gmn,1.0,1.0)
    sqrtg=torch.sqrt(torch.clamp(-torch.linalg.det(g),min=1e-30))
    el,=torch.autograd.grad((sqrtg*Lf).sum(),Thl,create_graph=True)
    matter_sq=(el**2)*wgeom
    phi=(einstein_sq*bmask).sum()+(matter_sq*bmask).sum()
    return phi


def body_and_freeze(G, rcore=1.0):
    bmask=torch.zeros(G['Nr'],G['Nth'],G['Nps'],device=DEV)
    rok=(G['rg']>G['rc']+rcore)&(G['rg']<G['ri']-0.5)
    bmask[rok,4:-4,:]=1.0
    # freeze mask (where DOF are NOT optimized): core shell, theta edges, r-seal
    freeze=torch.ones(G['Nr'],G['Nth'],G['Nps'],dtype=torch.bool,device=DEV)
    freeze[rok,4:-4,:]=False
    return bmask, freeze


def relax_descent(g0, Th0, G, kap8, seed_g=None, seed_Th=None, steps=400, lr=2e-3,
                  rcore=1.0, tag="", verbose=True):
    bmask,freeze=body_and_freeze(G,rcore)
    wgeom=NW.geom_weight(G)
    # parametrize the FREE metric & Th as optimizable; frozen held at base.
    g_base=(seed_g if seed_g is not None else g0).clone()
    Th_base=(seed_Th if seed_Th is not None else Th0).clone()
    # free perturbation tensors (only body); use full-tensor delta restricted by mask
    dg=torch.zeros_like(g_base,requires_grad=True)
    dTh=torch.zeros_like(Th_base,requires_grad=True)
    opt=torch.optim.Adam([dg,dTh],lr=lr)
    free3=(~freeze).float()[...,None,None]
    free_th=(~freeze).float()
    hist=[]
    for it in range(steps):
        opt.zero_grad()
        dg_sym=0.5*(dg+dg.transpose(-1,-2))
        g=g_base+dg_sym*free3
        Th=Th_base+dTh*free_th
        phi=residual_norm_full(g,Th,G,kap8,bmask,wgeom)
        phi.backward()
        opt.step()
        if verbose and (it%50==0 or it==steps-1):
            with torch.no_grad():
                offmax=(0.5*(dg+dg.transpose(-1,-2))*free3)[...,T,PS].abs().max().item()
                print(f"  [{tag}] it={it} phi={phi.item():.4e} max|dg_tpsi|={offmax:.3e}",flush=True)
        hist.append(phi.item())
    with torch.no_grad():
        dg_sym=0.5*(dg+dg.transpose(-1,-2))
        g=g_base+dg_sym*free3
        Th=Th_base+dTh*free_th
    return dict(g=g.detach(),Th=Th.detach(),hist=hist,bmask=bmask)
