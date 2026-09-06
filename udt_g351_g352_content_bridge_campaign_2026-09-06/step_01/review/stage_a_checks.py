"""Independent exact reduced-query witnesses; no repository imports or writes."""
from fractions import Fraction as F
import json

# All coordinates, metric/phase/cut/observer data and label identity are fixed.
# A=2 gives beta=-2du, C=2 partial_v, screen J=1 in the prior
# UNPROMOTED conditional construction. This check does not re-prove that recipe.
delta = F(3, 2)
omega = (F(2), F(5), F(7))
areas = (F(1), F(1), F(1))
# mu_f=delta*f(x) dxdy on V=[0,1]^2; f=a+b*x.
weights = {"candidate": (F(1), F(0)),
           "doubled": (F(2), F(0)),
           "same_total_changed_profile": (F(1, 2), F(1))}

def amount(coeff, left=F(0), right=F(1)):
    a, b = coeff
    return delta * (a*(right-left) + b*(right*right-left*left)/2)

results = {}
for name, coeff in weights.items():
    a, b = coeff
    assert min(a, a+b) > 0  # analytic affine bound on all [0,1]
    full = amount(coeff)
    half = amount(coeff, F(0), F(1,2))
    assert full > 0 and 0 < half < full
    assert full == half + amount(coeff, F(1,2), F(1))
    sample = F(1,3)
    f = a+b*sample
    density = [delta*f/J for J in areas]
    rates = [w*n/delta for w,n in zip(omega,density)]
    for i,j in [(0,1),(1,2),(0,2)]:
        assert density[j]*areas[j] == density[i]*areas[i]
        assert rates[j]/rates[i] == (omega[j]/omega[i])*(areas[i]/areas[j])
    # Fixed-mu common phase/spacing rescaling is a gauge, changing mu is not.
    phase_scale = F(5,3)
    assert [phase_scale*w*n/(phase_scale*delta)
            for w,n in zip(omega,density)] == rates
    results[name] = {"affine_weight": [str(a),str(b)],
                     "total_amount": str(full),
                     "left_half_amount": str(half),
                     "rates_at_x_1_over_3": list(map(str,rates))}

assert amount(weights["doubled"]) == 2*amount(weights["candidate"])
assert amount(weights["same_total_changed_profile"]) == amount(weights["candidate"])
assert amount(weights["same_total_changed_profile"],F(0),F(1,2)) != amount(weights["candidate"],F(0),F(1,2))
assert results["candidate"]["rates_at_x_1_over_3"] != results["same_total_changed_profile"]["rates_at_x_1_over_3"]

print(json.dumps({"status":"PASS", "evidence_type":"exact_rational_reduced_query_witnesses",
                  "actual_geometry_scope":"conditional constant-A=2 candidate; J=1 only",
                  "full_G350_domain_reproved":False,
                  "coupled_physical_UDT_solutions_claimed":False,
                  "label_identification_and_endpoint_maps_fixed":True,
                  "spacing":str(delta),"frequency_inputs":list(map(str,omega)),
                  "results":results}, indent=2))
