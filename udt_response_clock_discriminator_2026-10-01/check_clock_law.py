#!/usr/bin/env python3
"""Finite exact checks of RCD1; general proofs retain written hypotheses."""
from pathlib import Path
import sys,json,hashlib
import sympy as s
B=Path(__file__).resolve().parent
x=s.symbols('L',real=True); coords=(x,*s.symbols('x y z',real=True)); p=s.Function('p')(x)
alpha,lam,h,b3,b4,b5,b6,beta=s.symbols('alpha Lambda H0 b3 b4 b5 b6 beta',real=True)
checks={}
def zero(name,v):
 v=s.factor(s.cancel(v));checks[name]=str(v);assert v==0,(name,v)
def geometry(scale,coordinate):
 g=s.diag(-scale**2,scale**2,scale**2,scale**2);gi=g.inv();n=4
 ga=[[[s.simplify(sum(gi[a,d]*(s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d])) for d in range(n))/2) for c in range(n)]for b in range(n)]for a in range(n)]
 ric=s.Matrix(n,n,lambda a,b:s.simplify(sum(s.diff(ga[k][a][b],coords[k])-s.diff(ga[k][a][k],coords[b])+sum(ga[k][k][j]*ga[j][a][b]-ga[k][b][j]*ga[j][a][k] for j in range(n))for k in range(n))))
 R=s.factor(sum(gi[a,b]*ric[a,b] for a in range(n)for b in range(n)))
 hs=s.Matrix(n,n,lambda a,b:s.simplify(s.diff(R,coords[a],coords[b])-sum(ga[k][a][b]*s.diff(R,coords[k])for k in range(n))))
 box=s.factor(sum(gi[a,b]*hs[a,b]for a in range(n)for b in range(n)))
 G=ric-R*g/2;Q=2*R*ric-R**2*g/2+2*(g*box-hs)
 return g,gi,ric,R,hs,box,G,Q

def main():
 g,gi,ric,R,hs,box,G,Q=geometry(p,x)
 U=3*s.diff(p,x)**2/p**4
 V=36*s.diff(p,x)*s.diff(p,x,3)/p**6-18*s.diff(p,x,2)**2/p**6-72*s.diff(p,x)**2*s.diff(p,x,2)/p**7
 H=s.diff(p,x)/p**2;dt=lambda v:s.diff(v,x)/p
 P=dt(R);K=dt(H);J=2*R*K+dt(P)-H*P
 C=s.factor((G[0,0]+alpha*Q[0,0])/p**2-lam)
 D=s.factor((G[1,1]+alpha*Q[1,1])/p**2+lam)
 zero('scalar_from_original_metric',R-6*s.diff(p,x,2)/p**3)
 zero('U_original_Einstein00',G[0,0]/p**2-U)
 zero('V_original_Q00',Q[0,0]/p**2-V)
 zero('original00_clock_constraint',C-(U+alpha*V-lam))
 zero('original_shape_clock_condition',C+D+2*(K+alpha*J))
 zero('original_conservation',dt(C)+3*H*(C+D))
 zero('derivative_integrated_clock_condition',dt(U+alpha*V)-6*H*(K+alpha*J))
 zero('trace_from_original_metric',sum(gi[a,b]*(G[a,b]+alpha*Q[a,b])for a in range(4)for b in range(4))-(-R+6*alpha*box))
 for a in range(4):
  for b in range(4):
   if a!=b:
    zero(f'Ric_offdiag_{a}{b}',ric[a,b]);zero(f'Q_offdiag_{a}{b}',Q[a,b])
 for i in [2,3]:zero(f'spatial_isotropy_{i}',(G[i,i]+alpha*Q[i,i])/p**2+lam-D)
 sub=lambda expression,q:s.factor(expression.subs(p,q).doit())
 q=1/(1-h*x)
 for name,v in [('U',U-3*h**2),('V',V),('K',K),('J',J)]:zero('constant_H_'+name,sub(v,q))
 zero('flat_constraint',sub(C,1)+lam)
 # Clock-coordinate rescaling, not a new adopted physical scale symmetry.
 ell=s.symbols('ell',positive=True);jets=s.symbols('z0:5');jetmap={s.diff(p,x,k):jets[k] for k in range(5)}
 for name,v,weight in [('U',U,-2),('V',V,-4),('K',K,-2),('J',J,-4)]:
  vv=v.subs(jetmap,simultaneous=True);scaled=vv.subs({jets[k]:jets[k]/ell**k for k in range(5)},simultaneous=True)
  zero('units_'+name,scaled-ell**weight*vv)
 curve=1+b3*x**3+b4*x**4+b5*x**5+b6*x**6
 cs=s.series(sub(C,curve),x,0,5).removeO().expand()
 zero('flat_event_constraint_constant',cs.coeff(x,0)+lam)
 zero('flat_event_L3',cs.coeff(x,3)-864*alpha*b3*b4)
 zero('flat_event_L4',cs.coeff(x,4)-(27*b3**2+alpha*(864*b4**2+3240*b3*b5)))
 zero('cubic_quintic_balance',cs.coeff(x,4).subs({b4:0,b5:-b3/(120*alpha)}))
 u1,u2,v1,v2=s.symbols('u1 u2 v1 v2');aa=(u2-u1)/(v1-v2);ll=u1+aa*v1
 zero('parameter_identification_second_point',u2+aa*v2-ll)
 # Existing PCC1 control evaluated in ORIGINAL proper-time equations, not p chosen cubic.
 t=s.symbols('t',real=True);a=1+beta*t**3;HH=s.diff(a,t)/a;RR=6*(s.diff(HH,t)+2*HH**2);PP=s.diff(RR,t)
 CC=3*(1+2*alpha*RR)*HH**2-alpha*RR**2/2+6*alpha*HH*PP-lam
 coeff=s.series(CC,t,0,6).removeO().expand()
 zero('proper_cubic_initial_constraint',coeff.coeff(t,0)+lam)
 zero('proper_cubic_original00_leading',coeff.coeff(t,4)-27*beta**2)
 zero('proper_cubic_original00_next',coeff.coeff(t,5)-1944*alpha*beta**3)
 trace=-RR+6*alpha*(-s.diff(RR,t,2)-3*HH*PP)+4*lam
 zero('proper_cubic_original_trace_leading',s.series(trace,t,0,2).removeO().expand().coeff(t,1)+36*beta)
 # A held-out point matters: two-point calibration need not satisfy a third.
 wrong_third=s.Rational(1)+aa.subs({u1:0,u2:1,v1:0,v2:1})*2-ll.subs({u1:0,u2:1,v1:0,v2:1})
 assert wrong_third==-1
 result={'status':'PASS','exact_zero_assertions':len(checks),'checks':checks,'third_point_control':{'residual':str(wrong_third),'rejected':True},'scope':'Finite exact verification; written smooth-interval proof owns sufficiency and degeneracy, not check count.','sympy':s.__version__,'python':sys.version.split()[0],'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 out=B/'SYMBOLIC_RESULT.json'
 with out.open('x')as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps({k:v for k,v in result.items()if k!='checks'},indent=2))
if __name__=='__main__':main()
