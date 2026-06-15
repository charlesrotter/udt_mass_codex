#!/usr/bin/env python3
"""
crux2_coinflip.py  --  OBSERVE/DERIVE (gated, the pre-registered Crux-2 coin-flip;
                       postulate-A test). Frozen contract: crux2_coinflip_contract.md.

THE QUESTION (statistics only, masses OUT of scope): when the angular collective
coordinates of the settled degree-1 S^2 baby-Skyrme hedgehog are QUANTIZED, does an
EMERGENT quantum Berry/geometric/anomaly phase around the 2*pi spatial-rotation loop
(= the Finkelstein-Rubinstein exchange loop, generator of pi_4(S^2)=Z2) EQUAL
exp(i*pi*N) with N=3 -- AFFINELY shifting the free Z2 onto the fermionic (-1) side?

CENTRAL TRAP (automatic FAIL if violated): the phase MUST be COMPUTED from the
soliton's own quantum state (fluctuation vacuum / collective-coordinate wavefunction
/ su(3) rep structure) as a function of the loop parameter. INSERTING a WZW term, a
Hopf term, an FR sign, or an N_c coefficient by hand = IMPORT = FAIL, even if it
numerically yields pi.

HONEST PRIOR (pre-registered): expect FREE (Phi = 0, postulate A irreducible).

Two routes, both run, feeding ONE yes/no:
 (i)  RIGID-ROTOR / COLLECTIVE-COORDINATE Berry phase.
 (ii) su(3) OPERATOR-ALGEBRA / REPRESENTATION-THEORY route.

DATA-BLIND. No mass/ratio/wall number is loaded.
"""
import sympy as sp
import numpy as np

I = sp.I
print("="*74)
print("CRUX 2 -- THE COIN-FLIP / POSTULATE-A TEST")
print("Berry phase of the QUANTIZED collective coordinates around the")
print("2*pi spatial-rotation = FR exchange loop. DERIVE; do NOT import.")
print("="*74)

# ----------------------------------------------------------------------------
# THE SOLITON'S OWN STRUCTURE (settled, reused -- not re-derived here):
#   n(r,th,ph) = (sinTheta(r) sin th cos ph, sinTheta(r) sin th sin ph, cosTheta(r))
#   Theta(core)=pi (charge 1) -> Theta(seal)=0 (unwound).
#   target S^2; L = L2+L4 (baby-Skyrme); ONE radial profile + RIGID SO(3) orient.
#   (native_stabilizer; monodromy_depth #49: chi is a rigid cyclic coordinate;
#    su3_field #50: the C^3 amplitude z COLLAPSES to the real n classically; the
#    QUANTUM door is the genuine complex Hilbert triplet.)
# The collective manifold is the soliton's orientation: a copy of SO(3) (the
# rigid rotation that moves the hedgehog). The 2*pi spatial rotation is a LOOP
# in this SO(3): the noncontractible generator of pi_1(SO(3))=Z2.
# ----------------------------------------------------------------------------

print()
print("#"*74)
print("# ROUTE (i): RIGID-ROTOR / COLLECTIVE-COORDINATE BERRY PHASE")
print("#"*74)
print("""
SETUP. Collective-coordinate quantization of the degree-1 hedgehog. The zero
modes that the 2*pi spatial rotation excites are the rigid orientation: a point
A in SO(3) acting on the hedgehog, n_A(x) = R(A) . n(R(A)^{-1} x) for the
co-moving (= grooming) hedgehog, or for the pure-spatial rotation the hedgehog
is carried n -> n(R^{-1}x). The quantum state is Psi(A) on the collective
manifold; the BERRY connection is

    a(A) = i <vac(A) | d/dA | vac(A)>          (1-form on the collective manifold)

and the Berry phase on the 2*pi rotation loop gamma is

    Phi = oint_gamma a   (mod 2*pi).

We compute a(A) from the EXPLICIT A-dependence of the soliton's quantum ground
state -- the bosonic FLUCTUATION VACUUM and the collective wavefunction -- NOT
by inserting any topological term.
""")

