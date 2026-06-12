import sympy as sp
# The draft says the d_theta h_tr piece "survives into the spin-2 projection with the same
# e^{2phi0}/r^2 coefficient as the canonical scalar deflection 2 e^{2phi0} d_theta dphi/r^2".
# Scalar coeff (of d_theta dphi) = 2 e^{2phi0}/r^2. Gravitomag coeff (of d_theta h_tr) = 1 e^{2phi0}/r^2.
# The COEFFICIENT MULTIPLYING THE FIELD differs by factor 2; the METRIC STRUCTURE e^{2phi0}/r^2 is identical.
# Draft claim 2 wording in CLAUDE.md prompt says "coefficient e^{2phi0}/r^2 - structurally the same".
# CG draft says "same e^{2phi0}/r^2 coefficient ... reproduced exactly".
# Strictly: the metric prefactor e^{2phi0}/r^2 is identical (TRUE); but the scalar has an extra numeral 2.
# "reproduced exactly" in the draft refers to the SCALAR PIECE matching §12.15.2 (residual 0), a separate claim.
r,th=sp.symbols('r theta',real=True)
phi0=sp.Function('phi0')(r)
dphi=sp.Function('dphi')(r,th)
scalar = 2*sp.exp(2*phi0)*sp.diff(dphi,th)/r**2
print("scalar coeff of d_theta dphi:", sp.simplify(sp.diff(sp.expand(scalar),sp.Derivative(dphi,th))))
print("gravitomag coeff of d_theta h_tr: exp(2phi0)/r^2  (factor 2 smaller numeral, same metric structure)")
