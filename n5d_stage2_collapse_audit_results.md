# N5d Stage-2 STATIC S-Dir COLLAPSE MECHANISM AUDIT — results (π₂ tile; DESIGN/PROVISIONAL/Outcome D)

> **⚠⚠ CORRECTION / RETRACTION (2026-07-06 EOD-3, later same day — supersedes the "factor-2 structural deficit"
> conclusion below). The §5/§7 conclusion ("STRUCTURAL closure failure; π₂ matter factor-2 too weak; Hseal=−0.96
> L-independent; no finite-L cell") is WITHDRAWN — it was an OVER-READ of a soft-mode artifact.** A follow-up probe
> (`n5d_stage2_collapse_reconcile` inline, `scratchpad`) keeping Hseal IN the objective at FIXED L reaches **Hseal=0
> with the field equations satisfied** (Phi~1e-9), and a soft-mode characterization shows the fixed-L Jacobian has a
> **genuine near-null direction** (s_min=6.8e-14, well-separated; s_2nd=6.2e-9) along which **Hseal slides ~FREELY
> through zero** (dHseal/ds=1.5e-2 vs d‖F_field‖/ds=6e-10). The **−0.96 was merely where the *drop-Hseal* solve lands
> on a flat valley — NOT a hard floor.** Both this audit AND its blind verifier only ever probed the drop-Hseal valley
> point (the verifier prompt inherited the author's blind spot), so both "confirmed" −0.96 without testing the slide.
> **Corrected read (PROVISIONAL, pending a fresh blind pass): the collapse is a FREE-BOUNDARY / SOFT-MODE DEGENERACY
> (classification d) + severe ill-conditioning (s_min~1e-14) — the closure is nearly degenerate with the field
> solution manifold, so L is not cleanly determined and the free-L LM slides down a degenerate drain (Hseal→~0 AND
> L→0 both nearly cost-free). Per the pre-registered rule this leans NUMERICAL-PATH / degeneracy (item 8), NOT a hard
> structural matter deficit (item 9).** Whether an EXACT finite-L closed cell exists is REOPENED (the joint
> Hseal=0 ∧ ρ'(r_s)=0 residual is ~3e-5/L — smallest at LARGE L; possibly a large-cell limit, not a hard no). The
> small-L SCALING (§1), the fixed-L machine-precision solvability (§2), and the H(r_s) term VALUES (§3) stand as
> measurements; only their INTERPRETATION as a hard structural deficit is retracted. See the CORRECTION note appended
> at the end for the full record.

**Date:** 2026-07-06 (EOD-3) · **Author:** Claude Opus 4.8 (1M) · script `n5d_stage2_collapse_audit.py`.
**Diagnostic only** (empirical scaling + bounded FIXED-L relaxations + H(r_s) decomposition; NO free-L solve, NO
pilot, NO S-JC2/FIX-2/higher-ℓ implementation, NO finite-L target/penalty/anchor). Status: **DESIGN / PROVISIONAL /
Outcome D.** π₂ axisymmetric S² tile ONLY. **NO Outcome A/B, NO pin/continuum, NO π₃ claim, NO physics verdict.**

## Purpose
Determine WHY the static S-Dir co-relaxed π₂ tile has no finite-L closed cell (the blind-verified L→0 collapse,
`n5d_stage2_sdir_pilot_results.md`). Regime held fixed: static · S-Dir · block-diagonal · Branch-P · ℓ=2-only ·
π₂ co-relaxed source · λ=−½ · no flat source. PRM=(Z,XI,KAP,N)=(8,1,1,1), Nr=12, Nth=8.

## 1. Small-L scaling of the residual blocks (empirical; d/dr=(2/L)D_ζ)
Holding the ζ-profile fixed and varying L (factor L:1→1/8):
| block | scaling | | block | scaling |
|---|---|---|---|---|
| phi_ode | ~1/L² | | fr_mir / rho_mir / shear_core | ~1/L |
| f_pde | ~1/L² | | Hseal | **~O(1) (L-independent)** |
| shear_ode | ~1/L² | | rho_ode (angular-tension-dominated) / shear_seal | ~O(1) |

The field-equation/kinetic rows blow up as 1/L² at fixed profile → minimizing ‖F‖² drives the ζ-profiles onto the
**L-independent** field equations (making those rows ~0). Crucially **Hseal is O(1) and L-independent** — the seal
closure does not scale with L, so it cannot select an L.

## 2. Fixed-L relaxation → Hseal(L) (the decisive probe: fields relaxed with L HELD, Hseal row + L unknown dropped)
Reduced system (132 unknowns [φ,ρ,uf,a2] × the 132 non-Hseal rows) relaxes to **machine precision at every L**:

| L | Phi_reduced (warm) | Hseal(L) |
|---|---|---|
| 2.0 → 0.015 | 2e-11 → 2e-15 | **−0.959686 at EVERY L** |

**Hseal(L) = −0.9597, constant, for all L∈[0.015, 2.0] — it never crosses zero.** With L fixed the whole system
(field eqs + mirror BCs + shear rows) is solvable to machine precision; the ONLY unsatisfiable condition is the seal
closure H(r_s)=0, and it is unsatisfiable at every finite L. (Cold-start at very small L shows a *near*-zero Hseal —
but that is UNDERCONVERGENCE, Phi stuck ~5e-5; the fully-relaxed value is −0.96. Blind-verified.)

## 3. WHY — H(r_s) term decomposition at the relaxed mirror seal (L=0.4, Phi=4e-13)
At the relaxed S-Dir mirror seal the BCs give φ'(r_s)=ρ'(r_s)=f_r(r_s)=0 and the relaxed shear gives a2'(r_s)≈0, so
**every kinetic term of H(r_s) vanishes**:
| term | value |
|---|---|
| (Z/2)ρ²φ'², −2e^{−2φ}ρ'², +(1/10)e^{−2φ}ρ²a2'², −(ξ/2)ρ²I_r, −(κN²/2)I4r (all KINETIC) | ≈ 0 (1e-9…1e-26) |
| **−2 (boundary constant)** | **−2.00000** |
| **+(ξ/2)(Ith+N²Is) (angular potential, leading)** | **+1.00000 exactly** |
| +(κN²/2)I4th/ρ² (angular potential, quartic) | +0.0403 |
| **H(r_s) = SUM** | **−0.9597** |

**The π₂ angular matter POTENTIAL = +1.040 vs the boundary constant −2 → a factor-of-~2 deficit (needs +2 to close,
supplies +1.04).** The leading piece (ξ/2)(Ith+N²Is) = +1.000000 exactly — the rigid-hedgehog N=1 angular tension
(Ith=Is=1). This deficit is **L-independent AND amplitude-independent** (amp→0.5, a2_amp→0.2 leave the potential at
+1.035…+1.040; blind-verified) — no static config lifts it toward +2.

## 4. Blind adversarial verification — CONFIRMED
Independent verifier (agent `aed5f1d571dbc7e7b`, 2026-07-06; own LM harness; audit/pilot scripts + tests/ not read;
adversarially tasked to find ANY closing static config): **CLAIM CONFIRMED.** Reproduced (i) fixed-L reduced solve
to machine precision at every L, (ii) **Hseal = −0.959686 L-independent, no zero-crossing** (cold near-zero = under-
convergence, not closure), (iii) decomposition H(r_s) = −2 + angular(+1.040), (ξ/2)(Ith+N²Is)=+1.000000 exactly,
(iv) amplitude scan amp→0.5/a2→0.2 keeps the potential at +1.04 — **no config produced Hseal≥0.**

## 5. Classification of the collapse mechanism (Charles's taxonomy)
**STRUCTURAL static S-Dir closure failure**, specifically **(e) the π₂ matter sector cannot support finite-L
closure** (the static angular matter potential is a factor-~2 too weak to cancel the geometric boundary constant),
manifesting as **(d) a free-boundary degeneracy** (Hseal is L-independent → the H(r_s)=0 row cannot select any L, so
freeing L makes the solver drain L→0 degenerately). **NOT (a)** Hseal-incompatible-with-mirror (the mirror BCs ARE
satisfiable to machine precision); **NOT (b)** overconstrained (the fixed-L reduced system is well-posed, solves to
1e-15); **NOT (c)** a missing residual term (Stage-2b code blind-verified, no algebraic inconsistency found);
**NOT (f)** an S-Dir-specific artifact (a2'(r_s)≈0 at the relaxed solution, so the S-JC2 BC a2'(r_s)=0 would change
H(r_s) negligibly — the deficit is in the angular potential, not the seal-BC term).

Per the pre-registered rule: **no finite-L Hseal zero-crossing under fixed-L diagnostics ⇒ STRUCTURAL** (not a
numerical path issue — the fixed-L system is machine-solvable at every L; it is the closure that has no root).

## 6. Is any static S-Dir finite-L cell plausible? — NO
Hseal = −0.96 for all L∈[0.015,2.0] and for all matter/shear amplitudes tested; the deficit is L- and
amplitude-independent. A static S-Dir co-relaxed π₂ cell cannot close. (Scoped to this regime; π₂ tile only.)

## 7. Recommended next fork (a CHARLES decision — reasoning, not a directive)
The obstruction is a **specific constant deficit in the STATIC seal Hamiltonian**: H(r_s) = −2 + (angular matter
≈ +1). Fixes that do NOT touch this balance are ruled OUT by the diagnostics: **higher-ℓ shear** (the shear
kinetic/potential is ~0 at the seal) and the **S-JC2 seal fork** (a2'(r_s)≈0 already) would not supply the missing
+1. Only forks that ADD a term to the Hamiltonian constraint can:
- **(PRIMARY) Non-static / time-live sector.** The missing balance is a clean factor of 2, and canon
  **C-2026-07-04-1 (seal-involution SECTOR SPLIT)** already says the **spatial depth mirror φ→−φ governs the STATIC
  seal**, while **t→−t governs the TIME-ON sector**. The static spatial-mirror seal supplies exactly +1 of the +2
  needed; the natural home for the other +1 is the t→−t time-on sector (seal = time reversal, canon). This is the
  mathematically- AND canonically-indicated fork.
- **(SECONDARY) Embedded / critical-universe coupling.** The −2 is the boundary/cosmological constant of a LONE
  static cell; the finite-cell canon says the matter cell is MIRRORED against the universe cell at ONE critical
  amount. The effective boundary term for an embedded cell may differ from the bare −2 (the ambient/critical balance).
- **NOT recommended:** higher-ℓ shear, S-JC2, off-diagonal/Branch (none changes the −2-vs-+1 static balance;
  diagnostics show the deficit is in the angular potential, L- and amplitude-independent).

## 8. Scope warning (binding)
π₂ axisymmetric S² tile only — this collapse-mechanism finding **cannot bank Outcome A/B** for the π₃ hopfion (open
premise for Charles). Scoped to static · S-Dir · block-diagonal · Branch-P · ℓ=2-only · π₂ · λ=−½ · Z=8/ξ=κ=1/N=1.
Status: DESIGN / PROVISIONAL / Outcome D. No pin, no continuum, no physics verdict.

---

## CORRECTION / RETRACTION (2026-07-06 EOD-3, later same day) — the "structural factor-2 deficit" was a soft-mode over-read

Script `n5d_stage2_collapse_reconcile.py`. Two fixed-L probes (bounded, CPU, single process):

**(1) TRADEOFF — keeping Hseal in the objective reaches Hseal=0 at finite L:** at fixed L, the DROP-Hseal solve
(field eqs + BCs exact, Hseal not minimized) gives Hseal≈−0.9 — but the KEEP-Hseal solve (Hseal in the objective,
overdetermined by 1) reaches **Hseal=0.0000 with the field equations still satisfied** (Phi~1e-9), leaving only a
small ρ-mirror residual ~3e-5/L:

| L | drop-Hseal: Hseal | keep-Hseal: minPhi | Hseal | rho_mir |
|---|---|---|---|---|
| 0.6 | −0.937 | 1.9e-9 | 0.0000 | 4.3e-5 |
| 0.4 | −0.924 | 9.6e-9 | 0.0000 | 9.7e-5 |
| 0.2 | −0.877 | 2.1e-7 | 0.0000 | 4.6e-4 |
| 0.1 | −0.788 | 3.1e-6 | 0.0000 | 1.8e-3 |

**(2) SOFT-MODE — Hseal slides ~freely along a genuine near-null direction:** the fixed-L (drop-Hseal) Jacobian has
a **well-separated near-null mode** (s_min=6.7e-14 vs s_2nd=6.2e-9). Moving along it: **dHseal/ds = +1.5e-2** while
**d‖F_field‖/ds = +4e-10** — Hseal sweeps through 0 at ~2.6e7× the rate the field residual changes. Config A
(drop, Hseal=−0.92) and Config B (keep, Hseal=0) are **97% connected along this soft mode**. So **−0.96 was merely
where the drop-Hseal solve lands on a flat valley — NOT a hard floor.**

**What is RETRACTED:** §5 classification "(e) π₂ matter factor-2 too weak" and §6 "no static S-Dir finite-L cell
plausible" and the §7 headline that higher-ℓ/S-JC2 are ruled out *because of a hard deficit*. The "+1.000000 vs −2"
decomposition (§3) is a correct measurement of ONE valley point, but it is NOT a hard obstruction — Hseal is not
pinned there.

**What STANDS (measurements):** §1 small-L scaling; §2 fixed-L machine-precision solvability of the field system;
§3 term VALUES at the drop-Hseal point.

**Corrected mechanism (PROVISIONAL, pending a FRESH blind pass framed around the soft mode — the earlier blind
verifier inherited the author's drop-Hseal blind spot and so could not catch this):** the collapse is a
**FREE-BOUNDARY / SOFT-MODE DEGENERACY (classification d)** with severe ill-conditioning (s_min~1e-14) — the seal
closure is nearly degenerate with the field solution manifold, so L is not cleanly determined and the free-L LM
slides down a degenerate drain (Hseal→~0 AND L→0 both nearly cost-free; this matches the pilot's Hseal floor ≈−6e-3,
i.e. NEAR 0, not near −0.96). Per the pre-registered taxonomy this leans **NUMERICAL-PATH / degeneracy (item 8)**,
NOT a hard structural matter deficit (item 9). **Whether an EXACT finite-L closed cell exists is REOPENED:** the
joint {Hseal=0 ∧ ρ'(r_s)=0} residual is ~3e-5/L (smallest at LARGE L) — possibly a large-cell limit rather than a
hard no. **Owed before re-banking any mechanism: a fresh blind pass explicitly tasked to (a) confirm/deny the soft
mode + free Hseal-slide, (b) settle whether the soft mode is a physical zero-mode/gauge vs a discretization artifact,
(c) determine whether an exact finite-L (or large-L) closed cell exists.** π₂ tile only; DESIGN/PROVISIONAL/Outcome D.
