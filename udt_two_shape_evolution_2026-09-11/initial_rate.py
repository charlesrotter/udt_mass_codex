#!/usr/bin/env python3
"""Exact TI2 metric-three-jet calculation; conditional Ric=0, no PDE trajectory.

Method exposure: read TI1's raw-metric two-jet implementations. This extension is
parent construction, not an independent review. FRAME_AND_DISCOVERY owns choices.
"""
import argparse
import itertools as I
import json
import platform
import sympy as S

parser = argparse.ArgumentParser()
parser.add_argument('--mutant', choices=['omit_spatial_ricci_rate', 'freeze_third_time'])
args = parser.parse_args()
p,r,px,rx,pxx,rxx = S.symbols('p r p_X r_X p_XX r_XX', real=True)
s = S.Symbol('s', real=True, nonzero=True)
d = p*p+r*r
k = (d-s*s)/(2*s)
K = S.Matrix([[k,0,0],[0,s-p,-r],[0,-r,s+p]])
tau = S.trace(K)
def DX(f):
    return f.diff(p)*px+f.diff(r)*rx+f.diff(px)*pxx+f.diff(rx)*rxx
def clean(f):
    return S.factor(f)
Kx = DX(K)
Kxx = DX(Kx)
Kd = tau*K-2*K*K
Ric3d = S.Matrix(3,3,lambda i,j: Kxx[i,j]
                  -(Kxx[0,j] if i==0 else 0)
                  -(Kxx[i,0] if j==0 else 0)
                  +(S.trace(Kxx) if i==j==0 else 0))
Kdd = Ric3d+2*tau*tau*K-6*tau*K*K+4*K*K*K
if args.mutant == 'omit_spatial_ricci_rate':
    Kdd -= Ric3d
gtt = -2*Kd
gttt = -2*Kdd
if args.mutant == 'freeze_third_time':
    gttt = gttt.subs({p:0,r:0,px:0,rx:0,pxx:0,rxx:0})
sign = [-1,1,1,1]
giD = S.zeros(4)
giD[1:4,1:4] = 2*K
dg = S.MutableDenseNDimArray.zeros(4,4,4)
ddg = S.MutableDenseNDimArray.zeros(4,4,4,4)
ddgD = S.MutableDenseNDimArray.zeros(4,4,4,4)
for i,j in I.product(range(3),repeat=2):
    dg[i+1,j+1,0] = -2*K[i,j]
    ddg[i+1,j+1,0,0] = gtt[i,j]
    ddg[i+1,j+1,0,1] = ddg[i+1,j+1,1,0] = -2*Kx[i,j]
    ddgD[i+1,j+1,0,0] = gttt[i,j]
    ddgD[i+1,j+1,0,1] = ddgD[i+1,j+1,1,0] = DX(gtt[i,j])
    ddgD[i+1,j+1,1,1] = -2*Kxx[i,j]
G = {}; GD = {}
for a,b,c in I.product(range(4),repeat=3):
    G[a,b,c] = (dg[a,c,b]+dg[a,b,c]-dg[b,c,a])/2
    GD[a,b,c] = (ddg[a,c,b,0]+ddg[a,b,c,0]-ddg[b,c,a,0])/2
R = {}; RD = {}
for a,b,c,h in I.product(range(4),repeat=4):
    key = a,b,c,h
    R[key] = clean((ddg[a,h,b,c]+ddg[b,c,a,h]-ddg[a,c,b,h]-ddg[b,h,a,c])/2
                  +sum(sign[e]*(G[e,b,c]*G[e,a,h]-G[e,b,h]*G[e,a,c]) for e in range(4)))
    RD[key] = clean((ddgD[a,h,b,c]+ddgD[b,c,a,h]-ddgD[a,c,b,h]-ddgD[b,h,a,c])/2
                   +sum(sign[e]*(GD[e,b,c]*G[e,a,h]+G[e,b,c]*GD[e,a,h]
                                 -GD[e,b,h]*G[e,a,c]-G[e,b,h]*GD[e,a,c]) for e in range(4))
                   +sum(giD[e,f]*(G[e,b,c]*G[f,a,h]-G[e,b,h]*G[f,a,c])
                        for e,f in I.product(range(4),repeat=2)))
