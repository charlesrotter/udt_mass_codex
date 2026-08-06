# MAP + Probe 1 — the time-live lane, copresence as a nonlocal object

Date: 2026-08-06. Branch: grok. Author: driver (Opus). Charles's go: "Open the time-live lane with
copresence as a nonlocal object and bring in the GPU if needed." MODE: MAP (frame whole, no compute)
+ a FROZEN first-probe contract. Nomenclature: `c_eff` = Charles's term; `c_E` = driver's shorthand.

## 0. Why we are here (the two catches that sent us off-static)

The static crux test (2026-08-06) landed CT-TRIVIAL, and BOTH reviews located why:
- **Wrong slice (a theorem):** on a STATIC metric, the copresence "now" is forced to coincide with
  the metric's unique hypersurface-orthogonal timelike Killing frame -> it carries zero independent
  content. Staticity RIGS triviality. Cannot test copresence where it is forced to be redundant.
- **Wrong object (a likely import):** a LOCAL field u is the aether reading the MAP flagged, NOT
  Charles's "interconnectedness," which is a RELATION BETWEEN DISTANT POINTS — inherently NONLOCAL.
  A pointwise-invariant scan cannot see a between-points structure by construction.
This lane fixes both: go TIME-LIVE (un-pin copresence) and pose copresence NONLOCALLY.

## 1. What going time-live buys (the un-pinning — structural, to be verified in Probe 1)

Time-live reciprocal-lock: `ds^2 = -e^{-2phi(x,t)}c^2 dt^2 + e^{2phi(x,t)}dx^2` (+ transverse). With
`phi_t != 0`:
- `∂_t` is NO LONGER Killing -> generically NO timelike Killing vector -> the static "u = xi/|xi|"
  pinning theorem DOES NOT APPLY. Copresence is free to carry independent content.
