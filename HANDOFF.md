# HANDOFF — Resume Instructions and Perspective

## THE GOAL — READ BEFORE ANYTHING ELSE (Charles, 2026-06-13)

The goal is THE FORMATION, TOPOLOGY, AND PROPERTIES OF PARTICLES
(particles = the closed cells). Deliver: what TYPES exist
(families/generations), HOW they form, their PROPERTIES (angular
numbers + MASSES, aimed at the lepton wall numbers). NOT "what a
cavity looks like inside."

RECURRING FAILURE MODE TO AVOID (Charles named it the "evil genie";
the innocent version is "LLMs reach for the easiest response"): every
push this session drifted to the TRACTABLE thing instead of the GOAL —
the interior/bulk solve (DEAD END: smooths to one round type, #34),
frozen backgrounds, the trust-window, determinacy/counting
sub-questions, action-extremization, invented mechanisms (stiffness,
integer-tiling, constituent-counting), and narration/reassurance.
Do NOT. WHERE THE ANSWER LIVES: the BOUNDARY / TOPOLOGY / FORMATION
sector — the H1 AREA FORM (which produced the only real discrete
results, N=3, q=1/3, eta=1/18), the seal/closure, the mirror fold. The
seal is hard/singular — that is WHERE THE PHYSICS IS, not a reason to
retreat to the interior. Aim at the WHOLE goal; do not stop at a
sub-result; do not invent; deliver the answer, not reassurance.
(Full lesson: memory goal-particles-not-interior.)


Rewritten 2026-06-13 at the critical-universe reframe. Supersedes the
2026-06-12 W-series version (in git history; the W1-W8 blow-by-blow is
in the results docs + NEGATIVES_REGISTRY, not repeated here).

Read order for a new instance:
1. THIS FILE, all of it — the perspective and the working discipline.
2. CRITICAL_UNIVERSE_FRAME.md — the governing frame (confirmed by
   Charles 2026-06-13). Then CATALOG_FRAME.md (which it subsumes).
3. STATE.md — the FRAME REDIRECT block leads; frontier + queue follow.
4. CLAUDE.md — the charter. NEGATIVES_REGISTRY.md (#1-#31) before
   treating any banked negative as blocking.
5. Results docs as needed (w_alg, w6, w8 are the live ones).

## The perspective (carry this; do not re-derive your way back to it)

The program is one derivation from a candidate theory of matter — and
this session found, after a long conversation, that we had been asking
the derivation the wrong way for months. THE FRAME, in plain terms:

The METRIC is primary and GENERATES the dilation field (not the other
way round). The universe is the metric curving a FINITE amount of
mass-energy. Matter — particles — exist only at ONE CRITICAL AMOUNT of
mass-energy, where the curvature is exactly enough to hold structure;
depart in either direction and you get unformed energy. It is a
two-sided critical point, dimensionful — the same shape of idea as the
cosmological critical density (Omega = 1). The horizon condition the
program already found, c^2 = 2GM/r* (the universe at its own
Schwarzschild compactness), is plausibly that critical condition.

This frame DISSOLVES the two things the program was stuck on, with no
invented mechanism: DISCRETENESS is how the critical finite energy
PARTITIONS (a fixed total beads into preferred portions — not a
vibration spectrum); STIFFNESS is the universe SITTING at the critical
point (not an added term). The whole W2-W8 stiffness/spectrum/catalog
effort re-reads as solving PIECES of a whole we were solving wrong.

THE ONE OPEN, CHECKABLE THREAD: does closing the WHOLE metric PIN one
absolute universe (Charles's "it only closes one way") or leave a
scale-family? The solved pieces look scale-free (c and G alone are
scale-free; the quantities we test are dimensionless RATIOS = the wall
numbers; absolute scale normally set by one observation). Charles
bets the whole carries a ruler the pieces don't. That bet is THE
calculation (see Queue).

## How to work (the discipline this session paid for)

- SOLVE THE WHOLE METRIC. Unreduced. Both radial-phi AND angular
  sectors co-equal. ADD NOTHING (no W_wave/stiffness/D_cell/kappa).
  SLAVE NOTHING (no algebraic q* elimination, no scanned shape). Do
  NOT extremize a chosen action as a substitute for analyzing the
  metric's geometry. Every AI before has shortcut exactly here.
- Charles holds the FRAME; the driver executes and verifies. He
  corrected the driver's framing three times this session (each a
  real fix). Watch your own verbs: "add/demand/select/quantize" are
  invent-tells; "compute/what is there/does it close" are the native
  register. Aim verifiers at NEGATIVES as hard as positives (the
  session's deepest find came from a verifier attacking a recorded
  death).
- Verifier-before-record (independent, own machinery); pre-register;
  data-blind vs the wall numbers (never tune); commit per result;
  nothing canonical without Charles. Maximize subagents to conserve
  context; GPU = V100 torch float64 (CLAUDE.md pitfalls).
- Memory carries the deep lessons: critical-universe-frame,
  particle-catalog-frame, framing-not-computation-charles-role,
  domino-heuristic-template-tripwire, integer-insight-origin.

## Must-not-lose (durable facts; the rest is in the results docs)

- The frame above and its one open thread.
- The DATA-BLIND test: the six lepton wall numbers (contract 26fc757;
  C_M1=0.977679087638, C_E1=1.93121474779, ratio=1.97530536575 +
  warped triple). The masses we predict are RATIOS (dimensionless).
- Banked GEOMETRIC results that survive as pieces of the whole (these
  came from analyzing geometry — the durable path): the seal = a
  same-minus MIRROR FOLD, not an edge (w6_results); Misner-Sharp mass
  = the cell's public charge (Q=2 p_F); the angular numbers q=1/3,
  eta=1/18, N=3 from the H1 AREA FORM (the one native discreteness so
  far — topological/geometric, the template); the 1.90-class ratio =
  2 pi^2/(3 G*) exactly, Gelfand-Bratu (w_alg_results); the per-ray
  structures Liouville/Tzitzeica/Poschl-Teller (exactly solvable).
- 7.004 (dilation depth at the CMB boundary) = ln(1+z_CMB) via
  1+z=e^phi — currently an observational anchor; whether closure
  derives it is the determines-vs-relates question made concrete.
- NEGATIVES_REGISTRY #1-#31 are premise-scoped; the discreteness
  refusals (#1 box-control, #28 bands-not-lines, W7, W8 #31) were
  MODE-SPECTRUM/STABILITY questions and do NOT bind the critical-
  universe frame (they answered the wrong question).
- Convention: W4-B kappas are member-unit (kappa_true = kappa*2/c_m);
  all kappa!=0/time-dependent physics is hypothesis-grade.
- Provenance: theorem scripts rescued in rescued_workspaces/ (commit
  scripts WITH results docs — a near-loss happened 2026-06-11).
  AUDIT.md is Charles's untracked S116 macro copy; leave it.

## Queue (ordered)

DETERMINACY ASIDE (registry #32/#33, w_whole_results.md): a
single-cell whole-profile closure does NOT pin a unique universe —
absolute size is scale-free (#32, units, one observation) and the
single-cell compactness is a continuum (#33). NOTE: the
"integer cell-tiling / whole-number-of-lumps" idea that briefly
appeared as a redirect was a DRIVER OVER-REFRAME, NOT Charles's — it
is STRUCK. Charles's picture is that the geometry forces the TYPES of
lumps (what kinds of stable structures can exist), not a count of
identical tiled lumps. The determinacy/pinning analysis itself was a
DETOUR from the actual instruction below.

DONE 2026-06-13 (registry #34): the interacting-whole BULK INTERIOR
solve (both sectors live, two-way) gives EXACTLY ONE TYPE — a round
cell, a smooth continuum; the metric's angular operator is pure
DAMPING (no bulk angular source). The interior is a DEAD END for
types. Confirmed: the TYPES live at the BOUNDARY/TOPOLOGY, not the
bulk.

STRUCTURE SOLVED 2026-06-13 (registry #36, wcc_results.md,
blind-verified): the WHOLE closed cell (interior + seal mirror-fold
closure, both sectors, two-way, solved as one BVP — finally NOT
truncated at the interior) supports NO dynamical angular structure —
ONE ROUND body even closed (the angular nonlinearity -v_theta^2
linearizes to EXACTLY ZERO about round => sign-definite pure damping;
angular gap positive under every seal closure). THE STRUCTURE IS
COHOMOLOGICAL, NOT DYNAMICAL: the H1 area form is topological
(integral = 4pi; an EXACT boundary transgression d[(ln f)omega_H1]
delivered at the closure, invisible to the bulk EL). This is WHY
q=1/3 and N=3 are real yet NEVER appear in any dynamical spectrum
(cohomology vs eigenvalues) — and why every spectral discreteness
hunt (#1/#28/W7/W8/#34) failed: wrong sector. The geometry splits
into a trivial round dynamical body + a non-trivial TOPOLOGICAL
2-form at the seal, and ALL real structure (the discreteness, the
numbers that worked) is in the topological part.

1. THE GOAL PUSH (queue head, now TOPOLOGICAL not dynamical): derive
   the PARTICLE TYPES from the COHOMOLOGY OF THE CLOSURE — what the
   area form omega_H1 (integral 4pi), the exact boundary transgression
   d[(ln f)omega_H1], and the seal's odd-parity crease sector encode
   about distinct types. This is purely topological/cohomological work
   on the closure — NOT dynamics, NOT a mode spectrum, NOT
   mass-matching, NOT integer-hunting (the {3,5,7} numerology was
   rejected #35). FIRST: the dedicated TOPOLOGY VERIFIER on the #36
   D3 reading — does the area-form transgression glue antisymmetrically
   across D=0 under the actual same-minus junction (vs the orientation
   argument used)? Then: assemble the cohomological closure structure
   (the area form + transgression + parity sectors) toward what
   distinguishes types. Properties/masses come AFTER the type-structure
   is topologically derived; the seal charge-correction Delta_p_F
   (per type, from the mirror-fold crease BC) is the bridge to numbers,
   data-blind, LAST.
2. Absolute scale stays one observational anchor (#32).
3. Macro consilience roadmap (memory) once the frame is load-bearing.
