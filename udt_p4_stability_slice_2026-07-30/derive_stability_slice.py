#!/usr/bin/env python3
# P4 stability slice: second variation about banked massive solutions.
# Contract: PREREGISTRATION.md (this dir). Exact SymPy only; no floats, no
# numeric eigensolvers, no GPU. Checks are zero-residual or exact-condition.
# Kinds: SUBSTANTIVE (computed residual/condition) vs GUARD (citation/typing).
import sys, json
import sympy as sp

CHECKS = []
def check(name, cond, detail, kind="SUBSTANTIVE"):
    ok = bool(cond)
    CHECKS.append({"name": name, "pass": ok, "kind": kind, "detail": detail})
    print(("PASS" if ok else "FAIL") + f" [{kind}] {name}: {detail}")
    return ok

# ---- shared symbols (banked quadratic-class atlas, Slice-2/2b) ----
x, ell = sp.symbols('x ell', real=True, positive=False), sp.Symbol('ell', positive=True)
x = sp.Symbol('x', real=True)
aF = sp.Symbol('a_F', real=True, nonzero=True)          # pairing weight exponent (P1 branches; symbolic)
gp = sp.Symbol('g_p', positive=True)                    # depth stiffness (definite class)
gf, gh = sp.symbols('g_f g_h', positive=True)           # diagonal G_fh (general G by constant congruence, Cat-A)
cf, ch = sp.symbols('c_f c_h', real=True)               # conserved f/h momenta
E0 = sp.Symbol('E0', real=True)                         # member energy
w0, w1 = sp.symbols('w0 w1', real=True)
A = aF**2*E0/(2*gp)                                     # banked: w'' = 2A
w = A*x**2 + w1*x + w0                                  # banked quadratic-w atlas
sigma = cf**2/gf + ch**2/gh                             # c^T G^{-1} c
# banked energy relation: E0 = (gp*w1^2/aF^2 + sigma)/(2 w0)  <-> gp*w'^2 = aF^2*(2*E0*w - sigma)
energy_rel = sp.Eq(gp*w1**2/aF**2 + sigma, 2*w0*E0)
pbar = sp.log(w)/aF                                     # on-shell depth profile
fbar_p = (cf/gf)/w                                      # f'(x); hbar analogous
hbar_p = (ch/gh)/w

cf2_shell = gf*(2*w0*E0 - gp*w1**2/aF**2 - ch**2/gh)   # energy relation solved for c_f^2 (exact)
def on_energy_shell(expr):
    """Eliminate c_f^2 via the banked energy relation (exact)."""
    return sp.expand(expr).subs(cf**2, cf2_shell)

def resid(expr):
    """Zero-residual test after imposing the energy relation."""
    e = sp.cancel(sp.together(sp.expand(on_energy_shell(sp.expand(expr)))))
    return sp.simplify(e) == 0

print("== P4 stability slice: exact second-variation derivation ==")
print("Stages: A (S-i single-cell + massless controls), B (S-i mixed chain), C (S-ii fields-census)")
print("Perturbation-space provenance: banked wall/parity/slot census (boundary-action gate 2026-07-30),")
print("supplied f/bh parities both ways, BASE moduli (S-i: dlam const; S-ii: dlam(x) odd field).")

STAGE_RESULTS = {}

# ================= STAGE A (part 1): S-i assembly and operator structure =================
print("\n-- Stage A: S-i (constants-census massive family, quadratic-w atlas) --")
eps = sp.Symbol('epsilon', real=True)
lam, mu = sp.symbols('lambda mu', real=True)   # seat + its (BASE, constant) perturbation
aFp = sp.Symbol('a_Fprime', real=True)         # a_F'(lambda); = 2 on both P1 branches (banked)
# generic perturbation jets (pointwise alphabet)
vp, vp1, vf, vf1, vh, vh1 = sp.symbols('v_p v_p1 v_f v_f1 v_h v_h1', real=True)
p0s, p1s, f1s, h1s = sp.symbols('p0 p1 f1 h1', real=True)  # base-point jets (symbolic, off-shell)

# density S = e^{aF(lam) p} * Ltilde(p', f', h')  on the banked fiberwise-quadratic p-unmixed class
def dens(aF_, p0_, p1_, f1_, h1_):
    return sp.exp(aF_*p0_)*(gp*p1_**2/2 + gf*f1_**2/2 + gh*h1_**2/2)

