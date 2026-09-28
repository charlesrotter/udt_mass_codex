#!/usr/bin/env python3
"""Independent source-first exact controls; no author script imports."""
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import sympy as s

checks = []


def zero(name, value):
    reduced = s.simplify(value)
    passed = reduced == 0
    checks.append({"name": name, "residual": str(reduced), "passed": bool(passed)})
    if not passed:
        raise RuntimeError(f"{name}: {reduced}")


t, x = s.symbols("t x", real=True)
kappa, a = s.symbols("kappa a", positive=True)
F = s.Function("F")(x)
phi = -s.log(F) / 2

# Equality of signed one-forms on a positive connected interval.
zero("P_opt_residual_factorization", 1/F-kappa*s.diff(phi,x)-(2+kappa*s.diff(F,x))/(2*F))
Flin = 1-2*x/kappa
zero("affine_profile_P_opt", 1/Flin-kappa*s.diff(-s.log(Flin)/2,x))
Fcounter = s.exp(-2*a*x)
kappaeff = s.simplify(1/Fcounter/s.diff(-s.log(Fcounter)/2,x))
zero("positive_counterprofile_effective_kappa", kappaeff-s.exp(2*a*x)/a)
zero("counterprofile_nonconstant_derivative", s.diff(kappaeff,x)-2*s.exp(2*a*x))
zero("constant_profile_P_opt_nonzero_residual", (1/s.Integer(1)-kappa*0)-1)

# Independent coordinate connection and full 1+1 Ricci contraction.
coord = [t,x]
g = s.diag(-F, 1/F)
gi = g.inv()
Gamma = [[[s.simplify(sum(gi[i,l]*(s.diff(g[l,j],coord[k])+s.diff(g[l,k],coord[j])-s.diff(g[j,k],coord[l]))/2 for l in range(2))) for k in range(2)] for j in range(2)] for i in range(2)]
Ric = s.zeros(2)
for i in range(2):
    for j in range(2):
        Ric[i,j] = s.simplify(sum(s.diff(Gamma[k][i][j],coord[k])-s.diff(Gamma[k][i][k],coord[j])+sum(Gamma[k][k][l]*Gamma[l][i][j]-Gamma[k][j][l]*Gamma[l][i][k] for l in range(2)) for k in range(2)))
R = s.simplify(sum(gi[i,j]*Ric[i,j] for i in range(2) for j in range(2)))
zero("longitudinal_scalar_curvature", R+s.diff(F,x,2))
zero("affine_profile_zero_curvature", R.subs(F,Flin).doit())

# Coordinate construction provides stronger flatness evidence than one scalar.
rho, eta = s.symbols("rho eta", real=True, positive=True)
T, X = rho*s.sinh(eta), rho*s.cosh(eta)
J = s.Matrix([[s.diff(T,eta),s.diff(T,rho)],[s.diff(X,eta),s.diff(X,rho)]])
pullback = s.simplify(J.T*s.diag(-1,1)*J)
for i in range(2):
    for j in range(2):
        zero(f"Rindler_pullback_{i}_{j}", pullback[i,j]-s.diag(-rho**2,1)[i,j])
zero("rho_from_affine_profile", s.diff(kappa*s.sqrt(Flin),x)**2-1/Flin)

# Static clock incidence follows from time-translation of the null ray.
FA, FB, F0 = s.symbols("F_A F_B F_0", positive=True)
rAB = s.sqrt(FB/FA)
rBA = s.sqrt(FA/FB)
zero("static_opposite_future_exchange_inverse", rAB*rBA-1)
zero("static_readout_lapse_ratio", s.log(rAB)-(s.log(FB)-s.log(FA))/2)
zero("receive_from_lower_lapse_redshift_control", rAB.subs({FA:s.Rational(1,4),FB:1})-2)
zero("send_to_lower_lapse_blueshift_control", rAB.subs({FA:1,FB:s.Rational(1,4)})-s.Rational(1,2))
zero("reference_normalization_optical_length", (1/s.sqrt(F0))/(F/F0)-s.sqrt(F0)/F)
zero("reference_normalization_affine_slope", (-2/kappa)*s.sqrt(F0)/F0+2/(kappa*s.sqrt(F0)))
zero("reference_normalization_preserves_clock_ratio", s.sqrt((FB/F0)/(FA/F0))-rAB)

