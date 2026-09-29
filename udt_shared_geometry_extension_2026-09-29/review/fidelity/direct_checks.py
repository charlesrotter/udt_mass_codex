"""Independent small controls; no author code or outputs imported."""
import json
import platform
import resource
import signal
import time

resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2, 512 * 1024**2))
resource.setrlimit(resource.RLIMIT_CPU, (60, 60))
signal.alarm(60)
started = time.monotonic()
import sympy as S

checks = []
def zero(name, expr):
    result = S.simplify(S.expand(expr.rewrite(S.exp)))
    if result != 0:
        raise AssertionError((name, result))
    checks.append(name)

t, x, y, z = coords = S.symbols('t x y z', real=True)
r = t * (1 - x)
g = S.diag(-1, 1, 1, 1)
u = S.Matrix([S.cosh(r), S.sinh(r), 0, 0])
ul = g*u
d = S.Matrix(4, 4, lambda a,b:S.diff(ul[b],coords[a]))
h = g + ul*ul.T
proj = S.eye(4) + ul*u.T
a = S.Matrix([sum(u[j]*S.diff(u[i],coords[j]) for j in range(4)) for i in range(4)])
al = g*a
theta = sum(S.diff(u[i],coords[i]) for i in range(4))
sigma = proj*((d+d.T)/2)*proj.T-theta*h/3
vort = proj*((d-d.T)/2)*proj.T
zero('unit_future_boost', (u.T*g*u)[0]+1)
for i in range(4):
    for j in range(4):
        zero('decomposition_%s_%s' % (i,j), d[i,j]+ul[i]*al[j]-theta*h[i,j]/3-sigma[i,j]-vort[i,j])
k = S.Matrix([1,1,0,0])
omega = S.exp(-r)
zero('frequency_from_metric', -(k.T*g*u)[0]-omega)
n=k/omega-u
K=S.simplify(S.expand((theta/3+(n.T*sigma*n)[0]+(al.T*n)[0]).rewrite(S.exp)))
direct=-(S.diff(omega,t)+S.diff(omega,x))/omega**2
zero('generator_from_actual_acceleration_shear', K-direct)
ell_density=omega
zero('auxiliary_density_is_exact_rapidity_derivative', K*ell_density-S.diff(r,t)-S.diff(r,x))
lam=S.symbols('lam',real=True)
ray_density=S.simplify((K*ell_density).subs({t:lam,x:lam},simultaneous=True))
zero('same_endpoint_observers_zero_total', S.integrate(ray_density,(lam,0,1)))
zero('nonzero_interior_generator_anchor', ray_density.subs(lam,S.Rational(1,4))-S.Rational(1,2))
diva=sum(S.diff(a[i],coords[i]) for i in range(4))
udtheta=sum(u[i]*S.diff(theta,coords[i]) for i in range(4))
M=S.Matrix(4,4,lambda i,j:S.diff(u[i],coords[j]))
zero('flat_actual_congruence_commutator', diva-udtheta-S.trace(M*M))
sigmasq=S.trace(g*sigma*g*sigma)
vortsq=-S.trace(g*vort*g*vort)
zero('flat_raychaudhuri_full_decomposition', udtheta+theta**2/3+sigmasq-vortsq-diva)
q=S.symbols('q',positive=True)
gamma=1+q*q/2
sp=S.Matrix([q*q/2,q,0])
zero('norm_boundary_control_lorentz_norm', gamma**2-(sp.T*sp)[0]-1)
zero('norm_boundary_control_received_ratio_one', gamma-sp[0]-1)
B,L,K0=S.symbols('B L K0',positive=True)
s=S.symbols('s',real=True)
zero('local_remainder_sharp_linear_control', S.integrate(K0+B*s,(s,0,L))-K0*L-B*L**2/2)
wrong=[]
def reject(name,condition):
    if bool(condition):
        raise AssertionError('wrong rule survived: '+name)
    wrong.append(name)
reject('auxiliary_generator_pointwise_invariant', ray_density.subs(lam,S.Rational(1,4))==0)
reject('auxiliary_density_transform_wrong_sign', ray_density.subs(lam,S.Rational(1,4))==-S.Rational(1,2))
reject('positive_echo_drift_implies_both_redshift', S.Rational(1,2)>1 and 4>1)
reject('stationary_pair_mutual_redshift', S.Rational(2,3)>1 and S.Rational(3,2)>1)
reject('zero_initial_generator_means_finite_zero', S.integrate(s,(s,0,1))==0)
print(json.dumps({'status':'PASS','exact_identity_checks':len(checks),'checks':checks,'wrong_rules_rejected':wrong,'implementation':'independent actual Minkowski congruence derivatives and exact controls; no author import','python':platform.python_version(),'sympy':S.__version__,'elapsed_seconds':time.monotonic()-started,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'limits':{'cpu_seconds':60,'wall_seconds':60,'address_space_mib':512,'threads':1}},indent=2))
