"""NAP1 exact pointwise specialization; no response-class adoption.

Original metric Hessian convention reused from pinned LSR1 parent_exact.py.
This parent symbolic implementation is not independent of that historical method.
The separate source-first reviewer uses its own Fraction/Christoffel implementation.
"""
import hashlib
import json
import platform
import sys
from pathlib import Path
import sympy as s

x = s.Matrix(s.symbols('x y z', real=True))
c, p, q, d, e, h, a, b = s.symbols('c2 s11 s22 s12 s13 s23 a b', real=True)
S = s.Matrix([[p,d,e],[d,q,h],[e,h,-p-q]])
C = s.Matrix([[0,-x[2],x[1]],[x[2],0,-x[0]],[-x[1],x[0],0]])
D = C.T*S*C
r2 = x.dot(x)
eta = s.diag(-1,1,1,1)
coords = [s.Symbol('x0'),*x]
g = s.diag(-1-c*r2,1,1,1)
g[1:,1:] = s.eye(3)-c*x*x.T+D
origin = dict.fromkeys(coords,0)
checks = []
def zero(label, expr):
    vals = list(expr) if isinstance(expr,s.MatrixBase) else [expr]
    residuals = [s.factor(v) for v in vals]
    if any(v != 0 for v in residuals):
        raise AssertionError((label,[str(v) for v in residuals]))
    checks.append(label)

zero('metric_at_center',g.subs(origin)-eta)
for i in coords:
    zero('zero_first_derivative_'+str(i),g.diff(i).subs(origin))
g2 = {(i,j,k,l):s.diff(g[i,j],coords[k],coords[l]).subs(origin)
      for i in range(4) for j in range(4) for k in range(4) for l in range(4)}
R = {(i,j,k,l):(g2[i,l,j,k]+g2[j,k,i,l]-g2[i,k,j,l]-g2[j,l,i,k])/2
     for i in range(4) for j in range(4) for k in range(4) for l in range(4)}
Ric = s.Matrix(4,4,lambda j,l:sum(eta[i,i]*R[i,j,i,l] for i in range(4)))
scalar = s.trace(eta*Ric)
target_Ric = -3*c*eta
target_Ric[1:,1:] += 3*S
zero('original_metric_Ricci',Ric-target_Ric)
zero('original_metric_scalar',scalar+12*c)
E = a*Ric+b*scalar*eta
TF = E-s.trace(eta*E)*eta/4
target_TF = s.zeros(4)
target_TF[1:,1:] = 3*a*S
zero('conditional_response_TF',TF-target_TF)

u = s.Matrix([1,0,0,0])
unit = [s.eye(3)[:,i] for i in range(3)]
dirs = [unit[0],unit[1],(3*unit[0]+4*unit[1])/5,
        (3*unit[0]+4*unit[2])/5,(3*unit[1]+4*unit[2])/5]
balances = []
for i,n in enumerate(dirs):
    zero('unit_direction_'+str(i),n.dot(n)-1)
    n4 = s.Matrix([0,*n])
    uf,nf = eta*u,eta*n4
    H = 2*(uf*uf.T+nf*nf.T)
    zero('reciprocal_tangent_trace_'+str(i),s.trace(eta*H))
    balance = s.expand(s.trace(eta*E*eta*H))
    zero('full_factor_two_balance_'+str(i),balance-6*a*n.dot(S*n))
    balances.append(balance)
parameters = [p,q,d,e,h]
matrix = s.Matrix([v.subs(a,1)/6 for v in balances]).jacobian(parameters)
assert matrix.rank()==5
checks.append('five_direction_rank_5')
zero('scalar_response_blindness_control',s.Matrix(balances).subs(a,0))
zero('all_S_zero_center_TF',TF.subs(dict.fromkeys(parameters,0)))
trace_witness = E.subs({**dict.fromkeys(parameters,0),a:1,b:0,c:1})
assert trace_witness == -3*eta and trace_witness != s.zeros(4)
checks.append('DDR_allows_nonzero_trace_response')