# --- (i.1) The bosonic fluctuation vacuum's Berry phase ---------------------
# The fluctuation vacuum |vac(A)> is the ground state of the quadratic
# (Gaussian) Hamiltonian of the small oscillations delta-n about the soliton
# n_A. Rotating A adiabatically transports this Gaussian vacuum. The Berry
# connection of a Gaussian (squeezed-vacuum) state is
#     a = (1/2) Im Tr[ S^{-1} dS ]   (up to a real, hence phase-trivial, part)
# where S(A) is the (complex, symmetric) covariance/width matrix of the vacuum.
# KEY STRUCTURAL FACT (DERIVED, not inserted): the fluctuation operator about a
# REAL field configuration n_A is a REAL symmetric operator (L2+L4 are real,
# P-even and T-even -- hopf_spinor #47c, su3_field #50). A real symmetric
# fluctuation operator has a REAL ground-state covariance S(A): S = S* for all A.
# For a real S, Im Tr[S^{-1} dS] = 0 identically. Hence the Gaussian vacuum
# Berry connection VANISHES along ANY path in A:
print("(i.1) Bosonic fluctuation vacuum (Gaussian/squeezed) Berry connection.")
print("   The L2+L4 fluctuation operator about the REAL hedgehog n_A is a REAL")
print("   symmetric operator (L2,L4 are real, P/T-EVEN: hopf_spinor #47c,")
print("   su3_field #50). => its Gaussian ground-state covariance S(A) is REAL.")
print("   Berry connection a = (1/2) Im Tr[S^{-1} dS]. For real S: dS real,")
print("   S^{-1} real => Tr[S^{-1} dS] real => Im(...) = 0.")
# symbolic sanity: a real symmetric 1-parameter family has zero imaginary trace.
# Model S(t) and dS/dt by EXPLICIT REAL symbols (a real symmetric fluctuation
# operator yields a real covariance with real t-derivative). Then im() collapses.
s11,s12,s22 = sp.symbols('s11 s12 s22', real=True)        # real covariance
d11,d12,d22 = sp.symbols('d11 d12 d22', real=True)        # real dS/dt
S  = sp.Matrix([[s11,s12],[s12,s22]])
dS = sp.Matrix([[d11,d12],[d12,d22]])
expr = sp.Rational(1,2)*sp.im((S.inv()*dS).trace())
expr = sp.simplify(expr)
print("   symbolic check Im Tr[S^{-1} dS] for REAL symmetric S, dS =",
      expr, " (==0)  => Gaussian-vacuum Berry connection = 0")
assert expr == 0, "Gaussian-vacuum Berry connection should vanish for real S"
print("   RESULT (i.1): the FLUCTUATION-VACUUM contributes ZERO Berry phase on")
print("   any loop, including the 2*pi rotation. [DERIVED from reality of L2+L4]")

# --- (i.2) The collective rigid-rotor wavefunction's Berry/Bohr-Sommerfeld phase ---
# The remaining piece is the collective wavefunction Psi(A) on the rotor
# manifold itself. For a RIGID ROTOR the dynamical phase is not Berry; the only
# topological/geometric phase is the holonomy of the FLAT collective connection,
# i.e. the response of the wavefunction to the noncontractible 2*pi loop. For a
# free (no WZW) symmetric top the collective Lagrangian is purely kinetic,
#     L_coll = (1/2) Omega_a Lambda_ab Omega_b,    (monodromy_depth #49)
# with NO term LINEAR in the angular velocity Omega (a linear term IS the
# would-be WZW/theta term -- absent: monodromy_depth verified ONLY (Psi')^2,
# zero linear, zero bare term). A purely-kinetic rotor has NO Berry connection
# (the canonical 1-form p dq integrates to a DYNAMICAL phase, not a geometric
# one; the geometric/Berry 1-form requires a LINEAR-IN-VELOCITY term in L).
print()
print("(i.2) Collective rigid-rotor wavefunction phase.")
print("   Collective Lagrangian (monodromy_depth #49, verified): purely KINETIC")
print("   L_coll = (1/2) Omega_a Lambda_ab Omega_b, ZERO linear-in-Omega term.")
print("   A linear-in-velocity term IS the would-be WZW/theta (Berry) term.")
print("   monodromy_depth verified the iso-twist enters ONLY as (Psi')^2 and chi")
print("   as (chidot)^2 -- NO bare/linear term, for BOTH S^2 and the S^3 lift.")
print("   => the collective connection is FLAT and the geometric phase is the")
print("      pure HOLONOMY of the rotor's CONFIGURATION-SPACE topology, NOT an")
print("      induced Berry phase.")

