# Native \(D_A\) on the simple metric — root-of-root derive

## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 (header retrofit) |
| **Mode** | DERIVE |
| **Slice scope** | chart origin simple metric |
| **Observing or targeting?** | OBSERVE |
| **Comparator scaffolds** | NONE |
| **Verifier status** | see body |
| **Build-on grade** | **CONDITIONAL** |
| **Re-run commands** | see body / N/A |

### Premise ledger

| Item | Role | Tag | Enters claim? |
|------|------|-----|---------------|
| See body | full ledger | mixed | Y |

### What is NOT claimed

- Physics canon. Hygiene grade ≠ nature proof.
- Scope wider than slice above.

### Do not build on (if any)

- CHOSE/explore items without restating premises.

---


**Date:** 2026-07-09 · **Mode: DERIVE (geometry only)**  
**Prior:** `simple_metric_sne_validator_reconstruct_MAP.md`  
**Stance:** Earlier SNe stack had **some correct components**, not a complete model.  
**Status:** PROVISIONAL geometric result for **observer at chart origin**.

---

## 0. Question

Is \(D_A = r\,e^{-\phi}\) (or “old \(r\) is \(D_M\)-like”) **native** on

\[
ds^2=-e^{-2\phi}c^2 dt^2+e^{2\phi}dr^2+r^2 d\Omega^2,
\]

or is geometric \(D_A=r\) forced and the old formula something else?

---

## 1. Geometric angular diameter distance (observer at origin)

**Chart:** observer at \(r=0\), \(\phi(0)=0\) by gauge (relational seat = chart origin).  
**Source:** sphere \(r=r_s\).

**Definition:** \(D_A = L_\perp / \Delta\theta\), with \(L_\perp\) proper transverse size at the source and \(\Delta\theta\) angle at the observer.

| Step | Content | Status |
|------|---------|--------|
| Area of sphere | \(4\pi r^2\) from \(g_{\theta\theta}=r^2\) | Identity |
| Transverse stick at \(r_s\) | \(L = r_s\,\mathrm{d}\theta_{\mathrm{coord}}\) | Identity |
| Radial null generators from origin | angular coordinates constant along rays (SSS) | Standard |
| Observed angle at origin | \(=\mathrm{d}\theta_{\mathrm{coord}}\) | Chart origin |
| **\(D_A\)** | \(L/\Delta\theta = r_s\) | **FORCED** |

\[
\boxed{D_A = r
\quad\text{(simple metric, observer at chart origin)}}
\]

**Not forced as \(D_A\):** \(r e^{-\phi}\), \(\int e^{\phi}dr\), free functions.  
Those are **other** lengths (or counters); they are not the area-based angular diameter distance.

---

## 2. Etherington (unchanged)

Banked: \(d_L=(1+z)^2 D_A\) with \(1+z=e^{\phi}\) (static).

With §1:

\[
\boxed{d_L = r\,(1+z)^2 = r\,e^{2\phi} = r\,g_{rr}}
\]

The old corpus form \(d_L=r\,e^{\phi}=r\sqrt{g_{rr}}\) is short **one** factor of \(e^{\phi}=\sqrt{g_{rr}}\).

---

## 3. Clean naming: what the old formula *was*

Define the intermediate Etherington length (standard ladder):

\[
D_M \equiv (1+z)\,D_A.
\]

With \(D_A=r\):

\[
\boxed{D_M = r\,(1+z)}
\qquad
d_L = (1+z)\,D_M = r\,(1+z)^2.
\]

**Old validator wrote:**

\[
d_L^{\mathrm{(old\ label)}} = r\,(1+z).
\]

**Geometric content of that expression:** it is exactly \(D_M\), not \(d_L\).

| Object | Formula when \(D_A=r\) | Old scorecard |
|--------|----------------------|---------------|
| \(D_A\) | \(r\) | called \(D_A=r\) (OK) |
| \(D_M\) | \(r(1+z)\) | **labeled \(d_L\)** (ERROR) |
| \(d_L\) | \(r(1+z)^2\) | not used |

**Root of the root (this chart):**  
not “\(D_A\) should have been \(r/(1+z)\)” as a new metric fact, but  

> **\(r(1+z)\) is the correct \(D_M\); it was mislabeled as luminosity distance — missing the last \((1+z)=\sqrt{g_{rr}}\).**

The reconstruct MAP’s “pointer” \(D_A=r/(1+z)\) is the **counterfactual** that would keep the *old numerical \(d_L\)* under true n=2. It is **not** the native geometric \(D_A\). It would require denying §1.

---

## 4. Correct components vs not (updated, partial model)

Aligned with Charles: **some components correct; model not complete.**

| Component | Verdict |
|-----------|---------|
| Simple reciprocal metric | Keep as live spine |
| \(1+z=e^{\phi}\) | Keep |
| Areal \(r\), geometric \(D_A=r\) at chart origin | Keep (this derive) |
| \(D_M=r(1+z)\) as algebra | **Correct expression** (old formula’s body) |
| Calling that \(d_L\) | **Wrong** (root) |
| Locked cubic \(\phi(r)\) form | **Ansatz** — may contain signal; not FE-complete |
| Cubic under true \(d_L=r(1+z)^2\) | **Fails** SNe hard (χ²/dof≈4.6) — so cubic+areal+\(d_L\) is not the full sky model |
| Hyperbolic \(x=X\tanh\phi\) + J1 + n=2 | Form OK; **numeric shape fail** as packaged |
| Free \(D_A(r)\) | Still quarantined — not needed to state the root |

---

## 5. What this closes / opens

### Closes

- Hope that native geometry secretly sets \(D_A=r/(1+z)\) while keeping \(g_{\theta\theta}=r^2\) and chart-origin observer — **no**, not without redefining \(D_A\).
- “Just fix the root on the same cubic \(r(z)\)” as a complete SNe theory — numbers already show that fails.

### Opens (honest next)

1. **Profile:** under true \(d_L=r(1+z)^2\), what \(\phi(r)\) (or sourced FE solution) does the metric actually give? (matter source / closure — prior Q1, not SNe-tuned.)  
2. **Hyperbolic join:** if \(r\not\equiv x\), compositional distance ≠ areal — still not free \(D_A\), but reopens J1.  
3. **Off-center / multi-observer atlas:** this note is **chart origin only**. Relational isotropy says each observer is origin of *their* chart; if that chart is always the simple form, §1 applies per observer. A different metric ansatz in observer frame would need a separate derive.  
4. **Mine old cubic as \(D_M(z)\) shape only:** old fit says \(D_M^{\mathrm{(emp)}}\approx r_{\mathrm{cubic}}(z)\,(1+z)\) tracked data *if* used as \(d_L\). Under correct naming, that would mean they fitted **\(d_L\approx D_M\)**, i.e. data were matched to something that should have been one power short — so the cubic \(r(z)\) is **not** automatically the true areal \(r(z)\). Treat cubic coefficients as **historical clue**, not as validated \(r(z)\).

---

## 6. One-line

**On the simple metric with the observer at the chart origin, geometric \(D_A=r\) is forced; \(d_L=r(1+z)^2\). The old SNe formula \(r(1+z)\) is the correct \(D_M\), mislabeled as \(d_L\) (one missing \(\sqrt{g_{rr}}\)). That is a real correct component; it is not a complete model, and it does not license \(D_A=r/(1+z)\) as native geometry.**
