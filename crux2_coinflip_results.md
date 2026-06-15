# Coin-Flip Crux 2 — The Postulate-A Test (the quantized Berry/anomaly phase) — Results

Date: 2026-06-15. Driver: Claude (Opus 4.8, 1M context). NEW file
(append-never-edit, Self-Hardening discipline). Mode: **OBSERVE/DERIVE-gated**
(the pre-registered coin-flip Crux 2 — the postulate-A test). Frozen contract:
`crux2_coinflip_contract.md` (signed off; nothing retuned after).
**DATA-BLIND**: STATISTICS ONLY. No mass/ratio/wall number / Koide / sqrt(2) /
45-deg loaded, computed, or compared.

THE QUESTION (verbatim from the contract): when the angular collective
coordinates are quantized (hbar applied; real n -> the complex su(3)-triplet
Hilbert space, #50's door), does an EMERGENT quantum Berry/geometric/anomaly
phase around the 2pi-spatial-rotation loop (= the FR exchange loop, generator of
pi_4(S^2)=Z2) EQUAL exp(i*pi*N) (N=3), AFFINELY shifting the free Z2 onto the
fermionic (-1) side?

Script (commit-grade, this push):
- `crux2_coinflip.py` — sympy CPU: route (i) the collective-coordinate /
  rigid-rotor Berry phase (Gaussian fluctuation-vacuum connection + free-rotor
  holonomy); route (ii) the su(3) oscillator operator-algebra / rep-theory phase
  (spin-1 carrier, Fock-state U(2pi), normal-ordering central-extension test,
  half-integer-sector test, the N=3 channel test). All checks run; the one
  symbolic identity (Im Tr[S^{-1}dS]=0 for real S) is asserted.

Blind verifier: **PENDING** (verifier-before-record; attack-here block at end).

---

## 0. PREMISE LEDGER (every fixed value tagged chose vs derived)

| # | Premise | chose / derived | note |
|---|---------|-----------------|------|
| P1 | The settled carrier is the degree-1 S^2 baby-Skyrme hedgehog, L = L2 + L4, ONE radial profile Theta(r) + RIGID SO(3) orientation; no 2nd internal profile | DERIVED | native_stabilizer; monodromy_depth #49 (chi rigid cyclic) |
| P2 | The statistics loop is the 2pi spatial-rotation = FR exchange loop, generator of pi_4(S^2)=Z2; the coin is two-sided but classically FREE | DERIVED | crux1 #51 (blind-verified 7e2b9c4f1a8d6035) |
| P3 | Quantization promotes the 3 complex l=1 amplitudes z=(z_-1,z_0,z_+1) to a genuine complex Hilbert triplet (su(3) as the OPERATOR algebra) — #50's open door | DERIVED-as-the-door | su3_field #50 (classically z collapses to real n; the quantum sector is the genuine complex triplet) |
| P4 | L2, L4 are REAL and P/T-EVEN (no metric-free, T-odd Hopf term; no linear-in-velocity WZW/theta term) | DERIVED | hopf_spinor #47c; monodromy_depth #49 (only (Psi')^2,(chidot)^2; zero linear, zero bare); su3_field #50 |
| P5 | The su(3) generators are the normal-ordered bilinears T^i = a^dag(lambda^i/2)a of the 3 oscillators; spatial rotation acts via su(3) ⊃ so(3) (the l=1 L_a) | DERIVED-as-construction | the standard Schwinger/Jordan oscillator realization of su(3) on the l=1 carrier |
| P6 | The Berry connection of a Gaussian (squeezed-vacuum) state is a = (1/2) Im Tr[S^{-1} dS], S the complex covariance | DERIVED (standard) | the geometric phase of a Gaussian ground state |
| P7 | "DERIVED, not IMPORTED" = the phase is computed from the soliton's own quantum state (fluctuation vacuum / collective wavefunction / su(3) rep structure) as a function of the loop parameter; inserting a WZW/Hopf/FR/N_c term = IMPORT = FAIL | CHOSE (the contract's central trap, adopted verbatim) | crux2 contract |

