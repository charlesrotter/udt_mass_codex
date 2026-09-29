"""Independent source-first exact checks. No author/reviewer code imports."""
import json
import platform
from pathlib import Path
import sympy as s

checks = []
observations = {}

def equal(name, lhs, rhs=0):
    residual = lhs-rhs
    vals = list(residual) if isinstance(residual, s.MatrixBase) else [residual]
    vals = [s.factor(v) for v in vals]
    assert all(v == 0 for v in vals), (name, vals)
    checks.append(name)

def nonzero(name, expr):
    assert s.simplify(expr) != 0, (name, expr)
    checks.append(name)

eta = s.diag(-1,1,1,1)
basis = [s.eye(4)[:,i] for i in range(4)]
indices = [(i,j) for i in range(4) for j in range(i,4)]

def symvec(M):
    return s.Matrix([M[i,j] for i,j in indices])

def H(u,n):
    uf,nf=eta*u,eta*n
    equal('pair_unit', (u.T*eta*u)[0], -1)
    equal('pair_spatial_unit', (n.T*eta*n)[0], 1)
    equal('pair_orthogonal', (u.T*eta*n)[0], 0)
    return 2*(uf*uf.T+nf*nf.T)

pairs=[H(basis[0],basis[i]) for i in range(1,4)]
for i,j in [(1,2),(1,3),(2,3)]:
    pairs.append(H(basis[0], s.Rational(5,13)*basis[i]+s.Rational(12,13)*basis[j]))
C,S=s.Rational(13,5),s.Rational(12,5)
for i in range(1,4):
    hb=H(C*basis[0]+S*basis[i], S*basis[0]+C*basis[i])
    pairs.append(hb)
    uf,nf=eta*basis[0],eta*basis[i]
    equal('boosted_covector_sign',hb/2-(C*C+S*S)*pairs[i-1]/2,
          2*C*S*(uf*nf.T+nf*uf.T))
shape_columns=s.Matrix.hstack(*map(symvec,pairs))
equal('shape_rank',shape_columns.rank(),9)
for h in pairs: equal('shape_trace',s.trace(eta*h))
pairing=s.Matrix([[h[i,j]*eta[i,i]*eta[j,j]*(1 if i==j else 2)
                   for i,j in indices] for h in pairs])
equal('balance_rank',pairing.rank(),9)
equal('metric_annihilator',pairing*symvec(eta),s.zeros(9,1))
equal('one_pair_rank',pairing[:1,:].rank(),1)
observations['pair_rank']=9
observations['annihilator_basis']=[str(v) for v in pairing.nullspace()[0]]

xs=s.symbols('x0:10')
X=s.zeros(4)
for v,(i,j) in zip(xs,indices): X[i,j]=X[j,i]=v
a,b,q=s.symbols('a b q')
rx=s.trace(eta*X)
TF=lambda M,g=eta: M-s.trace(g.inv()*M)*g/4
E=a*X+b*rx*eta
equal('class_trace_projection',TF(E),a*TF(X))
equal('arbitrary_trace_invisible',TF(E+q*eta),TF(E))
equal('pure_trace_vacuity',TF(b*rx*eta),s.zeros(4))
for aa,bb,rank in [(2,3,10),(4,-1,9),(0,1,1),(0,0,0)]:
    op=symvec(E.subs({a:aa,b:bb})).jacobian(xs)
    equal('coefficient_stratum',op.rank(),rank)
equal('inverse_generic_class',(E-b*s.trace(eta*E)*eta/(a+4*b))/a,X)

t,x,y,z=s.symbols('t x y z', real=True)
coords=(t,x,y,z)

def geometry(g):
    inv=g.inv()
    Gamma=[[[s.factor(sum(inv[i,l]*(s.diff(g[l,k],coords[j])+
        s.diff(g[l,j],coords[k])-s.diff(g[j,k],coords[l])) for l in range(4))/2)
        for k in range(4)] for j in range(4)] for i in range(4)]
    Ric=s.Matrix(4,4,lambda j,k:s.factor(sum(
        s.diff(Gamma[i][j][k],coords[i])-s.diff(Gamma[i][j][i],coords[k])+
        sum(Gamma[i][i][l]*Gamma[l][j][k]-Gamma[i][k][l]*Gamma[l][j][i]
            for l in range(4)) for i in range(4))))
    R=s.factor(s.trace(inv*Ric))
    def div(B):
        return s.Matrix([s.factor(sum(inv[i,l]*(s.diff(B[i,j],coords[l])-
            sum(Gamma[k][l][i]*B[k,j]+Gamma[k][l][j]*B[i,k] for k in range(4)))
            for i in range(4) for l in range(4))) for j in range(4)])
    def hessian(f):
        return s.Matrix(4,4,lambda i,j:s.factor(s.diff(f,coords[i],coords[j])-
            sum(Gamma[k][i][j]*s.diff(f,coords[k]) for k in range(4))))
    return inv,Ric,R,div,hessian

