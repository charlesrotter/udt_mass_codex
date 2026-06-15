#!/usr/bin/env python3
"""
matter_ansatz_derive.py -- EXACT symbolic determination of the matter-field ansatz
behind the committed native L2+L4 reduced stress (rho,p_r) and angular-integrated
radial energies (E2_r,E4_r).

Driver: Claude (Opus 4.8, 1M).  2026-06-15.  DATA-BLIND.  xi,kappa free positive
symbols (structural match, sympy simplify==0; not numerical).

Action (settled, native):
  L2 = -(xi/2)    g^{mn} d_m n . d_n n
  L4 = -(kappa/4) g^{mp} g^{nq} S_{mn}.S_{pq}
  Skyrme term S_mn.S_pq via the Lagrange identity (valid for ANY target dim):
     S_mn.S_pq = (d_m n.d_p n)(d_n n.d_q n) - (d_m n.d_q n)(d_n n.d_p n)
n a unit vector into the target sphere.

Reduced metric:  ds^2 = -e^{-2phi}dt^2 + e^{2phi}dr^2 + r^2(dth^2 + sin^2 th dps^2)
sqrt(-g) = r^2 sin th ;  static spatial measure  sqrt(g_3) = e^{phi} r^2 sin th.
For a STATIC field the energy density is -T^t_t.

COMMITTED ground truth (native_stabilizer_results.md / complete_metric_batched.py):
  X = e^{-2phi}Theta'^2 ,  Y = sin^2(Theta)/r^2
  rho = (xi/2)(X+2Y) + (kappa/2)(2XY + Y^2)
  p_r =  (xi/2)(X-2Y) + (kappa/2)(2XY - Y^2)
  E2_r = (2 pi xi /3) e^{-phi}[ r^2 sin^2T T'^2 + 2 r^2 T'^2 + 4 e^{2phi} sin^2T ]
  E4_r = (2 pi kap/3) e^{-phi}[ (2 r^2 sin^4T + 2 r^2 sin^2T)T'^2 + e^{2phi} sin^4T ]/r^2

CANDIDATE ANSAetze tested (all degree-1, charge fixed by Theta(core)=pi->Theta(seal)=0):
  S2_naive   : N  = (sinTh sinth cosps, sinTh sinth sinps, cosTh)         [|N|!=1]
  S2_unit    : n  = N/|N|                                                  [|n|=1, S^2]
  S3_skyrme  : n4 = (sinTh sinth cosps, sinTh sinth sinps, sinTh costh, cosTh)
               [|n4|=1, the SU(2)/S^3 chiral Skyrme hedgehog]

RESULT (proved below, simplify==0):
  * S3_skyrme reproduces the committed POINTWISE STRESS (rho,p_r) EXACTLY,
    pointwise in theta -- no equatorial restriction.  It is a genuine unit vector.
  * S2_naive reproduces the committed ANGULAR-INTEGRATED ENERGIES (E2_r,E4_r)
    EXACTLY (density -L, measure e^{phi}r^2 sin th) -- but is NOT unit.
  * The two committed objects therefore come from TWO DIFFERENT fields: the engine
    uses the S^3-hedgehog stress and the S^2-hedgehog energy.  They are NOT mutually
    consistent (S3 energy != committed E; S2 stress != committed (rho,p_r)).
  This is the load-bearing finding: the committed reduced stress is the SU(2)/S^3
  Skyrme hedgehog; the energies were banked from the (non-unit) S^2 m-winding form.
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
meas = sp.exp(phi)*r**2*sp.sin(th)          # static proper measure

def dot(a, b): return (a.T*b)[0]

def derivs(n):
    d = len(n)
    return [sp.Matrix([sp.diff(n[k], c) for k in range(d)]) for c in coords]

def Lagrangians(n):
    """L2, L4 (Lagrange-identity Skyrme, any target dim) on the UDT metric."""
    dn = derivs(n)
    gg = [[dot(dn[m], dn[k]) for k in range(4)] for m in range(4)]
    L2 = -(xi/2)*sum(gi[m, m]*gg[m][m] for m in range(4))
    L4 = -(kap/4)*sum(gi[m, m]*gi[k, k]*(gg[m][m]*gg[k][k] - gg[m][k]*gg[k][m])
                      for m in range(4) for k in range(4))
    return sp.simplify(L2), sp.simplify(L4)

def hilbert_stress(n):
    """Diagonal mixed Hilbert stress T^mu_mu (Lagrange-identity Skyrme)."""
    G = sp.symbols('G0 G1 G2 G3', real=True)
    Gm = sp.diag(*G); Gimat = Gm.inv()
    dn = derivs(n)
    gg = [[dot(dn[m], dn[k]) for k in range(4)] for m in range(4)]
    L2 = -(xi/2)*sum(Gm[m, m]*gg[m][m] for m in range(4))
    L4 = -(kap/4)*sum(Gm[m, m]*Gm[k, k]*(gg[m][m]*gg[k][k] - gg[m][k]*gg[k][m])
                      for m in range(4) for k in range(4))
    L = L2 + L4
    sub = {G[i]: gi[i, i] for i in range(4)}
    return {i: sp.simplify(gi[i, i]*((-2*sp.diff(L, G[i]) + Gimat[i, i]*L).subs(sub)))
            for i in range(4)}

def angint(dens):
    e = sp.expand(dens*meas)
    return sp.simplify(sp.integrate(sp.integrate(e, (ps, 0, 2*sp.pi)), (th, 0, sp.pi)))

# committed targets
X = sp.exp(-2*phi)*Thp**2
Y = sp.sin(Th)**2/r**2
rho_c = (xi/2)*(X+2*Y) + (kap/2)*(2*X*Y + Y**2)
pr_c = (xi/2)*(X-2*Y) + (kap/2)*(2*X*Y - Y**2)
E2_c = (2*sp.pi*xi/3)*sp.exp(-phi)*(r**2*sp.sin(Th)**2*Thp**2 + 2*r**2*Thp**2
                                    + 4*sp.exp(2*phi)*sp.sin(Th)**2)
E4_c = (2*sp.pi*kap/3)*sp.exp(-phi)*((2*r**2*sp.sin(Th)**4 + 2*r**2*sp.sin(Th)**2)*Thp**2
                                     + sp.exp(2*phi)*sp.sin(Th)**4)/r**2

Nraw = sp.Matrix([sp.sin(Th)*sp.sin(th)*sp.cos(ps),
                  sp.sin(Th)*sp.sin(th)*sp.sin(ps),
                  sp.cos(Th)])
# (S2_unit = Nraw/|Nraw| is the genuine-unit S^2 map; its symbolic Hilbert L4 is
#  extremely slow and it reproduces NEITHER committed object, so it is omitted from
#  the production run.  The decisive two ansaetze are below.)
ansatze = {
    'S2_naive': Nraw,
    'S3_skyrme': sp.Matrix([sp.sin(Th)*sp.sin(th)*sp.cos(ps),
                            sp.sin(Th)*sp.sin(th)*sp.sin(ps),
                            sp.sin(Th)*sp.cos(th),
                            sp.cos(Th)]),
}

summary = {}
for name, n in ansatze.items():
    print("\n" + "#"*72)
    print("# ANSATZ:", name, "  components:", list(n))
    print("#"*72)
    nrm = sp.simplify(dot(n, n))
    print("|n|^2 =", nrm, " ->", "UNIT" if nrm == 1 else "NOT unit")

    # --- pointwise stress (full theta), equate to committed pointwise ---
    T = hilbert_stress(n)
    rho = sp.simplify(-T[0]); pr = sp.simplify(T[1])
    drho = sp.simplify(rho - rho_c); dpr = sp.simplify(pr - pr_c)
    stress_ok = (drho == 0 and dpr == 0)
    print("rho - committed (pointwise) =", drho)
    print("p_r - committed (pointwise) =", dpr)

    # --- angular-integrated energies (density -L) ---
    L2, L4 = Lagrangians(n)
    E2 = angint(-L2); E4 = angint(-L4)
    dE2 = sp.simplify(E2 - E2_c); dE4 = sp.simplify(E4 - E4_c)
    energy_ok = (dE2 == 0 and dE4 == 0)
    print("E2_r - committed =", dE2)
    print("E4_r - committed =", dE4)

    summary[name] = (nrm == 1, stress_ok, energy_ok)

print("\n" + "="*72)
print("SUMMARY  (ansatz : unit? | pointwise stress matches | energies match)")
print("="*72)
for name, (u, s, e) in summary.items():
    print(f"  {name:11s}: unit={u!s:5s} | stress={'PASS' if s else 'FAIL':4s} | "
          f"energy={'PASS' if e else 'FAIL'}")
print("""
CONCLUSION:
  Committed POINTWISE stress (rho,p_r)  <==  S3_skyrme  (UNIT SU(2)/S^3 hedgehog)
      n = ( sinTheta(r) sin th cos ps,
            sinTheta(r) sin th sin ps,
            sinTheta(r) cos th,
            cosTheta(r) )                      |n| = 1, exact, pointwise in theta.
  Committed ENERGIES (E2_r,E4_r)        <==  S2_naive   (non-unit m-winding form).
  The two committed objects are from DIFFERENT fields -- the unit ansatz to code
  into a general 3-D solver is the S3_skyrme hedgehog (reproduces the stress that
  sources phi exactly); the banked E2_r,E4_r belong to the S^2 non-unit reduction
  and do NOT equal the S3 hedgehog's integrated energy (flagged, not patched).
""")
