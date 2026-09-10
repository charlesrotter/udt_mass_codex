#!/usr/bin/env python3
"""Exact construction checks; no repository scientific implementation imports.

FREE: diagnostic profiles and rational constants below are mathematical witnesses,
not selected physics. Supplied signature/chart/class come from WORK_ORDER.md.
"""
import json
import platform
import sympy as sp

checks = []


def zero(name, expr):
    if isinstance(expr, sp.MatrixBase):
        residuals = [sp.simplify(x) for x in expr]
    else:
        residuals = [sp.simplify(expr)]
    passed = all(x == 0 for x in residuals)
    checks.append({"name": name, "passed": passed,
                   "residuals": [str(x) for x in residuals]})
    if not passed:
        raise AssertionError((name, residuals))


def truth(name, condition, evidence):
    passed = bool(condition)
    checks.append({"name": name, "passed": passed, "evidence": evidence})
    if not passed:
        raise AssertionError((name, evidence))


def gram(N, beta, gamma):
    # Coordinate components built from the supplied full metric definition.
    g = sp.zeros(4)
    covclock = sp.Matrix([1, *beta])
    g -= N**2 * covclock * covclock.T
    g[1:, 1:] += gamma
    return g


def recover(T, records):
    # Input contains only T plus six m,B records, not a metric or beta/gamma.
    q = [sp.simplify(m**2 / T**2) for m, B in records]
    beta = sp.Matrix([sp.simplify(records[i][0] * records[i][1]) for i in range(3)])
    gamma = sp.diag(*q[:3])
    for k, (i, j) in enumerate(((0, 1), (0, 2), (1, 2)), 3):
        gamma[i, j] = gamma[j, i] = sp.simplify((q[k] - q[i] - q[j]) / 2)
    return beta, gamma


