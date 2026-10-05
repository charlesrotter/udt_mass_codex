"""Exact rational lower bound for a reviewer-discovered affine-limit counterexample."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json
B=Path(__file__).resolve().parent
m=F(1);a=F(3001,1000);H=F(9,50);E=F(1)
fa=1-2*m/a-H*H*a*a
b2=F(999,1000)**2*a*a/fa
S2=1+H*H*b2
Slo=F(14,5)
assert a>3*m and fa>0 and m/a**3-H*H>0
assert b2<a*a/fa and Slo*Slo<S2
grid=[a,F(301,100),F(302,100),F(305,100),F(31,10),F(32,10),F(35,10),F(4),F(5),F(6)]
rows=[];integral_lower=F(0)
for left,right in zip(grid,grid[1:]):
    # w²=s²/S² increases with r>a>3m, so 1/w decreases.
    w2=1-b2*(1-2*m/right)/(right*right*S2)
    assert 0<w2<1
    # q=floor(1000/sqrt(w²))/1000, computed solely with integers.
    q=F(isqrt((1000000*w2.denominator)//w2.numerator),1000)
    assert q*q*w2<=1
    integral_lower+=(right-left)*q
    rows.append({'left':str(left),'right':str(right),'w2_at_right':str(w2),'q_lower':str(q)})
# J=S*C=-a+integral_a^infty(S/s-1)dr. Remaining tail is positive.
Jlower=integral_lower-grid[-1]
margin=H*Slo*Jlower-E
assert Jlower>0 and margin>0, (Jlower,margin)
# B=S*C/H-E/(H²*S)=J/H-E/(H²*S) > margin/(H²*Slo)>0.
Blower=margin/(H*H*Slo)
r={'status':'PASS_EXACT_RATIONAL','m':str(m),'a':str(a),'H':str(H),'E':str(E),
   'b_star':'negative sqrt(b_squared)','b_squared':str(b2),'S_squared':str(S2),
   'S_lower':str(Slo),'rows':rows,'J_lower':str(Jlower),'positive_margin':str(margin),
   'B_lower':str(Blower),'meaning':'D_o=1/H+B/R+O(R^-2), B>positive rational lower bound; eventual above-limit approach within conditional class, not UDT countermodel'}
with (B/'CEILING_EXACT_RESULT.json').open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(json.dumps({'status':r['status'],'B_lower':str(Blower),'positive_margin':str(margin)}))
