#!/usr/bin/env python3
import hashlib,json,os,resource
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(2147483648,2147483648))
assert os.environ['OPENBLAS_NUM_THREADS']=='1' and os.environ['OMP_NUM_THREADS']=='1'
import mpmath as mp
mp.mp.dps=60
base=Path(__file__).resolve().parent
datafile=base.parent/'CONSTRUCTION_RESULT.json'
data=json.loads(datafile.read_text()); rows=data['ray_records']
assert len(rows)==40
def num(x):return mp.mpf(x)
def dot(g,u,w):return sum(g[i]*u[i]*w[i] for i in range(4))
max_contraction=max_sky=mp.mpf(0)
groups={}
for row in rows:
    groups.setdefault((row['dps'],row['Lambda'],row['phi0']),[]).append(row)
    L=num(row['Lambda']);R=num(row['R']);b=num(row['b'])
    a=mp.mpf(10);f=1-2/R-L*R**2/3;fe=1-2/a-L*a*a/3
    v=mp.sqrt(1-f);q=mp.sqrt(1-f*b*b/R**2)
    h=1-3/a;om=mp.sqrt(1/a**3-L/3)
    go=[-f,1/f,R*R,R*R];ge=[-fe,1/fe,a*a,a*a]
    uo=[1/f,v,0,0];ue=[1/mp.sqrt(h),0,0,om/mp.sqrt(h)]
    ko=[1/f,q,0,b/R**2];ke=[1/fe,mp.sqrt(1-fe*b*b/a**2),0,b/a**2]
    wo=-dot(go,uo,ko);we=-dot(ge,ue,ke)
    er=[v/f,1,0,0];ep=[0,0,0,1/R]
    sky=[-dot(go,ko,er)/wo,-dot(go,ko,ep)/wo]
    delta=abs(we/wo-num(row['Z_endpoint']))
    angular=max(abs(sky[j]+num(row['n_propagation'][j])) for j in range(2))
    tolerance=mp.mpf('1e-28') if row['dps']==36 else mp.mpf('1e-50')
    assert delta<tolerance and angular<tolerance
    max_contraction=max(max_contraction,delta);max_sky=max(max_sky,angular)

max_arrival=max_drift=max_incidence=max_tau=max_det=max_analytic_drift=mp.mpf(0)
step_records=[];quad_records=[];wrong_first=None
for key,rr in groups.items():
    rr.sort(key=lambda r:num(r['t_e']))
    mid=rr[2];L=num(mid['Lambda']);R=num(mid['R']);b=num(mid['b'])
    h=mp.mpf('0.7');omega=mp.sqrt(mp.mpf('0.001')-L/3)
    f=lambda x:1-2/x-L*x*x/3
    v=lambda x:mp.sqrt(1-f(x))
    s=lambda x,p:mp.sqrt(1-f(x)*p*p/(x*x))
    A=lambda x,p:(1-v(x)*s(x,p))/f(x)
    analytic=None
    if key[0]==60:
        integrate=lambda fun,lo,hi:mp.quadgl(fun,[lo,hi])
        T=integrate(lambda x:1/(f(x)*s(x,b)),10,R)
        P=integrate(lambda x:b/(x*x*s(x,b)),10,R)
        O=integrate(lambda x:1/(f(x)*v(x)),50,R)
        tau=integrate(lambda x:1/v(x),50,R)
        I=integrate(lambda x:1/(x*x*s(x,b)**3),10,R)
        inc=max(abs(T-O+num(mid['t_e'])),abs(P+omega*num(mid['t_e'])+num(mid['phi0'])))
        tauerr=abs(tau-num(mid['tau_o']))
        det=-I*A(R,b)/v(R)
        deterr=abs(det-num(mid['incidence_jacobian_det']))
        assert max(inc,tauerr,deterr)<mp.mpf('1e-45')
        Rdot=v(R)*(1-omega*b)/A(R,b)
        bdot=(-omega-b*Rdot/(R*R*s(R,b)))/I
        logZdot=-omega*bdot/(1-omega*b)-(mp.diff(lambda x:A(x,b),R)*Rdot+mp.diff(lambda p:A(R,p),b)*bdot)/A(R,b)
        analytic=logZdot/mp.sqrt(h)
        max_incidence=max(max_incidence,inc);max_tau=max(max_tau,tauerr);max_det=max(max_det,deterr)
        quad_records.append({'Lambda':mid['Lambda'],'phi0':mid['phi0'],'incidence_error':str(inc),'arrival_error':str(tauerr),'determinant_error':str(deterr),'analytic_optical_drift':str(analytic)})
    arrival_errors=[];drift_errors=[]
    for left,right in [(0,4),(1,3)]:
        lo=rr[left];hi=rr[right]
        de=(num(hi['t_e'])-num(lo['t_e']))*mp.sqrt(h)/2
        tm=num(lo['tau_o']);tc=num(mid['tau_o']);tp=num(hi['tau_o'])
        Zarr=(tp-tm)/(2*de)
        A2=(tp-2*tc+tm)/de**2
        slope=(num(hi['Z_endpoint'])-num(lo['Z_endpoint']))/(tp-tm)
        derr=abs(A2/Zarr-slope);aerr=abs(Zarr-num(mid['Z_endpoint']))
        assert aerr<mp.mpf('1e-7') and derr<mp.mpf('1e-7')
        arrival_errors.append(aerr);drift_errors.append(derr)
        if analytic is not None:
            ad=abs(analytic-slope)
            assert ad<mp.mpf('1e-7')
            max_analytic_drift=max(max_analytic_drift,ad)
        if key==(36,'0','-0.2') and left==0:
            wrong_first=abs(A2/(Zarr*Zarr)-slope)
            assert wrong_first>mp.mpf('1e-4')
    assert arrival_errors[1]<mp.mpf('.4')*arrival_errors[0]+mp.mpf('1e-25')
    assert drift_errors[1]<mp.mpf('.4')*drift_errors[0]+mp.mpf('1e-25')
    max_arrival=max(max_arrival,*arrival_errors);max_drift=max(max_drift,*drift_errors)
    step_records.append({'key':key,'arrival_errors':list(map(str,arrival_errors)),'drift_errors':list(map(str,drift_errors))})
result={'status':'PASS','input_sha256':hashlib.sha256(datafile.read_bytes()).hexdigest(),'saved_rows':40,'independent_quadrature_midpoints':4,'dps':60,'max_endpoint_contraction_error':str(max_contraction),'max_sky_error':str(max_sky),'max_incidence_error':str(max_incidence),'max_arrival_integral_error':str(max_tau),'max_determinant_error':str(max_det),'max_arrival_frequency_error':str(max_arrival),'max_drift_arrival_error':str(max_drift),'max_analytic_drift_difference':str(max_analytic_drift),'original_defect_reproduced':str(wrong_first),'groups':step_records,'quadrature':quad_records,'mpmath_version':mp.__version__,'maxrss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(base/'SAVED_CHECK_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['groups','quadrature']},indent=2))
