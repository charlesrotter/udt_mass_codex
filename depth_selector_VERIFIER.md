# BLIND ADVERSARIAL VERIFIER — Depth-Selector Breather (`depth_selector_breather_results.md`)

**Verifier agent:** claude-opus-4-8[1m] (blind adversarial). **Date:** 2026-06-19.
**Mandate:** try to BREAK the claim, not confirm it. DATA-BLIND (no lepton/mass/ratio/wall
numbers loaded). No git commit.
**Method:** independent re-derivation. I wrote my own scripts and did NOT trust the
constructor's numbers:
- `depth_selector_verif_confine.py` — brute confinement sweep + fake-well/smuggling audit
- `depth_selector_verif_well.py` — characterize interior minima
- `depth_selector_verif_analytic.py` — EXACT slope-crossing threshold (sympy + high-res)
- `depth_selector_verif_truewell.py` — true-double-well window resolution
- `depth_selector_verif_window.py` — quantize the in-window well + provenance
- `depth_selector_verif_box_and_tower.py` — box-control audit + max-tower scan
- `depth_selector_verif_ladder.py` — mass-ladder assignment robustness

**THE CLAIM UNDER ATTACK:** "U(D)=c_grav(e^{2D}-1)+(1/2)A0^2 omega^2(D) is MONOTONE RISING
(a half-well, no interior minimum below D*), construction-robust; quantization gives only
box-controlled levels; mass_n=cost(D_n) is sub-exponential and capped; the depth-selector
does NOT close."

---

## VERDICT: **STANDS-WITH-CORRECTIONS**

The central PHYSICAL conclusion — **the breather depth-selector does NOT close** (no native
multi-rung exponential tower; what tower-like structure exists is box-controlled; the mass
ladder is sub-exponential and capped at cost(D*)) — **STANDS**, and on the mass-ladder and
box-control attacks it stands cleanly and robustly.

BUT the constructor's **stated reason is materially WRONG**, and one headline sub-claim is
**FALSE as written**: U(D) is **NOT** "monotone-rising, construction-robust." A **genuine
interior double-well with omega^2>0 (NOT tachyonic, NOT fake) DOES exist** for legitimate
parameter choices the constructor never scanned. The non-closure is real, but it is because
that well is **SHALLOW (holds ~1 bound depth level)**, not because the well is **absent**.
The doc reaches the right verdict through a demonstrably incorrect intermediate claim — a
classic "fixed a value to make it solvable, then declared the slice's result the frame's
result" error (CLAUDE.md "How we work" failure (b)).

---

## THE SINGLE MOST DANGEROUS ATTACK I FOUND (the correction)

**The "monotone-rising, construction-robust" claim is an artifact of fixing c_grav=1 and
scanning only A0^2 in {1,5,20,100}.** Confinement depends only on the dimensionless ratio
**R := A0^2/c_grav** (the carrier weight vs gravity). The constructor's grid never left
R<=100. The interior-well **threshold is R≈136** for the constructor's own (floor=2, D*=2.6,
k=4); above it a TRUE interior local minimum appears.

`depth_selector_verif_truewell.py` (high-res, sympy slope g(D)=2e^{2D}-(1/2)R·cb·k·D^{k-1}):

```
 R=A0^2/c_grav   interior structure (floor=2, D*=2.6, k=4)
   100           monotone (no interior stationary point)           <- constructor's regime
   136           TRUE double-well: Umax@0.99, Umin@1.52, omega2(min)=1.77  <- MISSED
   150           TRUE double-well: Umin@1.92, omega2(min)=1.41
   170           TRUE double-well: Umin@2.155, omega2(min)=1.055         <- omega2>0 by a margin
   200           TRUE double-well: Umin@2.39,  omega2(min)=0.56
   250+          local max & min merge; global min jumps to the cap D* (omega2->0)
```

The well at R=170 is unambiguously real (verif_window): a local MAX at D=0.99 (a left
carrier barrier, height 9.46) and a local MIN at D=2.155 with **omega2=1.055>0 throughout**
(no tachyon), a right exponential wall (height 17.06). `c_grav` is tagged in the doc's own
premise ledger as "CHOSE (unit; cancels in ratios)" — so choosing R in [136,230] is exactly
as legitimate as the constructor's R<=100. **The doc's "construction-robust monotone"
(its Part 8, four constructions) is robust only because all four were run at c_grav=1,
A0^2<=100 — i.e. all in the sub-threshold corner. It is a slice, not the whole frame.**

