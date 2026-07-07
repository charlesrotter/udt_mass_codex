import sympy as sp

r, th, phi, phir, Z, xi, kap, N, rho = sp.symbols('r theta phi phip Z xi kappa N rho', positive=True)
fr, fth, f, alpha, lam = sp.symbols('f_r f_theta f alpha lambda', real=True)

# Winding carrier n=(sin f cos Nψ, sin f sin Nψ, cos f). Static f=f(r,θ).
# G_mn = ∂_m n · ∂_n n. Nonzero static: G_rr=f_r^2, G_thth=f_th^2, G_psipsi=N^2 sin^2 f
# Physical inverse metric (areal ρ=r): g^{rr}=e^{-2φ}, g^{thth}=1/rho^2, g^{psipsi}=1/(rho^2 sin^2 th), g^{tt}=-e^{2φ}/c^2
# Channel-corrected (bare) ḡ: strip depth weights -> ḡ^{rr}=1 (radial), angular unchanged.
# GENERAL radial weight: g^{rr}_used = e^{alpha*phi}.  alpha=0 => bare/blind ; alpha=-2 => physical-g.

Grr, Gthth, Gpsi = fr**2, fth**2, N**2*sp.sin(f)**2
grr = sp.exp(alpha*phi)                 # general radial weight
gthth = 1/rho**2
gpsi  = 1/(rho**2*sp.sin(th)**2)

# L2 density = -(xi/2) g^{mn} G_mn  (radial + angular channels), measure sqrt(-g)=c*rho^2*sin th (phi-free)
L2 = -sp.Rational(1,2)*xi*( grr*Grr + gthth*Gthth + gpsi*Gpsi )
measure = rho**2*sp.sin(th)          # drop c
integrand = (L2*measure)

# Only the radial channel carries phi. Vary action wrt phi (algebraic, no deriv of phi here since L2 has no phi'):
dintegrand_dphi = sp.diff(integrand, phi)
print("d(L2*measure)/dphi =", sp.simplify(dintegrand_dphi))
print("  -> at alpha=0  (channel-corrected / blind):", sp.simplify(dintegrand_dphi.subs(alpha,0)))
print("  -> at alpha=-2 (physical g^{rr}=e^{-2phi}) :", sp.simplify(dintegrand_dphi.subs(alpha,-2)))

# The phi-EL equation: full action S=∫ c*rho^2*sin th [ (Z/2)phi'^2/rho^2? ] ... 
# Use the field-eq doc's kinetic: R1-weighted density = rho^2 phi'^2 (phi-free). 
# Reduced 1-D radial action per 4π: S_phi = ∫ dr [ (Z/2) rho^2 phip^2 ]  giving (rho^2 phi')' from EL,
# plus Branch-P 𝒦 source giving -4 e^{-2φ} (per doc:119 Z(r^2 phi')'=4e^{-2φ}).
# Add matter: integrate the radial-channel matter term over θ. Radial matter density (per 4π, incl measure):
#   M_phi(phi) = -(xi/2) e^{alpha phi} * rho^2 * (∫ sin th f_r^2 dth) = -(xi/2) e^{alpha phi} rho^2 * 2 I_r
Ir = sp.Symbol('I_r', positive=True)   # I_r = 1/2 ∫ sinθ f_r^2 dθ
M_phi = -sp.Rational(1,2)*xi*sp.exp(alpha*phi)*rho**2*(2*Ir)   # radial-channel matter, θ-integrated
dM_dphi = sp.diff(M_phi, phi)
print("\nMatter contribution to φ-EL  δS_m/δφ = ∂M/∂φ =", sp.simplify(dM_dphi))
print("  alpha=0  :", sp.simplify(dM_dphi.subs(alpha,0)), "  (φ-BLIND: matter absent from φ-eq)")
print("  alpha=-2 :", sp.simplify(dM_dphi.subs(alpha,-2)))
print("\nSo φ-EOM (Branch P, round):  Z (rho^2 φ')' = 4 e^{-2φ}  -  [∂M/∂φ]")
print("  = 4 e^{-2φ}  +  alpha * xi * e^{alpha φ} rho^2 I_r   (matter source, vanishes iff alpha=0)")
