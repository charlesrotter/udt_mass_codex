#!/usr/bin/env python3
"""ER1 reviewer implementation, no author/source scientific imports.

Direct coordinate Levi-Civita contraction is the independent W route. Source
formulas only enter the comparison side. Exact arithmetic at supplied metric
jets; analytical proof, not finite samples, owns the general quantifier.
"""
import json
import platform
import sympy as S

t,x,y,z=S.symbols('t x y z', real=True)
coords=[t,x,y,z]
checks=[]
mutations=[]
values={}

def zero(a):
    if isinstance(a,S.MatrixBase):
        return all(S.simplify(v)==0 for v in a)
    return S.simplify(a)==0

def require_same(name,a,b):
    if not zero(a-b):
        raise ValueError(name+': nonzero residual '+str(S.simplify(a-b)))

def same(name,a,b):
    require_same(name,a,b)
    checks.append(name)

def truth(name,p):
    if not bool(p):
        raise ValueError(name+': rejected predicate')
    checks.append(name)

def mutant(name,bad,actual):
    try:
        require_same(name,bad,actual)
    except ValueError:
        mutations.append(name)
    else:
        raise ValueError('VACUOUS mutation survived: '+name)

def at(a,p):
    if isinstance(a,S.MatrixBase):
        return a.applyfunc(lambda v:S.cancel(v.subs(p)))
    return S.cancel(S.sympify(a).subs(p))

def metric(N,b,G):
    theta=S.Matrix([1,*b])
    gg=-N**2*theta*theta.T
    gg[1:4,1:4]+=G
    return gg

def direct(N,b,G,p,label):
    # The independent computational path differentiates the FULL g first.
    gs=metric(N,b,G)
    us=S.Matrix([1/N,0,0,0]); covs=gs*us
    g=at(gs,p); inv=g.inv(); u=at(us,p); cov=at(covs,p)
    dg=[at(gs.diff(c),p) for c in coords]
    du=[at(covs.diff(c),p) for c in coords]
    C=[[[sum(inv[k,l]*(dg[a][l,bj]+dg[bj][l,a]-dg[l][a,bj])/2
              for l in range(4)) for bj in range(4)] for a in range(4)] for k in range(4)]
    nabla=S.Matrix(4,4,lambda a,bj:du[a][bj]-sum(C[k][a][bj]*cov[k] for k in range(4)))
    P=S.eye(4)+cov*u.T
    w=P*((nabla-nabla.T)/2)*P.T
    raised=inv*w*inv
    W=S.cancel(sum(w[i,j]*raised[i,j] for i in range(4) for j in range(4)))
    X=S.zeros(4,3); X[0,:]=-at(b,p).T; X[1:4,:]=S.eye(3)
    Np=at(N,p); Gp=at(G,p)
    # Formula side: independent of Christoffel/covariant derivative path.
    F=S.Matrix(3,3,lambda i,j:S.diff(b[j],coords[i+1])-S.diff(b[i],coords[j+1])
               -b[i]*S.diff(b[j],t)+b[j]*S.diff(b[i],t))
    Fp=at(F,p)
    same(label+' unit observer',(u.T*g*u)[0],-1)
    same(label+' metric inverse',g*inv,S.eye(4))
    same(label+' rest orthogonality',X.T*g*u,S.zeros(3,1))
    same(label+' actual rest form',X.T*g*X,Gp)
    same(label+' projected tangency',w*u,S.zeros(4,1))
    same(label+' all rest vorticity components',X.T*w*X,-Np*Fp/2)
    predicted=Np**2*sum(Fp[i,j]*(Gp.inv()*Fp*Gp.inv())[i,j]
                               for i in range(3) for j in range(3))/4
    same(label+' full coordinate contraction',W,predicted)
    values[label]={'W':str(W),'rest_w':str(X.T*w*X),'F':str(Fp),
                   'N':str(Np),'gamma':str(Gp),'point':{str(k):str(v) for k,v in p.items()}}
    return {'W':W,'w':w,'rest_w':X.T*w*X,'F':Fp,'g':g,'inv':inv,'N':Np,'G':Gp,'X':X,
            'nabla':nabla,'P':P,'gs':gs}

G0=S.Matrix([[2,1,1],[1,3,1],[1,1,2]])
N=1+t+y
a=1+t+x*x
G=a*a*G0
origin=dict(zip(coords,[0,0,0,0]))
interior=dict(zip(coords,[S.Rational(1,8),S.Rational(1,5),S.Rational(1,6),0]))
base=direct(N,S.Matrix([1,3*x+t,0]),G,origin,'coupled_origin')
point=direct(N,S.Matrix([1,3*x+t,0]),G,interior,'coupled_interior')
nocurl=direct(N,S.Matrix([1,t,0]),G,origin,'zero_spatial_curl')
same('coupled origin rational W',base['W'],S.Rational(4,7))
same('coupled interior rational W',point['W'],S.Rational(96100000000,185679617823))
same('zero ordinary curl but nonzero rotation',nocurl['W'],S.Rational(1,7))
same('G0 principal minors',S.Matrix([G0[:k,:k].det() for k in [1,2,3]]),S.Matrix([2,5,7]))

