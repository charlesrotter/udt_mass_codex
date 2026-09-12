#!/usr/bin/env python3
"""Original-metric source-first check. No parent candidate/code imports."""
import json, platform
import sympy as S
t,x,y,z=S.symbols('t x y z', real=True)
a=S.Function('a')(t,x); P=S.Function('P')(t,x)
coords=(t,x,y,z)
g=S.diag(-S.exp(2*a),S.exp(2*a),t*S.exp(P),t*S.exp(-P))
gi=g.inv()
G=[[[S.simplify(sum(gi[i,l]*(S.diff(g[l,k],coords[j])+S.diff(g[l,j],coords[k])-S.diff(g[j,k],coords[l])) for l in range(4))/2) for k in range(4)] for j in range(4)] for i in range(4)]
def R(i,j,m,n):
    return S.diff(G[i][n][j],coords[m])-S.diff(G[i][m][j],coords[n])+sum(G[i][m][l]*G[l][n][j]-G[i][n][l]*G[l][m][j] for l in range(4))
def Ds(f,s):return S.diff(f,t)+s*S.diff(f,x)
checks={}
for s in (-1,1):
    h=S.exp(-2*a); k=(h,s*h,S.Integer(0),S.Integer(0))
    for i in range(4):
        checks[f'geodesic_{s}_{i}']=S.simplify(h*Ds(k[i],s)+sum(G[i][j][l]*k[j]*k[l] for j in range(4) for l in range(4)))==0
    tides=[]
    for i,sign in ((2,1),(3,-1)):
        b=S.sqrt(t)*S.exp(sign*P/2)
        E=[S.Integer(0)]*4; E[i]=1/b
        for j in range(4):
            checks[f'parallel_{s}_{i}_{j}']=S.simplify(h*Ds(E[j],s)+sum(G[j][m][n]*k[m]*E[n] for m in range(4) for n in range(4)))==0
        T=S.simplify(sum(R(i,j,i,n)*k[j]*k[n] for j in (0,1) for n in (0,1)))
        target=-h*h*(Ds(Ds(b,s),s)-2*Ds(a,s)*Ds(b,s))/b
        checks[f'original_curvature_{s}_{i}']=S.simplify(T-target)==0
        q=Ds(P,s)
        sub={S.diff(a,t):(-1/t+t*(S.diff(P,t)**2+S.diff(P,x)**2))/4,S.diff(a,x):t*S.diff(P,t)*S.diff(P,x)/2}
        Tv=S.simplify(T.subs(sub))
        compact=-sign*h*h*(Ds(q,s)/2+3*q/(4*t)-t*q**3/4)
        checks[f'vacuum_tide_{s}_{i}']=S.simplify(Tv-compact)==0
        tides.append(Tv)
        # Check off-diagonal curvature from the actual metric as well.
        other=5-i
        cross=sum(R(i,j,other,n)*k[j]*k[n] for j in (0,1) for n in (0,1))
        checks[f'cross_tide_{s}_{i}']=S.simplify(cross)==0
    checks[f'vacuum_trace_{s}']=S.simplify(sum(tides))==0
v=S.symbols('v'); b=S.Function('b')(v); I=S.Function('I')(v)
D=b*I
jac=S.diff(D,v,2)-S.diff(b,v,2)/b*D
checks['integral_jacobi']=S.simplify(jac.subs({S.diff(I,v,2):-2*S.diff(b,v)/b**3,S.diff(I,v):1/b**2}))==0
checks['integral_vertex_slope']=S.simplify(S.diff(D,v).subs({S.diff(I,v):1/b**2,I:0})*b)==1
print(json.dumps({'kind':'exact symbolic original metric check; zeros not independent evidence counts','python':platform.python_version(),'sympy':S.__version__,'checks':checks,'passed':sum(checks.values()),'total':len(checks)},indent=2,sort_keys=True))
assert all(checks.values()),'source-first original-metric check failed'
