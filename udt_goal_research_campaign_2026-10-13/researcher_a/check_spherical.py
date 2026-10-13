"""Exact GRC1 A2: metric-first curvature and null-affine areal identities."""
import sympy as s
import json,platform
checks={}; outputs={}
def connection(g,coords):
    gi=g.inv(); n=len(coords)
    return [[[s.simplify(sum(gi[a,d]*(s.diff(g[d,c],coords[j])+s.diff(g[d,j],coords[c])-s.diff(g[j,c],coords[d])) for d in range(n))/2) for c in range(n)] for j in range(n)] for a in range(n)]
def curvature(g,coords,G):
    n=len(coords)
    return [[[[s.simplify(s.diff(G[a][j][c],coords[i])-s.diff(G[a][i][c],coords[j])+sum(G[a][i][d]*G[d][j][c]-G[a][j][d]*G[d][i][c] for d in range(n))) for j in range(n)] for i in range(n)] for c in range(n)] for a in range(n)]
def zero(m):return all(s.simplify(v)==0 for v in m)
t,r,th,ph,mu=s.symbols('t r th ph mu',positive=True)
f=1-2*mu/r
coords=[t,r,th,ph]
g=s.diag(-f,1/f,r*r,r*r*s.sin(th)**2)
G=connection(g,coords); R=curvature(g,coords,G)
# e0=f^-1/2 partial_t, e1=f^1/2 partial_r,e2=1/r partial_th
# R(e0,e1) and R(e0,e2) in tetrad: factor s_i s_j s_b / s_a.
sc=[1/s.sqrt(f),s.sqrt(f),1/r,1/(r*s.sin(th))]
ops=[]
for j in [1,2]:
    ops.append(s.Matrix(4,4,lambda a,c:s.simplify(R[a][c][0][j]*sc[0]*sc[j]*sc[c]/sc[a])))
B1=s.zeros(4);B1[0,1]=B1[1,0]=1
B2=s.zeros(4);B2[0,2]=B2[2,0]=1
checks['schwarzschild_radial_boost']=zero(ops[0]-2*mu/r**3*B1)
checks['schwarzschild_transverse_boost']=zero(ops[1]+mu/r**3*B2)
outputs['schwarzschild_boost_coefficients']=[str(ops[0][0,1]),str(ops[1][0,2])]
# General spherical diagonal base: null vectors k+=(sqrt(B),sqrt(A)),
# k-=(sqrt(B),-sqrt(A)); these represent directions only, affine extension exists.
A=s.Function('A',positive=True)(t,r); B=s.Function('B',positive=True)(t,r)
h=s.diag(-A,B); C=connection(h,[t,r]); Hess=-s.Matrix(2,2,lambda i,j:C[1][i][j])
kp=s.Matrix([s.sqrt(B),s.sqrt(A)]); km=s.Matrix([s.sqrt(B),-s.sqrt(A)])
np=s.simplify((kp.T*Hess*kp)[0]);nm=s.simplify((km.T*Hess*km)[0])
checks['null_hessian_sum']=s.simplify(np+nm+s.diff(A,r)+A*s.diff(B,r)/B)==0
checks['null_hessian_difference']=s.simplify(np-nm+2*s.sqrt(A/B)*s.diff(B,t))==0
# This means both vanish iff B_t=0 and partial_r(A B)=0.
# With B_t=0, A B depends on t alone, removable by time reparameterization.
F=1/B; K=s.Matrix([1/s.sqrt(A*B),0]); Kflat=h*K
Lie=s.Matrix(2,2,lambda i,j:sum(K[d]*s.diff(h[i,j],[t,r][d])+h[d,j]*s.diff(K[d],[t,r][i])+h[i,d]*s.diff(K[d],[t,r][j]) for d in range(2)))
Lie=s.simplify(Lie)
checks['kodama_lie_tt']=s.simplify(Lie[0,0]-s.sqrt(A/B)*s.diff(B,t)/B)==0
checks['kodama_lie_rr']=s.simplify(Lie[1,1]-s.diff(B,t)/s.sqrt(A*B))==0
checks['kodama_lie_tr']=s.simplify(Lie[0,1]-s.diff(A*B,r)/(2*B*s.sqrt(A*B)))==0
outputs['diagonal_null_hessian_sum']=str(s.simplify(np+nm))
outputs['diagonal_null_hessian_difference']=str(s.simplify(np-nm))
# The time-live reciprocal metric A=f(t,r),B=1/f has determinant -1,
# but violates NAR whenever f_t != 0.
q=s.Function('q',positive=True)(t,r)
Hp=Hess.subs({A:q,B:1/q}).doit()
kps=kp.subs({A:q,B:1/q});kms=km.subs({A:q,B:1/q})
qp=s.simplify((kps.T*Hp*kps)[0]); qm=s.simplify((kms.T*Hp*kms)[0])
checks['reciprocal_dynamic_plus']=s.simplify(qp-s.diff(q,t)/q)==0
checks['reciprocal_dynamic_minus']=s.simplify(qm+s.diff(q,t)/q)==0
outputs['reciprocal_dynamic_null_hessians']=[str(qp),str(qm)]
# One-direction EF comparison, arbitrary f(v,r), no field equation.
v=s.symbols('v',real=True); Q=s.Function('F')(v,r)
e=s.Matrix([[-Q,1],[1,0]]); EC=connection(e,[v,r]);EH=-s.Matrix(2,2,lambda i,j:EC[1][i][j])
l=s.Matrix([0,-1]);nn=s.Matrix([1,Q/2])
checks['ef_first_direction_affine']=all(EC[a][1][1]==0 for a in range(2))
checks['ef_first_hessian']=s.simplify((l.T*EH*l)[0])==0
checks['ef_second_hessian']=s.simplify((nn.T*EH*nn)[0]-s.diff(Q,v)/2)==0
outputs['ef_second_null_hessian']=str(s.simplify((nn.T*EH*nn)[0]))
# Original 4D Ricci vs radial Hessian for EF metric. This also checks angular terms retained.
eg=s.Matrix([[-Q,1,0,0],[1,0,0,0],[0,0,r*r,0],[0,0,0,r*r*s.sin(th)**2]])
EG=connection(eg,[v,r,th,ph]);ER=curvature(eg,[v,r,th,ph],EG)
Ric=s.Matrix(4,4,lambda c,j:s.simplify(sum(ER[a][c][a][j] for a in range(4))))
ll=s.Matrix([0,-1,0,0]);nn4=s.Matrix([1,Q/2,0,0])
checks['ef_radial_ricci_first']=s.simplify((ll.T*Ric*ll)[0])==0
checks['ef_radial_ricci_second']=s.simplify((nn4.T*Ric*nn4)[0]+s.diff(Q,v)/r)==0
outputs['ef_second_radial_ricci']=str(s.simplify((nn4.T*Ric*nn4)[0]))
result={'python':platform.python_version(),'sympy':s.__version__,'checks':checks,'passed':all(checks.values()),'outputs':outputs,'meaning':'Exact coordinate recomputation and symbolic identities; no adoption, source equation or global coverage.'}
print(json.dumps(result,indent=2));assert all(checks.values()),result