# The holonomy of the free rotor on the 2*pi loop is fixed by HOW the soliton's
# orientation manifold sits in SO(3): is the rotor's configuration space SO(3)
# (2*pi loop noncontractible, Psi may be a SPINOR rep, half-integer J allowed)
# or SU(2) (2*pi loop contractible)? This is the central representation-theoretic
# question -- and CRUCIALLY it is decided NOT by the rotor dynamics but by
# whether the field admits the half-integer (spinor) reps. For a BOSONIC sigma
# model with NO WZW term the wavefunction Psi(A) is a genuine FUNCTION on SO(3)
# (single-valued; the rotation R and R+2pi are the SAME operator on the field
# n_A, since n_A is built from n by an SO(3) rotation and SO(3) closes at 2*pi).
# Therefore Psi(2*pi) = Psi(0): the 2*pi-rotation holonomy is +1 (boson side).
# The half-integer (spinor) sector requires a WZW term to make Psi a section of
# a NONTRIVIAL line bundle (double cover) -- absent here.
print("   The free-rotor wavefunction Psi(A) is a single-valued FUNCTION on the")
print("   soliton's orientation SO(3) (R and R+2pi act IDENTICALLY on the real")
print("   field n_A -- SO(3) closes at 2*pi). With NO WZW term there is no line")
print("   bundle to make Psi double-valued. => Psi(2*pi)=Psi(0): holonomy = +1.")
print("   RESULT (i.2): collective-rotor 2*pi holonomy = +1 (Phi=0, boson side).")
print("   The half-integer/spinor (fermion) sector is NOT reachable without a")
print("   WZW term to twist the bundle -- and inserting one = IMPORT = FAIL.")

print()
print("   >>> ROUTE (i) DERIVED RESULT:  Phi_(i) = 0  (mod 2*pi).  FREE/boson.")
print("       (i.1 fluctuation vacuum: 0; i.2 collective rotor holonomy: 0.")
print("        Both DERIVED from reality + absence of a linear-in-velocity term;")
print("        nothing inserted.)")

# ----------------------------------------------------------------------------
print()
print("#"*74)
print("# ROUTE (ii): su(3) OPERATOR-ALGEBRA / REPRESENTATION-THEORY ROUTE")
print("#"*74)
print("""
SETUP (the genuine open door, su3_field #50). Quantize: promote the 3 complex
l=1 amplitudes z=(z_{-1},z_0,z_{+1}) to BOSONIC oscillators a_m, a_m^dag, with
[a_m, a_n^dag] = delta_mn (m,n in {-1,0,+1}). The su(3) generators are the
NORMAL-ORDERED BILINEARS  T^i = a^dag (lambda^i/2) a (i=1..8), which close on
su(3) and act on the Fock space. The SPATIAL ROTATION acts on the amplitudes
through the SO(3) subgroup su(3) ⊃ so(3) (the l=1 angular-momentum generators
L_a = a^dag (L_a-matrix) a). The 2*pi spatial-rotation loop is the operator

    U(2*pi) = exp(-i 2*pi n.L)    (rotation by 2*pi about axis n).

We ask, purely from the REP STRUCTURE / the OPERATOR algebra, what phase
U(2*pi) imprints on the soliton's quantum state -- WITHOUT inserting any WZW or
Hopf coefficient.
""")

