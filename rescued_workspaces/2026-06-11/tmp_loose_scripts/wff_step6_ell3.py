"""
Step 6: ell=3 fluctuation channels added (background still ell<=2,
tadpole-relaxed; ell=3 background tadpole is O(kappa^3), vanishing in the
limits). Tests:
  - lambda=2 (a1) limit stability at 4/15 (corrections predicted O(kappa^4));
  - lambda=6 (gamma1, gamma2) limit shifts at O(kappa^2) (predicted);
  - anchor values with ell=3 channels (convergence diagnostics).
Real harmonics added:
  Y31 = sqrt(21/32pi) sqrt(1-x^2)(5x^2-1) cos(phi)
  Y32 = sqrt(105/16pi) (1-x^2) x cos(2phi)
"""
import mpmath as mp
mp.mp.dps = 25
PASS=[];FAIL=[]
def check(name, ok, detail=""):
    (PASS if ok else FAIL).append(name)
    print(("PASS " if ok else "FAIL ")+name+("   "+detail if detail else ""))

pi = mp.pi
c20 = mp.sqrt(5/(16*pi))
c11 = mp.sqrt(3/(4*pi)); c21 = mp.sqrt(15/(4*pi)); c31 = mp.sqrt(21/(32*pi))
c22 = mp.sqrt(15/(16*pi)); c32 = mp.sqrt(105/(16*pi))

# norm sanity
for nm, prof, m in [("Y31", lambda x: c31*mp.sqrt(1-x**2)*(5*x**2-1), 1),
                    ("Y32", lambda x: c32*(1-x**2)*x, 2)]:
    nrm = pi*mp.quad(lambda x: prof(x)**2, [-1,1])
    check(f"norm {nm} == 1", abs(nrm-1)<1e-20, mp.nstr(nrm,10))

def f0(x,K,G):  return 1+K*x+G*c20*(3*x**2-1)
def df0(x,K,G): return K+6*G*c20*x

# m=1 channels via h-profiles (g = sqrt(1-x^2) h): h_a=c11, h_g=c21 x, h_d=c31(5x^2-1)
def entry_m1(hA,dhA,hB,dhB,K,G):
    def integ(x):
        f=f0(x,K,G); df=df0(x,K,G)
        HA=hA(x)/f; HB=hB(x)/f
        dHA=(dhA(x)*f-hA(x)*df)/f**2
        dHB=(dhB(x)*f-hB(x)*df)/f**2
        grad = x**2*HA*HB - x*(1-x**2)*(dHA*HB+HA*dHB) + (1-x**2)**2*dHA*dHB
        return f*(grad+HA*HB)
    return pi/2*mp.quad(integ,[-1,1])

# m=2 channels: g_g2=c22(1-x^2), g_d2=c32(1-x^2)x ; direct form, m=2
def entry_m2(gA,dgA,gB,dgB,K,G):
    def integ(x):
        f=f0(x,K,G); df=df0(x,K,G)
        uA=gA(x)/f; uB=gB(x)/f
        duA=(dgA(x)*f-gA(x)*df)/f**2
        duB=(dgB(x)*f-gB(x)*df)/f**2
        return f*((1-x**2)*duA*duB + 4*uA*uB/(1-x**2))
    return pi/2*mp.quad(integ,[-1,1])

hA  = (lambda x: c11, lambda x: 0)
hG  = (lambda x: c21*x, lambda x: c21)
hD  = (lambda x: c31*(5*x**2-1), lambda x: 10*c31*x)
g2  = (lambda x: c22*(1-x**2), lambda x: -2*c22*x)
d2  = (lambda x: c32*(1-x**2)*x, lambda x: c32*(1-3*x**2))

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

