"""No new incidence cases: independently audit saved angular margin and coarse bounds."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
import mpmath as mp
mp.mp.dps=75
OUT=Path(__file__).parent;PKG=OUT.parent
source=json.loads((OUT/'SAVED_REPLAY.json').read_text())
rows=source['comparisons']
a=next(r for r in rows if r['label']=='long_base' and mp.mpf(r['ell'])==200)
b=next(r for r in rows if r['label']=='long_double' and mp.mpf(r['ell'])==200)
margin=abs(mp.mpf(a['own']['theta'])-mp.mpf(b['own']['theta']))-(mp.mpf('.005')+mp.mpf('.0025'))/290000*(mp.mpf('.2')+mp.mpf('.05'))-mp.mpf('1e-7')
parent=json.loads((PKG/'CONSTRUCTION_RESULT.json').read_text())['precisions'][-1]
assert margin>0 and abs(margin-mp.mpf(parent['long_angle_pair_separation_margin']))<mp.mpf('1e-60')
# Independently chosen coarse rational bound chain, not parent-bound function.
y=F(1,50000);B=F(1,10000);sm=F(999,1000);sp=F(1001,1000);W=F('1.00000002')
I=(10-y)/sp**3;J=(1-9*B)*I
assert B*J>9*y
bp=(B/sm+9*F('1.000000006')/(1-9*B))/I
assert bp<1
logF=9/(1-9*B)+F('10.002')+F('.000101')
assert logF<20 and W-1+W*y*20<F(1,2000)
yw=F('0.00001001');Bw=F('0.00001');Iw=(20-yw)/sp**3
assert Iw>F('19.94')
bpw=(Bw/sm+F(25,4)*F('1.000000006')/(1-F(25,4)*Bw))/F('19.94')
assert bpw<F('.314')
timing=F(1,200)*(F(1,2)+F(3,2)*F(1,2000))*F('1.6')/2+F(1,200)*(1+F(1,2000))*F('.1')/2
angular=F(3,4)*F(1,200)*F('1.6')/290000+F(1,200)*F('.1')/(2*290000)
assert timing<F('.003') and angular<F('5e-8')
r=dict(status='PASS',additional_incidence_cases=0,total_independent_incidence_cases=56,angular_margin=mp.nstr(margin,70),independent_rational_bounds={k:str(v) for k,v in dict(I=I,J=J,Bprime=bp,logFprime=logF,witness_I=Iw,witness_Bprime=bpw,short_log_upper=timing,short_angle_upper=angular).items()},script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(OUT/'REMAINING_ARITHMETIC.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r))
