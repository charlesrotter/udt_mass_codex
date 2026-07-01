import sympy as sp
r,c,xi,kap8,rs,A=sp.symbols('r c xi kappa8 r_s A',positive=True)
# G^t_t = e^{-2phi}(-2r phi' - e^{2phi}+1)/r^2 ; let u=e^{-2phi}. Then
# e^{-2phi}(1-e^{2phi}-2r phi')/r^2.  Note d/dr(r u)=u+r u', u=e^{-2phi}, u'=-2phi'e^{-2phi}
# G^t_t = (1 - (r u)')/r^2  (standard). Set = kap8 T^t_t = -kap8 xi/r^2
u=sp.Function('u')(r)
Gtt=(1 - sp.diff(r*u,r))/r**2
sol=sp.dsolve(sp.Eq(Gtt, -kap8*xi/r**2), u)
print("solve G^t_t=-kap8 xi/r^2 =>", sol)
# expect u = e^{-2phi} = 1 - kap8 xi - C/r  (solid angle deficit + Schwarzschild)

# ---- Skyrme robustness: does a Skyrme term preserve T^t_t=T^r_r? ----
# Skyrme L4 ~ -(1/4)(d_mu n x d_nu n)^2 contracted.  For a PURELY ANGULAR config
# (d_t n=d_r n=0), all field gradients are transverse (theta,phi). The Skyrme term
# built from d_mu n still has d_t n = d_r n = 0, so T_tt and T_rr get contributions
# only via g_tt L4 and g_rr L4 (the explicit field-gradient pieces vanish for t,r).
# => T^t_t = L4 = T^r_r again.  Verify symbolically for the hedgehog.
t,th,ph=sp.symbols('t theta phi')
phi=sp.Function('phi')(r)
g=sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
ginv=g.inv(); coords=[t,r,th,ph]
n=sp.Matrix([sp.sin(th)*sp.cos(ph),sp.sin(th)*sp.sin(ph),sp.cos(th)])
dn=sp.Matrix([[sp.diff(n[a],coords[mu]) for a in range(3)] for mu in range(4)])
# Skyrme: F_{mu nu}^a = d_mu n^b d_nu n^c eps... ; use scalar L4 = (d_mu n.d_nu n)(d^mu n.d^nu n)-(d_mu n.d^mu n)^2
# build h_{mu nu}=dn_mu.dn_nu
h=sp.Matrix(4,4, lambda i,j: sum(dn[i,a]*dn[j,a] for a in range(3)))
hud=sp.simplify(ginv*h)  # h^mu_nu
L4=sp.simplify( sum(hud[i,j]*hud[j,i] for i in range(4) for j in range(4)) - (sp.trace(hud))**2 )
# Skyrme stress: T_{mn} = 4*[ h_{m a} h^a_n - ... ] + g_{mn}L4 (schematic); but the KEY:
# the field-gradient part of T_{tt},T_{rr} vanishes since dn_t=dn_r=0. Show diagonal mixed:
# T^t_t field-part = combos of h_{t.}=0 => only g_tt L4 term => T^t_t=L4. same r.
print("\nh_{tt}=",h[0,0]," h_{rr}=",h[1,1]," (both 0 => Skyrme field-part vanishes for t,r)")
print("L4 (Skyrme density, hedgehog):", L4)
print("=> Skyrme T^t_t = T^r_r = (coupling)*L4 identically (no d_t,d_r n). T^t_t=T^r_r PRESERVED.")
