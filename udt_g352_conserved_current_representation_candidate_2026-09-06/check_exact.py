"""Bounded exact regression witnesses, not proof or physical confirmation.

All metric/witness parameters are free-and-explored mathematical data. No
physical action/equation/constant is selected. Writes no files. Execute without
Python optimization; --mutation intentionally damages one implementation branch.
"""
import argparse
import json
from pathlib import Path
import platform
import sympy as S

parser = argparse.ArgumentParser()
parser.add_argument('--mutation', choices=[
    'omit_area', 'coordinate_divergence', 'divergence_zero',
    'all_products', 'omit_frequency', 'omit_label_jacobian'])
mutation = parser.parse_args().mutation
if not __debug__:
    raise RuntimeError('Assertions require non-optimized Python')
passed = []


def eq(name, actual, expected):
    assert S.simplify(actual - expected) == 0, name
    passed.append(name)


def truth(name, statement):
    assert bool(statement), name
    passed.append(name)


def density(s, spacing, area):
    if mutation == 'omit_area':
        return s / spacing
    return s / (spacing * area)


def divergence(g, vector, coordinates):
    if mutation == 'divergence_zero':
        return S.Integer(0)
    if mutation == 'coordinate_divergence':
        return S.simplify(sum(S.diff(vector[a], coordinates[a]) for a in range(4)))
    volume = S.simplify(S.sqrt(-g.det()))
    return S.simplify(sum(S.diff(volume * vector[a], coordinates[a])
                          for a in range(4)) / volume)


def product_compatible(F, theta):
    if mutation == 'all_products':
        return True
    return S.simplify(S.diff(F, theta)) == 0


def readout(rho, k, u, g):
    omega = -(u.T * g * k)[0]
    if mutation == 'omit_frequency':
        omega = S.Integer(1)
    return S.simplify(rho * omega)


def relabel(coefficient, inverse_substitution, inverse_jacobian):
    value = coefficient.subs(inverse_substitution, simultaneous=True)
    if mutation == 'omit_label_jacobian':
        return value
    return value * inverse_jacobian


# Arbitrary H,W and non-diagonal positive screen block: no zero-shift assumption.
H, W1, W2, a, b, c, q1, q2 = S.symbols('H W1 W2 a b c q1 q2', real=True)
g = S.Matrix([[0, 1, 0, 0], [1, H, W1, W2],
              [0, W1, a, b], [0, W2, b, c]])
k = S.Matrix([1, 0, 0, 0])
eq('general_volume_screen_determinant', g.det(), -(a*c-b*b))
eq('full_gradient_matching', (g*k-S.Matrix([0, 1, 0, 0])).norm()**2, 0)
eq('null_norm', (k.T*g*k)[0], 0)
cut = S.Matrix([[q1, q2], [0, 0], [1, 0], [0, 1]])
for i in range(2):
    for j in range(2):
        eq(f'variable_cut_gram_{i}_{j}', (cut.T*g*cut)[i, j], g[i+2, j+2])

# Nonzero expansion: metric determinant rather than coordinate divergence.
r = S.symbols('r', positive=True)
theta, x, y, z, t = S.symbols('theta x y z t', real=True)
coords = [r, theta, x, y]
g_exp = S.Matrix([[0, 1, 0, 0], [1, -1, 0, 0],
                  [0, 0, r*r, 0], [0, 0, 0, r*r]])
rho = density(S.Integer(3), S.Integer(2), r*r)
eq('expanding_density_value', rho, 3/(2*r*r))
eq('expanding_current_conserved', divergence(g_exp, rho*k, coords), 0)
eq('nonconserved_control_detected', divergence(g_exp, k, coords), 2/r)
eq('zero_content', density(S.Integer(0), S.Integer(2), r*r), 0)
F = 2 + theta*theta + x*x + y*y
eq('phase_dependent_current_conserved', divergence(g_exp, F/r**2*k, coords), 0)
truth('phase_dependence_not_product', not product_compatible(F, theta))
truth('same_mu_is_product', product_compatible(2+x*x+y*y, theta))

# Genuinely correlated density and a varying-total density are distinct controls.
eq('correlation_mixed_log_derivative', S.diff(S.log(1+theta*x), theta, x),
   1/(1+theta*x)**2)
mass = S.integrate(2+theta, (x, 0, 1), (y, 0, 1))
eq('varying_total_mass', mass, 2+theta)
eq('varying_total_mass_derivative', S.diff(mass, theta), 1)
eq('initial_data_transport', S.diff(r*r*(F/r**2), r), 0)

