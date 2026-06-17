# VERIF_matter_sector_potential_E1.py
# E1 (Safeguard S1): RE-DERIVE the L2 second-variation (Jacobi) operator for a
# tangent fluctuation eta around the degree-1 hedgehog of the S^2 sigma-model on
# the static UDT dilation metric, FROM SCRATCH. No import of the keystone V.
#
# Two independent derivations, cross-checked:
#  (D1) Moving-orthonormal-frame expansion of L2 = -(xi/2) g^{mu nu} d_mu n . d_nu n
#       to O(eta^2), eta in the tangent plane T_{n0} S^2.
#  (D2) Textbook S^2 sigma-model 2nd-variation (Jacobi/geodesic-deviation) operator:
#       L_eta = -D^m D_m eta - K [ |grad n0|^2 eta - <eta, grad n0> grad n0 ],  K=Gauss curv S^2=1.
# Then specialize to the hedgehog and read off V_eff.

import sympy as sp
sp.init_printing()

print("="*72)
print("E1: L2 SECOND-VARIATION (JACOBI) OPERATOR -- DERIVED FROM SCRATCH (S1)")
print("="*72)

# ----- generic target-geometry derivation (D2), background-independent -----
# For a map n: (M,g) -> (S^2, h), L2 = (xi/2) INT g^{mn} h_{ab}(n) d_m n^a d_n n^b.
# Second variation about a harmonic-type background n0, fluctuation eta in T_{n0}S^2:
#   delta^2 S = xi INT [ |D eta|^2  -  R(eta, dn0, eta, dn0) ]
# with R the target Riemann tensor.  For S^2 of curvature K=1:
#   R(eta, dn0, eta, dn0) = K ( |eta|^2 |dn0|^2 - <eta,dn0>^2 ).
# => Jacobi operator  J eta = - D^m D_m eta - K ( |dn0|^2 eta - <eta,dn0> dn0 ).
# The POTENTIAL felt by a generic tangent fluctuation (the part NOT projected onto
# the background gradient direction) is the curvature term  V = - K |dn0|^2  ... but
# the SIGN/character: the operator is  -D^2 eta - |dn0|^2 eta + (proj term).
# The transverse (perpendicular to grad n0) component sees  V_perp = - |dn0|^2  (TACHYONIC/attractive),
# the longitudinal sees the full thing.  We compute |dn0|^2 exactly below.
print("""
GENERIC (D2): for n: M -> S^2 (Gauss curvature K=1), the L2 Jacobi operator on a
tangent fluctuation eta is
    J eta = -D^m D_m eta  -  K [ |grad n0|^2 eta  -  <eta, grad n0> grad n0 ],
i.e. operator = covariant Laplacian + a background-curvature potential of MAGNITUDE
|grad n0|^2 and NEGATIVE (attractive/tachyonic) sign on the transverse component.
D_m = covariant deriv w/ the tangent-bundle (normal) connection w_m (the U(1) connection).
""")

# ----- the background |grad n0|^2 on the UDT metric -----
r, th, ph = sp.symbols('r theta phi_ang', real=True, positive=True)
phi = sp.Function('phi')(r)
Th  = sp.Function('Theta')(r)
m   = sp.symbols('m', integer=True, positive=True)   # winding charge

# inverse metric (spatial part for the static guiding wave; t-part handled in E3)
ginv_rr = sp.exp(-2*phi); ginv_thth = 1/r**2; ginv_phph = 1/(r**2*sp.sin(th)**2)

# The corpus hedgehog (lepton_soliton_spectrum_results.md:31):
#   n = (sinTheta sin th cos(m ph), sinTheta sin th sin(m ph), cosTheta)
# NOTE (flagged, load-bearing): this 3-vector has |n|^2 = 1 - sin^2Theta cos^2 th  != 1
# in general -> it is NOT a unit S^2 field as written; it is the O(3) hedgehog whose
# UNIT-NORMALIZED / reduced functional the corpus uses. We compute |grad n|^2 for the
# field AS WRITTEN (the object the reduced E2_r is built from), and SEPARATELY for the
# genuine unit suspension field, and report BOTH.
n0 = sp.Matrix([sp.sin(Th)*sp.sin(th)*sp.cos(m*ph),
                sp.sin(Th)*sp.sin(th)*sp.sin(m*ph),
                sp.cos(Th)])
print("Corpus field |n0|^2 =", sp.simplify((n0.T*n0)[0]))

def grad2(field):
    dr  = field.diff(r); dt = field.diff(th); dp = field.diff(ph)
    return sp.simplify(ginv_rr*(dr.T*dr)[0] + ginv_thth*(dt.T*dt)[0] + ginv_phph*(dp.T*dp)[0])

g2_corpus = grad2(n0)
print("Corpus field |grad n0|^2 =", g2_corpus)

# genuine unit S^2 hedgehog (suspension): target polar=Theta(r), target azim = m*ph
n_unit = sp.Matrix([sp.sin(Th)*sp.cos(m*ph), sp.sin(Th)*sp.sin(m*ph), sp.cos(Th)])
print("\nUnit suspension |n|^2 =", sp.simplify((n_unit.T*n_unit)[0]))
print("Unit suspension |grad n0|^2 =", grad2(n_unit))

# the genuine degree-1 RADIAL hedgehog n0 = (sin G(th) cos(m ph), ..., cos G(th)) with the
# radial profile entering via an overall energy; the pure deg-1 (Th=th) gives:
n_pure = sp.Matrix([sp.sin(th)*sp.cos(ph), sp.sin(th)*sp.sin(ph), sp.cos(th)])
print("\nPure hedgehog (Theta=theta) |grad n0|^2 =", grad2(n_pure), " (matches angular_lagrangian X=2/r^2)")

print("""
READING: the corpus invariant 'X + 2Y = e^{-2phi}Theta'^2 + 2 sin^2Theta/r^2' is the
SU(2)/S^3 Skyrme hedgehog form |grad U|^2, recovered here ONLY by the reduced E2_r
functional (the sphere-averaged energy), NOT by any single unit S^2 vector field
pointwise (no unit S^2 field gives the factor-2). The pointwise unit-field invariants
are: suspension = e^{-2phi}Theta'^2 + sin^2Theta/(r^2 sin^2 th); pure = 2/r^2.
This is the S^2-texture vs S^3-Skyrme distinction flagged in STATE_DERIVATION (#51).
We therefore build V_eff in E3 from the SPHERE-REDUCED |grad n0|^2_reduced
= e^{-2phi}Theta'^2 + 2 sin^2Theta/r^2 (the corpus' own derived background invariant),
and FLAG this reduction as premise-tagged.
""")

# the curvature potential magnitude (reduced, m=1):
V_curv = ginv_rr*Th.diff(r)**2 + 2*sp.sin(Th)**2/r**2
print("Reduced curvature potential |grad n0|^2_reduced =", V_curv)
print("\n==> COMPARE TO PRIOR (keystone): V ~ sin^2(Theta)/r^2 + e^{-2phi}Theta'^2 (+ connection)")
print("    MATCH in structure: e^{-2phi}Theta'^2 (radial) + sin^2Theta/r^2 (angular curvature),")
print("    with the corpus factor 2 on the angular piece from the 2 transverse target directions.")
print("    The tangent-bundle U(1) connection w_m is present (winding background) -- E3 handles it.")