---

## ROUTE (i) — RIGID-ROTOR / COLLECTIVE-COORDINATE BERRY PHASE

**Setup.** Collective-coordinate quantization of the degree-1 hedgehog. The
zero modes the 2pi spatial rotation excites are the rigid orientation A in
SO(3); the quantum state is Psi(A) on the collective manifold; the Berry
connection is a(A) = i <vac(A)| d/dA |vac(A)>, and Phi = oint_gamma a (mod 2pi)
on the 2pi-rotation loop gamma. The phase is computed from the EXPLICIT
A-dependence of the soliton's own quantum ground state — the bosonic
fluctuation vacuum and the collective wavefunction — not by inserting a term.

### (i.1) Bosonic fluctuation-vacuum Berry connection = 0 [DERIVED]
|vac(A)> is the Gaussian ground state of the quadratic Hamiltonian of the small
oscillations delta-n about n_A. Its Berry connection is a = (1/2) Im Tr[S^{-1}dS]
(P6), with S the complex covariance/width matrix. The L2+L4 fluctuation operator
about the REAL hedgehog n_A is a **REAL symmetric** operator (P4: L2, L4 real,
P/T-even). A real symmetric fluctuation operator has a **REAL** ground-state
covariance S(A) = S*(A). For real S (and real dS), Tr[S^{-1}dS] is real, so its
imaginary part vanishes:

    a = (1/2) Im Tr[S^{-1} dS] = 0    (symbolically asserted == 0 in-script).

> **(i.1) RESULT: the fluctuation vacuum contributes ZERO Berry phase on any
> loop, including the 2pi rotation. DERIVED from the reality of L2+L4.**

