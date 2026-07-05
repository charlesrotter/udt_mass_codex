# One-body SHAPIRO TIME-DELAY on the native UDT one-body metric — DERIVATION

**Status: BANKED — BLIND-VERIFIED (verifier a758095ce3b865414, 2026-07-05: OVERALL HOLDS, no corrections;
all 6 attacks PASS). The load-bearing second-order `9π/4−2` was independently re-derived by a DIFFERENT
method (exact semi-analytic O(m²) coefficient, distinct from this doc's polynomial fit — guarding against
a shared-bug false pass; agreement ~5e-8), with a Schwarzschild control returning `15π/4−2` on the same
machinery. Leading log `2m̂` / γ_UDT=1 confirmed all-orders exact (no m²·lnR term); β=0 + ambient F(s;R)
cross-check confirmed; the FRAME VERDICT (partially frame-robust; clock factor √A(ρ_obs) does not cancel;
g-vs-ĝ fork located-not-resolved) confirmed correct + honestly stated; data-blind; consistent with the
banked deflection (same exponential-lapse 9π/4 signature, −3π/2 departure).**
DERIVE node (armchair/CAS): symbolic quadrature + weak-field series + a high-precision mpmath
cross-check. NO data load, NO PDE solve. Companion to the just-banked, blind-verified one-body NULL
DEFLECTION (`one_body_null_deflection_results.md`, verifier a2a421e68678e4687): **same metric, same
gauge, same conventions**. CAS: `shapiro_delay_cas.py` (ALL CHECKS PASS, data-blind).

**What this computes.** The companion deflection discharged the one-body BENDING observable. This is
its null-sector partner on the identical metric: the **coordinate-time Shapiro delay** of a null ray
from ρ₁ to ρ₂ past closest approach ρ₀, and — the key differentiator — whether the **measured** (proper-
time) delay inherits the g-vs-ĝ frame fork that the deflection escapes.

Frame + banked inputs (cited, none re-posited): metric `ds²=−A c²dt²+B dρ²+ρ²dΩ²` (canon
C-2026-06-18-1); one-body exterior `A(ρ)=e^{−2ν artanh(β/x)}ρ^{2s}`, `x=√(ρ²+β²)` at `E=1`
(R2 S3, `r2_final_cas.py:263`); s=0 clean case `A=e^{−2m̂/ρ}`, `B=e^{+2m̂/ρ}` (a=1, Δ=1 normalized
gauge); form reciprocity `A·B=1/a²` (S5a); `m̂=νβ=M=−q>0` (attractive σ=+1); `s=2μ/Z∈[0,½]`;
`D(ρ₀)=e^{φ₀}ρ₀^{−s}/a` conical prefactor. GR/PPN enters **only** in §4, as a reference curve, after
the native expression is derived.

---

## 0. Premise ledger (every fixed thing tagged)

| # | premise | tag |
|---|---|---|
| 1 | metric form `ds²=−e^{−2φ}c²dt²+e^{2φ}dr²+ρ²dΩ²` | **CHOSE-cited** (canon C-2026-06-18-1) |
| 2 | one-body exterior `A=e^{−2ν artanh(β/x)}ρ^{2s}`; s=0: `A=e^{−2m̂/ρ}`, `B=e^{+2m̂/ρ}` | **DERIVED** (R2 S3, banked) |
| 3 | form reciprocity `B=1/(a²A)` ⇒ `√(B/A)=1/(aA)` | **DERIVED** (R2 S5a, banked) |
| 4 | null geodesics conformally invariant ⇒ **coordinate** delay frame-robust | **DERIVED** (R2 S10b, banked) |
| 5 | static clock rate `dτ=√A dt` (g) / `=dt` (ĝ, Â_tt=−c²) — rides g-vs-ĝ fork | **DERIVED** (R2 §0.5/S13e, banked) |
| 6 | gauge `E=1, φ̃∞=0, φ₀=0, a=1` (⇒Δ=1) for the s=0 one-body row | **CHOSE** (S4-legal) |
| 7 | attractive branch σ=+1 (`m̂>0`) | **CHOSE-cited** (banked) |
| 8 | to O(m̂²): `√(B/A)=e^{+2m̂/ρ}` **exactly** (Z,artanh corrections O(m̂³)) | **DERIVED** (S3d) |
| 9 | reference (no-mass) leg time at fixed ρ₀ = `√(ρ²−ρ₀²)` (straight ray, same turning radius) | **CHOSE** (reference convention; only the LOG coeff + the native−GR DIFFERENCE are convention-free) |
| 10 | GR/PPN `2(1+γ)GM/c³ ln(...)`, γ=1, 15π/4 second order | **method** — reference ONLY, entered AFTER native derivation (§4) |
| 11 | all symbolic/numeric claims | **DERIVED** (CAS, this doc) |

