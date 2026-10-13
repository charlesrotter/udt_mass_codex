"""Independent exact arithmetic and saved-endpoint reconstruction for FAC1.

No author code imports. This does not rederive the directional series or certify
the numerical integration; it recomputes the load-bearing summaries and endpoint
frequency ratios from saved fields.
"""
import hashlib
import json
import math
import platform
from fractions import Fraction as F
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def double_factorial(n):
    return math.prod(range(n, 0, -2))

def average(terms):
    # Terms are c * n_x^(2i) * n_z^j. Uniform unit sphere in three dimensions.
    value = F(0)
    for c, i, j in terms:
        if j % 2 == 0:
            value += c * F(double_factorial(2*i-1)*double_factorial(j-1),
                           double_factorial(2*i+j+1))
    return value

def kasner_mean(coefficients):
    return sum((F(c,486*(2*k+1)) for k,c in enumerate(coefficients)), F(0))

exact = {}
exact['kasner_plus'] = kasner_mean([-43,204,-117])
exact['kasner_minus'] = kasner_mean([-31,114,-27])
assert exact['kasner_plus'] == exact['kasner_minus'] == F(4,1215)
for sense in [1,-1]:
    terms = [(F(4,96),2,0),(F(4,96),1,2),(F(-4,96),1,0),
             (F(2,96),0,4),(F(4*sense,96),0,3),
             (F(-3,96),0,2),(F(-4*sense,96),0,1),(F(1,96),0,0)]
    exact['plane_'+str(sense)] = average(terms)
    assert exact['plane_'+str(sense)] == F(1,720)
exact['electric_coefficient'] = exact['kasner_plus']/F(8,27)
exact['magnetic_coefficient'] = 2*exact['plane_1']-exact['electric_coefficient']
assert exact['electric_coefficient'] == F(1,90)
assert exact['magnetic_coefficient'] == -F(1,120)

kerr = []
for r in [F(3,2),F(31,20)]:
    a2, y2, rplus = F(15,16), F(4,5), F(5,4)
    ay2 = a2*y2
    sigma = r*r+ay2
    delta = r*r-2*r+a2
    E2 = 6*r*r*(r*r-3*ay2)**2/sigma**6
    B2 = 6*ay2*(3*r*r-ay2)**2/sigma**6
    gtt = -(1-2*r/sigma)
    quartic = (4*E2-3*B2)/360
    assert r>rplus and delta>0 and 0<y2<1 and quartic<0
    if r == F(3,2):
        assert E2 == 0 and B2 == F(2,9) and quartic == -F(1,540)
    else:
        assert gtt<0
    kerr.append({k:str(v) for k,v in locals().copy().items()
                 if k in ['r','sigma','delta','E2','B2','gtt','quartic','rplus']})

def scale_squares(t, epsilon, flat):
    powers = (0.,0.,0.) if flat else (-1/3,2/3,2/3)
    factor = math.exp(epsilon*(t-1)**2)
    return [factor*t**(2*r) for r in powers]

def omega(t, q, P, epsilon, flat):
    a2 = scale_squares(t,epsilon,flat)
    w = math.sqrt(math.fsum(qi*qi/ai for qi,ai in zip(q,a2)))
    gamma = math.sqrt(1+math.fsum(pi*pi/ai for pi,ai in zip(P,a2)))
    return w*gamma-math.fsum(qi*pi/ai for qi,pi,ai in zip(q,P,a2))

file_names = ['vacuum_baseline_data.json','vacuum_fine_data.json',
              'flat_fine_data.json','deform_neg5_data.json']
numeric=[]
for name in file_names:
    path = BASE/'researcher_b'/name
    data=json.loads(path.read_text())
    eps=data['arguments']['epsilon']
    flat=data['arguments']['flat']
    for result in data['results']:
        logs=[[],[]]
        weights=result['angular_weights']
        max_diff=0.
        for row in result['angular_records']:
            T=row['preparation_t']; P=row['receiver_momenta']
            q=row['outgoing_q']; qrev=row['reverse_q']
            lp=math.log(omega(1.,q,[0.,0.,0.],eps,flat)/
                        omega(row['outgoing_t'],q,P,eps,flat))
            lm=math.log(omega(T,qrev,P,eps,flat)/
                        omega(row['reverse_t'],qrev,[0.,0.,0.],eps,flat))
            logs[0].append(lp);logs[1].append(lm)
            max_diff=max(max_diff,abs(lp-row['log_plus']),abs(lm-row['log_minus']))
        means=[math.fsum(w*l for w,l in zip(weights,ls)) for ls in logs]
        err=max(abs(means[0]-result['M_plus']),abs(means[1]-result['M_minus']))
        werr=abs(math.fsum(weights)-1)
        assert max_diff<=5e-14 and err<=1e-14 and werr<=1e-14
        numeric.append(dict(file=name,sha256=sha(path),L=result['L'],
                            M_plus=means[0],M_minus=means[1],
                            M_plus_over_L4=means[0]/result['L']**4,
                            M_minus_over_L4=means[1]/result['L']**4,
                            max_log_discrepancy=max_diff,
                            max_mean_discrepancy=err,weight_sum_error=werr))

report=dict(status='PASS_EXACT_ARITHMETIC_AND_ARTIFACT_CORRESPONDENCE_ONLY',
            python=platform.python_version(),source_sha256=sha(Path(__file__)),
            exact={k:str(v) for k,v in exact.items()},kerr=kerr,numeric=numeric,
            scientific_limits='No fresh ray solve, no numeric enclosure, no native adoption.')
print(json.dumps(report,indent=2))
