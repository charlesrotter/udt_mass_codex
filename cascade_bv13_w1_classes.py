"""bv13 W1 chunks 1-5: per-class endpoint terms of S''(0) for
   L = (Z/2) rho^2 phi'^2 - 2 e^{-2 phi} rho'^2 + 2 - U(rho)
evaluated on the fold pins, using the validated formula
   B_b = L'(b) beta^2 + 2 (L_y.u + L_{y'}.u')|_b beta + L(b) b2 + p(b).w(b)   (minus same at a)
with the second-order endpoint-constraint expansions substituted.
Fold pins (background): even fold r_c: phi'=rho'=0.  odd fold r_s: phi=0, rho'=0.
Conditions claimed needed: H(fold)=0, pins, phi''(fold)=0.
Each chunk is a separate tiny symbolic job; verdict printed per class.
"""
import sympy as sp

Z = sp.Symbol('Z', positive=True)
# background values at a fold treated as SYMBOLS (generic), pins imposed per fold:
phi, phip, phipp, rho, rhop, rhopp = sp.symbols('phi phip phipp rho rhop rhopp', real=True)
Uf = sp.Function('U')
u_, up_, v_, vp_ = sp.symbols('u up v vp', real=True)         # first-order field variations at the fold
wphi, wrho = sp.symbols('wphi wrho', real=True)               # second-order field variations at the fold
beta, b2 = sp.symbols('beta b2', real=True)                   # endpoint shift, its second order
alpha, a2 = sp.symbols('alpha a2', real=True)

# L and partials as functions of (phi, phip, rho, rhop)
P, PP, R, RP = sp.symbols('P PP R RP')
Lsym = (Z/2)*R**2*PP**2 - 2*sp.exp(-2*P)*RP**2 + 2 - Uf(R)
def d(expr, s): return sp.diff(expr, s)
L_phi, L_phip, L_rho, L_rhop = [d(Lsym, s) for s in (P, PP, R, RP)]
sub = {P: phi, PP: phip, R: rho, RP: rhop}
L0   = Lsym.subs(sub)
Lphi, Lphip, Lrho, Lrhop = [x.subs(sub) for x in (L_phi, L_phip, L_rho, L_rhop)]

# EOM-substituted second derivatives (from the banked EOMs, re-derived independently below in chunk EOM)
phipp_eom = 4*sp.exp(-2*phi)*rhop**2/(Z*rho**2) - 2*phip*rhop/rho
rhopp_eom = 2*phip*rhop - (Z/4)*rho*sp.exp(2*phi)*phip**2 + (sp.exp(2*phi)/4)*sp.diff(Uf(rho), rho)

# ---------------- chunk EOM: independent EL re-derivation (one small job) ----------------
rr = sp.Symbol('r'); F = sp.Function('f')(rr); G = sp.Function('g')(rr)
Lfun = (Z/2)*G**2*sp.diff(F, rr)**2 - 2*sp.exp(-2*F)*sp.diff(G, rr)**2 + 2 - Uf(G)
EL_phi = sp.diff(Lfun, F) - sp.diff(sp.diff(Lfun, sp.diff(F, rr)), rr)
EL_rho = sp.diff(Lfun, G) - sp.diff(sp.diff(Lfun, sp.diff(G, rr)), rr)
solved = sp.solve([EL_phi, EL_rho], [sp.diff(F, rr, 2), sp.diff(G, rr, 2)], dict=True)[0]
m = {F: phi, sp.diff(F, rr): phip, G: rho, sp.diff(G, rr): rhop}
chk1 = sp.simplify(solved[sp.diff(F, rr, 2)].subs(m) - phipp_eom)
chk2 = sp.simplify(solved[sp.diff(G, rr, 2)].subs(m) - rhopp_eom)
print("[EOM] independent EL matches banked phi'',rho'' forms:", chk1 == 0 and chk2 == 0)

# total r-derivative of L along the background, with EOM second derivatives
Lprime = (Lphi*phip + Lrho*rhop + Lphip*phipp_eom + Lrhop*rhopp_eom)

# Hamiltonian
H = phip*Lphip + rhop*Lrhop - L0

# =============== chunk 2: phi''(fold)=0 from EOM (both folds) ===============
print("[chunk2] phi'' at even fold (phip=rhop=0):", sp.simplify(phipp_eom.subs({phip: 0, rhop: 0})))
print("[chunk2] phi'' at odd fold (rhop=0, any phi,phip):", sp.simplify(phipp_eom.subs({rhop: 0})))

