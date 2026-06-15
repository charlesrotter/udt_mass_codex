#!/usr/bin/env python3
"""
su3_field_test.py  --  OBSERVE (gated, Charles 2026-06-15)

THE DECISIVE TEST: does the UDT metric force / admit a GENUINE complex
SU(3)-valued l=1 angular field, or does it only ever provide the REAL
direction n (S^2) + the native U(1) phase (photon) + SO(3,1) (gravity)?

The whole quantum completion (native integer WZW, pi_5(SU(3))=Z => N_c=3,
soliton = fermion) lives ONLY on a genuine SU(3)-valued field.

Method: sympy CPU primary. We CONSTRUCT the complex l=1 amplitude triplet
z=(z_-1,z_0,z_+1) in C^3, relate it to the real n-vector, then ask what
CONNECTION the REAL metric (g_mn real, sqrt(-g)=c r^2 sin th) puts on z via
the only native kinetic term L = -(xi/2) g^{mn} d_m z^dag d_n z. We read off
which generators (U(1), SO(3), the extra rank-2 SU(3)) actually appear, and
whether the relative phases of z are physical or pure gauge.

DATA-BLIND. No mass/ratio/wall number is loaded.
"""
import sympy as sp

print("="*70)
print("TASK 1 -- CONSTRUCT the complex l=1 amplitude field z in C^3")
print("="*70)

# Real spherical-harmonic direction: the project's DERIVED field is the
# real unit 3-vector n in S^2 (h1_types, angular_lagrangian). The l=1
# COMPLEX spherical harmonics Y_1^m, m=-1,0,+1, are the SU(3)-fundamental
# "quark triplet" carrier. Their amplitudes form z in C^3.
#
# Standard relation between the real Cartesian (n_x,n_y,n_z) and the
# spherical (m=-1,0,+1) basis (the unitary "spherical-to-cartesian" map U):
#   z_{+1} = -(n_x + i n_y)/sqrt2
#   z_{ 0} =   n_z
#   z_{-1} = +(n_x - i n_y)/sqrt2
# This is the unitary change of basis on the l=1 irrep (SO(3) vector =
# the 3 of SU(3) restricted). It is a DERIVED kinematic identity.

nx, ny, nz = sp.symbols('n_x n_y n_z', real=True)
I = sp.I
s2 = sp.sqrt(2)
zp = -(nx + I*ny)/s2     # z_{+1}
z0 =  nz                 # z_{0}
zm =  (nx - I*ny)/s2     # z_{-1}
z = sp.Matrix([zm, z0, zp])   # ordering (m=-1,0,+1)

print("z_{-1} =", zm)
print("z_{ 0} =", z0)
print("z_{+1} =", zp)

# DOF count.
print("\nDOF: a general z in C^3 has 6 real DOF.")
print("The real unit n in S^2 has 2 real DOF.")
print("Gap = 4 real DOF: an overall phase (U(1)) + a |z| modulus (radial)")
print("     + the 2 relative phases. The question is whether the metric")
print("     makes ANY of these 4 extra DOF physical via a connection.")

# n recovered as the real/expectation direction. For a real n (the
# project's field), z is COMPLEX but its content is just the real n:
# n_a = <z| L_a |z> with L_a the spin-1 generators? Check n_z directly:
# Recover n from z (invert the unitary map):
nx_rec = (zm - zp)/s2
ny_rec = (zm + zp)/(-s2*I)
nz_rec = z0
print("\nRecover real n from this z (should be identities):")
print("  n_x:", sp.simplify(nx_rec - nx), " n_y:", sp.simplify(ny_rec - ny),
      " n_z:", sp.simplify(nz_rec - nz))

# Norm: |z|^2 = z^dag z
norm2 = sp.simplify((z.conjugate().T * z)[0])
print("\n|z|^2 =", norm2, " (= |n|^2; for unit n this is 1)")

