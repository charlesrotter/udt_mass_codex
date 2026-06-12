"""
Step 5: the ell<=2-class corrected background and the corrected n_eff.

Background class extended: f0 = F[1 + kappa x] + G*Y20(x), with
  (i)  gamma0 relaxed:  P_gamma0(kappa, G) = 0   (no ell=2 tadpole),
  (ii) capacity demand: P_F(kappa, G) = -(4pi/9) y^{-1/3}  (monopole EL
       with F = y^{-q}, q=1/3, s=1/9; at y=1: -4pi/9).
In this class  n_eff = 1 - 2pi (2*S - lambda)/(-P_F)   per channel.
At G=0 this reduces exactly to 1 - 2kappa(2S-lambda)/(L-2kappa)  (checked).
Static gamma0 response is exact at kappa->0 (kinetic correction shown to
be relatively O(kappa^2) by the power counting y^{-2/3} vs y^{-1/3}).
"""
import mpmath as mp
import sympy as sp, pickle
mp.mp.dps = 25
PASS=[];FAIL=[]
def check(name, ok, detail=""):
    (PASS if ok else FAIL).append(name)
    print(("PASS " if ok else "FAIL ")+name+("   "+detail if detail else ""))

pi = mp.pi
c10 = mp.sqrt(3/(4*pi)); c20 = mp.sqrt(5/(16*pi))
c11 = mp.sqrt(3/(4*pi)); c21 = mp.sqrt(15/(4*pi)); c22 = mp.sqrt(15/(16*pi))
EPS = mp.mpf('1e-9')

def f0(x, K, G):  return 1 + K*x + G*c20*(3*x**2-1)
def df0(x, K, G): return K + 6*G*c20*x

def P_full(F, K, G):
    # P = (2pi/4) int (1-x^2) (df/dx)^2 / f dx ; f = F + (K x + G c20(3x^2-1)) [K,G are coefficients at F-units]
    def integ(x):
        f = F + K*x + G*c20*(3*x**2-1)
        d = K + 6*G*c20*x
        return (1-x**2)*d**2/f
    return (2*pi/4)*mp.quad(integ, [-1, 1])

def P_F(K, G):
    e = mp.mpf('1e-7')
    return (P_full(1+e,K,G)-P_full(1-e,K,G))/(2*e)

def tad_g0(K, G):
    e = mp.mpf('1e-7')
    return (P_full_pert(K,G,e)-P_full_pert(K,G,-e))/(2*e)

def P_full_pert(K, G, e):
    def integ(x):
        f = f0(x,K,G) + e*c20*(3*x**2-1)
        d = df0(x,K,G) + 6*e*c20*x
        return (1-x**2)*d**2/f
    return (2*pi/4)*mp.quad(integ, [-1, 1])

# Hessian entries on general background (1D quadrature, rationalized analytic derivatives)
def entry(gA, dgA, gB, dgB, m, K, G):
    def integ(x):
        f = f0(x,K,G); df = df0(x,K,G)
        uA = gA(x)/f; uB = gB(x)/f
        duA = (dgA(x)*f - gA(x)*df)/f**2
        duB = (dgB(x)*f - gB(x)*df)/f**2
        t = (1-x**2)*duA*duB*f
        if m: t += m**2*uA*uB*f/(1-x**2)
        return t
    cm = 2*pi if m==0 else pi
    return cm/2*mp.quad(integ, [-1, 1])

# m=1 basis: g = sqrt(1-x^2) h ; handle endpoint singularity analytically:
# use rationalized forms instead: write entries via h-functions (all rational)
def entry_m1(hA, dhA, hB, dhB, K, G):
    def integ(x):
        f = f0(x,K,G); df = df0(x,K,G)
        HA = hA(x)/f; HB = hB(x)/f
        dHA = (dhA(x)*f - hA(x)*df)/f**2
        dHB = (dhB(x)*f - hB(x)*df)/f**2
        grad = x**2*HA*HB - x*(1-x**2)*(dHA*HB+HA*dHB) + (1-x**2)**2*dHA*dHB
        return f*(grad + HA*HB)
    return pi/2*mp.quad(integ, [-1, 1])

hA1  = lambda x: c11;      dhA1 = lambda x: 0
hG1  = lambda x: c21*x;    dhG1 = lambda x: c21
gG2  = lambda x: c22*(1-x**2); dgG2 = lambda x: -2*c22*x

with open('/tmp/wff_entries.pkl','rb') as fh: D = pickle.load(fh)
k = D['k']
import sympy
M1f = {key: sympy.lambdify(k, v, 'mpmath') for key, v in D['M1'].items()}
M22f = sympy.lambdify(k, D['M22'], 'mpmath')
Pgf  = sympy.lambdify(k, D['Pg'], 'mpmath')
Lk = lambda K: mp.log((1+K)/(1-K))