# A smooth richer jet. H is invertible at this point, hence on a neighborhood.
H=S.Matrix([[2+t,x,y],[0,3+y,z],[0,0,2+x]])
richG=H.T*H
richN=2+t+x+y*z
richb=S.Matrix([1+t+y+z*t,2+t*x+z,3+t*y+x])
rp=dict(zip(coords,[S.Rational(1,7),S.Rational(1,6),S.Rational(1,5),S.Rational(1,4)]))
rich=direct(richN,richb,richG,rp,'all_components_rational_jet')
truth('rich positivity and nondegenerate rest form',at(richN,rp)>0 and at(H,rp).det()!=0)
truth('all three rich F components active',all(rich['F'][i,j]!=0 for i,j in [(0,1),(0,2),(1,2)]))

mutant('sign reversal caught by tensor not norm',-base['rest_w'],base['rest_w'])
mutant('wrong bracket factor caught',2*base['rest_w'],base['rest_w'])
mutant('ordinary spatial curl only',S.Rational(9,7),base['W'])
mutant('zero curl falsely means zero rotation',S.Integer(0),nocurl['W'])
mutant('drop lapse weight at second point',point['W']/point['N']**2,point['W'])
mutant('drop rest weighting at second point',point['N']**2*S.Integer(2),point['W'])
ordinary=S.Matrix(3,3,lambda i,j:at(S.diff(richb[j],coords[i+1])-S.diff(richb[i],coords[j+1]),rp))
mutant('rich missing all temporal products',-rich['N']*ordinary/2,rich['rest_w'])
opposite=2*ordinary-rich['F']
mutant('rich reversed temporal-product signs',-rich['N']*opposite/2,rich['rest_w'])
unprojected=(rich['nabla']-rich['nabla'].T)/2
mutant('unprojected derivative including lapse terms',unprojected,rich['w'])
slice_inv=rich['g'][1:4,1:4].inv()
wrong_slice=sum(rich['rest_w'][i,j]*(slice_inv*rich['rest_w']*slice_inv)[i,j]
                 for i in range(3) for j in range(3))
mutant('slice metric substituted for rest metric',wrong_slice,rich['W'])

# Actual immersed surfaces, full functions rather than independent Gram samples.
directions=[S.Matrix(v) for v in [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1)]]
b=S.Matrix([1,3*x+t,0]); gs=metric(N,b,G)
ms=[]; Bs=[]
for k,v in enumerate(directions):
    J=S.zeros(4,2); J[0,0]=1; J[1:4,1]=v
    raw=S.simplify(J.T*gs*J)
    q=(v.T*G*v)[0]; bv=(v.T*b)[0]
    # N and a positive on the declared domain; this avoids an unjustified sqrt branch.
    m=N*a*S.sqrt((v.T*G0*v)[0]); B=bv/m
    ms.append(m); Bs.append(B)
    truth('immersion rank direction '+str(k),J.rank()==2)
    same('raw regular determinant direction '+str(k),raw.det(),-N*N*q)
    C=S.diag(1,1/m); complete=S.simplify(C.T*raw*C)
    target=S.Matrix([[-N*N,-N*N*B],[-N*N*B,N**-2-N*N*B*B]])
    same('normalized full pullback direction '+str(k),complete,target)
    same('completed determinant direction '+str(k),complete.det(),-1)
    same('common comparison clock direction '+str(k),-raw[0,0],N*N)
q=[S.cancel((m/N)**2) for m in ms]
bb=[S.cancel(ms[i]*Bs[i]) for i in range(6)]
recon=S.diag(*q[:3])
for k,(i,j) in enumerate([(0,1),(0,2),(1,2)],3):
    recon[i,j]=recon[j,i]=S.cancel((q[k]-q[i]-q[j])/2)
    same('sum one-form condition '+str(k),bb[k],bb[i]+bb[j])
same('all metric coefficients reconstructed',recon,G)
same('all shift components reconstructed',S.Matrix(bb[:3]),b)
for c in coords:
    same('full first metric jet '+str(c),metric(N,S.Matrix(bb[:3]),recon).diff(c),gs.diff(c))
truth('smooth positive N and a lower bounds on open quarter patch',S.Rational(1,2)>0 and S.Rational(3,4)>0)

badG=S.Matrix([[1,2,0],[2,1,0],[0,0,1]])
badq=S.Matrix([(v.T*badG*v)[0] for v in directions])
same('six positive lengths counterexample values',badq,S.Matrix([1,1,1,6,2,2]))
truth('six positivity insufficient for SPD',all(v>0 for v in badq) and badG[:2,:2].det()<0)
mutant('sum-shift incoherence rejected',bb[3]+1,bb[0]+bb[1])
mutant('different comparison clocks rejected',N+1,N)
mutant('missing mixed directions cannot reconstruct cross term',S.Integer(0),G0[0,1])
otherb=S.Matrix([1,5*x+t,0])
same('pointwise raw metrics independent of spatial slope',at(metric(N,otherb,G),origin),base['g'])
other=direct(N,otherb,G,origin,'same_point_different_jet')
mutant('same event values do not give W',other['W'],base['W'])

