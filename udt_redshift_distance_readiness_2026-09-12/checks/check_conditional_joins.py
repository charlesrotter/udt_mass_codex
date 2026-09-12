"""Exact ZDR1 join anchors; no source imports, fit, data, or whole-theory certification."""
from datetime import datetime, timezone
import json
import platform
import sympy as sp

s, T, D, Z0, eps = sp.symbols('s T D Z0 eps', positive=True)
Z = Z0*(1+eps*s/T)
v = 2*D+Z0**2*(s+eps*s**2/T+eps**2*s**3/(3*T**2))
t, x = (v+s)/2, (v-s)/2
dt, dx = sp.diff(t,s), sp.diff(x,s)
eta = sp.diag(-1,1,1,1)
U = sp.Matrix([dt/Z,dx/Z,0,0])
k = sp.Matrix([1,1,0,0])
omega_o = sp.factor(-(U.T*eta*k)[0])
eqs = {
    'null_incidence': sp.factor((t-s)**2-x**2),
    'proper_time_norm': sp.factor((U.T*eta*U)[0]+1),
    'proper_clock_jacobian_squared': sp.factor(dt**2-dx**2-Z**2),
    'observed_frequency': sp.factor(omega_o-1/Z),
    'finite_duration': sp.factor(sp.integrate(Z,(s,0,T))-Z0*T*(1+eps/2)),
}
assert all(value==0 for value in eqs.values()),eqs
values={Z0:2,eps:sp.Rational(1,5),T:1,D:1}
duration=sp.integrate(Z,(s,0,T)).subs(values)
point_only=(Z0*T).subs(values)
fractional=sp.factor(duration/point_only-1)
assert duration==sp.Rational(11,5) and point_only==2
assert fractional==sp.Rational(1,10) and fractional<values[eps]

# Direct energy accounting keeps photon number, proper time, area, energy distinct.
Le,Ee,ze,dt_e,dOm,AA = sp.symbols('Le Ee Z dt_e dOmega A_eo',positive=True)
Ao=ze**2*AA
number=Le*dt_e*dOm/(4*sp.pi*Ee)
Fo=sp.factor(number*(Ee/ze)/((ze*dt_e)*(Ao*dOm)))
luminosity_distance_squared=sp.factor(Le/(4*sp.pi*Fo))
assert luminosity_distance_squared==ze**4*AA
count_only=sp.factor(number*Ee/((ze*dt_e)*(Ao*dOm)))
wrong_distance_squared=sp.factor(Le/(4*sp.pi*count_only))
assert wrong_distance_squared==ze**3*AA
assert sp.factor((wrong_distance_squared-luminosity_distance_squared).subs({ze:2,AA:3}))==-24

# Work in log coordinates to verify coefficient/area-versus-distance typing.
f,a,z,l=sp.symbols('logF logdA logZ logL',real=True)
closure=sp.log(4*sp.pi)+f+2*a+4*z-l
coefficients=[sp.diff(closure,q) for q in (f,a,z,l)]
assert coefficients==[1,2,4,-1]

# Exact finite arrival map at eps=0 includes the constant-redshift limit.
assert sp.factor(sp.integrate(Z.subs(eps,0),(s,0,T))-Z0*T)==0

result={
    'checked_utc':datetime.now(timezone.utc).isoformat(),
    'python':platform.python_version(),'sympy':sp.__version__,
    'purpose':__doc__,'pass':True,
    'exact_symbolic_identities':{name:str(value) for name,value in eqs.items()},
    'rational_actual_metric_control':{'Z0':'2','epsilon':'1/5','T':'1','D':'1',
        'observer_duration':str(duration),'initial_redshift_times_duration':str(point_only),
        'relative_difference':str(fractional),'uniform_bound':'1/5'},
    'flux_expression':str(Fo),'dL_squared':str(luminosity_distance_squared),
    'omitted_energy_factor_control':str(wrong_distance_squared),
    'log_closure_coefficients':list(map(str,coefficients)),
    'negative_controls':[
        'Initial endpoint Z0 alone fails to equal the exact finite interval when epsilon=1/5',
        'Omitting received energy redshift yields Z^3 A_eo, different from bolometric Z^4 A_eo'],
    'limits':'Exact algebra and one supplied flat metric/observer control; no physics identification, error-bound certification, source theorem replay, dataset, fit, or native cosmic model.'}
print(json.dumps(result,indent=2))
