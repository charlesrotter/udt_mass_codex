"""Additional candidate-exposed exact checks using the reviewer's frozen geometry."""
import contextlib
import io
import json
import runpy
from pathlib import Path
import sympy as s

with contextlib.redirect_stdout(io.StringIO()):
    d = runpy.run_path(str(Path(__file__).with_name('check_exact.py')))
Gf,f,r = d['Gf'],d['f'],d['r']
records=[]
def check(name,value):
    entries=list(value) if isinstance(value,s.MatrixBase) else [value]
    residuals=[s.simplify(x) for x in entries]
    assert all(x==0 for x in residuals),(name,residuals)
    records.append({'name':name,'residuals':[str(x) for x in residuals]})
eps,ell=s.symbols('eps ell',positive=True)
q=eps*r*r/ell**4
control=Gf.subs(f,1+eps*r**4/ell**4).doit()
check('candidate quartic full Einstein from independent geometry',control-s.diag(5*q,5*q,10*q,10*q))

rho,w=s.symbols('rho w',positive=True)
gamma=s.symbols('gamma',real=True)
solutions=s.solve(gamma**2-(gamma-1/rho)**2-w**2-1,gamma)
assert len(solutions)==1
Gamma=solutions[0]
expected=(rho+1/rho+rho*w*w)/2
check('mutual transport interlock from unit-clock equation',Gamma-expected)
check('reversal with carried screen norm',Gamma.subs({rho:1/rho,w:rho*w},simultaneous=True)-Gamma)
check('planar inverse mutual',Gamma.subs(w,0)-(rho+1/rho)/2)
check('positive screen gap',Gamma-(rho+1/rho)/2-rho*w*w/2)

eta=s.diag(-1,1,1,1)
syms=s.symbols('r00 r01 r02 r03 r11 r12 r13 r22 r23 r33')
Ric=s.Matrix([[syms[0],syms[1],syms[2],syms[3]],
              [syms[1],syms[4],syms[5],syms[6]],
              [syms[2],syms[5],syms[7],syms[8]],
              [syms[3],syms[6],syms[8],syms[9]]])
a,b=s.symbols('a b')
R=s.trace(eta*Ric)
E=a*Ric+b*R*eta
check('G301 trace-free coefficient independence',E-s.trace(eta*E)*eta/4-a*(Ric-R*eta/4))

Ns,No=s.symbols('N_source N_observer',positive=True)
clock_ratio=No/Ns
frequency_ratio=No/Ns
# For a static conserved Killing-frequency query omega_source/omega_observer=N_observer/N_source.
check('source-to-observer redshift sign',s.exp(-(-s.log(clock_ratio)))-frequency_ratio)
delta_z=s.log(No/Ns)
check('redshift delta_z sign',s.exp(delta_z)-frequency_ratio)

print(json.dumps({'status':'PASS','count':len(records),'checks':records,
 'scope':'candidate-exposed supplemental exact checks; previous 20 source-first checks reused from unchanged frozen implementation',
 'new_current_candidate_code_exposure':True},indent=2))
