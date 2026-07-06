"""
NO-SELECTOR AUDIT — CAS (sympy, exact, bounded; NO PDE solve, NO data).
Load-bearing steps:
  T1  equivariance lock of the standard Hopf map (spatial torus axis <-> target n_inf axis)
  T2  manifest target-SO(3) invariance of L2 (|dn|^2) and L4 (Skyrme F_ij), and absence of V_ab n_a n_b
  T3  n_inf is a gauge choice; charge readout is target-SO(3) scalar
  T4  the induced-shear source (stress) is a TARGET-SCALAR (target-blind), and the single-channel
      readout requires a fixed axis a (breaks SO(3)); the summed readout = degree.
Data-blind: no lepton/hadron numbers. 1/3 appears only as an END check, never as an input.
"""
import sympy as sp

print("="*72)
print("T2 — manifest target-SO(3) invariance of L2 and L4 (finite rotation)")
print("="*72)

# General SO(3) rotation via Rodrigues about a generic axis, angle a.
a = sp.symbols('a', real=True)
ux,uy,uz = sp.symbols('ux uy uz', real=True)
# normalize axis symbolically later; use a concrete generic axis to keep it exact & fast:
# use axis (1,2,3)/sqrt(14) and a symbolic angle a -> R in SO(3), det=1
import sympy
u = sp.Matrix([1,2,3]); u = u/ sp.sqrt(u.dot(u))
K = sp.Matrix([[0,-u[2],u[1]],[u[2],0,-u[0]],[-u[1],u[0],0]])
R = sp.eye(3) + sp.sin(a)*K + (1-sp.cos(a))*(K*K)
R = sp.simplify(R)
print("det(R) =", sp.simplify(R.det()), " (SO(3) => +1)")
print("R^T R - I =", sp.simplify(R.T*R - sp.eye(3)))

# n and its two spatial derivatives as generic target vectors (unconstrained algebra check
# of the CONTRACTION structure; |n|=1 not needed for invariance of the contractions).
n   = sp.Matrix(sp.symbols('n1 n2 n3', real=True))
di  = sp.Matrix(sp.symbols('p1 p2 p3', real=True))   # d_i n
dj  = sp.Matrix(sp.symbols('q1 q2 q3', real=True))   # d_j n

# L2 core: dn . dn  (contract with delta_ab). Rotate all three vectors by same R.
L2      = di.dot(di)
L2_rot  = (R*di).dot(R*di)
print("\nL2 |d_i n|^2 invariant:", sp.simplify(L2_rot - L2) == 0)

# L4 core: F_ij = n . (d_i n x d_j n) = eps_abc n_a p_b q_c  (scalar triple product)
F      = n.dot(di.cross(dj))
F_rot  = (R*n).dot((R*di).cross(R*dj))
print("L4 F_ij = n.(d_i n x d_j n) invariant:", sp.simplify(F_rot - F) == 0)
# also the SQUARE (what enters the action)
print("L4 (F_ij)^2 invariant:", sp.simplify(F_rot**2 - F**2) == 0)

# --- L4 SKYRME HILBERT STRESS invariance (verifier a28..-added: the load-bearing P2 term,
#     which the first CAS asserted but did not compute). Three spatial derivatives d1,d2,d3;
#     F_ij = n.(d_i n x d_j n) (target scalar per pair i,j). Skyrme stress spatial block
#     T4_ij = sum_k F_ik F_jk - (1/4) delta_ij sum_{kl} F_kl^2. Each component must be
#     target-SO(3) invariant because every F carries NO free target index.
dd = [sp.Matrix(sp.symbols('a1 a2 a3', real=True)),
      sp.Matrix(sp.symbols('b1 b2 b3', real=True)),
      sp.Matrix(sp.symbols('c1 c2 c3', real=True))]
def Fpair(i, j, N, D): return N.dot(D[i].cross(D[j]))
def T4(i, j, N, D):
    cross_term = sum(Fpair(i, k, N, D)*Fpair(j, k, N, D) for k in range(3))
    trace = sum(Fpair(k, l, N, D)**2 for k in range(3) for l in range(3))
    return cross_term - (sp.Rational(1, 4)*trace if i == j else 0)
