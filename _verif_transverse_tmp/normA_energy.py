"""
Does the NORMALIZED candidate-A field (genuinely unit) reproduce the corpus reduced
energy? Compute (1/2) sphere-integral of |grad n_hat|^2 sqrt(g) and compare to E2_corpus.
If different, that tells us the corpus background is genuinely the NON-unit field.
"""
import sympy as sp
r, th, ph = sp.symbols('r theta phi', positive=True)
phd = sp.Function('phidil')(r)
F = sp.Function('Theta')(r)

nA = sp.Matrix([sp.sin(F)*sp.sin(th)*sp.cos(ph),
                sp.sin(F)*sp.sin(th)*sp.sin(ph),
                sp.cos(F)])
norm = sp.sqrt(nA.dot(nA))
nhat = nA/norm

def grad2(n0):
    dnr = sp.Matrix([sp.diff(c,r) for c in n0])
    dnt = sp.Matrix([sp.diff(c,th) for c in n0])
    dnp = sp.Matrix([sp.diff(c,ph) for c in n0])
    return ( sp.exp(-2*phd)*dnr.dot(dnr) + (1/r**2)*dnt.dot(dnt)
          + (1/(r**2*sp.sin(th)**2))*dnp.dot(dnp) )

print("|nhat|^2 =", sp.simplify(nhat.dot(nhat)))
g = grad2(nhat)
dens = g*sp.exp(phd)*r**2*sp.sin(th)
# integrate over phi analytically; theta numerically-ish via symbolic if possible
Iph = sp.integrate(dens,(ph,0,2*sp.pi))
print("integrated over phi; now theta (may be slow)...")
# substitute a numeric F, F', phd to compare magnitude at a sample point
import numpy as np
from sympy import lambdify
Fp = sp.diff(F,r)
expr = Iph
# Build numeric: pick F=1.0 rad, F'=0.5, phd=0, r=1
fnum = lambdify((th, F, Fp, phd, r), expr, 'numpy')
from scipy.integrate import quad
def integrand(thv, Fv, Fpv, phv, rv):
    return float(fnum(thv, Fv, Fpv, phv, rv))
val,_ = quad(integrand, 1e-6, np.pi-1e-6, args=(1.0,0.5,0.0,1.0))
print("normalized-A: (1/2)*sphere-int at (F=1,F'=.5,phi=0,r=1) =", 0.5*val)

# corpus E2_r at same point:
E2c = (2*np.pi/3)*np.exp(-0.0)*(1.0**2*np.sin(1.0)**2*0.5**2 + 2*1.0**2*0.5**2 + 4*np.exp(0.0)*np.sin(1.0)**2)
print("corpus E2_r at same point                          =", E2c)
