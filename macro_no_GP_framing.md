# MACRO FRAMING — do **not** use Branch G / Branch P labels

**Date:** 2026-07-08 · **Status: CHARLES PIN (working rule for all macro work).**  
**Parallel doc** (does not edit LIVE / external / older MAPs).  
**Supersedes for macro vocabulary:** any “macro = Branch G”, “macro = Branch P”, “P-type macro”, “G vacuum control as a branch choice” language in the parallel macro thread.

---

## 0. The pin

**Macro work does not choose, name, or pre-select “Branch G” or “Branch P.”**

Those labels grew up for **cell / microphysics bookkeeping** (continuum exterior vs finite-cell regime in the founding two-player writeup). Dragging them into the universe problem re-imports:

- a false fork (“which branch is the cosmos?”),
- cell-package connotations (seals, winding, frozen round `h`, “intrinsically finite-domain”),
- and a habit of **picking an equation set before** the matter-coupled action has spoken.

For the macro: **one clean action, free transverse geometry, clean matter; let the symmetry regime and the equations be outputs.**

---

## 1. What exists in the action (keep the physics, drop the brand names)

There is a **single** base skeleton:

```
S = ∫ c √h [ (Z_φ/2) φ'² + R^{(2)}[h] + 𝒦_treatment + L_m ]
```

Inside that skeleton there is a **treatment of `𝒦`** (extrinsic/transverse term):

| Physics (use these words) | Old label (do **not** use in macro prose) |
|---------------------------|-------------------------------------------|
| `𝒦` **compensated** (× `e^{2φ}`) so depth-shift stays exact → φ **decouples** from transverse geometry in bulk | “Branch G” |
| `𝒦` **uncompensated** → depth-shift **broken** → φ **couples** to transverse geometry | “Branch P” |

The **switch criterion** (what makes compensation the wrong or right description) is **underived**. For macro work we do **not** resolve it by saying “we’re on P” or “we’re on G.”

**Especially:** do not say “matter-sourced macro = Branch P.” Say instead, if needed:

> Matter can reach φ through geometry only when the shift is not enforced as an exact bulk symmetry; whether that is implemented as uncompensated `𝒦`, as a direct α-weight once shift is broken, or as an output of the solve, is part of what we determine — not a branch badge.

---

## 2. Why G/P language is harmful on the macro

1. **Category error** — founding map: G ≈ continuum exterior, P ≈ finite cell / microphysics. That map was a **regime slogan**, not a derived cosmology taxonomy.  
2. **Contamination bleed** — “P” pulls winding, seals, frozen `h=r²Ω`, two-player cell scalar. We already spent a session undoing that.  
3. **False choice** — macro is not a menu item on a two-item list.  
4. **Hides α** — calling the work “P” made it easy to re-freeze φ-blindness as “the P equation,” undoing the 2026-07-07 CHOSE-lever result.  
5. **Hides free `h`** — “P has no vacuum” was scoped to **frozen** transverse metric; free `h` was the point of the clean-core pivot.

---

## 3. Vocabulary for the macro thread (binding for new parallel work)

### Use

- **Clean core** — metric form; EH-empty; kinetic for φ; free `h_AB` / free `D_A`; clean `L_m`  
- **Depth-shift** exact or broken (output or ledgered treatment of `𝒦`, not a branch name)  
- **Compensated / uncompensated `𝒦`** only when discussing that **term**, not as cosmology identity  
- **Sourceless bulk φ** vs **geometry-coupled φ** vs **direct α-coupling** (when α ≠ 0)  
- **Vacuum reference** (matter off) vs **matter-coupled macro**  
- **Cell package** = contamination (OUT)  
- **α** = FREE radial matter–φ weight once shift is not exact (Thread B banked); not “Branch P parameter”

### Avoid in macro docs / solves / talk

- “Branch G”, “Branch P”, “G/P”, “P-type macro”, “G-type cosmos”  
- “We’re on Branch ___ for the universe”  
- “Drop Branch P” / “keep both branches open” as the macro program statement  
- Using the **cell two-player scalar** as “the” macro equation under a branch name

### Historical / cell docs

G/P may remain in **old cell results** and founding FE docs as provenance. When citing them for macro, **translate**:

> “In the founding writeup, compensated `𝒦` gave …; uncompensated with frozen `h=r²Ω` gave … . Macro does not inherit those labels.”

---

## 4. How this re-reads recent parallel work

| Doc / result | Re-read under this pin |
|--------------|-------------------------|
| Q1 posture (a)/(b)/(c) | Keep as **source-channel** options; strip any “only in Branch P” as **definition of the channel**, not a branch pick |
| Clean-core MAP Q2 “G/P/composite” | **Retire for macro** — replace with: treatment of `𝒦` + α + free `h` are ledger items; regime is output |
| First observe “Branch G/P” | Means: **compensated vacuum reference** vs **uncompensated geometry-coupled φ EL** in a free-`D_A` slice — **α=0 control**. Keep the math; drop the brand in forward citations |
| φ-blindness re-audit | Unchanged: α CHOSE when shift not exact; P16 spin import still out. Say “P-type” → “shift not exact / matter-coupled regime” |
| external.md §4 | Still useful physics; its remaining “Branch G/P” strings are **legacy naming** for the same `𝒦` switch — macro writers should not copy the labels |

---

## 5. What the macro program *is* (no branches)

1. **Action:** clean core + free transverse geometry + clean matter (including α free when shift is not forced exact).  
2. **Do not** pre-select compensated vs uncompensated as “which universe.” Prefer: write the action terms you are using, tag CHOSE/DERIVED, solve, report what symmetry remains.  
3. **Vacuum (matter off)** is a **reference limit**, not “Branch G cosmology.”  
4. **Cell package** stays out.  
5. **Optics n=2**, closure-not-SNe, data-blind depth — unchanged.  
6. **Goal:** what macro `φ` and `D_A` **emerge**; not which branch logo sticks.

---

## 6. Minimal equation language (example)

Instead of “Branch P free-`D_A` EL”, write:

```
# uncompensated 𝒦, free D_A, optional direct weight α (FREE)
Z d/dr(D_A² φ') = 4 e^{−2φ} (D_A')² + α e^{αφ} σ
```

and ledger: `𝒦` uncompensated = CHOSE for this probe / or “output of …” when derived; `α` = FREE; `σ` = stand-in or from `L_m`.

Instead of “Branch G vacuum”, write:

```
# compensated 𝒦, matter off, free D_A
Z D_A² φ' = q ,   D_A'' = −q²/(4 Z D_A³)
```

as the **sourceless compensated reference**.

---

## 7. One-line summary

**Macro = one clean action and free geometry, not a G/P choice; keep the `𝒦` and α physics, retire the branch names for all forward macro work.**
