"""Gate-0 normalization confirm: derive the rho-EOM matter force from the SAME L_m that matches the
base f-PDE, and compare its coefficient to the base rho_ode matter term +(e^{2phi}/4)(xi rho I_r -
kap N^2 I_4th/rho^3).  Uses the theta-integrated (moment) matter Lagrangian, s=0 (round)."""
import sympy as sp
r = sp.symbols('r'); Z, xi, kap, N = sp.symbols('Z xi kappa N', positive=True)
phi=sp.Function('phi')(r); rho=sp.Function('rho')(r)
Ir=sp.Function('I_r')(r); Ith=sp.Function('I_th')(r); Is=sp.Function('I_s')(r)
I4r=sp.Function('I_4r')(r); I4th=sp.Function('I_4th')(r)
ph1=sp.diff(phi,r); rh1=sp.diff(rho,r); e2m=sp.exp(-2*phi); e2p=sp.exp(2*phi)

# theta-integrated matter Lagrangian from L_m (round), using I=1/2 int sin(...) convention (base moments):
#   L_m_reduced = xi[rho^2 I_r + I_th + N^2 I_s] + kap N^2[I_4r + I_4th/rho^2]   (derived by hand+CAS)
Lm_red = xi*(rho**2*Ir + Ith + N**2*Is) + kap*N**2*(I4r + I4th/rho**2)
# geometric reduced Lagrangian (reverse-engineered to give base vacuum EOMs/H):
Lgeo = sp.Rational(1,2)*Z*rho**2*ph1**2 - 2*e2m*rh1**2 + 2
L = Lgeo + Lm_red

# rho-EOM: EL_rho = d/dr(dL/drho') - dL/drho = 0 ; solve for rho''
ELrho = sp.diff(L, rho) - sp.diff(sp.diff(L, rh1), r)
rh2 = sp.symbols('rhopp')
rho_eom = sp.solve(ELrho.subs(sp.diff(rho,r,2), rh2), rh2)[0]
print("rho'' (from my L_m) =", sp.simplify(rho_eom))

# base rho_ode: rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2 + (e^{2phi}/4)(xi rho I_r - kap N^2 I_4th/rho^3)
rho_base = 2*ph1*rh1 - sp.Rational(1,4)*Z*rho*e2p*ph1**2 + (e2p/4)*(xi*rho*Ir - kap*N**2*I4th/rho**3)
print("\nrho'' (base)        =", sp.simplify(rho_base))
diff = sp.simplify(rho_eom - rho_base)
print("\nrho''(mine) - rho''(base) =", diff)
# extract the ratio of the matter-force terms
mine_force = sp.simplify(rho_eom - (2*ph1*rh1 - sp.Rational(1,4)*Z*rho*e2p*ph1**2))
base_force = (e2p/4)*(xi*rho*Ir - kap*N**2*I4th/rho**3)
print("\nmy matter force / base matter force =", sp.simplify(mine_force/base_force))
