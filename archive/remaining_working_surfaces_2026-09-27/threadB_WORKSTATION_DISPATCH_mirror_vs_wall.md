# Thread B — workstation dispatch: mirror vs WR-L wall seal

**Date:** 2026-07-10 · **Branch:** `grok` · **GPU OK** · Static only

---

## 0. Job in one line

f2d closed cell: does a **WR-L causal-wall-style seal** (no \(f_r=0\) drain channel; \(L\) not free-boundary) stop the \(I_r\to0\) drain that **survives** round / non-round / topology under finite-mirror \(H=0\)?

---

## 1. Sync

```bash
git fetch origin && git checkout grok && git pull origin grok
cd /path/to/udt_mass_codex
```

---

## 2. Read order

| # | File | Why |
|---|------|-----|
| 1 | **This file** | Job bounds |
| 2 | `threadB_f2d_drain_solver_first_MAP.md` | DOF list + post-audit: next = closure |
| 3 | `threadB_f2d_nonround_topological_audit_results.md` | Drain survives; \(Q=N\); \(I_r\) drains not topology |
| 4 | `threadB_coupled_cell_flatness_Lselector_results.md` | Baseline mirror drain |
| 5 | `cell_solver_f2d.py` | Edit in place |

Optional: WR-L wall character — `simple_metric_L_wall_regularity_closure_results.md` / `simple_metric_timelive_AP_exact_derive_results.md` (wall optical; not a hard edge).

---

## 3. Arms (pre-register both)

| Arm | Seal | Role |
|-----|------|------|
| **A** | Finite mirror \(H=0\) (current) | Control — expect drain |
| **B** | WR-L / **causal-wall-style** seal | Test — forbids \(f_r=0\) at seal; pins \(L\) by wall residual, not free collapse |

**Wall-style BC (intent — implement from native residual/wall, not a hard edge):**

- Seal is residual wall character: \(A\to0\) optical / unattainable, **not** a Dirichlet hard wall.  
- Matter angular profile: **do not** allow the seal condition that lets \(f_r=0\) and the residual minimizer dump \(I_r\).  
- \(L\) / outer scale: **pinned or constrained** by wall residual (no free-boundary \(L\to0\) or \(L\to\infty\)).  
- Re-derive seal rows from existing f2d junction package + WR-L residual wall language; tag every BC CHOSE vs THEORY.

If a pure WR-L geometric wall cannot be expressed on the present f2d cell variables, **document the obstruction** and implement the **nearest native** seal that (i) blocks \(f_r=0\) drain channel and (ii) pins \(L\) — still no hard edge, no new coupling.

---

## 4. Hold fixed

- **Static**, diagonal, Branch-P  
- Self-consistent \(f\) (no prescribed \(I_r\))  
- α freeze as prior (e.g. \(\{0,-1,-2\}\)); ASRC_C = −0.5 settled  
- Winding diagnostic \(Q=N\) (N=1 and optionally N=2)  
- Optional: one non-round S-Dir row (shear held) so closure is not confounded with round-only  
- Convergence axis: maxit 40 → 120+ (drain deepens under mirror — must re-check under wall)

---

## 5. Pre-registered tests

| ID | Question |
|----|----------|
| **T1** | Under wall seal, does \(I_r\) stay finite at high maxit (not →0)? |
| **T2** | Does \(L\) stay finite / non-runaway (vs mirror \(N=1\to0\), \(N=2\to\infty\))? |
| **T3** | Winding still \(Q=N\)? |
| **T4** | Control arm A still drains (sanity)? |

**Characterize, do not retune** after seeing numbers.  
Drain survives wall seal ⇒ scoped FAILURE of **this** DOF → next = time-live eigenmode (MAP DOF 1).  
Drain dies under wall only ⇒ report \(I_r\), \(L\), \(Q\) vs α/N; still CONDITIONAL until blind-checked.

---

## 6. ANTI-HANG / GPU

- Nr ≤ 16/24 (spot Nr=12); one process; cap LM iters  
- Bound wall-clock → **throughput-limited** OK  
- torch float64 if used; no concurrent GPU jobs  
- Prefer recompute on saved fields for diagnostics  

---

## 7. Out of scope (red)

- dS / Λ native fill  
- New mechanism or coupling to force flat  
- Prescribed \(I_r\) as closed-cell win  
- SNe / mass / particle spectrum  
- Full time-live dynamics (**after** this job if wall still drains)  
- \(g_{tr}\) / non-reciprocal metric (**last**)  
- Hard spatial edge / artificial Dirichlet wall that is not residual-native  

---

## 8. Deliverable

1. `threadB_f2d_mirror_vs_wall_results.md` (hygiene header + premise ledger + table)  
2. Arms A vs B: \(I_r\), \(L\), \(Q\), \(q_{\mathrm{raw}}\), \(\|F\|^2\), maxit, α, N  
3. Explicit seal implementation note (what BC rows changed; CHOSE vs THEORY)  
4. Verdict: wall stops drain / drain survives / throughput-limited / obstructed  
5. Commit + push `grok` (no force-push)

---

## 9. Smoke

```bash
PYTHONPATH=$(pwd) python3 scratchpad/run_f2d_nonround_topo.py   # optional: reproduce drain baseline
python3 -m pytest tests/ -q --tb=no                              # if solver imports change
```

---

## One-line for the implementer

**Same static f2d cell: mirror \(H=0\) vs WR-L wall-style seal that blocks \(f_r=0\) and pins \(L\); ask if \(I_r\) drain dies — no new coupling, no hard edge.**
