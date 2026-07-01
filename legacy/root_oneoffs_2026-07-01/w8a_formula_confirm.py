#!/usr/bin/env python3
"""W8 PHASE-A (ASSEMBLE) — formula confirmation scratch.

NO GPU, NO heavy compute.  This script does ONLY light sympy to pin the
EXACT forms quoted in w8_catalog_problem.md, so a Phase-B solver agent
can trust the transcription.  Every claim is an assert.  Nothing here is
new physics; all forms are re-derived/cross-checked against the
committed scripts (w4a_system.py, w5_arm2_sym.py, w6_arm1_lib.py,
w4b_evolib.py, mass_audit_results.md).

Log: /tmp/w8a_formula_confirm.log
"""
import sys
import sympy as sp
from sympy import Rational as Ra

P = []
def ck(tag, cond, note=""):
    ok = bool(cond)
    P.append(ok)
    print(f"W8A-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

# ----------------------------------------------------------------------
# 1. THE METRIC + det g (areal canon rho = r survives all w) — w4a A0
# ----------------------------------------------------------------------
T, th = sp.symbols('T theta', real=True)
r = sp.Symbol('r', positive=True)
f, q = sp.Symbol('f', positive=True), sp.Symbol('q', real=True)
wp = sp.Symbol('w_p', positive=True)        # w_p = 1 + w
sth = sp.Symbol('s_th', positive=True)
W = wp**2
g4 = sp.Matrix([[-f, 0, 0, 0],
                [0, 1/f, q, 0],
                [0, q, r**2*W, 0],
                [0, 0, 0, r**2*sth**2/W]])
D = r**2*W - f*q**2                          # f * det of (r,th) block
ck("1a", sp.simplify(g4.det() + (r**2*sth**2/W)*D) == 0,
   "det g4 = -(r^2 sin^2/W) D,  D = r^2(1+w)^2 - f q^2")
# angular determinant block is r^4 sin^2 independent of w (areal canon):
ck("1b", sp.simplify((r**2*W)*(r**2*sth**2/W) - r**4*sth**2) == 0,
   "g_thth g_phph = r^4 sin^2 (rho = r areal for ALL w)")
# same-minus fold: with time row (a,b)=(g_Tr,g_Tth), det lifts on D=0
a_, b_ = sp.symbols('a b', real=True)
g5 = sp.Matrix([[-f, a_, b_, 0],
                [a_, 1/f, q, 0],
                [b_, q, r**2*W, 0],
                [0, 0, 0, r**2*sth**2/W]])
det5 = sp.simplify(g5.det())
det5_tgt = -(r**2*sth**2/W)*(f*D*(1+a_**2) + (b_-f*q*a_)**2)/f
ck("1c", sp.simplify(det5 - det5_tgt) == 0,
   "time-on det g4 = -(r sin)^2/[f(1+w)^2][f D(1+a^2)+(b-fqa)^2] (W6)")
# on D=0: substitute the q that makes r^2 W - f q^2 = 0, i.e. q^2 = r^2 W/f
q_fold = sp.sqrt(r**2*W/f)
det5_on = sp.simplify(det5.subs(q, q_fold))
ck("1d", sp.simplify(det5_on + (r**2*sth**2/W)*(b_-f*q_fold*a_)**2/f) == 0,
   "on D=0: det g4 -> -(r sin)^2 (b-fqa)^2/[f(1+w)^2] != 0 (fold, not edge)")

# ----------------------------------------------------------------------
# 2. C1 density at q=0 static + the runaway tadpole — w4a A2/A4
# ----------------------------------------------------------------------
c = sp.Integer(2)                            # positive banked convention
fr, fth = sp.symbols('f_r f_theta', real=True)
phir, phith = -fr/(2*f), -fth/(2*f)
ginv = g4.inv()
K2 = ginv[1,1]*phir**2 + 2*ginv[1,2]*phir*phith + ginv[2,2]*phith**2
L_C1 = sp.simplify((c/2)*f*K2*(r*sth*sp.sqrt(D)/wp))
L_C1_q0 = sp.simplify(L_C1.subs(q, 0))
ck("2a", sp.simplify(L_C1_q0 - (c/8)*sth*(r**2*fr**2 + fth**2/(f*W))) == 0,
   "L_C1(q=0) = (c/8) sin[r^2 f_r^2 + f_th^2/(f(1+w)^2)], c=2")
dLdw = sp.simplify(sp.diff(L_C1_q0, wp))
ck("2b", sp.simplify(dLdw + (c/4)*sth*fth**2/(f*wp**3)) == 0,
   "dL_C1/dw|q=0 = -(c/4) sin f_th^2/(f(1+w)^3): the C1 runaway tadpole")

# ----------------------------------------------------------------------
# 3. W_wave (W2/VW1 species) + D_alg (W5) + the (1-2k/f) factor — w5 B
# ----------------------------------------------------------------------
wsym, wr_s, wT_s = sp.symbols('w w_r w_T', real=True)
L_W = 2*r**2*sth/(1+wsym)**2 * (wT_s**2/f - f*wr_s**2)
ck("3a", sp.simplify(L_W.subs(wT_s, 0)
                     + 2*r**2*sth*f*wr_s**2/(1+wsym)**2) == 0,
   "W_wave static = -2 r^2 sin f w_r^2/(1+w)^2; chars dr/dT = +-f")
L_C1ang = (c/8)*sth*fth**2/(f*W)
D_alg = -sth*fth**2/(2*f**2*W)
ck("3b", sp.simplify(D_alg + (2/f)*L_C1ang) == 0,
   "D_alg = -(1/2) sin f_th^2/(f^2(1+w)^2) == -(2/f) L_C1ang (densities)")
kap = sp.Symbol('kappa', real=True)
ck("3c", sp.simplify((L_C1ang + kap*D_alg) - (1 - 2*kap/f)*L_C1ang) == 0,
   "L_C1ang + kappa D_alg = (1 - 2 kappa/f) L_C1ang: cancels on f=2kappa")

# ----------------------------------------------------------------------
# 4. q* algebraic branch (angular sector closes algebraically) — w4a A6
# ----------------------------------------------------------------------
A_ = f*r**2*W*fr**2 + fth**2
dLdq = sp.together(sp.diff(L_C1, q))
qstar = 2*r**2*W*fr*fth/A_
ck("4a", sp.simplify(dLdq.subs(q, qstar)) == 0,
   "q* = 2 r^2(1+w)^2 f_r f_th/(f r^2(1+w)^2 f_r^2 + f_th^2) solves dL/dq=0")
Delta_w = f*r**2*W*fr**2 - fth**2
ck("4b", sp.simplify(A_**2 - 4*f*r**2*W*(fr*fth)**2 - Delta_w**2) == 0,
   "A^2 - 4 f r^2 W (f_r f_th)^2 = Delta_w^2 (Delta_w = f r^2(1+w)^2 f_r^2 - f_th^2)")

# ----------------------------------------------------------------------
# 5. Misner-Sharp mass observable — mass_audit (m=(y/2)(1-f); p_F)
# ----------------------------------------------------------------------
# MS mass of a spherical exterior leaf in areal radius: m(r) = (r/2)(1-f).
# For the banked vacuum f = C + a/r the exterior MS mass is constant = -a/2:
Cc, aa = sp.symbols('C a', real=True)
m_of = (r/2)*(1 - (Cc + aa/r))
ck("5a", sp.simplify(m_of - ((1-Cc)*r/2 - aa/2)) == 0,
   "m_MS(r)=(r/2)(1-f); on vacuum f=C+a/r the a-part gives const -a/2")
# p_F as the interface-momentum jet functional: p_F = y M0' - M0 (Legendre),
# i.e. the constant exterior charge; check it equals -a/2 on the vacuum leaf
# M0(y) = (y/2)(1-f) with f=1+a/y (C=1 exterior): p_F = y M0' - M0
y = sp.Symbol('y', positive=True)
M0 = (y/2)*(1 - (1 + aa/y))      # = -a/2 exactly (C=1 exterior weld), const
pF = sp.simplify(y*sp.diff(M0, y) - M0)
# M0 is constant (= -a/2); M0'=0 so p_F = -M0 = +a/2; Q = 2 p_F = a
ck("5b", sp.simplify(M0 + aa/2) == 0 and sp.simplify(pF - aa/2) == 0,
   "M0 = -a/2 (const exterior); p_F = yM0'-M0 = +a/2 = -M0; Q = 2 p_F = a "
   "(p_F = the constant exterior MS charge of the leaf)")

# ----------------------------------------------------------------------
# 6. reduced v-chart wave equation (the Phase-B solve variable) — w4b
# ----------------------------------------------------------------------
# v = ln(1+w) makes the wave sector exactly free; per-ray tortoise dr/dx=f:
#   v_TT = v_xx + 2(f/r) v_x + S(v;x)
# confirm the static-source equilibrium structure (S_on equilibrium e^{3v}=1-2k/f)
v0 = sp.Symbol('v0', real=True)
S_on0 = (c*fth**2/(16*kap*r**2))*(sp.exp(v0) - (1 - 2*kap/f)*sp.exp(-2*v0))
ck("6a", sp.simplify(S_on0.subs(v0, sp.log(1 - 2*kap/f)/3)) == 0,
   "ON-branch equilibrium e^{3v}=1-2k/f (exists only where f>2kappa)")
ck("6b", sp.simplify(S_on0.subs(v0, 0) - c*fth**2/(8*f*r**2)) == 0,
   "S_on(v=0)=+(c/8)f_th^2/(f r^2) kappa-FREE: every shaped cell self-dresses")

print(f"\nW8A FORMULA CONFIRM: {sum(P)}/{len(P)} PASS")
sys.exit(0 if all(P) else 1)
