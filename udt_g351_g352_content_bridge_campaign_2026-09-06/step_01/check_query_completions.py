"""Exact finite eligibility/non-selection controls; no physical identification.

This applies the reviewed conditional phase/current only on its admitted metric
branch. It does not verify source ownership by token matching and does not prove
these query completions are fully coupled UDT physical solutions. No file writes.
"""
import sys
sys.dont_write_bytecode = True
import argparse
import json
from pathlib import Path
import platform
import sympy as S

ap = argparse.ArgumentParser()
ap.add_argument('--mutation', choices=['erase_weight','phase_blind','observer_weighted_mu',
    'gauge_rebuild_mu','coordinate_area_identity'])
mutation = ap.parse_args().mutation
if not __debug__: raise RuntimeError('Assertions require ordinary Python')
inputs = json.loads((Path(__file__).parent/'WITNESS_INPUTS.json').read_text())
theta,r,lam,nu = S.symbols('theta r lambda nu',real=True)
coords = [theta,r,lam,nu]
L,Delta = map(S.Rational,[inputs['screen_length_L'],inputs['phase_spacing']])
A = S.Rational(inputs['metric_branch_A'])
K = S.sign(A)*L**2*(lam**2-nu**2)/2
g = S.Matrix([[K,1,0,0],[1,0,0,0],[0,0,L**2,0],[0,0,0,L**2]])
gi = g.inv()
beta = S.Matrix([1,0,0,0]); C0 = gi*beta
volume = S.sqrt(-g.det())
checks=[]
def eq(name,a,b=0):
    assert S.simplify(a-b)==0,name
    checks.append(name)
def div(C):
    return S.simplify(sum(S.diff(volume*C[i],coords[i]) for i in range(4))/volume)
def phase_derivative(f):
    return S.Integer(0) if mutation=='phase_blind' else S.diff(f,theta)
def U(omega):
    return S.Matrix([-omega,(1+K*omega**2)/(2*omega),0,0])
qx,qy = map(S.Rational,inputs['cut_graph_gradient'])
E = S.Matrix([[0,0],[qx,qy],[1,0],[0,1]])
Jactual = S.sqrt((E.T*g*E).det())
J = S.Integer(1) if mutation=='coordinate_area_identity' else Jactual
eq('metric_determinant',g.det(),-L**4)
eq('full_null_gradient',(beta.T*gi*beta)[0])
eq('intrinsic_metric_cut_area',J,L**2)
eq('base_current_conservation',div(C0))
bad = 1+theta**2
eq('phase_dependent_control_still_conserved',div(bad*C0))
eq('phase_dependence_detected',phase_derivative(bad),2*theta)
eq('generator_dependent_control_not_conserved',div((1+r)*C0),1)
point = {lam:S.Rational(inputs['label_point'][0]),nu:S.Rational(inputs['label_point'][1])}
frequencies = list(map(S.Rational,inputs['observer_frequencies']))
gauge = S.Rational(inputs['phase_gauge_factor'])
rows=[]
for index,expression in enumerate(inputs['weights']):
    # lambda is a Python keyword; the parser-only alias denotes the same symbol.
    f = S.sympify(expression.replace('^','**').replace('lambda','ell'),locals={'ell':lam})
    assert f.is_nonnegative is True
    checks.append(f'nonnegative_weight_{index}')
    computed = S.Integer(1) if mutation=='erase_weight' else f
    density = Delta*L**2*computed
    total = S.integrate(density,(lam,0,1),(nu,0,1))
    eq(f'total_amount_{index}',total,S.Rational(inputs['expected_total_amounts'][index]))
    eq(f'phase_independent_{index}',phase_derivative(computed))
    Cf = computed*C0
    eq(f'conserved_current_{index}',div(Cf))
    rates=[];densities=[]
    for w in frequencies:
        obs=U(w)
        eq(f'unit_observer_{index}_{w}',(obs.T*g*obs)[0],-1)
        omega = -(beta.T*obs)[0]
        actual_density=density*(w/frequencies[0])**2 if mutation=='observer_weighted_mu' else density
        rate = S.simplify(omega/Delta*actual_density/J)
        eq(f'current_readout_match_{index}_{w}',rate,-(obs.T*g*Cf)[0])
        densities.append(actual_density);rates.append(rate)
        new_density = gauge*actual_density if mutation=='gauge_rebuild_mu' else actual_density
        eq(f'fixed_measure_gauge_{index}_{w}',gauge*omega/(gauge*Delta)*new_density/J,rate)
    eq(f'observer_neutral_measure_{index}',densities[0],densities[1])
    eq(f'division_free_rate_transfer_{index}',rates[1],frequencies[1]/frequencies[0]*rates[0])
    ratio = None if f==0 else S.simplify(rates[1]/rates[0])
    if ratio is not None: eq(f'nonzero_rate_ratio_{index}',ratio,frequencies[1]/frequencies[0])
    rows.append(dict(weight=str(f),amount=str(total),rates_at_label_point=[str(q.subs(point)) for q in rates],
        transfer_ratio=None if ratio is None else str(ratio),zero_ratio_not_formed=f==0))
# A conserved aligned current need not itself be the fixed phase gradient.
eq('nonconstant_current_dual_not_closed',S.diff((1+lam**2)*beta[0],lam),2*lam)
assert rows[0]['amount']!=rows[1]['amount'] and rows[0]['rates_at_label_point']!=rows[1]['rates_at_label_point']
checks.append('two_nonzero_inequivalent_same_query_completions')
print(json.dumps(dict(kind='exact bounded query-completion evidence, not physical solutions or source-selection proof',
    python=platform.python_version(),sympy=S.__version__,mutation=mutation,checks=checks,
    guard_groups_passed=len(checks),metric_shape=[4,4],cut_area=str(Jactual),weights=rows,
    phase_dependent_divergence=str(div(bad*C0)),phase_dependent_product_defect=str(S.diff(bad,theta))),indent=2))
