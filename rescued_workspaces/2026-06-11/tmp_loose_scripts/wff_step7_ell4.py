"""
Step 7: ell=4 fluctuation channels. Unified rationalized entry formula for
profile Y = (1-x^2)^{m/2} p(x) cos(m phi):
  M_AB = (pi/2) int f * [ (1-x^2)^{m+1} PA' PB' - m x (1-x^2)^m (PA PB)'
                          + m^2 (1-x^2)^{m-1} PA PB ] dx,   P = p/f.
Verifies lambda=2 and lambda=6 limits unchanged by ell=4 (power-counting
check) and extracts lambda=12 limits (stable at ell<=4 by the same
counting: l=5 enters only at O(kappa^4)).
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

# profiles: (poly, dpoly, m, l)
C = {(1,1): mp.sqrt(3/(4*pi)),  (2,1): mp.sqrt(15/(4*pi)),
     (3,1): mp.sqrt(21/(32*pi)),(4,1): mp.sqrt(45/(32*pi)),
     (2,2): mp.sqrt(15/(16*pi)),(3,2): mp.sqrt(105/(16*pi)),(4,2): mp.sqrt(45/(64*pi)),
     (3,3): mp.sqrt(35/(32*pi)),(4,3): mp.sqrt(315/(32*pi))}
P_ = {(1,1): (lambda x: 1,        lambda x: 0),
      (2,1): (lambda x: x,        lambda x: 1),
      (3,1): (lambda x: 5*x**2-1, lambda x: 10*x),
      (4,1): (lambda x: 7*x**3-3*x, lambda x: 21*x**2-3),
      (2,2): (lambda x: 1,        lambda x: 0),
      (3,2): (lambda x: x,        lambda x: 1),
      (4,2): (lambda x: 7*x**2-1, lambda x: 14*x),
      (3,3): (lambda x: 1,        lambda x: 0),
      (4,3): (lambda x: x,        lambda x: 1)}

# norm sanity: pi * int (1-x^2)^m p^2 = 1
for key in C:
    l, m = key[0], key[1]
    nrm = pi*mp.quad(lambda x: (1-x**2)**m*(C[key]*P_[key][0](x))**2, [-1,1])
    check(f"norm Y{l}{m}", abs(nrm-1)<1e-20, mp.nstr(nrm,8))

def entry(keyA, keyB, K, G):
    m = keyA[1]; assert keyB[1]==m
    pA, dpA = P_[keyA]; pB, dpB = P_[keyB]
    cA, cB = C[keyA], C[keyB]
    def integ(x):
        f = f0(x,K,G); df = df0(x,K,G)
        PA = cA*pA(x)/f; PB = cB*pB(x)/f
        dPA = cA*(dpA(x)*f-pA(x)*df)/f**2
        dPB = cB*(dpB(x)*f-pB(x)*df)/f**2
        t = (1-x**2)**(m+1)*dPA*dPB - m*x*(1-x**2)**m*(dPA*PB+PA*dPB) \
            + m**2*(1+x**2)*(1-x**2)**(m-1)*PA*PB
        return f*t
    return pi/2*mp.quad(integ, [-1,1])

# cross-check vs step6 values at a test point
Kt, Gt = mp.mpf('0.2'), mp.mpf('0.0175875')
ref = entry((1,1),(1,1),Kt,Gt)
check("unified entry sane (M_a1a1 ~ 1+)", abs(ref-1)<0.2, mp.nstr(ref,10))

def P_F(K,G):
    e=mp.mpf('1e-7')
    def P(F):
        def integ(x):
            f=F+K*x+G*c20*(3*x**2-1); d=K+6*G*c20*x
            return (1-x**2)*d**2/f
        return (2*pi/4)*mp.quad(integ,[-1,1])
    return (P(1+e)-P(1-e))/(2*e)

def tad_g0(K,G):
    e=mp.mpf('1e-7')
    def P(GG):
        def integ(x):
            f=f0(x,K,GG); d=df0(x,K,GG)
            return (1-x**2)*d**2/f
        return (2*pi/4)*mp.quad(integ,[-1,1])
    return (P(G+e)-P(G-e))/(2*e)

def block(keys, K, G):
    n=len(keys)
    B=mp.matrix(n,n)
    for i in range(n):
        for j in range(i,n):
            B[i,j]=B[j,i]=entry(keys[i],keys[j],K,G)
    return B

def schur_onto(B, idx):
    nn=B.rows; rest=[i for i in range(nn) if i!=idx]
    if not rest: return B[0,0]
    Bxx=mp.matrix([[B[i,j] for j in rest] for i in rest])
    Bxw=mp.matrix([B[i,idx] for i in rest])
    sol=mp.lu_solve(Bxx,Bxw)
    return B[idx,idx]-sum(Bxw[i]*sol[i] for i in range(nn-1))

def neff(K,G,lam,S):
    return 1-2*pi*(2*S-lam)/(-P_F(K,G))

m1keys=[(1,1),(2,1),(3,1),(4,1)]
m2keys=[(2,2),(3,2),(4,2)]
m3keys=[(3,3),(4,3)]

print("\n-- limits with ell<=4 fluctuation channels --")
vals={}
for K in [mp.mpf('0.2'),mp.mpf('0.1'),mp.mpf('0.05')]:
    G=mp.findroot(lambda G: tad_g0(K,G), mp.mpf('0.44')*K**2)
    B1=block(m1keys,K,G); B2=block(m2keys,K,G); B3=block(m3keys,K,G)
    out=(neff(K,G,2, schur_onto(B1,0)),
         neff(K,G,6, schur_onto(B1,1)),
         neff(K,G,6, schur_onto(B2,0)),
         neff(K,G,12,schur_onto(B1,2)),
         neff(K,G,12,schur_onto(B2,1)),
         neff(K,G,12,schur_onto(B3,0)))
    vals[float(K)]=out
    print(f"k={mp.nstr(K,3)}: "+"  ".join(mp.nstr(o,9) for o in out))
names=['lam=2 m=1','lam=6 m=1','lam=6 m=2','lam=12 m=1','lam=12 m=2','lam=12 m=3']
from fractions import Fraction
print("\nRichardson limits and rational matches:")
lims=[]
for i,nm in enumerate(names):
    r1=(4*vals[0.1][i]-vals[0.2][i])/3
    r2=(4*vals[0.05][i]-vals[0.1][i])/3
    lims.append(r2)
    fr=Fraction(float(r2)).limit_denominator(400)
    print(f"  {nm}: {mp.nstr(r1,10)} / {mp.nstr(r2,10)}   ~ {fr} = {float(fr):.10f}")
check("lambda=2 limit = 4/15 stable under ell=4", abs(lims[0]-mp.mpf(4)/15)<2e-5, mp.nstr(lims[0],10))
check("lambda=6 m=1 limit = 5 stable under ell=4", abs(lims[1]-5)<2e-4, mp.nstr(lims[1],10))
check("lambda=6 m=2 limit = -1 stable under ell=4", abs(lims[2]+1)<2e-4, mp.nstr(lims[2],10))

# anchor values with ell<=4 fluctuations (convergence diagnostic only)
Ks=mp.mpf('0.7680027679502'); Gs=mp.mpf('0.2542920109211')
B1=block(m1keys,Ks,Gs); B2=block(m2keys,Ks,Gs)
print("\nanchor with ell<=4 fluct: n_a =", mp.nstr(neff(Ks,Gs,2,schur_onto(B1,0)),10),
      " n_g1 =", mp.nstr(neff(Ks,Gs,6,schur_onto(B1,1)),10),
      " n_g2 =", mp.nstr(neff(Ks,Gs,6,schur_onto(B2,0)),10))
print("(ell<=3 fluct gave:        0.3230318586,  4.063117428,  -0.9353635715)")
print("(ell<=2 fluct gave:        0.232742,      -0.883390,    -5.068544)")

print(f"\n==== {len(PASS)} PASS / {len(FAIL)} FAIL ====")
if FAIL: print("FAILED:", FAIL)
