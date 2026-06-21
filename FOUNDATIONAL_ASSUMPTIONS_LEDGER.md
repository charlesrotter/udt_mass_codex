# FOUNDATIONAL ASSUMPTIONS LEDGER — the recipes/structures UDT rests on

**Status:** living ledger, driver-maintained. Each item is TO BE DISCUSSED with Charles (each is a
task). **NOT canon.** Created 2026-06-21 (Charles's zoom-out: "are there other foundational
assumptions we need to deal with?"). Purpose: make EVERY load-bearing foundational assumption VISIBLE —
derived vs assumed vs admitted — before more physics is built on it (Principle 6 + 7; the
make-visible-and-ponder method).

## THE KEY LINKAGE (read first)
The program's central result — *"the CLASSICAL metric is a continuum (no classical discreteness) => we
MUST quantize"* — is CONDITIONAL on this whole stack. Birkhoff (-> round frozen -> continuum) is a
curvature-action theorem; whether matter is barren/rich is a matter-action + a(phi) question; box-control
is a boundary-structure question. **If any of these foundational recipes is genuinely different under
UDT, the classical metric may do MORE than we found — and we might need less quantization, or none.**
So this audit is not hygiene; it directly bears on the central conclusion. Most items are LARGELY
ANALYTIC to settle (cheaper than the throughput-walled solver) and LOGICALLY PRIOR to more solver work.

## SOLVER REUSABILITY (if a foundational recipe changes)
The P1-P5d solver MACHINERY (discretization, re-pose-to-full-rank, JFNK/dense-LM/continuation, gates,
time framework, native matter sector) is OPERATOR-AGNOSTIC -> REUSABLE. The curvature OPERATOR is a
contained swap (P1 was built to route a general operator). The PHYSICS VERDICTS (Birkhoff/continuum/
soliton/one-soft-object) depend on the operator -> RE-DERIVED. So a changed recipe = modify-the-operator
+ re-run-the-physics, NOT a full rebuild — but which verdicts survive is unknown until the recipe is known.

---

## THE LEDGER (ranked by load-bearing x unverified)

### F1 — The gravity-side CURVATURE ACTION  [ASSUMED = GR Einstein-Hilbert; DEEPEST OPEN]
What's assumed: the whole everything-on solver used the standard Einstein tensor G_mu_nu (the EH R-term)
on the gravity side; all UDT modification was put in the matter source. "Vacuum = GR" is therefore
BUILT-IN (a choice), not derived. Bears DIRECTLY on Birkhoff -> the continuum verdict. The deepest
Principle-7 item. Counterweight: the obvious f(phi)R modification is Cassini-dead + validated cosmology
uses minimal coupling => leans plain-R, but never DERIVED from the positional-dilation principle.
To settle (analytic): derive UDT's gravitational action from the principle (like C-18-1 derived the
metric form) — is it plain R, f(phi)R, or genuinely new? MAP exists target = the curvature-action MAP.

### F2 — The matter-side ACTION (L2 + L4)  [PARTLY AUDITED; completeness/forced-ness NOT established]
The twin of F1. L4 (= metric-norm of the native H1 area-form current) was blind-verified NATIVE (not an
imported Skyrme coefficient). BUT: is L2+L4 the COMPLETE, FORCED native matter action, or assembled/
chosen? Why those terms and not others? Derived from the principle, or settled on a plausible form?
Determines what the matter DOES. To settle (analytic): is the matter action forced (uniqueness-type
argument from UDT's structure) or are there admissible extra terms?

### F3 — The matter coupling a(phi)  [UNDER-DETERMINED; a=-1 SILENTLY USED EVERYWHERE]
How a particle's rest mass dilates with position. Field-eqn arc: a is under-determined; a=-1 = GR;
a!=-1 = genuine modification, UNFORCED at the principle level. Silent load-bearing fact: EVERY P1-P5d
solve used a=-1. So "matter is GR-coupled" is baked into every result (like F1's "curvature is GR").
To settle: derive a(phi) from UDT's matter structure (a covariant rest-mass definition — Killing energy
vs Noether charge — was the named decisive computation), or establish it stays under-determined.

### F4 — The finite-cell / seal / boundary STRUCTURE  [CANONIZED but POSITED]
Finite mirrored cells, no spatial infinity, seal = mirror-fold = time-reversal (t->-t). Canon (C-10-2)
but a strong structural posit; bears on box-control and the spectrum (a different boundary could change
what "the cell" does to discreteness). To settle: is the finite-cell/seal structure DERIVED (from the
principle / closure) or posited? What forces the seal = time-reversal reading?

### F5 — The critical-universe / "matter at one critical amount" HYPOTHESIS  [FRAME, not derived]
Metric primary (generates phi); universe = metric curving a finite mass-energy; matter exists only at
ONE critical amount; departures unform. The critical-energy hypothesis for particle formation. A framing
assumption (more load-bearing on cosmology than mass). To settle/clarify: derived, or a working frame?

### F6 — POSTULATE A boundary  [ADMITTED assumption — not hidden, but the boundary is a CHOICE]
Postulate ONLY {hbar, spin-1/2, statistics}; i = area-form native; no SM import. Honestly admitted as
input (Charles's decision). The DISCUSSION items: is the boundary right (only these three)? Is
quantization even the right framework vs later geometric emergence (the door-open clause)? Note: Step A
showed spin-1/2 actually rides the imported metaplectic framework (generic to S^2) — so "what is truly
postulated vs what comes free with the framework" needs a clean ledger.

### F7 — The SCALE BRIDGE / ~40-order autonomy gap  [KNOWN OPEN structural gap]
Gravity is scale-invariant -> ratios/shapes only; UDT admits one cosmic anchor (ln(1+z_CMB)=7.004) +
the particle m_e anchor. The open question (C-10-2's "sharp open question"): what makes particle-scale
cells spectrally autonomous from the Gpc domain. Not an assumption to remove — a gap to close.

### F8 — Embedded CHOICES in the "derived" metric form  [DERIVED form, with chart/symmetry choices]
C-18-1 derived the metric FORM from "remain relativistic", but static / spherical / diagonal / areal-r
and the slot-id P8 (conjugate-to-time = grad phi) are CHOICES, not consequences (the free solution-space
DOF). Mostly the DOF we've been exploring, but the derivation isn't choice-free — keep visible.

---

## HONEST CAVEAT
This is the driver's best audit; per the charter the driver cannot always see its own smuggled frames
(Charles holding the frame is irreplaceable). A SYSTEMATIC audit — an agent reading CANON.md + every
derivation doc + the premise ledgers, classifying each foundational claim derived/assumed/admitted —
would likely surface more and is cheap (reading, not solving). Recommended as F0 (the audit that
completes this list) before committing to derive any single one.

## DISCUSSION / DECISION ORDER (proposed, gated on Charles)
F0 systematic audit (cheap, completes the list) -> then pick: F1 (curvature action) and F2 (matter
action) are the deepest twins + logically prior to P5e; F3 (a(phi)) is the silent coupling. F4/F5/F6/F7/F8
discussed as they bear. Each item above is a TASK to be discussed before any derive/build.
