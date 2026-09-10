"""Additional data-map checks prompted by review of the author time check.

Differentiate actual local Lie derivatives before restricting to the observer.
Reuses only the reviewer's exact sphere integral; imports no constructor code.
No curvature identity is used. Exact CPU, no physical realization claimed.
"""
import json
import sys
import sympy as S
from check_independent import angular, clean, coords, ns

t,x,y,z=coords
nx,ny,nz=ns
Ubase=S.Matrix([1,0,0,0])
spacezero={x:0,y:0,z:0}
records=[]

def from_metric(name,g,U,F):
    L=S.Matrix(4,4,lambda a,b:sum(
        U[c]*S.diff(g[a,b],coords[c]) + g[c,b]*S.diff(U[c],coords[a]) +
        g[a,c]*S.diff(U[c],coords[b]) for c in range(4)))
    K=S.Matrix([1]+[n/f for n,f in zip(ns,F)])
    gc=g.subs(spacezero)
    unit_null=clean((K.T*gc*K)[0] - (sum(n*n for n in ns)-1))
    if unit_null != 0:
        raise AssertionError((name,'null norm',unit_null))
    qtime=clean(-(K.T*L.subs(spacezero)*K)[0]/2)
    mtime=angular(qtime)
    drift=clean(S.diff(mtime,t).subs(t,0))
    records.append({'name':name,'q_on_central_worldline':str(qtime),
                    'mean_on_central_worldline':str(mtime),
                    'dot_mean_at_origin':str(drift),'null_norm_residual':str(unit_null)})
    return qtime,mtime,drift,L

beta,kappa,b,s=S.symbols('beta kappa b s',real=True)
F=[S.exp(beta*t*t/2)]*3
q,m,dm,_=from_metric('drift',S.diag(-1,*[f*f for f in F]),Ubase,F)
assert dm==-beta and q.subs(t,0)==0
N=1+kappa*(x*x+y*y+z*z)/2
q,m,dm,_=from_metric('static_lapse',S.diag(-N*N,1,1,1),Ubase/N,[1,1,1])
assert q==m==dm==0  # t is still an unconstrained symbol here.
B=S.Matrix([1,-b*y/2,b*x/2,0])
q,m,dm,L=from_metric('unit_Killing_twist',S.diag(0,1,1,1)-B*B.T,Ubase,[1,1,1])
assert L==S.zeros(4)  # full neighborhood, before worldline restriction.
assert q==m==dm==0
F=[S.exp(s*t),S.exp(-s*t),1]
q,m,dm,_=from_metric('shear',S.diag(-1,*[f*f for f in F]),Ubase,F)
assert clean(q+s*(nx*nx-ny*ny))==0 and m==dm==0
F=[S.exp(t+t*t),S.exp(2*t-t*t),S.exp(-t+S.Rational(3,2)*t*t)]
N=1+2*x+S.Rational(3,2)*(x*x+y*y+z*z)
B=S.Matrix([1,-2*y,2*x,0])
q,m,dm,_=from_metric('mixed',S.diag(0,*[f*f for f in F])-N*N*B*B.T,Ubase/N,F)
assert clean(m+S.Rational(2,3)+t)==0 and dm==-1
print(json.dumps({'status':'PASS','versions':{'python':sys.version.split()[0],
      'sympy':S.__version__},'records':records,
      'evidence':'exact Lie-derivative clock data with t retained through angular averaging'},indent=2))
