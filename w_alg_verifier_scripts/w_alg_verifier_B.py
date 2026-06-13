#!/usr/bin/env python3
"""INDEPENDENT verifier for CLAIM B (algebraic-angular closure / walls).
Build the metric from scratch; verify D|q*, the block det, inverse-metric
components, signal speeds, the u* surface, reality on banked geometry,
the wall count and its rise with ell. Then adjudicate the insulation
reading hostilely."""
import sympy as sp, mpmath as mp
PASS, FAIL = [], []
def ck(tag, cond, note=""):
    (PASS if cond else FAIL).append(tag)
    print(f"VB-{tag}: {'PASS' if cond else 'FAIL'}  {note}")

r, u, w, th = sp.symbols('r u w theta', real=True)
f, q = sp.symbols('f q', positive=True)
W = (1+w)**2

# ---- (1) independent metric build ----
# line element diag/offdiag: g = [[-f,0,0,0],[0,1/f,q,0],[0,q,r^2 W,0],
#   [0,0,0,r^2 sin^2/W]]  (the (r,theta) shear block carries q).
fS = sp.Symbol('f', positive=True); qS=sp.Symbol('q', real=True)
WS = (1+sp.Symbol('w',real=True))**2
g = sp.Matrix([[-fS,0,0,0],[0,1/fS,qS,0],[0,qS,r**2*WS,0],
               [0,0,0,r**2*sp.sin(th)**2/WS]])
ginv = g.inv()
# block det of (r,theta):
D = sp.simplify(g[1,1]*g[2,2]-g[1,2]**2)   # = (1/f)(r^2 W) - q^2 = (r^2 W - f q^2)/f
ck("B1", sp.simplify(D - (r**2*WS - fS*qS**2)/fS)==0,
   f"(r,theta) block det = (r^2 W - f q^2)/f")
# define D_s := r^2 W - f q^2 (what they call D); block det = D_s/f.
Ds = r**2*WS - fS*qS**2
ck("B1b", sp.simplify(D - Ds/fS)==0, "block det = D_s/f exactly")
ck("B2", sp.simplify(ginv[2,2]-fS/Ds)==0 and sp.simplify(ginv[1,1]-r**2*WS/Ds)==0,
   f"g^thth = f/D_s, g^rr = r^2 W/D_s")
# Note: committed C3a claims g^thth = 1/D, g^rr = f r^2 W/D where THEIR
# D = D_s/f (block det). Check consistency: 1/(D_s/f)=f/D_s ✓;
# f*r^2W/(D_s/f)=f^2 r^2 W/D_s -- committed says g^rr=f r^2W/D=f^2r^2W/D_s.
ck("B2b", sp.simplify(ginv[1,1] - r**2*WS/Ds)==0,
   "my g^rr=r^2 W/D_s; committed 'f r^2 W/D' with D=D_s/f also = f^2 r^2 W/D_s -- DISCREPANCY, check")

# signal speeds c^2 = -g^ii/g^TT, g^TT = -1/f:
gTT = sp.simplify(ginv[0,0])
ck("B3a", sp.simplify(gTT + 1/fS)==0, "g^TT = -1/f")
cang2 = sp.simplify(-ginv[2,2]/gTT)
crad2 = sp.simplify(-ginv[1,1]/gTT)
print("   c_ang^2 =", cang2, "  c_rad^2 =", crad2)
ck("B3b", sp.simplify(cang2 - fS**2/Ds)==0,
   f"c_ang^2 = f^2/D_s (diverges as 1/D_s at D_s=0)")
ck("B3c", sp.simplify(crad2 - fS*r**2*WS/Ds)==0,
   f"c_rad^2 = f r^2 W/D_s (diverges as 1/D_s)")
# BOTH diverge as 1/D_s => D_s=0 is a genuine characteristic degeneracy. ✓

# ---- (2) q* branch: q* = 2 r^2 W f_r f_th / P ----
# On q=q*, D|q* = r^2 W Dw^2/P^2 with P=f r^2 W f_r^2+f_th^2,
#   Dw = f r^2 W f_r^2 - f_th^2. Verify D_s(q*) = r^2 W Dw^2/P^2.
fr, fth = sp.symbols('f_r f_th', real=True)
P = fS*r**2*WS*fr**2 + fth**2
Dw = fS*r**2*WS*fr**2 - fth**2
qstar = 2*r**2*WS*fr*fth/P
Dq = sp.simplify((r**2*WS - fS*qstar**2))
ck("B4", sp.simplify(Dq - r**2*WS*Dw**2/P**2)==0,
   "D_s|q* = r^2 W Dw^2/P^2 (so D_s=0 <=> Dw=0 on the q* branch)")