---

## 1. The exact Shapiro coordinate-time quadrature (native)

Equatorial null ray on `ds²=−A c²dt²+B dρ²+ρ²dχ²`. Conserved `E=A c²ṫ`, `L=ρ²χ̇`; null condition
`−Ac²ṫ²+Bρ̇²+ρ²χ̇²=0` ⇒ `ρ̇²=[E²/(Ac²)−L²/ρ²]/B`. The **coordinate time** follows from
`dt/dρ=ṫ/ρ̇`:

  **`c·dt/dρ = √(B/A) / √(1 − A(ρ)·b²/ρ²)`,   `b=Lc/E`.**   [CAS check A — derived from the null condition, no GR]

The turning point ρ₀ is where the radicand vanishes: **`b²=ρ₀²/A(ρ₀)`** (same as the deflection). The
one-leg coordinate time from ρ₀ out to ρ is `c t_leg(ρ)=∫_{ρ₀}^{ρ}√(B/A)dρ'/√(1−(ρ₀²/ρ'²)(A(ρ')/A(ρ₀)))`,
manifestly regular at the turning point (the `y=ρ₀/ρ` substitution of the deflection doc regularizes
the `R⁻¹ᐟ²` endpoint; CF-QUAD does not fire). The **Shapiro delay** is the excess of this over the
no-mass straight-ray time `√(ρ²−ρ₀²)`:

  **`c·Δt_leg = ∫_{ρ₀}^{ρ} [ √(B/A)/√(1−(ρ₀²/ρ'²)(A(ρ')/A(ρ₀))) − 1/√(1−ρ₀²/ρ'²) ] dρ'`.**

A one-way passage ρ₁→ρ₂ across the mass is two such legs (ρ₀→ρ₁ and ρ₀→ρ₂); a radar round trip is
2× the one-way.

**Frame-robustness of the COORDINATE delay.** The integrand uses only the null condition and `A,B` — no
timelike/matter (`a(φ)`) input. Under `ĝ=e^{2φ}g` the null condition rescales by an overall `e^{2φ}`
that cancels in `dt/dρ`; the coordinate `t` label is untouched. So **`Δt_coord` is frame-robust**, like
the deflection angle. The MEASURED (proper-time) delay is a separate question — §5.

---

## 2. β=0 / no-mass consistency, and the ambient sector cross-check

**Mass off (β=0, m̂=0), s=0:** `√(B/A)=1` and `A/A(ρ₀)=1`, so the two integrands coincide and
`Δt_leg=0` — **zero excess delay**, as required.

**Ambient sector present (the radar row F(s;R)).** The setup contains the banked ambient radar row: for
a **radial** ray (b=0) the coordinate time is `c t=∫√(B/A)dρ`, and with the ambient areal metric
`A=e^{−2φ₀}ρ^{2s}`, `B=e^{2φ₀}ρ^{−2s}/a²`,

  `√(B/A)=e^{2φ₀}ρ^{−2s}/a`  ⇒  `c t=(e^{2φ₀}/a)·ρ^{1−2s}/(1−2s)`   [CAS check B]

which is exactly the S6b antiderivative `anti_t` with its `e^{2φ₀}/a` prefactor. Hence the round-trip
ruler-normalized ratio reproduces `F(s;R)=(1−s)/(1−2s)·ρ₁^s(ρ₂^{1−2s}−ρ₁^{1−2s})/(ρ₂^{1−s}−ρ₁^{1−s})`,
`F(0;R)=1` (banked R2 S6b). **The Shapiro quadrature contains the ambient time-tilt sector exactly**;
the one-body log below rides on top of it. (For s≠0 this ambient tilt is the frame-DEPENDENT radar row
R2-5 — see §5/§6.)

---

## 3. Weak-field expansion (the deliverable) — s=0 clean case

To O(m̂²) the lapse is exactly `√(B/A)=e^{+2m̂/ρ}` (S3d; artanh/Z corrections are O(m̂³)).

