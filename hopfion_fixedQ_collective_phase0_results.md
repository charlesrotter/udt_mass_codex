## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-10 |
| **Mode** | OBSERVE / DEMO (collective coordinate only) |
| **Parent** | `hopfion_fixedQ_isorotation_MAP.md` |
| **Script** | `hopfion_fixedQ_collective_phase0.py` → `hopfion_fixedQ_collective_phase0_out.json` |
| **Build-on grade** | **DEMO** — finite-\(R\) minimum of reduced \(E_Q(R)\); **not** a PDE hopfion, **not** a mass |
| **Object** | Scale reduction informed by H3 virial \(E_2/E_4\simeq 0.9995\) only |

### Premise ledger

| Item | Tag |
|------|-----|
| \(E_2/E_4=0.9995\) | BANKED H3 (virial ~1%) |
| \(E_4=1\), \(\xi=\kappa=1\) | CHOSE gauge/normalization |
| \(I_2=I_4=1\) | **CHOSE** order-1 inertia norm — absolute \(R_Q\) not physical until profile integrals |
| Fixed-\(Q\) energy formula | THEORY (collective Noether charge on \(L_2+L_4\) scale family) |

---

# Phase 0 — fixed-\(Q\) collective scale energy

\[
E_Q(R)=E_2 R+\frac{E_4}{R}+\frac{Q^2}{2(I_2 R^3+I_4 R)}.
\]

## Pre-registered tests

| ID | Result |
|----|--------|
| **P0-T1** finite interior min for \(Q>0\) | **PASS** (all \(Q\in\{0.5,1,2,5\}\)) |
| **P0-T2** \(E_Q''(R_Q)>0\) | **PASS** (stable vs scale) |
| **P0-T3** \(Q\to0\) recovers Derrick \(R_*=\sqrt{E_4/E_2}\) | **PASS** (\(<2\%\)) |

## Table (CHOSE \(I_2=I_4=1\))

| \(Q\) | \(R_Q\) | \(E_Q''(R_Q)\) |
|------:|--------:|---------------:|
| 0 | 1.000 | 2.002 |
| 0.5 | 1.058 | 1.951 |
| 1 | 1.203 | 1.853 |
| 2 | 1.554 | 1.692 |
| 5 | 2.431 | 1.342 |

(Matches external DEMO shape: \(R_Q\) grows with \(Q\), curvature stays positive.)

## What this does **not** claim

- Not a solved isorotating hopfion PDE.  
- Not absolute physical radius (inertia moments not from H3 field — field checkpoint not in repo; regenerate for Phase 0b).  
- Not SM mass / lepton.  
- Not resolution of G/P exterior (static P still drifts).

## Next (Phase 1)

Stationary isorotation PDE for \(\mathbf n_\omega\) on flat FS, continuation from H3 \(\omega=0\) / \(Q=0\), with regenerated field if needed. Then Phase 2 metric backreaction.

---

## One-line

**Phase 0 DEMO: reduced \(E_Q(R)\) has a stable finite-\(R\) minimum for \(Q>0\) under H3 virial ratio + CHOSE inertia norm — green light for Phase 1 PDE, not a mass.**
