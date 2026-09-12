"""Independent source-first algebra, no parent implementation imports."""
import hashlib
import json
from pathlib import Path
import platform
import sympy as s
import time

base = Path(__file__).resolve().parent
start = time.monotonic()
a, b = s.symbols('a b', real=True)
r0, r1, r2, r, p, x, u, h = s.symbols('r0 r1 r2 r p x u h', positive=True)
f = lambda z: 1+a*z*z+b/z
checks = []
def zero(label, expr):
    reduced = s.factor(expr)
    ok = reduced == 0
    checks.append({'name':label, 'passed':bool(ok), 'residual':str(reduced)})
    if not ok:
        raise AssertionError(label+': '+str(reduced))
q1, q2 = f(r1)/f(r0), f(r2)/f(r0)
M = s.Matrix([[r1*r1-q1*r0*r0, 1/r1-q1/r0],
              [r2*r2-q2*r0*r0, 1/r2-q2/r0]])
D = (r1-r0)*(r2-r0)*(r2-r1)*(r0+r1+r2)/(r0*r1*r2*f(r0))
zero('general calibration determinant', M.det()-D)
zero('coefficient a recovery', (s.Matrix([[q1-1,M[0,1]],[q2-1,M[1,1]]]).det()/D)-a)
zero('coefficient b recovery', (s.Matrix([[M[0,0],q1-1],[M[1,0],q2-1]]).det()/D)-b)
# Direct static frame k contractions. Choose E=1 and J=j.
j=s.symbols('j', positive=True)
kr2=1-j*j*f(r)/(r*r)
zero('full equatorial null tangent', -f(r)*(1/f(r))**2+kr2/f(r)+r*r*(j/(r*r))**2)
zero('local frame spatial speed norm', kr2+j*j*f(r)/(r*r)-1)
zero('orbit first integral', (1/j**2-f(1/u)*u*u)-(1/j**2-a-u*u-b*u**3))
zero('local angle a derivative', s.diff((a+u*u+b*u**3)/(a+h),a)-(h-u*u-b*u**3)/(a+h)**2)
# Parent candidate transformation is checked after exposure, independently by substitution.
u_x=1-x*x
rr=p/u_x
H=1/p**2+b/p**3-1/rr**2-b/rr**3
Jx=2-x*x+(b/p)*(3-3*x*x+x**4)
Vx=u_x*u_x+a*p*p+(b/p)*u_x**3
zero('transformed turning denominator H',H-x*x*Jx/p**2)
zero('transformed lapse V',f(rr)-Vx/(u_x*u_x))
# Squared integrands avoid assuming square root identities outside the permitted positive leg.
phi2=s.diff(rr,x)**2/(rr**4*H)
time2=(f(p)/p**2)*s.diff(rr,x)**2/(f(rr)**2*H)
zero('transformed angle integrand squared',phi2-4/Jx)
zero('transformed time integrand squared',time2-4*p*p*f(p)/(Vx*Vx*Jx))
# Primitive flat b=0 angular result, on p<R.
R=s.symbols('R',positive=True)
zero('flat angular endpoint derivative',s.diff(s.acos(p/R),R)**2-1/(R**4*(1/p**2-1/R**2)))
# Internal defect injections show these equalities would catch omitted lapse and a terms.
mutants={
 'omit local lapse': s.factor(s.diff(u*u/(a+h),a)-(h-u*u-b*u**3)/(a+h)**2) != 0,
 'omit time metric lapse': s.factor((f(p)/p**2)*s.diff(rr,x)**2/H-4*p*p*f(p)/(Vx*Vx*Jx)) != 0,
 'omit determinant f0':s.factor(M.det()-D*f(r0)) != 0,
}
if not all(mutants.values()): raise AssertionError('vacuous mutant check')
result={'kind':'exact symbolic support, not proof by sampling', 'python':platform.python_version(),
 'sympy':s.__version__, 'seconds':time.monotonic()-start,'checks':checks,'defect_injections':mutants,
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'candidate_exposure':'algebra derived in SOURCE_FIRST_NOTES before exposure; transform check added after candidate read',
 'imports_parent_scientific_code':False}
with (base/'EXACT_CHECK_RESULT.json').open('x') as out: json.dump(result,out,indent=2);out.write('\n')
print(json.dumps(result,sort_keys=True))
