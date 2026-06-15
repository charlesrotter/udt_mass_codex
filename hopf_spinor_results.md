# Is UDT's winding field n the SQUARE of a FORCED spinor? (Hopf route) — Results

Date: 2026-06-14. Driver: Claude (Opus 4.8, 1M context). NEW file
(append-never-edit, Self-Hardening discipline). Mode: **OBSERVE** (gated,
authorized by Charles). This is the **LAST of three spinor-origin routes**.
The two prior routes both found the time-reversal fold does NOT force the
spinor:
- LOCAL seal-value (fermion_forcing_results.md, #46): a nonstationary cell
  forces sigma-ODD matter, but the forced source's SEAL-VALUE is identically
  zero, so a single-valued sigma-ODD BOSON (Proca-type, T^2=+1) suffices —
  the fermion's two-valuedness is NOT forced locally.
- GLOBAL spin structure (global_spin_structure_results.md): a spin structure
  EXISTS (w_2=0), but sigma is an involution (sigma^2=id); the antiperiodic
  (T^2=-1) structure is NOT EVEN ADMITTED for interval time, and only a free,
  UNFORCED Z_2 option if time closes into a circle. q=1/3 is in H^2, the wrong
  slot for a spin structure.

THE QUESTION (this push): is UDT's winding unit-3-vector field n the SQUARE of
a FORCED spinor via the Hopf map n_a = psi-dagger sigma_a psi — such that the
spinor is the PRIMITIVE object (n derived from it, with its own Dirac dynamics
and a native sqrt(m)) — or is n primitive and psi merely a re-labelling
(circular, proves nothing)?

**No mass / ratio / data.** All statements are about the ALGEBRA and TOPOLOGY
of rewriting the settled native Lagrangian L = L2 + L4. No Dirac field is
imported and asserted forced.

Frame / banked inputs:
- Settled native angular Lagrangian L = L2 + L4 (native_stabilizer_results.md,
  CANON C-2026-06-14-1):
    L2 = -(xi/2) g^{mn} d_m n_a d_n n_a
    L4 = -(kappa/4) (d_m n x d_n n)^2  = -(kappa/4) |omega_H1 winding current|^2_g
  with unit 3-vector n_a (|n|=1, target S^2). Charge-1 hedgehog soliton,
  stabilized at size lambda* = sqrt(B/A) ~ sqrt(kappa/xi) (NATIVE Skyrme term).
- The Hopf map: n_a = psi-dagger sigma_a psi for a 2-component complex spinor
  psi, |psi|^2=1 (CP^1 / Bloch-sphere representation; S^3 -> S^2 Hopf bundle).

Scripts (commit-grade, this push):
- `hopf_spinor.py` — sympy CPU: explicit Hopf map, |n|=1 on |psi|=1, the
  L2->CP^1 identity, the L4/winding-density->Berry-curvature identity, and the
  reasoned topological-term / sqrt(m) / statistics analysis.
- `hopf_spinor_verify.py` — independent numerical (numpy FD) confirmation of
  the two pointwise identities over 20000 random points on |psi|=1 with random
  tangent velocities (max residual ~1e-9, the FD truncation floor).

Blind verifier: **PENDING** (verifier-before-record; attack-here block at end).

---

## 0. PREMISE LEDGER (every fixed value tagged chose vs derived)

| # | Premise | chose / derived | note |
|---|---------|-----------------|------|
| P1 | Settled native angular Lagrangian L = L2 + L4 | DERIVED | native_stabilizer_results.md, CANON C-2026-06-14-1 |
| P2 | n_a = psi-dagger sigma_a psi, |psi|^2=1 (the Hopf/CP^1 parametrization) | DERIVED-as-identity (any unit 3-vector admits it) / CHOSE to adopt it as the probe | the Hopf bundle S^3->S^2 is a standard fact; choosing to read n THROUGH it is the route under test |
| P3 | sigma_a = Pauli matrices; the U(1) gauge redundancy psi ~ e^{i alpha} psi | DERIVED | psi and e^{i alpha}psi give the SAME n: the fiber of the Hopf map |
| P4 | "the squared psi is a Dirac fermion (anticommuting, T^2=-1)" | **NOT ASSUMED — under test** | the load-bearing anti-circularity step |
| P5 | A Hopf/WZ statistics term would be ADDED to L2+L4 (not contained in them) | DERIVED (shown below) | L2, L4 are metric-contracted, P/T-even; A^dA is metric-free, T-odd |
| P6 | Finkelstein-Rubinstein/Wilczek-Zee soliton-fermion is a QUANTUM (hbar) statement | DERIVED (standard) | it is a path-integral Berry-phase / spin-statistics result |

---

## TASK 1 — L2 -> CP^1: BOSONIC re-encoding (DERIVED, verified)

**The Hopf map (sympy, exact).** With psi = (z0, z1), z0=a0+i b0, z1=a1+i b1:

    n_x = 2(a0 a1 + b0 b1)
    n_y = 2(a0 b1 - a1 b0)
    n_z = a0^2 + b0^2 - a1^2 - b1^2
    |psi|^2 = a0^2 + b0^2 + a1^2 + b1^2

and |n|^2 = (|psi|^2)^2, so **|psi|=1 => |n|=1** (the target S^2). [DERIVED]

**The L2->CP^1 identity (verified to machine/FD precision, hopf_spinor_verify.py,
20000 random points on |psi|=1 with random tangent velocities, max residual
1.4e-9 = the finite-difference floor):**

    (1/4) sum_a (d_m n_a)(d_m n_a)  ==  |d_m psi|^2  -  |psi-dagger d_m psi|^2
                                    ==  |D_m psi|^2 ,   D_m = d_m - i A_m ,
                                    A_m = -i psi-dagger d_m psi   (COMPOSITE U(1)).

Therefore, exactly:

    **L2 = -(xi/2) g^{mn} d_m n . d_n n  =  -2 xi g^{mn} (D_m psi)-dagger (D_n psi)
         =  -2 xi |D psi|^2_g     — the gauged CP^1 model.**

This is the standard O(3) sigma-model -> CP^1 identity, here confirmed natively
on UDT's own L2. (chose: nothing; derived identity. The xi and the factor-of-4
are normalization carried from L2.)

