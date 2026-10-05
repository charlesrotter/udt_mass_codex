"""Exposed recomputation with original equations, never imports parent code."""
import json,hashlib,sys,platform
from pathlib import Path
import mpmath as mp
mp.mp.dps=75
OUT=Path(__file__).parent; PKG=OUT.parent
counter=0

def state(row,ell_override=None):
    global counter
    counter+=1
    assert counter+28<=100
    m,a,H,E,R0=[mp.mpf(row[k]) for k in ['m','a','H','E','R_initial']]
    ell=mp.mpf(row['ell'] if ell_override is None else ell_override)
    h=1-3*m/a; omega=mp.sqrt(m/a**3-H**2)
    if E==1:
        R=(mp.sqrt(2*m)/H*mp.sinh(mp.asinh(H*R0**mp.mpf('1.5')/mp.sqrt(2*m))+mp.mpf('1.5')*H*ell))**(mp.mpf(2)/3)
    else:
        def proper(u):
            return mp.quad(lambda z:1/mp.sqrt(H*H+(E*E-1)*mp.exp(-2*z)/R0**2+2*m*mp.exp(-3*z)/R0**3),[0,u])
        u=mp.findroot(lambda u:proper(u)-ell,H*ell,tol=mp.mpf('1e-65')) if ell else mp.mpf(0)
        assert abs(proper(u)-ell)<mp.mpf('1e-60')
        R=R0*mp.exp(u)
    x=1/R
    V=lambda q:mp.sqrt(H*H+(E*E-1)*q*q+2*m*q**3)
    s=lambda q,b:mp.sqrt(1+H*H*b*b-b*b*q*q+2*m*b*b*q**3)
    d=mp.quad(lambda q:1/(V(q)*(E*q+V(q))),[0,x])
    def integrals(b):
        P=mp.quad(lambda q:b/s(q,b),[x,1/a])
        U=mp.quad(lambda q:b*b/(s(q,b)*(1+s(q,b))),[x,1/a])
        return P,U
    def residual(b):
        P,U=integrals(b)
        return P-omega*U-omega*d
    b=mp.findroot(residual,omega*a*x/(H*H),tol=mp.mpf('1e-65'))
    assert abs(residual(b))<mp.mpf('1e-60')
    P,U=integrals(b); te=-d-U
    vv=V(x); ss=s(x,b); alpha=1/(E*x+vv)+vv*b*b/(1+ss)
    Z=(1-omega*b)/(mp.sqrt(h)*x*alpha)
    np=b/alpha; nr=(ss/(E*x+vv)-vv*b*b/(1+ss))/alpha
    theta=mp.atan2(np,nr)
    return dict(R=R,b=b,Z=Z,logZ=mp.log(Z),theta=theta,t_e=te,y=x/H,incidence_residual=abs(residual(b)))

def interval(d,T,sigma,eps,q):
    eta=mp.mpf(1)/2000
    lo=min((d-2*eps)/(T-2*sigma),(d-2*eps)/(T+2*sigma))
    hi=max((d+2*eps)/(T-2*sigma),(d+2*eps)/(T+2*sigma))
    return [max(mp.mpf(0),(lo-q)/(1+eta)),(hi+q)/(1-eta)]