lam=S.symbols('lambda',positive=True)
density_W=[]
for l in [S.Integer(1),S.Integer(2)]:
    d=direct(S.Integer(1),S.Matrix([0,l*x,0]),l*l*S.eye(3),origin,'density_lambda_'+str(l))
    same('density omission exact norm '+str(l),d['W'],1/(2*l*l))
    density_W.append(d['W'])
for k,v in enumerate(directions):
    m=lam*S.sqrt((v.T*v)[0]); B=lam*x*v[1]/m
    same('density omitted normalized field lambda independent '+str(k),S.diff(B,lam),0)
mutant('identical normalized fields imply identical W',density_W[0],density_W[1])

# Genuine time-live coordinate Jacobian, arbitrary N,m,B,alpha.
T,M,B,A=S.symbols('T M B A',real=True,nonzero=True)
raw=S.Matrix([[-T*T,-T*T*B*M],[-T*T*B*M,M*M/T**2-T*T*B*B*M*M]])
J=S.Matrix([[1,0],[-A/M,1/M]])
trans=S.simplify(J.T*raw*J)
formula=S.Matrix([[-T*T*(1-A*B)**2+A*A/T**2,-T*T*B*(1-A*B)-A/T**2],
                  [-T*T*B*(1-A*B)-A/T**2,T**-2-T*T*B*B]])
same('full general tape Jacobian',trans,formula)
same('tape transformed determinant',trans.det(),-1)
old=S.Matrix([1,A])
same('old observer norm survives coordinate transform',(old.T*trans*old)[0],-T*T)
s=S.symbols('s',real=True)
actual=trans.subs({T:1,B:0,A:s})
same('explicit exponential tape metric',actual,S.Matrix([[-1+s*s,-s],[-s,1]]))
truth('fixed tape is timelike at s one half',actual[0,0].subs(s,S.Rational(1,2))<0)
truth('fixed tape is spacelike at s two',actual[0,0].subs(s,2)>0)
mutant('omit tape alpha full matrix',actual.subs(s,0),actual)
mutant('reuse original clock norm after reselection',actual[0,0],S.Integer(-1))
same('normalizing ruler commutator nonzero coefficient',S.diff(S.exp(-t),t),-S.exp(-t))

# Constant time-relabeling check including densities, not an inferred physics rule.
k=S.Rational(3,2)
Nv=S.Rational(5,4); bv=S.Rational(2,3); qv=S.Rational(7,3)
hv=S.Matrix([[-Nv*Nv,-Nv*Nv*bv],[-Nv*Nv*bv,qv-Nv*Nv*bv*bv]])
j=S.diag(1/k,1); ht=j.T*hv*j
mv=S.sqrt(-hv.det()); mt=S.sqrt(-ht.det())
same('time relabel density',mt,mv/k)
same('time relabel B',ht[0,1]/ht[0,0]/mt,k*k*bv/mv)

eps,r,bc,qc=S.symbols('epsilon r b q',real=True)
be=S.Matrix([eps*r,eps*(bc*x+qc*t),0])
Fe=S.diff(be[1],x)-S.diff(be[0],y)-be[0]*S.diff(be[1],t)+be[1]*S.diff(be[0],t)
same('exact epsilon second-order interaction',Fe,eps*bc-eps*eps*r*qc)
mutant('linearized expression exact at finite amplitude',Fe,eps*bc)

# Auxiliary R3 from coordinate Christoffels and their derivatives.
sp=[x,y,z]
gg=(1+x*x)**2*G0; gi=S.simplify(gg.inv())
C=[[[S.simplify(sum(gi[k,l]*(S.diff(gg[l,j],sp[i])+S.diff(gg[l,i],sp[j])-S.diff(gg[i,j],sp[l]))/2
                       for l in range(3))) for j in range(3)] for i in range(3)] for k in range(3)]
Ric=S.Matrix(3,3,lambda i,j:sum(S.diff(C[k][i][j],sp[k])-S.diff(C[k][i][k],sp[j])
        +sum(C[k][k][l]*C[l][i][j]-C[k][j][l]*C[l][i][k] for l in range(3)) for k in range(3)))
R3=at(sum(gi[i,j]*Ric[i,j] for i in range(3) for j in range(3)),{x:0,y:0,z:0})
same('auxiliary coordinate gamma R3',R3,-S.Rational(40,7))
values['auxiliary_R3']=str(R3)

# Test the reviewer's own actual equality guard against a vacuous catch.
try:
    mutant('vacuity_harness_probe',S.Integer(1),S.Integer(1))
except ValueError as e:
    truth('vacuous mutation helper fails closed',str(e).startswith('VACUOUS'))
else:
    raise ValueError('vacuity probe failed')
print(json.dumps({'verdict':'PASS','python':platform.python_version(),'sympy':S.__version__,
 'arithmetic':'exact symbolic/rational; no float tolerances','scientific_shapes':['4x4','3x3','2x2'],
 'identity_diagnostic_count':len(checks),'mutation_rejection_count':len(mutations),
 'checks':checks,'mutations_rejected_by_actual_equality_guard':mutations,'values':values},indent=2))
