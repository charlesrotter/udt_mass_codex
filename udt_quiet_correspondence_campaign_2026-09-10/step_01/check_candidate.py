"""QC1 author exact/symbolic support; analytic inequalities remain proof-owned."""
import hashlib
import json
import platform
from pathlib import Path

import sympy as s

checks = 0


def same(a, b, label):
    global checks
    z = s.simplify(a-b)
    assert z == 0, (label, z)
    checks += 1


def le(a, b, label):
    global checks
    assert bool(a <= b), (label, a, b)
    checks += 1


x, z, tvar = s.symbols('x z tvar', positive=True)
U = (x*x+2/x)/3
V = (x*x-1/x)/3
kernel = s.Rational(2, 3)*(x*x/z**3-1/x)
same(x*x*s.diff(U, x, 2)/2-U, 0, 'U homogeneous')
same(x*x*s.diff(V, x, 2)/2-V, 0, 'V homogeneous')
for h, d0, d1 in [(U, 1, 0), (V, 0, 1)]:
    same(h.subs(x, 1), d0, 'anchor value')
    same(s.diff(h, x).subs(x, 1), d1, 'anchor derivative')
same(kernel.subs(z, x), 0, 'Green diagonal')
same(s.diff(kernel, x).subs(z, x), 2/x**2, 'Green derivative jump')
same(s.integrate(kernel, (z, 1, x)), U-1, 'mass both anchor sides')
same(s.integrate(s.diff(kernel, x), (z, 1, x)), s.diff(U, x), 'derivative mass')
same(s.diff(U, x, 2), 2*U/x**2, 'second mass')

resonant = []
for n in range(-3, 5):
    answer = s.integrate(kernel*z**n, (z, 1, x))
    same(answer.subs(x, 1), 0, f'anchor0 n={n}')
    same(s.diff(answer, x).subs(x, 1), 0, f'anchor1 n={n}')
    same(x*x*s.diff(answer, x, 2)/2-answer, x**n, f'inhomogeneous n={n}')
    if n in (-1, 2):
        assert answer.has(s.log)
        checks += 1
        resonant.append(n)

# Supplied rational numerical controls, not physical parameter choices.
l, u = s.Rational(1, 2), s.Integer(2)
grid = [l, s.Rational(3, 4), s.Integer(1), s.Rational(3, 2), u]
M_U = max(U.subs(x, l), U.subs(x, u))
M_V = max(abs(V.subs(x, l)), abs(V.subs(x, u)))
U1, U2, V1, V2 = [s.diff(h, x, j) for h, j in [(U,1),(U,2),(V,1),(V,2)]]
M_U1 = max(abs(U1.subs(x,l)), abs(U1.subs(x,u)))
M_V1 = max(V1.subs(x,l), V1.subs(x,u))
M_V2 = max(abs(V2.subs(x,l)), abs(V2.subs(x,u)))
cases = []
for n in [-3, -2, 0, 1, 3, 4]:
    for sign in [-1, 1]:
        eta0 = s.Rational(1,100)
        eta1 = s.Rational(1,200)
        residual = sign*z**n/1000
        epsilon = max(l**n,u**n)/1000
        y = eta0*U-sign*eta1*V+s.integrate(kernel*residual, (z,1,x))
        D0 = eta0*M_U+eta1*M_V+epsilon*(M_U-1)
        D1 = (eta0+epsilon)*M_U1+eta1*M_V1
        D2 = (eta0+epsilon)*U2.subs(x,l)+eta1*M_V2
        le(D0, s.Rational(1,2), 'uniform positivity certificate')
        for point in grid:
            bs = [eta0*U+eta1*abs(V)+epsilon*(U-1),
                  (eta0+epsilon)*abs(U1)+eta1*V1,
                  (eta0+epsilon)*U2+eta1*abs(V2)]
            for j in range(3):
                actual = abs(s.diff(y,x,j).subs(x,point))
                bound = bs[j].subs(x,point)
                le(actual,bound,f'pointwise{j}, n={n}, sign={sign}, x={point}')
                le(bound,[D0,D1,D2][j],f'uniform{j}')
            qvalue = 1+y.subs(x,point)
            le(s.Rational(1,2),qvalue,'pointwise positive')
        cases.append({'n':n,'sign':sign,'epsilon':str(epsilon),'D0':str(D0)})

