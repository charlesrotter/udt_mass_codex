"""Independent exact NT2 checks, constructed before author NT2 exposure.

Physics inputs: supplied smooth (-+++) metric and owner-provisional Ric=Lambda g.
Witness Lambda=0, chart/profile/slice: FREE supplied restricted construction.
SymPy is a mathematical method; no imported author scientific implementation.
"""
import itertools as it
import json
import platform
from functools import lru_cache
import sympy as s

def emit(name, value):
    print(json.dumps({name: value}, default=str, sort_keys=True), flush=True)

emit('versions', {'python': platform.python_version(), 'sympy': s.__version__})
ii = range(4)
pairs = list(it.combinations(ii, 2))
pairindex = {p:i for i,p in enumerate(pairs)}
eta = s.diag(-1,1,1,1)
unknowns = s.symbols('q0:21')
bilinear = s.zeros(6)
for k,(i,j) in enumerate(it.combinations_with_replacement(range(6),2)):
    bilinear[i,j] = bilinear[j,i] = unknowns[k]

def Q(a,b,c,d):
    if a==b or c==d:
        return s.S.Zero
    sign = (1 if a<b else -1)*(1 if c<d else -1)
    return sign*bilinear[pairindex[tuple(sorted((a,b)))],pairindex[tuple(sorted((c,d)))]]

alg = [Q(a,b,c,d)+Q(b,c,a,d)+Q(c,a,b,d) for a,b,c,d in it.product(ii,repeat=4)]
alg += [sum(eta[a,a]*Q(a,b,c,a) for a in ii) for b,c in it.product(ii,repeat=2)]
algM = s.linear_eq_to_matrix(alg, unknowns)[0]
basis = algM.nullspace()
assert len(basis)==10 and algM.rank()==11
Qbasis = s.Matrix.hstack(*basis)
qflat = s.Matrix([Q(*a) for a in it.product(ii,repeat=4)])
qmap = qflat.jacobian(unknowns)*Qbasis
emit('weyl_space', {'ambient':21, 'constraint_rank':11, 'dimension':10})

def factor_matrix(nu):
    eq=[nu[m]*Q(a,b,c,d)+nu[a]*Q(b,m,c,d)+nu[b]*Q(m,a,c,d)
        for m,a,b in it.combinations(ii,3) for c,d in pairs]
    return s.linear_eq_to_matrix(eq,unknowns)[0]*Qbasis

matrices={}
for name,nu,expected in [('timelike',[1,0,0,0],10),('spacelike',[0,1,0,0],10),('null',[1,0,0,1],8)]:
    M=factor_matrix(nu)
    assert M.rank()==expected
    matrices[name]=M
    emit(name, {'nu':nu,'rank':M.rank(),'kernel_dimension':10-M.rank(), 'matrix':M.tolist()})

n=s.Matrix([1,0,0,1])
a,b=s.symbols('a b',real=True)
H=s.zeros(4)
H[1,1],H[1,2],H[2,1],H[2,2]=a,b,b,-a
P=s.Matrix([n[i]*n[k]*H[j,l]-n[j]*n[k]*H[i,l]-n[i]*n[l]*H[j,k]+n[j]*n[l]*H[i,k]
            for i,j,k,l in it.product(ii,repeat=4)])
Pmap=P.jacobian([a,b])
nullbasis=qmap*s.Matrix.hstack(*matrices['null'].nullspace())
assert Pmap.rank()==2 and nullbasis.row_join(Pmap).rank()==2
emit('null_shape', {'complete_kernel_matches_two_real_screen_amplitudes':True,
                    'electric': [[s.expand(P[(i*64)+j]) for j in range(1,4)] for i in range(1,4)]})

