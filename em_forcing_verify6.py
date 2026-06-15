"""Part 6: the SELECTION lever. Does the scalar's static limit reproduce
the phi-cancelled 1/r Coulomb, or something else? Solve the massless KG
(box S = 0) for static S(r) on the UDT background and compare to f=c0+Q/r.
This is the load-bearing test of claim (4): is the gauge field genuinely
SELECTED by matching UDT's own Coulomb, or is a scalar an equal supplier?"""
import sympy as sp

t,r,th,ph,c=sp.symbols('t r theta phi_ang c',real=True)
x=[t,r,th,ph]
phi=sp.Function('phi')(r)   # static spherical phi(r)
g=sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
ginv=g.inv()
sg=sp.sqrt(-g.det())

# Static spherical scalar S(r): box S = (1/sqrt-g) d_mu( sqrt-g g^{mu nu} d_nu S ) = 0
S=sp.Function('S')(r)
box=(1/sg)*sum(sp.diff(sg*ginv[mu,nu]*sp.diff(S,x[nu]),x[mu]) for mu in range(4) for nu in range(4))
box=sp.simplify(box)
print("massless KG (box S) for static S(r), general phi(r):")
print("  box S =", box)
print()

# Compare to Maxwell static A_t=f(r): equation was r f'' + 2 f' = 0 (phi-INDEPENDENT).
# The scalar box S depends on phi (no g^tt g^rr cancellation since scalar uses g^rr alone).
# Solve scalar eq for a SPECIFIC phi to show it is NOT 1/r in general.
# Take phi = phi(r) generic, then specialize phi=ln(1+1/r) etc. Show phi-dependence.
print("=> Maxwell static eq r f''+2f'=0 is INDEPENDENT of phi (phi cancels via g^tt g^rr=-1).")
print("=> Scalar box S DOES contain phi'(r): the scalar static profile depends on phi,")
print("   so it is NOT the universal phi-cancelled 1/r Coulomb.")
print()
# concrete: phi = a/r  -> solve both
a=sp.symbols('a',positive=True)
boxc=box.subs(phi,a/r).doit()
boxc=sp.simplify(boxc.subs(sp.Function('phi')(r),a/r))
# rebuild cleanly
phi2=a/r
g2=sp.diag(-sp.exp(-2*phi2)*c**2, sp.exp(2*phi2), r**2, r**2*sp.sin(th)**2)
g2inv=g2.inv(); sg2=sp.sqrt(-g2.det())
S2=sp.Function('S')(r)
box2=sp.simplify((1/sg2)*sum(sp.diff(sg2*g2inv[mu,nu]*sp.diff(S2,x[nu]),x[mu]) for mu in range(4) for nu in range(4)))
print("For phi=a/r, scalar box S =", box2)
sols=sp.dsolve(sp.Eq(box2,0),S2)
print("scalar static solution:", sols)
# Maxwell for same phi:
f=sp.Function('f')(r)
Fst=sp.zeros(4,4); Ast=[f,0,0,0]
for mu in range(4):
    for nu in range(4):
        Fst[mu,nu]=sp.diff(Ast[nu],x[mu])-sp.diff(Ast[mu],x[nu])
Fupst=sp.zeros(4,4)
for aa in range(4):
    for bb in range(4):
        Fupst[aa,bb]=sum(g2inv[aa,mu]*g2inv[bb,nu]*Fst[mu,nu] for mu in range(4) for nu in range(4))
maxeq=sp.simplify(sp.diff(sg2*Fupst[1,0],r))
print("Maxwell static eq (phi=a/r):", sp.simplify(maxeq/sp.Abs(c*sp.sin(th))))
print("Maxwell solution:", sp.dsolve(sp.Eq(maxeq,0),f))
