"""Read saved parent data; independently differentiate its linear metric jet."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib, json

p=Path('udt_curvature_measurement_feasibility_2026-10-02/SAVED_CONTROL.json')
data=json.loads(p.read_text()); tests=[]
def test(name, ok, evidence):
    tests.append(dict(name=name,passed=bool(ok),evidence=evidence))
    if not ok: raise AssertionError(name)

eta=[Q(-1),Q(1),Q(1),Q(1)]
k=[Q(5,4),-Q(3,4),Q(0),Q(0)]
def h_second(a,b,c,d):
    # h_cd=-(rho/3) eta_cd; d_a d_b rho(0)=-k_a k_b.
    return k[a]*k[b]*eta[c]/3 if c==d else Q(0)
def gamma_derivative(p,a,b,c):
    return eta[a]*(h_second(p,b,a,c)+h_second(p,c,a,b)-h_second(p,a,b,c))/2
ric=[[sum(gamma_derivative(c,c,a,b)-gamma_derivative(b,c,a,c) for c in range(4)) for b in range(4)] for a in range(4)]
saved=[[Q(x) for x in row] for row in data['ricci']]
for a,b in product(range(4),repeat=2):
    test('linear Ricci '+str((a,b)),ric[a][b]==saved[a][b],ric[a][b])
R=sum(eta[a]*ric[a][a] for a in range(4))
test('scalar from original linear metric jet',R==1,R)
norm_k=sum(eta[a]*k[a]**2 for a in range(4))
test('independent scalar box coefficient',norm_k==-1,-norm_k)
alpha=Q(data['alpha'])
for a,b in product(range(4),repeat=2):
    metric=eta[a] if a==b else Q(0)
    original_linear_tensor=ric[a][b]-metric*R/2+2*alpha*(metric*(-norm_k)+k[a]*k[b])
    test('original linear tensor '+str((a,b)),original_linear_tensor==0,original_linear_tensor)

v=Q(data['speed']); gamma=Q(5,4)
test('saved frame gamma',gamma**2*(1-v*v)==1,gamma)
frames=[[Q(1),Q(0),Q(0),Q(0)]]
for i in range(1,4):
    for sign in [1,-1]:
        frames.append([gamma if a==0 else sign*gamma*v if a==i else Q(0) for a in range(4)])
c=[sum(ric[a][b]*u[a]*u[b] for a,b in product(range(4),repeat=2)) for u in frames]
test('all saved contractions from metric jet',c==list(map(Q,data['contractions'])),c)
scalar=sum(c[1:])/(2*gamma**2*v**2)-(1+3/v**2)*c[0]
test('saved contractions scalar recombination',scalar==R,scalar)

samples=[{key:Q(value) for key,value in row.items()} for row in data['trace_samples']]
dR=samples[1]['R']-samples[0]['R']; dX=samples[1]['Box_R']-samples[0]['Box_R']
alpha_affine=dR/(6*dX); lambda_affine=(samples[0]['R']-6*alpha_affine*samples[0]['Box_R'])/4
test('independent affine fixture recovery',alpha_affine==Q(2,3) and lambda_affine==Q(1,20),dict(alpha=alpha_affine,Lambda=lambda_affine))
test('independent third affine sample',6*alpha_affine*samples[2]['Box_R']-samples[2]['R']+4*lambda_affine==0,samples[2])
test('affine fixture is separate from conformal metric fixture',alpha_affine!=alpha,dict(metric_alpha=alpha,affine_alpha=alpha_affine))

print(json.dumps(dict(status='PASS',checks=len(tests),saved_source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),method='stdlib Fraction direct linearized connection derivatives; no parent script import',results=tests),indent=2,default=str))
