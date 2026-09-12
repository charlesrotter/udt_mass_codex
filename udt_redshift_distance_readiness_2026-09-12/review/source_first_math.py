"""Source-first documentary controls; no parent science/code/output imports.

Question: independently reconstruct sign, finite-duration and conditional flux joins.
Supplied metrics and conventional packet bookkeeping are controls, not physical laws.
CPU-only, one thread, symbolic/exact arithmetic; 180 seconds / 2 GiB via capture_existing.
"""
import json
import platform
import sympy as s

eta, L = s.symbols('eta L', positive=True)
# Conformal metric g=eta^2(-deta^2+dx^2+dy^2+dz^2), fixed x endpoints.
# Null incidence is eta_o=eta_e+L, while proper time primitive is eta^2/2.
tau_e = eta**2/2
tau_o = (eta+L)**2/2
Z = s.cancel(s.diff(tau_o,eta)/s.diff(tau_e,eta))
dt_e = tau_e.subs(eta,2)-tau_e.subs(eta,1)
dt_o = (tau_o.subs(eta,3-1)-tau_o.subs(eta,1)).subs(L,1)
duration_integral = s.integrate(Z*s.diff(tau_e,eta),(eta,1,2)).subs(L,1)
assert dt_e==s.Rational(3,2) and dt_o==s.Rational(5,2)
assert duration_integral==dt_o
assert Z.subs({eta:1,L:1})*dt_e==3 and dt_o!=3

# Static primary metric: along an outward radial ray, dt=e^(2 phi)dr.
# Stationarity makes its coordinate travel time independent of emission time.
# Proper-time lapse is exp(-phi); normalized congruence has U^t=exp(phi).
r, th = s.symbols('r th', positive=True)
phi=s.Function('phi')(r)
sqrt_abs_det_g=r**2*s.sin(th)
# U^r=U^theta=U^varphi=0, every metric coefficient is time independent.
static_expansion=s.Integer(0)
phi_e,phi_o=s.symbols('phi_e phi_o', real=True)
static_clock_ratio=s.exp(-phi_o)/s.exp(-phi_e)
static_frequency_ratio=s.exp(phi_e)/s.exp(phi_o)
assert s.simplify(static_clock_ratio/static_frequency_ratio)==1

# Conditional conventional packet accounting, not a consequence of G352.
# Source emits energy Lum*dte, count=(Lum*dte)/Ee; isotropic fraction is
# dOmega_e/(4 pi), dOmega_e=dAo/Dg^2; each arrival has Eo=Ee/Zeta.
Lum,dte,Ee,dAo,Dg,Zeta,Da=s.symbols('Lum dte Ee dAo Dg Zeta Da',positive=True)
N_emit=Lum*dte/Ee
N_detect=N_emit*dAo/(4*s.pi*Dg**2)
received_energy=N_detect*Ee/Zeta
observed_flux=s.cancel(received_energy/(Zeta*dte*dAo))
flux_with_reciprocity=s.cancel(observed_flux.subs(Dg,Zeta*Da))
luminosity_distance=s.sqrt(s.cancel(Lum/(4*s.pi*flux_with_reciprocity)))
assert luminosity_distance==Da*Zeta**2

# G280 source-control: derive transverse equations from the Brinkmann metric,
# then solve their independent initial-value solutions analytically.
u,v,x,y,a,lam=s.symbols('u v x y a lam', real=True)
g=s.Matrix([[a*(x*x-y*y),-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
gi=g.inv();q=[u,v,x,y]
gamma_uu=[s.simplify(sum(gi[j,d]*(2*s.diff(g[d,0],u)-s.diff(g[0,0],q[d])) for d in range(4))/2) for j in range(4)]
aa=s.symbols('aa',positive=True)
Bx=s.sinh(s.sqrt(aa)*lam)/s.sqrt(aa)
By=s.sin(s.sqrt(aa)*lam)/s.sqrt(aa)
assert gamma_uu[2]==-a*x and gamma_uu[3]==a*y
assert s.simplify(s.diff(Bx,lam,2)-aa*Bx)==0
assert s.simplify(s.diff(By,lam,2)+aa*By)==0
assert Bx.subs(lam,0)==By.subs(lam,0)==0
assert s.diff(Bx,lam).subs(lam,0)==s.diff(By,lam).subs(lam,0)==1
relative_area=s.series(Bx*By/lam**2,lam,0,9)
assert s.expand(relative_area.removeO()).coeff(lam,4)==-aa**2/s.Integer(90)

print(json.dumps({
 'evidence_type':'symbolic and exact arithmetic controls, not empirical or general proof',
 'python':platform.python_version(),'sympy':s.__version__,
 'conformal_clock_ratio':str(Z),'finite_source_duration':str(dt_e),
 'finite_observer_duration':str(dt_o),'integrated_clock_ratio':str(duration_integral),
 'wrong_first_epoch_constant_prediction':'3',
 'static_observer_expansion':str(static_expansion),
 'static_clock_ratio':str(s.simplify(static_clock_ratio)),
 'conditional_packet_flux':str(observed_flux),
 'conditional_flux_after_metric_reciprocity':str(flux_with_reciprocity),
 'conditional_luminosity_distance':str(luminosity_distance),
 'plane_wave_transverse_connection':str(gamma_uu[2:]),
 'plane_wave_relative_area_series':str(relative_area),
 'status':'PASS'
},indent=2))
