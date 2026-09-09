"""Independent source-first exact check; no author candidate/code import.

Question: what survives locally for an exact Kasner core in every actual
smooth LG2 completion? CPU symbolic method, T>0, no discretization. The
source-family and comparison slicing are supplied mathematical controls.
The run_capture wrapper enforces 512 MiB and 60 seconds; one thread below.
"""
import itertools
import json
import platform
import sympy as s

t = s.symbols('t', positive=True)
q = s.symbols('q', real=True)
d = 1 + q + q*q
p = [-q/d, (1+q)/d, q*(1+q)/d]
metric = [-s.Integer(1)] + [t**(2*z) for z in p]

def diff(expr, mu):
    return s.diff(expr, t) if mu == 0 else s.Integer(0)

connection = {}
for a,b,c in itertools.product(range(4), repeat=3):
    value = ((diff(metric[a], b) if a == c else 0)
             + (diff(metric[a], c) if a == b else 0)
             - (diff(metric[b], a) if b == c else 0))/(2*metric[a])
    connection[a,b,c] = s.simplify(value)

def riemann(a,b,c,e):
    value = diff(connection[a,e,b], c)-diff(connection[a,c,b], e)
    value += sum(connection[a,c,z]*connection[z,e,b]
                 - connection[a,e,z]*connection[z,c,b] for z in range(4))
    return s.simplify(value)

curv = {key: riemann(*key) for key in itertools.product(range(4), repeat=4)}
ricci = s.Matrix(4,4,lambda b,e: s.simplify(sum(curv[a,b,a,e] for a in range(4))))
assert ricci == s.zeros(4), ricci
electric = s.diag(*[s.simplify(curv[i,0,i,0]) for i in range(1,4)])
magnetic_zero = all(curv[0,i,j,k] == 0 for i,j,k in itertools.product(range(1,4), repeat=3))
assert magnetic_zero
kretsch = s.factor(sum(metric[a]**2 * value**2 /
                      (metric[a]*metric[b]*metric[c]*metric[e])
                      for (a,b,c,e),value in curv.items() if value != 0))
i2 = s.factor(s.trace(electric**2))
i3 = s.factor(s.trace(electric**3))
characteristic = electric.charpoly().as_expr()
disc = s.factor(s.discriminant(characteristic, electric.charpoly().gen))
shape = s.factor(2*disc/i2**3)
assert s.simplify(kretsch - 8*i2) == 0
assert s.simplify(shape - (1-6*i3**2/i2**3)) == 0
assert s.diff(shape,t) == 0
assert s.simplify(s.diff(kretsch,t) + 4*kretsch/t) == 0
assert shape.subs(q,1) == 0
assert shape.subs(q,s.Rational(6,5)) > 0
assert s.factor(kretsch.subs(q,1)) == s.Rational(64,27)/t**4

# Separate algebraic reconstruction of the actual source's supplied u family.
u = s.symbols('u', real=True)
c = (1-u*u)/(1+u*u)
sn = 2*u/(1+u*u)
pu = [(1-2*c)/3, (1+c-s.sqrt(3)*sn)/3, (1+c+s.sqrt(3)*sn)/3]
assert s.factor(sum(pu)-1) == 0
assert s.factor(sum(z*z for z in pu)-1) == 0
eu = [s.factor(z*(1-z)) for z in pu]
iu = s.factor(sum(z*z for z in eu))
ju = s.factor(sum(z*z*z for z in eu))
shape_u = s.factor(1-6*ju**2/iu**3)
assert shape_u == u*u*(u*u-3)**2/(u*u+1)**3
ratio_u = s.factor(8*iu/s.Rational(64,27))
assert s.simplify(ratio_u-(1-shape_u)) == 0

# Causal Euclidean-speed bound: future T>=T0, pmin<1.
z,T0,pm = s.symbols('z T0 pm', positive=True)
length = T0*((t/T0)**(1-pm)-1)/(1-pm)
assert s.simplify(s.diff(length,t)-(t/T0)**(-pm)) == 0
assert s.simplify(length.subs(t,T0)) == 0

print(json.dumps({
    'python':platform.python_version(), 'sympy':s.__version__,
    'route':'diagonal metric -> Christoffels -> full Riemann contraction',
    'parameterization_q':[str(s.factor(x)) for x in p],
    'ricci':str(ricci), 'magnetic_zero':magnetic_zero,
    'electric':str(electric), 'kretschmann':str(kretsch),
    'trace_Q2':str(i2), 'trace_Q3':str(i3),
    'characteristic_discriminant':str(disc),
    'shape_2disc_over_traceQ2_cubed':str(shape),
    'shape_at_q_6_over_5':str(shape.subs(q,s.Rational(6,5))),
    'shape_in_source_u':str(shape_u),
    'curvature_core_over_taub_same_T':str(ratio_u),
    'future_speed_integral':str(length),
    'notes':['Exact algebra only; not a proof of the imported PDE theorem.',
             'No author candidate, code or outputs were accessed.',
             'The integral is a sufficient inner-domain estimate, not every wavefront.']
},indent=2))
