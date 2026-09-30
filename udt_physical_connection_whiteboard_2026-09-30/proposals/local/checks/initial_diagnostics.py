"""Small exact diagnostics of unadopted proposals; no field equation certified."""
import json
import platform
import sympy as s

e, v, d, q, r = s.symbols('epsilon v D Q r', real=True)
z = s.sqrt((1+s.exp(2*e)*v)/(1-s.exp(2*e)*v))
dd = s.diff(s.log(z), e).subs(e, 0)
assert s.simplify(dd-2*v/(1-v*v)) == 0
inverse_square = s.expand((d*d+(-d)**2)/2)
assert inverse_square == d*d
quiet_first = s.diff((e*q)**2/2, e).subs(e, 0)
quiet_second = s.diff((e*q)**2/2, e, 2).subs(e, 0)
assert quiet_first == 0 and quiet_second == q*q
rapidity_density = s.sinh(2*r)/4-r/2
assert s.simplify(s.diff(rapidity_density, r)-s.sinh(r)**2) == 0
assert rapidity_density.subs(r, 0) == 0
assert s.limit(rapidity_density, r, s.oo) == s.oo
eps_positive = s.symbols('eps_positive', positive=True)
W_positive = ((48*eps_positive**2)**2)**s.Rational(1,4)
assert s.simplify(W_positive-4*s.sqrt(3)*eps_positive) == 0
W = 4*s.sqrt(3)*s.Abs(e)
right = s.limit(W/e, e, 0, dir='+')
left = s.limit(W/e, e, 0, dir='-')
assert right == 4*s.sqrt(3) and left == -4*s.sqrt(3)
print(json.dumps({
  'python': platform.python_version(), 'sympy': s.__version__,
  'kind': 'author exact algebra diagnostics; not independent review',
  'network_inverse_pair_contrast': str(inverse_square),
  'flat_fixed_coordinate_protocol_D_derivative': str(s.factor(dd)),
  'flat_comoving_first_variation': str(quiet_first),
  'flat_comoving_second_variation': str(quiet_second),
  'timelike_hyperboloid_radial_volume': str(rapidity_density),
  'hyperboloid_total_volume': 'infinite',
  'tidal_modulus_positive_side': str(W_positive),
  'tidal_modulus_right_derivative': str(right),
  'tidal_modulus_left_derivative': str(left),
  'omissions': ['full ensemble existence or smoothing', 'physical query measure',
    'full action variation', 'plane-wave reconstruction', 'empirical recovery',
    'field solution', 'independent review'],
}, indent=2))
