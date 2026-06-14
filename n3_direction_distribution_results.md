# The Energy Distribution Across the Three N=3 Directions — Results

Date: 2026-06-14. Driver: Claude (Opus 4.8, 1M context). NEW file
(append-never-edit, Self-Hardening discipline). Mode: **DERIVE** (gated,
authorized by Charles). Frame: CANON C-2026-06-14-1 + refinement;
native_stabilizer_results.md (the settled L2+L4 angular Lagrangian);
h1_types_results.md (N=3, End(H1)=1+3+5). **DATA-BLIND**: no lepton/hadron
wall numbers, no Koide, no sqrt(2), no 45-deg condition loaded, computed, or
compared. **NO spinor, NO Dirac, NO hbar, NO photon** — only L2+L4 and the
metric. All amplitudes reported as pure numbers (kappa/xi cancels in ratios).

Scripts (commit-grade, this push):
- `n3_direction_iso_inertia.py` — V100 torch float64: the iso-moment-of-inertia
  tensor Lambda_ab over the finite cell (flat + deep-phi).
- `n3_isotropy_check.py` — CRITICAL self-audit: pure-hedgehog isotropy + grid
  convergence + profile-run convergence (rules grid artifact in/out).
- `n3_split_characterize.py` — resolution independence, AXIAL-vs-Z3 pattern,
  L2/L4 split, kappa/cell/deep-phi dependence, sqrt-structure read-out.
- `n3_analytic_audit.py` — sympy CLOSED-FORM angular integrals + numeric radial:
  matches the GPU 3D tensor to 4 digits; exposes the mechanism analytically.

Blind verifier: **PENDING** (verifier-before-record; attack-here block at end).

---

## THE QUESTION (operationalized, premises tagged)

The charge-1 hedgehog soliton has an internal SO(3) orientation in the target
space. The THREE N=3 directions are the three target axes / the l=1 internal
channel. We compute the energy associated with each of the three and ask:
**degenerate or split? if split, by what native mechanism, and with what
amplitude/pattern? is a sqrt(m) amplitude native here?**

### Operational definition of "the 3 N=3-direction modes" [CHOSE, stated loud]

We identify the three N=3 directions with the **three SO(3) iso-rotation
generators** T_a (a=1,2,3) acting on the unit-vector field n — i.e. the
eps_abc triplet, the **spin-1 piece of the forced alphabet End(H1) = 3⊗3 =
1+3+5** (h1_types_results.md). An infinitesimal iso-rotation about target axis
a is the field velocity

    v_a = T_a n = e_a x n          [(T_a)_{bc} = -eps_{abc}].

Promoting the soliton's internal orientation R∈SO(3) to a slow collective
coordinate R(t)=exp(omega_a T_a t), the iso-rotation kinetic energy is
(1/2) Lambda_{ab} omega_a omega_b, with the **iso-moment-of-inertia tensor**

    Lambda_{ab} = INT d^3x  sqrt(g) e^{2phi}/c^2  [
        (xi/2)(v_a.v_b)
      + (kappa/2) g^{ij}( (v_a.v_b)(d_i n.d_j n) - (v_a.d_i n)(v_b.d_j n) ) ]

read off as the t-t kinetic form of the SETTLED L2+L4 action (the L4 piece is
the t-t reduction of L4 = -(kappa/4)(d_m n x d_n n)^2 = |omega_H1 current|^2_g,
native_stabilizer Task 1). **The "energy of the three N=3 directions" = the
three eigenvalues of Lambda_ab** (the inertia / energy cost of unit iso-angular
velocity about each target axis). **DEGENERATE <=> Lambda_ab ∝ delta_ab.**

Tags: the **iso-rotation generators v_a = e_a x n** are DERIVED (the SO(3)
action on the n-field is the l=1/spin-1 channel of End(H1)). Choosing the
**collective-coordinate inertia** as "the energy of a direction" is CHOSE
(standard soliton collective-coordinate energy; used classically and
data-blind — we report Lambda_ab as a pure-number RATIO structure and do NOT
multiply by hbar or form hbar^2/2Lambda; no quantization smuggled).

### Soliton setup [DERIVED ansatz + BVP, reused machinery]

