"""NR1 reviewer-owned exact geometry and Laurent checks, no candidate imports.

Frozen before reading parent candidate. Primitive physical wavenumber is symbolic.
The q0-orthonormal frame at fixed T0 is a coordinate rescaling, not a selected scale.
"""
import json
import platform
import sys
import sympy as s

e = s.Symbol('epsilon')
T, kap = s.symbols('T kappa', positive=True)
p, c, u, v, px, cx, ux, vx, pxx, cxx = s.symbols(
    'p c u v px cx ux vx pxx cxx', real=True)
jet = {p: px, c: cx, u: ux, v: vx, px: pxx, cx: cxx}


def tr2(a):
    a = s.expand(a)
    return sum(a.coeff(e, j) * e**j for j in range(3))


def dx(a):
    return s.expand(sum(s.diff(a, key) * val for key, val in jet.items()))


def di(a, i):
    return dx(a) if i == 0 else s.S.Zero


def zero(a):
    return s.expand(a) == 0


checks = []


def check(name, a):
    passed = bool(a)
    checks.append(dict(name=name, passed=passed))
    if not passed:
        raise AssertionError(name)


H = s.Matrix([[0, 0, 0], [0, p, c], [0, c, -p]])
V = s.Matrix([[0, 0, 0], [0, u, v], [0, v, -u]])
q = s.eye(3) + 2 * e * H
qi = s.eye(3) - 2 * e * H + 4 * e**2 * H * H
K0 = s.diag(-1, 2, 2) / (3 * T)
K = K0 + e * (4 * H / (3 * T) + V)
check('inverse_to_second_order', all(zero(tr2(a)) for a in qi*q-s.eye(3)))

G = [[[tr2(sum(qi[a, l] * (di(q[l, j], i) + di(q[l, i], j)
                   - di(q[i, j], l)) / 2 for l in range(3)))
       for j in range(3)] for i in range(3)] for a in range(3)]
Ric = s.zeros(3)
for i in range(3):
    for j in range(3):
        Ric[i, j] = tr2(sum(di(G[a][i][j], a)-di(G[a][i][a], j)
            + sum(G[a][a][b]*G[b][i][j]-G[a][j][b]*G[b][i][a]
                  for b in range(3)) for a in range(3)))
R = tr2(sum(qi[i,j]*Ric[i,j] for i in range(3) for j in range(3)))
Kmixed = (qi*K).applyfunc(tr2)
tau = tr2(s.trace(Kmixed))
Knorm = tr2(s.trace(Kmixed*Kmixed))
Ham = tr2(R+tau*tau-Knorm)
Mom = []
for i in range(3):
    Mom.append(tr2(sum(di(Kmixed[j,i], j)
        + sum(G[j][j][l]*Kmixed[l,i]-G[l][j][i]*Kmixed[j,l]
              for l in range(3)) for j in range(3))-di(tau,i)))

check('background_H_constraint', zero(Ham.coeff(e,0)))
check('background_all_M_constraints', all(zero(a.coeff(e,0)) for a in Mom))
check('first_H_constraint', zero(Ham.coeff(e,1)))
check('first_all_M_constraints', all(zero(a.coeff(e,1)) for a in Mom))
M2 = s.expand(Mom[0].coeff(e,2))
R2 = s.expand(R.coeff(e,2))
H2 = s.expand(Ham.coeff(e,2))
expected_M2 = 4*(p*px+c*cx)/T+2*(px*u+cx*v)+4*(p*ux+c*vx)
expected_R2 = 8*(p*pxx+c*cxx)+6*(px*px+cx*cx)
expected_H2 = expected_R2-2*(u*u+v*v)-8*(p*u+c*v)/(3*T)
check('geometric_M2_vs_hand_argument', zero(M2-expected_M2))
check('geometric_R2_vs_hand_argument', zero(R2-expected_R2))
check('geometric_H2_vs_hand_argument', zero(H2-expected_H2))
check('transverse_quadratic_momenta_vanish', all(zero(a.coeff(e,2)) for a in Mom[1:]))

# Exact Fourier algebra uses Laurent polynomials rather than trigonometric quadrature.
z = s.Symbol('z', nonzero=True)
pc, ps, cc, cs, uc, us, vc, vs = s.symbols('pc ps cc cs uc us vc vs', real=True)
C, S = (z+1/z)/2, (z-1/z)/(2*s.I)
four = {p:pc*C+ps*S,c:cc*C+cs*S,u:uc*C+us*S,v:vc*C+vs*S}
for key, val in jet.items():
    if key in four:
        four[val] = s.I*kap*z*s.diff(four[key],z)


