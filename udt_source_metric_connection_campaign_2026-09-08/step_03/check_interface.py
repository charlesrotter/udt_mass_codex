"""Exact same-author sign/projection controls; no coupled metric solve."""
import json
import platform
import sympy as S

checks = {}
values = {}
def check(name, condition, value=None):
    checks[name] = bool(condition)
    assert checks[name], name
    if value is not None:
        values[name] = str(value)
def zero(obj):
    return all(S.simplify(x)==0 for x in obj)
def geometry(metric, coords):
    m=len(coords)
    inv=metric.inv()
    connection=[[[S.simplify(sum(inv[k,l]*(S.diff(metric[l,j],coords[i])+
        S.diff(metric[l,i],coords[j])-S.diff(metric[i,j],coords[l]))/2
        for l in range(m))) for j in range(m)] for i in range(m)] for k in range(m)]
    ric=S.Matrix(m,m,lambda i,j:S.simplify(sum(
        S.diff(connection[k][i][j],coords[k])-S.diff(connection[k][i][k],coords[j])+
        sum(connection[k][k][l]*connection[l][i][j]-connection[k][j][l]*connection[l][i][k]
        for l in range(m)) for k in range(m))))
    scalar=S.simplify(sum(inv[i,j]*ric[i,j] for i in range(m) for j in range(m)))
    return connection,ric,scalar

t,x,y,z=S.symbols('t x y z',real=True)
a=1+t*x  # Restrict a>0. General diagnostic geometry, not a solution claim.
g=S.diag(-1,1,a*a,a*a)
connection,Ric,R=geometry(g,[t,x,y,z])
Einstein=S.simplify(Ric-R*g/2)
gamma=g[1:,1:]
conn3,Ric3,R3=geometry(gamma,[x,y,z])
K=-gamma.diff(t)/2
Km=gamma.inv()*K
trK=S.trace(Km)
H=S.simplify(R3+trK**2-S.trace(Km*Km))
T=Km-trK*S.eye(3)
coords3=[x,y,z]
M=S.Matrix([S.simplify(sum(S.diff(T[j,i],coords3[j])+
    sum(conn3[j][j][k]*T[k,i]-conn3[k][j][i]*T[j,k] for k in range(3))
    for j in range(3))) for i in range(3)])
check('hamiltonian_full_geometry',S.simplify(H-2*Einstein[0,0])==0,H)
check('momentum_full_geometry',zero(M+Einstein[0,1:].T),M)
check('nonzero_momentum_anchor',S.simplify(M[0]-2/a)==0 and M[0]!=0,M[0])
check('wrong_codazzi_sign_rejected',S.simplify(M[0]-Einstein[0,1])==4/a)

n,E,beta,Lam=S.symbols('n E beta Lam',positive=True)
eta=S.diag(-1,1,1,1)
v=S.Matrix([S.Rational(3,5),S.Rational(4,5),0])
q=S.Matrix([-E,E*v[0],E*v[1],0]); ell=eta*q
k=S.Matrix([1/(2*E),-v[0]/(2*E),-v[1]/(2*E),0])
Q=n*q*q.T
Ricmodel=Lam*eta+beta*Q
check('null_frame_normalization',(q.T*eta*q)[0]==0 and (ell.T*eta*k)[0]==-1)
check('trace_relation',S.simplify(S.trace(eta*Ricmodel)-4*Lam)==0)
check('same_null_blindness',S.simplify((ell.T*Ricmodel*ell)[0])==0)
check('complementary_null_signal',S.simplify((k.T*Ricmodel*k)[0]-beta*n)==0)
check('mixed_null_scalar',S.simplify((ell.T*Ricmodel*k)[0]+Lam)==0)
check('hamiltonian_density_factor',Q[0,0]==n*E**2)
check('momentum_density_factor',zero(-Q[0,1:].T-n*E**2*v))
check('time_symmetric_nonzero_source_rejected',S.simplify((beta*n*E**2*v).dot(beta*n*E**2*v))==beta**2*n**2*E**4)
check('readout_tensor_weight_distinct',S.simplify(n*E**2-n*E)!=0)
check('eikonal_spatial_data',S.simplify(sum(q[i]**2 for i in range(1,4))-E**2)==0)
check('tracefree_bianchi_coefficient',S.Rational(1,2)-S.Rational(1,4)==S.Rational(1,4))
A0,alpha,Lc,C=S.symbols('A0 alpha Lc C',real=True)
check('constant_metric_term_absorption',S.expand((Lc-alpha*A0)*eta+alpha*(A0*eta+C*Q)-(Lc*eta+alpha*C*Q))==S.zeros(4))
check('vacuum_not_nonzero_coupling',beta*Q!=S.zeros(4))
print(json.dumps({'kind':'same-author exact identities/finite controls, not coupled existence',
    'python':platform.python_version(),'sympy':S.__version__,'checks':checks,
    'values':values,'passed':len(checks)},indent=2,sort_keys=True))
