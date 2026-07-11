# Hopfion Phase 2 — workstation dispatch: metric backreaction

**Date:** 2026-07-10 · **Branch:** `grok` · **GPU preferred** (N≥192 fields; consumer GPU OK for smoke only)

---

## 0. Job in one line

On the **held hopfion** (H3 / Phase 1b isorotation), couple geometry (\(\phi\) and needed metric DOFs) to the carrier stress / \(\Sigma_\phi\), then re-ask exterior flux **plateau vs drift** with a self-consistent source — **no** \(G=8\pi T\), **no** SM mass claim.

---

## 1. Sync

```bash
git fetch origin && git checkout grok && git pull origin grok
cd /path/to/udt_mass_codex
```

**Regenerate base field if needed** (large `.npz` not in git):

```bash
cd hopfion_arc_scripts_2026-07-05
# Held static-class hopfion (Phase 1b used this class):
python3 drive_production.py 192 6 1 1 hopf 1.6 350 0.015 p2_base '' 15
# Optional isorotation continuation (Phase 1b recipe):
cd ..
python3 hopfion_fixedQ_phase1b_production.py --N 192 --L 6 --static_steps 40 --q_steps 120 \
  --Q 0,1.0 --restart hopfion_arc_scripts_2026-07-05/prod_p2_base.npz \
  --rescale_every 0 --qmin 0.85 --save hopfion_phase2_n_field.npz
```

Keep fields **local** (gitignored patterns already cover `hopfion_fixedQ_phase1b_field*.npz` / `prod_p1b*`; add new names if needed).

---

## 2. Read order

| # | File | Why |
|---|------|-----|
| 1 | **This file** | Job bounds |
| 2 | `hopfion_fixedQ_isorotation_MAP.md` | Phase 2 definition |
| 3 | `hopfion_fixedQ_phase1b_production_results.md` | Held \(Q\) continuation on flat FS |
| 4 | `hopfion_GP_exterior_probe_results.md` | Static P ⇒ **drift**, G ⇒ plateau (baseline to beat or re-state) |
| 5 | `hopfion_mass_background_coupling_MAP.md` | Mass lane orientation; hedgehog ≠ hopfion |
| 6 | `matter_carrier_provenance_audit_results.md` | Carrier = **POSIT** |
| 7 | `hopfion_arc_scripts_2026-07-05/fs_hopfion.py` | FS energy / \(Q_H\) / grids |

---

## 3. Physics scope (binding)

### Object
- **H3-class \(Q_H\sim 1\) hopfion only** (production-held field).  
- **Never** f2d \(\pi_2\) hedgehog.

### Metric
- **Minimum viable:** reciprocal diagonal \(\phi(r)\) (or \(\phi(\mathbf x)\)) sourced by carrier stress / \(\Sigma_\phi\) proxy from fixed \(Q\) isorotation (\(|\partial_T\mathbf n|^2=\omega^2(n_x^2+n_y^2)\), etc.).  
- **If** \(\rho+p_r>0\) or equations overconstrain: **drop pure \(B=1/A\) interior** — allow at least \(A,B\) (and \(g_{Tr}\) if forced). Tag every extension CHOSE vs THEORY.  
- **No** Einstein continuum \(G=8\pi T\) import as the bulk law; use **native** \(\phi\)-channel / action variation.

### Carrier
- Prefer **fixed profile** from Phase 1b at chosen \(Q\in\{0,1\}\) first (metric solve with frozen \(\mathbf n\)), then optional co-relax.  
- Isorotation: \(\mathbf n(T,\mathbf x)=R_{\hat z}(\omega T)\mathbf n_\omega(\mathbf x)\) with \(\omega=Q/I[\mathbf n]\) or fixed \(\omega\).

---

## 4. Pre-registered tests (characterize, no retune)

| ID | Question |
|----|----------|
| **P2-T1** | Does a regular coupled \(\phi\) (and metric) solve exist with \(\|\mathbf n\|\) hopfion held (\(\|Q_H\|\ge 0.85\))? |
| **P2-T2** | Exterior flux \(q(r)=Z r^2\phi'\) (or honest radial flux): **plateau / drift / undecided** vs static P baseline? |
| **P2-T3** | Sensitivity table vs \(\phi_{\mathrm{amb}}\) (or core \(\phi_c\)) and \(Z_\phi\in\{1,8\}\) — class, not one number |
| **P2-T4** | \(Q=0\) static hopfion vs \(Q>0\) isorotation: does time structure change exterior class? |

**Success language (honest):**
- Plateau with robust \(q\neq 0\) → flux **meaningful to interpret** (still not SM mass; conditioned on free moduli).  
- Drift remains → bank: self-consistent source still boxy in this metric sector; need more DOFs or native switch.  
- Solve fails / topology dies → solver-first report; halt-don’t-salvage.

---

## 5. Suggested arms (minimum matrix)

| Arm | Carrier | Metric |
|-----|---------|--------|
| **A** | Static H3-class (\(Q=0\)) | Native φ solve + hopfion stress / \(\Sigma\) proxy |
| **B** | Phase 1b isorotation \(Q=1\) (frozen \(\mathbf n_\omega\)) | Same |
| **C** (if A/B overconstrained) | Same as B | Relax \(B=1/A\); document |

Control: pure vacuum Branch-P exterior (no hopfion) should still **drift** if source ON — sanity.

---

## 6. ANTI-HANG / GPU

- Prefer **workstation GPU**; single process; no concurrent jobs  
- N=192 default; N=128 smoke only if debugging  
- Cap Newton/LM/iters; bound wall-clock → **throughput-limited** OK  
- torch float64; ignore NVML warnings if stack matches repo notes  
- Do **not** commit multi-100MB `.npz` fields — results md + small JSON only  

---

## 7. Out of scope (red)

- SM / lepton masses, SNe, free \(D_A\), dS native fill  
- f2d hedgehog, more mirror-vs-wall cell seals  
- Branch-G clean-\(q\) tautology; cherry-pick \(r_{\mathrm{lo}}\) δm  
- Topology ⇒ branch slogans  
- New couplings to force plateau  
- Claim “unique UDT system” from \(L_2+L_4\) alone  

---

## 8. Deliverable

1. `hopfion_phase2_metric_backreaction_results.md` (hygiene + premise ledger + T1–T4 table)  
2. Small JSON diagnostics (flux profiles optional, not huge fields)  
3. Explicit: which metric ansatz; CHOSE vs THEORY tags  
4. Verdict line: plateau / drift / obstructed / throughput-limited  
5. Commit + push `grok` (no force-push)  
6. Optional: one blind adversarial pass before calling BANKED  

---

## 9. Smoke (before long runs)

```bash
# Phase 1b sanity (optional if field already held)
python3 hopfion_fixedQ_phase1b_production.py --N 128 --L 6 --static_steps 30 --q_steps 20 \
  --Q 0,1 --seed hopf --ssize 1.6 --qmin 0.85
python3 -m pytest tests/ -q --tb=no   # if shared solvers touched
```

---

## One-line for the implementer

**Freeze held hopfion \(\mathbf n\) (static and/or \(Q=1\) isorotation); solve native metric/φ backreaction; classify exterior flux plateau vs drift — H3 only, no G=8πT, no mass number.**