ok_T4 = all(sp.simplify(T4(i, j, R*n, [R*d for d in dd]) - T4(i, j, n, dd)) == 0
            for (i, j) in [(0, 0), (0, 1), (1, 2), (2, 2)])
print("L4 Skyrme stress T4_ij (00,01,12,22) all target-SO(3) invariant:", ok_T4,
      " => the Skyrme stress carries NO free target index (P2 holds for L4).")

print("""
=> The ONLY target tensors in L2+L4 are delta_ab (in |dn|^2) and eps_abc (in F),
   the unique SO(3)-invariant rank-2 and rank-3 tensors. No V_ab n_a n_b with V!~delta
   appears; adding one is the only way to break the target SO(3) (=> outcome C).""")

# Infinitesimal check of the delta-contraction anti-symmetry (why no linear anisotropy survives)
th = sp.Matrix(sp.symbols('t1 t2 t3', real=True))
def cross(A,B): return A.cross(B)
dn = cross(th, n)              # infinitesimal rotation delta n = theta x n
# delta(n_a n_a) = 2 n . (theta x n) = 0 identically:
print("\ndelta(|n|^2) under rotation =", sp.simplify( (2*n.dot(cross(th,n))) ), " (=> |n|^2 rot-invariant)")

print("\n"+"="*72)
print("T1 — equivariance lock: standard Hopf map, spatial z-rotation = target pole-rotation")
print("="*72)
x,y,z,al = sp.symbols('x y z alpha', real=True)
r2 = x**2 + y**2 + z**2
I  = sp.I
# Standard degree-1 Hopf map, target stereographic coordinate w = (n1+i n2)/(1-n3),
# n_inf = north pole (0,0,1) at spatial infinity:
w  = (2*(x + I*y)) / (r2 - 1 + 2*I*z)
# spatial rotation about z-axis by alpha: (x,y)->(x cos - y sin, x sin + y cos), z,r fixed
xr = x*sp.cos(al) - y*sp.sin(al)
yr = x*sp.sin(al) + y*sp.cos(al)
w_sprot = w.subs({x:xr, y:yr}, simultaneous=True)
# claim: w_sprot = exp(i alpha) * w   (a target rotation about the pole axis by alpha)
# NB (verifier a28..): must .rewrite(cos) so exp(i*alpha) expands to trig before simplify,
# else sympy prints a nonzero residual against the "=0" claim.
claim = sp.simplify((w_sprot - sp.exp(I*al)*w).rewrite(sp.cos))
print("w(R_z(alpha) x) - e^{i alpha} w(x) =", claim, " (0 => spatial z-rot == target pole-rot)")
# control: the OPPOSITE sense e^{-i alpha} is NOT a symmetry (nonzero => direction is fixed)
ctrl = sp.simplify((w_sprot - sp.exp(-I*al)*w).rewrite(sp.cos))
print("control w(R_z(alpha) x) - e^{-i alpha} w(x) =", "0" if ctrl == 0 else "nonzero",
      " (nonzero => the lock fixes the RELATIVE sense, not an absolute axis)")

print("""
=> A spatial rotation about the torus/symmetry axis is IDENTICAL to a target rotation
   about n_inf. The hopfion is invariant under the DIAGONAL SO(2) (a lock of the RELATIVE
   spatial<->target orientation), NOT a pinning of any absolute axis.""")

print("\n"+"="*72)
print("T3/T1b — n_inf and the spatial torus axis are BOTH free moduli (co-rotate)")
print("="*72)
# A general spatial rotation moves the torus axis over a full S^2; via equivariance the
# target pole n_inf moves over a full S^2 too. Demonstrate: rotate the whole map about the
# x-axis by beta -> the field is a NEW hopfion with a TILTED torus axis and a TILTED n_inf.
be = sp.symbols('beta', real=True)
# On the isotropic round cell r2 is rotation-invariant; the ENERGY density depends on r only
# through rotation-scalars, so any spatially-rotated hopfion is degenerate (zero-mode).
print("r^2 is spatial-rotation invariant:", sp.simplify(r2.subs({y:y*sp.cos(be)-z*sp.sin(be),
        z:y*sp.sin(be)+z*sp.cos(be)}, simultaneous=True) - r2) == 0,
      "=> spatially-rotated hopfion is energy-degenerate (free orientation zero-mode).")