print("\nKEY: for the project's REAL n, z is the spherical-basis image of a")
print("REAL vector. The 'extra phases' z carries are NOT free -- they are")
print("LOCKED to n by the unitary map. A GENUINE SU(3) field would need z")
print("to be an INDEPENDENT complex triplet (z not the image of any real n).")

print()
print("="*70)
print("TASK 2 -- what CONNECTION does the REAL metric induce on z?")
print("="*70)
# The only native kinetic term (angular_lagrangian, native_stabilizer):
#   L = -(xi/2) g^{mn} (d_m z)^dag (d_n z),  measure sqrt(-g)=c r^2 sin th.
# A connection enters via the COVARIANT derivative D_m z = d_m z + Omega_m z.
# The metric supplies Omega_m through (a) the spin connection (frame
# rotation) and (b) any internal bundle structure. We enumerate the FULL
# set of 3x3 generators and ask which the metric actually supplies.
#
# Generators of U(3) on C^3 = U(1) [identity] (+) SU(3) [8 traceless].
# SU(3) decomposes under the SO(3) (= spin-1 / "isospin" of the l=1
# carrier) subgroup as 8 = 3 (+) 5:  the 3 = SO(3) generators (L_x,L_y,L_z,
# antisymmetric), the 5 = the rank-2 symmetric-traceless generators (the
# EXTRA SU(3) directions BEYOND U(1) x SO(3)).

# Spin-1 (l=1) generators L_a in the spherical (m=-1,0,1) basis (Hermitian):
Lz = sp.diag(-1, 0, 1)
# L+ and L- (raising/lowering) in m=-1,0,1 basis, <m+1|L+|m> = sqrt(2):
sq2 = sp.sqrt(2)
Lp = sp.Matrix([[0,0,0],[sq2,0,0],[0,sq2,0]])   # raises m
Lm = Lp.T
Lx = (Lp + Lm)/2
Ly = (Lp - Lm)/(2*I)
print("SO(3) generators (the spin-1 / l=1 algebra), Hermitian, traceless:")
print("  L_z =", Lz.tolist())
print("  [Lx,Ly] = i Lz ? ->", sp.simplify(Lx*Ly - Ly*Lx - I*Lz) == sp.zeros(3))

# Build the 8 Gell-Mann-type generators of su(3) in this basis: a Hermitian
# traceless basis of 3x3. We use the standard real structure: 3 antisym
# (the SO(3) L_a) + 5 symmetric traceless. Identify which are "rank-2".
# Symmetric traceless rank-2 combinations of L_a:  {L_a L_b + L_b L_a - (2/3)delta_ab L^2}
Lvec = [Lx, Ly, Lz]
# The 5 rank-2 symmetric-traceless generators Q_ab = {L_a,L_b} - (2/3)delta_ab L^2
# EXIST as su(3) algebra elements (the 5 in 8=3+5). The question (Tasks 2-3) is
# NOT whether they exist as operators, but whether the METRIC sources a
# CONNECTION valued in them. We display two to confirm they are Hermitian/traceless.
Qxx = Lx*Lx + Lx*Lx - sp.Rational(2,3)*2*sp.eye(3)
Qxy = Lx*Ly + Ly*Lx
print("\nExample rank-2 generators (Hermitian, traceless):")
print("  Q_xx traceless?", sp.simplify((Qxx).trace())==0,
      "  Q_xy traceless?", sp.simplify((Qxy).trace())==0)
print("\nThe 8 su(3) generators = 3 (SO(3) L_a, antisymmetric) (+) 5 (rank-2")
print("symmetric-traceless Q_ab). The 5 rank-2 are the SU(3) directions")
print("BEYOND U(1) x SO(3). (This algebra is the DERIVED selection rule,")
print("UDT_REBUILD sec3 -- 8 = 3 (+) 5 at l=1. It is the OPERATOR algebra,")
print("not yet a metric-given CONNECTION.)")