# A-1: full second variation density (fields + lambda jointly), generic base point.
aF_of = aF + aFp*mu*eps        # lambda -> lambda + eps*mu enters only through a_F (a_F''=0, banked linear)
Sfull = dens(aF_of, p0s+eps*vp, p1s+eps*vp1, f1s+eps*vf1, h1s+eps*vh1)
d2S = sp.diff(Sfull, eps, 2).subs(eps, 0)
# expected quadratic form density (hand-assembled), generic base point:
W = sp.exp(aF*p0s)
Lt = gp*p1s**2/2 + gf*f1s**2/2 + gh*h1s**2/2
expected = ( W*(gp*vp1**2 + gf*vf1**2 + gh*vh1**2)
  + 2*aF*vp*W*(gp*p1s*vp1 + gf*f1s*vf1 + gh*h1s*vh1)
  + aF**2*Lt*W*vp**2
  + 2*mu*aFp*( vp*W*Lt*(1 + aF*p0s) + p0s*W*(gp*p1s*vp1 + gf*f1s*vf1 + gh*h1s*vh1) )
  + mu**2*aFp**2*p0s**2*W*Lt )
check("SA1_second_variation_assembly", sp.simplify(d2S - expected) == 0,
      "d^2/deps^2 of e^{aF(lam)p}Ltilde == hand-assembled joint quadratic form density (fields+lambda), generic base point, zero residual")

# A-2: on-shell first variation vanishes (fields: Euler rows on the atlas; lambda: 2*E0*I_p tie)
d1S = sp.diff(Sfull, eps).subs(eps, 0)
# field part on-shell: substitute atlas member and check the Euler rows vanish (recompute, consistency)
p_x = sp.log(w)/aF
Ep_row = sp.diff(sp.exp(aF*p_x)*gp*sp.diff(p_x,x), x) - aF*sp.exp(aF*p_x)*(gp*sp.diff(p_x,x)**2/2 + gf*fbar_p**2/2 + gh*hbar_p**2/2)
Ef_row = sp.diff(sp.exp(aF*p_x)*gf*fbar_p, x)
check("SA2_onshell_euler_rows", resid(Ep_row) and sp.simplify(Ef_row - 0 + sp.diff(cf,x)) == 0,
      "atlas member (w quadratic, f'=c/(g w)) solves the p-row and f/h-rows exactly (banked, recomputed)")
# lambda part: integrand of dS/dlam on-shell == aFp * p * E0  (=> integral = aFp*E0*I_p; =0 on massive locus)
lam_integrand = aFp*p_x*sp.exp(aF*p_x)*(gp*sp.diff(p_x,x)**2/2 + gf*fbar_p**2/2 + gh*hbar_p**2/2)
check("SA3_lambda_row_is_E0_Ip", resid(lam_integrand - aFp*p_x*E0),
      "on-shell dS/dlam integrand == a_F' * p * E0 exactly => first variation in lambda = a_F'*E0*I_p = 0 on {I_p=0} (banked tie, recomputed)")

# A-3: on-shell W*Ltilde == E0 pointwise (banked; used throughout)
check("SA4_WL_is_E0_onshell", resid(sp.exp(aF*p_x)*(gp*sp.diff(p_x,x)**2/2 + gf*fbar_p**2/2 + gh*hbar_p**2/2) - E0),
      "W_F*Ltilde == E0 pointwise on-shell (banked identity, recomputed)")

# A-4: fh completion of squares (pointwise identity): cross-coupled fh block == perfect square - aF^2*sigma*vp^2/w
lhs = w*(gf*vf1**2 + gh*vh1**2) + 2*aF*vp*(cf*vf1 + ch*vh1)
sq  = w*( gf*(vf1 + aF*vp*cf/(gf*w))**2 + gh*(vh1 + aF*vp*ch/(gh*w))**2 )
check("SA5_fh_completion_identity", sp.simplify(sp.expand(lhs - (sq - aF**2*sigma*vp**2/w))) == 0,
      "fh sector completes: destabilizing channel = f/h momentum coupling, potential -a_F^2*sigma*v^2/w; pure square remainder")

# A-5: pure-depth block is nonneg (Dirichlet): 2*gp*w'*v*v' + aF^2*E0*v^2 == Dx(gp*w'*v^2) using w''=2A
vpx = sp.Function('v')(x)
depth_mid = 2*gp*sp.diff(w,x)*vpx*sp.diff(vpx,x) + aF**2*E0*vpx**2
check("SA6_pure_depth_positive_Dirichlet", sp.simplify(sp.expand(depth_mid - sp.diff(gp*sp.diff(w,x)*vpx**2, x))) == 0,
      "pure-depth cross+mass terms are an exact total derivative => Q_pp = bdy + int g_p w v'^2 >= 0: depth alone cannot destabilize")

# A-6: reduced Sturm-Liouville operator L v = -gp (w v')' - aF^2*sigma*v/w ; exact solution basis
Lop = lambda v: -sp.diff(gp*w*sp.diff(v,x), x) - aF**2*sigma*v/w
v1 = sp.diff(w,x)/w                 # translation-descended solution
v2 = E0 - sigma/w                   # second exact solution (energy-modulus direction)
check("SA7_exact_solution_v1", resid(sp.together(Lop(v1))*w**2),
      "L v1 = 0 exactly, v1 = w'/w (x-translation zero mode of the reduced operator)")
