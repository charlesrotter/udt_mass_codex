"""PRI1 independent exact rational anchors; no producer imports."""
import json
import platform
from fractions import Fraction as F

sign = (-1, 1, 1, 1)
checks = {}
rejects = {}

def dot(x, y):
    return sum(sign[i] * x[i] * y[i] for i in range(4))

def matvec(a, x):
    return [sum(a[i][j] * x[j] for j in range(4)) for i in range(4)]

def moment(pop):
    return [[sum(w * sign[i] * k[i] * sign[j] * k[j] for w, k in pop)
             for j in range(4)] for i in range(4)]

def bil(a, u, v):
    return sum(u[i] * a[i][j] * v[j] for i in range(4) for j in range(4))

def test(name, truth):
    checks[name] = bool(truth)
    assert truth, name

def reject(name, false_statement):
    rejects[name] = not bool(false_statement)
    assert not false_statement, name

kp, km = (F(1), F(1), F(0), F(0)), (F(1), F(-1), F(0), F(0))
pop = [(F(16), kp), (F(1), km)]
m = moment(pop)
u = [F(5,4), F(3,4), F(0), F(0)]
v = [F(3,4), F(5,4), F(0), F(0)]
ey = [F(0), F(0), F(1), F(0)]
test("two_beams_future_null", all(k[0] > 0 and dot(k,k) == 0 for _, k in pop))
test("rest_frame_unit_pair", dot(u,u) == -1 and dot(v,v) == 1 and dot(u,v) == 0)
test("moment_trace_zero", sum(sign[i] * m[i][i] for i in range(4)) == 0)
energy = bil(m,u,u)
mixed = [[sign[i] * m[i][j] for j in range(4)] for i in range(4)]
test("two_beam_rest_energy", energy == 8)
test("two_beam_rest_eigenvector", matvec(mixed,u) == [-energy * x for x in u])
test("two_beam_zero_spatial_flux", bil(m,u,v) == 0 and bil(m,u,ey) == 0)
test("longitudinal_hessian", 2 * (bil(m,v,v) + energy) == 32)
test("transverse_hessian", 2 * (bil(m,ey,ey) + energy) == 16)
ddr = 2 * sum(w * (dot(k,u)**2 + dot(k,v)**2) for w,k in pop)
test("positive_reciprocal_pairing", ddr == 32)
reject("raw_positive_moment_satisfies_DDR", ddr == 0)

boost = [[F(5,4), F(3,4), F(0), F(0)],
         [F(3,4), F(5,4), F(0), F(0)],
         [F(0), F(0), F(1), F(0)],
         [F(0), F(0), F(0), F(1)]]
pop_b = [(w, matvec(boost,k)) for w,k in pop]
ub = matvec(boost,u)
mb = moment(pop_b)
test("rational_boost_covariant_energy", bil(mb,ub,ub) == energy and dot(ub,ub) == -1)
mixed_b = [[sign[i]*mb[i][j] for j in range(4)] for i in range(4)]
test("rational_boost_covariant_eigenvector", matvec(mixed_b,ub) == [-energy*x for x in ub])

beam_values = []
for er in (F(1), F(2), F(4), F(8)):
    ur = [(er + 1/er)/2, (er - 1/er)/2, F(0), F(0)]
    beam_values.append(dot(kp,ur)**2)
test("single_beam_exact_decreasing_controls", beam_values == [F(1), F(1,4), F(1,16), F(1,64)])

axes=[]
for j in range(1,4):
    for orientation in (-1,1):
        k=[F(1),F(0),F(0),F(0)]
        k[j]=F(orientation)
        axes.append((F(1,6),k))
rotated=[]
for w,k in axes:
    rotated.append((w,[k[0],F(3,5)*k[1]-F(4,5)*k[2],F(4,5)*k[1]+F(3,5)*k[2],k[3]]))
ma,mr=moment(axes),moment(rotated)
test("distinct_populations_null", all(dot(k,k)==0 for _,k in axes+rotated))
test("identical_isotropic_second_moments", ma==mr and ma==[[F(1),0,0,0],[0,F(1,3),0,0],[0,0,F(1,3),0],[0,0,0,F(1,3)]] )
fourth_a=sum(w*k[1]**2*k[2]**2 for w,k in axes)
fourth_r=sum(w*k[1]**2*k[2]**2 for w,k in rotated)
test("different_fourth_angular_moments", fourth_a==0 and fourth_r==F(96,625))
reject("second_moment_identifies_population", fourth_a==fourth_r)
reject("isotropic_second_moment_is_pure_metric", ma[0][0] == -ma[1][1])

# Exact product rule, chosen rational diagnostics not a physical variation law.
d0,d1,w0,dw=F(2),F(3),F(5),F(7)
# coefficient of epsilon in (w0+epsilon*dw)*(d0+epsilon*d1)^2/2
coefficient=F(1,2)*(w0*2*d0*d1+dw*d0*d0)
fixed_part=w0*d0*d1
measure_part=F(1,2)*dw*d0*d0
test("full_measure_product_rule", coefficient==fixed_part+measure_part==44)
reject("positive_baseline_measure_may_be_frozen_without_rule", coefficient==fixed_part)

# Infinite sequence: k_n=2^-n*(1,1,0,0), mu_n=2^n, n>=1.
# Full second moment sum is sum 2^-n=1; first moment sum is sum 1=+infinity.
n=8
second_partial=sum(F(2)**(-j) for j in range(1,n+1))
first_partial=sum(F(2)**j * F(2)**(-j) for j in range(1,n+1))
test("finite_second_infinite_first_partial_control", second_partial==F(255,256) and first_partial==8)

print(json.dumps({"status":"PASS", "python":platform.python_version(),
 "arithmetic":"stdlib fractions.Fraction, exact", "checks":checks,
 "false_claim_rejections":rejects,
 "outputs":{"two_beam_rest_energy":str(energy), "DDR_pairing":str(ddr),
 "beam_energy_controls":[str(x) for x in beam_values],
 "different_fourth_moment":str(fourth_r), "full_score_derivative":str(coefficient)},
 "limits":"Finite exact anchors; analytic general proofs are in SOURCE_FIRST.md. No physical law adopted."},indent=2))
