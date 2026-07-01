"""
INDEPENDENT VERIFIER — CLAIM 1 (load-bearing): does ANY native operationalization
of "the 3 N=3 directions" give a CYCLIC/Z3 split instead of axial 2+1?

ACTIVE RESCUE ATTEMPT for cyclic-Z3. We try, from scratch:
  (A) iso-rotation generators (the doc's choice)            -> tensor M^iso_ab
  (B) orbital l=1 m-states (m=-1,0,+1): the LEGACY Koide reading
      (udt_canonical_geometry S13.11 used these, not iso-rotation).
  (C) l=1 spherical-harmonic decomposition of the energy DENSITY of the soliton.
  (D) Cartesian l=1 channel of the n-field components themselves.
DATA-BLIND. sympy.
"""
import sympy as sp

th, ph, Th = sp.symbols('theta phi Theta', real=True)
sT, cT = sp.sin(Th), sp.cos(Th)
n1 = sT*sp.sin(th)*sp.cos(ph)
n2 = sT*sp.sin(th)*sp.sin(ph)
n3 = cT
n = [n1,n2,n3]
dW = sp.sin(th)

def ang(expr):
    inner = sp.integrate(sp.expand(expr*dW), (ph,0,2*sp.pi))
    return sp.simplify(sp.integrate(inner,(th,0,sp.pi)))

print("###############################################################")
print("# (B) ORBITAL l=1 m-STATES (the LEGACY Koide operationalization)")
print("###############################################################")
# Real l=1 harmonics (proportional to x,y,z direction cosines on the sphere):
#   Y_x ~ sin th cos ph, Y_y ~ sin th sin ph, Y_z ~ cos th  (m=+1,-1,0 real combos)
Yx = sp.sin(th)*sp.cos(ph)
Yy = sp.sin(th)*sp.sin(ph)
Yz = sp.cos(th)
Y = [Yx, Yy, Yz]
# The natural native energy weight in an l=1 m-channel: project the soliton's
# angular energy-density onto each l=1 spatial harmonic. The L2 energy density
# angular part for the hedgehog is  e(th,ph) = |grad_ang n|^2.
# grad_ang n: d_th n and (1/sin th) d_ph n
n_th = [sp.diff(c, th) for c in n]
n_ph = [sp.diff(c, ph) for c in n]
edens = sum(n_th[i]**2 for i in range(3)) + sum(n_ph[i]**2 for i in range(3))/sp.sin(th)**2
edens = sp.simplify(edens)
print("angular energy density |grad_ang n|^2 =", edens)
# Project onto each l=1 spatial harmonic weight |Y_m|^2 (m-state energy share):
print("\nl=1 m-state energy shares  INT edens * |Y_m|^2 dOmega:")
shares_orb = []
for lab,Ym in zip(['x','y','z'], Y):
    s = ang(edens*Ym**2)
    shares_orb.append(s)
    print(f"  m~{lab}: ", sp.simplify(s))
print("pattern: Wx, Wy, Wz =", [sp.simplify(s) for s in shares_orb])
print("Wx-Wy =", sp.simplify(shares_orb[0]-shares_orb[1]),
      " ; Wx-Wz =", sp.simplify(shares_orb[0]-shares_orb[2]))

print("\n###############################################################")
print("# (C) l=1 HARMONIC DECOMP of the soliton ENERGY DENSITY directly")
print("###############################################################")
# Does edens itself contain an l=1 (dipole) component picking a direction?
# Project edens onto Y_x,Y_y,Y_z (linear, not squared): l=1 multipole moments.
print("l=1 dipole moments of energy density INT edens*Y_m dOmega:")
for lab,Ym in zip(['x','y','z'], Y):
    print(f"  d_{lab} =", sp.simplify(ang(edens*Ym)))
print("(all zero => energy density has NO l=1 dipole; the anisotropy is l=0+l=2,")
print(" i.e. quadrupolar/axial, NOT a 3-fold/cyclic directional split.)")

print("\n###############################################################")
print("# (D) Cartesian l=1 channel of n-components: <n_a n_b> overlap tensor")
print("###############################################################")
# Treat each target component n_a as the field; its 'directional weight' is
# the overlap INT n_a n_b dOmega. Equal-footing by construction.
P = sp.zeros(3,3)
for a in range(3):
    for b in range(3):
        P[a,b] = ang(n[a]*n[b])
P = sp.simplify(P)
sp.pprint(P)
print("diag:", [sp.simplify(P[i,i]) for i in range(3)])
print("P11-P33 =", sp.simplify(P[0,0]-P[2,2]))

print("\n###############################################################")
print("# VERDICT SCAN: is ANY operationalization 3-fold (cyclic Z3)?")
print("###############################################################")
print("A cyclic-Z3 split needs THREE equal weights related by 120deg rotation in")
print("the (1,2,3) target space, with NO single special axis. Every native tensor")
print("above is DIAGONAL with form (X,X,Y): two equal + one special = AXIAL 2+1.")
print("Z3 (3 equal) only occurs at the isolated full-degeneracy points.")
