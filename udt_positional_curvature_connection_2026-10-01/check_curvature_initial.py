"""PCC1 original-coordinate curvature check; no imported curvature routine."""
import itertools,json,sys,platform
import sympy as s
from pathlib import Path
N=4; inds=range(N); t,r,th,ph=s.symbols('t r theta phi',real=True); mu,k=s.symbols('mu kappa',real=True)
x=(t,r,th,ph); f=1-2*mu/r-k*r*r; eta=(-1,1,1,1)
g=(-f,1/f,r*r,r*r*s.sin(th)**2)
Gamma={}
def simp(z):return s.factor(s.trigsimp(s.cancel(z)))
for a,b,c in itertools.product(inds,repeat=3):
 z=sum((s.diff(g[d],x[b]) if d==c else 0)+(s.diff(g[d],x[c]) if d==b else 0)-(s.diff(g[b],x[d]) if b==c else 0) for d in [a])/(2*g[a])
 z=simp(z)
 if z!=0:Gamma[a,b,c]=z
G=lambda a,b,c:Gamma.get((a,b,c),s.S.Zero)
# A(i,j,b,a)=g(R(di,dj)db,da), using the original Christoffels.
A={}
for i,j,b,a in itertools.product(inds,repeat=4):
 z=s.diff(G(a,j,b),x[i])-s.diff(G(a,i,b),x[j])+sum(G(a,i,c)*G(c,j,b)-G(a,j,c)*G(c,i,b) for c in inds)
 z=simp(g[a]*z)
 if z!=0:A[i,j,b,a]=z
# Each nonzero component has even occurrences of every basis index. On f>0,
# 0<theta<pi the products of the orthonormal basis factors have these squares.
e2=(1/f,f,1/r**2,1/(r*r*s.sin(th)**2)); Ah={}
for idx,z in A.items():
 counts=[idx.count(i) for i in inds];assert all(c%2==0 for c in counts),(idx,counts)
 Ah[idx]=simp(z*s.prod(e2[i]**(counts[i]//2) for i in inds))
H=lambda idx:Ah.get(tuple(idx),s.S.Zero)
B=lambda i,j,a,b: (eta[j]*eta[i] if j==a and i==b else 0)-(eta[i]*eta[j] if i==a and j==b else 0)
checks=[]
def eq(name,a,b=0):
 z=simp(a-b);assert z==0,(name,z);checks.append(name)
# Independent target formulas are used only AFTER original curvature was obtained.
w=mu/r**3
six={(1,0,0,1):-2*w-k,(2,0,0,2):w-k,(3,0,0,3):w-k,(1,2,2,1):-w+k,(1,3,3,1):-w+k,(2,3,3,2):2*w+k}
for idx,z in six.items():eq('tidal_'+str(idx),H(idx),z)
for idx in itertools.product(inds,repeat=4):
 eq('delta_'+''.join(map(str,idx)),H(idx)-H(idx).subs(k,0),k*B(*idx))
Ric=s.Matrix(N,N,lambda a,b:sum(eta[i]*H((i,a,b,i)) for i in inds))
for a,b in itertools.product(inds,repeat=2):eq('Ric_'+str((a,b)),Ric[a,b],3*k*eta[a] if a==b else 0)
R=sum(eta[a]*Ric[a,a] for a in inds);eq('scalar',R,12*k)
Kretsch=sum(s.prod(eta[a] for a in idx)*H(idx)**2 for idx in itertools.product(inds,repeat=4));eq('Kretschmann',Kretsch,48*w*w+24*k*k)
W2=sum(s.prod(eta[a] for a in idx)*(H(idx)-k*B(*idx))**2 for idx in itertools.product(inds,repeat=4));eq('Weyl_square',W2,48*w*w)
# Finite rational boost/direction tests of the derived component difference.
def tensor_contraction(dic,X,Y,Z,W):
 return sum(dic.get(idx,0)*X[idx[0]]*Y[idx[1]]*Z[idx[2]]*W[idx[3]] for idx in itertools.product(inds,repeat=4))
D={idx:simp(z-z.subs(k,0)) for idx,z in Ah.items()}
U=[s.Rational(5,4),s.Rational(3,4),0,0];n=[0,0,1,0]
eq('boost_norm',sum(eta[i]*U[i]**2 for i in inds),-1)
eq('boosted_delta_tide',tensor_contraction(D,n,U,U,n),-k)
# One-frame false-pass control: a spatial constant-curvature tensor.
S={idx:B(*idx) for idx in itertools.product(inds,repeat=4) if all(a>0 for a in idx)}
U0=[1,0,0,0]
for j in (1,2,3):
 nj=[int(i==j) for i in inds];eq('one_frame_blind_'+str(j),tensor_contraction(S,nj,U0,U0,nj))
eq('boost_exposes_spatial_curvature',tensor_contraction(S,n,U,U,n),s.Rational(9,16))
# Physical patch controls: mu=1/50,r=1,k=1/25 gives f=23/25,f0=24/25.
subs={mu:s.Rational(1,50),r:1,k:s.Rational(1,25)}
eq('positive_patch',f.subs(subs),s.Rational(23,25));eq('reference_patch',f.subs(k,0).subs(subs),s.Rational(24,25))
assert f.subs(subs)>0 and f.subs(k,0).subs(subs)>0
# Deliberately wrong sign and total-isotropy assertions must fail.
assert simp(H((1,0,0,1))-(-k))!=0
assert simp(tensor_contraction(D,n,U,U,n)-k)!=0
checks.extend(['negative_control_total_isotropy_rejected','negative_control_wrong_sign_rejected'])
result={'status':'PASS','checks':len(checks),'check_labels':checks,'python':platform.python_version(),'sympy':s.__version__,'convention':'A(i,j,b,a)=g(R(di,dj)db,da)','metric_diagonal':[str(z) for z in g],'christoffels':{','.join(map(str,idx)):str(z) for idx,z in Gamma.items()},'coordinate_curvature':{','.join(map(str,idx)):str(z) for idx,z in A.items()},'orthonormal_curvature':{','.join(map(str,idx)):str(z) for idx,z in Ah.items()},'Ricci':[[str(z) for z in row] for row in Ric.tolist()],'scalar':str(R),'Kretschmann':str(simp(Kretsch)),'Weyl_square':str(simp(W2)),'positive_patch':{str(a):str(b) for a,b in subs.items()},'boosted_spatial_control':'9/16','limits':'Exact component/regression controls, not proof of all-frame polarization, finite-clock integration, empirical or native admission.'}
print(json.dumps(result,indent=2,sort_keys=True))
