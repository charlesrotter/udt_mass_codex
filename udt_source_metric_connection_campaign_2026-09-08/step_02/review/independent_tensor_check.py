"""SM2 source-first exact diagnostics; no author imports or result reads."""
import json
import platform
import sympy as s


checks = []
numbers = {}


def require(name, condition, value=None):
    assert bool(condition), name
    checks.append(name)
    if value is not None:
        numbers[name] = str(value)


def zero_matrix(matrix):
    return all(s.simplify(entry) == 0 for entry in matrix)


eta = s.diag(-1, 1, 1, 1)
q0 = s.Matrix([-1, 0, 0, 1])


def boost(axis):
    matrix = s.zeros(4)
    matrix[0, axis] = matrix[axis, 0] = 1
    return matrix


def rotation(axis1, axis2):
    matrix = s.zeros(4)
    matrix[axis1, axis2] = 1
    matrix[axis2, axis1] = -1
    return matrix


rotation_z = rotation(1, 2)
null_x = boost(1) - rotation(1, 3)
null_y = boost(2) - rotation(2, 3)
generators = [rotation_z, null_x, null_y]
require('stabilizer_generators_lorentz', all(
    zero_matrix(a.T * eta + eta * a) for a in generators))
require('stabilizer_generators_fix_covector', all(
    zero_matrix(a.T * q0) for a in generators))
components = s.symbols('p0:10')
p = s.zeros(4)
k = 0
for i in range(4):
    for j in range(i, 4):
        p[i, j] = p[j, i] = components[k]
        k += 1
equations = [entry for a in generators for entry in a.T * p + p * a]
matrix, rhs = s.linear_eq_to_matrix(equations, components)
require('full_stabilizer_nullity_two', len(matrix.nullspace()) == 2,
        len(matrix.nullspace()))
aa, bb = s.symbols('aa bb')
target = aa * eta + bb * q0 * q0.T
require('metric_and_null_square_invariant', all(
    zero_matrix(a.T * target + target * a) for a in generators))
rotation_equations = list(rotation_z.T * p + p * rotation_z)
rotation_matrix, _ = s.linear_eq_to_matrix(rotation_equations, components)
require('rotation_only_false_pass_has_four_parameters',
        len(rotation_matrix.nullspace()) == 4,
        len(rotation_matrix.nullspace()))
preferred_time = s.diag(1, 0, 0, 0)
require('preferred_time_mutant_passes_rotation_only', zero_matrix(
    rotation_z.T * preferred_time + preferred_time * rotation_z))
bad_invariance = null_x.T * preferred_time + preferred_time * null_x
require('preferred_time_mutant_rejected_by_null_rotation',
        not zero_matrix(bad_invariance), bad_invariance)

# Cartesian Minkowski partial divergence is the full covariant divergence.
# This avoids a density-divergence formula and any author implementation.
t, x, y, z = s.symbols('t x y z', real=True)
coords = [t, x, y, z]
radius = s.sqrt(x*x + y*y + z*z)
phase = radius - t
q = s.Matrix([s.diff(phase, coordinate) for coordinate in coords])
ell = eta * q
require('spherical_phase_is_null', s.simplify((q.T * eta * q)[0]) == 0)
acceleration = s.Matrix([sum(ell[a] * s.diff(ell[b], coords[a])
                            for a in range(4)) for b in range(4)])
require('spherical_phase_affine', zero_matrix(acceleration))
expansion = s.simplify(sum(s.diff(ell[a], coords[a]) for a in range(4)))
require('spherical_expansion', s.simplify(expansion - 2/radius) == 0,
        expansion)
amplitude = s.symbols('amplitude', positive=True)
density = amplitude / radius**2
current = density * ell
current_div = s.simplify(sum(s.diff(current[a], coords[a]) for a in range(4)))
require('spherical_product_current_conserved', current_div == 0, current_div)