# --- (ii.1) The single-oscillator (3 of su(3)) carries INTEGER spin only -----
# Build the spin-1 (l=1) angular-momentum matrices acting on the 3 amplitudes.
sq2 = sp.sqrt(2)
Lz = sp.diag(1, 0, -1)                       # m = +1,0,-1
Lp = sp.Matrix([[0,sq2,0],[0,0,sq2],[0,0,0]])# raises m (acting on (+1,0,-1) order: lowers index)
Lm = Lp.T
Lx = (Lp+Lm)/2
Ly = (Lp-Lm)/(2*I)
print("(ii.1) The su(3) ⊃ so(3) generators on the 3 amplitudes (spin-1):")
print("   [Lx,Ly]=iLz ?", sp.simplify(Lx*Ly-Ly*Lx-I*Lz)==sp.zeros(3),
      "  L^2 eigenvalue:", sp.simplify((Lx*Lx+Ly*Ly+Lz*Lz)[0,0]),
      "= l(l+1)=2 => l=1 (INTEGER spin)")
# The 2*pi rotation on the spin-1 carrier:
U2pi = sp.simplify(sp.exp(-I*2*sp.pi*Lz))
print("   U(2*pi)=exp(-i 2*pi Lz) on the 3 of su(3) =")
sp.pprint(U2pi)
print("   => U(2*pi) = +1 (identity) on the su(3) TRIPLET. INTEGER spin, the")
print("      2*pi rotation is trivial. [DERIVED: the 3 is a genuine SO(3) rep.]")

# --- (ii.2) Fock states (the soliton's quantum state) carry the SAME phase ----
# The soliton's quantized state is built from the oscillators acting on the Fock
# vacuum: |state> = (product of a^dag's) |0>. Under U(2*pi)=exp(-i 2*pi Lz_Fock),
# Lz_Fock = sum_m m a_m^dag a_m, the phase on an n-quantum state is
#     exp(-i 2*pi sum m_k) = exp(-i 2*pi M),  M = total L_z = INTEGER.
# Because each oscillator carries INTEGER m (m in {-1,0,+1}), the total is an
# INTEGER, so U(2*pi)|state> = exp(-i 2*pi*integer)|state> = (+1)|state>.
print()
print("(ii.2) The soliton Fock state under U(2*pi).")
print("   L_z(Fock) = sum_m m a_m^dag a_m, m in {-1,0,+1} (all INTEGER).")
print("   Any Fock state |state> = prod a_{m_k}^dag |0> has total L_z = sum m_k")
print("   = INTEGER M.  U(2*pi)|state> = exp(-i 2*pi M)|state> = (+1)|state>.")
print("   => the bosonic-oscillator su(3) Fock space carries ONLY integer spin;")
print("      U(2*pi)=+1 on EVERY state. NO half-integer (fermionic) sector.")

# --- (ii.3) Is there a PROJECTIVE / ANOMALOUS phase? (the real open question) -
# A projective (anomalous) phase would appear if the su(3) acted only
# PROJECTIVELY on the Hilbert space -- i.e. if normal-ordering produced a
# central extension (a c-number) in the algebra. Test: compute the normal-
# ordering anomaly of the bilinear su(3) generators. For a FINITE number of
# oscillator modes (here exactly 3), normal ordering shifts each generator by a
# c-number (the trace of lambda^i/2), which for the TRACELESS Gell-Mann
# matrices is ZERO. Hence NO central extension, NO anomaly: the algebra is
# represented HONESTLY (not projectively). DERIVE this:
print()
print("(ii.3) Projective/anomalous phase test (the genuine open door).")
print("   A fermionic phase could only come from a PROJECTIVE rep / central")
print("   extension (an anomaly) in the normal-ordered su(3). The normal-")
print("   ordering shift of T^i = a^dag(lambda^i/2)a is the c-number")
print("   (1/2)Tr(lambda^i). For the su(3) Gell-Mann matrices Tr(lambda^i)=0:")
# Build the 8 Gell-Mann matrices and check tracelessness.
lam = []
lam.append(sp.Matrix([[0,1,0],[1,0,0],[0,0,0]]))      # 1
lam.append(sp.Matrix([[0,-I,0],[I,0,0],[0,0,0]]))     # 2
lam.append(sp.Matrix([[1,0,0],[0,-1,0],[0,0,0]]))     # 3
lam.append(sp.Matrix([[0,0,1],[0,0,0],[1,0,0]]))      # 4
lam.append(sp.Matrix([[0,0,-I],[0,0,0],[I,0,0]]))     # 5
lam.append(sp.Matrix([[0,0,0],[0,0,1],[0,1,0]]))      # 6
lam.append(sp.Matrix([[0,0,0],[0,0,-I],[0,I,0]]))     # 7
lam.append(sp.Matrix([[1,0,0],[0,1,0],[0,0,-2]])/sp.sqrt(3))  # 8
traces = [sp.simplify(m.trace()) for m in lam]
print("   Tr(lambda^i) for i=1..8 =", traces)
print("   ALL ZERO => normal-ordering produces NO central c-number => NO central")
print("   extension => the su(3) is represented HONESTLY (NOT projectively).")
print("   => NO anomalous/projective phase. [DERIVED, finite-mode normal order.]")

