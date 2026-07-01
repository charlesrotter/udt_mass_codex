"""
DECISIVE TEST (convention-robust): does the L2+L4 action on the back-reacted
UDT cell SOURCE an internal-longitude twist Psi(r), or is Psi=const forced?

Key structural fact to verify: if the action depends on Psi ONLY through (Psi')^2
(no term linear in Psi' and no Psi-without-derivative term), then:
  - Psi = const is ALWAYS a solution of the Psi-EOM (the EOM is d/dr[W(r) Psi']=0
    with Psi'=0 satisfying it), and
  - it is the ENERGY-MINIMIZING solution (any Psi'!=0 strictly raises E since the
    Psi'^2 coefficient W(r) >= 0),
  - NOTHING (not phi, not the seal BC, not back-reaction) can SOURCE a nonzero
    Psi gradient, because there is no source term. The seal BCs Psi(core),Psi(seal)
    free => natural BC W Psi'=0 => Psi'=0.
This is the escape-hatch killer: a depth-dependent Berry phase needs Psi'(r)!=0
with depth-dependent swept solid angle. If Psi enters only as (Psi')^2, no twist.

We test this on TWO carriers:
  (I) easy-axis S^2 baby-Skyrme: n=(sinTh cosB, sinTh sinB, cosTh), B=ph+Psi(r)
 (II) Skyrme S^3 hedgehog pion field with an added internal twist.
For each: form the FULL L2+L4 radial functional and read the Psi-dependence.
"""
import sympy as sp

r, th, ph, u = sp.symbols('r theta phi u', real=True)
Th = sp.Function('Theta')(r)
Ps = sp.Function('Psi')(r)
phi = sp.Function('phi')(r)
xi, kappa = sp.symbols('xi kappa', positive=True)

grr,gthth,gphph = sp.exp(-2*phi), 1/r**2, 1/(r**2*sp.sin(th)**2)
sqrtg = sp.exp(phi)*r**2*sp.sin(th)
coords=[r,th,ph]; ginv=[grr,gthth,gphph]
def cross(a,b):
    return sp.Matrix([a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]])

def radial_functional(comps):
    """comps: list of target-space component functions (3 for S^2, 4 for S^3).
    L2 = (xi/2) g^{ij} d_i n . d_j n ; L4 from the antisymmetric S_{ij} (3-vec for S^2)."""
    dn=[[sp.diff(c,coords[i]) for c in comps] for i in range(3)]  # dn[i] vector
    # L2
    L2=sp.Rational(1,2)*xi*sum(ginv[i]*sum(d**2 for d in dn[i]) for i in range(3))
    # L4 only well-defined as cross product for 3-comp (S^2). For S^3 use the
    # Skyrme term tr([L_i,L_j]^2) analog; here we only need the PSI-structure,
    # which the L2 azimuthal sector already exposes. Compute L4 for 3-comp case.
    if len(comps)==3:
        nv=sp.Matrix(comps)
        L4=0
        dnv=[sp.diff(nv,coords[i]) for i in range(3)]
        for i in range(3):
            for j in range(3):
                Sij=cross(dnv[i],dnv[j])
                L4+=ginv[i]*ginv[j]*Sij.dot(Sij)
        L4=sp.Rational(1,4)*kappa*L4
    else:
        L4=0
    dens=sp.simplify(sqrtg*(L2+L4))
    e=sp.integrate(dens,(ph,0,2*sp.pi))
    eos=sp.simplify(e/sp.sin(th)).rewrite(sp.cos).subs(sp.sin(th)**2,1-u**2).subs(sp.cos(th),u)
    eos=sp.simplify(eos)
    if eos.has(th):
        # azimuthal global-monopole log tail: integrate the regular part, flag the tail
        return ('HAS_TH_TAIL', eos)
    return ('OK', sp.simplify(sp.integrate(eos,(u,-1,1))))

print("="*70)
print("CARRIER I: easy-axis S^2 baby-Skyrme with internal twist Psi(r)")
print("  n = (sinTh cos(ph+Psi), sinTh sin(ph+Psi), cosTh)")
print("="*70)
B=ph+Ps
compsI=[sp.sin(Th)*sp.cos(B), sp.sin(Th)*sp.sin(B), sp.cos(Th)]
status,EI = radial_functional(compsI)
print("status:",status)
print("radial functional E_r[Th,Psi,phi] =")
print(EI)

# Read the Psi-dependence: is it purely (Psi')^2 ?
Psp=sp.Derivative(Ps,r)
print("\n--- Psi-structure of E_r ---")
# coefficient of Psi'^2, and check no bare Psi or linear Psi'
EI_exp = sp.expand(EI)
# substitute Psi'-> a symbol to inspect polynomial structure
a = sp.symbols('a')   # stands for Psi'
EI_sub = EI_exp.subs(sp.Derivative(Ps,r), a)
poly = sp.Poly(EI_sub, a) if EI_sub.has(a) else None
if poly is not None:
    print("degree in Psi':", poly.degree())
    print("coeffs (high->low):", poly.all_coeffs())
else:
    print("E_r has NO Psi' dependence at all:", not EI_sub.has(a))
print("E_r depends on bare Psi (not via derivative)?:", EI_sub.has(Ps))
