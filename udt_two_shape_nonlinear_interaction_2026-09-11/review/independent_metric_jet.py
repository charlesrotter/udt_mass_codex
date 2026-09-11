#!/usr/bin/env python3
"""Source/data-first TI1 check: original metric 2-jet, no author imports.

Conditional Ric=0, flat gamma on T0, K=-gamma_T/2. Spatial evolution sets
gamma_TT=4K^2-2tr(K)K; directly reconstruct all original Riemann/Ricci and
FIRST-pair Hodge contraction. Exact symbols, CPU, no sampling or PDE solve.
"""
import itertools
import json
import platform
import sympy as S

p,r,px,rx=S.symbols('p r p_X r_X',real=True)
s=S.Symbol('s',real=True,nonzero=True)
k=(p*p+r*r-s*s)/(2*s)
K=S.Matrix([[k,0,0],[0,s-p,-r],[0,-r,s+p]])
Kx=K.diff(p)*px+K.diff(r)*rx
tau=S.trace(K)
g=S.diag(-1,1,1,1)
sign=[-1,1,1,1]
dg=S.MutableDenseNDimArray.zeros(4,4,4)
ddg=S.MutableDenseNDimArray.zeros(4,4,4,4)
gtt=4*K*K-2*tau*K
for i,j in itertools.product(range(3),repeat=2):
    dg[i+1,j+1,0]=-2*K[i,j]
    ddg[i+1,j+1,0,0]=gtt[i,j]
    ddg[i+1,j+1,0,1]=ddg[i+1,j+1,1,0]=-2*Kx[i,j]
Gamma=S.MutableDenseNDimArray.zeros(4,4,4)
for a,b,c in itertools.product(range(4),repeat=3):
    Gamma[a,b,c]=sign[a]*(dg[a,c,b]+dg[a,b,c]-dg[b,c,a])/2
C=S.MutableDenseNDimArray.zeros(4,4,4,4)
for a,b,c,d in itertools.product(range(4),repeat=4):
    C[a,b,c,d]=S.factor((ddg[a,d,b,c]+ddg[b,c,a,d]-ddg[a,c,b,d]-ddg[b,d,a,c])/2
        +sum(sign[e]*(Gamma[e,b,c]*Gamma[e,a,d]-Gamma[e,b,d]*Gamma[e,a,c]) for e in range(4)))
Ric=S.Matrix(4,4,lambda b,d:S.factor(sum(sign[a]*C[a,b,a,d] for a in range(4))))
if Ric != S.zeros(4): raise AssertionError(('Original Ricci',Ric))
star=S.MutableDenseNDimArray.zeros(4,4,4,4)
for a,b,c,d in itertools.product(range(4),repeat=4):
    star[a,b,c,d]=S.factor(sum(S.LeviCivita(a,b,e,f)*sign[e]*sign[f]*C[e,f,c,d]/2
        for e,f in itertools.product(range(4),repeat=2)))
P=S.factor(sum(sign[a]*sign[b]*sign[c]*sign[d]*C[a,b,c,d]*star[a,b,c,d]
    for a,b,c,d in itertools.product(range(4),repeat=4)))
H=S.factor(tau*tau-S.trace(K*K))
M=S.Matrix([S.factor(Kx[0,i]-(S.diff(tau,p)*px+S.diff(tau,r)*rx if i==0 else 0)) for i in range(3)])
if H != 0 or M!=S.zeros(3,1): raise AssertionError(('constraints',H,M))
out={'route':'full original metric 2-jet and four-index FIRST-pair Hodge',
    'python':platform.python_version(),'sympy':S.__version__,
    'variables':[str(x) for x in (p,r,px,rx,s)],'K':str(K),'Ricci':str(Ric),
    'Hamiltonian':str(H),'momentum':str(M),'P':str(P),'E':str(S.Matrix(3,3,lambda i,j:C[i+1,0,j+1,0])),
    'B_first_dual':str(S.Matrix(3,3,lambda i,j:star[i+1,0,j+1,0]))}
A,B,theta,X=S.symbols('A B theta X',real=True)
harmonic={p:A*S.cos(X),r:B*S.cos(X+theta),px:-A*S.sin(X),rx:-B*S.sin(X+theta)}
out['harmonic_P']=str(S.trigsimp(P.subs(harmonic)))
out['phase_wronskian']=str(S.trigsimp((p*rx-r*px).subs(harmonic)))
out['zero_and_one_controls']={name:str(S.simplify(P.subs(sub))) for name,sub in {
    'zero':{p:0,r:0,px:0,rx:0},'p_only':{r:0,rx:0},'r_only':{p:0,px:0},
    'aligned':{r:2*p,rx:2*px}}.items()}
# Equation-violating omitted quadratic Kxx completion: original Hamiltonian.
bad=S.Matrix([[-s/2,0,0],[0,s-p,-r],[0,-r,s+p]])
out['invalid_completion_H']=str(S.factor(S.trace(bad)**2-S.trace(bad*bad)))
print(json.dumps(out,indent=2))
