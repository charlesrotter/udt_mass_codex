# Depth-Monodromy of the Collective-Coordinate Soliton — Results

Date: 2026-06-15. Driver: Claude (Opus 4.8, 1M context). NEW file
(append-never-edit, Self-Hardening discipline). Mode: **GATED OBSERVE** (the
FIRST quantum-completion-frontier computation, authorized by Charles). Frame:
CANON C-2026-06-14-1; native_stabilizer_results.md (settled L2+L4 sized
soliton); n3_direction_distribution_results.md (the iso-rotation collective
coordinate + iso-inertia Lambda_ab(D)). **DATA-BLIND**: no lepton/hadron wall
numbers, no Koide, no sqrt(2), no 45-deg loaded, computed, or compared. #48
(no evenly-spaced ladder) is treated as a GUARD, not a target.

THE QUESTION (LLM#3 facet 1b, hbar-free FIRST): does the settled L2+L4 soliton,
reduced to its COLLECTIVE COORDINATES on the finite back-reacted cell, produce a
DEPTH-DEPENDENT angular MONODROMY whose single-valuedness QUANTIZES the
otherwise-continuous cell depth D into a discrete ladder D_n?

DISCIPLINE HELD: we DERIVE whether the monodromy EXISTS — we do NOT import the
LLM#3 mechanism and assume it. hbar-free classical single-valuedness is tested
FIRST; Bohr-Sommerfeld only as a flagged fallback.

Scripts (commit-grade, this push):
- `monodromy_depth_probe.py` — V100 torch float64 + scipy BVP: Task 1, the
  make-or-break test of every candidate angular phase for depth dependence,
  reusing the settled native_profile_bvp machinery + the n3 iso-inertia.
- `monodromy_collective_reduction.py` — sympy CPU: the exact collective-coordinate
  reduction, canonical momentum p_chi, the classical single-valuedness test
  (Task 3), and the flagged Bohr-Sommerfeld fallback (Task 4).

Blind verifier: **PENDING** (verifier-before-record; attack-here block at end).

---

## TASK 1 — THE MAKE-OR-BREAK: DOES A DEPTH-DEPENDENT ANGULAR MONODROMY EXIST?

### The collective / angular coordinates of the settled soliton (derived)

The settled native carrier (native_stabilizer_results.md) is the charge-1
easy-axis baby-Skyrme hedgehog of a **unit 3-vector** n (target S^2):

    n = ( sinTheta(r) sin th cos ph, sinTheta(r) sin th sin ph, cosTheta(r) ),
    Theta(r_core)=pi (charge 1)  ->  Theta(r_int=seal)=0 (unwound exterior).

Its angular structure is EXACTLY two objects, both derived:
  (a) the **topological winding** (degree/charge B) — fixed by the BCs;
  (b) the **rigid internal SO(3) orientation** R (the iso-rotation collective
      coordinate), generators v_a = e_a x n; the cyclic phase chi = iso-rotation
      angle about the easy axis (target-3) (n3_direction_distribution_results.md).

CRITICAL STRUCTURAL FACT: an S^2 / baby-Skyrme hedgehog has **ONE radial profile
Theta(r)** plus the **rigid** orientation R. There is NO second internal profile
psi(r) (that would require an S^3 / SU(2) Skyrme target, which is NOT the settled
n-field model). So every candidate "angular phase" is one of: the winding, the
rigid orientation, or a geometric (Berry) phase along the radial path.

### Every candidate phase, tested for depth dependence (DERIVED, not assumed)

Depth family (chose, the settled cell B1): phi = -p ln(r_int/r); the depth
D = phi at the core = -p ln(r_int/r_core). p=0 flat; p>0 deep. BVP profile solved
on the V100 (residual ~1e-8) for p = 0, 0.25, 0.5, 1.0, 1.5, 2.0:

    p     D=phi_core   degree B   dTheta   Berry(merid)   Lambda_3(D)   Lambda_perp(D)
   0.00     0.0000     1.00000   3.1416      0.0000          8.806        3662.4
   0.25    -1.3712     1.00000   3.1416      0.0000         15.515        2916.1
   0.50    -2.7424     1.00000   3.1416      0.0000         29.024        2414.0
   1.00    -5.4848     1.00000   3.1416      0.0000         65.427        1766.8
   1.50    -8.2272     1.00000   3.1416      0.0000        102.797        1363.0
   2.00   -10.9696     1.00000   3.1416      0.0000        134.111        1087.4

Read-out (the load-bearing result):

- **(P1) Topological winding / degree B = 1 for ALL depths** (spread 0.0e0). The
  winding is RIGID, depth-INDEPENDENT — it is degree-1 by topology, fixed by the
  charge-1 BCs Theta(core)=pi -> Theta(seal)=0. Nothing accumulates with D.

- **(P2) Accumulated profile angle dTheta = Theta(core)-Theta(seal) = pi for ALL
  depths** (spread 0.0e0). Fixed by the BCs; depth-INDEPENDENT.

- **(P4) The geometric (Berry) phase the internal vector traverses along the
  radial path core->seal = 0 EXACTLY.** The hedgehog's internal point n(r) traces
  a MERIDIAN on the target S^2 (from south pole Theta=pi to north pole Theta=0) at
  fixed internal longitude; a meridian sweeps ZERO solid angle and has
  d(longitude)=0, so the accumulated geometric phase = INT(1-cosTheta)d(longitude)
  = 0 identically, for every depth. There is **NO radially-accumulated angular
  phase that depends on D**.

- **(P3) The iso-inertia Lambda_3(D) IS depth-dependent** (8.81 -> 134.11 as the
  cell deepens p: 0 -> 2; monotone, smooth) — but it is a **STIFFNESS (an inertia /
  moment), NOT an accumulated phase**. The conjugate phase chi is a RIGID GLOBAL
  collective coordinate: it is ONE number for the whole soliton, with ZERO radial
  accumulation across the cell. chi is cyclic in TIME (period 2pi), not in radius.

### VERDICT (Task 1, the make-or-break): **NO depth-dependent angular monodromy
exists.** The settled charge-1 hedgehog carries only (i) a rigid degree-1 winding
(depth-independent) and (ii) a rigid global iso-rotation phase chi (zero radial
accumulation). The single depth-dependent angular quantity, Lambda_3(D), is a
stiffness, not a phase whose single-valuedness could bite. There is no Theta(D)
that the field accumulates across the cell and whose 2 pi n roots could quantize
D. The chi collective coordinate is RIGID, with a fixed (degree-1) winding and
NO depth-dependent accumulated phase. **This is the load-bearing kill.**

---

## TASK 2 — THE COLLECTIVE-COORDINATE REDUCTION + CANONICAL STRUCTURE (sympy, exact)

Even though Task 1 already kills the depth-monodromy, we carry the reduction
through to make the canonical structure explicit and to test single-valuedness
honestly (Tasks 3-4). Promoting the rigid orientation to a slow collective
coordinate chi(t) (iso-rotation about the easy axis), the settled L2+L4 t-t
reduction (n3_direction_distribution) gives the effective Lagrangian

    L_eff(chi, chidot; D) = (1/2) Lambda_3(D) chidot^2 - E0(D).

Canonical momentum (sympy):  **p_chi = dL_eff/d(chidot) = Lambda_3(D) chidot.**
L_eff has NO explicit chi  =>  chi is CYCLIC  =>  **p_chi = const = J (conserved).**
EOM:  chidot = J/Lambda_3(D) = omega = const;  chi(t) = omega t + chi_0 (uniform
rotation). **The rotation rate omega is a FREE classical initial datum** — for any
depth D and any J >= 0 there is a perfectly good uniform iso-rotation.

The "monodromy function" the LLM#3 mechanism needs, Theta(D) = accumulated phase
across the cell, does NOT exist here: chi accumulates in TIME (omega t), not in
radius, and its per-cell radial accumulation is identically zero (Task 1, P3/P4).
J_chi = oint p_chi dchi = 2 pi Lambda_3(D) omega is well-defined per TIME period,
but it is a function of (D, omega) — with omega free — not of D alone.

---

## TASK 3 — THE CLASSICAL (hbar-FREE) SINGLE-VALUEDNESS TEST — **selects NO D_n**

Classical single-valuedness of the iso-rotation: chi is an SO(3)/U(1) angle, so
chi and chi+2pi are the same physical configuration. Over a time period T of the
uniform rotation, the accumulated phase is Delta chi = omega T = 2 pi (one full
revolution; T = 2 pi/omega).

**Delta chi = 2 pi n is satisfied for EVERY omega** (just integrate n revolutions);
it imposes NO condition on omega, hence NO condition on D. The phase closes for
ALL depths. The rotation rate omega = J/Lambda_3(D) is free; the depth D and omega
are INDEPENDENT continuous data; single-valuedness ties chi's period to omega, NOT
to D.

**=> CLASSICAL SINGLE-VALUEDNESS DOES NOT SELECT DISCRETE D. There are no D_n,
isolated or otherwise.** The accumulated phase per period is 2 pi for all D
identically — there is no Theta(D) function with isolated 2 pi n roots. The depth
continuum (NEGATIVES #39/#43) is NOT lifted.

(Counterfactual, flagged in the probe: if one MIS-identified a monotone "phase"
from Lambda_3(D), a single monotone Theta_acc(D) would give a ladder whose spacing
is set by dD/d(2pi) — generically EVENLY spaced in the monotone variable, the
geometric ladder KILLED by #48, not isolated/uneven. But this is moot: no such
accumulated phase exists.)

---

## TASK 4 — BOHR-SOMMERFELD FALLBACK — **RIDES hbar; quantizes SPIN, not DEPTH**

[FLAGGED LOUDLY: this section RIDES hbar — an import. It is the fallback only
because the classical test (Task 3) selected nothing.]

The only way a condition on chi can constrain anything is to quantize the
conserved momentum p_chi = J itself:

    J_chi = oint p_chi dchi = 2 pi Lambda_3(D) omega = 2 pi hbar (n + nu).   [rides hbar]

But note WHAT this quantizes: it fixes the **angular momentum J = hbar(n+nu) of the
iso-rotor** — the SPIN of the soliton — building a ROTATIONAL BAND on a SINGLE
cell of arbitrary depth:

    E_n(D) = E0(D) + J^2/(2 Lambda_3(D)) = E0(D) + hbar^2 (n+nu)^2 / (2 Lambda_3(D)).

For FIXED D this is a tower of SPIN states on ONE cell; it does NOT select which
depths D exist. **The integer n labels the soliton's SPIN, not a depth rung; D
remains a free continuum.** To convert this into a depth ladder one would have to
ADD a non-native constraint linking J to D (e.g. self-consistency E0(D) =
J^2/2Lambda_3) — an IMPORTED relation, exactly the kind of patch the charter
forbids. With no native link, **even riding hbar the natural single-valuedness
condition quantizes SPIN, not DEPTH.**

---

## TASK 5 — THE MASS PATTERN — **no depth ladder to report**

Since no D_n are selected (classical) and Bohr-Sommerfeld quantizes spin not depth,
there is NO native discrete depth ladder D_n and hence NO M(D_n) sequence from this
mechanism. The Misner-Sharp mass m(D) = (c^2 r/2G)(1 - e^{-2phi}) and the soliton
energy E0(D) remain CONTINUOUS in D — the #39/#43 depth continuum is NOT lifted by
the angular monodromy. The only discrete structure available (and only by riding
hbar) is the SPIN tower E_n = E0(D) + hbar^2(n+nu)^2/(2 Lambda_3(D)) on a cell of
arbitrary depth: an **n^2-spaced rotational band**, O(1) in shape, NOT a large
lepton-like hierarchy and NOT a depth selection.

---

## PREMISE LEDGER (chose / derived / rides-hbar)

DERIVED (fell out of the settled objects / exact symbolic / solved BVP):
- The settled carrier is the S^2 baby-Skyrme charge-1 easy-axis hedgehog with ONE
  radial profile Theta(r) + rigid SO(3) orientation; no second internal profile
  psi(r) exists (that needs an S^3/SU(2) target, not the n-field) [native_stabilizer].
- degree B = 1 and dTheta = pi for ALL depths (depth-INDEPENDENT, to BC precision).
- The radial Berry/geometric phase = 0 exactly (meridian path, zero swept solid
  angle, d(longitude)=0).
- Lambda_3(D) is depth-dependent (8.81 -> 134.11, p:0->2) but is a STIFFNESS, not
  a phase [n3_direction_distribution iso-inertia, reproduced here].
- L_eff = (1/2)Lambda_3(D)chidot^2 - E0(D); p_chi = Lambda_3(D)chidot; chi cyclic
  => p_chi conserved; omega = J/Lambda_3 a free classical datum [sympy, exact].
- Classical Delta chi = 2 pi closes for ALL omega and ALL D => selects no D_n
  [sympy/analytic].

CHOSE (provisional, tagged; none a smuggled mechanism):
- The depth family phi = -p ln(r_int/r), depth D = phi_core; p in {0,...,2} scan
  [the settled cell log profile B1; numerical scaffolding].
- chi = iso-rotation about the easy axis as "the angular collective phase" [the
  natural cyclic collective coordinate; the standard soliton reduction].
- xi=1 units; finite cell [r_core=0.05, r_int=r_core+12L]; BVP grid [scaffolding].

RIDES-hbar (import, flagged; used only as the Task-4 fallback):
- Bohr-Sommerfeld J_chi = 2 pi hbar (n+nu). It quantizes SPIN, not depth.

---

## HONEST VERDICT: **NO-MONODROMY**

**There is NO depth-dependent angular monodromy in the settled single-cell
charge-1 hedgehog.** (1) The make-or-break check is unambiguous: the soliton's
angular content is a rigid degree-1 winding (depth-independent) plus a rigid
global iso-rotation phase chi with zero radial accumulation; the only
depth-dependent angular quantity (Lambda_3(D)) is a stiffness, not an accumulated
phase. (2) Classical (hbar-free) single-valuedness Delta chi = 2 pi n closes for
every depth and selects NO discrete D_n. (3) Even the Bohr-Sommerfeld fallback —
which RIDES hbar — quantizes the soliton's SPIN, not the cell depth; D stays a
free continuum. (4) Consequently there is no native depth ladder and no M(D_n)
mass pattern; only an hbar-imported n^2 spin band on a cell of arbitrary depth.

The verdict is **NO-MONODROMY** (and, as a corollary, NOT the EVENLY-SPACED
geometric ladder either, since no ladder is selected at all). The LLM#3 facet-1b
mechanism, tested honestly and hbar-free FIRST, does NOT discretize the depth:
the chi collective coordinate is rigid, with no depth-dependent accumulated phase
to quantize. This CORROBORATES and does not lift NEGATIVES #39/#43 (depth is a
continuum in isolation); the single-cell collective-coordinate quantization adds
SPIN structure, not a depth selection. The depth-discreteness gap is NOT closed
by single-cell angular monodromy — consistent with the standing read that lepton
discreteness needs an ingredient beyond the bare single-cell L2+L4 hedgehog
(spinor/WZW statistics, or an inter-cell/ensemble link).

SCOPE (premise set carried by this negative, for NEGATIVES_REGISTRY):
single-cell; settled L2+L4 S^2 baby-Skyrme charge-1 easy-axis hedgehog; depth
family phi=-p ln(r_int/r); static back-reacted cell with same-minus mirror seal;
collective-coordinate reduction to the rigid SO(3) iso-rotation; classical
single-valuedness (hbar-free) primary, Bohr-Sommerfeld flagged. If a DIFFERENT
carrier admits a genuine second internal profile psi(r) (an S^3/SU(2) target), or
if an inter-cell phase links chi across cells, the existence question REOPENS and
this negative is CONDITIONS-CHANGED.

---

## BLIND VERIFIER — PENDING. ATTACK HERE:

1. **The make-or-break ansatz choice (load-bearing).** The kill rests on the
   settled carrier being an S^2 baby-Skyrme hedgehog with only ONE radial profile
   + a rigid orientation, so there is no internal profile psi(r) to carry a
   depth-dependent accumulated phase. VERIFY this is forced by the settled model
   (native_stabilizer) and not a convenience: does the L2+L4 n-field admit ANY
   second profile/internal-twist degree of freedom (e.g. a non-hedgehog charge-1
   configuration, an axially-symmetric ansatz with an internal longitude profile
   psi(r), or an S^3 lift) that WOULD accumulate a depth-dependent phase? If yes,
   the existence question reopens.
2. **The Berry-phase = 0 claim.** Confirm independently that the internal vector
   n(r) traces a meridian (d(longitude)=0) along the radial path so the geometric
   phase vanishes for every depth. Check whether the BACK-REACTION or the seal
   mirror-fold induces any internal longitude rotation psi(r) != const that would
   give a nonzero, depth-dependent Berry phase. (If the seal twists the internal
   frame, a monodromy could reappear.)
3. **The classical-vs-hbar boundary.** Confirm that Delta chi = 2 pi closes for
   all omega and all D (no hidden D-dependence in the period), and that the ONLY
   way to constrain D is to quantize J (rides hbar) — and that quantizing J gives
   SPIN, not DEPTH. Hunt for a native (hbar-free) constraint linking J to D that
   I may have missed (e.g. a regularity/seal condition on the rotating profile
   that ties omega to D).
4. **Lambda_3(D) monotonicity.** Confirm Lambda_3(D) is smooth/monotone with no
   isolated structure (8.81 -> 134.11), so no "accidental" depth selection hides
   in the inertia. mpmath at deeper p to be sure float64 holds.
5. **Whole-before-slice.** This tested the depth-MONODROMY route specifically.
   Confirm the negative is scoped to that route and does NOT over-claim against
   other depth-selection mechanisms (charge-N towers, seal quantization, ensemble
   self-consistency) — those remain open and are NOT addressed here.

---

## DATA-BLIND CONFIRMATION

No lepton/hadron wall numbers, no Koide ratio, no sqrt(2), no 45-degree condition,
no lepton number was loaded, matched, or consulted in any script or in this
document. The push was METRIC-LED (does the settled collective-coordinate reduction
produce a depth-dependent monodromy?), tested hbar-FREE FIRST, and the LLM#3
mechanism was DERIVED-or-refuted, never assumed. #48 was used only as a guard.
The negative is reported as it fell out.

---
## VERIFIER-CLEARED — STANDS (appended 2026-06-15; agent a578d8f97c25bf4f6)
Independent re-derivation + active S^3/psi(r) rescue. NO-MONODROMY STANDS, with
a SHARPER reason: the internal-longitude twist Psi(r) enters L2+L4 ONLY through
(Psi')^2 (coefficient W = pi xi r^2 e^{-phi} sin^2 Theta >= 0), with ZERO linear
Psi' term and NO bare-Psi term — so Psi=const is the forced minimum, no source
for a depth-twist, for BOTH the S^2 baby-Skyrme AND a genuine S^3/SU(2) Skyrme
field (the iso-twist is a U(1)-cyclic coordinate either way). Berry phase = 0,
winding depth-fixed (deg 1, dTheta=pi), chi cyclic => Delta chi=2 pi n closes
for every D (no D_n). Bohr-Sommerfeld quantizes SPIN, not depth. THE DECISIVE
STRUCTURAL POINT: a genuine depth-monodromy would need the S^3 HOPF/WZW
TOPOLOGICAL (pi_3) term — NOT a sigma-model profile — and that term is ABSENT
from L2+L4 (consistent with hopf_spinor #47c). Non-blocking: a profile-
normalization convention in the source ansatz (verdict rides only on the
convention-robust Psi-structure + BC-fixed invariants).
