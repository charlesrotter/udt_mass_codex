#!/usr/bin/env python3
"""verify_ncat_density.py -- INDEPENDENT re-derivation of L2+L4 density for
n=(sinG cos(k psi), sinG sin(k psi), cosG), G=G(r,theta), on UDT metric.
Built from scratch -- NOT importing the claim's forms. Adversarial verifier."""
import sympy as sp
t,r,th,ps = sp.symbols('t r theta psi', real=True)
xi,kap = sp.symbols('xi kappa', positive=True)
k = sp.symbols('k', positive=True)
phi = sp.Symbol('phi', real=True)
G = sp.Function('G')(r,th)
Gr=sp.diff(G,r); Gt=sp.diff(G,th)
n = sp.Matrix([sp.sin(G)*sp.cos(k*ps), sp.sin(G)*sp.sin(k*ps), sp.cos(G)])
coords=[t,r,th,ps]
g = sp.diag(-sp.exp(-2*phi), sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
gi = g.inv()
print("|n|^2 =", sp.simplify((n.T*n)[0]))
dn = [sp.Matrix([sp.diff(n[i],c) for i in range(3)]) for c in coords]
def dot(a,b): return (a.T*b)[0]
# L2 = -(xi/2) g^{mn} dn_m . dn_n  ; metric diagonal
gg=[[sp.simplify(dot(dn[m],dn[l])) for l in range(4)] for m in range(4)]
L2 = -(xi/2)*sum(gi[m,m]*gg[m][m] for m in range(4))
# L4 Skyrme = -(kap/4) g^{mm}g^{ll}(gg_mm gg_ll - gg_ml gg_lm)
L4 = -(kap/4)*sum(gi[m,m]*gi[l,l]*(gg[m][m]*gg[l][l]-gg[m][l]*gg[l][m])
                  for m in range(4) for l in range(4))
Gs,Grs,Gts=sp.symbols('G Gr Gt',real=True)
sub={sp.diff(G,r):Grs, sp.diff(G,th):Gts, G:Gs}
d2=sp.simplify((-L2).subs(sub)); d4=sp.simplify((-L4).subs(sub))
print("\n-L2 =", d2)
print("\n-L4 =", d4)
# claim's stated densities:
claim_d2 = (xi/2)*(sp.exp(-2*phi)*Grs**2 + Gts**2/r**2 + k**2*sp.sin(Gs)**2/(r**2*sp.sin(th)**2))
claim_d4 = (k**2*kap/2)*sp.sin(Gs)**2*(sp.exp(-2*phi)*Grs**2 + sp.exp(2*phi)*Gts**2/r**2)/r**2
print("\nL2 matches claim:", sp.simplify(d2-claim_d2)==0)
print("L4 matches claim:", sp.simplify(d4-claim_d4)==0)
# proper measure
meas=sp.exp(phi)*r**2*sp.sin(th)
I2=sp.expand(sp.simplify(d2*meas)); I4=sp.expand(sp.simplify(d4*meas))
claim_I2=(xi/2)*(sp.exp(-2*phi)*Grs**2*r**2 + Gts**2 + k**2*sp.sin(Gs)**2/sp.sin(th)**2)*sp.exp(phi)*sp.sin(th)
claim_I4=(k**2*kap/2)*sp.sin(Gs)**2*(sp.exp(-2*phi)*Grs**2 + sp.exp(2*phi)*Gts**2/r**2)*sp.exp(phi)*sp.sin(th)
print("\nI2 (proper integrand) matches claim:", sp.simplify(I2-claim_I2)==0)
print("I4 (proper integrand) matches claim:", sp.simplify(I4-claim_I4)==0)
# pole behavior: as th->0, the k^2 sin^2 G/sin^2 th term. finite energy requires sinG->0.
print("\nPole term in I2: k^2 sin^2(G)/sin^2(th) * eph * sin(th) = k^2 sin^2(G) eph / sin(th)")
print("  -> diverges as th->0 unless sin(G)->0 at poles. CONFIRMED native pole regularity.")
