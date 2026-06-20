#!/usr/bin/env python3
"""
INDEPENDENT VERIFIER: hybrid-accuracy vs off-diagonal magnitude A.
NO Newton solve.  Single Einstein evaluations only.

Plan:
- Build an ANALYTIC steep diagonal background a,b,c,d (soliton-like:
  b ~ p*ln(r/r_seal)) plus a smooth off-diagonal warp e_rt (and e_tp,e_rp) of
  controllable magnitude A.
- The P1 hybrid error vs TRUTH is:
     err = [e_spec(full) - e_spec(diag)] - [e_true(full) - e_true(diag)]
  because the hybrid backbone G_weyl is exact for the diagonal part, so the
  diagonal-truth cancels and only the off-diagonal DELTA's discretization error
  remains.  TRUTH = analytic Einstein from sympy on the SAME analytic metric.
- Sweep A; report max|err| over the body in the off-diagonal blocks AND the
  diagonal-block back-reaction.  KEY: does err stay flat (cancellation holds) or
  blow up as A grows (off-diag no longer small on the steep background)?
"""
import os
os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK", "0")
os.environ.setdefault("PYTORCH_NO_CUDA_MEMORY_CACHING", "1")
import math, numpy as np, torch
torch.set_default_dtype(torch.float64)
import sympy as sp

from full3d_spectral import (Grid3D, attach_coord_weight, build_metric,
    einstein_mixed, einstein_mixed_weyl, DEV, T, R, TH, PS)
import p1_residual_general_einstein as P1

# ---------- analytic metric definition (must match build_metric exactly) ----------
# build_metric:
#  g_tt=-e^{2a}, g_rr=e^{2b}, g_thth=e^{2c} r^2, g_psps=e^{2d} r^2 sth^2
#  g_rth=e_rt*r, g_rps=e_rp*r*sth, g_thps=e_tp*r^2*sth
# choose smooth analytic warps a,b,c,d and off-diag fields e_rt,e_rp,e_tp.
rs, ths, ps_s, Asym = sp.symbols('r th ps A', real=True)
p_val = 0.4
r_seal = 0.05 + 14.0  # ri
# soliton-like steep diagonal (smooth, analytic): b = p*ln(r/r_seal); a=-b-style gauge
a_e = -p_val*sp.log(rs/r_seal) * sp.Rational(1,3)            # some nontrivial a (B!=1/A)
b_e =  p_val*sp.log(rs/r_seal)                               # STEEP core (1/r deriv)
c_e =  0.05*sp.exp(-((rs-(0.05+5.0))**2)/4.0)*sp.sin(ths)**2
d_e =  0.03*sp.exp(-((rs-(0.05+5.0))**2)/4.0)*sp.cos(ths)**2
# off-diagonal warp fields (the 'e' fields, dimensionless); magnitude scales with A
bump = sp.exp(-((rs-(0.05+5.0))**2)/4.0)
e_rt_e = Asym*bump*sp.sin(ths)**2
e_rp_e = Asym*0.7*bump*sp.sin(ths)*sp.cos(ps_s)
e_tp_e = Asym*0.5*bump*sp.sin(ths)

sth_e = sp.sin(ths)
g_sym = sp.zeros(4,4)
g_sym[0,0] = -sp.exp(2*a_e)
g_sym[1,1] =  sp.exp(2*b_e)
g_sym[2,2] =  sp.exp(2*c_e)*rs**2
g_sym[3,3] =  sp.exp(2*d_e)*rs**2*sth_e**2
g_sym[1,2] = g_sym[2,1] = e_rt_e*rs
g_sym[1,3] = g_sym[3,1] = e_rp_e*rs*sth_e
g_sym[2,3] = g_sym[3,2] = e_tp_e*rs**2*sth_e

coords = [sp.Symbol('t'), rs, ths, ps_s]  # t with d_t=0

def einstein_mixed_sympy(gm):
    ginv = gm.inv()
    n=4
    # christoffel
    Gamma = [[[sp.Integer(0)]*n for _ in range(n)] for _ in range(n)]
    for la in range(n):
        for mu in range(n):
            for nu in range(n):
                s=sp.Integer(0)
                for si in range(n):
                    s += ginv[la,si]*(sp.diff(gm[si,nu],coords[mu])
                                      +sp.diff(gm[si,mu],coords[nu])
                                      -sp.diff(gm[mu,nu],coords[si]))
                Gamma[la][mu][nu]=s/2   # no simplify (lambdify handles it; truth exact)
    # Ricci R_{mn}=d_a G^a_{mn}-d_n G^a_{ma}+G^a_{ab}G^b_{mn}-G^a_{nb}G^b_{ma}
    Ric=sp.zeros(n,n)
    for mu in range(n):
        for nu in range(n):
            s=sp.Integer(0)
            for al in range(n):
                s+=sp.diff(Gamma[al][mu][nu],coords[al])
                s-=sp.diff(Gamma[al][mu][al],coords[nu])
                for be in range(n):
                    s+=Gamma[al][al][be]*Gamma[be][mu][nu]
                    s-=Gamma[al][nu][be]*Gamma[be][mu][al]
            Ric[mu,nu]=s
    Rsc=sp.Integer(0)
    for mu in range(n):
        for nu in range(n):
            Rsc+=ginv[mu,nu]*Ric[mu,nu]
    Gmn=Ric-sp.Rational(1,2)*gm*Rsc
    Gmix=ginv*Gmn
    return Gmix

