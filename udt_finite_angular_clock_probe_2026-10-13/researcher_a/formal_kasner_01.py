"""Original-coordinate axial Bianchi-I clock series; exploratory author code.

The bookkeeping ring truncates L at degree 4. Direction z=n_1^2 remains
symbolic. Null incidence is solved as a vector equation, not along a frozen
radial sheet. Reverse emission is at B0, not the later relay.
"""
import hashlib
import json
from pathlib import Path
import platform
import sys
import time

import sympy as s

N = 4
z, w = s.symbols('z w')
q = [z, 1-z]


def series(value=0):
    return [s.sympify(value)] + [s.S.Zero]*N


def add(a, b):
    return [s.expand(a[i]+b[i]) for i in range(N+1)]


def neg(a):
    return [-v for v in a]


def sub(a, b):
    return add(a, neg(b))


def scale(a, c):
    return [s.expand(c*v) for v in a]


def mul(a, b):
    return [s.expand(sum(a[j]*b[i-j] for j in range(i+1))) for i in range(N+1)]


def shift(a, k):
    return [s.S.Zero]*k+a[:N+1-k]


def power(a, p):
    assert a[0] == 1, a[0]
    delta = sub(a, series(1))
    out, term = series(1), series(1)
    for j in range(1, N+1):
        term = mul(term, delta)
        out = add(out, scale(term, s.binomial(p, j)))
    return out


def integer_power(a, p):
    out = series(1)
    for _ in range(p):
        out = mul(out, a)
    return out


def log_series(a):
    assert a[0] == 1, a[0]
    delta, term, out = sub(a, series(1)), series(1), series()
    for j in range(1, N+1):
        term = mul(term, delta)
        out = add(out, scale(term, s.Rational((-1)**(j+1), j)))
    return out


def substitute_w(a, endpoint):
    out = series()
    cache = {j: integer_power(endpoint, j) for j in range(N+2)}
    for k, coefficient in enumerate(a):
        for (j,), value in s.Poly(coefficient, w).terms():
            out = add(out, shift(scale(cache[j], value), k))
    return out


def integral(a, lower, upper):
    antiderivative = [s.integrate(v, w) for v in a]
    return sub(substitute_w(antiderivative, upper), substitute_w(antiderivative, lower))


def substitute(a, mapping):
    return [s.expand(v.subs(mapping)) for v in a]


def eqzero(value, label):
    assert s.expand(value) == 0, (label, s.factor(value))


def prepare(r):
    R = sum(q[i]*r[i] for i in range(2))
    R2 = sum(q[i]*r[i]**2 for i in range(2))
    S = sum(q[i]*r[i]*(2*r[i]+1) for i in range(2))
    t2, t4 = -R/2, -R*S/24
    T = [s.S.One, s.S.Zero, s.expand(t2), s.S.Zero, s.expand(t4)]
    C = []
    X_over_L = []
    for ri in r:
        c3 = ri*(t2*(1-2*ri)-R2/2)/3
        C.append([s.S.Zero, -ri, s.S.Zero, s.expand(c3), s.S.Zero])
        x3 = -2*ri*t2/3
        x5 = (-2*ri*t4+ri*(2*ri+1)*t2**2)/5
        X_over_L.append([s.S.One, s.S.Zero, s.expand(x3), s.S.Zero, s.expand(x5)])
    V0_sq = series(1)
    for i in range(2):
        V0_sq = add(V0_sq, scale(mul(mul(C[i], C[i]), power(T, -2*r[i])), q[i]))
    Ut = power(V0_sq, s.Rational(1, 2))
    # Check the independently written original preparation equations through
    # the orders supported by retained coefficients.
    for i in range(2):
        eqzero(3*C[i][3]-r[i]*(2*t2*C[i][1]-(Ut[2]-t2)), 'parallel_C_L2')
    eqzero(2*Ut[2]+sum(r[i]*q[i]*C[i][1] for i in range(2)), 'parallel_U_L1')
    eqzero(4*Ut[4]+sum(r[i]*q[i]*(C[i][3]-(2*r[i]+1)*t2*C[i][1]) for i in range(2)), 'parallel_U_L3')
    eqzero(12*t4-S*t2, 'preparation_t_L2')
    return T, C, X_over_L, Ut


def metric_t(r, t):
    return [power(t, -2*ri) for ri in r]


def frequency(r, K, t):
    terms = metric_t(r, t)
    W2 = series()
    for i in range(2):
        W2 = add(W2, scale(mul(mul(K[i], K[i]), terms[i]), q[i]))
    return power(W2, s.Rational(1, 2))