# =============== chunk 3: L_rho(r_s) = -4 rho''(r_s) via EOM ===============
Lrho_s   = Lrho.subs({phi: 0, rhop: 0})
rhopp_s  = rhopp_eom.subs({phi: 0, rhop: 0})
print("[chunk3] L_rho(r_s) - (Z rho phip^2 - U'(rho)) =",
      sp.simplify(Lrho_s - (Z*rho*phip**2 - sp.diff(Uf(rho), rho))))
print("[chunk3] L_rho(r_s) + 4 rho''(r_s) =", sp.simplify(Lrho_s + 4*rhopp_s))

# =============== chunk 1a: alpha^2 class = L'(a) on even-fold pins ===============
print("[1a alpha^2] L'(r_c)|pins =", sp.simplify(Lprime.subs({phip: 0, rhop: 0})), " -> CANCELS" )

# =============== chunk 1b: beta^2 class ===============
# two sources of beta^2: L'(b) beta^2 (formula) and p_phi * (-phi'' beta^2) from the second-order
# expansion of the essential constraint phi(b(e),e)=0:
#   0 = phi'' b1^2 + 2 u' b1 + phi' b2 + w_phi  =>  w_phi = -phi'' beta^2 - 2 up beta - phip b2
Lprime_s = sp.simplify(Lprime.subs({phi: 0, rhop: 0}))
print("[1b beta^2] L'(r_s)|pins =", Lprime_s)
phipp_s = sp.simplify(phipp_eom.subs({rhop: 0}))
print("[1b beta^2] phi''(r_s)|pins (coeff of the constraint beta^2 piece) =", phipp_s, " -> CANCELS")

# =============== chunk 1c: alpha*beta class ===============
print("[1c alpha*beta] no term in B_b - B_a couples the two endpoints -> ABSENT (structural)")

# =============== chunk 1d: alpha*(field) class at r_c ===============
lin_a = 2*(Lphi*u_ + Lphip*up_ + Lrho*v_ + Lrhop*vp_)
lin_a = sp.simplify(lin_a.subs({phip: 0, rhop: 0}))
print("[1d alpha*field] 2(L_y.u+L_y'.u')|_{r_c} =", lin_a)
# second-order at a: L(a)*a2 + p(a).w(a); p_phi(a)=Z rho^2 phip =0, p_rho(a)=-4e^{-2phi}rhop=0
pa_phi = sp.simplify(Lphip.subs({phip: 0, rhop: 0}))
pa_rho = sp.simplify(Lrhop.subs({phip: 0, rhop: 0}))
La     = sp.simplify(L0.subs({phip: 0, rhop: 0}))
Ha     = sp.simplify(H.subs({phip: 0, rhop: 0}))
print("[1d second-order at r_c] p_phi(a) =", pa_phi, ", p_rho(a) =", pa_rho,
      ", L(a) =", La, "= -H(a) (H(a)=", Ha, ") -> a2 coeff = L(a), vanishes iff H(r_c)=0")

# =============== chunk 1e: beta*(field) class + second-order shifts at r_s ===============
# B_b pieces: 2(L_y.u+L_y'.u')|_b beta  +  L(b) b2  +  p_phi(b) w_phi + p_rho(b) w_rho
# with w_phi = -2 up beta - phip b2 (phi''_s=0 used, chunk 1b), w_rho FREE.
pb_phi = sp.simplify(Lphip.subs({phi: 0, rhop: 0}))
pb_rho = sp.simplify(Lrhop.subs({phi: 0, rhop: 0}))
Lb     = sp.simplify(L0.subs({phi: 0, rhop: 0}))
Hb     = sp.simplify(H.subs({phi: 0, rhop: 0}))
print("[1e] p_rho(r_s) =", pb_rho, " -> w_rho coefficient CANCELS (free 2nd-order rho shift decouples)")
b2_coeff = sp.simplify(Lb + pb_phi*(-phip))          # L(b) b2 + p_phi*(-phip b2)
print("[1e] b2 coefficient = L(b) - p_phi phi' =", b2_coeff, " (should equal -H(r_s))")
print("[1e] b2 coeff + H(r_s) =", sp.simplify(b2_coeff + Hb), " -> CANCELS iff H(r_s)=0")
lin_b = 2*(Lphi*u_ + Lphip*up_ + Lrho*v_ + Lrhop*vp_)
lin_b = sp.expand(lin_b.subs({phi: 0, rhop: 0}))
cross = sp.simplify(lin_b*beta/2*2 + pb_phi*(-2*up_*beta))    # linear class + w_phi up-part
cross = sp.collect(sp.expand(cross), [u_, up_, v_, vp_])
print("[1e] total beta*(field) survivor =", cross)
print("[1e] equals 2*L_rho(r_s)*beta*v ? ->", sp.simplify(cross - 2*Lrho_s*beta*v_) == 0)
