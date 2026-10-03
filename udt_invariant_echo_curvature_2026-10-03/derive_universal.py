"""Finite formal symmetric-pair expansion. Geometry assumptions are in the plan.
No supplied response equation; degree7 group log determines interval through8.
FREE method controls: two letters, degree7, exact rational polynomials.
"""
from fractions import Fraction as Q
from math import factorial
from pathlib import Path
import json,time,platform
import sympy as S
B=Path(__file__).resolve().parent
start=time.monotonic();MAX=7
# keys (noncommutative word, x exponent, y exponent); U='u', n='n'.
def mul(a,b):
 c={}
 for (w,i,j),v in a.items():
  for (z,k,l),q in b.items():
   if len(w)+len(z)>MAX:continue
   t=(w+z,i+k,j+l);c[t]=c.get(t,Q(0))+v*q
 assert len(c)<200000
 return {t:v for t,v in c.items() if v}
def add(a,b,factor=Q(1)):
 c=a.copy()
 for t,v in b.items():c[t]=c.get(t,Q(0))+factor*v
 return {t:v for t,v in c.items() if v}
def exp(letter,which,scalar):
 return {(letter*d,d if which=='x' else 0,d if which=='y' else 0):Q(scalar**d,factorial(d)) for d in range(MAX+1)}
p={('',0,0):Q(1)}
for args in [('u','x',-1),('n','',1),('u','y',2),('n','',1),('u','x',-1)]:p=mul(p,exp(*args))
v=add(p,{('',0,0):Q(1)},-1);log={};power={('',0,0):Q(1)}
for d in range(1,MAX+1):
 power=mul(power,v);log=add(log,power,Q((-1)**(d+1),d))
assert all(len(w)%2 for w,i,j in log)
x,y=S.symbols('x y',real=True)
# Dynkin projection D_left(L_d)=d L_d, then divide2 for radial half-log.
z={d:{} for d in [1,3,5,7]}
for (word,i,j),val in log.items():
 d=len(word);sgn=1
 if d==1:key=word
 else:
  if word[0]==word[1]:continue
  if word[:2]=='nu':sgn=-1
  key=('A' if word[2]=='u' else 'B')+word[3:]
  # degree3 C.U=A, C.n=B; each two further brackets contributes -R.
 c=S.Rational(val.numerator,val.denominator)*sgn*x**i*y**j/(2*d)
 z[d][key]=z[d].get(key,0)+c
for d in z:z[d]={k:S.factor(v) for k,v in z[d].items() if S.expand(v)!=0}
t,a,b,c=S.symbols('T aa ab bb',real=True)
K={(i,j):S.Symbol('K'+str(i)+str(j),real=True) for i in range(4) for j in range(i,4)}
def kv(i,j):return K[tuple(sorted([i,j]))]
def ix(root,last):return {'Au':0,'An':1,'Bu':2,'Bn':3}[root+last]
def dot3(v,w):return a if v==w=='A' else c if v==w=='B' else b
# C=R(n,U), so C.u=A,C.n=B; R(w,e)=sign*C.
def sign(w,e):return 0 if w==e else (1 if (w,e)==('n','u') else -1)
def cv(w):return 'A' if w=='u' else 'B'
def pairing(v,w):
 if len(v)>len(w):return pairing(w,v)
 if v in ['u','n']:
  if w in ['u','n']:return (-1 if v=='u' else 1) if v==w else 0
  if len(w)==1:return {('u','A'):0,('u','B'):-t,('n','A'):t,('n','B'):0}[v,w]
  if len(w)==3:return sign(w[2],v)*dot3(w[0],cv(w[1]))
  if len(w)==5:return sign(w[4],v)*kv(ix(w[0],w[1]),ix(cv(w[3]),w[2]))
 if len(v)==len(w)==1:return dot3(v,w)
 if len(v)==1 and len(w)==3:return kv(ix(w[0],w[1]),ix(v,w[2]))
 raise ValueError((v,w))
def dp(i,j):
 return S.expand(sum(v*w*pairing(k,l) for k,v in z[i].items() for l,w in z[j].items()))
f={2:dp(1,1),4:2*dp(1,3),6:2*dp(1,5)+dp(3,3),8:2*dp(1,7)+2*dp(3,5)}
f={d:S.factor(v) for d,v in f.items()}
# Solve future roots with fixed proper preparation L, x=s/L,y=b/L.
# Formal epsilon=L^2; construct arrival b/L=1+B2 e+B4 e²+B6 e³,
# return a/L=2+A2 e+A4 e²+A6 e³ using original F(a,b), not F(b,a).
e=S.Symbol('e');F=sum(f[d]*e**((d-2)//2) for d in f)
def tr(expr,degree=4):return S.series(expr,e,0,degree).removeO().expand()
Bc=[];Ac=[];yy=S.Integer(1);xx=S.Integer(2)
for order in range(1,4):
 zc=S.Symbol('bc'+str(order));trial=yy+zc*e**order
 eq=tr(F.subs({x:0,y:trial}),order+1).coeff(e,order)
 sol=S.solve(eq,zc)[0];Bc.append(S.factor(sol));yy+=sol*e**order
 zc=S.Symbol('ac'+str(order));trial=xx+zc*e**order
 eq=tr(F.subs({x:trial,y:yy},simultaneous=True),order+1).coeff(e,order)
 sol=S.solve(eq,zc)[0];Ac.append(S.factor(sol));xx+=sol*e**order
Fx=S.diff(F,x);Fy=S.diff(F,y)
pser=tr(-Fx.subs({x:0,y:yy})/Fy.subs({x:0,y:yy}))
qser=tr(-Fy.subs({x:xx,y:yy},simultaneous=True)/Fx.subs({x:xx,y:yy},simultaneous=True))
D=tr(S.log(qser)-S.log(pser)+S.log(2-pser**2))
# Lie triple integrability gives R(A,n)=R(B,U); identify bivectors1and2.
rels={K[1,2]:K[1,1],K[2,2]:K[1,1],K[0,2]:K[0,1],K[2,3]:K[1,3]}
Dcoeff={str(2*i):str(S.factor(D.coeff(e,i).subs(rels,simultaneous=True))) for i in range(1,4)}
out={'status':'EXPLORATORY_FORMAL_RESULT','method':'universal degree7 Cartan half-log and actual two future roots; geometry/projection require independent review','python':platform.python_version(),'sympy':S.__version__,'duration_seconds':time.monotonic()-start,'terms_log':len(log),'Z':{str(d):{k:str(v) for k,v in m.items()} for d,m in z.items()},'interval':{str(d):str(v) for d,v in f.items()},'first_arrival':list(map(str,Bc)),'return_arrival':list(map(str,Ac)),'p':str(S.factor(pser)),'q':str(S.factor(qser)),'D_raw':str(S.factor(D)),'D_coefficients':Dcoeff,'invariant_definitions':'A=R(n,U)U; B=R(n,U)n; T=g(A,n); aa=g(A,A),ab=g(A,B),bb=g(B,B); Kij=R(V_i,Z_i,V_j,Z_j), pairs (A,U),(A,n),(B,U),(B,n).'}
(B/'UNIVERSAL_FORMAL_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'duration':out['duration_seconds'],'D':Dcoeff}))
