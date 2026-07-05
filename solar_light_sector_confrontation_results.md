# Solar light-sector confrontation — FROZEN UDT predictions vs published solar-system data

**Status: BANKED — BLIND-VERIFIED (verifier adb471c72a1f5b552, 2026-07-05: OVERALL HOLDS, no corrections;
all 7 points PASS, false-pass hunt clean). Every σ-margin (Cassini 0.913σ, VLBI 0.667σ), the μas/ps
estimates (deflection 4.38 μas, Shapiro 49 ps/leg), the self-consistency (1.751″), and the fractional
sizes independently reproduced to full precision. Both frozen predictions quoted VERBATIM from the
banked derivation docs — NO parameter fitted, NO branch selected after the data load (s=0 pre-registered).
Verdict correctly ACCEPT/BOUND, correctly labeled consistency-not-discrimination, correctly makes no
claim on s (CF-CAT). The Cassini value (2.1±2.3)×10⁻⁵ confirmed canonical (Bertotti+ 2003); a
search-engine hallucination of a different value was caught + dismissed by the verifier.**

**★ THIS DOCUMENT LOADS OBSERVATIONAL DATA.** Unlike the two frozen, data-blind predictions it
confronts (`one_body_null_deflection_results.md`, `one_body_shapiro_delay_results.md` — both banked,
blind-verified, grep-clean of any data number), THIS doc is the AUTHORIZED, gated DATA STEP: it loads
published solar-system constraints and compares them ONLY against the already-frozen UDT formulas.
Loading Cassini/VLBI numbers here is CORRECT (this is the confrontation, not a derivation). **NO
retuning, NO branch adjustment, NO new derivation** is performed or permitted (attested in §7). Per
the pre-registered no-retuning rule (`J_of_s_light_deflection_confrontation_MAP.md` §6) the only allowed
verdicts are ACCEPT / REJECT / BOUND against the frozen forms.

CONFRONTATION NODE (armchair/arithmetic): loads published constants + evaluates the frozen formulas at
solar values. No PDE solve, no CAS re-derivation of the predictions. Only the clean **s=0** case is
confronted (s≠0 rides the conical/scale ambiguity CF-ABS and is NOT confrontable — MAP §0(i)). Per the
banked CF-CAT finding: the solar tests bound the ONE-BODY γ sector; they do NOT cleanly bound the
vacuum dial s.

---

## 0. The frozen UDT predictions (QUOTED, not re-derived)

From the two banked, blind-verified data-blind derivations (s=0 clean case, normalized gauge Δ=1):

**Light DEFLECTION** (`one_body_null_deflection_results.md`, verifier a2a421e68678e4687):

  **α_UDT(b) = 4·(m/b) + (9π/4)·(m/b)² + O(m³/b³)**,  m ≡ GM/c², b = impact parameter.

- Leading coefficient **4** ⇒ **γ_UDT = 1**, FORCED by the metric's form reciprocity B = 1/(a²A), NOT
  fitted (the ρ-dependent parts of A and B have equal slopes ⇒ the PPN-γ analog is exactly 1).
- Second order **9π/4 ≈ 7.0686** (native exponential-lapse value) vs Schwarzschild **15π/4 ≈ 11.781**.
  Ratio (9π/4)/(15π/4) = 3/5; convention-free native−GR departure = **−3π/2**.

**SHAPIRO delay** (`one_body_shapiro_delay_results.md`, verifier a758095ce3b865414):

  **c·Δt_oneway = 2m·ln(4r₁r₂/b²) + 2m + O(m²)**  (s=0 clean).

- Leading-log coefficient **2m** (exact, all-orders) ⇒ **γ_UDT = 1**, MATCHES GR.
- Second order per leg **(9π/4 − 2) ≈ 5.0686** vs GR **(15π/4 − 2) ≈ 9.7810**; convention-free
  native−GR departure = **−3π/2** per leg (same exponential-lapse signature as the deflection).
- The proper-time OBSERVABLE is only PARTIALLY frame-robust (leading log frame-clean; the
  second-order / ambient pieces ride the g-vs-ĝ clock-rate fork) — this does not affect the
  leading-order γ=1 confrontation below.

