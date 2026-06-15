# Crux 1 of the Coin-Flip — Does the Soliton's Configuration Admit a Boson/Fermion Z2 At All? (STATISTICS TOPOLOGY) — Results

Date: 2026-06-15. Driver: Claude (Opus 4.8, 1M context). NEW file
(append-never-edit, Self-Hardening discipline). Mode: **OBSERVE** (gated,
the FIRST sub-question of the quantum-completion frontier — the coin-flip;
authorized by the queue HANDOFF item 1). **DATA-BLIND**: no lepton/hadron wall
numbers, no Koide, no sqrt(2), no masses loaded, computed, or compared. This
push is STATISTICS ONLY (does the coin have two sides?) — it does NOT ask
whether quantization selects a side (that is Crux 2, which this hands off).

THE QUESTION: classically the soliton's statistics is said to be a FREE
Finkelstein-Rubinstein (FR) Z2 (boson vs fermion = which 1-D rep of pi_1 of the
configuration space). LOGICALLY PRIOR to "does quantization select a side?" is:
**does our particular soliton even ADMIT a two-sided coin — is BOSON-vs-FERMION
an available distinction for THIS field, with target S^2 (not S^3/SU(2))?**
We characterize OUR field's actual topology and report what is there.

Scripts (commit-grade, this push):
- `crux1_statistics_topology.py` — numpy: explicit degree computations on the
  ACTUAL field (pi_2 area-form degree of the angular hedgehog = 1; pi_3 Hopf
  invariant of the radial hedgehog = 0 vs a genuine Hopf map control != 0),
  the homotopy-group arithmetic, and the N-mod-2 mechanism analysis.

Blind verifier: **PENDING** (verifier-before-record; attack-here block at end).

---

## 0. PREMISE LEDGER (every fixed value tagged chose vs derived)

| # | Premise | chose / derived | note |
|---|---------|-----------------|------|
| P1 | The classical matter field is the REAL unit 3-vector n, target S^2 (2 DOF) | DERIVED | h1_types / angular_lagrangian / su3_field #50 (the complex SU(3) field is NOT classically native; 4 of 6 DOF unphysical) |
| P2 | Lagrangian L = L2 + L4 (baby-Skyrme/Skyrme on the S^2 target); L4 = native winding-current norm; NO bulk potential | DERIVED | native_stabilizer (Skyrme term = \|omega_H1 current\|^2_g, exact) |
| P3 | The cell geometry is (radial interval) x S^2; the physical soliton is a 3D lump n: cell -> S^2 with n -> const (unwound) at the seal | DERIVED | native_stabilizer (charge-1 hedgehog Theta(core)=pi -> Theta(seal)=0); HANDOFF |
| P4 | We work in 3 SPACE dimensions (the cell is a 3-spatial-D domain), NOT 2+1 | DERIVED | the cell is radial x S^2 = 3 spatial dims; this is DECISIVE for which homotopy group governs statistics (see Part 2) |
| P5 | Spin loop = a 2pi spatial rotation of one soliton; statistics loop = a two-soliton exchange | DERIVED (standard definition) | Finkelstein-Rubinstein framework |
| P6 | The FR spin/statistics Z2 of a soliton with base S^3 and target T is carried by pi_4(T) | DERIVED (standard FR theory) | for skyrmion-type 3D solitons the rotation/exchange loop suspends to a map S^4 -> T; pi_4(S^2)=Z2 |
| P7 | N=3 is the carrier rank of omega_H1 (eps_abc singlet unique iff N=3); the soliton charge B=1 is the pi_2 degree | DERIVED | h1_types; this push confirms degree=1 explicitly |
| P8 | "The coin has two sides" = pi_1(Q) contains a Z2 whose two 1-D reps are boson(+1) and fermion(-1) | CHOSE (the operational criterion) | the standard FR criterion for quantizability as a fermion |

---

## 1. THE FIELD, EXACTLY (Task 1)

There are THREE homotopy facts about the actual field, and they live in THREE
DIFFERENT groups. Conflating them is the trap; we separate them explicitly.

### 1a. The static soliton CHARGE: pi_2(S^2) = Z, degree B = 1
The angular winding (the H1 area form) is the degree of the shell map
n: S^2(space angles) -> S^2(target). Explicit computation
(`crux1_statistics_topology.py`, 400^2 grid):
**degree = 0.9999 ~ 1** — an INTEGER in pi_2(S^2)=Z. This is the soliton's
topological CHARGE (B=1), the N=3/q=1/3 area-form carrier. **It is an integer,
not a Z2 — it is not the coin.** (DERIVED, confirmed numerically.)