The settled native carrier (native_stabilizer_results.md) is the easy-axis
baby-Skyrme hedgehog with radial profile,

    n = ( sinTheta(r) sin th cos ph, sinTheta(r) sin th sin ph, cosTheta(r) ),
    Theta(r_core)=pi (charge 1)  ->  Theta(r_int)=0 (unwound exterior),

on the finite back-reacted cell ds^2 = -e^{-2phi}c^2 dt^2 + e^{2phi}dr^2 +
r^2 dOmega^2, sqrt(g)=e^{phi} r^2 sin th. The profile Theta(r) is the EL BVP
solution of E2_r+E4_r (native_profile_bvp machinery, residual ~1e-8); width
~ sqrt(kappa/xi). Backgrounds: flat phi=0 (theorem) and deep log cell
phi=-p ln(r_int/r), p=0.5,1,2.

---

## THE RESULT: SPLIT (axial 2+1), native to the easy-axis ansatz

### Self-audit first (verifier-before-record discipline, run by the driver)

The PURE hedgehog Theta=theta (no radial profile) is EXACTLY SO(3)-covariant
(iso-rotation = space-rotation), so its Lambda_ab MUST be isotropic. The
integrator reproduces this to grid precision (n3_isotropy_check.py):
spread (max-min)/mean = 1.77e-4 -> 4.36e-5 -> 1.08e-5 -> 2.69e-6 as nth=nph =
60 -> 120 -> 240 -> 480 (converges as 1/n^2 -> 0), off-diagonal = machine zero
(~1e-15), three diagonals -> equal (2493.29). **The integrator is correct and
an isotropic case reads isotropic.** Therefore any split in the PROFILE run is
physics, not a coordinate artifact.

### The split is REAL and resolution-independent

For the BVP profile Theta(r), Lambda_ab does NOT converge to isotropic — it
splits, stably, into **two equal + one distinct** (n3_split_characterize.py,
flat, kappa=xi=1, cell=12L):

    nth=nph     Lambda_perp(11=22)    Lambda_3(33)     ratio perp/along-3
      120          3662.483            14.4991            252.601
      240          3662.404            14.4991            252.596
      360          3662.389            14.4991            252.595

Off-diagonal = machine zero (~2e-15). **Eigenvalues: {Lambda_3, Lambda_perp,
Lambda_perp}** with eigenvector of the distinct one along the **target-3 axis**.

### The pattern is AXIAL (2+1), NOT cyclic Z3

Lambda_ab = diag(Lambda_perp, Lambda_perp, Lambda_3) with all off-diagonals
zero. The two perpendicular target axes (1,2) are degenerate; the third
(target-3) is special. **This is an axial 2+1 pattern, NOT a cyclic/Z3 pattern.**
There is no three-fold symmetric splitting; one direction is singled out.

### The mechanism (CLOSED FORM): the easy-axis structure of the native ansatz

The settled ansatz has **n3 = cosTheta(r) depending only on r** — it singles
out target-axis 3 as the "easy axis" along which the profile interpolates
pi->0. The closed-form L2 angular integrals (sympy, n3_analytic_audit.py) make
the mechanism exact:

    INT |v_3|^2 dOmega = (8 pi/3) sin^2 Theta(r)      [spins the (n1,n2)
        winding PHASE; LOCALIZED to the twist region; -> 0 in the unwound
        exterior where Theta->0]
    INT |v_1|^2 dOmega = (4 pi/3)(cos 2Theta(r) + 2)  [TILTS the easy axis;
        -> (4pi/3)(3) = 4pi in the unwound exterior (Theta->0), i.e. NON-zero
        over the ENTIRE cell volume]

So:
- **Lambda_3 (along the easy axis)** = (xi/2) INT r^2 (8pi/3) sin^2Theta dr —
  soliton-LOCALIZED, cell-size-INDEPENDENT (~14.5 across cells 12L-30L).
- **Lambda_perp (tilting the easy axis)** = (xi/2) INT r^2 (4pi/3)(cos2Theta+2)
  dr — picks up cos^2Theta(r)~1 over the WHOLE exterior, so it integrates the
  entire cell volume and is **cell-size DIVERGENT**.