Both: **γ_UDT = 1 EXACTLY at leading order.** Only s=0 is the clean confrontable case.

---

## 1. Loaded constraints (with citations) — the observational inputs

| # | quantity | value | source (citation) |
|---|---|---|---|
| D1 | Cassini Shapiro-delay γ | **γ − 1 = (2.1 ± 2.3) × 10⁻⁵** | Bertotti, Iess & Tortora, *Nature* **425**, 374 (2003). Tightest γ; a SHAPIRO-DELAY measurement. |
| D2 | VLBI solar light-deflection γ | **γ − 1 ≈ (−0.8 ± 1.2) × 10⁻⁴** | Lambert & Le Poncin-Lafitte, *A&A* (2009/2011); Shapiro et al. (2004). VLBI global solutions; the exact figure varies by analysis, all at the ~10⁻⁴ level. A DEFLECTION measurement. |
| D3 | Solar mass length | **GM_⊙/c² = 1.4766 km** | standard (IAU/JPL). |
| D4 | Solar radius | **R_⊙ = 6.957 × 10⁵ km** | standard (IAU nominal). |
| D5 | conversions | 1 rad = 206265″ = 2.06265 × 10¹¹ μas | standard. |

Derived grazing geometry (from D3/D4): **m/b|_grazing = GM_⊙/(c²R_⊙) = 2.1225 × 10⁻⁶** (matches the
quoted 2.123 × 10⁻⁶).

**Self-consistency sanity check (§Task 1).** Leading grazing deflection
4·(m/b) = 4 × 2.1225 × 10⁻⁶ = 8.4899 × 10⁻⁶ rad = **1.7512″** — reproduces the canonical solar
light-bending 1.7517″ (the ~0.03% residual is the R_⊙ rounding; the leading UDT coefficient 4 is exactly
the GR value). ✔ Self-consistency confirmed.

---

## 2. Leading-order confrontation — γ_UDT = 1 (point prediction, no free parameter)

UDT predicts **γ = 1 exactly** at leading order in BOTH the deflection (coeff 4) and the Shapiro delay
(coeff 2m). This is a POINT prediction: the leading term carries no free parameter and no fit — it is
forced by the metric's form reciprocity (§0). Compare to the measured γ:

| test | measured γ − 1 | UDT γ − 1 | departure (σ) | verdict |
|---|---|---|---|---|
| **Cassini Shapiro (D1)** | (2.1 ± 2.3) × 10⁻⁵ | **0** (exact) | \|0 − 2.1e−5\|/2.3e−5 = **0.91σ** | **PASS** (ACCEPT) |
| **VLBI deflection (D2)** | (−0.8 ± 1.2) × 10⁻⁴ | **0** (exact) | \|0 − (−0.8e−4)\|/1.2e−4 = **0.67σ** | **PASS** (ACCEPT) |

**Verdict: UDT PASSES the leading-order solar light-sector tests.** The γ=1 point prediction sits
**0.91σ** from the Cassini central value and **0.67σ** from the VLBI central value — both comfortably
inside 1σ. No parameter was adjusted to achieve this (§7).

### 2b. Recorded: leading-order UDT gives γ = 1, FORCED not fitted (§Task 3)
The leading coefficients (deflection 4·(m/b); Shapiro 2m·ln) are the GR values because the s=0 one-body
metric has A = 1 − 2m/ρ, B = 1 + 2m/ρ at leading order with EQUAL ρ-slopes — the space-to-time
curvature ratio (PPN-γ analog) = 1 is a consequence of B = 1/(a²A) (form reciprocity), a structural
feature of the UDT metric, NOT a value chosen to match data. This is a genuine consistency confirmation
(see §8 on its discriminating power).

---

## 3. Second-order UDT-vs-GR difference at solar grazing (§Task 5) — the future-precision signature

The leading term is γ=1 for both theories, so the FIRST place UDT departs from GR is second order in m/b.