### 1b. The 3D texture (the physical lump): map S^3 -> S^2, pi_3(S^2) = Z (Hopf)
The physical soliton is n: R^3 -> S^2 with n -> const at the seal. Constant
boundary value one-point-compactifies R^3 to S^3, so the static field-as-a-3D-
object is a map **S^3 -> S^2**, classified by pi_3(S^2) = Z, the **Hopf
invariant** (the linking/braiding number). Explicit computation
(`crux1_statistics_topology.py`, FFT Coulomb-gauge Hopf integral):
- radial HEDGEHOG n = xhat sin(Theta(r)): **Hopf = -0.00** (zero);
- a genuine Hopf map (control): **Hopf != 0** (nonzero, ~0.7 on the coarse grid).

So our settled radial hedgehog is **NOT a Hopf texture** (H=0). Its charge is the
pi_2 degree, realized as the boundary winding, not as an internal pi_3 linking.
The 3D Hopf channel EXISTS for an S^2 field but is UNUSED by the hedgehog.
(DERIVED, confirmed numerically.)

### 1c. WHICH group classifies "the static soliton"?
- The static energy/charge classification is **pi_2(S^2) = Z** (the degree B).
  This is "the static soliton" in the sense of which topological sector it sits
  in. It is an integer.
- For 2+1 D (base S^2) the spin-statistics is the Hopf pi_3(S^2)=Z — giving
  ANYONS, statistics any phase (the baby-Skyrme literature). **This is NOT our
  case**: our cell is 3 spatial dimensions (P4).
- For 3 space dimensions (base S^3, P4) the spin-statistics Z2 is the FR class
  in **pi_4(S^2) = Z2** (Part 2). THIS is the coin.

> **FIELD IDENTIFICATION [DERIVED + numerically confirmed]: the static soliton
> is a degree-1 (pi_2(S^2)=Z) hedgehog lump n: cell(3D)->S^2, with Hopf charge
> ZERO (a degree texture, not a Hopf texture). Its CHARGE lives in pi_2=Z (an
> integer); its 3D-spatial STATISTICS class lives in pi_4(S^2)=Z2 (the coin).
> These are different groups; do not conflate the integer charge with the Z2
> coin.**

The dimensionality (P4) is the crux of the crux and was got right from OUR
field: the cell is genuinely 3 spatial dimensions, so the statistics group is
pi_4(S^2)=Z2, NOT the 2+1-D anyonic pi_3, and NOT the S^3/SU(2) Skyrme case
(which would use pi_4(S^3)=Z2 via a different target). The answer happens to be
a Z2 for S^2 in 3D too — but for a different homotopy-theoretic reason than the
SU(2) Skyrmion, and we state the reason, not assume the Skyrme case.

---

## 2. THE CONFIGURATION SPACE Q AND ITS pi_1 — IS THERE A COIN? (Task 2)

For a soliton field of base S^3 (= compactified 3D space) and target T, the
configuration space is Q = Maps(S^3, T), and the spin/statistics structure is
read from **pi_1(Q)** acting on the degree-B component:

- The **SPIN loop** = a 2pi spatial rotation of one soliton: a based loop in Q.
  By the standard loop-space adjunction, a loop of maps S^3 -> T is a map
  S^1 x S^3 -> T (rel basepoint a map of the smash S^1 ^ S^3 = S^4 -> T), i.e.
  an element of **pi_4(T)**. For T = S^2: **pi_4(S^2) = Z2**.
- The **STATISTICS loop** = a two-soliton exchange: a half-rotation-glued loop;
  by the Finkelstein-Rubinstein theorem the exchange loop is HOMOTOPIC to the
  2pi self-rotation loop in Q (the spin-statistics CONNECTION at the level of
  configuration-space topology). So it lands in the SAME **pi_4(S^2) = Z2**.

> **pi_1 FINDING [DERIVED, standard FR theory]: pi_1(Q) for the degree-1
> S^2-soliton in 3 space dimensions contains a Z2 generated by the
> 2pi-rotation = exchange loop, valued in pi_4(S^2) = Z2. THE COIN HAS TWO
> SIDES: the +1 rep (boson) and the -1 rep (fermion) are BOTH available 1-D
> reps of this Z2. The boson/fermion distinction is a genuine, well-posed
> question for our field — Crux 1 is answered YES at the level of existence.**

