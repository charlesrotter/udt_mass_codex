"""
Determine the CORRECT unit degree-1 hedgehog n0(r,theta,phi) that reproduces the
reduced invariant |grad n0|^2 = e^{-2phi} T'^2 + 2 sin^2T / r^2  (the corpus form).
Candidate A (canonical hedgehog): target unit vector points along spatial r-hat,
  tilted by profile Theta(r):
    n0 = ( sinTheta(r)*sin(theta)*cos(phi),
           sinTheta(r)*sin(theta)*sin(phi),
           cosTheta(r) )   <- NOT unit; rejected.
Candidate B (true hedgehog, target=spatial direction with polar angle Theta_eff):
  The standard O(3) hedgehog: n0 = rhat-rotated. Use the construction
    n0 = cos(Theta) * zhat ... no.
Actually the canonical hedgehog (Skyrme/baby-skyrmion 3D) is:
    n0 = ( sin f(r) * x/r-pattern ).  The well-known UNIT hedgehog is
    n0 = ( sin Theta(r) * \hat r_x, sin Theta(r) * \hat r_y, ... ) only unit if combined
    with cos on the SAME axis. The genuine unit map of degree 1 is the IDENTITY-like
    map  S^2_space -> S^2_target  composed with a radial profile rotation about a fixed
    axis is NOT it.
The真 degree-1 hedgehog: n(x) = ( sin Theta(r) \hat n_perp + cos Theta(r) \hat z )? no.

The clean unit hedgehog used in ALL chiral-soliton work:
    n0 = ( sin Theta(r) * sin theta * cos phi,
           sin Theta(r) * sin theta * sin phi,
           cos Theta(r) )
   IS the standard ansatz and its |grad|^2 (flat) = Theta'^2 + 2 sin^2Theta/r^2 *ONLY*
   when we use it as a map and the norm is... let's just COMPUTE both the norm and
   the gradient invariant symbolically and see which candidate matches the corpus.
"""
import sympy as sp

r, th, ph = sp.symbols('r theta phi', positive=True)
Th = sp.Function('Theta')(r)
ph_d = sp.Function('phidil')(r)  # dilation phi(r); use exp(-2 phi) on rr

def grad2(n0):
    dnr = sp.Matrix([sp.diff(c,r) for c in n0])
    dnt = sp.Matrix([sp.diff(c,th) for c in n0])
    dnp = sp.Matrix([sp.diff(c,ph) for c in n0])
    g = ( sp.exp(-2*ph_d)*dnr.dot(dnr) + (1/r**2)*dnt.dot(dnt)
          + (1/(r**2*sp.sin(th)**2))*dnp.dot(dnp) )
    return sp.simplify(g)

# Candidate A
nA = sp.Matrix([sp.sin(Th)*sp.sin(th)*sp.cos(ph),
                sp.sin(Th)*sp.sin(th)*sp.sin(ph),
                sp.cos(Th)])
print("A |n|^2 =", sp.simplify(nA.dot(nA)))
print("A grad2 =", grad2(nA))

# Candidate B: true unit hedgehog -- target direction = (theta_t=Theta? ) ... use
# the genuine one: n0 = ( sin Theta cos(phi)... ) where polar=Theta(r) but azimuth
# carries the FULL solid angle via a SECOND angle. The degree-1 hedgehog identifies
# the target sphere with the SPATIAL sphere AND applies radial profile to the polar:
# n0 = ( sin(g) ... ) Hmm. The standard "rational map / hedgehog":
#   n0 = ( sin Theta(r) * \hat e_theta? )
# Let's just test the manifestly-unit form with target angles (Theta(r), phi):
nB = sp.Matrix([sp.sin(Th)*sp.cos(ph),
                sp.sin(Th)*sp.sin(ph),
                sp.cos(Th)])
print("\nB |n|^2 =", sp.simplify(nB.dot(nB)))
print("B grad2 =", grad2(nB))