def main():
    t, x, y, z, sigma = sp.symbols('t x y z sigma', real=True)
    variables = (t, x, y, z)
    b, r, s = sp.symbols('b r s', real=True)
    # FREE smooth coupled profiles, globally positive lapse and conformal factor.
    N = sp.exp(t+y)
    A = sp.exp(t+x*x)
    G0 = sp.Matrix([[2, 1, 1], [1, 3, 1], [1, 1, 2]])
    gamma = A**2 * G0
    beta = sp.Matrix([r, b*x+s*t, 0])
    directions = [sp.Matrix(v) for v in
                  ((1, 0, 0), (0, 1, 0), (0, 0, 1),
                   (1, 1, 0), (1, 0, 1), (0, 1, 1))]
    g = gram(N, beta, gamma)
    truth('G0_positive_definite_Sylvester',
          all(G0[:k, :k].det() > 0 for k in (1, 2, 3)),
          [str(G0[:k, :k].det()) for k in (1, 2, 3)])
    U = sp.Matrix([1/N, 0, 0, 0])
    zero('unit_observer', (U.T*g*U)[0]+1)
    records = []
    a1, a2, a3 = sp.symbols('a1 a2 a3', real=True)
    for k, v in enumerate(directions):
        F = sp.Matrix([t, a1+sigma*v[0], a2+sigma*v[1], a3+sigma*v[2]])
        J = F.jacobian([t, sigma])
        truth(f'actual_immersion_rank_{k}', J.rank() == 2, str(J))
        zero(f'actual_surface_mixed_partials_{k}',
             F.diff(t).diff(sigma)-F.diff(sigma).diff(t))
        h = J.T*g*J
        q = (v.T*gamma*v)[0]
        bv = (beta.T*v)[0]
        m = N*A*sp.sqrt((v.T*G0*v)[0])
        B = bv/m
        records.append((m, B))
        zero(f'raw_pullback_{k}', h-sp.Matrix([[-N**2, -N**2*bv],
                                            [-N**2*bv, q-N**2*bv**2]]))
        zero(f'density_determinant_{k}', h.det()+m**2)
        C = sp.diag(1, 1/m)
        hs = C.T*h*C
        zero(f'normalized_germ_{k}', hs-sp.Matrix([[-N**2, -N**2*B],
                                                 [-N**2*B, 1/N**2-N**2*B**2]]))
        zero(f'normalized_determinant_{k}', hs.det()+1)
    beta_r, gamma_r = recover(N, records)
    zero('recovered_beta', beta_r-beta)
    zero('recovered_gamma', gamma_r-gamma)
    for k, (i, j) in enumerate(((0, 1), (0, 2), (1, 2)), 3):
        zero(f'shift_sum_coherence_{k}', records[k][0]*records[k][1]-beta_r[i]-beta_r[j])
    g_r = gram(N, beta_r, gamma_r)
    zero('reconstructed_metric', g_r-g)
    for var in variables:
        zero(f'reconstructed_first_jet_{var}', g_r.diff(var)-g.diff(var))

    # Omission controls show explicit ambiguity/rejection, not global minimality.
    qD = lambda M: [(v.T*M*v)[0] for v in directions]
    I = sp.eye(3)
    lambda_value = sp.Integer(2)  # FREE exact counterexample value.
    zero_beta = sp.zeros(3, 1)
    flat_g1 = gram(sp.Integer(1), zero_beta, I)
    flat_g2 = gram(sp.Integer(1), zero_beta, lambda_value**2*I)
    for k, v in enumerate(directions):
        J = sp.zeros(4, 2)
        J[0, 0] = 1
        J[1:, 1] = v
        h1, h2 = J.T*flat_g1*J, J.T*flat_g2*J
        C1 = sp.diag(1, 1/sp.sqrt(-h1.det()))
        C2 = sp.diag(1, 1/sp.sqrt(-h2.det()))
        zero(f'omit_density_identical_normalized_metric_{k}', C1.T*h1*C1-C2.T*h2*C2)
    truth('omit_density_different_metric_and_density', lambda_value**2 != 1,
          {'gamma_ratio': str(lambda_value**2), 'density_ratio': str(lambda_value)})
    cross = sp.Matrix([[1, sp.Rational(1, 3), 0], [sp.Rational(1, 3), 1, 0], [0, 0, 1]])
    zero('omit_mixed_directions_same_axial_q', sp.Matrix(qD(cross)[:3])-sp.Matrix(qD(I)[:3]))
    truth('omit_mixed_directions_distinct_SPD', cross != I and cross.det() > 0,
          {'cross12': str(cross[0, 1]), 'det': str(cross.det())})
    bad = sp.Matrix([[1, 2, 0], [2, 1, 0], [0, 0, 1]])
    truth('directional_positivity_not_SPD', all(q > 0 for q in qD(bad)) and
          (sp.Matrix([1, -1, 0]).T*bad*sp.Matrix([1, -1, 0]))[0] < 0,
          {'six_q': [str(q) for q in qD(bad)], 'negative_test': '-2'})
    mutated = list(records)
    mutated[3] = (records[3][0], records[3][1]+1/records[3][0])
    failure = sp.simplify(mutated[3][0]*mutated[3][1]-beta_r[0]-beta_r[1])
    truth('incoherent_sum_shift_rejected', failure != 0, str(failure))

    N_variable = sp.exp(x)
    unit_lapse_g = gram(N_variable, sp.zeros(3, 1), I)
    unit_U = sp.Matrix([1/N_variable, 0, 0, 0])
    zero('unit_tangent_has_T_one', (unit_U.T*unit_lapse_g*unit_U)[0]+1)
    bracket_component = -sp.diff(1/N_variable, x)
    truth('unit_U_and_coordinate_spatial_field_noncommute', bracket_component != 0,
          str(bracket_component))

    # Actual spacetime tape chart, independently transformed by its Jacobian.
    S = sp.symbols('S', real=True)
    old_coordinates = sp.Matrix([t, sp.exp(-t)*S])
    tape_J = old_coordinates.jacobian([t, S])
    h_raw = sp.diag(-1, sp.exp(2*t))
    h_tape = sp.simplify(tape_J.T*h_raw*tape_J)
    zero('actual_tape_coordinate_pullback', h_tape-sp.Matrix([[S**2-1, -S], [-S, 1]]))
    zero('actual_tape_coordinate_determinant', h_tape.det()+1)
    truth('actual_tape_clock_changed', h_tape[0, 0] != -1,
          'T_fixed_S^2=1-S^2, regular clock only |S|<1; original T=1')
    original_clock_new_components = sp.Matrix([1, S])
    zero('original_clock_still_has_T_one',
         (original_clock_new_components.T*h_tape*original_clock_new_components)[0]+1)
    zero('tape_differential_has_time_term', sp.diff(sp.exp(t)*sigma, t)-sp.exp(t)*sigma)
    truth('density_normalized_fields_noncommute', -sp.exp(-t) != 0,
          '[partial_t,exp(-t)partial_sigma]=-exp(-t)partial_sigma')

    return {'status': 'PASS', 'evidence_type': 'exact symbolic construction regression',
            'review_status': 'fresh separate-context review pending',
            'runtime_model_version': 'UNATTESTED', 'python': platform.python_version(),
            'sympy': sp.__version__, 'directions': [list(map(str, v)) for v in directions],
            'shapes': {'metric': [4, 4], 'pair_J': [4, 2], 'pair_h': [2, 2],
                       'record_count': 6, 'coordinate_first_jet_count': 4},
            'parameters': {'N': str(N), 'A': str(A), 'beta': list(map(str, beta)),
                           'G0': str(G0), 'domain': 'R^4; positive exponential N,A'},
            'check_count': len(checks), 'checks': checks}


if __name__ == '__main__':
    try:
        result = main()
    except Exception as error:
        print(json.dumps({'status': 'FAIL', 'error': repr(error), 'checks': checks}, indent=2))
        raise
    print(json.dumps(result, indent=2))
