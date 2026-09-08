"""Same-author finite symbolic anchors for SM2, not a universal proof."""
import json
import platform
import sympy as S

checks = {}
def check(name, condition):
    checks[name] = bool(condition)
    assert checks[name], name

t,u,v,w,z = S.symbols('t u v w z', real=True)
g = S.Matrix([[0,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
q = S.Matrix([0,-1,0,0])
# Columns are the new null-frame basis in the old basis.
L = S.Matrix([[1,t**2/2,t,0],[0,1,0,0],[0,t,1,0],[0,0,0,1]])
P = S.Matrix([[u,v,0,0],[v,w,0,0],[0,0,z,0],[0,0,0,z]])
check('null_rotation_metric', S.simplify(L.T*g*L-g) == S.zeros(4))
check('null_rotation_covector', L.T*q == q)
res = S.expand(L.T*P*L-P)
check('first_stabilizer_constraint', res[0,2] == t*u)
check('second_stabilizer_constraint', S.expand(res[2,1].subs(u,0)) == t*(v+z))
normal = P.subs({u:0,v:-z})
check('remaining_matrix_form', normal == z*g+w*q*q.T)
check('full_stabilizer_sufficiency', S.simplify(L.T*normal*L-normal) == S.zeros(4))
n,theta = S.symbols('n theta', positive=True)
A,B = S.Function('A'),S.Function('B')
check('chain_transport_coefficient', S.expand(S.diff(B(n),n)*(-n*theta)+B(n)*theta) == theta*(B(n)-n*S.diff(B(n),n)))
C = S.symbols('C',real=True)
check('linear_density_sufficient', S.simplify(C*n-n*S.diff(C*n,n)) == 0)
check('ratio_ode_equivalence', S.simplify(S.diff(B(n)/n,n)+(B(n)-n*S.diff(B(n),n))/n**2) == 0)
check('mutation_quadratic_expansion_rejected', S.simplify(n**2-n*S.diff(n**2,n)) == -n**2)
check('quadratic_false_pass_on_zero_expansion', (-n**2*theta).subs(theta,0) == 0)
r,x,phi = S.symbols('r x phi', positive=True)
check('variable_metric_coefficient_rejected', S.diff(A(1+x),x) != 0)
W = S.Function('W')(phi,x)
check('extra_transported_scalar_not_constant', S.diff(W,r) == 0 and S.diff(W,x) != 0)
check('mutation_untransported_weight_rejected', S.diff(r*W,r) == W and W != 0)
print(json.dumps({'kind':'same-author exact anchors and mutations; not independent proof',
    'python':platform.python_version(),'sympy':S.__version__,'checks':checks,
    'passed':len(checks)},indent=2,sort_keys=True))
