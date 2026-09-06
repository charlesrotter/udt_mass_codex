import json
import platform
import sympy as S

u, v, x, y = S.symbols('u v x y', real=True)
a, kappa, Delta, h = S.symbols('a kappa Delta h', positive=True)
p, t, fx, fy = S.symbols('p t fx fy', real=True)
H = S.Function('H')(u, x, y)
g = S.Matrix([[H, -1, 0, 0], [-1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
gi = g.inv()
checks = []

def equal(name, left, right=0):
    if isinstance(left, S.MatrixBase) or isinstance(right, S.MatrixBase):
        diff = left - right
        assert all(S.simplify(e) == 0 for e in diff), (name, diff)
    else:
        assert S.simplify(left-right) == 0, (name, left, right)
    checks.append(name)

equal('determinant', g.det(), -1)
phase_cov = S.Matrix([-kappa, 0, 0, 0])
K = gi * phase_cov
equal('full_raised_phase', K, S.Matrix([0, kappa, 0, 0]))
equal('null_phase', (phase_cov.T * gi * phase_cov)[0])
observer = S.Matrix([a, (1+p*p+t*t+H*a*a)/(2*a), p, t])
equal('observer_unit', (observer.T*g*observer)[0], -1)
omega = -(observer.T*phase_cov)[0]
equal('frequency', omega, a*kappa)
cut = S.Matrix([[0, 0], [fx, fy], [1, 0], [0, 1]])
equal('full_cut_gram', cut.T*g*cut, S.eye(2))
screen = cut + K*(observer.T*g*cut)/omega
equal('screen_observer_orthogonal', observer.T*g*screen, S.zeros(1, 2))
equal('screen_gram', screen.T*g*screen, S.eye(2))
w = S.Function('w')(u, x, y)
D = S.Matrix([0, w, 0, 0])
equal('geometric_current_rate', -(observer.T*g*D)[0], a*w)
equal('product_rate', omega/Delta * (Delta*w/kappa), a*w)
equal('divergence', sum(S.diff(D[i], c) for i, c in enumerate((u,v,x,y))))
equal('homothety_rate', -(observer/h).T*(h*h*g)*(D/h**4), S.Matrix([a*w/h**3]))
equal('homothety_current_volume', h**4/h**4, 1)

def profile_data(profile):
    equal('harmonic_'+str(len(checks)), S.diff(profile,x,2)+S.diff(profile,y,2))
    n = S.expand(S.diff(profile,x,2)**2 + S.diff(profile,x,y)**2)
    ax, ay = S.diff(n,x)/(4*n), S.diff(n,y)/(4*n)
    q = S.factor(ax*ax+ay*ay)
    # w=q*N^(1/4); w^4 is rational and retains positivity on N,q>0.
    fourth = S.factor(q**4*n)
    return n, q, fourth

cubic = x**3-3*x*y*y
n, q, w4 = profile_data(cubic)
r2 = x*x+y*y
equal('cubic_N', n, 36*r2)
equal('cubic_q', q, 1/(4*r2))
equal('cubic_w_fourth', w4, S.Rational(9,64)/r2**3)
equal('cubic_stationarity', S.diff(w4,u))

quartic = x**4-6*x*x*y*y+y**4
mixed = cubic+u*quartic
nm, qm, wm4 = profile_data(mixed)
F = 1+4*u*x+4*u*u*r2
G = 1+8*u*x+16*u*u*r2
equal('mixture_N', nm, 36*r2*F)
equal('mixture_q', qm, G/(4*r2*F))
equal('mixture_w_fourth', wm4, S.Rational(9,64)*G**4/(r2*F)**3)
log_u = S.factor(S.diff(wm4,u)/(4*wm4))
equal('mixed_log_u_at_zero', log_u.subs(u,0), 5*x)
equal('mixed_log_ux_at_zero', S.diff(log_u,x).subs(u,0), 5)

# Independent exact discrete rejection of rank-one factorization.
values = {(ui,xi): S.factor(wm4.subs({u:ui,x:xi,y:0}))
          for ui in (0,S.Rational(1,4)) for xi in (1,2)}
minor = S.factor(values[(0,1)]*values[(S.Rational(1,4),2)]
                 -values[(0,2)]*values[(S.Rational(1,4),1)])
assert minor != 0
checks.append('mixture_nonzero_product_minor')

# Exact finite-label amount on an annular sector, r in [1,4], angle in [0,1].
# Choose kappa=sqrt(6), Delta=2 in supplied length units; s=(1/2)r^(-3/2).
rad = S.symbols('rad', positive=True)
mu_total = S.integrate(S.Rational(1,2)/S.sqrt(rad), (rad,1,4))
equal('finite_annular_label_amount', mu_total, 1)
points = []
for xv,av in ((1,S.Rational(1,2)),(4,S.Rational(3,2))):
    n0 = n.subs({x:xv,y:0})
    q0 = q.subs({x:xv,y:0})
    b0 = S.root(n0,4)
    w0 = S.simplify(q0*b0)
    s0 = S.simplify(2*w0/S.sqrt(6))
    freq = S.sqrt(6)*av
    rate = S.simplify(freq*s0/2)
    equal('point_rate_'+str(xv), rate, av*w0)
    points.append(dict(x=str(xv),y='0',Uu=str(av),b=str(b0),q=str(q0),
                       w=str(w0),s=str(s0),omega=str(freq),Gamma=str(rate)))

# General rank-one family and deliberately nonseparable multiplier.
A = 1+u*u
f = 2+x*x+y*y
ws = A*f
equal('separable_mixed_log', S.diff(S.diff(ws,u)/ws,x))
bad = S.exp(u*x)
equal('nonseparable_mixed_log', S.diff(S.diff(bad,u)/bad,x), 1)
alpha = S.symbols('alpha', positive=True)
equal('phase_spacing_gauge', (alpha*kappa)/(alpha*Delta), kappa/Delta)
equal('fixed_amount_compensated_factorization', (alpha*kappa)/Delta*(Delta*w/(alpha*kappa)),w)
equal('changed_spacing_compensated_factorization', kappa/(alpha*Delta)*(alpha*Delta*w/kappa),w)

print(json.dumps(dict(python=platform.python_version(),sympy=S.__version__,
                     guard_groups=len(checks),checks=checks,points=points,
                     annular_mu_total=str(mu_total),
                     negative_log_ux_at_u0='5',negative_fourth_minor=str(minor),
                     negative_fourth_values={str(k):str(z) for k,z in values.items()}),
                 indent=2,sort_keys=True))
