"""RT2 source-first exact diagnostics; no author imports or result reads."""
import itertools
import json
import platform

import sympy as s

u, r, x, y = s.symbols('u r x y', real=True)
coords = (u, r, x, y)
N = 4
passed = []
rejected = {}


def zero(value):
    entries = list(value) if isinstance(value, s.MatrixBase) else [value]
    return all(s.simplify(t) == 0 for t in entries)


def check(name, value):
    assert zero(value), (name, value)
    passed.append(name)


def red(name, residual):
    try:
        assert zero(residual), (name, residual)
    except AssertionError:
        rejected[name] = str(residual)
    else:
        raise AssertionError(('false pass', name))


def geometry(H):
    g = s.Matrix([[H, 1, 0, 0], [1, 0, 0, 0],
                  [0, 0, 1, 0], [0, 0, 0, 1]])
    inv = g.inv()
    C = [[[s.simplify(sum(inv[k, l] * (s.diff(g[l, j], coords[i])
                + s.diff(g[l, i], coords[j]) - s.diff(g[i, j], coords[l]))
                for l in range(N)) / 2) for j in range(N)]
                for i in range(N)] for k in range(N)]
    Ric = s.Matrix(N, N, lambda i, j: s.simplify(sum(
        s.diff(C[k][i][j], coords[k]) - s.diff(C[k][i][k], coords[j])
        + sum(C[k][i][j] * C[l][k][l] - C[l][i][k] * C[k][j][l]
              for l in range(N)) for k in range(N))))
    scalar = s.simplify(sum(inv[i, j] * Ric[i, j]
                           for i, j in itertools.product(range(N), repeat=2)))
    return g, inv, C, Ric, scalar


def divergence(v, C):
    return s.simplify(sum(s.diff(v[i], coords[i])
                         + sum(C[i][i][k] * v[k] for k in range(N))
                         for i in range(N)))


q = s.Matrix([1, 0, 0, 0])
H1 = -(2 + u) * (3 * x*x + x**4 / 6)
g1, gi1, C1, Ric1, R1 = geometry(H1)
sigma1 = (2 + u) * (3 + x*x)
check('separable_actual_full_Ricci', Ric1 - sigma1 * q*q.T)
check('separable_actual_scalar', R1)
check('separable_metric_determinant', g1.det() + 1)
check('separable_null_exact_gradient', (q.T*gi1*q)[0])
check('separable_connection_current_conservation', divergence(sigma1*gi1*q, C1))
check('separable_log_mixed_derivative', s.diff(s.log(sigma1), u, x))
check('fixed_measure_unique_phase_squared', sigma1 / (3+x*x) - (2+u))
check('fixed_measure_primitive_derivative', s.diff(s.Rational(2, 3)*(2+u)**s.Rational(3, 2), u)**2 - (2+u))
check('fixed_measure_full_tensor', (sigma1/(2+u)) * ((2+u)*q*q.T) - Ric1)
red('fixed_phase_prescribed_measure_mismatch', (sigma1-(3+x*x)).subs({u:0, x:0}))
red('free_measure_constant_changes_current', (sigma1/2-sigma1).subs({u:0, x:0}))

H2 = -2*x*x-u*x**3/3
g, gi, C, Ric, R = geometry(H2)
sigma = 2+u*x
check('nonseparable_actual_full_Ricci', Ric-sigma*q*q.T)
check('nonseparable_actual_scalar', R)
check('nonseparable_full_square_zero', (gi*Ric)**2)
check('nonseparable_connection_current_conservation', divergence(sigma*gi*q, C))
mixed = s.diff(s.log(sigma), u, x)
check('nonseparable_log_mixed_exact_value', mixed-2/sigma**2)
red('fixed_label_free_measure_factorization_fails', mixed.subs({u:0, x:0}))

a = 1+u*u
F = u+u**3/3
check('increasing_phase_derivative', s.diff(F, u)-a)
qp = a*q
np = sigma/a**2
j = sigma*gi*q
jp = np*gi*qp
check('transformed_full_source_tensor', np*qp*qp.T-Ric)
check('transformed_connection_current_conservation', divergence(jp, C))
check('all_current_components_scaling', jp-j/a)
red('wrong_density_exponent', ((sigma/a)*qp*qp.T-Ric).subs({u:s.Rational(1,4), x:0}))
red('claimed_unchanged_current', (jp-j).subs({u:s.Rational(1,4), x:0}))

