"""CES1 reviewer algebra; no producer code imported. See SOURCE_FIRST.md."""
import json
import platform
from pathlib import Path
import sympy as S

out = Path(__file__).resolve().parent / "INDEPENDENT_RESULT.json"
assert not out.exists(), "Preserve prior check outputs"
passed = []
rejected = []

def equal(name, lhs, rhs):
    difference = S.simplify(lhs - rhs)
    assert difference == 0, (name, difference)
    passed.append(name)

def reject(name, wrong, correct):
    difference = S.simplify(wrong - correct)
    assert difference != 0, (name, "vacuous mutation")
    rejected.append({"name": name, "nonzero_difference": str(difference)})

eps, t, r = S.symbols("epsilon t r", real=True)
f = S.Function("f")(t, r)
w = S.symbols("w", positive=True)
g = S.diag(-S.exp(-2*eps*f), S.exp(2*eps*f))
k = S.Matrix([S.exp(2*eps*f)*w, w])
equal("exact_radial_null_constraint", (k.T*g*k)[0], 0)
equal("exact_radial_determinant", g.det(), -1)
equal("momentum_time_component", (g*k)[0], -w)
pdot_t = (k.T*g.diff(t)*k)[0] / 2
equal("covariant_geodesic_momentum_equation", pdot_t,
      2*eps*S.diff(f,t)*S.exp(2*eps*f)*w**2)
dlogw_dr = -pdot_t / w**2
equal("frequency_first_variation_density",
      S.diff(dlogw_dr,eps).subs(eps,0), -2*S.diff(f,t))
h = g.diff(eps).subs(eps,0)
equal("covariant_strain_factor_two", h[0,0], 2*f)
equal("reciprocal_radial_component", h[1,1], 2*f)
equal("reciprocal_metric_trace", S.trace(g.subs(eps,0).inv()*h), 0)

s, L, v, B0, B1 = S.symbols("s L v B0 B1", real=True)
gamma = S.symbols("gamma", positive=True)
d = S.Function("Delta")(s)
arrival = S.solve(S.Symbol("T") - (s+L+v*S.Symbol("T")+d), S.Symbol("T"))[0]
equal("moving_receiver_exact_intersection", arrival, (s+L+d)/(1-v))
delay = 2*(s*B0+B1)
arrival_var = S.diff(arrival,d)*delay
equal("moving_receiver_first_variation", arrival_var, delay/(1-v))
Z0 = S.diff(arrival.subs(d,0),s)/gamma
equal("proper_receiver_normalization", Z0, 1/(gamma*(1-v)))
Zvar = S.diff(arrival_var,s)/gamma
equal("fractional_clock_response", Zvar/Z0, 2*B0)

# Algebraic rapidity variable z=exp(eta)>1 keeps controls exact.
z = S.symbols("z", positive=True)
velocity = (z**2-1)/(z**2+1)
lorentz = (z+1/z)/2
equal("rapidity_to_unit_velocity", lorentz**2*(1-velocity**2), 1)
equal("baseline_received_Doppler_ratio", Z0.subs({v:velocity,gamma:lorentz}), z)

R = (L+v*s)/(1-v)
I = 2*R*(s*B0+B1)
omega_o = R*gamma*(1-v)
Vcoordinate = I/((1/gamma)*omega_o)
equal("FCV1_coordinate_arrival", Vcoordinate, arrival_var)
equal("FCV1_proper_arrival", I/omega_o, arrival_var/gamma)
equal("FCV1_full_Q_coordinate_label", S.diff(Vcoordinate,s)/(1/(1-v)), 2*B0)
equal("FCV1_full_Q_proper_label", S.diff(I/omega_o,s)/Z0, 2*B0)

eta, mean_eta = S.symbols("eta mean_eta", positive=True)
per_query_derivative = S.diff((eta+eps*2*B0)**2/2,eps).subs(eps,0)
equal("squared_contrast_chain_rule", per_query_derivative, 2*eta*B0)
equal("fixed_measure_mean_derivative", per_query_derivative.subs(eta,mean_eta), 2*B0*mean_eta)

# Polynomial control is not a smooth compact-support certification.
x = S.symbols("x", real=True)
polynomial = x**2*(1-x)**2
B0_control = S.integrate(polynomial,(x,0,1))
B1_control = S.integrate(x*polynomial,(x,0,1))
equal("polynomial_B0_control", B0_control, S.Rational(1,30))
equal("polynomial_B1_control", B1_control, S.Rational(1,60))
equal("original_null_ODE_integral_control",
      S.integrate(2*(s+x)*polynomial,(x,0,1)), s/S.Integer(15)+S.Rational(1,30))

control = {s:S.Rational(3,2),L:3,v:S.Rational(3,5),gamma:S.Rational(5,4),
           B0:S.Rational(1,30),B1:S.Rational(1,60),eta:S.Rational(2,3)}
reject("omitted_receiver_intersection_motion", delay.subs(control), arrival_var.subs(control))
reject("omitted_proper_clock_normalization", S.diff(arrival.subs(d,0),s).subs(control), Z0.subs(control))
reject("wrong_null_momentum_sign", -2*B0_control, 2*B0_control)
reject("missing_reciprocal_factor_two", B0_control, 2*B0_control)
reject("falsely_stationary_contrast", S.Integer(0), per_query_derivative.subs(control))
reject("inverse_Doppler_for_received_ratio", S.Rational(1,2), Z0.subs(control))

result = {
    "status": "PASS",
    "evidence_type": "exact symbolic algebra controls; analytic support proof in SOURCE_FIRST.md",
    "python": platform.python_version(), "sympy": S.__version__,
    "identities_passed": len(passed), "identities": passed,
    "wrong_formulas_rejected": len(rejected), "rejections": rejected,
    "derived_response": "delta log Z = 2 B0; delta C = 2 B0 mean_eta > 0 in frozen positive-rapidity class",
    "omissions": "No numerical bump integration, PDE, locality analysis, full source reproof, empirical or adoption claim."
}
out.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