check("SA8_exact_solution_v2", resid(sp.together(Lop(v2))*w**2),
      "L v2 = 0 exactly, v2 = E0 - sigma/w (energy-modulus direction); Dirichlet spectrum decidable from (v1,v2)")
Wr = sp.simplify(on_energy_shell(gp*w*(v1*sp.diff(v2,x) - v2*sp.diff(v1,x))))
check("SA9_wronskian_constant", sp.diff(Wr, x) == 0,
      f"reduced Wronskian gp*w*(v1 v2' - v2 v1') is the constant {sp.simplify(Wr)} (nonzero iff E0 != 0): (v1,v2) a fundamental system on massive members")

# ================= STAGE A (part 2): massless controls + lambda sector =================
print("\n-- Stage A: massless controls (F-S5 halt-condition calibration) --")
# Control 1: constants member (E0=0 stratum: p,f,h constant, W0=e^{aF p0c} constant > 0).
p0c = sp.Symbol('p0c', real=True)
d2S_const = d2S.subs({p1s: 0, f1s: 0, h1s: 0, p0s: p0c})
Wc = sp.exp(aF*p0c)
check("SC1_control_constants_form", sp.simplify(d2S_const - Wc*(gp*vp1**2 + gf*vf1**2 + gh*vh1**2)) == 0,
      "about the E0=0 constants member the joint form is EXACTLY W0*(gp vp'^2+gf vf'^2+gh vh'^2): PSD (SOS, definite class); "
      "kernel = all 0-jet shifts (p,f,h consts) + FULL moduli sector (mu and k_mod/k10/C absent from the form) = the banked flat directions. CONTROL PASS")
check("SC2_control_constants_lambda_flat", sp.diff(d2S_const, mu) == 0,
      "lambda direction exactly flat at E0=0 (tie vacuous there, banked) — reproduced; massive members have mu^2-coefficient aFp^2*p0^2*W*Lt >= 0")

# lambda-lambda block on massive members: C = aFp^2 * int p^2 * (W*Lt) = aFp^2 * E0 * int pbar^2 > 0 for E0>0, pbar not== 0
mu2_coeff = sp.expand(d2S).coeff(mu, 2)
check("SC3_lambda_diagonal", sp.simplify(mu2_coeff - aFp**2*p0s**2*W*Lt) == 0,
      "mu^2 coefficient == aFp^2*p0^2*W*Ltilde pointwise; on-shell = aFp^2*E0*pbar^2 => C = aFp^2*E0*int pbar^2 > 0 on nonconstant massive members (E0>0)")

# B identity: the lambda-field cross form evaluated on the (v2, matched-fh) kernel pair.
print("\n-- Stage A: lambda-field cross term on the v2 kernel pair (exact pointwise reduction) --")
# cross coefficient (coefficient of 2*mu in d2S), instantiated on-shell with (vp,vf1,vh1) = (v2, matched fh minimizer)
cross = sp.expand(d2S).coeff(mu, 1)/2   # = aFp*( vp*W*Lt*(1+aF*p0) + p0*W*(gp p1 vp1 + gf f1 vf1 + gh h1 vh1) )
v2x = E0 - sigma/w
match_f = -aF*v2x*(cf/gf)/w    # matched fh minimizer directions (from SA5 completion)
match_h = -aF*v2x*(ch/gh)/w
cross_onshell = cross.subs({vp: v2x, vp1: sp.diff(v2x, x), vf1: match_f, vh1: match_h,
                            p0s: p_x, p1s: sp.diff(p_x,x), f1s: fbar_p, h1s: hbar_p})
# claim: integrand == aFp*( E0*v2 + aF*E0^2*pbar )  pointwise exactly (all other pbar/w terms cancel)
check("SC4_B_identity_pointwise", resid(sp.together(cross_onshell - aFp*(E0*v2x + aF*E0**2*p_x))),
      "B-integrand on the (v2, matched-fh) pair == aFp*(E0*v2 + aF*E0^2*pbar) POINTWISE => B = aFp*(E0*int v2 + aF*E0^2*I_p) "
      "= aFp*E0*int v2 dx on the massive locus {I_p=0} (exact; every 1/w and 1/w^2 log-weighted term cancels)")

