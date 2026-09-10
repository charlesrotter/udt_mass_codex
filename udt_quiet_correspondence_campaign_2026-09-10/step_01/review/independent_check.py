"""QC1 independent exact checks; no author imports or author outputs.

Argument implementation: monomial/resonant forcing of the Euler operator,
then direct Christoffel-to-Riemann computation from the full 4-metric.
The Green identity and kernel masses are separate symbolic comparisons.
These finite checks support, and do not replace, the source-first proof.
"""
import json
import platform
import sympy as s

x, t = s.symbols('x t', positive=True)
h0 = (x**2 + 2/x)/3
h1 = (x**2 - 1/x)/3
K = s.Rational(2, 3)*(x**2/t**3 - 1/x)
checks = []
def exact(label, expr):
    val = s.simplify(expr)
    assert val == 0, (label, val)
    checks.append(label)
def check(label, condition):
    assert condition, label
    checks.append(label)
def op(v):
    return s.expand(x*x*s.diff(v,x,2)/2-v)
def matched_particular(k):
    # Solve in log radius: characteristic polynomial (k-2)*(k+1).
    if k == 2:
        p = s.Rational(2,3)*x*x*s.log(x)
    elif k == -1:
        p = -s.Rational(2,3)*s.log(x)/x
    else:
        p = s.Rational(2,(k-2)*(k+1))*x**k
    return p-p.subs(x,1)*h0-s.diff(p,x).subs(x,1)*h1

exact('h0 value', h0.subs(x,1)-1)
exact('h0 slope', s.diff(h0,x).subs(x,1))
exact('h1 value', h1.subs(x,1))
exact('h1 slope', s.diff(h1,x).subs(x,1)-1)
exact('h0 null', op(h0))
exact('h1 null', op(h1))
exact('diagonal Green value', K.subs(t,x))
exact('diagonal Green derivative', s.diff(K,x).subs(t,x)-2/x**2)
exact('integrated Green mass', s.integrate(K,(t,1,x))-(h0-1))
exact('integrated derivative mass', s.integrate(s.diff(K,x),(t,1,x))-s.diff(h0,x))

for k in (-4,-1,0,1,2,3,5):
    w = matched_particular(k)
    exact(f'forcing {k}', op(w)-x**k)
    exact(f'anchor value {k}', w.subs(x,1))
    exact(f'anchor slope {k}', s.diff(w,x).subs(x,1))
    exact(f'Green comparison {k}', s.integrate(K*t**k,(t,1,x))-w)

# Exact-rational constant forcing saturates signed endpoint bounds on BOTH sides.
for xx in (s.Rational(1,3),s.Rational(1,2),s.Rational(3,4),s.Integer(1),
           s.Rational(5,4),s.Integer(2),s.Integer(3)):
    q0=s.Rational(1,100)
    w=q0*(h0-1)
    exact(f'saturated profile {xx}',w.subs(x,xx)-q0*(h0-1).subs(x,xx))
    exact(f'saturated slope {xx}',abs(s.diff(w,x).subs(x,xx))-q0*abs(s.diff(h0,x).subs(x,xx)))
    exact(f'saturated second derivative {xx}',s.diff(w,x,2).subs(x,xx)-2*q0*h0.subs(x,xx)/xx**2)
    check(f'mass nonnegative {xx}',(h0-1).subs(x,xx)>=0)
    if xx !=1:
        mid=(1+xx)/2
        check(f'kernel orientation {xx}',s.sign(K.subs({x:xx,t:mid}))==s.sign(xx-1))

# Full metric geometry, independent of memorized orthonormal curvature formulas.
tau,r,theta,phi=s.symbols('tau r theta phi', real=True)
coords=(tau,r,theta,phi)
f=s.Function('f')(r)
diag=(-f,1/f,r*r,r*r*s.sin(theta)**2)
inverse=tuple(1/v for v in diag)
def dg(i,j,k):
    return s.diff(diag[i],coords[k]) if i==j else s.Integer(0)
def Gamma(a,b,c):
    return s.simplify(inverse[a]*(dg(a,c,b)+dg(a,b,c)-dg(b,c,a))/2)
gammas={(a,b,c):Gamma(a,b,c) for a in range(4) for b in range(4) for c in range(4)}
def Rlower(a,b,c,d):
    val=s.diff(gammas[a,d,b],coords[c])-s.diff(gammas[a,c,b],coords[d])
    val+=sum(gammas[a,c,e]*gammas[e,d,b]-gammas[a,d,e]*gammas[e,c,b] for e in range(4))
    return s.simplify(diag[a]*val)
frame_square=(1/f,f,1/r**2,1/(r*s.sin(theta))**2)
targets={(0,1):s.diff(f,r,2)/2,(0,2):s.diff(f,r)/(2*r),
         (0,3):s.diff(f,r)/(2*r),(1,2):-s.diff(f,r)/(2*r),
         (1,3):-s.diff(f,r)/(2*r),(2,3):(1-f)/r**2}
for (i,j),target in targets.items():
    exact(f'full curvature {i}{j}{i}{j}',Rlower(i,j,i,j)*frame_square[i]*frame_square[j]-target)

# Genuine mutation rejection: missing sphere +1 changes curvature angular term.
check('reject omitted sphere curvature',(targets[2,3]-(-f/r**2))!=0)
check('reject left-anchor absolute orientation', K.subs({x:s.Rational(1,2),t:s.Rational(3,4)})<0)
check('reject deleted value datum',h0.subs(x,s.Rational(3,2))!=0)
check('reject deleted slope datum',h1.subs(x,s.Rational(3,2))!=0)
check('reject common tidal sign mutation',targets[0,1]-(-s.diff(f,r,2)/2)!=0)
check('reject common tide dimensional loss',r*r*targets[2,3]-(1-f)/r**2!=0)

print(json.dumps({'status':'PASS','checks':len(checks),'labels':checks,
 'python':platform.python_version(),'sympy':s.__version__,
 'kind':'symbolic exact finite identity checks plus six explicit defect rejections',
 'proof_owner':'SOURCE_FIRST_REPORT.md; finite checks are not a norm theorem',
 'author_code_imported':False,'author_candidate_exposure_when_written':False},indent=2))