Ric = S.Matrix(4,4,lambda b,h:clean(sum(sign[a]*R[a,b,a,h] for a in range(4))))
RicD = S.Matrix(4,4,lambda b,h:clean(sum(sign[a]*RD[a,b,a,h] for a in range(4))
                            +sum(giD[a,c]*R[a,b,c,h] for a,c in I.product(range(4),repeat=2))))
checks = []
def check(name, values):
    if not isinstance(values,(list,tuple,S.MatrixBase)):
        values=[values]
    residuals=[clean(v) for v in values]
    bad=[str(v) for v in residuals if v!=0]
    checks.append({'name':name,'components':len(residuals),'nonzero':bad})
    if bad:
        print(json.dumps({'mutant':args.mutant,'checks':checks},indent=2))
        raise AssertionError(name)
check('original_Ricci',Ric)
check('time_derivative_original_Ricci_including_inverse_metric',RicD)
check('all_initial_constraints',[tau*tau-S.trace(K*K), *[Kx[0,i]-(DX(tau) if i==0 else 0) for i in range(3)]])
check('Riemann_and_rate_algebraic_identities',[
    z for Q in (R,RD) for a,b,c,h in I.product(range(4),repeat=4)
    for z in (Q[a,b,c,h]+Q[b,a,c,h],Q[a,b,c,h]-Q[c,h,a,b],
              Q[a,b,c,h]+Q[a,c,h,b]+Q[a,h,b,c])])
def dual_component(Q,a,b,c,h):
    return clean(sum(S.LeviCivita(a,b,e,f)*sign[e]*sign[f]*Q[e,f,c,h]/2
                     for e,f in I.product(range(4),repeat=2)))
def dual_rate(a,b,c,h):
    base=dual_component(RD,a,b,c,h)-tau*dual_component(R,a,b,c,h)
    return clean(base+sum(S.LeviCivita(a,b,e,f)*(
        giD[e,m]*sign[f]*R[m,f,c,h]+sign[e]*giD[f,m]*R[e,m,c,h])/2
        for e,f,m in I.product(range(4),repeat=3)))
E = S.Matrix(3,3,lambda i,j:R[i+1,0,j+1,0])
ED = S.Matrix(3,3,lambda i,j:RD[i+1,0,j+1,0])
BM = S.Matrix(3,3,lambda i,j:dual_component(R,i+1,0,j+1,0))
BD = S.Matrix(3,3,lambda i,j:dual_rate(i+1,0,j+1,0))
P = clean(16*S.trace(E*BM))
PD = clean(16*S.trace(ED*BM+E*BD+4*K*E*BM))
check('P_matches_full_TI1_initial_scalar',P+32*k*(p*rx-r*px))
check('E_B_and_time_rates_symmetric',[*(E-E.T),*(BM-BM.T),*(ED-ED.T),*(BD-BD.T)])
check('tracefree_E_B_and_differentiated_metric_traces',[
    S.trace(E),S.trace(BM),S.trace(ED+2*K*E),S.trace(BD+2*K*BM)])
harm = {pxx:-p,rxx:-r}
PDh = clean(PD.subs(harm))
ratio = clean(PDh/P)
eps = S.Symbol('epsilon',real=True)
L0 = S.limit(ratio.subs({p:eps*p,r:eps*r,px:eps*px,rx:eps*rx}),eps,0)
remainder = clean(PDh-L0*P)
out={'python':platform.python_version(),'sympy':S.__version__,'mutant':args.mutant,
     'route':'original lower Riemann from full metric three-jet; differentiated Hodge and inverse-metric E.B contraction',
     'variables':[str(v) for v in (p,r,px,rx,pxx,rxx,s)],'checks':checks,
     'K':str(K),'K_T':str(Kd),'Ric3_T':str(Ric3d),'K_TT':str(Kdd),
     'E':str(E),'B':str(BM),'E_T':str(ED),'B_T':str(BD),
     'P':str(P),'P_T_general_profile_jet':str(PD),'P_T_harmonic':str(PDh),
     'L_harmonic':str(ratio),'L0':str(L0),'S':str(remainder),
     'controls':{name:{'P':str(clean(P.subs(sub))), 'P_T':str(clean(PDh.subs(sub))),
                       'S':str(clean(remainder.subs(sub)))} for name,sub in {
         'zero':{p:0,r:0,px:0,rx:0},'p_only':{r:0,rx:0},'r_only':{p:0,px:0},
         'aligned':{r:2*p,rx:2*px},'opposite':{r:-2*p,rx:-2*px}}.items()}}
print(json.dumps(out,indent=2))
