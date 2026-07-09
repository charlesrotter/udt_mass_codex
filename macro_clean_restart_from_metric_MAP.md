# MAP — Clean restart: from the metric up (strip AI/assumption cruft)

**Date:** 2026-07-08 · **Mode: MAP / PONDER only. No compute.**  
**Charles direction:** It may be better to start from the field equations and let go of assumptions that may be AI cruft — perhaps even from the metric itself.  
**Status: DRAFT for Charles.** Parallel doc; does not edit LIVE/CANON/external.

---

## 0. Why restart

The recent macro thread accumulated a **stack of working choices** that were useful as probes but are easy to mistake for theory:

| Accumulated choice | Role it played | Risk |
|--------------------|----------------|------|
| “Uncompensated `𝒦`” as default dynamics | Geometry couples to φ | CHOSE probe, rebranded as if forced |
| Continuum `μ e^{αφ}` stand-in | Matter in EL | Not native `L_m` |
| Finite core / point center / σ-jet | Regularity recipes | Numerics habits |
| Free outward IVP | “See if edge appears” | Wrong question class for a limit edge |
| G/P language (even when banned late) | Bookkeeping | Cell contamination |
| α free / α=0 / φ-blind fights | Coupling lever | Mixed CHOSE and derived |
| Gaussian profiles, boxes, φ_cut | Solver knobs | Invisible physics |

**Null we trust as scoped:** under *that* stack, free IVP does not produce `φ→∞` at finite radius.  
**We should not trust:** that stack as “what UDT says.”

**Restart rule:** only carry what is **forced by postulates + metric + native derivation**, or is **explicitly re-ledgered as FREE** with Charles’s eyes on it. Everything else is **parked**, not assumed.

---

## 1. The clean ladder (only climb one rung at a time)

```text
  [0] Owner postulates (R1–R3 + named side premises)
           ↓
  [1] METRIC FORM          ← start here (canon)
           ↓
  [2] What the metric ALONE implies (redshift, optics, kinematics)
           ↓
  [3] What bulk dynamics are FORCED (action / EL) — native, not GR default
           ↓
  [4] What remains FREE (matter sector, transverse freedom, weights)
           ↓
  [5] Macro solutions / edge / x_max     ← only after 1–4 are clean
           ↓
  [6] Particles embedded in that background
```

Recent work jumped around **3–5** with soft **4**. Restart means: **re-walk 1→2→3 slowly**, re-derive or re-verify, refuse to import step-5 gadgets into step-3.

---

## 2. Rung [1] — Metric (keep; this is the solid floor)

**Canon (C-2026-06-18-1):** bare metric form **derived** from relativity requirements:

- **R1** dilation depends on **differences** in φ  
- **R2** dilations **compose**  
- **R3** **mutual reciprocity**  
- **+ named sides:** regularity of the dilation factor; R3↔length reciprocity analog (`g_tt g_rr = −c²`)

**Static spherical result (structure only):**

```text
ds² = −e^{−2φ} c² dt² + e^{2φ} dr² + (transverse 2-geometry)
```

**Scope (do not overclaim):**

| Fixed by metric postulates | **Not** fixed by metric postulates |
|----------------------------|-------------------------------------|
| How φ enters `g_tt`, `g_rr` | Profile `φ(r)` |
| Redshift law for static observers: `1+z = e^{Δφ}` | What sources φ |
| Reciprocal radial structure B=1/A | Edge, `x_max`, matter content |
| | Whether transverse radius is `r` or free `D_A(r)` / full `h_AB` |

**Charles pin candidate:** for restart, **transverse geometry is not frozen to `r²dΩ²` by the metric postulates** — freezing was a chart/simplicity choice in many docs (including early native FE with `r²dΩ`). Treat **free transverse size** as the open geometric question, not as “already decided by R1–R3.”

---

## 3. Rung [2] — Metric alone (kinematics / optics) — re-state, little cruft

From the metric **without** field equations:

1. **Redshift** (static observers): `1+z = e^{φ_s − φ_o}`.  
2. **Frame-relation reading:** each observer can set `φ=0` at themselves (R1 as gauge of zero).  
3. **Luminosity distance power n=2** under photon number conservation + null geodesics on this metric (banked this session’s arc; keep as kinematics, not as cosmology fit).  
4. **`φ→∞` means infinite redshift** for that chart — a geometric *meaning* of an edge, not yet a theorem that such a locus exists.

**Park:** any claim that the metric *forces* a finite-coordinate `φ→∞` edge. That is dynamics + global solution, not kinematics.

---

## 4. Rung [3] — Field equations (the real restart surface)

### 4.1 What is solid and should be re-held

| Claim | Status | Note |
|-------|--------|------|
| On this reciprocal family, bare **EH bulk vanishes** (boundary term) | CAS + blind verified (founding native FE) | Why “vacuum ≠ GR by default” |
| Bulk dynamics need a **native** source (not smuggled Einstein equation) | Principle 7 / charter | Restart must re-derive or re-verify the bulk action, not inherit solver cruft |
| Shift-invariant **kinetic for φ** is the natural R1-respecting bulk piece | Derived structure in founding FE | Coefficients / normalization still free |
| √(−g) φ-free on reciprocal family | CAS | Structural |

### 4.2 What is **not** solid enough to carry as “the field equations”

| Item | Why it’s cruft-risk |
|------|---------------------|
| Full package `S = ∫[(Z/2)φ'² + R⁽²⁾ + 𝒦_branch + L_m]` used as if unique | Skeleton was proposed; **matter and `𝒦` treatment not forced uniquely** |
| G/P “branches” | Cell bookkeeping; **banned for macro** |
| “Matter is φ-blind” as universal | **Conditional** on shift levers; Charles already relaxed for broken-shift regimes; P16 is a **different** (spin) question |
| Continuum `μ e^{αφ}` | Stand-in from our probes |
| Winding S² matter as default macro | Particle package |
| Two-player cell scalar as macro equation | Provenance: micro specialization |
| Finite-core IC, Gaussian μ, σ-jet, IVP edge hunt | Numerics program, not FE |