# Cartesian radial recomputation differentiates the current in physical coordinates.
eta = S.diag(-1, 1, 1, 1)
R = S.sqrt(x*x+y*y+z*z)
phase = R-t
beta = S.Matrix([S.diff(phase, v) for v in [t, x, y, z]])
krad = eta*beta
eq('cartesian_radial_null', (krad.T*eta*krad)[0], 0)
eq('cartesian_radial_conservation',
   divergence(eta, krad/R**2, [t, x, y, z]), 0)
eq('cartesian_nonconserved_control', divergence(eta, krad, [t, x, y, z]), 2/R)

# A phase-dependent PASSIVE relabeling changes coefficients, not the current.
# x'=(1+theta)x on theta>-1; the full retained domain changes with the coordinates.
xp = S.symbols('xp', real=True)
oldF, oldJ = 2+x, r*r
inverse = {x: xp/(1+theta)}
invjac = 1/(1+theta)
newF = relabel(oldF, inverse, invjac)
newJ = relabel(oldJ, inverse, invjac)
eq('label_density_jacobian', newF, (2+xp/(1+theta))/(1+theta))
eq('label_ratio_invariant', newF/newJ, ((2+x)/r**2).subs(inverse))
truth('passive_coefficient_can_vary', S.simplify(S.diff(newF, theta)) != 0)
eq('passive_full_domain_total', S.integrate(newF, (xp, 0, 1+theta)), S.Rational(5,2))

# Positive affine phase gauge; nonlinear reparameterization at fixed spacing is not it.
scale, spacing, seed, area = S.symbols('scale spacing seed area', positive=True)
eq('affine_current_invariant', scale*density(seed, scale*spacing, area),
   density(seed, spacing, area))
eq('nonlinear_current_changes', (1+2*theta)*density(seed, spacing, area)
   - density(seed, spacing, area), 2*theta*seed/(spacing*area))
eq('nonlinear_current_still_conserved',
   divergence(g_exp, (1+2*theta)/r**2*k, coords), 0)

# Saved-input exact cut/readout witness: area from full variable-cut tangent Gram.
inputs = json.loads((Path(__file__).parent/'WITNESS_INPUTS.json').read_text())
spacing_value = S.Rational(inputs['phase_spacing'])
per_angle = S.Rational(inputs['measure_per_solid_angle'])
qv, qw = map(S.Rational, inputs['cut_gradient'])
knorth = S.Matrix([1, 0, 0, 1])
witness = []
for i, item in enumerate(inputs['cuts']):
    rad = S.Rational(item['radius'])
    observer = S.Matrix(list(map(S.Rational, item['observer'])))
    E = S.Matrix([[qv, qw], [2*rad, 0], [0, 2*rad], [qv, qw]])
    gram = E.T*eta*E
    Jcut = S.sqrt(gram.det())
    omega = -(observer.T*eta*knorth)[0]
    rhocut = density(4*per_angle, spacing_value, Jcut)
    gamma = readout(rhocut, knorth, observer, eta)
    eq(f'cut_{i}_observer_unit', (observer.T*eta*observer)[0], -1)
    eq(f'cut_{i}_full_area', Jcut, 4*rad*rad)
    eq(f'cut_{i}_clock_rate', gamma,
       [S.Rational(7,30), S.Rational(7,375)][i])
    # Rest-screen projection preserves area and measures the same 3-form contraction.
    projected = E.copy()
    for col in range(2):
        projected[:, col] = E[:, col] + ((observer.T*eta*E[:, col])[0]/omega)*knorth
        eq(f'cut_{i}_rest_screen_{col}', (observer.T*eta*projected[:, col])[0], 0)
    eq(f'cut_{i}_rest_screen_area', (projected.T*eta*projected).det(), gram.det())
    form_value = S.det(S.Matrix.hstack(rhocut*knorth, observer,
                                      projected[:, 0], projected[:, 1]))
    eq(f'cut_{i}_time_screen_intensity', S.Abs(form_value)/Jcut, gamma)
    witness.append({key: str(value) for key, value in {
        'area': Jcut, 'omega': omega, 'rho': rhocut, 'gamma': gamma,
        'absolute_form_on_time_screen': S.Abs(form_value)}.items()})
eq('nonzero_two_cut_ratio', S.Rational(witness[1]['gamma'])/S.Rational(witness[0]['gamma']),
   S.Rational(2,25))

print(json.dumps({'kind': 'exact finite regression, not analytic proof',
                  'python': platform.python_version(), 'sympy': S.__version__,
                  'mutation': mutation, 'passed': len(passed), 'checks': passed,
                  'cut_witness': witness, 'ratio': '2/25'}, indent=2))