# sanity at G=0 against symbolic
kap1 = mp.findroot(lambda K: (Lk(K)-2*K)/K - mp.mpf(4)/9, mp.mpf('0.68'))
t = entry_m1(hA1,dhA1,hA1,dhA1,kap1,0)
check("entry_m1 aa at G=0 vs symbolic", abs(t-M1f[(1,1)](kap1))<1e-18, f"{mp.nstr(t,15)}")
t = entry_m1(hA1,dhA1,hG1,dhG1,kap1,0)
check("entry_m1 ag at G=0 vs symbolic", abs(t-M1f[(1,2)](kap1))<1e-18)
t = entry(gG2,dgG2,gG2,dgG2,2,kap1,0)
check("entry m=2 at G=0 vs symbolic", abs(t-M22f(kap1))<1e-18)
check("tad_g0 at G=0 vs symbolic P_g", abs(tad_g0(kap1,0)-Pgf(kap1))<1e-12)
check("P_F at G=0 = -pi(L-2k)/k", abs(P_F(kap1,0)+pi*(Lk(kap1)-2*kap1)/kap1)<1e-12,
      f"{mp.nstr(P_F(kap1,0),12)}")

def neff_class(K, G, lam, S):
    return 1 - 2*pi*(2*S - lam)/(-P_F(K,G))

# consistency at G=0:
S0 = M1f[(1,1)](kap1) - M1f[(1,2)](kap1)**2/M1f[(2,2)](kap1)
n0a = neff_class(kap1, 0, 2, S0)
check("class formula reduces at G=0", abs(n0a - (1-2*kap1*(2*S0-2)/(Lk(kap1)-2*kap1)))<1e-12,
      f"{mp.nstr(n0a,12)}")

# ---- joint solve at the anchor y=1: P_g0 = 0, P_F = -4pi/9 ----
def eqs(K, G):
    return [tad_g0(K,G), P_F(K,G) + 4*pi/9]
Ks, Gs = mp.findroot(lambda K,G: eqs(K,G), (mp.mpf('0.75'), mp.mpf('0.15')))
print("\nell<=2 demanded background at y=1:  kappa* =", mp.nstr(Ks,13), "  G* =", mp.nstr(Gs,13))
check("ell<=2 anchor solved", abs(tad_g0(Ks,Gs))<1e-15 and abs(P_F(Ks,Gs)+4*pi/9)<1e-15)

def all_neff(K, G):
    Maa = entry_m1(hA1,dhA1,hA1,dhA1,K,G)
    Mag = entry_m1(hA1,dhA1,hG1,dhG1,K,G)
    Mgg = entry_m1(hG1,dhG1,hG1,dhG1,K,G)
    M2v = entry(gG2,dgG2,gG2,dgG2,2,K,G)
    Sa = Maa - Mag**2/Mgg
    Sg = Mgg - Mag**2/Maa
    return (neff_class(K,G,2,Sa), neff_class(K,G,6,Sg), neff_class(K,G,6,M2v))

na, ng, n2 = all_neff(Ks, Gs)
print("ell<=2 anchor n_eff:  m=1 a (lam=2):", mp.nstr(na,12))
print("                      m=1 g (lam=6):", mp.nstr(ng,12))
print("                      m=2   (lam=6):", mp.nstr(n2,12))
na0, ng0, n20 = all_neff(kap1, 0)
print("ell<=1 anchor n_eff (same routine): ", mp.nstr(na0,12), mp.nstr(ng0,12), mp.nstr(n20,12))
print("Delta from ell=2 inclusion:", mp.nstr(na-na0,6), mp.nstr(ng-ng0,6), mp.nstr(n2-n20,6))

# ---- corrected kappa->0 limits in the ell<=2 class ----
print("\n-- kappa->0 limits, ell<=2 class (G solved from tadpole=0 at each kappa) --")
vals = {}
for K in [mp.mpf('0.2'), mp.mpf('0.1'), mp.mpf('0.05')]:
    G = mp.findroot(lambda G: tad_g0(K,G), mp.mpf('0.4')*K**2/c20/4)
    na_, ng_, n2_ = all_neff(K, G)
    vals[float(K)] = (na_, ng_, n2_, G)
    print(f"kappa={mp.nstr(K,3)}: G={mp.nstr(G,6)}  n_a={mp.nstr(na_,9)}  n_g={mp.nstr(ng_,9)}  n_2={mp.nstr(n2_,9)}")
# Richardson in kappa^2: n(k) = n0 + c k^2 -> n0 = (4 n(k/2) - n(k))/3
for idx, nm in [(0,'m=1 a'),(1,'m=1 g'),(2,'m=2')]:
    r1 = (4*vals[0.1][idx] - vals[0.2][idx])/3
    r2 = (4*vals[0.05][idx] - vals[0.1][idx])/3
    print(f"limit {nm}: Richardson {mp.nstr(r1,9)} / {mp.nstr(r2,9)}")
# compare with ell<=1 limits 11/10, -25/14, -17/7
print("ell<=1 limits were: 1.1, -1.785714..., -2.428571...")

print(f"\n==== {len(PASS)} PASS / {len(FAIL)} FAIL ====")
if FAIL: print("FAILED:", FAIL)