def mode(a, n):
    return s.expand(a.subs(four, simultaneous=True)).coeff(z,n)


meanM = s.expand(mode(M2,0))
meanHV = s.expand(mode(px*u+cx*v,0))
check('exact_mean_M2_is_minus_two_wave_pairing', zero(meanM+2*meanHV))
check('quadratic_forcing_only_zero_and_second_harmonics', all(
    zero(mode(a,1)) and zero(mode(a,-1)) for a in (M2,H2)))

J,Y,Jd,Yd = s.symbols('J Y Jd Yd', real=True)
Ac,As,Bc,Bs,Ec,Es,Fc,Fs = s.symbols('Ac As Bc Bs Ec Es Fc Fs', real=True)
bessel = {pc:Ac*J+Bc*Y,ps:As*J+Bs*Y,uc:Ac*Jd+Bc*Yd,us:As*Jd+Bs*Yd,
          cc:Ec*J+Fc*Y,cs:Es*J+Fs*Y,vc:Ec*Jd+Fc*Yd,vs:Es*Jd+Fs*Yd}
Dplus, Dcross = Ac*Bs-As*Bc, Ec*Fs-Es*Fc
D = Dplus+Dcross
W = J*Yd-Jd*Y
meanBessel = s.expand(meanM.subs(bessel))
check('all_eight_constants_charge', zero(meanBessel-kap*W*D))

# Direct finite-dimensional full-constraint right inverse, arbitrary output target.
h,m1,m2,m3 = s.symbols('h m1 m2 m3')
L = s.Matrix([[s.Rational(8,3)/T,s.Rational(2,3)/T,0,0],
              [0,-s.I*kap,0,0],[0,0,s.I*kap,0],[0,0,0,s.I*kap]])
target=s.Matrix([h,m1,m2,m3])
right=s.Matrix([3*T*h/8-m1*s.I/(4*kap),m1*s.I/kap,m2/(s.I*kap),m3/(s.I*kap)])
check('full_axial_nonzero_constraint_right_inverse', all(zero(a) for a in L*right-target))
check('nonzero_frequency_rank4', s.factor(L.det()) != 0)
check('mean_Hamiltonian_adjustable', s.Rational(8,3)/T != 0)

# Actual controls reintroduce defects and require the corresponding predicate false.
mutations=[]


def reject(name, predicate):
    caught=not bool(predicate)
    mutations.append(dict(name=name, caught=caught))
    if not caught:
        raise AssertionError('false pass: '+name)


reject('omit_connection_and_inverse_corrections', zero(M2-(2*(px*u+cx*v))))
reject('reverse_velocity_derivative_term', zero(M2-(expected_M2-8*(p*ux+c*vx))))
reject('omit_cross_polarization_charge', zero(meanBessel-kap*W*Dplus))
reject('lose_Wronskian_orientation', zero(meanBessel+kap*W*D))
reject('discard_Hamiltonian_corrector', (L[:,1:]).rank()==4)
reject('discard_transverse_momentum_corrector', L[:,[0,1,2]].rank()==4)
balanced={Ac:1,As:0,Bc:0,Bs:1,Ec:0,Es:1,Fc:1,Fs:0}
check('balanced_nonzero_polarization_charges_survive', D.subs(balanced)==0)
reject('require_each_polarization_charge_zero',
       Dplus.subs(balanced)==0 and Dcross.subs(balanced)==0)
unbalanced={Ac:1,As:0,Bc:0,Bs:1,Ec:0,Es:0,Fc:0,Fs:0}
reject('universal_realisability_of_eight_constants', D.subs(unbalanced)==0)
check('standing_profile_zero_charge', D.subs({As:0,Bs:0,Es:0,Fs:0})==0)

print(json.dumps(dict(kind='NR1_REVIEW_INDEPENDENT_EXACT_ADM_AND_LAURENT',
    model='UNKNOWN',python=sys.version,sympy=s.__version__,platform=platform.platform(),
    symbolic_geometry=dict(q_shape=[3,3],K_shape=[3,3],epsilon_order=2,
        momenta=[str(s.expand(a.coeff(e,2))) for a in Mom],
        scalar_curvature=str(R2),hamiltonian=str(H2),mean_momentum=str(meanM),
        bessel_mean_momentum=str(s.factor(meanBessel)),right_inverse_det=str(s.factor(L.det()))),
    checks=checks,mutations=mutations,all_passed=all(a['passed'] for a in checks)
       and all(a['caught'] for a in mutations)),indent=2))
