## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | MAP (solver-first — mismatch → DOFs left out) |
| **Source** | External MAP on banked Thread B pilot (Charles-relayed) |
| **Prior result** | `threadB_coupled_cell_flatness_Lselector_results.md` (CONDITIONAL) |
| **Build-on grade** | **MAP** — no new run; no mechanism; no closed-cell claim |
| **Observing or targeting?** | OBSERVE solver completeness — not “show a lump” |

### Premise ledger

| Item | Tag |
|------|-----|
| f2d pilot: static, diagonal, round, finite-mirror \(H=0\), no shear | **SCOPE of banked run** |
| Drain \(I_r\to0\), \(L\to0\) robust | **BANKED CONDITIONAL** (not under-iteration) |
| Prescribed-\(I_r\) flat cross | **PROBE only** — not self-consistent win |
| α CHOSE; \(S=-(\alpha/2)\cdots\) settled | BANKED |
| Next tests | GPU later — not this MAP |

---

# Thread B f2d drain — solver-first MAP (DOFs left out)

## 0. Current result (already clear)

Self-consistent closed f2d cell **drains** (\(I_r\to0\), \(L\to0\)), robust under convergence and \(\alpha\).  
Prescribed-\(I_r\) probe is the **only** place flat closure appears.

**Do not** re-bank probe flat as closed-cell win.  
**Do not** claim mass / particle / SNe / cosmology from this slice.

---

## 1. DOFs left out of the pilot slice

### 1. Time-live / nonstatic — **OPEN, highest priority (physics)**

f2d slice is **static**. If \(I_r\) is a live angular/residual object, a static residual minimizer may simply relax it away.  
Rhymes with macro lesson: static L is a regime chart; time-live is the open appearance sector.

**GPU later:** time-live perturbation or eigenmode about the drained solution — any mode with nonzero \(I_r\) restoring?  
**Do not** add coupling/mechanism.

### 2. Non-round / shear — **OPEN**

Run was **round**, explicitly **no shear**. Round ansatz may make the angular sector too easy to unwind/drain.

**GPU later:** non-round \(f(r,\theta)\), shear-like angular residuals, or \(m\neq0\) structure — ask only whether \(I_r>0\) can persist.

### 3. Boundary / mirror closure — **CHOSE / OPEN**

Closed f2d used finite mirror **\(H=0\)**. That closure may be too strong/quiet and let the minimizer collapse the cell.

**GPU later:** compare mirror vs WR-L **causal-wall-style** closure. No hard-edge assumption.

### 4. Topological charge enforcement — **OPEN**

Table: \(q_{\mathrm{raw}}\to\sim 10^{-7}\) with \(I_r\to0\) — solve may sit in **unwound/trivial** sector, not a nonzero topological cell.

**GPU later:** enforce intended topological class / boundary winding; re-check drain.

### 5. Reciprocal diagonal metric restriction — **WORKING / OPEN**

Slice keeps diagonal reciprocal form. If closed cell needs \(g_{tr}\), \(B\neq1/A\), or other metric DOF, solver is blind.

**GPU later: not first.** Only after time-live / non-round / boundary tests fail.

---

## 2. What not to do

| Forbidden | Why |
|-----------|-----|
| Treat prescribed-\(I_r\) flat as closed-cell win | Imposed \(I_r\); self-consistent drains |
| New mechanism / coupling to force flat | Mismatch → solver first |
| Mass / particle / SNe from this slice | Scope |
| dS native fill | Closed any α |
| Jump straight to full metric non-diagonal | Last on list |

---

## 3. Recommended next GPU job

\[
\boxed{\text{non-round + topological-boundary f2d, still static, before full time-live.}}
\]

**Reason:** smallest change that tests “drain = round sector unwinds.”  
Full time-live is more fundamental but a larger solver jump.

**After that (if drain persists):** mirror vs wall-style closure, then time-live eigenmode about drain.

---

## 4. Relation to residual L time-live

Macro time-live appearance (`simple_metric_timelive_AP_exact_derive_results.md`) and cell time-live DOF are **related lessons** (static minimizers quiet residual structure) but **different sectors** — do not identify without derivation.

---

## One-line

**f2d drain is a real residual-minimizer of the static round mirror slice; left-out DOFs are time-live, non-round/shear, mirror vs wall closure, topology, then metric form — next GPU = non-round + topological BC still static.**

---

## Audit result (2026-07-09) — drain SURVIVES non-round + topology

**`threadB_f2d_nonround_topological_audit_results.md`** (commit `452e1f7`)

- **FAILURE (scoped):** drain survives non-round shear + topology \(N=1,2\) + \(\alpha<0\); deepens with convergence.
- **MAP refinement:** “unwound sector” **falsified** — winding \(Q\) pins to \(N\) exactly; what drains is radial \(I_r\) (\(f\to\) rigid hedgehog), orthogonal to topology.
- **Next DOF (refined):** mirror vs **WR-L causal-wall** closure (mirror permits \(f_r=0\) at seal — drain channel). Then time-live eigenmode if still drains.