This well is NOT a smuggled fake (Attack 2): omega^2>0 throughout the well; the left wall is
the carrier's own energy at small D ((1/2)A0^2·floor, real positive energy), not omega^2<0.
The constructor's claim that "the only thing that could have produced an interior minimum is
omega^2<0" is **false** — a real omega^2>0 interior min exists.

---

## WHY THE NON-CLOSURE VERDICT NEVERTHELESS SURVIVES (the deeper ground)

The well exists — but it cannot TOWER. `depth_selector_verif_box_and_tower.py` +
`verif_window.py`:

1. **The true interior well (omega^2>0, clear of D*) is SHALLOW: it holds ~1 bound depth
   level.** At R=170 the interior barrier is 9.46 and exactly **one** level sits below it.
   This is the SAME "1 stable level, then nothing" obstruction the radial carrier hit
   (quantized_carrier doc Finding 2) — now on the depth axis.

2. **The level IS well-intrinsic, not box-controlled** (anti-box PASS): extending the outer
   box from D*=2.6 to 4.5 leaves the trapped level fixed (167.93 -> 167.6, stable). So I
   confirm the well, when it exists, is genuine and intrinsic — but it holds one state.

3. **The only ways to "pack more levels" are illegitimate:** (i) press R high so the min
   rides the cap (omega^2->0, the right wall becomes the tachyon cap itself — the relocated
   #44 trap the doc correctly names); or (ii) crank the depth-mode mass m_D — and the level
   count then scales **linearly with m_D** (22->44->88->178 for m_D=1,4,16,64), which is
   textbook **box-control**, not a native tower. My max-tower scan over the FULL legitimate
   space (floor in {2,6,12}, D* in [2.4,3.4], k in [3.5,4.9], all R) found "22 levels" only
   at omega2_min=0.024 (cap-pinned) with m_D-linear scaling — i.e. a box, not a native tower.

**So: a genuine confining well exists, but it is single-level; no native multi-rung
exponential tower emerges anywhere in the legitimate ranges. The depth-selector does NOT
close — confirmed, but for a corrected reason.**

---

## ATTACK-BY-ATTACK

**1. CONFINEMENT — constructor claim PARTIALLY FALSIFIED, verdict survives.**
U(D) is NOT monotone-rising/construction-robust. A true interior double-well (omega^2>0)
exists for R=A0^2/c_grav in a finite window (~136–230 at floor=2,D*=2.6,k=4; finite
threshold for EVERY legitimate (floor,D*,k) — verif_analytic table). The tachyon cap
max(omega^2,0) is correct (a tachyon is not a standing wave — agreed), and it is NOT what
kills the well: even WITHOUT the cap, no min forms at R<=100, and WITH the cap a real min
forms at R>=136. The constructor's "well requires omega^2<0" reasoning is wrong.

**2. SMUGGLING / FAKE-WELL — no fake well; but the constructor SUPPRESSED a real well.**
No omega^2<0 fake well was smuggled (good). The "no left wall" sub-claim is correct in the
monotone regime (carrier D-slope ~ D^{k-1}->0 as D->0, no 1/D^2 barrier). BUT the constructor
**over-truncated the frame** by not scanning c_grav/large-R: a real left barrier (the
carrier energy (1/2)A0^2·floor at D=0) appears above threshold. So the error is an
ARTIFICIAL SUPPRESSION of a real well by under-scanning, the mirror image of the smuggling
it guarded against.

**3. BOX-CONTROL — STANDS (independently reproduced).**
In the monotone regime (R=5) my from-scratch eigensolve reproduces the box law: #levels
grows with D* and sqrt(m_D); spacing ~1/m_D (D*=2.0/2.6/3.2, m_D=1/4/16 -> 5/10/21,
13/27/54, 31/63/127). Box-control diagnosis is correct. And in the well regime, any
multi-level "tower" is ALSO m_D-box-controlled (linear in m_D). Correct that box-control =
not native.

**4. MASS LADDER — STANDS (assignment-robust).**
Independently: under BOTH physically meaningful D_n assignments (eigenfunction peak and
mean <D>), ratios DECREASE monotonically (peak: 3.59->1.32; mean: 1.83->1.16) and the
ladder is capped at cost(D*)=180.3. No reasonable assignment yields constant (exponential)
ratios. Sub-exponential + capped CONFIRMED, assignment-robust.

**5. PROVENANCE — NATIVE-FLAVORED with two flagged modeling shortcuts (under-flagged in doc).**
- E_grav(D)=c_grav(e^{2D}-1): native-to-metric B1, GR-form flag carried (consistent).
- omega^2(D)=floor-c_bind D^k: native carrier form from the quantized_carrier doc.
- back-reaction A^2(D)=2c_grav(e^{2D}-1)/omega^2(D): the doc calls this "DERIVED (native
  MS/Hamiltonian constraint)." I find it is a **MODEL** of the constraint, not the
  constraint: it (i) equates the WHOLE enclosed MS mass to the carrier energy (no other
  source) and (ii) uses the QUADRATIC/harmonic carrier energy (1/2)A^2 omega^2 — a
  small-amplitude (linearized) energy, at finite breather amplitude A. Principle-2 caution.
  The doc tags it "DERIVED" too strongly; it is native-flavored modeling, not the pointwise
  coupled G=kT solve (which the doc DOES flag as the load-bearing SHORTCUT — so the residual
  is acknowledged, just mis-tagged in the ledger row).