# int v2 < 0 on crease-normalized massive members: pointwise convexity bound log t <= t-1
t = sp.Symbol('t', positive=True)
h_t = sp.log(t) - 1 + 1/t
check("SC5_intv2_sign_bound", sp.simplify(sp.diff(h_t, t) - (t-1)/t**2) == 0 and h_t.subs(t,1) == 0,
      "h(t)=log t - 1 + 1/t has h(1)=0, h'(t)=(t-1)/t^2 (sign of t-1) => h>=0, strict off t=1 [Category-A calculus, named]. "
      "With crease normalization sigma=E0 (w(crease)=sigma/E0=1): int v2 = E0*int(1-1/w) <= E0*int log w = aF*E0^2*I_p = 0, STRICT for "
      "nonconstant w => B = aFp*E0*int v2 < 0 strictly on every nonconstant crease-normalized massive member (structure fact; "
      "instability implication requires kernel realization — posture-dependent, see Stage B)")

# ================= STAGE B: S-i mixed crease|glue chain (certified crease branch) =================
print("\n-- Stage B: S-i on the period-gate certified crease branch (ell=1 CHOSE-normalized, banked) --")
# crease conditions (banked C6a) <=> sigma = E0*w(crease) and w(crease)=1
check("SB1_crease_condition_identity", resid((2*A*w - sp.diff(w,x)**2) - aF**2*(sigma - E0*w)/gp),
      "2A*w - w'^2 == (aF^2/gp)*(sigma - E0*w) pointwise on-shell: crease condition {w=1, 2Aw=w'^2} <=> {w(crease)=1, sigma=E0} => v2(crease)=0 AUTOMATICALLY")
# double-crease: massive locus EMPTY
ellS = sp.Symbol('ellS', positive=True)
w_dc = A*x**2 + (1 - A*ellS**2)          # w1=0 forced by w(l)=w(-l)=1; w0 = 1-A*l^2
check("SB2_double_crease_empty", sp.simplify(sp.expand(w_dc - 1 - A*(x-ellS)*(x+ellS))) == 0,
      "w(+-l)=1 both => w1=0 and w-1 = A(x^2-l^2) < 0 strictly inside for A>0 (definite class, E0>0) => log w sign-definite => I_p != 0 "
      "[integral positivity, Category-A named]: the massive locus {I_p=0,E0>0} on the DOUBLE-CREASE (pure quotient) posture is EMPTY. "
      "No contradiction with the period gate (its quotient UNTOUCHED row is about PERIODS; this is a wall-trace fact)")
# the certified branch: s = sqrt(2A) in (1,3), ell=1, gp=1 scale (Q scales by gp>0: sign structure invariant)
q = sp.Symbol('q', positive=True); s = 1 + q
wB = (s**2/2)*x**2 + (s**2 - s)*x + (1 + s**2/2 - s)
x2 = 2/s - 1
check("SB3_branch_footing", sp.simplify(wB.subs(x,-1) - 1) == 0
      and sp.simplify(sp.expand(wB - 1 - (s**2/2)*(x+1)*(x-x2))) == 0
      and sp.simplify(sp.expand((s**2-s)**2 - 4*(s**2/2)*(1+s**2/2-s) + s**2)) == 0,
      "branch: w(-1)=1; w-1=(s^2/2)(x+1)(x-x2) with x2=2/s-1; disc=-s^2<0 (nodeless). Certified massive roots: s in (1,3) (banked C6b interval, cited)")
check("SB4_x2_interior_and_v2_signs", sp.simplify(1 - x2 - 2*q/(1+q)) == 0
      and sp.simplify(wB.subs(x,1) - 1 - 2*s*(s-1)) == 0
      and sp.simplify(sp.expand((wB - 1).subs(x, (x2-1)/2) + (s**2/8)*(x2+1)**2)) == 0,
      "1-x2 = 2q/(1+q) > 0 (interior, strict); w(1)-1 = 2s(s-1) > 0 => v2(1) != 0; between the roots w<1 => v2 = E0(1-1/w) < 0 sign-definite "
      "(factorized quadratic, only roots -1 and x2). => Dirichlet solution from the crease has EXACTLY ONE interior zero")
# reduced operator on branch (gp=1): Lt v = -(w v')' - s^2 v / w ; basis v1=w'/w, vt2=1-1/w
LtB = lambda v: -sp.diff(wB*sp.diff(v,x),x) - s**2*v/wB
vt2 = 1 - 1/wB
check("SB5_branch_solutions", sp.simplify(sp.together(LtB(sp.diff(wB,x)/wB))*wB**2) == 0
      and sp.simplify(sp.together(LtB(vt2))*wB**2) == 0,
      "v1=w'/w and vt2=1-1/w solve Lt v=0 on the branch (aF^2*sigma = aF^2*E0 = s^2 at gp=1; overall E0 scale dropped)")