**STATISTICS OF psi (the decisive point):**
- psi entered as a COMMUTING complex doublet (z0, z1 ordinary c-numbers).
- L2 in psi is QUADRATIC, SECOND-ORDER (|D psi|^2, Klein-Gordon/CP^1 form),
  with NO gamma-matrix and NO first-order Dirac operator psibar(i gamma.D)psi.
- The gauge redundancy psi ~ e^{i alpha(x)} psi (both give the same n) means
  psi is a SECTION OF THE HOPF BUNDLE / a point of CP^1 = S^2 — a CONSTRAINED
  BOSONIC field with T^2 = +1.

> **VERDICT Task 1: the kinematic squaring gives a BOSONIC CP^1 spinor — a
> constrained complex SCALAR doublet (T^2=+1), NOT a genuine Dirac fermion.**
> This CONFIRMS the expectation in the prompt: the Hopf-squaring is a
> re-encoding, not a forced fermion.

---

## TASK 2 — L4 -> Berry curvature; NO Hopf/WZ term in L2+L4 (DERIVED)

**The winding density IS the composite Berry curvature (verified to FD
precision, hopf_spinor_verify.py, max residual 2.2e-9):**

    n . (d_s n x d_t n)  ==  2 F_st ,   F_st = d_s A_t - d_t A_s
                                              = -i(psi_s-dagger psi_t - psi_t-dagger psi_s).

So the skyrmion winding 2-form (== omega_H1 winding current, h1_types /
native_stabilizer) is exactly TWICE the curvature dA of the composite
connection A = -i psi-dagger d psi. [DERIVED]

Consequently, in CP^1 variables,

    **L4 = -(kappa/4) |winding current|^2_g  =  -kappa |F(A)|^2_g**

— a Maxwell-type term for the COMPOSITE connection A. It is **manifestly
BOSONIC and metric-dependent** (contracted with the UDT inverse metric, exactly
as in native_stabilizer Task 1). It is the energy/Skyrme term.

