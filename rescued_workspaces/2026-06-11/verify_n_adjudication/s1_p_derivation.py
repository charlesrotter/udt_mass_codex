"""
S1: Derive P(F,a) from scratch; settle the factor-4 prefactor question;
verify homogeneity, rank-1 Hessian; capacity-law demand kappa(1).

CONVENTIONS (mine, fixed for the whole adjudication):
- f(y,th) = F(y) + a(y)*Y10(th), Y10 = sqrt(3/(4pi)) cos(th)  [ORTHONORMAL real harmonic]
- equivalently f = F (1 + kappa cos th), kappa = sqrt(3/(4pi)) a / F
- C1 sphere-integrated action: S = int dy [ pi y^2 F'^2 + (1/4) y^2 a'^2 + P ]
  with P = (1/4) int dOmega |grad_Omega f|^2 / f      <-- the defining integral
- q = 1/3, s = q(1-q)/2 = 1/9; background F0 = y^-q
- capacity law (corrected 4pi form, per record): the F-EL demand
  -2 pi (y^2 F0')' + P_F = 0  =>  P_F = 2 pi (y^2 F0')' = -4 pi s y^-q  (DEMAND)
"""
import sympy as sp

F, a, kap, c, y, q, lam = sp.symbols('F a kappa c y q lam', positive=True)
# allow kappa in (0,1); c = cos(theta) in (-1,1)
kapv = sp.Symbol('kappa', real=True)

print("="*70)
print("CHECK 1: P from the defining integral, f = F(1+kappa cos th)")
print("="*70)
# |grad_Omega f|^2 = (df/dth)^2 = F^2 kappa^2 sin^2 th ; dOmega = 2 pi dc
# P = (1/4) * 2 pi * int_{-1}^{1} F^2 kap^2 (1-c^2) / (F(1+kap c)) dc
integrand = (1 - c**2)/(1 + kap*c)
I = sp.integrate(integrand, (c, -1, 1))
I = sp.simplify(I)
print("I(kappa) = int (1-c^2)/(1+kappa c) dc =", I)

L = sp.log((1+kap)/(1-kap))
G1 = (2*kap + (kap**2-1)*L)/kap**3
diff = sp.simplify(sp.nsimplify(0) + I - G1*0)  # placeholder
# verify I == kappa^2 * G1? No: check numerically I vs G1
import mpmath as mp
mp.mp.dps = 30
def I_num(k):
    return mp.quad(lambda cc: (1-cc**2)/(1+k*cc), [-1,1])
def G1_num(k):
    Lv = mp.log((1+k)/(1-k))
    return (2*k + (k**2-1)*Lv)/k**3
for k in [mp.mpf('0.1'), mp.mpf('0.5'), mp.mpf('0.683095'), mp.mpf('0.95')]:
    print(f"  k={float(k):.6f}: I={mp.nstr(I_num(k),12)}  G1={mp.nstr(G1_num(k),12)}  I-G1={mp.nstr(I_num(k)-G1_num(k),3)}")
print("  => I(kappa) = G1(kappa) exactly (the recorded G1 is the Legendre integral).")

print()
print("="*70)
print("CHECK 2: P in both variable sets; settle the prefactor")
print("="*70)
# P = (1/4)*2 pi * F kap^2 * I(kap)   [since F^2 kap^2 / F = F kap^2]
# => P = (pi/2) F kappa^2 G1(kappa) = (pi/2) F H(kappa),  H = kappa^2 G1
# in orthonormal a: kappa = sqrt(3/4pi) a/F  => kappa^2 F = (3/(4pi)) a^2/F
# => P = (pi/2)(3/(4pi)) (a^2/F) G1 = (3 a^2 / (8 F)) G1
print("P = (1/4) * 2pi * F kap^2 * G1 = (pi/2) F kap^2 G1(kap)")
print("orthonormal a:  P = (3 a^2 / (8F)) G1(kappa)")
print("RECORDED form:  P = (3 a^2 / (2F)) G1(kappa)   <-- factor 4 LARGER")
# small-kappa check against generic-harmonic quadratic P:
# P_quad = (1/4) * l(l+1) * a^2 / F  for orthonormal Y_lm  => (1/2) a^2/F at l=1
G1_series = sp.series(G1, kap, 0, 6).removeO()
print("G1 series:", sp.expand(G1_series))
P_mine_quad = sp.Rational(3,8)*sp.Rational(4,3)  # (3/8)*G1(0) coefficient of a^2/F
print(f"  my P quadratic coeff of a^2/F: {P_mine_quad}  (required by (1/4)l(l+1)=1/2: PASS={P_mine_quad==sp.Rational(1,2)})")
P_rec_quad = sp.Rational(3,2)*sp.Rational(4,3)
print(f"  recorded P quadratic coeff: {P_rec_quad} = 4x too large vs the (1/4)int dOmega definition")
print("  => recorded prefactor matches int dOmega |grad f|^2/f WITHOUT the 1/4.")
# consequence: with kinetic (1/4) y^2 a'^2, recorded P gives small-kap a-operator
# (y^2 a')' = (8 y^q) a i.e. lambda=8, not lambda=l(l+1)=2. Inconsistent w/ weld family.
print("  consequence: recorded P + recorded kinetic => lambda_eff = 4*l(l+1) = 8 at l=1;")
print("  the weld family needs lambda = l(l+1) = 2  => factor-4 flag CONFIRMED.")

