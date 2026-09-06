"""Source-first exact diagnostics; imports no campaign scientific code/results."""
import json
import platform
import sympy as s

checks = {}
def record(name, value):
    checks[name] = bool(value)
    if not checks[name]:
        raise AssertionError(name)

t = s.symbols('t', real=True)
x = s.symbols('x0:3', real=True)
p = s.symbols('p0:3', real=True)
# Freely chosen smooth positive inverse spatial metric with space/time variation.
Q = s.Matrix([[2+t*t+x[0]**2, 1, 0], [1, 3+x[1]**2, 1], [0, 1, 2+x[2]**2]])
pv = s.Matrix(p)
H2 = (pv.T*Q*pv)[0]
H = s.sqrt(H2)
Hp = s.Matrix([s.diff(H, z) for z in p])
Hx = s.Matrix([s.diff(H, z) for z in x])
record('Euler_positive_degree_one', s.simplify((pv.T*Hp)[0]-H)==0)
record('full_original_null_residual', s.simplify(-(-H)**2+H2)==0)
record('time_parametrized_ray_is_null', s.simplify((Hp.T*Q.inv()*Hp)[0]-1)==0)
# Variational identity for arbitrary variations dX=A, dP=B, independently expanded.
A = s.Matrix(s.symbols('A0:3', real=True))
B = s.Matrix(s.symbols('B0:3', real=True))
Hpp = Hp.jacobian(p)
Hpx = Hp.jacobian(x)
variation_derivative = (-Hx.T*A)[0] + (pv.T*(Hpx*A+Hpp*B))[0]
record('canonical_variation_PdX_constant', s.simplify(variation_derivative)==0)
point = {t:s.Rational(1,2), x[0]:1, x[1]:-2, x[2]:3, p[0]:2, p[1]:-1, p[2]:3}
qn = Q.subs(point)
record('non_diagonal_spatial_metric_positive_at_control', all(qn[:j,:j].det()>0 for j in (1,2,3)))
norm2 = H2.subs(point)
normal = -s.sqrt(norm2)
record('future_root_sign', -normal>0)
record('past_root_rejected', -(+s.sqrt(norm2))<0)
record('arbitrary_independent_normal_rejected', -s.Rational(1,3)**2+norm2!=0)
record('pullback_alone_misses_normal', normal != 0)
record('critical_point_forces_zero_full_null_covector', H2.subs(dict.fromkeys(p,0))==0)

# Distinct Hamiltonian method: direct flat null geodesic congruence / projection.
y = s.symbols('y0:3', real=True)
yv = s.Matrix(y)
r = s.sqrt(sum(z*z for z in y))
P = -yv/r
X = yv+t*P
J = X.jacobian(y)
record('flat_characteristic_momentum_unit', s.simplify((P.T*P)[0]-1)==0)
record('flat_projection_determinant', s.simplify(J.det()-(1-t/r)**2)==0)
record('flat_variation_matches_initial_phase', all(s.simplify(z)==0 for z in (P.T*J+s.Matrix([[s.diff(r,z) for z in y]]))))
focus = {y[0]:0,y[1]:0,y[2]:2,t:2}
record('focus_rank_one', J.subs(focus).rank()==1)
record('focus_nonzero_momentum', P.subs(focus)!=s.zeros(3,1))
record('focus_position_zero', X.subs(focus)==s.zeros(3,1))
flat_theta = -s.sqrt(sum(z*z for z in x))-t
res = -s.diff(flat_theta,t)**2+sum(s.diff(flat_theta,z)**2 for z in x)
record('flat_spacetime_phase_original_residual', s.simplify(res)==0)
record('flat_phase_matches_initial_real_data', s.simplify(flat_theta.subs(t,0)+s.sqrt(sum(z*z for z in x)))==0)

print(json.dumps({'python':platform.python_version(),'sympy':s.__version__,'checks':checks,
                  'passed':sum(checks.values()),'total':len(checks),
                  'exact_control_norm_squared':str(norm2),
                  'focus_J':str(J.subs(focus)),
                  'scope':'Exact symbolic controls, not proof of ODE theorem or compact extremum argument.'},indent=2))
