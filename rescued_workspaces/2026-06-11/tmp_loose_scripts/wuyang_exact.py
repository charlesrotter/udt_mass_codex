import numpy as np
from numpy.polynomial import polynomial as P

# Exact check: monopole harmonics Y_{q,l,m} are eigenfunctions of H(q,m) with
# eigenvalue l(l+1)-q^2, l=|q|,|q|+1,...  (Wu-Yang 1976, Tamm).
# We verify by constructing the Hamiltonian in a *spectral* (good) way:
# Use substitution f = sin(th)^|m-q?|... Instead verify the lowest state analytically.

# Ground state for given q, lowest l=|q|: Y has form
#   (1-cos)^a (1+cos)^b  with the right a,b. For l=|q|, m ranges -|q|..|q|.
# Known: eigenvalue of operator -1/s d/dth (s d/dth) + (m-q c)^2/s^2  is  l(l+1)-q^2.
# Let's verify operator eigenvalue by acting on a trial: take q=1/2, l=1/2, m=1/2.
# Monopole harmonic: Y_{1/2,1/2,1/2} ∝ cos(th/2)  (up to phase), section in one gauge.
import sympy as sp
th=sp.symbols('theta', positive=True)

def apply_H(q,m,f):
    s=sp.sin(th); c=sp.cos(th)
    term1 = -1/s*sp.diff(s*sp.diff(f,th),th)
    term2 = (m-q*c)**2/s**2 * f
    return sp.simplify((term1+term2)/f)

# q=1/2 ground multiplet l=1/2: candidate eigenfunctions
print("q=1/2:")
for (m,f) in [(sp.Rational(1,2), sp.cos(th/2)), (sp.Rational(-1,2), sp.sin(th/2))]:
    e=apply_H(sp.Rational(1,2),m,f)
    print(f"  m={m}, f -> eigenvalue {sp.nsimplify(e)}  (expect l(l+1)-q^2 = 1/2*3/2-1/4 = 1/2)")

# q=1 ground multiplet l=1, m=-1,0,1
print("q=1:")
for (m,f) in [(1, sp.cos(th/2)**2), (0, sp.sin(th)), (-1, sp.sin(th/2)**2)]:
    e=apply_H(1,m,f)
    print(f"  m={m}, f -> eigenvalue {sp.simplify(e)}  (expect 1*2-1 = 1)")

# q=0 (ordinary spherical harmonics) l=1
print("q=0:")
for (m,f) in [(0, sp.cos(th)), (1, sp.sin(th)), (0, sp.Integer(1))]:
    e=apply_H(0,m,f)
    print(f"  m={m}, f -> eigenvalue {sp.simplify(e)}")
