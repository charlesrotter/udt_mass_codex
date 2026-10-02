"""Exposed finite exact Lagrange inversion of saved a(t); no solver/parent helpers."""
import hashlib
import json
import platform
from pathlib import Path
import sympy as s

out=Path(__file__).resolve().parent
source=Path('udt_environment_response_candidates_2026-10-01/CUBIC_RECOMPUTATION.json')
saved=json.loads(source.read_text())
t=s.symbols('t')
degree=7

def log_clock(a):
    inv=s.series(1/a,t,0,degree+1).removeO()
    eta=s.integrate(inv,t)
    inverse_ratio=s.series(t/eta,t,0,degree+1).removeO()
    log_derivative=s.series(s.diff(a,t)/a,t,0,degree).removeO()
    result=[s.Integer(0)]
    for n in range(1,degree+1):
        expression=s.series(log_derivative*inverse_ratio**n,t,0,n).removeO()
        result.append(s.expand(expression).coeff(t,n-1)/n)
    return result

a=sum(s.Rational(x)*t**n for n,x in enumerate(saved['a_coefficients'][:degree+1]))
logp=log_clock(a)
logq=[(2**n-1)*v for n,v in enumerate(logp)]
assert logp==[s.Rational(x) for x in saved['logp_coefficients'][:degree+1]]
assert logq==[s.Rational(x) for x in saved['logq_coefficients'][:degree+1]]
alpha=-logp[3]/(120*logp[5])
assert alpha==1 and logp[4]==0
control=log_clock(1+logp[3]*t**3)
assert control[3]==logp[3] and control[5]==0
constraint_defect=27*control[3]**2
shape_defect=6*control[3]
assert constraint_defect==s.Rational(3,160000)
assert shape_defect==s.Rational(1,200)
record={
    'status':'PASS','source':str(source),
    'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'method':'Lagrange inversion after independent conformal-time integration; no parent recurrence/helpers',
    'degree':degree,'logp':[str(x) for x in logp],
    'logq':[str(x) for x in logq],
    'cubic':str(logp[3]),'quintic':str(logp[5]),'inferred_alpha':str(alpha),
    'cubic_control':{'logp':[str(x) for x in control],
        'original00_L4':str(constraint_defect),'shape_L1':str(shape_defect)},
    'python':platform.python_version(),'sympy':s.__version__,
    'scope':'Exact finite saved-artifact recomputation; exposed; no evolution, observation, finite-interval error bound or physical admission'
}
with (out/'LAGRANGE_RESULT.json').open('x') as f:
    json.dump(record,f,indent=2);f.write('\n')
print(json.dumps(record,indent=2))
