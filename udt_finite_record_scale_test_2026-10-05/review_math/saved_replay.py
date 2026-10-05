"""Independent recomputation from parent saved states; parent code never imported."""
import hashlib,json,platform
from pathlib import Path
import mpmath as mp
mp.mp.dps=90
P=Path(__file__).resolve().parents[1];R=Path(__file__).resolve().parent
source=P/'CONSTRUCTION_RESULT.json';a=json.loads(source.read_text());data=max(a['precisions'],key=lambda p:p['dps'])
M=mp.mpf
checks=[];errors={}
def compare(key,u,v,tol=M('1e-50')):
    e=abs(M(u)-M(v))/max(1,abs(M(u)),abs(M(v)))
    errors[key]=mp.nstr(e,30);assert e<tol,key
def original(row):
    m,Aphys,H,E,rad,b=[M(row[k]) for k in ['m','a','H','E','R','b']]
    mu=m*H;A=Aphys*H;y=1/(H*rad);B=H*b;w=mp.sqrt(mu/A**3-1);h=1-3*mu/A
    W=lambda z:mp.sqrt(1+(E*E-1)*z*z+2*mu*z**3)
    Q=lambda z:1-z*z+2*mu*z**3
    s=lambda z:mp.sqrt(1+B*B*Q(z))
    U=mp.quad(lambda z:B*B/(s(z)*(1+s(z))),[y,1/A])
    angular=mp.quad(lambda z:B/s(z),[y,1/A])
    d=mp.quad(lambda z:1/(W(z)*(E*z+W(z))),[0,y])
    incidence=angular-w*U-w*d
    I=mp.quad(lambda z:1/s(z)**3,[y,1/A]);Wv=W(y);sy=s(y);D=E*y+Wv
    alpha=1/D+Wv*B*B/(1+sy)
    Bp=(B/sy+w*alpha/(Wv*(1-w*B)))/I
    Wp=((E*E-1)*y+3*mu*y*y)/Wv
    Sp=(B*Bp*Q(y)+B*B*(-y+3*mu*y*y))/sy
    ap=-(E+Wp)/D**2+Wp*B*B/(1+sy)+2*Wv*B*Bp/(1+sy)-Wv*B*B*Sp/(1+sy)**2
    Z=(1-w*B)/(mp.sqrt(h)*y*alpha)
    K=H*Wv*(1-y*(-w*Bp/(1-w*B)-ap/alpha))
    nphi=B/alpha;nr=(sy/D-Wv*B*B/(1+sy))/alpha;theta=mp.atan2(nphi,nr)
    theta_p=(Bp/alpha-B*ap/alpha**2)/nr
    angular_rate=H*y*Wv*theta_p/theta
    y0=1/(H*M(row['R_initial']));L=mp.log(y0/y)
    elapsed=mp.quad(lambda u:1/W(y0*mp.exp(-u)),[0,L])/H
    return dict(incidence=incidence,time_residual=elapsed-M(row['ell']),b_x=Bp/H**2,
                t_e=-(d+U)/H,A=y*alpha,Z=Z,logZ=mp.log(Z),K_length=K,K_over_H=K/H,
                theta=theta,n_phi=nphi,n_r=nr,angular_rate=angular_rate,angular_over_H=angular_rate/H)

replayed=[]
for label,rows in data['records'].items():
    for index,row in enumerate(rows):
        got=original(row)
        assert abs(got['incidence'])<M('1e-55') and abs(got['time_residual'])<M('1e-55')
        for key,value in got.items():
            if key not in ['incidence','time_residual']:compare(f'{label}:{index}:{key}',row[key],value)
        replayed.append({'label':label,'index':index,'incidence_residual':mp.nstr(got['incidence'],30),'proper_time_residual':mp.nstr(got['time_residual'],30)})

