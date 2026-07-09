# RESULT — Improved closure window (M-bracket, outer turn after expansion)

**Date:** 2026-07-08 · **Status: PROVISIONAL**  
**Contract:** `macro_pathB_dust_closure_window_CONTRACT.md`  
**Script:** `macro_pathB_dust_closure_window.py`  
**Parents:** WP2 dust observe · native matter edge MAP  

**Dust = FREE probe on Path B — not fundamental UDT matter. No SNe.**

---

## 1. Improved CLOSE definition (as run)

All required:

1. `D_max / D_0 ≥ 3` (real expansion)  
2. `D'` crosses `+ → ≤0` after that growth  
3. `r_turn ≥ 2 r_c` (not core-stuck)  
4. No crash to `D→ε` as the outcome class  

Labels: **OPEN** / **CLOSE** / **COLLAPSE**.  
φ ceiling break recorded but **not** required for CLOSE.

---

## 2. Primary family — gauss `r_c=1`, `Q₀=0.5`

Sorted by mass `M = ∫ 4π D²ρ dr`:

| Class | n | M range (probe units) |
|-------|--:|------------------------|
| OPEN | 57 | ~0.19 – 818 (mostly low M; some high holes) |
| **CLOSE** | **20** | **~79 – 658** |
| COLLAPSE | 11 | ~256 – 817 (upper end) |

**Transitions (along increasing M):**

```text
last OPEN before first CLOSE:   M ≈ 72
first CLOSE:                    M ≈ 79
first COLLAPSE after CLOSE:     M ≈ 256
```

**Bootstrap-shaped ladder (this family):**

```text
M ≲ 70     →  OPEN (vacuum-like / free expansion)
M ≳ 80     →  CLOSE candidates appear (outer turn after growth)
M ≳ 250    →  COLLAPSE mixes in; high-M mostly dies
```

**Not a single spike:** CLOSE spans ~0.9 dex in M with **gaps** (some M in the band still OPEN).  
So: **threshold + upper mess**, not “one exact mass only.”

Sample CLOSE:

| M | ρ₀ | ratio Dmax/D0 | r_turn | φ_max |
|--:|---:|--------------:|-------:|------:|
| 79 | 2.65 | 109 | 2.22 | 2.97 |
| 113 | 3.78 | 221 | 2.11 | 3.30 |
| 199 | 6.43 | 306 | 2.22 | 3.97 |
| 272 | 8.63 | 382 | 2.03 | 4.19 |
| 452 | 13.8 | 107 | 2.47 | 4.09 |

All CLOSE here also **break vacuum φ∼2** (φ_max ≳ 3).

---

## 3. Cross-checks

### Matter-only seed `Q₀=0` (gauss rc=1)

| | |
|--|--|
| first CLOSE | M ≈ **101** |
| CLOSE band | ~101 – 660 (2 clusters) |
| COLLAPSE after | M ≈ **290** |

Same **order of magnitude** onset as Q₀=0.5 (M~80–100), so the window is not an artifact of a large initial φ' alone.

### Top-hat `r_c=1.5`, Q₀=0.5

Under the **strict** outer-turn cuts: almost no CLOSE (**n=1**, M~461).  
Many runs OPEN with high φ or COLLAPSE.  

**Shape matters** for counting CLOSE — gauss family is much more “turn-friendly” than top-hat under R_sep=2 and R_exp=3.  
⇒ Do **not** claim a universal M* from one profile.

### Larger core gauss `r_c=2`, Q₀=0.5

CLOSE M ∈ ~**92 – 369** (n=6); onset again M~**90**.  
`M/r_c` onset ~46 (different scaling) — raw M more stable across r_c=1 vs 2 than M/r_c for onset (~80–90 vs 46).

### Sensitivity to R_exp

On a 24-point subset, R_exp ∈ {2,3,5} gave the **same** n_CLOSE=2 and M∈[169,220] — coarse; primary dense scan is the better map.

---

## 4. Scorecard vs bootstrap hunch

| Hunch | Verdict under improved CLOSE |
|-------|------------------------------|
| Light masses stay open / vacuum-like | **YES** (M ≲ 70–90) |
| Only special amounts “work” | **PARTIAL** — band with gaps, not a unique M |
| Heavy fails | **YES** (collapse dominates high M) |
| Narrow critical window | **Onset is sharp-ish**; width is **wide (~1 dex)** with intermittency |
| Profile-independent | **NO** — top-hat almost kills CLOSE count |

**Charles bootstrap idea:** still a **good lead** at the level of **open → structured → collapse**, not yet a single critical mass theorem.

---

## 5. What this does *not* establish

- A physical universe mass in SI units  
- `φ→∞` edge  
- That dust is UDT matter  
- That CLOSE = derived junction/matching  
- Uniqueness under all FREE thresholds (R_exp, R_sep)

---

## 6. Recommended next (after this)

1. **Matching exterior:** at turn, glue to Path B vacuum (ρ=0) and test continuity — closer to limit/`x_max` story.  
2. **Tighten intermittency:** denser M scan only in M∈[70,300]; map OPEN holes inside the band.  
3. **Invariant search:** does a combination other than M (e.g. M/φ_max, action) collapse the band?  
4. **N1 native matter** — so success is not owned by FREE dust.  
5. Verifier if any CLOSE claim is to be banked harder.

---

## 7. One-line summary

**With “outer turn after real expansion,” Path B+dust shows a sharp-ish open→close onset near M~80–100 and collapse at high M, but CLOSE is a gappy band (~1 dex), not a single mass — bootstrap-shaped, profile-sensitive, still a probe.**