# Rebuild full four-dimensional metric connection before reading curvature targets.
tt, r, theta, phi = s.symbols('tt r theta phi', real=True)
coords = [tt,r,theta,phi]
F = s.Function('F')(r)
g = s.diag(-F,1/F,r*r,r*r*s.sin(theta)**2)
gi = g.inv()
Gamma = [[[s.simplify(sum(gi[a,d]*(s.diff(g[d,b],coords[c])+
          s.diff(g[d,c],coords[b])-s.diff(g[b,c],coords[d])) for d in range(4))/2)
          for c in range(4)] for b in range(4)] for a in range(4)]


def rcov(a,b,c,d):
    return s.simplify(sum(g[a,e]*(s.diff(Gamma[e][d][b],coords[c])-
           s.diff(Gamma[e][c][b],coords[d])+sum(Gamma[e][c][k]*Gamma[k][d][b]-
           Gamma[e][d][k]*Gamma[k][c][b] for k in range(4))) for e in range(4)))


scales = [1/s.sqrt(F),s.sqrt(F),1/r,1/(r*s.sin(theta))]
targets = {(0,1):s.diff(F,r,2)/2,(0,2):s.diff(F,r)/(2*r),
           (0,3):s.diff(F,r)/(2*r),(1,2):-s.diff(F,r)/(2*r),
           (1,3):-s.diff(F,r)/(2*r),(2,3):(1-F)/r**2}
for (a,b), target in targets.items():
    same(rcov(a,b,a,b)*scales[a]**2*scales[b]**2,target,f'orthogonal section{a}{b}')
for i in range(1,4):
    for j in range(1,4):
        if i != j:
            same(rcov(0,i,0,j),0,f'tidal offdiag{i}{j}')
same(Gamma[1][0][0]/F/s.sqrt(F), s.diff(F,r)/(2*s.sqrt(F)), 'proper support acceleration')
same(s.diff(s.log(s.sqrt(F)),r),s.diff(F,r)/(2*F),'coordinate log lapse derivative')

# Exact positive-input checks of denominator-sensitive algebra, independently of profiles.
for qv,pv,qp,pp in [(s.Rational(1,2),1,2,-1),(2,3,-1,2),(1,1,0,0),
                    (s.Rational(1,4),s.Rational(1,2),1,s.Rational(1,3))]:
    qv,pv,qp,pp = map(s.Rational,(qv,pv,qp,pp))
    m = min(qv,pv)
    b0,b1=abs(qv-pv),abs(qp-pp)
    le(abs(qp/(2*qv)-pp/(2*pv)), b1/(2*m)+abs(pp)*b0/(2*m*m),'H algebra')
    le(abs(qp/(2*s.sqrt(qv))-pp/(2*s.sqrt(pv))),
       b1/(2*s.sqrt(m))+abs(pp)*b0/(4*m**s.Rational(3,2)),'J algebra')

# Specific false-pass controls; not an exhaustive mutation suite.
assert s.simplify((x*x*s.diff(- (U-1),x,2)/2+(U-1))-1) != 0
checks += 1  # wrong Green sign must fail original residual
assert s.simplify((1-F)/r**2 - (-F/r**2)) != 0
checks += 1  # removing sphere curvature changes a full-metric component

print(json.dumps({'status':'PASS','assertions':checks,'python':platform.python_version(),
      'sympy':s.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'method':'symbolic Green identities, rational finite support, full coordinate Riemann reconstruction',
      'resonant_residual_powers':resonant,'finite_profile_cases':cases,
      'negative_controls':['wrong Green sign','sectional formula with sphere term removed'],
      'limitations':'Finite checks support algebra; general continuity/domain/norm/clock Lipschitz claims rely on analytic proof; no empirical test'},indent=2))