Analytic-angular x numeric-radial reproduces the GPU 3D tensor to 4 digits
(L2-only: perp 3655.74 vs 3655.75; along-3 8.806 vs 8.806; ratio 415.1) —
the split is not an integrator artifact. The split is dominated by L2
(L2 ratio 415); L4 alone gives only ratio 1.17 (it is soliton-localized in
both channels).

### The amplitude is NOT a clean pure number — it is background-dependent

The split RATIO is NOT a single universal constant. It depends on the cell and
the background (n3_split_characterize.py Section 4):

    case            Lambda_perp   Lambda_along3   ratio perp/along-3
    flat kappa=0.25    463.5          1.90           244.4
    flat kappa=1.00   3662.4         14.50           252.6
    flat kappa=4.00  29117.5        115.1            253.0
    flat kappa=9.00  98067.4        388.1            252.7    <- ratio ~const in kappa/xi
    flat cell=8L      1091.3         13.59            80.3
    flat cell=12L     3662.4         14.50           252.6
    flat cell=20L    16878.4         15.23          1108.5
    flat cell=30L    56829.0         15.59          3645.6    <- ratio DIVERGES in cell size
    deep p=0.0        3662.4         14.50           252.6
    deep p=0.5        2419.4         32.68            74.0
    deep p=1.0        1779.1         71.64            24.8
    deep p=2.0        1135.1        164.16             6.91    <- ratio SHRINKS with phi-depth

Two robust facts and one caveat:
- **Lambda_along3 is the localized, well-defined number** (cell-independent
  ~14.5 in flat; grows with phi-depth as the back-reaction stiffens the core).
- **Lambda_perp is cell-size divergent** (the easy-axis tilt has a long-range
  cos^2Theta tail filling the cell) — the global-monopole signature.
- **The perp/along-3 ratio is therefore NOT a clean universal pure number**:
  it is ~253 only at the specific flat 12L cell; it diverges with cell size and
  collapses (toward ~7) with phi-depth. The ONE robust dimensionless statement
  is the AXIAL PATTERN (2 equal + 1 distinct) and the SIGN (the easy axis is
  far CHEAPER to spin than to tilt: Lambda_3 << Lambda_perp).

---

## THE sqrt-STRUCTURE VERDICT: NO native sqrt(m) in this winding sector

Every quantity that fell out is **mass/energy-dimensioned**. Lambda_ab is an
inertia (mass·length^2 / an energy per unit angular-velocity-squared); the
iso-rotation energy is E = (1/2) Lambda_ab omega_a omega_b — **quadratic in the
angular velocity / collective coordinate omega**. In this classical
winding-sector computation the natural primitive amplitude is the collective
coordinate omega (or the orientation R∈SO(3)) and the energy is omega^2 ·
(inertia). There is **NO place where mass appears as the SQUARE of a more
primitive amplitude such that a sqrt(m)-amplitude is the native object**: the
inertia itself is energy-valued, and the only "square" present is the trivial
kinetic omega^2 (the amplitude IS omega, energy IS quadratic, but a
sqrt(energy) is not a distinguished native variable — omega is dimensionless-up-
to-time and energy-per-omega^2 is the inertia). A sqrt(m) amplitude is what a
DIRAC SPINOR supplies (its component being sqrt-of-a-density); this computation
deliberately used NO spinor, and **no sqrt(m) amplitude is native to the
winding sector alone.** Mass here is partitioned as ENERGY across the three
directions (an inertia tensor), not as a squared amplitude.

(Honest nuance: one can always WRITE E ~ omega^2 and call omega "sqrt(E/inertia)",
but that is a tautology of any kinetic term, not a native sqrt(mass) STRUCTURE.
The winding sector hands back energies/inertias, not a primitive amplitude whose
square is the mass.)

---

## PREMISE LEDGER (chose vs derived)

DERIVED (fell out of the settled objects / exact symbolic / solved BVP):
- The iso-rotation generators v_a = e_a x n are the SO(3)/spin-1 (l=1) channel
  of the forced alphabet End(H1)=1+3+5 [h1_types].
- The L2+L4 t-t kinetic form (the inertia density) IS the settled action's
  time-reduction [native_stabilizer L4 = |omega_H1|^2_g].
- The easy-axis hedgehog n=(sinTheta sin th cos ph, ..., cosTheta(r)) is the
  settled native carrier [native_stabilizer ansatz]; BVP profile (residual ~1e-8).
