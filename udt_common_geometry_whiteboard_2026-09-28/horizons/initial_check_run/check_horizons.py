"""Exact author checks for CHECK_FREEZE.md, not an independent review."""
import os
for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[name] = '2'
import sys, json, platform, hashlib, resource
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
import sympy as s

root = Path(__file__).resolve().parent
checks = []
def zero(name, expression):
    residual = s.simplify(s.expand(expression))
    checks.append({'name': name, 'residual': str(residual), 'pass': residual == 0})

t, l = s.symbols('t l', real=True)
N = s.Function('N')(l)
g = s.diag(-N**2, 1)
inv = g.inv()
coords = [t, l]
G = [[[s.simplify(sum(inv[a,d]*(s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d])) for d in range(2))/2) for c in range(2)] for b in range(2)] for a in range(2)]
Ric = s.Matrix(2,2,lambda b,d:s.simplify(sum(s.diff(G[a][b][d],coords[a])-s.diff(G[a][a][b],coords[d])+sum(G[a][a][e]*G[e][b][d]-G[a][d][e]*G[e][a][b] for e in range(2)) for a in range(2))))
R = s.simplify(sum(inv[i,j]*Ric[i,j] for i in range(2) for j in range(2)))
zero('Ricci_scalar_from_Christoffels',R+2*s.diff(N,l,2)/N)
zero('static_oriented_acceleration',G[1][0][0]/N**2-s.diff(N,l)/N)
delta = s.Function('delta')(l)
zero('tidal_depth_Riccati', (s.diff(N,l,2)/N).subs(N,s.exp(-delta)).doit()-(s.diff(delta,l)**2-s.diff(delta,l,2)))
E = s.symbols('E',positive=True)
v = s.Matrix([E/N**2, E/N])
zero('null_constraint', (v.T*g*v)[0])
for a in range(2):
    zero('null_geodesic_'+str(a), v[1]*s.diff(v[a],l)+sum(G[a][b][c]*v[b]*v[c] for b in range(2) for c in range(2)))
zero('Killing_energy', N**2*v[0]-E)
zero('affine_integrand',1/v[1]-N/E)
zero('optical_integrand',v[0]/v[1]-1/N)
zero('reciprocal_determinant',s.det(s.diag(-N**2,1/N**2))+1)

k,p = s.symbols('k p',positive=True)
Np = (1+k*l/p)**(-p)
primitive = p/(k*(1-p))*((1+k*l/p)**(1-p)-1)
zero('power_family_affine_primitive_p_not_1',s.diff(primitive,l)-Np)
zero('power_family_affine_primitive_p_1',s.diff(s.log(1+k*l)/k,l)-Np.subs(p,1))
zero('power_family_depth_initial_value',(-s.log(Np)).subs(l,0))
zero('power_family_depth_initial_slope',s.diff(-s.log(Np),l).subs(l,0)-k)
zero('exponential_affine_primitive',s.diff((1-s.exp(-k*l))/k,l)-s.exp(-k*l))
zero('exponential_reciprocal_endpoint',s.diff((1-s.exp(-k*l))/k,l)-s.exp(-k*l))
zero('finite_simple_root_lapse_acceleration',s.diff(s.log(1-k*l),l)+k/(1-k*l))
zero('finite_simple_root_flatness',s.diff(1-k*l,l,2))

eta=s.symbols('eta',positive=True)
beta=s.tanh(eta); gamma=s.cosh(eta)
zero('SR_received_forward',1/(gamma*(1-beta))-s.exp(eta))
zero('SR_received_return',gamma*(1+beta)-s.exp(eta))
zero('SR_gamma_from_Doppler',gamma-(s.exp(eta)+s.exp(-eta))/2)
zero('SR_time_dilation_not_Doppler',s.exp(eta)-gamma-s.sinh(eta))
a,tau,te=s.symbols('a tau te',positive=True)
Tb=s.sinh(a*tau)/a; Xb=s.cosh(a*tau)/a
emit=-s.exp(-a*tau)/a; receive=s.exp(a*tau)/a
zero('accelerated_outgoing_intersection',Tb-Xb-emit)
zero('accelerated_return_intersection',Tb+Xb-receive)
zero('accelerated_forward_clock_factor',1/s.diff(emit,tau)-s.exp(a*tau))
zero('accelerated_return_clock_factor',s.diff(receive,tau)-s.exp(a*tau))
zero('accelerated_echo_map',receive+1/(a*a*emit))

rho,T,kappa=s.symbols('rho T kappa',positive=True)
M=s.Matrix([rho*s.sinh(kappa*T),rho*s.cosh(kappa*T)])
J=M.jacobian([T,rho])
pulled=s.simplify(J.T*s.diag(-1,1)*J)
for i in range(2):
    for j in range(2):zero('Rindler_exact_pullback_'+str(i)+str(j),pulled[i,j]-s.diag(-kappa*kappa*rho*rho,1)[i,j])
x=s.symbols('x',positive=True)
f=x/(1+x)
zero('Schwarzschild_relative_lapse_error',f/x-1+x/(1+x))
zero('Schwarzschild_radial_factor',x/f-(1+x))

result={'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','kind':'author exact symbolic regression; not independent review','python':platform.python_version(),'sympy':s.__version__,'checks':checks,'count':len(checks),'derived_R2':str(R),'limits':{'power_p_less_equal_1_affine':'infinite as l tends to +infinity','power_p_greater_1_affine':'p/[k(p-1)] from 0 to +infinity','exponential_affine':'1/k from 0 to +infinity'},'failures':[c for c in checks if not c['pass']]}
(root/'CHECK_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
sys.exit(0 if result['status']=='PASS' else 1)