# U is unit; compute acceleration from connection, not a supplied acceleration formula.
U = [1/s.sqrt(F),s.Integer(0)]
acc = [s.simplify(sum(U[j]*s.diff(U[i],coord[j])+sum(Gamma[i][j][k]*U[j]*U[k] for k in range(2)) for j in range(2))) for i in range(2)]
zero("unit_observer", (s.Matrix(U).T*g*s.Matrix(U))[0]+1)
zero("static_acceleration_t", acc[0])
zero("static_acceleration_x", acc[1]-s.diff(F,x)/2)
# n=+/-sqrt(F) partial_x; d ell_U=|dx|/sqrt(F).
acc_plus = s.simplify(g[1,1]*acc[1]*s.sqrt(F))
zero("plus_direction_clock_rate", acc_plus-s.diff(F,x)/(2*s.sqrt(F)))
zero("plus_direction_rate_integrand", acc_plus/s.sqrt(F)-s.diff(s.log(F),x)/2)
zero("P_opt_rate_per_optical_length", (s.sqrt(F)*acc_plus).subs(F,Flin).doit()+1/kappa)

# All-direction constant rest-length clock rate is a separate strong condition.
H, rate = s.symbols("H rate", real=True)
a1,a2,a3 = s.symbols("a1 a2 a3", real=True)
s11,s22,s12,s13,s23 = s.symbols("s11 s22 s12 s13 s23", real=True)
sig = s.Matrix([[s11,s12,s13],[s12,s22,s23],[s13,s23,-s11-s22]])
avec = s.Matrix([a1,a2,a3])
unit = [s.eye(3)[:,i] for i in range(3)]
directions = unit+[-v for v in unit]+[(unit[i]+unit[j])/s.sqrt(2) for i,j in [(0,1),(0,2),(1,2)]]
equations = [H+avec.dot(n)+(n.T*sig*n)[0]-rate for n in directions]
solution = s.solve(equations,[H,a1,a2,a3,s11,s22,s12,s13,s23],dict=True)
expected = {H:rate,a1:0,a2:0,a3:0,s11:0,s22:0,s12:0,s13:0,s23:0}
if solution != [expected]:
    raise RuntimeError(f"all-direction solution: {solution}")
checks.append({"name":"all_direction_constant_rate_conditions","solution":{str(k):str(v) for k,v in solution[0].items()},"passed":True})

root = Path(__file__).resolve().parents[2]
package = root/"udt_july_optical_time_dilation_lead_2026-09-28"
paths = ["simple_metric_L_native_optical_derive_results.md", "simple_metric_L_wall_regularity_closure_results.md", "udt_positional_geometry_clock_connection_2026-09-28/CANDIDATE.md", "udt_positional_geometry_clock_connection_2026-09-28/SCOPED_REGISTRY.json", "udt_null_clock_depth_integrability_assessment_2026-09-10/INITIAL_CANDIDATE.md", "udt_null_clock_depth_integrability_assessment_2026-09-10/REPAIR.md"]
pins = json.loads((package/"SOURCE_PINS.json").read_text())["sources"]
source_checks = []
for name in paths:
    sha = hashlib.sha256((root/name).read_bytes()).hexdigest()
    matches = sha == pins[name]
    source_checks.append({"path":name,"sha256":sha,"pin_match":matches})
    if not matches:
        raise RuntimeError(f"source pin mismatch: {name}")

print(json.dumps({"utc":datetime.now(timezone.utc).isoformat(),"python":platform.python_version(),"sympy":s.__version__,"checks_passed":len(checks),"checks":checks,"source_pins":source_checks,"interpretation":"Exact conditional algebra; diagnostic profiles are not physically selected; no new-candidate exposure or author-code reuse."},indent=2))
