# Phase G — conditional mass readout on the corrected carrier (RESULTS)

**Date:** 2026-07-16 · **Dispatch:** `UDT_H3_CORRECTED_G_THEN_F_SEQUENCING_DISPATCH.md` · **Branch:** grok
**Observing or targeting:** OBSERVING — a unit-response consistency readout on the certified carrier;
no target number, DATA-BLIND (no particle labels/observed masses/fitted couplings; no kappa_g used).
**Verifier status:** independent verifier `verify_noNull_phaseG_mass.py` — **PASS 90/90**
(own one-sided orientations; own stencil residuals; own bond fluxes from the saved u fields;
every production scalar reproduced). Production: `noNull_phaseG_mass.py` → `noNull_phaseG_mass_ALL.json`.
**NOT claimed:** a native-UDT mass derivation (the lapse identity is CONDITIONAL on the EH metric-only
action premise); a physical wall at any readout radius (solver boundary only); boundary-independent
potential normalization at finite padding; virial closure (see finding F2); infinite-volume statements.

## Premise ledger
- S² carrier + L2+L4 functional: **POSIT/CHOSE** (bedrock: metric = stage, not actors).
- Eight-orientation discretization: **DERIVED numerically** (no Nyquist null, O(h²), cubic-symmetric).
- Lapse identity D²N = κ_g N ρ₄, M_N = 2∫Nρ₄: **CONDITIONAL** (EH metric-only action).
- Poisson solver: direct DST-I diagonalization of the SAME 7-point Dirichlet operator (category-A;
  exact to roundoff — supersedes the old continuum-kernel Hockney with its ~1.75% 7-point residual).
- Carriers: the three independently relaxed critical fields (hashes in the JSON), NOT subsamples.

## Gates (all green, at every grid and padding)
| gate | requirement | worst measured |
|---|---|---|
| energy reproduction (E2, E4) | <1e-12 rel | 2.2e-16 |
| rho4 >= 0 | roundoff | min = 0.0 exact |
| rho + S = 2 rho4 (pointwise) | <1e-12 relmax | 2.1e-16 |
| Poisson residual r_P | <1e-9 | 1.4e-12 |
| discrete Gauss flux vs enclosed source | <1e-6 rel | 4.2e-12 (explained by r_P integral) |
| padding independence of flux ratios | report | identical to 8 digits across p=1/1.5/2 |

## Numbers (raw → continuum audit; NOT pure h² — h⁴ visible at 128³, slopes reported in JSON)
| quantity | 128³ | 192³ | 256³ | Richardson (fine pair) | 3-pt h²+h⁴ |
|---|---|---|---|---|---|
| E2 | 128.8329 | 132.1179 | 133.0803 | 134.310 | 134.175 |
| E4 | 142.9981 | 142.0627 | 141.8779 | 141.642 | 141.747 |
| E2+E4 | 271.8311 | 274.1806 | 274.9582 | 275.952 | 275.922 |
| **2E4 = M_N⁽⁰⁾** | 285.9963 | 284.1255 | 283.7558 | **283.283** | **283.495** |
| δ_vir=(E2−E4)/(E2+E4) | −0.0521 | −0.0363 | −0.0320 | −0.0265 | −0.0275 |

Charges: Q_fwd = −0.9673/−0.9862/−0.9923 (Q_sym within 1e-3 of Q_fwd). Criticality M-norms
0.0411/0.0173/0.0157 (match the stored NK values). Localization: E4 tail outside the a=2.95 cube
= 8.3–9.2e-4; the a=1 cube holds only 62–68% (broad source; omitted-tail reported, no wall claimed).
u(0) varies with padding (−11.86 → −12.68 at 256³): boundary-dependent normalization, reported as such.

## Conclusion (bounded exactly as dispatched)
**CONDITIONAL on the EH lapse identity, weak-field unit response: M_N⁽⁰⁾ = 2E4** within the displayed
discretization, source-tail (≤9.2e-4), linearization, and boundary errors. On surfaces enclosing all
but the tail, M_N⁽⁰⁾/2E4 = 1 − tail to 12 digits (Gauss identity — a consistency statement, not a
discovery; the informative outputs are E4, the virial relation, convergence, and localization).

## Findings for audit/ponder
- **F1 (the readout):** continuum-extrapolated 2E4 ≈ **283.3–283.5** (units ξ=κ=1); E2+E4 ≈ 275.9.
- **F2 (virial does NOT close):** δ_vir → ≈ **−2.7%** in the continuum audit (E2 < E4 persistently).
  2E4 and E2+E4 are DISTINCT numbers on this carrier; they are never silently identified. Note the
  contrast with the superseded Phase-A/C record (old centered-operator carrier: "M=2E4=E2+E4 to
  0.05%"). Continuum infinite-volume Derrick would force E2=E4 at criticality; the certified carrier
  is critical for the FIXED-BOX pinned problem, where the scaling variation is not admissible — the
  −2.7% is plausibly a finite-box effect (L=6, HBW=2), but that interpretation is UNPROVEN here.
  Discriminating box-effect vs operator-content belongs to a box/mask study or the boundary-layer
  theorem work — NOT assumed in this record.
- **F3:** E2 and E4 converge from opposite sides (E2 rising, E4 falling) — their h-errors partially
  cancel in E2+E4 (consistent with E=274.958 at 256³ matching the certified NK energy exactly).

**STOP per dispatch: F is NOT run. Awaiting G audit.**