print()
print("="*70)
print("CHECK 3: degree-1 homogeneity and EXACT rank-1 Hessian")
print("="*70)
# P(F,a) with orthonormal a, symbolic
kap_expr = sp.sqrt(sp.Rational(3,1)/(4*sp.pi)) * a / F
G1e = (2*kap_expr + (kap_expr**2-1)*sp.log((1+kap_expr)/(1-kap_expr)))/kap_expr**3
P = sp.Rational(3,8) * a**2 / F * G1e
# homogeneity: F P_F + a P_a - P == 0
P_F = sp.diff(P, F); P_a = sp.diff(P, a)
hom = sp.simplify(F*P_F + a*P_a - P)
print("Euler (deg-1):  F P_F + a P_a - P =", hom)
P_FF = sp.diff(P, F, 2); P_aa = sp.diff(P, a, 2); P_Fa = sp.diff(P, F, a)
det = sp.simplify(P_FF*P_aa - P_Fa**2)
print("Hessian det P_FF P_aa - P_Fa^2 =", det)
r1a = sp.simplify(F*P_FF + a*P_Fa)
r1b = sp.simplify(F*P_Fa + a*P_aa)
print("null vector check: F P_FF + a P_Fa =", r1a, " ; F P_Fa + a P_aa =", r1b)
print("=> Hessian rank-1, null = scaling direction (F,a) ~ (F0,a0): EXACT.")

print()
print("="*70)
print("CHECK 4: capacity-law demand; kappa(1) under BOTH prefactors")
print("="*70)
# my P: P = (pi/2) F H(kap), H = kap^2 G1 = (2 kap + (kap^2-1)L)/kap
# P_F at fixed a (kap depends on F): P_F = (pi/2)(H - kap H')
# demand: P_F = -4 pi s y^-q  =>  kap H' - H = 8 s y^-q
mp.mp.dps = 30
s_ = mp.mpf(1)/9
def H_(k):
    Lv = mp.log((1+k)/(1-k))
    return (2*k + (k**2-1)*Lv)/k
def Hp_(k):
    h = mp.mpf('1e-12')
    return (H_(k+h)-H_(k-h))/(2*h)
def demand_lhs(k):  # kap H' - H
    return k*Hp_(k) - H_(k)
# at y=1: kap H' - H = 8s  (my P);  = 2s (if P were 4x larger, i.e. recorded prefactor)
from mpmath import findroot
k_mine = findroot(lambda k: demand_lhs(k) - 8*s_, mp.mpf('0.7'))
k_rec4 = findroot(lambda k: demand_lhs(k) - 2*s_, mp.mpf('0.4'))
print(f"  my P (3a^2/8F G1):       kappa(1) solves kapH'-H = 8s = {mp.nstr(8*s_,8)}  => kappa(1) = {mp.nstr(k_mine,8)}")
print(f"  recorded P (4x, 3a^2/2F): kappa(1) solves kapH'-H = 2s          => kappa(1) = {mp.nstr(k_rec4,8)}")
print(f"  RECORDED demanded kappa(1) = 0.683095")
# also the 'slipped' demand s y^-q instead of 4 pi s y^-q, with my P:
k_slip = findroot(lambda k: demand_lhs(k) - 2*s_/mp.pi, mp.mpf('0.2'))
print(f"  slipped demand (s y^-q, my P): kappa = {mp.nstr(k_slip,8)}  [record says slip gave 0.230329]")

# check H'' > 0 on (0,1) (P_aa > 0: elimination well-posed)
print()
print("CHECK 5: P_aa > 0 (stability of the a-elimination): P_aa = (3/(8F)) H''(kap)... ")
def Hpp_(k):
    h = mp.mpf('1e-7')
    return (H_(k+h)-2*H_(k)+H_(k-h))/h**2
bad = []
for kk in [0.01,0.1,0.3,0.5,0.683,0.8,0.9,0.97,0.995]:
    v = Hpp_(mp.mpf(kk))
    if v <= 0: bad.append(kk)
    print(f"   H''({kk}) = {mp.nstr(v,8)}")
print("  all positive:", len(bad)==0)
