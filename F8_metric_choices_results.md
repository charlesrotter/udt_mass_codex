# F8 CLOSURE RECORD — Choice-Provenance of the "Derived" Metric Form

**Mode:** OBSERVE, DATA-BLIND, READ-ONLY on committed docs (this is the only new file).
Bounded analytic, CPU sympy/mpmath class. **No mass / ratio / wall number used anywhere.**
**Constructor:** Claude Opus 4.8 (1M), 2026-06-21. Verifier-before-record: an ATTACK HERE
block is provided; a blind adversarial pass is required before this is treated as banked.

**Purpose (Charles's "finish everything" directive):** tie off F8 — the embedded choices in the
C-2026-06-18-1 "derived" metric form — to a CLEAN state. Characterize EACH embedded choice as
DERIVED-from-the-relativistic-principle vs CHOSEN (a free solution-space DOF), record which
CHOSEN items are already RELAXED vs UNRELAXED, and state the honest residual.

**Sources read (committed, read-only):**
- `relativistic_metric_rederivation_results.md` (the C-18-1 derivation: R1/R2/R3 -> form; Parts 1-3 + premise ledger P1-P11 + blind verifier verdict)
- `CANON.md` C-2026-06-18-1 (the "four INDEPENDENT CHOICES not consequences" note) + C-2026-06-10-1 (areal reading / rho=r)
- `native_positional_dilation_distance_readings.py` (the rho=r theorem — conditional structure)
- `native_dilation_weight_derivation_results.md` (P7' the orbit-area premise)
- `P5e_proper_results.md` (the full off-diagonal + time-live solve — what it relaxed; what stayed spherical)
- `FOUNDATIONAL_ASSUMPTIONS_LEDGER.md` (scoreboard + F8 entry)

---

## 1. THE DERIVED-vs-CHOSEN TABLE (every embedded choice in the metric form)

The C-18-1 metric form, fully written:
`ds^2 = - e^{-2 phi} c^2 dt^2 + e^{+2 phi} dr^2 + r^2 dOmega^2`, with `g_tt g_rr = -c^2`.

| # | Embedded choice | DERIVED / CHOSEN | Precise reason | Premise tag |
|---|---|---|---|---|
| 1 | **Exponential dilation law** `g_tt = -e^{-2phi}c^2` (R1+R2) | **DERIVED** | Unique positive solution of the multiplicative Cauchy/composition FE `g(x)g(y)=g(x+y)` under regularity. R1 (depends on phi-DIFFERENCES only) + R2 (composes) + P4 (g continuous/monotone/>0, physically mandatory for a clock rate) FORCE the exponential. Verifier STRENGTHENED: R1 + differentiability alone gives it (R2 automatic). The value k=-1 is pure CONVENTION (the definition phi:=-(1/2)ln(-g_tt/c^2)); no physics. | P5 (derived), P6 (convention), P4 (named-assumed regularity) |
| 2 | **Reciprocal tie** `B=1/A`, i.e. `g_tt g_rr = -c^2` (R3) | **DERIVED (conditionally, slot-modulo)** | Forced by R3 mutual reciprocity (time factor x length factor = 1) GIVEN the exponential law, SOURCE-FREE / KINEMATIC — no stress tensor, no action, no field equation, no asymptotic flatness. NOT GR's `(AB)'=0`-from-matter (that is DOWNSTREAM consistency, auto-satisfied). The inverse-vs-equal reading is essentially forced once exp-law + phi->-phi "swap = neither preferred" is accepted (e^{-x}=1/e^{x}). **The one genuine load is the SLOT (item 7).** | P9 (derived from P5+P7+P8) |
| 3 | **STATIC** (d_t phi = 0) | **CHOSEN** | R1-R3 are instantaneous/local kinematic statements, SILENT on d/dt. Non-stationary phi is explicitly allowed (verifier confirmed, axis C). A free solution-space DOF. | P10 (choice) |
| 4 | **SPHERICAL symmetry** | **CHOSEN** | R1-R3 say NOTHING about the angular/transverse block. `r^2 dOmega^2` is a CHOICE; an ellipsoidal/sheared/off-round transverse 2-metric on constant-phi surfaces is equally allowed. Reciprocity transverse to grad phi is VACUOUS (zero phi-difference => identity, tie=1), so it cannot constrain the angular block. A free solution-space DOF. | P10 (choice) |
| 5 | **DIAGONAL** (no off-diagonal/shift) | **CHOSEN** | R1-R3 do not exclude off-diagonal g_{0i}, g_{ij} (rotation / frame-dragging / shear) not along grad phi. A free solution-space DOF. | P10 (choice) |
| 6 | **AREAL-r chart** (rho = r) | **CHOSEN-chart, made THEOREM-conditional** | See §1a below. R1-R3 leave the radial gauge (areal vs isotropic vs proper) FREE — pure chart choice at the bare-form layer. BUT once the AREAL READING is canonized (C-10-1) and B=1/A is imposed in that chart, `rho = r` is FORCED (R-AREAL THEOREM, up to a shift constant). So rho=r is "chosen-then-promoted-to-theorem-by-a-prior-canon-choice," not free-floating and not independently postulated. | P10 (choice) -> conditional theorem |
| 7 | **Slot-id P8** (direction conjugate-to-time under reciprocity = grad phi, i.e. radial) | **CHOSEN (the irreducible analog choice)** | The one genuine non-trivial choice underneath item 2. R3 ties g_tt to ONE conjugate length dilation; that it is the phi-GRADIENT direction (radial), not a transverse one, is the physically obvious but UNFORCED analog identification. No circularity (P8 assumes the pairing, B=1/A follows; it does not assume B=1/A). If revised (g_tt tied to a transverse component), the tie CHANGES. | P8 (named-assumed) |
| 8 | **P7'** (the constant-depth shift acts at fixed invariant orbit-area) | **CHOSEN, physically justified** | Used in the native-weight derivation: the SO(3)-orbit area is the invariant label that does not rescale under phi->phi+const while the (t,r) block does. Physically the right choice (the statement "orbit-sphere area is invariant under the depth shift" IS chart-independent — verifier confirmed in a phi-mixing chart), but a PREMISE, not a consequence. The "angular sector is special" obstruction survives on it. | P7' (chose, physically justified) |

### 1a. The rho=r reconciliation (CANON says theorem — is it forced or a chart choice?)

Both, in a clean two-layer sense — there is NO contradiction:

- **At the BARE-FORM layer (C-18-1):** the chart (areal vs isotropic vs proper radial gauge) is
  GENUINELY FREE — R1-R3 are silent on it. So at this layer rho=r is a CHOICE.
- **At the AREAL-READING layer (C-10-1, canonized prior):** the R-AREAL THEOREM
  (`native_positional_dilation_distance_readings.py`, exact sympy) states
  `[B=1/A holds in the areal chart] <=> rho(r) = ±r + const in any B=1/A chart`. So ONCE the
  areal reading is the canonized reading AND B=1/A is imposed, rho=r is FORCED (no longer an
  independent postulate; the shift constant r0's only physical content is a finite-area inner
  sphere/puncture if extended to r->0, else a pure relabel).
- **The honest framing:** rho=r is a *theorem conditional on a prior CHOICE of reading*. The
  "areal reading" itself (C-10-1) was fixed by MACRO DATA (d_L=r(1+z), D_M=r, Misner-Sharp;
  Pantheon+/DESI), not derived from R1-R3. So rho=r is forced by the geometry GIVEN the areal
  reading; the areal reading is the load-bearing (data-anchored) choice, not rho=r itself.
- Cross-check: the OTHER readings are NOT free coincidences — R-PROPER imposed with B=1/A is
  DEGENERATE (forces g_tt=-1, phi==0, no dilation at all), so it is incompatible; R-COORDINATE
  leaves rho free and is then INCOMPLETE (owes a statement of what r measures). The areal reading
  is the unique non-degenerate, data-consistent one. This SHARPENS the choice but does not make it
  derived-from-R1-R3.

**Net on item 6:** tag = CHOSEN-chart whose downstream value (rho=r) is THEOREM-FORCED by a prior
data-anchored reading-choice. Visible, clean, not a smuggle — but NOT principle-derived.

---

## 2. EACH CHOSEN ITEM: free-DOF-we-explore vs potential-smuggle; RELAXED vs UNRELAXED

| Choice | Free-DOF-we-explore vs potential-smuggle | RELAXED? | Where relaxed / status |
|---|---|---|---|
| **STATIC** (#3) | FREE DOF we explore (the time-live frontier; the phi-angular hunch lives in the nonstationary sector, C-13-1) | **RELAXED** | P5e_proper: genuine multi-harmonic, free-omega, finite-amplitude TIME-LIVE solve; STEP2 + STEP3 earlier. Time turned ON. Result: SOFTENS (box-control survives). |
| **DIAGONAL** (#5) | FREE DOF we explore (off-diagonal/shift = rotation/frame-dragging channel) | **RELAXED** | P1 wired the off-diagonals; P5e_proper has the LIVE off-diagonal time row g_tr=H (0 statically=gauge, sourced dynamically maxH 0.004->0.061). The channel STEP-2 gauged away is ON. Result: ACTIVE but box-control survives. |
| **SPHERICAL** (#4) | FREE DOF we explore (the off-round / non-spherical sector — Charles's hunch home for angular structure) | **UNRELAXED on the DERIVED operator** (see §3) | The everything-on build (pre-derivation, EH-operator era) explored OFF-ROUND and found box-control (incl. 3-cell persistence). But the C-18-1 DERIVED-operator solves this session (matter_regrade, STEP2, P5e_proper) were ALL SPHERICAL (fields = f(t,r), r-only spatial). **This is the scoped residual.** |
| **AREAL chart** (#6) | FREE DOF (chart), value pinned by C-10-1 reading -> rho=r theorem | **UNRELAXED, but LOW-RISK** | A chart choice; downstream binary verdicts (C=0 vs C>0) are gauge-invariant (Lemma 2). Changing the chart relabels, does not add physics (verifier: gauge-invariant). Not a structure-hiding suspect. |
| **Slot-id P8** (#7) | Potential SMUGGLE in PRINCIPLE (the one genuine analog choice under B=1/A) — but LOW physical risk: the gradient direction is the only one where reciprocity is non-vacuous | **NOT relaxed (and arguably should not be)** | Named, scope-void-if-revised. Not a numerics DOF — it is a definitional analog choice. The transverse alternative is VACUOUS, so the radial slot is essentially forced. Keep VISIBLE; not a solver knob. |
| **P7'** (#8) | Physically justified premise, not a numerics DOF; the invariance statement is chart-independent | **NOT relaxed (premise)** | Named [CHOSE, physically justified]. The "angular sector is special" obstruction rests on it. Keep VISIBLE; revisit only if the orbit-area invariance is challenged. |

**Summary of relaxed/unrelaxed:**
- **RELAXED already:** STATIC (P5e/STEP2), DIAGONAL/off-diagonal (P1/P5e). Both turned ON; both
  preserved the box-control / continuum verdict.
- **UNRELAXED:** SPHERICAL symmetry **on the derived operator** (the live residual), the AREAL
  chart (low-risk gauge), and the two definitional premises P8/P7' (not solver DOF).

---

## 3. THE HONEST QUESTION: does any UNRELAXED choice hide structure the solves missed?

**The one live residual: NON-SPHERICAL on the DERIVED operator is UNTESTED.**

- SPHERICAL is the only unrelaxed choice that is a genuine *physical* solution-space DOF (the
  others are a gauge and two definitional premises). It is therefore the only one that could hide
  structure.
- The phi-angular discreteness hunch (Charles's standing prime suspect) lives EXACTLY in the
  angular/non-spherical sector — so this residual is the most physically-loaded one to be honest about.
- **What we DO have (leans box-control):** the pre-derivation everything-on build explored the
  OFF-ROUND / non-spherical sector and found box-control, verified including a 3-cell high-mode
  persistence test (memory [[everything-on-solver-build]]; off-round box-controlled). That work
  leans strongly toward "non-spherical does not rescue a discrete spectrum either."
- **What we do NOT have (the gap):** that off-round work was on the ASSUMED-EH operator era. The
  C-18-1 DERIVED operator (vacuum != GR, e^{2phi} weight) solves THIS session — matter_regrade,
  STEP2_timelive, P5e_proper — were ALL SPHERICAL (metric fields = functions of (t,r) only, no
  theta-dependence wired into the metric). The off-round sector has NOT been re-run on the derived
  operator.
- **Honest statement (scoped residual):** *Non-spherical structure on the DERIVED operator is
  UNTESTED.* The verdict is supported by (a) the analytic fact that reciprocity is vacuous
  transverse to grad phi (so R1-R3 add no angular constraint either way), and (b) the prior
  off-round box-control on the EH operator — but it is an INHERITANCE, not a re-derivation. Per the
  SOLVER-FIRST discipline, "have we explored the solution space with EVERYTHING ON, or only a
  corner" is answered HONESTLY: time ON (yes), off-diagonal ON (yes), **non-spherical ON the
  derived operator (NO)**. This is a corner left for the off-round-on-derived-operator solve.
- **Why this does NOT reopen the central verdict (calibration):** the central "must-quantize" /
  continuum conclusion already survived the deepest import (the F1 derived operator) on the
  fully-coupled P5e-proper machinery in the SPHERICAL sector, AND survived off-round on the EH
  operator. For non-spherical-on-derived to OVERTURN it, the derived operator would have to do in
  the angular sector something the EH operator did not — possible in principle (the e^{2phi} weight
  is exactly what the native-weight derivation found CANNOT wash out transverse curvature — the
  angular obstruction), so this residual is not idle. It is the right next off-round target IF a
  mismatch ever points there, but it is NOT load-bearing on the current verdict (the scoreboard
  already grades F8 PARTIAL and lists "spherical still a working choice").

**F8 closure verdict:** F8 is CLEAN-and-VISIBLE, not derived-away. Of the eight embedded choices,
TWO are DERIVED (exponential law; reciprocal tie, slot-modulo), SIX are CHOSEN. Of the six CHOSEN,
TWO physical DOF are already RELAXED (static, off-diagonal) with the verdict surviving; ONE chart
choice (areal/rho=r) is gauge-low-risk and theorem-pinned by a prior reading; TWO are definitional
premises (P8, P7') kept visible; and ONE — SPHERICAL symmetry on the DERIVED operator — is the
single genuine UNRELAXED physical residual, leaning box-control on prior (EH-operator) off-round
evidence but UNTESTED on the derived operator. F8 moves PARTIAL -> CLEAN-WITH-ONE-NAMED-RESIDUAL.

---

## PREMISE LEDGER (this record)

| # | Premise | Status |
|---|---|---|
| L1 | C-18-1 derivation is correct as banked (R1/R2/R3 -> form; P1-P11 ledger; blind-verified STANDS-CONDITIONALLY) | INHERITED (banked canon + verifier) |
| L2 | The R-AREAL THEOREM (`rho=r <=> B=1/A in areal chart`) is exact | INHERITED (sympy-exact, banked C-10-1) |
| L3 | The areal READING itself (C-10-1) was fixed by MACRO DATA, not derived from R1-R3 | INHERITED (CANON provenance note) — load-bearing for the rho=r "theorem" framing |
| L4 | P5e_proper relaxed STATIC + DIAGONAL but stayed SPHERICAL (fields = f(t,r)) | OBSERVED (read P5e_proper §P-0/§3-5: 5 fields A,B,H,phi,Theta = f(t,r)) |
| L5 | The off-round box-control evidence is from the PRE-DERIVATION EH-operator everything-on build, not the derived operator | INHERITED (memory [[everything-on-solver-build]]); this is the residual's exact scope |
| L6 | Reciprocity transverse to grad phi is vacuous (so R1-R3 add no angular constraint) | INHERITED (verifier axis C, banked) — the analytic leg of "spherical is a free choice" |
| L7 | No mass / ratio / wall number used; DATA-BLIND | THIS RECORD (provenance classification only) |

**This record DERIVES nothing new** — it CLASSIFIES the provenance of already-banked choices and
NAMES the one untested residual. It is a make-visible deliverable, not a derive.

---

## ATTACK HERE (for the blind adversarial verifier)

1. **DERIVED/CHOSEN tags (items 1-8):** Is any item mis-tagged? Hardest: is the reciprocal tie
   (item 2) genuinely DERIVED, or does the slot-id P8 (item 7) make it effectively CHOSEN? Confirm
   the two-layer split (tie derived GIVEN the slot; slot chosen) is honest and matches the C-18-1
   verifier verdict (axis B: "B=1/A forced by R3-as-read-by-P7/P8, not by relativity in the abstract").
2. **rho=r reconciliation (§1a):** Is "theorem conditional on a prior data-anchored reading-choice"
   the right reading of the R-AREAL THEOREM? Attack: is rho=r actually FORCED by R1-R3 (making it
   DERIVED, not CHOSEN)? Verify it is NOT — that R1-R3 leave the chart free and the areal reading is
   the added (C-10-1, data-fixed) input. Check the R-PROPER degeneracy and R-COORDINATE
   incompleteness claims against the .py.
3. **RELAXED claims (§2):** Verify STATIC and DIAGONAL are GENUINELY relaxed on the DERIVED operator
   (read P5e_proper: time-live free-omega ON; off-diagonal g_tr=H LIVE). Confirm the box-control
   verdict survived BOTH relaxations (not a stalled solve — the #60 static gate PASSED to the digit).
4. **The residual (§3) — the load-bearing claim:** Verify that the derived-operator solves this
   session (matter_regrade, STEP2, P5e_proper) were ALL SPHERICAL (fields = f(t,r), no theta in the
   metric). Verify the off-round box-control evidence is PRE-DERIVATION (EH-operator). If EITHER is
   wrong — if a non-spherical derived-operator solve exists, or if the off-round work was on the
   derived operator — the residual is mis-stated. This is where an over-claim ("we tested it") or an
   under-claim ("totally unexplored") would hide.
5. **Calibration:** Does naming the spherical residual OVERSTATE the threat to the central verdict?
   Confirm the record correctly says it does NOT reopen "must-quantize" (already survived F1-derived
   operator spherically + off-round on EH) while honestly flagging the e^{2phi} angular obstruction
   as the reason the residual is "not idle." Check neither dramatized nor dismissed.
6. **Smuggle audit:** Did this record silently DERIVE anything (it must only CLASSIFY)? Did it import
   any value? Confirm DATA-BLIND.

---

## THE SINGLE CLEANEST STATEMENT

> The C-18-1 metric form has EIGHT embedded choices. TWO are DERIVED from "remain relativistic":
> the exponential dilation law (R1+R2, clean) and the reciprocal tie B=1/A (R3, source-free,
> modulo the one analog slot-choice). SIX are CHOSEN: static, spherical, diagonal, the areal
> chart, the slot-id P8, and P7'. Static and diagonal are already RELAXED on the derived operator
> (P5e-proper: time and the off-diagonal row LIVE) and the continuum/box-control verdict SURVIVED
> both. The areal chart is a low-risk gauge whose rho=r consequence is theorem-pinned by the prior
> data-anchored areal reading. P8 and P7' are visible definitional premises, not solver knobs. The
> ONE genuine unrelaxed physical residual is NON-SPHERICAL structure ON THE DERIVED OPERATOR —
> untested this session (the prior off-round box-control was on the assumed-EH operator), leaning
> box-control but honestly the corner the derived-operator solves did not enter. F8 is therefore
> CLEAN-AND-VISIBLE with one named residual, not a smuggle.
---

## VERIFICATION (2026-06-21) — blind over-closure pass, agent a45d3c75a8520bba9
VERDICT: CLEAN — honest tie-off, open residuals kept visible, no over-closure.
Specific: derived-vs-chosen table honest (rho=r = theorem conditional on a DATA-ANCHORED areal reading, not
cleanly principle-derived; P8 honestly CHOSEN). The non-spherical-on-the-derived-operator residual is genuinely
OPEN (P5e_proper ansatz confirmed spherical: fields f(t,r), fixed r^2 dOmega^2; the off-round box-control lean is
INHERITED from pre-derivation EH work, not re-derived) — left visible, and soundly argued not to reopen
must-quantize (which survived spherically on the derived op + off-round on EH).
