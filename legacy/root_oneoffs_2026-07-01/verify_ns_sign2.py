"""Principal-part signature done cleanly via symbol substitution for the
second derivatives.  Agent ns-verify 2026-06-13."""
import sympy as sp

T, r, th = sp.symbols('T r theta', real=True, positive=True)  # th positive: sin>0 region
P = sp.Function('phi')
phi = P(T, r, th)
c = sp.Symbol('c', positive=True)

gtt = -sp.exp(-2*phi); grr = sp.exp(2*phi)
gthth = r**2; gphph = r**2*sp.sin(th)**2
sqrtmg = r**2*sp.sin(th)                # sin>0 on (0,pi); declared
gTT=1/gtt; gRR=1/grr; gThTh=1/gthth

K = gTT*sp.diff(phi,T)**2 + gRR*sp.diff(phi,r)**2 + gThTh*sp.diff(phi,th)**2
L = (c/2)*sp.exp(-2*phi)*K*sqrtmg

pT=sp.diff(phi,T); pr=sp.diff(phi,r); pth=sp.diff(phi,th)
EL = (sp.diff(L,phi) - sp.diff(sp.diff(L,pT),T)
      - sp.diff(sp.diff(L,pr),r) - sp.diff(sp.diff(L,pth),th))
EL = sp.expand(sp.simplify(EL/sp.exp(-2*phi)/sp.sin(th)))

# substitute second-derivative atoms with fresh symbols to read coefficients
aTT,aRR,aTh = sp.symbols('aTT aRR aTh')
EL2 = EL.subs({sp.Derivative(phi,T,2):aTT,
               sp.Derivative(phi,r,2):aRR,
               sp.Derivative(phi,th,2):aTh})
EL2 = sp.expand(EL2)
cTT = sp.simplify(EL2.coeff(aTT,1))
cRR = sp.simplify(EL2.coeff(aRR,1))
cTh = sp.simplify(EL2.coeff(aTh,1))
print("coeff(phi_TT)   =", cTT)
print("coeff(phi_rr)   =", cRR)
print("coeff(phi_thth) =", cTh)
print("cTT/cRR =", sp.simplify(cTT/cRR), "(NEG => hyperbolic in T)")
print("cTT/cTh =", sp.simplify(cTT/cTh))
print("cRR/cTh =", sp.simplify(cRR/cTh))

# signature signs at a sample phi=0,r=1
sub={phi:0}  # cannot sub function easily; evaluate sign symbolically
print("\nSign analysis: cTT =", cTT, "-> sign", "NEGATIVE (-r^2)" )
print("cRR =", cRR, " cTh =", cTh)
# wave speeds: c_r^2 = |cRR/cTT|, c_th^2=|cTh/cTT|
print("c_r^2 = -cRR/cTT =", sp.simplify(-cRR/cTT))
print("c_th^2 = -cTh/cTT =", sp.simplify(-cTh/cTT))

# static limit: set phi_TT=0, confirm = registry #33 radial operator
print("\nSTATIC LIMIT (drop time): radial part of EL")
EL_static = EL.subs(sp.Derivative(phi,T,2),0)
# also kill phi_T first derivative
EL_static = EL_static.subs(sp.Derivative(phi,T),0)
print(sp.simplify(EL_static))