### 3a. Deflection second-order difference
  Δα(UDT−GR) = (9π/4 − 15π/4)(m/b)² = **−(3π/2)(m/b)²**  (UDT bends LESS than GR at 2nd order).

At grazing m/b = 2.1225 × 10⁻⁶:

| quantity | value (rad) | value (μas) |
|---|---|---|
| UDT 2nd-order term (9π/4)(m/b)² | 3.184 × 10⁻¹¹ | **6.57 μas** |
| GR 2nd-order term (15π/4)(m/b)² | 5.307 × 10⁻¹¹ | **10.95 μas** |
| **\|difference\| (3π/2)(m/b)²** | **2.123 × 10⁻¹¹** | **4.38 μas** |

Fractional size of the difference relative to the leading deflection:
(3π/2)(m/b)²/[4(m/b)] = (3π/8)(m/b) = **2.50 × 10⁻⁶** — i.e. the discriminating term is ~10⁻⁶ of the
already-measured leading bending, ~10⁻¹¹ rad of the total geometry.

### 3b. Shapiro second-order difference (order of magnitude)
Convention-free native−GR departure = **−(3π/2)·m²/b per leg**. At grazing (b = R_⊙, m = GM_⊙/c²):

- magnitude per leg = (3π/2)·m²/R_⊙ = 1.477 × 10⁻⁵ km ⇒ /c = **≈ 49 ps per leg** (≈ 0.05 ns).
- Leading log one-way delay (r₁,r₂ ~ 1 AU, grazing): c·Δt ≈ 35.8 km ⇒ **≈ 119 μs** one-way.
- **Fractional size: ~49 ps / 119 μs ≈ 4.1 × 10⁻⁷** of the leading Shapiro delay (per leg vs one-way,
  order-of-magnitude). Both express the SAME −3π/2 exponential-vs-Schwarzschild O(1/b²) origin.

---

## 4. CAN current data resolve 9π/4 vs 15π/4? — CANNOT (§Task 6)

**Clear statement: current data CANNOT resolve the native 9π/4 vs GR 15π/4 second-order distinction.**

- The tight γ constraints (Cassini γ to ±2.3 × 10⁻⁵; VLBI to ±1.2 × 10⁻⁴) bound the **LEADING** term
  (the γ=1 coefficient) — where UDT and GR are IDENTICAL. They do not probe the second-order coefficient.
- The second-order difference is ~**4.4 μas** in deflection (a ~10⁻¹¹-rad, ~2.5 × 10⁻⁶-fractional effect)
  and ~**49 ps** in Shapiro delay (~4 × 10⁻⁷ fractional). Both are far below current astrometric/timing
  reach at the Sun: Cassini's γ precision (2 × 10⁻⁵ on the leading term) corresponds to sensitivity
  nowhere near the (m/b)² ≈ 4.5 × 10⁻¹² relative geometry where the 9π/4-vs-15π/4 term lives.
- Gaia-class global astrometry reaches the low-μas level on stellar positions but not on a controlled
  grazing-solar second-order coefficient; no existing solar-system experiment isolates the (m/b)² light
  term at the few-μas / tens-of-ps level required.

**Therefore the 9π/4 signature is a FUTURE-precision target, not currently testable.**

### 4b. What precision WOULD distinguish them (future target)
To separate 9π/4 from 15π/4 at grazing one needs to measure the second-order light-bending coefficient
to better than the ~4 μas difference — i.e. astrometry of grazing rays at the **≲ 1 μas** level with
control of the (m/b)² term (equivalently, resolving the deflection to ~10⁻¹¹ rad / ~10⁻⁶ of the leading
bend), or Shapiro timing sensitive to the **~tens-of-ps** second-order leg term. This is roughly
one-to-two orders of magnitude beyond current dedicated solar-grazing measurements — a target for a
future dedicated μas-astrometry or ps-timing solar-limb experiment, not a present discriminator.

---

## 5. Verdict summary (ACCEPT / BOUND, per the frozen no-retuning rule)

