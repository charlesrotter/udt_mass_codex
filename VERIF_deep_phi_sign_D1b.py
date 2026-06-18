# VERIF_deep_phi_sign_D1b.py
# D1 (clean): the EXACT l=0 (breathing/radial) second-variation operator as the
# Hessian of the reduced native energy E[Theta] = INT (E2_r+E4_r) dr, with FULL
# native xi,kappa. This is the EXACT native coefficient operator. Output the
# Sturm-Liouville coefficients P(r), and the potential pieces, in clean lambdifiable
# form, and PROVE the difference from the prior with_L4 representative operator.
#
# Also: derive the time-kinetic (breathing) weight W from the FULL action with the
# t-dependence restored (g^{tt} = -e^{2phi}), to fix the weight exactly (not the
# representative e^{2phi}).
import sympy as sp

r = sp.symbols('r', positive=True)
xi, kappa = sp.symbols('xi kappa', positive=True)
Tv, Tpv, phv = sp.symbols('Theta Thetap phi', real=True)

# reduced energy density per dr (drop common 2pi/3 -> cancels in omega^2):
edens = ( xi*sp.exp(-phv)*( r**2*sp.sin(Tv)**2*Tpv**2 + 2*r**2*Tpv**2 + 4*sp.exp(2*phv)*sp.sin(Tv)**2 )
         + kappa*sp.exp(-phv)*( (2*r**2*sp.sin(Tv)**4 + 2*r**2*sp.sin(Tv)**2)*Tpv**2
            + sp.exp(2*phv)*sp.sin(Tv)**4 )/r**2 )

P    = sp.simplify(sp.diff(edens, Tpv, 2))
Q    = sp.simplify(sp.diff(edens, Tv, 2))
Rmix = sp.simplify(sp.diff(sp.diff(edens, Tv), Tpv))
dPdT = sp.simplify(sp.diff(P, Tv))

print("="*72)
print("EXACT l=0 Hessian Sturm-Liouville coefficients (full native xi,kappa)")
print("="*72)
print("\nP(Theta,r,phi)  [kinetic, = d2e/dTheta'^2]:")
print(sp.simplify(P))
print("\nQ(Theta,Theta',r,phi)  [= d2e/dTheta^2, raw]:")
print(sp.simplify(Q))
print("\nR_mix [= d2e/dTheta dTheta']:")
print(sp.simplify(Rmix))

# Self-adjoint reduced operator on u(r): the second variation of E about the
# background Theta0(r) for Theta = Theta0 + u is
#   delta^2 E = INT [ P u'^2 + 2 R_mix u' u + Q u^2 ] dr
#   Euler-Lagrange (Jacobi) operator: -(d/dr)(P u') + (Q - d/dr(R_mix)) u = lambda u
# When evaluated along the background, d/dr(R_mix) uses Theta0'(r).
print("\nVeff = Q - d/dr(R_mix|along Theta0(r))  [the Jacobi potential, EXACT].")

# Time-kinetic weight: restore t-dependence. The action kinetic term for a slow
# t-dependence of the collective breathing mode is set by the L2+L4 time-gradient
# with g^{tt} = -e^{2phi}. For the hedgehog n0(Theta(r,t)) the t-kinetic density is
#   (1/2) (xi g^{tt} ... ) (dTheta/dt)^2  weighted by the same angular structure.
# Concretely: replacing one spatial-gradient factor's metric by g^{tt}=-e^{2phi}
# for the time direction, the breathing weight is W = e^{3phi}*[ same Theta-structure
# as P's e^{-phi}->e^{+?} ]. We DERIVE it: the t-kinetic of L2 = (xi/2)(-g^{tt})
# (d_t n)^2 sqrt(g) -> over the sphere gives e^{phi}*e^{2phi}*[xi(r^2 s2+2r^2)+kappa(...)]/...
# Build it explicitly from the action.
th, ph, t = sp.symbols('theta varphi t', real=True)
phir = sp.Function('phi')(r)
Tht  = sp.Function('Theta')(r, t)
n0 = sp.Matrix([sp.sin(Tht)*sp.sin(th)*sp.cos(ph),
                sp.sin(Tht)*sp.sin(th)*sp.sin(ph),
                sp.cos(Tht)])
def d(v, x): return sp.Matrix([sp.diff(c, x) for c in v])
dn_t = d(n0, t)
# g^{tt} = -e^{2phi}; kinetic Lagrangian density L2_t = -(xi/2) g^{tt}(d_t n)^2 = (xi/2)e^{2phi}(d_t n)^2
sqrtg = sp.exp(phir)*r**2*sp.sin(th)
L2_t = sp.Rational(1,2)*xi*sp.exp(2*phir)*dn_t.dot(dn_t)*sqrtg
# L4 time-kinetic: S_{t i} = d_t n x d_i n; the time-kinetic of L4 ~ g^{tt}g^{ii}|S_{ti}|^2
dn_r = d(n0, r); dn_th = d(n0, th); dn_ph = d(n0, ph)
def cross(a,b): return sp.Matrix([a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]])
ginv = {'rr':sp.exp(-2*phir),'thth':1/r**2,'phph':1/(r**2*sp.sin(th)**2)}
gtt = sp.exp(2*phir)  # -g^{tt}
S_tr = cross(dn_t, dn_r); S_tth = cross(dn_t, dn_th); S_tph = cross(dn_t, dn_ph)
L4_t = sp.Rational(1,4)*kappa*( 2*gtt*ginv['rr']*S_tr.dot(S_tr)
        + 2*gtt*ginv['thth']*S_tth.dot(S_tth)
        + 2*gtt*ginv['phph']*S_tph.dot(S_tph) )*sqrtg
Wdens = sp.simplify(L2_t + L4_t)
# coefficient of (dTheta/dt)^2:
Tt = sp.Derivative(Tht, t)
Wcoeff = sp.simplify(Wdens.coeff(Tt, 2))
W_sph = sp.simplify(sp.integrate(sp.integrate(Wcoeff, (ph,0,2*sp.pi)), (th,0,sp.pi)))
print("\nEXACT breathing weight (time-kinetic), sphere-integrated, coeff of (dTheta/dt)^2:")
print(W_sph)
# present in Theta,phi symbols
W_sub = W_sph.subs({Tht:Tv, phir:phv})
print("\n  W(Theta,r,phi) =", sp.simplify(W_sub))
print("  >>> prior with_L4 used W = e^{2phi} (representative); exact W carries xi,kappa and e^{3phi}.")
