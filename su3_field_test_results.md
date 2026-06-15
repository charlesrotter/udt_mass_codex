# Does the UDT metric force a GENUINE complex SU(3)-valued l=1 field? — Results

Date: 2026-06-15. Driver: Claude (Opus 4.8, 1M context). NEW file
(append-never-edit, Self-Hardening discipline). Mode: **OBSERVE** (gated,
authorized by Charles 2026-06-15). DATA-BLIND (no mass/ratio/wall number
loaded).

THE QUESTION: the project's DERIVED angular field is the REAL unit 3-vector
n (S^2, 2 DOF); su(3) appears only as the OPERATOR/symmetry algebra of the
l=1 carrier (8 = 3 (+) 5, a selection rule — UDT_REBUILD §3), and the
"quark" two-weight charges are assigned LABELS, not a derived complex field.
The open question, never directly tested: does the UDT METRIC actually
FORCE or ADMIT a GENUINE complex SU(3)-VALUED l=1 field — the structure a
native INTEGER WZW term (pi_5(SU(3))=Z => N_c=3, forcing the soliton to be
a fermion) requires — or does the metric only ever provide the REAL
direction n (S^2) + the native U(1) phase (the photon, em_forcing) +
SO(3,1) (gravity)?

WHY THIS IS THE CRUX (context, not re-derived): #49 (monodromy_depth,
blind-verified) established that the ENTIRE quantum completion (fermion
statistics + sqrt(m) + the depth/mass ladder) collapses to ONE question —
does UDT have a native WZW/Hopf term tied to N=3=N_c? That term lives ONLY
on a genuine SU(3)-valued (or S^3) field. The S^2/real-n case gives only a
FREE Finkelstein-Rubinstein Z_2 (#47/#49).

Scripts (commit-grade, this push):
- `su3_field_test.py` — sympy CPU: constructs the complex l=1 amplitude
  triplet z in C^3, relates it to the real n, builds the spin-1 (SO(3))
  generators + the rank-2 Q_ab (the 5 in 8=3+5), audits which generators a
  native connection supplies, and tests whether the relative phases of z are
  physical or collapse to the real n. All checks PASS (n-recovery exact;
  [Lx,Ly]=iLz exact; the native invariants are exactly functions of n).

Blind verifier: **PENDING** (verifier-before-record; attack-here block at end).

---

## 0. PREMISE LEDGER (every fixed value tagged chose vs derived)

| # | Premise | chose / derived | note |
|---|---------|-----------------|------|
| P1 | UDT background ds^2 = -e^{-2phi}c^2dt^2 + e^{2phi}dr^2 + r^2 dOmega^2, g_mn REAL | DERIVED | CANON; g^tt g^rr=-1 |
| P2 | The DERIVED angular field is the REAL unit 3-vector n, target S^2, 2 DOF | DERIVED | h1_types, angular_lagrangian (recon-confirmed) |
| P3 | The l=1 complex carrier z=(z_-1,z_0,z_+1) in C^3 = the SU(3)-fundamental "quark triplet"; relation to n = the standard unitary spherical<->cartesian map | DERIVED (kinematic identity) | z is the spherical-basis image of n |
| P4 | The only native angular kinetic term is L = -(xi/2) g^{mn} d_m z^dag d_n z (the unique 2-derivative diffeo+target-isometry scalar) | DERIVED-as-unique | angular_lagrangian D3-D4 |
| P5 | su(3) = 3 (+) 5 under SO(3): the 3 = antisymmetric L_a, the 5 = symmetric-traceless rank-2 Q_ab (the EXTRA SU(3) directions beyond U(1)xSO(3)) | DERIVED | standard l=1 rep theory; UDT_REBUILD §3 |
| P6 | The spin connection of a REAL metric g_mn is so(p,q)-valued (ANTISYMMETRIC frame indices) | DERIVED (theorem) | omega = antisymmetrized Christoffel in an orthonormal frame |
| P7 | The native U(1) (em_forcing, the photon) acts as the OVERALL phase (identity generator 1_3) | DERIVED | em_forcing_results.md; Maxwell A_m couples to the conserved abelian current |
| P8 | A "connection" requires a metric-given gauge 1-form Omega_m^A valued in a generator T_A; a GLOBAL symmetry (z^dag z invariant) is NOT a connection | DERIVED (definition) | gauging vs symmetry |
| P9 | "Genuine SU(3) field" = z is an INDEPENDENT complex triplet (not the spherical image of any real n) AND has all 8 generators acting physically | CHOSE (the criterion) | this is the operational definition of the thing under test |

---

## 1. TASK 1 — the complex l=1 field z in C^3 and its relation to n

The l=1 complex spherical-harmonic amplitudes form z = (z_{-1}, z_0, z_{+1})
in C^3 (the SU(3) fundamental / "quark" triplet). The project's REAL field n
maps to z by the standard unitary spherical<->cartesian change of basis
(`su3_field_test.py`, exact sympy):

    z_{+1} = -(n_x + i n_y)/sqrt2 ,   z_0 = n_z ,   z_{-1} = (n_x - i n_y)/sqrt2 .

- |z|^2 = z^dag z = n_x^2 + n_y^2 + n_z^2 = |n|^2 (=1 for the unit n). [exact]
- The inverse map recovers n EXACTLY: n_x = (z_{-1}-z_{+1})/sqrt2,
  n_y = (z_{-1}+z_{+1})/(-sqrt2 i), n_z = z_0 (residuals identically 0). [exact]

**DOF count:** a general z in C^3 = **6 real DOF**; the real unit n in S^2 =
**2 real DOF**. The gap = 4 real DOF: an overall U(1) phase, a |z| modulus
(radial), and the 2 RELATIVE phases of z_m. THE DECISIVE QUESTION (Tasks
2-3): does the metric make ANY of those 4 extra DOF PHYSICAL via a
connection — i.e. is z a genuinely independent complex triplet, or is it
just the spherical IMAGE of the real n (4 extra DOF unphysical)?

For the project's REAL n, z is NOT an independent complex triplet — its 6
real components are LOCKED to the 2 real components of n by the unitary map.
A GENUINE SU(3) field would require z to be free of any real-n parametrization.

---

## 2. TASK 2 — what CONNECTION does the REAL metric induce on z?

A connection enters z's kinetic term through the covariant derivative
D_m z = d_m z + Omega_m z, with Omega_m valued in the 3x3 generators.
U(3) on C^3 = U(1) [identity] (+) SU(3) [8 traceless]. Under the SO(3)
(spin-1) subgroup, su(3) = **3 (+) 5**:
- the **3** = antisymmetric L_a (the SO(3)/spin-1 generators; verified
  [Lx,Ly]=iLz exactly);
- the **5** = symmetric-traceless rank-2 Q_ab = {L_a,L_b} - (2/3)delta_ab L^2
  (verified Hermitian + traceless) — **the SU(3) directions BEYOND U(1)xSO(3).**

**The generator audit — which native term supplies which generator:**

| generator block | dim | native source | supplied? |
|---|---|---|---|
| U(1) (identity 1_3, overall phase) | 1 | the photon / Maxwell A_m (em_forcing) | **YES** |
| SO(3) (antisymmetric L_a) | 3 | the spin connection on the round S^2: omega_ph^{12} = -cos theta | **YES** |
| SO(3,1) boosts (t-r frame) | 3 | the spin connection (gravity) | **YES** |
| **rank-2 symmetric-traceless Q_ab (the EXTRA su(3))** | **5** | **— none —** | **NO** |

- **2a. The spin connection** of the real UDT metric is so(3,1)-valued:
  ANTISYMMETRIC in the frame indices (omega = the antisymmetrized Christoffel
  in an orthonormal frame, P6 — a theorem for any real symmetric g_mn). On
  the l=1 carrier it acts as the antisymmetric L_a ONLY. The angular piece is
  the round-S^2 Levi-Civita connection omega_ph^{12} = -cos theta (an SO(2)
  frame rotation). It supplies **NO symmetric rank-2 generator.**
- **2b. The native U(1)** (em_forcing, the photon): z -> e^{i alpha(x)} z,
  generator = the IDENTITY 1_3. It acts on the OVERALL phase ONLY; it does
  NOT mix the components z_m, so it supplies **NO su(3) direction.**
- **2c. Verdict:** the metric supplies a connection valued in **U(1) (+)
  SO(3) (+) SO(3,1)** generators. The 5 rank-2 Q_ab — exactly the generators
  that distinguish SU(3) from U(1)xSO(3) — have **NO native gauge field.**

---

## 3. TASK 3 — is z GENUINELY complex, or does it collapse to the real n?

A connection makes a relative phase of z physical iff there is a metric-given
1-form A_m^A coupling to a generator T_A that is NOT the identity (U(1)) and
NOT a pure SO(3) rotation (which acts on the REAL n). The rank-2 Q_ab are the
only candidates. Native-term audit (`su3_field_test.py`):

- **(i) Spin connection** — so(3,1)/antisymmetric => L_a only. No Q_ab.
- **(ii) U(1)/Maxwell A_m** — identity => overall phase only. No Q_ab.
- **(iii) The native kinetic term** L = -(xi/2) g^{mn} d_m z^dag d_n z is
  GLOBALLY SU(3)-invariant (z^dag z and dz^dag.dz are SU(3)-scalars) — but a
  GLOBAL symmetry is the selection-rule algebra, NOT a gauged connection (P8).
  Gauging requires a metric-given Omega_m^{(Q)}, which does not exist. No Q_ab.
- **(iv) The native L4/Skyrme term** = -kappa|F(A)|^2_g is the squared
  COMPOSITE U(1) Berry curvature (hopf_spinor Task 2): metric-contracted,
  P/T-EVEN, ABELIAN. It is U(1)-type, not a non-abelian SU(3) connection.
  No Q_ab.

**Consequence for the phases of z.** Under the only native connections — the
U(1) overall phase (pure gauge, removable) and the SO(3) frame rotation
(which acts on z exactly as it rotates the real n, since z is the spherical
image of n) — the relative phases of z carry NO physical content beyond the
real direction n. Demonstrated concretely (exact sympy):

- z^dag z = |n|^2 (a function of n);
- the n <-> z map is invertible (z's full content IS the real n);
- <z|L_a|z> = (n x n)_a = **0** — the spherical image of a real n carries
  ZERO angular momentum; it sits in the L=0 expectation locus, with no
  internal SU(3) excitation. A sharp restatement of the collapse.

> **TASK 3 RESULT: z is NOT genuinely complex. It COLLAPSES to the real n.**
> Every native (U(1)xSO(3))-invariant of z is a function of the real n
> alone (+ the removable U(1) phase). The 5 rank-2 directions that would
> make z's internal phases physically distinct from n have NO native
> connection, so they are never acted on. The metric's only invariant
> angular content is the real direction n (S^2) plus the abelian photon
> phase.

---

## 4. TASK 4 — THE WZW CONSEQUENCE

A native INTEGER WZW term requires the SU(3) GROUP-MANIFOLD target (maps
U(x) into SU(3), pi_5(SU(3))=Z, level = N_c integer) — i.e. all 8
generators physically realized, the SU(3) target genuinely present.

The metric supplies **U(1) x SO(3) x SO(3,1)**, NOT the rank-2 Q_ab, and z
COLLAPSES to the real n. The angular target is therefore **S^2** (= the real
n; S^2 = SU(3)/U(2), the coset keeping only the 2 real DOF), NOT the SU(3)
group manifold:
- **pi_5(S^2) = Z_2** (NOT Z) — a FREE Z_2, not an integer-graded WZW level.
- pi_3(S^2) = Z (the Hopf class), but the Hopf term is metric-FREE & P/T-ODD,
  whereas L2+L4 are metric-contracted & P/T-EVEN (hopf_spinor #47c) — so no
  native Hopf term either.

> **TASK 4 VERDICT: a native INTEGER WZW (SU(3) target, pi_5=Z, level=N_c)
> is NOT supported.** The metric gives the S^2 (real-n) target, whose
> statistics input is the FREE Finkelstein-Rubinstein Z_2 (#47/#49) — a free
> sign, NOT a metric-forced integer. The integer-WZW route is NOT native;
> the fermion stays the free FR Z_2.

---

## 5. TASK 5 — THE ONE HONEST OPEN DOOR (reported, not chased)

**The QUANTUM sector.** Quantizing the angular collective coordinates makes
the mode amplitudes a GENUINE complex Hilbert-space triplet: hbar promotes
the relative phases of z to physical quantum-state phases, acted on by the
angular-momentum / spin-1 operator algebra (the su(3) KINEMATICS, the
DERIVED selection-rule algebra, now acting on a real C^3 state). Whether the
QUANTIZED theory carries an EMERGENT WZW/Hopf phase (an induced theta-term
from integrating out hbar fluctuations, or a Berry phase over the collective
manifold) is **GENUINELY OPEN** — it is precisely the live frontier #49
named (the whole quantum completion rests on this single crux). It is NOT
excluded, but it is **NOT classically native**: it would RIDE hbar, exactly
as #47b/c and #49 concluded. We do NOT assume it.

**The other named door — emergent SU(3) from U(1)(photon) + the angular
structure — is NOT supported classically.** The U(1) is the abelian
overall-phase; the angular SO(3) is the real-frame rotation; their product
is U(1)xSO(3), which does NOT close into SU(3). The rank-2 Q_ab commutators
[L_a, Q_bc] do generate more Q's at the ALGEBRA level (the operator su(3) is
closed) — but no native CONNECTION sources any Q to begin with, so there is
nothing to close into a gauged SU(3). Algebra closure is the selection rule
(already banked); it is not a metric-given non-abelian gauge field.

---

## 6. PREMISE LEDGER ROLLUP / honest scope

DERIVED (forced by the metric / our objects / general covariance):
- z's relation to n (the unitary spherical map; exact, invertible).
- The spin connection is so(3,1) (antisymmetric) => L_a only (P6, a theorem).
- The native U(1) is the overall-phase identity (em_forcing).
- The native kinetic + L4 terms supply NO rank-2 Q_ab connection.
- z's native invariants are all functions of the real n (z collapses).
- The angular target is S^2; pi_5(S^2)=Z_2 (free), not the SU(3) pi_5=Z.

CHOSEN (flagged):
- P9, the operational definition of "genuine SU(3) field" (independent
  complex triplet + all 8 generators acting). A different, weaker definition
  ("su(3) as the operator algebra") is ALREADY banked as DERIVED but is a
  SELECTION RULE, not a gauged field — and does not support a WZW.
- The minimal kinetic model (no extra hand-added non-abelian connection —
  which would be an IMPORT, forbidden by Principle 1).

NOT CLAIMED: no mass/ratio/wall-number. The quantum-sector door (Task 5) is
reported open, NOT chased or assumed.

---

## 7. VERDICT

**(1) Does the metric induce an SU(3) connection or only U(1)xSO(3)xSO(3,1)?**
**ONLY U(1) x SO(3) x SO(3,1).** The 5 rank-2 symmetric-traceless Q_ab
generators — exactly those distinguishing SU(3) from U(1)xSO(3) — have NO
native gauge field. The real symmetric metric's spin connection is
so(3,1) (antisymmetric => L_a only); the native U(1) is the overall phase;
the kinetic/L4 terms are globally SU(3)-invariant but not gauged. No native
term supplies a Q_ab-valued connection.

**(2) Is z genuinely complex or does it collapse to real n?**
**It COLLAPSES to the real n.** z is the spherical image of n; the n<->z map
is invertible; every native (U(1)xSO(3))-invariant of z is a function of n
alone (+ the removable U(1) phase); <z|L|z> = n x n = 0. The 4 extra real
DOF are unphysical (no connection acts on them).

**(3) Is a native integer WZW supported?**
**NO.** The angular target is S^2 (pi_5 = Z_2, a free sign), not the SU(3)
group manifold (pi_5 = Z, integer level). The metric does not supply the
SU(3) structure an integer WZW requires.

**(4) THE VERDICT + the one open door.**
**REAL-S^2 + U(1)-ONLY.** The UDT metric provides the REAL direction n (S^2)
+ the native U(1) phase (the photon, em_forcing) + SO(3,1) (gravity), and
NOT a genuine SU(3)-valued field. Consequently there is NO native integer
WZW; the soliton's statistics input remains the FREE Finkelstein-Rubinstein
Z_2 (#47/#49). The ONE honest open door is the QUANTUM sector: hbar makes the
angular mode amplitudes a genuine complex triplet acted on by the su(3)
operator algebra, and whether an EMERGENT WZW/Hopf phase arises there is
genuinely open (the live frontier #49) — NOT classically native, riding hbar,
and NOT assumed here.

This DIRECTLY answers, in the negative for the classical metric, the crux #49
isolated: the integer-WZW / N_c=3 / soliton-is-a-fermion route is not native
to the classical UDT metric. It does not refute the quantum-sector route — it
SHARPENS the frontier to exactly that route.

Tag: METRIC-LED ("what structure does the metric put on the complex l=1
field?"), not TEMPLATE-LED ("can the metric make an SU(3) gauge field?"). The
verdict stops at REAL-S^2+U(1)-ONLY and names the quantum door rather than
narrating "SU(3) is excluded forever."

---

## BLIND VERIFIER — PENDING. Attack here:

1. **The spin-connection theorem (P6, the load-bearing claim).** Re-derive
   independently that a REAL symmetric metric g_mn generates, via the
   vielbein, only an ANTISYMMETRIC (so(p,q)) spin connection — and that on
   the l=1 carrier this is the antisymmetric L_a, never the symmetric Q_ab.
   Attack: is there ANY native curvature/torsion/non-metricity object on the
   UDT background that could carry a symmetric internal index pair? (e.g. the
   extrinsic curvature of a slicing, a second fundamental form, the dpf
   anisotropy mode's Hessian — could any source a Q_ab connection natively?)
2. **The collapse (Task 3).** Independently confirm z's native invariants are
   all functions of n. Try to EXHIBIT a native invariant of z that is NOT a
   function of n (+ U(1) phase) — if one exists, z does NOT collapse and the
   verdict flips toward AMBIGUOUS/SU(3)-FORCED.
3. **The U(1) generator (P7).** Confirm the native EM/photon acts as the
   identity 1_3 (overall phase), not as a component-mixing generator. If the
   photon coupled non-trivially across z_m it could supply more than U(1).
4. **The WZW topology (Task 4).** Confirm the target is S^2 (not the SU(3)
   group manifold or S^3) GIVEN the collapse, and that pi_5(S^2)=Z_2 (free)
   vs pi_5(SU(3))=Z (integer). Check the Hopf (pi_3) exclusion against
   hopf_spinor #47c (metric-free/P-T-odd vs the metric-contracted/P-T-even
   L2+L4).
5. **The quantum door (Task 5).** Confirm it is correctly scoped as OPEN and
   hbar-riding, NOT smuggled as a native classical result, and NOT excluded.
   Attack the "U(1)+angular does not close into SU(3)" claim: is there a
   native composite (e.g. the photon curvature times the angular winding)
   that realizes a rank-2 generator after all?
6. **Targeting check.** Was the honest likely outcome (REAL-S^2+U(1)-ONLY)
   reached by DERIVING the missing generators, or steered? Confirm no SU(3)
   gauge field was imported and called native; confirm the verdict is
   calibrated (the open quantum door named, not buried).

---
## VERDICT NOTE (appended 2026-06-15; blind verifier PENDING)
REAL-S^2 + U(1)-ONLY. The classical UDT metric does NOT force/admit a genuine
SU(3)-valued l=1 field. The metric-induced connection is U(1) (photon, identity
gen) x SO(3) (antisymmetric L_a = the spin connection) x SO(3,1) (gravity); the
5 SYMMETRIC rank-2 Q_ab generators (exactly SU(3)\U(1)xSO(3)) have NO native
gauge field (the spin connection of a real symmetric metric is so(3,1)-valued
/ antisymmetric — a theorem). z in C^3 collapses to the real n (4 of 6 DOF
unphysical; <z|L_a|z> = (n x n) = 0). Target = S^2 = SU(3)/U(2), pi_5(S^2)=Z_2
(free sign) NOT pi_5(SU(3))=Z (integer N_c). => NO native integer WZW; the
fermion stays the free FR Z_2 (consistent #47/#49). THE ONE OPEN DOOR: the
QUANTUM sector — hbar promotes the angular amplitudes to a complex Hilbert-space
triplet on which the su(3) OPERATOR ALGEBRA acts; whether the WZW/fermion
emerges THERE is the genuinely open frontier (rides hbar, not classical).
Verifier target: the spin-connection-antisymmetry theorem; any native object
carrying a symmetric internal index pair.

---

## BLIND ADVERSARIAL VERIFIER PASS — 2026-06-15
VERIFIER su3_field / 2026-06-15 / a3f7c1e9d4b86205 (independent machinery, not a
re-run of su3_field_test.py).

VERDICT: **STANDS-WITH-CAVEAT.** The central claim — the classical metric induces
a connection valued only in U(1) x SO(3) x SO(3,1), with the 5 symmetric rank-2
Q_ab (= the coset distinguishing SU(3) from U(1)xSO(3)) getting NO native gauge
field, so z collapses to the real n and no native integer WZW exists — survives
every independent attack.

INDEPENDENT REPRODUCTION OF THE LOAD-BEARING THEOREM (rebuilt from metric-
compatibility om^T eta + eta om = 0, NOT from the committed script): the connection
is forced antisymmetric (a=d=0, c=-b). CRUCIALLY this uses ONLY eta-preservation,
NEVER the symmetry of g_mn — so the theorem is STRONGER and more general than the
doc states. Rebuilt the spin-1 generators a different way (real Cartesian SO(3) ->
3 antisym + 5 symmetric-traceless) and confirmed a symmetric-valued connection is
incompatible with the antisymmetric metric-compatible spin connection.

ADVERSARIAL BREAKS (all FAILED): (A) non-metricity Q_mab is symmetric but =0 for
Levi-Civita (would be a Principle-1 import); (B) dilation gradient dphi is purely
radial, an SO(3)-scalar, carries no a,b index pair; (C) extrinsic curvature K_ab
enters as a tensor source, not a connection 1-form (explicit S^2 frame connection
[[0,-cos th],[cos th,0]] is antisymmetric); (D) <z|Q_ab|z> is nonzero but exactly
the QUADRUPOLE of the real n (= -(n_z^2-1/3) for Q_zz) — a function of n, no
independent phase DOF (sharpens the collapse beyond the doc: <z|L|z>=0 AND
<z|Q|z>=quadrupole(n)); (E) composite U(1)_photon x winding stays in {1, L_a}
([1_3,L_a]=0); reaching Q_ab needs L_aL_b (a curvature, not a 1-form); (F) verdict
robust to U(1)-generator (Cartan) ambiguity. Homotopy checked: pi_3(S^2)=Z,
pi_5(S^2)=Z2, pi_5(SU(3))=Z — the integer WZW genuinely needs the SU(3)/S^3 target
the collapse denies.

ERRATUM (cosmetic, non-load-bearing): the doc writes the target as "S^2 =
SU(3)/U(2)"; that coset is CP^2 (4-dim), not S^2. The target IS genuinely S^2 (the
2 real DOF of n) — established by the collapse independently of the coset name —
so the verdict is unaffected. Use "S^2 = SU(2)/U(1) = SO(3)/SO(2)" in any future
record.

OPEN HINGES (correctly scoped OPEN by the doc): (1) the QUANTUM sector — hbar
promoting the amplitudes to a complex Hilbert triplet with an emergent WZW/Berry
phase (NOT excluded by this work); (2) a non-metric/torsionful UDT extension would
be a new mechanism (Principle-1 import), legitimately outside the metric's native
scope. No data/wall-numbers; no targeting (the absence of the Q_ab connection is
DERIVED, not steered).
