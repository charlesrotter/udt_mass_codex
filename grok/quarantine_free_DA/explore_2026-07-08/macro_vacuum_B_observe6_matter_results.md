# OBSERVE-6 — Dilated dust on option B (does matter tame hard/soft?)

**Date:** 2026-07-08  
**Mode:** OBSERVE (not target).  
**Equations:** `macro_FE_matter_dilated_B.md`  
**Script / data:** `macro_vacuum_B_observe6_matter.py`, `macro_vacuum_B_observe6_matter_data.json`  
**Prior:** O1–O5 vacuum throat map.  
**Status:** PROVISIONAL — one continuum probe, not native unique matter.

---

## Premise ledger

| Item | Tag |
|------|-----|
| W=1, free D, Z=1 representative | CHOSE / FREE |
| \(L_m = -\rho D^2 e^{-2\phi}\) dilated | CHOSE minimal continuum (Charles dilation) |
| φ-blind \(L_m=-\rho D^2\) | CONTROL only (known incomplete) |
| ρ = gaussian about throat (or off-throat), prescribed | FREE profile — not dynamical fluid |
| Throat IVP seeds | FREE family |
| Observing or targeting? | **Observing** — no sky fit |

---

## Equations (dilated)

\[
(Z D^2\phi')' = 4 e^{-2\phi}(D')^2 + 2\rho D^2 e^{-2\phi}
\]

\[
(e^{-2\phi} D')' = -\tfrac{Z}{4} D(\phi')^2 + \tfrac12 \rho D e^{-2\phi}
\]

Matter **directly sources φ** and adds a positive push to the expansion flux F.

---

## What we saw (scoped)

### 1. Hard side (+φ′ outward): dilated dust does **not** soften the pinch

For \(u_*>0\), vacuum already pinches. **Adding dilated ρ makes the pinch earlier** (smaller \(r_{\mathrm{pinch}}\)):

| \(u_*\) | vacuum \(r_{\mathrm{pinch}}\) | dilated ρ=1 | ρ=5 | ρ=10 |
|---------|------------------------------|-------------|-----|------|
| 0.05 | ~18.6 | ~3.8 | ~2.1 | ~1.8 |
| 0.1 | ~9.8 | ~3.5 | ~2.1 | ~1.8 |
| 0.2 | ~5.4 | ~3.1 | ~2.0 | ~1.7 |

**Plain:** more dilated dust on the hard side **hastens** the shutdown — it pumps φ up (extra RHS on FE-φ), which is the direction that pinches.

### 2. Soft side (−φ′ outward): moderate dilated dust can **flip** soft → hard

| Setup | Fate to large r |
|-------|-----------------|
| vacuum \(u=-0.1\) | plateau \(D\approx0.94\), φ slides down |
| dilated ρ=0.1, \(u=-0.1\) | still long-lived (D even grows) |
| dilated ρ≥0.5, \(u=-0.1\) | **pinches**; φ ends **up** (~3.4) |
| dilated ρ≥1, \(u=-0.2\) | pinches |

**Plain:** enough dilated matter at the throat **overpowers** the soft-side story and drives a hard-side-like end.

### 3. φ-blind control “survives” by inflating D — not trusted as theory

Blind dust with moderate ρ: **no pinch**, D grows large (tens→hundreds). That matches the old warning: φ-blind continuum can produce **artifact survival / expansion** without true dilation coupling.

**Use only as contrast**, not as the tamed universe.

### 4. Off-throat dilated lump (ρ peak at r=3, \(u=0.1\))

| ρ₀ | Fate |
|----|------|
| 1, 5 | still pinch (~r=5) |
| 20 | reaches r=40 with large D (matter-dominated push) |

Heavy enough off-center dilated density can prevent pinch in this IVP — but via **strong D growth**, not a gentle “sky-like” profile. Not scored as success; just noted.

---

## Answer to the motivating question

> Do we need matter to tame the angular sector?

| Claim | After O6 |
|-------|----------|
| Vacuum hard/soft is weird vs sky | still true |
| **This** minimal dilated dust tames it into something sky-like | **Not observed** |
| Dilated dust reduces hard-side violence | **Opposite** — often worse (earlier pinch) |
| Matter can change the phase portrait a lot | **Yes** |
| φ-blind “tames” by D blow-up | Yes, and **distrusted** |

**Honest status:** first continuum probe did **not** deliver “matter calms the bulge into a normal cosmos.” It showed dilated ρ is a **strong driver of φ**, often reinforcing the hard fate.

That does **not** kill matter-in-general — only this **prescribed gaussian dilated dust on throat IVPs**.

---

## What this does *not* say

- Not “matter never works”  
- Not “fallback C now mandatory” (not a vacuum blocker; matter probe failed to tame, different issue)  
- Not a sky constraint on Z or ρ₀  
- Not unique native matter (geometric channels, dynamical fluid, different weight still open)

---

## Solver-first checklist (mismatch to “tame” hope)

1. **Left out?** Dynamical ρ (continuity), pressure, free BVP vs IVP, compensated hybrid C, other \(L_m\) weights  
2. **Numeric?** Unlikely — vacuum limits recovered; mono structure consistent  
3. **Frozen?** ρ shape prescribed FREE; only throat family  
4. **Whole space?** No — one profile class, Z=1, static  

⇒ **Incomplete continuum sector**, not “metric says no matter.”

---

## Incremental next (when ready)

1. **OBSERVE-7:** same FE, but ρ in a **ball** interior with outer vacuum (matched), not throat-centered gaussian — different question.  
2. **Fallback C probe:** compensated vacuum + dilated matter only as source of φ.  
3. **Ponder** with Charles: is “tame angular” the right ask, or “different seed/BVP”?  

Recommend brief **ponder** before another large scan — O6 is a real negative for the *naive* “sprinkle dilated dust on the throat” idea.

---

## Plain summary

We invited matter that **feels dilation**. On the empty bulge, that matter mostly **shoves φ harder**, so the side that already pinches pinches **sooner**, and the soft side can get **dragged into a pinch** too. The “dumb” non-dilated dust can keep spheres open by inflating them — but we already know that coupling is incomplete.  

So: **matter matters, but this first spoonful did not tame the angular sector into something that looks like home.** Next matter try needs a clearer setup — or a different packaging — not a bigger ρ knob on the same throat.