- **Leading order (γ):** **ACCEPT / PASS** — UDT γ=1 is 0.91σ (Cassini) / 0.67σ (VLBI) from data.
- **Second order (9π/4):** **BOUND only** — current data cannot constrain it; the native −3π/2 departure
  is a future-precision target. No REJECT is warranted or possible at present precision.
- **The vacuum dial s:** **NOT bounded by these tests** (CF-CAT/CF-ABS, MAP §0) — solar tests confront
  the ONE-BODY γ sector; only s=0 was confrontable here, and s≠0 rides the conical ambiguity. This
  confrontation makes NO claim about s.

---

## 6. Honest characterization (§Task 8): consistency, NOT a discriminating test

Because γ_UDT = 1 is EXACT (forced by form reciprocity) and GR (γ=1) already fits the solar data, **UDT
passes the leading-order solar light tests BY CONSTRUCTION.** At the leading order these tests cannot
distinguish UDT from GR — both predict γ=1 identically. So the PASS is a **genuine consistency
confirmation** (UDT is not falsified by the tightest solar-system light constraints; a theory with γ≠1
would have been ruled out here, and UDT is not), but it is **NOT a discriminating test** between UDT and
GR. The place UDT and GR differ — the second-order 9π/4 vs 15π/4 — is below current reach (§4). The
9π/4 is banked as a **future-precision target**, the one solar-light quantity that could someday
discriminate.

---

## 7. NO-RETUNING / NO-BRANCH-ADJUSTMENT ATTESTATION (§Task 7)

I attest, per the pre-registered no-retuning rule (`J_of_s_light_deflection_confrontation_MAP.md` §6),
that in producing this confrontation I:
- changed **NOTHING** in the frozen UDT predictions — α_UDT = 4(m/b)+(9π/4)(m/b)² and
  c·Δt = 2m·ln(4r₁r₂/b²)+2m are quoted verbatim from the banked docs, not re-derived or altered;
- adjusted **NO** parameter (s, (Z,μ), M/q) to fit data — none was touched;
- made **NO** branch adjustment after seeing the data (the s=0 clean branch was fixed BEFORE the data
  load, as the only confrontable case per the frozen MAP; s was not selected to match anything);
- introduced **NO** new term, mechanism, or reinterpretation of a pre-registered clean failure;
- performed ONLY the authorized operation: load published constants and evaluate/compare the frozen
  formulas (ACCEPT / BOUND). Any model change found necessary after this would be a NEW
  pre-registration, run from scratch — not a retune of this one.

---

## 8. Premise ledger — every LOADED number (value + citation + tag)

| # | quantity | value | tag / source |
|---|---|---|---|
| L1 | Cassini γ−1 | (2.1 ± 2.3) × 10⁻⁵ | **LOADED-DATA** — Bertotti, Iess & Tortora, Nature 425, 374 (2003) |
| L2 | VLBI γ−1 | (−0.8 ± 1.2) × 10⁻⁴ | **LOADED-DATA** — Lambert & Le Poncin-Lafitte A&A (2009/2011); Shapiro et al. (2004) |
| L3 | GM_⊙/c² | 1.4766 km | **LOADED-DATA** — standard IAU/JPL |
| L4 | R_⊙ | 6.957 × 10⁵ km | **LOADED-DATA** — standard IAU nominal |
| L5 | 1 rad | 206265″ = 2.06265 × 10¹¹ μas | **LOADED-DATA** — standard conversion |
| L6 | 1 AU (Shapiro geometry) | 1.495978707 × 10⁸ km | **LOADED-DATA** — standard, used only for the Shapiro leading-log order-of-magnitude |
| L7 | c | 299792.458 km/s | **LOADED-DATA** — standard, for ps/μs conversions |
| — | m/b\|grazing | 2.1225 × 10⁻⁶ | **DERIVED** from L3/L4 |
| — | 4, 9π/4, 15π/4, 3π/2, 2m, 9π/4−2 | — | **FROZEN PREDICTION coeffs** (banked docs; NOT data) |

All acceptance criteria (σ-thresholds) are the standard "central value ± stated σ" of the cited
measurements; no criterion was chosen to engineer a pass.

