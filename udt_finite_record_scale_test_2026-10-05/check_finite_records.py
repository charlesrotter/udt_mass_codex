"""FRI1 exact rational envelopes and finite same-proper-time records.
Reuses the version-pinned reviewed TSI incidence evaluator; no empirical fit.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,platform,importlib.util
import mpmath as mp
B=Path(__file__).resolve().parent
SRC=Path('udt_timing_scale_identifiability_2026-10-05/check_timing_scale.py')

def bounds(mu,amin,amax,emax,wmax,y,bbar):
    sm=F(999,1000);sp=F(1001,1000);wm=1+F(2,10**8)
    assert sm*sm<1-bbar*bbar/(amin*amin)
    assert sp*sp>1+bbar*bbar
    assert wm*wm>1+(emax*emax-1)*y*y+2*mu*y**3
    wp=(emax*emax-1)*y+3*mu*y*y
    assert wp<F(2,1000)
    D=emax*y+wm;Dp=emax+wp
    I=(1/amax-y)/sp**3;J=(1-wmax*bbar)*I
    assert J*bbar>wmax*y
    almax=1+wm*bbar*bbar/(1+sm)
    almin=1/D
    bp=(bbar/sm+wmax*almax/(1-wmax*bbar))/I
    assert bp<1
    sd=(bbar*bp*(1+y*y+2*mu*y**3)+bbar*bbar*(y+3*mu*y*y))/sm
    j=wm*D*bbar*bbar/(1+sm)
    jd=((wp*D+wm*Dp)*bbar*bbar+2*wm*D*bbar*bp)/(1+sm)+wm*D*bbar*bbar*sd/(1+sm)**2
    blog=wmax*bp/(1-wmax*bbar)+Dp+jd
    rate_error=(wm-1)+wm*y*blog
    ap=jd+(1+j)*Dp
    npmax=bbar/almin
    assert npmax*npmax<1-sm*sm
    assert sm/D-wm*bbar*bbar/(1+sm)>0
    tp=(bp/almin+bbar*ap/almin**2)/sm
    angular_bound=y*wm*tp
    return dict(I=I,J=J,Wmax=wm,Wprime=wp,alpha_max=almax,Bprime=bp,sprime=sd,jprime=jd,logFprime=blog,relative_rate_error=rate_error,alpha_prime=ap,theta_prime=tp,angular_per_H=angular_bound)

def exact():
    g=bounds(F(1,100),F(1,20),F(1,10),F(10),F(9),F(1,50000),F(1,10000))
    assert g['alpha_max']<F('1.000000006') and g['sprime']<F('.000101')
    assert g['jprime']<F('.000101') and g['logFprime']<20
    assert g['relative_rate_error']<F(1,2000)
    assert g['alpha_prime']<F('10.003') and g['theta_prime']<2
    assert g['angular_per_H']<F(1,20000)
    q=bounds(F(1,200),F(1,20),F(1,20),F(1),F(25,4),F(1001,10**8),F(1,100000))
    assert q['I']>F('19.94') and q['Bprime']<F('.314')
    assert q['theta_prime']<F(1,3) and q['angular_per_H']<F(1,290000)
    H=F(1,200);delta=F(1,10);T=F(8,5);eta=F(1,2000)
    support=F(1,100000)/(1-H*g['Wmax']*delta/2)
    assert support<F(1001,10**8)
    timing=H*(F(1,2)+F(3,2)*eta)*T/2+H*(1+eta)*delta/2
    angle=F(3,4)*H*T/F(290000)+H*delta/(2*F(290000))
    assert timing<F('.003') and angle<F('5e-8')
    # Positive synthetic center reports really can be finite-window means plus errors.
    assert F('.002')+H*(1+eta)*delta/2<F('.003')
    assert H/F(20000)*delta/2<F('5e-8')
    serial=lambda d:{k:{'exact':str(v),'decimal':float(v)} for k,v in d.items()}
    return dict(global_domain=serial(g),witness_shape=serial(q),
        exact_short_compatibility={'log_upper':str(timing),'angle_upper':str(angle),'backward_y_upper':str(support)},
        status='PASS',interpretation='Rational inequality checks support the written continuum proof; not finite-sample certification.')

def fixed_time(m,a,H,E,R0,ell):
    y0=1/(H*R0);mu=m*H
    W=lambda y:mp.sqrt(1+(E*E-1)*y*y+2*mu*y**3)
    target=H*ell
    if target:
        q=mp.findroot(lambda q:mp.quad(lambda t:1/W(y0*mp.exp(-t)),[0,q])-target,target)
    else:q=mp.mpf(0)
    res=mp.quad(lambda t:1/W(y0*mp.exp(-t)),[0,q])-target
    assert abs(res)<mp.power(10,-mp.mp.dps+8)
    R=R0*mp.exp(q)
    if E==1:
        cc=mp.asinh(H*R0**mp.mpf('1.5')/mp.sqrt(2*m))
        rex=(mp.sqrt(2*m)/H*mp.sinh(cc+mp.mpf('1.5')*H*ell))**(mp.mpf(2)/3)
        assert abs(R/rex-1)<mp.power(10,-mp.mp.dps+8)
    out=tsi.point(m,a,H,E,mp.mpf(0),R)
    out.update(ell=ell,R_initial=R0,proper_time_residual=abs(res),logZ=mp.log(out['Z']))
    return out

def enclosure(z0,z1,T):
    eta=mp.mpf('.0005');sig=mp.mpf('.001')*T;eps=mp.mpf('.003');q=mp.mpf('.000005')
    lo=T-2*sig;hi=T+2*sig;d=z1-z0
    rlo=min((d-2*eps)/lo,(d-2*eps)/hi)
    rhi=max((d+2*eps)/lo,(d+2*eps)/hi)
    return max(mp.mpf(0),(rlo-q)/(1+eta)),(rhi+q)/(1-eta)

def serial(q):return {k:mp.nstr(v,mp.mp.dps) for k,v in q.items()}
def run(dps):
    mp.mp.dps=dps;rows={};H0=mp.mpf(1)/200;eta=mp.mpf('.0005');delta=mp.mpf('.1')
    for label,T,lam,E in [('short_base','1.6',1,1),('short_double','1.6',2,1),('long_base','200',1,1),('long_double','200',2,1),('long_boost','200',1,10)]:
        arr=[]
        for k in range(5):
            ell=mp.mpf(T)*k/4
            r=fixed_time(mp.mpf(lam),mp.mpf(10*lam),H0/lam,mp.mpf(E),mp.mpf(20000000*lam),ell)
            assert r['R']>=r['R_initial']
            assert abs(r['K_over_H']-1)<eta
            assert r['theta']>0
            arr.append(r)
        rows[label]=arr
    common=[]
    for a,b in zip(rows['short_base'],rows['short_double']):
        z=(a['logZ']+b['logZ'])/2;th=(a['theta']+b['theta'])/2
        certificates=[]
        for r in [a,b]:
            ez=abs(z-r['logZ'])+r['H']*(1+eta)*delta/2
            et=abs(th-r['theta'])+r['H']/290000*delta/2
            assert ez<mp.mpf('.003') and et<mp.mpf('5e-8')
            certificates.append({'log_window_error_upper':mp.nstr(ez,dps),'angle_window_error_upper':mp.nstr(et,dps)})
        common.append({'ell':mp.nstr(a['ell'],dps),'reported_log':mp.nstr(z,dps),'reported_angle':mp.nstr(th,dps),'certificates':certificates})
    shortband=enclosure(mp.mpf(common[0]['reported_log']),mp.mpf(common[-1]['reported_log']),mp.mpf('1.6'))
    assert shortband[0]<=H0/2<=H0<=shortband[1]
    long=[]
    for label in ['long_base','long_boost']:
        observed=[r['logZ']+mp.mpf('.002')*k for r,k in zip(rows[label],[-1,1,0,-1,1])]
        band=enclosure(observed[0],observed[-1],mp.mpf(200))
        assert band[0]<H0<band[1]
        assert (band[1]-band[0])/H0<mp.mpf('.025')
        assert H0/2<band[0]
        long.append({'label':label,'observed_log':[mp.nstr(z,dps) for z in observed],
          'H_enclosure':[mp.nstr(z,dps) for z in band],'relative_width':mp.nstr((band[1]-band[0])/H0,dps),
          'source_drift_bound':'.000005','log_error_bound':'.003','each_time_error':'.2'})
    # This finite angular comparison is diagnostic, not an all-parameter inverse theorem.
    a=rows['long_base'][-1];b=rows['long_double'][-1]
    difference=abs(a['theta']-b['theta'])
    margin=difference-(a['H']+b['H'])/290000*(mp.mpf('.2')+delta/2)-2*mp.mpf('5e-8')
    assert margin>0
    # Deliberately treating untimed homothetic data as the same timed record fails.
    assert abs(rows['long_base'][-1]['logZ']-rows['long_double'][-1]['logZ'])>mp.mpf('.1')
    return dict(dps=dps,records={key:[serial(q) for q in arr] for key,arr in rows.items()},
      short_common_records=common,short_H_enclosure=[mp.nstr(z,dps) for z in shortband],
      long_enclosures=long,long_angle_pair_separation_margin=mp.nstr(margin,dps),
      incorrect_same_time_homothety='REJECTED by displayed actual-record difference')

if __name__=='__main__':
    frozen=json.loads((B/'CANDIDATE_FREEZE.json').read_text())
    assert hashlib.sha256(SRC.read_bytes()).hexdigest()==frozen['sha256'][str(SRC)]
    spec=importlib.util.spec_from_file_location('reviewed_tsi',SRC);tsi=importlib.util.module_from_spec(spec);spec.loader.exec_module(tsi)
    result=dict(python=platform.python_version(),mpmath=mp.__version__,code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),reused_evaluator_sha256=hashlib.sha256(SRC.read_bytes()).hexdigest(),exact=exact(),precisions=[])
    for dps in [40,70]:
        result['precisions'].append(run(dps));print('precision',dps,'PASS',flush=True)
    mp.mp.dps=70;errs=[]
    for label in result['precisions'][0]['records']:
        for lo,hi in zip(*(p['records'][label] for p in result['precisions'])):
            for key in ['R','b','logZ','theta','K_length']:
                errs.append(abs(mp.mpf(lo[key])-mp.mpf(hi[key]))/max(1,abs(mp.mpf(hi[key]))))
    assert max(errs)<mp.mpf('1e-25')
    result.update(status='PASS',max_scaled_precision_error=mp.nstr(max(errs),70),finite_incidence_cases=50,
        coverage='Two scale companions, five common times, short/long records, E1/E10 long controls.50 solves including40/70-digit repeats. Exact domain/uncertainty proofs are separate.')
    with (B/'CONSTRUCTION_RESULT.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({'status':'PASS','finite_incidence_cases':50,'max_scaled_precision_error':result['max_scaled_precision_error']}))
