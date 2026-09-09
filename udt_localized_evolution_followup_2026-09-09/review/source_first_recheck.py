"""Preserved failure is an unresolved symbolic power simplification, not curvature.

Continue the independently built metric-tensor calculation while normalizing
the exponent of the positive symbol t explicitly. No author evidence is read.
"""
import importlib.util
import json
import platform
import sympy as s

spec=importlib.util.spec_from_file_location('initial_review_check',
    'udt_localized_evolution_followup_2026-09-09/review/source_first_check.py')
m=importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(m)
except AssertionError:
    assert hasattr(m,'kretsch')
else:
    raise AssertionError('Expected initial preserved simplification failure absent')
t,q,p=m.t,m.q,m.p

def normalize(expr):
    expr=s.powsimp(s.expand(expr))
    return s.factor(expr.replace(
        lambda z: z.is_Pow and z.base==t,
        lambda z: t**s.factor(z.exp)))

# Each independent tensor contraction term has t^-4 after power normalization.
terms=[normalize(m.metric[a]**2*value**2/
                 (m.metric[a]*m.metric[b]*m.metric[c]*m.metric[e]))
       for (a,b,c,e),value in m.curv.items() if value!=0]
kretsch=s.simplify(s.powsimp(sum(terms),deep=True,force=True))
i2,i3,disc=m.i2,m.i3,m.disc
shape=s.factor(2*disc/i2**3)
assert s.factor(kretsch-8*i2)==0
assert s.factor(shape-(1-6*i3**2/i2**3))==0
assert s.diff(shape,t)==0
assert s.factor(s.diff(kretsch,t)+4*kretsch/t)==0
assert shape.subs(q,1)==0
assert shape.subs(q,s.Rational(6,5))>0
assert kretsch.subs(q,1)==s.Rational(64,27)/t**4

u=s.symbols('u',real=True)
c=(1-u*u)/(1+u*u)
sn=2*u/(1+u*u)
pu=[(1-2*c)/3,(1+c-s.sqrt(3)*sn)/3,(1+c+s.sqrt(3)*sn)/3]
assert s.factor(sum(pu)-1)==0
assert s.factor(sum(z*z for z in pu)-1)==0
eu=[s.factor(z*(1-z)) for z in pu]
iu=s.factor(sum(z*z for z in eu))
ju=s.factor(sum(z*z*z for z in eu))
shape_u=s.factor(1-6*ju**2/iu**3)
assert shape_u==u*u*(u*u-3)**2/(u*u+1)**3
ratio_u=s.factor(8*iu/s.Rational(64,27))
assert s.factor(ratio_u-(1-shape_u))==0

T0=s.symbols('T0',positive=True)
pm=s.symbols('pmin',real=True)
length=T0*((t/T0)**(1-pm)-1)/(1-pm)
assert s.simplify(s.diff(length,t)-(t/T0)**(-pm))==0
assert s.simplify(length.subs(t,T0))==0

print(json.dumps({
 'python':platform.python_version(),'sympy':s.__version__,
 'route':'metric -> Christoffels -> full Riemann contraction; normalized positive-time powers',
 'ricci':str(m.ricci),'magnetic_zero':m.magnetic_zero,
 'electric':str(m.electric),'kretschmann':str(kretsch),
 'trace_Q2':str(i2),'trace_Q3':str(i3),
 'characteristic_discriminant':str(disc),
 'shape_2disc_over_traceQ2_cubed':str(shape),
 'shape_at_q_6_over_5':str(shape.subs(q,s.Rational(6,5))),
 'shape_in_source_u':str(shape_u),
 'curvature_core_over_taub_same_T':str(ratio_u),
 'future_speed_integral':str(length),
 'retained_failure':'Initial direct contraction expression was equal but SymPy did not normalize its exponents to zero.',
 'status':'EXACT_ALGEBRA_PASSED; PDE/domain theorem remains analytical and conditional'
},indent=2))
