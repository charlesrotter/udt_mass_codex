# Class-B embedded-rung — pre-build RESONANCE TEST design (Charles's Derivations 1–7; NO build)

**Date:** 2026-07-07 · **Author:** Charles (derivations) + Claude Opus 4.8 (transcription). **Design/derivation only —
NO build, NO solve, NO pilot, NO physics verdict.** Status: DESIGN / PROVISIONAL. This is the SEAMLESS-PICKUP SPEC for
the next session's derivation pass. Builds on `classB_embedded_rung_gatecheck_results.md` (gate-checks: anchor cancels
in ratios to leading order; H_amb(N)=0 is a dead knob; real rung data = q_N + depth/node count) and the old no-band
Class-B-vs-continuous-ambient wall (`cell_solver_f2d_classB_run_results.md`).

## The banked framing (from the gate-checks + the old wall)
- The old no-band wall was **NOT a flux wall**: the dilation-flux match already closed, `π_{φ,c}=q ≈ 3.8–4.0 ≈ π_{φ,amb}`.
- The wall was the **matter-geometry pair (R4,R5)** = the ρ-momentum + angular-energy conditions. Two branches:
  - **Branch A** (`ρ'_amb>0`): closure requires radial matter energy `I_r>0`, but minimal Class-B matter **drains to
    `I_r≈0`** (radial structure never free under the f-PDE, even seeded large).
  - **Branch B** (`ρ'_amb≤0`): the ρ-momentum match opens, but the **angular-skin energy match R5** blocks.
- ⇒ the wall = **minimal Class-B matter lacks the radial/angular structure needed for embedding.** Replacing a
  continuous `q_amb` by a discrete `q_N` only **samples isolated points of the same failed continuous space** — it
  cannot by itself fix the wall.

## Derivation 1 & 5 — Branch A: the I_r resonance test (cheap, no-build)
The ρ-momentum (R4): `π'_ρ = Zρφ'² − ξρ I_r + κN_w² I_{4θ}/ρ³`. Matching to the ambient and solving for the required
radial matter term, using `q_N = Zρ_s² φ'(r_s)`:
```
I_{r,req}(N) = [ q_N²/(Z ρ_s³) + κ N_w² I_{4θ}/ρ_s³ − π'_{ρ,amb}(N) ] / (ξ ρ_s)
```
Natural minimal solution gives `I_{r,natural} ≈ 0`. **Branch A is evadable at rung N only if `I_{r,req}(N) ≈ 0`.**

## Derivation 2 & 7 — the depth match must be GAUGE-INVARIANT (a difference, not the seal value)
Class B fixes `φ(r_s)=0` with `φ'(r_s)` free. So one CANNOT also impose a raw `φ(r_s)=φ_N` (that abandons the Class-B
gauge). The rung-depth match must be a **difference**: `Δφ_cell = φ_c − φ_s = φ_c` (since `φ_s=0`), i.e.
```
Δφ_cell = Δφ_N        (equivalently  e^{φ_c − φ_s} = x_N)
```
**The correct rung conditions are `q_cell = q_N` AND `Δφ_cell = Δφ_N` — NOT `H_N` (dead knob), NOT raw `φ_s=φ_N`.**
Caveat (Der 7): matter is **φ-blind** (couples through `h_AB`, not φ), so a depth match `Δφ_cell=Δφ_N` **does NOT
directly add a matter force to the f-PDE** — `Δφ_N ⇏ I_r>0` unless it changes the solved geometry (ρ, h_AB, K) enough
to make radial structure energetically required.

## Derivation 6 — Branch B: the angular-energy resonance test (cheap, no-build)
When `ρ'_amb≤0`, R4 opens but the angular-energy match blocks: `R5 = E_{ang,cell} − m_amb`. Define
```
A_N = E_{ang,natural} − m_amb(N)
```
**Branch B is evadable at rung N only if `A_N ≈ 0` (crosses zero) for some rung.**

## Derivation 3 & 4 — why the wall likely survives + the build gate
The wall was a **matter-STRUCTURE wall**, not a wrong-ambient-value wall. So the discrete ladder can help only via:
1. **Resonant escape** — a rung lands where `I_{r,req}(N) ≈ 0` AND `A_N ≈ 0` (checkable NO-BUILD); or
2. **Structural escape** — the rung flux+depth match changes the f-sector boundary problem so radial structure stops
   draining (needs a real build; more important but not cheap).
