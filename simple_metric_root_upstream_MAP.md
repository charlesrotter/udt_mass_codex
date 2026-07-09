# MAP — Where upstream is the root problem most likely?

**Date:** 2026-07-09 · **Mode: MAP / PONDER**  
**Stance:** Earlier SNe stack had **some** correct components, not a complete model.  
**Banked:** n=2; chart-origin \(D_A=r\); old \(r(1+z)=D_M\) mislabeled as \(d_L\).  
**Not:** free \(D_A\), SNe-tuned knobs, metric rewrite as first move.

---

## 0. Separate two “roots”

| Problem | What it is | Status |
|---------|------------|--------|
| **Root A** | Old scorecard used \(d_L=r(1+z)\) instead of \(r(1+z)^2\) | **Diagnosed** — \(D_M\) mislabeled as \(d_L\); one missing \(\sqrt{g_{rr}}\) |
| **Root B** | Under **correct** optics, neither locked cubic nor hyp+J1 matches Pantheon shape | **Live** — this is what still needs an upstream home |

Root A explains the **false win**.  
Root B is why elegance is not yet on the sky. **Do not hunt Root A again as if it fixed Root B.**

---

## 1. Ranked upstream suspects (for Root B)

Likelihood = how well it explains the facts we already have, without inventing fluids.

### #1 — **Profile / source (what \(\phi(r)\) or \(r(z)\) actually is)** — **MOST LIKELY** (sharpened 2026-07-09)

**Why it sits here**

- Native optics + \(D_A=r\) are now tight: \(d_L=r(1+z)^2\) is forced at chart origin.  
- Both **tested** \(r(z)\) packages fail under that law:
  - locked cubic → χ²/dof ≈ 4.6  
  - hyperbolic J1 \(x=X\tanh\phi\) → χ²/dof ≈ 2.2, systematic high-\(z\) over-distance  
- Cubic was always **ansatz** (D-POLY-1), irregular at 0 — never a completed FE solution.  
- Sourceless vacuum already fails under both n=1 and n=2 (prior).  
- Solver-first: mismatch indicts **incomplete solve of the macro field** (matter/closure/source) before the metric spine.

**OBSERVE tile:** `simple_metric_sourced_profile_observe_results.md`  
Compensated + dilated dust (regular origin): high \(z\) possible, SNe demo χ²/dof~10.  
**Structural:** \(\phi\sim ar^2\Rightarrow d_L\sim\sqrt{z}\) at low \(z\) — fails linear Hubble; **not** fixable by ρ amount/width.

**Free \(D_A\) unquarantine tile:** `simple_metric_freeDA_lowz_observe_results.md`  
Free \(D_A\) **does not** evade the parity: \(p\sim 1/2\) still; dilated quiet center freezes \(\phi=0\).  
Next inside #1: native **linear** low-\(z\) via origin/chart/operator (not free-\(D_A\) knobs).

**What “correct component” from the old stack remains**

- Metric + redshift law.  
- Algebra \(D_M=r(1+z)\).  
- Maybe a **rough idea** that a smooth stiff \(\phi(r)\) can exist — **not** the cubic coefficients as truth.

**Empirical shape clue (characterize, not fit):**  
If old numbers tracked true \(d_L\) by accident under wrong label, then under true law one would need roughly

\[
r_{\mathrm{true}}(z)\sim \frac{r_{\mathrm{cubic}}(z)}{1+z}
\]

so that \(r_{\mathrm{true}}(1+z)^2\sim r_{\mathrm{cubic}}(1+z)\). That is a **target shape for later observation of FE solutions**, not a knob.

**Hunt:** matter-sourced / closure-gated background under n=2; report what \(r(z)\) **emerges** — do not tune to Pantheon first.

---

### #2 — **Chart join J1 (\(r\equiv x\))** — **PLAUSIBLE for the hyp package**

**Why**

- Hyperbolic law is about **compositional** distance \(x=X\tanh\phi\).  
- Simple metric’s \(D_A\) is **areal** \(r\).  
- J1 identified them by default; that was **CHOSE**, not forced.  
- Wrong join ⇒ wrong \(d_L(z)\) even with right \(\phi\) and right n=2.  
- Does **not** require free \(D_A(r)\); it requires a **derived** \(r(x)\) or a proof they coincide.

