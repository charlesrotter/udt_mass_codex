"""Independent RT1 diagnostics: no author imports or author-output reads.

All metrics/forms below are free-and-explored analytic diagnostic choices,
not physical models. The coordinate convention is signature(-+++),
Ric_bd = d_a Gamma^a_bd - d_d Gamma^a_ba
         + Gamma^a_ac Gamma^c_bd - Gamma^a_dc Gamma^c_ba.
General local proof is in the independent argument, not these finite checks.
"""

import json
import platform
import sympy as s

u, r, x, y = s.symbols('u r x y', real=True)
coords = (u, r, x, y)
N = 4
records = []
red = []


def zero(name, expression):
    entries = list(expression) if isinstance(expression, s.MatrixBase) else [expression]
    residuals = [s.simplify(v) for v in entries]
    assert all(v == 0 for v in residuals), (name, residuals)
    records.append(name)


def require_equal(actual, expected):
    difference = actual - expected
    entries = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
    residuals = [s.simplify(v) for v in entries]
    if any(v != 0 for v in residuals):
        raise AssertionError(str(residuals))


def require_positive(value):
    if not value > 0:
        raise AssertionError(str(value))


def require_rank_one(matrix):
    rank = matrix.rank()
    if rank != 1:
        raise AssertionError('rank=' + str(rank))


def catch(name, action):
    try:
        action()
    except AssertionError as failure:
        red.append({'name': name, 'actual_rejection': str(failure)})
    else:
        raise AssertionError('false pass: ' + name)


def geometry(metric):
    inverse = metric.inv()
    connection = [[[s.simplify(sum(
        inverse[a, d] * (s.diff(metric[d, b], coords[c])
                        + s.diff(metric[d, c], coords[b])
                        - s.diff(metric[b, c], coords[d]))
        for d in range(N)) / 2)
        for c in range(N)] for b in range(N)] for a in range(N)]
    ricci = s.zeros(N)
    for b in range(N):
        for d in range(N):
            ricci[b, d] = s.simplify(sum(
                s.diff(connection[a][b][d], coords[a])
                - s.diff(connection[a][b][a], coords[d])
                + sum(connection[a][a][c] * connection[c][b][d]
                      - connection[a][d][c] * connection[c][b][a]
                      for c in range(N))
                for a in range(N)))
    scalar = s.simplify(s.trace(inverse * ricci))
    return inverse, connection, ricci, scalar, s.simplify(ricci - scalar * metric / 4)


def divergence(vector, connection):
    return s.simplify(sum(s.diff(vector[a], coords[a])
        + sum(connection[a][a][b] * vector[b] for b in range(N))
        for a in range(N)))


def tensor_divergence(tensor, inverse, connection):
    return s.Matrix([s.simplify(sum(inverse[a, c] * (
        s.diff(tensor[a, b], coords[c])
        - sum(connection[d][c][a] * tensor[d, b]
              + connection[d][c][b] * tensor[a, d] for d in range(N)))
        for a in range(N) for c in range(N))) for b in range(N)])


def wedge_da(oneform):
    exterior = [[s.diff(oneform[j], coords[i]) - s.diff(oneform[i], coords[j])
                 for j in range(N)] for i in range(N)]
    return {(i, j, k): s.simplify(oneform[i] * exterior[j][k]
             - oneform[j] * exterior[i][k] + oneform[k] * exterior[i][j])
            for i in range(N) for j in range(i + 1, N)
            for k in range(j + 1, N)}


# First actual metric: nonzero null Ricci, both coefficient signs.
q = s.Matrix([1, 0, 0, 0])
wave_data = []
for sign in (1, -1):
    H = -sign * (2 + u**2) * (x**2 + y**2)
    metric = s.Matrix([[H, 1, 0, 0], [1, 0, 0, 0],
                       [0, 0, 1, 0], [0, 0, 0, 1]])
    inverse, connection, ricci, scalar, tracefree = geometry(metric)
    beta = s.Integer(3 * sign)  # FREE optional comparison coefficient.
    density = 2 * (2 + u**2) / 3
    ell = inverse * q
    current = density * ell
    zero('wave scalar sign' + str(sign), scalar)
    zero('wave full Ricci sign' + str(sign),
         ricci - 2 * sign * (2 + u**2) * q * q.T)
    zero('wave full source equality sign' + str(sign),
         tracefree - beta * density * q * q.T)
    zero('wave exact null phase sign' + str(sign), (q.T * ell)[0])
    zero('wave conserved current sign' + str(sign), divergence(current, connection))
    zero('wave direct Bianchi sign' + str(sign),
         tensor_divergence(tracefree, inverse, connection))
    observer = s.Matrix([-1, (H + 1) / 2, 0, 0])
    zero('wave observer norm sign' + str(sign), (observer.T * metric * observer)[0] + 1)
    zero('wave future observer readout sign' + str(sign),
         -(observer.T * metric * current)[0] - density)
    B = tracefree / beta
    observed_B = (observer.T * B * observer)[0]
    root = -B * observer / s.sqrt(observed_B)
    zero('wave canonical future root square sign' + str(sign), root * root.T - B)
    zero('wave canonical root future sign' + str(sign),
         (root.T * observer)[0] + s.sqrt(density))

    # Non-affine increasing F(u)=u+u^3. It changes current, keeps full S.
    phase_derivative = 1 + 3 * u**2
    new_q = phase_derivative * q
    new_density = density / phase_derivative**2
    new_current = new_density * inverse * new_q
    zero('nonlinear rephase full source sign' + str(sign),
         tracefree - beta * new_density * new_q * new_q.T)
    zero('nonlinear rephase conserved sign' + str(sign), divergence(new_current, connection))
    zero('nonlinear rephase current scaling sign' + str(sign),
         new_current - current / phase_derivative)
    wave_data.append({'sign': sign, 'Ric_uu': str(ricci[0, 0]),
                      'R': str(scalar), 'div_j': str(divergence(current, connection)),
                      'new_j_r_at_u1': str(new_current[1].subs(u, 1)),
                      'old_j_r_at_u1': str(current[1].subs(u, 1))})
    if sign == 1:
        catch('wrong phase-density exponent', lambda: require_equal(
            (beta * (density / phase_derivative) * new_q * new_q.T).subs(u, 1),
            tracefree.subs(u, 1)))
        catch('source coefficient sign reversed', lambda: require_equal(
            (-beta * density * q * q.T).subs(u, 1), tracefree.subs(u, 1)))
        catch('wrong beta positivity', lambda: require_positive(-observed_B.subs(u, 1)))
        catch('nonlinear rephase falsely called unchanged current', lambda: require_equal(
            new_current.subs(u, 1), current.subs(u, 1)))

