"""Independent exact matrix-connection calculation; mathematical method only."""
import itertools
import json
import platform
import sympy as s

u,v,x,y,e,c=s.symbols('u v x y e c', real=True)
z=(u,v,x,y); ids=range(4); slots=list(itertools.product(ids,repeat=4))
H=x**3-3*x*y*y-2*e*v*y+c*e*e*x**4
g=s.Matrix([[H,-1,0,e*x*x],[-1,0,0,0],[0,0,1,0],[e*x*x,0,0,1]])
gi=g.inv()
clean=lambda q:s.factor(q)
# Gamma[a] is the connection matrix for differentiation in coordinate a.
Gamma=[s.Matrix(4,4,lambda d,b:clean(sum(gi[d,h]*(s.diff(g[h,b],z[a])+s.diff(g[h,a],z[b])-s.diff(g[a,b],z[h])) for h in ids)/2)) for a in ids]
R={(a,b): (Gamma[b].diff(z[a])-Gamma[a].diff(z[b])+Gamma[a]*Gamma[b]-Gamma[b]*Gamma[a]).applyfunc(clean) for a,b in itertools.product(ids,repeat=2)}
Q={t:clean(sum(g[t[3],h]*R[t[0],t[1]][h,t[2]] for h in ids)) for t in slots}
Ric=s.Matrix(4,4,lambda b,d:clean(sum(R[a,b][a,d] for a in ids)))
scalar=clean(s.trace(gi*Ric))
coefficient=s.solve(Ric[0,0],c)
assert coefficient==[s.Rational(2,3)], coefficient
gc=g.subs(c,coefficient[0]); gic=gi.subs(c,coefficient[0])
assert Ric.subs(c,coefficient[0])==s.zeros(4)
p={u:0,v:0,x:1,y:0,c:coefficient[0]}
gp=g.subs(p); gip=gi.subs(p); W={k:q.subs(p) for k,q in Q.items()}
def dual(A, inverse):
    return {(a,b,d,h):clean(sum(s.LeviCivita(a,b,k,l)*inverse[k,m]*inverse[l,n]*A[m,n,d,h] for k,l,m,n in slots)/2) for a,b,d,h in slots}
star=dual(W,gip)
B={(a,b,d,f):clean(sum(gip[h,k]*gip[m,n]*(W[a,h,d,m]*W[b,k,f,n]+star[a,h,d,m]*star[b,k,f,n]) for h,k,m,n in slots)) for a,b,d,f in slots}
minor=clean(B[0,0,0,0]*B[0,2,0,2]-B[0,0,0,2]**2)
minor_y=clean(B[0,0,0,0]*B[0,3,0,3]-B[0,0,0,3]**2)
assert minor !=0 or minor_y!=0
# All slots of unperturbed B reproduce the source root.
assert all(clean(val.subs(e,0)-(36 if k==(0,0,0,0) else 0))==0 for k,val in B.items())
# Complete induced data on the same fixed spacelike graph.
dt=s.Matrix([2,1,0,0]); S=clean(-(dt.T*gic*dt)[0]); X=s.Matrix([[1,0,0],[-2,0,0],[0,1,0],[0,0,1]])
gamma=(X.T*gc*X).subs(v,-2*u).applyfunc(clean)
Ss=S.subs(v,-2*u); normal=-(gic*dt).subs(v,-2*u)/s.sqrt(Ss)
K=s.Matrix(3,3,lambda i,j:clean(-sum(X[a,i]*X[b,j]*(2*Gamma[a][0,b]+Gamma[a][1,b]) for a,b in itertools.product(ids,repeat=2)).subs(c,coefficient[0]).subs(v,-2*u)/s.sqrt(Ss)))
assert clean(gamma.det()-Ss)==0
assert clean((normal.T*gc.subs(v,-2*u)*normal)[0]+1)==0
assert (X.T*gc.subs(v,-2*u)*normal).applyfunc(clean)==s.zeros(3,1)
assert S.subs({u:0,v:0,x:1,y:0,e:0})==5
def nz(A):return {','.join(map(str,k)):str(val) for k,val in A.items() if val!=0}
print(json.dumps(dict(python=platform.python_version(),sympy=s.__version__,Ricci=[[str(q) for q in Ric.row(i)] for i in ids],scalar=str(scalar),completion_coefficient=str(coefficient[0]),S=str(S),gamma=str(gamma),K=str(K),normal=str(normal),root_minor_x=str(minor),root_minor_y=str(minor_y),event_B=nz(B),event_Q=nz(W),event_dual=nz(star),full_Ricci_zero=True,full_baseline_root=True,full_data_normalization=True),indent=2))