---

## 9. For the verifier / attack surface

1. **σ-margin arithmetic.** Cassini: |0 − 2.1 × 10⁻⁵| / 2.3 × 10⁻⁵ = **0.913σ**. VLBI:
   |0 − (−0.8 × 10⁻⁴)| / 1.2 × 10⁻⁴ = **0.667σ**. Both < 1σ ⇒ PASS. Re-check these divisions; confirm
   the UDT value entering is γ−1 = 0 (exact), not a fitted number.
2. **Self-consistency check.** 4·(m/b) = 4 × (1.4766/6.957 × 10⁵) = 8.490 × 10⁻⁶ rad × 206265 =
   **1.7512″** vs canonical 1.7517″ (≤0.03% = R_⊙ rounding). Confirm the leading coefficient is exactly
   GR's 4 (γ=1), so this sanity check does NOT test UDT vs GR — it tests the arithmetic.
3. **μas estimate (deflection 2nd order).** (3π/2)(m/b)² = 1.5·π·(2.1225 × 10⁻⁶)² = 2.123 × 10⁻¹¹ rad
   × 2.06265 × 10¹¹ = **4.38 μas**. UDT term 6.57 μas, GR term 10.95 μas. Fractional vs leading:
   (3π/8)(m/b) = 2.50 × 10⁻⁶. Re-verify the squaring and the rad→μas conversion.
4. **Shapiro 2nd-order size.** (3π/2)·m²/R_⊙ = 1.477 × 10⁻⁵ km ⇒ /c ≈ 49 ps per leg; leading log
   (r ~ 1 AU) ≈ 119 μs one-way ⇒ fractional ~4 × 10⁻⁷. Order-of-magnitude only (per-leg vs one-way).
5. **CANNOT-resolve claim.** Confirm the second-order difference (~4 μas / ~49 ps, ~10⁻⁶–10⁻⁷
   fractional) is below Cassini/VLBI reach (which bound the LEADING γ term at 10⁻⁵–10⁻⁴). Attack whether
   any current experiment isolates the (m/b)² light coefficient — it does not.
6. **No-retuning attestation (§7).** Grep this doc against the two banked prediction docs: the frozen
   formulas must appear verbatim; no parameter (s, Z, μ, M) is set to a fitted value; the s=0 branch was
   fixed before the data load. Confirm the "consistency-not-discrimination" honesty (§6) is stated, not
   buried.
7. **Category discipline (CF-CAT/CF-ABS).** Confirm the doc bounds the ONE-BODY γ sector and makes NO
   claim that Cassini/VLBI bound the vacuum dial s (only s=0 confronted; s≠0 = conical, not confronted).

---

## LAB-LOG
- 2026-07-05: FROZEN DATA CONFRONTATION of the two banked, blind-verified s=0 light-sector predictions
  (deflection 4(m/b)+(9π/4)(m/b)²; Shapiro 2m·ln(4r₁r₂/b²)+2m) against published solar constraints
  (Cassini γ−1 = (2.1±2.3)e−5, Bertotti et al. 2003; VLBI γ−1 = (−0.8±1.2)e−4, Lambert & Le
  Poncin-Lafitte 2009/2011). **Results:** self-consistency 4(m/b)=1.7512″ ✔; **leading-order γ_UDT=1
  PASSES at 0.91σ (Cassini) / 0.67σ (VLBI)** — a consistency confirmation, NOT a discriminating test
  (γ=1 forced by form reciprocity, matches GR by construction). Second-order UDT−GR difference = 4.38 μas
  deflection / ~49 ps Shapiro (fractional 2.5e−6 / 4e−7) — **current data CANNOT resolve 9π/4 vs 15π/4**;
  it is a FUTURE ≲1-μas / tens-of-ps target. NO retuning, NO branch adjustment, NO new derivation
  (attested §7). Solar tests bound the ONE-BODY γ sector, NOT the vacuum dial s (CF-CAT/CF-ABS). **DRAFT
  — owes a blind adversarial verifier pass before banking (`verifier-before-record`).**
