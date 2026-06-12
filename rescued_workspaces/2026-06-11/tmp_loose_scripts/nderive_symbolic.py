"""
Native derivation attempt: n = W_ff via gluing-balance / canonical-structure.
Symbolic leg. All per-solid-angle, radial sector. Conventions:
  L_C1 = (1/4)[y^2 f'^2 + |grad_Omega f|^2 / f],  f = e^{-2 phi}
  collar background f0 = y^{-q}, q = 1/3
  completion family L_src = c_n(y) f^n,  c_n = J f0^{1-n}/n,  J = -s y^{-q},
  s = q(1-q)/2.   (n=0 member: L_src0 = J f0 ln(f/f0), the phi-linear slot.)
EL sign convention: delta S / delta f = 0 with
  delta(1/4 y^2 f'^2)/delta f = -(1/2)(y^2 f')'
  delta(c_n f^n)/delta f      = n c_n f^{n-1}
so EOM:  (1/2)(y^2 f')' = n c_n f^{n-1}   [check S1 fixes signs].
"""
import sympy as sp

y, q, n, lam, w, eps, beta = sp.symbols('y q n lambda w epsilon beta', positive=True)
nn = sp.Symbol('n')  # allow negative n where needed
s = q*(1-q)/2
f0 = y**(-q)
J = -s*y**(-q)

PASS = 0; FAIL = 0
def check(name, expr_zero):
    global PASS, FAIL
    ok = sp.simplify(expr_zero) == 0
    if not ok:
        ok = sp.simplify(sp.expand(sp.powsimp(sp.expand(expr_zero), force=True))) == 0
    print(("PASS" if ok else "FAIL"), name)
    if ok: PASS += 1
    else: FAIL += 1; print("   residual:", sp.simplify(expr_zero))

f = sp.Function('f')
c_n = J*f0**(1-nn)/nn

# ---------------- S1: criticality of f0 for the total sourced action, all n,q
EL_C1_bg = -sp.Rational(1,2)*sp.diff(y**2*sp.diff(f0,y), y)
EL_src_bg = nn*c_n*f0**(nn-1)
check("S1 criticality: EL_C1[f0] + EL_src[f0] = 0 (all n, q)",
      sp.powsimp(EL_C1_bg + EL_src_bg, force=True))

# n=0 member: L_src0 = J f0 ln(f/f0); dL/df = J f0 / f -> J at f0
g = sp.Symbol('g', positive=True)
L0mem = J*f0*sp.log(g/f0)
check("S1b n=0 member first jet = J at f0", sp.diff(L0mem, g).subs(g, f0) - J)

# ---------------- S2: second jet of source = constant mass; mu = (1-n)q(1-q)
W_ff = sp.powsimp(nn*(nn-1)*c_n*f0**(nn-2), force=True)   # d^2 L_src/df^2 at f0
check("S2 W_ff = (1-n)s exactly (constant in y)", sp.simplify(W_ff - (1-nn)*s))
# perturbation eq: (y^2 u')' = 2*W_ff*... : -(1/2)(y^2 u')' + W_ff u + angular = 0
mu = sp.simplify(2*W_ff)
check("S2b mu = (1-n)q(1-q)", mu - (1-nn)*q*(1-q))
check("S2c n=0 member second jet -> mu = 2s", 2*sp.diff(L0mem, g, 2).subs(g, f0) - 2*s)

# ---------------- S3: indicial -> nu(n) = sqrt(17-8n) at q=1/3
a = sp.Symbol('a')
mu13 = mu.subs(q, sp.Rational(1,3))
roots = sp.solve(sp.Eq(a*(a+1), mu13), a)
nu_from_mu = sp.sqrt(1 + 4*mu13)/sp.Rational(1,3)
check("S3 nu = sqrt(17-8n) at q=1/3", sp.simplify(nu_from_mu - sp.sqrt(17-8*nn)))