print("Building sympy Einstein (full and diagonal)... this is the slow part.")
import time; t0=time.time()
Gmix_full_sym = einstein_mixed_sympy(g_sym)
g_diag_sym = g_sym.copy()
g_diag_sym[1,2]=g_diag_sym[2,1]=g_diag_sym[1,3]=g_diag_sym[3,1]=g_diag_sym[2,3]=g_diag_sym[3,2]=sp.Integer(0)
Gmix_diag_sym = einstein_mixed_sympy(g_diag_sym)
print(f"  sympy Einstein built in {time.time()-t0:.0f}s")

# lambdify the off-diag DELTA = Gfull - Gdiag for the components we care about
delta_sym = Gmix_full_sym - Gmix_diag_sym
comps = {'rth':(1,2),'rps':(1,3),'thps':(2,3),'tt':(0,0),'rr':(1,1),'thth':(2,2),'psps':(3,3)}
delta_fns={}
for nm,(i,j) in comps.items():
    delta_fns[nm]=sp.lambdify((rs,ths,ps_s,Asym), delta_sym[i,j], 'numpy')

# ---------- grid eval ----------
G = Grid3D(24,6,8, rc=0.05, cell=14.0); G=attach_coord_weight(G)
bod = G.body.cpu().numpy()
RR = G.Rg.cpu().numpy(); TT=G.THg.cpu().numpy(); PP=G.PSg.cpu().numpy()

def field(expr_fn_args, A):
    return None

# numpy lambdified diagonal/offdiag FIELD builders (to feed build_metric on grid)
a_fn=sp.lambdify((rs,ths,ps_s),a_e,'numpy'); b_fn=sp.lambdify((rs,ths,ps_s),b_e,'numpy')
c_fn=sp.lambdify((rs,ths,ps_s),c_e,'numpy'); d_fn=sp.lambdify((rs,ths,ps_s),d_e,'numpy')
ert_fn=sp.lambdify((rs,ths,ps_s,Asym),e_rt_e,'numpy')
erp_fn=sp.lambdify((rs,ths,ps_s,Asym),e_rp_e,'numpy')
etp_fn=sp.lambdify((rs,ths,ps_s,Asym),e_tp_e,'numpy')

def tens(x):
    return torch.tensor(np.broadcast_to(x,RR.shape).copy(),device=DEV)

a_g=tens(a_fn(RR,TT,PP)); b_g=tens(b_fn(RR,TT,PP))
c_g=tens(c_fn(RR,TT,PP)); d_g=tens(d_fn(RR,TT,PP))

print("\nA-sweep:  max|hybrid_delta - true_delta| over body")
print(f"{'A':>10} | {'rth':>10} {'rps':>10} {'thps':>10} | {'tt(diag)':>10} {'rr(diag)':>10} | {'|e_rt|max':>9}")
for A in [0.0, 1e-4, 1e-3, 1e-2, 0.05, 0.1, 0.2]:
    ert=tens(ert_fn(RR,TT,PP,A)); erp=tens(erp_fn(RR,TT,PP,A)); etp=tens(etp_fn(RR,TT,PP,A))
    # P1 hybrid delta = einstein_mixed(full)-einstein_mixed(diag) (the bracket)
    g_full=build_metric(G,a_g,b_g,c_g,d_g,e_rt=ert,e_rp=erp,e_tp=etp)
    g_diag=build_metric(G,a_g,b_g,c_g,d_g)
    Gf,_,_,_=einstein_mixed(G,g_full)
    Gd,_,_,_=einstein_mixed(G,g_diag)
    hyb_delta=(Gf-Gd).cpu().numpy()
    row=[]
    for nm in ['rth','rps','thps','tt','rr']:
        i,j=comps[nm]
        true_d=delta_fns[nm](RR,TT,PP,A)
        true_d=np.broadcast_to(true_d,RR.shape)
        err=np.abs(hyb_delta[...,i,j]-true_d)[bod].max()
        row.append(err)
    ertmax=np.abs(ert.cpu().numpy()[bod]).max()
    print(f"{A:>10.1e} | {row[0]:>10.2e} {row[1]:>10.2e} {row[2]:>10.2e} | {row[3]:>10.2e} {row[4]:>10.2e} | {ertmax:>9.2e}")
