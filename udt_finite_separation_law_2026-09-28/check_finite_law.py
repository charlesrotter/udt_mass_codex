"""Exact conditional comparison checks; no physical metric or law is selected."""
import json
import platform
import sympy as S

eta = S.diag(-1, 1, 1, 1)
e0 = S.Matrix([1, 0, 0, 0])
checks = []


def zero(name, value):
    entries = list(value) if isinstance(value, S.MatrixBase) else [value]
    assert all(S.simplify(x) == 0 for x in entries), (name, value)
    checks.append(name)


def boost(gamma, s):
    return S.Matrix.vstack(S.Matrix([[gamma, *s]]),
                           S.Matrix.hstack(s, S.eye(3) + s*s.T/(gamma+1)))


def ray(M, n):
    v = M * S.Matrix([1, *n])
    return v[0], v[1:4, 0]/v[0]


Bx = boost(S.Rational(5, 4), S.Matrix([S.Rational(3, 4), 0, 0]))
By = boost(S.Rational(5, 3), S.Matrix([0, S.Rational(4, 3), 0]))
R = S.Matrix([[1,0,0,0],[0,0,-1,0],[0,1,0,0],[0,0,0,1]])
for name, M in [('Bx', Bx), ('By', By), ('rotation', R), ('product', By*Bx)]:
    zero(name+'_metricity', M.T*eta*M-eta)
    zero(name+'_determinant', M.det()-1)

records = []
for i, n in enumerate([S.Matrix([0,1,0]), S.Matrix([S.Rational(1,3),S.Rational(2,3),S.Rational(2,3)])]):
    f1, n1 = ray(Bx, n)
    f2, n2 = ray(By, n1)
    f, no = ray(By*Bx, n)
    zero(f'case{i}_unit_launch', n.dot(n)-1)
    zero(f'case{i}_unit_arrival', no.dot(no)-1)
    zero(f'case{i}_composition', f-f2*f1)
    zero(f'case{i}_direction', no-n2)
    fi, ni = ray((By*Bx).inv(), no)
    zero(f'case{i}_inversion_factor', f*fi-1)
    zero(f'case{i}_inversion_direction', ni-n)
    c = By*Bx*e0
    Z = c[0]-c[1:4,0].dot(no)
    zero(f'case{i}_clock_contraction', Z-1/f)
    chi = c[1:4,0]/c[0]
    zero(f'case{i}_projective_norm', 1-chi.dot(chi)-1/c[0]**2)
    zero(f'case{i}_projective_readout', c[0]*(1-chi.dot(no))-Z)
    # Insert a different physical intermediate rest frame. Its changes cancel.
    C = By.inv()
    fm1, nm = ray(C*Bx, n)
    fm2, _ = ray(By*C.inv(), nm)
    zero(f'case{i}_middle_frame_cancels', fm1*fm2-f)
    # Passive endpoint chart changes carry clocks as well as k; e0 is not fixed.
    q = S.Matrix([1,*no]); c2=R*c; q2=R*q
    zero(f'case{i}_passive_rotation', (c2.T*eta*q2)[0]-(c.T*eta*q)[0])
    wrong = ray(By,n)[0]*f1
    assert wrong != f
    checks.append(f'case{i}_uncarried_direction_rejected')
    assert c[0] != Z
    checks.append(f'case{i}_gamma_as_redshift_rejected')
    assert ray((By*Bx).inv(),n)[0]*f != 1
    checks.append(f'case{i}_uncarried_inverse_rejected')
    records.append({'launch':list(map(str,n)), 'forward_frequency':str(f),
                    'Z':str(Z), 'wrong_uncarried_frequency':str(wrong),
                    'gamma':str(c[0]), 'direction':list(map(str,no))})

# Exact planar orientation controls, not the full four-dimensional law.
zero('aligned_planar_Z', 1/ray(Bx,S.Matrix([1,0,0]))[0]-S.Rational(1,2))
zero('opposite_planar_Z', 1/ray(Bx,S.Matrix([-1,0,0]))[0]-2)
zero('transverse_Z', 1/ray(Bx,S.Matrix([0,1,0]))[0]-S.Rational(4,5))

# All-regular family with bounded-state norm ->1 but Z identically1.
q = S.symbols('q', positive=True)
gam=1+q*q/2
sp=S.Matrix([q*q/2,q,0])
B=boost(gam,sp)
zero('boundary_family_unit_clock', gam*gam-sp.dot(sp)-1)
zero('boundary_family_metricity', B.T*eta*B-eta)
zero('boundary_family_redshift_one', gam-sp[0]-1)
zero('boundary_family_norm_identity', sp.dot(sp)/gam**2-(1-1/gam**2))
zero('boundary_family_norm_limit', S.limit(sp.dot(sp)/gam**2,q,S.oo)-1)
inverse_ray=S.simplify(B.inv()*S.Matrix([1,1,0,0]))
zero('boundary_family_null_launch', (inverse_ray.T*eta*inverse_ray)[0])
zero('boundary_family_launch_frequency_one', inverse_ray[0]-1)
zero('boundary_family_transport', B*inverse_ray-S.Matrix([1,1,0,0]))

# Approach variable t>0, r=1-t^2. Each example is in |mu|<=1 for small t.
t,C = S.symbols('t C', positive=True)
r=1-t*t
def Z_of(mu):
    return (1-r*mu)/S.sqrt(1-r*r)
zero('aligned_boundary_zero', S.limit(Z_of(1),t,0,dir='+'))
assert S.limit(Z_of(0),t,0,dir='+') == S.oo
checks.append('fixed_transverse_boundary_infinite')
zero('critical_angle_finite', S.limit(Z_of(1-C*t),t,0,dir='+')-C/S.sqrt(2))
zero('faster_angle_zero', S.limit(Z_of(1-t**S.Rational(3,2)),t,0,dir='+'))
assert S.limit(Z_of(1-S.sqrt(t)),t,0,dir='+') == S.oo
checks.append('slower_angle_infinite')
assert S.simplify(gam-sp[0]) == 1 and S.limit(gam,q,S.oo)==S.oo
checks.append('boundary_norm_alone_infinite_claim_rejected')

print(json.dumps({'status':'PASS','evidence':'exact symbolic/rational checks, not a proof census',
                  'python':platform.python_version(),'sympy':S.__version__,
                  'count':len(checks),'checks':checks,'records':records,
                  'fixed_redshift_family':{'gamma':str(gam),'Z':'1','limit_norm_squared':'1'}},indent=2))
