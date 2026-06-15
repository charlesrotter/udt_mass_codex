"""
CARRIER II (claim 4): the S^3/SU(2) Skyrme hedgehog. Does an internal twist
Psi(r) here carry a genuine depth-dependent phase that S^2 cannot?

Skyrme field U=exp(i F(r) hat{n}.tau), with hat{n} a unit 3-vector pointing in a
direction that can carry BOTH the spatial winding AND an internal twist.
The pion 4-vector: (n0,n1,n2,n3)=(cos F, sin F * m1, sin F * m2, sin F * m3),
m = unit vector. For the hedgehog m=hat r. We ADD an internal isospin twist:
rotate the (1,2) isospin components by an angle Psi(r): an explicit S^3 helix.

We test the SAME structural question: does Psi enter only as (Psi')^2 (=> no
source, no revived monodromy), or does S^3 admit a linear/source term (=> a
genuine internal phase, the structural reason S^3 differs from S^2)?
"""
import sympy as sp

r, th, ph, u = sp.symbols('r theta phi u', real=True)
F  = sp.Function('F')(r)     # Skyrme profile (analog of Theta)
Ps = sp.Function('Psi')(r)   # internal isospin twist
phi = sp.Function('phi')(r)
xi = sp.symbols('xi', positive=True)

grr,gthth,gphph = sp.exp(-2*phi), 1/r**2, 1/(r**2*sp.sin(th)**2)
sqrtg = sp.exp(phi)*r**2*sp.sin(th)
coords=[r,th,ph]; ginv=[grr,gthth,gphph]

# hat r in spatial frame:
hr = sp.Matrix([sp.sin(th)*sp.cos(ph), sp.sin(th)*sp.sin(ph), sp.cos(th)])
# apply an internal isospin rotation by Psi(r) about isospin-3 axis to hat r:
Rz = sp.Matrix([[sp.cos(Ps),-sp.sin(Ps),0],[sp.sin(Ps),sp.cos(Ps),0],[0,0,1]])
m = Rz*hr   # twisted unit direction (still unit)
# pion 4-vector on S^3:
n0=sp.cos(F)
nvec=sp.sin(F)*m
comps=[n0,nvec[0],nvec[1],nvec[2]]
# check unit
chk=sp.simplify(sum(c**2 for c in comps)-1)
print("S^3 unit check:",chk)

# L2 sigma-model energy on S^3 (the Skyrme 2-derivative term):
L2=sp.Rational(1,2)*xi*sum(ginv[i]*sum(sp.diff(c,coords[i])**2 for c in comps) for i in range(3))
dens=sp.simplify(sqrtg*L2)
e=sp.integrate(dens,(ph,0,2*sp.pi))
eos=sp.simplify(e/sp.sin(th)).rewrite(sp.cos).subs(sp.sin(th)**2,1-u**2).subs(sp.cos(th),u)
eos=sp.simplify(eos)
print("\nth remains?",eos.has(th))
if not eos.has(th):
    Efun=sp.simplify(sp.integrate(eos,(u,-1,1)))
else:
    Efun=eos
print("\nS^3 radial functional E_r[F,Psi,phi] =")
print(Efun)

a=sp.symbols('a')
Es=sp.expand(Efun).subs(sp.Derivative(Ps,r),a)
print("\n--- Psi-structure on S^3 ---")
if Es.has(a):
    p=sp.Poly(Es,a)
    print("degree in Psi':",p.degree())
    print("coeff of Psi'^1 (LINEAR SOURCE):", sp.simplify(p.coeff_monomial(a)))
    print("coeff of Psi'^0 has bare Psi?:", sp.expand(p.coeff_monomial(1)).has(Ps))
else:
    print("no Psi' dependence")
print("E_r depends on bare Psi?:", Es.has(Ps))