### (i.2) Collective free-rotor 2pi holonomy = +1 [DERIVED]
The collective Lagrangian (monodromy_depth #49, verified) is purely kinetic,
L_coll = (1/2) Omega_a Lambda_ab Omega_b, with **ZERO linear-in-Omega term**. A
linear-in-velocity term IS the would-be WZW/theta (Berry) term; #49 verified the
iso-twist enters ONLY as (Psi')^2 and chi as (chidot)^2 — no bare/linear term —
for BOTH the S^2 baby-Skyrme and the S^3 lift. Hence the collective connection
is FLAT, and the geometric phase on the 2pi loop is the pure HOLONOMY of the
rotor's configuration-space topology, NOT an induced Berry phase. The free-rotor
wavefunction Psi(A) is a single-valued FUNCTION on the soliton's orientation
SO(3) (the rotation R and R+2pi act IDENTICALLY on the real field n_A — SO(3)
closes at 2pi). With no WZW term there is no line bundle to make Psi
double-valued, so Psi(2pi) = Psi(0): holonomy = +1. The half-integer (spinor /
fermion) sector requires a WZW term to twist the bundle — inserting one = IMPORT
= FAIL.

> **(i.2) RESULT: collective-rotor 2pi holonomy = +1 (Phi = 0, boson side).
> DERIVED from the absence of a linear-in-velocity term.**

> **ROUTE (i) DERIVED RESULT: Phi_(i) = 0 (mod 2pi). FREE / boson.**

---

## ROUTE (ii) — su(3) OPERATOR-ALGEBRA / REPRESENTATION-THEORY ROUTE

**Setup (the genuine open door, #50).** Promote the 3 complex l=1 amplitudes to
BOSONIC oscillators a_m, a_m^dag ([a_m,a_n^dag]=delta_mn, m in {-1,0,+1}). The
su(3) generators are the normal-ordered bilinears T^i = a^dag(lambda^i/2)a (P5),
closing on su(3) and acting on Fock space. Spatial rotation acts through
su(3) ⊃ so(3); the 2pi loop is U(2pi) = exp(-i 2pi n.L). We compute the phase
U(2pi) imprints from the REP STRUCTURE alone, without inserting any coefficient.

### (ii.1) The carrier is INTEGER spin (the 3, l=1) [DERIVED]
The su(3) ⊃ so(3) generators on the 3 amplitudes satisfy [Lx,Ly]=iLz exactly,
with L^2 = l(l+1) = **2 => l = 1** (integer spin). Exact sympy:

    U(2pi) = exp(-i 2pi Lz) = 1_3   (the identity on the triplet).

> **(ii.1) U(2pi) = +1 (identity) on the su(3) triplet — integer spin, trivial
> 2pi rotation.**

### (ii.2) Every Fock state carries U(2pi) = +1 [DERIVED]
L_z(Fock) = sum_m m a_m^dag a_m with m in {-1,0,+1} (all integer). Any Fock
state |state> = prod a_{m_k}^dag |0> has total L_z = sum m_k = INTEGER M, so
U(2pi)|state> = exp(-i 2pi M)|state> = (+1)|state>. The bosonic-oscillator su(3)
Fock space carries ONLY integer spin; U(2pi) = +1 on every state. No
half-integer (fermionic) sector.

### (ii.3) NO projective / anomalous phase [DERIVED]
A fermionic phase could only come from a PROJECTIVE rep / central extension (an
anomaly) in the normal-ordered su(3). The normal-ordering shift of
T^i = a^dag(lambda^i/2)a is the c-number (1/2)Tr(lambda^i). For all 8 Gell-Mann
matrices, Tr(lambda^i) = 0 (computed in-script: [0,0,0,0,0,0,0,0]). Hence
normal ordering produces NO central c-number => NO central extension => the
su(3) is represented HONESTLY (not projectively) => NO anomalous/projective
phase. [DERIVED, finite-mode (3-oscillator) normal ordering.]

### (ii.4) No native half-integer fundamental [DERIVED, reused #50]
The ONLY way the su(3) Fock construction yields half-integer SO(3) spin is if
the fundamental oscillators carried half-integer m — i.e. if the carrier were
the 2 of SU(2) (a genuine spinor), not the 3 of su(3). su3_field #50 DERIVED
that the metric supplies the REAL n / the 3 (S^2 target), NOT the SU(2)/S^3
spinor target. No half-integer fundamental exists to build a fermion from;
inserting a 2-of-SU(2) carrier = IMPORT = FAIL.

### (ii.5) N=3 has no channel into the 2pi phase [DERIVED]
N=3 is the eps_abc singlet rank / the DIMENSION of the fundamental (3
oscillators), NOT a pi_5(SU(3))=Z WZW level (the integer-WZW channel is
non-native, #50). The 2pi phase is exp(-i 2pi M) with M the total integer L_z;
having 3 oscillators changes the RANGE of M but never makes it half-integer. So
N=3 does NOT enter as exp(i*pi*N). This matches crux1 #51 (and its blind
verifier): an integer N can act on the Z2 only by MULTIPLICATION (a
homomorphism Z2->Z2, == identity for N odd), never as the AFFINE +1 shift a
fermion requires. Explicit: exp(-i 2pi M) = +1 for M = 0,1,2,3, whereas
exp(i*pi*3) = -1 — the two never coincide because M is forced integer.

> **ROUTE (ii) DERIVED RESULT: U(2pi) = +1 on every su(3) Fock state; NO
> projective/anomalous phase (traceless Gell-Mann => no central extension); NO
> native half-integer fundamental (the metric gives the 3, not the SU(2) 2);
> N=3 has no channel into the 2pi phase. Phi_(ii) = 0 (mod 2pi). FREE / boson.**

---

## CENTRAL-TRAP SELF-AUDIT (was the phase DERIVED, not INSERTED?)

The verdict is Phi = 0 (FREE). The trap is symmetric: it forbids INSERTING a
phase to manufacture pi, and equally we must confirm we did not ARTIFICIALLY
ZERO a phase by omitting a native term. Term by term:

- **(i.1):** Phi=0 followed from L2+L4 being REAL & P/T-even (a DERIVED property:
  hopf_spinor #47c, su3_field #50, verified there) — a real symmetric
  fluctuation operator has a real Gaussian covariance => Im Tr = 0. Nothing
  omitted; the reality is a theorem about the settled action.
- **(i.2):** Phi=0 followed from the collective Lagrangian having NO
  linear-in-velocity term (monodromy_depth #49 verified ONLY (Psi')^2,(chidot)^2,
  zero linear, zero bare — for BOTH S^2 and the S^3 lift). A linear term IS the
  WZW/Berry term; including it by hand would be the IMPORT. We did not add it AND
  confirmed the native reduction does not produce it.
- **(ii):** Phi=0 followed from (a) integer-spin carrier (3 of su(3), l=1,
  L^2=2), (b) traceless Gell-Mann => no normal-ordering central extension =>
  honest (non-projective) rep, (c) no native half-integer fundamental (#50).
  Each is a COMPUTED property of the operator algebra, not an assumed sign.
- The ONE place a pi could have entered (a WZW/Hopf/theta term, an FR sign, an
  N_c coefficient) is exactly what the contract forbids inserting — and what
  #47c/#49/#50/#51 independently DERIVED to be ABSENT from the native theory. We
  did not insert it; we confirmed its absence is the REASON for Phi=0.

> **CONCLUSION: Phi=0 is DERIVED from the absence (proven elsewhere, reused
> here) of the native term that would source it, plus computed reality /
> integrality / non-projectivity of the soliton's own quantum state. NOTHING
> was inserted; NOTHING native was omitted. TRAP CLEARED.**

---

## VERDICT — **FAIL / FREE** (postulate A IRREDUCIBLE)

| route | observable | derived value |
|---|---|---|
| (i) rigid-rotor / collective-coordinate Berry phase | Phi_(i) | **0 (mod 2pi)** |
| (ii) su(3) operator-algebra / rep-theory phase | Phi_(ii) | **0 (mod 2pi)** |

Combined single yes/no: **postulate A is NOT derived.** Against the frozen
criteria:
- PASS (Phi = pi*N, N=3, DERIVED) — **not met**.
- FAIL / FREE (Phi = 0, or undetermined, or N put in by hand) — **MET**:
  Phi = 0 in both routes, DERIVED.
- OTHER coefficient (not pi*N) — **not applicable** (the phase is exactly 0).

> **VERDICT: FAIL / FREE. Postulate A (the fermion) is IRREDUCIBLE in the
> quantized angular sector of the settled L2+L4 S^2 hedgehog. The free
> pi_4(S^2)=Z2 coin (crux1 #51) is NOT landed by an emergent quantum Berry /
> geometric / anomaly phase: that phase is 0, exactly as the pre-registered
> HONEST PRIOR predicted. UDT must POSTULATE the fermion (as the SM does); it is
> not forced by quantizing the soliton's collective / angular coordinates.**

The honest prior is CONFIRMED, not surprised. Per hypothesis discipline the
blind verifier is still aimed hardest at any way a PASS could have been missed
(see attack-here block) — but no PASS was produced to defend.

---

## USEFUL STRUCTURAL FINGERPRINT (even though FREE)

Per Charles (a potentially ill-posed question may still emit useful info):

1. **The obstruction is the CARRIER's representation, localized cleanly.** The
   integer-spin carrier (the 3 of su(3), l=1) makes U(2pi) = +1 EXACTLY. The
   fermion would need a SPINOR fundamental (the 2 of SU(2), half-integer m) that
   the metric does not supply. The coin-flip does not fail for a subtle dynamical
   reason — it fails because the native carrier is an integer-spin rep.

2. **All routes collapse to ONE missing object: a native double cover.** Route
   (i.2) (no linear-in-velocity / WZW term) and route (ii.4) (no half-integer
   fundamental) are the SAME obstruction viewed as DYNAMICS vs REPRESENTATION.
   The entire coin-flip crux reduces to a single yes/no: *does the native theory
   admit a double cover — an SU(2)/spinor target, or a WZW line bundle that makes
   the collective wavefunction double-valued?* Answer, consistent across
   #47/#49/#50/#51 and confirmed here at the quantized level: **NO.** This is the
   sharpest statement yet of where the fermion would have to come from.

3. **N=3 enters the Z2 only multiplicatively, never affinely — now confirmed at
   the OPERATOR level.** crux1 #51 showed this topologically (degree-N acts as
   xN mod 2 = identity for odd N); here it is reconfirmed at the level of the
   quantized rotation: U(2pi) = exp(-i 2pi M), M integer, = +1 regardless of how
   many (3) oscillators carry it. The affine +1 shift a fermion needs has no
   operator channel from the count N=3.

4. **The traceless-Gell-Mann no-anomaly result is a positive structural fact.**
   The finite-mode (3-oscillator) su(3) is represented honestly (no central
   extension), so the genuinely open door #50 named — "could the quantized su(3)
   carry an anomalous/projective phase?" — is now CLOSED for the bosonic
   oscillator realization: it cannot. A projective phase would require either a
   non-traceless generator set (not su(3)) or an infinite-mode anomaly (not the
   finite l=1 carrier).

---

## PREMISE LEDGER ROLLUP (chose vs derived)

DERIVED (computed / reused-and-confirmed):
- (i.1) real symmetric fluctuation operator => real Gaussian covariance =>
  Im Tr[S^{-1}dS] = 0 (symbolic, asserted).
- (i.2) collective Lagrangian has no linear-in-velocity term (#49) => flat
  connection => single-valued Psi on SO(3) => 2pi holonomy = +1.
- (ii.1) the carrier is l=1 (L^2=2, integer spin); U(2pi)=1_3 exactly.
- (ii.2) every Fock state has integer total L_z => U(2pi)=+1.
- (ii.3) all Tr(lambda^i)=0 => no central extension => non-projective rep => no
  anomalous phase.
- (ii.4) no native half-integer fundamental (the metric gives the 3, not the
  SU(2) 2; su3_field #50).
- (ii.5) N=3 has no channel into the 2pi phase (consistent crux1 #51).

CHOSE (provisional, tagged; none a smuggled mechanism):
- P7, the contract's central-trap criterion ("DERIVED = computed from the
  soliton's own quantum state; inserting a term = IMPORT = FAIL"), adopted
  verbatim.
- The Schwinger/oscillator realization of su(3) on the l=1 carrier (P5) — the
  standard quantization of the angular amplitudes, #50's door made operator.

NOT CLAIMED: no mass/ratio/wall-number; no PASS to defend; the fermion is not
excluded as a POSTULATE — it is shown not to be FORCED by this quantization.

---

## SCOPE (premise set carried by this negative, for NEGATIVES_REGISTRY)

Single-cell; settled L2+L4 S^2 baby-Skyrme charge-1 easy-axis hedgehog; the 2pi
spatial-rotation = FR exchange loop (pi_4(S^2)=Z2 generator, crux1 #51);
collective-coordinate / rigid-rotor quantization (Gaussian fluctuation vacuum +
free-rotor holonomy) for route (i); the bosonic Schwinger-oscillator su(3)
realization on the l=1 amplitudes for route (ii); hbar applied as a solid
anchor; L2,L4 real & P/T-even with no linear-in-velocity / WZW / Hopf term (#47c,
#49, #50). If a DIFFERENT carrier admits a genuine SU(2)/spinor (S^3) target, OR
a native linear-in-velocity (WZW/theta/Berry) term is uncovered, OR an
inter-cell/ensemble phase links the collective coordinate, the existence
question REOPENS and this negative is CONDITIONS-CHANGED.

---

## BLIND VERIFIER — PENDING. ATTACK HERE:

1. **The Gaussian-vacuum-Berry-connection = 0 claim (i.1, load-bearing).**
   Independently confirm a = (1/2) Im Tr[S^{-1}dS] for a Gaussian ground state,
   and that a REAL symmetric L2+L4 fluctuation operator forces a real covariance
   S (so a = 0). Attack: is there ANY native complex structure in the fluctuation
   operator (e.g. a first-order-in-time / gyroscopic term, a Berry curvature from
   the L4 winding) that would make S genuinely complex and a nonzero? If one
   exists, route (i.1) reopens.
2. **The "no linear-in-velocity term" claim (i.2).** Re-derive that the
   collective Lagrangian is purely kinetic (no WZW/theta linear-in-Omega term)
   from the settled L2+L4 — cross-check monodromy_depth #49 (only (Psi')^2,
   (chidot)^2). Try to EXHIBIT a linear-in-velocity term from the back-reaction,
   the seal mirror-fold, or an L4 cross term — if present, the rotor connection
   is not flat and the 2pi holonomy may be nontrivial.
3. **The single-valued-Psi-on-SO(3) claim (i.2).** Challenge whether the
   soliton's orientation manifold is SO(3) (2pi loop noncontractible, +1 for a
   FUNCTION) and whether any native structure could make Psi a section of a
   nontrivial bundle (double cover) WITHOUT inserting a WZW term.
4. **The integer-spin carrier (ii.1/ii.2).** Confirm L^2=2 (l=1) and U(2pi)=1_3
   exactly; confirm every Fock state has integer L_z. Attack: could a DIFFERENT
   native quantization of the l=1 amplitudes (e.g. a constrained/projected Fock
   space, a CP^2 coherent-state quantization) carry a half-integer or
   fractional 2pi phase?
5. **The no-anomaly claim (ii.3, the genuine open door).** Re-derive that
   Tr(lambda^i)=0 for all 8 Gell-Mann matrices => no normal-ordering central
   extension => non-projective rep. Attack the FINITE-mode assumption: is there
   any regularization / infinite-tower (higher-l) completion of the angular
   sector that WOULD produce a central extension / projective phase? (This is the
   one place a PASS could still hide — aim hardest here.)
6. **The N=3 channel (ii.5).** Confirm N=3 enters only multiplicatively (==
   identity for odd N), never affinely. Try to EXHIBIT an operator channel by
   which the count 3 becomes a half-integer 2pi phase (should fail without a
   spinor fundamental / integer-WZW level #50 denies).
7. **Targeting check.** The verdict is FREE (Phi=0), matching the honest prior.
   Confirm it was DERIVED from the soliton's own quantum state, not steered;
   confirm NO WZW/Hopf/FR/N_c term was inserted (no IMPORT), AND no native term
   was silently omitted to force Phi=0 (the symmetric trap). Confirm no
   mass/ratio/wall-number entered.

---

## BLIND ADVERSARIAL VERIFIER PASS — 2026-06-15

VERIFIER crux2_coinflip / 2026-06-15 / 3069f8befd063fb8 (independent machinery —
own Gaussian-state Berry-connection construction, own spin-1 / su(3) generators
from the angular-momentum algebra, own field-theoretic / measure / cocycle
reasoning; NOT a re-run-and-agree of crux2_coinflip.py).

VERDICT: **STANDS-WITH-CAVEAT.** Both routes give Phi=0; the result FAIL/FREE
(postulate A IRREDUCIBLE) survives independent reproduction AND the hardest
field-theoretic / infinite-mode / measure-anomaly attack the contract flagged.
The caveat is scoping, not load-bearing: the result's own "all routes collapse to
ONE missing object = a native double cover" fingerprint is SOUND, and the one
genuine residual hinge (the sigma-grading of omega_H1 under the same-minus seal,
#47b) is correctly a CONDITIONS-CHANGED trigger, not a present defect.

INDEPENDENTLY REPRODUCED (own machinery):
- ROUTE (i.1). Built the Gaussian (squeezed) ground-state Berry connection
  a = i<psi|d_A psi> from scratch. For ANY REAL normalized state a=0 exactly
  (<psi|d_A psi> = (1/2)d_A<psi|psi> = 0, and real). SHARPENED the attack
  surface: the ONLY way to a nonzero connection is a COMPLEX vacuum width
  W=Wr+iWi, giving Re(a) = dWi/(4 Wr) != 0 — which requires an antisymmetric
  p-q (first-order-in-time / gyroscopic) term in the fluctuation Hamiltonian.
  That term IS the linear-in-velocity WZW/Berry term #49 verified ABSENT (only
  (chidot)^2,(Psi')^2). So Wi=0 -> a=0. (i.1) reproduced, vulnerability located.
- ROUTE (ii). Rebuilt spin-1 generators from the |1,m> algebra (not the script's
  matrices): [Jx,Jy]=iJz, J^2=2 (l=1). U(2pi)=exp(-i2pi n.J)=1_3 for ANY axis
  (integer eigenvalues {1,0,-1}). Rebuilt su(3) from E_ij: all 8 generators
  traceless => no normal-ordering c-number => non-projective rep. Reproduced.

THE KEY TEST — FIELD-THEORETIC / INFINITE-MODE / MEASURE ATTACK (the flagged
vulnerability that the result is a finite collective-coordinate truncation). All
four named routes hunted HARDEST for a nonzero phase; ALL closed by the SAME
firewall the finite result used, now lifted to the functional level:
 (a) Fermionic determinant / eta-invariant / spectral-flow: requires a
     fundamental fermion to integrate out — ABSENT (hopf_spinor #47c: bosonic
     CP^1, no first-order Dirac op). The bosonic functional determinant
     det(-D^2+...) is a real-positive Laplace-type det (phase 0); there is NO
     bosonic eta (eta needs a first-order Dirac spectrum). The (i.1) reality
     LIFTS to infinite modes. NO PASS.
 (b) WZW/theta from the MEASURE (Fujikawa Jacobian): the bosonic sigma-model
     Jacobian is the target-curvature (beta-function) anomaly — a P/T-EVEN
     LOCAL term, NOT a P/T-ODD topological WZW/Hopf. And it cannot manufacture
     an integer N=3 coefficient: the only 5D slot is pi_5(S^2)=Z2 (a FREE sign,
     no Z to hold 3). NO PASS.
 (c) 2-cocycle / projective phase from the full current algebra: a Schwinger /
     Mickelsson-Faddeev cocycle is an INTERNAL gauge anomaly, the WRONG object
     for the spatial-rotation spin-statistics Z2 (the rotation generator is the
     spacetime L, fixed by integer spin). And a projective rep of the rotation
     itself is classified by H^2(SO(3),U(1))=Z2 = the SAME free Z2 (the SU(2)
     double cover) — a CHOICE of lift, not a derived pi*N. NO derived PASS.
 (d) Is the rigid-rotor truncation topologically faithful (sees pi_4(S^2)=Z2)?
     YES to the COIN's EXISTENCE: the rotor's 2pi loop = gen of pi_1(SO(3))=Z2
     = the same loop that suspends to S^4->S^2 = pi_4(S^2)=Z2 (crux1). The
     truncation faithfully sees the noncontractible loop (both sides of the
     coin); what it cannot see is a PHASE assigned to the loop by a topological
     term OUTSIDE its finite action — and that term is exactly the
     absent/free WZW sign (b)/(c). No HIDDEN derived phase. NO PASS.
 OUTCOME: NO nonzero DERIVED phase exists at the field-theoretic level. The
 truncation did not hide a fermion; the functional computation reproduces Phi=0.

EXTRA SUBTLE CHECK (the real-Skyrme fermion mechanism, not in the doc's framing):
in the genuine Skyrme model the fermion appears NOT as "holonomy +1" but via the
FR-constrained HALF-INTEGER offset nu in the spin tower E_n=E0+hbar^2(n+nu)^2/2L
(#49), with nu=N_c*B/2 from the integer-graded 5D WZW (pi_5(SU(3))=Z). I checked
whether our rotor smuggles nu=1/2: nu is FIXED by the rotor WZW term, which #49
verified ABSENT and #50 found has no integer channel => nu=0 (boson) is DERIVED,
not assumed. Half-integer nu would require the very WZW term the contract forbids
importing. The script's "holonomy +1" IS the nu=0 statement and correctly
inherits nu=0 from the verified-flat rotor. CONFIRMS FAIL/FREE; does not break it.

SYMMETRIC DERIVED-NOT-IMPORTED AUDIT (did the constructor OMIT a native term to
force Phi=0?). Three candidates assessed by independent degree/parity reasoning:
 - SEAL eta=1/18 transgression: a 2-form in H^2, EXACT, sigma-EVEN, with no leg
   along the rotor loop. A statistics WZW is a 3-form (P/T-ODD). Wrong DEGREE
   (2!=3), wrong PARITY, wrong location. Cannot source a 2pi phase. Not omitted.
 - NONSTATIONARY / time-row sector: the one route that COULD deposit a linear-
   in-velocity term -> complex width -> nonzero (i.1). But #46's forced source is
   sigma-odd yet seal-vanishing and quadratic; #49 verified (chidot)^2 only, zero
   linear, for S^2 AND S^3; antiperiodic time is not even admitted for interval
   time (canon). Correctly scoped out; OPEN only if time CLOSES (a premise
   change). Properly a CONDITIONS-CHANGED trigger, not a silent omission.
 - sigma-ODD omega_H1 / genuine S^3-Hopf lift (#47b, THE sharpest candidate):
   a parity re-grading of a 2-form (omega_H1, H^2) cannot make it a 3-form Hopf
   term (degree firewall); it feeds the SEPARATE background spin-structure Z2
   (crux1's (c)), not the soliton's FR coin; and even an S^3 lift carries
   (Psi')^2 only with Hopf invariant 0 (crux1 numerics). Does NOT source a
   derived 2pi phase on current evidence.
 AUDIT VERDICT: NO native term was wrongfully omitted. Phi=0 is derived from a
 genuine absence (degree/parity/integer-channel firewalls), not a hidden zeroing.
 The symmetric trap is CLEARED both ways (nothing inserted; nothing omitted).

FINGERPRINT CHECK: "all routes collapse to ONE missing object = a native double
cover." SOUND. Route (i.2) no-linear-term, route (ii.4) no-half-integer-
fundamental, the nu=0 offset, and the field-theoretic (b)/(c)/(d) are all the
SAME object — the absence of (a WZW line bundle / a half-integer rep / an SU(2)
spinor target / a flat-Z2-nontrivial-connection), i.e. a native DOUBLE COVER.
Every face is the free pi_5(S^2)=Z2 sign vs the absent integer pi_5(SU(3))=Z
level. The collapse is genuine, not a narrated convergence.

RESIDUAL OPEN HINGE (correctly handed forward, not a defect here): the
sigma-grading of omega_H1 under the same-minus mirror seal (#47b) — IF (against
the degree firewall) it were ever shown to inject a P/T-ODD 3-form / open a
Hopf-nontrivial S^3 lift, OR if time closes into a circle (admitting the
antiperiodic structure), the existence question REOPENS and this negative is
CONDITIONS-CHANGED. On present evidence both firewalls (degree 2!=3; parity
even-vs-odd; no integer pi_5 channel) hold, so Phi=0 is not artificially forced.

TARGETING CHECK: the verdict FREE (Phi=0) was DERIVED from the soliton's own
quantum state (real Gaussian vacuum; integer-spin l=1 carrier; traceless su(3))
plus the reused, blind-verified absences (#47c/#49/#50/#51), not steered. No
WZW/Hopf/FR/N_c term was inserted (no IMPORT); no native term was silently
omitted (symmetric trap cleared). No mass / ratio / Koide / sqrt(2) / 45-deg /
wall number was loaded, computed, or compared (DATA-BLIND held). The result does
not over-claim (the fermion is NOT excluded as a POSTULATE — only shown not
FORCED) nor under-claim (a genuine two-sided coin exists; it is simply unlanded).

VERIFIER crux2_coinflip / 2026-06-15 / 3069f8befd063fb8