- The copresence congruence acquires nonzero EXPANSION `theta` and possibly SHEAR — the universe
  "stretches dynamically" (Charles's "stretches with distance ... sounds dynamic").
- An ABSOLUTE-VELOCITY invariant `gamma = -g(U_sys, u)` becomes GENUINE (a matter 4-velocity vs the
  copresence now), NOT reducible to the Killing energy (which no longer exists). This is the seed of
  preferred-frame effects — the Cassini/SPARC ladder handle, magnitude law-set (not claimed now).

## 2. Copresence as a NONLOCAL object — the formalization fork (do NOT pick the convenient one)

The reviews named four nonlocal readings. Faithfulness to "interconnectedness = relation between
distant points / whole-conditions-part":
- **N1 preferred FOLIATION** (a global "now" slicing). Nearly local; the aether/Horava reading.
  LEAST faithful — this is the import to AVOID as the primary object. (Keep as a contrast only.)
- **N2 integrated depth-stretch `V(A)/V(B)`** = the orchestra's between-points depth cocycle `delta`,
  a path integral of the depth structure. NONLOCAL, and already NATIVE (orchestra-derived, no import),
  and COMPUTABLE. FAITHFUL (an explicit A-to-B relation). **RECOMMENDED first object.**
- **N3 phi-weighted HOLONOMY** = a loop integral of the depth structure (the time-live period the
  08-05 OT probe computed, `R^0_2`). Nonlocal, path-dependent, native. Natural companion to N2.
- **N4 MACHIAN constraint** = the copresence now fixed by the WHOLE matter-energy configuration.
  MOST faithful to "interconnectedness," deepest — but needs a matter configuration to be defined,
  so it is DOWNSTREAM of N2/N3 (revisit once a source is in play).
RECOMMENDATION: run Probe 1 on **N2 (+ its N3 holonomy)** — nonlocal, native, computable, faithful;
contrast against N1 (local) to expose the difference. N4 is the horizon target, not the first step.

## 3. Probe 1 — the frozen first question (OBSERVE, analytic/symbolic, NO solve, NO GPU)

On a time-live reciprocal-lock configuration `phi(x,t)` (phi_t != 0), with copresence posed as the
NATIVE nonlocal depth relation N2 (and its N3 holonomy):
- **(Q1)** Is the copresence structure STILL metric-pinned (the static triviality persists dynamically
  — CT-TRIVIAL survives off-static), or does time-live UN-PIN it so it carries a genuine invariant?
- **(Q2)** Is there now a COORDINATE-INVARIANT, in-principle-measurable quantity built from
  (g, nonlocal-copresence) that pure-metric GR CANNOT express — specifically: (a) is `gamma =
  -g(U_sys,u)` a genuine non-Killing invariant; (b) is the N3 time-live holonomy period NON-EXACT
  and NON-GAUGE (unlike the static case, where the orchestra found it exact -> `a` free)?
- **(Q3)** Does any such invariant reference `phi`/reciprocal-lock/copresence SPECIFICALLY (a UDT
  result), or is it again imported generality (holds on any time-dependent GR metric)? The static
  probe's Q3 failed exactly here — Probe 1 must clear this bar to count as UDT content.

Outcome classes (pre-committed): **TL-TRIVIAL** (still metric-pinned/gauge, no UDT invariant) /
**TL-INVARIANT-GENERIC** (a real invariant but GR-generic, not UDT-specific) / **TL-INVARIANT-UDT**
(a genuine non-gauge invariant referencing the reciprocal-lock/copresence — the profound outcome,
ATTACK HARDEST) / **TL-MIXED**.

## 4. Premise ledger (chose / derived / THEORY / HABIT)

- reciprocal-lock metric class — THEORY (canon C-2026-06-18-1).
- TIME-LIVE branch `phi(x,t)` — CHOSE (the whole point; free-and-explored, not pinned).
- copresence = N2 native depth relation — CHOSE, faithfulness-tagged (Charles's "interconnectedness";
  N2 recommended over N1-aether; Charles may redirect the object).
- `gamma = -g(U_sys,u)` as the absolute-velocity invariant — DERIVED-candidate (Review 2), to verify.
- NO law, NO matter source yet (N4 deferred), NO magnitude — all downstream/unclaimed.

## 5. Plan, GPU, anti-hang

1. Probe 1 (now): SYMBOLIC/analytic only (sympy, CPU) — un-pinning + invariant existence. NO solve,
   NO GPU, no hang risk. Delegated, chunked (<=120-line appends, final report <=30 lines).
2. TWO adversarial reviews (different directions) as always; external review owed for any bank.
3. ONLY IF Probe 1 yields a real UDT invariant whose SIZE needs solving: a BOUNDED time-dependent
   solve — GPU (batched torch float64) for eigen/scan pieces on SAVED fields; the coupled solve
   SINGLE clean process, capped grid (Nr<=16/24), capped iters, NEVER concurrent, NEVER
   launch-and-poll (ANTI-HANG rule; six+ agents hung that way). Report throughput-limited partials
   honestly rather than hang.
4. N4 (Machian) and magnitude/Cassini-ladder are later gates, not Probe 1.

## 6. Falsifiers (F-STEER now points at PROFOUND — attack it hardest)

- **F-STEER:** after the static null, the driver WANTS TL-INVARIANT-UDT. Any step selected/phrased
  toward it fires. Reviews attack the profound outcome hardest; TL-TRIVIAL is first-class.
- **F-GAUGE:** a coordinate/probe-direction quantity called invariant without a scalar/measurable
  (the 08-05 error; Review-1's boosted-u catch).
- **F-IMPORT:** smuggling the aether/Horava ACTION or a GR foliation as the native object (Principle
  4: their MATH is a mine; their physics is gated). N1 kept only as contrast.
- **F-GENERIC:** an invariant that holds on any time-dependent GR metric (not UDT-specific) — the
  static Q3 failure; must be cleared (Q3).
- **F-SCOPE:** stamped time-live / reciprocal-lock class / free-kinematic; not a general theorem.
