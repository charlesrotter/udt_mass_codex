"""Symbolic/exact controls for the local phase argument, not ODE certification."""
import argparse
import json
import sympy as s

ap = argparse.ArgumentParser()
ap.add_argument('--mutant', choices=('past_root', 'omit_spatial_force',
                                    'wrong_characteristic_sign', 'allow_zero'))
mode = ap.parse_args().mutant
guards = []


def check(name, condition):
    if not condition:
        print(json.dumps({'status': 'FAIL', 'guard': name, 'mutant': mode,
                          'passed_before_failure': guards}, sort_keys=True))
        raise SystemExit(1)
    guards.append(name)


def zero(x):
    return s.simplify(x) == 0


# Formal generic positive-definite inverse spatial metric A. Sympy checks
# identities on Q>0; positivity/nonzero-domain hypotheses are analytic inputs.
p = s.Matrix(s.symbols('p1 p2 p3', real=True))
a11, a22, a33, a12, a23, a31 = s.symbols('a11 a22 a33 a12 a23 a31', real=True)
b11, b22, b33, b12, b23, b31 = s.symbols('b11 b22 b33 b12 b23 b31', real=True)
a = s.Matrix([[a11, a12, a31], [a12, a22, a23], [a31, a23, a33]])
da = s.Matrix([[b11, b12, b31], [b12, b22, b23], [b31, b23, b33]])
q = (p.T*a*p)[0]
f = s.sqrt(q)
fp = s.Matrix([s.diff(f, x) for x in p])
fpp = s.hessian(f, list(p))
fx = (p.T*da*p)[0]/(2*f)  # one arbitrary spatial directional derivative
fpx = s.Matrix([s.diff(fx, x) for x in p])
check('degree_one_euler_identity', zero(p.dot(fp)-f))
check('momentum_hessian_contraction', all(zero(x) for x in p.T*fpp))
check('mixed_derivative_euler_identity', zero(p.dot(fpx)-fx))
force = s.Integer(0) if mode == 'omit_spatial_force' else -fx
variational_residual = s.simplify(force+p.dot(fpx))
check('full_variational_covector_identity', zero(variational_residual))

# Exact non-Euclidean initial covector, not just its tangential restriction.
inverse_metric = s.diag(-1, 1, 4, 9)
tangent = s.Matrix([3, 2, 0])
norm = s.Integer(5)
normal = norm if mode == 'past_root' else -norm
covector = s.Matrix([normal, *tangent])
raised = inverse_metric*covector
check('full_initial_null_residual', (covector.T*raised)[0] == 0)
check('full_initial_future_root', raised[0] > 0)
check('initial_tangential_pullback', covector[1:, :] == tangent)
wrong_normal = s.Matrix([-4, *tangent])
check('independent_normal_magnitude_rejected', (wrong_normal.T*inverse_metric*wrong_normal)[0] == 9)


def admissible_initial_gradient(v):
    length2 = sum(x*x for x in v)
    return length2 >= 0 if mode == 'allow_zero' else length2 > 0


check('zero_initial_phase_gradient_excluded', not admissible_initial_gradient((0, 0, 0)))
check('nonzero_initial_phase_gradient_admitted', admissible_initial_gradient((3, 2, 0)))

# Exact incoming phase/projection control on flat space before the crossing.
x, y, z, t = s.symbols('x y z t', real=True)
coords = s.Matrix([x, y, z])
radius = s.sqrt(x*x+y*y+z*z)
theta = -radius-t
theta_covector = s.Matrix([s.diff(theta, v) for v in (t, x, y, z)])
flat_inverse = s.diag(-1, 1, 1, 1)
theta_raised = flat_inverse*theta_covector
check('original_flat_phase_eikonal', zero((theta_covector.T*theta_raised)[0]))
check('original_flat_phase_future', theta_raised[0] == 1)
affine_resid = s.Matrix([sum(theta_raised[a]*s.diff(theta_covector[b], v)
                            for a, v in enumerate((t, x, y, z))) for b in range(4)])
check('full_gradient_affine_geodesic_identity', all(zero(v) for v in affine_resid))

sign = 1 if mode == 'wrong_characteristic_sign' else -1
flow = (1+sign*t/radius)*coords
point = {x: s.Integer(3), y: s.Integer(0), z: s.Integer(0), t: s.Integer(1)}
flow_point = flow.subs(point)
transported_theta = -s.sqrt(flow_point.dot(flow_point))-1
check('phase_constant_on_correct_characteristics', transported_theta == -3)
r0 = s.symbols('r0', positive=True)
jac = s.simplify(flow.jacobian(coords).subs({x: r0, y: 0, z: 0}))
check('projection_radial_transverse_eigenvalues',
      all(zero(v) for v in jac-s.diag(1, 1-t/r0, 1-t/r0)))
determinant = s.factor(jac.det())
check('projection_boundary', determinant.subs(t, r0) == 0 and determinant.subs(t, 0) == 1)

# A compact-slice critical-point control; the maximum theorem is analytic.
phi_torus = s.cos(x)+s.cos(y)+s.cos(z)
critical = tuple(s.diff(phi_torus, v).subs({x: 0, y: 0, z: 0}) for v in (x, y, z))
check('torus_critical_point_control', critical == (0, 0, 0))
check('critical_null_covector_must_vanish', -s.Symbol('normal', real=True)**2 ==
      (s.Matrix([s.Symbol('normal', real=True), 0, 0, 0]).T*flat_inverse*
       s.Matrix([s.Symbol('normal', real=True), 0, 0, 0]))[0])

print(json.dumps({
    'status': 'PASS', 'mutant': mode, 'guard_count': len(guards), 'guards': guards,
    'symbolic_euler_residual': str(s.simplify(p.dot(fp)-f)),
    'symbolic_variational_residual': str(variational_residual),
    'initial_covector': list(map(str, covector)),
    'initial_raised_vector': list(map(str, raised)),
    'wrong_normal_null_residual': '9',
    'incoming_projection_jacobian_at_axis': [[str(v) for v in jac.row(i)] for i in range(3)],
    'incoming_projection_determinant': str(determinant),
    'compact_control_gradient': list(map(str, critical)),
    'sympy_version': s.__version__,
    'hypotheses_not_machine_proved': ['actual smooth supplied metric', 'positive spatial metric',
                                    'local ODE existence/smooth dependence', 'projection inverse domain',
                                    'compact maximum theorem', 'physical interpretation'],
    'evidence_type': 'exact/symbolic identities and scoped controls, not independent proof',
}, indent=2, sort_keys=True))
