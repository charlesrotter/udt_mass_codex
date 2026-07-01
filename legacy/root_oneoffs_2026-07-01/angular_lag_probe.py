"""
angular_lag_probe.py — PRE-WORK PROBE (not the deliverable).

Goal: find out, by direct symbolic integration, WHAT angular gradient
energy over S^2, evaluated on the project's own anisotropy mode
   f = F (1 + kappa cos theta),  a = F kappa/sqrt(3),
reproduces the project's banked angular potential
   P(F,a) = (3 a^2/(8F)) G1(kappa) = (pi/2) F kappa^2 G1(kappa),
   G1 = (2k + (k^2-1) L)/k^3,  L = ln((1+k)/(1-k)).

This is the anti-smuggling test for TASK 5: if the unit-3-vector
(hedgehog) gradient energy integral REPRODUCES G1, the angular sector
IS the global monopole and we wrote our own functional. If not, it isn't.

The hedgehog n = (sin Th cos ph, sin Th sin ph, cos Th).  The radial-
winding (degree-1) map Th = theta gives the round monopole.  The
project's ANISOTROPY mode is a *polar deformation* of the embedding:
the latitude pushed by kappa.  We model it as a tilt of the n-field's
polar angle and ask which scalar built from |grad n|^2 integrates to G1.
"""
import sympy as sp

th, ph, k = sp.symbols('theta varphi kappa', positive=True)
L = sp.log((1+k)/(1-k))
G1 = (2*k + (k**2 - 1)*L)/k**3

# target (per the project, up to the F kappa^2 prefactor):
#   P / ((pi/2) F) = kappa^2 G1(kappa)
target = k**2 * G1
print("TARGET  kappa^2 G1 =", sp.simplify(sp.series(target, k, 0, 8).removeO()))

# ---------------------------------------------------------------
# Candidate A: GLOBAL MONOPOLE gradient energy of the unit field with a
# polar-anisotropic embedding.  For a hedgehog n with polar angle
# Theta(theta), the sigma-model energy density on S^2 is
#   e = (1/2)[ Theta_theta^2 + sin^2(Theta)/sin^2(theta) ]   (per the round metric)
# The transverse term sin^2(Theta)/sin^2(theta) is the global-monopole
# angular-deficit piece.  We test the ANISOTROPY by the natural one-
# parameter family that makes the SOLID-ANGLE measure of n anisotropic
# with amplitude kappa.  The cleanest project-native version: the field
# whose energy on S^2 weighted by the deformed area element (1+kappa cos)
# reproduces G1.  Test the pure transverse (monopole) piece first.
# ---------------------------------------------------------------

# The deformed AREA element on the anisotropic sphere f=F(1+kappa cos th):
#   the induced 2-metric radius-squared scales like f^2 ~ F^2(1+kappa cos)^2.
# The transverse gradient energy of a unit field on a sphere of position-
# dependent radius integrates the *winding density* weighted by 1/radius^2
# against the area element radius^2 sin th -> sin th, BUT the global-
# monopole INVARIANT piece is INT (1 - n_r) type.  Let us just integrate
# the candidate densities and pattern-match the kappa-series to G1.

def integ(dens):
    """integrate dens * sin(theta) over the sphere, /(2) for the 1/2, /(2pi)*2pi."""
    I = sp.integrate(dens*sp.sin(th), (th, 0, sp.pi))
    return sp.simplify(I)

# Candidate A1: transverse monopole density on the DEFORMED sphere.
# winding density of a degree-1 map weighted by the local inverse metric
# factor 1/(1+kappa cos th)^2 (the f^{-2} from the angular part of g),
# integrated against the area element (1+kappa cos th)^... .  Try the
# natural global-monopole reduction: e ~ 1/(1+kappa cos th)^2, measure sin.
densA1 = 1/(1 + k*sp.cos(th))**2
IA1 = integ(densA1)
print("\nA1  INT [1/(1+k cos)^2] sin dth =", IA1)
print("    series:", sp.series(IA1, k, 0, 8).removeO())

# Candidate A2: e ~ 1/(1+kappa cos th)  (single power)
IA2 = integ(1/(1 + k*sp.cos(th)))
print("\nA2  INT [1/(1+k cos)] sin dth =", IA2)
print("    series:", sp.series(IA2, k, 0, 8).removeO())

# Candidate A3: the LOG itself.  Note L = ln((1+k)/(1-k)) = INT_{-1}^{1} du/(1+ k u)?  check.
u = sp.symbols('u')
I_log = sp.integrate(1/(1 + k*u), (u, -1, 1))
print("\nA3  INT_{-1}^{1} du/(1+k u) =", sp.simplify(I_log), " (= L/k)")

# G1 itself: G1 = (2k+(k^2-1)L)/k^3.  Let's see what integral gives k^2 G1.
# k^2 G1 = (2k + (k^2-1)L)/k.  And L/k = INT du/(1+ku).  So
# k^2 G1 = 2 + (k^2-1)/k^2 * (k L/... ) ... do it directly:
expr = (2*k + (k**2-1)*L)/k     # = k^2 G1
print("\nk^2 G1 =", sp.simplify(expr))
print("   series:", sp.series(expr, k, 0, 8).removeO())

# Try to MATCH: is k^2 G1 == c1 * INT (cos^2 th)/(1+k cos th)^? ...
# Global monopole transverse energy with embedding cos(Theta)=cos th and
# the DEFORMED metric usually gives INT sin^2(Theta)/g_thth.  Let's brute
# a small basis of integrands u^p/(1+k u)^q and fit to k^2 G1.
print("\n--- brute pattern search for k^2 G1 as INT_{-1}^1 N(u)/(1+k u)^q du ---")
for q in [1, 2, 3]:
    for Npoly, label in [(1, "1"), (u**2, "u^2"), (1-u**2, "1-u^2"),
                         (u, "u"), (u**2-sp.Rational(1,3), "u^2-1/3")]:
        val = sp.integrate(Npoly/(1+k*u)**q, (u, -1, 1))
        val = sp.simplify(val)
        diff = sp.simplify(val - expr)
        tag = "  <<< MATCH" if diff == 0 else ""
        if tag:
            print(f"  q={q} N={label}: {val}{tag}")
# also test linear combinations giving global-monopole form (1 - cosTh)/...
print("\n--- global-monopole-style INT (1-u^2)/(1+k u)^2 etc ---")
for q in [1,2,3]:
    val = sp.simplify(sp.integrate((1-u**2)/(1+k*u)**q, (u,-1,1)))
    print(f"  q={q}: INT(1-u^2)/(1+ku)^{q} =", val, " series", sp.series(val,k,0,6).removeO())