v = s.Matrix(s.symbols('v1 v2 v3', real=True))
gamma2 = g[1:,1:]
m2_coefficient = s.expand(v.dot(gamma2*v)+c*r2*v.dot(v))
zero('density_second_jet_retains_S',m2_coefficient-
     (v.dot(v)+c*(r2*v.dot(v)-x.dot(v)**2)+v.dot(D*v)))
density_probes = [
    (unit[1],unit[2]),(unit[0],unit[2]),(unit[0],unit[1]),
    (unit[2],unit[0]+unit[1]),(unit[1],unit[0]+unit[2]),
    (unit[0],unit[1]+unit[2])]
density_values = [(n.cross(w)).dot(S*n.cross(w)) for n,w in density_probes]
zero('six_density_coefficients',s.Matrix(density_values)-s.Matrix(
    [p,q,-p-q,p+q-2*d,-q-2*e,-p-2*h]))
density_matrix = s.Matrix(density_values).jacobian(parameters)
assert density_matrix.rank()==5
checks.append('full_density_rank_5')
zero('radial_density_S_blindness',x.dot(D*x))

# General positive raw diagonal pair, normalized only after complete pullback.
f, G = s.symbols('f G',positive=True)
m = s.sqrt(f*G)
raw = s.diag(-f,G)
normalizer = s.diag(1,1/m)
completed = normalizer.T*raw*normalizer
zero('exact_completed_pair',completed-s.diag(-f,1/f))
zero('full_tuple_reconstruction',s.diag(1,m).T*completed*s.diag(1,m)-raw)
zero('normalized_determinant',completed.det()+1)

# Passive frame change: actual full metric and germ transformed together.
A = s.eye(4);A[:2,:2]=s.Matrix([[s.Rational(5,3),s.Rational(4,3)],
                              [s.Rational(4,3),s.Rational(5,3)]])
J = s.Matrix([[1,0],[0,1],[0,2],[0,-1]])
zero('full_pair_covariance', (A.inv()*J).T*(A.T*g*A)*(A.inv()*J)-J.T*g*J)

# These hostile alternatives are compared to original computed outputs.
offdiag = {p:0,q:0,d:1,e:0,h:0,a:1}
hostile = {
    'axis_only_misses_mixed_S': all(v.subs(offdiag)==0 for v in balances[:2])
                              and balances[2].subs(offdiag)!=0,
    'half_tangent_wrong_normalization': balances[2].subs(offdiag)!=
                                       3*dirs[2].dot(S*dirs[2]).subs(offdiag),
    'drop_density_loses_real_angular_information': density_values[3].subs(offdiag)!=0,
    'forcing_E_zero_rejects_valid_pointwise_DDR_trace':trace_witness!=s.zeros(4),
    'a_zero_cannot_reject_nonzero_S':all(v.subs({**offdiag,a:0})==0 for v in balances),
}
assert all(hostile.values()),hostile
print(json.dumps({'status':'PASS','python':platform.python_version(),'sympy':s.__version__,
 'argv':sys.argv,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'check_count':len(checks),'checks':checks,'hostile_recomputations':hostile,
 'response_balances':[str(v) for v in balances],
 'balance_matrix':[[str(v) for v in matrix.row(i)] for i in range(matrix.rows)],
 'balance_rank':matrix.rank(),'balance_determinant':str(matrix.det()),
 'density_probes':[[list(map(str,n)),list(map(str,w))] for n,w in density_probes],
 'density_coefficients':list(map(str,density_values)),'density_rank':density_matrix.rank(),
 'scalar':str(scalar),'trace_witness':str(trace_witness),
 'scope':'Exact center-jet and supplied-pair algebra; G301 membership explicitly conditional; no native physical admission, new response or neighborhood solution claim.'},indent=2))