**6. OVER/UNDER-CLAIM.**
- **OVER-CLAIM (material):** "U(D) monotone-rising, construction-robust; no interior minimum;
  the only thing that could make a min is omega^2<0." FALSE — a real omega^2>0 interior well
  exists above an R-threshold the scan never reached.
- **Correct net verdict, under-justified:** "depth-selector does not close." TRUE, but the
  honest reason is "the true well is single-level / can't tower," not "no well exists."
- No over-claim on box-control or the capped sub-exponential ladder (both stand).

---

## WHAT THE DOC SHOULD SAY (corrected verdict)

U(D) is native (B1 cost + native carrier freq + native-flavored back-reaction model). It is
**NOT monotone in general**: for carrier-to-gravity ratio R=A0^2/c_grav above a finite
threshold (~136 at the baseline params) a **genuine interior confining well with omega^2>0**
forms (the constructor missed it by fixing c_grav=1, A0^2<=100). **However that well is
SHALLOW — it traps ~1 bound depth level (well-intrinsic, box-control PASS) — so it does not
produce a native multi-rung exponential tower.** Pushing for more levels either drives the
min onto the tachyon cap (omega^2->0, the relocated #44 box trap) or relies on the depth-mode
mass m_D (box-control, level count linear in m_D). The mass ladder mass_n=cost(D_n) is
sub-exponential (decreasing ratios, assignment-robust) and capped at cost(D*). **NET: the
breather depth-selector does NOT close — confirmed, but because the well is single-level, not
because U(D) fails to confine.** This is the SAME "1 stable level then nothing" obstruction
as the radial carrier, now on the depth axis.

---

## DISCIPLINE CHECKS
- DATA-BLIND: PASS (no wall/lepton/ratio numbers loaded; pure structural form test).
- Independent re-derivation: PASS (own sympy slope analysis + own numpy eigvalsh eigensolve;
  constructor's torch tridiagonal NOT trusted; results cross-checked at high resolution).
- Anti-numerology: PASS (no rational promoted; all counts/ratios are shape diagnostics).
- No git commit (per mandate).

## BANKED (for NEGATIVES_REGISTRY / the results doc)
The depth-selector NON-CLOSURE STANDS with a corrected premise set: **the obstruction is
"the native interior depth-well is single-level (shallow), not absent."** Premises carried:
modeled profile forms (E_grav~e^{2D}, omega^2~floor-D^k); back-reaction = native-flavored
MS-constraint MODEL with quadratic carrier energy; fully-coupled time-live solve NOT built
(the one place a qualitatively different/deeper well could appear). If a future coupled solve
makes the interior well DEEP (multi-level, omega^2>0, m_D-independent), this negative is
CONDITIONS-CHANGED and must be re-graded.
