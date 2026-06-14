"""
INDEPENDENT VERIFIER (blind adversarial) — angular structure of the L2+L4
winding sector, derived FROM SCRATCH with sympy. No reuse of the original
n3_*.py scripts. DATA-BLIND: no lepton numbers, no Koide, no sqrt(2).

Goal:
  (1) Derive INT |v_a|^2 dOmega for the iso-rotation generators v_a = e_a x n
      independently, to check the claimed closed forms:
          INT|v_3|^2 = (8pi/3) sin^2 Theta
          INT|v_1|^2 = INT|v_2|^2 = (4pi/3)(cos 2Theta + 2)
  (2) Build the FULL angular cross-tensor M_ab(Theta) = INT (v_a.v_b) dOmega
      and check it is diagonal -> axial 2+1 vs cyclic Z3.
  (3) Test ALTERNATIVE operationalizations of "the 3 directions":
        - the 3 orbital l=1 m-states (m=-1,0,+1) energy weights
        - is there ANY native choice giving a cyclic (3-equal up to phase) split?
"""
import sympy as sp

th, ph, Th = sp.symbols('theta phi Theta', real=True)

# Easy-axis hedgehog unit vector (settled native carrier). Theta=Theta(r), here
# treated as a parameter at fixed r; angular integral over (theta,phi).
sT, cT = sp.sin(Th), sp.cos(Th)
n1 = sT*sp.sin(th)*sp.cos(ph)
n2 = sT*sp.sin(th)*sp.sin(ph)
n3 = cT
n = sp.Matrix([n1, n2, n3])

# iso-rotation generators v_a = e_a x n
e = [sp.Matrix([1,0,0]), sp.Matrix([0,1,0]), sp.Matrix([0,0,1])]
v = [ea.cross(n) for ea in e]

dOmega = sp.sin(th)  # measure; integrate theta:0..pi, phi:0..2pi

def ang_int(expr):
    inner = sp.integrate(sp.expand_trig(sp.expand(expr*dOmega)), (ph, 0, 2*sp.pi))
    return sp.simplify(sp.integrate(inner, (th, 0, sp.pi)))

print("=== L2 angular integrals INT (v_a . v_b) dOmega ===")
M = sp.zeros(3,3)
for a in range(3):
    for b in range(3):
        M[a,b] = ang_int((v[a].T*v[b])[0])
M = sp.simplify(M)
sp.pprint(M)

print("\nDiagonal entries:")
for a in range(3):
    print(f"  M[{a}{a}] =", sp.simplify(M[a,a]))
print("Off-diagonals (should be 0 for diagonal/axial):")
for a in range(3):
    for b in range(3):
        if a!=b:
            print(f"  M[{a}{b}] =", sp.simplify(M[a,b]))

# Claimed forms:
claim3 = sp.Rational(8,3)*sp.pi*sp.sin(Th)**2
claim1 = sp.Rational(4,3)*sp.pi*(sp.cos(2*Th)+2)
print("\nCheck claimed closed forms:")
print("  M33 - (8pi/3)sin^2Theta =", sp.simplify(M[2,2]-claim3))
print("  M11 - (4pi/3)(cos2Theta+2) =", sp.simplify(M[0,0]-claim1))
print("  M22 - (4pi/3)(cos2Theta+2) =", sp.simplify(M[1,1]-claim1))

print("\nExterior limit Theta->0 (unwound):")
print("  M11(0) =", sp.simplify(M[0,0].subs(Th,0)), " (claim 4pi -> fills cell)")
print("  M33(0) =", sp.simplify(M[2,2].subs(Th,0)), " (claim 0 -> localized)")
print("Core limit Theta->pi:")
print("  M11(pi) =", sp.simplify(M[0,0].subs(Th,sp.pi)))
print("  M33(pi) =", sp.simplify(M[2,2].subs(Th,sp.pi)))

# Is the angular tensor EVER 3-fold (cyclic) for any Theta? Eigen-pattern:
print("\n=== Pattern test: is M_ab ever cyclic-Z3 (3 equal) for any Theta? ===")
diff = sp.simplify(M[0,0]-M[2,2])
print("  M11 - M33 =", diff)
sol = sp.solve(diff, Th)
print("  M11==M33 solutions in Theta:", sol)
print("  -> isotropic only at isolated Theta (full degeneracy), else 2+1 axial.")
