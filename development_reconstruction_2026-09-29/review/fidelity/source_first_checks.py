"""Small exact algebra controls, independently authored before candidate exposure.

These do not prove geometric existence, physical admission or semantic coverage.
"""
from fractions import Fraction as F
from pathlib import Path
import json

checks = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


# A regular shifted pair, preserving the full metric and positive ruler density.
h00, h01, h11 = F(-4), F(-6), F(16)
det = h00 * h11 - h01 * h01
m = F(10)
T2 = -h00
beta = h01 / h00
L2 = h11 - h01 * h01 / h00
check("shifted_pair_reconstruction", -T2 * beta == h01 and L2 - T2 * beta**2 == h11)
check("completed_ruler_density", m*m == -det == T2*L2)
hs = (h00, h01/m, h11/(m*m))
check("completed_determinant", hs[0]*hs[2]-hs[1]*hs[1] == -1)
check("retained_tuple_recovers_pullback", (hs[0], hs[1]*m, hs[2]*m*m) == (h00,h01,h11))
check("diagonal_only_wrong_with_shift", h00*h11 != det)

# Actual two-map echo algebra. The maps are supplied, not native realizations.
p,q = F(2),F(3)
P = p*q
dRds, dTds = (P-1)/2,(P+1)/2  # c_E=1
check("actual_echo_radar_derivative", dRds/dTds == F(5,7))
check("actual_return_not_inverse", q != 1/p)
p2,q2 = F(4), F(1,2)
check("positive_radar_drift_not_both_redshift", (p2*q2-1)/(p2*q2+1)>0 and q2<1)

# Covariant dimensional powers c^a G^b: mass exponent forces b=0,
# time exponent then forces a=0; hence no length exponent +1 is possible.
b=F(0); a=-2*b
check("constants_alone_no_intrinsic_length_monomial", a+3*b != 1)

# Constant homothety matched-clock protocol f_l(s)=l*f(s/l).
# For f(s)=s^2+3s+5, matched s_l=l*s gives unchanged derivative.
l,s=F(7),F(2)
check("matched_clock_ratio_homothety", 2*(l*s)/l+3 == 2*s+3)

# G350/G351/G352 are different mathematical premise increments.
R,A=F(3),F(2)
check("conservation_does_not_select_frequency_weight", A**-1 != R*A**-1)

print(json.dumps({"scope":"exact algebra regression controls, no science promotion",
                  "count":len(checks),"passed":checks}, indent=2))
