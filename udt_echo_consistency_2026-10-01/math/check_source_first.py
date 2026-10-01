"""Finite exact checks for the frozen synchronous reconstruction.

All geometry parameters are FREE supplied comparisons, not UDT-selected values.
This independently arranged code imports no parent or prior mathematical code.
"""
import json
import platform
import sympy as s

t, x, y, z = s.symbols('tau x y z', real=True)
mu, k = s.symbols('mu k', positive=True)
a = s.Function('a')(t)
coords = [t, x, y, z]
g = s.diag(-1, a*a, 1, s.exp(2*mu*y))
gi = g.inv()
Gamma = [[[s.simplify(sum(gi[i,m]*(s.diff(g[m,j],coords[l])
    + s.diff(g[m,l],coords[j])-s.diff(g[j,l],coords[m]))
    for m in range(4))/2) for l in range(4)] for j in range(4)]
    for i in range(4)]
checks = []

def zero(label, expr):
    value = s.simplify(s.trigsimp(expr))
    if value != 0:
        raise AssertionError((label, str(value)))
    checks.append(label)

def nonzero(label, expr):
    value = s.simplify(expr)
    if value == 0 or value.is_zero is not False:
        raise AssertionError((label, str(value)))
    checks.append(label)

def riemann(i,j,l,m):
    return s.simplify(s.diff(Gamma[i][m][j],coords[l])
        -s.diff(Gamma[i][l][j],coords[m])
        +sum(Gamma[i][l][b]*Gamma[b][m][j]
            -Gamma[i][m][b]*Gamma[b][l][j] for b in range(4)))

for i in range(4):
    zero(f'clock_geodesic_{i}', Gamma[i][0][0])
zero('clock_unit', g[0,0]+1)
zero('preparation_connection_xxt',Gamma[1][1][0]-s.diff(a,t)/a)
zero('preparation_connection_txx',Gamma[0][1][1]-a*s.diff(a,t))

for direction in (-1,1):
    ray = s.Matrix([1/a,direction/a**2,0,0])
    zero(f'null_{direction}', (ray.T*g*ray)[0])
    for i in range(4):
        acc = sum(ray[j]*s.diff(ray[i],coords[j]) for j in range(4))
        acc += sum(Gamma[i][j][l]*ray[j]*ray[l]
                   for j in range(4) for l in range(4))
        zero(f'affine_ray_{direction}_{i}',acc)
    zero(f'frequency_{direction}', -(g*ray)[0]-1/a)

# Convention: R^i_{j l m}; contraction Ric_{jm}=R^i_{j i m}.
Ric = s.Matrix(4,4,lambda j,m: sum(riemann(i,j,i,m) for i in range(4)))
scalar = s.simplify(sum(gi[j,m]*Ric[j,m] for j in range(4) for m in range(4)))
zero('scalar_original_metric',scalar-(2*s.diff(a,t,2)/a-2*mu**2))
zero('clock_section_component',-riemann(0,1,0,1)+a*s.diff(a,t,2))
zero('mixed_section_component',riemann(0,2,0,2))
zero('transverse_section_component',riemann(2,3,2,3)+mu**2*s.exp(2*mu*y))

eta, L = s.symbols('eta L', real=True)
branches = [('positive',s.cosh(k*t),1/s.cos(k*eta),k*k),
            ('zero',s.Integer(1),s.Integer(1),s.Integer(0)),
            ('negative',s.cos(k*t),1/s.cosh(k*eta),-k*k)]
ratios = {}
for name,at,A,K in branches:
    zero(name+'_jacobi',s.diff(at,t,2)-K*at)
    zero(name+'_initial_norm',at.subs(t,0)-1)
    zero(name+'_initial_parallel',s.diff(at,t).subs(t,0))
    # Compute curvature of the conformal clock sheet from its scale factor.
    zero(name+'_conformal_curvature',
         (A*s.diff(A,eta,2)-s.diff(A,eta)**2)/A**4-K)
    p=A.subs(eta,L)/A.subs(eta,0)
    q=A.subs(eta,2*L)/A.subs(eta,L)
    zero(name+'_elimination',q*(2-p*p)-p)
    zero(name+'_chain_rule',p*q-A.subs(eta,2*L)/A.subs(eta,0))
    ratios[name]={'p':str(p),'q':str(q),'pq':str(s.simplify(p*q))}

for name,c in [('positive',s.Rational(4,5)),('negative',s.Rational(5,4))]:
    # c denotes cos(alpha) or cosh(alpha), independently of symbolic p/q.
    p=1/c
    q=c/(2*c*c-1)
    zero(name+'_rational_relation',q-p/(2-p*p))
    nonzero(name+'_reject_reciprocal',q-1/p)
    nonzero(name+'_reject_total_as_leg',p*q-q)

print(json.dumps({'verdict':'PASS','evidence':'exact symbolic regression; analytic proof separately frozen',
    'python':platform.python_version(),'sympy':s.__version__,
    'count':len(checks),'checks':checks,'ratios':ratios,
    'scalar':str(scalar),'limits':'Finite direct branches proved analytically; no global classification'},indent=2))