**IS THERE A HOPF / WESS-ZUMINO (statistics) TERM? — NO, not in L2+L4 (DERIVED):**
- The Hopf term is theta_H * INT A ^ dA: **metric-FREE** and **P/T-ODD**. Both
  L2 = -2 xi |D psi|^2_g and L4 = -kappa |F|^2_g are **metric-CONTRACTED** and
  **P- and T-EVEN**. Neither contains A ^ dA. A Hopf term is a SEPARATE term one
  would have to ADD by hand; **UDT's settled L = L2 + L4 does NOT generate one.**
- In 3+1 D the object that makes a skyrmion a fermion is not the (2+1 D) Hopf
  term but the Finkelstein-Rubinstein (FR) statistics phase tied to
  pi_4(S^2) = Z_2 — the Z_2 Wess-Zumino-Witten coefficient. That coefficient is
  a discrete Z_2 CHOICE (FR phase 0 => boson, pi => fermion); it is **NOT fixed
  by the energy functional L2 + L4**. The Skyrme/CP^1 energy is statistics-blind.

> **VERDICT Task 2: L4 maps to the squared composite Berry curvature |F(A)|^2_g
> — bosonic, metric-dependent, P/T-even. It is NOT a Hopf/WZ topological term,
> and L2+L4 do not contain or force one. The soliton's statistics (boson vs
> fermion) is an INDEPENDENT discrete Z_2 input (the FR/WZ coefficient), not
> determined by UDT's settled angular Lagrangian.**

---

## TASK 3 — THE ANTI-CIRCULARITY GATE (load-bearing)

Two cleanly separated claims:

- **(a) Re-encode n as a bosonic CP^1 spinor.** TRUE and CHEAP. n_a =
  psi-dagger sigma_a psi with |psi|=1 is a kinematic identity; L2->|D psi|^2,
  L4->|F(A)|^2 follow. But psi here is a CONSTRAINED BOSONIC scalar doublet
  (Task 1), psi ~ e^{i alpha}psi is pure gauge redundancy, and the map is
  invertible (n <-> psi-mod-phase). **This is circular: n is primitive and psi
  is a re-labelling of the SAME bosonic degrees of freedom. It proves nothing
  about fermions.** Rewriting is free.

- **(b) The geometry FORCES a fermion.** A forced fermion needs DYNAMICS or
  forced STATISTICS:
  - **A fundamental Dirac psi with its own action psibar(i gamma.D - m)psi and a
    native sqrt(m):** NOT present. L2+L4 are second-order bosonic energies; no
    first-order Dirac operator and no gamma-matrices appear (Task 1). The Hopf
    psi has NO independent action — its only dynamics ARE L2+L4, i.e. the
    bosonic CP^1 model. There is no native Dirac sector here.
  - **The soliton quantized as a fermion via a FORCED topological term:** the
    FR/WZ statistics coefficient is NOT forced by L2+L4 (Task 2); it is a free
    Z_2 input. UDT's energy functional is statistics-blind.

> **VERDICT Task 3: UDT gives (a) — a BOSONIC CP^1 RE-ENCODING (circular). It
> does NOT give (b): no fundamental Dirac action / sqrt(m) falls out, and the
> soliton-fermion (FR/WZ) statistics term is not forced by L2+L4. Rewriting n
> as psi proves nothing; the spinor is NOT forced by the Hopf squaring.**

---

## TASK 4 — hbar / QUANTIZATION HONESTY

Even IF one elected to make the soliton fermionic via the FR/WZ Z_2 term, that
is a **QUANTUM statistics statement**: the FR phase / skyrmion-as-fermion result
is a property of the PATH INTEGRAL (a Berry/Aharonov-type phase exp(i pi) =
exp(i S_WZ/hbar) picked up under the 2pi rotation / particle exchange of the
soliton configuration). It needs hbar and the quantum measure to even be
defined. UDT flags hbar as a not-yet-native add-on.

CLASSICAL vs QUANTUM forcing:
- **Classical:** L2 + L4 are a classical bosonic field theory. Classically the
  charge-1 soliton is a bosonic lump with a definite size. NOTHING classical
  forces half-integer spin or anticommuting statistics.
- **Quantum:** the only route to "the soliton IS a fermion" is the
  quantum FR/WZ mechanism, which RIDES hbar (the Berry phase / path-integral),
  AND requires the free Z_2 coefficient to be set to pi (not forced — Task 2).

