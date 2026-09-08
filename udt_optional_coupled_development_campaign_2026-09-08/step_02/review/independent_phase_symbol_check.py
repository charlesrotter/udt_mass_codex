"""Post-candidate exact diagnostic of shifted roots and constrained symbols.

Independently uses ADM geometry and tangential Fourier compatibility;
imports neither author scripts nor earlier reviewer test results.
"""
import json
import platform
import sympy as S

checks, reds, values = [], [], {}


def scalar_entries(value):
    return list(value) if isinstance(value, S.MatrixBase) else [value]


def accept_zero(value):
    assert all(S.simplify(x) == 0 for x in scalar_entries(value)), str(value)


def check(name, value):
    accept_zero(value)
    checks.append(name)


def red(name, value):
    try:
        accept_zero(value)
    except AssertionError:
        reds.append({'name': name, 'status': 'RED', 'residual': str(value)})
    else:
        raise AssertionError('mutant passed: ' + name)


R = S.Rational
L = S.Matrix([[R(3,2),R(1,5),0],[0,R(4,3),R(2,7)],[0,0,R(5,4)]])
gamma = L.T*L
alpha = R(7,5)
shift = S.Matrix([R(2,7),R(-1,3),R(3,8)])
g = S.zeros(4)
g[0,0] = -alpha**2+(shift.T*gamma*shift)[0]
for i in range(3):
    g[0,i+1] = g[i+1,0] = (gamma*shift)[i]
    for j in range(3):
        g[i+1,j+1] = gamma[i,j]
gi = g.inv()
p = S.Matrix(S.symbols('p1:4', real=True))
energy = S.sqrt((p.T*gamma.inv()*p)[0])
# Coordinate null phase from independently decomposing E(N+v).
Q = (shift.T*p)[0]-alpha*energy
q = S.Matrix([Q,*p])
ell = gi*q
point = dict(zip(p,L.T*S.Matrix([3,4,0])))
qp, lp = q.subs(point), ell.subs(point)
b = sum(gi[0,i+1]*p[i] for i in range(3))
D = b*b-gi[0,0]*(p.T*gi[1:,1:]*p)[0]
root = ((-b+S.sqrt(D))/gi[0,0]).subs(point)
check('shifted_nonorthogonal_metric_null', (qp.T*gi*qp)[0])
check('candidate_root_matches_ADM_covector', root-qp[0])
check('positive_time_component', lp[0]-S.Rational(25,7))
check('root_velocity_derivative',
      S.Matrix([S.diff(Q,p[i]).subs(point)+lp[i+1]/lp[0] for i in range(3)]))
W = S.sqrt(-g.det())
check('coordinate_flux_lapse_cancellation', W*lp[0]-S.sqrt(gamma.det())*5)
wrong_root = ((-b-S.sqrt(D))/gi[0,0]).subs(point)
wrong_q = S.Matrix([wrong_root,*p.subs(point)])
wrong_ell = gi*wrong_q
red('other_null_root_is_not_future', wrong_ell[0]-lp[0])
red('coordinate_m_is_not_sheet_density', W*lp[0]-1)
values['shifted_geometry'] = {'Q':str(qp[0]),'ell':list(map(str,lp)),
                              'W':str(W),'m_over_n':str(W*lp[0]),
                              'other_root_time_component':str(wrong_ell[0])}

px, py, pz, m, E = S.symbols('px py pz m E', positive=True)
pv = S.Matrix([px,py,pz])
V = pv/S.sqrt((pv.T*pv)[0])
k = S.Matrix([0,1,0])
base = {px:E,py:0,pz:0}
# Principal symbol of p_t+(-Q_p dot partial_i p)=0 and continuity,
# before restricting to curl-compatible transverse amplitudes.
A = S.zeros(4)
for i in range(3):
    for j in range(3):
        A[i,j] = (k[i]*V[j]).subs(base)
    A[3,i] = (m*sum(k[j]*S.diff(V[j],pv[i]) for j in range(3))).subs(base)
A[3,3] = (k.T*V)[0].subs(base)
embedding = S.Matrix([[0,0],[1,0],[0,0],[0,1]])
J = S.Matrix([[0,0],[m/E,0]])
check('curl_compatible_transverse_embedding', k.cross(embedding[:3,0]))
check('invariant_principal_subspace', A*embedding-embedding*J)
check('nilpotent_square', J*J)
assert J.rank() == 1
checks.append('nonzero_rank_one_with_one_eigenvector')
red('remove_density_directional_derivative', J)

y,t,frequency,eps,m0,e0 = S.symbols('y t frequency eps m0 e0', positive=True)
phase_amp = eps*S.cos(frequency*y)
density_amp = m0/e0*t*eps*frequency*S.sin(frequency*y)
check('explicit_Fourier_solution', S.diff(density_amp,t)+m0/e0*S.diff(phase_amp,y))
check('frequency_amplification', density_amp.subs({frequency:11,y:S.pi/22,t:1,eps:1,m0:2,e0:3})-R(22,3))
red('frozen_density_false_solution', (m0/e0*S.diff(phase_amp,y)).subs(
    {frequency:11,y:S.pi/22,t:1,eps:1,m0:2,e0:3}))
values['principal'] = {'A':str(A),'embedding':str(embedding),'J':str(J),
                       'kernel_dimension':2-J.rank(),'Fourier_amplitude_ratio_at_k11_t1':str(R(22,3))}

print(json.dumps({'python':platform.python_version(),'sympy':S.__version__,
                  'checks_passed':len(checks),'checks':checks,'red_paths':reds,
                  'values':values},indent=2,sort_keys=True))
