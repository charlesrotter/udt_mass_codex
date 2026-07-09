# MAP — Bulk completion for a native limit edge (after HE1)

**Date:** 2026-07-08 · **Mode: MAP only (theory options). No invent-for-fit.**  
**Trigger:** HE1 — outer `φ→∞` at finite chart radius is **incompatible** with Path A vacuum/dilated dust and **blocked on Path B** by EL_D’s `e^{2φ}(φ')²` under EH + R1 kinetic.  
**Parents:** `macro_hard_edge_asymptotics_HE1_results.md` · `macro_native_edge_HARD_MAP.md` · Phase 1–3 restart.

---

## 0. Goal

Identify **which bulk changes are *candidates*** to restore a native hard edge (or an honest substitute), each with:

- what obstruction it removes,  
- derivation path (not a knob),  
- kill criteria,  
- CHOSE vs must-derive.

**Principle 1:** no term because it “would help the edge.” Every term needs a **native warrant** (R1–R3, measure, EH structure, channel matter, finite-cell principle).

---

## 1. Obstruction recap (what bulk must address)

| Obstruction | Where |
|-------------|--------|
| **O1** Path A: `(r²φ')'=0` forbids outer log/power blowup of φ | Areal + kinetic only |
| **O2** Path A + dilated ρ: source `∝ e^{−2φ}→0` at edge | Cannot balance blowup |
| **O3** Path B: smooth finite `D_A` ⇒ `φ'∼C/D²` ⇒ φ→∞ needs infinite r | Free `D_A` + EH+kin |
| **O4** Path B: `φ→∞` makes **`Z D_A e^{2φ}(φ')²` dominate EL_D** | Catastrophic; blocks singular-edge ansätze |
| **O5** Dilated dust thins at edge | Does not cancel O4 |

**Minimal requirement for E-hard-1 (`φ→∞` at finite r):** neutralize **O4** (and O1 if staying areal), without smuggling GR free functions.

---

## 2. Completion options (catalog)

### C1 — **Areal gauge only + different bulk (not free-`D_A` EH)**

Stay on Path A (`D_A=r`). EH empty. Edge must come from **changing the φ equation**, not free transverse radius.

| Candidate sub-term | Warrant path | Hits |
|--------------------|--------------|------|
| **C1a** Potential `V(φ)` in action | Only if derived from dilation principle (usually **forbidden** as free V) | Could allow nonlinear EL and finite-r blowup |
| **C1b** Higher-derivative / geometric scalar from metric only | Derive from curvature invariants of reciprocal family | Might change EL order |
| **C1c** Matter that **does not** thin as `e^{−2φ}` | Conflicts with static energy redshift unless new sector | O2 |

**Kill C1a:** free `V(φ)` is classic dilaton cruft unless forced.  
**Default stance:** C1a **OUT** unless Charles forces a potential principle.

### C2 — **Drop or reweight the R1 kinetic near the edge (Z→0 or dynamical Z)**

O4 has leading **`Z D e^{2φ}(φ')²`**. If `Z=0`, that term dies; EL_D changes character.

| | |
|--|--|
| **Warrant** | Weak: Z was FREE normalization; setting Z=0 removes R1 bulk that Path A relies on |
| **Hit** | Removes O4’s worst term; may re-open singular edges |
| **Kill** | Path A vacuum becomes empty of bulk; theory loses shift-clean kinetic |

**Stance:** only as a **diagnosed limit** (“edge sector with frozen kinetic”), not global Z=0.

### C3 — **Do not vary free `D_A` through full EH (constraint / gauge)**

HE1 used free variation of `D_A` in `D_A² R`. Phase 2: EH bulk nonempty only if `D_A` varied.

| | |
|--|--|
| **Warrant** | Areal radius as **gauge** (Path A): don’t vary `D_A`; EH empty |
| **Hit** | Returns to Path A — **still no outer φ→∞** (O1) |
| **Stance** | Explains Path A/B split; **does not by itself** give hard outer edge |

### C4 — **Add extrinsic/transverse geometric term with controlled φ weight**

e.g. compensated vs raw `𝒦` densities (illustrative (A)/(B) from Phase 2) **in addition to or instead of** full EH free-`D_A` variation.

