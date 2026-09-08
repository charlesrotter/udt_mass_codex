"""BG2 source-first exact anchors; no author code or result import."""
import itertools
import json
import platform
import sympy as s

I = s.eye(3)
checks = []
def equal(name, left, right):
    diff = left-right
    values = list(diff) if isinstance(diff, s.MatrixBase) else [diff]
    assert all(s.simplify(x) == 0 for x in values), (name, diff)
    checks.append(name)

u,v,w,b,c,d = s.symbols('u v w b c d', real=True)
K=s.Matrix([[u,b,c],[b,v,d],[c,d,w]])
q0=K-s.trace(K)*I/3
x=s.Matrix(s.symbols('x1:4', real=True))
r=(x.T*x)[0]
def ell(z, vec):
    return z*vec.T+vec*z.T-s.Rational(2,3)*(z.dot(vec))*I
def project(z, Q):
    rr=z.dot(z)
    inv=(I-z*z.T/(4*rr))/rr
    return Q-ell(z, inv*Q*z)
Q=project(x,q0).applyfunc(s.factor)
equal('TT_symbol_trace',s.trace(Q),0)
equal('TT_symbol_transverse',Q*x,s.zeros(3,1))
equal('TT_symbol_idempotent',project(x,Q),Q)
equal('TT_symbol_annihilates_longitudinal',project(x,ell(x,s.Matrix([1,2,3]))),s.zeros(3))
principal=lambda z,A: z*(A*z).T+(A*z)*z.T-z.dot(z)*A-s.trace(A)*z*z.T
equal('full_Ricci_symbol_on_TT',principal(x,Q),-r*Q)
polar=s.Matrix([[0,0,1],[0,0,0],[1,0,0]])
freq=s.Matrix([0,1,0])
equal('polarization_TT',project(freq,polar),polar)
equal('drift_principal_nonzero',principal(freq,project(freq,polar))[:,2],s.Matrix([-1,0,0]))

# Direct differential of invariant-frame Koszul connection/curvature.
# FREE mathematical p,q; specialization is p=2/c_radius, q=2*c_radius/a_radius².
p,q=s.symbols('p q',positive=True)
C=s.MutableDenseNDimArray.zeros(3,3,3)
for i,j,k,val in [(0,1,2,q),(1,2,0,p),(2,0,1,p)]:
    C[i,j,k]=val; C[j,i,k]=-val
G=s.MutableDenseNDimArray.zeros(3,3,3)
DG=s.MutableDenseNDimArray.zeros(3,3,3)
for i,j,k in itertools.product(range(3),repeat=3):
    G[i,j,k]=(C[i,j,k]-C[j,k,i]+C[k,i,j])/2
for i,j,k in itertools.product(range(3),repeat=3):
    DG[i,j,k]=sum(2*K[k,l]*G[i,j,l] -
        (sum(C[i,j,m]*K[m,l]-C[j,l,m]*K[m,i]+C[l,i,m]*K[m,j]
             for m in range(3)) if l==k else 0)
        for l in range(3))
def curvature(g,dg=None):
    out=s.zeros(3)
    for j,k in itertools.product(range(3),repeat=2):
        for i,m in itertools.product(range(3),repeat=2):
            if dg is None:
                out[j,k]+=g[j,k,m]*g[i,m,i]-g[i,k,m]*g[j,m,i]-C[i,j,m]*g[m,k,i]
            else:
                out[j,k]+=(dg[j,k,m]*g[i,m,i]+g[j,k,m]*dg[i,m,i]
                           -dg[i,k,m]*g[j,m,i]-g[i,k,m]*dg[j,m,i]-C[i,j,m]*dg[m,k,i])
    return out.applyfunc(s.expand)
ric=curvature(G)
Sdirect=curvature(G,DG)
equal('Berger_Ricci_direct',ric,s.diag(p*q-q*q/2,p*q-q*q/2,q*q/2))
DK=s.MutableDenseNDimArray.zeros(3,3,3)
DDK=s.MutableDenseNDimArray.zeros(3,3,3,3)
for a,i,j in itertools.product(range(3),repeat=3):
    DK[a,i,j]=-sum(G[a,i,m]*K[m,j]+G[a,j,m]*K[i,m] for m in range(3))
