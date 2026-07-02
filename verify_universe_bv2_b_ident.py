"""bv2_b_ident.py — BLIND VERIFIER C1/C2: pointwise identifications (phi,rho)->(-phi,g(rho,phi))
with optional weight w(r); pullback mismatch for P; exact invariance for G; mirrored-extension
EOM residuals (BOTH equations, not just phi's).
"""
import sympy as sp

r, Z = sp.symbols('r Z', positive=True)
ph, rh, p1, r1 = sp.symbols('ph rh p1 r1', real=True)   # phi, rho, phi', rho' as plain symbols
w = sp.symbols('w', positive=True)                       # weight (constant test; r-dep discussed)
g = sp.Function('g')(rh, ph)

L_P  = sp.Rational(1,2)*Z*rh**2*p1**2 - 2*sp.exp(-2*ph)*r1**2 + 2
L_G  = sp.Rational(1,2)*Z*rh**2*p1**2 - 2*r1**2 + 2

# Image fields under the identification + reflection r -> 2 rs - r:
# phi~ = -phi, rho~ = g(rho,phi); d(phi~)/dr(image) = +p1 (odd x reflection),
# d(rho~)/dr(image) = -(g_rho r1 + g_phi p1) but SIGNS drop (quadratic). Use:
gt_p = p1                       # |phi~'|
gt_r = sp.diff(g, rh)*r1 + sp.diff(g, ph)*p1   # |rho~'| up to sign

def image_L(L):
    return L.subs([(p1, gt_p), (r1, gt_r), (ph, -ph), (rh, g)], simultaneous=True)

print("=== C1: match w * L(image) = L, coefficientwise in (p1, r1) ===")
for name, L in [('P', L_P), ('G', L_G)]:
    D = sp.expand(w*image_L(L) - L)
    poly = sp.Poly(D, p1, r1)
    eqs = {m: sp.simplify(c) for m, c in zip(poly.monoms(), poly.coeffs())}
    print(f"\nBranch {name} mismatch coefficients (monomials in (phi',rho')):")
    for m, c in eqs.items():
        print("  ", m, ":", c)

# --- solve the G matching by hand-logic, CAS-checked ---
print("\n--- G branch matching ---")
gr, gp = sp.symbols('g_r g_p')  # partials of g
# coefficients: p1^2: (Z/2)(w g^2 - rh^2) - 2 w gp^2 ... build explicitly
G_sym = sp.Function('G')  # not needed; do with generic partial symbols:
gg = sp.symbols('gg', positive=True)
c_r1r1 = -2*w*gr**2 + 2
c_p1r1 = -4*w*gr*gp
c_p1p1 = sp.Rational(1,2)*Z*(w*gg**2 - 1*0) - 2*w*gp**2 - sp.Rational(1,2)*Z*rh**2
c_p1p1 = sp.Rational(1,2)*Z*w*gg**2 - 2*w*gp**2 - sp.Rational(1,2)*Z*rh**2
c_const = 2*w - 2
sols = sp.solve([c_r1r1, c_p1r1, c_p1p1], [gr, gp, gg], dict=True)
print("solutions of field-term matching (gr, gp, gg):")
for s in sols: print("  ", s)
print("with the constant term 2w-2=0 -> w=1:", sp.solve(c_const, w))

# --- P branch: show field-term matching is CONTRADICTORY (no pointwise g works) ---
print("\n--- P branch matching ---")
c_r1r1P = -2*w*sp.exp(2*ph)*gr**2 + 2*sp.exp(-2*ph)
c_p1r1P = -4*w*sp.exp(2*ph)*gr*gp
c_p1p1P = sp.Rational(1,2)*Z*w*gg**2 - 2*w*sp.exp(2*ph)*gp**2 - sp.Rational(1,2)*Z*rh**2
solsP = sp.solve([c_r1r1P, c_p1r1P, c_p1p1P], [gr, gp, gg], dict=True)
print("P solutions:", solsP)
print("NOTE: gr depends on phi -> g_r = +-e^{-2phi}/sqrt(w) forces g_phi != 0, but matching forces g_phi=0.")
print("Integrability: g_r = e^{-2ph}/sqrt(w) => d(g_r)/dph = -2e^{-2ph}/sqrt(w) != d(g_p)/drh = 0 -> CONTRADICTION.")

# === C2: pullback difference with the FORCED candidate g=rho, w=1 ===
print("\n=== C2 ===")
Lt_P = L_P.subs(ph, -ph)      # rho unchanged, derivative signs irrelevant
diff_P = sp.simplify(Lt_P - L_P)
print("P: L~ - L =", diff_P, " == -4 sinh(2phi) rho'^2 :",
      sp.simplify(diff_P + 4*sp.sinh(2*ph)*r1**2) == 0)
Lt_G = L_G.subs(ph, -ph)
print("G: L~ - L =", sp.simplify(Lt_G - L_G), " (exact invariance)")

# === C2b: mirrored extension of a P-solution -> EOM residuals ===
print("\n=== C2b: EOM residuals of the mirrored extension ===")
rr = sp.symbols('r')
phi = sp.Function('phi')(rr); rho = sp.Function('rho', positive=True)(rr)
P1 = sp.diff(phi, rr); R1 = sp.diff(rho, rr)
P2 = sp.diff(phi, rr, 2); R2d = sp.diff(rho, rr, 2)
phipp_P = 4*sp.exp(-2*phi)*R1**2/(Z*rho**2) - 2*P1*R1/rho
rhopp_P = 2*P1*R1 - Z/4*rho*sp.exp(2*phi)*P1**2
# image at mirrored point: phi_i=-phi, rho_i=rho, phi_i'=+P1, rho_i'=-R1, phi_i''=-P2, rho_i''=+R2d
# residual of phi-eq for image: phi_i'' - [4 e^{-2 phi_i} rho_i'^2/(Z rho_i^2) - 2 phi_i' rho_i'/rho_i]
res_phi = (-P2) - (4*sp.exp(2*phi)*R1**2/(Z*rho**2) - 2*P1*(-R1)/rho)
res_phi = sp.simplify(res_phi.subs(P2, phipp_P))
claim = -(4*R1**2/(Z*rho**2))*(sp.exp(-2*phi) + sp.exp(2*phi))
print("phi-eq residual =", sp.simplify(res_phi))
print("  equals claim -(4rho'^2/(Z rho^2))(e^{-2phi}+e^{2phi}):", sp.simplify(res_phi - claim) == 0)
# residual of rho-eq for image: rho_i'' - [2 phi_i' rho_i' - (Z/4) rho_i e^{2 phi_i} phi_i'^2]
res_rho = (R2d) - (2*P1*(-R1) - Z/4*rho*sp.exp(-2*phi)*P1**2)
res_rho = sp.simplify(res_rho.subs(R2d, rhopp_P))
print("rho-eq residual =", sp.expand(res_rho), "  (claim silent on this one)")
# both residuals at the fold surface with pins phi=0, rho'=0:
print("phi-res at (phi=0? no—needs rho'=0):", sp.simplify(res_phi.subs(R1, 0)))
print("rho-res at rho'=0 and phi=0:", sp.simplify(res_rho.subs(R1, 0).subs(phi, 0)))
