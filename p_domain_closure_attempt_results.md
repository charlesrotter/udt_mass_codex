# P_domain Closure Attempt Results

Status: working audit, not canonical.
Created: 2026-06-10.
Script: `native_source_share_boundary_identity_audit.py` (all numbers below
reproduce from it; script amended same-day per the adversarial verifier
before any commit).
Alters nothing existing; new files only.

## Purpose

Record a CLOSURE ATTEMPT on **P_domain** — the one remaining pre-spectrum
postulate (`negative_phi_native_geometry.md`, verdict 382) — and its honest
outcome. The attempt tried to (a) reduce the function-valued collar source
law `s(q)=q/3` to a single φ0 boundary identity ("supply = demand"), and
(b) add a second, action-independent route ("value-pinning", D3) to the
rejection of the `q₂=2/3` companion mode. Both headline claims were sent to
a blind adversarial verifier before banking.

## Outcome headline

**P_domain REMAINS OPEN.**

- The attempted new route (value-pinning D3) **FAILED adversarial
  verification**: the decomposition `f=(R/r)^p h` has gauge freedom in `p`
  — for any `B ≠ 0`, choosing `p* = ln f(r_in)/ln(R/r_in)` satisfies the
  two-end pinning `y=0` with `δ_h ≠ 0` while `q_φ0 = p* + δ_h` still
  carries the B-mode. D3 forces `B=0` only because `p` was frozen at `1/3`
  first, which presupposes either the finite-action filter (D3 collapses
  into D4) or an underived two-point Dirichlet datum (doc line 30128,
  section 424, stated only conditionally).
- The "supply = demand" framing turned out to be a **restatement** of
  existing doc content: sections 270/285-287 (verdicts 270/271), 375, 377,
  393, 397/verdict 382, including the general-N form
  `q(1−q)/2 = q/N ⇒ q = 1−2/N` (doc lines 29383, 29927).

## What the attempt DID produce (the surviving value)

- **(a) CHECK E** — first numerical demonstration that the
  pointwise/local share law `s_loc = (1/3)(1 − f(1−q))` cannot sustain
  `s = 1/9` along the collar: outward, finite-t blow-up at `t ≈ 4.148`;
  inward, `q → 1`, `s_loc → 0`. This upgrades banked verdicts 267/268 from
  "conditional" to "one specific running mechanism positively excluded".
- **(b)** The exact factorization `(local share) − q = (f−1)(q−1)`,
  showing the local share equals `q` only at `f=1` (on the physical
  branch `q ≠ 1`).
- **(c)** A single-file verified composition of the whole P_domain chain
  with a premise ledger (CHECK F) — useful as a dependency record, not as
  new derivation.
- **(d)** An independent re-derivation (sympy, 31/31 checks) of every
  link, confirming the doc's existing localization is correct.

## The corrected open-premise count

**Three** premises stand between the banked geometry and P_domain (not one,
as the attempt's first draft claimed):

1. **Source product rule `s(φ0) = q/3` from the UDT variational
   principle.** The no-go in `native_curvature_share_action_no_go.py`
   shows a local bulk scalar action cannot supply it; the needed object is
   derivative-dependent/boundary.
2. **Collar constancy / transport of `s`.** CHECK E shows it cannot come
   from the local geometry; it is a separate physical premise.
3. **Self-similarity `p = q`** vs the split-boundary-layer alternative
   (doc section 393 Alternative B).

## Verifier record

Blind adversarial verifier, 2026-06-10, agent `a6a4b911ef8e39af8`:

- All 31 sympy checks **independently confirmed**.
- Novelty claims (1)-(3) **REFUTED** as restatements, with exact
  section/line citations: sections 270 (lines 19297-19326), 285 (lines
  20475-20570, verdict 270 "endpoint/collar self-consistency"), 286
  (verdict 271), 375, 377, 393, 397/verdict 382, and the generalization
  `q(1−q)/2 = q/N ⇒ q = 1−2/N` (lines 29383, 29927).
- D3 independence **REFUTED** via gauge-freedom construction, with
  numerical counterexamples `B = +0.2 → p* = 0.4318` and
  `B = −0.1 → p* = 0.2705`, both satisfying two-end pinning with
  `δ_h ≠ 0`. The two-end pinning argument itself is prior art (doc
  sections 429 [lines 30584-30690], 430, 432); the script's original
  citation (lines 29996-30010) covers only the OUTER-end normalization —
  the inner-end statement is line 30128 and conditional.
- CHECK E **independently reproduced** (scipy RK45, rtol 1e-10, blow-up at
  `t = 4.1483`; the script's RK4 gives `t ≈ 4.1484`).
- **Five amendments required and implemented same-day** in the script:
  (1) CHECK C relabeled "independent re-derivation confirming sections
  270/285-287"; (2) the FINAL VERDICT reworded as a single-file
  composition of banked verdicts 178 + 267/268 + 270/271/272 + 382, not a
  gap-narrowing; (3) D3 withdrawn as an independent route and relabeled
  dependent, with the citation fixed and D5 stating the B-rejection rests
  on D4 alone; (4) CHECK E relabeled the genuinely new artifact; (5) the
  open-premise count corrected to three in CHECK F and the FINAL VERDICT.

## Lesson for future sessions

Attempted-closure write-ups must be verifier-checked for novelty against
the 31k-line doc BEFORE celebrating a narrowing. The doc's own
localization (verdicts 272/382) was already correct — and sharper than the
attempt's headline. The cheap failure mode here was not wrong algebra (all
31 checks were right) but re-deriving banked content and labeling it new,
plus promoting a gauge-dependent argument (D3) to an independent route.

## Relation to existing docs

This audit downgrades nothing in `negative_phi_native_geometry.md`; it
reconfirms that doc's localization of P_domain and adds one new exclusion
(CHECK E) in support of its verdicts 267/268. The derivation targets remain
the three premises listed above, with premise (1) — the boundary source
product rule from the variational principle — as the natural next gate.
