"""Independent SymPy rational verification of saved ceiling certificate."""
from pathlib import Path
import hashlib,json,resource
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
import sympy as s
p=Path(__file__).resolve().parent
src=p.parent/'CEILING_EXACT_RESULT.json'
data=json.loads(src.read_text())
Q=s.Rational
m,a,H,E=(Q(data[k]) for k in ['m','a','H','E'])
f=lambda r:1-2*m/r-H**2*r**2
b2=Q(999,1000)**2*a*a/f(a)
S2=1+H*H*b2
assert b2==Q(data['b_squared']) and S2==Q(data['S_squared'])
assert a>3*m and f(a)>0 and m/a**3-H**2>0 and b2<a*a/f(a)
r=s.symbols('r',positive=True)
w2=1-b2*(1-2*m/r)/(r*r*S2)
deriv=s.factor(s.diff(w2,r))
assert s.simplify(deriv-2*b2*(r-3*m)/(S2*r**4))==0
rows=[]
total=Q(0)
previous=a
for row in data['rows']:
 left,right,q=Q(row['left']),Q(row['right']),Q(row['q_lower'])
 assert left==previous and right>left and left>=a and q>0
 wr=s.cancel(w2.subs(r,right))
 assert wr==Q(row['w2_at_right']) and 0<wr<1
 margin=s.cancel(1-q*q*wr)
 assert margin>=0
 # Concrete negative control: doubling the proposed lower bound must fail.
 false_margin=s.cancel(1-(2*q)**2*wr)
 assert false_margin<0
 total+=(right-left)*q
 rows.append({'left':str(left),'right':str(right),'valid_margin':str(margin),'doubled_q_margin_rejected':str(false_margin)})
 previous=right
Jlo=total-previous
Slo=Q(data['S_lower'])
assert Slo>0 and Slo*Slo<S2 and Jlo>0
margin=H*Slo*Jlo-E
Blo=Jlo/H-E/(H*H*Slo)
assert margin>0 and Blo>0
assert Jlo==Q(data['J_lower']) and margin==Q(data['positive_margin']) and Blo==Q(data['B_lower'])
out={'status':'PASS_EXACT_CERTIFICATE','method':'independent symbolic derivative and rational checking of supplied lower-bound certificate; no parent code execution','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'monotonic_derivative':str(deriv),'rational_intervals':len(rows),'negative_controls_rejected':len(rows),'rows':rows,'J_lower':str(Jlo),'positive_margin':str(margin),'B_lower':str(Blo),'finite_numeric_cases_so_far':30,'conservative_count_including_each_certificate_and_negative_control':30+2*len(rows)}
(p/'EXACT_CERTIFICATE_RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