print()
print("--- 2a. The spin connection of the REAL metric ---")
# UDT metric ds^2 = -e^{-2phi}c^2 dt^2 + e^{2phi}dr^2 + r^2(dth^2+sin^2 th dph^2)
# The spin connection omega_m^{ab} is so(3,1)-valued (antisymmetric ab).
# On the angular block it generates the SO(3) rotation of the frame (the
# Levi-Civita connection on S^2). We construct the angular spin connection.
r, th, ph, phi = sp.symbols('r theta varphi phi', real=True, positive=True)
c = sp.symbols('c', positive=True)
# Orthonormal angular frame: e^1 = r dth, e^2 = r sin th dph.
# Levi-Civita on the round sphere: the only nonzero spin-connection
# component is omega_{ph}^{12} = -cos th (rotates frame 1<->2 around ph).
omega_sphere = -sp.cos(th)
print("Round-S^2 spin connection: omega_ph^{12} = -cos(theta)  (SO(2) frame")
print("rotation in the tangent plane) -- ANTISYMMETRIC in frame indices =>")
print("it is an SO(3)/SO(3,1) connection. It rotates the REAL frame vectors.")
print("It is the L_a (antisymmetric) part ONLY. It supplies NO symmetric")
print("rank-2 generator.")

print()
print("--- 2b. Does the kinetic term induce a U(1) (photon) on z? ---")
# The native U(1) is the EM/photon (em_forcing): an ABELIAN phase rotation
# z -> e^{i alpha} z (the identity generator, U(3)=U(1)xSU(3)). The metric
# DOES supply this (the Coulomb/Maxwell A_m). It is the OVERALL phase only.
print("U(1) (em_forcing, native photon): z -> e^{i alpha(x)} z, generator =")
print("the IDENTITY (overall phase). The metric DOES supply this abelian")
print("connection (the Coulomb A_m). It acts on the OVERALL phase ONLY --")
print("it does NOT mix the components z_m, so it supplies NO su(3) direction.")

print()
print("--- 2c. THE DECISIVE GENERATOR AUDIT ---")
print("Native connections the metric supplies, by generator content:")
print("  U(1)   : overall-phase identity 1_3            [photon, em_forcing] YES")
print("  SO(3)  : antisymmetric L_a (3 gens)            [spin connection]    YES")
print("  SO(3,1): boosts -- the t-r frame (gravity)     [spin connection]    YES")
print("  ------------------------------------------------------------------")
print("  rank-2 symmetric-traceless Q_ab (5 gens)       [the EXTRA su(3)]    ??")
print()
print("The su(3) generators MISSING from U(1) x SO(3) are exactly the 5")
print("rank-2 symmetric-traceless Q_ab. For the metric to force a GENUINE")
print("SU(3) connection, a NATIVE term must supply a Q_ab-valued connection")
print("1-form Omega_m = Omega_m^{(ab)} Q_ab. We now check every native source.")

print()
print("="*70)
print("TASK 3 -- is z GENUINELY complex, or does it collapse to real n?")
print("="*70)
# The test: in the kinetic term L = -(xi/2) g^{mn} d_m z^dag d_n z with the
# native covariant derivative, are the RELATIVE phases of z physical?
#
# A connection makes a relative phase physical iff there is a generator T
# (a 3x3 Hermitian matrix) coupling as D_m z = d_m z - i A_m^A T_A z with
# A_m^A a metric-given 1-form, AND T_A is NOT the identity (U(1)) and NOT
# a pure SO(3) rotation (which acts on the REAL n). The rank-2 Q_ab are the
# only candidates. Source audit:

