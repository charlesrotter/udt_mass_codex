# Class-B (charged-core) run — q closes π_φ, but no band; matching needs matter structure that doesn't emerge

**Date:** 2026-07-02. **Mode:** OBSERVE (Class-B charged-core embedded run; gate cleared, D1/D2/R4
blind-verified). **Driver:** Claude Code. **Scripts:** `cell_solver_f2d_classB_run.py`
(+ `scratch_f2d_classB_summary.json`), reusing the CAS-verified operators + embedded-matching machinery
+ two-tier filter. **Status:** **BLIND-VERIFIED 2026-07-02 (agent a6c617e, PASS — claim 2 attacked
hardest, held) — bankable as a scoped PROVISIONAL result.** UNLABELED. **NOT a discreteness/frame verdict.**
Foundation: `embedded_classB_mini_MAP.md` (D1/D2/R4), `verify_classB_derivations.py` (airtight π_ρ' identity),
`cell_solver_f2d_embedded_run_results.md` (the Class-A obstruction this addresses).

## Headline (lay first)
The **charged core solves HALF the Class-A obstruction cleanly, and the other half is a MATTER wall the
minimal core cannot supply** — a sharp, verified null pointing at a sourced-**matter** core.
1. **q closes the dilation-flux match (the mechanism, confirmed).** Imposing the inner BC π_φ,c=q (q a
   Newton unknown, D1) drives the flux residual R3→~1e-13, with **q determined ≈ +3.95 (N=1) / +3.82
   (N=2) ≈ π_φ,amb = Z·q_A = 4.0** (canon "external charge = seal flux"; seed-independent). The Class-A
   mirror left R3 stuck at −3.99. The charge genuinely rescues the π_φ match the gradient-free core failed.
2. **But NO band / NO matched cell** — and the obstruction is now a verified TWO-BRANCH MATTER wall:
   - **Where ρ'_amb > 0:** closing the ρ-flux match R4 REQUIRES **I_r > 0** (the airtight identity
     `π_ρ' = Zρφ'² − ξρI_r + κN²I_4θ/ρ³`), but **I_r ≈ 0 does not emerge** — N=1 rigid f=θ is an EXACT
     f-PDE zero (I_r~1e-17); N=2 forced-small (I_r~1e-5), far below the O(1–10) needed. The seeded I_r>0
     RELAXES away (V7: radial structure never free; near-rigid is the stationary solution).
   - **Where ρ'_amb ≤ 0** (past a turning-point ambient): R4 *opens* (can reach ~−0.06), **but then R5 —
     the skin angular-energy match E_ang,cell=m_amb — is the single-signed O(1) obstruction.**
   The leftover pair (R4,R5) has NO common zero; min ||(R4,R5)|| = 0.774 (N=1) / 2.68 (N=2) is a REAL
   floor (verifier's finer scan bracketing the turning point — not a coarse-scan miss). Either branch:
   the minimal φ-charge core lacks the MATTER STRUCTURE (radial I_r AND/OR the right E_ang) to match.

## Counting realization (over-by-1, faithful to Ruling 1 + D1)
Augmented unknowns `[φ(Nr), ρ(Nr), u(Nr·Nθ), q]`; inner BC π_φ,c=Zρ_c²φ'_c=q (no φ-mirror), ρ'_c=0,
f_r,c=0. Made SQUARE at fixed (a,L) by ONE added row = the seal flux match π_φ,s=π_φ,amb (which DETERMINES
q — D3-consistent; verifier: legitimate, not vacuously circular since R4,R5 stay leftover). Leftovers
R4=π_ρ,s−π_ρ,amb, R5=E_ang,s−m_amb read off; over-by-1 → closure only at isolated a. **No a closes both.**

## The deep read (the loop closes — argument, all pieces CAS+blind-verified)
Matching a gradient-carrying universe REQUIRES radial matter structure I_r>0 (R4 ruling); I_r>0 is NEVER
energetically free (Step-0 V7); the minimal φ-charge core does NOT force it → **the cell can exist only if
something FORCES matter structure, and a bare charge does not.** "The price of matching the universe"
(I_r>0 — a candidate for mass) is REQUIRED but NOT SUPPLIED here. The forward objects (structurally
motivated, not patches): a **sourced-MATTER core** (a D1 variant — inject winding/radial structure at the
core, not just φ-charge) and/or more in-frame matter freedom (X²/L6, P4). Also: R5 says the skin-energy
match is a second matter condition — the core must supply E_ang too.

## The I_r-vs-sign(ρ'_amb) free test — VACUOUS (honest)
No cell closed → the test cannot be positively confirmed (correctly labeled VACUOUS). The seeded-then-
relaxed I_r is an ambient-forcing artifact, NOT banked as evidence. (On unmatched N=2 rows I_r was
actually larger where ρ'_amb<0 — the opposite of a naive positive correlation — so no correlation is claimed.)

## Filters
Adapted Derrick + two-tier stability were correctly SKIPPED (no genuine cell to filter).

## Scope / premises
ONE slice: MODEL ambient (2 declared families: native radial ρ'_amb=+1, and a turning-point ρ_A=R0−c(r−r*)²
spanning ρ'_amb sign); N∈{1,2}; Z=8; ξ=κ=1; Nr=16/Nθ=12; bounded (a,L) box; **minimal Class-B (φ-charge
only)** — a sourced-matter core is the untested D1 variant. Nonexistence is numerical (many seeds) +
structural (the airtight π_ρ' identity + V7). All CHOSE/THEORY/MODEL tagged. NOT a discreteness/frame verdict.

## VERIFIER
**Blind adversarial pass — 2026-07-02, agent `a6c617e`. PASS (all claims).** Independent bounded re-checks
(own seeds/solves, not the JSON): (1) q closes π_φ CONFIRMED (q≈+3.95/+3.82 seed-independent; imposed-flux
row honest, not vacuously circular). (2) **I_r≈0 is REAL, not solver failure — attacked hardest:** 4 seed
shapes, amplitudes to 0.5 (seed I_r to 7.1), 300–400 iters, coupled + frozen-geometry f-PDE — I_r drained
to ~0 in EVERY converged solve (N=1 machine-zero/exact; N=2 ~1e-5 forced fixed point); large-I_r configs
all STALLED (not solutions). Could not make I_r persist. V7-confirmed. (3) R4-never-closes CONFIRMED +
SHARPENED to the two-branch (R4/I_r where ρ'_amb>0; R5/matter where ρ'_amb≤0) mechanism above; min-norm a
real floor. (4) I_r-correlation honestly VACUOUS, not dressed as confirmation. (5) gate sound, counting
genuinely square, no hollow checks, MODEL labeled, no band sculpted. **Forward read (something must FORCE
I_r>0 → sourced-MATTER core) is SOUND — a solver-first conclusion, not a mechanism import.**