# ---------------- S4: exact background radial conservation identity
# h_tot = (1/4) y^2 f'^2 + c_n f^n  evaluated on-shell;  claim:
# d/dy [ (1/4) y^2 f0'^2 + c_n f0^n ] = -(1/2) y f0'^2 + c_n'(y) f0^n
LHS = sp.diff(sp.Rational(1,4)*y**2*sp.diff(f0,y)**2 + c_n*f0**nn, y)
RHS = -sp.Rational(1,2)*y*sp.diff(f0,y)**2 + sp.diff(c_n, y)*f0**nn
check("S4 background conservation identity (exact, all n,q)",
      sp.powsimp(sp.expand(LHS - RHS), force=True))

# Generic-field version (uses EOM): for any f solving (1/2)(y^2 f')' = n c_n f^{n-1}:
# d/dy[ (1/4) y^2 f'^2 + c_n f^n ] = -(1/2) y f'^2 + c_n' f^n
F = sp.Function('F')(y)
lhs_gen = sp.diff(sp.Rational(1,4)*y**2*sp.diff(F,y)**2 + c_n*F**nn, y)
rhs_gen = -sp.Rational(1,2)*y*sp.diff(F,y)**2 + sp.diff(c_n,y)*F**nn
diff_gen = sp.expand(lhs_gen - rhs_gen)
# substitute EOM: F'' = (2 n c_n F^{n-1} - 2 y F')/y^2
eom_Fpp = (2*nn*c_n*F**(nn-1) - 2*y*sp.diff(F,y))/y**2
diff_gen = diff_gen.subs(sp.diff(F,y,2), eom_Fpp)
check("S4b generic on-shell conservation identity", sp.simplify(diff_gen))

# ---------------- S5: exchange term on background is FIRST-JET (n-independent)
exchange = sp.powsimp(nn*c_n*f0**(nn-1)*sp.diff(f0,y), force=True)  # = J f0'
check("S5 exchange on background = J*f0' = s q y^{-2q-1} (n-free)",
      sp.simplify(exchange - s*q*y**(-2*q-1)))

# ---------------- S6: would-be closure A (total leak = 0 on background)
leak = sp.powsimp(-sp.Rational(1,2)*y*sp.diff(f0,y)**2 + sp.diff(c_n,y)*f0**nn, force=True)
leak_coeff = sp.simplify(leak / y**(-2*q-1))
sols = sp.solve(sp.Eq(leak_coeff, 0), nn)
print("S6 closure-A solutions n =", sols)
nA = sols[0]
check("S6 closure-A: n = 2(1-q)/(2-q)", sp.simplify(nA - 2*(1-q)/(2-q)))
print("   at q=1/3: n =", sp.nsimplify(nA.subs(q, sp.Rational(1,3))),
      " -> nu^2 =", sp.nsimplify(17 - 8*nA.subs(q, sp.Rational(1,3))))

# ---------------- S7: would-be closure B (source's own bookkeeping: c_n' f^n = 0)
srcleak = sp.powsimp(sp.diff(c_n, y)*f0**nn, force=True)
solsB = sp.solve(sp.Eq(sp.simplify(srcleak*y**(2*q+1)), 0), nn)
print("S7 closure-B solutions n =", solsB, " (q != 0)  -> nu^2 =", [17-8*v for v in solsB])

# ---------------- S8: additive-normalization freedom annihilates both closures
# adding b(y) (f-independent) to L_src changes NO jet but shifts every
# energy-density bookkeeping demand by b'(y). Exhibit b for arbitrary target n*:
bcoef = sp.Symbol('b0')
b = bcoef*y**(-2*q)
cond = sp.simplify((leak_coeff + sp.diff(b, y)/y**(-2*q-1)))
bsol = sp.solve(sp.Eq(cond, 0), bcoef)
print("S8 b0(n,q) making closure-A hold for ANY n:", sp.simplify(bsol[0]))
check("S8 existence: residual zero after substitution",
      sp.simplify(cond.subs(bcoef, bsol[0])))

