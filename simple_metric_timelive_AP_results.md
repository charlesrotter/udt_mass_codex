## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE (first-cut time-live appearance) |
| **Question** | Recompute pure AP with time-live residual — does the high‑\(z\) gap grow? |
| **Build-on grade** | **LEAD** — **not** full Einstein time-live |
| **Machine** | `simple_metric_timelive_AP_out.json` · re-run: see script in session / regenerate from notes |

### Premise ledger

| Item | Tag |
|------|-----|
| Background residual L: \(A_0=1-r/X\) | WORKING |
| Time-live **ansatz** \(A=A_0\bigl(1+\varepsilon\,s(r)\cos(\omega t+\phi)\bigr)\) | **FREE** probe (not derived Einstein solution) |
| Envelope \(s=16\xi^2(1-\xi)^2\) (0 at centre & wall) | FREE |
| \(\varepsilon=0.05\), \(\Omega=\omega X\in\{0.5,1,2,5\}\) | FREE scan |
| Redshift approx: \(1+z=\sqrt{A_{\mathrm{obs}}/A_{\mathrm{em}}}\) along null \(t(r)\) | adiabatic / static-observer endpoints |
| Full Einstein backreaction / multipole self-gravity | **NOT** in this solve |
| Observing or targeting? | OBSERVE whether gap grows with \(z\) |

### What this is **not**

- Not the finished “time-live native S²” cell solver.  
- Not a refit of DESI BAO.  
- Not a mechanism patch to force high‑\(z\) AP onto data.

---

# Time-live recompute of pure AP (first cut)

## Context

Static residual L forces
\[
R_L=\frac{\Delta z}{\theta}=z+\frac{z^2}{2}
\]
(\(X\)-independent). That matches low‑\(z\) LRG AP and runs **high** vs high‑\(z\) BAO.

Charles: oscillations are time-dependent → high‑\(z\) lookback should feel more of that → gap might grow.

Existing repo “time-live on L” (`simple_metric_angular_timelive_L_*`) = **time-harmonic probe multipoles on frozen L**, densifying as optical wall depth \(\to\infty\). Useful background, **not** an AP recompute.

---

## What we ran

1. **Null rays** inward on reciprocal metric with prescribed \(A(t,r)\).  
2. **Proper stick** at emission: \(\theta=\ell/r\), \(\Delta z\) from two ends.  
3. **Phase average** over emission phase \(\phi\) (16 samples).  
4. **Sanity:** \(\varepsilon=0\) recovers \(R_L\) to \(\sim 10^{-4}\).

---

## Results (character)

### 1. Phase-averaged \(R\) stays on \(R_L\)

For \(\varepsilon=0.05\) and all scanned \(\Omega\):

\[
\langle R\rangle_\phi \;\approx\; R_L(z)
\]
to better than **0.3%** at every \(z\) from 0.3 to 2.3.

**Small monochromatic residual oscillation does not systematically pull mean AP off static L** in this ansatz.

### 2. Phase scatter does **not** grow with \(z\) — it **shrinks** at high \(z\)

| \(z\) | \(R_{\mathrm{std}}/R_L\) (phase scatter) |
|------:|------------------------------------------:|
| 0.3 | ~3% |
| 0.5 | ~1.4% |
| 1.0 | ~2.7% |
| 2.0 | ~1.0% |
| 2.3 | ~0.7% |

**Why (important):** the FREE envelope \(s(r)\to 0\) at the wall. High‑\(z\) shells sit near \(A\to0\), where we **forced** the oscillation to die. So high‑\(z\) sources feel **less** of this particular time-live decoration, not more.

### 3. No \(\Omega\) dependence in the adiabatic readout

All \(\Omega\) gave **identical** tables. Reason: redshift used
\[
1+z=\sqrt{A(t_o,r_o)/A(t_e,r_s)}
\]
depends on **endpoints**. With \(s(0)=0\), \(A_{\mathrm{obs}}\approx 1\). Path history and \(\omega\) drop out of this approximation. A true non-adiabatic / \(k_t\)-evolution treatment could reintroduce \(\omega\); **not done here**.

### 4. Optical lookback still grows with \(z\)

On static L:
\[
\frac{t_{\mathrm{opt}}}{X}=2\ln(1+z),\qquad
\text{phase }\sim 2\Omega\ln(1+z).
\]
Lookback **does** grow — but in this ansatz it does not drive a growing AP gap, because of (2)–(3).

---

## Answer to Charles’s intuition

| Intuition | This first-cut |
|-----------|----------------|
| Oscillations are time-dependent | Assumed (prescribed) |
| High \(z\) = deeper lookback | Yes (\(t_{\mathrm{opt}}\uparrow\)) |
| Therefore high‑\(z\) **gap to data** should grow | **Not shown** — mean \(R\) stays on \(R_L\); scatter shrinks when \(s\to0\) at wall |
| Static L is the zero mode | Supported for **mean** AP under small monochromatic residual |

So: **time-live as “small residual oscillation on L” does not, by itself, open a high‑\(z\) hole in \(R_L\).**  
The high‑\(z\) BAO tension with static \(R_L\) is **not cured and not explained** by this probe.

The densification result (infinite optical cavity) remains a separate structural fact: time-live **probe** towers densify at the wall; that is about mode spacing, not yet about \(\Delta z/\theta\).

---

## What a *real* time-live solve would still need

| Step | Status |
|------|--------|
| Prescribed \(A(t,r)\) AP | **This tile** |
| Non-adiabatic photon \(k_t\) along path | OPEN |
| Envelope / modes **derived** (not FREE \(s(r)\)) | OPEN |
| Full Einstein residual dynamics + backreaction | OPEN (heavy; anti-hang) |
| Local finite cavity (discrete \(\omega\)) vs filled wall continuum | Side corridor already scoped |

If residual oscillation **peaks at large depth** (not vanishing at the wall), high‑\(z\) scatter could reverse and grow — that would be a different FREE envelope or a derived mode shape.

---

## One-line

**First-cut time-live AP on L (prescribed 5% residual oscillation): phase-averaged \(\Delta z/\theta\) stays on static \(R_L\); scatter does not grow with \(z\) when the envelope dies at the wall — so “time-dependent oscillations ⇒ high‑\(z\) gap grows” is not confirmed by this solve; full Einstein time-live remains open.**
