# Class-B rung-resonance — per-rung classification (NO build): the matter-structure wall SURVIVES the discrete ladder

**Date:** 2026-07-07 · **Mode:** OBSERVE / classification only — NO solver build, NO implementation, NO physics
verdict, NO Outcome A/B, NO pin/continuum, NO π₃, NO lepton targeting. Data-blind. **Status: DESIGN / PROVISIONAL /
Outcome D.** Author: Claude Opus 4.8 (1M). Generator: `scratchpad/classify_rung_resonance.py`. Gate that this stands
on: `classB_rung_resonance_owed_first_adjudication.md` (identities BLIND-CONFIRMED). Ladder data:
`stageD_frozen_forecast.md:70-89` (N=20…39, blind-verified/canon φ/ρ-sector). Spec + `m_amb` adjudication: Charles
2026-07-07 (geometric angular seal target `T_ang,seal = 2 + H_amb`; gate-check-b `H_amb(N)=0` ⇒ **`T_ang,seal = 2`**;
Misner–Sharp `M_N=−q_N` kept SEPARATE, NOT inserted as the angular target).

## Fixed inputs (chose-or-derived)
- Couplings `Z=8` (THEORY, canon), `ξ=κ=1` (THEORY-minimal), `I_{4θ}=1` (rigid-hedgehog normalization; CHOSE — the
  natural/minimal profile; a reconstructed I_{4θ}(N) is a variant). Angular seal target `T_ang,seal=2` (Charles's
  adjudication, from `E_ang(r_s)=2+H_amb`, `H_amb(N)=0`).
- `q_N, Θ(N), a_seal(N)` — DERIVED (Stage-D ladder, blind-verified/canon; the z_CMB anchor `x_c=1/1101` cancels in
  ratios to leading order, gate-check a).
- **`ρ_s(N) = 1 ± a_seal(N)`, `a_seal=√Z/Θ`** — RECONSTRUCTED, HIGH-confidence: Lemma-D's Z-test gives
  `|ρ_s−1|(N=8)=0.0964 = √8/Θ(8)` exactly, so the sealing amplitude *is* `|ρ_s−1|`; parity sign from Stage-B B3
  (odd N → ρ_s<1, even N → ρ_s>1; 13/13 blind, zero exceptions). Ladder range N=20…39: `ρ_s ∈ [0.957, 1.043]`.
- `Δφ_N = φ_c − φ_s = φ_c = ln(1/1101) = −7.004` — the SHARED cosmic anchor depth (Class B sets φ_s=0). The rungs
  differ in node count N + charge q_N, NOT in total depth (Lemma D: "the anchor sets q's scale and the phase, not the
  sealing amplitude"). Reported per-rung but rung-INDEPENDENT; node count N is the per-rung depth-STRUCTURE index.
- **`π'_{ρ,amb}(N)` — RECONSTRUCTED, LOW-confidence (NOT banked as derived).** The frozen forecast tabulates the φ/ρ
  envelope, not the ambient's matter R4. Structural form only: the seal sits at an ambient ρ'-node ⇒ `π_ρ,amb=0` there
  and `π'_{ρ,amb} = −4e^{−2φ_s}ρ''_amb = −4ρ''_amb` (φ_s=0). SIGN by parity: even N (ρ_s>1, ρ-max, ρ''<0) → `π'_{ρ,amb}>0`;
  odd N (ρ_s<1, ρ-min, ρ''>0) → `π'_{ρ,amb}<0`. MAGNITUDE `4|ρ''_amb|` requires the ambient's ρ'' at the seal — NOT in
  the banked table; flagged uncertain and handled by casework below.

## THE TWO SCREENS

### Angular screen `A_N = E_ang,natural − 2`  (FULLY COMPUTABLE — no reconstructed input)
`E_ang,natural = (ξ/2)(1+N_w²) + (κN_w²/2)(I_{4θ}/ρ_s²)`.
- **N_w=1:** `A_N = 1/(2ρ_s²) − 1`. Over N=20…39: **`A_N ∈ [−0.540, −0.457]` — SINGLE-SIGNED NEGATIVE, never crosses 0.**
  Zero-crossing would require `ρ_s = 1/√2 = 0.7071`; the ladder's `ρ_s ∈ [0.957, 1.043]` NEVER reaches it. (That
  crossing needs `a_seal=0.293` ⇒ `Θ≈9.65` ⇒ `N≈2` — below the banked ladder scope `N≳8` and far below the forecast.)