| | |
|--|--|
| **Warrant** | Must come from **ADM split / extrinsic geometry of transverse 2-metric**, not from “need edge” |
| **Hit** | Can change EL_D singular structure; may avoid `e^{2φ}(φ')²` dominance if EH is not the only transverse term |
| **Kill** | If term is only the old G/P fork without derivation; if it reintroduces cell-only finite-domain artifact with frozen `h=r²Ω` |

**Stance:** **Primary bulk-completion research track** — re-derive transverse action from metric split carefully; compare EL singular structure to O4.

### C5 — **Native matter with non-thinning channel at large φ**

| | |
|--|--|
| **Warrant** | Channel-corrected defect matter / continuum limit (N1) |
| **Hit** | Might source EL without `e^{−2φ}` death |
| **Kill** | Violates dilation toward edge without new principle; cell seals |

**Stance:** secondary; dilation is Charles-correct for ordinary energy; exotic channel needs derivation.

### C6 — **Abandon E-hard-1; complete theory with E-hard-3 / E-hard-4 / E-hard-2**

| Alt edge | Bulk demand |
|----------|-------------|
| **E-hard-4 φ ceiling** | Current bulk may already suffice (see ceiling probe) |
| **E-hard-3 marginal M** | Needs quasilocal M definition on UDT metric |
| **E-hard-2 finite-cell BC** | Needs derived boundary data, not φ→∞ |

**Stance:** if C2–C5 fail warrants, **E-hard-1 is the wrong edge for this bulk** — complete theory along 3/4/2 instead of forcing φ→∞.

---

## 3. Ranking for derivation effort

| Rank | Option | Role |
|------|--------|------|
| **1** | **C4** transverse geometric action re-derivation | Best chance to fix O4 *with geometric warrant* |
| **2** | **C6 / E-hard-4** φ-ceiling as honest outer story of *current* bulk | Matches numerics; lowest invention |
| **3** | **C6 / E-hard-3** marginal mass | Scale without φ→∞ |
| **4** | **C3** clarify gauge vs dynamics | Conceptual hygiene |
| **5** | **C2** Z→0 edge sector | Diagnostic only |
| **6** | **C1a** free V(φ) | **OUT** by default |
| **7** | **C5** non-dilating matter | Only with native channel proof |

---

## 4. Proposed work packages

### WP-BC1 — Transverse action from metric split (C4)
- Start from `ds² = −e^{−2φ}c²dt² + e^{2φ}dr² + h_{AB}dx^A dx^B`  
- Derive which scalars (`R^{(2)}`, `𝒦`, weights) appear from **natural geometric constructions** (not EH alone vs pure kinetic)  
- Compute EL_D singular structure as `φ→∞`  
- **Success:** O4 removed by a **derived** term  
- **Null:** only EH+kinetic reappear → document; go E-hard-4/3  

### WP-BC2 — φ-ceiling formalization (E-hard-4)  
- See companion results `macro_pathB_phi_ceiling_results.md`  
- Turn numeric attractor into a **stated theorem candidate** with precise data class  

### WP-BC3 — Quasilocal mass on UDT metric (E-hard-3)
- Define M from Path A Coulomb (known M∼−q) and Path B asymptotics  
- Candidate marginal condition; CAS  

---

## 5. Anti-cruft

| Forbidden | Why |
|-----------|-----|
| Add `V(φ)` to get a wall | Mechanism import |
| Set Z=0 globally “for the edge” | Kills Path A bulk |
| Put back G/P labels as two theories | Framing ban |
| Cell seals as macro edge | Contamination |
| Ignore HE1 and shoot φ→∞ anyway | Waste |

---

## 6. Decision tree

```text
HE1: φ→∞ finite r blocked by current bulk
        │
        ├─► WP-BC1 (C4 transverse re-derive)
        │         │
        │         ├─ O4 fixed natively → return to hard-edge BVP
        │         └─ O4 remains → do not force E-hard-1
        │
        ├─► WP-BC2 (φ ceiling)  ← honest outer story of *this* bulk
        │
        └─► WP-BC3 (marginal M) ← scale without φ→∞
```

---

## 7. One-line summary

**Bulk completion for a true `φ→∞` edge must neutralize Path B’s `e^{2φ}(φ')²` EL_D obstruction—best candidate is a derived transverse geometric action (C4); otherwise complete the theory with a φ-ceiling and/or marginal mass, not free potentials or φ-blind sources.**
