# RESULT — Dilated matter toward the edge (Path B dust corrected)

**Date:** 2026-07-08 · **Status: PROVISIONAL**  
**Charles:** matter is dilated as it moves toward the edge.  
**Frame:** `macro_matter_dilation_edge_FRAME.md`  
**Script:** `macro_pathB_dilated_dust_observe.py`  

**Corrects:** φ-blind dust probe (`L_m=−ρ D_A²`) used in WP2 / closure / match.

---

## 1. Corrected probe

Static dust energy in the center chart scales as `T_{tt}∼ρ e^{−2φ}`.  
**Dilated probe:**

```text
L_m = −ρ₀ f(r) D_A² e^{−2φ}
```

| Tag | |
|-----|--|
| `e^{−2φ}` | THEORY-motivated (static `u_t`, energy redshift) |
| `f(r)`, ρ₀ | FREE profile/amount |
| Still not N1 native defect continuum | FREE probe |

**EL (CAS):**

- **EL_φ** gains **direct** matter: `+2 ρ D_A² e^{−2φ}` in the sympy convention of the script stack  
- **EL_D** source **thins** as `e^{−2φ}` when φ rises  

→ Toward the edge, if φ grows, matter **self-thins** (dilates away as a source).

---

## 2. Side-by-side (gauss r_c=1, Q₀=0.5)

| | **φ-blind** (old) | **Dilated e^{−2φ}** (corrected) |
|--|-------------------|----------------------------------|
| Vacuum-like low M | OPEN, φ∼2 | OPEN, φ∼2 |
| Medium M turns + MATCH_OK | **Yes** (M∼100–600) | **No** — **0 MATCH_OK** |
| Ceiling break φ≫2 | Strong (φ∼3–4) | **Weak** (φ climbs only slowly; max ∼3 at huge M) |
| COLLAPSE high M | Yes | Rare in this scan (mostly NO_TURN) |
| Vacuum exterior match after turn | 100% when turn exists | **N/A** (no qualifying turns) |

**Headline:**  
Putting Charles’s dilation back in **removes** the earlier “critical turn / MATCH_OK mass band.” That band was largely an artifact of **φ-blind** (non-dilated) dust staying strong at large φ.

---

## 3. Dilated scan detail (r_c=1, Q₀=0.5)

- **All 64** amount points: **NO_TURN** under improved outer-turn criteria  
- φ_max: **∼2.03 → ∼3.04** only at the highest ρ₀ (M up to ∼10⁵)  
- No COLLAPSE_INT in that family (source softens before it can over-crush in the same way)

**Q₀=0 dilated:** mostly COLLAPSE_INT or dead φ=0 at low M — dilated dust alone does **not** robustly bootstrap redshift the way φ-blind medium dust did.

**r_c=2 dilated:** again **0 MATCH_OK**, all NO_TURN in scan.

---

## 4. Physical reading

1. **Dilation toward the edge is the right correction** — φ-blind continuum was incomplete for UDT.  
2. **Self-thinning** makes outer source fade as φ rises → favors **smooth approach to vacuum-like exterior** without a sharp D' turn.  
3. Prior bootstrap “narrow close window” from φ-blind dust is **downgraded**: interesting numerics, **wrong matter weight**.  
4. Edge/`x_max` with dilated matter likely needs:  
   - different CLOSE definition (not D' turn), and/or  
   - **matching / BVP** with φ large and source naturally small, and/or  
   - **native** matter sector (N1), not only this dust probe.

---

## 5. What to keep / drop

| Keep | Drop / regrade |
|------|----------------|
| Path B vacuum results (no matter) | φ-blind CLOSE/MATCH mass bands as physical |
| Metric-form + dilation philosophy | “Dust turns = critical universe” |
| `e^{−2φ}` as default weight for static energy density probes | α free grids without metric reason |

---

## 6. Recommended next

1. **Redefine outer success** for dilated matter: e.g. source ∫ρ e^{−2φ}→0, φ→φ_∞ or φ floor, D'→const (S2), **without** requiring a turn.  
2. **BVP:** fix outer vacuum S2 data; shoot dilated M for match — test bootstrap under dilation.  
3. **N1** native continuum with dilation built in from channels.  
4. Do not re-run φ-blind mass tournaments.

---

## 7. One-line

**Dilated dust (∼e^{−2φ}) kills the φ-blind turn/MATCH_OK mass window: matter self-thins toward the edge, so earlier “critical close” was an incomplete-probe artifact; edge work must use dilation-aware matter and likely matching, not D'-turn alone.**
