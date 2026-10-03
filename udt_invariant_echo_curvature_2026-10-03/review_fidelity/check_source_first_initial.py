"""IEC1 independently authored ultrastatic symmetric-control calculation."""
from pathlib import Path
import hashlib, json, math, platform, sys
import sympy as S
import mpmath as mp

BASE = Path(__file__).resolve().parent
x, y, K = S.symbols('x y K', real=True)
families = [('orthogonal', S.Rational(3,4), S.Rational(5,4), S.Integer(0)),
            ('tilted', S.Rational(3,4), S.Rational(5,4), S.Rational(3,5)),
            ('static', S.Integer(0), S.Integer(1), S.Rational(3,5))]
records=[]

def convolution(p,q):
    out={}
    for i,v in p.items():
        for j,w in q.items():
            if i+j<=8:out[i+j]=out.get(i+j,0)+v*w
    return out

def cospoly(v):
    return {2*j:(-K)**j*v**(2*j)/S.factorial(2*j) for j in range(5)}

def sinpoly(v):
    return {2*j+1:(-K)**j*v**(2*j+1)/S.factorial(2*j+1) for j in range(4)}

def incidence(u,gamma,b):
    h2=1+b*b*u*u
    # C_K(hL)-1, d S_K(hL), d²[C_K(hL)-1].
    cm={2*j:(-K)**j*h2**j/S.factorial(2*j) for j in range(1,5)}
    ds={2*j+1:b*gamma*(-K)**j*h2**j/S.factorial(2*j+1) for j in range(4)}
    dc={j:b*b*gamma*gamma*v/h2 for j,v in cm.items()}
    f=cospoly(u*(x-y))
    for p,q,factor in [(cm,convolution(cospoly(u*x),cospoly(u*y)),1),
                       (dc,convolution(sinpoly(u*x),sinpoly(u*y)),K),
                       (ds,sinpoly(u*(y-x)),-K)]:
        for j,v in convolution(p,q).items():f[j]=f.get(j,0)+factor*v
    for j,v in cospoly(gamma*(y-x)+b*u).items():f[j]=f.get(j,0)-v
    out=[S.cancel(S.expand(f[j])/K) for j in [2,4,6,8]]
    assert S.expand(out[0]-((y-x)**2-1)/2)==0
    return out

def solve_series(f):
    ev=lambda v:S.expand(v.subs(y,x+1))
    a2=-ev(f[1])
    a4=-S.expand(a2*a2/2+ev(S.diff(f[1],y))*a2+ev(f[2]))
    a6=-S.expand(a2*a4+ev(S.diff(f[1],y))*a4+
                 ev(S.diff(f[1],y,2))*a2*a2/2+
                 ev(S.diff(f[2],y))*a2+ev(f[3]))
    for v in [a2,a4,a6]:
        assert len(S.Poly(v,x,K).terms()) < 200
    return [S.factor(v) for v in [a2,a4,a6]]

def logcoeff(c):
    c2,c4,c6=c
    return [c2,S.expand(c4-c2*c2/2),S.expand(c6-c2*c4+c2**3/3)]

def actual(u,gamma,b,curv,L):
    h=mp.sqrt(1+b*b*u*u); d=b*gamma/h
    if curv==1:C=mp.cos; H=mp.sin
    else:C=mp.cosh; H=mp.sinh
    def f(s,t):
        return (C(u*(s-t))+(C(h*L)-1)*(C(u*s)*C(u*t)+curv*d*d*H(u*s)*H(u*t))
                -curv*d*H(h*L)*H(u*(t-s))-C(gamma*(t-s)+b*u*L))
    first=mp.findroot(lambda t:f(0,t),(L*mp.mpf('.9'),L*mp.mpf('1.1')))
    final=mp.findroot(lambda s:f(s,first),(L*mp.mpf('1.9'),L*mp.mpf('2.1')))
    p=-mp.diff(lambda s:f(s,first),0)/mp.diff(lambda t:f(0,t),first)
    q=-mp.diff(lambda t:f(final,t),first)/mp.diff(lambda s:f(s,first),final)
    r=max(abs(f(0,first)),abs(f(final,first)))
    future1=gamma*first+b*u*L
    future2=gamma*(final-first)-b*u*L
    assert future1>0 and future2>0 and p>0 and q>0 and 2-p*p>0
    assert r<mp.mpf('1e-70')
    D=mp.log(q)-mp.log(p/(2-p*p))
    return first,final,p,q,D,r,future1,future2