def main():
    data=json.loads((PKG/'CONSTRUCTION_RESULT.json').read_text())['precisions'][-1]
    comparisons=[]; maxerr=mp.mpf(0); resultstates={}
    for label,rows in data['records'].items():
        resultstates[label]=[]
        for row in rows:
            own=state(row); resultstates[label].append(own)
            errors={k:abs(own[k]-mp.mpf(row[k]))/max(1,abs(own[k])) for k in ['R','b','Z','logZ','theta','t_e']}
            err=max(errors.values()); maxerr=max(err,maxerr)
            assert err<mp.mpf('1e-45'),(label,row['ell'],err)
            comparisons.append(dict(label=label,ell=row['ell'],max_scaled_difference=mp.nstr(err,30),own={k:mp.nstr(v,70) for k,v in own.items()}))
    support=[]
    for label in ['short_base','short_double','long_boost']:
        own=state(data['records'][label][0],'-0.05')
        assert own['y']<mp.mpf('1.001e-5')
        support.append(dict(label=label,ell='-.05',y=mp.nstr(own['y'],60)))
    means=[]
    for i,record in enumerate(data['short_common_records']):
        r0=resultstates['short_base'][i]; r1=resultstates['short_double'][i]
        for key,obs in [('logZ','reported_log'),('theta','reported_angle')]:
            center=(r0[key]+r1[key])/2
            assert abs(center-mp.mpf(record[obs]))<mp.mpf('1e-45')
        for j,label in enumerate(['short_base','short_double']):
            own=resultstates[label][i]; H=mp.mpf(data['records'][label][i]['H'])
            log_upper=abs(mp.mpf(record['reported_log'])-own['logZ'])+H*(1+mp.mpf(1)/2000)*mp.mpf('.05')
            angle_upper=abs(mp.mpf(record['reported_angle'])-own['theta'])+H/mp.mpf(290000)*mp.mpf('.05')
            assert log_upper<mp.mpf('.003') and angle_upper<mp.mpf('5e-8')
            assert abs(log_upper-mp.mpf(record['certificates'][j]['log_window_error_upper']))<mp.mpf('1e-45')
            assert abs(angle_upper-mp.mpf(record['certificates'][j]['angle_window_error_upper']))<mp.mpf('1e-45')
            means.append(dict(centre=record['ell'],label=label,log_upper=mp.nstr(log_upper,50),angle_upper=mp.nstr(angle_upper,50)))
    d=mp.mpf(data['short_common_records'][-1]['reported_log'])-mp.mpf(data['short_common_records'][0]['reported_log'])
    short=interval(d,mp.mpf('1.6'),mp.mpf('.0016'),mp.mpf('.003'),mp.mpf('.000005'))
    assert all(abs(a-mp.mpf(b))<mp.mpf('1e-45') for a,b in zip(short,data['short_H_enclosure']))
    assert short[0]<=mp.mpf('.0025')<=mp.mpf('.005')<=short[1]
    longs=[]
    for item in data['long_enclosures']:
        values=list(map(mp.mpf,item['observed_log'])); label=item['label']
        for i,(v,off) in enumerate(zip(values,['-.002','.002','0','-.002','.002'])):
            assert abs(v-resultstates[label][i]['logZ']-mp.mpf(off))<mp.mpf('1e-45')
            assert abs(mp.mpf(off))+mp.mpf('.005')*(1+mp.mpf(1)/2000)*mp.mpf('.05')<mp.mpf('.003')
        out=interval(values[-1]-values[0],mp.mpf(200),mp.mpf('.2'),mp.mpf('.003'),mp.mpf('.000005'))
        assert all(abs(a-mp.mpf(b))<mp.mpf('1e-45') for a,b in zip(out,item['H_enclosure']))
        assert out[0]<mp.mpf('.005')<out[1]
        longs.append(dict(label=label,H_enclosure=list(map(lambda x:mp.nstr(x,70),out)),length_enclosure=[mp.nstr(1/out[1],40),mp.nstr(1/out[0],40)]))
    candidate=PKG/'INITIAL_CANDIDATE.md'
    result=dict(status='PASS',new_incidence_cases=counter,total_independent_incidence_cases=counter+28,max_scaled_record_difference=mp.nstr(maxerr,40),source={'candidate_sha256':hashlib.sha256(candidate.read_bytes()).hexdigest(),'construction_sha256':hashlib.sha256((PKG/'CONSTRUCTION_RESULT.json').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},python=sys.version,mpmath=mp.__version__,platform=platform.platform(),comparisons=comparisons,support=support,finite_window_bounds=means,short_H_enclosure=[mp.nstr(x,60) for x in short],long_enclosures=longs)
    (OUT/'SAVED_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','new_incidence_cases','total_independent_incidence_cases','max_scaled_record_difference','short_H_enclosure','long_enclosures']}))
if __name__=='__main__':main()