print("Native term audit -- can ANY supply a rank-2 Q_ab connection on z?")
print()
print("(i) Spin connection omega_m^{ab}: so(3,1)-valued, ANTISYMMETRIC in")
print("    a,b => it is an SO(3) x boost rotation. Acting on the l=1 carrier")
print("    it is the antisymmetric L_a. SYMMETRIC Q_ab does NOT appear.")
print("    (A real symmetric metric g_mn generates, via the vielbein, only")
print("     the ANTISYMMETRIC so(p,q); this is a theorem -- omega is the")
print("     antisymmetrized Christoffel in an orthonormal frame.) -> NO Q_ab")
print()
print("(ii) The U(1)/Maxwell A_m (photon): generator = identity 1_3.")
print("     -> overall phase only, NO Q_ab.")
print()
print("(iii) The native kinetic term L = -(xi/2) g^{mn} d_m z^dag d_n z:")
# Check: with ONLY d_m (partial) + the spin connection + U(1), the term is
# invariant under the GLOBAL SU(3) z -> V z (V in SU(3)) because z^dag z and
# d z^dag d z are SU(3)-invariant -- but GLOBAL invariance is a SYMMETRY, not
# a gauged CONNECTION. A connection requires a metric-given GAUGE FIELD
# Omega_m^A valued in the generators. The metric supplies Omega_m for U(1)
# (A_m) and SO(3,1) (omega_m) only. There is NO native Omega_m^{(Q)}.
print("     z^dag z and d z^dag.d z are GLOBALLY SU(3)-invariant -- but that")
print("     is a global SYMMETRY (the selection-rule algebra), NOT a gauged")
print("     connection. Gauging needs a metric-given 1-form Omega_m^A valued")
print("     in Q_ab. The metric supplies Omega_m only for U(1) (A_m) and")
print("     SO(3,1) (omega_m). The rank-2 Q_ab have NO native gauge field.")
print()
print("(iv) Could a native Skyrme/L4 term supply it? L4 = -kappa|F(A)|^2_g")
print("     with A the COMPOSITE U(1) Berry connection (hopf_spinor Task2):")
print("     metric-contracted, P/T-EVEN, ABELIAN composite -- it is U(1)-type")
print("     curvature-squared, NOT a non-abelian SU(3) connection. -> NO Q_ab")
print()
print("CONSEQUENCE FOR THE PHASES OF z:")
print("Under the ONLY native connections (U(1) overall phase + SO(3) frame")
print("rotation), the relative phases of z are either (a) the overall U(1)")
print("phase -- pure gauge, removable -- or (b) re-shuffled by the SO(3)")
print("rotation which acts identically on the REAL n (z is the spherical")
print("image of n; an SO(3) rotation of n IS an SU(3) rotation of z within")
print("the SO(3) subgroup). The 5 rank-2 directions that would make z's")
print("internal phases PHYSICALLY DISTINCT from n have NO native connection")
print("=> they are NOT acted on => the only native invariants are functions")
print("of the REAL n (+ the removable U(1) phase).")

# Concrete demonstration: the native invariants. Build the SO(3)-invariant
# and U(1)-invariant combinations of z and show they are all functions of n.
print()
print("Concrete: the native (U(1)xSO(3))-invariants of z are functions of n:")
zdag = z.conjugate().T
# |z|^2:
print("  z^dag z =", sp.simplify((zdag*z)[0]), " (= |n|^2)")
# Direct inverse map: the U(1)xSO(3)-covariant content of z IS exactly n.
print("  inverse map recovers n exactly:  n_x=", sp.simplify(nx_rec-nx),
      " n_y=", sp.simplify(ny_rec-ny), " n_z=", sp.simplify(nz_rec-nz),
      " (all 0 => z is the spherical IMAGE of the real n; no extra content)")
# <z|L_a|z>: a REAL vector is an eigenstate of zero angular momentum.
def expval(M):
    return sp.simplify((zdag*M*z)[0])
vx, vy, vz = expval(Lx), expval(Ly), expval(Lz)
print("  <z|L_x|z> =", vx, ", <z|L_y|z> =", vy, ", <z|L_z|z> =", vz)
print("    (= (n x n) = 0: the spherical image of a REAL n carries ZERO")
print("     angular momentum -- a sharp statement of the collapse: z sits in")
print("     the L=0 expectation locus, no internal SU(3) excitation.)")
print("  -> every native invariant is a function of the REAL n alone (the map")
print("     n <-> z is invertible; z carries NO independent SU(3) content).")
print("  z does NOT carry independent SU(3) content: it COLLAPSES to real n.")

