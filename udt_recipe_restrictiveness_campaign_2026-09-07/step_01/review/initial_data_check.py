"""Independently differentiated original intrinsic constraints; reviewer code only."""
import contextlib
import io
import itertools
import json
from pathlib import Path
import runpy
with contextlib.redirect_stdout(io.StringIO()):
    d=runpy.run_path(str(Path(__file__).with_name('source_first.py')))
s=d['s']; u,v,x,y,k=(d[a] for a in ('u','v','x','y','k'))
g,h,inv,dinv,G,dG,T=(d[a] for a in ('g','h','inv','dinv','G','dG','Tang'))
I=range(4); J=range(3); xyz=(u,x,y); simp=s.simplify
sub={v:-2*u,k:-2}; L=x**3-3*x*y**2+4
dt=s.Matrix([2,1,0,0]); n= -inv*dt/s.sqrt(L)
dL=simp(-(dt.T*dinv*dt)[0]).subs(sub)
dn=(-dinv.subs(sub)*dt/s.sqrt(L)-n*dL/(2*L)).applyfunc(simp)
ga=T.T*g*T; ha=(T.T*h*T).subs(sub)
gi=ga.inv(); hi=-gi*ha*gi
K=s.Matrix(3,3,lambda i,j:simp(-sum(T[a,i]*T[b,j]*dt[c]*G[c,a,b] for a,b,c in itertools.product(I,repeat=3))/s.sqrt(L)))
dK=s.Matrix(3,3,lambda i,j:simp(-sum(T[a,i]*T[b,j]*dt[c]*dG[c,a,b].subs(sub) for a,b,c in itertools.product(I,repeat=3))/s.sqrt(L)-K[i,j]*dL/(2*L)))
assert simp((n.T*g*n)[0]+1)==0
assert simp(2*(dn.T*g*n)[0]+(n.T*h.subs(sub)*n)[0])==0
assert (T.T*(g*dn+h.subs(sub)*n)).applyfunc(simp)==s.zeros(3,1)
GC={}; HC={}
for a,b,c in itertools.product(J,repeat=3):
    dg=[s.diff(ga[z,c],xyz[b])+s.diff(ga[z,b],xyz[c])-s.diff(ga[b,c],xyz[z]) for z in J]
    dh=[s.diff(ha[z,c],xyz[b])+s.diff(ha[z,b],xyz[c])-s.diff(ha[b,c],xyz[z]) for z in J]
    GC[a,b,c]=simp(sum(gi[a,z]*dg[z] for z in J)/2)
    HC[a,b,c]=simp(sum(hi[a,z]*dg[z]+gi[a,z]*dh[z] for z in J)/2)
ric=s.zeros(3); dric=s.zeros(3)
for a,b in itertools.product(J,repeat=2):
    ric[a,b]=simp(sum(s.diff(GC[c,a,b],xyz[c])-s.diff(GC[c,a,c],xyz[b])+sum(GC[c,c,z]*GC[z,a,b]-GC[c,b,z]*GC[z,a,c] for z in J) for c in J))
    dric[a,b]=simp(sum(s.diff(HC[c,a,b],xyz[c])-s.diff(HC[c,a,c],xyz[b])+sum(HC[c,c,z]*GC[z,a,b]+GC[c,c,z]*HC[z,a,b]-HC[c,b,z]*GC[z,a,c]-GC[c,b,z]*HC[z,a,c] for z in J) for c in J))
R3=simp(s.trace(gi*ric)); dR3=simp(s.trace(hi*ric+gi*dric))
A=gi*K; dA=hi*K+gi*dK
ham=simp(R3+s.trace(A)**2-s.trace(A*A))
dham=simp(dR3+2*s.trace(A)*s.trace(dA)-2*s.trace(A*dA))
def mom(A,C):
    return [simp(sum(s.diff(A[j,i],xyz[j])+sum(C[j,j,m]*A[m,i]-C[m,j,i]*A[j,m] for m in J) for j in J)-s.diff(s.trace(A),xyz[i])) for i in J]
momentum=mom(A,GC)
dmomentum=[simp(sum(s.diff(dA[j,i],xyz[j])+sum(HC[j,j,m]*A[m,i]+GC[j,j,m]*dA[m,i]-HC[m,j,i]*A[j,m]-GC[m,j,i]*dA[j,m] for m in J) for j in J)-s.diff(s.trace(dA),xyz[i])) for i in J]
assert ham==dham==0
assert momentum==dmomentum==[0,0,0]
# Explicit first-order root-direction derivative obstruction, independent of scale.
cx=y/(3*(x*x+y*y)); cy=x/(3*(x*x+y*y))
obstruction=s.Matrix([[s.diff(cx,x),s.diff(cy,x)],[s.diff(cx,y),s.diff(cy,y)]])
assert obstruction.subs({x:1,y:0})==s.Matrix([[0,-s.Rational(1,3)],[s.Rational(1,3),0]])
print(json.dumps(dict(gamma0=ga.tolist(),gamma1=ha.tolist(),K0=K.tolist(),K1=dK.tolist(),normal0=list(n),normal1=list(dn),Hamiltonian=[ham,dham],momentum0=momentum,momentum1=dmomentum,root_line_derivative=obstruction.tolist(),root_line_derivative_at_point=obstruction.subs({x:1,y:0}).tolist()),indent=2,default=str))
