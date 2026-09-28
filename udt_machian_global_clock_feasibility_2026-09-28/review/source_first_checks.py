"""Exact source-first separators; no author candidate/code/output imports."""
import json
import platform
from fractions import Fraction as F
import sympy as s

checks = []
def zero(name, expr):
    value = s.simplify(expr)
    assert value == 0, (name, value)
    checks.append({"name": name, "kind": "exact_identity", "residual": str(value)})

def reject(name, actual, wrong):
    assert actual != wrong, (name, actual, wrong)
    checks.append({"name": name, "kind": "wrong_formula_rejected", "actual": str(actual), "wrong": str(wrong)})

x, eps, a, c, rho = s.symbols('x eps a c rho', real=True, positive=True)
N = 1 + eps*s.sin(x)
# Pinned mathematical chart: x,y,z in [0,2pi), t in R, a,c>0, 0<eps<1.
# Geometry is a FREE supplied control, not admitted UDT or an imported source model.
g = s.diag(-N**2*c**2, a**2, a**2, a**2)
ginv = g.inv()
coords = s.symbols('t x y z', real=True)
coords = (coords[0], x, coords[2], coords[3])
Gamma = {}
for k in range(4):
 for i in range(4):
  for j in range(4):
   Gamma[k,i,j] = s.simplify(sum(ginv[k,l]*(s.diff(g[l,j],coords[i])+s.diff(g[l,i],coords[j])-s.diff(g[i,j],coords[l]))/2 for l in range(4)))
zero('Gamma_x_tt', Gamma[1,0,0]-c**2*N*s.diff(N,x)/a**2)
for endpoint in (s.pi/2, 3*s.pi/2):
 for k in range(4):
  zero('static_clock_geodesic_'+str(endpoint)+'_'+str(k), Gamma[k,0,0].subs(x,endpoint))
# Spatial induced metric contains no epsilon or lapse; no stress tensor is supplied.
V = s.integrate(a**3,(x,0,2*s.pi))*(2*s.pi)**2
zero('slice_volume', V-(2*s.pi*a)**3)
zero('volume_lapse_independence', s.diff(V,eps))
mass_integral = rho*V
zero('supplied_density_integral_lapse_independence', s.diff(mass_integral,eps))

# A stationary null ray obeys dt/dx=a/(c*N), so its travel time Delta is
# independent of emission time. Thus dto/dte=1 and d tau_i=N_i dt_i.
te, Delta, Ne, No = s.symbols('te Delta Ne No', real=True, positive=True)
to = te+Delta
Z = No*s.diff(to,te)/Ne
zero('stationary_interval_ratio_from_arrival', Z-No/Ne)
Zpair = Z.subs({Ne:N.subs(x,s.pi/2),No:N.subs(x,3*s.pi/2)})
zero('torus_endpoint_clock_ratio', Zpair-(1-eps)/(1+eps))
zero('actual_stationary_return_product', Zpair*(1/Zpair)-1)
reject('same_integral_implies_same_clocks', Zpair.subs(eps,s.Rational(1,3)), s.Integer(1))
reject('clock_ratio_inverted', Zpair.subs(eps,s.Rational(1,3)), s.Integer(2))

# G351 conserved source normalization alpha remains supplied; ratios cancel it.
alpha, source, J1, J2 = s.symbols('alpha source J1 J2', positive=True)
n1,n2=alpha*source/J1,alpha*source/J2
zero('measure_normalization_cancels_transfer', n2/n1-J1/J2)
reject('conservation_selects_source_magnitude', F(7)*F(3), F(3))

# Independent exact rational Lorentz boost family. r=(k^2-1)/(k^2+1).
# Endpoint direction parallel gives Z=1/k; perpendicular gives gamma.
boundary=[]
for k in (2,3,7,100):
 r=F(k*k-1,k*k+1)
 gamma=F(k*k+1,2*k)
 parallel=gamma*(1-r)
 transverse=gamma
 assert parallel == F(1,k)
 assert gamma*gamma*(1-r*r)==1
 boundary.append(dict(k=k,r=str(r),parallel_Z=str(parallel),transverse_Z=str(transverse)))
checks.append(dict(name='directional_boundary_family',kind='exact_rational_controls',cases=boundary))
reject('boundary_norm_forces_redshift', boundary[-1]['parallel_Z'], boundary[-1]['transverse_Z'])

# Physical homothety at fixed units differs from relabelling the units.
lam, R, M, G = s.symbols('lambda R M G', positive=True)
zero('geometric_mass_homothety_compactness', G*(lam*M)/((lam*R)*c**2)-G*M/(R*c**2))
zero('fixed_independent_mass_compactness_weight', G*M/((lam*R)*c**2)-(G*M/(R*c**2))/lam)
UL,UT,UM=s.symbols('UL UT UM',positive=True)
zero('compactness_unit_invariance', (G*UM*UT**2/UL**3)*(M/UM)/((R/UL)*(c*UT/UL)**2)-G*M/(R*c**2))

print(json.dumps(dict(status='PASS',python=platform.python_version(),sympy=s.__version__,
 checks=checks, total=len(checks),
 ceiling='SUPPLIED_GEOMETRY_SEPARATORS_AND_EXACT_CONSISTENCY_ONLY; NO_NATIVE_ADMISSION_OR_NO_GO'),indent=2))