> **VERDICT Task 4: any "soliton-is-fermion" reading RIDES quantization (hbar)
> AND an unforced Z_2 choice. It is native only to the extent UDT's quantum
> sector is — and UDT's quantum/hbar sector is NOT yet native. So even the
> favourable reading is doubly non-native: it needs (i) hbar and (ii) a free
> topological coefficient. This is a QUANTUM statement, not a classical
> forcing.**

---

## TASK 5 — sqrt(m) STATUS

L2, L4 are quadratic / quartic in d psi (bosonic energy densities). The soliton
MASS = INT (E2 + E4) d^3x is an ENERGY — LINEAR in the energy density, not a
square-root of one. psi is normalized |psi|=1: it is a pure PHASE/DIRECTION,
carrying NO sqrt(energy) amplitude weight. A Dirac-type sqrt(m) amplitude (the
Koide structure) would come from a FIRST-ORDER operator psibar(i gamma.D - m)psi
whose on-shell norm is sqrt(m)-weighted — and that operator is ABSENT here.

> **VERDICT Task 5: NO native sqrt(m) emerges from the Hopf route. The squared
> psi is amplitude-1 (a direction), not a sqrt(m)-weighted amplitude. This is
> CONSISTENT with #45 / n3_direction_distribution_results.md: sqrt(m) is the
> spinor INPUT, not an output of the bosonic winding sector.**

---

## OVERALL VERDICT — **RE-ENCODING-ONLY** (with the soliton-fermion route, if invoked, riding hbar)

The Hopf squaring n_a = psi-dagger sigma_a psi is a kinematic BOSONIC CP^1
re-encoding (Task 1): L2 -> -2 xi |D psi|^2, L4 -> -kappa |F(A)|^2, with psi a
constrained scalar doublet (T^2=+1, gauge redundancy psi ~ e^{i alpha}psi). It
is **circular** — n is primitive, psi re-labels the same bosonic DOF — and
**proves nothing about fermions**. UDT's settled L2+L4 contain **NO Hopf/WZ
topological term** and do **NOT force** the soliton's statistics (the FR/WZ
Z_2 coefficient is a free input, Task 2). There is **NO fundamental Dirac
action and NO native sqrt(m)** (Tasks 3, 5). The only conceivable fermion —
"the soliton quantized as a fermion" — RIDES hbar AND an unforced Z_2 choice
(Task 4), so it is doubly non-native given UDT's quantum sector is not yet
native.

**Classification: RE-ENCODING-ONLY (circular bosonic CP^1).** NOT FORCED
(no classical Dirac / native sqrt(m)); the SOLITON-IS-FERMION-via-quantization
route exists only as an UNFORCED, hbar-riding option, not a forcing.

