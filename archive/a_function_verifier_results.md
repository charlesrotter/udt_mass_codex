# BLIND ADVERSARIAL VERIFIER — a(phi) as a FUNCTION / eps-carrier departure claim

**Verifier:** Claude Opus 4.8 (1M), blind adversarial | **Date:** 2026-06-18
**Target:** `udt_a_function_both_extremes_results.md` (constructor, same date),
scripts `a_function_both_extremes.py`, `a_function_carrier_robustness.py`.
**Method:** independent sympy derivation of the Ricci scalar + eps(phi) for all
L_metric definitions BEFORE reading the constructor's doc/scripts. Then compared.
**Stance:** attack hardest the claim that confirms the hoped-for result (UDT
departs from GR). A clean refutation is the valuable outcome.

---

## 0. ONE-LINE VERDICT

> **PARTIAL — and the constructor's load-bearing self-caveat is itself WRONG (in the
> project's favor on existence, but for a reason that REOPENS the convention crux).**
> Independently: (i) the Ricci scalar is reproduced EXACTLY; (ii) eps(phi) RUNS as
> `eps0·e^{-phi}` (log-rate −1) — and it runs in the COORDINATE corner too, once units
> are kept consistent. The constructor's "corner B (coordinate-gradient) makes eps
> phi-INDEPENDENT / carrier vanishes" is a **units-mismatch artifact** (they compared a
> PROPER Compton length to a COORDINATE gradient interval). So **eps-running is more
> robust than the constructor claimed** — it does NOT die in any consistent corner.
> BUT: (iii) "eps runs" does **NOT** force "a departs." a = d(ln m)/dphi could be
> EXACTLY −1 for all phi even with eps running, unless one POSITS that the from-afar
> mass m couples to eps with nonzero strength. That coupling (f(eps)≠0) and its
> power-law SHAPE k·eps^p are **unforced ansatz**, not derived. **Existence-of-departure
> is NOT forced; only the EP anchor (a→−1 as eps→0) and — IF a departure exists — its
> e^{-pphi} DIRECTION are forced.** The departure claim is therefore real-as-a-possibility
> but **convention/ansatz-gated, not forced**: it survives the corner attack but falls to
> attack #2 (shape/existence posited).

---

## 1. INDEPENDENT RICCI SCALAR — REPRODUCED EXACTLY

My own Christoffel→Ricci→scalar computation (4D, metric
`ds^2=-e^{-2phi}c0^2dt^2+e^{2phi}dr^2+r^2dOmega^2`, phi=phi(r)) gives:

```
 R = (2/r^2) e^{-2phi} [ -2 r^2 phi'^2 + r^2 phi'' + 4 r phi' + (e^{2phi} - 1) ]
```