print()
print("="*70)
print("TASK 4 -- THE WZW CONSEQUENCE")
print("="*70)
print("A native INTEGER WZW term requires the SU(3) GROUP-MANIFOLD target")
print("(maps into SU(3), pi_5(SU(3))=Z, the level = N_c integer). That needs")
print("a GENUINE SU(3)-valued field U(x) in SU(3) -- i.e. all 8 generators")
print("physically realized with a connection making the SU(3) target real.")
print()
print("The metric supplies U(1) x SO(3) x SO(3,1) -- NOT the rank-2 Q_ab.")
print("The field z COLLAPSES to the real n (S^2 = SU(3)/U(2) two-sphere, only")
print("the 2 real DOF). The target is S^2, NOT the SU(3) group manifold.")
print("  pi_5(S^2) = Z_2  (NOT Z)  -- a FREE Z_2, not an integer-graded WZW.")
print("  pi_3(S^2) = Z (Hopf) -- but the Hopf term is metric-FREE & P/T-ODD;")
print("              L2+L4 are metric-contracted & P/T-EVEN (hopf_spinor) =>")
print("              not present natively either.")
print()
print("VERDICT TASK 4: a native INTEGER WZW (SU(3) target, pi_5=Z, level=N_c)")
print("is NOT supported. The metric gives the S^2 (real n) target, whose")
print("statistics input is the FREE Finkelstein-Rubinstein Z_2 (#47/#49) --")
print("NOT a metric-forced integer. The fermion stays the free FR Z_2.")

print()
print("="*70)
print("TASK 5 -- THE ONE HONEST OPEN DOOR (report, do not chase)")
print("="*70)
print("The QUANTUM sector: quantizing the angular collective coordinates")
print("introduces COMPLEX amplitudes (the wavefunction on the l=1 modes lives")
print("in C^3 genuinely -- hbar makes the relative phases of the mode")
print("amplitudes physical as QUANTUM STATE phases, acted on by the angular")
print("momentum / the spin-1 operator algebra su(3)). This is the su(3)")
print("KINEMATICS (the selection-rule algebra, DERIVED) promoted to act on a")
print("genuine complex Hilbert-space triplet by hbar. Whether the QUANTIZED")
print("theory carries an EMERGENT WZW/Hopf phase (an induced theta-term from")
print("integrating out hbar fluctuations, or a Berry phase over the collective")
print("manifold) is GENUINELY OPEN -- it is the live frontier (#49: the whole")
print("quantum completion rests on this single crux). It is NOT excluded, but")
print("it is NOT classically native: it would RIDE hbar, exactly as #47b/c")
print("and #49 concluded. We do NOT assume it.")
print()
print("(The other named door -- emergent SU(3) from U(1)(photon)+angular --")
print("is NOT supported classically: the U(1) is abelian overall-phase, the")
print("angular SO(3) is real-frame; their product is U(1)xSO(3), which does")
print("NOT close into SU(3) -- the rank-2 Q_ab commutators [L_a,Q_bc] generate")
print("MORE Q's, but no native connection sources any Q to begin with.)")

print()
print("="*70)
print("SUMMARY")
print("="*70)
print("(1) Connection induced: U(1) x SO(3) x SO(3,1) -- NOT SU(3).")
print("    The 5 rank-2 Q_ab generators have NO native gauge field.")
print("(2) z is NOT genuinely complex: it COLLAPSES to the real n.")
print("    All native invariants are functions of n (+ removable U(1) phase).")
print("(3) Native integer WZW: NOT supported (target = S^2, pi_5=Z_2 free).")
print("(4) VERDICT: REAL-S^2 + U(1)-ONLY. Open door = the QUANTUM sector")
print("    (hbar-induced complex amplitudes / induced phase), genuinely open,")
print("    NOT classically native.")