u,v,x,y=s.symbols('u v x y',real=True)
coords=(u,v,x,y)
F=u*(a*(x*x-y*y)+2*b*x*y)
g=s.Matrix([[F,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
gi=g.inv()
assert g.det()==-1 and gi[0,0]==0 and gi[0,1]==-1 and s.simplify(gi[1,1]+F)==0

def geometry(metric,coordinates):
    dim=len(coordinates)
    jj=range(dim)
    inverse=metric.inv()
    @lru_cache(None)
    def Gamma(k,i,j):
        return s.simplify(sum(inverse[k,l]*(s.diff(metric[l,j],coordinates[i])+s.diff(metric[l,i],coordinates[j])-s.diff(metric[i,j],coordinates[l])) for l in jj)/2)
    @lru_cache(None)
    def Rup(r,i,j,k):
        return s.simplify(s.diff(Gamma(r,j,k),coordinates[i])-s.diff(Gamma(r,i,k),coordinates[j])+sum(Gamma(r,i,h)*Gamma(h,j,k)-Gamma(r,j,h)*Gamma(h,i,k) for h in jj))
    @lru_cache(None)
    def Rlow(i,j,k,l):
        return s.simplify(sum(metric[l,r]*Rup(r,i,j,k) for r in jj))
    ric=s.Matrix(dim,dim,lambda j,k:s.simplify(sum(Rup(i,i,j,k) for i in jj)))
    return inverse,Gamma,Rup,Rlow,ric

_,Gamma,Rup,Rlow,ric=geometry(g,coords)
assert ric==s.zeros(4)
Qvals={inds:Rlow(*inds) for inds in it.product(ii,repeat=4)}
origin={u:0,v:0,x:0,y:0}
assert all(expr.subs(origin)==0 for expr in Qvals.values())
assert Rlow(0,2,0,2)==a*u and Rlow(0,2,0,3)==b*u and Rlow(0,3,0,3)==-a*u
n0=(1,0,0,0)
H0=s.zeros(4)
H0[2,2],H0[2,3],H0[3,2],H0[3,3]=a,b,b,-a
def P0(i,j,k,l):
    return n0[i]*n0[k]*H0[j,l]-n0[j]*n0[k]*H0[i,l]-n0[i]*n0[l]*H0[j,k]+n0[j]*n0[l]*H0[i,k]
fulljet=[]
for m,inds in it.product(ii,it.product(ii,repeat=4)):
    expr=s.diff(Qvals[inds],coords[m])
    for slot in ii:
        for r in ii:
            replaced=list(inds); replaced[slot]=r
            expr-=Gamma(r,m,inds[slot])*Qvals[tuple(replaced)]
    value=s.simplify(expr.subs(origin))
    assert s.simplify(value-n0[m]*P0(*inds))==0
    if value!=0: fulljet.append([m,*inds,str(value)])
emit('actual_metric', {'determinant':-1,'full_Ricci':ric.tolist(),
      'curvature_nonzero_components':[[*k,str(val)] for k,val in Qvals.items() if val!=0],
      'full_covariant_jet_nonzero':fulljet,'all_1024_jet_components_match':True,
      'scalar_sector':0,'metric_equation_is_neighborhood_identity':True})

z,X,Y=s.symbols('z X Y',real=True)
f=s.Function('f')(z,X,Y)
A=1+f
gamma=s.diag(A,1,1)
gami,Gam3,_,_,ric3=geometry(gamma,(z,X,Y))
K=s.Matrix([[-s.diff(f,z),-s.diff(f,X),-s.diff(f,Y)],[-s.diff(f,X),0,0],[-s.diff(f,Y),0,0]])/(2*s.sqrt(A))
Kmix=gami*K
trK=s.trace(Kmix)
R3=s.simplify(s.trace(gami*ric3))
ham=s.simplify(R3+trK**2-s.trace(Kmix*Kmix))
cs=(z,X,Y)
mom=[]
for i in range(3):
    div=sum(s.diff(Kmix[j,i],cs[j]) for j in range(3))
    div+=sum(Gam3(j,j,r)*Kmix[r,i]-Gam3(r,j,i)*Kmix[j,r] for j,r in it.product(range(3),repeat=2))
    mom.append(s.simplify(div-s.diff(trK,cs[i])))
lap=s.diff(f,X,2)+s.diff(f,Y,2)
assert s.simplify(ham+lap/A)==0
assert s.simplify(mom[0]+lap/(2*s.sqrt(A)))==0
assert mom[1:]==[0,0]

# Independent lapse/shift calculation of the sign and every K component.
beta=s.Matrix([-f,0,0])
dtgamma=s.zeros(3); dtgamma[0,0]=-s.diff(f,z)
KfromADM=s.Matrix(3,3,lambda i,j:s.simplify(s.sqrt(A)/2*(-dtgamma[i,j]+s.diff(beta[j],cs[i])+s.diff(beta[i],cs[j])-2*sum(Gam3(r,i,j)*beta[r] for r in range(3)))))
assert s.simplify(KfromADM-K)==s.zeros(3)
f0=-z*(a*(X*X-Y*Y)+2*b*X*Y)/(2*s.sqrt(2))
assert s.simplify(s.diff(f0,X,2)+s.diff(f0,Y,2))==0
emit('lawful_spacelike_data', {'domain':'A=1+f>0, open near origin; no boundary',
     'K_from_original_minus_half_Lie_normal':KfromADM.tolist(), 'R3':R3,
     'Hamiltonian':ham,'momentum':mom,
     'all_four_residuals_zero_for_transverse_harmonic_witness':True})
emit('PASS', {'full_tensor_classification':True,'actual_local_Ricci_flat_realization':True,
              'lawful_spacelike_constraints':True,'general_Lambda_realization':'NOT_CLAIMED'})