- **N_w=2:** `A_N = 0.5 + 2/ρ_s²`. Over N=20…39: **`A_N ∈ [+2.340, +2.673]` — SINGLE-SIGNED POSITIVE, `≥2.3` always.**
- **SENSITIVITY TO THE CHOSE INPUT `I_{4θ}` (verifier-flagged, on the record):**
  `A_N(N_w=1)=I_{4θ}/(2ρ_s²)−1` ⇒ vanishes at `I_{4θ}=2ρ_s²≈1.83–2.18` (equivalently target `T≈1.46–1.55` vs 2). So a
  factor-~2 larger rigid moment would FLIP the N_w=1 angular screen into resonance — the N_w=1 verdict is NOT robust to
  `I_{4θ}` at the ~2 level. **N_w=2 IS robust:** `A_N(N_w=2)=0.5+2I_{4θ}/ρ_s² ≥ 0.5` for ANY `I_{4θ}>0` (the ξ-term
  structural floor), flipping only if `T≥2.5`. Mitigation: even if `I_{4θ}≈2` opened `A_N(N_w=1)≈0`, a TRUE candidate
  still needs `I_{r,req}≈0`, which is strictly impossible on odd rungs and undecided (unreconstructed `π'_{ρ,amb}`) on
  even rungs — so no *demonstrable* TRUE candidate appears regardless. The verdict is mitigated, not eliminated, by the
  two-screen AND. (A reconstructed `I_{4θ}(N)` for the actual sealed profile — not the rigid 1 — is the variant that
  would settle this; out of scope for this NO-BUILD screen.)
- **⇒ NO rung passes `A_N ≈ 0`, for either winding (at the rigid `I_{4θ}=1`). The angular channel is BLOCKED for every rung** — because the
  ladder's `ρ_s` is pinned near 1 (small sealing amplitude `a_seal ≤ 0.043`), it cannot depart far enough to bring the
  rigid winding's angular energy onto the geometric target 2.

