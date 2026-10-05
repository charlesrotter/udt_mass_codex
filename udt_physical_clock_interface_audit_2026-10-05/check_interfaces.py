"""PIA1 bounded arithmetic anchors; no empirical fit or geometric solve."""
from fractions import Fraction as F
import json, platform, hashlib
from pathlib import Path
import mpmath as mp
mp.mp.dps=70
checks=[]
def record(name,passed,**values):
    assert passed,name
    checks.append(dict(name=name,status='PASS',**{k:str(v) for k,v in values.items()}))
def m(q):return mp.mpf(q.numerator)/q.denominator
num=F(9991,10000); hmax=F(17,20); alpha=F(1000000006,1000000000); ymax=F(1,50000)
record('exact_squared_Z_floor',num*num>F(54180)**2*hmax*alpha**2*ymax**2,
       floor_squared=num*num/(hmax*alpha**2*ymax**2),decimal_floor=m(num)/(mp.sqrt(m(hmax))*m(alpha)*m(ymax)))
record('exact_shape_ratios',1/(F(1,10)*ymax)==500000 and 1/(F(1,100)*ymax)==5000000,
       R_over_a_min=500000,R_over_m_min=5000000)
eta=F(1,2000); q_over_H=F(1,1000); Hdelta=F(1,2000)
d=(1+eta+q_over_H)*Hdelta; bias=d*d/8
record('exact_phase_estimator_bias',bias<F(314,10**10),bias=bias,decimal=m(bias))
j=mp.log(mp.sinh(m(d)/2)/(m(d)/2))
record('linear_Y_phase_counter_control',0<j<m(bias),gap=j,bound=m(bias))
r=1-mp.exp(-mp.mpf('.003'))
record('log_relative_error_conversion',abs(-mp.log(1-r)-mp.mpf('.003'))<mp.mpf('1e-65'),r=r)
angle=mp.mpf('5e-8')*180/mp.pi*3600*1000
record('angular_unit_conversion',mp.mpf('10.31')<angle<mp.mpf('10.32'),mas=angle)
record('long_short_duration_and_source_budget',F(1,200)*200==1 and F(1,200)*F(8,5)==F(1,125)
       and F(5,10**6)/F(1,200)==q_over_H,C_long=1,C_short=F(1,125),q_over_H=q_over_H)
# Analytic two-history readout equality: Z_i=exp(K_i*t), constant source1;
# source2 composed with its own emission map has log frequency (K2-K1)*t.
K1=F(1,100);K2=F(1,50);t=F(3,2)
Y1=K1*t;Y2=K2*t-(K2-K1)*t
record('unrestricted_source_drift_ambiguity',Y1==Y2,Y1=Y1,Y2=Y2)
# A bounded-amplitude source need not have a bounded rate without regularity.
amplitude=F(1,1000);rates=[amplitude*w for w in (1,1000000)]
record('bounded_amplitude_not_rate_bound',rates[1]/rates[0]==1000000,amplitude=amplitude,peak_derivatives=rates)
Qe=F(1,100); Zmin=F(54180);qo=Qe/Zmin
record('source_time_conversion',qo*Zmin==Qe,emitter_Q=Qe,receiver_q_upper=qo)
out={'status':'PASS','cases':len(checks),'scope':'Exact arithmetic and70-digit illustrative anchors; written argument owns continuum bounds. No numerical interval certification, observation, source-law derivation or domain admission.',
     'python':platform.python_version(),'mpmath':mp.__version__,'dps':mp.mp.dps,
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks':checks}
with Path('udt_physical_clock_interface_audit_2026-10-05/CONSTRUCTION_RESULT.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out,indent=2))