# Freely chosen different static lapse, regular near x=y=1.
N=2+x*x+y**4
g=s.diag(-N*N,1,1,1)
inv,Ric,R,div,hessian=geometry(g)
dR=s.Matrix([s.diff(R,c) for c in coords])
equal('bianchi_from_metric',div(Ric),dR/2)
equal('Einstein_identity_from_metric',div(Ric-R*g/2),s.zeros(4,1))
equal('shape_divergence_from_metric',div(TF(Ric,g)),dR/4)
equal('class_divergence_from_metric',div(a*Ric+b*R*g),(a/2+b)*dR)
nonzero('Ricci_not_offshell_conserved',div(Ric)[1].subs({x:1,y:1}))
shape=TF(R*Ric,g)
j=div(shape)
equal('nonlinear_shape_divergence',j,Ric*inv*dR)
curl=s.factor(s.diff(j[2],x)-s.diff(j[1],y))
curl_point=s.factor(curl.subs({x:1,y:1}))
nonzero('trace_completion_obstruction',curl_point)
observations['different_lapse_metric']='diag(-(2+x^2+y^4)^2,1,1,1)'
observations['different_lapse_R']=str(R)
observations['different_lapse_curl_xy_at_1_1']=str(curl_point)
observations['different_lapse_div_Ric_x_at_1_1']=str(div(Ric)[1].subs({x:1,y:1}))
equal('conditional_conserved_completion',div(a*TF(Ric,g)-a*R*g/4+q*g),s.zeros(4,1))

# Two diagnostic action-response geometries; the second activates derivative terms.
for exponent in [1,6]:
    gm=s.diag(-1,t**exponent,t**exponent,t**exponent)
    im,rm,scalar,dm,hm=geometry(gm)
    Hess=hm(scalar)
    box=s.factor(s.trace(im*Hess))
    Er2=(2*scalar*rm-scalar**2*gm/2+2*(gm*box-Hess)).applyfunc(s.factor)
    equal('R_squared_trace',s.trace(im*Er2),6*box)
    equal('R_squared_divergence',dm(Er2),s.zeros(4,1))
    if exponent==1:
        equal('scalar_flat_R',scalar)
        equal('scalar_flat_R_squared',Er2,s.zeros(4))
        nonzero('scalar_flat_Ricci_shape',TF(rm,gm)[0,0])
        observations['scalar_flat_Ricci']=[str(rm[i,i]) for i in range(4)]
    else:
        nonzero('derivative_term_active',box)
        nonzero('wrong_algebraic_response_rejected',dm(2*scalar*rm-scalar**2*gm/2)[0])
        observations['nonconstant_R_control']={'R':str(scalar),'boxR':str(box),
            'E_R2_diagonal':[str(Er2[i,i]) for i in range(4)]}

# Flat linearization: h_xx=t^6 gives delta R=d_t^2 h_xx, not zero.
deltaR=s.diff(t**6,t,2)
Hess0=s.Matrix(4,4,lambda i,j:s.diff(deltaR,coords[i],coords[j]))
Elin=2*(eta*s.trace(eta*Hess0)-Hess0)
equal('R_squared_linear_TT',Elin[0,0])
equal('R_squared_linear_spatial',Elin[1,1],-720*t*t)
nonzero('full_R_squared_flat_linearization_not_zero',Elin[1,1])
observations['flat_R_squared_linear_diagonal']=[str(Elin[i,i]) for i in range(4)]

# Same-action density conversion on a non-normalized metric and nonzero tangent.
gm=s.diag(-4,9,16,25)
em=s.Matrix([[2,1,0,0],[1,3,2,0],[0,2,5,1],[0,0,1,7]])
hm=s.Matrix([[3,2,1,0],[2,4,0,1],[1,0,6,2],[0,1,2,8]])
v=-gm.inv()*hm*gm.inv()
inverse_pair=s.trace(em*v)
covariant_pair=-s.trace(gm.inv()*em*gm.inv()*hm)
equal('same_action_variation_sign',inverse_pair,covariant_pair)
nonzero('wrong_plus_density_sign_rejected',inverse_pair+covariant_pair)
observations['inverse_variation_pairing']=str(inverse_pair)

# Optional unadopted scalar-field comparison: tensor conservation uses its EOM.
psi=t*t+x**3/3
grad=s.Matrix([s.diff(psi,c) for c in coords])
V=psi**3/3
T=grad*grad.T-eta*((grad.T*eta*grad)[0]/2+V)
matter_div=s.Matrix([sum(eta[i,i]*s.diff(T[i,j],coords[i]) for i in range(4))
                     for j in range(4)])
boxpsi=sum(eta[i,i]*s.diff(psi,coords[i],coords[i]) for i in range(4))
equal('scalar_matter_Noether_identity',matter_div,(boxpsi-psi**2)*grad)
nonzero('matter_not_offshell_conserved',matter_div[0].subs({t:1,x:1}))
observations['matter_div_t_at_1_1']=str(matter_div[0].subs({t:1,x:1}))

report={'scope':'Independent exact source-first controls, not a native response proof',
        'python':platform.python_version(),'sympy':s.__version__,
        'checks':checks,'check_count':len(checks),'observations':observations}
out=Path(__file__).with_name('INDEPENDENT_SOURCE_RESULTS.json')
with out.open('x') as stream: json.dump(report,stream,indent=2); stream.write('\n')
print(json.dumps(report,sort_keys=True,indent=2))