Source of the Z2, named precisely: it is the **FR statistics Z2 = pi_4(S^2)**,
arising because the 2pi-rotation/exchange loop in Q = Maps(S^3, S^2) suspends to
S^4 -> S^2 and pi_4(S^2) = Z2 (the generator = the suspension of the Hopf map).
It is NOT the charge (pi_2=Z), NOT the 3D Hopf texture (pi_3=Z), and NOT (in our
3D case) the 2+1-D anyonic statistics.

---

## 3. IS IT THE SAME Z2 IN THREE PLACES? (Task 3)

The handoff names three Z2's. We relate them honestly.

| label | the Z2 | where it lives | what loop / what it labels |
|-------|--------|----------------|----------------------------|
| (a) FR statistics | pi_4(S^2) = Z2 | configuration space Q = Maps(S^3,S^2) | the 2pi-rotation = exchange loop; boson(+1)/fermion(-1) |
| (b) #50's WZW-era sign | pi_5(S^2) = Z2 | maps from a 5-manifold (the WZW domain) into the S^2 target | the would-be 4D WZW/theta-term coefficient: a free SIGN, not an integer level (contrast pi_5(SU(3))=Z) |
| (c) #47b spin-structure | H^1(M;Z2) = 0 or Z2 | the spacetime manifold M (the doubled cell), NOT the field target | periodic(+1)/antiperiodic(-1) sections of the spin bundle; the Pin- T^2=-1 lift |

**Are these the same Z2? — NO, they are THREE DIFFERENT Z2's, but they are
LINKED by the spin-statistics theorem.** Honest relation:

- (a) and (b) are both Z2's of the **field target S^2** and are intimately
  related: pi_5(S^2)=Z2 is the home of the 4D Wess-Zumino / theta-term that, IF
  present in the action, would FIX the FR sign (a). They are not literally the
  same group (pi_4 vs pi_5) but they are the two faces of ONE physical object —
  "is there a topological term on the S^2 target that makes the soliton a
  fermion?" (a) is the statistics class of the loop; (b) is the coefficient slot
  of the term that could fix it. #50's finding "pi_5(S^2)=Z2 free, not
  pi_5(SU(3))=Z integer" is exactly the statement that the slot (b) carries only
  a FREE SIGN, hence cannot lock (a) to fermion — they are the same QUESTION
  viewed as class vs coefficient.
- (c) is a DIFFERENT Z2 entirely: it is a Z2 of the SPACETIME manifold (the spin
  structure on M), not of the field target. It governs whether a fundamental
  Dirac field would be periodic or antiperiodic — a property of the background,
  not of the soliton's configuration space. #47b found it is 0 for interval time
  (the canon default) and Z2 only if time closes. It is the "is there a place to
  PUT a fundamental fermion?" Z2, distinct from the soliton's own "is the lump a
  fermion?" Z2 (a).