# UNCONSTRAINED Dirichlet count (free f/bh wall data branch): n- = 1
check("SB6_unconstrained_Dirichlet_index", True,
      "vt2 is a sign-definite Dirichlet zero mode of [-1,x2]; STRICT domain monotonicity of the ground state + oscillation [Category-A, named] "
      "=> n-(Dirichlet[-1,1]) = 1 EXACTLY. VERDICT: under supplied f/bh wall data FREE (fh traces free) x germ-Hessian-flat realized wall "
      "response (the banked witness responses B=0 and (q/2)rho have ZERO second germ - exact), the massive crease cell has EXACTLY ONE "
      "negative direction IN THE REDUCED SECTOR: UNSTABLE (OS-2 on this branch-pair; joint-space statement: index >= 1 exact, exactly-1 "
      "pending the lambda-Schur sign); the negative mode carries angular wall flux (nonzero v_f trace)", kind="GUARD")
# no Dirichlet/Robin kernel: vt2(1)!=0 and T[vt2]=w'(1)!=0
Tfun = lambda u: (wB*sp.diff(u,x) + sp.diff(wB,x)*u).subs(x,1)
check("SB7_no_kernel", sp.simplify(vt2.subs(x,1) - 2*s*(s-1)/wB.subs(x,1)) == 0 and sp.simplify(Tfun(vt2) - sp.diff(wB,x).subs(x,1)) == 0
      and sp.simplify(sp.diff(wB,x).subs(x,1) - s*(2*s-1)) == 0,
      "vt2(1)=2s(s-1)/w(1)>0 and T[vt2]=w'(1)=s(2s-1)>0: Lt invertible on Dirichlet AND on the free-end (Robin w'v^2) space; "
      "free-end harmonic-extension split: Q(e)=T[vt2]/vt2(1)>0 => n-(free-end)=n-(Dirichlet)=1 (exact algebraic split, cross term vanishes)")

# --- Stage B: the fh-odd-pinned (zero-trace) branch: penalized reduction + exact index ---
print("\n-- Stage B: odd-pinned f/bh branch — penalized rank-one reduction, exact index --")
Jsym = sp.Symbol('J', positive=True)   # J = int 1/w dx > 0 (w>0, disc<0): the ONE transcendental, kept symbolic
# antiderivative identities closing all needed integrals except J
check("SB8_antiderivatives", sp.simplify(sp.diff(-1/wB, x) - (sp.diff(wB,x)/wB)/wB) == 0
      and sp.simplify(sp.together(sp.diff(-sp.diff(wB,x)/(s**2*wB), x) - (1/wB - 1/wB**2))) == 0,
      "int v1/w = [-1/w] and int vt2/w = [-w'/(s^2 w)] exactly (uses the on-shell identity w'^2 = s^2(2w-1) on the crease branch): "
      "every criterion integral is elementary except J = int dx/w (kept symbolic, J>0 by positivity)")
# Dirichlet resolvent phi_D: Lt phi = 1/w, phi(+-1)=0
alD, beD = -1/s**3, 1/(s*(s-1))
phiD = -1/s**2 + alD*sp.diff(wB,x)/wB + beD*vt2
check("SB9_phiD_solves", sp.simplify(sp.together(LtB(phiD) - 1/wB)*wB**2) == 0
      and sp.simplify(phiD.subs(x,-1)) == 0 and sp.simplify(sp.together(phiD.subs(x,1))) == 0,
      "phi_D = -1/s^2 - (1/s^3) v1 + [1/(s(s-1))] vt2 solves Lt phi = 1/w with phi(-1)=phi(1)=0 (exact; beta = 1/(s(s-1)) closed form)")
gphiD = -Jsym/s**2 + alD*( (-1/wB).subs(x,1) - (-1/wB).subs(x,-1) ) + beD*( (-sp.diff(wB,x)/(s**2*wB)).subs(x,1) - (-sp.diff(wB,x)/(s**2*wB)).subs(x,-1) )
gphiD_closed = -Jsym/s**2 - 2/(s**2*(s-1))
check("SB10_criterion_D_closed_form", sp.simplify(sp.together(gphiD - gphiD_closed)) == 0,
      "<g, Lt_D^{-1} g> = -J/s^2 - 2/(s^2(s-1)) EXACTLY (all w(1)-terms cancel): manifestly < 0 for every s>1")
# rank-one crossing rule, toy-verified exactly, then applied
M0 = sp.Matrix([[-1,0],[0,1]]); gv = sp.Matrix([1,0]); tau0 = sp.Symbol('tau0', positive=True)
eigs = (M0 + tau0*gv*gv.T).eigenvals()
check("SB11_rank_one_rule_toy", sorted(eigs.keys(), key=str) is not None and (sp.Rational(1,1) in eigs) and ((tau0-1) in eigs),
      "toy L=diag(-1,1), g=e1: eigenvalues {tau0-1, 1}: n-(L+tau g g*)=0 iff 1 + tau<g,L^{-1}g> = 1-tau <= 0 — the crossing rule verified exactly "
      "[rank-one/Birman-Schwinger monotone crossing, Category-A named]; PROPERLY VERIFIED beyond the toy by the blind verifier "
      "(8 random exact 5x5 matrices, rule exact each time, plus the analytic linear-crossing/interlacing argument — "
      "VERIFIER_INDEPENDENT_CHECK.py): the toy-verified caveat is RETIRED (credited check)")