def blocks(K,G):
    # m=1 3x3 over {a1(l1), g1(l2), d1(l3)}
    Maa=entry_m1(*hA,*hA,K,G); Mag=entry_m1(*hA,*hG,K,G); Mad=entry_m1(*hA,*hD,K,G)
    Mgg=entry_m1(*hG,*hG,K,G); Mgd=entry_m1(*hG,*hD,K,G); Mdd=entry_m1(*hD,*hD,K,G)
    B1=mp.matrix([[Maa,Mag,Mad],[Mag,Mgg,Mgd],[Mad,Mgd,Mdd]])
    # m=2 2x2 over {g2(l2), d2(l3)}
    M22=entry_m2(*g2,*g2,K,G); M23=entry_m2(*g2,*d2,K,G); M33=entry_m2(*d2,*d2,K,G)
    B2=mp.matrix([[M22,M23],[M23,M33]])
    return B1,B2

def schur_onto(B, idx):
    nn=B.rows; rest=[i for i in range(nn) if i!=idx]
    Bxx=mp.matrix([[B[i,j] for j in rest] for i in rest])
    Bxw=mp.matrix([B[i,idx] for i in rest])
    sol=mp.lu_solve(Bxx,Bxw)
    return B[idx,idx]-sum(Bxw[i]*sol[i] for i in range(nn-1))

def neff(K,G,lam,S):
    return 1-2*pi*(2*S-lam)/(-P_F(K,G))

# kappa->0 limits with ell=3 fluctuations (background G from tadpole)
print("-- limits with ell=3 fluctuation channels --")
vals={}
for K in [mp.mpf('0.2'),mp.mpf('0.1'),mp.mpf('0.05')]:
    G=mp.findroot(lambda G: tad_g0(K,G), mp.mpf('0.44')*K**2)
    B1,B2=blocks(K,G)
    Sa=schur_onto(B1,0); Sg=schur_onto(B1,1); S2=schur_onto(B2,0)
    na=neff(K,G,2,Sa); ng=neff(K,G,6,Sg); n2=neff(K,G,6,S2)
    # also lambda=12 channel d1/d2? l=3: lam=12: diagonal-only kept channels
    Sd1=schur_onto(B1,2); Sd2=schur_onto(B2,1)
    nd1=neff(K,G,12,Sd1); nd2=neff(K,G,12,Sd2)
    vals[float(K)]=(na,ng,n2,nd1,nd2)
    print(f"k={mp.nstr(K,3)}: n_a={mp.nstr(na,10)} n_g1={mp.nstr(ng,10)} n_g2={mp.nstr(n2,10)} "
          f"n_d1={mp.nstr(nd1,9)} n_d2={mp.nstr(nd2,9)}")
names=['lam=2 m=1','lam=6 m=1','lam=6 m=2','lam=12 m=1','lam=12 m=2']
print("\nRichardson limits (kappa^2):")
lims=[]
for i,nm in enumerate(names):
    r1=(4*vals[0.1][i]-vals[0.2][i])/3
    r2=(4*vals[0.05][i]-vals[0.1][i])/3
    lims.append(r2)
    print(f"  {nm}: {mp.nstr(r1,10)} / {mp.nstr(r2,10)}")
check("lambda=2 limit stable at 4/15 under ell=3", abs(lims[0]-mp.mpf(4)/15)<1e-5, mp.nstr(lims[0],10))
print("rational guesses: ",
      [mp.nstr(lims[i],8) for i in range(5)])
from fractions import Fraction
for i,nm in enumerate(names):
    fr=Fraction(float(lims[i])).limit_denominator(400)
    print(f"  {nm}: limit ~ {fr} = {float(fr):.9f}  (computed {mp.nstr(lims[i],9)})")

# anchor with ell=3 channels
Ks=mp.mpf('0.7680027679502'); Gs=mp.mpf('0.2542920109211')
B1,B2=blocks(Ks,Gs)
na=neff(Ks,Gs,2,schur_onto(B1,0)); ng=neff(Ks,Gs,6,schur_onto(B1,1)); n2=neff(Ks,Gs,6,schur_onto(B2,0))
print("\nanchor (kappa*,G*) with ell=3 fluctuations: n_a =", mp.nstr(na,10),
      " n_g1 =", mp.nstr(ng,10), " n_g2 =", mp.nstr(n2,10))
print("(vs ell<=2 fluct: 0.232742, -0.883390, -5.068544)")

print(f"\n==== {len(PASS)} PASS / {len(FAIL)} FAIL ====")
if FAIL: print("FAILED:", FAIL)
