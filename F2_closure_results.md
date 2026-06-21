# F2 — CLOSURE RECORD (the matter action L2+L4): tie-off to a CLEAN state

**Mode:** OBSERVE, METRIC-LED, DATA-BLIND. Closing FOUNDATIONAL_ASSUMPTIONS_LEDGER item F2 per
Charles's "finish everything" directive. No mass / ratio / spectrum / wall number loaded, consulted,
or derived. **Driver:** Claude (Opus 4.8, 1M context), 2026-06-21. **Compute:** CPU only, bounded
sympy (`/tmp/f2_closure_so3.py`, uncommitted). NO heavy solve. **Status:** UNVERIFIED (no blind
verifier pass yet) — record-candidate, not banked. NOT canon.

**Closes:** F2 = RESOLVED-but-with-residuals. This record (a) re-states the verdict crisply,
(b) parks the {X^2, L6} ambiguity as a CLOSED-as-scoped value-open residual, (c) examines the ONE
load-bearing assumption (full-SO(3) target — derived or assumed?), and (d) confirms the new derived
operator (vacuum!=GR, a=e^{phi}) does not move the F2 term-classification.

**Sources read (READ-ONLY):** `F2_matter_action_forcedness_results.md` (+ its appended VERIFICATION,
agent a4aa12aa522f06b6c), `matter_regrade_derived_operator_results.md` (+ VERIFICATION),
`MATTER_SECTOR_MAP_new_foundation.md`, `FOUNDATIONAL_ASSUMPTIONS_LEDGER.md` (scoreboard + F2 entry),
`CANON.md` (C-2026-06-14-1 + its refinement; C-2026-06-18-1).

---

## 1. THE F2 VERDICT, RE-STATED CRISPLY (the tie-off)

> **{L2, L4} is MINIMAL-BUT-NOT-UNIQUE.** It is the cleanest, most-native minimal stabilized native
> matter action — but it is NOT the unique admissible action. F2 resolves as
> *assembled-from-a-principled-but-non-unique-basis*, with one term genuinely FORBIDDEN, two genuinely
> admissible-but-omitted, and a single load-bearing premise (full-SO(3) target) on which the
> forbidding rests.

Component statements (each verifier-checkable; all blind-verified in the source doc except the
SO(3)-provenance examination in Sec 3, which is NEW here):

