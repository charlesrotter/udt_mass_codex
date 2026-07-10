## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-10 |
| **Mode** | OBSERVE / Phase 1 pilot (flat FS isorotation) |
| **Script** | `hopfion_fixedQ_phase1_isorotation.py` |
| **Parent** | `hopfion_fixedQ_isorotation_MAP.md` · Phase 0 DEMO |
| **Build-on grade** | **LEAD / PILOT** — machinery + first numbers; **not** a resolved isorotating hopfion |
| **Device** | CUDA float64, single process |

### Premise ledger

| Item | Tag |
|------|-----|
| Flat FS \(L_2+L_4\), no metric backreaction | Phase 1 scope |
| Target isorotation about \(\hat e_z\); \(E_Q=E+Q^2/(2I)\) | THEORY (collective) |
| \(I\) = L2 + L4 time-space inertia | DERIVED from ansatz |
| Gradient flow on \(E_Q\) (not arrested-Newton) | **WORKING / weak** — known insufficient vs H3 production |
| Grid N=48/64, L=5 | category-A bounded pilot |
| Object: \(Q_H\sim 1\) sector seed | not f2d hedgehog |

---

# Phase 1 pilot — fixed-\(Q\) isorotation (flat FS)

## What was built

1. Reuse `hopfion_arc_scripts_2026-07-05/fs_hopfion.py` energy + Hopf charge.  
2. Moment of inertia \(I\) for \(\partial_T\mathbf n=\omega\,\hat e_z\times\mathbf n\).  
3. Effective energy \(E_Q=E_{\mathrm{static}}+Q^2/(2I)\).  
4. Projected gradient flow on \(S^2\) with vacuum pin at box edge.  
5. Continuation in \(Q\) from a warm static field.

## Runs (bounded)

### A) N=48, toroidal seed, \(Q\in\{0,0.5,1\}\)

| \(Q\) | final \(E_Q\) | \(E_2/E_4\) | \(I\) | \(\|Q_H\|\) |
|------:|-------------:|------------:|------:|----------:|
| 0 | 294.2 | 1.13 | 163.3 | **0.53** |
| 0.5 | 279.6 | 1.22 | 162.6 | **0.48** |
| 1.0 | 256.8 | 1.44 | 161.3 | **0.40** |

Energy falls under flow, but **topology slips** (same coarse-grid pathology H3 documented at N≲96). Virial drifts away from ~1. **Not** a held isorotating hopfion.

### B) N=64, Hopf seed, \(Q=0\) only (topology check)

| step | \(E\) | \(E_2/E_4\) | \(\|Q_H\|\) |
|------|------:|------------:|----------:|
| 0 (seed) | ~793 | 6.60 | — |
| after ~100 GD steps | 760 | 6.32 | **0.936** |

Topology **holds better**, but field is **far from** FS minimizer (virial ≫1, energy ≫ banked \(\hat E\sim 286\)). Confirms charge diagnostic works; plain GD does not replace production arrested-Newton.

## Pre-registered reading (Phase 1 pilot)

| Goal | Status |
|------|--------|
| Implement \(E_Q\), \(I\), continuation | **DONE** |
| Hold \(\|Q_H\|\gtrsim 0.9\) while relaxing at \(Q>0\) on production-grade minimizer | **NOT YET** |
| Report stable isorotating hopfion | **NOT YET** |

## Diagnosis (solver-first, not mechanism)

MISMATCH → SOLVER: H3 existence required **arrested-Newton + resolution ladder + Derrick rescale**, not Adam/plain GD. Phase 1 pilot used **plain projected GD** ⇒ topology/virial unprotected on coarse grids.

## What is established

- Fixed-\(Q\) variational principle is **coded and runs on GPU**.  
- \(I\) is finite and smooth on hopfion-like seeds.  
- Phase 0 collective DEMO remains the only **clean** finite-\(R_Q\) table; Phase 1 PDE needs production-grade flow.

## NOT claimed

- Resolved isorotating hopfion.  
- Mass or G/P resolution.  
- Metric backreaction (Phase 2).

## NEXT (Phase 1b — still here or workstation)

1. **Port production `relax_newton` + optional Derrick rescale** from `drive_production.py` into the \(E_Q\) functional (or minimize \(E\) at fixed \(\omega\) with the same flow).  
2. Start from **regenerated H3 field** (N≥160) as restart, not raw seed.  
3. Continue \(Q\) slowly with topology monitors every step; halt if \(\|Q_H\|<0.85\).  
4. Only then claim Phase 1 existence/no-go.

---

## One-line

**Phase 1 pilot: fixed-\(Q\) energy and inertia work on CUDA; plain GD does not hold a hopfion — next is production-style Newton from a regenerated H3 field under \(E_Q\).**
