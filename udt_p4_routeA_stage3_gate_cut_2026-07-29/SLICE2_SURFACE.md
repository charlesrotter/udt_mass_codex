# P4 Route A Stage 3 — SLICE-2 SURFACE (TC6): the exact remaining work per surviving cell

Date: 2026-07-29. Contract: `PREREGISTRATION.md`. **This is a HANDLE, not a launch:** no
Slice-2 leg is run here, no candidate declared, no member of ℛ_PW selected (F-S1), no fork
decided. The cells below are the 20 adjudicated composite cells of `GATE_CUT_LEDGER.tsv`
(5 pairing branches × {GENERIC, KMOD0} × {LOCALLY-EXACT, NONVARIATIONAL}), all
witness-nonempty at the declared scope, plus the 10 CENSUS-REQUIRED resonance cells.

## 1. The surface in five lines

1. Every surviving cell still owes the two WS legs — R5 (same-solution closure on ONE
   solution of 𝓡 = 0) and R14 (bootstrap stays admissibility) — plus gate 2 (per-modulus
   J06 branch recording) and gate 4's current-conservation leg: ALL solution-dependent,
   none dischargeable candidate-free (F-S6 boundary of Slice 1).
2. Gate 1's on-shell leg differs per stratum: GENERIC = explicit integrability of a
   formally DETERMINED 3+7 system on one solution; KMOD0 = the same PLUS the L23-orbit
   quotient (one algebraic identity ↔ one gauge direction); RES-CNEQ0 = blocked on the
   queued deeper resonance census (CENSUS-REQUIRED).
3. On the LOCALLY-EXACT cells gate 5 needs the per-candidate wall depth from the declared
   N (derived machinery banked here: N = 2 self-pairable at jet ≤ 2; N = 3/4 needs the
   typed extension) and gate 6 needs completion data (L4) before any non-torsion period can
   be computed; on the NONVARIATIONAL cells gate 5 reduces to R_wall/R_corner admissibility
   plus wall-equation closure, gate 6 to the J11 holonomy classification [F-S7 flag].
4. Four forks gate everything downstream: L4/BR-C (completion class), BR-B (boundary
   varied-vs-held — role of the wall equations), L8/BR-A (α frozen-vs-active), and the
   pairing supply itself (P1 volume + per-slot weights; P2 distributional class) — each a
   CHOOSE that Slice 2 must either receive from Charles or carry as labeled branches.
5. Honest cost shape: the WS legs require solving 𝓡 = 0 members — the first
   solution-touching step of the whole P4 arc; everything else in Slice 2 is
   candidate-indexed symbolic work of Stage-3-Slice-1 size or smaller.

## 2. Per-cell remaining work (the 2×2 core, per pairing branch)

### LOCALLY-EXACT × GENERIC (any enumerated pairing branch)
- Gate 1 on-shell: explicit integrability of the determined 3-ODE + 7-relation system on
  ONE solution; symmetric principal symbol available (condition (i)); per-candidate symbol
  nondegeneracy check. Cost: per-candidate symbolic ODE analysis (bounded; no new theory).
- R5: mass/volume/density functionals on that same solution — needs the R5 functional
  definitions instantiated on the finite cell (no cross-solution splicing). Cost: moderate;
  first solution-dependent tile.
- Gate 2: pairing of each modulus direction, J06 determined-vs-retained branch RECORDED
  (both branches legal; the k_mod-determined branch needs r_tf ≢ 0 — banked slot theorem).
  Cost: cheap, per-candidate.
- Gate 4 WS leg: current statements on solutions (no identities to check generically —
  banked). Cost: cheap once a solution exists.
- Gate 5: instantiate the N = 2 wall census (self-pairable typed) for the candidate's
  actual R_wall; BR-B fork sets equation-vs-consistency role. Corners: general-arena
  census still typed-only (a derivation tile of its own).
- Gate 6: completion-class periods await L4; mixing candidates owe J07 transition data
  (two-sided twisted cocycle TYPE, banked) — classification machinery needs a source check
  before any load-bearing use (F-S7).
- R14: admissibility reading of any bootstrap structure on the solution set.

### LOCALLY-EXACT × KMOD0
All of the above PLUS: carry the L23-orbit quotient in gate 1 (identity ↔ gauge direction,
balanced); candidates touching the stratum must satisfy the banked identity cut (their
r_tf is tied to M); the λ-slot's anchored-log structure (P1 λ-dependent instances;
A1-corrected scope: the λ-slot is forced nonzero, log-carrying via a_F′·p0, IFF
∂λ(W_F·R_a) ≢ 0 for some field slot — in particular for every λ-INDEPENDENT nonzero field
sector, NOT for every nonzero field sector) must be carried in the candidate declaration
with that exact condition.

### NONVARIATIONAL × GENERIC
- Gate 1 on-shell: same determined-system integrability, WITHOUT symbol symmetry — the
  compatibility complex must be computed per candidate (Fischer–Marsden-style machinery,
  transformed; no assumed identities). Cost: per-candidate, potentially harder than LE
  (no variational structure to lean on).
- Gate 5: parity/sector-split + anchored-φ admissibility of the candidate's own
  R_wall/R_corner; on the varied fork, wall-equation closure with the bulk zero set.
- Gate 6: J11 holonomy of the closure data over the cycle census — classification [F-S7:
  the twisted-H¹ analog is MODEL-KNOWLEDGE; a source check is owed before load-bearing
  use]; completion cycles await L4.
- R5/R14/gate 2/gate 4 as in the LE cell (solution-dependent).

### NONVARIATIONAL × KMOD0
As above plus the identity cut and orbit quotient (same as LE × KMOD0).

### RES-CNEQ0 (all pairings, both cells): CENSUS-REQUIRED
Blocked on the queued deeper resonance-census tile (the banked shear identity is an
EXAMPLE; the stratification is TYPED-NOT-EXHAUSTED). No Slice-2 leg may adjudicate a
resonance-contacting sub-family before that census.

## 3. Cross-cell derivation tiles Slice 2 also owes (candidate-indexed, not per-cell)

- The P3 wall-block symmetry conditions (the wall analog of (i)–(iii)) per declared N —
  derivable with the same machinery as TC3 (bounded symbolic).
- The general-arena corner census (codim-2; typed-only here).
- The restricted-EH G3 status under the enumerated pairings (the R12 restrict-vs-vary
  check on the Route C stationary system) — an observation tile, bounded symbolic.
- The jet-3/4 exhaustive parametrization IF any 4th-order candidate is declared (currently
  typed via the order-4 anchor only).

## 4. What Slice 2 may NOT inherit as decided

Nothing here says any member closes on a solution, is differentiable on the cell, or has
controlled periods; the full ℛ = ℛ_PW ∩ {WS/GC} could still be empty, a point, or a family
(J15 — all first-class). The L6 fork is now a computed pairing-relative PARTITION, not a
decision. No pairing, completion, boundary stance, or α fork is chosen. Physics
adjudication stays with Charles.
