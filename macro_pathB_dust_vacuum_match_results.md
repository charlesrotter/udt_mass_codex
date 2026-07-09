# RESULT — Dust interior → Path B vacuum exterior match at turn

**Date:** 2026-07-08 · **Status: PROVISIONAL**  
**Contract:** `macro_pathB_dust_vacuum_match_CONTRACT.md`  
**Script:** `macro_pathB_dust_vacuum_match.py`  
**Parents:** closure-window results · WP2 dust  

Dust = **FREE probe**. Matching = C⁰ state handoff + vacuum Path B integration.

---

## 1. Procedure

1. Integrate **dust on** from flat core.  
2. If **qualifying turn** (expand ≥3×, `r_turn≥2 r_c`, `D'→≤0`): record state.  
3. Continue from that state with **ρ≡0** (vacuum Path B) to `r_ext ≈ max(r_t+8, 3 r_t)`.  
4. **MATCH_OK** if exterior stays finite, no D-floor crash, no φ runaway.  
5. Else **MATCH_FAIL** / **NO_TURN** / **COLLAPSE_INT**.

---

## 2. Headline

### Among all interiors that achieve a qualifying turn:

```text
MATCH_OK rate = 100%
MATCH_FAIL    = 0
```

(across primary + Q₀=0 + r_c=2 scans)

**So vacuum matching does not further filter the mass window.**  
If the interior turns “properly,” the Path B vacuum exterior **always** accepts the data and stays healthy in this lab (mild φ drift, D stays positive).

The bottleneck remains: **getting a qualifying turn at all** (NO_TURN vs MATCH_OK), not exterior rejection.

---

## 3. MATCH_OK mass windows

| Family | MATCH_OK M | n | Δlog₁₀ M |
|--------|------------|--:|---------:|
| gauss r_c=1, Q₀=0.5 | **~108 – 655** | 20 | 0.78 |
| gauss r_c=1, Q₀=0 | **~58 – 641** | 17 | 1.05 |
| gauss r_c=2, Q₀=0.5 | **~92 – 369** | 6 | 0.60 |

**Onset (first MATCH_OK)** still ~ **M ~ 60–110** depending on seed.  
**Width** still **~0.6–1 dex**, with NO_TURN holes inside the broad mid-mass range.

Exterior diagnostics on MATCH_OK samples: typically `Δφ_ext ~ 0–0.15` (no blowup), `D` remains O(10–100).

---

## 4. Class counts (primary: rc=1, Q₀=0.5)

| Class | n | M span |
|-------|--:|--------|
| NO_TURN | 44 | light + some mid/high gaps |
| MATCH_OK | 20 | ~108–655 |
| MATCH_FAIL | **0** | — |
| COLLAPSE_INT | 11 | heavy |

---

## 5. Reading vs prior hopes

| Hope | Outcome |
|------|---------|
| Matching would **narrow** M to a thin critical band | **Not observed** — 100% of turns match |
| Matching would **reject** many turners | **No** |
| Bootstrap open → structured → collapse | **Still yes** (NO_TURN / MATCH_OK / COLLAPSE_INT) |
| Unique M* | **Still no** |

**Implication:** For this Path B + FREE dust system, “close” is decided almost entirely by **interior turn dynamics**. Vacuum exterior is a **soft landing**, not a sharp selector.

That weakens “critical mass from junction to vacuum” *for this probe*, unless the matching rule is hardened (e.g. require exterior `D'→v_*`, or `φ→φ_∞` with constraint, or Israel-type jump from a thin shell).

---

## 6. What would harden matching (if continuing this path)

| Harder match rule | Why it might select M |
|-------------------|------------------------|
| Exterior `D' → 0` asymptotically | Stronger than “doesn’t die” |
| Exterior = exact S2 vacuum (`φ=const`, `D''=0`) within tolerance | Discrete targets |
| Derived junction (discontinuity allowed only if theory says so) | Needs derivation |
| E-φ∞ on exterior | Vacuum Path B resists high φ |

---

## 7. Recommendation after this result

1. **Stop expecting C⁰ vacuum handoff alone to pick unique M** — it won’t in this lab.  
2. Either:  
   - **Accept band-like structure** as the probe’s truth and move to **native matter (N1)** / better bulk, or  
   - **Harden exterior asymptotics** (one new contract: exterior must approach S2 vacuum within ε).  
3. Do **not** keep re-scanning ρ₀ with soft MATCH_OK.

**Lean:** harden once — require exterior approach to **φ≈const and D'≈const** (S2 vacuum) within tolerance; if still a wide band or empty, freeze dust-probe closure story as **band + soft match** and pivot energy to **native matter derivation**.

---

## 8. One-line summary

**Every qualifying dust turn C⁰-matches a healthy Path B vacuum exterior (0 fails) — matching doesn’t narrow mass; selection still sits in the turn itself, as a ~1 dex MATCH_OK band above M~60–110.**