# ---------------- S9: second-order flux identity; mu drops from the leak
u = sp.Function('u')(y)
muS = sp.Symbol('mu')
h2 = sp.Rational(1,2)*y**2*sp.diff(u,y)**2 - sp.Rational(1,2)*(lam*y**q + muS)*u**2
dh2 = sp.diff(h2, y)
eom_upp = ((lam*y**q + muS)*u - 2*y*sp.diff(u,y))/y**2   # from (y^2 u')' = (lam y^q + mu) u
dh2 = sp.expand(dh2.subs(sp.diff(u,y,2), eom_upp))
target = -y*sp.diff(u,y)**2 - sp.Rational(1,2)*q*lam*y**(q-1)*u**2
check("S9 d h2/dy = -y u'^2 - (q/2) lam y^{q-1} u^2  (mu-FREE leak)",
      sp.simplify(dh2 - target))

# ---------------- S9b: dilation current; mu enters only via slot-covariant companions
J_D = y*h2 - w*u*(y**2*sp.diff(u,y))
dJD = sp.expand(sp.diff(J_D, y).subs(sp.diff(u,y,2), eom_upp))
targetD = -(sp.Rational(1,2)+w)*y**2*sp.diff(u,y)**2 \
          - (sp.Rational(1,2)+w)*(lam*y**q + muS)*u**2 - sp.Rational(1,2)*q*lam*y**q*u**2
check("S9b dilation anomaly = -(1/2+w)[y^2 u'^2 + (lam y^q+mu)u^2] - (q/2) lam y^q u^2",
      sp.simplify(dJD - targetD))
# at w = -1/2 the mu term drops entirely:
check("S9c w=-1/2: anomaly = -(q/2) lam y^q u^2 (mu-free)",
      sp.simplify(dJD.subs(w, -sp.Rational(1,2)) + sp.Rational(1,2)*q*lam*y**q*u**2))

# ---------------- S10: bilinear concomitant is principal-symbol-only (mu-blind)
u1, u2 = sp.Function('u1')(y), sp.Function('u2')(y)
B = y**2*(sp.diff(u1,y)*u2 - u1*sp.diff(u2,y))
dB = sp.diff(B, y)
e1 = ((lam*y**q + muS)*u1 - 2*y*sp.diff(u1,y))/y**2
e2 = ((lam*y**q + muS)*u2 - 2*y*sp.diff(u2,y))/y**2
dB = dB.subs({sp.diff(u1,y,2): e1, sp.diff(u2,y,2): e2})
check("S10 concomitant conserved for all mu (symplectic current mu-blind)", sp.simplify(dB))
# interface jump: u continuous, Delta p = -W u with symmetric (scalar) W:
W = sp.Symbol('W'); uw, p1m, p2m = sp.symbols('u_w p1m p2m')
# B^+ - B^- with p_i^+ = p_i^- - W u_i(y_w), u_i continuous (here u1(y_w)=u2(y_w)=uw
# is NOT general; use general boundary values):
u1w, u2w, p1, p2 = sp.symbols('u1w u2w p1 p2')
Bminus = 2*(p1*u2w - u1w*p2)   # p = (1/2) y^2 u' -> y^2 u' = 2p
Bplus  = 2*((p1 - W*u1w)*u2w - u1w*(p2 - W*u2w))
check("S10b symplectic form preserved across interface for ANY W (any n)",
      sp.expand(Bplus - Bminus))

# ---------------- S11: slot second-jet transformation law (the connection statement)
# source potential V(f) = c_n f^n; slot g with f = F(g):
# W_gg = F'^2 V_ff + F'' V_f.  At background, V_f = J (slot-invariant first jet);
# the SECOND jet is connection-dependent: choosing the slot in which the source
# is "bare" (W=0) IS choosing n:  n_bare(F) = 1 - f0 F''/F'^2.
fv = sp.Symbol('f', positive=True)
V = c_n*fv**nn
V_f = sp.diff(V, fv); V_ff = sp.diff(V, fv, 2)
phi = sp.Symbol('phi')
Fphi = sp.exp(-2*phi)
W_phiphi = (sp.diff(Fphi,phi)**2*V_ff + sp.diff(Fphi,phi,2)*V_f).subs(fv, f0)
W_phiphi = sp.powsimp(W_phiphi.subs(Fphi, f0), force=True)
check("S11 W_phiphi at background = 4 n J f0  (vanishes iff n=0)",
      sp.simplify(W_phiphi - 4*nn*J*f0))