print("\n"+"="*72)
print("T4 — induced-shear SOURCE is a target-SCALAR (target-blind); single-channel needs fixed axis")
print("="*72)
# The stress that sources h_AB is built from d_mu n_a d_nu n_a (delta_ab contraction) -> target scalar.
# Show a representative stress component T_ij ~ dn_i . dn_j (sum over target index a) is SO(3) invariant.
Tij      = di.dot(dj)                    # sum_a (d_i n_a)(d_j n_a)
Tij_rot  = (R*di).dot(R*dj)
print("shear source T_ij = sum_a d_i n_a d_j n_a  target-SO(3) invariant:",
      sp.simplify(Tij_rot - Tij) == 0, " => carries NO target index (target-blind).")

# The equal-thirds single-channel readout: pick ONE target axis a. Build a degree-1 map on S^2
# and integrate n_a * (winding density) over the sphere. Use the hedgehog n = (sin th cos ph, ...).
th_,ph_ = sp.symbols('theta varphi', real=True)
nh = sp.Matrix([sp.sin(th_)*sp.cos(ph_), sp.sin(th_)*sp.sin(ph_), sp.cos(th_)])
nth = sp.diff(nh, th_); nph = sp.diff(nh, ph_)
wdens = nh.dot(nth.cross(nph))           # = sin theta (unit winding density)
wdens = sp.simplify(wdens)
print("\nunit winding density n.(n_th x n_ph) =", wdens)
# total degree:
tot = sp.integrate(sp.integrate(wdens, (ph_,0,2*sp.pi)), (th_,0,sp.pi))/(4*sp.pi)
print("total degree (1/4pi) INT wdens =", sp.simplify(tot), " (the SCALAR public charge)")
# single-channel share for a=3 (n_3^2 weighting), and the SUM over the three axes:
shares = []
for aidx in range(3):
    ch = sp.integrate(sp.integrate(nh[aidx]**2*wdens, (ph_,0,2*sp.pi)), (th_,0,sp.pi))/(4*sp.pi)
    shares.append(sp.simplify(ch))
print("per-target-axis shares (1/4pi)INT n_a^2 wdens =", shares, " sum =", sp.simplify(sum(shares)))
print("""
=> Each channel = 1/3 (END check, not an input); the SUM = 1 = the degree = the public scalar.
   A single 1/3 is obtained ONLY by fixing one axis a in the readout = breaking target SO(3)
   by hand (OR dividing the scalar total by the rank N=3 -- also a hand reporting convention,
   not a native observable). No native field supplies a fixed-axis projector.""")

# --- P3 EXHAUSTIVENESS as a direct theorem (verifier a28..-offered strengthening):
#     on the isotropic degree-1 config the ONLY surviving target-tensor moment of the winding
#     is the SCALAR. Vector moment INT n_a wdens = 0; 2-tensor INT n_a n_b wdens = (4pi/3) delta_ab
#     (traceless part = 0). So no target-INDEXED observable exists to carry a 1/3.
vec = [sp.integrate(sp.integrate(nh[a]*wdens, (ph_,0,2*sp.pi)), (th_,0,sp.pi)) for a in range(3)]
print("\nvector moment INT n_a wdens =", [sp.simplify(v) for v in vec], " (all 0 => no target-vector observable)")
ten = sp.Matrix(3,3, lambda a,b: sp.simplify(
        sp.integrate(sp.integrate(nh[a]*nh[b]*wdens, (ph_,0,2*sp.pi)), (th_,0,sp.pi))))
print("2-tensor moment INT n_a n_b wdens =", ten.tolist())
print("  traceless part =", sp.simplify(ten - (ten.trace()/3)*sp.eye(3)).tolist(),
      " (=> only the SCALAR trace survives; P3 exhaustive)")

print("\nDONE — all checks exact; no PDE solve; 1/3 only as an end check.")