This is the THIRD spinor-origin route to land negative. The local seal-value
(#46), the global spin structure, and now the Hopf-squaring all agree: **the
time-reversal fold / the angular winding sector does NOT FORCE a fermion.** The
spinor is, at most, FAVOURED/NATURAL/ADMITTED — never forced — by the settled
classical UDT structure; a genuine fermion needs either an hbar-quantum sector
(not yet native) or a new ingredient beyond L2+L4 and the t->-t fold.

REFRAME FLAG (method discipline): three spinor-FORCING routes have now
returned NOT-FORCED. Per the charter tripwire, a run of refusals indicts the
QUESTION ("does the t->-t fold / winding sector FORCE a fermion?") and triggers
a ZOOM-OUT, not a fourth drill. The honest reading: fermion statistics may be a
QUANTUM-SECTOR (hbar) property that the classical metric admits but does not
force — and the discreteness/Koide program should not wait on a forced-fermion
derivation from the classical angular Lagrangian.

---

## PREMISE LEDGER SUMMARY (chose vs derived)

DERIVED (fell out / verified):
- |psi|=1 => |n|=1 (Hopf map onto target S^2) [Task 1, sympy].
- L2 = -2 xi |D psi|^2 with composite A = -i psidag d psi [Task 1, identity
  verified to FD precision 1.4e-9].
- winding density n.(dn x dn) = 2 dA = 2 F(A) (Berry curvature) [Task 2,
  verified to FD precision 2.2e-9]; L4 = -kappa |F(A)|^2_g.
- psi is a CONSTRAINED BOSONIC doublet (T^2=+1, gauge psi ~ e^{i alpha}psi)
  [Task 1].
- L2, L4 are metric-contracted, P/T-EVEN => contain no metric-free, T-ODD
  A^dA Hopf term [Task 2].
- No first-order Dirac operator, no native sqrt(m) [Tasks 3, 5].

CHOSE (provisional, tagged; none a smuggled mechanism):
- Adopting the Hopf/CP^1 reading of n as the probe [P2] — a legitimate
  identity, the route under test.
- The minimal G = (matter); xi, kappa > 0 normalizations carried from L2/L4.
- Reading "soliton-is-fermion" via FR/WZ as the ONLY non-trivial fermion route
  in 3+1 D [Task 2/4] — standard, but the Z_2 coefficient is acknowledged free.

---

## BLIND VERIFIER — PENDING. ATTACK HERE:

1. **Task 1 identity.** Re-derive (1/4) sum_a (d n_a)^2 = |D psi|^2 (composite
   A) by an INDEPENDENT route (e.g. CP^1 projector P = psi psidag, n.sigma =
   2P - 1, and tr((dP)^2)); confirm psi is bosonic (no anticommuting structure
   smuggled). Confirm the gauge redundancy psi ~ e^{i alpha}psi leaves n and L2
   invariant.
2. **Task 2 / Hopf term.** Confirm L4 = -kappa |F(A)|^2_g and that NEITHER L2
   NOR L4 contains A ^ dA. Independently confirm that in 3+1 D the soliton
   statistics is an FR/WZ Z_2 choice NOT fixed by the energy functional — try
   to EXHIBIT a term in L2+L4 that fixes it (should fail), or show the FR phase
   is determined (should require an ADDED term). Check pi_4(S^2)=Z_2 is the
   right home for the statistics (vs the pi_3 Hopf invariant of 2+1 D).
3. **Anti-circularity (Task 3).** Attack from both sides: (i) try to EXHIBIT a
   native first-order Dirac action / sqrt(m) hiding in L2+L4 (should fail); (ii)
   try to FORCE the FR Z_2 = pi from some UDT structure (seal parity? q=1/3?
   the H^2 transgression?) — if any forces it, the verdict flips toward
   SOLITON-IS-FERMION. Be ruthless that re-encoding is free.
4. **hbar honesty (Task 4).** Confirm the FR/skyrmion-fermion mechanism is
   genuinely a QUANTUM (path-integral Berry-phase) statement that needs hbar,
   and cannot be obtained classically from L2+L4. Distinguish a classical
   forcing from a quantum one.
5. **sqrt(m) (Task 5).** Confirm no sqrt(m) amplitude appears; cross-check #45.
6. **Targeting check.** The verdict is RE-ENCODING-ONLY / NOT-FORCED. Was the
   question honestly answered, or did the doc steer toward a desired negative?
   Check it does not UNDER-claim a real forcing that is present.

---
## VERDICT NOTE (appended 2026-06-14; verifier PENDING; THIRD converging negative)
RE-ENCODING-ONLY / spinor NOT forced. n=psi-dag-sigma-psi gives a BOSONIC CP^1
field (T^2=+1, composite gauge redundancy; CP^1=L2 verified to FD ~1e-9), a
kinematic re-labelling — n is primitive. L4 = squared composite Berry curvature
(Maxwell-type, P/T-EVEN), NOT the (metric-free, T-ODD) Hopf term => statistics-
blind; the Finkelstein-Rubinstein Z_2 (pi_4(S^2)) is a FREE input, not fixed by
the energy. The soliton-as-fermion route rides hbar AND the unforced Z_2. No
native sqrt(m) (consistent #45). => with the LOCAL fold (#46) and the GLOBAL spin
structure, ALL THREE classical routes agree: the t->-t fold / classical winding
sector does NOT force a fermion. REFRAME (method): a run of 3 refusals indicts
the QUESTION ("does the classical metric force a fermion?") — the honest answer
is that fermion statistics is a QUANTUM-SECTOR (hbar) property the classical
metric ADMITS but does not FORCE (converges with UDT_REBUILD sec 6: the ruler
lives in the metric's own quantum sector).