W_ff_bg = sp.powsimp(V_ff.subs(fv, f0), force=True)
check("S11b W_ff at background = (n-1) J / f0  (vanishes iff n=1)",
      sp.simplify(W_ff_bg - (nn-1)*J/f0))
# general slot bareness condition:
Fg = sp.Function('Fg')
gsym = sp.Symbol('g')
n_bare = sp.solve(sp.Eq(sp.Derivative(Fg(gsym),gsym)**2*(nn-1)*J/f0
                        + sp.Derivative(Fg(gsym),gsym,2)*J, 0), nn)[0]
print("S11c bareness slot law: n_bare = ", sp.simplify(n_bare),
      "  [= 1 - f0 F''/F'^2 ; F=id -> 1, F=e^{-2phi} -> 0]")
check("S11c f-slot: n_bare(F=id) = 1",
      n_bare.subs({sp.Derivative(Fg(gsym),gsym,2): 0, sp.Derivative(Fg(gsym),gsym): 1}) - 1)
check("S11d phi-slot: n_bare(F=e^{-2phi}) = 0",
      sp.simplify(n_bare.subs({sp.Derivative(Fg(gsym),gsym,2): 4*f0,
                               sp.Derivative(Fg(gsym),gsym): -2*f0})))

# ---------------- S12: fork-collapse anchor recheck (banked; cheap re-verification)
# jet2_phi[a] - jet2_f[-2 f0 a] = d/dy(-q y^{1-2q} a^2)
aa = sp.Function('a')(y)
# f-slot second jet density (radial), u = delta f:
def jet2_f(uu):
    kin = sp.Rational(1,4)*y**2*sp.diff(uu,y)**2
    massC1 = 0
    src = sp.Rational(1,2)*(1-nn)*s*uu**2   # W_ff/2 u^2, W_ff = (1-n)s... times? W_ff=(1-n)s
    return kin + src
# phi-slot: f = f0 e^{-2 a} expanded to second order; full sourced action second jet
ph = sp.Symbol('a0')
ffull = f0*sp.exp(-2*aa)
Lfull = sp.Rational(1,4)*y**2*sp.diff(ffull,y)**2 + c_n*ffull**nn
t = sp.Symbol('t')
Lt = Lfull.subs(aa, t*aa)
jet2_phi_density = sp.expand(sp.diff(Lt, t, 2).subs(t, 0)/2)
jet2_f_density = sp.expand(jet2_f(-2*f0*aa))
diff_jets = sp.powsimp(sp.expand(jet2_phi_density - jet2_f_density), force=True)
contact = sp.diff(-q*y**(1-2*q)*aa**2, y)
check("S12 fork collapse: jet2_phi[a] - jet2_f[-2 f0 a] = d/dy(-q y^{1-2q} a^2), all n,q",
      sp.simplify(sp.expand(diff_jets - contact)))

# ---------------- S13: distributional weld in the phi-slot
# weld: f = y^{-q} (y<1), f = 1 (y>1); f continuous, Pi_f = (1/2) y^2 f' jumps by q/2.
# Pi_phi = -y^2 f f'.   Delta Pi_phi = -2 f(1) Delta Pi_f  (continuous factor).
DPi_f = sp.Rational(1,2)*(0 - (-q))     # q/2
DPi_phi_direct = -(0 - 1*1*(-q))        # -[y^2 f f']_-^+ at y=1: -(0 - (-q)) ... careful
# Pi_phi(1^-) = -1*1*(-q) = q ; Pi_phi(1^+) = 0 ; Delta = 0 - q = -q
DPi_phi = 0 - q
check("S13 Delta Pi_phi = -2 f(1) Delta Pi_f (slot-covariant jump)",
      sp.simplify(DPi_phi - (-2*1*DPi_f)))

print(f"\nSymbolic leg: {PASS} PASS / {FAIL} FAIL")