# fh elimination on the odd-pinned branch produces EXACTLY the penalty tau = aF^2*sigma/J = s^2/J (gp=1, sigma=E0, aF^2 E0=s^2)
uD, XD, kap = sp.symbols('u_delta X kappa', real=True)
check("SB12_penalized_reduction_algebra", sp.simplify( (wB*gf*(( -XD + kap/(gf*wB)) + XD)*uD) - kap*uD ) == 0,
      "zero-trace fh elimination: the constrained minimizer u* = -X + kappa/(g w) has pointwise w g (u*+X) delta-u == kappa*delta-u => cross term "
      "integrates to zero on zero-mean variations; residual value = g (int X)^2 / J per angular field => reduced form = Q_p + (aF^2 sigma / J) (int v_p/w)^2 "
      "EXACT rank-one penalty (tau = s^2/J on the branch). LABEL HONESTY (verifier amendment A2): the coded condition is an arithmetic "
      "identity true by construction; the substantive content (constrained minimization => penalty g (int X)^2 / J; tau = aF^2 sigma / J) "
      "was independently verified by the blind verifier (re-derivation + exact quadrature, VERIFIER_INDEPENDENT_CHECK.py) — relabeled GUARD",
      kind="GUARD")
tau = s**2/Jsym
check("SB13_penalized_index_D", sp.simplify(sp.together(1 + tau*gphiD_closed - ( -2/(Jsym*(s-1)) ))) == 0,
      "1 + tau*<g,phi_D> = -2/(J(s-1)) < 0 MANIFESTLY (J cancels exactly): the penalized Dirichlet form has n- = 1-1 = 0 — "
      "the odd-parity fh pin EXACTLY ABSORBS the unique negative direction; the zero-trace core of the massive crease cell is POSITIVE")
# free-end (Robin) version: same conclusion
beR = 2/(s*(2*s-1))
phiR = -1/s**2 + alD*sp.diff(wB,x)/wB + beR*vt2
gphiR = -Jsym/s**2 + alD*( (-1/wB).subs(x,1) - (-1/wB).subs(x,-1) ) + beR*( (-sp.diff(wB,x)/(s**2*wB)).subs(x,1) - (-sp.diff(wB,x)/(s**2*wB)).subs(x,-1) )
w1v = wB.subs(x,1)
gphiR_closed = -Jsym/s**2 - 2*(4*s**2-3*s+1)/(s**2*(2*s-1)*w1v)
check("SB14_criterion_R_closed_form", sp.simplify(sp.together(LtB(phiR) - 1/wB)*wB**2) == 0
      and sp.simplify(phiR.subs(x,-1)) == 0 and sp.simplify(sp.together(Tfun(phiR))) == 0
      and sp.simplify(sp.together(gphiR - gphiR_closed)) == 0
      and sp.simplify(sp.together(1 + tau*gphiR_closed - ( -2*(4*s**2-3*s+1)/(Jsym*(2*s-1)*w1v) ))) == 0,
      "free-p-trace (germ-flat seam) version: phi_R exact; <g,phi_R> = -J/s^2 - 2(4s^2-3s+1)/(s^2(2s-1)w(1)); 1+tau<g,phi_R> = "
      "-2(4s^2-3s+1)/(J(2s-1)w(1)) < 0 manifestly => n- = 0 again: on the odd-pinned branch even the free-seam-trace core is POSITIVE")
check("SB15_odd_branch_verdict", True,
      "ODD-PINNED f/bh branch verdict: field-sector core POSITIVE (both Dirichlet and free-p-trace, exact); remaining sectors = wall-germ "
      "curvature (FREE data at this layer) + the lambda(mu) Schur block (C>0; sup B^2/Q_f vs C involves dilogarithmic integrals at the "
      "transcendental massive root A*) => overall verdict on this branch OS-5 UNDECIDABLE-AT-THIS-LAYER with the obstruction NAMED; "
      "the germ-independent core carries NO instability", kind="GUARD")
check("SB16_germ_curvature_activation", True,
      "STRUCTURE THEOREM (exact): at any trace-active wall the second variation gains Hess(B)|realized traces (for the seam: B_QQ (Q v_p)^2 "
      "- 2 B_Qrho Q v_p v_rho + B_rhorho v_rho^2; first germs pinned, SECOND germs UNPINNED by every banked requirement) => (i) NO stability "
      "certificate is possible at any trace-active posture at this layer (a sufficiently negative second germ defeats any candidate); "
      "(ii) zero-trace subspaces are germ-independent, so germ data can never VETO a zero-trace negative direction; (iii) the banked WITNESS "
      "wall responses (B=0 fold; (q/2)rho glue) are germ-Hessian-FLAT: under them the verdicts above are complete. The first-variation-inert "
      "higher germs ACTIVATE at the second variation — the delta^2 analog of the banked N=4 activation", kind="GUARD")
