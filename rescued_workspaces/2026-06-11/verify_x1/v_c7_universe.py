"""C7: universe-side asymmetry under f -> 1/f."""
import sympy as sp

y, th = sp.symbols('y theta', positive=True)
phi = sp.Function('phi')(y)

# radial C1 density of the reduced functional: (y^2/4) F'^2 (monopole part;
# full <f'^2> = F'^2 + a'^2, same structure mode by mode).
F = sp.exp(2*phi)
dens_F = (y**2/4)*sp.diff(F, y)**2
# universe side: G = 1/F = exp(-2 phi)  i.e. phi_G = -phi
G = 1/F
dens_G_form = (y**2/4)*sp.diff(G, y)**2   # same FORM in the inverted variable
ratio = sp.simplify(dens_G_form/dens_F)
print("density(1/f)/density(f) =", ratio, "  [= e^{-8 phi}]")
# i.e. writing the f-side density in universe variables: f'^2 = (1/G)'^2 *
# ... equivalently dens_F = dens_G_form * e^{8 phi_G->...}:
print("so the C1 radial density gains e^{±8 phi} under f -> 1/f: f'^2 = G'^2/G^4 =",
      sp.simplify(sp.diff(1/sp.Function('G')(y), y)**2
                  - sp.diff(sp.Function('G')(y), y)**2/sp.Function('G')(y)**4))

# form-identity of the angular potential for F < 1: P = F k^2 G1(k) / 8.
# quadrature derivation never used F > 1; check numerically at F < 1:
import mpmath as mp
mp.mp.dps = 30
SQ3 = mp.sqrt(3)
def Lf(k): return mp.log((1+k)/(1-k))
def G1(k): return (2*k + (k**2-1)*Lf(k))/k**3
mxe = 0
for Fv, kv in [('0.2','0.5'), ('0.5','0.9'), ('0.9','0.3'), ('0.05','0.7')]:
    Fv = mp.mpf(Fv); kv = mp.mpf(kv)
    quad = mp.quad(lambda t: mp.sin(t)*(Fv*kv*mp.sin(t))**2/(4*Fv*(1+kv*mp.cos(t))),
                   [0, mp.pi])/2
    closed = Fv*kv**2*G1(kv)/8
    mxe = max(mxe, abs(quad-closed))
print("form-identity at F<1 (quadrature, max err):", mp.nstr(mxe, 3))
print("angular stiffness P = F k^2 G1/8: proportional to F at fixed shape kappa ->")
print("  softer by factor F on universe side (F<1).  [algebraic from closed form]")