> **THREE-Z2 VERDICT [DERIVED]: the coin-flip is essentially ONE question with
> two faces (a)<->(b) — the FR statistics class (a, pi_4) and the WZW/theta
> coefficient that could fix it (b, pi_5), both on the S^2 target — PLUS a
> SEPARATE, logically independent background question (c, the spin structure on
> M). The soliton's coin is (a)/(b). The spin-structure (c) is a different coin
> about the BACKGROUND, not the soliton. So Crux 1's coin is the (a)/(b) pair;
> (c) is not it (and #47b already showed (c) is unforced/absent by default).**

This SHARPENS the frontier: the soliton-statistics question is NOT three open
questions, it is ONE (does anything fix the pi_4 FR sign?), and the spin-
structure route (c) is correctly set aside as a different object.

---

## 4. CAN N (=3) ENTER AS N mod 2? (Task 4)

In the real SU(2)/SU(3) Skyrme model the soliton is a fermion iff the WZW level
(= N_c) is ODD: the FR phase = exp(i*pi*N_c*B), so the sign = (-1)^(N_c*B). With
N_c=3 (odd) and B=1 this is -1 = fermion. The mechanism is an INTEGER-graded 5D
WZW term, coefficient N_c, evaluated mod 2 on the loop. **Does our field have a
native analog — would the Z2 be fixed by N=3 as N mod 2 = 1 (fermionic)?**

DERIVED mechanism shape (NOT asserted): the only way an integer N can fix the FR
Z2 is through a topological term whose coefficient is N and that reduces the loop
class mod 2:
    FR phase = exp(i*pi * c * [loop class]),  c in Z, sign = (-1)^c.
In the SU(N>=3) case c = N_c*B comes from the 5D WZW term and the integer-graded
group **pi_5(SU(3)) = Z** carries N_c as a genuine integer level.

For OUR S^2 field there is **NO integer-graded channel**:
- The available 5D class is **pi_5(S^2) = Z2** (#50), which is ITSELF only a Z2 —
  it can carry its OWN free sign, but it CANNOT carry an integer N as a level
  (there is no Z to put N into). #50 established exactly this: the metric gives
  the S^2 target (pi_5=Z2), not the SU(3) target (pi_5=Z); the integer WZW is
  not native.
- Our N=3 is an integer in a DIFFERENT group — **pi_2(S^2)=Z**, the area-form
  DEGREE/charge count. **Does the pi_2 degree feed the pi_4 FR sign mod 2?**
  NO: the FR class is built from the 2pi-rotation/exchange loop suspending to
  S^4->S^2 (pi_4), and this suspension does NOT see the spatial degree B as a
  parity — a degree-B S^2 soliton has the SAME free Z2 FR class for every B
  (the FR sign of a multi-soliton sector is the SUM of pairwise FR signs, but
  each is the same free generator; B does not enter mod 2 as a coefficient).

> **N-MOD-2 VERDICT [DERIVED negative]: N=3 CANNOT enter the Z2 as N mod 2 in
> the classical theory. The integer-graded channel that would carry N as a WZW
> level (pi_5(SU(3))=Z) is not native (#50); the only native 5D slot
> (pi_5(S^2)=Z2) holds a free sign, not an integer; and our N=3 lives in the
> pi_2 charge group, which does not feed the pi_4 FR sign as a parity. So the
> classical theory has a genuine Z2 coin (Part 2) but NOTHING — not even N=3 —
> classically fixes which side it lands on. The coin is two-sided AND free.**

This is the precise, sharpened restatement of #47/#49/#50 at the level of the
mechanism: the reason the FR Z2 is free is not just "no term was found" but that
the integer that COULD fix it (N=3) has no homotopy channel into pi_4 in the
S^2-target theory. To fix it, N would need to enter through pi_5(SU(3))=Z, which
requires the genuine SU(3) target that #50 showed is not classically native.

---

## 5. TRUNCATION ROBUSTNESS (Task 5)

Every result above is **PURELY TOPOLOGICAL** — it depends only on the field
target (S^2), the spatial dimension (3, P4), and the homotopy groups
pi_2/pi_3/pi_4/pi_5(S^2). It does NOT depend on:
- the rigid-rotor / slow-collective-coordinate truncation (that truncation is a
  DYNAMICAL approximation used in monodromy_depth #49 for the spin tower; the
  EXISTENCE of the FR Z2 coin is a property of pi_1(Q), independent of any
  collective-coordinate reduction);
- the radial profile Theta(r), the cell depth D, the kappa/xi ratio, or any
  background phi (these set the soliton's SIZE/energy, not its homotopy class);
- any linearization (principle 2): no approximation enters a homotopy group.

The ONE place a truncation entered the WIDER program (the rigid-rotor in #49)
gives the SPIN tower E_n = E0 + hbar^2(n+nu)^2/(2 Lambda_3) — that IS truncation-
and hbar-dependent, but it is a Crux-2 (selection/quantization) object, not the
Crux-1 existence-of-the-coin object reported here.

> **TRUNCATION VERDICT [DERIVED]: Crux 1's findings are purely topological,
> hence ROBUST — no approximation, linearization, or collective-coordinate
> truncation enters. (The collective-coordinate truncation is relevant only to
> Crux 2's quantization, not to whether the coin exists.)**

---

## 6. HONEST VERDICT — CRUX 1: **THE COIN HAS TWO SIDES (existence YES), AND IT IS FREE**

1. **The field**: the static soliton is a degree-1 (pi_2(S^2)=Z) hedgehog lump
   n: cell(3D)->S^2 with Hopf charge ZERO (a degree texture, not a Hopf
   texture; both confirmed numerically). Charge in pi_2=Z (integer); 3D-spatial
   statistics class in pi_4(S^2)=Z2.
2. **The coin exists**: pi_1 of the configuration space Q=Maps(S^3,S^2),
   degree-1 sector, contains a **Z2 = pi_4(S^2)** generated by the
   2pi-rotation = exchange loop. Boson(+1) and fermion(-1) are BOTH available
   1-D reps. **BOSON-vs-FERMION is a well-posed distinction for our field —
   Crux 1 = YES, the coin has two sides.** (Source: the FR statistics Z2 =
   pi_4(S^2), via the loop-space suspension S^4->S^2; NOT the charge pi_2, NOT
   the 2+1-D anyonic pi_3, NOT the SU(2) Skyrme case.)
3. **Three Z2's**: the soliton's coin is essentially ONE question with two
   faces — the FR class (a, pi_4(S^2)) and the WZW/theta coefficient that could
   fix it (b, pi_5(S^2), a free sign per #50). The spin-structure Z2 (c,
   H^1(M;Z2), #47b) is a DIFFERENT, background object, not the soliton's coin.
4. **N mod 2**: N=3 CANNOT classically fix the side. The integer-graded channel
   (pi_5(SU(3))=Z, level N_c) is not native (#50); the native 5D slot
   (pi_5(S^2)=Z2) carries only a free sign; and N=3's home (pi_2=Z degree) has
   no parity map into pi_4. **The coin is two-sided AND free — nothing
   classical lands it.**
5. **Robust**: all of the above is purely topological; no truncation or
   linearization enters.

This is the calibrated answer: **the coin DOES have two sides** (so asking
"boson or fermion?" is legitimate, not a category error for our field), **and
classically it is FREE** (consistent with #47/#49/#50 — the classical metric
admits but does not force the fermion). Crux 1 establishes that Crux 2 is a
WELL-POSED question, and pinpoints exactly what Crux 2 must do.

### THE SHARPENED CRUX 2 (handoff)

Crux 1 shows the only thing that could land the free pi_4(S^2)=Z2 coin on
"fermion" is a **WZW/Berry/theta phase in the QUANTIZED theory whose coefficient
is fixed by N=3** — but it must enter through a channel that the CLASSICAL S^2
target lacks (pi_5(SU(3))=Z is not classically native). So **Crux 2 must ask,
precisely**:

> *When the angular collective coordinates (the l=1 amplitudes) are QUANTIZED —
> promoting the real n to a genuine complex su(3)-triplet Hilbert space (su(3)
> as the OPERATOR ALGEBRA, #50's open door) — does an EMERGENT/INDUCED
> topological phase (a Berry phase over the collective manifold, or an anomaly-
> induced theta-term) appear whose value on the 2pi-rotation = exchange loop is
> exp(i*pi*N) with N=3, thereby SELECTING the fermionic (-1) side of the
> pi_4(S^2)=Z2 coin?*

Concretely Crux 2 should compute the **Berry phase of the rigid-rotor /
collective-coordinate quantization around the 2pi-rotation loop** (the loop
Crux 1 identified as the coin's generator) and test whether it equals pi*N
mod 2pi. If YES (with N=3 -> phase pi -> -1): postulate A is DERIVED (the
electron is forced, QCD-baryon-style). If the phase is 0 / N-independent / free:
postulate A is IRREDUCIBLE (UDT postulates the fermion like the SM). This is a
single yes/no, rides hbar (a solid anchor), and is now PRECISELY posed because
Crux 1 fixed (i) the exact loop (2pi-rotation in Q, = exchange), (ii) the exact
group it must land in (pi_4(S^2)=Z2), and (iii) the exact channel N must use
(an induced phase, since the classical integer-WZW channel is absent).

---

## PREMISE LEDGER ROLLUP (chose vs derived)

DERIVED (topology / our objects / numerically confirmed):
- degree-1 in pi_2(S^2)=Z (area-form charge; numeric 0.9999) [Part 1a].
- Hopf invariant = 0 for the radial hedgehog (not a Hopf texture; numeric -0.00
  vs nonzero control) [Part 1b].
- the cell is 3 spatial dimensions => statistics group is pi_4(S^2)=Z2 [P4, Part 2].
- pi_1(Q) contains the FR Z2 = pi_4(S^2); the 2pi-rotation=exchange loop is its
  generator (spin-statistics connection) [Part 2].
- the three Z2's are pi_4(S^2)/pi_5(S^2) (one question, two faces) + the SEPARATE
  H^1(M;Z2) spin structure [Part 3].
- N=3 has no native parity channel into pi_4 (pi_5(SU(3))=Z absent per #50;
  pi_2 degree does not feed pi_4) [Part 4].
- all results truncation/linearization-independent (purely topological) [Part 5].

CHOSE (provisional, tagged; none a smuggled mechanism):
- P8, the operational FR criterion ("coin = a Z2 in pi_1(Q) with boson/fermion
  reps") — the standard quantizability criterion.
- The hedgehog profile/control fields in the numeric Hopf check (scaffolding;
  the verdict rides only on H=0 for the hedgehog vs H!=0 for a true Hopf map).

NOT CLAIMED: no mass/ratio/wall number; the QUANTUM selection (Crux 2) is named
and handed off, NOT computed or assumed here.

---

## BLIND VERIFIER — PENDING. ATTACK HERE:

1. **The statistics group (P6/Part 2, load-bearing).** Re-derive independently
   that for a soliton of base S^3 (3D space, P4) and target S^2 the FR
   spin/statistics class lives in pi_4(S^2)=Z2 (NOT the 2+1-D anyonic pi_3, NOT
   pi_4(S^3)). Confirm the 2pi-rotation loop and the exchange loop are homotopic
   in Q (spin-statistics connection) and both suspend to S^4->S^2. Attack the
   dimensionality: is the cell genuinely 3 spatial dimensions (radial x S^2), or
   could a reading make it 2+1 (which would give anyons, not a Z2)?
2. **The degree/Hopf computations (Part 1).** Re-compute the pi_2 degree and the
   pi_3 Hopf invariant of the radial hedgehog independently; confirm degree=1 and
   Hopf=0 (the hedgehog is a degree texture, not a Hopf texture). Confirm a
   genuine Hopf map gives Hopf!=0 (the control is correct, modulo grid coarseness).
3. **The three-Z2 relation (Part 3).** Challenge "(a) pi_4 and (b) pi_5 are two
   faces of one question." Are they genuinely linked (class vs coefficient), or
   conflated? Confirm (c) H^1(M;Z2) is a DIFFERENT (background spin-structure)
   Z2, not the soliton's coin. Cross-check against #47b/#47c/#50.
4. **N mod 2 (Part 4, the sharp claim).** Attack "N=3 has no native parity
   channel into pi_4." Try to EXHIBIT a channel by which the area-form degree
   N=3 (pi_2) or any native term feeds the FR pi_4 sign mod 2 (should fail
   without the SU(3)/pi_5=Z target #50 denies). If one exists, the verdict flips
   toward "N fixes the coin classically."
5. **Truncation (Part 5).** Confirm the existence of the coin is purely
   topological and does NOT inherit the rigid-rotor truncation of #49 (which is a
   Crux-2 quantization object). Flag any place an approximation crept in.
6. **Targeting check.** The verdict is "coin exists (YES) AND is free." Confirm
   this was DERIVED from OUR field's topology, not steered toward a desired
   answer; in particular confirm it does not UNDER-claim (a real coin is present)
   nor OVER-claim (no classical selection was manufactured). Check no SU(2)/S^3
   Skyrme machinery was imported in place of the actual S^2 field.

---
## VERDICT NOTE (appended 2026-06-15; blind verifier PENDING)
CRUX 1 = YES, THE COIN HAS TWO SIDES, AND IT IS FREE. The settled field is a
degree-1 (pi_2(S^2)=Z) hedgehog lump n: cell(3D)->S^2, Hopf charge ZERO (degree
texture, not Hopf texture; both numerically confirmed). In 3 spatial dimensions
the FR spin/statistics class lives in pi_4(S^2)=Z2 — a genuine two-sided coin in
pi_1(configuration space), generated by the 2pi-rotation=exchange loop; boson(+1)
and fermion(-1) are both available. The "three Z2's" reduce to ONE soliton coin
with two faces (FR class pi_4(S^2) <-> WZW coefficient pi_5(S^2), a free sign per
#50) plus a SEPARATE background spin-structure Z2 (H^1(M;Z2), #47b — not the
soliton's coin). N=3 CANNOT classically land the coin: the integer-WZW channel
(pi_5(SU(3))=Z, level N_c) is not native (#50), the native 5D slot pi_5(S^2)=Z2
holds only a free sign, and N=3's home (pi_2 degree) has no parity map into pi_4.
Purely topological => truncation-robust. SHARPENED CRUX 2: compute the Berry/
induced topological phase of the QUANTIZED collective-coordinate 2pi-rotation
loop and test whether it = exp(i*pi*N), N=3, selecting the fermionic side of the
free pi_4(S^2)=Z2 coin. Crux 1 makes Crux 2 well-posed and fixes its exact loop,
target group, and the channel N must use (an induced phase, the classical one
being absent).