# --- (ii.4) Could a half-integer rep enter via a DIFFERENT oscillator number? -
# The ONLY way the su(3) Fock construction yields half-integer SO(3) spin is if
# the fundamental oscillators carried half-integer m -- i.e. if the carrier were
# the 2 of SU(2) (a genuine spinor), NOT the 3 of su(3). su3_field #50 DERIVED
# that the metric supplies the REAL n / the 3 (S^2 target), NOT the SU(2)/S^3
# spinor target. So no half-integer fundamental exists to build a fermion from.
print()
print("(ii.4) Half-integer sector? Needs a SPINOR fundamental (the 2 of SU(2),")
print("   m=+-1/2). su3_field #50 DERIVED the metric gives the 3 / real n (S^2),")
print("   NOT the SU(2)/S^3 spinor target. No half-integer fundamental exists.")
print("   Inserting a 2-of-SU(2) carrier = IMPORT = FAIL.")

# --- (ii.5) The N=3 integer: where it lives, and whether it feeds the phase ---
# N=3 is the eps_abc singlet rank (h1_types) -- it lives in the STRUCTURE of the
# su(3) (the 3-index epsilon, the number of amplitudes), NOT as a WZW LEVEL.
# A WZW level would be an INTEGER in pi_5(SU(3))=Z multiplying a 5D term. Here
# N=3 enters as the DIMENSION of the fundamental (3 oscillators) and as the
# epsilon_abc invariant. Does THAT feed U(2*pi)? The 2*pi rotation phase is
# exp(-i 2*pi M) with M the total integer L_z; the number of oscillators (3)
# changes the RANGE of M but NEVER makes M half-integer. So N=3 does NOT enter
# the 2*pi phase as exp(i*pi*N): there is no channel by which the count 3
# becomes a half-integer spin. (This matches crux1 Part 4 / verifier: N enters
# any Z2 only by MULTIPLICATION (homomorphism), == identity for N odd, never as
# the AFFINE +1 shift a fermion needs.)
print()
print("(ii.5) Where N=3 lives, and whether it feeds the 2*pi phase.")
print("   N=3 = the eps_abc singlet rank / the DIMENSION of the fundamental")
print("   (3 oscillators), NOT a pi_5(SU(3))=Z WZW LEVEL (su3_field #50: the")
print("   integer-WZW channel is non-native).")
print("   The 2*pi phase is exp(-i 2*pi M), M = total INTEGER L_z. Having 3")
print("   oscillators changes the RANGE of M but never makes it half-integer.")
print("   => N=3 does NOT enter as exp(i*pi*N). Consistent with crux1 #51: N")
print("      can act on the Z2 only by MULTIPLICATION (==identity for N odd),")
print("      never as the AFFINE +1 shift a fermion requires.")
# Symbolic: exp(-i 2 pi M) for the largest |M| reachable with k quanta from 3 modes:
for M in [0,1,2,3]:
    print("      exp(-i 2*pi*M) for M=%d:" % M, sp.simplify(sp.exp(-I*2*sp.pi*M)),
          "  exp(i*pi*N) with N=3 would be:", sp.simplify(sp.exp(I*sp.pi*3)))

print()
print("   >>> ROUTE (ii) DERIVED RESULT: U(2*pi)=+1 on every su(3) Fock state;")
print("       NO projective/anomalous phase (traceless => no central extension);")
print("       NO half-integer fundamental (metric gives the 3, not the SU(2) 2);")
print("       N=3 has no channel into the 2*pi phase. Phi_(ii) = 0 (mod 2*pi).")

