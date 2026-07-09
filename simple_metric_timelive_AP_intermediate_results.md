## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE (intermediate needle tests) |
| **Tests** | **I1** wall-loud envelope · **I2** non-adiabatic \(k_t\) |
| **Build-on grade** | **LEAD** — still not full Einstein time-live |
| **Machine** | `simple_metric_timelive_AP_intermediate_out.json` |

### Premise ledger

| Item | Tag |
|------|-----|
| Background \(A_0=1-r/X\) (L) | WORKING |
| \(A=A_0(1+\varepsilon s(r)\cos(\omega t+\phi))\), \(\varepsilon=0.05\) | FREE probe |
| Envelopes: mid / wall \(\xi^4\) / wall soft | FREE family |
| Non-adiabatic: \(\mathrm{d}k_t/\mathrm{d}r=\partial_t A/A^2\) along null | THEORY (geodesic on this metric family) |
| Full Einstein residual dynamics | **NOT** |

---

# Intermediate tests: does the needle move?

## What we added beyond the first cut

| Test | Change |
|------|--------|
| **I1 Wall-loud** | \(s(r)\) **peaks near the wall** (not vanishing there) |
| **I2 Non-adiabatic** | Evolve \(k_t\) along the ray; \(1+z=E_{\mathrm{em}}/E_{\mathrm{obs}}\) with \(E\propto -k_t/\sqrt{A}\) |

Sanity: \(\varepsilon=0\) → adiabatic = non-adiabatic = \(R_L\).

---

## Results (character)

### A. Phase-averaged \(\langle R\rangle\) still hugs \(R_L\)

Across **all** envelopes and both modes, at \(\Omega=1\):

\[
\langle R\rangle_\phi / R_L \;\approx\; 1
\]
to \(\lesssim 0.2\%\) mean offset (occasionally \(\sim 0.2\%\) high at high \(z\) for wall-loud non-adiabatic — **not** a systematic drop toward DESI).

**Needle:** mean AP **does not** slide from \(R_L\sim 5\) down to DESI Lyα \(\sim 4.66\).

### B. Scatter **does** grow with \(z\) when wall-loud + non-adiabatic

**Wall-loud soft envelope, non-adiabatic, \(\Omega=1\):**

| \(z\) | phase scatter \(R_{\mathrm{std}}/R_L\) |
|------:|--------------------------------------:|
| 0.3 | 0.6% |
| 0.7 | 1.5% |
| 1.0 | 2.4% |
| 1.5 | 4.2% |
| 2.0 | 6.2% |
| **2.3** | **7.5%** |

**Wall \(\xi^4\), non-adiabatic:** scatter 0.7% → **6.7%** by \(z=2.3\).

**Mid envelope, adiabatic:** scatter **falls** with \(z\) (old first-cut).

**Mid envelope, non-adiabatic:** scatter large (~7–10%) but **flat / not monotonically rising** with \(z\).

So Charles’s intuition is **partially confirmed**:

> With residual time-dependence that is **loud near the wall** and **non-adiabatic** photon transport, **phase scatter grows with lookback.**

That is a real needle move for **variance**, not for **mean bias**.

### C. \(\Omega\)-dependence appears only with non-adiabatic \(k_t\)

Adiabatic tables: all \(\Omega\) identical (endpoint \(A\) only).  
Non-adiabatic: \(\Omega=5\) vs \(\Omega=1\) differ — path history matters.

### D. Can a single phase hit DESI’s \(F\sim 4.66\)?

At \(z\sim 2.3\), \(R_L\sim 4.95\):

| Setup | \(\langle R\rangle\) | \(R_{\min}\) over phases |
|-------|----------------------|---------------------------|
| Wall-loud / non-ad | ~4.95–4.96 | ~4.4–4.5 |
| Mid / non-ad (\(\Omega=5\)) | ~4.94 | **~2.9** (extreme phase) |

Phase **minima** can undershoot DESI; **phase-averaged** survey-like number stays on \(R_L\).  
A real catalog averages many lines of sight / phases → mean, not min.

---

## How to read this for the big project

| Question | Intermediate answer |
|----------|---------------------|
| Does time-live *automatically* fix high‑\(z\) mean AP? | **No** (still) |
| Does anything grow with \(z\) as guessed? | **Yes — phase scatter**, if wall-loud + non-adiabatic |
| Is full Einstein+AP still the decisive instrument? | **Yes** for a *derived* residual and a stable mean shift |
| Did intermediates earn more work? | **Yes, modestly** — non-adiabatic + wall-loud is the interesting corner; mid+adiabatic is a dead end for the gap |

**Not earned yet:** multi-month full time-live Einstein solver *solely* to chase mean BAO AP — mean needle still nailed to \(R_L\) under FREE monochromatic residual.

**Earned:** if building further, prioritize

1. non-adiabatic light,  
2. residual amplitude near deep shells (wall sector),  
3. eventually **derived** \(A(t,r)\) (or \(\phi(t,r)\)) so envelope is not FREE.

---

## One-line

**Intermediates: wall-loud + non-adiabatic residual oscillation makes AP **phase scatter grow with \(z\)** (intuition confirmed for variance); phase-averaged \(R\) still sits on static \(R_L\) and does not drop to DESI’s high‑\(z\) \(F\) — mean gap needs more than a FREE 5% cosine.**
