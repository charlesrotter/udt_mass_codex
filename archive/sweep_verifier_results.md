# SWEEP — Independent Hostile Verifier Pass (registry #39 / commit 87e7891)

Verifier: agent b3e91f7a2c8d4061 (INDEPENDENT, HOSTILE, blind). Date 2026-06-13.
Own machinery: from-scratch DOP853 outward integrator with EXACT mirror-parity
BC phi'(r_in)=0 (the challenger used -1e-7), own quadrature, own shooting fold
test, own linear-tail analysis. Did NOT re-run the challenger's scripts. Posture
per the charter's hypothesis discipline: aimed HARDEST at the prior-confirming
central claim (the Phi-ruler / one-universe reading). Log: /tmp/sweep_verify.log.

Prosecuting: sweep_results.md + sweep_*.py, headline claims 1-6.

---

## VERDICT TABLE

| Claim | Verdict |
|---|---|
| 1. One round-cell family in p; comp=1-e^{-2p}; r* shrinks/asymptotes; Gm/c^2 saturates ~0.503; Kretschmann at core | **CONFIRMED** (closed forms machine-exact) |
| 2. r* SLAVED to (p,Phi), not a free dial | **CONFIRMED** |
| 3. *** Phi sets an ABSOLUTE LENGTH => answers open thread "in the direction of bet (a), a real scale exists" *** | **DEMOTED** — the rescaling is real and exact, but the bet-(a) reading is an OVER-CLAIM. See below. |
| 4. Two-sided form/unform interval; deep edge a smooth seal (not 2nd fold) | **CONFIRMED** |
| 5. Every Legendre lobe l=1..4 relaxes to round at machine zero | **CONFIRMED** (re-asserted; consistent with #34 premise scope) |
| 6. Method: physical Dirichlet cell is a Bratu turning-point; outward-from-core is the robust traversal | **CONFIRMED** |

---

## CLAIM 3 — THE CORRECTED HONEST READING (the single most important output)

The dimensional rescaling is mathematically CORRECT and I confirm it to machine:
the substitution u = sqrt(Phi)*r maps a cell (p, r_in, Phi) onto a cell
(p, sqrt(Phi)*r_in, 1), so the EXACT identity

    r*(p, r_in, Phi) = r*(p, sqrt(Phi)*r_in, 1) / sqrt(Phi)

holds to dev ~1e-14 (tested at four independent (p,r_in,Phi) points). And the
small-core limit r*(r_in->0) -> 1.786187 at Phi=1 is r_in-independent to 6 digits.
So the bulk equation is genuinely NOT scale-INVARIANT — Phi (dim 1/length^2)
breaks the symmetry. That part is solid.

**But "not scale-invariant" is NOT "one universe is pinned," and the commit
conflates them. The kill-shot lands:**

- **(A-a) Phi is a FREE dimensionful INPUT, not determined by anything in this
  solve.** At fixed p=0.5 I swept Phi over 8 decades: r* runs 168.90 (Phi=1e-4)
  -> 2.07 (Phi=1) -> 1.008 (Phi=1e4). Dialing Phi is *exactly* dialing the
  absolute scale of the cell. "1/sqrt(Phi) is a ruler" is TRUE but VACUOUS for
  the one-vs-family question: ANY single free dimensionful constant sets a scale
  by dimensional analysis; that never selects a UNIQUE scale. This is a
  one-parameter scale-FAMILY indexed by Phi — bet (b) relabeled from r* to Phi,
  not bet (a). sweep_results.md (4) even concedes this in its own CAVEAT
  ("whether Phi is itself fixed... is the next determines-question... what sets
  its absolute value is the remaining open step") — yet the commit headline and
  section (8) say "in the direction of bet (a)." The headline contradicts the
  body's own caveat.

- **(A-b) Even at FIXED Phi, the configuration is NOT pinned.** A continuum in
  depth p survives (I verified every p in [0.05, 3.0] is a valid cell). So the
  whole-bulk solve leaves TWO unconstrained moduli: Phi (absolute scale) AND p
  (shape/compactness). Nothing here closes either.

- **(A-c) Correct determines-vs-relates verdict:** the whole bulk metric (as
  posed here) only RELATES r* to (p, Phi); it does NOT DETERMINE a unique
  (Phi, p). This is the SAME honest outcome already banked as registry #33
  ("the frame as currently closed RELATES X to E but does not pin it... X free").
  The sweep re-renders #33's continuum off the flow chart (good, CONFIRMED) but
  does NOT advance the determines question — it leaves it exactly where #33 left
  it. The "direction of bet (a)" claim is therefore unsupported by this work.

- **C2 table is itself misleading.** The challenger's C2 ("wall*sqrt(Phi) =
  const") does NOT hold with r_in fixed: I reproduce wall*sqrt(Phi) = 1.258,
  1.159, 1.071, 0.999, 0.945, 0.905 across Phi=0.25..8 — a 28% drift, not a
  constant. The clean 1/sqrt(Phi) law holds ONLY in the r_in->0 limit (where
  r_in drops out of u=sqrt(Phi)r). The exact content is the rescaling IDENTITY,
  not the approximate C2 wall table. Relatedly, "r*(Phi)=r*(1)/sqrt(Phi) EXACTLY"
  is only exact at r_in->0; at fixed r_in=1, r**sqrt(Phi) runs 1.76..8.84.

**Bottom line on the open thread: UNCHANGED. The metric carries a ruler-SHAPE
(it is not scale-invariant), but it does NOT carry a ruler-VALUE (Phi is free),
and it does NOT pin p. This is determines-vs-relates on the RELATES side — bet
(a) is NOT supported; the result is a (Phi, p) two-modulus family.**

---

## CLAIM 1/2 — CLOSED FORMS (CONFIRMED, my own integrator)

- comp = 1 - e^{-2p} EXACT (max|dev| = 0.0 to machine across p=0.05..5). phi_max
  sits at the core for every p (argmax@core), so compactness literally IS depth.
- r* asymptote: 1.685895 (p=20); vacuum edge: r* -> 2.20920 as p->0 (p=1e-5 gives
  2.209197). Both match the folded-in amendments (1.6859 / 2.2092).
- Misner-Sharp Gm/c^2: NOT exactly 1/2. It overshoots to ~0.509 near p=2 then
  settles to a LIMITING 0.50257 (p=10..20). The "~0.503 saturation" headline is
  accurate; "exactly 1/2" would be WRONG. It is a near-1/2 limiting gravitating
  mass, close to but not equal to the c^2=2GM/r* horizon value; the relation to
  the horizon condition is suggestive, not exact, and should be stated as ~0.503
  (NOT 1/2). r* is monotone-decreasing in p with no second fold (CONFIRMED).

## CLAIM 4/6 — INTERVAL + BRATU (CONFIRMED)

- Deep edge: integration fails past p~22 from genuine float overflow on
  phi''(core)=1-e^{3p} (~-1e29), exactly as the challenger states; the solution
  has already asymptoted by p~12 (r*, comp, ms all flat). Smooth seal limit,
  not a numerical second fold. CONFIRMED.
- Bratu turning point: at fixed r*=2.0, phi(r*) vs core depth D is NON-monotone
  (rises to +0.023 then falls through 0 to -0.13) — a genuine fold. This is why
  Dirichlet-Dirichlet Newton has a bad basin and why outward-from-core (no
  root-find) is the robust traversal. Method finding CONFIRMED.

## CLAIM 3/5 — IS THE ONE-ROUND CONTINUUM REAL OR AN ANSATZ WALL? (mostly real)

Charles's walling-off critique checked directly. The outward-from-core integration
stops at the FIRST phi=0 (event terminal) — so I integrated PAST r* to ask whether
the cut excludes genuine multi-cell / nodal solutions.

- The field DOES keep crossing zero past r* (every ~1.8 in r). BUT this is the
  LINEARIZED Bessel tail, not a chain of cells: near phi=0 the eq linearizes to
  phi'' + (2/r)phi' + 3*Phi*phi = 0, half-wavelength pi/sqrt(3*Phi)=1.814
  (observed 1.8, match), and the lobe amplitudes DECAY monotonically
  (0.115, 0.084, 0.054, 0.046, ...). So the higher zeros are the damped
  exterior/medium ripple BELOW phi=0, not equal-amplitude alternative cells.
  Picking the first zero as the matter-cell interface (phi=0, amplitude O(p)) is
  physically correct. The "one round type" is NOT an artificial wall on the
  fundamental branch — VERDICT: real, not an ansatz artifact.
- RESIDUAL SCOPE (record honestly): the sweep covers the NODELESS fundamental
  branch only. Genuinely nodal interior cells (phi with an interior node before
  r*, i.e. phi excursion both signs inside the cell) were not enumerated by the
  outward-from-core-with-phi'(r_in)=0 ansatz; the angular round-relaxation (5)
  is likewise the existing #34 premise (BULK dynamical sector, smooth seeds), not
  a new reach into the boundary/H1 sector. These are not refutations, but the
  "no bifurcation anywhere" reading should be scoped to the nodeless bulk branch.

---

## WHAT MUST BE REWORDED IN commit 87e7891 / registry #39 BEFORE PUSH

1. **DELETE the "answers the open one-universe-vs-scale-family thread in the
   direction of Charles's bet (a)" claim from the commit message, section (4)
   final paragraph, and section (8).** Replace with the honest reading: the bulk
   metric is NOT scale-invariant (Phi breaks the symmetry — a real ruler-SHAPE),
   but Phi is a FREE dimensionful input and p is a free modulus, so the solve
   RELATES r* to (p, Phi) and does NOT DETERMINE a unique configuration. The open
   thread is UNADVANCED; this is the RELATES side of determines-vs-relates, i.e.
   consistent with bet (b) / a (Phi, p) two-modulus family — same standing as
   registry #33. Bet (a) requires a CLOSURE that fixes Phi (and p); none is shown.
2. **Reword "the source Phi carries an ABSOLUTE RULER 1/sqrt(Phi)"** to "the bulk
   equation is not scale-invariant; Phi sets the rescaling u=sqrt(Phi)*r (exact),
   but its VALUE is unfixed — a ruler-shape, not a ruler-value." Drop/soften C2
   as an exact law (it drifts 28% at fixed r_in; the exact statement is the
   rescaling identity in the r_in->0 limit).
3. **State Gm/c^2 as ~0.503 (limiting), explicitly NOT 1/2**, and present the
   horizon-condition tie as suggestive, not derived.
4. **Scope claims 1/5** ("one round type, no bifurcation") to the NODELESS bulk
   branch (the higher zeros are the linear medium tail — verified — but nodal
   interior cells and the boundary/H1 sector are out of scope, per #33/#34
   premises).

The closed forms, the slaving, the Bratu method, the seal characterization, and
the continuum re-rendering of #33 are all SOUND and survive. The single thing
that must NOT be pushed is the "direction of bet (a)" / "absolute ruler answers
the open thread" over-claim — it conflates not-scale-invariant with one-universe.