def enclosure(records,T):
    T=M(T);sigma=T/M(1000);eps=M('.003');q=M('.000005');eta=M('.0005')
    drop=M(records[-1])-M(records[0]);lo=min((drop-2*eps)/(T-2*sigma),(drop-2*eps)/(T+2*sigma))
    hi=max((drop+2*eps)/(T-2*sigma),(drop+2*eps)/(T+2*sigma))
    return max(M(0),(lo-q)/(1+eta)),(hi+q)/(1-eta)

for i,row in enumerate(data['short_common_records']):
    models=[data['records']['short_base'][i],data['records']['short_double'][i]]
    for outkey,key in [('reported_log','logZ'),('reported_angle','theta')]:
        compare(f'midpoint:{i}:{key}',row[outkey],sum(M(m[key]) for m in models)/2)
    for j,m in enumerate(models):
        logcert=abs(M(row['reported_log'])-M(m['logZ']))+M(m['H'])*M('1.0005')*M('.05')
        anglecert=abs(M(row['reported_angle'])-M(m['theta']))+M(m['H'])*M('.05')/290000
        compare(f'window:{i}:{j}:log',row['certificates'][j]['log_window_error_upper'],logcert)
        compare(f'window:{i}:{j}:angle',row['certificates'][j]['angle_window_error_upper'],anglecert)
        assert logcert<M('.003') and anglecert<M('5e-8')
short=enclosure([r['reported_log'] for r in data['short_common_records']], '1.6')
for j in range(2):compare(f'short_interval:{j}',data['short_H_enclosure'][j],short[j])
assert short[0]<=M('.0025')<=M('.005')<=short[1]
intervals={}
for info in data['long_enclosures']:
    lo,hi=enclosure(info['observed_log'],'200');label=info['label']
    offsets=[-1,1,0,-1,1]
    for i,(z,state) in enumerate(zip(info['observed_log'],data['records'][label])):
        compare(f'long_record:{label}:{i}',z,M(state['logZ'])+M('.002')*offsets[i])
    compare(f'{label}:lower',info['H_enclosure'][0],lo)
    compare(f'{label}:upper',info['H_enclosure'][1],hi)
    compare(f'{label}:width',info['relative_width'],(hi-lo)/M('.005'))
    assert lo<=M('.005')<=hi and M('.0025')<lo and (hi-lo)/M('.005')<M('.025')
    intervals[label]=[mp.nstr(lo,50),mp.nstr(hi,50)]
angle_gap=abs(M(data['records']['long_base'][-1]['theta'])-M(data['records']['long_double'][-1]['theta']))
angle_margin=angle_gap-2*M('5e-8')-(M('.005')+M('.0025'))*(M('.05')+M('.2'))/290000
compare('angle_margin',data['long_angle_pair_separation_margin'],angle_margin)
assert angle_margin>0

# Each corrupted replay consumes a case; frozen changes only diagnose the checker.
ref=data['records']['long_boost'][-1]
corrupt_r=dict(ref);corrupt_r['R']=str(M(ref['R'])*M('1.001'))
badtime=abs(original(corrupt_r)['time_residual']);assert badtime>M('.1')
corrupt_b=dict(ref);corrupt_b['b']=str(M(ref['b'])*M('1.01'))
badincidence=abs(original(corrupt_b)['incidence']);assert badincidence>M('1e-8')
out={'status':'PASS','python':platform.python_version(),'mpmath':mp.__version__,
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'cases_this_pass':len(replayed)+2,'cumulative_incidence_cases':36+len(replayed)+2,
 'replays':replayed,'max_readout_scaled_error':mp.nstr(max(M(v) for v in errors.values()),30),
 'long_intervals':intervals,'short_interval':[mp.nstr(v,50) for v in short],
 'long_angle_separation_margin':mp.nstr(angle_margin,50),
 'corruption_controls':{'radial_perturbation_time_residual':mp.nstr(badtime,30),'ray_perturbation_incidence_residual':mp.nstr(badincidence,30)}}
with (R/'SAVED_REPLAY_RESULT.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out,indent=2))
