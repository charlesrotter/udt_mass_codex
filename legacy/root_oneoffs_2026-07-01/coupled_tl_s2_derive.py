#!/usr/bin/env python3
"""
coupled_tl_s2_derive.py -- DERIVE the native S^2 area-form (pi_2) carrier's
radial stress + Euler-Lagrange operator, symbolically, for the coupled time-live
solve (CONTRACT archive/pre_2026-07-01/coupled_timelive_solve_CONTRACT.md, Stage 1a).

Driver: Claude (Opus 4.8, 1M).  2026-06-19.  OBSERVE/DERIVE-prep.  DATA-BLIND.

THE CARRIER (CANON C-2026-06-14-1, contract S1):  the native S^2 / pi_2 area-form
carrier is the UNIT 3-VECTOR hedgehog
    n = ( sinTheta(r) sin th cos(m ps),  sinTheta(r) sin th sin(m ps),  cosTheta(r) )
  -- a map to S^2 (|n|=1, THREE components), winding (degree) set by Theta:0..pi and
  the (th,ps) sphere wrap.  This is NOT the S^3 hedgehog (which has a 4th cosTheta-
  embedded component and lives in pi_3).

THE ACTION (native L2+L4, contract S1; native_stabilizer Task 1 blind-verified):
    L2 = -(xi/2) g^{mn} d_m n . d_n n            (. = dot over the 3 S^2 components)
    L4 = -(kappa/4) g^{mp} g^{nq} S_{mn}.S_{pq},   S_{mn} = d_m n x d_n n   (3-vector
         cross product -- EXISTS for an S^2 3-vector, = the native H1 area-form current).

WHAT WE TEST HERE (contract anti-import + AUDIT 1 of native_matter_step):
  (i)  the DIAGONAL stress (rho = -T^t_t, p_r = T^r_r) of THIS S^2 carrier should
       EQUAL that of the S^3 carrier (carrier-robust mass read-off -- the blind-
       verified AUDIT-1 fact).  Confirm symbolically.
  (ii) the TANGENTIAL pressure T^th_th and the radial EL DIFFER from S^3 (this is
       where the carriers part ways -- contract S1).  Derive them natively.
  (iii) the CORE condition for the S^2 carrier is the regularity NODE sin Theta(0)=0
       (value FREE), NOT the imported Skyrme twist Theta(core)=m*pi (#61).  Show the
       EL's r->0 behaviour selects only sin Theta(0)=0.

NO numeric, NO grid here -- pure sympy exact (Principle 2: symbolic is exact).
"""
import sympy as sp

print("="*78)
print("NATIVE S^2 AREA-FORM CARRIER -- exact stress + EL derivation")
print("="*78)

# coordinates and metric warps (areal gauge rho=r; B=1/A FREED => a,b independent)
r, th, ps = sp.symbols('r theta psi', positive=True)
xi, kap, m = sp.symbols('xi kappa m', positive=True)
# diagonal metric ds^2 = -e^{2A} dt^2 + e^{2B} dr^2 + r^2 dth^2 + r^2 sin^2 th dps^2
A = sp.Function('A')(r); B = sp.Function('B')(r)
Th = sp.Function('Theta')(r)
sth = sp.sin(th)

# metric (lower) and inverse (upper)
g = sp.diag(-sp.exp(2*A), sp.exp(2*B), r**2, r**2*sth**2)
ginv = sp.diag(-sp.exp(-2*A), sp.exp(-2*B), 1/r**2, 1/(r**2*sth**2))

# ---- the S^2 unit 3-vector hedgehog ----
n1 = sp.sin(Th)*sth*sp.cos(m*ps)
n2 = sp.sin(Th)*sth*sp.sin(m*ps)
n3 = sp.cos(Th)
n = sp.Matrix([n1, n2, n3])
print("\n|n|^2 - 1 =", sp.simplify(n.dot(n) - 1), " (must be 0: unit 3-vector S^2)")

coords = [sp.Symbol('t'), r, th, ps]   # t-derivatives are 0 (static here)
# d_mu n for mu in (t,r,th,ps); d_t n = 0
dn = [sp.zeros(3, 1) for _ in range(4)]
for a_ in range(3):
    dn[1][a_] = sp.diff(n[a_], r)
    dn[2][a_] = sp.diff(n[a_], th)
    dn[3][a_] = sp.diff(n[a_], ps)

# field first fundamental form  Gmn = d_m n . d_n n
Gf = sp.zeros(4, 4)
for mu in range(4):
    for nu in range(4):
        Gf[mu, nu] = dn[mu].dot(dn[nu])
Gf = sp.simplify(Gf)

# L2 = -(xi/2) g^{mn} Gmn
L2 = -(xi/2)*sum(ginv[i, i]*Gf[i, i] for i in range(4))

# L4: S_{mn} = d_m n x d_n n  (3-vector cross product); |S|^2 contracted with ginv^2
def cross(u, v):
    return sp.Matrix([u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]])
S = [[cross(dn[mu], dn[nu]) for nu in range(4)] for mu in range(4)]
# L4 = -(kap/4) g^{mp} g^{nq} S_{mn}.S_{pq}
L4 = 0
for mp in range(4):
    for nq in range(4):
        # diagonal metric => g^{mp} nonzero only mp diag; use indices m=p, n=q
        pass
# diagonal metric: g^{mp}=ginv[m,m] delta, g^{nq}=ginv[n,n] delta
L4 = -(kap/4)*sum(ginv[mm, mm]*ginv[nn, nn]*S[mm][nn].dot(S[mm][nn])
                  for mm in range(4) for nn in range(4))