def tensor_div(tensor):
    return s.Matrix([s.simplify(sum(s.diff(tensor[a, b], coords[a])
                                   for a in range(4))) for b in range(4)])


function_a = s.Function('A')
function_b = s.Function('B')
tensor = function_a(density) * eta + function_b(density) * ell * ell.T
divergence = tensor_div(tensor)
nn = s.symbols('nn', positive=True)
expected = eta * s.Matrix([s.diff(function_a(density), c) for c in coords])
coefficient = (function_b(density) - density *
               s.diff(function_b(nn), nn).subs(nn, density)) * expansion
expected += coefficient * ell
require('full_cartesian_divergence_matches_general_reduction',
        zero_matrix(divergence - expected))
cc, dd = s.symbols('cc dd', real=True)
good = cc * eta + dd * density * ell * ell.T
require('classified_tensor_spherical_divergence_zero',
        zero_matrix(tensor_div(good)))
event = {t: 0, x: 1, y: 2, z: 2, amplitude: 9}
bad_quadratic_div = tensor_div(density**2 * ell * ell.T)
bad_quadratic_at = bad_quadratic_div.subs(event)
require('quadratic_density_mutant_rejected_on_expansion',
        not zero_matrix(bad_quadratic_at), bad_quadratic_at)
require('quadratic_density_exact_expected_divergence',
        zero_matrix(bad_quadratic_div + density**2 * expansion * ell))

# A genuine parallel product family supplies density as a transverse label
# function. Its values and transverse derivatives are unrestricted locally.
parallel_ell = s.Matrix([1, 0, 0, 1])
parallel_density = 2 + x
parallel_bad = parallel_density**2 * parallel_ell * parallel_ell.T
require('quadratic_density_mutant_passes_parallel_family',
        zero_matrix(tensor_div(parallel_bad)))
bad_metric = parallel_density * eta
bad_metric_div = tensor_div(bad_metric)
require('variable_metric_coefficient_rejected',
        not zero_matrix(bad_metric_div), bad_metric_div)
generic_metric_div = tensor_div(function_a(parallel_density) * eta)
require('parallel_family_isolates_A_derivative',
        s.simplify(generic_metric_div[1] -
                   s.diff(function_a(nn), nn).subs(nn, parallel_density)) == 0)

# A transported but nonconstant scalar changes the available data class.
transported = 2 + x/radius
transport_residual = s.simplify(sum(ell[a] * s.diff(transported, coords[a])
                                  for a in range(4)))
require('extra_scalar_transported', transport_residual == 0)
require('extra_transport_data_tensor_conserved', zero_matrix(
    tensor_div(density * transported * ell * ell.T)))
nontransported = 2 + radius
bad_extra_div = tensor_div(density * nontransported * ell * ell.T)
require('nontransported_scalar_mutant_rejected',
        not zero_matrix(bad_extra_div.subs(event)), bad_extra_div.subs(event))
require('nontransported_scalar_full_residual', zero_matrix(
    bad_extra_div - density * ell))

# Supplied normalization checks use actual G352 simultaneous gauge.
Theta, Delta, scale, shift = s.symbols('Theta Delta scale shift', positive=True)
gauge_derivative = s.diff((scale*Theta + shift)/(scale*Delta), Theta)
require('phase_and_spacing_gauge_invariant',
        s.simplify(gauge_derivative - 1/Delta) == 0)
require('phase_only_scaling_is_not_gauge',
        s.simplify(s.diff((2*Theta + shift)/Delta, Theta) - 1/Delta) != 0)
measure_rescaled = cc * eta + dd * (2*density) * ell * ell.T
require('measure_scaling_changes_tensor_null_part',
        not zero_matrix((measure_rescaled - good).subs({**event, dd: 1})))

print(json.dumps({'checks': checks, 'count': len(checks),
                  'values': numbers, 'python': platform.python_version(),
                  'sympy': s.__version__, 'evidence': 'exact symbolic diagnostics'},
                 indent=2, sort_keys=True))