### Radial screen `I_{r,req}(N) = [q_N²/(Zρ_s³) + κN_w²I_{4θ}/ρ_s³ − π'_{ρ,amb}(N)]/(ξρ_s)`
Realizability: `I_r = ½∫sinθ f_r² dθ ≥ 0`, so `I_{r,req}<0` = impossible, `>0` = radial structure required, `≈0` = resonance.
The flux term `q_N²/(Zρ_s³) ≈ 0.02` is tiny (q_N∈[0.22,0.42]); the **angular-skin term `κN_w²I_{4θ}/ρ_s³ ≈ N_w²`
DOMINATES**. So `I_{r,req}` resonance needs `π'_{ρ,amb}(N) ≈ q_N²/(Zρ_s³)+N_w²/ρ_s³` (≈0.90 for N_w=1, ≈3.6 for N_w=2).
- **Odd N (ρ_s<1): `π'_{ρ,amb}<0`** ⇒ `I_{r,req} > 0` strictly (both bracket terms +, minus a negative) — **RADIAL
  STRUCTURE REQUIRED, never resonance, never impossible.** (`I_{r,req}` at π'_{ρ,amb}=0: 1.10–1.20 (N_w=1) / 4.4–4.7 (N_w=2).)
- **Even N (ρ_s>1): `π'_{ρ,amb}>0`** ⇒ resonance `I_{r,req}≈0` is **POSSIBLE only if the (unreconstructed) magnitude
  `4|ρ''_amb|` lands on `pia_needed` (≈0.90 for N_w=1 / ≈3.6 for N_w=2).** NOT decidable from banked data — flagged.

## Result table (both windings; generator `classify_rung_resonance.py`)
`A_N` is exact; `Ir_req(pia=0)` is the agnostic-reference radial demand; `pia_needed` = the `π'_{ρ,amb}` a rung would
need for `I_r` resonance; `pia_sign` = the structural parity sign of `π'_{ρ,amb}`.

**N_w = 1** (A_N single-signed ≈ −0.5; all rungs `ang=blocked`):
```
 N  par   Theta    q_N     rho_s     A_N     Ir_req(pia=0)  pia_needed  pia_sign   Ir-flag
 20 even  66.53  0.41594  1.04251  -0.5399     0.86490       0.90167    + (max)  poss-if-pia~need
 21  odd  69.65  0.39732  0.95939  -0.4568     1.20366       1.15478    - (min)  RADIAL-REQ(odd)
 ...   (monotone; full 20 rows in the JSON/generator)  ...
 39  odd 126.05  0.21972  0.97756  -0.4768     1.10162       1.07690    - (min)  RADIAL-REQ(odd)
   A_N range [-0.5399, -0.4568]  -> SINGLE-SIGNED (blocked; crossing rho_s=0.707 unreachable, N~2)
```
**N_w = 2** (A_N single-signed ≈ +2.5; all rungs `ang=blocked`):
```
 N  par   Theta    q_N     rho_s     A_N     Ir_req(pia=0)  pia_needed  pia_sign   Ir-flag
 20 even  66.53  0.41594  1.04251  +2.3402     3.40469       3.54943    + (max)  poss-if-pia~need
 21  odd  69.65  0.39732  0.95939  +2.6729     4.74474       4.55207    - (min)  RADIAL-REQ(odd)
 ...   A_N range [+2.3402, +2.6729]  -> SINGLE-SIGNED (blocked; 0.5+2/rho^2 >= 2.3 always)  ...
```

## CLASSIFICATION SUMMARY (per the DESIGN-doc classes)
| Screen | N_w=1 | N_w=2 |
|---|---|---|
| **Which rungs pass `I_{r,req}≈0`?** | odd N: none (radial required). even N: only IF `π'_{ρ,amb}≈0.90` (unreconstructed — undecided) | odd N: none. even N: only IF `π'_{ρ,amb}≈3.6` (unreconstructed — undecided) |
| **Which rungs pass `A_N≈0`?** | **NONE** (A_N ≈ −0.5, single-signed) | **NONE** (A_N ≈ +2.5, single-signed) |
| **Any rung passes BOTH (TRUE candidate)?** | **NO** | **NO** |

- **Dead / positive-branch / turning-branch / TRUE:** every rung is **dead on the angular screen** (A_N blocked). Even
  rungs are at most a *conditional* positive-branch candidate on the radial screen (undecided pending `π'_{ρ,amb}`);
  odd rungs are radial-structure-required. **No rung is a TRUE candidate.**

## BUILD GATE (Der 4): **NOT MET → DO NOT build.**
No rung makes both screens small. The angular screen alone is single-signed away from zero for EVERY rung (both
windings), so the build gate fails independently of the unreconstructed `π'_{ρ,amb}` — the conclusion is robust to the
one low-confidence input. Supplying a discrete `q_N` samples isolated points of the same failed space: the ladder's
`ρ_s` stays pinned near 1, so the angular-energy target (2) is never met, and matter is φ-blind so the depth match
`Δφ_cell=Δφ_N` does not add the needed radial/angular structure. **The matter-structure wall SURVIVES the discrete
ladder** — as the DESIGN-doc provisional read anticipated (discreteness gives a discrete flux WITHOUT a resonant
boundary target). A build would be justified only by the *structural-escape* route (Der 3.2 — a rung changes the
f-sector boundary problem so radial structure stops draining), which this NO-BUILD screen cannot test.

## Cautions honored (Charles's spec)
1. `π'_{ρ,amb}(N)` is RECONSTRUCTED (structural sign only; magnitude not banked) — flagged; the verdict does not rely
   on it (angular screen decides). 2. `ρ_s(N)` reconstructed from `a_seal=√Z/Θ` (Lemma-D Z-test-anchored) — flagged.
   3. `M_N=−q_N` kept SEPARATE (a flux/mass accounting quantity), NOT used as the angular target. 4. No independently
   derived per-rung Misner–Sharp mass was computed; none inserted. 5. **A rung "hit" is NOT interpreted as a particle
   mass** (none hit anyway). **This is NOT a physics verdict and NOT a mass prediction** — it is a NO-BUILD pre-build
   screen that says a bounded Class-B single-rung flux/depth build is NOT presently justified.

## Scope / premises
π₂ static S-Dir tile; Class-B seal (`seal_phi="B"`); MODEL-free (ladder rungs, not a model ambient); N=20…39
(forecast range; N=20–22 banked, N≳23 extrapolation beyond the banked ladder — carries Stage-D's ≤0.4% law accuracy).
Windings N_w∈{1,2}. Data-blind on lepton numbers; rides only x_c (cancels in ratios to leading order). DESIGN /
PROVISIONAL / Outcome D. NOT TARGETING the lepton ladder — this was OBSERVE (which rungs, if any, hit resonance: none).

## VERIFIER
**Blind adversarial pass — 2026-07-07, agent `a5993671d47c56be4`. PASS (verdict CONFIRMED); one under-disclosed
sensitivity surfaced and now folded in above.** Independent re-derivation (from-scratch, not importing the generator)
reproduced A_N digit-for-digit both windings (N=20: −0.5399/+2.3402; N=39: −0.4768/+2.5929); re-ran
`classify_rung_resonance.py` = full 20-rung table matches. Adjudication:
- **A_N single-signed / crossing unreachable — CONFIRMED.** ρ_s=0.7071 needs a_seal=0.2929 → Θ=9.657 → N≈2 (outside
  N=20–39, below banked scope N≳8). Ladder ρ_s∈[0.957,1.043] never approaches it.
- **ρ_s=1±a_seal, a_seal=√Z/Θ — CONFIRMED/HONEST.** Θ(8)=9π+0.3209π=29.28; √8/29.28=0.0966 ≈ Lemma-D Z-test 0.0964;
  forecast-table a_seal = √8/Θ to 5 digits. Defensible leading-order proxy, RECONSTRUCTED-flag honest.
- **Parity sign logic for π'_{ρ,amb} — HONEST.** Odd N → all three bracket terms positive → I_{r,req}>0 strictly (never
  resonance) regardless of magnitude; doc honestly states the magnitude is unreconstructed and the verdict does NOT
  depend on it (angular screen decides). Confirmed: even forcing π'_{ρ,amb}=pia_needed on every even rung, the AND-gate
  still fails (A_N blocks all).
- **No targeting / data-blind — CONFIRMED.** Only Z=8, ξ=κ=I_{4θ}=1, x_c=1/1101 (CMB anchor, not a lepton mass); T=2
  traces to virial V5 geometry, not reverse-engineered.
- **ONE FRAGILITY (verifier's catch, now quantified in the Angular-screen §):** A_N(N_w=1) flips to resonance at
  `I_{4θ}≈2` (`T≈1.5`); N_w=2 robust (ξ-floor). Mitigated by the two-screen AND (odd-N radial block strict; even-N
  undecided) ⇒ no *demonstrable* TRUE candidate. Verifier recommended stating this on the record — DONE (above).
- **Scope — HONEST**, DESIGN/PROVISIONAL/Outcome D, no overclaim.
**Net (verifier): CONFIRM "no TRUE candidate → do not build," robust to the unreconstructed π'_{ρ,amb}.**
