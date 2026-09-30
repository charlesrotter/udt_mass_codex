"""Independent exact anchors; no producer code or result imports."""
import json
import platform
import sympy as s

identities = []
rejections = []
values = {}

def zero(name, x):
    entries = list(x) if isinstance(x, s.MatrixBase) else [x]
    assert all(s.simplify(e) == 0 for e in entries), (name, x)
    identities.append(name)

def nonzero(name, x):
    entries = list(x) if isinstance(x, s.MatrixBase) else [x]
    assert any(s.simplify(e) != 0 for e in entries), (name, x)
    rejections.append(name)

G = s.diag(-1, 1, 1, 1)
e0 = s.Matrix([1, 0, 0, 0])
e1 = s.Matrix([0, 1, 0, 0])

def moment(pop):
    total = s.zeros(4)
    for weight, k in pop:
        zero('null-support-' + str(len(identities)), (k.T * G * k)[0])
        cov = G * k
        total += weight * cov * cov.T
    return total

def pairing(A, B):
    return s.trace(G * A * G * B)

def strain(u, n):
    a, b = G*u, G*n
    return 2 * (a*a.T + b*b.T)

t, a, b = s.symbols('t a b', real=True)
z = a*s.cosh(t) + b*s.sinh(t)
zero('hyperbolic-geodesic-Hessian', s.diff(z*z, t, 2)-2*s.diff(z,t)**2-2*z*z)

kp, km = e0+e1, e0-e1
T = moment([(s.Integer(16),kp), (s.Integer(1),km)])
U = s.Matrix([s.Rational(5,4), s.Rational(3,4),0,0])
rho = (U.T*T*U)[0]
zero('unit-future-observer', (U.T*G*U)[0]+1)
zero('unequal-beam-eigenobserver', T*U + rho*G*U)
zero('unequal-beam-density-eight', rho-8)
zero('null-moment-trace', s.trace(G*T))
J = 16*kp+km
nonzero('first-moment-direction-not-minimizer', T*J*(J.T*G*J)[0]-(J.T*T*J)[0]*G*J)
nonzero('wrong-eigenvalue-sign', T*U-rho*G*U)
nonzero('omit-index-lowering', T*U+rho*U)
values['unequal_beams'] = {'T_cov':str(T), 'U':str(U), 'rho':str(rho), 'J':str(J)}

L = s.Matrix([[s.Rational(5,3),0,s.Rational(4,3),0],[0,1,0,0],
              [s.Rational(4,3),0,s.Rational(5,3),0],[0,0,0,1]])
zero('rational-boost-Lorentz', L.T*G*L-G)
Tb = moment([(s.Integer(16),L*kp),(s.Integer(1),L*km)])
zero('pushforward-vs-direct-moment', Tb-G*L*G*T*G*L.T*G)
Ub = L*U
zero('boosted-eigenobserver', Tb*Ub+rho*G*Ub)
zero('boosted-observer-unit', (Ub.T*G*Ub)[0]+1)
Hb = strain(L*e0,L*e1)
zero('reciprocal-pairing-covariance',pairing(Tb,Hb)-pairing(T,strain(e0,e1)))
zero('direct-positive-pairing-68',pairing(T,strain(e0,e1))-68)
nonzero('raw-moment-DDR',pairing(T,strain(e0,e1)))
zero('trace-term-invisible',pairing(G,strain(e0,e1)))

r = s.symbols('r', real=True)
Ur=s.Matrix([s.cosh(r),s.sinh(r),0,0])
B=moment([(s.Integer(1),kp)])
q=(Ur.T*B*Ur)[0]
zero('single-beam-decay',s.expand(q.rewrite(s.exp))-s.exp(-2*r))
zero('single-beam-no-critical-along-aligned-boost',s.diff(s.exp(-2*r),r)+2*s.exp(-2*r))
zero('single-beam-positive-DDR',pairing(B,strain(e0,e1))-4)

six=[]
for i in range(1,4):
    ei=s.zeros(4,1); ei[i]=1
    six += [(s.Integer(1),e0+ei),(s.Integer(1),e0-ei)]
Ts=moment(six)
zero('six-beam-isotropic-second-moment',Ts-s.diag(6,2,2,2))
zero('six-beam-e0-eigenobserver',Ts*e0+6*G*e0)
zero('six-beam-DDR-pairing-sixteen',pairing(Ts,strain(e0,e1))-16)
nonzero('second-moment-isotropy-does-not-pass-DDR',pairing(Ts,strain(e0,e1)))
ax=sum(weight*k[1]**4 for weight,k in six)
diag=sum(weight*((k[1]+k[2])/s.sqrt(2))**4 for weight,k in six)
nonzero('second-moment-isotropy-not-angular-isotropy',ax-diag)
values['fourth_directional_moments']={'axis':str(ax),'diagonal':str(diag)}

n,N=s.symbols('n N',integer=True,positive=True)
first=s.summation(2**n*2**(-n),(n,1,N))
second=s.summation(2**n*2**(-2*n),(n,1,N))
zero('infinite-count-first-partial-moment',first-N)
zero('infinite-count-second-partial-moment',second-(1-2**(-N)))
values['low_frequency_partial_moments']={'first':str(first),'second':str(second)}

print(json.dumps({'status':'PASS','python':platform.python_version(),
                  'sympy':s.__version__,'identity_count':len(identities),
                  'identities':identities,'nonidentity_count':len(rejections),
                  'nonidentities':rejections,'values':values},indent=2))
