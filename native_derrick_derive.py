"""
native_derrick_derive.py -- TASK 2 (symbolic Derrick scaling) + TASK 3 (EOS).

Hedgehog ansatz with radial profile Theta(r):
   n = (sin Theta(r) sin th cos ph, sin Theta sin th sin ph, cos Theta)?
NO -- the standard O(3)/Skyrme hedgehog for a unit-3-vector knot is
   n = (sin Theta(r) hat-r_2d ... ) ; for the topological-charge-1 hedgehog
   n(x) = (sin Theta(r) * x_hat , cos Theta(r))? -> that is the S^3 Skyrmion.
For the S^2 target O(3) baby/Faddeev knot the carrier is the ell=1 hedgehog
   n = ( sin Theta(r) sin th cos ph,  sin Theta(r) sin th sin ph,  cos Theta(r) )
with Theta(r_core)=pi (or 0) at core, Theta->0 at infinity/seal.  This is the
unit-3-vector hedgehog whose winding 2-form is omega_H1.  We carry it exactly.

We build E2 (two-derivative, the L2 of #43) and E4 (the NATIVE Skyrme term
proven in native_skyrme_derive.py) as proper-energy integrals on the UDT metric
with honest measure, then Derrick-scale Theta(r)->Theta(r/lambda).
"""
import sympy as sp

r, th, ph, lam = sp.symbols('r theta phi_a lambda', positive=True)
phi0, xi, kappa, c = sp.symbols('phi0 xi kappa c', positive=True)
Th = sp.Function('Theta')

# unit 3-vector hedgehog (ell=1 carrier)
Theta = Th(r)
n = sp.Matrix([sp.sin(Theta)*sp.sin(th)*sp.cos(ph),
               sp.sin(Theta)*sp.sin(th)*sp.sin(ph),
               sp.cos(Theta)])

# coords x^m = (r,theta,phi). (static, drop t)
coords = [r, th, ph]
# UDT spatial metric (static slice): e^{2phi} dr^2 + r^2 dth^2 + r^2 sin^2th dph^2
# treat phi = phi(r) as a background; for Derrick exponent counting we keep phi
# as a GENERIC background function but first do the SCALE-FREE deep background
# phi = -p ln r (the deep-cell log profile used in B1) AND the flat phi=0 case.
g_dn = sp.diag(sp.exp(2*phi0), r**2, r**2*sp.sin(th)**2)  # phi0 const placeholder
g_up = g_dn.inv()
sqrtg = sp.sqrt(g_dn.det())   # spatial sqrt(g) = e^{phi0} r^2 sin th

# d_m n
dn = [sp.diff(n, x) for x in coords]

def dot(a,b): return (a.T*b)[0,0]

# E2 density: (xi/2) g^{mn} d_m n . d_n n
e2_dens = sp.Rational(1,2)*xi*sum(g_up[m,m]*dot(dn[m],dn[m]) for m in range(3))
e2_dens = sp.simplify(e2_dens)

# E4 density (NATIVE Skyrme = (kappa/4) g^{mp}g^{nq} S_mn.S_pq, S_mn=d_m n x d_n n)
def cross(a,b):
    return sp.Matrix([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]])
S = {}
for m in range(3):
    for k in range(3):
        S[(m,k)] = cross(dn[m], dn[k])
e4_dens = 0
for m in range(3):
    for k in range(3):
        for p in range(3):
            for q in range(3):
                e4_dens += g_up[m,p]*g_up[k,k]*0  # placeholder
e4_dens = sp.Rational(1,4)*kappa*sum(
    g_up[m,p]*g_up[k,kk]*dot(S[(m,k)],S[(p,kk)])
    for m in range(3) for k in range(3) for p in range(3) for kk in range(3))
e4_dens = sp.simplify(e4_dens)

print("E2 density (per sqrtg) :", sp.simplify(e2_dens))
print("E4 density (per sqrtg) :", sp.simplify(e4_dens))

# proper energies: integrate density * sqrtg over th,ph analytically; keep r.
def angint(expr):
    e = sp.integrate(expr*sqrtg, (ph,0,2*sp.pi))
    e = sp.integrate(e, (th,0,sp.pi))
    return sp.simplify(e)

E2_r = angint(e2_dens)   # integrand in r (proper)
E4_r = angint(e4_dens)
print("\nE2 radial integrand (x dr):", sp.simplify(E2_r))
print("E4 radial integrand (x dr):", sp.simplify(E4_r))

# ---- Derrick scaling: Theta(r) -> Theta(r/lambda).  Substitute u=r/lambda. ----
# Under r->lambda*u, Theta(r)=Th(u), Theta'(r)=Th'(u)/lambda, dr=lambda du.
u = sp.symbols('u', positive=True)
Thu = sp.Function('Theta')(u)
def rescale(expr):
    # replace Theta(r)->Theta(u), Theta'(r)-> diff(Theta(u),u)/lambda, r->lambda u, dr->lambda du
    e = expr
    e = e.subs(sp.Derivative(Th(r), r), sp.Derivative(Thu, u)/lam)
    e = e.subs(Th(r), Thu)
    e = e.subs(r, lam*u)
    return sp.simplify(e*lam)   # *lam from dr=lam du

E2_lam = rescale(E2_r)
E4_lam = rescale(E4_r)
print("\n--- Derrick scaling Theta(r)->Theta(r/lambda) ---")
print("E2(lambda) integrand:", sp.simplify(E2_lam))
print("E4(lambda) integrand:", sp.simplify(E4_lam))

# extract lambda power (flat phi0=const background -> pull e^{phi0} constants out)
def lam_power(expr):
    # collect overall lambda exponent
    e = sp.simplify(expr/expr.subs(lam,1))
    return sp.simplify(e)
print("\nE2 lambda-factor:", lam_power(E2_lam))
print("E4 lambda-factor:", lam_power(E4_lam))

print("""
INTERPRETATION:
 In flat-ish (phi0 const) UDT static slice, the angular measure r^2 and metric
 give E2 ~ lambda^{+1}, E4 ~ lambda^{-1} (classic Derrick counts in 3D).
 E(lambda)=A lambda + B/lambda has a UNIQUE minimum at lambda* = sqrt(B/A):
   dE/dlambda = A - B/lambda^2 = 0 => lambda* = sqrt(B/A) > 0, stable (E''>0).
 => a FINITE preferred size is pinned by the ratio of the E4 (kappa) and E2 (xi)
    coefficients and the geometry.  The e^{2phi0} factors multiply A,B and
    SHIFT lambda* but do not remove the minimum (both >0). Deep-phi (phi=-p ln r)
    handled numerically in the BVP script.
""")

# ---- TASK 3: stress tensor pieces for the profile (symbolic, to feed EOS map) ----
print("="*60); print("TASK 3 prep: p_r+rho from L2 and L4 (Skyrme) contributions")
# For the L2 hedgehog with radial twist, banked: p_r+rho = xi e^{-2phi}(Theta')^2.
# Compute the L4 (Skyrme) contribution to p_r+rho symbolically below in the
# numeric script using the full T^m_n; here we just record the L2 piece.
print("L2 piece (banked CANON D7):  p_r+rho |_L2 = xi e^{-2phi} (Theta')^2")
print("L4 piece computed in native_profile_bvp.py via full T^m_n.")
