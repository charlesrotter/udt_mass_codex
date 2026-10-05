#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,resource
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
HERE=Path(__file__).resolve().parent
source=HERE.parent/'CEILING_EXACT_RESULT.json'
d=json.loads(source.read_text())
m,a,H,E=map(F,[d[x] for x in ['m','a','H','E']])
fa=1-2*m/a-H*H*a*a
assert a>3*m and fa>0 and m/a**3>H*H
b2=F(999,1000)**2*a*a/fa
S2=1+H*H*b2
Slo=F(d['S_lower'])
assert b2==F(d['b_squared']) and S2==F(d['S_squared'])
assert b2<a*a/fa and Slo*Slo<S2
last=a
lower=-a
out=[]
for row in d['rows']:
    left,right,q=map(F,[row[k] for k in ['left','right','q_lower']])
    assert left==last and right>left
    w2=(1-b2*(1-2*m/right-H*H*right*right)/(right*right))/S2
    assert w2==F(row['w2_at_right']) and 0<w2<1 and q*q*w2<=1
    lower+=(right-left)*(q-1)
    last=right
    out.append({'q':str(q),'w2':str(w2),'bound_margin':str(1-q*q*w2)})
B=lower/H-E/(H*H*Slo)
assert lower==F(d['J_lower']) and B==F(d['B_lower']) and B>0
bad_q=2*F(d['rows'][0]['q_lower'])
bad_w2=F(d['rows'][0]['w2_at_right'])
assert bad_q*bad_q*bad_w2>1
r={'passed':True,'B_lower':str(B),'J_lower':str(lower),'rows':out,
   'doubled_first_q_rejected':True,'exact_case_count':2,'conservative_cumulative_cases':73,
   'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
   'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'CERTIFICATE_RESULT.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'passed':True,'B_lower':str(B),'doubled_q_rejected':True}))