1. **Core {L2, L4} is NATIVE + NECESSARY.**
   - **L2** = `(xi/2) g^{ab} D_a n . D_b n` is the **UNIQUE** 2-derivative diffeo + target-isometry
     scalar (angular_lagrangian D3, blind-verified). FORCED present.
   - A **4-derivative stabilizer is FORCED PRESENT** by Derrick (`{L2}` alone collapses to L=0,
     banked #43); some higher-than-2-derivative term is necessary.
   - **L4** = `(kappa/4)|omega_H1|^2 ~ l1*l2` is the area-form-native member of the 4-deriv space
     (the metric-norm of UDT's OWN H1 winding current; blind-verified native, not an imported Skyrme
     coefficient).

2. **The 4-derivative STRAIN-INVARIANT space is EXACTLY 2-dimensional** on the S^2 target:
   `span{ X^2 = (l1+l2)^2 , |omega_H1|^2 = l1*l2 }`. Re-confirmed this push (sympy): the symmetric
   strain `S_munu = D_mu n . D_nu n` has rank <= 2 on a 2-dim target, so its algebraic degree-2
   invariants are spanned by the two power-sum combinations; the "other" usual Skyrme invariant
   `tr(S^2) = l1^2+l2^2 = X^2 - 2|omega_H1|^2` lies in that span (no third). **L4 is the
   Jacobian/antisymmetric combination `l1*l2` (the area-form pullback); X^2 is the orthogonal
   symmetric `(l1+l2)^2` (NOT an area-form pullback).**
   - **SCOPE TAG (verifier B1, binding):** "exactly 2-dim / no third" is **STRAIN-ALGEBRAIC** — it
     counts invariants built algebraically from the FIRST-derivative strain (the standard Skyrme
     basis). 4-derivative scalars involving SECOND derivatives (e.g. `(box n)^2`, `(D^2 n)·(D^2 n)`)
     are **non-strain-algebraic** and lie OUTSIDE this count. Read "the 4-deriv space is 2-dim" as
     *the strain class*, not literally all 4-derivative scalars. (Scope, not a refutation; flagged so
     it is not re-attempted as if it covered every 4-deriv operator.)

3. **Admissible extras (survive every forcing principle, but OMITTED from {L2,L4}):**
   - **X^2** = `(l1+l2)^2` (squared-L2-density): admissible by diffeo+SO(3) invariance, but **NOT
     area-form-native** (fails provenance test (c)). Moves the **MASS SPECTRUM**, NOT the EOS / B=1/A
     (it is purely-angular on the hedgehog, preserves `T^t_t = T^r_r`). Its omission is a CHOICE
     (cleanest-native), not a derivation.
   - **L6** = area-current-squared (`B_mu B^mu`, the topological-current norm): admissible AND
     area-form-native, just **subleading** (6-derivative). Its omission is "leading-order truncation"
     — a legitimate, explicit modeling choice.

4. **FORBIDDEN: a bulk potential V(n)** — killed by the **full target SO(3)** (the same isometry that
   makes L2 unique). A full-SO(3)-invariant function of a unit vector is necessarily CONSTANT
   (transitive action; only invariant is `n.n=1`); a non-trivial V requires a preferred target axis,
   i.e. SO(3) -> SO(2). This is the audit's strongest forcing result and a **CORRECTION to the
   corpus** (the CANON scope line had listed V(n) as a "robust-to" admissible addition; under full
   SO(3) it is forbidden in the bulk). Re-confirmed this push (sympy/transitivity).

5. **Scale (depth-shift) symmetry is NEUTRAL** on angular-term selection: under `phi -> phi + lambda`
   the angular metric block is invariant, so EVERY purely-angular term (V, L2, L4, L6) is
   scale-invariant. The new dilatation tool does NOT select {L2,L4} and does NOT forbid any angular
   term. Its content is structural: it marks the **angular sector as scale-neutral** and the **time /
   radial gradient channels as the breakers** (weights +-2, +-4, ...). (verifier B3, SUPPORTED.)

**Net survivor table (unchanged from the source doc, re-stated):**

| term | (a) scale | (b) SO(3)+diffeo | (c) area-form | (d) Derrick | NET |
|---|---|---|---|---|---|
| **L2** | invariant | **unique 2-deriv** | (n/a) | needs partner | **FORCED present** |
| **L4** | invariant | pass | **native (selected)** | qualifies as stabilizer | **present + natively privileged** |
| **X^2** | invariant | pass | NOT native | qualifies as stabilizer | **admissible (non-native), VALUE-OPEN** |
| **L6** | invariant | pass | native (current^2) | allowed, not required | **admissible (native, subleading), VALUE-OPEN** |
| **V(n)** | invariant | **FORBIDDEN (full SO(3))** | compatible | shrinks alone | **KILLED** (unless SO(3)->SO(2)) |

---

## 2. THE {X^2, L6} AMBIGUITY — parked as a BOUNDED, VALUE-OPEN, CLOSED-AS-SCOPED residual

This is the only genuinely-open content inside F2 (besides the SO(3) premise, Sec 3). It is closed
**as-scoped**, not left hanging:

**WHAT IT IS.** Two terms — `X^2` (the second 4-derivative invariant, admissible-but-not-area-form-
native) and `L6` (native, subleading) — survive every forcing principle and are OMITTED from the
minimal {L2,L4}. Their coefficients are free.

**WHAT IT AFFECTS — and, crucially, WHAT IT DOES NOT.**
- **Affects:** the soliton PROFILE and hence the **MASS SPECTRUM** (a different 4-/6-derivative
  contraction reshapes the body).
- **Does NOT affect:** the **EOS / B=1/A / box-control verdict.** Both X^2 and L6 are
  **purely-angular on the hedgehog**, so (by the angular_lagrangian verifier strengthening) they
  preserve `T^t_t = T^r_r` and change only `T^theta_theta` / the solid-angle-deficit value. So they do
  NOT break the angular B=1/A source, and — confirmed downstream in STEP2_timelive — the time-live
  box-control was tested **ACTION-ROBUST across the {L4, X^2} ambiguity** (w^2 ~ 1/R^2 either way).

**THEREFORE it touches NO current physics conclusion.** Every banked verdict that F2 feeds —
B=1/A-sourced-by-the-angular-sector (C-2026-06-14-1), the box-control / classical-continuum
"must-quantize" headline, the soliton EOS — is INDEPENDENT of the {X^2, L6} coefficients. The
ambiguity lives entirely on the (data-blind, not-yet-computed) SPECTRUM axis.

**SCOPED-CLOSED STATEMENT (the tie-off):**
> The {X^2, L6} coefficients are **parked VALUE-OPEN** (Charles's directive). This is a BOUNDED
> residual: it moves the mass spectrum only, never the EOS / B=1/A / box-control, so it does not
> disturb any current physics conclusion. It is the **matter-side analogue of the gravity-side free
> kinetic ratio X** (the value-open coupling in the derived gravity operator): a real, named,
> coefficient-level freedom that is honestly carried, not a flaw to be hunted. It becomes live only
> when (and if) Charles opens the SPECTRUM — at which point it is a finite, enumerated 2-parameter
> family `{X^2, L6}` on top of the necessary core, NOT an open-ended "what other terms?" question.

So the ambiguity is a CLOSED-as-scoped residual (bounded, enumerated, spectrum-only, parked
value-open), not a hanging thread.

---

## 3. THE LOAD-BEARING ASSUMPTION — is the carrier target genuinely FULL SO(3)? [the one place F2 could still move]

The verifier flagged this explicitly: **the whole verdict — both L2's uniqueness AND V-forbidden —
rests on the carrier's target symmetry being FULL SO(3).** If the target symmetry is REDUCED (e.g. to
SO(2) about an axis), a non-trivial potential `V(n) = f(n.a)` re-enters, L2 is no longer the unique
2-derivative scalar, and the survivor table changes. This is the one place F2's verdict could move.
So: **is full-SO(3) DERIVED or ASSUMED, and does anything in UDT's structure reduce it?**

### 3.1 What "full SO(3)" means here — and the key distinction

The carrier is the unit 3-vector field `n_a`, target S^2, with SO(3) acting on the target (the
internal index a). "Full SO(3)" = the ACTION (the Lagrangian density's term-selection rules) is
invariant under arbitrary rotations of the target sphere — NO preferred internal direction. The
critical distinction is between:
- **(i) the symmetry of the ACTION / term-selection** (what makes L2 unique and V forbidden), versus
- **(ii) the symmetry of a particular SOLUTION** (the hedgehog `n = x/r`).

The hedgehog solution is NOT SO(3)-invariant by itself — it correlates the internal frame with the
spatial frame (it is invariant only under the DIAGONAL "grand spin" SO(3) of simultaneous
space+internal rotation). **But that is a property of the chosen CONFIGURATION, not of the action.**
The forbidding of V(n) is a statement about which TERMS the action may contain — it depends on (i),
the term-selection symmetry, NOT on (ii). A spontaneously-hedgehog solution of a fully-SO(3)-symmetric
action does not introduce a V(n) term; it just picks an orientation. So **the hedgehog axis does NOT
reduce the action's target symmetry** — this is the standard soliton situation (the action keeps full
internal symmetry; the soliton breaks it spontaneously, costing no potential term).

### 3.2 Does ANYTHING in UDT's structure reduce the action's target symmetry below full SO(3)?

Examined the three candidate axis-breakers UDT actually carries:

1. **The hedgehog / deg-1 map axis** — **NO (spontaneous, not a term).** As above: `n = x/r` breaks
   SO(3) -> diagonal-SO(3) at the SOLUTION level only. The ACTION retains full target SO(3); no V(n)
   term is licensed. (sympy/transitivity: the term-selection ring is still generated by `n.n=1`.)

2. **The seal / eta = 1/18 boundary object** — **NO bulk reduction; it is a BOUNDARY object.** CANON
   (refinement to C-2026-06-14-1) is explicit: *"eta=1/18 is a seal/boundary object, NOT a bulk
   potential."* The seal lives on the mirror-fold boundary (the involution surface), not in the bulk
   Lagrangian density. A boundary object can carry its own reduced symmetry without reducing the BULK
   action's target SO(3) — the bulk term-selection (where V would live) is untouched. **Promoting eta
   from a boundary object to a bulk axis-breaking potential would itself be a NEW POSIT** — and the
   source doc already flags exactly this ("eta is canonically a BOUNDARY object... promoting it to a
   bulk potential would itself be a posit to flag"). So eta as-canonized does NOT reduce the target
   symmetry; only a (flagged, not-taken) re-posit would.

3. **The eta / charge axis in the target (q=1/3, N=3)** — **NO.** N=3 and q=1/3 are read dial-free off
   the area form `omega_H1 = eps_abc n_a dn_b ^ dn_c`. The Levi-Civita `eps_abc` is the fully-SO(3)-
   INVARIANT tensor (it is what makes the eps-singlet unique iff N=3). It privileges no axis; it is the
   volume form on the target, invariant under the full group. So the very objects carrying the counts
   are full-SO(3) structures — they REINFORCE full SO(3), they do not break it.

### 3.3 Is full-SO(3) DERIVED or ASSUMED?

**Honest grade: INHERITED-from-the-carrier-definition, not independently re-derived in F2 — but it is
the SAME assumption L2's uniqueness already rests on, and it is structurally REINFORCED by UDT's own
objects.** Specifically:
- It is **DERIVED-at-the-carrier-level** in the sense that the carrier was settled as the unit
  3-vector / S^2 with the eps_abc area form (CANON C-2026-06-14-1; the S^2 object-identity
  blind-verified). The natural isometry group of that target, acting on the action, IS full SO(3) — a
  reduced symmetry would require an ADDITIONAL structure (a preferred internal direction) that the
  carrier as-defined does NOT contain.
- It is **ASSUMED in the sense that no separate UDT principle FORCES "no preferred internal axis"** —
  it is the absence of an extra posit, not the presence of a derivation. (The premise tag C-F2-b in
  the source doc is honest: "full target SO(3) is the native symmetry... CHOSE/inherited; if the
  carrier's native symmetry is actually reduced, V re-enters.")

**RESOLUTION (the tie-off for item 3):**
> Full target SO(3) is the symmetry of the carrier AS CANONIZED (unit 3-vector, S^2, eps_abc area
> form); it is the SAME assumption L2's uniqueness already uses, so F2 imports no NEW load here. The
> three UDT structures that COULD reduce it — the hedgehog axis, the seal/eta, the charge counts — do
> NOT reduce the BULK action's target symmetry: the hedgehog breaks it only SPONTANEOUSLY (solution,
> not term), the seal/eta is a BOUNDARY object (CANON-explicit, not a bulk potential), and eps_abc /
> N=3 / q=1/3 are themselves full-SO(3)-INVARIANT objects that reinforce it. The ONLY way V(n)
> re-enters is a deliberate, separately-flagged NEW POSIT promoting the seal/eta to a bulk
> axis-breaking potential — which is not on the table and would be caught as a posit. **So F2's
> verdict is STABLE: full SO(3) holds unless a future explicit posit reduces it, and nothing in the
> current structure does.** This is the resolution, not merely a re-flag: the candidate reducers are
> named and each is shown not to bite.

(One open honesty note, kept VISIBLE: if a FUTURE derivation were to show the carrier's native
symmetry is genuinely reduced — e.g. the open S^2-vs-S^3 reconciliation, or a seal that imprints a
bulk axis — V(n) re-enters and the survivor table changes. That is a CONDITIONS-CHANGED hook on F2,
not a current gap; it is parked, not hidden.)

---

## 4. THE NEW OPERATOR (vacuum!=GR, a=e^{phi}) does NOT change the F2 term-classification [confirmed, with reason]

The matter sector was re-graded on the newly-derived gravity operator (`matter_regrade_derived_
operator_results.md`, blind-verified): vacuum != GR (scalar-tensor `E_munu = f G + (g box - nn)f -
Xf(...)`, `f = e^{2phi}`), and the rest-mass coupling DERIVED a(phi) = e^{+phi} (not the old a=-1).
**Does this move F2's term-classification (the basis {L2,L4,X^2,L6,V}, the uniqueness, the
forbidding)? NO — and the reason is structural, not coincidental:**

**The F2 term-classification is a TARGET-GEOMETRY + COVARIANCE question, which is OPERATOR-AGNOSTIC.**
What selects the admissible matter terms is:
- **diffeo invariance** (build scalars from `D_mu n` contracted with `g^{mn}` and `sqrt(-g)`), and
- **target-isometry (SO(3)/S^2) invariance** (which functions of `n` and its strain are allowed).

Neither of these references the GRAVITY action / curvature operator. The basis enumeration (the
4-deriv space = 2-dim, X^2 vs L4 provenance, V forbidden under SO(3)) is **PRE-GRAVITY**: it is fixed
the moment the carrier (unit 3-vector, S^2, eps_abc) and the spacetime covariance rules are fixed. The
`matter_regrade` doc's own CARRY-OVER list confirms exactly this — **L2 native-ness, L4 native-ness,
the omega_H1 charge / N=3 / q=1/3 / eta, and the S^2 carrier all CARRY OVER UNCHANGED** ("covariance /
uniqueness / topology, not curvature-form"), explicitly because they are operator-independent.

What the new operator DOES change is **how the matter terms COUPLE and BACK-REACT** (a(phi)=e^{phi} is
now PHYSICAL/non-absorbable; the exterior gains scalar hair {m,q}; B=1/A breaks once hair is live;
mass numbers need re-run). Those are DYNAMICAL / quantitative consequences — they live downstream of
the term-classification, on the SPECTRUM/solve axis (the same axis the {X^2,L6} ambiguity lives on).
They do not re-open which terms are admissible, unique, or forbidden.

**One consistency check on the SO(3) premise under the new operator:** the new operator introduces the
scalar field phi as an independent dynamical player coupling to matter via `a(phi)=e^{phi}`. Does that
coupling imprint a preferred TARGET (internal) direction and thereby reduce SO(3)? **No** — phi is a
spacetime scalar (a depth field), with no internal/target index; it couples to the SO(3)-invariant
matter density (an `n.n`-type scalar), so it cannot select a target axis. The depth coupling breaks
SCALE symmetry (matter = the scale-breaker, with teeth) but is silent on the INTERNAL SO(3). So the
operator change leaves the Sec 3 SO(3) resolution intact as well.

> **(4) verdict:** the F2 term-classification, uniqueness, and V-forbidding are TARGET-geometry +
> covariance facts — operator-agnostic — so the derived vacuum!=GR / a=e^{phi} operator does NOT
> change them. It changes the matter terms' DYNAMICS (coupling, back-reaction, exterior, spectrum),
> which is downstream and already on the value-open / needs-a-solve axis. F2 is closed independently
> of the operator derivation.

---

## 5. WHAT REMAINS GENUINELY OPEN IN F2 (the honest residual list)

After this closure, F2's open content is FINITE, BOUNDED, and PARKED — nothing blocks current physics:

| # | residual | status |
|---|---|---|
| R-a | **{X^2, L6} coefficients** | **VALUE-OPEN, CLOSED-as-scoped** (Sec 2): spectrum-only, parked per Charles; matter-side analogue of gravity-side free-X; bounded 2-param family, not open-ended. Does NOT touch EOS/B=1/A/box-control. |
| R-b | **Full-SO(3) target as inherited-not-independently-derived** | **RESOLVED-as-scoped** (Sec 3): same assumption as L2-uniqueness; no UDT structure currently reduces it (hedgehog=spontaneous, seal/eta=boundary, eps_abc=invariant); V re-enters ONLY via a future flagged posit or a reduced-carrier re-derivation -> a CONDITIONS-CHANGED hook, not a current gap. |
| R-c | **Strain-algebraic SCOPE of the "2-dim 4-deriv space"** | **SCOPED** (Sec 1.2, verifier B1): true for strain-algebraic invariants; 2nd-derivative scalars (e.g. (box n)^2) are a separate class outside the count. Recorded so "no third 4-deriv term" is not over-read. |
| R-d | **The coupling VALUES xi, kappa (hence l=sqrt(kappa/xi))** | **OUT OF F2 SCOPE / parked elsewhere** — this is the scale-VALUE provenance crux (MATTER_SECTOR_MAP Sec 2), the F2-scale-half / F7 bridge, value-open. F2 (term-FORM) is separate from and prior to the coupling-VALUE question. |

**Nothing in this list blocks a current physics conclusion.** F2 (the FORM of the matter action) is
RESOLVED: necessary core {L2,L4}, two enumerated admissible extras parked value-open, one forbidden
term V(n) under a stable full-SO(3) premise, operator-agnostic. The clean "unique" was not available
and was not manufactured; the honest "minimal-but-not-unique" is tied off.

---

## 6. PREMISE LEDGER (chose / derived — for this closure record)

| # | premise / claim | status |
|---|---|---|
| K1 | {L2,L4} minimal-but-not-unique (necessary core + extras {X^2,L6} + V forbidden) | DERIVED upstream + blind-verified (F2 source doc) |
| K2 | 4-deriv strain space EXACTLY 2-dim {X^2, l1*l2}; tr(S^2)=X^2-2*L4 in span | DERIVED (re-confirmed sympy this push) |
| K3 | V(n) const under full SO(3) (transitive on S^2; only invariant n.n=1) | DERIVED (re-confirmed sympy this push) |
| K4 | {X^2,L6} move SPECTRUM only, not EOS/B=1/A/box-control (purely-angular, preserve T^t_t=T^r_r) | DERIVED upstream (angular_lagrangian verifier + STEP2 action-robustness) |
| K5 | hedgehog axis = SPONTANEOUS (solution), does NOT reduce the ACTION's target SO(3) | DERIVED (standard soliton fact; sympy term-ring still generated by n.n) — NEW this push |
| K6 | seal/eta = BOUNDARY object, NOT a bulk potential; does not reduce bulk SO(3) | DERIVED-from-CANON (refinement to C-2026-06-14-1, explicit) — NEW examination this push |
| K7 | eps_abc / N=3 / q=1/3 are full-SO(3)-INVARIANT objects (reinforce, not reduce) | DERIVED (eps is the invariant volume form) — NEW this push |
| K8 | full-SO(3) = inherited-from-carrier (= L2-uniqueness assumption), not independently forced | CHOSE/inherited (honest grade) — the C-F2-b premise, resolved-as-scoped not removed |
| K9 | F2 term-classification is operator-agnostic (target-geometry+covariance, pre-gravity) | DERIVED (matter_regrade carry-over list confirms) — restated this push |
| K10 | phi-coupling (a=e^{phi}) is a spacetime scalar, no target index => cannot reduce internal SO(3) | DERIVED (this push) — closes the operator-vs-SO(3) cross-check |

---

## 7. ATTACK HERE (for a blind verifier)

1. **The SO(3) examination (the load-bearing one, NEW here, Sec 3).** Confirm the action-symmetry vs
   solution-symmetry distinction: that the hedgehog `n=x/r` breaks SO(3) SPONTANEOUSLY (it is a
   configuration invariant only under diagonal grand-spin SO(3)) and does NOT license a V(n) TERM in a
   fully-SO(3)-symmetric action. Then attack the three reducers: is the seal/eta GENUINELY a boundary
   object (CANON) and not secretly a bulk axis? Could the open S^2-vs-S^3 reconciliation, or any other
   committed UDT structure, imprint a PREFERRED INTERNAL direction in the BULK action? If any does,
   V(n) re-enters and F2 moves — this is the single place to break the closure.

2. **The operator-agnostic claim (Sec 4).** Confirm the F2 basis/uniqueness/forbidding genuinely does
   NOT reference the curvature operator — that it is fixed by diffeo + target-isometry alone. Check the
   cross-claim that the phi-coupling (a=e^{phi}), being a spacetime scalar with no target index, cannot
   reduce the internal SO(3). A counterexample (a derived matter coupling that DID carry a target
   index) would break this.

3. **The {X^2,L6} EOS-robustness (Sec 2).** Re-confirm X^2 and L6 are purely-angular on the hedgehog
   and therefore preserve `T^t_t=T^r_r` (so they cannot break B=1/A or move box-control) — i.e. the
   ambiguity is genuinely spectrum-only. Spot-check against the STEP2_timelive action-robustness claim.

4. **The 2-dim count + scope tag (Sec 1.2).** Re-derive `tr(S^2) = X^2 - 2|omega_H1|^2` (the third
   "usual" invariant is in the span). Confirm the strain-algebraic SCOPE tag is correctly stated: that
   2nd-derivative 4-deriv scalars (e.g. (box n)^2) are a DIFFERENT class outside the 2-dim count, so
   "no third" is strain-class, not all-4-deriv.

5. **Calibration.** Judge whether "RESOLVED-with-bounded-value-open-residuals" over-claims. The
   honest bar: F2 should be closed iff nothing in its residual list blocks a current physics
   conclusion AND the one verdict-moving premise (SO(3)) is either derived or shown
   stable-under-current-structure. Confirm or push back.
---

## VERIFICATION (2026-06-21) — blind over-closure pass, agent a45d3c75a8520bba9
VERDICT: CLEAN — honest tie-off, open residuals kept visible, no over-closure.
Specific: the full-SO(3) STABLE verdict survives the hardest attack — hedgehog breaking is spontaneous (config,
not an action term); eta/seal is canonically a BOUNDARY object (CANON 172-173), not a bulk axis-breaker;
phi (a=e^phi) is a spacetime scalar with no target index so cannot reduce internal SO(3). Honestly graded
INHERITED-not-independently-derived with the V-re-entry escape hatch (reduced carrier / S2-vs-S3) kept visible.
{X^2,L6} value-open scoping accurate (spectrum-only, EOS/box-control untouched).