### 3a. Leading LOGARITHMIC term
Expanding the excess integrand to O(m̂) (ρ₀ held fixed) gives the closed form [CAS check C]

  **`d(cΔt)/dρ |_{O(m̂)} = m̂·(2ρ+3ρ₀)/[(ρ+ρ₀)√(ρ²−ρ₀²)]`,**

which splits as `2/√(ρ²−ρ₀²) + ρ₀/[(ρ−ρ₀)^{1/2}(ρ+ρ₀)^{3/2}]`. Integrating ρ₀→R:

- `∫2/√(ρ²−ρ₀²)dρ = 2 arccosh(ρ/ρ₀) → 2 ln(2R/ρ₀)` (large R) — **the log**;
- `∫ρ₀/[(ρ−ρ₀)^{1/2}(ρ+ρ₀)^{3/2}]dρ = ∫₀^∞ τ^{−1/2}(2+τ)^{−3/2}dτ = 2^{−1}B(½,1) = 1` — a finite constant
  (per leg). [CAS check C]

So **per leg** `c·Δt_leg = m̂[2 arccosh(ρ_i/ρ₀) + 1] + O(m̂²)`, and the **one-way** delay is

  **`c·Δt_oneway = 2m̂·ln(4ρ₁ρ₂/ρ₀²) + 2m̂ + O(m̂²)`.**

- **Leading-log coefficient = `2m̂`, exact** (all-orders): because `√(B/A)=e^{2m̂/ρ}` has 1/ρ-tail
  coefficient exactly `2m̂` and the denominator contributes only 1/ρ² tails, the log coefficient
  receives **no** higher-order-in-m̂ correction. **Argument = `4ρ₁ρ₂/ρ₀²`** (native `e^φ`-areal form of
  the standard `4r₁r₂/b²`; ρ₀→b at leading order).
- The `+2m̂` finite piece and the log argument's constant are reference-convention-dependent (premise 9);
  the **coefficient 2m̂ and the argument's ρ-dependence are convention-free**.

### 3b. Second-order UDT-specific correction (analog of the deflection's 9π/4)
Define the b-localized (R-independent) excess `W(m̂)=lim_{R→∞}[cΔt_leg − 2m̂ arccosh(R/ρ₀)]`. High-
precision mpmath (ρ₀=1, R up to 1e14, fit in m̂) gives, **per leg**, [CAS check D]

  **`W(m̂) = m̂ + (9π/4 − 2)·(m̂²/ρ₀) + O(m̂³)`,   `9π/4 − 2 = 5.0685834706…` (matches to ~1e-9).**

So the native second-order Shapiro coefficient carries the **same `9π/4`** exponential-lapse number as
the deflection's second-order term. (The stability of `W` across R=1e10…1e14 confirms there is **no**
m̂² ln R term — the log coefficient is purely 2m̂, as stated in 3a.) The `−2` is a common geometric/
reference constant (see §4); the metric-nonlinearity part is `9π/4`.

### 3c. s≠0 — flagged, not claimed (see §6)
For s≠0 the same conical/scale prefactor `D(ρ₀)=e^{φ₀}ρ₀^{−s}/a` multiplies the mass log, `b` is not a
length (`[b]=[ρ]^{1−s}`), and the ambient tilt `F(s;R)` (frame-DEPENDENT, R2-5) enters additively. The
clean, dimensionally-normal, gauge-clean case is **s=0 only** (CF-ABS). Kept separate.

---

## 4. GR comparison (GR enters ONLY here, as a reference curve)

Running the identical machinery on Schwarzschild (`A=1−2m/ρ`, `B=(1−2m/ρ)⁻¹`, γ=1) gives [CAS check D]

  **`W_GR(m) = m + (15π/4 − 2)·(m²/ρ₀) + O(m³)`,   `15π/4 − 2 = 9.7809724510…`.**

Leading log (both): `c Δt_oneway = 2m̂ ln(4ρ₁ρ₂/ρ₀²)` (γ=1). Comparison:

| quantity | UDT (native) | GR (γ=1 ref) | verdict |
|---|---|---|---|
| **leading-log coeff** | `2m̂` (one-way); `4m̂` round-trip | `2(1+γ)GM/c³·½`→`2GM/c³` one-way; `4GM/c³` round-trip | **MATCHES** (`γ_UDT=1`, `m̂↔GM/c²`) |
| **log argument** | `4ρ₁ρ₂/ρ₀²` | `4r₁r₂/b²` | **MATCHES** (areal ρ₀↔b at leading) |
| **2nd-order coeff** (per leg, `×m̂²/ρ₀`) | `9π/4 − 2` | `15π/4 − 2` | **DEPARTS** |
| **native − GR 2nd-order** (per leg) | `(9π/4−2)−(15π/4−2) = −3π/2` | — | **`−3π/2`, convention-FREE** |

