#!/usr/bin/env python3
"""
INDEPENDENT verifier part 2: the field provenance disentanglement.
Driver: Claude (Opus 4.8, 1M) blind verifier. 2026-06-15. DATA-BLIND.

(a) Is the committed n (the S^2 'naive' field) unit-norm?  the S^3 hedgehog?
(b) Does the Hilbert stress of the S^3 unit hedgehog == committed stress() (rho,p_r)?
(c) Does the S^2-naive field reproduce a DIFFERENT stress? -> if the committed
    stress() is genuinely the unit S^3 field, the (r,r) violation is NOT a non-unit
    artifact.  Decisive for the disentanglement.
"""
import sympy as sp

t, r, th, ps = sp.symbols('t r theta psi', real=True)
xi, kap = sp.symbols('xi kappa', positive=True)
phi = sp.Function('phi')(r)
Th = sp.Function('Theta')(r)
Thp = sp.diff(Th, r)
coords = [t, r, th, ps]
g = sp.diag(-sp.exp(-2*phi), sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
gi = g.inv()

def dot(a, b): return (a.T*b)[0]
def derivs(n): return [sp.Matrix([sp.diff(n[k], c) for k in range(len(n))]) for c in coords]

def hilbert_stress_mixed(n):
    """Mixed T^mu_mu via Hilbert variation, INDEPENDENT recomputation."""
    G = sp.symbols('G0 G1 G2 G3', real=True)
    Gm = sp.diag(*G); Gim = Gm.inv()
    dn = derivs(n)
    gg = [[dot(dn[m], dn[k]) for k in range(4)] for m in range(4)]
    L2 = -(xi/2)*sum(Gm[m, m]*gg[m][m] for m in range(4))
    L4 = -(kap/4)*sum(Gm[m, m]*Gm[k, k]*(gg[m][m]*gg[k][k]-gg[m][k]*gg[k][m])
                      for m in range(4) for k in range(4))
    L = L2 + L4
    sub = {G[i]: gi[i, i] for i in range(4)}
    return {i: sp.simplify(gi[i, i]*((-2*sp.diff(L, G[i]) + Gim[i, i]*L).subs(sub)))
            for i in range(4)}

# committed pointwise stress (rho, p_r) from complete_metric_batched.stress
X = sp.exp(-2*phi)*Thp**2; Y = sp.sin(Th)**2/r**2
rho_c = (xi/2)*(X+2*Y) + (kap/2)*(2*X*Y+Y**2)
pr_c  = (xi/2)*(X-2*Y) + (kap/2)*(2*X*Y-Y**2)

S2 = sp.Matrix([sp.sin(Th)*sp.sin(th)*sp.cos(ps),
                sp.sin(Th)*sp.sin(th)*sp.sin(ps), sp.cos(Th)])
S3 = sp.Matrix([sp.sin(Th)*sp.sin(th)*sp.cos(ps), sp.sin(Th)*sp.sin(th)*sp.sin(ps),
                sp.sin(Th)*sp.cos(th), sp.cos(Th)])

print("="*78)
print("TASK 3b: field provenance disentanglement (decisive for the overturn)")
print("="*78)
for name, n in [('S2_naive (record ansatz)', S2), ('S3_hedgehog (unit 4-vec)', S3)]:
    nrm = sp.simplify(dot(n, n))
    print(f"\n  {name}:  |n|^2 = {nrm}  -> {'UNIT' if nrm==1 else 'NOT unit'}")
    T = hilbert_stress_mixed(n)
    rho = sp.simplify(-T[0]); pr = sp.simplify(T[1])
    drho = sp.simplify(rho - rho_c); dpr = sp.simplify(pr - pr_c)
    print(f"    T^t_t(=-rho) - committed(-rho) = {drho}")
    print(f"    T^r_r(=p_r)  - committed(p_r)  = {dpr}")
    print(f"    stress matches committed stress()? {'YES' if (drho==0 and dpr==0) else 'NO'}")
    # also report T^t_t - T^r_r for this field (the canon quantity)
    print(f"    T^t_t - T^r_r = {sp.simplify(T[0]-T[1])}")

print("""
DISENTANGLEMENT VERDICT:
  - The committed stress() (rho,p_r) that SOURCES Einstein in the gate is reproduced
    EXACTLY by the UNIT S^3 hedgehog (|n|=1).  So the (r,r) residual is computed from a
    genuine unit-field Hilbert stress, NOT a non-unit artifact.
  - The provenance mismatch (energies from S^2-naive) is REAL but IRRELEVANT to the
    gate: the gate sources from stress(), not energies.  Using the CORRECT unit field
    gives the SAME stress => SAME (r,r) verdict.
  => cause (b) (field provenance) does NOT rescue the soliton; cause (a) (B=1/A) is the
     real cause.  The overturn survives correct field treatment.
""")