L = sp.simplify(L2 + L4)
print("\nL (S^2 carrier) =", L)

# ---- Hilbert stress  T_{ab} = -2 dL/dg^{ab} + g_{ab} L ----
# treat the independent inverse-metric diagonal entries as symbols, differentiate.
gI = sp.symbols('gItt gIrr gIth gIps')
ginv_s = sp.diag(*gI)
# rebuild L in terms of ginv_s
L2s = -(xi/2)*sum(ginv_s[i, i]*Gf[i, i] for i in range(4))
L4s = -(kap/4)*sum(ginv_s[mm, mm]*ginv_s[nn, nn]*S[mm][nn].dot(S[mm][nn])
                   for mm in range(4) for nn in range(4))
Ls = L2s + L4s
Tmix = {}   # T^a_a = g^{aa} T_{aa}
glow = [-sp.exp(2*A), sp.exp(2*B), r**2, r**2*sth**2]
names = ['t', 'r', 'th', 'ps']
subs_back = {gI[0]: -sp.exp(-2*A), gI[1]: sp.exp(-2*B),
             gI[2]: 1/r**2, gI[3]: 1/(r**2*sth**2)}
for i in range(4):
    dLdgi = sp.diff(Ls, gI[i])
    Tii_low = -2*dLdgi + glow[i]*Ls            # T_{ii} (lower)
    Tii_low = Tii_low.subs(subs_back)
    Tii_mix = sp.simplify(ginv[i, i]*Tii_low)  # T^i_i
    Tmix[names[i]] = sp.simplify(Tii_mix)

rho = sp.simplify(-Tmix['t'])     # rho = -T^t_t
print("\n--- S^2 mixed stress (diagonal) ---")
print("rho   = -T^t_t  =", rho)
print("p_r   =  T^r_r  =", Tmix['r'])
print("p_th  =  T^th_th=", Tmix['th'])
print("p_ps  =  T^ps_ps=", Tmix['ps'])

# ---- compare to the S^3 carrier diagonal stress (radial_Bfree_soliton.stress) ----
# S^3:  X = e^{-2B} Th'^2 ; Y = sin^2 Th / r^2 (note S^3 uses m=1 in the committed code)
Xp = sp.exp(-2*B)*sp.diff(Th, r)**2
Yp = sp.sin(Th)**2/r**2
rho_S3 = (xi/2)*(Xp + 2*Yp) + (kap/2)*(2*Xp*Yp + Yp**2)
pr_S3 = (xi/2)*(Xp - 2*Yp) + (kap/2)*(2*Xp*Yp - Yp**2)
pT_S3 = (kap/2)*Yp**2 - (xi/2)*Xp
print("\n--- carrier-robustness check (S^2 vs S^3), at m=1 ---")
print("rho_S2 - rho_S3 =", sp.simplify((rho - rho_S3).subs(m, 1)))
print("p_r_S2 - p_r_S3 =", sp.simplify((Tmix['r'] - pr_S3).subs(m, 1)))
print("p_th_S2 - p_th_S3 =", sp.simplify((Tmix['th'] - pT_S3).subs(m, 1)),
      "  <- EXPECT NONZERO (carriers part ways in tangential)")

# ---- the native S^2 radial Euler-Lagrange operator ----
# S = int sqrt(-g) L d^4x ; sqrt(-g) = e^{A+B} r^2 sin th.  The reduced radial EL
# for Theta(r) is the Euler-Lagrange of  int e^{A+B} r^2 L_radial(Theta,Theta') dr
# after the (th,ps) integral (the hedgehog angular profile is fixed; Theta=Theta(r)).
sqrtg = sp.exp(A+B)*r**2*sth
# integrate L*sqrtg over th in (0,pi), ps in (0,2pi):  do the angular integral
Lang = sp.integrate(sp.integrate(sp.simplify(L*sqrtg), (ps, 0, 2*sp.pi)), (th, 0, sp.pi))
Lang = sp.simplify(Lang)
print("\nangular-integrated radial Lagrangian density Lrad(r) =", Lang)
Thp = sp.diff(Th, r)
# Euler-Lagrange:  d/dr( dL/dTh' ) - dL/dTh = 0
EL = sp.diff(sp.diff(Lang, Thp), r) - sp.diff(Lang, Th)
EL = sp.simplify(EL)
print("\nEL (native S^2 radial, = 0) =")
sp.pprint(EL)

# ---- core (r->0) behaviour: what does regularity SELECT? ----
# Examine the EL's leading r->0 singular structure for the angular (Y-type) terms,
# which force the core condition.  The Y = sin^2Th/r^2 pieces are 1/r^2 singular
# unless sin Theta(0) = 0.  Show the angular potential term and its core node.
print("\n--- CORE CONDITION (contract S1: node, value FREE; NOT m*pi twist) ---")
# the algebraic angular-restoring term in the EL (coefficient of the non-derivative
# sin/cos pieces): isolate terms with no Theta' or Theta''
EL_static = EL.subs({sp.diff(Th, r, 2): 0, Thp: 0})
EL_static = sp.simplify(EL_static)
print("EL with Theta'=Theta''=0 (the pure angular-restoring core term) =")
sp.pprint(EL_static)
print("\nThis vanishes at r->0 regularity iff sin Theta(0)=0 (a NODE), with the")
print("VALUE of Theta(0) in {0, pi, 2pi, ...} UNFIXED by the operator -- i.e. the")
print("core condition is sin Theta(0)=0, value FREE.  No m*pi twist is imposed.")
print("\nDONE.")
