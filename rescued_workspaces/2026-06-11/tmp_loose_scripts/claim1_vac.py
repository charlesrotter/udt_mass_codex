import sympy as sp
# Vacuum field eq from S_phi = -(C/2) INT e^{-2phi}(dphi)^2 sqrt(-g)
# (dphi)^2 = g^rr phi'^2 = e^{-2phi}phi'^2 ; sqrt(-g)=r^2 sin th
r, th = sp.symbols('r theta', real=True)
phi = sp.Function('phi')(r)
C = sp.symbols('C', positive=True)
L = -sp.Rational(1,2)*C*sp.exp(-2*phi)*( sp.exp(-2*phi)*sp.diff(phi,r)**2 )*(r**2)  # drop sin th const
# Euler-Lagrange: d/dr(dL/dphi') - dL/dphi = 0
dLdphip = sp.diff(L, sp.diff(phi,r))
dLdphi  = sp.diff(L, phi)
EL = sp.diff(dLdphip, r) - dLdphi
EL = sp.simplify(EL)
print("EL (raw) =", EL)
# normalize: divide by coefficient to get phi'' + ...
EL2 = sp.expand(EL / ( -C*sp.exp(-4*phi)*r**2 ))
print("EL normalized =", sp.simplify(EL2))
# compare to phi'' + 2phi'/r - 2phi'^2
target = sp.diff(phi,r,2) + 2*sp.diff(phi,r)/r - 2*sp.diff(phi,r)**2
print("target - EL2 =", sp.simplify(EL2 - target))
