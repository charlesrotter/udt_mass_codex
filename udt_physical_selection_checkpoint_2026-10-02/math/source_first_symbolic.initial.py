"""PSC1 source-first exact checks; no parent or peer code imports."""
import json, platform
import sympy as s

checks = {}
def zero(name, expression):
    value = s.factor(s.cancel(expression))
    checks[name] = str(value)
    assert value == 0, (name, value)

alpha, P0 = s.symbols('alpha P0', nonzero=True)
beta, Lam = s.symbols('beta Lambda')
t = s.symbols('t')
a = s.Function('a')(t)
coords = [t, *s.symbols('x y z')]
g = s.diag(-1, a*a, a*a, a*a)
gi = g.inv()
n = 4
Gamma = [[[s.simplify(sum(gi[i,k]*(s.diff(g[k,j],coords[l])+
    s.diff(g[k,l],coords[j])-s.diff(g[j,l],coords[k]))/2 for k in range(n)))
    for l in range(n)] for j in range(n)] for i in range(n)]
Ric = s.Matrix(n,n,lambda i,j:s.simplify(sum(
    s.diff(Gamma[k][i][j],coords[k])-s.diff(Gamma[k][i][k],coords[j])+
    sum(Gamma[k][k][l]*Gamma[l][i][j]-Gamma[k][j][l]*Gamma[l][i][k]
        for l in range(n)) for k in range(n))))
Rg = s.simplify(sum(gi[i,j]*Ric[i,j] for i in range(n) for j in range(n)))
zero('geometric_R',Rg-6*(s.diff(a,t,2)/a+(s.diff(a,t)/a)**2))
Ft, ft = s.Function('F')(t), s.Function('f')(t)
hess = s.Matrix(n,n,lambda i,j:s.diff(Ft,coords[i],coords[j])-
    sum(Gamma[k][i][j]*s.diff(Ft,coords[k]) for k in range(n)))
box = sum(gi[i,j]*hess[i,j] for i in range(n) for j in range(n))
E = Ft*Ric-ft*g/2+g*box-hess+Lam*g
Ht = s.diff(a,t)/a
zero('original_C',E[0,0]-(3*Ft*Ht**2-(Ft*Rg-ft)/2+3*Ht*s.diff(Ft,t)-Lam))
zero('original_D',E[1,1]/a**2-(Ft*(s.diff(Ht,t)+3*Ht**2)-ft/2-
    s.diff(Ft,t,2)-2*Ht*s.diff(Ft,t)+Lam))
for i in range(4):
    for j in range(4):
        if i != j: zero(f'original_offdiag_{i}{j}',E[i,j])
zero('original_isotropy_2',E[2,2]-E[1,1])
zero('original_isotropy_3',E[3,3]-E[1,1])

A,H,R,P = s.symbols('A H R P')
f = R+alpha*R**2+beta*R**3
F = s.diff(f,R)
S = s.diff(F,R)
Q = R/6-2*H**2
W = (F*R-2*f+4*Lam-3*s.diff(S,R)*P**2)/(3*S)-3*H*P
dt = lambda q: s.diff(q,A)*A*H+s.diff(q,H)*Q+s.diff(q,R)*P+s.diff(q,P)*W
C = 3*F*H**2-(F*R-f)/2+3*H*S*P-Lam
D = F*(Q+3*H**2)-f/2-(s.diff(S,R)*P**2+S*W)-2*H*S*P+Lam
zero('trace_not_assumed_sufficient',-C+3*D)
zero('constraint_propagates',dt(C)+4*H*C)
zero('off_shell_Bianchi_on_trace_ODE',dt(C)+3*H*(C+D))
initial = {A:1,H:0,R:0,P:P0,Lam:0}
zero('initial_original00',C.subs(initial))
jets = [A]
for k in range(1,6): jets.append(s.factor(dt(jets[-1])))
acoef = [s.factor(q.subs(initial)/s.factorial(k)) for k,q in enumerate(jets)]
expected = [1,0,0,P0/36,-beta*P0**2/(48*alpha),
    -P0/(4320*alpha)+3*beta**2*P0**3/(80*alpha**2)]
