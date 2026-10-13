"""Exact SR adverse control for an unadopted universal projective-clock proposal."""
import json
import platform
import sympy as s

t = s.symbols('tau', real=True)
b = s.symbols('b', positive=True)
gamma = s.symbols('gamma', positive=True)
# Physical domain gamma>1; gamma**2-1=gamma**2*v**2.
f = gamma*t + s.sqrt(b*b + (gamma*gamma-1)*t*t)
null_residual = s.simplify(-(gamma*f-t)**2+b*b+(gamma*gamma-1)*f*f)
normalization = s.simplify(-gamma**2+(gamma**2-1))
jets = [s.simplify(s.diff(f,t,j).subs(t,0)) for j in range(1,4)]
schwarzian = s.simplify(jets[2]/jets[0]-s.Rational(3,2)*(jets[1]/jets[0])**2)
target = -3*(gamma**2-1)**2/(2*gamma**2*b**2)
assert null_residual == 0
assert normalization == -1
assert s.simplify(schwarzian-target) == 0
assert schwarzian.subs({gamma:s.Rational(5,4), b:1}) == -s.Rational(243,800)
print(json.dumps({
    'python':platform.python_version(), 'sympy':s.__version__,
    'domain':'b>0, gamma>1, neighborhood of tau=0, signature -++',
    'clock_map':str(f), 'null_residual':str(null_residual),
    'receiver_velocity_norm':str(normalization),
    'clock_map_jets_at_zero':[str(j) for j in jets],
    'schwarzian_at_zero':str(schwarzian),
    'exact_example':'gamma=5/4, b=1: -243/800',
    'claim':'Universal zero Schwarzian of arbitrary inertial proper-clock maps fails already in SR; no exclusion of matched or restricted projective-clock proposals.',
    'checks_passed':True
},indent=2))
