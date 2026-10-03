"""Exact two-family clock-incidence control; independently authored for CPW1."""
import json
import platform
import sympy as sp

L = sp.symbols('L', positive=True)
t, b = sp.symbols('t b', real=True)
checks = []

def zero(name, expr):
    value = sp.simplify(expr)
    assert value == 0, (name, str(value))
    checks.append(name)

records = []
for label, x, arrival in [
    ('static', sp.S(0), 2*L),
    ('accelerated', t*t/(8*L), 4*L*(sp.sqrt(2)-1)),
]:
    velocity = sp.diff(x, t)
    proper_rate = sp.sqrt(1-velocity**2)
    outgoing_b = t+L-x
    p = sp.simplify((sp.diff(outgoing_b,t)/proper_rate).subs(t,0))
    # Return incidence is t+x(t)-L-b=0; differentiate implicitly.
    return_incidence = t+x-L-b
    dt_db = -sp.diff(return_incidence,b)/sp.diff(return_incidence,t)
    q_chain = sp.simplify((proper_rate*dt_db).subs(t,arrival))
    v_arrival = sp.simplify(velocity.subs(t,arrival))
    # Returning affine tangent k=(1,-1), B unit clock=(1,0).
    # Frequency at A is gamma_A*(1+v_A), with eta=(-,+).
    omega_A = sp.simplify((1+velocity)/proper_rate)
    q_frequency = sp.simplify((1/omega_A).subs(t,arrival))
    zero(label+'_first_reception', outgoing_b.subs(t,0)-L)
    zero(label+'_outgoing_ratio', p-1)
    zero(label+'_return_incidence', return_incidence.subs({t:arrival,b:L}))
    zero(label+'_independent_frequency', q_chain-q_frequency)
    zero(label+'_proper_clock_norm', (-1+velocity**2)/proper_rate**2+1)
    assert sp.simplify(arrival/L-1).is_positive
    checks.append(label+'_future_after_relay')
    assert sp.simplify(1-v_arrival**2).is_positive
    checks.append(label+'_timelike_at_reception')
    records.append(dict(family=label, x=str(x), arrival_over_L=str(arrival/L),
                        p=str(p), q=str(q_chain), v_return=str(v_arrival)))

qa = sp.sqrt(sp.sqrt(2)-1)
zero('accelerated_return_value_squared',
     sp.sympify(records[1]['q'])**2-qa**2)
assert sp.sympify(records[1]['q']).is_positive
checks.append('accelerated_return_positive')
assert sp.simplify(1-qa).is_positive
checks.append('same_outgoing_unequal_return')
assert len(checks) <= 30
print(json.dumps(dict(status='PASS', python=platform.python_version(),
                     sympy=sp.__version__, families=2, cases=2,
                     scalar_assertions=len(checks), checks=checks, records=records,
                     scope='Supplied flat accelerated-clock control; outside ESR PSW free-clock scope',
                     sampling='exact symbolic, no finite-sampling universal inference'), indent=2))
