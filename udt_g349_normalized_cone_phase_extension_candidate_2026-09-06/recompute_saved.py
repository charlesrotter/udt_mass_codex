"""Read saved inputs and recompute finite readouts with stdlib rational arithmetic.

No check_exact import, symbolic package, or stored-output-as-input calculation.
Same author/context: this is implementation separation, not independent review.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math

saved = json.loads(Path(__file__).with_name('CHECK_RESULT.json').read_text())
data = saved['saved_readout_inputs']
vec = lambda entries: tuple(F(q) for q in entries)
direction = vec(data['direction'])
screen = [vec(data['screen1']), vec(data['screen2'])]
cut_gradients = vec(data['cut_gradients'])
radii = vec(data['radii'])
observers = [vec(obs) for obs in data['observers']]
spacing, density = F(data['spacing']), F(data['density'])


def minkowski(v, w):
    return -v[0]*w[0] + sum(v[j]*w[j] for j in (1, 2, 3))


def rational_sqrt(value):
    numerator, denominator = math.isqrt(value.numerator), math.isqrt(value.denominator)
    if numerator*numerator != value.numerator or denominator*denominator != value.denominator:
        raise ValueError('Witness square root is not rational')
    return F(numerator, denominator)


k = (F(1), *direction)
results = []
for radius, observer in zip(radii, observers):
    # Direct Cartesian cut differentials: time derivative and spatial vector.
    tangents = [(cut_gradients[j],
                 *(cut_gradients[j]*direction[m]+radius*screen[j][m] for m in range(3)))
                for j in range(2)]
    gram00 = minkowski(tangents[0], tangents[0])
    gram11 = minkowski(tangents[1], tangents[1])
    gram01 = minkowski(tangents[0], tangents[1])
    jacobian = rational_sqrt(gram00*gram11 - gram01*gram01)
    omega = -minkowski(observer, k)
    if minkowski(observer, observer) != -1 or observer[0] <= 0:
        raise AssertionError('Invalid saved observer')
    results.append((jacobian, omega, omega*density/(spacing*jacobian)))
actual = {'jacobians': [str(row[0]) for row in results],
          'omegas': [str(row[1]) for row in results],
          'rates': [str(row[2]) for row in results],
          'ratio': str(results[1][2]/results[0][2])}
if actual != saved['readout_outputs']:
    raise AssertionError({'recomputed': actual, 'saved': saved['readout_outputs']})
print(json.dumps({'status': 'PASS_SAVED_INPUT_RATIONAL_RECOMPUTATION',
                  'method': 'Cartesian finite cut Gram and observer contraction',
                  'independence': 'different implementation; same author/context',
                  'results': actual}, indent=2))
