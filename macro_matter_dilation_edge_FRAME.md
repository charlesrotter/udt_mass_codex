# FRAME — Matter is dilated toward the edge (correction to dust probe)

**Date:** 2026-07-08 · **Charles:** remember the matter will be dilated as it moves toward the edge.  
**Status:** Binding physical reminder for macro matter; corrects φ-blind dust probe as incomplete.

---

## 1. What was missing

The FREE dust probe used:

```text
L_m = −ρ(r) D_A²     (no φ)
```

so **EL_φ was vacuum-identical** and dust only bent `D_A`. That is **φ-blind matter**.

In UDT, **position is dilation**. Toward the edge φ rises (higher redshift). Matter **there is not the same as matter at the observer** for clocks, energies, and how it sources geometry. A probe that ignores that is missing the theory’s main character.

---

## 2. What “dilated toward the edge” means (lay)

| At center (φ≈0) | Toward edge (φ large) |
|-----------------|------------------------|
| Reference clocks | Clocks run slow (dilation) |
| Rest energy / rates “full” | Energies **redshifted** relative to the center chart |
| Source “full strength” | Gravitational source should **thin / weight** with dilation |

So as one moves out, matter is **dilated**, not a fixed ρ pasted on a curved background in a GR-style φ-blind way.

This is **not** an optional α-grid to improve fits; it is a **structural requirement** of positional dilation.

---

## 3. Metric-level weight (first honest implementation)

On the UDT metric, static observer 4-velocity satisfies:

```text
u^t = e^{φ}/c ,   u_t = −c e^{−φ}
```

Dust energy density in the **tt** stress scales as:

```text
T_{tt} ∼ ρ u_t u_t ∼ ρ c² e^{−2φ}
```

So the **energy** that gravitates, in center-chart components, carries **`e^{−2φ}`**.

**Corrected FREE probe (still a probe, not final native matter):**

```text
L_m = −ρ₀ f(r) D_A² e^{−2φ}
```

with `f(r)` a FREE radial profile (gauss/top-hat), `ρ₀` amount.

| Effect | |
|--------|--|
| **EL_φ** | Picks up **direct** matter term ∝ `ρ e^{−2φ}` (dilation feeds φ) |
| **EL_D** | Source ∝ `ρ e^{−2φ}` (thins as φ grows) |
| Toward edge | If φ rises, source **self-thins** — natural for a soft outer completion |

**Tag:** weight `e^{−2φ}` is **THEORY-motivated** from static dust `T_{tt}` on this metric (not a free α scan). Profile `f(r)` and ρ₀ remain FREE.

**Not claimed:** this is the unique UDT continuum matter (N1 defect continuum still open).

---

## 4. Relation to older α story

Thread-B style `α` with `e^{αφ}` is a **general weight**.  
Here **α = −2** on the density is singled out by **static energy redshift / u_t**, not by fit.

P16 (spin minimal coupling) is a **different** question — do not conflate.

---

## 5. Expected consequence for bootstrap / closure

Self-thinning toward large φ may:

- Help **cap** or **shape** the outer source without hand-tuned outer BC  
- Change the M-window vs φ-blind dust  
- Make “vacuum exterior match” more natural (source → 0 as φ grows)

Re-run closure/match diagnostics with dilated dust — see `macro_pathB_dilated_dust_observe.py`.

---

## 6. One-line

**Matter toward the edge must carry dilation (energy ∼ e^{−2φ} for static dust); φ-blind ρ was an incomplete probe and is superseded for edge/mass work.**
