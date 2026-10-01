"""Finite algebraic control of the PSW1 prepared-clock curvature coefficient.

Supplied local metric, not a native UDT field. CPU only; no evolution/ray search.
The proof in SOURCE_FIRST.md, rather than these regression checks, owns scope.
"""
import json
import platform
import sympy as S

q, x, t, L, s, eps = S.symbols('q x t L s eps', real=True)
coords = (t, x)
g = S.diag(-(1+q*x*x), 1)
gi = g.inv()
Gamma = [[[S.simplify(sum(gi[a,d]*(S.diff(g[d,c],coords[b])+
             S.diff(g[d,b],coords[c])-S.diff(g[b,c],coords[d]))/2
             for d in range(2))) for c in range(2)] for b in range(2)] for a in range(2)]
def R(a,b,c,d):
    return S.simplify(S.diff(Gamma[a][d][b],coords[c])-
        S.diff(Gamma[a][c][b],coords[d])+
        sum(Gamma[a][c][e]*Gamma[e][d][b]-
            Gamma[a][d][e]*Gamma[e][c][b] for e in range(2)))

checks=[]
def equal(name, value, expected):
    residual=S.simplify(value-expected)
    if residual != 0:
        raise AssertionError((name, residual))
    checks.append(dict(name=name, value=str(value), expected=str(expected)))
def scaled(expr, order):
    return S.series(expr.subs({L:eps*L,t:eps*t,s:eps*s}),eps,0,order).removeO().expand()

equal('electric_curvature_at_origin', (g[0,0]*R(0,1,0,1)).subs(x,0),q)
receiver=L-q*L*t*t/2
velocity=S.diff(receiver,t)
coordinate_geodesic=S.diff(receiver,t,2)+q*receiver-2*q*receiver/(1+q*receiver**2)*velocity**2
equal('receiver_coordinate_geodesic_residual_below_degree_three',scaled(coordinate_geodesic,3),0)
equal('receiver_initial_position',receiver.subs(t,0),L)
equal('receiver_initial_radial_velocity',velocity.subs(t,0),0)

optical=x-q*x**3/6
equal('null_travel_derivative_through_quadratic',S.series(S.diff(optical,x)-(1+q*x*x)**S.Rational(-1,2),x,0,4).removeO(),0)
T=s+L-q*L*(s+L)**2/2-q*L**3/6
arrival_residual=T-s-optical.subs(x,receiver.subs(t,T))
equal('moving_receiver_null_arrival_through_cubic',scaled(arrival_residual,4),0)
tau=t+q*L*L*t/2
proper_rate=S.sqrt(1+q*receiver**2-velocity**2)
equal('proper_clock_rate_through_quadratic',scaled(S.diff(tau,t)-proper_rate,3),0)
A=S.expand(tau.subs(t,T))
Z=S.diff(A,s).subs(s,0)
Z2=S.series(Z,L,0,3).removeO()
equal('actual_arrival_derivative',Z2,1-q*L**2/2)
equal('log_shift_quadratic',S.series(S.log(Z),L,0,3).removeO(),-q*L**2/2)
equal('single_proper_flight_time_is_different',S.series(A.subs(s,0),L,0,4).removeO(),L-q*L**3/6)

# Independent endpoint-frequency expression for this static control.
N2_at_arrival=1+q*receiver.subs(t,T.subs(s,0))**2
v_at_arrival=velocity.subs(t,T.subs(s,0))
freq_ratio=(1-v_at_arrival/S.sqrt(N2_at_arrival))/S.sqrt(N2_at_arrival-v_at_arrival**2)
equal('endpoint_frequency_ratio',S.series(1/freq_ratio,L,0,3).removeO(),Z2)
fixed_receiver=S.series(S.sqrt(1+q*L*L),L,0,3).removeO()
equal('fixed_receiver_wrong_sign_gap',fixed_receiver-Z2,q*L*L)
e1,e2,e3=S.symbols('e1 e2 e3',real=True)
equal('six_axis_quadratic_average',sum(-e*L**2/2 for e in (e1,e1,e2,e2,e3,e3))/6,-(e1+e2+e3)*L**2/6)
equal('tracefree_directional_example_average',sum(-e*L**2/2 for e in (-2,1,1))/3,0)

print(json.dumps(dict(status='PASS',python=platform.python_version(),sympy=S.__version__,
    scope='Exact polynomial jets in a supplied local static product metric; no native or finite-distance claim',
    checks=checks),indent=2))
