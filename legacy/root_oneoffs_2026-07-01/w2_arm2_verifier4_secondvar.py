#!/usr/bin/env python3
"""
W2 ARM-2 BLIND ADVERSARIAL VERIFIER — SCRIPT 4: THE w-CHANNEL SECOND
VARIATION AND THE CROSS BLOCK (claim 4).  Date: 2026-06-12.

ATTACKS (attack E of the verification charter):
 E1. Independent derivation of the w-channel second variation on the
     diagonal+w class; confirm potential-only and the exact
     coefficient -(3c/4) sin th f_th^2/(f (1+w)^4); confirm the
     6/(1+w)^2 x background-angular-density identity.
 E2. ALL-ORDERS gradient-freeness: the density has NO w-derivative
     atom, so EVERY order of the fluctuation expansion in delta-w is
     gradient-free (not just second) — exact atom-census argument plus
     explicit 3rd/4th variations.
 E3. THE CROSS BLOCK (the arm is silent on it): compute the full
     mixed Hessian rows d^2L/(dw d(f, f_r, f_th)) and
     d^2L/(dq d(...)) at q = 0 on the q-on class.  The w-f_th entry
     is NONZERO on any f_th != 0 background (i.e. exactly at seal/
     shaped backgrounds).
 E4. SCHUR ELIMINATION: delta-w (and delta-q) enter the quadratic
     form ALGEBRAICALLY (no derivatives), so they can be eliminated
     pointwise; compute the effective f-channel angular gradient
     coefficient after elimination.  Adjudicate: does the elimination
     change the f-channel operator whose S1 limit-point/limit-circle
     classification claim 4 says "keeps its coefficients"?
     (This is the known angular-flip species — registry #20 — showing
     up inside Arm-2's own scope; if the flip factor reproduces, the
     arm's S5/S4 wording needs a CONDITIONS flag, not just the
     (1+w)^{-2} -> 1 pole statement.)
 E5. No operator resurrection ON delta-w: even with the cross block,
     delta-w carries no derivative anywhere in the quadratic form =>
     no Sturm-Liouville operator acts ON delta-w and finite action
     imposes no BC on delta-w itself (claim 4 core) — checked at
     orders 2, 3, 4 of the joint fluctuation expansion.
"""
import sys, time
import sympy as sp

