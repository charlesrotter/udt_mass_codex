"""BLIND VERIFIER symbolic derivations (independent of S1 code).

Model (from banked context only):
  f(u) = F*Y0 + a*Y1 + b*Y2 + g*Y3, Y_l orthonormal: Y0=1, Y1=sqrt3 u,
  Y2=(sqrt5/2)(3u^2-1), Y3=(sqrt7/2)(5u^3-3u).
  P = (1/8) Int_{-1}^{1} (1-u^2) f_u^2 / f du.

Derive:
  D1: P at ell<=1 == (3a^2/8F) G1(kappa), G1=(2k+(k^2-1)L)/k^3  [banked]
  D2: 2 P_F == -H, H = L/(2k)-1                                  [banked]
  D3: P_a == sqrt3 [L(1+k^2)-2k]/(8k^2)                          [banked]
  D4: T2 = dP/db|_{b=g=0} == sqrt5 (2k-L)/(4k)                   [banked]
  D5: T3 = dP/dg|_{b=g=0}  -> closed form + small-k series       [C2]
      S1 claim: sqrt7[(30k-62k^3)-(15-36k^2+9k^4)L]/(48k^4),
      series (3 sqrt7/35) k^3 + ...
  D6: seal log law at ell<=1: P_F -> -(1/4)ln(1/mu)+O(1),
      P_a -> +(sqrt3/4)ln(1/mu)+O(1) with mu = F(1-k) (pole u=-1 for a>0;
      equivalently u=+1 for a<0; Y_X at the DIP pole: (1, -sqrt3)).  [C4]
"""
import sympy as sp

u, k, F = sp.symbols('u k F', positive=True)
s3, s5, s7 = sp.sqrt(3), sp.sqrt(5), sp.sqrt(7)
L = sp.log((1 + k)/(1 - k))

# ---------- ell<=1 exact potential (a>0, kappa=sqrt3 a/F in (0,1)) ------
a = k*F/s3
f1 = F*(1 + k*u)
P1 = sp.integrate((1 - u**2)*sp.diff(f1, u)**2/f1, (u, -1, 1))/8
P1 = sp.simplify(P1)

G1 = (2*k + (k**2 - 1)*L)/k**3
chk_D1 = sp.simplify(P1 - 3*a**2/(8*F)*G1)
print("D1  P(ell<=1) - (3a^2/8F)G1 =", chk_D1)

# P_F at fixed a: rewrite P1 in (F, a) then differentiate
A = sp.symbols('A', positive=True)
P1_Fa = P1.subs(k, s3*A/F)
PF = sp.simplify(sp.diff(P1_Fa, F).subs(A, k*F/s3))
H = L/(2*k) - 1
print("D2  2P_F + H =", sp.simplify(2*PF + H))

Pa = sp.simplify(sp.diff(P1_Fa, A).subs(A, k*F/s3))
Wp = (L*(1 + k**2) - 2*k)/(8*k**2)
print("D3  P_a - sqrt3 W' =", sp.simplify(Pa - s3*Wp))

# ---------- tadpoles on the ell<=1 background ----------
Y2 = (s5/2)*(3*u**2 - 1)
Y3 = (s7/2)*(5*u**3 - 3*u)
fu = sp.diff(f1, u)

def tadpole(Y):
    # d/de P[f1 + e Y] at e=0
    integ = (1 - u**2)*(2*fu*sp.diff(Y, u)/f1 - fu**2*Y/f1**2)/8
    return sp.simplify(sp.integrate(integ, (u, -1, 1)))

T2 = tadpole(Y2)
T2_banked = s5*(2*k - L)/(4*k)
print("D4  T2 - banked =", sp.simplify(T2 - T2_banked))

T3 = tadpole(Y3)
T3_S1 = s7*((30*k - 62*k**3) - (15 - 36*k**2 + 9*k**4)*L)/(48*k**4)
print("D5  T3 (my derivation) =", sp.simplify(T3))
print("D5  T3 - S1 closed form =", sp.simplify(T3 - T3_S1))
ser = sp.series(T3, k, 0, 8)
print("D5  T3 small-k series =", ser)

# F-independence sanity (degree-1 homogeneity of P => tadpoles depend on k
# only): T3 was computed at general F -- confirm no F left
print("D5  free symbols of T3:", T3.free_symbols)

# ---------- D6: seal log law from the exact ell<=1 closed forms ----------
# dip pole u=-1 (a>0): mu = F(1-k). Set k = 1 - mu/F, expand mu -> 0.
mu = sp.symbols('mu', positive=True)
PF_mu = PF.subs(k, 1 - mu/F)
Pa_mu = Pa.subs(k, 1 - mu/F)
# leading behavior: coefficient of log(mu)
print("D6  P_F:  lim coeff of ln(1/mu):",
      sp.limit(PF_mu/sp.log(1/mu), mu, 0, '+'))
print("D6  P_a:  lim coeff of ln(1/mu):",
      sp.limit(Pa_mu/sp.log(1/mu), mu, 0, '+'))
print("    (Y at dip pole u=-1: Y0=1, Y1=-sqrt3; law says -Y_X(pole)/4",
      "= -1/4 and +sqrt3/4 = +0.433...)")
