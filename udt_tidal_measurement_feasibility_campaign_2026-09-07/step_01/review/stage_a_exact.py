"""Independent exact rotation-jet and nuisance-direction reconstruction."""
import json
import platform
import sympy as s

t = s.symbols('t', real=True)
wx, wy, wz, ax, ay, az = s.symbols('wx wy wz ax ay az', real=True)
t11, t22, t33, t12, t13, t23 = s.symbols('t11 t22 t33 t12 t13 t23', real=True)
length = s.symbols('L', positive=True)
q = s.symbols('q', real=True)
eye = s.eye(3)
T = s.Matrix([[t11, t12, t13], [t12, t22, t23], [t13, t23, t33]])

def cross(x, y, z):
    return s.Matrix([[0, -z, y], [z, 0, -x], [-y, x, 0]])

W = cross(wx, wy, wz)
Wd = cross(ax, ay, az)
rotation_jet = eye + t * W + t*t * (Wd + W*W) / 2
records = {}

def check(name, expression):
    if hasattr(expression, 'applyfunc'):
        simplified = expression.applyfunc(s.expand)
        ok = simplified == s.zeros(*simplified.shape)
    else:
        simplified = s.expand(expression)
        ok = simplified == 0
    assert ok, (name, simplified)
    records[name] = True

# Generate nine force-difference components from three fixed positive arms.
columns = []
for j in range(3):
    rplus = length * eye[:, j] / 2
    rminus = -rplus
    holding = []
    for r in (rplus, rminus):
        inertial_position = rotation_jet * r
        inertial_acceleration = inertial_position.diff(t, 2).subs(t, 0)
        freely_falling_acceleration = -T * r
        holding.append(inertial_acceleration - freely_falling_acceleration)
    half_difference = (holding[0] - holding[1]) / 2
    columns.append(s.expand(2 * half_difference / length))
D = s.Matrix.hstack(*columns)
symD = (D + D.T) / 2
antiD = (D - D.T) / 2
check('rotation_jet_orthogonality_through_order_2', (rotation_jet.T*rotation_jet).diff(t,2).subs(t,0))
check('compensation_gradient', D - (T + W*W + Wd))
check('symmetric_inversion', symD - W*W - T)
check('angular_acceleration_antisymmetric_part', antiD - Wd)
check('trace_correction', s.trace(D) + 2*(wx*wx+wy*wy+wz*wz) - s.trace(T))
check('gravity_potential_gradient_opposite_tide', -(symD-W*W) - (-T))
check('absolute_scalar_bias_alias', (T+q*eye) + (W*W+Wd-q*eye) - D)
centering = s.eye(4) - s.ones(4)/4
check('constant_removed_by_centering', centering*s.ones(4,1))
check('rotation_leaves_isotropic_scalar_unchanged_at_jet_order_2', (rotation_jet.T*(q*eye)*rotation_jet).diff(t,2).subs(t,0))

# Exact counterexamples to wrong signs and omitted factor two; no reused oracle.
sub = {t11:2,t22:3,t33:5,t12:7,t13:11,t23:13,wx:1,wy:2,wz:3,ax:4,ay:5,az:6}
assert (symD + W*W - T).subs(sub) != s.zeros(3)
records['opposite_rotation_sign_rejected'] = True
assert (symD/2 - W*W - T).subs(sub) != s.zeros(3)
records['missing_half_difference_factor_rejected'] = True
assert (symD-W*W+T).subs(sub) != s.zeros(3)
records['potential_equals_tide_sign_rejected'] = True

print(json.dumps({
    'python': platform.python_version(), 'sympy': s.__version__,
    'kind': 'exact_symbolic_and_synthetic_no_observations',
    'checks': records,
    'D': str(D), 'trace_T': str(s.trace(T)),
    'wrong_rotation_sign_trace_residual': str(s.expand(s.trace(symD+W*W-T))),
    'scalar_alias': 'T -> T+qI; additive compensation-gradient bias -> bias-qI',
    'limitations': 'Local ideal conditional interface; not a physical sensor calibration or GOCE data validation.'
}, indent=2, sort_keys=True))