for a,b0,i,j in itertools.product(range(3),repeat=4):
    DDK[a,b0,i,j]=-sum(G[a,b0,m]*DK[m,i,j]+G[a,i,m]*DK[b0,m,j]+
                          G[a,j,m]*DK[b0,i,m] for m in range(3))
Scov=s.Matrix(3,3,lambda i,j:sum(-DDK[k,i,k,j]-DDK[k,j,k,i]+DDK[k,k,i,j] for k in range(3)))
equal('FULL_tensor_Koszul_vs_uncommuted',Sdirect,Scov)
equal('nonzero_mixed_lower_order_anchor',Sdirect[0,2],-(2*p*q+q*q)*c)
equal('nonzero_second_mixed_lower_order_anchor',Sdirect[1,2],-(2*p*q+q*q)*d)
equal('constant_pure_trace_S_zero',Sdirect.subs({u:1,v:1,w:1,b:0,c:0,d:0}),s.zeros(3))
M=s.Matrix([sum(DK[j,j,i] for j in range(3)) for i in range(3)])
equal('full_homogeneous_momentum',M,s.Matrix([(q-p)*d,(p-q)*c,0]))
gap=q*(q-p)
e3=s.Matrix([0,0,1]); Ph=s.diag(1,1,0); Pv=s.diag(0,0,1)
Bdot=Sdirect+2*K*ric
Y=Ph*Bdot*e3/gap
kv=Ph*K*e3
Pdot=Y*e3.T+e3*(Y-2*kv).T
equal('projector_commutation_derivative',Bdot*Pv+ric*Pdot-Pdot*ric-Pv*Bdot,s.zeros(3))
equal('projector_idempotency_derivative',Pdot*Pv+Pv*Pdot,Pdot)
equal('projector_moving_selfadjoint_derivative',Pdot-Pdot.T,2*(K*Pv-Pv*K))
equal('raised_Ricci_mixed_anchor',Bdot[0,2],-2*p*q*c)

# Deliberately changed implementations must fail an actual matching anchor.
mutations={}
def must_fail(name,test):
    try:
        test()
    except AssertionError:
        mutations[name]='CAUGHT'
    else:
        raise AssertionError(('mutation survived',name))
must_fail('Ricci_variation_sign',lambda:equal('mutant_sign',-Scov,Sdirect))
badDD=s.MutableDenseNDimArray(DDK)
for a,b0,i,j in itertools.product(range(3),repeat=4):
    badDD[a,b0,i,j]+=sum(G[a,b0,m]*DK[m,i,j] for m in range(3))
badS=s.Matrix(3,3,lambda i,j:sum(-badDD[k,i,k,j]-badDD[k,j,k,i]+badDD[k,k,i,j] for k in range(3)))
must_fail('dropped_derivative_index_connection',lambda:equal('mutant_derivative_index',badS,Sdirect))
must_fail('dropped_inverse_metric_term',lambda:equal('mutant_inverse_metric',Sdirect[0,2],-2*p*q*c))
must_fail('TT_projection_wrong_sign',lambda:equal('mutant_projection',(q0+ell(x,(I-x*x.T/(4*r))*q0*x/r))*x,s.zeros(3,1)))
must_fail('missing_projector_metric_dual_term',lambda:equal('mutant_dual',Y*e3.T+e3*Y.T-(Y*e3.T+e3*Y.T).T,2*(K*Pv-Pv*K)))
print(json.dumps({'python':platform.python_version(),'sympy':s.__version__,
  'exact_checks':len(checks),'checks':checks,'mutations':mutations,
  'principal_polarization':str(polar),'principal_frequency':str(freq),
  'principal_drift_numerator':str(principal(freq,polar)[:,2]),
  'full_direct_S':str(Sdirect),'full_raised_Bdot':str(Bdot.applyfunc(s.expand)),
  'scope':'exact algebra anchors, not global elliptic/IFT certification'},indent=2))