- **Leading: MATCHES GR** — `γ_UDT=1`, exactly consistent with the deflection. No first-order departure.
- **Second order: DEPARTS** — native `9π/4` vs Schwarzschild `15π/4`, ratio `(9π/4)/(15π/4)=3/5`, the
  **same native signature as the deflection**. The reference-convention constant `−2` is identical in
  both (a γ=1 geometric term), so the **convention-independent** native-vs-GR Shapiro second-order
  departure is exactly **`−3π/2` per leg** — numerically equal to the deflection's second-order
  departure `15π/4−9π/4 = 3π/2` (same exponential-vs-Schwarzschild O(1/ρ²) origin).

Pre-registered outcome **CF-GRMATCH-at-leading / departure-at-O(m̂²)** — a γ=1 leading term with a
native second-order signature that Cassini-class precision would bound (data confrontation is a later,
separately gated step).

---

## 5. ★ THE FRAME SUBTLETY — is the Shapiro OBSERVABLE frame-robust? (load-bearing)

Handled explicitly; the g-vs-ĝ fork is **not** silently resolved.

**Step 1 — the coordinate delay is frame-robust** (§1): built from null geodesics; `Δt_coord`
is conformally invariant. Same status as the deflection.

**Step 2 — the observable is a PROPER-TIME interval on the observer's clock.** A static observer at
ρ_obs converts coordinate time to measured time by the clock rate `dτ = √A(ρ_obs) dt` (g-frame). Both
the delayed round-trip and its no-mass reference are read on the SAME clock at the SAME location, so
the clock rate factors OUT of the differential as a single multiplicative normalization:

  **`Δτ_obs = √A(ρ_obs) · Δt_coord,excess`.**

The factor `√A(ρ_obs)` **rides the g-vs-ĝ fork** (premise 5, R2 §0.5):
- **g-frame:** `√A(ρ_obs)=e^{−m̂/ρ_obs}·(ambient ρ_obs^{s})` — departs from 1;
- **ĝ (matter/Jordan) frame:** `Â_tt=−c²` (flat) ⇒ `√Â=1` exactly ⇒ `Δτ̂_obs=Δt_coord,excess`.

**Verdict — PARTIALLY frame-robust (differs from the deflection).**
- The **leading-log term IS frame-robust**: the clock factor is `1+O(m̂/ρ_obs)`, so it corrects the
  `2m̂ ln(...)` term only at **O(m̂²)**. The γ=1 leading-log Shapiro prediction is frame-clean.
- The **second-order term and the ambient s-tilt are frame-CONDITIONAL**: the observer clock-rate
  normalization `√A(ρ_obs)` (unity in ĝ, `e^{−m̂/ρ_obs}·ρ_obs^s` in g) multiplies the whole delay, and
  the ambient tilt enters as the frame-DEPENDENT radar row `F(s;R)` (R2-5, FD).
- Structurally the Shapiro OBSERVABLE is a **null-geodesic path (frame-robust) read out by a clock
  (frame-dependent)** — it lands in the same "mixes a clock and a ruler ⇒ frame-dependent" class as the
  radar row R2-5, NOT in the deflection's pure-angle "one genuinely frame-robust" class (R2 §0.6).

**So the key way Shapiro DIFFERS from the deflection:** the deflection is a pure coordinate angle with
no clock readout ⇒ fully frame-robust; the Shapiro delay's leading log is frame-robust but its
normalization and second-order/ambient structure inherit the clock-rate frame fork. (For a distant
observer, `ρ_obs`→∞ makes `√A→1`, suppressing the g-frame factor in practice; the ambient s-tilt is the
larger frame lever. This does not resolve the fork — it locates where the fork enters.)

---

## 6. s=0 clean vs s≠0 (kept separate)

- **s=0 (Route A, normalized gauge Δ=1):** unambiguous. Leading `2m̂ ln(4ρ₁ρ₂/ρ₀²)`, second order
  `(9π/4−2)m̂²/ρ₀` per leg. No conical prefactor, `b` is a length, ρ₀↔b clean.
