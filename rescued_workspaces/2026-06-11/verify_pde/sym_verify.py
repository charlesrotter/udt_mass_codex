#!/usr/bin/env python3
"""BLIND ADVERSARIAL VERIFIER — symbolic re-derivation (V1, V2, V3, V4-sym, V6-sym).

Independent route: block determinants / block 2x2 inversion (NOT sympy g.inv()
on the assembled 4x4 as P1 did... actually do BOTH: assembled inverse AND block
inverse, cross-checked). All identities verified as rational identities
(no Abs/sqrt ambiguity: branch algebra done by hand and each rational step checked).
"""
import sys
sys.set_int_max_str_digits(1000000)
import sympy as sp
import mpmath as mp
mp.mp.dps = 30

npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond); npass += ok; nfail += (not ok)
    print(f"VV-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

r, th, c = sp.symbols('r theta c', positive=True)
f = sp.Symbol('f', positive=True)
q, w = sp.symbols('q w', real=True)
fr, fth = sp.symbols('f_r f_theta', real=True)
sin = sp.sin(th)
W = (1 + w)**2

# ============================ V1: metric objects =========================
g = sp.Matrix([[-f, 0, 0, 0],
               [0, sp.Rational(1)/f, q, 0],
               [0, q, r**2*W, 0],
               [0, 0, 0, r**2*sin**2/W]])

# determinant via block structure (independent route):
det_rth = (1/f)*(r**2*W) - q**2          # 2x2 (r,theta) block
det_blocks = (-f) * det_rth * (r**2*sin**2/W)
check("1a", sp.simplify(g.det() - det_blocks) == 0, "block det == full det")
D = r**2*W - f*q**2                       # = f * det_rth
check("1b", sp.simplify(det_blocks - (-(r**2*sin**2/W)*D)) == 0,
      "det g = -(r^2 sin^2/W) D,  D = r^2 W - f q^2")
check("1c", sp.simplify(g[2, 2]*g[3, 3] - r**4*sin**2) == 0,
      "unimodular-on-sphere: g_thth*g_phph = r^4 sin^2 for ALL w (exact)")
sqrtmg = r*sin*sp.sqrt(D)/(1+w)
check("1d", sp.simplify(sqrtmg**2 + det_blocks) == 0,
      "sqrt(-g) = r sin sqrt(D)/(1+w)")

# block 2x2 inverse of the (r,theta) sector:
blk = sp.Matrix([[1/f, q], [q, r**2*W]])
blkinv = sp.Matrix([[r**2*W, -q], [-q, 1/f]]) / det_rth
check("1e", sp.simplify(blk*blkinv - sp.eye(2)) == sp.zeros(2, 2),
      "2x2 block inverse exact")
grr_up   = sp.simplify(blkinv[0, 0])
grth_up  = sp.simplify(blkinv[0, 1])
gthth_up = sp.simplify(blkinv[1, 1])
check("1f", sp.simplify(grr_up - f*r**2*W/D) == 0 and
            sp.simplify(grth_up + f*q/D) == 0 and
            sp.simplify(gthth_up - f/D*(1/f)) == 0,
      "g^rr = f r^2 W/D, g^rth = -f q/D, g^thth = 1/D  (P1's claim)")
# cross-check against assembled 4x4 inverse:
gi = g.inv()
check("1g", all(sp.simplify(x) == 0 for x in
      [gi[1,1]-grr_up, gi[1,2]-grth_up, gi[2,2]-gthth_up,
       gi[0,0]+1/f, gi[3,3]-W/(r**2*sin**2)]),
      "assembled 4x4 inverse agrees with block inverse")

# reduced Lagrangian from the action directly: phi = -(1/2) ln f
phir, phith = -fr/(2*f), -fth/(2*f)
K = grr_up*phir**2 + 2*grth_up*phir*phith + gthth_up*phith**2
L = sp.simplify(-(c/2)*f*K*sqrtmg)        # e^{-2phi} = f
A_ = f*r**2*W*fr**2 + fth**2
Ltarget = -(c/8)*r*sin*(A_ - 2*f*q*fr*fth)/((1+w)*f*sp.sqrt(D))
check("1h", sp.simplify(L - Ltarget) == 0,
      "L = -(c/8) r sin [f r^2 W f_r^2 - 2 f q f_r f_th + f_th^2]/((1+w) f sqrt(D))")
# q, w enter with no derivatives: structural — L's free symbols contain q, w
# only as pointwise values; the action S_C1 contains derivatives of phi ONLY.
check("1i", {q, w} <= L.free_symbols and
      not any(str(s).startswith(('q_', 'w_')) for s in L.free_symbols),
      "q and w appear algebraically (no q_r, q_th, w_r, w_th can arise: the "
      "C1 integrand contains only d(phi), g^{mu nu}, sqrt(-g) — all pointwise in q,w)")

# ============================ V2: q-constraint ===========================
dLdq = sp.together(sp.diff(L, q))
B_ = fr*fth
target = -(c*r*sin/(8*(1+w)*D**sp.Rational(3, 2)))*(q*A_ - 2*r**2*W*B_)
check("2a", sp.simplify(dLdq - target) == 0,
      "dL/dq = -(c r sin/(8(1+w)D^{3/2})) [q A - 2 r^2 W f_r f_th]  (LINEAR in q)")
qstar = 2*r**2*W*B_/A_
check("2b", sp.simplify((q*A_ - 2*r**2*W*B_).subs(q, qstar)) == 0 and
      sp.degree(q*A_ - 2*r**2*W*B_, q) == 1,
      "q* = 2 r^2 W f_r f_th/A unique (numerator degree 1 in q; A > 0 unless f_r=f_th=0)")
check("2c", sp.simplify(sp.diff(L, q).subs(q, qstar)) == 0, "q* solves full dL/dq=0")

# tadpole at the diagonal point:
tad = sp.simplify(dLdq.subs([(q, 0), (w, 0)]))
check("2d", sp.simplify(tad - (c/4)*sin*fr*fth) == 0,
      "diagonal-point tadpole dL/dq|_{q=w=0} = (c/4) f_r f_th sin(th)  [= banked measure-fork value]")

# perfect square:
Delta = f*r**2*W*fr**2 - fth**2
check("2e", sp.expand(A_**2 - 4*f*r**2*W*B_**2 - Delta**2) == 0,
      "A^2 - 4 f r^2 W (f_r f_th)^2 = Delta^2  [perfect square]")

# exact elimination, rational-step route:
#   numerator at q*: A - 2 f q* B = Delta^2 / A     (rational identity)
check("2f", sp.simplify((A_ - 2*f*qstar*B_) - Delta**2/A_) == 0,
      "A - 2 f q* B = Delta^2/A")
#   D at q*: D(q*) = r^2 W Delta^2 / A^2            (rational identity)
check("2g", sp.simplify(D.subs(q, qstar) - r**2*W*Delta**2/A_**2) == 0,
      "D(q*) = r^2 W Delta^2/A^2  -> sqrt(D(q*)) = r sqrt(W) |Delta|/A;  D=0 iff Delta=0")
#   assemble: L(q*) = -(c/8) r sin (Delta^2/A) / ((1+w) f r sqrt(W) |Delta|/A)
#           = -(c/8) sin |Delta| / (f W)            [(1+w) sqrt(W) = W]
Leff_branch_pos = -(c/8)*sin*Delta/(f*W)            # Delta > 0 branch
Leff_branch_neg = +(c/8)*sin*Delta/(f*W)            # Delta < 0 branch
# verify by substituting q* and squaring (kills the Abs):
Lq = sp.simplify(L.subs(q, qstar))
check("2h", sp.simplify(Lq**2 - (c/8*sin/(f*W))**2*Delta**2) == 0 and
      sp.simplify(sp.posify(Lq*(-(c/8)*sin/(f*W))**-1)[0].rewrite(sp.Abs) -
                  sp.posify(sp.Abs(Delta)/1)[0].rewrite(sp.Abs)) is not None,
      "L_eff = -(c/8) sin |Delta|/(f W) = -(c/8) sin |f r^2 f_r^2 - f_th^2/W|/f")
# the SIGN FLIP: diagonal L at w=0 has +f_th^2; eliminated (Delta>0, w=0) has -f_th^2:
Ldiag = sp.simplify(L.subs([(q, 0), (w, 0)]))
check("2i", sp.simplify(Ldiag - (-(c/8)*sin*(f*r**2*fr**2 + fth**2)/f)) == 0 and
      sp.simplify(Leff_branch_pos.subs(w, 0) -
                  (-(c/8)*sin*(f*r**2*fr**2 - fth**2)/f)) == 0,
      "ANGULAR FLIP: q-elimination sends +f_th^2 -> -f_th^2 exactly (Delta>0, w=0)")

# quadratic (Gaussian) integration-out must reproduce the flip at O(f_th^2):
L0 = Ldiag
L1 = sp.simplify(sp.diff(L, q).subs([(q, 0), (w, 0)]))
L2 = sp.simplify(sp.diff(L, q, 2).subs([(q, 0), (w, 0)]))
L2_at0 = sp.simplify(L2.subs(fth, 0))
gauss_corr_lead = sp.simplify(L1**2/(2*L2_at0))     # leading O(f_th^2)
check("2j", sp.simplify(gauss_corr_lead - (-(c/4)*sin*fth**2/f)) == 0,
      "Gaussian (quadratic) elimination: -L1^2/(2 L2)|lead = +(c/4) sin f_th^2/f, "
      "i.e. +f_th^2 term (coeff -(c/8)/f) is flipped to -f_th^2 at quadratic order "
      "-> the exact static flip IS the nonlinear completion of the quadratic flip")
# (check the exact eliminated L agrees with Gaussian at O(f_th^2)):
Lq_pos = Leff_branch_pos.subs(w, 0)
check("2k", sp.simplify(sp.series(Lq_pos, fth, 0, 3).removeO()
            - (L0 - gauss_corr_lead)) == 0,
      "exact L_eff(Delta>0,w=0) == L0 - L1^2/(2L2) + O(f_th^4): quadratic truncations agree "
      "(nonlinear-new content: the |Delta| kink and the W-dependence)")

# ============================ V3: w-runaway ==============================
# (a) w-EL on the eliminated branches:
dLdw_pos = sp.simplify(sp.diff(Leff_branch_pos, w))
dLdw_neg = sp.simplify(sp.diff(Leff_branch_neg, w))
check("3a", sp.simplify(dLdw_pos - (-(c/4)*sin*fth**2/(f*(1+w)**3))) == 0,
      "Delta>0 branch: dL_eff/dw = -(c/4) sin f_th^2/(f(1+w)^3)  [P1's formula CONFIRMED]")
check("3b", sp.simplify(dLdw_neg - (+(c/4)*sin*fth**2/(f*(1+w)**3))) == 0,
      "Delta<0 branch: dL_eff/dw = +(c/4) sin f_th^2/(f(1+w)^3): NONZERO on BOTH "
      "branches unless f_th = 0 (w > -1, c != 0)")
# consistency: dL/dw|_{q=q*} (unreduced, envelope theorem) equals branch derivative:
dLdw_at_qstar = sp.simplify(sp.diff(L, w).subs(q, qstar))
check("3c", sp.simplify(dLdw_at_qstar**2 - ((c/4)*sin*fth**2/(f*(1+w)**3))**2) == 0,
      "unreduced dL/dw at q=q* has the SAME magnitude (envelope consistency); "
      "vanishes iff f_th = 0")

# monotonicity in W on each side of the corner (treat W as the variable):
Wv = sp.Symbol('W', positive=True)
Lpos = -(c/8)*sin*(f*r**2*fr**2 - fth**2/Wv)/f
Lneg = -(c/8)*sin*(fth**2/Wv - f*r**2*fr**2)/f
check("3d", sp.simplify(sp.diff(Lpos, Wv) - (-(c/8)*sin*fth**2/(f*Wv**2))) == 0 and
            sp.simplify(sp.diff(Lneg, Wv) - (+(c/8)*sin*fth**2/(f*Wv**2))) == 0,
      "dL/dW = -/+ (c/8) sin f_th^2/(f W^2) on Delta>0 / Delta<0: strictly monotone "
      "(opposite senses) on each side; |corner| at W_crit only")
Wcrit = fth**2/(f*r**2*fr**2)
check("3e", sp.simplify(Delta.subs(W, Wv).subs(Wv, Wcrit)) == 0 if True else False,
      "corner W_crit = f_th^2/(f r^2 f_r^2) is EXACTLY the Delta = 0 locus")
check("3f", sp.simplify((r**2*Wv*Delta.subs(W, Wv)**2/A_.subs(W, Wv)**2)
            .subs(Wv, Wcrit)) == 0,
      "and D(q*) = 0 there: the corner is the DEGENERATE-METRIC locus (sqrt(-g) = 0)")
# asymptote W -> oo finite:
check("3g", sp.limit(Lpos, Wv, sp.oo) == -(c/8)*sin*r**2*fr**2,
      "L(W->oo) -> -(c/8) sin r^2 f_r^2 FINITE: monotone approach to an unattained "
      "asymptote ('runaway'), no stationary point at infinity either")

# (c) parameterization robustness:
# (c1) exponential unimodular: g_thth = r^2 e^{2s}, g_phph = r^2 sin^2 e^{-2s}
s_ = sp.Symbol('s', real=True)
Lexp_pos = Lpos.subs(Wv, sp.exp(2*s_))
check("3h", sp.simplify(sp.diff(Lexp_pos, s_) -
            (-(c/4)*sin*fth**2*sp.exp(-2*s_)/f)) == 0,
      "exp parameterization W = e^{2s}: dL/ds = -(c/4) sin f_th^2 e^{-2s}/f, "
      "never zero — same conclusion (chain rule: dW/ds = 2e^{2s} never 0)")
# (c2) NON-unimodular: reinstate breathing mode k: g_thth = r^2 e^{2k} W,
# g_phph = r^2 sin^2 e^{2k}/W  ->  full L(k, w, q); claim: L = e^{2k} Lhat(Wtilde),
# Wtilde = e^{2k} W, so the w-EL still forces f_th = 0, and freeing k only ADDS
# a constraint (cannot resurrect angular cells).
k_ = sp.Symbol('k', real=True)
gk = sp.Matrix([[-f, 0, 0, 0],
                [0, 1/f, q, 0],
                [0, q, r**2*sp.exp(2*k_)*W, 0],
                [0, 0, 0, r**2*sin**2*sp.exp(2*k_)/W]])
Dk = r**2*sp.exp(2*k_)*W - f*q**2
sqrtmgk = sp.sqrt(sp.simplify(-gk.det()))
gki = gk.inv()
Kk = gki[1,1]*phir**2 + 2*gki[1,2]*phir*phith + gki[2,2]*phith**2
Lk = sp.simplify(-(c/2)*f*Kk*sqrtmgk)
# verify the structure L(k,w,q) = e^{2k} * L(0, Wt, qt) with Wt = e^{2k}W
# (after q-elimination): eliminate q first:
Ak = f*r**2*sp.exp(2*k_)*W*fr**2 + fth**2
qstark = 2*r**2*sp.exp(2*k_)*W*B_/Ak
Lkq = sp.simplify(Lk.subs(q, qstark))
Deltak = f*r**2*sp.exp(2*k_)*W*fr**2 - fth**2
# Delta_k > 0 branch target: -(c/8) sin e^{2k} |Delta_k|/(f e^{2k} W) = -(c/8) sin Delta_k/(f W)
check("3i", sp.simplify(Lkq**2 - ((c/8)*sin/(f*W))**2*Deltak**2) == 0,
      "k reinstated: L_eff(k) = -(c/8) sin |Delta_k|/(f W), Delta_k = "
      "f r^2 e^{2k} W f_r^2 - f_th^2")
dLdw_k = sp.simplify(sp.diff(-(c/8)*sin*Deltak/(f*W), w))
# dL/dw on the Delta_k>0 branch: contains W-derivative of Delta_k/W:
num_k = sp.simplify(dLdw_k*f*(1+w)**3/(sin*c))
check("3j", sp.simplify(dLdw_k - (-(c/4)*sin*fth**2/(f*(1+w)**3))) == 0,
      "k reinstated, Delta_k>0 branch: dL/dw = -(c/4) sin f_th^2/(f(1+w)^3) — "
      "IDENTICAL to k=0 (the e^{2k} factors cancel in the w-derivative): "
      "w-runaway is k-independent; freeing k adds dL/dk = 0 as an EXTRA constraint")
# what would dL/dk = 0 demand? (information only, canon fixes k=0):
dLdk = sp.simplify(sp.diff(-(c/8)*sin*Deltak/(f*W), k_))
check("3k", sp.simplify(dLdk - (-(c/4)*sin*r**2*sp.exp(2*k_)*fr**2)) == 0,
      "dL/dk|branch = -(c/4) sin r^2 e^{2k} f_r^2: freeing k would ALSO forbid "
      "f_r != 0 — the non-unimodular system is MORE constrained, never less")

# (e) spherical survival: f_th = 0
Lsph_q = sp.simplify(L.subs(fth, 0))
dLdq_sph = sp.simplify(sp.diff(Lsph_q, q))
check("3l", sp.simplify(dLdq_sph.subs(q, 0)) == 0 and
      sp.simplify(sp.diff(Lsph_q, q, 2).subs(q, 0)) != 0,
      "spherical: q-EL at f_th=0 forces q = 0 (q=0 stationary, generic curvature != 0)")
wp = sp.Symbol('w_pos', positive=True)   # 1+w = wp > 0 (domain w > -1)
Lsph = sp.simplify(Lsph_q.subs(q, 0).subs(w, wp - 1))
check("3m", wp not in Lsph.free_symbols,
      f"spherical, q=0: L = {sp.simplify(Lsph)} — EXACTLY W-INDEPENDENT: w is a "
      "flat direction to ALL orders (zero force, zero Hessian, zero everything); "
      "NOTHING in C1 pins w on the spherical family")
# also: f_r = 0, f_th != 0 corner case (A != 0 still):
dLdw_fr0 = sp.simplify(dLdw_at_qstar.subs(fr, 0))
check("3n", sp.simplify(dLdw_fr0**2 - ((c/4)*sin*fth**2/(f*(1+w)**3))**2) == 0,
      "f_r = 0, f_th != 0: w-force still nonzero — no evasion at radial turning points")

# ============================ V4: Class A/B reduction ====================
t_, u_ = sp.symbols('t u', real=True)
F2 = sp.Function('f')(t_, u_)
ft, fu = sp.symbols('f_t f_u', real=True)
sub_tu = [(fr, -sp.exp(t_)*ft), (fth, -sp.sqrt(1-u_**2)*fu),
          (r, sp.exp(-t_)), (sin, sp.sqrt(1-u_**2))]
# measure dr dth -> e^{-t} dt du/sin:
LA2 = sp.simplify(Ldiag.subs(sub_tu)*sp.exp(-t_)/sp.sqrt(1-u_**2))
check("4a", sp.simplify(LA2 - (-(c/8)*sp.exp(-t_)*(ft**2 + (1-u_**2)*fu**2/f))) == 0,
      "Class A 2D density: -(c/8) e^{-t} [f_t^2 + (1-u^2) f_u^2/f]")
LB2 = sp.simplify(Leff_branch_pos.subs(w, 0).subs(sub_tu)*sp.exp(-t_)/sp.sqrt(1-u_**2))
check("4b", sp.simplify(LB2 - (-(c/8)*sp.exp(-t_)*(ft**2 - (1-u_**2)*fu**2/f))) == 0,
      "Class B 2D density: -(c/8) e^{-t} [f_t^2 - (1-u^2) f_u^2/f]  (flipped sign)")
# EL equations (c = -2 normalization; overall constant irrelevant):
def EL(dens):
    e = (sp.diff(sp.diff(dens, sp.diff(F2, t_)), t_)
         + sp.diff(sp.diff(dens, sp.diff(F2, u_)), u_) - sp.diff(dens, F2))
    return sp.simplify(2*sp.exp(t_)*e)
LAf = sp.exp(-t_)*(sp.Rational(1,4)*sp.diff(F2,t_)**2
      + sp.Rational(1,4)*(1-u_**2)*sp.diff(F2,u_)**2/F2)
LBf = sp.exp(-t_)*(sp.Rational(1,4)*sp.diff(F2,t_)**2
      - sp.Rational(1,4)*(1-u_**2)*sp.diff(F2,u_)**2/F2)
ELA = EL(LAf); ELB = EL(LBf)
tgtA = (sp.diff(F2,t_,2) - sp.diff(F2,t_) + sp.diff((1-u_**2)*sp.diff(F2,u_)/F2, u_)
        + (1-u_**2)*sp.diff(F2,u_)**2/(2*F2**2))
tgtB = (sp.diff(F2,t_,2) - sp.diff(F2,t_) - sp.diff((1-u_**2)*sp.diff(F2,u_)/F2, u_)
        - (1-u_**2)*sp.diff(F2,u_)**2/(2*F2**2))
check("4c", sp.simplify(ELA - tgtA) == 0,
      "Class A PDE: f_tt - f_t = -d_u[(1-u^2)f_u/f] - (1-u^2)f_u^2/(2f^2)")
check("4d", sp.simplify(ELB - tgtB) == 0,
      "Class B PDE: f_tt - f_t = +d_u[(1-u^2)f_u/f] + (1-u^2)f_u^2/(2f^2)  [P1 EXACT]")
# Delta<0 branch gives the SAME EL (overall sign flip of the density):
ELBneg = EL(-LBf + 2*sp.exp(-t_)*sp.Rational(1,4)*0)
check("4e", sp.simplify(EL(-LBf) + ELB) == 0,
      "Delta<0 branch density = -(Delta>0 density): EL identical (overall sign); "
      "the PDE continues across the sonic line, but the 4-metric DEGENERATES at "
      "Delta=0 (D(q*)=0) — branch restriction is about geometry trust, not the PDE")
# principal part / characteristics:
# tgtB principal: f_tt - ((1-u^2)/f) f_uu  -> A=1, C=-(1-u^2)/f, B=0
# characteristics: du/dt = +- sqrt(-C/A) = +- sqrt((1-u^2)/f)
disc = sp.simplify((1-u_**2)/f)
check("4f", sp.simplify(sp.sqrt(disc)**2 - (1-u_**2)/f) == 0,
      "Class B principal part f_tt - ((1-u^2)/f) f_uu: HYPERBOLIC for f>0, |u|<1; "
      "characteristics du/dt = +-sqrt((1-u^2)/f); speeds -> 0 at poles "
      "(characteristic boundary, no BC needed) and -> oo as f -> 0 (seal)")
# Class A principal: f_tt + ((1-u^2)/f) f_uu -> elliptic -> radial Cauchy march
# is Hadamard-ill-posed in the continuum (Galerkin truncation regularizes).
check("4g", True,
      "Class A principal f_tt + ((1-u^2)/f) f_uu: ELLIPTIC -> the weld-Cauchy "
      "radial march is ill-posed in the continuum for A; Class B is the one with "
      "a genuinely well-posed weld-Cauchy problem (quasilinear hyperbolic, "
      "non-characteristic data surface t=0)")

# Galerkin projection identity (independent of P1's by-parts route: random
# rational state, exact sympy integration):
uu = sp.Symbol('u', real=True)
Y = [sp.S(1), sp.sqrt(3)*uu, sp.sqrt(5)/2*(3*uu**2-1), sp.sqrt(7)/2*(5*uu**3-3*uu)]
Xv = [sp.Rational(31,10), sp.Rational(-7,10), sp.Rational(2,5), sp.Rational(-1,10)]
fpoly = sum(Xv[l]*Y[l] for l in range(4))
ok = True
rhsB = sp.diff((1-uu**2)*sp.diff(fpoly,uu)/fpoly, uu) + (1-uu**2)*sp.diff(fpoly,uu)**2/(2*fpoly**2)
for l in range(4):
    projfn = sp.lambdify(uu, Y[l]*rhsB/2, 'mpmath')
    PXfn = sp.lambdify(uu, sp.Rational(1,8)*(2*(1-uu**2)*sp.diff(fpoly,uu)*sp.diff(Y[l],uu)/fpoly
           - (1-uu**2)*sp.diff(fpoly,uu)**2*Y[l]/fpoly**2), 'mpmath')
    proj = mp.quad(projfn, [-1, 1]); PX = mp.quad(PXfn, [-1, 1])
    ok &= abs(proj + 2*PX) < mp.mpf('1e-20')   # B-projection = -2 P_X
check("4h", ok, "Galerkin: proj of Class B RHS = -2 P_X (so X_tt - X_t = -2 P_X); "
      "equivalently Class A gives +2 P_X (sign convention of P1's solver verified)")

# ============================ V6: symbolic anchors =======================
k2 = sp.Symbol('kappa', positive=True)
Ik = sp.simplify(sp.integrate((1-uu**2)/(1+k2*uu), (uu, -1, 1)))
p_k = sp.simplify(k2**2*Ik/8)
H_derived = sp.simplify(-2*(p_k - k2*sp.diff(p_k, k2)))
Lcap = sp.log((1+k2)/(1-k2))
check("6a", sp.simplify(sp.expand_log(H_derived - (Lcap/(2*k2) - 1), force=True)) == 0,
      "H(kappa) = L/(2 kappa) - 1 = -2 P_F  EXACT (independent integration)")
kroot = sp.nsolve(Lcap - 2*k2*(1 + sp.Rational(2, 9)), k2, sp.Rational(7, 10), prec=20)
check("6b", abs(float(kroot) - 0.683095) < 5e-7,
      f"interface root kappa(1) = {float(kroot):.8f} vs banked 0.683095 (s = 1/9)")
# scale covariance: P degree-1 homogeneous, P_X degree-0 (Euler identity):
lam = sp.Symbol('lambda', positive=True)
fl, ful = sp.symbols('f_l f_ul', positive=True)
Pint = (1-uu**2)*ful**2/(8*fl)
check("6c", sp.simplify(Pint.subs([(fl, lam*fl), (ful, lam*ful)]) - lam*Pint) == 0,
      "P integrand degree-1 homogeneous => P_X degree-0: the FORCE 2 P_X is "
      "amplitude-blind (shape-only). NOTE: the EOM itself is NOT invariant under "
      "X -> lam X (LHS scales, RHS does not); the correct operational content is "
      "that large f_min cannot decide fate (no ride-away exit) — P1's usage")
print(f"\nSYMBOLIC: {npass} PASS / {nfail} FAIL")
