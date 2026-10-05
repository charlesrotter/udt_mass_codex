"""Exposed saved-quantity replay; separate SciPy Brent/integrated-time implementation."""
from pathlib import Path
import json,math,hashlib,sys
import scipy
from scipy.integrate import quad
from scipy.optimize import brentq
P=Path(__file__).resolve().parent
source=P.parent/'CONSTRUCTION_RESULT.json'
data=json.loads(source.read_text())['precisions'][-1]
output={'status':'RUNNING','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'python':sys.version,'scipy':scipy.__version__,'prior_case_count':36,'case_count':0,'rows':[]}

def save():
    (P/'SAVED_REPLAY_RESULT.json').write_text(json.dumps(output,indent=2)+'\n')

def solve(raw,R=None):
    output['case_count']+=1
    assert output['case_count']<=64
    m,a,H,E,bs=[float(raw[k]) for k in ['m','a','H','E','b_star']]
    R=float(raw['R']) if R is None else R
    x=1/R;om=math.sqrt(m/a**3-H*H);h=1-3*m/a
    def S(y,b):return math.sqrt(1+b*b*(H*H-y*y+2*m*y**3))
    def W(y):return math.sqrt(H*H+(E*E-1)*y*y+2*m*y**3)
    def integ(fn,lo,hi):return quad(fn,lo,hi,epsabs=2e-12,epsrel=2e-12,limit=150)[0]
    def phi(b,y):return integ(lambda q:b/S(q,b),y,1/a)
    def u(b,y):return integ(lambda q:b*b/(S(q,b)*(1+S(q,b))),y,1/a)
    d=integ(lambda y:1/(W(y)*(E*y+W(y))),0,x)
    target=phi(bs,0)-om*u(bs,0)+om*d
    fn=lambda b:phi(b,x)-om*u(b,x)-target
    margin=.95*a/math.sqrt(1-2*m/a-H*H*a*a)
    b=brentq(fn,-margin,margin,xtol=2e-13,rtol=1e-14)
    sr,sa=S(x,b),S(1/a,b);v=W(x)/x
    A=1/(E+v)+v*b*b*x*x/(1+sr)
    Z=(1-om*b)/(math.sqrt(h)*A)
    sn=b*x/A;cs=(sr/(E+v)-v*b*b*x*x/(1+sr))/A
    angle=math.atan2(sn,cs)
    ii=integ(lambda y:1/S(y,b)**3,x,1/a);ph=phi(b,x)
    result=dict(b=b,A=A,Z=Z,theta=angle,j_parallel=A*a*sa*R*sr*ii,
        j_perp=A*a*R*math.sin(ph)/b if b else A*(R-a),residual=abs(fn(b)))
    assert result['residual']<=1e-10
    return result

def derivative(raw):
    R=float(raw['R']);q=solve(raw);p=solve(raw,R*(1+1e-4));n=solve(raw,R*(1-1e-4))
    E,m,H=[float(raw[k]) for k in ['E','m','H']]
    dt=quad(lambda r:1/math.sqrt(E*E-1+2*m/r+H*H*r*r),R*(1-1e-4),R*(1+1e-4),epsabs=1e-12,epsrel=1e-12)[0]
    q['K_length']=math.log(p['Z']/n['Z'])/dt
    q['angular_rate']=-math.log(abs(p['theta']/n['theta']))/dt
    q['delta_ell']=dt
    return q

try:
    selected=[r for r in data['actual_incidences'] if float(r['R'])==100000]
    selected+= [r['scaled_point'] for r in data['homotheties']]
    maxima={'scaled_error':0.,'relative_rate_error':0.,'residual':0.}
    for raw in selected:
        rec=derivative(raw)
        err={k:abs(rec[k]-float(raw[k]))/max(1,abs(float(raw[k]))) for k in rec if k in raw}
        rateerr={k:abs(rec[k]/float(raw[k])-1) for k in ['K_length','angular_rate']}
        output['rows'].append({'saved_input':raw,'recomputed':rec,'errors':err,'relative_rate_errors':rateerr});save()
        assert max(err.values())<1e-7
        assert max(rateerr.values())<1e-5
        maxima['scaled_error']=max(maxima['scaled_error'],max(err.values()))
        maxima['relative_rate_error']=max(maxima['relative_rate_error'],max(rateerr.values()))
        maxima['residual']=max(maxima['residual'],rec['residual'])
    sides=[]
    for diff in data['timed_differences']:
        for name in ['plus','minus']:
            raw=diff[name];rec=solve(raw)
            err={k:abs(rec[k]-float(raw[k]))/max(1,abs(float(raw[k]))) for k in rec if k in raw}
            sides.append({'saved_input':raw,'recomputed':rec,'errors':err})
            assert max(err.values())<1e-7
    output['sides']=sides
    # Verify dimensional vector: c^3/(G K) is mass, not a physical mass law.
    c=(1,-1,0);g=(3,-2,-1);k=(0,-1,0)
    assert tuple(3*c[i]-g[i]-k[i] for i in range(3))==(0,0,1)
    output.update(status='PASS',maxima=maxima,cumulative_case_count=36+output['case_count'])
    save();print(json.dumps({k:output[k] for k in ['status','case_count','cumulative_case_count','maxima']},indent=2))
except BaseException as e:
    output.update(status='FAIL',error=repr(e));save();raise
