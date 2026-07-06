"""Gate-0.5: pin lambda so S_m^base = lambda S_m^std reproduces BOTH the base rho-EOM matter force AND
the base H matter integrand with ONE lambda; then read off the corrected shear source and off-round H."""
import sympy as sp
r=sp.symbols('r'); Z,xi,kap,N,lam=sp.symbols('Z xi kappa N lambda')
phi=sp.Function('phi')(r); rho=sp.Function('rho')(r)
Ir=sp.Function('I_r')(r); Ith=sp.Function('I_th')(r); Is=sp.Function('I_s')(r)
I4r=sp.Function('I_4r')(r); I4th=sp.Function('I_4th')(r)
ph1=sp.diff(phi,r); rh1=sp.diff(rho,r); e2m=sp.exp(-2*phi); e2p=sp.exp(2*phi)

# reduced Lagrangians (theta-integrated via I=1/2 int sin(...) moments):
Lgeo = sp.Rational(1,2)*Z*rho**2*ph1**2 - 2*e2m*rh1**2 + 2
Lm_std = xi*(rho**2*Ir + Ith + N**2*Is) + kap*N**2*(I4r + I4th/rho**2)
L = Lgeo + lam*Lm_std

# --- (3a) rho-EOM: solve lam so matter force matches base +(e^{2phi}/4)(xi rho I_r - kap N^2 I_4th/rho^3) ---
ELrho = sp.diff(L,rho) - sp.diff(sp.diff(L,rh1),r)
rh2=sp.symbols('rhopp'); rho_eom=sp.solve(ELrho.subs(sp.diff(rho,r,2),rh2),rh2)[0]
mine_force = sp.simplify(rho_eom - (2*ph1*rh1 - sp.Rational(1,4)*Z*rho*e2p*ph1**2))
base_force = (e2p/4)*(xi*rho*Ir - kap*N**2*I4th/rho**3)
lam_rho = sp.solve(sp.Eq(sp.simplify(mine_force/base_force),1), lam)
print("(3a) lambda from rho-EOM (mine_force/base_force = 1):", lam_rho)

# --- (3b) H matter: Beltrami H of lam*Lm_std vs base H matter integrand ---
# Beltrami matter-H (reduced): H_m = sum q' dL/dq' - L ; the f_r-kinetic moments (I_r,I_4r) carry q'd/dq'->2x
# H_m^std = 2(xi rho^2 I_r + kap N^2 I_4r) - Lm_std
Hm_std = 2*(xi*rho**2*Ir + kap*N**2*I4r) - Lm_std
Hm = sp.simplify(lam*Hm_std)
H_base_matter = (-sp.Rational(1,2)*xi*rho**2*Ir + sp.Rational(1,2)*xi*(Ith+N**2*Is)
                 - sp.Rational(1,2)*kap*N**2*I4r + sp.Rational(1,2)*kap*N**2*I4th/rho**2)
lam_H = sp.solve(sp.Eq(sp.simplify(Hm - H_base_matter), 0), lam)
print("(3b) lambda from H matter (lam*H_m^std - base = 0):", lam_H)
print("     lam*H_m^std - base_H_matter at lambda=-1/2:", sp.simplify((lam*Hm_std - H_base_matter).subs(lam,-sp.Rational(1,2))))

# --- (4) corrected shear source: Tshear_base = lambda * (rho^2/2) T_s  (pointwise) ---
print("\n(4) corrected shear source (lambda=-1/2):  Tshear_base = -1/2 * (rho^2/2) T_s = -(rho^2/4) T_s")

# --- (8) exact checks: pointwise T_s^std, rigid hedgehog, phi-blindness unaffected ---
rho_s,s,fr,fth,th,f=sp.symbols('rho s f_r f_theta theta f',positive=True)
S=sp.sin(th); sf=sp.sin(f); a_=rho_s**2*sp.exp(s); b_=rho_s**2*sp.exp(-s)*S**2
aa,bb=sp.symbols('aa bb',positive=True)
L2=sp.Rational(1,2)*xi*(fr**2+fth**2/aa+N**2*sf**2/bb)
L4=sp.Rational(1,2)*kap*((N*sf*fr)**2/bb+(N*sf*fth)**2/(aa*bb))
Lm=L2+L4
Ts=sp.simplify(((2*aa*sp.diff(Lm,aa)+Lm)-(2*bb*sp.diff(Lm,bb)+Lm)).subs({aa:a_,bb:b_}))
Tshear_base = sp.simplify(-sp.Rational(1,4)*rho_s**2*Ts)     # -(rho^2/4) T_s
print("T_s^std =", Ts)
print("Tshear_base = -(rho^2/4) T_s =", Tshear_base)
Ts_L2 = sp.simplify(((2*aa*sp.diff(L2,aa)+L2)-(2*bb*sp.diff(L2,bb)+L2)).subs({aa:a_,bb:b_}))
print("rigid hedgehog Tshear_base(L2) at s=0,f=theta(f_th=1),N=1:",
      sp.simplify((-sp.Rational(1,4)*rho_s**2*Ts_L2).subs(s,0).subs(f,th).subs(N,1).subs(fth,1)))
