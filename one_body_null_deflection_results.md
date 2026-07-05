# One-body NULL-geodesic deflection on the native UDT one-body metric — DERIVATION

**Status: BANKED — BLIND-VERIFIED (verifier a2a421e68678e4687, 2026-07-05: OVERALL HOLDS, no corrections
required; all 7 attacks PASS). The load-bearing s=0 result `4(m̂/b)+(9π/4)(m̂/b)²` was independently
re-derived TWO ways — own symbolic weak-field series with an independent ρ₀→b conversion (K₂=9π/4−4 to
15 digits) AND a direct high-precision mpmath null-geodesic integral ((α−4u)/u²→7.0686, NOT
Schwarzschild's 11.78). The GR reference 15π/4 was validated on the verifier's OWN machinery (fed
Schwarzschild → 15π/4); γ_UDT=1 confirmed; the s-dependence of K₁(s) confirmed real with the conical
CF-ABS caveat honest; no timelike/matter smuggle; data-blind; GR reference-only.** DERIVE node
(armchair/CAS): symbolic quadrature + weak-field series, no data load, no PDE solve. CAS:
`one_body_null_deflection_cas.py` (ALL CHECKS PASS, data-blind).

**What this discharges.** The quantity flagged **OWED** in `J_of_s_light_deflection_confrontation_MAP.md`
§1.2 / §8 / premise-7: the one-body (mass) null deflection `δ_body(b; m̂, s, Z)` — the impact-parameter-
DEPENDENT bending that actually confronts Cassini/VLBI. The ambient number `J(s)` (impact-parameter-
INDEPENDENT) was already banked (R2 S7); this is the SEPARATE mass observable, kept on its own track
throughout (per the MAP's §0 load-bearing distinction).

Frame + banked inputs (cited, none re-posited): metric `ds² = −e^{−2φ}c²dt² + e^{+2φ}dr² + ρ²dΩ²`
(canon C-2026-06-18-1); one-body exterior `A(ρ) = e^{−2ν·artanh(β/x)}·ρ^{2s}`, `x=√(ρ²+β²)` at
`E=1` (R2 S3/S9, `r2_final_cas.py:263`); `m̂ = νβ = M = −q > 0` (attractive σ=+1), `q̂ = −νβ`,
`ν = 2√(Z+μ²)/Z`, `s = 2μ/Z ∈ [0,½]`; form reciprocity `A·B = 1/a²` (S5a); null geodesics
conformally invariant (S10b) — the whole computation is frame-robust (g-vs-ĝ fork does NOT enter).

---

## 0. Premise ledger (every fixed thing tagged)

| # | premise | tag |
|---|---|---|
| 1 | metric form `ds²=−e^{−2φ}c²dt²+e^{2φ}dr²+ρ²dΩ²` | **CHOSE-cited** (canon C-2026-06-18-1) |
| 2 | one-body exterior `A=e^{−2ν artanh(β/x)}ρ^{2s}`, lapse `e^{−2φ̃}=1+2q̂/x+2q̂²/x²+…`, `m̂=νβ=−q` | **DERIVED** (R2 S3c/d, banked) |
| 3 | form reciprocity `B = 1/(a²A)` | **DERIVED** (R2 S5a, banked) |
| 4 | null geodesics conformally invariant ⇒ light frame-robust | **DERIVED** (R2 S10b, banked) |
| 5 | gauge `E=1, φ̃∞=0, φ₀=0` for the one-body rows | **CHOSE** (S4-legal; invariants surfaced where possible) |
| 6 | attractive branch σ=+1 (`m̂>0`) | **CHOSE-cited** (banked; σ=−1 is the other sheet) |
| 7 | `a` (ambient scale constant, `ρ=ar+b`) | **gauge/integration-data** (S4b/c) — tracked for cancellation |
| 8 | to O(m̂²): `f≡A/ρ^{2s}=e^{−2m̂/ρ}` (Z enters only at O(m̂³) via ν) | **DERIVED** (S3d expansion; §4 note) |
| 9 | GR curves `4GM/c²b`, `15π/4 (GM/c²b)²`, γ=1 | **method** — reference ONLY, entered AFTER native derivation (§5) |
| 10 | all symbolic/numeric claims | **DERIVED** (CAS, this doc) |

---

## 1. The exact null deflection quadrature (native)

Equatorial null ray on `ds² = −A c²dt² + B dρ² + ρ²dχ²`. Conserved `E = A c² ṫ`, `L = ρ²χ̇`; null
condition `−Ac²ṫ² + Bρ̇² + ρ²χ̇² = 0` gives `ρ̇² = [E²/(Ac²) − L²/ρ²]/B` and hence

  **`dχ/dρ = √B / ( ρ·√( (ρ²/ρ₀²)·(A(ρ₀)/A(ρ)) − 1 ) )`**    [CAS check 0]

with the turning point `ρ₀` where `ρ̇=0`, i.e. the **impact parameter** `b` set by `b² = ρ₀²/A(ρ₀)`
(`b = Lc/E`). The **exact deflection** is

  **`α(b) = 2∫_{ρ₀}^∞ (√B/ρ) dρ / √( (ρ²/ρ₀²)(A(ρ₀)/A(ρ)) − 1 ) − π`.**

Using `A = ρ^{2s}f`, `f = e^{−2φ̃}`, `B = 1/(a²A)` ⇒ `√B = ρ^{−s}/(a√f)`, and substituting
`y = ρ₀/ρ ∈ (0,1]` (regular at the turning point `y=1`), the whole thing **factorizes**:

  **`α + π = D(ρ₀)·K(ε)`,   `D(ρ₀) = e^{φ₀}·ρ₀^{−s}/a` (= `Δρ₀^{−s}`),**
  **`K(ε) = 2∫₀¹ y^{s−1}·f^{−1/2}·R^{−1/2} dy`,  `f=e^{−2εy}`, `R = y^{2s−2}e^{−2ε(1−y)} − 1`,  `ε = m̂/ρ₀`.**

`D(ρ₀)` is the **same local ruler-area prefactor** as in the ambient row (R2 S7). The turning point
substitution makes `R⁻¹ᐟ²` integrable at `y→1` (`R ≈ (2−2s)(1−y)`); every weak-field term stays finite
because the mass perturbation `δR ∝ (1−y)` supplies the softening factor. **Quadrature convergent,
turning point well-defined** (CF-QUAD does NOT fire).

**Does the ambient scale constant `a` cancel from the angle? NO.** `√B` carries `1/a`, so the entire
integrand — hence the entire swept azimuth `D(ρ₀)K(ε)` — carries an overall `1/a` (and `e^{φ₀}`). This
is a **finding, not an error**: it is exactly the ambient CONICAL/gauge factor already flagged for the
J(s) row (MAP §0(i), CF-ABS/CF-ORIGIN). `a` is a common prefactor on BOTH the ambient and the mass
pieces; it never cancels from the total angle. At `s=0` with the normalized gauge `Δ=e^{φ₀}/a=1` the
factor is unity and the angle is clean; for `Δ≠1` even flat vacuum sweeps `Δ·π` (a cone). See §4/CF-A.

**Frame-robustness.** The derivation used ONLY the null condition and the metric functions `A,B` — no
timelike/matter (`a(φ)`) input. So the conformal invariance of null geodesics (S10b) applies: `α` is
unchanged under `ĝ=e^{2φ}g`. **The one-body deflection does NOT ride the g-vs-ĝ fork** (CF-FRAME does
not fire).

---

## 2. β=0 consistency (mass off) — reduces to the ambient J(s)

At `β=0` (no body), `φ̃=0`, `f=1`, so `A→ρ^{2s}`, and the integrand collapses:
`y^{s−1}(y^{2s−2}−1)^{−1/2} = 1/√(1−y^{2−2s})`  [CAS check 1]. Hence

  `K(0) = 2∫₀¹ dy/√(1−y^{2−2s}) = J(s)`,   `α+π = D(ρ₀)·J(s)`   (the banked ambient azimuth),

with `J(0)=π`, `J(½)=4` reproduced. This is the clean cross-check: the setup **contains the ambient
sector exactly**, and the ambient/one-body split is `α+π = D(ρ₀)J(s) + D(ρ₀)[K(ε)−J(s)]` — first term
ambient, second term the pure one-body (mass) piece. **Kept separate throughout** (§5 table).

---

## 3. Weak-field expansion (the deliverable)

To O(m̂²) the native lapse is exactly `f = e^{−2m̂/ρ}` (S3d; the artanh/x corrections and all Z-dependence
beyond `m̂=νβ` are O(m̂³)). So `A = ρ^{2s}(1 − 2m̂/ρ + 2m̂²/ρ²)`, `B = (1/a²)ρ^{−2s}(1 + 2m̂/ρ + 2m̂²/ρ²)`.

### 3a. Leading mass term and its s-dependence (the conjecture test)
`K₁(s) ≡ dK/dε|₀ = 2∫₀¹ [ y/√(1−y^{m}) + (1−y)/(1−y^{m})^{3/2} ] dy = 2∫₀¹ (1−y^{m+1})/(1−y^{m})^{3/2} dy`,
`m=2−2s`, with the analytic-continued-Beta closed form
`K₁(s) = (2/m)[B(1/m,−½) − B((m+2)/m,−½)]`, `B(p,−½)=Γ(p)Γ(−½)/Γ(p−½)`  [CAS check 2]:

| s | 0 | ¼ | ⅓ | ½ |
|---|---|---|---|---|
| **K₁(s)** | **4** | (32Γ(⅙)Γ(⅓)−60Γ(⅔)Γ(⅚))/(45√π) ≈ 4.8328 | 9π/4 − 3√π Γ(¾)/Γ(¼) ≈ 5.2714 | **20/3** ≈ 6.6667 |

**K₁(s) is NOT constant — it GROWS with s.** ⇒ **The MAP's conjecture (that the S3c "no s×q mixing"
carries to null rays) FAILS at the level of the leading coefficient.** The mass and ambient sectors
split additively in the metric *exponent* (`φ = φ̃ − s ln ρ`, `f=e^{−2φ̃}` s-independent), but the
deflection is a *nonlinear functional* of the metric, so the ambient curvature (exponent `m=2−2s`)
re-weights how the mass bends light. **This s-sensitivity is, however, entangled with the ambient
conical/scale anomaly** — see 3b.

### 3b. The physical fixed-b one-body deflection
Working at fixed impact parameter `b` (the observable geometry), with `b² = ρ₀^{2−2s}e^{2ε}` and
`ρ₀ ≈ b^{1/(1−s)}` at leading order, the mass-induced extra bending is
`Δα_mass(b) = D(ρ₀)[e^{εs/(1−s)}K(ε) − J(s)]`, giving the leading term

  **`Δα_mass(b) ≈ (1/a)·C(s)·m̂·b^{−(1+s)/(1−s)}`,  `C(s) = K₁(s) + s·J(s)/(1−s)`**   [CAS check 5]

| s | 0 | 0.1 | ¼ | ⅓ | ½ |
|---|---|---|---|---|---|
| **C(s)** | **4** | 4.631 | 5.983 | 7.069 | 10.667 |
| **b-exponent** `−(1+s)/(1−s)` | **−1** | −1.222 | −1.667 | −2 | −3 |

For `s≠0` the one-body deflection acquires an **s-dependent coefficient AND a non-integer b-scaling
exponent** (and, dimensionally, `b` is not a length — `[b]=[ρ]^{1−s}`). This non-`1/b` scaling and the
`1/a` prefactor are the SAME conical/scale anomaly that leaves the ambient observable-status OPEN
(CF-ABS). **So for `s≠0`, s×q mixing IS present at leading order for null rays, but it rides the
conical ambiguity — its observable status inherits CF-ABS.**

### 3c. The clean case s=0 (Route A) — leading + native O(m̂²/b²) departure
Only at `s=0` is the deflection a clean, dimensionally-normal `1/b` angle. With the normalized gauge
(`Δ=1`, i.e. `a=e^{φ₀}`), the full weak-field one-body deflection is  [CAS checks 3,4]

  **`Δα_mass(b) |_{s=0} = 4·(m̂/b) + (9π/4)·(m̂/b)² + O(m̂³/b³)`.**

- Leading `4(m̂/b)` (independently confirmed by direct null-geodesic integration; residual scales as
  `(m̂/b)³`).
- Second order `9π/4 ≈ 7.0686`, a genuine **native** number from the exponential-lapse structure
  (`A=e^{−2m̂/ρ}`, `B=e^{+2m̂/ρ}` — the "Yilmaz-type" exponential metric, NOT Schwarzschild).

### 3d. Route B (s=½) leading
`K₁(½)=20/3`, `C(½)=32/3≈10.667`, b-exponent `−3`. The mass bending is much stronger and scales as
`b^{−3}` — a strong structural signature, but fully entangled with the s=½ conical anomaly.

---

## 4. Where Z and a live
- **Z**: does NOT appear in the deflection to O(m̂²) once expressed in the mass `m̂=νβ` (Z is absorbed
  into `m̂`). Z first re-enters at **O(m̂³)** (through the artanh/x correction `∝1/ν² = Z²/4(Z+μ²)`).
- **a**: does NOT cancel — it is the overall conical/gauge prefactor `D(ρ₀)=e^{φ₀}ρ₀^{−s}/a` common to
  ambient and mass pieces. Clean only in the normalized gauge `Δ=e^{φ₀}/a=1` (and only at `s=0` is the
  angle also dimensionally normal). **This is the ambient CONICAL issue, not an error.**

---

## 5. Full separated result (ambient / one-body / cross), each piece tagged

`α(b) = [AMBIENT] + [ONE-BODY mass] + [cross]`, all carrying the common conical `D(ρ₀)`:

| piece | expression | s-dependence | tag |
|---|---|---|---|
| **AMBIENT** | `D(ρ₀)J(s) − π` | `J(s)`: `J(0)=π`, `J(½)=4`, slope `π(1−ln2)` | banked (R2 S7); **observable-status OPEN** (conical, CF-ABS) |
| **ONE-BODY (mass)** | `D(ρ₀)[K(ε)−J(s)]` = `(1/a)C(s)m̂ b^{−(1+s)/(1−s)} + …` | leading coeff `C(s)` **s-DEPENDENT**; s=0: `4(m̂/b)+(9π/4)(m̂/b)²` | **DERIVED (this doc)** — the OWED quantity |
| **cross (s×q)** | subsumed in `C(s)`'s s-dependence + the non-`1/b` b-exponent | present at leading order (conjecture fails) but entangled with conical anomaly | **DERIVED (this doc)** |

**s fork preserved:** Route A `s=0` → clean `4(m̂/b)+(9π/4)(m̂/b)²`; Route B `s=½` → `C=32/3`, `b^{−3}`;
continuous sheet in between. Ambient and one-body kept on separate tracks (MAP §0 discipline).

---

## 6. GR comparison form (GR enters ONLY here, as a reference curve)

Native (s=0, normalized gauge): `A = 1 − 2m̂/ρ` (time), `B = 1 + 2m̂/ρ` (space) at leading order.
The ρ-dependent parts have equal coefficients ⇒ the **space-to-time-curvature ratio (the PPN-γ analog)
is `γ_UDT = 1` at leading order**, forced by the form reciprocity `B = 1/(a²A)`.

  **`Δα_UDT = 4(m̂/b) + (9π/4)(m̂/b)² + …`   vs   `α_GR = 4(GM/c²b) + (15π/4)(GM/c²b)² + …` (γ=1).**

- **Leading coefficient: MATCHES GR** (`4`, with `m̂ ↔ GM/c²`); `γ_UDT = 1`.
- **Second order: DEPARTS** — `9π/4` (native) vs `15π/4` (Schwarzschild). This is the native O(1/b²)
  signature of the exponential lapse (`+2q̂²/x²` structure, S3d). Ratio `(9π/4)/(15π/4) = 3/5`.

This is the pre-registered outcome **CF-GRMATCH-at-leading / departure-at-O(1/b²)**: a γ=1 leading term
(so no first-order departure to constrain) with a native second-order signature that Cassini/VLBI
precision would bound.

---

## 7. Pre-registered clean failures (frozen)

- **CF-COEFF-≠4** (leading ≠ GR's 4): **DID NOT FIRE** at s=0 — leading is exactly `4` (`γ_UDT=1`).
- **CF-GRMATCH-then-O(1/b²)** (leading matches GR, departure at second order): **THIS IS THE OUTCOME**
  at s=0 — `9π/4` vs `15π/4`. Cassini/VLBI bound the second-order term, not the leading.
- **CF-MIX** (s×q mixing at leading order ⇒ one-body deflection carries s-sensitivity): **FIRED** —
  `K₁(s)` and `C(s)` are s-dependent and the b-exponent shifts from `−1`. The MAP's no-s×q-mixing
  conjecture is **refuted for null rays**. Caveat: for `s≠0` this rides the ambient conical/scale
  anomaly (CF-ABS), so whether it is a clean observable is itself OPEN; only `s=0` is unambiguous.
- **CF-A** (the `a`/gauge constant does NOT cancel from the angle): **FIRED** — but as the *known*
  conical/gauge factor `D(ρ₀)=e^{φ₀}ρ₀^{−s}/a`, common to ambient and mass, not an error. Clean at
  `s=0`, `Δ=1`.
- **CF-QUAD** (non-convergent / turning point ill-defined): **DID NOT FIRE** — `y=ρ₀/ρ` regularizes;
  all weak-field terms finite.
- **CF-FRAME** (a frame-dependent timelike input smuggled in): **DID NOT FIRE** — only the null
  condition + `A,B` used; conformal invariance intact.
- **CF-NUM** (a forbidden data number needed to FORM the prediction): **DID NOT FIRE** — everything is
  dimensionless (`m̂/b`, `s`) / ratio form; grep-clean.

---

## 8. DERIVED vs OPEN vs OWED (summary)

- **DERIVED (this doc, CAS-verified):** the exact one-body null deflection quadrature `α+π=D(ρ₀)K(ε)`;
  β=0 → ambient `J(s)` cross-check; the leading mass coefficient `K₁(s)` (closed form; s=0→4, s=½→20/3,
  **s-dependent**); the fixed-b coefficient `C(s)` + b-exponent `−(1+s)/(1−s)`; **s=0 result
  `4(m̂/b)+(9π/4)(m̂/b)²`** (leading = GR's 4, `γ_UDT=1`; second order `9π/4` DEPARTS from GR's `15π/4`);
  a-non-cancellation (conical prefactor); frame-robustness (no timelike input); Z absent to O(m̂²).
- **OPEN (inherited, not resolved here):** for `s≠0`, whether the s-dependent one-body deflection is a
  clean observable or is absorbed into the ambient conical/scale ambiguity (CF-ABS); the ambient row's
  own observable-status (MAP §0(i)). At `s=0` there is no such ambiguity.
- **OWED next (separately gated, with Charles, BEFORE any data):** the null-sector Shapiro delay on the
  same metric (same quadrature family); then — Charles's go — load Cassini/VLBI bounds and run the
  frozen ACCEPT/REJECT/BOUND (no retuning) against `4(m̂/b)+(9π/4)(m̂/b)²` and the γ=1 leading.

---

## 9. For the verifier / attack surface (load-bearing steps)

1. **The leading coefficient `4` and `γ_UDT=1` at s=0** — re-derive `B=1/(a²A)` ⇒ equal space/time
   ρ-slopes ⇒ leading `4(m̂/b)`. Confirm independently (own Christoffel or own quadrature).
2. **The second-order `9π/4` (NOT `15π/4`)** — the load-bearing native departure. Re-integrate the s=0
   reduced integral to O(ε²) (`c₂ = 9π/4 − 4`), convert `ε→u=m̂/b` via `ε=u+u²`, and/or re-run the
   direct null-geodesic integral (CAS check 4). Confirm it is the exponential-metric value, not
   Schwarzschild's. This is where a sign/coefficient slip would live.
3. **The s-dependence of `K₁(s)` / `C(s)` (CF-MIX)** — the conjecture-refuting claim. Re-evaluate
   `K₁(s)` at several s (closed form + raw integral). Confirm it is genuinely s-dependent and not an
   artifact of the `D(ρ₀)`/ρ₀-vs-b bookkeeping; probe whether the mixing is separable from the conical
   anomaly (the honest caveat) or physical.
4. **`a` non-cancellation (CF-A)** — confirm the integrand carries an irreducible `1/a`; confirm it is
   the same conical `D(ρ₀)` as the ambient row and that `s=0, Δ=1` is the only fully-clean point.
5. **No timelike smuggle (CF-FRAME)** — audit that only the null condition and `A,B` enter; the mass
   `m̂` is a field integration constant (S3), not a matter-coupling input.
6. **Data-blindness** — grep the doc + CAS for any observational number (there are none; `4`, `9π/4`,
   `15π/4`, `20/3`, `32/3` are derived/reference coefficients, not data).

---

## Reproducible CAS (inline; full script `one_body_null_deflection_cas.py`, ALL CHECKS PASS)

```python
import sympy as sp, mpmath as mp; mp.mp.dps=30
rho,rho0,y,s,eps,a,c,En,L,Af,Bf,A0 = sp.symbols('rho rho0 y s epsilon a c En L Af Bf A0',positive=True)
# [0] exact null integrand from the metric (no GR):
rhodot2=(En**2/(Af*c**2)-L**2/rho**2)/Bf; dphi=(L/rho**2)/sp.sqrt(rhodot2)
b2=rho0**2/A0; claim=sp.sqrt(Bf)/(rho*sp.sqrt((rho**2/rho0**2)*(A0/Af)-1))
assert sp.simplify(dphi.subs(L,En*sp.sqrt(b2)/c)-claim)==0
# reduced: alpha+pi=D(rho0)K(eps); f=e^{-2 eps y}, R=y^{2s-2}e^{-2 eps(1-y)}-1, eps=mhat/rho0
f=sp.exp(-2*eps*y); R=y**(2*s-2)*sp.exp(-2*eps*(1-y))-1
P=y**(s-1)*f**sp.Rational(-1,2)*R**sp.Rational(-1,2)
# [1] beta=0 -> ambient J(s):
assert sp.simplify(P.subs(eps,0)-1/sp.sqrt(1-y**(2-2*s)))==0
# [2] leading coeff K1(s) (s-dependent): closed form via analytic-continued Beta
G=sp.gamma; B=lambda q:G(q)*G(-sp.Rational(1,2))/G(q-sp.Rational(1,2))
K1=lambda sv:(2*(B(1/(2-2*sv))-B((2-2*sv+2)/(2-2*sv))))/(2-2*sv)
assert abs(float(K1(0))-4)<1e-9 and sp.simplify(K1(sp.Rational(1,2)))==sp.Rational(20,3)
# [3] s=0 weak field to O(mhat^2): c1=4, c2=9pi/4-4 ; fixed-b: 4(mhat/b)+(9pi/4)(mhat/b)^2
P0=2*sp.exp(eps*y)/sp.sqrt(sp.exp(-2*eps*(1-y))-y**2); ser=sp.series(P0,eps,0,3).removeO()
c1=mp.quad(sp.lambdify(y,ser.coeff(eps,1),'mpmath'),[0,1]); assert abs(c1-4)<1e-12
c2=mp.quad(sp.lambdify(y,ser.coeff(eps,2),'mpmath'),[0,1]); assert abs(c2-(9*mp.pi/4-4))<1e-10
# [4] end-to-end null-geodesic integral matches 4u+(9pi/4)u^2:
Kx=lambda e:2*mp.quad(lambda t:mp.e**(e*t)/mp.sqrt(mp.e**(-2*e*(1-t))-t**2),[0,1])
e=mp.mpf('0.005'); al=Kx(e)-mp.pi; u=e*mp.e**(-e); assert abs(al-(4*u+9*mp.pi/4*u**2))/al<4e-4
```

## LAB-LOG
- 2026-07-05: derived the OWED one-body null deflection (MAP §1.2). Exact quadrature `α+π=D(ρ₀)K(ε)`;
  β=0 recovers ambient `J(s)`. **Key results:** leading mass coeff `K₁(s)` is **s-DEPENDENT**
  (4→20/3), refuting the no-s×q-mixing conjecture for null rays (with the conical-anomaly caveat for
  s≠0); the clean `s=0` deflection `4(m̂/b)+(9π/4)(m̂/b)²` MATCHES GR at leading (`γ=1`) and DEPARTS at
  second order (`9π/4` vs `15π/4`); `a` does NOT cancel (conical prefactor); Z absent to O(m̂²); light
  frame-robust (no timelike smuggle). Data-blind, grep-clean, single process, seconds. **DRAFT —
  blind adversarial verifier pass OWED before banking (`verifier-before-record`); data load is a
  separate later gated step.**
