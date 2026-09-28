"""Exact controls; analytic hypotheses/proofs remain in INITIAL_CANDIDATE."""
import json
import platform
import sympy as s

checks = {}
wrong = {}

def equal(name, a, b=0):
    residual = s.simplify(a-b)
    assert all(v == 0 for v in residual) if isinstance(residual, s.MatrixBase) else residual == 0, (name, residual)
    checks[name] = str(s.simplify(a))

def reject(name, a, b=0):
    residual = s.simplify(a-b)
    assert residual != 0 and residual.is_zero is False, (name, residual)
    wrong[name] = str(residual)

# Differentiate actual nonlinear outward/return maps, including shifted argument.
u = s.symbols('u', positive=True)
b = s.symbols('b', positive=True)
c = s.symbols('c', positive=True)
f = u+u**2
g = b**3+b+4
F = g.subs(b, f)
p = s.diff(f, u)
q = s.diff(g, b).subs(b, f)
P = s.diff(F, u)
T, R = (u+F)/2, c*(F-u)/2
equal('actual_echo_chain', P, p*q)
equal('radar_derivative', s.diff(R,u)/s.diff(T,u)/c, (P-1)/(P+1))
equal('radar_inverse_product', (1+(P-1)/(P+1))/(1-(P-1)/(P+1)), P)
equal('positive_radar_time_derivative', s.diff(T,u), (1+P)/2)
reject('wrong_inverse_in_place_of_return', P.subs(u,1), 1)
reject('wrong_return_argument', P.subs(u,1), (p*s.diff(g,b).subs(b,u)).subs(u,1))
relay = b+b**2/5
Fl = g.subs(b,relay.subs(b,f))
equal('latency_chain', s.diff(Fl,u), p*s.diff(relay,b).subs(b,f)*s.diff(g,b).subs(b,relay.subs(b,f)))
reject('omit_latency_derivative', s.diff(Fl,u).subs(u,1), (p*s.diff(g,b).subs(b,relay.subs(b,f))).subs(u,1))

# Metric value and radar speed from two separately recorded slopes.
o, d = s.symbols('Omega D', positive=True)
beta = (d**2-1)/(d**2+1)
root = s.simplify(s.sqrt(1-beta**2))
p0, q0 = o*d, d/o
equal('proper_clock_outgoing', o*root/(1-beta), p0)
equal('proper_clock_incoming', (1+beta)/(o*root), q0)
equal('metric_factor_ratio', s.sqrt(p0/q0), o)
equal('echo_tanh_exponential_form', (p0*q0-1)/(p0*q0+1), beta)
assert s.Rational(1,2)<1 and 3>1 and s.Rational(1,2)*3>1
checks['one_blue_positive_radar_drift'] = 'p=1/2,q=3,beta=1/5'

# Full Christoffel calculation on the declared totally geodesic product control.
t,x,y,z = s.symbols('t x y z', real=True)
k,a,v = s.symbols('k a v', real=True)
coords = [t,x,y,z]
phi = (k+a*t)*x**2
Omega = s.exp(phi)
metric = s.diag(-c**2*Omega**2, Omega**2, 1, 1)
inv = metric.inv()
def connection(g, gi):
    return [[[s.simplify(sum(gi[i,m]*(s.diff(g[m,l],coords[j])+s.diff(g[m,j],coords[l])-s.diff(g[j,l],coords[m])) for m in range(4))/2) for l in range(4)] for j in range(4)] for i in range(4)]
G = connection(metric,inv)
V = [1,c*v,0,0]
acc = [s.simplify(sum(G[i][j][l]*V[j]*V[l] for j in range(4) for l in range(4))) for i in range(4)]
vdot_original = s.simplify(-(acc[1]-c*v*acc[0])/c)
equal('original_geodesic_radar_acceleration', vdot_original, -(1-v**2)*(c*s.diff(phi,x)+v*s.diff(phi,t)))
equal('transverse_geodesic_y', acc[2])
equal('transverse_geodesic_z', acc[3])
equal('reference_proper_clock', Omega.subs(x,0),1)
equal('reference_free_fall', G[1][0][0].subs(x,0))
Sdot = s.simplify(vdot_original/(1-v**2))
Kdot = s.diff(phi,t)+c*v*s.diff(phi,x)
equal('reconstruct_time_gradient', (Kdot+v*Sdot)/(1-v**2),s.diff(phi,t))
equal('reconstruct_space_gradient', (-Sdot-v*Kdot)/(1-v**2),c*s.diff(phi,x))
reject('drop_geodesic_sign', (Sdot-c*s.diff(phi,x)-v*s.diff(phi,t)).subs({t:1,x:2,c:1,k:1,a:1,v:s.Rational(1,3)}))
# A local free B at a turning point is not an eternally stationary clock.
equal('turning_point_radar_acceleration', vdot_original.subs({a:0,v:0}),-2*c*k*x)
equal('turning_point_ratio_product', (p0*q0).subs(d,1),1)

