"""
Diagnose/validate the L4 angular integral robustly via u=cos(th) substitution.
Reproduce native_stabilizer's E4_r for the settled hedgehog (Psi=const),
then turn on Psi(r).
"""
import sympy as sp

r, th, ph = sp.symbols('r theta phi', real=True, positive=True)
u = sp.symbols('u', real=True)   # u = cos(theta), du = -sin th dth
Th = sp.Function('Theta')(r)
Ps = sp.Function('Psi')(r)
phi = sp.Function('phi')(r)
xi, kappa = sp.symbols('xi kappa', real=True, positive=True)

def build(with_psi):
    A = Th
    B = ph + (Ps if with_psi else 0)
    n = sp.Matrix([sp.sin(A)*sp.cos(B), sp.sin(A)*sp.sin(B), sp.cos(A)])
    grr_inv, gthth_inv, gphph_inv = sp.exp(-2*phi), 1/r**2, 1/(r**2*sp.sin(th)**2)
    sqrtg = sp.exp(phi)*r**2*sp.sin(th)
    coords=[r,th,ph]; ginv=[grr_inv,gthth_inv,gphph_inv]
    dn=[sp.diff(n,x) for x in coords]
    def cross(a,b):
        return sp.Matrix([a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]])
    L2 = sp.Rational(1,2)*xi*sum(ginv[i]*dn[i].dot(dn[i]) for i in range(3))
    L4=0
    for i in range(3):
        for j in range(3):
            Sij=cross(dn[i],dn[j])
            L4 += ginv[i]*ginv[j]*Sij.dot(Sij)
    L4 = sp.Rational(1,4)*kappa*L4
    return sqrtg, L2, L4

def angint(dens):
    e = sp.integrate(dens, (ph, 0, 2*sp.pi))    # ph trivial (axial)
    e = sp.simplify(e)
    # e already carries a sin(th) from sqrtg. Convert ALL th -> u=cos th.
    # Replace sin(th)^2 -> (1-u^2), and the leftover single sin(th) (the measure)
    # is absorbed by du. So: INT_0^pi e dth = INT_{-1}^{1} (e / sin th) du.
    e_over_sin = sp.simplify(e/sp.sin(th))
    # now substitute: every sin(th)^2 -> 1-u^2 ; there must be NO odd power of sin left
    e_sub = e_over_sin.rewrite(sp.cos)
    e_sub = e_sub.subs(sp.sin(th)**2, 1-u**2)
    e_sub = e_sub.subs(sp.cos(th), u)
    e_sub = sp.simplify(e_sub)
    # guard: no remaining th
    assert not e_sub.has(th), f"th remains: {e_sub}"
    return sp.simplify(sp.integrate(e_sub, (u, -1, 1)))

print("VALIDATION: settled hedgehog (Psi=const)")
sqrtg,L2,L4 = build(False)
E2 = angint(sqrtg*L2); E4 = angint(sqrtg*L4)
print("E2_r =", sp.simplify(E2))
print("E4_r =", sp.simplify(E4))
E4_ref = (2*sp.pi*kappa/3)*sp.exp(-phi)*((2*r**2*sp.sin(Th)**4+2*r**2*sp.sin(Th)**2)*sp.diff(Th,r)**2 + sp.exp(2*phi)*sp.sin(Th)**4)/r**2
print("E4_r - native_stabilizer ref =", sp.simplify(E4 - E4_ref))
E2_ref = (2*sp.pi*xi/3)*sp.exp(-phi)*(r**2*sp.sin(Th)**2*sp.diff(Th,r)**2 + 2*r**2*sp.diff(Th,r)**2 + 4*sp.exp(2*phi)*sp.sin(Th)**2)
print("E2_r - native_stabilizer ref =", sp.simplify(E2 - E2_ref))

print("\n" + "="*70)
print("NOW WITH INTERNAL TWIST Psi(r) TURNED ON")
print("="*70)
sqrtg,L2,L4 = build(True)
E2p = angint(sqrtg*L2); E4p = angint(sqrtg*L4)
Etot = sp.simplify(E2p+E4p)
print("E2_r[Psi] =", sp.simplify(E2p))
print("\nE4_r[Psi] =", sp.simplify(E4p))
print("\nTOTAL radial integrand E_r[Theta,Psi,phi] =")
print(sp.simplify(Etot))
import pickle
pickle.dump(sp.srepr(Etot), open('/tmp/Etot.pkl','wb'))
print("\n(saved Etot)")