for k in range(6):zero(f'a_jet_{k}',acoef[k]-expected[k])
b3,b4,b5 = expected[3:]
zero('b5_normalized_relation',b5+b3/(120*alpha)-s.Rational(12,5)*b4**2/b3)
zero('beta_normalized_relation',beta+alpha*b4/(27*b3**2))

# Original flat metric first variation in Fourier form, before the scalar shell.
k = s.symbols('k0:4')
eta = s.diag(-1,1,1,1)
k2 = -k[0]**2+sum(q*q for q in k[1:])
h = -2*alpha*eta
traceh = sum(eta[i,i]*h[i,i] for i in range(4))
Ric1 = s.Matrix(4,4,lambda i,j:s.expand((
    -sum(eta[l,l]*k[l]*k[i]*h[l,j] for l in range(4))
    -sum(eta[l,l]*k[l]*k[j]*h[l,i] for l in range(4))
    +k2*h[i,j]+k[i]*k[j]*traceh)/2))
R1 = sum(eta[i,i]*Ric1[i,i] for i in range(4))
G1 = Ric1-eta*R1/2
E1 = G1+2*alpha*(-eta*k2+s.Matrix(4,4,lambda i,j:k[i]*k[j]))*R1
shell = {k[0]**2:sum(q*q for q in k[1:])+1/(6*alpha)}
zero('scalar_curvature_normalization',s.expand(R1-1).subs(shell))
for i in range(4):
    for j in range(4):zero(f'flat_original_linear_E_{i}{j}',s.expand(E1[i,j]).subs(shell))
eps,z = s.symbols('epsilon z')
zero('beta_absent_in_linear_F',s.diff(F.subs(R,eps*z),eps).subs(eps,0)-2*alpha*z)

# Static radial original linear metric test: independent derivative expressions.
r,m,amp,mu = s.symbols('r m amplitude mu', positive=True)
rad = amp*s.exp(-m*r)/r
lap = lambda q:s.diff(q,r,2)+2*s.diff(q,r)/r
Psi = -mu/r-alpha*rad
Phi = -mu/r+alpha*rad
static_R = 4*lap(Phi)-2*lap(Psi)
mshell={m**2:1/(6*alpha)}
zero('static_geometric_R',s.expand(static_R-rad).subs(mshell))
G00=2*lap(Phi)
zero('static_original00',s.expand(G00-2*alpha*lap(rad)).subs(mshell))
# Spatial radial and transverse components are independent Hessian eigenvalues.
for name,eigen in [('radial',lambda q:s.diff(q,r,2)),('transverse',lambda q:s.diff(q,r)/r)]:
    Gii=eigen(Phi-Psi)+lap(Psi-Phi)
    zero('static_original_'+name,s.expand(Gii+2*alpha*(lap(rad)-eigen(rad))).subs(mshell))

# Full constant-background conformal realization of the trace pole.
rb,fb,sb,m2,boxu,u,Tij,gij = s.symbols('Rb Fb fpp mass2 Boxu u Hessij gij', nonzero=True)
sigma = -sb*u/(2*fb)
delta_R = -2*rb*sigma+3*sb*boxu/fb
bg_shell={boxu:(fb-rb*sb)*u/(3*sb)}
zero('curved_geometric_deltaR',(delta_R-u).subs(bg_shell))
delta_E = (sb*Tij + sb*gij*boxu/2 + rb*sb*u*gij/4+
    (rb*sb/4-fb/2)*u*gij+sb*(gij*boxu-Tij))
zero('curved_full_tensor_scalar_realization',delta_E.subs(bg_shell))
const = s.symbols('normalization', nonzero=True)
Fconstantpole=const*(R+3*m2)
zero('constant_pole_selection_ODE',Fconstantpole-(R+3*m2)*s.diff(Fconstantpole,R))
fixed_vac_derivative=s.diff(R*F-2*f+4*Lam,R)
zero('fixed_Lambda_vacuum_interval_massless',fixed_vac_derivative-(R*S-F))
primitive = s.integrate(F,R)
zero('entropy_primitive',s.diff(primitive,R)-F)
print(json.dumps({'python':platform.python_version(),'sympy':s.__version__,
    'checks':checks,'a_coefficients':[str(v) for v in acoef],
    'clock_coefficients_through5':[str(v) for v in acoef],
    'scope':'exact identities and local jets only; no physical selection/adoption'},indent=2))
