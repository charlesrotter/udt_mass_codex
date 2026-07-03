"""th2 CAS: verify the two NEW reductions symbolically.
C1  H_tot = 0  <=>  rho'^2 = (e^{2phi}/2) W,  W = Phi^2/(2 Z rho^2) + U(rho) - 2.
C2  the rho-EOM is EXACTLY rho'' = 2 phi' rho' + (e^{2phi}/4) dW/drho at fixed Phi
    (with the Phi-drift term reproducing part of 2phi'rho' -- shown as identity).
C3  seal turning point: W(rho_s)=0 <=> Theorem B  U(rho_s) = 2 - q^2/(2 Z rho_s^2).
C4  bottom reduction: u'' - 2phi'u' + e^{2phi}|s1| u = e^{2phi} dt, with
    zeta' = k = e^phi sqrt|s1|  ==>  u_zz - psi_z u_z + u = dt/|s1|   (exact given those two)
C5  flux eq: Phi' = 4 e^{-2phi} u'^2  ==>  p_z = gamma e^{-2psi} v_z^2 - p^2 with
    p = Phi/(Z x_c e^psi sqrt|s1|), v = u |s1|/dt, gamma = 4 dt^2/(Z s1^2 x_c^2),
    given rho ~ 1 in Phi=Z rho^2 phi' (TRUNC O(u), flagged).
"""
import sympy as sp

ok = lambda name, e: print(f"  [{'PASS' if e else 'FAIL'}] {name}")
r = sp.Symbol('r')
Z, s1, dt, xc = sp.symbols('Z s1 dt x_c', positive=True)   # s1 = |s1|
phi = sp.Function('phi')(r); rho = sp.Function('rho')(r)
U = sp.Function('U')

# C1
Phi = Z*rho**2*phi.diff(r)
H = Z/2*rho**2*phi.diff(r)**2 - 2*sp.exp(-2*phi)*rho.diff(r)**2 - 2 + U(rho)
W = Phi**2/(2*Z*rho**2) + U(rho) - 2
ok("C1: H=0 <=> rho'^2=(e^{2phi}/2)W  (H - [W - 2 e^{-2phi} rho'^2] == 0)",
   sp.simplify(H - (W - 2*sp.exp(-2*phi)*rho.diff(r)**2)) == 0)

# C2: EOM form
rhopp_eom = 2*phi.diff(r)*rho.diff(r) - Z/4*rho*sp.exp(2*phi)*phi.diff(r)**2 + sp.exp(2*phi)/4*U(rho).diff(rho.__class__('rho'))
# cleaner: use explicit symbol for dU
rr = sp.Symbol('rrho', positive=True)
Up = sp.Function("U'")
Wsym = Phi**2/(2*Z*rho**2)  # differentiate W in rho at fixed Phi
dW_drho = sp.diff(sp.Symbol('Phi2')/(2*Z*rr**2) + U(rr) - 2, rr)
# substitute Phi2 -> (Z rho^2 phi')^2 and rr -> rho:
dW = dW_drho.subs({sp.Symbol('Phi2'): Phi**2, rr: rho})
rhs_eom = 2*phi.diff(r)*rho.diff(r) - Z/4*rho*sp.exp(2*phi)*phi.diff(r)**2 + sp.exp(2*phi)/4*U(rho).subs(rho, rr).diff(rr).subs(rr, rho)
ok("C2: -(Z/4) rho e^{2phi} phi'^2 + (e^{2phi}/4)U'(rho) == (e^{2phi}/4) dW/drho|_Phi",
   sp.simplify((rhs_eom - 2*phi.diff(r)*rho.diff(r)) - sp.exp(2*phi)/4*dW) == 0)

# C3: W(rho_s)=0 with q=Phi(r_s)
q, rho_s = sp.symbols('q rho_s', positive=True)
Wseal = q**2/(2*Z*rho_s**2) + sp.Symbol('U_s') - 2
ok("C3: W_seal=0 <=> U_s = 2 - q^2/(2 Z rho_s^2)",
   sp.simplify(sp.solve(Wseal, sp.Symbol('U_s'))[0] - (2 - q**2/(2*Z*rho_s**2))) == 0)

# C4: bottom phase-coordinate reduction
z = sp.Symbol('zeta')
u = sp.Function('u')(z); psi = sp.Function('psi')(z)
phi_b = sp.log(xc)/1 + psi           # phi = phi_c + psi, e^{phi_c}=x_c
k = sp.exp(phi_b)*sp.sqrt(s1)        # dzeta/dr
# u'' (in r) = k^2 u_zz + k k_z u_z ; k_z = k psi_z ; phi' = k psi_z
lhs = (k**2*u.diff(z,2) + k*(k*psi.diff(z))*u.diff(z)) - 2*(k*psi.diff(z))*(k*u.diff(z)) \
      + sp.exp(2*phi_b)*s1*u - sp.exp(2*phi_b)*dt
ok("C4: reduces to u_zz - psi_z u_z + u = dt/s1",
   sp.simplify(lhs/k**2 - (u.diff(z,2) - psi.diff(z)*u.diff(z) + u - dt/s1)) == 0)

# C5: flux equation reduction (rho->1 in Phi flagged)
PhiF = sp.Function('Phi')(z)
p = PhiF/(Z*xc*sp.exp(psi)*sp.sqrt(s1))
v = u*s1/dt
gamma = 4*dt**2/(Z*s1**2*xc**2)
# Phi' = 4 e^{-2phi} (u')^2 ; d/dr = k d/dz ; psi_z = p (definition of the slow map: phi' = Phi/Z at rho~1)
# p_z = Phi_z/(Z xc e^psi sqrt(s1)) - p psi_z ; Phi_z = Phi'/k = 4 e^{-2phi} k u_z^2
Phi_z = 4*sp.exp(-2*phi_b)*k*(u.diff(z))**2
p_z = Phi_z/(Z*xc*sp.exp(psi)*sp.sqrt(s1)) - p*psi.diff(z)
target = gamma*sp.exp(-2*psi)*(v.diff(z))**2 - p**2
ok("C5: p_z = gamma e^{-2psi} v_z^2 - p^2   (given psi_z = p)",
   sp.simplify(p_z.subs(psi.diff(z), p) - target) == 0)
print("  [note] C5 premise psi_z = p uses phi' = Phi/(Z rho^2) with rho->1: TRUNC O(u), flagged;")
print("         C4 uses k = e^phi sqrt|s1| i.e. Q->|s1|: TRUNC O(Z phi'^2/4|s1|), flagged;")
print("         both O(1%)-class at the bottom, degrade near seal (bottom-layer scope only).")
