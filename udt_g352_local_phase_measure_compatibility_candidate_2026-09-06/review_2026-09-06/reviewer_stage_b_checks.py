"""Bounded separate-context review checks; original source files are never edited.

Independent geometric arithmetic uses only Fraction, not candidate implementations.
In-memory implementation mutations are explicitly separate regression probes.
"""
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
import hashlib
import json
import platform
import traceback

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / 'udt_g352_local_phase_measure_compatibility_candidate_2026-09-06'


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def lorentz(a, b):
    return -a[0]*b[0] + dot(a[1:], b[1:])


def sqrtq(q):
    a, b = isqrt(q.numerator), isqrt(q.denominator)
    assert a*a == q.numerator and b*b == q.denominator
    return Q(a, b)


def independent_geometry():
    # Off-equator stereographic sphere chart, independently differentiated.
    x, y = Q(1, 3), Q(1, 2)
    denominator = 1+x*x+y*y
    numerator = [2*x, 2*y, 1-x*x-y*y]
    n = [value/denominator for value in numerator]
    nx = [(d*denominator-value*2*x)/denominator**2
          for d, value in zip([2, 0, -2*x], numerator)]
    ny = [(d*denominator-value*2*y)/denominator**2
          for d, value in zip([0, 2, -2*y], numerator)]
    assert dot(n, n) == 1 and dot(n, nx) == dot(n, ny) == 0
    solid_angle = sqrtq(dot(nx, nx)*dot(ny, ny)-dot(nx, ny)**2)
    assert solid_angle == 4/denominator**2
    ray = [Q(1)] + n
    assert lorentz(ray, ray) == 0
    observers = [[Q(1), Q(0), Q(0), Q(0)], [Q(5,4)] + [Q(3,4)*v for v in n]]
    rows = []
    for radius, observer in zip([Q(2), Q(3)], observers):
        # Cut gradients deliberately nonzero. t=r-theta on each phase sheet.
        cut_x, cut_y = Q(2, 5), Q(-3, 7)
        X = [cut_x] + [cut_x*a+radius*b for a, b in zip(n, nx)]
        Y = [cut_y] + [cut_y*a+radius*b for a, b in zip(n, ny)]
        gram = [lorentz(X,X), lorentz(X,Y), lorentz(Y,Y)]
        assert gram == [radius**2*dot(nx,nx), radius**2*dot(nx,ny), radius**2*dot(ny,ny)]
        area = sqrtq(gram[0]*gram[2]-gram[1]**2)/solid_angle
        assert observer[0] > 0 and lorentz(observer, observer) == -1
        frequency = -lorentz(observer, ray)
        density, spacing = Q(5,6), Q(7,3)
        rate = frequency*density/(spacing*area)
        rows.append({'radius': str(radius), 'area_per_solid_angle': str(area),
                     'frequency': str(frequency), 'rate': str(rate)})
    assert [r['area_per_solid_angle'] for r in rows] == ['4','9']
    assert [r['frequency'] for r in rows] == ['1','1/2']
    assert Q(rows[1]['rate'])/Q(rows[0]['rate']) == Q(2,9)
    # Different measures on a fixed unit-square label chart, same total.
    def polynomial_mass(coeffs, end):
        return sum(c*end**(degree+1)/Q(degree+1) for degree,c in enumerate(coeffs))
    uniform, profile = [Q(1)], [Q(1,2), Q(1)]
    assert polynomial_mass(uniform,Q(1)) == polynomial_mass(profile,Q(1)) == 1
    assert polynomial_mass(uniform,Q(1,2)) == Q(1,2)
    assert polynomial_mass(profile,Q(1,2)) == Q(3,8)
    return {'sphere_direction': list(map(str,n)), 'solid_angle_coefficient': str(solid_angle),
            'cuts': rows, 'transfer': '2/9', 'unit_square_half_masses': ['1/2','3/8'],
            'method': 'Fraction Cartesian stereographic derivatives and Lorentzian Gram determinants; nonzero cut gradients'}


def mutated_candidate_probes():
    import sympy as sp
    original_path = PACKAGE / 'check_witnesses.py'
    original = original_path.read_text()
    probes = [
        ('reverse_frequency_sign', 'freq = -(observer.T * covector)[0]', 'freq = (observer.T * covector)[0]'),
        ('omit_frequency_in_rate', 'frequencies[i] * density / (spacing * jacobians[i])', 'density / (spacing * jacobians[i])'),
        ('area_equals_radius', 'jacobians = [sp.sqrt((gram.det()/sp.sin(a)**2).subs(radius, ri)) for ri in (2, 3)]', 'jacobians = [sp.Rational(ri) for ri in (2, 3)]'),
    ]
    out = []
    for name, before, after in probes:
        assert original.count(before) == 1
        modified = original.replace(before, after)
        namespace = {'__name__': 'review_probe', '__file__': str(original_path)}
        exec(compile(modified, f'<{name}>', 'exec'), namespace)
        try:
            namespace['collect_checks']()
        except AssertionError as exc:
            detail = traceback.format_exc()
            (ROOT / f'{name}.failure.txt').write_text(detail)
            out.append({'probe': name, 'caught': True, 'failure': str(exc),
                        'modified_source_sha256': hashlib.sha256(modified.encode()).hexdigest()})
        else:
            raise AssertionError(f'Expected a failing code probe: {name}')
    # Deliberately wrong acceleration implementation. All original examples are affine.
    namespace = {'__name__': 'review_probe', '__file__': str(original_path)}
    exec(compile(original, '<zero_acceleration_probe>', 'exec'), namespace)
    genuine_acceleration = namespace['acceleration']
    namespace['acceleration'] = lambda metric, vector, coords: sp.zeros(len(coords),1)
    namespace['collect_checks']()
    data_mutations = namespace['sensitivity_checks']()
    assert len(namespace['CHECKS']) == 86
    assert all(value['rejected'] for value in data_mutations.values())
    t,x,y,z = sp.symbols('t x y z', real=True)
    metric = sp.diag(-1,1,1,1)
    vector = sp.Matrix([1+t,0,0,1+t])
    expected = sp.Matrix([1+t,0,0,1+t])
    actual = genuine_acceleration(metric,vector,(t,x,y,z))
    assert actual == expected
    assert namespace['acceleration'](metric,vector,(t,x,y,z)) != expected
    out.append({'probe': 'replace_acceleration_by_zero', 'caught_by_original_86_checks': False,
                'original_data_sensitivity_rejections': len(data_mutations),
                'reviewer_nonaffine_null_control_catches_it': True,
                'correct_acceleration': list(map(str,actual)),
                'meaning': 'Exposes declared finite-check coverage limit; does not refute analytic Hessian proof or original correct helper.'})
    return {'sympy': sp.__version__, 'probes': out}


def main():
    result = {'python': platform.python_version(), 'model_identity': 'UNKNOWN',
              'independent_geometry': independent_geometry(),
              'implementation_probes': mutated_candidate_probes(),
              'limits': ['No accepted-source replay or scientific promotion',
                         'Three caught code mutations plus one surviving mutant; not exhaustive mutation coverage',
                         'Finite exact arithmetic is not the general local proof']}
    (ROOT / 'REVIEWER_STAGE_B_RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
