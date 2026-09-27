#!/usr/bin/env python3
"""Independent exact native controls and abstract exceptional linearization.

No production/native/static-check imports; no full perturbation PDE claim.
"""
import hashlib
import json
import platform
from fractions import Fraction as Q
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
checks = {}
def ck(label, actual, expected):
    checks[label] = {"actual":str(actual),"expected":str(expected)}
    assert actual == expected, (label, actual, expected)

# Free mathematical control ell is used as unit of length; no physical selection.
fa, fb, fc = [1+Q(r)**2 for r in [1,2,3]]
ck("q_AB",fb/fa,Q(5,2)); ck("q_CB",fb/fc,Q(1,2))
ck("composition",(fb/fa)*(fc/fb),fc/fa)
ck("reversal",(fb/fa)*(fa/fb),Q(1))
for label,a in [("A",fa),("C",fc)]:
    q = fb/a
    # Generic-angle angular metric entries at r=2ell, sin(theta)^2=3/4.
    # Base diagonal is (-fb,1/fb,4,3). Squared Jacobian is (1/a,a,1,1).
    gy = [(-fb)/a, a/fb, Q(4), Q(3)]
    ck(label+"_pair_det",gy[0]*gy[1],Q(-1))
    ck(label+"_theta_carry",gy[2],Q(4))
    ck(label+"_phi_carry",gy[3],Q(3))
    ck(label+"_full_det",gy[0]*gy[1]*gy[2]*gy[3],Q(-12))
    ck(label+"_carried_null",gy[0]+gy[1]*q**2,Q(0))
    ck(label+"_base_null_slope",a*q,fb)
    ck(label+"_proper_ratio_squared",(a/fb)/(fb/a)*q**2,Q(1))
    ck(label+"_wrong_second_cone",q**2-1,Q(21,4) if label=="A" else Q(-3,4))

# E9: variation of arbitrary component, retaining every metric/Ricci coefficient.
eps, alpha = s.symbols("epsilon alpha",nonzero=True)
rho, Ric0, dRic, g0, h, boxrho, Hessrho, dC = s.symbols(
    "rho Ric0 dRic g0 h boxrho Hessrho dC")
R0 = -1/(2*alpha)
R = R0+eps*rho
F = 1+2*alpha*R
L = R+alpha*R**2
C = 1/(8*alpha)
metric = g0+eps*h
# Because R0 is constant, all differential-operator variations acting on F0 vanish.
E = F*(Ric0+eps*dRic)-L*metric/2 +2*alpha*eps*(metric*boxrho-Hessrho)
dres = s.expand(s.diff(E-C*metric,eps).subs(eps,0))
expected = 2*alpha*(rho*Ric0+g0*boxrho-Hessrho)
ck("E9_arbitrary_component",s.simplify(dres-expected),s.Integer(0))
ck("E9_no_dRic",s.diff(dres,dRic),s.Integer(0))
ck("E9_no_h",s.diff(dres,h),s.Integer(0))
ck("E9_zero_scalar_direction",s.simplify(dres.subs({rho:0,boxrho:0,Hessrho:0})),s.Integer(0))
vary_C = s.diff(E-(C+eps*dC)*metric,eps).subs(eps,0)
ck("varying_C_term",s.simplify(vary_C-dres+dC*g0),s.Integer(0))
trace_E9 = 2*alpha*(R0*rho+4*boxrho-boxrho)
ck("E10_trace",s.simplify(trace_E9-(6*alpha*boxrho-rho)),s.Integer(0))
ck("omitted_C_h_detected",s.simplify(s.diff(E,eps).subs(eps,0)-dres),h/(8*alpha))

result = {"status":"PASS","check_count":len(checks),"checks":checks,
    "python":platform.python_version(),"sympy":s.__version__,
    "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "limits":"Finite native controls and abstract full component linearization; no general query population or full metric-perturbation PDE certification."}
(HERE/"DIRECT_CHECK_RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"status":"PASS","exact_checks":len(checks),"python":result["python"],"sympy":result["sympy"]},indent=2))