- Pure-hedgehog isotropy (exact SO(3)) — reproduced to grid precision: the
  integrator is correct.
- The SPLIT is real and resolution-independent (ratio 252.6 stable 120-360).
- AXIAL 2+1 pattern, off-diagonal = machine zero (NOT cyclic Z3).
- CLOSED-FORM mechanism: INT|v_3|^2 = (8pi/3)sin^2Theta (localized);
  INT|v_1|^2 = (4pi/3)(cos2Theta+2) (fills the cell) — sympy exact, matches GPU.
- Lambda_along3 localized/cell-independent; Lambda_perp cell-size divergent.

CHOSE (provisional, tagged; none a smuggled mechanism):
- "3 N=3 directions" = 3 SO(3) iso-generators (the natural l=1 reading). A
  DIFFERENT operationalization (e.g. the 3,5 theta-varying pieces of End(H1),
  or the 3 radial modes) could give a different distribution — flagged.
- Collective-coordinate inertia as "the energy of a direction" (standard;
  classical, data-blind, no hbar).
- xi=1 units; finite cell [r_core, r_int], r_core=0.05, cells 8L-30L.
- phi backgrounds flat + deep log p=0.5,1,2.

---

## HONEST VERDICT (one paragraph, mapped to the three pre-declared outcomes)

The three N=3 directions are **SPLIT, not degenerate** — but in an **AXIAL
(2+1) pattern, not a cyclic/Z3 one**, and the splitting amplitude is **not a
clean universal pure number**. The native mechanism is the **easy-axis
structure of the settled hedgehog ansatz**: because n3 = cosTheta(r) singles
out target-axis 3, spinning the winding phase about that axis (Lambda_3) is
soliton-localized and cheap, while tilting the easy axis (Lambda_perp, axes 1
and 2) costs the long-range cos^2Theta tail over the whole cell — so
Lambda_perp >> Lambda_3 with the two perpendicular axes degenerate. The robust
dimensionless content is the PATTERN (2 equal + 1 distinct) and the SIGN
(easy-axis spin far cheaper than tilt); the ratio itself (~253 at flat 12L)
DIVERGES with cell size and SHRINKS with phi-depth, so it is background-
dependent, not a constant like sqrt(2). No sqrt(m) amplitude is native to this
winding sector: every quantity is energy/inertia-valued, mass is partitioned as
energy across the directions, and the only square present is the trivial
kinetic omega^2 — the sqrt(m) primitive is exactly the spinor input this
computation deliberately omitted. **Mapped to the pre-declared outcomes: this
is NOT clean (A) DEGENERATE, and NOT (B) SPLIT-with-amplitude-sqrt(2). It is
closest to (C) SPLIT WITH A DIFFERENT AMPLITUDE — UDT's native winding-sector
prediction is an AXIAL 2+1 easy-axis split (Lambda_perp >> Lambda_3), whose
amplitude is background-dependent (not a universal pure number) and whose
pattern (one special axis, two degenerate) is NOT the three-fold Koide-style
structure.** The decisive corollary for the program: a cyclic three-fold
(Koide-type) splitting and a native sqrt(m) amplitude do NOT emerge from the
winding sector alone — both would require an EXTERNAL source (a spinor's
sqrt-amplitude and spin multiplicity, or an inter-cell/ensemble coupling that
treats the three on equal footing), consistent with the (A)-flavored reading
that the lepton splitting needs an ingredient beyond the single-cell L2+L4
hedgehog.

---

## BLIND VERIFIER — PENDING. ATTACK HERE:

1. **The operational definition (the load-bearing choice).** Is "3 N=3
   directions = 3 SO(3) iso-generators" the right native reading, or should the
   three be the 3-piece of End(H1)=1+3+5 (a different object), or the three
   lowest RADIAL modes, or the three components of the l=1 fluctuation of n?
   Re-do with at least one alternative and check whether SPLIT/axial survives or
   the pattern changes. The whole verdict rides on this choice.
