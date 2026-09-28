#!/usr/bin/env python3
"""Post-exposure independent exact checks. Imports no construction code."""
import json
import platform
import sympy as s

alpha,A,N=s.symbols('alpha A N', nonzero=True)
R3,D,rho,lam,R=s.symbols('R3 D rho lambda R')
eta=s.diag(-1,1,1,1)
pairs=[(i,j) for i in range(4) for j in range(i,4)]
def sym(values,n,pairlist):
    ans=s.zeros(n)
    for t,(i,j) in zip(values,pairlist):
        ans[i,j]=ans[j,i]=t
    return ans
rho2=sym(s.symbols('rho2_0:10'),4,pairs)
boxrho2=sym(s.symbols('boxrho2_0:10'),4,pairs)
boxrho=s.trace(eta*rho2)
boxboxrho=s.trace(eta*boxrho2)
# Direct flat linearized Ricci from the second metric jet h_ab,cd.
h2=lambda a,b,c,d:-2*alpha*eta[a,b]*rho2[c,d]
ric=s.Matrix(4,4,lambda a,b:s.expand(sum(eta[c,c]*(h2(c,b,c,a)+h2(c,a,c,b)-h2(a,b,c,c)-h2(c,c,a,b)) for c in range(4))/2))
rl=s.trace(eta*ric)
gl=ric-eta*rl/2
e=gl+12*alpha**2*(eta*boxboxrho-boxrho2)
checks={}
checks['scalar_curvature_recomputed_from_metric_jet']=s.simplify(rl-6*alpha*boxrho)==0
expected=-2*alpha*(eta*(boxrho-6*alpha*boxboxrho)-(rho2-6*alpha*boxrho2))
for i,j in pairs:
    checks[f'full_scalar_residual_factor_{i}{j}']=s.simplify(e[i,j]-expected[i,j])==0
# Prolonged KG equation implies Hess(box rho)=Hess(rho)/(6 alpha).
onshell={boxrho2[i,j]:rho2[i,j]/(6*alpha) for i,j in pairs}
for i,j in pairs:
    checks[f'full_scalar_lift_component_{i}{j}']=s.simplify(e[i,j].subs(onshell))==0
# Curvature is rho when the unprolonged equation also holds.
kg_jet={rho2[3,3]:rho/(6*alpha)+rho2[0,0]-rho2[1,1]-rho2[2,2]}
checks['scalar_curvature_normalized_on_shell']=s.simplify((rl-rho).subs(kg_jet))==0

# Pure-gauge linearized scalar curvature vanishes for arbitrary Fourier vector
# and gauge amplitude; the nonzero rho mode cannot be pure gauge.
q=s.Matrix(s.symbols('q0:4'))
xi=s.Matrix(s.symbols('xi0:4'))
gauge=q*xi.T+xi*q.T
q_up=eta*q
q2=(q.T*q_up)[0]
gaugeR=(q_up.T*gauge*q_up)[0]-q2*s.trace(eta*gauge)
checks['gauge_scalar_curvature_zero']=s.expand(gaugeR)==0

# Auxiliary elimination, including the fixed DDR trace-sector sign.
psi=s.symbols('psi')
V=(psi-1)**2/(4*alpha)
density=psi*R-V+2*lam
checks['auxiliary_equation']=s.simplify(s.diff(density,psi)-(R-(psi-1)/(2*alpha)))==0
checks['auxiliary_density_eliminates']=s.simplify(density.subs(psi,1+2*alpha*R)-(R+alpha*R**2+2*lam))==0
g,rc,HessR,boxR=s.symbols('g rc HessR boxR')
aux=(psi*rc-psi*R*g/2+V*g/2-lam*g+2*alpha*(g*boxR-HessR)).subs(psi,1+2*alpha*R)
metric=(1+2*alpha*R)*rc-(R+alpha*R**2)*g/2+2*alpha*(g*boxR-HessR)-lam*g
checks['auxiliary_metric_response_eliminates']=s.simplify(aux-metric)==0
critical=s.simplify(metric.subs({R:-1/(2*alpha),HessR:0,boxR:0,lam:0}))
checks['critical_constant_scalar_response_retained']=critical==g/(8*alpha)

# Independent Legendre check with nondiagonal positive metric and six arbitrary
# K components. The normal velocity is 2NK and shift terms cancel separately.
L=s.Matrix([[1,0,0],[1,1,0],[0,1,1]])
h=L*L.T
hi=h.inv()
pair3=[(i,j) for i in range(3) for j in range(i,3)]
K=sym(s.symbols('K0:6'),3,pair3)
ktr=s.trace(hi*K)
kquad=s.trace(hi*K*hi*K)
pi=(hi*K*hi-ktr*hi)/A  # sqrt(det h)=1
pitr=s.trace(h*pi)
pq=s.trace(h*pi*h*pi)
H=A*(pq-pitr**2/2)-R3/A+D
legendre=2*N*sum(pi[i,j]*K[i,j] for i in range(3) for j in range(3))-N*H
checks['nondiagonal_full_symmetric_Legendre_map']=s.simplify(legendre-N*((kquad-ktr**2+R3)/A-D))==0
vel=2*N*A*(h*pi*h-pitr*h/2)
checks['six_component_kinematic_map']=all(s.simplify(vel[i,j]-2*N*K[i,j])==0 for i,j in pair3)

out={'python':platform.python_version(),'sympy':s.__version__,'arithmetic':'exact symbolic',
     'exposure':'After CANDIDATE.md read; no parent or constructor code imported or read before this script',
     'checks':checks,'passed':sum(checks.values()),'total':len(checks),
     'limit':'Formal first variation about flat fixed lambda=0; no finite-amplitude, stability or global PDE claim.'}
print(json.dumps(out,indent=2,sort_keys=True))
assert all(checks.values()),out
