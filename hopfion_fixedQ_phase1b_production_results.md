## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-10 |
| **Mode** | OBSERVE — Phase 1b production-style isorotation |
| **Scripts** | `hopfion_fixedQ_phase1b_production.py` · `hopfion_arc_scripts_2026-07-05/drive_production.py` |
| **Out** | `hopfion_fixedQ_phase1b_production_out.json` (fields `*_field_Q*.npz` local only, not git) |
| **Build-on grade** | **LEAD / PHASE1B** — held \(Q_H\) under fixed-\(Q\) continuation on flat FS; **not** metric backreaction; **not** a mass |
| **Device** | CUDA float64, single process |

### Premise ledger

| Item | Tag |
|------|-----|
| Flat FS \(L_2+L_4\) | Phase 1 scope |
| Arrested-Newton on \(E_Q=E+Q^2/(2I)\) | Category-A (H3 production recipe) |
| \(I\) for \(\hat e_z\) isorotation (L2+L4) | DERIVED from ansatz |
| H3-class object (N=192 production field) | BANKED-style hold (\(\|Q_H\|\approx0.97\)) |
| Metric backreaction | Phase 2 — not done |
| Absolute \(Q\) units | free gauge of Noether charge scale |

---

# Phase 1b — fixed-\(Q\) continuation HOLDS

## Build

1. **Static base:** production arrested-Newton + damped Derrick rescale  
   `drive_production.py` N=192 L=6 hopf seed a=1.6, 350 steps →  
   \(\hat E\approx386\), \(E_2/E_4\approx0.966\), \(\|Q_H\|\approx0.9675\), CLASS=**HOLDS+CONVERGED**.  
   (N=160 toroidal 280 steps **failed** topology \(\|Q\|\to0.73\) — resolution/seed lesson.)

2. **Isorotation:** restart from that field; arrested-Newton on \(E_Q\) (no Derrick at \(Q>0\)); halt if \(\|Q_H\|<0.85\).

## Results table (N=192, L=6, ξ=κ=1)

| \(Q\) | \(\|Q_H\|\) | \(E_Q\) | \(E\) | \(E_2/E_4\) | \(I\) | \(\omega=Q/I\) | held |
|------:|----------:|--------:|------:|------------:|------:|---------------:|:----:|
| 0 | 0.9675 | 385.69 | 385.69 | 0.966 | 155.05 | 0 | yes |
| 0.5 | 0.9679 | 383.37 | 383.37 | 0.962 | 154.67 | 3.23e-3 | yes |
| 1.0 | 0.9682 | 381.19 | 381.19 | 0.957 | 154.30 | 6.48e-3 | yes |
| 2.0 | 0.9685 | 379.15 | 379.14 | 0.953 | 153.96 | 1.30e-2 | yes |

**Verdict:** `PHASE1B_HOLDS_Q_CONTINUATION`

## Pre-registered reading

| Goal | Status |
|------|--------|
| Production Newton on \(E_Q\) | **DONE** |
| Hold \(\|Q_H\|\gtrsim 0.85\) for \(Q>0\) | **PASS** (~0.968 all) |
| Topology-preserving continuation | **PASS** (slight \(\|Q_H\|\) increase) |
| Full nonlinear metric backreaction | **NOT DONE** (Phase 2) |
| Localized mass / G/P resolution | **NOT claimed** |

## Observations

- \(E_Q\) and \(E\) decrease mildly with \(Q\) under this flow (still descending; not fully arrested to a new virial fixed point at large \(Q\)).  
- \(I\) nearly constant (~155); \(\omega\) scales ~linearly with \(Q\).  
- Virial stays near 1 (0.95–0.97) — not the GD collapse of Phase 1 pilot.  
- Static P exterior boxy flux is **unchanged** by this (flat FS Phase 1 only).

## NOT claimed

- Particle mass or lepton wall.  
- Branch-G exterior.  
- That plain time-live linear modes are unstable (still no-go on hedgehog).  
- Phase 2 metric with \(A,B,C\).

## NEXT — Phase 2

Couple the held isorotating (or fixed-\(\omega\)) profile to \(\phi\) / non-reciprocal metric; re-ask exterior flux class with \(\langle\Sigma_\phi\rangle>0\).

---

## One-line

**Phase 1b: from a held N=192 hopfion, fixed-\(Q\) isorotation continuation preserves \(Q_H\sim0.97\) through \(Q=2\) under arrested-Newton on \(E_Q\) — green light for Phase 2 metric backreaction, not a mass.**