# Exact inertial pair: derive incidence from straight null paths.
L = s.symbols('L',positive=True)
vb = s.Rational(3,5)
gam = 1/s.sqrt(1-vb**2)
f_flat = (u+L/c)/(gam*(1-vb))
g_flat = gam*(1+vb)*b+L/c
F_flat = s.simplify(g_flat.subs(b,f_flat))
T_flat, R_flat = (u+F_flat)/2,c*(F_flat-u)/2
equal('inertial_outgoing_ratio',s.diff(f_flat,u),2)
equal('inertial_return_ratio',s.diff(g_flat,b),2)
equal('inertial_radar_trajectory', R_flat,L+vb*c*T_flat)
equal('inertial_ordinary_proper_time',gam**2*(1-vb**2),1)

# Third-clock direct vs relay: positive causal delay has no fixed derivative sign.
for vel in [s.Rational(1,5),-s.Rational(1,5)]:
    gamma = 1/s.sqrt(1-vel**2)
    direct = (u+1)/(gamma*(1-vel))
    route = (u+3)/(gamma*(1+vel))
    delta = s.simplify(route-direct)
    equal('triangle_delay_derivative_'+str(vel),s.diff(delta,u),-2*gamma*vel)
    assert delta.subs(u,0)>0
    checks['positive_delay_'+str(vel)] = str(delta.subs(u,0))
    reject('wrong_equal_direct_relay_'+str(vel),delta.subs(u,0))

# Four-dimensional conformal curvature from original Christoffel/Ricci definition.
# This polynomial is ONLY the local patch inside a smooth cutoff, not the global
# compact construction. The analytic proof owns unchanged clock neighborhoods.
x0 = s.Rational(1,2)
psi = k*(x-x0)**2
cg = s.exp(2*psi)*s.diag(-1,1,1,1)
cgi = cg.inv()
CG = connection(cg,cgi)
Ric = s.zeros(4)
for i in range(4):
    for j in range(4):
        Ric[i,j] = s.simplify(sum(s.diff(CG[m][i][j],coords[m])-s.diff(CG[m][i][m],coords[j])+sum(CG[m][m][n]*CG[n][i][j]-CG[m][j][n]*CG[n][i][m] for n in range(4)) for m in range(4)))
scalar = s.simplify(sum(cgi[i,j]*Ric[i,j] for i in range(4) for j in range(4)))
equal('interior_conformal_curvature',scalar.subs(x,x0),-12*k)
ell = [1,1,0,0]
nullacc = [s.simplify(sum(CG[i][j][m]*ell[j]*ell[m] for j in range(4) for m in range(4))) for i in range(4)]
for i in range(4): equal('conformal_null_pregeodesic_'+str(i),nullacc[i],2*s.diff(psi,x)*ell[i])
reject('wrong_conformal_invariance_of_scalar',scalar.subs({x:x0,k:1}),0)

# Dimensional solvability, including why another measured dimensional datum helps.
dim = s.Matrix([[1,3],[-1,-2],[0,-1]]) # columns c,G; rows L,T,M
equal('dimension_rank',dim.rank(),2)
for label,target in [('length',s.Matrix([1,0,0])),('time',s.Matrix([0,1,0]))]:
    assert dim.row_join(target).rank()==3
    checks['no_cG_only_'+label] = 'augmented rank3 > rank2'
equal('mass_length_dimensions',dim*s.Matrix([-2,1])+s.Matrix([0,0,1]),s.Matrix([1,0,0]))
equal('density_length_dimensions',dim*s.Matrix([1,-s.Rational(1,2)])-s.Matrix([-3,0,1])/2,s.Matrix([1,0,0]))
equal('measured_duration_length',dim*s.Matrix([1,0])+s.Matrix([0,1,0]),s.Matrix([1,0,0]))

# Boundary and controlled local expansion controls (not physical populations).
n = s.symbols('n',positive=True)
equal('beta_boundary_one_leg_blue',s.limit((n-1)/(n+1),n,s.oo),1)
equal('blue_return_limit',s.limit(1/n,n,s.oo),0)
reject('wrong_boundary_forces_both_divergent',s.limit(1/n,n,s.oo),1)
equal('nearby_metric_has_no_linear_term',s.diff(phi,x).subs(x,0))
equal('nearby_quadratic_coefficient',s.diff(phi,x,2).subs(x,0)/2,k+a*t)
print(json.dumps({'status':'PASS','python':platform.python_version(),'sympy':s.__version__,'exact_identities_and_controls':len(checks),'wrong_rules_rejected':len(wrong),'checks':checks,'wrong_rule_residuals':wrong,'limits':'Exact controls are not proof of general metric admission, global asymptote or observational precision.'},indent=2))