mp.mp.dps=90
numeric=[]
for name,u,gamma,b in families:
    assert gamma*gamma-u*u==1
    f=incidence(u,gamma,b)
    outgoing=solve_series(f)
    returning=solve_series([v.xreplace({x:y,y:x}) for v in f])
    p=[S.diff(v,x).subs(x,0) for v in outgoing]
    first2,first4,_=[v.subs(x,0) for v in outgoing]
    g2,g4,g6=returning
    at1=lambda v:v.subs(x,1)
    q=[at1(S.diff(g2,x)),
       at1(S.diff(g2,x,2))*first2+at1(S.diff(g4,x)),
       at1(S.diff(g2,x,2))*first4+at1(S.diff(g2,x,3))*first2**2/2+
       at1(S.diff(g4,x,2))*first2+at1(S.diff(g6,x))]
    P=[S.factor(v) for v in logcoeff(p)];Q=[S.factor(v) for v in logcoeff(q)]
    D=[S.factor(Q[0]-3*P[0]),S.factor(Q[1]-3*P[1]-4*P[0]**2),
       S.factor(Q[2]-3*P[2]-8*P[0]*P[1]-8*P[0]**3)]
    T=K*u*u*(1-b*b)
    assert S.expand(P[0]+T/2)==0 and S.expand(Q[0]+3*T/2)==0
    if name=='static':assert all(v==0 for v in P+Q+D)
    rec={'name':name,'u':str(u),'gamma':str(gamma),'b':str(b),
         'incidence_degree2_4_6_8':[str(v) for v in f],
         'outgoing_scaled_coeff2_4_6':[str(v) for v in outgoing],
         'return_scaled_coeff2_4_6':[str(v) for v in returning],
         'log_p_coeff2_4_6':[str(v) for v in P],
         'log_q_coeff2_4_6':[str(v) for v in Q],
         'D_coeff2_4_6':[str(v) for v in D],
         'T':str(T),'T_Wnorm2_over3':str(S.factor(T*K*K*u*u*gamma*gamma*(1-b*b)/3)),
         'Vnorm2':str(K*K*u**4*(1-b*b)*b*b)}
    records.append(rec)
    if name=='static':continue
    u0=mp.mpf(str(u.p))/int(u.q);g0=mp.mpf(str(gamma.p))/int(gamma.q)
    b0=mp.mpf(str(b.p))/int(b.q)
    for curv in [1,-1]:
        errors=[]
        for inv in [10,20,40,80]:
            L=mp.mpf(1)/inv
            first,final,pv,qv,dv,res,ft1,ft2=actual(u0,g0,b0,curv,L)
            predicted=sum(mp.mpf(str(v.subs(K,curv).p))/int(v.subs(K,curv).q)*L**power
                          for v,power in zip(D,[2,4,6]))
            err=abs(dv-predicted);errors.append(err)
            numeric.append(dict(family=name,K=curv,L=str(L),first=str(first),final=str(final),
                                p=str(pv),q=str(qv),D=str(dv),D_series=str(predicted),
                                error=str(err),original_residual=str(res),
                                future1=str(ft1),future2=str(ft2)))
        # An observed asymptotic order diagnostic; not a certified remainder bound.
        rates=[mp.log(errors[i]/errors[i+1])/mp.log(2) for i in range(3)]
        assert all(r>mp.mpf('7.5') for r in rates)
        rec.setdefault('observed_error_orders',{})[str(curv)]=[str(r) for r in rates]
assert len(numeric)<=30
result={'verdict':'PASS_SCOPED_EXACT_CONTROLS_AND_NUMERICAL_BRANCH_CHECKS',
        'versions':{'python':sys.version,'sympy':S.__version__,'mpmath':mp.__version__,
                    'platform':platform.platform()},
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'symbolic_families':len(families),'scalar_cases':len(numeric),'digits':mp.mp.dps,
        'records':records,'numeric':numeric}
out=BASE/'SOURCE_FIRST_RESULT.json';assert not out.exists()
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'verdict':result['verdict'],'families':len(families),'scalar_cases':len(numeric),
                  'coefficients':[{k:r[k] for k in ['name','D_coeff2_4_6','T_Wnorm2_over3','Vnorm2']}
                                  for r in records]},indent=2))
