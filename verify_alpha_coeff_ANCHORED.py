#!/usr/bin/env python3
"""
verify_alpha_coeff_ANCHORED.py  --  DEFINITIVE adjudication of the round-cell
phi-equation DIRECT MATTER SOURCE coefficient (phi-blindness relaxed by a
radial weight e^{alpha*phi}).

THE CONTEST (two prior passes disagree by FACTOR *and* SIGN):
  A: Z(rho^2 phi')' = 4 e^{-2phi} rho'^2  +  ( +alpha ) * xi e^{alpha phi} rho^2 I_r
       (verify_alpha_source_coeff.py, and the doc/charter)
  B: Z(rho^2 phi')' = 4 e^{-2phi} rho'^2  +  ( -alpha/2 ) * xi e^{alpha phi} rho^2 I_r
       (verify_TAB_transverse_stress.py ITEM 5, and the Thread-B implementer)

THE ANCHOR TEST (the tie-breaker -- NOT an isolated derivation):
  ONE self-consistent normalization of the full native reduced action
      S = INT sqrt(h) [ (Z/2)phi'^2 + R2[h] + K_P + L_m ],  sqrt(h)=rho^2 sin(theta)
  must reproduce, by Euler-Lagrange, ALL of the following KNOWN-CORRECT results:
    (1) base phi-EOM :  Z(rho^2 phi')' = 4 e^{-2phi} rho'^2
    (2) base rho-EOM :  rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2
    (3) verified T_AB in the rho-eom:  +(e^{2phi}/4)(xi rho I_r - kap N^2 I_4th/rho^3)
  The normalization that reproduces (1)-(3) is THE correct one; whatever it yields
  for (4) the alpha-source coefficient IS the answer.  A candidate that fails any of
  (1)-(3) is DISQUALIFIED.

Fresh, zero-context.  Own sympy.  Trust neither prior script's stated value.
"""
import sympy as sp

