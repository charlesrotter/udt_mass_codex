# Thread B — workstation dispatch (one page)

**Date:** 2026-07-09 · **Branch:** `grok` · **GPU OK** · Do **not** chase continuum dS

---

## 0. Job in one line

Full self-consistent round **cell** \((f,\phi,\rho)\): does \(\alpha\neq 0\) + transverse matter stress **close a flat cell** and **matter-select \(L=r_s\)**?

---

## 1. Clone / sync

```bash
git fetch origin && git checkout grok && git pull origin grok
cd /path/to/udt_mass_codex   # repo root
```

---

## 2. Read order (this order)

| # | File | Why |
|---|------|-----|
| 1 | **`threadB_coupled_cell_flatness_Lselector_CHARTER.md`** | Full charter, EOMs, T1–T3, discipline |
| 2 | `udt_phi_blindness_relaxation_results.md` §1 + §3 | α lever; restoring channel LEADs |
| 3 | `simple_metric_alpha_restoring_probe_results.md` | Probe: right sign, can’t close alone |
| 4 | `simple_metric_dS_native_any_alpha_closed_results.md` | **dS closed any α — out of scope** |
| 5 | `simple_metric_Charles_rulings_center_dS_2026-07-09.md` | Ruling **(A)** seat OK; not a “fix L” job |
| 6 | `cell_solver_round.py` | Baseline φ-blind round cell (edit in place) |

Optional: `CLAUDE.md` DRIVER TRIGGERS + anti-hang; `LIVE.md` FRONTIER only if conflict.

---

## 3. Code rules

- **Edit** `cell_solver_round.py` (and shared helpers it already uses). **No** `*_v2` / parallel solver spawn.  
- Add **transverse \(T_{AB}\) stress** from native S² matter — **blind-verify that operator first** (independent re-derivation).  
- α freeze: **only** \(\{-0.5,-1,-2\}\). No retune after T1–T3.  
- α is **CHOSE** (p16 verdict C) — tag every table.  
- No fake ρ-source glue if collapse; halt and report.

---

## 4. Pre-registered tests (freeze before run)

| ID | Question |
|----|----------|
| **T1** | Exists deficit \(=0\) bounded cell for \(\alpha<0\)? |
| **T2** | Is \(r_s\) single-valued vs matter amplitude/scale (matter selects \(L\))? |
| **T3** | Core finite vs \(\rho\to 0\) collapse? |

Baseline check (φ-blind): `python3 cell_solver_round.py` — deficit stuck \(\sim -0.9\), never flat.

---

## 5. ANTI-HANG / GPU

- Nr ≤ 16/24 (or 1-D shooting with **capped** iters).  
- **One** process; no concurrent GPU jobs.  
- Cap Newton/Krylov; bound wall-clock → report **throughput-limited** if needed.  
- torch float64 OK if used; ignore NVML warning on this stack.  
- Prefer recompute on **saved** fields for diagnostics.

---

## 6. Out of scope (hard red)

- Native continuum **dS** / \(\Lambda\) fill (closed for any α)  
- Free \(D_A\), P_ell, SNe/χ² retune  
- Mechanism patches if T1 fails → **solver-first** (missing term, numeric, frozen DOF)  
- “Cure” residual L seat singularity (ruling **A** accepts regime boundary)

---

## 7. Deliverable back to repo

1. Results doc at root, e.g. `threadB_coupled_cell_flatness_Lselector_results.md`  
2. Premise ledger + α freeze + grid/iter budget  
3. T1/T2/T3 table (yes / no / weak / throughput-limited)  
4. Blind verify note on **\(T_{AB}\)** operator only if claiming close/pin  
5. Commit on `grok` with clear message; do not force-push  

Optional: JSON/pt fields for deficit scans (small, not multi-GB).

---

## 8. Smoke (before long runs)

```bash
python3 cell_solver_round.py          # φ-blind baseline sanity
python3 -m pytest tests/ -q --tb=no   # purity harness if solver imports change
```

---

## One-line for the implementer

**Extend round cell with α≠0 + real transverse stress; ask T1 flat / T2 L-select / T3 core — not dS, not SNe.**
