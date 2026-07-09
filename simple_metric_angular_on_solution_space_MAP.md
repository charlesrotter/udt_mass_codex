## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | MAP (no full solve yet) |
| **Frame** | residual dotted line + working **L** paint + orchestra (angular on) |
| **Status** | **FORWARD MAP** — Charles: search solution space with angular sector on; expect geometric coupling |
| **Build-on grade** | MAP only — no banked angular spectrum yet |
| **Related** | `UDT_DOTTED_LINE.md`, `UDT_METHOD_MUSIC.md`, `simple_metric_L_native_optical_derive_results.md` |

### Premise ledger

| Item | Tag |
|------|-----|
| Residual spine \(A=e^{-2\phi}\), multiplicative \(A\) | THEORY / DERIVED |
| Working cosmology paint **L** on spherical sector | WORKING (P-opt / mass lock / SNe) |
| Extend \(\phi=\phi(r)\) → angular dependence | **FREE first cut** (how much angular freedom) |
| Keep reciprocal \(g_{tt}g_{rr}=-c^2\) form with scalar \(\phi\) | CHOSE slice (simplest angular-on) |
| Keep areal \(r^2 d\Omega^2\) | THEORY simple-metric angular chart |
| Coupling constants between “sectors” | **FORBIDDEN** — only geometry |
| BAO fluid / \(c_s\), \(r_d\) import | **FORBIDDEN** as mechanism |
| Observing or targeting? | **OBSERVE** what angular-on solutions do — not “find BAO peak” |

### What is NOT claimed

- Angular sector already improves SNe.  
- BAO will emerge.  
- Coupling form pre-chosen beyond the metric.

---

# MAP — Angular sector ON (solution space)

## Lay agreement

Yes: **turning angular structure back on and exploring what the metric allows** is a native next move — more native than importing BAO acoustics.

Expect **complicated coupling**: not because we add a knob labeled “angular coupling,” but because **curvature mixes radial and angular derivatives** as soon as depth \(\phi\) depends on angle.

We silenced that section to hear the residual theme (L).  
Now we invite the section back **to play the same piece**, not a different concert.

---

## 1. What “angular on” means here

### Background (already in hand)
Spherical L package:
\[
\phi=\phi_L(r),\quad A=e^{-2\phi_L}=1-\frac{r}{X},
\]
static, diagonal, reciprocal, filled room.

### Minimal native extension (recommended first cut)
Keep the **same metric form**:
\[
ds^2=-e^{-2\phi}c^2 dt^2+e^{2\phi}dr^2+r^2 d\Omega^2,
\]
but allow
\[
\phi=\phi(r,\vartheta,\varphi)
\quad\text{(or axisymmetric \(\phi(r,\vartheta)\)).}
\]

**What stays:** residual interpretation of \(A=e^{-2\phi}\), areal spheres, reciprocity.  
**What changes:** \(A\) and \(\phi\) vary over the sky at fixed \(r\); Einstein/continuum (or native EL) **must** mix \(r\) and angles.

### What we are *not* doing first
- Free \(D_A(\theta)\), free multipole distance functions  
- Hand Lagrangian terms \(\phi\cdot Y_{lm}\) with free coefficients  
- Targeting “get a BAO wiggle”

---

## 2. Where the coupling comes from (native)

No extra constant is required for “sectors to talk.”

On this metric, as soon as \(\partial_\vartheta\phi\neq 0\) or \(\partial_\varphi\phi\neq 0\):

| Geometric fact | Effect |
|----------------|--------|
| Christoffel symbols involve \(\phi_r\), \(\phi_\vartheta\), … | Radial and angular gradients mix |
| Ricci / Einstein \(G_{\mu\nu}\) | Off-diagonal and multipole structure |
| Continuum \(T_{\mu\nu}\sim G_{\mu\nu}\) (E-room lean) | Stresses inherit that mix — **not** an independent angular fluid |
| Kinetic R1-style action for \(\phi\) (if used) | Angular gradients enter \(\lvert\nabla\phi\rvert^2\) with metric weights |

**Coupling complexity is expected and geometric.**  
Complicated ≠ free parameters. Complicated = **harder PDE / more modes**, still one residual field.

---

## 3. Solution-space program (ordered, observe-only)

### Regime A — Linear multipoles on L background *(first)*  
\[
\phi=\phi_L(r)+\varepsilon\sum_{\ell m}u_{\ell m}(r)\,Y_{\ell m}(\vartheta,\varphi)+\cdots
\]

**Observe (characterize, don’t filter):**
- Which \(\ell\) propagate / decay / singular at origin or wall?  
- Do angular modes backreact on residual / wall at \(O(\varepsilon^2)\)?  
- Any preferred radial scale set by \(X\) (geometric, not \(r_d\))?  
- Regularity at \(r=0\), behavior as \(r\to X\) under L.

**Anti-hang:** start low \(\ell\) (dipole/quadrupole), coarse radial grid, single process, bound iterations (project anti-hang).

**Question type:** METRIC-LED — “what does angular structure *do* on residual L?”  
Not: “can we get BAO?”

### Regime B — Axisymmetric nonlinear \(\phi(r,\vartheta)\)  
If A shows interesting structure, lift small ε.

### Regime C — Time-live angular  
Only after static angular character is partly mapped (dynamics open BAO-like *time* physics carefully, still no fluid import).

---

## 4. How this relates to BAO (honest)

| Layer | Status with angular-on |
|-------|-------------------------|
| BAO as **distance character** \(D_M(z)/X\) from radial L | Already possible **without** angular; still owed as multi-probe character |
| BAO as **acoustic peak / \(r_d\)** | Needs dynamics + standard-ruler physics — **not** assumed from multipoles |
| Angular sector may create **preferred scales / multipole weights** | **Possible** — to be observed, not required |

If multipoles only damp or only diverge, that is a **result** (characterize).  
It does not license importing baryon acoustics.

---

## 5. Orchestra check (method music)

| Solo so far | Angular-on role |
|-------------|-----------------|
| Residual note \(A\) | Still the **key** — angular is harmony, not a new root key |
| L paint | Background / working cosmology radial law |
| Mass lock / one \(X\) | Keep unless angular forces a principled revision |
| P-opt | Radial optical identity on spherical sector; angular light is a later verse |

**Whole before slice:** one multipole on a coarse grid is **one tile**, not “angular sector = BAO” or “angular dead.”

---

## 6. Completeness / imposition tripwires

- **Observing or targeting?** Observing. Stop if wording becomes “find the peak.”  
- **Chose or derived?** Background L = working; multipole basis = standard method (cat-A); no free coupling \(g_{\phi Y}\).  
- **Mismatch → solver:** if modes look ugly, check linearization, gauge, grid, wall BC — not a new mechanism.  
- **Do not** average angular “improvement” into SNe χ² as selection of L.

---

## 7. Deliverables for the first observe push

1. MAP freeze (this file) — **done**.  
2. Linear operator + numerics — **done** (`simple_metric_angular_on_L_multipole_results.md`).  
3. **Character found:** regular-at-origin static multipoles are **wall-loud**; no quiet static angular on filled L.  
4. Decision gate: **not** “angular damps softly”; rather **wall singularity / loudness** → next = dynamics or wall BC, not BAO import.

---

## 8. One-line

**Turn angular on by letting residual depth vary on spheres over the working L background; coupling is geometric (curvature mixes \(r\) and angles), not a free BAO mechanism — explore solution space, characterize modes, keep the residual monody as the key.**