# Second actual metric: factorization/Frobenius survive but conservation fails.
H = u * r**2 / 3
metric = s.Matrix([[H, 1, 0, 0], [1, 0, 0, 0],
                   [0, 0, r**2, 0], [0, 0, 0, r**2]])
inverse, connection, ricci, scalar, tracefree = geometry(metric)
beta = s.Integer(3)  # FREE, on the diagnostic region r>0.
density = r / 9
current = density * inverse * q
actual_div = divergence(current, connection)
zero('warped metric determinant', metric.det() + r**4)
zero('warped full Ricci', ricci - u * metric - r * q * q.T / 3)
zero('warped scalar variable', scalar - 4 * u)
zero('warped full null rank-one S', tracefree - beta * density * q * q.T)
zero('warped actual divergence', actual_div - s.Rational(1, 3))
gradient_scalar = s.Matrix([s.diff(scalar, c) for c in coords])
zero('warped direct contracted Bianchi',
     tensor_divergence(tracefree, inverse, connection) - gradient_scalar / 4)
zero('warped Bianchi current coefficient', beta * actual_div * q - gradient_scalar / 4)
catch('factorization alone falsely passes conservation', lambda: require_equal(actual_div, 0))

# Pointwise algebraic diagnostic, NOT a metric-Ricci realization claim.
flat = s.Matrix([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
m = s.Matrix([0, 0, 1, 0])
ranktwo = q * m.T + m * q.T
endomorphism = flat.inv() * ranktwo
zero('rank-two trace invariants all vanish', s.Matrix([
    s.trace(endomorphism**power) for power in range(1, 5)]))
zero('rank-two nilpotent cube', endomorphism**3)
zero('rank-two square explicit nonzero',
     endomorphism**2 - s.Matrix([[0, 0, 0, 0], [1, 0, 0, 0],
                               [0, 0, 0, 0], [0, 0, 0, 0]]))
catch('scalar invariants falsely substituted for rank-one tensor',
      lambda: require_rank_one(ranktwo))

# Supplied nonintegrable null-current diagnostic on an actual metric.
# This q is NOT asserted to factor that metric's trace-free Ricci.
twisting_q = s.Matrix([1, 0, 0, x])
twisting_metric = s.Matrix([[0, 1, 0, 0], [1, 0, 0, x],
                            [0, 0, 1, 0], [0, x, 0, 1]])
twisting_inverse, twisting_connection, twisting_ricci, twisting_R, twisting_S = geometry(twisting_metric)
twisting_current = twisting_inverse * twisting_q
zero('supplied twisting current null', (twisting_q.T * twisting_current)[0])
zero('supplied twisting current conserved', divergence(twisting_current, twisting_connection))
frob = wedge_da(twisting_q)
zero('twisting Frobenius explicit component', frob[(0, 2, 3)] - 1)
catch('conservation/nullness falsely implies phase integrability',
      lambda: require_equal(s.Matrix(list(frob.values())), s.zeros(4, 1)))

print(json.dumps({
    'status': 'PASS', 'python': platform.python_version(), 'sympy': s.__version__,
    'exact_diagnostic_groups': len(records), 'checks': records,
    'actual_red_controls': red, 'wave_metrics': wave_data,
    'warped_actual_metric': {'Ric': str(ricci), 'R': str(scalar),
                            'S': str(tracefree), 'div_j': str(actual_div)},
    'algebraic_only': {'rank': ranktwo.rank(),
                       'trace_powers': [str(s.trace(endomorphism**p)) for p in range(1, 5)]},
    'supplied_twisting_current_not_Ricci_factorization': {
        'q_wedge_dq': {str(k): str(v) for k, v in frob.items()},
        'actual_Ricci': str(twisting_ricci), 'actual_R': str(twisting_R),
        'actual_tracefree_Ricci': str(twisting_S)},
    'scope': 'Exact diagnostics, not proof or physical source adoption.'
}, indent=2, sort_keys=True))