Identical to the constructor's §3 expression. The `(e^{2phi}-1)` subterm IS present:
isolated, it contributes `2(1 - e^{-2phi})/r^2`, which → 0 as phi→0 (flat) and runs
with phi. **Confirmed: the Ricci scalar and its phi-running curvature subterm are
correctly computed.** (Attack #3, partial — see §4.)

## 2. INDEPENDENT eps(phi) FOR ALL THREE L_metric — and the CRUX (attack #1)

Take `lambda_C` as the local PROPER Compton length `lam0 = hbar/m0c0` (Sense-1, fixed),
and let `g=|dphi/dr|` (coordinate gradient magnitude). Metric scales:
- proper 1-e-fold length: `L_proper = e^{phi}/g`  (since dl = e^{phi}dr)
- coordinate 1-e-fold interval: `L_coord = 1/g`
- curvature radius: `L_curv ~ r/sqrt(|1-e^{-2phi}|)` (dominant R-subterm)

**eps = lambda_C / L_metric, taken AS the constructor takes it (proper lam0 over each L):**

| corner | eps(phi) | d(ln eps)/dphi | runs? |
|---|---|---|---|
| A proper-grad | `g·lam0·e^{-phi}` | **−1** | YES |
| B coord-grad | `g·lam0` | **0** | NO (constructor's claim) |
| C curvature | `lam0·e^{-phi}√\|e^{2phi}−1\|/r` | phi-dependent | YES |

So at face value I reproduce the constructor's corner table EXACTLY, including the
"corner B vanishes." **But this is where the crux lives, and the constructor lost it.**

### 2a. THE DECISIVE FINDING — corner B is a UNITS-MISMATCH artifact, not a real corner

eps is a RATIO OF TWO LENGTHS. It is only meaningful if BOTH lengths are measured the
same way (both proper, or both coordinate). The constructor's corner B divides a
**proper** Compton length `lam0` by a **coordinate** interval `1/g`. That is
dimensionally illegitimate — it is not "the coordinate corner," it is "a proper length
over a coordinate length," a unit error masquerading as a physical choice.

Fix it consistently. The coordinate Compton length is `lam0·e^{-phi}` (proper/e^{phi},
since dl=e^{phi}dr). Then:

```
 consistent corner B:  eps = (lam0 e^{-phi}) / (1/g) = g·lam0·e^{-phi},  d(ln eps)/dphi = −1
 corner A (proper/proper): eps = lam0 / (e^{phi}/g) = g·lam0·e^{-phi},  d(ln eps)/dphi = −1
 => A and consistent-B are IDENTICAL.   (sympy-verified, exact)
```

**There is no carrier-vanishing corner.** Once units are consistent, the coordinate and
proper readings COINCIDE and BOTH run as `e^{-phi}` (log-rate −1). The "corner B kills
the carrier / E2 returns" caveat — the constructor's own headline "SHARP CAVEAT" and the
single thing they flagged as make-or-break — is **WRONG**. The E2-re-entry surface they
worried about does not exist.

### 2b. Forced-vs-convention judgment on the scale choice (the prompt's core question)

The prompt asks: is choosing proper/curvature over coordinate a FORCED physical fact or
an unforced convention that merely RELOCATES the old "which-c"/a-menu ambiguity?

**Answer: the scale choice is NOT a free convention here — and that HELPS the claim, not
hurts it.** The apparent freedom (proper vs coordinate giving different eps) was an
ILLUSION created by mixing units. A dimensionless ratio of two physical lengths is
coordinate-invariant; computed consistently, proper-grad and coord-grad give the SAME
eps. So the "menu of corners" the constructor presented (and worried was an unforced
choice) collapses to ONE answer: eps = (hbar g/m0c0)·e^{-phi}, log-rate −1. The
curvature corner C differs only because |R|^{-1/2} is a genuinely DIFFERENT geometric
scale (a curvature radius, not a gradient length) — a legitimately distinct, also-running
choice, not a unit artifact. **Verdict on attack #1: the eps-running is FORCED (not
convention-dependent); the coordinate reading does NOT collapse to GR once units are
consistent.** This is a refutation of the constructor's caveat in the project's favor.

**BUT** — and this is the trap — eps-running being forced is NOT the departure claim. See §3.

## 3. THE REAL BREAK — "eps runs" ≠ "a departs" (attack #2, load-bearing)

The departure of interest is in `a := d(ln m)/dphi`, m = the from-afar mass. The
constructor's chain is:  `a = −1 + f(eps)`, `f(0)=0` (EP), `f(eps)=k·eps^p`.

Independently audited, the logical status of each link:

- **f(0)=0 (EP anchor): FORCED** — as eps→0 (object Compton length ≪ metric scale, the
  terrestrial/macroscopic regime) there is no scale comparison, so a→−1. Confirmed
  independently (attack #4 ✓). [Caveat: eps(0)=eps0=g·lam0 is NOT identically zero; the
  anchor is "a→−1 in the eps≪1 regime," which is the macroscopic regime, not literally
  "phi=0." The constructor's §4 conflates "phi=0" with "eps→0"; the honest statement is
  eps≪1, which holds at phi=0 only for a macroscopic L. Minor, noted.]

- **f(eps)≠0 for eps>0 (the EXISTENCE of a departure): NOT FORCED.** Nothing derived
  requires the from-afar mass m to depend on eps at all. a could be EXACTLY −1 for all
  phi (f≡0, pure GR) WITH eps running — the GR reading is fully consistent with a running
  eps. The constructor SLID from "eps runs" to "a departs" without a derivation that m
  feels eps. This is the same class of move the myopia memo warns about (assuming the
  tractable/desired branch). **The existence of the departure is POSITED via the nonzero
  coupling k, not derived.**

- **Shape f=k·eps^p: UNFORCED ANSATZ.** f(eps)=0, k·eps, k·eps^2, k·ln(1+eps),
  k(1−e^{−eps}) all satisfy f(0)=0. "Minimal analytic" is an aesthetic choice, not a
  physical constraint. The sign of k is also free (only k>0 amplifies into the core).
  The constructor flags this honestly in L7/§6 — credit given — but the headline and
  one-line bottom line still assert the departure "DOES produce" / "is VISIBLE," which
  overstates a posited coupling as a derived one.

- **Direction e^{-pphi} (asymmetry core-amplifies/cosmic-decays): FORCED CONDITIONALLY.**
  IF a departure exists and IF f is a positive power of a `e^{-phi}`-running eps, THEN the
  direction is fixed by sign(phi). Independently confirmed. But this is "forced GIVEN the
  unforced premises," so it is downstream of the existence gap.

**Net on attack #2: existence-of-departure is NOT forced once eps runs. The constructor
assumed it. Only the EP anchor and the conditional direction are forced.** This is the
real refutation surface, and it is NOT the one the constructor defended (they defended
the corner robustness, which actually survives; they did not defend the existence gap,
which does not).

## 4. RICCI/GRAVITY-SECTOR LEAD (attack #3)

The `(e^{2phi}-1)` term in R is real (§1). The constructor's §3-C/§8 lead — that the
curvature-corner running of a(phi) is "the same nonlinearity" as the gravity-sector
`e^{2phi}` self-term the relativistic-foundation flag suspects — is **structurally
suggestive but NOT established.** The curvature corner C running comes from `|R|^{-1/2}`
carrying `(e^{2phi}-1)`; this is a real, computed phi-dependence. Whether it "is one
nonlinearity" with the matter-side a(phi) is a coincidence-of-appearing-`e^{2phi}` vs a
genuine shared mechanism — the doc does NOT derive a link, only notes both contain
`e^{2phi}`. Correctly flagged by the constructor as "a lead, not a result." I concur:
**lead only; not load-bearing; do not bank.** Many UDT quantities carry `e^{2phi}` (it is
just g_rr); co-appearance is weak evidence.

## 5. MYOPIC-ERROR RE-AUDIT (attack #5)

- **E1 (constant-collapse):** AVOIDED. a is a function throughout; no constant relayed as
  the answer. ✓
- **E2 (single-log-rate / eps phi-independent):** The constructor BELIEVED corner B
  re-introduced E2 and flagged it as the residual. Independently, **corner B does NOT
  re-introduce E2** (units artifact, §2a) — so E2 is even less of a threat than they
  thought. The carrier is robust. ✓ (constructor over-worried here)
- **E3 (single extreme):** AVOIDED. Both extremes + middle addressed. ✓
- **NEW hidden myopia I found:** a DIFFERENT slice-collapse — collapsing "eps runs"
  (forced) onto "a departs" (posited). This is a fresh instance of the same family
  (assume the desired branch follows). The constructor caught the OLD three errors but
  introduced this fourth conflation. **Is `eps0^p e^{-pphi}` a hidden linearization?** —
  No; it is a chosen ansatz, not a truncation of something richer (there is no "fuller f"
  being Taylor-cut). But it IS an unforced SELECTION among admissible f, which is the
  ansatz-smuggle, not the linearization-smuggle.

---

## 6. ANSWERS TO THE PROMPT'S THREE DELIVERABLES

**(a) Independent eps(phi) for all three L_metric** (units kept consistent):
- proper-gradient: `eps = (hbar g/m0c0) e^{-phi}`, log-rate −1 (RUNS)
- coordinate-gradient (consistent units): `eps = (hbar g/m0c0) e^{-phi}`, log-rate −1
  (RUNS — IDENTICAL to proper; the constructor's "0" is a unit error)
- curvature |R|^{-1/2}: `eps = (lam0/r) e^{-phi}√|e^{2phi}−1|`, log-rate phi-dependent
  (RUNS, differently)

**(b) Forced-vs-convention on the scale choice:** eps-running is **FORCED**, not a
convention. The coordinate reading does NOT collapse to GR once units are consistent; it
coincides with the proper reading. The "which-c"/a-menu ambiguity is NOT relocated here —
it is resolved (for the gradient scales) by dimensional consistency. The constructor's own
make-or-break caveat is refuted in the project's favor.

**(c) Is existence-of-departure forced once eps runs?** **NO.** a = d(ln m)/dphi can be
≡ −1 with eps running. The departure requires the additional, UNDERIVED premise that the
from-afar mass couples to eps (k≠0). That premise — and the power-law shape — is posited.

---

## 7. FINAL VERDICT

**PARTIAL.**

FORCED / CONFIRMED:
- The Ricci scalar and its `(e^{2phi}-1)` running subterm (exact).
- eps(phi) RUNS as `e^{-phi}` (log-rate −1) — and **more robustly than claimed**: it does
  NOT vanish in the coordinate corner (that was a units artifact). The scale choice is
  NOT an unforced convention; gradient corners coincide. (Refutes the constructor's
  headline caveat, in the project's favor.)
- The EP anchor a→−1 in the eps≪1 (macroscopic) regime is forced.
- IF a departure exists, its e^{-pphi} core-amplify/cosmic-decay DIRECTION is forced.

NOT FORCED / REFUTED-as-forced:
- **The EXISTENCE of the departure (a≠−1 somewhere) is NOT forced by eps running.** It is
  POSITED via the coupling k≠0. "eps runs ⟹ a departs" is a conflation; the GR reading
  (a≡−1, f≡0) is fully consistent with the running eps.
- The SHAPE f=k·eps^p is an unforced ansatz (constructor flags this honestly).
- The onset phi and magnitude k are object-gated (constructor's claim — agreed).

**Bottom line for the load-bearing "UDT departs from GR" claim:** The departure is now a
well-posed, internally-consistent POSSIBILITY with a forced EP anchor and a forced
direction-IF-it-exists, sitting on a robustly-running control parameter eps. But the
EXISTENCE of the departure remains POSITED, not derived — the project has not yet shown
that the from-afar mass MUST feel the scale ratio. The prior "leans GR" terminus is NOT
fully dissolved: GR (a≡−1) survives as an admissible reading even with eps running. What
HAS genuinely advanced: the convention-ambiguity (which corner) that defeated prior passes
is RESOLVED by dimensional consistency (a real gain the constructor missed), and the open
question is correctly relocated — but relocated to "does m couple to eps at all (k≠0)?"
(a physical-coupling existence question), NOT merely to "where is the onset?" as the
constructor frames it.

**Recommendation:** Do NOT bank "a(phi) departs" as derived. Bank: (i) eps runs, forced,
corner-robust (CORRECT the constructor's vanishing-corner caveat — it is a unit error);
(ii) EP anchor forced; (iii) existence-of-departure = POSITED (k≠0), the next thing to
derive natively from the matter action, NOT assumed. The constructor defended the wrong
flank: the corner robustness is fine; the existence-of-coupling is the gap.
