"""
Step 8: FULL on-shell far-collar limits (static Schur + kinetic dressing).

Derived normal form for kept channel u with response vector v (exact at
leading adiabatic order; the adiabatic control parameter -> 0 as kappa->0
because the partner stiffness y^q M diverges relative to the gradient
scale):
  (y^2 u')' = [ 2 y^q S(kappa)/(1+|v|^2)
                + y^2(|v'|^2(1+|v|^2)-(v.v')^2)/(1+|v|^2)^2 ] u
At kappa->0:  gradient term -> 0 in n-units;  lambda-renormalization
  -2 S y^q |v|^2 -> -lambda y^q |v|^2  ->  Delta mu = -(2/3) lambda lim(|v|^2/kappa^2)
  (using y^q -> 2/(3 kappa^2)),  i.e.  Delta n = +3 lambda lim(|v|^2/kappa^2).
Full limit:  n_full = n_static + 3 lambda lim(|v|^2/kappa^2).
"""
import mpmath as mp
mp.mp.dps = 25
PASS=[];FAIL=[]
def check(name, ok, detail=""):
    (PASS if ok else FAIL).append(name)
    print(("PASS " if ok else "FAIL ")+name+("   "+detail if detail else ""))

pi = mp.pi
c20 = mp.sqrt(5/(16*pi))
def f0(x,K,G):  return 1+K*x+G*c20*(3*x**2-1)
def df0(x,K,G): return K+6*G*c20*x
C = {(1,1): mp.sqrt(3/(4*pi)),  (2,1): mp.sqrt(15/(4*pi)),
     (3,1): mp.sqrt(21/(32*pi)),(4,1): mp.sqrt(45/(32*pi)),
     (2,2): mp.sqrt(15/(16*pi)),(3,2): mp.sqrt(105/(16*pi)),(4,2): mp.sqrt(45/(64*pi)),
     (3,3): mp.sqrt(35/(32*pi)),(4,3): mp.sqrt(315/(32*pi))}
P_ = {(1,1): (lambda x: 1, lambda x: 0), (2,1): (lambda x: x, lambda x: 1),
      (3,1): (lambda x: 5*x**2-1, lambda x: 10*x), (4,1): (lambda x: 7*x**3-3*x, lambda x: 21*x**2-3),
      (2,2): (lambda x: 1, lambda x: 0), (3,2): (lambda x: x, lambda x: 1),
      (4,2): (lambda x: 7*x**2-1, lambda x: 14*x),
      (3,3): (lambda x: 1, lambda x: 0), (4,3): (lambda x: x, lambda x: 1)}
def entry(keyA,keyB,K,G):
    m=keyA[1]
    pA,dpA=P_[keyA]; pB,dpB=P_[keyB]; cA,cB=C[keyA],C[keyB]
    def integ(x):
        f=f0(x,K,G); df=df0(x,K,G)
        PA=cA*pA(x)/f; PB=cB*pB(x)/f
        dPA=cA*(dpA(x)*f-pA(x)*df)/f**2
        dPB=cB*(dpB(x)*f-pB(x)*df)/f**2
        return f*((1-x**2)**(m+1)*dPA*dPB - m*x*(1-x**2)**m*(dPA*PB+PA*dPB)
                  + m**2*(1+x**2)*(1-x**2)**(m-1)*PA*PB)
    return pi/2*mp.quad(integ,[-1,1])
def tad_g0(K,G):
    e=mp.mpf('1e-7')
    def P(GG):
        def integ(x):
            f=f0(x,K,GG); d=df0(x,K,GG)
            return (1-x**2)*d**2/f
        return (2*pi/4)*mp.quad(integ,[-1,1])
    return (P(G+e)-P(G-e))/(2*e)
def block(keys,K,G):
    n=len(keys); B=mp.matrix(n,n)
    for i in range(n):
        for j in range(i,n):
            B[i,j]=B[j,i]=entry(keys[i],keys[j],K,G)
    return B