r, th = sp.symbols('r theta', real=True)
Z, xi, kap, N = sp.symbols('Z xi kappa N', positive=True)
alpha = sp.Symbol('alpha', real=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho')(r)
phip = sp.Derivative(phi, r)
rhop = sp.Derivative(rho, r)
# rho-independent theta-moments (pure angular integrals of the S^2 map)
I_r, I_th, I_s, I_4r, I_4th = sp.symbols('I_r I_th I_s I_4r I_4th', real=True)

def EL(L, q):
    """Euler-Lagrange operator d/dr(dL/dq') - dL/dq  for a reduced 1-D Lagrangian."""
    qp = sp.Derivative(q, r)
    return sp.diff(sp.diff(L, qp), r) - sp.diff(L, q)

print("="*78)
print("ONE NORMALIZATION.  Reduced action density = INT_0^pi sin(theta) dtheta * rho^2 * [...]")
print("   (the angular integral of a theta-independent geometry piece = 2;")
print("    the matter radial channel's INT sin(theta) f_r^2 dtheta = 2*I_r -- SAME measure.)")
print("="*78)

# ---------- geometry densities (native, round h = rho^2 * Omega, Branch-P uncompensated K) ----
# R2[h] = 2/rho^2 ;  K_P = -2 e^{-2phi} rho'^2 / rho^2  ;  kinetic (Z/2) phi'^2
# Angle-integrate ( INT sin dtheta = 2 ) and multiply by the areal measure rho^2:
Lgeo = 2*rho**2*( sp.Rational(1,2)*Z*phip**2 + 2/rho**2 + (-2*sp.exp(-2*phi)*rhop**2/rho**2) )
Lgeo = sp.expand(Lgeo)      # = Z rho^2 phi'^2 + 4 - 4 e^{-2phi} rho'^2
print("\nLgeo(r) =", Lgeo)

# ---------- matter densities (phi-blind gbar; SAME sin(theta)*rho^2 measure) ----------
# radial channel -(xi/2) f_r^2 -> INT sin * rho^2 * (-(xi/2) f_r^2) = -xi rho^2 I_r  (the 1/2 & the 2 cancel)
# full 2-derivative + 4-derivative matter reduced to moments:
Lmatter = -xi*(rho**2*I_r + I_th + N**2*I_s) - kap*N**2*(I_4r + I_4th/rho**2)
print("Lmatter(r) =", Lmatter)

# =====================================================================================
# ANCHOR (1): base phi-EOM
# =====================================================================================
EL_phi_geo = sp.simplify(EL(Lgeo, phi))
base_phi_target = sp.simplify(2*Z*(rho**2*phip).diff(r) - 8*sp.exp(-2*phi)*rhop**2)  # = 2*[Z(rho^2phi')'-4e^-2phi rho'^2]
anchor1 = sp.simplify(EL_phi_geo - base_phi_target) == 0
print("\n[ANCHOR 1] base phi-EOM  Z(rho^2 phi')' = 4 e^{-2phi} rho'^2  reproduced:", anchor1)
assert anchor1, "FAIL anchor 1"

# =====================================================================================
# ANCHOR (2): base rho-EOM (geometry only)
# =====================================================================================
EL_rho_geo = sp.simplify(EL(Lgeo, rho))
rho_geo_sol = sp.simplify(sp.solve(EL_rho_geo, sp.Derivative(rho, (r, 2)))[0])
base_rho_target = 2*phip*rhop - sp.Rational(1,4)*Z*rho*sp.exp(2*phi)*phip**2
anchor2 = sp.simplify(rho_geo_sol - base_rho_target) == 0
print("[ANCHOR 2] base rho-EOM  rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2  reproduced:", anchor2)
assert anchor2, "FAIL anchor 2"

# =====================================================================================
# ANCHOR (3): verified transverse matter stress T_AB in the rho-eom
# =====================================================================================
EL_rho_full = sp.simplify(EL(Lgeo + Lmatter, rho))
rho_full_sol = sp.simplify(sp.solve(EL_rho_full, sp.Derivative(rho, (r, 2)))[0])
TAB_derived = sp.simplify(rho_full_sol - base_rho_target)
TAB_verified = sp.Rational(1,4)*sp.exp(2*phi)*(xi*rho*I_r - kap*N**2*I_4th/rho**3)
anchor3 = sp.simplify(TAB_derived - TAB_verified) == 0
print("[ANCHOR 3] verified T_AB  +(e^{2phi}/4)(xi rho I_r - kap N^2 I_4th/rho^3)  reproduced:", anchor3)
assert anchor3, "FAIL anchor 3"

print("\n==> ALL THREE ANCHORS PASS with this ONE normalization. It is the correct one.")

# =====================================================================================
# (4) READ OFF the alpha-source in the phi-EOM  --  FROM THE SAME NORMALIZATION
# Relax phi-blindness: the radial matter channel carries weight e^{alpha phi}.
# Only the radial (I_r) channel is weighted:  -xi rho^2 I_r  ->  -xi e^{alpha phi} rho^2 I_r
# =====================================================================================
Lmatter_alpha_radial = -xi*sp.exp(alpha*phi)*rho**2*I_r
EL_phi_full = sp.simplify(EL(Lgeo + Lmatter_alpha_radial, phi))
# matter contribution to the phi-EL:
matter_phi = sp.simplify(EL_phi_full - EL_phi_geo)      # = + alpha xi e^{alpha phi} rho^2 I_r
# EL = 2Z(rho^2 phi')' - 8 e^{-2phi} rho'^2 + matter_phi = 0.  Normalize operator to Z(rho^2phi')'
# by dividing by 2:  Z(rho^2phi')' = 4 e^{-2phi} rho'^2  -  matter_phi/2 .  Source S := RHS beyond base.
S_source = sp.simplify(-matter_phi/2)
print("\n" + "="*78)
print("(4) ALPHA-SOURCE, read off from the SAME (anchor-passing) normalization")
print("="*78)
print("   matter term in phi-EL (= -dLm_alpha/dphi) =", matter_phi)
print("   => Z(rho^2 phi')' = 4 e^{-2phi} rho'^2 + S,   S =", S_source)
coeff = sp.simplify(S_source/(xi*sp.exp(alpha*phi)*rho**2*I_r))
print("   COEFFICIENT of  xi e^{alpha phi} rho^2 I_r  =", coeff, "  (= -alpha/2)")

# compare to the two contestants
cand_A = alpha            # +alpha
cand_B = -alpha/2         # -alpha/2
print("\n   contestant A coefficient (+alpha)  matches:", sp.simplify(coeff-cand_A)==0)
print("   contestant B coefficient (-alpha/2) matches:", sp.simplify(coeff-cand_B)==0)

# =====================================================================================
# DISQUALIFY A: its hand-built geometry Lagrangian fails anchor (1)
# =====================================================================================
print("\n" + "="*78)
print("WHY A IS WRONG: its bespoke geometry Lagrangian is not the anchored normalization")
print("="*78)
LgeomA = -(Z/2)*rho**2*phip**2 - 2*sp.exp(-2*phi)*rhop**2   # from verify_alpha_source_coeff.py line 97
elA_geo = sp.simplify(EL(LgeomA, phi))
A_phi_sol = sp.simplify(sp.solve(elA_geo, sp.Derivative(phi,(r,2)))[0])
correct_phi_sol = sp.simplify(sp.solve(sp.Eq(Z*(rho**2*phip).diff(r), 4*sp.exp(-2*phi)*rhop**2),
                                       sp.Derivative(phi,(r,2)))[0])
A_reproduces_base = sp.simplify(A_phi_sol - correct_phi_sol) == 0
print("   A's LgeomA reproduces the base phi-EOM (correct +4 e^{-2phi} rho'^2 sign):", A_reproduces_base)
print("   -> A implies Z(rho^2phi')' = -4 e^{-2phi} rho'^2 (WRONG sign) => DISQUALIFIED on anchor 1.")
print("   Two compounding slips in A:")
print("     FACTOR 2: A normalizes geometry kinetic as -(Z/2)rho^2 phi'^2 (operator coeff Z, MISSING")
print("               the INT sin theta dtheta = 2 angular factor that the matter -xi rho^2 I_r carries).")
print("               The anchored geometry kinetic is +Z rho^2 phi'^2 (operator coeff 2Z); halving the")
print("               matter term on normalization gives alpha/2, not alpha.")
print("     SIGN:     A's e^{-2phi} rho'^2 term has the sign that flips the base phi-EOM RHS.")

# =====================================================================================
# alpha < 0 consequence (convention-independent, since anchored to (1)-(3))
# =====================================================================================
print("\n" + "="*78)
print("alpha<0 CONSEQUENCE (rho^2>0, I_r>=0, e^{alpha phi}>0):  sign(S) = sign(-alpha/2) = -sign(alpha)")
print("="*78)
for a_val in (sp.Rational(-1,2), -1, -2):
    val = S_source.subs(alpha, a_val)
    print(f"   alpha={a_val}:  S = {val}   -> POSITIVE  (DIRECT source ADDS to (rho^2 phi')', SUPPORTS structure)")

print("\n" + "="*78)
print("DEFINITIVE VERDICT")
print("="*78)
print("  CORRECT coefficient:  S = -(alpha/2) * xi * e^{alpha phi} * rho^2 * I_r   (contestant B).")
print("  verify_TAB_transverse_stress.py ITEM 5 (and the Thread-B implementer) is RIGHT.")
print("  verify_alpha_source_coeff.py (+alpha) and the doc/charter are WRONG (factor 2 AND sign).")
print("  For alpha<0 the DIRECT source is POSITIVE (restoring/supporting), NOT negative.")