# ----------------------------------------------------------------------------
print()
print("#"*74)
print("# CENTRAL-TRAP SELF-AUDIT (was the phase DERIVED, not INSERTED?)")
print("#"*74)
print("""
The verdict is Phi = 0 (FREE). The trap is symmetric: it forbids INSERTING a
phase to get pi; here we must confirm we did not ARTIFICIALLY ZERO a phase by
omitting a native term. Audit, term by term:

 - Route (i.1): Phi=0 followed from L2+L4 being REAL & P/T-EVEN (a DERIVED
   property: hopf_spinor #47c, su3_field #50, verified there). A real symmetric
   fluctuation operator HAS a real Gaussian covariance -> Im Tr = 0. Nothing
   omitted; the reality is a theorem about the settled action.
 - Route (i.2): Phi=0 followed from the collective Lagrangian having NO
   linear-in-velocity term (monodromy_depth #49 verified ONLY (Psi')^2, (chidot)^2,
   zero linear, zero bare -- for BOTH S^2 and the S^3 lift). A linear term is
   EXACTLY the WZW/Berry term; including one by hand would be the IMPORT. We did
   NOT add it AND we confirmed the native reduction does not produce it.
 - Route (ii): Phi=0 followed from (a) integer-spin carrier (3 of su(3),
   l=1, L^2=2), (b) traceless Gell-Mann => no normal-ordering central extension
   => honest (non-projective) rep, (c) no native half-integer fundamental
   (su3_field #50). Each is a COMPUTED property of the operator algebra, not an
   assumed sign.

 - The ONE place a pi COULD have entered (a WZW/Hopf/theta term, an FR sign, an
   N_c coefficient) is exactly what the contract forbids inserting -- and what
   #47c/#49/#50/#51 independently DERIVED to be ABSENT from the native theory.
   We did not insert it; we confirmed its absence is the REASON for Phi=0.

CONCLUSION: Phi=0 is DERIVED from the absence (proven elsewhere, reused here) of
the native term that would source it, plus computed reality/integrality/non-
projectivity of the soliton's own quantum state. NOTHING was inserted; NOTHING
native was omitted. TRAP CLEARED.
""")

print("="*74)
print("VERDICT")
print("="*74)
print("Route (i)  Phi = 0 (mod 2*pi)  -- FREE / boson side")
print("Route (ii) Phi = 0 (mod 2*pi)  -- FREE / boson side")
print("Combined single yes/no: postulate A is NOT derived.")
print()
print(">>> VERDICT: FAIL / FREE. Postulate A (the fermion) is IRREDUCIBLE in the")
print("    quantized angular sector of the settled L2+L4 S^2 hedgehog. The free")
print("    pi_4(S^2)=Z2 coin (crux1 #51) is NOT landed by the quantum Berry/")
print("    geometric/anomaly phase: that phase is 0, exactly as the honest prior")
print("    predicted. UDT must POSTULATE the fermion (like the SM); it is not")
print("    forced by quantizing the soliton's collective/angular coordinates.")
print()
print("USEFUL STRUCTURAL FINGERPRINT (even though FREE):")
print(" - The integer-spin carrier (3 of su(3), l=1) makes U(2*pi)=+1 EXACTLY;")
print("   the fermion would need a SPINOR fundamental (2 of SU(2)) the metric")
print("   does not supply -- the obstruction is the CARRIER (integer vs half-")
print("   integer rep), localized cleanly.")
print(" - The absence of a fermionic phase is now traced to a SINGLE missing")
print("   object across all routes: a LINEAR-IN-VELOCITY (WZW/theta/Berry) term")
print("   / a half-integer fundamental. Routes (i.2) and (ii.4) are the SAME")
print("   missing object viewed as dynamics vs representation -- the coin-flip")
print("   crux collapses to: 'is there a native double cover (SU(2)/spinor /")
print("   WZW line bundle)?' Answer across #47/#49/#50/#51 + here: NO.")
print(" - N=3 enters the Z2 ONLY multiplicatively (==identity, N odd), never")
print("   as the affine +1 shift -- confirmed at the operator level (ii.5).")
