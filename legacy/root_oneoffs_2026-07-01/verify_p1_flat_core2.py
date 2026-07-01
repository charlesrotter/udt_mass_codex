import sympy as sp
r, C1 = sp.symbols('r C1', positive=True)
phi = sp.symbols('phi', real=True)
# implicit: -phi + log(r)/2 + log(e^{2phi}-1)/2 = C1
# => log( r*(e^{2phi}-1) ) /2 - phi = C1  ... wait combine:
# -phi + (1/2)log(r) + (1/2)log(e^{2phi}-1) = C1
# multiply 2: -2phi + log(r) + log(e^{2phi}-1) = 2 C1
# => log( r*(e^{2phi}-1)*e^{-2phi} ) = 2C1
# => r*(e^{2phi}-1)*e^{-2phi} = K   (K=e^{2C1})
# => r*(1 - e^{-2phi}) = K
# => e^{-2phi} = 1 - K/r   => g_tt-like factor = -(1-K/r) c^2  : Schwarzschild with K=2m!
# g_rr = e^{2phi} = 1/(1 - K/r).
# So K = 2m is the mass parameter. Regular core (finite at r->0, no horizon inside cell):
#   e^{-2phi} = 1 - K/r is finite & positive at small r ONLY if K=0.
#   K>0 => blows up / sign change at r=K (horizon); K<0 => fine at r->0? 1+|K|/r -> +inf as r->0.
# Check regularity: phi finite at r=0 requires 1-K/r finite => K=0.
import sympy as sp
K = sp.symbols('K', real=True)
expr = 1 - K/r
print("e^{-2phi} = 1 - K/r ; at r->0 limit:", sp.limit(expr, r, 0, '+'))
# For K!=0 this is +-oo => phi singular at core. K=0 => e^{-2phi}=1 => phi=const => FLAT.
print("K=0 => e^{-2phi}=1 => phi const => Minkowski (flat). CONFIRMED")