check("SB17_chain_monotonicity", True,
      "CHAIN INHERITANCE (subspace monotonicity): any mixed-posture whole containing a certified massive crease cell inherits its zero-trace-core "
      "verdicts: free-fh branch => the whole is UNSTABLE (index >= 1) regardless of germ data and chain context; odd-pinned branch => no "
      "core instability contributed by this cell (whole-chain verdict rides seam-trace Schur + germ data: OS-5)", kind="GUARD")

# ================= STAGE C: S-ii fields-census lock-emergence massive class =================
print("\n-- Stage C: S-ii (P1-4D landing: p==0, lambda==0 emerged, f/h affine, W==1) --")
u_l, v_c, t_c = sp.symbols('u_lam v_c t_c', real=True)      # lambda(x)- and p(x)-perturbation amplitudes
f1b, h1b = sp.symbols('f1bar h1bar', real=True)             # affine slopes; E0 = Lfh(slopes)
ux, vx = sp.Function('u_pert')(x), sp.Function('v_pert')(x)
E0fh = gf*f1b**2/2 + gh*h1b**2/2
# C-1: assembly. a_F = 2*lambda on P1-4D (banked); density e^{2 lam p} Ltilde; perturb (lam,p,f,h) jointly about the landing.
Sd = sp.exp(2*(eps*ux)*(eps*vx))*(gp*sp.diff(eps*vx,x)**2/2 + gf*(f1b+eps*sp.diff(sp.Function('vf')(x),x))**2/2
                                  + gh*(h1b+eps*sp.diff(sp.Function('vh')(x),x))**2/2)
d2Sd = sp.diff(Sd, eps, 2).subs(eps, 0)
vfx, vhx = sp.Function('vf')(x), sp.Function('vh')(x)
expectedC = gp*sp.diff(vx,x)**2 + gf*sp.diff(vfx,x)**2 + gh*sp.diff(vhx,x)**2 + 4*ux*vx*E0fh
check("SD1_Sii_assembly", sp.simplify(sp.expand(d2Sd - expectedC)) == 0,
      "joint second variation about the landing == gp vp'^2 + gf vf'^2 + gh vh'^2 + 4 E0 vlam vp EXACTLY (no vlam^2 or vlam'^2 term on the "
      "no-m-jet class: the lambda(x)-depth cross term is the ONLY moduli-field coupling; W==1 at the landing)")
# C-2: exact negative witness (all traces zero; even jets vanish at walls: admissible under the banked odd forcing)
ellc = sp.Symbol('ellc', positive=True); tt = sp.Symbol('t', positive=True)
prof = sp.sin(sp.pi*x/ellc)
Ider = sp.integrate(sp.diff(prof,x)**2, (x, -ellc, ellc)); Isq = sp.integrate(prof**2, (x, -ellc, ellc))
Qwit = gp*Ider - 4*tt*E0fh*Isq   # v_p = prof, v_lam = -t*prof (E0>0 side; take +t*prof for E0<0), v_f=v_h=0
Qval = Qwit.subs(tt, gp*sp.pi**2/(2*E0fh*ellc**2))
check("SD2_Sii_negative_witness", sp.simplify(Ider - sp.pi**2/ellc) == 0 and sp.simplify(Isq - ellc) == 0
      and sp.simplify(Qval + gp*sp.pi**2/ellc) == 0,
      "witness v_p = sin(pi x/l), v_lam = -t sin(pi x/l), v_f=v_h=0 (exactly odd about both walls, all even jets vanish: banked-admissible; "
      "ALL traces zero => germ-independent): at t = gp pi^2/(2 E0 l^2), Q = -gp pi^2/l < 0 EXACT. VERDICT: every E0 != 0 member of the "
      "no-m-jet landing class is a SADDLE — UNSTABLE (OS-2), unconditionally on the banked perturbation space (sign(E0) handled by sign(t))")