### 4.3 Restart discipline for field equations

**Goal of the restart derive (when gated):**

> From the **metric family** + **R1–R3** + **EH-empty fact**, write the **most general native bulk action** (or EL system) that is forced, and list **every** unfixed piece in a ledger — with **zero** particle BCs, **zero** continuum stand-ins, **zero** edge targets.

**Order of questions (strict):**

1. What scalar densities can appear given R1 (shift) and the reciprocal metric measure?  
2. Is the φ kinetic term unique up to `Z_φ`?  
3. What is the clean status of transverse curvature `R⁽²⁾[h]` — forced, optional, topological?  
4. What is `𝒦` (extrinsic of transverse metric) — forced term, optional, weighted how?  
   - Do **not** name G/P; only “weight of this term.”  
5. What does “matter” mean before any particle ansatz — empty set / perfect fluid / geometric defect / unknown?  
6. Only then: spherical reduction with **free** `D_A` or full `h_AB`.

**Refuse until ledgered:** α, μ(r), core class, `x_max`, closure scans.

---

## 5. Rung [4] — FREE ledger template (empty until re-filled)

After a clean FE restart, every macro claim must point here:

| Symbol / choice | Forced by? | If free, who pins? |
|-----------------|------------|-------------------|
| `Z_φ` | | |
| Transverse `h_AB` free vs slaved | | |
| Weight of extrinsic/transverse term | | |
| Matter sector | | |
| Static / spherical symmetry | | |
| Edge definition | | |
| Constants of nature (`c`,`G` only?) | | |

Recent parallel docs **do not auto-fill** this table.

---

## 6. What to **park** from the last two days (not throw away)

Park as **hypothesis probes with known scope**, not as foundations:

- α-jet outward results  
- Finite-core continuum scans  
- φ→∞ IVP null  
- Edge/closure options E1–E4 as **architecture menu** (still useful *after* FE are clean)  
- `x_max ∼ GM/c²` dimensional story (still good **dimensional** advice; not a substitute for FE)

**Keep as orientation, not as axioms:**

- No G/P for macro  
- No cell package for macro  
- No SNe-as-input  
- Metric form + n=2 kinematics + EH-empty  
- “Something must give scale; vacuum alone is weak as a full cosmology” (scoped)

---

## 7. Relation to `x_max` / Charles’s c-analog

Your limit idea lives at **rung 5**, after dynamics exist.

**Allowed now (kinematic/dimensional):**

- `φ→∞` = infinite redshift (meaning).  
- Finite chart radius edge is *possible* in principle on this metric family.  
- Length scales need mass if only `c,G` are constants of nature.

**Not allowed as restart premise:**

- That continuum IVP must produce the edge.  
- That any particular L produces `x_max`.  
- That the edge is already in the metric postulates alone.

When FE are clean, **re-ask** existence of a limit edge as a **solution-class question**, preferably BVP/matching, not assumption-stuffed IVP.

---

## 8. Proposed restart sequence (work plan)

### Phase 0 — Agree the purge (this doc)
Charles signs: we **suspend** continuum stand-ins / G/P / IVP edge program as foundations.

### Phase 1 — Metric cold read (short)
- Re-state R1–R3 + sides from CANON / external in one page.  
- Write **only** what follows without FE.  
- Explicit list: transverse geometry **open**.

### Phase 2 — Field equations from scratch (main)
- Start from metric family (general `D_A` or `h_AB`, not only `r²`).  
- Re-establish EH-empty (CAS, already have scripts — re-run, don’t re-story).  
- Derive candidate bulk terms **one at a time** with CHOSE/DERIVED tags.  
- **Stop** before matter ansatz if matter is not forced.  
- Deliverable: `native_macro_FE_from_metric_*.md` + sympy notebook/script — **minimal**.

### Phase 3 — Only then solutions
- Vacuum of the **clean** system (what is forced).  
- Minimal matter **if** forced or Charles-pinned.  
- Edge / `x_max` as solution question.

### Phase 4 — Particles
- Only after a background is not a stack of stand-ins.

---

## 9. Anti-cruft rules for the restart

1. **No term enters because a previous IVP needed it.**  
2. **No particle BC** in macro FE derivation.  
3. **No G/P names.**  
4. **No “for tractability.”** If reduced, tag FREE reduction.  
5. **Every equation line:** derived from (cite) or FREE (why present).  
6. **Prefer shorter action** over richer stand-ins.  
7. **Verifier before bank** on any new FE claim.  
8. **Lay checkpoint with Charles** after Phase 1 and after Phase 2 before any Phase 3 solve.

---

## 10. Advice (driver)

**Yes — restart from the metric, then field equations, is the right move.**  
The last probes were good at **exposing** that assumption-heavy continuum IVP does not hand us `x_max`; they are bad at being the **foundation**.

**Do next (no big grid):**

1. You confirm Phase 0 purge.  
2. Phase 1: one clean “metric-only” page (can be co-written, short).  
3. Phase 2: native FE re-walk with free transverse geometry, empty FREE ledger, CAS on EH-empty + whatever bulk terms survive scrutiny.

**Do not next:** another μ/α/edge IVP scan on the old L.

---

## 11. One-line summary

**Strip the stand-ins; keep metric + EH-empty + redshift kinematics; re-derive field equations from the metric family with an empty free ledger; only then ask macro solutions and `x_max`.**
