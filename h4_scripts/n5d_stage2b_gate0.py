"""Gate-0 CAS: (1) pin the shear-kinetic constant C by matching the certified n5d_shear phi-correction
+(1/5Z)e^{-2phi}a2'^2; (3) verify the same L reproduces the E_s_geom operator; (4) matter-H off-round
reduces to the base H matter moments at s=0."""
import sympy as sp
r = sp.symbols('r'); Z = sp.symbols('Z', positive=True)
phi = sp.Function('phi')(r); rho = sp.Function('rho')(r); a2 = sp.Function('a2')(r)
ph1=sp.diff(phi,r); rh1=sp.diff(rho,r); a1=sp.diff(a2,r); e2m=sp.exp(-2*phi)
C = sp.symbols('C')                                     # shear-kinetic coefficient: L_shear = C e^{-2phi} rho^2 a2'^2

print("=== Gate-0.1: pin C by the certified phi-correction ===")
L = sp.Rational(1,2)*Z*rho**2*ph1**2 - 2*e2m*rh1**2 + 2 + C*e2m*rho**2*a1**2
ELphi = sp.diff(L,phi) - sp.diff(sp.diff(L,ph1),r)
ph2 = sp.symbols('phipp')
phi_eom = sp.solve(ELphi.subs(sp.diff(phi,r,2),ph2), ph2)[0]
phi_base = 4*e2m*rh1**2/(Z*rho**2) - 2*ph1*rh1/rho
correction = sp.simplify(phi_eom - phi_base)            # the a2 term in phi''
print("phi'' - base =", correction)
# certified: phi'' = base - (1/5Z) e^{-2phi} a2'^2  -> solve C
Csol = sp.solve(sp.Eq(correction, -sp.Rational(1,5)/Z*e2m*a1**2), C)
print("C solving  correction = -(1/5Z)e^{-2phi}a2'^2 :", Csol)

print("\n=== Gate-0.3: a2 EL operator vs E_s_geom = -e^{-2phi}[rho^2 a2'' + (2 rho rho' - 2 phi' rho^2) a2'] ===")
Cval = Csol[0]
Lc = L.subs(C, Cval)
ELa2 = sp.diff(Lc,a2) - sp.diff(sp.diff(Lc,a1),r)       # = delta S/delta a2 (the residual)
Es_op = -e2m*(rho**2*sp.diff(a2,r,2) + (2*rho*rh1 - 2*ph1*rho**2)*a1)
ratio = sp.simplify(ELa2/Es_op)
print("C value =", Cval, " => H_shear = C e^{-2phi} rho^2 a2'^2 =", Cval, "e^{-2phi} rho^2 a2'^2")
print("(delta S/delta a2) / E_s_geom_op =", ratio, "  (constant => SAME operator up to overall scale)")

print("\n=== Gate-0.4: matter-H off-round -> base H matter moments at s=0 (pointwise density) ===")
# pointwise matter: H_m density = f_r d(sqrt g L_m)/df_r - sqrt g L_m ; integrate over theta -> moments
rho_s, s, fr, fth, N, xi, kap, th, f = sp.symbols('rho s f_r f_theta N xi kappa theta f', positive=True)
S=sp.sin(th); sf=sp.sin(f)
a_=rho_s**2*sp.exp(s); b_=rho_s**2*sp.exp(-s)*S**2; sqrtg=rho_s**2*S
L2=sp.Rational(1,2)*xi*(fr**2+fth**2/a_+N**2*sf**2/b_)
L4=sp.Rational(1,2)*kap*((N*sf*fr)**2/b_+(N*sf*fth)**2/(a_*b_))
dens=sqrtg*(L2+L4)
Hm_dens = sp.simplify(fr*sp.diff(dens,fr) - dens)       # matter Hamiltonian density (per dtheta, /2pi)
print("H_m density (off-round) =", Hm_dens)
Hm0 = sp.simplify(Hm_dens.subs(s,0))
print("H_m density (s=0)       =", Hm0)
# base H matter integrand (per theta, from H_of_r, using moment defs Ir=1/2 int sin f_r^2 etc.):
#   -(xi/2)rho^2 I_r + (xi/2)(I_th + N^2 I_s) - (kap N^2/2) I_4r + (kap N^2/2) I_4th/rho^2
# integrand (x2, since I=1/2 int sin ...): base_ig = sin*[ -(xi/2)rho^2 f_r^2 + (xi/2)(f_th^2 + N^2 sin^2 f/sin^2)
#   - (kap N^2/2) sin^2 f f_r^2/sin^2 + (kap N^2/2) sin^2 f f_th^2/(rho^2 sin^2) ]
base_ig = S*( -sp.Rational(1,2)*xi*rho_s**2*fr**2 + sp.Rational(1,2)*xi*(fth**2 + N**2*sf**2/S**2)
              - sp.Rational(1,2)*kap*N**2*sf**2*fr**2/S**2 + sp.Rational(1,2)*kap*N**2*sf**2*fth**2/(rho_s**2*S**2) )
print("H_m(s=0) - base_integrand =", sp.simplify(Hm0 - base_ig), " (expect 0)")
print("\nGATE-0 SUMMARY: C =", Cval, " (H_shear = +(1/10)e^{-2phi}rho^2 a2'^2 if C=1/10); operator ratio =",
      ratio, "; matter-H round-limit diff above.")
