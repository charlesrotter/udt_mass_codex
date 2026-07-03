"""bv10_cas.py -- blind verifier: CAS checks for E1 (W-orbit reformulation) and
the E3 bottom-system reduction algebra. Independent of the derivation agent's scripts.

Banked EOMs (cell_solver_universe_T3.py, CAS-verified upstream):
  phi'' = 4 e^{-2phi} rho'^2 / (Z rho^2) - 2 phi' rho' / rho
  rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2 + (e^{2phi}/4) U'(rho)
  H_tot = (Z/2) rho^2 phi'^2 - 2 e^{-2phi} rho'^2 - 2 + U(rho) == 0
  Phi   = Z rho^2 phi'
"""
import sympy as sp

r = sp.symbols('r', real=True)
Z = sp.symbols('Z', positive=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho')(r)
U = sp.Function('U')

phip, rhop = sp.Derivative(phi, r), sp.Derivative(rho, r)
phipp_eom = 4*sp.exp(-2*phi)*rhop**2/(Z*rho**2) - 2*phip*rhop/rho
rhopp_eom = 2*phip*rhop - sp.Rational(1,4)*Z*rho*sp.exp(2*phi)*phip**2 \
            + sp.Rational(1,4)*sp.exp(2*phi)*sp.Derivative(U(rho), rho).doit()
H = sp.Rational(1,2)*Z*rho**2*phip**2 - 2*sp.exp(-2*phi)*rhop**2 - 2 + U(rho)
Phi = Z*rho**2*phip

print("=== E1 checks ===")
# (1) H=0 with phi' = Phi/(Z rho^2)  ==>  rho'^2 = (e^{2phi}/2) W,  W = Phi^2/(2 Z rho^2) + U - 2
PHI = sp.symbols('Phi_s', real=True)
W = PHI**2/(2*Z*rho**2) + U(rho) - 2
H_sub = H.subs(phip, PHI/(Z*rho**2))
rhop2_from_H = sp.solve(sp.Eq(H_sub, 0), rhop**2)[0]
chk1 = sp.simplify(rhop2_from_H - sp.exp(2*phi)/2*W)
print("(1) rho'^2 - (e^{2phi}/2) W from H=0:", chk1)

# (2) rho-EOM == 2 phi' rho' + (e^{2phi}/4) dW/drho |_Phi   (with phi' = Phi/(Z rho^2))
dWdrho = sp.diff(W, rho)
claim2 = 2*phip*rhop + sp.Rational(1,4)*sp.exp(2*phi)*dWdrho
chk2 = sp.simplify((rhopp_eom - claim2).subs(phip, PHI/(Z*rho**2)))
print("(2) rho''_eom - [2 phi' rho' + (e^{2phi}/4) dW/drho]:", chk2)

# (3) self-consistency: d/dr of rho'^2 = (e^{2phi}/2) W(rho, Phi(r)) with Phi' = 4 e^{-2phi} rho'^2
#     must reproduce the rho-EOM. First verify Phi' identity from the phi-EOM:
Phip = sp.diff(Phi, r).subs(sp.Derivative(phi, r, 2), phipp_eom)
chk3a = sp.simplify(Phip - 4*sp.exp(-2*phi)*rhop**2)
print("(3a) Phi' - 4 e^{-2phi} rho'^2:", chk3a)
Phi_f = sp.Function('Phi_f')(r)
Wr = Phi_f**2/(2*Z*rho**2) + U(rho) - 2
lhs = sp.diff(rhop**2, r)               # 2 rho' rho''
rhs = sp.diff(sp.exp(2*phi)/2*Wr, r)
rhs = rhs.subs(sp.Derivative(Phi_f, r), 4*sp.exp(-2*phi)*rhop**2)
# on-shell: substitute rho'^2 = (e^{2phi}/2) Wr wherever it appears, phi' = Phi_f/(Z rho^2)
expr = (lhs - rhs).subs(sp.Derivative(rho, r, 2),
        (2*phip*rhop + sp.Rational(1,4)*sp.exp(2*phi)*sp.diff(Wr, rho)))
expr = expr.subs(phip, Phi_f/(Z*rho**2))
expr = sp.expand(expr.subs(rhop**2, sp.exp(2*phi)/2*Wr))
print("(3) d/dr consistency residual:", sp.simplify(expr))

# (4) phase element: k dr with k^2 = e^{2phi} Q over a half-cycle, dr = drho/rho',
#     rho' = e^{phi} sqrt(W/2)  ==>  k dr = sqrt(2) sqrt(Q/W) drho  (pure algebra)
Q = sp.symbols('Q', positive=True)
Wp = sp.symbols('W', positive=True)
kdr = sp.sqrt(sp.exp(2*phi)*Q) / (sp.exp(phi)*sp.sqrt(Wp/2))
print("(4) k/rho' - sqrt(2) sqrt(Q/W):", sp.simplify(kdr - sp.sqrt(2)*sp.sqrt(Q/Wp)))

print()
print("=== E3 reduction checks (bottom system) ===")
# Coordinates: dzeta/dr = sqrt(|s1|) e^{phi};  psi = phi - phi_c (e^{phi_c} = x_c);
# rho = 1 + dhat*v, dhat = dtilde/|s1|;  U'(1+x) = 4*dtilde + 4*stilde1*x,  stilde1 = -|s1|.
s1, dt, xc = sp.symbols('s_1 delta_t x_c', positive=True)   # s1 = |s~1|, dt = delta~
zeta = sp.symbols('zeta', real=True)
v = sp.Function('v')(zeta); psi = sp.Function('psi')(zeta); p = sp.Function('p')(zeta)
dhat = dt/s1

# exact chain-rule transforms: for any F(r), F' = sqrt(s1) e^{phi} F_zeta
# phi'  = sqrt(s1) e^{phi} p          (p = psi_zeta = phi_zeta)
# phi'' = s1 e^{2phi} (p_zeta + p^2)
# rho'  = sqrt(s1) e^{phi} dhat v_zeta
# rho'' = s1 e^{2phi} dhat (v_zetazeta + p v_zeta)
ephi = xc*sp.exp(psi)
rho_z = 1 + dhat*v
phip_z  = sp.sqrt(s1)*ephi*p
phipp_z = s1*ephi**2*(sp.Derivative(p, zeta) + p**2)
rhop_z  = sp.sqrt(s1)*ephi*dhat*sp.Derivative(v, zeta)
rhopp_z = s1*ephi**2*dhat*(sp.Derivative(v, zeta, 2) + p*sp.Derivative(v, zeta))

# phi-EOM exact in zeta:
phi_eom_res = phipp_z - (4*ephi**-2*rhop_z**2/(Z*rho_z**2) - 2*phip_z*rhop_z/rho_z)
phi_eom_res = sp.simplify(phi_eom_res/(s1*ephi**2))
print("phi-EOM exact in zeta (0 = residual):")
p_eq_exact = sp.solve(sp.Eq(phi_eom_res, 0), sp.Derivative(p, zeta))[0]
p_eq_exact = sp.simplify(p_eq_exact)
print("  p_zeta =", p_eq_exact)
gamma_claim = 4*dt**2/(Z*s1**2*xc**2)
p_eq_claim = gamma_claim*sp.exp(-2*psi)*sp.Derivative(v, zeta)**2 - p**2
diff_p = sp.simplify(sp.expand(p_eq_exact - p_eq_claim))
print("  p_zeta(exact) - p_zeta(claim) =", diff_p, "   [dropped terms; O(dhat)]")

# rho-EOM exact in zeta with U'(rho) = 4 dt + 4 (-s1)(rho-1)  (linear-U' slice, banked C form):
Up_lin = 4*dt - 4*s1*(rho_z - 1)
rho_eom_res = rhopp_z - (2*phip_z*rhop_z - sp.Rational(1,4)*Z*rho_z*ephi**2*phip_z**2
                         + sp.Rational(1,4)*ephi**2*Up_lin)
rho_eom_res = sp.simplify(rho_eom_res/(s1*ephi**2*dhat))
v_eq_exact = sp.solve(sp.Eq(rho_eom_res, 0), sp.Derivative(v, zeta, 2))[0]
v_eq_exact = sp.expand(sp.simplify(v_eq_exact))
print("v-EOM exact in zeta:  v_zetazeta =", v_eq_exact)
v_eq_claim = p*sp.Derivative(v, zeta) - v + 1
diff_v = sp.simplify(v_eq_exact - v_eq_claim)
print("  v_zz(exact) - v_zz(claim) =", sp.simplify(diff_v), "  [dropped: -(Z/4) e^{2phi} rho p^2 / dhat, i.e. the (Z/4)phi'^2 source+restoring]")