def solve_branch(r, kind):
    T, C, X_over_L, Ut = prepare(r)
    tvar = [s.S.One, w, s.S.Zero, s.S.Zero, s.S.Zero]
    M = metric_t(r, tvar)
    V2 = series(1)
    for i in range(2):
        V2 = add(V2, scale(mul(mul(C[i], C[i]), M[i]), q[i]))
    V_inv = power(V2, s.Rational(-1, 2))
    endpoint = series(1)  # (t_arrival - 1)/L
    rho = series(1)
    lower = T[1:]+[s.S.Zero]

    def residuals(ep, angle):
        K = [series(1), angle]
        W_inv = power(frequency(r, K, tvar), -1)
        residual = []
        for i in range(2):
            ray = mul(mul(K[i], M[i]), W_inv)
            if kind == 'forward':
                motion = mul(mul(C[i], M[i]), V_inv)
                lhs = add(X_over_L[i], integral(motion, lower, ep))
                rhs = integral(ray, series(), ep)
            else:
                lhs = X_over_L[i]
                rhs = integral(ray, lower, ep)
            residual.append(sub(lhs, rhs))
        return residual

    for order in range(1, 4):
        a, b = s.symbols(f'a{order} b{order}')
        ep = endpoint.copy(); ep[order] = a
        angle = rho.copy(); angle[order] = b
        residual = residuals(ep, angle)
        solution = s.solve([residual[i][order] for i in range(2)], (a,b), dict=True)
        assert len(solution) == 1, solution
        endpoint[order] = s.factor(solution[0][a])
        rho[order] = s.factor(solution[0][b])
        print(kind, 'incidence order', order, 'time', endpoint[order], 'direction', rho[order], flush=True)
    # An arbitrary fourth-order ray direction cannot alter this L^4 ratio.
    rho[4] = s.Symbol('unneeded_direction4')
    K = [series(1), rho]
    arrival = add(series(1), shift(endpoint, 1))
    W_arr = frequency(r, K, arrival)
    W_initial = frequency(r, K, T if kind == 'reverse' else series(1))
    if kind == 'forward':
        V_arr2 = series(1)
        M_arr = metric_t(r, arrival)
        contraction = series()
        for i in range(2):
            V_arr2 = add(V_arr2, scale(mul(mul(C[i],C[i]),M_arr[i]),q[i]))
            contraction = add(contraction, scale(mul(mul(K[i],C[i]),M_arr[i]),q[i]))
        denominator = sub(mul(W_arr, power(V_arr2,s.Rational(1,2))),contraction)
        logp = sub(log_series(W_initial),log_series(denominator))
    else:
        numerator = mul(W_initial, Ut)
        M_initial = metric_t(r,T)
        for i in range(2):
            numerator = add(numerator,scale(mul(mul(K[i],C[i]),M_initial[i]),q[i]))
        logp = sub(log_series(numerator),log_series(W_arr))
    logp = [s.factor(v) for v in logp]
    assert not any(v.has(rho[4]) for v in logp)
    residual = residuals(endpoint, substitute(rho,{rho[4]:0}))
    for i in range(2):
        for j in range(4):
            eqzero(residual[i][j],f'{kind}_incidence_{i}_{j}')
    moments = []
    for v in logp:
        moment = sum(c/s.Integer(2*j+1) for (j,), c in s.Poly(v,z).terms())
        moments.append(s.factor(moment))
    print(kind,'log ratio',logp,'spherical moments',moments,flush=True)
    return {'log_ratio':[str(v) for v in logp], 'spherical_mean':[str(v) for v in moments],
            'arrival_minus_one_over_L':[str(v) for v in endpoint],
            'ray_covector_ratio':[str(v) for v in rho],
            'log_axis1':[str(s.factor(v.subs(z,1))) for v in logp],
            'log_axis2':[str(s.factor(v.subs(z,0))) for v in logp]}


def main():
    start = time.monotonic()
    r = [s.Rational(-1,3),s.Rational(2,3)]
    result = {'metric':'-dt^2+t^(-2/3)dx^2+t^(4/3)(dy^2+dz^2)',
              'event_t':1,'central_U':'partial_t','angular_variable':'z=n1^2',
              'status':'exploratory exact formal series; argument and review still needed',
              'python':platform.python_version(),'sympy':s.__version__,
              'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    for branch in ['forward','reverse']:
        result[branch]=solve_branch(r,branch)
    result['duration_seconds']=time.monotonic()-start
    dest=Path(__file__).with_name('formal_kasner_01_result.json')
    with dest.open('x') as f:
        json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':
    main()