**BUILD GATE (Der 4): do NOT build unless the rung changes R4/R5, not just q.** Merely supplying `q_N` → expect the old
wall to survive.

## NET — the next derivation pass (NO build): per-rung classification
For each candidate rung N, compute the tuple
```
N  ↦  ( q_N ,  Δφ_N ,  I_{r,req}(N) ,  A_N )
```
(q_N and Δφ_N from the ladder law: `q_N = 2Z√|s̃₁(d*_N)|(1−x_c)/Θ(N)`, `Θ(N)=(N+1)π+θ₀(N)`, `x_c=1/1101`; `I_{r,req}`,
`A_N` from the R4/R5 identities above — the ambient `π'_{ρ,amb}(N)`, `m_amb(N)`, `E_{ang,natural}` reconstructed from
the rung + the natural minimal-matter solution). Then classify:
| class | condition |
|---|---|
| **dead rung** | `I_{r,req}` large AND `A_N` large |
| **positive-branch candidate** | `I_{r,req}(N) ≈ 0` |
| **turning-branch candidate** | `A_N ≈ 0` |
| **TRUE candidate** | both near zero, or crossing in adjacent rungs |

**Only a TRUE candidate justifies a bounded Class-B single-rung flux/depth build.** If no rung makes both small, **do
not build** — the discreteness idea would be a discrete flux without a resonant boundary target, and the matter-
structure wall survives.

## Provisional read (Charles)
Discreteness is promising **only if it produces a resonant boundary target, not merely a discrete flux.** The old wall
was a matter-structure wall, so the rung must either **avoid** the need for `I_r>0` (resonance) or **force** `I_r>0`
through geometry (structural). The first is the cheap next test above; the second is the only reason a build would be
worth it.

## OWED FIRST — blind re-derivation of the load-bearing identities (before the classification pass builds on them)
This DESIGN doc is a faithful TRANSCRIPTION of Charles's Der 1-7; the R4/R5 identities and the old no-band numbers were
NOT independently re-derived here — they are cited to `cell_solver_f2d_classB_run_results.md`. **The entire rung
classification rests on `I_{r,req}(N)` and `A_N` being exactly right, so run a BLIND pass FIRST (or in parallel):**
(i) independently re-derive `π'_ρ = Zρφ'² − ξρI_r + κN_w²I_{4θ}/ρ³` and hence `I_{r,req}(N)` from the ρ-momentum
condition (R4), and `A_N = E_{ang,natural} − m_amb(N)` from the angular-energy condition (R5), from the native
action/junction — NOT from this doc; (ii) confirm the old no-band run's two-branch numbers (`q≈3.8-4.0` closed π_φ;
minimal matter `I_r→0`; Branch A needs I_r>0, Branch B blocks on R5). Frame it NEUTRALLY (adjudicate, don't confirm —
see [[verifier-framing-and-residual-artifacts]] / `n5d_stage2_collapse_audit_results.md` for why this session that
mattered twice). Only after the identities are blind-verified should the per-rung `(q_N, Δφ_N, I_{r,req}(N), A_N)`
classification be trusted as a build gate.

## Premise ledger (for the next pass)
- `q_N`, `Δφ_N`, `Θ(N)`, `x_c=1/1101` — DERIVED (Stage-D ladder, blind-verified, canon); the anchor cancels in ratios
  to leading order (gate-check a). CHOSE/reconstruct: `π'_{ρ,amb}(N)`, `m_amb(N)`, `E_{ang,natural}`, `ρ_s`, `I_{4θ}`
  at the rung seal — flag each as reconstructed-vs-tabulated; the ladder does NOT tabulate `π'_ρ` or `m_amb` per rung.
- Watch the template tripwire: run as OBSERVE (which rungs, if any, hit resonance) — not TARGET (find the lepton
  ladder). Data-blind on lepton numbers; rides the one z_CMB anchor (x_c), which cancels in ratios to leading order.
- Scope: π₂ static S-Dir tile; Class-B seal (`seal_phi="B"` already in `cell_solver_f2d.py`); NO Outcome A/B, NO
  pin/continuum, NO π₃. DESIGN / PROVISIONAL / Outcome D.
