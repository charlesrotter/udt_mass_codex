"""PJC1 symbolic replay of recovered source identities, not a native-law verifier."""
import datetime
import hashlib
import json
from pathlib import Path
import platform
import sys
import sympy as s

r, z, rstar = s.symbols('r z rstar', positive=True)
C, eps = s.symbols('C epsilon', real=True)
f = s.Function('f')(r)
N = s.Function('N')(r)
b = s.Function('b')
fp, fpp = s.diff(f, r), s.diff(f, r, 2)
A = (r*r*fpp-r*fp)/2
B = 1-f+r*fp/2
checks = {}
def zero(name, value):
    value = s.simplify(value)
    assert value == 0, (name, value)
    checks[name] = str(value)
zero('neighboring_interlock', A-r*s.diff(B,r))
zero('reconstruction_equation', r*fp-2*f-2*(B-1))
zero('integrating_factor', s.diff(f/r**2,r)-2*(B-1)/r**3)
reconstructed = r**2*(C+s.Integral(2*(b(z)-1)/z**3,(z,rstar,r)))
zero('supplied_b_reconstruction', r*s.diff(reconstructed,r)-2*reconstructed-2*(b(r)-1))
hom = f+C*r*r
zero('homogeneous_A_invisible', (r*r*s.diff(hom,r,2)-r*s.diff(hom,r))/2-A)
zero('homogeneous_B_invisible', 1-hom+r*s.diff(hom,r)/2-B)
zero('clock_A', A.subs(f,N*N).doit()-(r*r*(s.diff(N,r)**2+N*s.diff(N,r,2))-r*N*s.diff(N,r)))
zero('clock_B', B.subs(f,N*N).doit()-(1-N*N+r*N*s.diff(N,r)))
x = s.symbols('x',positive=True)
fe = (1+x*x)*s.exp(eps*(x-1)**2)
assert fe.is_positive is True
jets = [s.simplify(s.diff(fe,x,k).subs(x,1)) for k in range(3)]
assert jets == [2,2,2+4*eps]
BE=s.simplify((1-fe+x*s.diff(fe,x)/2).subs(x,1))
AE=s.simplify(((x*x*s.diff(fe,x,2)-x*s.diff(fe,x))/2).subs(x,1))
assert BE == 0 and AE == 2*eps
checks['exact_control_jet_and_amplitudes'] = {'f_jets_dimensionless':[str(v) for v in jets],
    'A_perp':str(BE),'A_parallel':str(AE),'epsilon_smallness_assumed':False}
wrong_A=(r*r*fpp+r*fp)/2
wrong_B=-f+r*fp/2
sign_residual=s.simplify(wrong_A-r*s.diff(B,r))
constant_residual=s.simplify(r*fp-2*f-2*(wrong_B-1))
assert sign_residual == r*fp and constant_residual == 2
checks['hostile_controls']={'wrong_sign_nonidentity_residual':str(sign_residual),
    'missing_constant_nonidentity_residual':str(constant_residual)}
out={'status':'PASS_SOURCE_FORMULA_REPLAY_ONLY','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'python':sys.version,'sympy':s.__version__,'platform':platform.platform(),'checks':checks,
    'maximum_claim':'source-relative interlock/reconstruction identities and explicit finite-data counter-reading; no new native law/admission/no-go'}
print(json.dumps(out,indent=2))