U = s.Matrix([-1, (H2+1)/2, 0, 0])
check('actual_observer_unit_norm', (U.T*g*U)[0]+1)
check('actual_observer_future_pairing', (U.T*g*(gi*q))[0]+1)
Gamma = -(U.T*g*j)[0]
Gammap = -(U.T*g*jp)[0]
check('full_current_observer_scalar', Gamma-sigma)
check('changed_current_observer_scalar', Gammap-sigma/a)
red('claimed_unchanged_readout', (Gammap-Gamma).subs({u:s.Rational(1,4), x:0}))

z = (2*x+u*x*x/2)/a**2
new = s.Matrix([F, r/a, z, y])
K = new.jacobian(coords)
D = sigma/a**2
check('label_Jacobian', s.diff(z, x)-D)
check('full_coordinate_Jacobian', K.det()-D)
L = K.inv()
gnew = s.simplify(L.T*g*L)
check('full_metric_determinant_transform', gnew.det()+1/D**2)
check('new_adapted_ray_metric_row', gnew[1, :]-s.Matrix([[1,0,0,0]]))
screen = gnew.extract([2,3], [2,3])
check('screen_full_Gram_metric', screen-s.diag(1/D**2,1))
Jnew = 1/D  # D>0 on the explicitly retained |u|,|x|<1/4 patch.
check('new_fixed_product_density', Jnew*np-1)
check('new_phase_current_components', K*jp-s.Matrix([0,np,0,0]))
Ricnew = s.simplify(L.T*Ric*L)
qnew = L.T*qp
check('transformed_full_covector', qnew-q)
check('transformed_full_source_tensor_new_coordinates', Ricnew-np*qnew*qnew.T)
Unew = K*U
jnew = K*jp
check('observer_scalar_coordinate_invariance', -(Unew.T*gnew*jnew)[0]-Gammap)
check('full_quotient_measure_Jacobian', Jnew*np*a*D-sigma/a)
red('missing_screen_Jacobian_breaks_product', (np-1).subs({u:0,x:0}))
red('same_labels_same_measure_phase_scale_breaks_match', (1/a**2-1).subs(u,s.Rational(1,4)))

# Exact finite patch support: for |u|<=1/4, |x|<=1/4, sigma>=31/16,
# a<=17/16, so D>=496/289>0 and endpoints cover a common |z|<1/4.
Dlower = s.Rational(31,16)/s.Rational(17,16)**2
assert Dlower > 0
passed.append('uniform_positive_finite_patch_Jacobian_bound')
endpoint_lower = (s.Rational(1,2)-s.Rational(1,128))/s.Rational(17,16)**2
assert endpoint_lower > s.Rational(1,4)
passed.append('common_new_label_box_covered')
reflection = s.diag(1,1,-1,1)
g_reflected = reflection.T*g*reflection
screen_reflected = g_reflected.extract([2,3],[2,3])
check('orientation_reversal_actual_screen_area', screen_reflected.det()-1)
check('orientation_reversal_actual_readout',
      -((reflection*U).T*g_reflected*(reflection*jp))[0]-Gammap)

print(json.dumps(dict(
    status='PASS_EXACT_DIAGNOSTICS', python=platform.python_version(),
    sympy=s.__version__, groups=len(passed), checks=passed,
    red_controls=len(rejected), rejected=rejected,
    exact_values=dict(separable_Ric_uu=str(Ric1[0,0]),
                      nonseparable_Ric_uu=str(Ric[0,0]),
                      mixed_log=str(s.simplify(mixed)),
                      new_label_D=str(D),
                      Gamma_at_point=str(Gamma.subs({u:s.Rational(1,4),x:0})),
                      Gammap_at_point=str(Gammap.subs({u:s.Rational(1,4),x:0})),
                      D_lower=str(Dlower), endpoint_lower=str(endpoint_lower)),
    limitations='Exact finite diagnostic identities and RED controls; general quantifiers belong to the sealed analytic argument.'
), indent=2, sort_keys=True))
