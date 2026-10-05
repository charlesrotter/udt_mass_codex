"""Independent source-first finite-incidence check; no candidate imports."""
import hashlib,json,platform
from pathlib import Path
import mpmath as mp

ROOT=Path(__file__).resolve().parent
def calc(Hstring,tstring,dps):
    mp.mp.dps=dps
    H=mp.mpf(Hstring);ell=mp.mpf(tstring)
    mu=mp.mpf('.005');A=mp.mpf('.05');y0=mp.mpf('.00001');E=mp.mpf(1)
    w=mp.sqrt(mu/A**3-1);h=1-3*mu/A
    Q=lambda z:1-z*z+2*mu*z**3
    W=lambda z:mp.sqrt(1+2*mu*z**3)
    # Exact E=1 radial receiver, parameter is proper length time ell.
    phase=mp.asinh(1/mp.sqrt(2*mu*y0**3))+mp.mpf('1.5')*H*ell
    y=(2*mu*mp.sinh(phase)**2)**(-mp.mpf(1)/3)
    d=mp.quad(lambda z:1/(W(z)*(E*z+W(z))),[0,y])
    ss=lambda z,B:mp.sqrt(1+B*B*Q(z))
    P=lambda B:mp.quad(lambda z:B/ss(z,B),[y,1/A])
    U=lambda B:mp.quad(lambda z:B*B/(ss(z,B)*(1+ss(z,B))),[y,1/A])
    G=lambda B:P(B)-w*U(B)-w*d
    B=mp.findroot(G,(mp.mpf('0'),w*A*y),tol=mp.mpf('1e-'+str(dps-10)),solver='secant')
    residual=abs(G(B));s=ss(y,B);Wv=W(y);D=E*y+Wv
    alpha=1/D+Wv*B*B/(1+s)
    Z=(1-w*B)/(mp.sqrt(h)*y*alpha)
    I=mp.quad(lambda z:1/ss(z,B)**3,[y,1/A])
    Bp=(B/s+w*alpha/(Wv*(1-w*B)))/I
    Wp=3*mu*y*y/Wv
    Sp=(B*Bp*Q(y)+B*B*(-y+3*mu*y*y))/s
    alphap=-(E+Wp)/D**2+Wp*B*B/(1+s)+2*Wv*B*Bp/(1+s)-Wv*B*B*Sp/(1+s)**2
    logFp=-w*Bp/(1-w*B)-alphap/alpha
    KoverH=Wv*(1-y*logFp)
    nphi=B/alpha;nr=(s/D-Wv*B*B/(1+s))/alpha
    theta=mp.atan2(nphi,nr)
    theta_p=(Bp/alpha-B*alphap/alpha**2)/nr
    theta_rate=-H*y*Wv*theta_p
    out=dict(H=H,ell=ell,y=y,B=B,logZ=mp.log(Z),theta=theta,KoverH=KoverH,
             original_incidence_residual=residual,direction_norm_error=abs(nphi*nphi+nr*nr-1),
             theta_rate=theta_rate,emitter_coordinate_time=-(d+U(B))/H)
    assert residual<mp.mpf('1e-55')
    assert out['direction_norm_error']<mp.mpf('1e-55')
    assert 0<y<mp.mpf('.00002') and 0<B<mp.mpf('.0001') and 1-w*B>0 and nr>0
    assert abs(KoverH-1)<mp.mpf('.0005')
    assert abs(theta_rate)<mp.mpf('3e-5')*H
    return {k:mp.nstr(v,dps) for k,v in out.items()}

times=['-.05','0','.05','1.55','1.6','1.65','199.95','200','200.05']
rows=[]
for dps in [70,90]:
    for H in ['.005','.0025']:
        for t in times:
            r=calc(H,t,dps);r['dps']=dps;rows.append(r)
checks={};diffs={}
for H in ['.005','.0025']:
    for t in times:
        pair=[r for r in rows if mp.mpf(r['H'])==mp.mpf(H) and mp.mpf(r['ell'])==mp.mpf(t)]
        for key in ['B','logZ','theta','KoverH']:
            delta=abs(mp.mpf(pair[0][key])-mp.mpf(pair[1][key]))
            diffs[f'{H}:{t}:{key}']=mp.nstr(delta,10)
            assert delta<mp.mpf('1e-45')
# Angular proof, separate from sampled rates: alpha>=1/Dmax, |alpha'/alpha|<10.003,
# B'<1, B<=1e-4, n_r=sqrt(1-n_phi^2), hence theta_y<1.01.
Dmax=mp.mpf('1.00020002');Bmax=mp.mpf('.0001')
theta_y_bound=(Dmax+Bmax*Dmax*mp.mpf('10.003'))/mp.sqrt(1-(Bmax*Dmax)**2)
assert theta_y_bound<mp.mpf('1.01')
assert mp.mpf('.00002')*mp.mpf('1.00000002')*theta_y_bound<mp.mpf('.00003')
midpoint_rows=[]
for t in ['0','1.6','200']:
    rr=[r for r in rows if r['dps']==90 and mp.mpf(r['ell'])==mp.mpf(t)]
    midpoint={key:(mp.mpf(rr[0][key])+mp.mpf(rr[1][key]))/2 for key in ['logZ','theta']}
    margins=[]
    for r in rr:
        H=mp.mpf(r['H'])
        lb=abs(midpoint['logZ']-mp.mpf(r['logZ']))+H*mp.mpf('1.0005')*mp.mpf('.05')
        ab=abs(midpoint['theta']-mp.mpf(r['theta']))+H*mp.mpf('.00003')*mp.mpf('.05')
        margins.append({'H':str(H),'log_worst_error':mp.nstr(lb,40),'angle_worst_error':mp.nstr(ab,40)})
        if t!='200':
            assert lb<mp.mpf('.003') and ab<mp.mpf('5e-8')
    midpoint_rows.append({'ell':t,'common_log_record':mp.nstr(midpoint['logZ'],50),'common_angle_record':mp.nstr(midpoint['theta'],50),'bounds':margins})
out={'status':'PASS','python':platform.python_version(),'mpmath':mp.__version__,
     'cases_consumed':len(rows),'cases_budget':100,'evidence':'high-precision numerical incidences plus analytic window enclosures',
     'rows':rows,'precision_differences':diffs,'midpoint_records':midpoint_rows,
     'theta_y_bound':mp.nstr(theta_y_bound,40),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
with (ROOT/'INCIDENCE_RESULT.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps({'status':out['status'],'cases':out['cases_consumed'],'midpoint_records':midpoint_rows},indent=2))
