"""
native_skyrme_derive.py  -- TASK 1 (make-or-break).

Is the Skyrme four-derivative term NATIVE = the UDT-metric norm of OUR OWN
derived H1 area-form / topological winding 2-form?

We DERIVE, never assert. Two objects:

  (A) the winding/topological current 2-form built from omega_H1:
        F_{mn} = eps_{abc} n_a d_m n_b d_n n_c  =  n . (d_m n x d_n n)   [scalar 2-form]
      Its UDT-metric norm:
        |F|^2_g = g^{mp} g^{nq} F_{mn} F_{pq}

  (B) the standard Skyrme/Faddeev four-derivative term (VECTOR cross product
      contracted with itself):
        S_{mn} := d_m n x d_n n   (3-vector valued antisym 2-form)
        L4_std = -(kappa/4) g^{mp} g^{nq} S_{mn} . S_{pq}

Question: is |F|^2_g == g^{mp}g^{nq} S_{mn}.S_{pq} (up to normalization), as an
IDENTITY on the constraint surface |n|=1 ?  If yes, the Skyrme term is the
metric-norm of our own omega_H1 current and is NATIVE.

We test the IDENTITY  S_{mn}.S_{pq}  vs  F_{mn} F_{pq}  fully symbolically with a
GENERAL n(x) satisfying |n|=1, then contract with the UDT inverse metric.
"""
import sympy as sp

print("="*70)
print("TASK 1: is Skyrme L4 = |omega_H1 current|^2_g  (NATIVE)?")
print("="*70)

# ---- General unit 3-vector field n(x) and its first derivatives ----
# Coordinates x^m, m=0..3 (t,r,theta,phi). We work index-free in target space:
# treat n and its partials d_m n as independent symbolic 3-vectors subject ONLY
# to the constraint |n|^2=1 (=> n . d_m n = 0).  We verify the pointwise tensor
# identity between the two 2-forms; metric contraction is linear and added after.

# Represent each d_m n (m a spacetime index) as a free 3-vector.
def vec(name):
    return sp.Matrix(3,1, lambda i,_: sp.Symbol(f'{name}{i}', real=True))

n   = vec('n')
# four spacetime directions
dn  = [vec(f'd{m}n') for m in range(4)]   # dn[m] = d_m n  (3-vector)

def cross(a,b):
    return sp.Matrix([
        a[1]*b[2]-a[2]*b[1],
        a[2]*b[0]-a[0]*b[2],
        a[0]*b[1]-a[1]*b[0]])

def dot(a,b):
    return (a.T*b)[0,0]

# Constraint surface |n|=1: enforce n.d_m n = 0.  We substitute n[2] dependent
# and d_m n's component to satisfy constraints numerically/symbolically later;
# for the ALGEBRAIC identity we use the off-shell vector identity then impose
# n.dn=0 and |n|=1.

# (A) scalar 2-form component F_{mn} = n . (d_m n x d_n n)
def F(m,k):
    return dot(n, cross(dn[m], dn[k]))

# (B) vector 2-form S_{mn} = d_m n x d_n n ; Skyrme uses S_{mn}.S_{pq}
def S(m,k):
    return cross(dn[m], dn[k])

# ---- The KEY algebraic identity (Lagrange / BAC-CAB based) ----
# For ANY 3-vectors, (a x b).(c x d) = (a.c)(b.d) - (a.d)(b.c).
# We want to compare, for the FULLY CONTRACTED scalars that appear in each
# Lagrangian, S_{mn}.S^{mn}  vs  F_{mn}F^{mn} (metric raised). First establish
# the pointwise relation between S_{mn}.S_{pq} and F_{mn},F_{pq}.

# Decompose d_m n in the basis {n, e1, e2} where e1,e2 span the tangent plane.
# On the constraint surface d_m n is TANGENT (n.d_m n=0), so d_m n lies in the
# 2-plane orthogonal to n. Write d_m n = a_m e1 + b_m e2 with {n,e1,e2} ON.
print("\n[1] Reduce to tangent-plane components (|n|=1 => d_m n _|_ n).")
a = sp.symbols('a0:4', real=True)   # e1-components of d_m n
b = sp.symbols('b0:4', real=True)   # e2-components of d_m n
# orthonormal triad n,e1,e2:
N  = sp.Matrix([0,0,1]); E1=sp.Matrix([1,0,0]); E2=sp.Matrix([0,1,0])
dnt = [a[m]*E1 + b[m]*E2 for m in range(4)]   # tangent d_m n

def Ft(m,k):  return dot(N, cross(dnt[m], dnt[k]))
def St(m,k):  return cross(dnt[m], dnt[k])

# Compare S_{mn}.S_{pq} with F_{mn} F_{pq} for all index pairs:
print("\n[2] Pointwise tensor identity  S_{mn}.S_{pq}  vs  F_{mn} F_{pq}:")
all_equal = True
for m in range(4):
    for k in range(4):
        for p in range(4):
            for q in range(4):
                lhs = sp.expand(dot(St(m,k), St(p,q)))
                rhs = sp.expand(Ft(m,k)*Ft(p,q))
                if sp.simplify(lhs-rhs) != 0:
                    all_equal=False
                    if (m,k,p,q) in [(0,1,0,1),(0,1,2,3),(1,2,1,2)]:
                        print(f"  MISMATCH ({m}{k},{p}{q}): S.S - FF = {sp.simplify(lhs-rhs)}")
print(f"  S_{{mn}}.S_{{pq}} == F_{{mn}} F_{{pq}}  for ALL index pairs: {all_equal}")

# ---- Now contract with the UDT inverse metric ----
print("\n[3] Contract both with the UDT inverse metric.")
phi, r, th, c, kappa, xi = sp.symbols('phi r theta c kappa xi', real=True, positive=True)
# ds^2 = -e^{-2phi}c^2 dt^2 + e^{2phi}dr^2 + r^2 dth^2 + r^2 sin^2 th dphi^2
g_dn = sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
g_up = g_dn.inv()
print("  g^{mn} diag =", [sp.simplify(g_up[i,i]) for i in range(4)])

# scalar norms (sum over m<n with factor 2, full contraction):
def norm_FF():
    tot = 0
    for m in range(4):
        for k in range(4):
            for p in range(4):
                for q in range(4):
                    tot += g_up[m,p]*g_up[k,q]*Ft(m,k)*Ft(p,q)
    return sp.expand(tot)

def norm_SS():
    tot = 0
    for m in range(4):
        for k in range(4):
            for p in range(4):
                for q in range(4):
                    tot += g_up[m,p]*g_up[k,q]*dot(St(m,k),St(p,q))
    return sp.expand(tot)

FF = norm_FF()
SS = norm_SS()
print("\n[4] g^{mp}g^{nq} F_{mn}F_{pq}  -  g^{mp}g^{nq} S_{mn}.S_{pq} =",
      sp.simplify(FF-SS))

print("\n  => Skyrme L4_std = -(kappa/4) g^{mp}g^{nq} S_{mn}.S_{pq}")
print("     |omega_H1 current|^2_g = g^{mp}g^{nq} F_{mn}F_{pq}")
print("     IDENTICAL up to the (kappa/4) normalization?  ",
      sp.simplify(FF-SS)==0)

# ---- sanity: the famous 'completeness' relation L4 = (1/2)[(tr L_mn)^2 - tr(L_mn^2)] ----
print("\n[5] CONCLUSION printed in results doc. Identity holds iff [2] and [4] both 0.")