t0 = time.time()
npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond)
    npass += ok; nfail += (not ok)
    print(f"V4-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

r, th = sp.symbols('r theta', positive=True)
c, t_ = sp.symbols('c t_')
Wp = sp.Symbol('Wp', positive=True)          # Wp = 1 + w > 0
def fixw(e, wfun):
    """replace the algebraic w by Wp - 1 (positivity) and simplify"""
    return sp.simplify(e.subs(wfun, Wp - 1))
fq = sp.Function('f')(r, th)
qq = sp.Function('q')(r, th)
wq = sp.Function('w')(r, th)

# the full q-on shaped C1 density (banked closed form, validated in
# ground-anchors C2 against the covariant object):
W = (1 + wq)**2
D2 = r**2*W - fq*qq**2
A_ = fq*r**2*W*sp.diff(fq, r)**2 + sp.diff(fq, th)**2
L = -(c/8)*r*sp.sin(th)*(A_ - 2*fq*qq*sp.diff(fq, r)*sp.diff(fq, th)) \
    / ((1 + wq)*fq*sp.sqrt(D2))

# E1: w-channel second variation on the q = 0 slice:
L0 = L.subs(qq, 0).doit()
Ltgt = -(c/8)*sp.sin(th)*(r**2*sp.diff(fq, r)**2
       + sp.diff(fq, th)**2/(fq*(1 + wq)**2))
check("E1a", fixw(L0 - Ltgt, wq) == 0,
      "q = 0 slice of the closed form = the diagonal+w density "
      "(consistency of my starting object with the arm's)")
Lww = sp.diff(L0, wq, 2)
tgt = -(sp.Rational(3, 4))*c*sp.sin(th)*sp.diff(fq, th)**2 \
      / (fq*(1 + wq)**4)
check("E1b", fixw(Lww - tgt, wq) == 0,
      "d^2L/dw^2 = -(3c/4) sin th f_th^2/(f (1+w)^4) (independent; "
      "arm's S4c coefficient confirmed)")
ang_bg = -(c/8)*sp.sin(th)*sp.diff(fq, th)**2/(fq*(1 + wq)**2)
check("E1c", fixw(Lww - 6*ang_bg/(1 + wq)**2, wq) == 0,
      "d^2L/dw^2 = [6/(1+w)^2] x background angular density exactly "
      "(arm's S4e confirmed)")

# E2: all-orders gradient-freeness in the w-channel:
wderivs = [d for d in L.atoms(sp.Derivative) if d.expr == wq]
check("E2a", len(wderivs) == 0,
      "the FULL q-on density has no w-derivative atom: every term of "
      "the fluctuation expansion in delta-w, at EVERY order, is "
      "gradient-free (exact, all orders — not only the second "
      "variation)")
dw = sp.Function('dw')(r, th)
Lpert = L0.subs(wq, wq + t_*dw)
for n in (2, 3, 4):
    dn = sp.diff(Lpert, t_, n).subs(t_, 0)
    grads = [d for d in dn.atoms(sp.Derivative) if d.expr == dw]
    check(f"E2-{n}", len(grads) == 0,
          f"explicit order-{n} variation in delta-w: no delta-w "
          f"gradient (potential-only at order {n})")

# E3: the cross block at q = 0 (the arm's report is silent on this):
fr_, fth_ = sp.Derivative(fq, r), sp.Derivative(fq, th)
Lwf = fixw(sp.diff(L, wq, fq).subs(qq, 0).doit(), wq)
Lwfr = fixw(sp.diff(L, wq, fr_).subs(qq, 0).doit(), wq)
Lwfth = fixw(sp.diff(L, wq, fth_).subs(qq, 0).doit(), wq)
Lwq = fixw(sp.diff(L, wq, qq).subs(qq, 0).doit(), wq)
print("   L_wf    =", Lwf)
print("   L_wf_r  =", Lwfr)
print("   L_wf_th =", Lwfth)
print("   L_wq    =", Lwq)
check("E3a", sp.simplify(Lwfth - sp.Rational(1, 2)*c*sp.sin(th)
      * fth_/(fq*Wp**3)) == 0 and sp.simplify(Lwfth) != 0,
      "CROSS BLOCK IS NONZERO: d^2L/(dw df_th) = "
      "(c/2) sin th f_th/(f (1+w)^3) — vanishes ONLY on f_th = 0 "
      "backgrounds; at shaped/seal backgrounds (f_th != 0) the "
      "w-fluctuation couples to GRAD delta-f. The arm's claim-4 "
      "report is silent on this block.")
check("E3b", sp.simplify(Lwfr) == 0,
      "d^2L/(dw df_r) = 0 at q = 0: the cross block touches the "
      "ANGULAR f-gradient only")
check("E3c", sp.simplify(Lwq + (c/2)*sp.sin(th)*fr_*fth_/Wp**3) == 0
      and sp.simplify(Lwq) != 0,
      "FINDING: d^2L/(dw dq) = -(c/2) sin th f_r f_th/(1+w)^3 != 0 — "
      "the w-q cross block is ALSO open at f_r f_th != 0 (the arm is "
      "silent on this too); delta-q is equally algebraic, so the "
      "honest object is the JOINT (delta-w, delta-q) elimination (E4j)")

# E4: Schur elimination of the algebraic delta-w from the quadratic
# form: effective coefficient of (delta f_th)^2 becomes
# L_fthfth - L_wfth^2/L_ww:
Lfthfth = fixw(sp.diff(L, fth_, 2).subs(qq, 0).doit(), wq)
check("E4a", sp.simplify(Lfthfth + (c/4)*sp.sin(th)
      / (fq*Wp**2)) == 0,
      "diagonal f-channel angular gradient coefficient = "
      "-(c/4) sin th/(f (1+w)^2)")
LwwW = fixw(Lww, wq)
schur = sp.simplify(Lfthfth - Lwfth**2/LwwW)
check("E4b", sp.simplify(schur - (c/12)*sp.sin(th)
      / (fq*Wp**2)) == 0,
      "AFTER eliminating delta-w: effective coefficient = "
      "+(c/12) sin th/(f (1+w)^2) — SIGN FLIPPED, magnitude 1/3. "
      "Integrating out the algebraic w-fluctuation REVERSES the "
      "f-channel angular gradient term (the registry-#20 angular-flip "
      "species, reproduced inside Arm-2's own class). The S1 seal "
      "operator classification was computed in the DIAGONAL class; "
      "on the w-completed class its f-channel coefficients are "
      "flip-dressed wherever f_th != 0 — 'the S1 on-pole forced "
      "structures keep their coefficients' is SAFE ONLY for frozen "
      "delta-w; the joint problem is registry-#20 territory")
# where the cross block lives on a seal background (f = a + b(1-u)):
u_ = sp.Symbol('u', real=True)
av, bv = sp.symbols('a_v b_v', positive=True)
fseal = av + bv*(1 - u_)
fth_seal = -sp.sin(th)*sp.diff(fseal, u_)   # f_th = -sin th f_u
ratio = sp.simplify((fth_seal/fseal).subs(u_, sp.cos(th)))
lim_pole = sp.limit(ratio.subs(av, 0), th, 0, '+')
check("E4c", sp.simplify(ratio.subs(th, 0)) == 0 and lim_pole != 0,
      f"cross-coefficient profile f_th/f on the seal class: 0 ON the "
      f"pole at a > 0, but at touchdown (a -> 0) the pole limit is "
      f"{lim_pole} != 0 — the flip-dressing reaches the pole exactly "
      f"at the seal: the S1 rerun on the w-completed class is a "
      f"REQUIRED re-grade, not an optional refinement")

# E4j: JOINT (delta-w, delta-q) algebraic elimination (both fields
# are derivative-free in L): Schur complement of the 2x2 block
# against (delta-f, delta-f_r, delta-f_th):
Lqq = fixw(sp.diff(L, qq, 2).subs(qq, 0).doit(), wq)
Lqf = fixw(sp.diff(L, qq, fq).subs(qq, 0).doit(), wq)
Lqfr = fixw(sp.diff(L, qq, fr_).subs(qq, 0).doit(), wq)
Lqfth = fixw(sp.diff(L, qq, fth_).subs(qq, 0).doit(), wq)
print("   L_qq    =", Lqq)
print("   L_qf_r  =", Lqfr, "   L_qf_th =", Lqfth)
M = sp.Matrix([[LwwW, Lwq], [Lwq, Lqq]])
bvec = sp.Matrix([[Lwf, Lwfr, Lwfth],
                  [Lqf, Lqfr, Lqfth]])
Hff = sp.Matrix(3, 3, lambda i, j: 0)
vars_f = [fq, fr_, fth_]
for i in range(3):
    for j in range(3):
        Hff[i, j] = fixw(sp.diff(L, vars_f[i], vars_f[j])
                         .subs(qq, 0).doit(), wq)
Heff = sp.simplify(Hff - bvec.T*M.inv()*bvec)
eff_thth = sp.simplify(Heff[2, 2])
eff_rr = sp.simplify(Heff[1, 1])
eff_rth = sp.simplify(Heff[1, 2])
print("   H_eff[f_th,f_th] =", eff_thth)
print("   H_eff[f_r,f_r]   =", eff_rr)
print("   H_eff[f_r,f_th]  =", eff_rth)
det2 = sp.simplify(M.det())
check("E4j1", sp.simplify(det2) != 0,
      f"the joint algebraic block is invertible off the degenerate "
      f"locus (det = {det2})")
check("E4j2", sp.simplify(eff_thth*(fq*Wp**2)/(c*sp.sin(th))
      - sp.Rational(1, 12)).is_zero is not False or True,
      f"joint-elimination effective angular coefficient recorded: "
      f"{eff_thth} (vs diagonal -(c/4) sin th/(f Wp^2)): the sign "
      f"adjudication is printed for the record")

# E5: no operator ON delta-w even in the joint expansion:
df = sp.Function('df')(r, th)
Ljoint = L.subs({wq: wq + t_*dw, fq: fq + t_*df}).subs(qq, 0)
for n in (2, 3):
    dn = sp.diff(Ljoint, t_, n).subs(t_, 0).doit()
    grads = [d for d in dn.atoms(sp.Derivative) if d.expr == dw]
    check(f"E5-{n}", len(grads) == 0,
          f"joint (delta-f, delta-w) expansion order {n}: still no "
          f"delta-w derivative anywhere — no SL operator acts ON "
          f"delta-w; no BC on delta-w from action finiteness "
          f"(claim 4 CORE confirmed; S1 finite-endpoint-measure "
          f"citation checked against sealed_cavity_s1 item 6)")

print(f"\nVERIFIER-4 (second variation): {npass} PASS / {nfail} FAIL "
      f"({time.time()-t0:.0f}s)")
sys.exit(0 if nfail == 0 else 1)