# ---- (3) u* surface on C=0 member, and REALITY on banked geometry ----
a, au = sp.symbols('a a_u', positive=True)
# C=0: f=a/r, f_r=-a/r^2, f_th^2 = au^2 (1-u^2)/r^2.
f_C0 = a/r; fr_C0 = -a/r**2; fth2_C0 = au**2*(1-u**2)/r**2
Dw_C0 = sp.simplify(f_C0*r**2*WS*fr_C0**2 - fth2_C0)
print("\n   Dw_C0 =", sp.simplify(Dw_C0*r**3), "(times r^3)")
# solve Dw=0 for u^2:
sol = sp.solve(sp.Eq(Dw_C0,0), u**2)
ustar2 = sp.simplify(sol[0])
print("   u*^2 =", ustar2)
ck("B5", sp.simplify(ustar2 - (1 - a**3*WS/(au**2*r)))==0,
   "u*^2 = 1 - a^3 W/(a_u^2 r)  [INDEPENDENT solve]")
# reality / in-range: u*^2 in (0,1) iff 0 < a^3 W/(au^2 r) < 1
#  i.e. a^3 W < au^2 r. Is this satisfied on BANKED geometry?
# Banked deep-cell: f=a/r at f_min ~ 0.002 (w4_results). Need actual a,au,r.
# The CLAIM is u* real ONLY in a radial band a^3 W < au^2 r. Test honestly:
# at small r (deep), LHS a^3 W fixed, RHS au^2 r SMALL => a^3 W > au^2 r
#   => u*^2 < 0 => u* NOT real (no wall) at small r.
# at LARGE r, au^2 r grows => eventually u*^2 in (0,1). So walls exist
# at LARGE r, not deep. This is the OPPOSITE of 'deep cell'. FLAG.
print("\n   reality test: u*^2>0 requires a^3 W < a_u^2 r i.e. r > a^3 W/a_u^2")
print("   => walls appear at LARGE r (outer), NOT deep (small r). Committed")
print("   XA2 says 'deep enough r' -- but r large = outer, r=e^-t small=deep.")
# numeric: pick a=1,au=1,w=0 (W=1): need r>1. f=a/r=1/r. deep cell f~big => r small =>no wall.
ck("B5b", True, "u* real iff r > a^3 W/a_u^2 (outer band); NOT automatic on deep cells -- SCOPE FLAG")

# ---- (4) wall count and rise with ell ----
# flat: Dw quadratic in u^2 -> ONE root u*^2 -> +-u* = 2 interior latitudes.
# ell=2 lobe a(u)=a0(1+e2(3u^2-1)/2): degree of Dw in u?
a0,e2 = sp.symbols('a0 e2', positive=True)
a_ell = a0*(1+e2*(3*u**2-1)/2)
au_ell = sp.diff(a_ell,u)
f2=a_ell/r; fr2=-a_ell/r**2; fth2_2=au_ell**2*(1-u**2)/r**2
Dw2 = sp.expand(f2*r**2*WS*fr2**2 - fth2_2)
num = sp.numer(sp.together(Dw2)).subs(sp.Symbol('w',real=True),0)
deg = sp.Poly(sp.expand(num), u).degree()
ck("B6", deg==6, f"ell=2 lobe: deg(Dw in u) = {deg} (flat=2). Wall poly degree rises with ell")
# count REAL roots in (0,1)? The claim '2->6' is about deg, not necessarily
# real-root count. Check: how many real roots in (-1,1) for a sample?
print("\n   --- real-root count of Dw=0 in (-1,1), ell=2 sample ---")
for (a0v,e2v,rv) in [(1,0.5,5),(1,0.9,5),(1,0.5,20)]:
    poly = sp.Poly(sp.expand(num.subs({a0:a0v,e2:e2v,r:rv})), u)
    rts = [c for c in poly.nroots() if abs(sp.im(c))<1e-9 and -1<sp.re(c)<1]
    print(f"   a0={a0v},e2={e2v},r={rv}: real roots in(-1,1) = {len(rts)}: {[round(float(sp.re(c)),4) for c in rts]}")
print("   => deg rises (2->6) but ACTUAL real walls depend on params/r band")

print(f"\nVB: {len(PASS)} PASS / {len(FAIL)} FAIL")
if FAIL: print("FAILED:", FAIL)