2. **The easy-axis ansatz.** The split is driven by n3=cosTheta(r) singling out
   target-3. Is that easy-axis form FORCED by the settled model, or is it a
   gauge/orientation choice that a different (e.g. fully symmetric S^3-type)
   charge-1 ansatz would remove? If a symmetric ansatz exists in the L2+L4 model
   that restores isotropy, the split is ansatz-dependent, not native. (Note:
   native_stabilizer SETTLED this exact ansatz; verify it is the unique native
   charge-1 carrier on S^2, not S^3.)
3. **The cell-size divergence of Lambda_perp.** Confirm INT|v_1|^2 ~
   (4pi/3)(cos2Theta+2) -> 4pi in the exterior (independently), and that the
   perp inertia genuinely fills the cell (global-monopole tail). Does the finite
   cell + seal mirror-fold REGULATE this (a Neumann seal might cut the tail), in
   which case Lambda_perp becomes finite and the ratio a real number? Re-run
   with the seal BC explicitly, not just a hard r_int cutoff.
4. **The sqrt verdict.** Confirm there is genuinely no native sqrt(m): vary the
   action to get the Hilbert inertia (not the hedgehog formula) and check the
   amplitude is omega (energy ~ omega^2), with no field-space quantity whose
   square is the mass. Hunt for a smuggled-in or smuggled-out sqrt.
5. **L2 vs L4 and deep-phi.** Confirm L2 dominates the split (ratio 415 vs L4's
   1.17) and that deep-phi collapses the ratio toward ~7 (p=2) — is there a
   phi-depth where the pattern INVERTS (Lambda_3 > Lambda_perp) or the axes
   re-degenerate? mpmath at deeper p to be sure float64 holds.

---

## DATA-BLIND CONFIRMATION

No lepton/hadron wall numbers, no Koide ratio, no sqrt(2), no 45-degree
condition, no lepton number was loaded, matched, or consulted in any script or
in this document. No spinor, Dirac operator, hbar, or photon entered the
computation — only the settled L2+L4 action and the UDT metric. The push was
METRIC-LED (what does the settled winding sector give for the three internal
directions?), not target-led. The amplitude was reported as it fell out
(background-dependent, axial 2+1), explicitly NOT tuned toward any comparison
value.

---

## VERIFIER-CLEARED — RESULT STANDS (appended 2026-06-14)

Blind verifier (Claude Opus 4.8, agent acdd8fd9d95206c42, 2026-06-14;
n3_direction_distribution_verifier_results.md + verif_n3_*.py) re-derived
independently and actively tried to rescue a cyclic-Z3 / native-sqrt(m). Both
decisive negatives STAND, with a STRUCTURAL theorem:
- AXIAL 2+1 IS ROBUST; CYCLIC Z3 NOT REACHABLE. FOUR native operationalizations
  (iso-rotation; the legacy ORBITAL l=1 m-state reading of S13.11; the l=1
  energy-density harmonic decomposition; the component-overlap tensor) ALL give
  a diagonal (X,X,Y) tensor — two equal + one special. The energy density has
  ZERO l=1 dipole (anisotropy is l=0 + l=2, axial/quadrupolar). STRUCTURAL: the
  easy-axis hedgehog n3=cosTheta leaves an exact SO(2) about axis 3, and an
  axisymmetric field can only give 2+1, NEVER a discrete 3-fold split.
- sqrt(m) NOT NATIVE; SPINOR-ONLY. L2+L4 is built entirely from the
  dimensionless unit vector n and its derivatives (quadratic/quartic in dn), so
  it contains NO term linear in a sqrt-of-density field with a mass coefficient
  — which is exactly what a Dirac mass m psibar psi supplies. Every native
  primitive is dimensionless (n), a count (winding B), a velocity (omega), or an
  energy/inertia; omega=sqrt(E/Lambda) is a tautology, not a native sqrt.
- Self-audit (isotropic hedgehog reads isotropic), closed forms, L4 axial,
  background-dependence: all CONFIRMED. NON-BLOCKING CORRECTION: the ratio's
  phi-depth trend is non-monotonic (inverts near p~0.75-1.5), not a monotonic
  shrink to ~7 — strengthens "not universal". The robust invariant is the
  axial 2+1 PATTERN (perp degenerate to machine precision at every depth).
BOTTOM LINE: Koide / sqrt(m) are NOT native to the bare single-cell winding
sector. Both require a spinor (Dirac mass) or an inter-cell/ensemble ingredient.
