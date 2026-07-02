"""bv2_c_folds.py — BLIND VERIFIER C3/C4: fold boundary-term collection, pins, corner charges.
Independent derivation: single-copy variation delta S = int(EL terms) + [pi_phi dphi + pi_rho drho]_{rc}^{rs};
fold identifications restrict the admissible (dphi, drho) at each end; natural BCs = the pins.
Also: doubled-momenta cross-check and the independent-partner glue.
"""
import sympy as sp

r, Z, eps = sp.symbols('r Z epsilon', positive=True)
phi = sp.Function('phi')(r); rho = sp.Function('rho', positive=True)(r)
eta = sp.Function('eta')(r); zeta = sp.Function('zeta')(r)   # variations
P1, R1 = sp.diff(phi, r), sp.diff(rho, r)

L = sp.Rational(1,2)*Z*rho**2*P1**2 - 2*sp.exp(-2*phi)*R1**2 + 2

# --- (0) boundary-term collection: dS/deps|0 = EL*var + d/dr[ pi_phi*eta + pi_rho*zeta ] ---
Lv = L.subs([(phi, phi + eps*eta), (rho, rho + eps*zeta)], simultaneous=True).doit()
dL = sp.diff(Lv, eps).subs(eps, 0)
pi_phi = Z*rho**2*P1
pi_rho = -4*sp.exp(-2*phi)*R1
ELphi = sp.diff(pi_phi, r) - sp.diff(L, phi)
ELrho = sp.diff(pi_rho, r) - sp.diff(L, rho)
check = sp.simplify(dL - (-ELphi*eta - ELrho*zeta + sp.diff(pi_phi*eta + pi_rho*zeta, r)))
print("boundary-term collection exact (dL = -EL.var + d/dr[pi.var]):", check == 0)

# --- (1) even fold identification (phi,rho)->(phi,rho) is an EXACT symmetry of L_P ---
p1s, r1s, phs, rhs_ = sp.symbols('p1 r1 ph rh')
Ls = sp.Rational(1,2)*Z*rhs_**2*p1s**2 - 2*sp.exp(-2*phs)*r1s**2 + 2
print("even fold (deriv signs flip) exact symmetry:",
      sp.simplify(Ls.subs([(p1s, -p1s), (r1s, -r1s)]) - Ls) == 0)

# natural BCs at r_c (delta phi, delta rho FREE): pi_phi=0, pi_rho=0
print("pi_phi=0 <=> phi'=0 :", sp.solve(sp.Eq(Z*rhs_**2*p1s, 0), p1s))
print("pi_rho=0 <=> rho'=0 :", sp.solve(sp.Eq(-4*sp.exp(-2*phs)*r1s, 0), r1s))

# --- (2) odd fold at r_s: identification phi_2(r_s) = -phi_1(r_s); continuity phi_2 = phi_1 ---
phis = sp.symbols('phi_s')
print("odd id + continuity: solve(-phi_s = phi_s):", sp.solve(sp.Eq(-phis, phis), phis))

# image-side momenta at the fold (image: phi_2(r)=-phi_1(2rs-r), rho_2(r)=rho_1(2rs-r))
# => phi_2'(rs+) = +phi_1'(rs-), rho_2'(rs+) = -rho_1'(rs-), phi_2(rs)= -phi_1(rs)
p1f, r1f, phf, rhf = sp.symbols("phip_s rhop_s phi_s rho_s")
pi_phi_cell = Z*rhf**2*p1f
pi_phi_img  = Z*rhf**2*(+p1f)                       # continuous automatically
pi_rho_cell = -4*sp.exp(-2*phf)*r1f
pi_rho_img  = -4*sp.exp(-2*(-phf))*(-r1f)
print("\n[pi_phi] across odd fold:", sp.simplify(pi_phi_img - pi_phi_cell), " (=0 identically -> phi', q FREE)")
jump_rho = sp.simplify(pi_rho_img - pi_rho_cell)
print("[pi_rho] across odd fold:", jump_rho)
print("  at phi_s=0:", jump_rho.subs(phf, 0), " -> W-E [pi_rho]=0 forces rho'_s=0:",
      sp.solve(sp.Eq(jump_rho.subs(phf, 0), 0), r1f))
print("  WITHOUT using phi_s=0, [pi_rho]=0 gives:", sp.solve(sp.Eq(jump_rho, 0), r1f),
      " (rho'_s=0 forced for ANY phi_s: coefficient -4(e^{2phi}+e^{-2phi}) never 0)")

# equivalently single-copy natural BC: delta rho(r_s) free -> pi_rho(r_s)=0 -> rho'_s = 0
print("single-copy natural BC pi_rho(r_s)=0 -> rho'_s:", sp.solve(sp.Eq(pi_rho_cell, 0), r1f))

# --- (3) INDEPENDENT-partner glue (two separate P-cells joined at r_s, odd relation of values only) ---
p1a, r1a, p1b, r1b, pha = sp.symbols("phip_a rhop_a phip_b rhop_b phi_a")
# continuity of phi with odd relation: phi_b(rs) = -phi_a(rs) AND phi_b(rs)=phi_a(rs) -> phi_a=0 (same pin)
# W-E momentum continuity with INDEPENDENT partner derivatives:
eq_phi = sp.Eq(Z*rhf**2*p1a, Z*rhf**2*p1b)          # pi_phi cont
eq_rho = sp.Eq(-4*sp.exp(-2*0)*r1a, -4*sp.exp(-2*0)*r1b)  # at phi=0
print("\nindependent partner: pi_phi cont ->", sp.solve(eq_phi, p1b), "; pi_rho cont ->", sp.solve(eq_rho, r1b))
print("  => derivatives PASS THROUGH (phi_b'=phi_a', rho_b'=rho_a'); NO rho'=0 pin without the mirror-image constraint")

# --- C4: fold values of E and Phi; corner charges ---
E = sp.Rational(1,2)*Z*rhf**2*p1f**2 - 2*sp.exp(-2*phf)*r1f**2
print("\nC4: E(r_c) with phi'=rho'=0:", E.subs([(p1f,0),(r1f,0)]))
q = sp.symbols('q')
E_rs = E.subs([(r1f, 0), (p1f, q/(Z*rhf**2))])
print("E(r_s) with rho'_s=0, phi'_s=q/(Z rho_s^2):", sp.simplify(E_rs),
      " == q^2/(2 Z rho_s^2):", sp.simplify(E_rs - q**2/(2*Z*rhf**2)) == 0)
# jumps across the fold (image values):
E_img = sp.Rational(1,2)*Z*rhf**2*p1f**2 - 2*sp.exp(+2*phf)*r1f**2
print("E jump img-cell:", sp.simplify(E_img - E), " -> 0 given phi_s=0 OR rho'_s=0:",
      sp.simplify((E_img - E).subs(phf,0)) == 0, sp.simplify((E_img - E).subs(r1f,0)) == 0)
print("Phi jump img-cell:", sp.simplify(Z*rhf**2*p1f - Z*rhf**2*p1f), "(identically 0 -> no delta in Phi)")