- **s≠0:** the mass log is multiplied by the conical/scale prefactor `D(ρ₀)=e^{φ₀}ρ₀^{−s}/a` (does not
  cancel), `b` is not a length, and the ambient `F(s;R)` tilt adds. The **same CF-ABS conical ambiguity
  as the deflection** ⇒ observable-status OPEN for s≠0. Not over-claimed here.

---

## 7. Pre-registered clean failures (FROZEN)

- **CF-COEFF≠GR** (leading log ≠ GR's, γ≠1): **DID NOT FIRE** — leading coeff exactly `2m̂` (γ_UDT=1).
- **CF-GRMATCH-then-O(m̂²)** (leading matches, departs at 2nd order): **THIS IS THE OUTCOME** —
  `9π/4` vs `15π/4` (native−GR = `−3π/2` per leg, convention-free).
- **CF-FRAME-RIDES** (the Shapiro observable rides the fork, unlike the deflection): **PARTIALLY FIRED**
  — coordinate delay + leading log frame-robust, but the proper-time observable carries a frame-
  dependent clock-rate normalization `√A(ρ_obs)` (unity in ĝ) ⇒ second-order/ambient pieces are
  frame-conditional. Shapiro is NOT in the deflection's pure-frame-robust class.
- **CF-ABS** (s≠0 conical/scale ambiguity): **FIRED** for s≠0 (same `D(ρ₀)` as the deflection); s=0 clean.
- **CF-QUAD** (non-convergent / log argument ill-defined): **DID NOT FIRE** — turning-point regular,
  `W(m̂)` R-stable to 1e-9, log argument `4ρ₁ρ₂/ρ₀²` well-defined.
- **CF-NUM** (a forbidden data number needed to FORM the prediction): **DID NOT FIRE** — everything is
  dimensionless/ratio (`m̂/ρ`, `2m̂`, `9π/4−2`, `−3π/2`); grep-clean, no Cassini/VLBI/PPN numbers, no G.

---

## 8. DERIVED vs OPEN vs OWED (summary)

- **DERIVED (this doc, CAS-verified):** the exact native Shapiro coordinate-time quadrature
  `c dt/dρ=√(B/A)/√(1−Ab²/ρ²)`; β=0→zero delay + ambient `F(s;R)` cross-check; **s=0 leading log
  `2m̂ ln(4ρ₁ρ₂/ρ₀²)` (coeff `2m̂` exact, γ_UDT=1)**; the finite `+2m̂`; the **second-order native
  coefficient `9π/4−2` per leg** (vs GR `15π/4−2`; native−GR `−3π/2`, convention-free); coordinate delay
  frame-robust; **the OBSERVABLE only PARTIALLY frame-robust** (leading log clean, normalization +
  second-order/ambient ride the clock-rate fork).
- **OPEN (inherited):** for s≠0 whether the delay is a clean observable or absorbed into the ambient
  conical/scale + frame ambiguity (CF-ABS, R2-5 FD); the g-vs-ĝ fork itself (not resolved — located).
- **OWED next (separately gated, with Charles, BEFORE any data):** — Charles's go — load Cassini/VLBI/
  radar bounds and run the frozen ACCEPT/REJECT/BOUND against `2m̂ ln(4ρ₁ρ₂/ρ₀²)` (γ=1) + the native
  second-order `9π/4−2`, holding the frame verdict (observable is frame-conditional at second order).

---

## 9. For the verifier / attack surface (load-bearing steps)

1. **The leading-log coefficient `2m̂` and its all-orders exactness (γ_UDT=1).** Re-derive
   `c dt/dρ=√(B/A)/√(1−Ab²/ρ²)` from the null condition; confirm `√(B/A)=e^{2m̂/ρ}` gives 1/ρ-tail
   exactly `2m̂` with no m̂²-log. This is where a factor-of-2 or a γ≠1 slip would live. (CAS A, C.)
2. **The second-order `9π/4−2` (NOT `15π/4−2`).** The load-bearing native departure. Re-run the
   b-localized `W(m̂)` fit (own quadrature, own subtraction of `2m̂ arccosh(R/ρ₀)`); confirm R-stability
   (no residual m̂² log) and the exponential-metric value `9π/4`, not Schwarzschild's `15π/4`. Confirm
   the convention-free invariant `native−GR = −3π/2`. (CAS D.)
3. **The frame verdict (§5).** The claim that the OBSERVABLE carries `√A(ρ_obs)` (unity in ĝ) and so is
   only PARTIALLY frame-robust — attack whether the clock factor really fails to cancel in the delay
   differential, and whether the leading log truly survives frame-clean (O(m̂/ρ_obs) correction). This
   is the key Shapiro-vs-deflection difference and the most interpretation-heavy step.
4. **No timelike smuggle in the coordinate delay.** Audit that §1 uses only the null condition + `A,B`;
   the clock factor `√A` enters ONLY in §5 (the observable), correctly flagged frame-dependent.
5. **Data-blindness.** grep the doc + CAS for any observational number (none; `2m̂`, `9π/4`, `15π/4`,
   `3π/2` are derived/reference coefficients).

---

## Reproducible CAS (inline; full script `shapiro_delay_cas.py`, ALL CHECKS PASS, data-blind)

```python
import sympy as sp, mpmath as mp; mp.mp.dps=40
rho,rho0,c,En,L,Af,Bf,b,m = sp.symbols('rho rho0 c E L Af Bf b m',positive=True)
# [A] exact c dt/drho from the null condition (no GR):
rhodot2=(En**2/(Af*c**2)-L**2/rho**2)/Bf; cdtdrho=c*(En/(Af*c**2))/sp.sqrt(rhodot2)
assert sp.simplify(cdtdrho.subs(L,En*b/c)-sp.sqrt(Bf/Af)/sp.sqrt(1-Af*b**2/rho**2))==0
# [C] s=0 O(m) excess integrand -> leading log 2m*arccosh + finite 1/leg:
I=sp.exp(2*m/rho)/sp.sqrt(1-(rho0**2/rho**2)*sp.exp(-2*m/rho+2*m/rho0)); Iflat=1/sp.sqrt(1-rho0**2/rho**2)
dI1=sp.simplify(sp.series(I-Iflat,m,0,2).removeO().coeff(m,1))
assert sp.simplify(dI1-(2*rho+3*rho0)/((rho+rho0)*sp.sqrt(rho**2-rho0**2)))==0
assert abs(mp.quad(lambda t:1/(mp.sqrt(t)*(2+t)**mp.mpf(1.5)),[0,mp.inf])-1)<1e-12  # finite=1/leg
# [D] second-order b-localized coeff: native 9pi/4-2, GR 15pi/4-2, diff -3pi/2:
def W(m_,R,kind):
    I=(lambda r: mp.e**(2*m_/r)/mp.sqrt(1-(1/r**2)*mp.e**(-2*m_/r+2*m_))) if kind=='udt' \
      else (lambda r:(1/(1-2*m_/r))/mp.sqrt(1-(1/r**2)*((1-2*m_/r)/(1-2*m_))))
    return mp.quad(I,[1,R])-mp.sqrt(R**2-1)-2*m_*mp.acosh(R)
def w2(kind,R=mp.mpf('1e13')):
    ms=[mp.mpf('1e-4')*k for k in (1,2,3,4)]
    return mp.lu_solve(mp.matrix([[x,x**2,x**3,x**4] for x in ms]),mp.matrix([W(x,R,kind) for x in ms]))[1]
wu,wg=w2('udt'),w2('gr')
assert abs(wu-(9*mp.pi/4-2))<1e-6 and abs(wg-(15*mp.pi/4-2))<1e-6 and abs((wg-wu)-3*mp.pi/2)<1e-8
```

## LAB-LOG
- 2026-07-05: derived the one-body Shapiro coordinate-time delay on the same s=0 metric as the banked
  deflection. Exact quadrature `c dt/dρ=√(B/A)/√(1−Ab²/ρ²)`; β=0→zero excess + contains ambient
  `F(s;R)`. **Key results:** leading log `2m̂ ln(4ρ₁ρ₂/ρ₀²)` (coeff `2m̂` exact ⇒ **γ_UDT=1**, MATCHES
  GR); native second-order `9π/4−2` per leg (vs GR `15π/4−2`; convention-free departure `−3π/2`, the
  **same 9π/4 exponential-lapse signature as the deflection**, ratio 3/5); **the OBSERVABLE only
  PARTIALLY frame-robust** — leading log frame-clean, but the proper-time delay carries a frame-
  dependent clock-rate normalization `√A(ρ_obs)` (unity in ĝ) so second-order/ambient pieces ride the
  g-vs-ĝ fork — Shapiro is NOT in the deflection's pure-frame-robust class. s=0 clean; s≠0 conical
  (CF-ABS). Data-blind, grep-clean, seconds. **DRAFT — blind adversarial verifier pass OWED before
  banking (`verifier-before-record`); data load is a separate later gated step.**