def schur_and_v2(B, idx):
    nn=B.rows; rest=[i for i in range(nn) if i!=idx]
    Bxx=mp.matrix([[B[i,j] for j in rest] for i in rest])
    Bxw=mp.matrix([B[i,idx] for i in rest])
    sol=mp.lu_solve(Bxx,Bxw)          # v = Bxx^{-1} c
    S=B[idx,idx]-sum(Bxw[i]*sol[i] for i in range(nn-1))
    v2=sum(sol[i]**2 for i in range(nn-1))
    return S, v2

m1keys=[(1,1),(2,1),(3,1),(4,1)]
m2keys=[(2,2),(3,2),(4,2)]
m3keys=[(3,3),(4,3)]
chans=[('lam=2  m=1', m1keys,0,2), ('lam=6  m=1', m1keys,1,6), ('lam=6  m=2', m2keys,0,6),
       ('lam=12 m=1', m1keys,2,12), ('lam=12 m=2', m2keys,1,12), ('lam=12 m=3', m3keys,0,12)]

print("-- lim |v|^2/kappa^2 and full far-collar limits --")
res={}
for K in [mp.mpf('0.1'), mp.mpf('0.05'), mp.mpf('0.025')]:
    G=mp.findroot(lambda G: tad_g0(K,G), mp.mpf('0.44')*K**2)
    Bs={'m1': block(m1keys,K,G), 'm2': block(m2keys,K,G), 'm3': block(m3keys,K,G)}
    row=[]
    for nm,keys,idx,lam in chans:
        b = Bs['m1'] if keys is m1keys else Bs['m2'] if keys is m2keys else Bs['m3']
        S,v2 = schur_and_v2(b, idx)
        row.append(v2/K**2)
    res[float(K)]=row
    print(f"k={mp.nstr(K,3)}: "+"  ".join(mp.nstr(r,8) for r in row))
from fractions import Fraction
print("\nRichardson lim |v|^2/kappa^2, Delta n = 3 lam lim, and n_full:")
n_static={'lam=2  m=1': mp.mpf(4)/15, 'lam=6  m=1': mp.mpf(5), 'lam=6  m=2': mp.mpf(-1),
          'lam=12 m=1': mp.mpf(113)/20, 'lam=12 m=2': mp.mpf(12)/5, 'lam=12 m=3': mp.mpf(-181)/60}
for i,(nm,keys,idx,lam) in enumerate(chans):
    r=(4*res[0.05][i]-res[0.1][i])/3
    r2=(4*res[0.025][i]-res[0.05][i])/3
    fr=Fraction(float(r2)).limit_denominator(600)
    nf=n_static[nm]+3*lam*r2
    frn=Fraction(float(nf)).limit_denominator(600)
    print(f"  {nm}: lim={mp.nstr(r,8)}/{mp.nstr(r2,8)} ~ {fr}   n_full = {mp.nstr(nf,10)} ~ {frn} = {float(frn):.9f}")
check("lam=2 m=1: lim|v|^2/k^2 = 5/36", abs((4*res[0.025][0]-res[0.05][0])/3-mp.mpf(5)/36)<1e-5,
      mp.nstr((4*res[0.025][0]-res[0.05][0])/3,9))

# adiabatic control parameter trend (must -> 0): r_ad ~ |Kv|/(y^q M |v|)
# scale check: y^q = 2/(3 k^2) grows; gradient scale fixed => r_ad ~ O(k^2)
Lk=lambda K: mp.log((1+K)/(1-K))
for K in [mp.mpf('0.2'),mp.mpf('0.1'),mp.mpf('0.05')]:
    yq=1/((mp.mpf(9)/4)*(Lk(K)-2*K)/K)
    print(f"k={mp.nstr(K,3)}: 1/(y^q M_gg) ~ {mp.nstr(1/(yq*3),6)} (adiabatic parameter scale)")

print(f"\n==== {len(PASS)} PASS / {len(FAIL)} FAIL ====")
if FAIL: print("FAILED:", FAIL)
