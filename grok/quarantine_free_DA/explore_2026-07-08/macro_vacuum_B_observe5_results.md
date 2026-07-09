# OBSERVE-5 — Symmetries (±φ′) and long-lived asymptotics

**Date:** 2026-07-08  
**Mode:** OBSERVE.  
**Script / data:** `macro_vacuum_B_observe5.py`, `macro_vacuum_B_observe5_data.json`  
**Prior:** O4 (+u pinches, −u long-lived).  
**Status:** PROVISIONAL characterization.

---

## Premise ledger

| Item | Tag |
|------|-----|
| Vacuum B | locked |
| Symmetry tests: φ→−φ, r→−r | theory probes |
| Asymptotics: u_*<0 to r=500 | method bound |
| Observing or targeting? | **Observing** |

---

## 5b. Is ±φ′ only a chart convention?

### φ → −φ (same r, D)

| Check | Result |
|-------|--------|
| CAS | **Not** a symmetry — \(e^{-2\phi}\) weights flip to \(e^{+2\phi}\) |
| Numeric residual of \((-\phi,D)\) | rel residual \(O(1)\) (not a solution) |

**⇒ Not removable by renaming the sign of φ alone.**

### r → −r (reparametrization)

| Check | Result |
|-------|--------|
| CAS | **Is** a symmetry of the same FE |
| Effect | Flips signs of \(\phi'\) and \(D'\) |

### Two sides of one throat (the real story)

On a **single** throat seed with \(u_*>0\), integrate both ways:

| Diagnostic | Value |
|------------|-------|
| \(D\) even about throat (\(+r\) vs \(-r\) sides) | \(\max|\Delta D| \sim 10^{-4}\) (numeric) |
| \(\phi\) odd about throat | \(\max|\phi_{\mathrm{out}}+\phi_{\mathrm{in}}| \sim 10^{-5}\) |
| \(D\) of \((-u)\) outward vs \((+u)\) inward | **err = 0** (same profile) |

**Plain conclusion:**

There are **not** two unrelated families “\(+\phi'\) cosmology” vs “\(-\phi'\) cosmology.”

There is **one two-sided throat geometry** (approximately \(D\) even, \(\phi\) odd about the bulge):

- The side toward **increasing φ** → **finite-r pinch**  
- The side toward **decreasing φ** → **long outer life, \(D\to D_\infty\)**

Calling the seed “\(+u\) outward” or “\(-u\) outward” only chooses **which side of the same object you label as increasing chart radius.** The geometric split is **directed by the gradient of φ**, forced by the \(e^{\pm 2\phi}\) weights — a real dynamical arrow, not an arbitrary chart whim, and **not** undone by \(\phi\to-\phi\).

---

## 5a. Long-lived side asymptotics (\(u_*<0\) outward, to \(r=500\))

All tested cases: **reach r=500**, no pinch; **\(D\) plateau to machine flatness** in the late window (`D_std_last ~ 0`).

### \(D_\infty(Z)\) — independent of \(|u_*|\)

| \(Z\) | \(D_\infty\) (all \(u\in\{-0.05,-0.1,-0.2\}\)) | \(1-D_\infty\) |
|------|-----------------------------------------------|---------------|
| 1 | 0.93964 | 0.06036 |
| 2 | 0.88336 | 0.11664 |
| 4 | 0.78187 | 0.21813 |
| 8 | 0.61618 | 0.38382 |

**Structural reason (consistent with scale-out):**  
r-rescaling maps different \(|u_*|\) to the same unit-slope problem; only \(Z\) remains. Hence \(D_\infty/D_*=f(Z)\) only.

### φ asymptotics on the plateau

Late window: \(\phi \approx a + b\, r\) with \(b = u_{\mathrm{end}} < 0\) **nearly constant** (secular linear drop).

| Consistency sketch | |
|--------------------|--|
| \(D\to D_\infty\), \(v\to 0\), \(G\to G_\infty\neq 0\) | \(\phi' \to G_\infty/D_\infty^2 = const < 0\) |
| \(F' \to -(Z/4) G_\infty^2/D_\infty^3 < 0\) | \(F\) drifts negative |
| \(D' = F e^{2\phi}\) | \(\phi\to-\infty\) makes \(e^{2\phi}\to 0\) so \(D'\) can stay ~0 — **consistent** with plateau |

**Not proven as a theorem** — numeric + local consistency only.

### What “edge” is not (yet)

\(\phi\to-\infty\) as \(r\to\infty\) on this side is **not** automatically a physical finite-distance edge; it is unbounded chart radius with ever-deeper dilation (redshift factor \(e^{\Delta\phi}\) grows without bound along the ray). Different from the **pinch** side (finite \(r\), \(D\to 0\)).

---

## Refined vacuum map (O1–O5)

```text
Vacuum B, free D, throat (D'=0, D>0):

                    increasing φ  ──►  PINCH (D→0, finite r)
                   /
  [ throat bulge ]
                   \
                    decreasing φ  ──►  PLATEAU D→D_∞(Z), φ ~ −|b| r

Polar smooth origin: blocked
Flat (φ'=0): eternal D const
```

**Fallback C:** still not activated — vacuum B has a coherent two-sided solution class.

**Sources:** still not required for this structure to exist.

---

## What this does *not* say

- Not observer cosmology / which side we live on  
- Not a fit for \(Z\) from \(D_\infty\)  
- Not uniqueness of all vacuum solutions (only throat sector)  
- Not that matter will preserve this arrow  

---

## Incremental next (when ready)

1. **OBSERVE-6:** closed-form / ODE reduction for \(f(Z)=D_\infty/D_*\) (quadrature on the decreasing-φ side?).  
2. Pinch-side: universal \(\phi_{\mathrm{pinch}}(Z)\) (O4 cluster) — analytic?  
3. Still later: \(L_m\).

Recommend **6** if we stay vacuum; or stop and **ponder with Charles** before sources — the vacuum picture is now a clear two-sided object.

---

## Plain summary

Flipping the sign of φ does **not** leave the equations the same — dilation weights pick a direction.  
Flipping the radial coordinate does.  
So “rising-φ pinches / falling-φ survives” describes the **two sides of one throat**, not two theories: walk toward higher φ and the sphere shuts; walk toward lower φ and the size settles to a floor set only by \(Z\), while φ keeps sliding down linearly in these runs.