**Why not #1 overall**

- Cubic failure is **not** a hyp-join issue; cubic already used areal \(r\).  
- So J1 can explain **hyp** miss; it does not by itself explain **cubic** miss under n=2.  
- Root B has **two** failed packages → shared trunk is more likely **profile/source** (or static regime) than J1 alone.

**Hunt:** either derive \(r(x)\) from the metric + composition, or drop J1 and keep hyp only as kinematic \(x(\phi)\) with areal \(r\) from FE.

---

### #3 — **Static SSS as the whole SNe sky** — **OPEN, not first drill**

**Why it could matter**

- Full n=2 derivation uses **static** metric (arrival-rate = energy redshift).  
- Elegant frame is relational dilation; static chart is a **slice**.  
- If the real sky needs time-live structure, static \(d_L(z)\) is the wrong observable map.

**Why not first**

- Blast radius huge; no positive lead yet that static is the √ scar.  
- Fix profile under static first; if a good static profile **never** appears with complete FE, **then** reopen dynamics.

---

### #4 — **Metric exponents / meaning of \(\phi\) in \(g_{\mu\nu}\)** — **DEEP TRUNK, LAST among geometry**

**Why Charles’s instinct is fair**

- Every √ is \(e^{\phi}\) or \(\sqrt{g_{rr}}\).  
- A wrong power in the line element would cascade through redshift, \(D_A\) story, and kinetics.

**Why not first**

- Current \(D_A=r\) and \(1+z=e^{\phi}\) are **internally consistent** on the held metric.  
- Changing \(e^{\pm 2\phi}\) reopens R1–R3 founding — high blast, Principle-7 territory only after #1–#2 fail cleanly.  
- Old n=1 error is already explained as **misuse of \(\sqrt{g_{rr}}\) in \(d_L\)**, not as wrong metric.

**Hunt only if:** complete sourced static solves still cannot produce any acceptable \(r(z)\) family under true n=2, and J1 is settled.

---

### #5 — **Reopen n=1 / free \(D_A\) / SNe-tuned cubic** — **REJECT as upstream fix**

- n=1 is not an escape (banked).  
- Free \(D_A\) quarantined.  
- Re-fitting cubic under n=2 is **targeting**, not uncovering.

---

## 2. Best single story (provisional)

```text
Upstream most likely:
  incomplete macro PROFILE (φ or r from FE + source/closure)
    under correct optics (D_A=r, d_L=r(1+z)²)

Secondary (hyp branch):
  J1 may mis-join compositional x to areal r

Already solved (old false win):
  r(1+z) was D_M, labeled d_L

Not first:
  rewrite metric exponents; dynamic SSS; free D_A
```

**One breath:**  
The metric spine and n=2 look fine; the old bug was calling \(D_M\) the luminosity distance.  
What we still lack is a **theory-born** \(r(z)\) (or \(r(x),\phi\)) under that spine — the cubic was a partial, non-FE stand-in that only looked good under the wrong label.

---

## 3. Recommended sequence (purist vs easy)

| Order | Action | Why |
|------:|--------|-----|
| 1 | Hold \(D_A=r\), \(d_L=r(1+z)^2\) fixed | Do not re-litigate Root A |
| 2 | **OBSERVE** sourced / closure-gated static backgrounds: what \(r(z)\) emerges? | #1 suspect |
| 3 | Compare emerged \(d_L(z)\) to data **after** structure exists (demo, not knob) | Charles guardrail |
| 4 | In parallel thin tile: **J1 stress** — can \(r(x)\) be derived or must it stay identity? | #2 for hyp |
| 5 | Only if 2–4 stall: metric \(\phi\)-power / dynamic reopen | #3–#4 |

**Easy wrong path:** re-fit cubic or hyp scale to Pantheon under n=2.  
**Pure path:** complete the profile from the metric + source, then look.

---

## 4. One-line

**Most likely upstream of the live SNe shape failure: not the metric’s \(D_A=r\) and not n=2, but the unsolved / ansatz macro profile (and secondarily the hyp areal join); the old root was labeling \(D_M\) as \(d_L\), which explained the false success but does not supply the true \(r(z)\).**