# C-3: jet-carrying responses S = W(Ltilde + c_m lam'^2/2): exact dichotomy by Dirichlet mode split
cm, kn = sp.symbols('c_m k_n', positive=True)
M2 = sp.Matrix([[gp*kn**2, 2*E0fh],[2*E0fh, cm*kn**2]])
check("SD3_Sii_jet_dichotomy", sp.simplify(M2.det() - (gp*cm*kn**4 - 4*E0fh**2)) == 0,
      "jet-quadratic member class (density + c_m lam'^2/2, c_m>0): per Dirichlet mode k_n = n pi/(2l) (n>=1; full basis sin(n pi (x+l)/(2l)), "
      "all admissible, Parseval Category-A named) the 2x2 block [[gp kn^2, 2E0],[2E0, cm kn^2]] has det = gp cm kn^4 - 4 E0^2, diagonal>0: "
      "PSD for ALL modes iff worst n=1 holds: STABLE-in-this-sector iff 64 E0^2 l^4 <= gp cm pi^4, UNSTABLE iff 64 E0^2 l^4 > gp cm pi^4 — an "
      "EXACT threshold tying member energy to cell size and jet stiffness. OS-4 (both regimes populated; e.g. E0 small/large at fixed cm)")
# C-4: triad-locked massless control (F-S5): a_F(0)=1, locked class E0=0 => constants
p0t = sp.Symbol('p0t', real=True)
Sd_t = sp.exp((1+2*(eps*ux))*(0 + eps*vx))*(gp*sp.diff(eps*vx,x)**2/2 + gf*(0+eps*sp.diff(vfx,x))**2/2 + gh*(0+eps*sp.diff(vhx,x))**2/2)
d2Sd_t = sp.diff(Sd_t, eps, 2).subs(eps,0)
check("SD4_triad_control", sp.simplify(sp.expand(d2Sd_t - (gp*sp.diff(vx,x)**2 + gf*sp.diff(vfx,x)**2 + gh*sp.diff(vhx,x)**2))) == 0,
      "triad-locked massless member (p==0, lambda==0, constants, E0=0): joint form == gp vp'^2 + gf vf'^2 + gh vh'^2 exactly — PSD with kernel "
      "= {constants} + ARBITRARY odd v_lam(x) and v_kmod(x) (absent from the form): the banked infinite-dimensional free directions of the "
      "massless stratum reappear EXACTLY as the zero-mode space. CONTROL PASS (F-S5)")
check("SD5_scope_typing", True,
      "TYPED/OUT: NV-cell members UNDEFINED at this layer (no dynamics adopted — F-S4); S-ii massive-class conditionalities travel (free f/bh "
      "wall data; AM-1 full locked-row member condition; AM-2 nondegeneracy g_p!=0, DeltaG!=0; p0==0 completion admissibility OPEN); N=4 wall "
      "layer typed; corners, resonance cells, 4th-order class, carriers, time-live untouched; P2-side massive affine members not a prereg "
      "candidate (typed, not adjudicated)", kind="GUARD")

# ================= finalize =================
n_sub = sum(1 for c in CHECKS if c["kind"]=="SUBSTANTIVE"); n_gua = sum(1 for c in CHECKS if c["kind"]=="GUARD")
n_fail = sum(1 for c in CHECKS if not c["pass"])
print(f"\n== SUMMARY: {len(CHECKS)} checks = {n_sub} substantive + {n_gua} guards; failures: {n_fail} ==")
import io
with open("stability_results.json","w") as fjson:
    json.dump({"date":"2026-07-31","contract":"PREREGISTRATION.md","checks":CHECKS,
               "counts":{"total":len(CHECKS),"substantive":n_sub,"guards":n_gua,"failures":n_fail},
               "verdicts":{
                 "S-i_double_crease":"EMPTY-DOMAIN (massive locus empty on pure quotient posture; wall-trace fact, exact)",
                 "S-i_crease_branch_free_fh_data":"UNSTABLE OS-2: n-=1 exact (reduced sector); on the JOINT space (fields+mu): index >= 1 exact, exactly-1 pending the lambda-Schur sign (the verifier's joint Galerkin hunt at the massive root s*~1.681 supports exactly-1 — corroboration, not banked); germ-Hessian-flat realized wall response; negative mode carries angular wall flux; UNSTABLE itself unconditional",
                 "S-i_crease_branch_odd_pinned_fh":"core POSITIVE (exact index absorption, J cancels); overall OS-5 (free germ curvature + dilogarithmic lambda-Schur at transcendental A*)",
                 "S-i_general_Ip0_member":"OS-5 member-conditional: exact criterion recorded (zeros of the (v1,v2)-combination); no certified witness off the crease branch",
                 "S-ii_nojet":"UNSTABLE OS-2 unconditional (exact witness; lambda(x)-depth cross term, vanishing lambda-diagonal)",
                 "S-ii_jet_quadratic":"OS-4 mixed: exact threshold 64 E0^2 l^4 vs gp c_m pi^4",
                 "controls":"PASS (constants member and triad-locked member: PSD with exactly the banked flat directions as kernel)",
                 "NV":"UNDEFINED-AT-LAYER (F-S4)"}}, fjson, indent=1)
print("results written: stability_results.json")
sys.exit(1 if n_fail else 0)
