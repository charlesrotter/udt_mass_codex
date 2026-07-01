import sympy as sp
r=sp.symbols('r',positive=True)
phi=sp.Function('phi')(r)
mu=sp.symbols('mu',positive=True)

# ROUTE B: hierarchy. Geometry's natural scalar law (no action) is Box_g phi = -G^th_th,
# i.e. Box_g phi = (derivatives only). GR massless scalar: Box phi = -S.
# The corpus "UDT-native" addition is -mu^2 phi (algebraic, 0th deriv in phi).
# Question: is mu^2 phi FORCED by the dilation composition rules, or carried as free input?
# The metric is slaved: phi = -(1/2)ln(-g_tt/c0^2). Under the dilation, what is the
# natural 'restoring' 0th-order operator? A dilation has a multiplicative composition:
# combine depth phi_a then phi_b -> phi_a+phi_b (ADDITIVE in phi = log of dilation).
# An additive group has NO intrinsic length scale -> NO forced mu (scale-free).
# A mu^2 phi term BREAKS the additive shift symmetry phi->phi+const. 
# Test: is the geometry shift-symmetric? Box_g phi under phi->phi+c:
phi_shift=phi+sp.symbols('c')
box=lambda f: (1/r**2)*sp.diff(r**2*sp.exp(-2*f)*sp.diff(f,r),r)
print("Box_g[phi] explicit:", sp.simplify(box(phi)*r**2*sp.exp(2*phi)))
# Note: e^{-2phi} prefactor means Box is NOT shift-symmetric in the usual flat sense,
# but the OPERATOR has no zeroth-order (algebraic phi) piece regardless of shift.
# The mu^2 phi term is an EXPLICIT added potential V(phi)=1/2 mu^2 phi^2.
# Is there ANY metric quantity that is algebraic-linear in phi (not e^{2phi}, not phi')?
# phi itself = -(1/2)ln(-g_tt/c0^2). A 'mu^2 phi' = -(mu^2/2) ln(-g_tt/c0^2) = log of metric.
# That is NOT a polynomial curvature invariant. Curvature invariants are built from
# g and its derivatives -> they contain e^{2phi}, phi', phi'' -- never bare ln-type phi.
print()
print("CONCLUSION ROUTE B: 'phi' (=log of the dilation) is not a curvature invariant.")
print("No geometric/curvature object is algebraic-linear in phi. The mu^2*phi term")
print("requires an ADDED potential V(phi)=1/2 mu^2 phi^2 in an action -> NOT forced by geometry.")
