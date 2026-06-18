"""
The genuine unit degree-1 hedgehog: target direction = spatial unit vector rhat,
with the radial profile acting as an SO(3) rotation by angle (pi - Theta(r)?) about
... The standard chiral hedgehog (the one giving E2_r in the corpus) is:

  U(x) = exp( i F(r) tau.rhat )  ->  n = (sin F rhat_x', ...)

For the O(3)/CP^1 sigma model the degree-1 hedgehog that yields
   |grad n|^2 = F'^2 + 2 sin^2 F / r^2   (flat)
is exactly  n0 = ( sin F(r) * rhat ) ??? no, that's not unit.

Resolution: the field n0 maps spatial S^2 -> target S^2. Degree 1 = identity map
composed with a radial twist. The map is:
   target polar angle  = F(r)     <-- depends ONLY on r (this is the hedgehog!)
   target azimuth      = phi      (spatial azimuth)
BUT then it does NOT depend on spatial theta -> degree 0. WRONG.

The TRUE 3D hedgehog (Skyrme) uses the SU(2) field with rhat, giving the pion field
n^a = rhat^a sin F, n^0 = cos F. That's a map S^3->S^3. For O(3) in 3D the unit
3-vector hedgehog of 'degree 1' (monopole-like) is:
   n0 = rhat = (sin theta cos phi, sin theta sin phi, cos theta)   (F profile trivial)
This IS unit and is the genuine hedgehog. Its reduced energy:
"""
import sympy as sp
r, th, ph = sp.symbols('r theta phi', positive=True)
phd = sp.Function('phidil')(r)

def grad2_density_sphere_int(n0):
    dnr = sp.Matrix([sp.diff(c,r) for c in n0])
    dnt = sp.Matrix([sp.diff(c,th) for c in n0])
    dnp = sp.Matrix([sp.diff(c,ph) for c in n0])
    g = ( sp.exp(-2*phd)*dnr.dot(dnr) + (1/r**2)*dnt.dot(dnt)
          + (1/(r**2*sp.sin(th)**2))*dnp.dot(dnp) )
    dens = sp.simplify(g)*sp.exp(phd)*r**2*sp.sin(th)   # * sqrt(g)
    I = sp.integrate(sp.integrate(dens,(ph,0,2*sp.pi)),(th,0,sp.pi))
    return sp.simplify(g), sp.simplify(I)

# Genuine hedgehog with profile F(r): n0 = ( sin F sin th cos ph, sin F sin th sin ph, cos F )
# We KNOW this is not pointwise unit, but the SPHERE INTEGRAL of |grad|^2 may still equal
# the corpus E2_r (the corpus reduced object). Let's verify: corpus E2_r integrand
#  (per dr) = (2pi/3) e^{-phi}[ r^2 sin^2F F'^2 + 2 r^2 F'^2 + 4 e^{2phi} sin^2F ].
# Note the L2 energy (1/2)|grad|^2 sqrt(g) integrated. So compare (1/2)*I to E2_r.
F = sp.Function('Theta')(r)
nH = sp.Matrix([sp.sin(F)*sp.sin(th)*sp.cos(ph),
                sp.sin(F)*sp.sin(th)*sp.sin(ph),
                sp.cos(F)])
g, I = grad2_density_sphere_int(nH)
print("hedgehog |grad|^2 pointwise =", g)
print("\nsphere-integral of |grad|^2 * sqrt(g) =")
sp.pprint(sp.expand(I))
print("\n(1/2)*I =")
half = sp.expand(I/2)
sp.pprint(half)
# corpus E2_r
xi=1
E2_corpus = (2*sp.pi*xi/3)*sp.exp(-phd)*( r**2*sp.sin(F)**2*sp.diff(F,r)**2
              + 2*r**2*sp.diff(F,r)**2 + 4*sp.exp(2*phd)*sp.sin(F)**2 )
print("\nE2_corpus =")
sp.pprint(sp.expand(E2_corpus))
print("\n(1/2)I - E2_corpus =", sp.simplify(half - E2_corpus))
