"""Author rederivation after exposure to reviewer SF3; independent ADM variation."""
import json
import platform
import sympy as S

x,e,k = S.symbols('x e k', real=True)
q=e*S.cos(k*x)
K=S.diag(S.Rational(1,3)-3*q*q/4,-S.Rational(2,3)-q,-S.Rational(2,3)+q)
tau=S.trace(K)
checks={}

def check(name,a):
    a=a.applyfunc(S.simplify) if isinstance(a,S.MatrixBase) else S.simplify(a)
    good=a==S.zeros(*a.shape) if isinstance(a,S.MatrixBase) else a==0
    checks[name]=bool(good)
    assert good,(name,a)

check('Hamiltonian_globally',tau*tau-S.trace(K*K))
check('momentum_x_globally',S.diff(K[0,0]-tau,x))
check('momentum_yz_globally',S.Matrix([S.diff(K[0,1],x),S.diff(K[0,2],x)]))
E=tau*K-K*K
check('E_trace',S.trace(E))
check('KE_STF',K*E-S.eye(3)*S.trace(K*E)/3)
# Full linearized spatial Ricci at the flat initial metric, delta gamma=-2K.
dh=-2*K
def D(i,v):
    return S.diff(v,x) if i==0 else S.S.Zero
dRic=S.Matrix(3,3,lambda i,j:(sum(D(l,D(i,dh[l,j]))+D(l,D(j,dh[l,i]))
    -D(l,D(l,dh[i,j])) for l in range(3))-D(i,D(j,S.trace(dh))))/2)
check('spatial_Ricci_variation',dRic-S.diag(0,-S.diff(q,x,2),S.diff(q,x,2)))
dK=tau*K
dtau=S.trace(dK)
dE=dRic+dtau*K+tau*dK-dK*K-K*dK
check('direct_ADM_E_variation',dE-2*tau*E-dRic)
B=S.Matrix([[0,0,0],[0,0,S.diff(q,x)],[0,S.diff(q,x),0]])
# At x=0 B=0 and every first derivative of gamma,K,E vanishes: Bdot=-curl E=0.
check('B_at_origin',B.subs(x,0))
check('E_first_derivatives_at_origin',S.diff(E,x).subs(x,0))
E0=S.simplify(E.subs(x,0)); W0=S.simplify(dE.subs(x,0))
I2,I3=S.factor(S.trace(E0**2)),S.factor(S.trace(E0**3))
A=S.factor(1-6*I3**2/I2**3)
rate=S.factor(36*I3*(I3*S.trace(E0*W0)-I2*S.trace(E0**2*W0))/I2**4)
target=2592*k*k*e*e*(e-2)*(e+2)/(3*e*e+4)**4
check('nA_formula',rate-target)
probe=S.Rational(1,6)
assert I2.subs(e,probe)!=0
assert rate.subs({e:probe,k:1}) == -S.Rational(5930496,5764801)
checks['original_denominator_nonzero_and_rate_exact']=True
check('matched_full_Q_K_at_origin',S.diff(E0,k))
check('matched_K_at_origin',S.diff(K.subs(x,0),k))
check('homogeneous_rate',rate.subs(k,0))
assert rate.subs({e:probe,k:1})!=rate.subs({e:probe,k:0})
checks['same_point_Q_K_different_rate']=True
# Do not use a cancelled formula to claim original diagnostic exists at e=2/3.
check('excluded_flat_point_original_I2',I2.subs(e,S.Rational(2,3)))
assert target.subs({e:S.Rational(2,3),k:1})!=0
checks['cancelled_denominator_false_pass_detected']=True
print(json.dumps({'python':platform.python_version(),'sympy':S.__version__,
    'exposure':'Reviewer SF3 known; no reviewer code imported or read before writing this check.',
    'method':'flat spatial Ricci first variation and admitted ADM; not 4D reviewer engine',
    'checks':checks,'all_passed':all(checks.values()),'I2':str(I2),'I3':str(I3),
    'A':str(A),'nA':str(rate),'original_domain':'I2 != 0; e=+/-2/3 excluded',
    'periodicity':'k=0 or 1 for the matched comparison on x period 2pi',
    'limits':'Exact initial rate only; actual existence uses written analytic/local interface.'},indent=2))
