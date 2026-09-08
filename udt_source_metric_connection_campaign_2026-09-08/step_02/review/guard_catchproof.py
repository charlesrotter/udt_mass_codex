"""Explicit RED-path catch proof for exact independent SM2 acceptance guards."""
import json
import sympy as s

t, x, y, z = s.symbols('t x y z', real=True)
coords = [t, x, y, z]
metric = s.diag(-1, 1, 1, 1)
r = s.sqrt(x*x + y*y + z*z)
ell = s.Matrix([1, x/r, y/r, z/r])
n = 9/r**2
event = {t: 0, x: 1, y: 2, z: 2}


def div(tensor):
    return s.Matrix([sum(s.diff(tensor[a, b], coords[a]) for a in range(4))
                     for b in range(4)]).applyfunc(s.simplify).subs(event)


def accept_zero(residual):
    assert all(s.simplify(value) == 0 for value in residual), str(residual)


red = {}


def require_red(name, residual):
    try:
        accept_zero(residual)
    except AssertionError as error:
        red[name] = str(error)
    else:
        raise RuntimeError('FALSE PASS: ' + name)


accept_zero(div(n * ell * ell.T))
require_red('replace_n_by_n_squared', div(n**2 * ell * ell.T))
accept_zero(div(3 * metric))
require_red('replace_constant_metric_coefficient_by_n', div(n * metric))
accept_zero(div(n * (2 + x/r) * ell * ell.T))
require_red('replace_transported_weight_by_radius', div(n * r * ell * ell.T))
null_rotation = s.Matrix([[0, 1, 0, 0], [1, 0, 0, -1],
                         [0, 0, 0, 0], [0, 1, 0, 0]])
q = s.Matrix([-1, 0, 0, 1])
correct = metric + q*q.T
accept_zero(null_rotation.T*correct + correct*null_rotation)
extra = s.diag(1, 0, 0, 0)
require_red('add_rotation_only_invariant_time_tensor',
            null_rotation.T*(correct + extra) + (correct + extra)*null_rotation)
Delta, Theta = s.symbols('Delta Theta', positive=True)
accept_zero([s.diff(2*Theta/(2*Delta), Theta) - 1/Delta])
require_red('rescale_phase_without_spacing',
            [s.diff(2*Theta/Delta, Theta) - 1/Delta])
print(json.dumps({'matching_acceptance_guards_red': red,
                  'red_count': len(red), 'positive_controls_passed': 5,
                  'scope': 'finite exact catch proof; not analytic completeness'},
                 indent=2, sort_keys=True))
