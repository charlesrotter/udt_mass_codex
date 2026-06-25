# Topological Winding-Soliton Sectors m=1,2,3,4 — MAP tile — 2026-06-16

**Push:** Winding-catalog map (completeness criteria 6, 8, 9). **Mode:** OBSERVE.
**DATA-BLIND** (units L=sqrt(kappa/xi)=1; no empirical/wall numbers loaded).
**Driver:** Claude (Opus 4.8, 1M). **Builds on:** off_round_solver_results.md (#60 wall
broken — full3d_newton.py explicit-Jacobian Newton/LM, category-A, value-equivalent 1.4e-14).
**New script (committed, no committed file edited):** `winding_catalog_map.py`.

## THE QUESTION
Does UDT carry a discrete catalog of distinct stable particle TYPES along the
topologically-PROTECTED winding (matter charge) axis? Solve the coupled
Einstein+L2+L4 static field equations in each winding sector m=1..4. Winding is an
integer (the Theta core/seal BC is hard-pinned: Theta(core)=m*pi, Theta(seal)=0), so an
m=2 config CANNOT relax to m=1 — each sector is an unambiguous question.

## METHOD / REGIME (one tile)
- Solver: full3d_newton.newton_solve (explicit jacrev Jacobian + augmented-lstsq LM,
  B=1/A FREE, all five fields a,b,c,d,Theta free, angular Einstein eqns imposed).
- Seeds: radial soliton solved AT winding m (spectral_radial_soliton.solve(m=m)) where it
  converges (m=1 only); ANALYTIC winding seed (Theta = m*pi*cos-ramp core->seal, b linear
  depth ramp, a=-b, c=d=0) for m>=2. **FINDING: the legacy radial LM solver does NOT
  converge for m>=2 (returns NaN/large F) — the analytic seed + full-3-D Newton is what
  carries the higher sectors.**
- Grid (production tile): Nr=18, Nth=6, Nps=8; p=0.4, kap8=0.05.
- m=2 cross-check: Nr=18,Nth=6,Nps=8 to a DEEP floor (30 Newton iters) to test whether the
  large mass is a convergence artifact.
- Stability: (a) matter-action second variation E''=d2/d eps2 of S=int sqrt(-g)(L2+L4) along
  controlled Theta modes (oblate P2, psi-breaking cos psi/cos 2psi/sin psi) at the converged
  metric; (b) RELAX test — inject a finite psi-breaking (cos 2psi) Theta deformation, re-solve
  the full coupled residual, see if psi-structure decays (axisym stable) or persists (off-axisym
  member). SIGN CALIBRATION via the round m=1 hedgehog (known stable): for m=1, S''<0 on ALL
  modes AND the relax-injected psi-structure decays + M_MS rises => **S''<0 = STABLE direction
  (energy E=-S curves UP); S''>0 would be the negative/downhill (platonic) mode.**

## RESULTS PER SECTOR (production tile, grid 18x6x8, p=0.4, kap8=0.05)

| m | seed     | Phi (start->end) | M_MS     | tvar (shape) | psivar    | maxB1A | per-comp res (max) |
|---|----------|------------------|----------|--------------|-----------|--------|--------------------|
| 1 | radial   | 1.55e3 -> 3.9e-11| 0.297669 | 0.0160 round | 8.5e-14   | 0.185  | tt2.1e-6 el7.9e-7  |
| 2 | analytic | 3.16e1 -> 1.5e-5 | 59.929   | 0.414 oblate | 5.2e-10   | 2.582  | tt2.8e-3 el2.2e-3  |
| 3 | analytic | 7.66e1 -> 1.4e-6 | 1024.28  | 1.013 struct | 2.9e-9    | 5.095  | tt4.8e-2 el1.0e-1  |
| 4 | analytic | 1.80e2 -> 2.5e-5 | 53.554   | 0.311 oblate | 6.3e-12   | 3.479  | tt6.2e-4 el2.3e-3  |

- m=1 reaches a DEEP floor (Phi 3.9e-11; raw residuals ~1e-7..1e-6 — fully converged).
  Round (tvar 0.016, psivar ~0). M_MS=0.298 ~ the #60 3-D round value 0.289.
- m=2,3,4 CONVERGE from the analytic winding seed (Phi drops 6-8 orders), but at 12 iters
  the RAW per-component Einstein residuals are 1e-3..1e-1 (NOT the floor) — the high-winding
  deep core is under-resolved on 18x6x8. So the M_MS *absolute values at 12 iters are
  resolution/convergence-limited*, AND the m=3 (1024) >> m=4 (53.6) NON-MONOTONICITY is the
  fingerprint of that (m=3 had the worst raw residuals).

## m=2 DEEP CROSS-CHECK (30 Newton iters, same grid)
Phi 3.16e1 -> **6.0e-11**; raw residuals all ~1e-6 (AT the floor). **M_MS = 59.272**
(vs 59.929 at 12 iters: ~1% shift). tvar=0.605 (MORE oblate than the 12-iter 0.41 — the
non-sphericity deepens with convergence, it is real geometry not under-convergence).
maxB1A=2.52 (B=1/A strongly free at the deep floor). psivar=5.8e-8 (axisymmetric, as built).
=> **The m=2 mass ~59 is ROBUST, not a convergence artifact.** One unit of winding multiplies
the mass by ~200x (0.30 -> 59).

## STABILITY (all sectors)
Matter-action second variation E'' (S'') along every probed mode is NEGATIVE in EVERY sector
(m=1: -2.3e2..-4.0e2; m=2: -1.2e3..-2.5e3; m=3: -1.2e4..-3.6e4; m=4: -1.7e3..-3.2e3),
INCLUDING the psi-breaking modes. By the m=1 sign calibration (S''<0 = stable), **no
psi-symmetry-breaking NEGATIVE (downhill) mode was detected in any sector** at this grid.
Relax test: the injected psi-breaking deformation DECAYS on re-solve in every sector
(m=1 1.0e-2->6.2e-3; m=2 1.5e-2->6.9e-3; m=3 1.6e-2->1.5e-2 [weak decay]; m=4 1.4e-2->3.9e-3),
and M_MS RISES under the perturbation for m=1,3,4 (m=2 dips ~1%). Consistent verdict:
**the axisymmetric winding solitons are stable (or at worst marginal) against the platonic
psi-breaking channel at this grid** — NO clear platonic ground-state fingerprint surfaced.
HONEST METHOD LIMIT: the E'' probe is the matter-sector second variation at FIXED metric (the
leading indicator; the metric responds adiabatically) — NOT the full coupled gravitational
Hessian. The m=3 weak psi-decay + larger raw residual is the one place to re-probe at finer grid.

## MASS PROGRESSION (data-blind; NOT compared to any empirical value)
M_MS: m=1 0.298 -> m=2 59 (deep-converged) -> m=3 1024* -> m=4 54* (* = under-converged at
this grid, absolute values unreliable; m=2 is the only m>=2 value cross-checked to the floor).
The robust statement: the winding mass is **STRONGLY SUPER-LINEAR / explosive** in the charge
— ~200x for m=1->m=2 — NOT the ~linear-in-charge scaling of flat-space Skyrmions. The deep
gravitational well of the steep multi-winding core dominates. A clean m=3,m=4 mass requires a
finer grid + deeper iterations (the m=2 deep run took 461s at 18x6x8).

## VERDICT ON THE CATALOG (winding axis), regime-stamped
At grid 18x6x8, p=0.4, kap8=0.05, B=1/A free, axisymmetric matter:
- **There IS a discrete family of distinct, topologically-protected winding solitons.** Every
  sector m=1..4 supports a converging static solution that cannot relax to a lower charge.
- They are GENUINELY DISTINCT TYPES, not one round family rescaled: m=1 is round (tvar 0.016);
  m>=2 are strongly NON-SPHERICAL (oblate/structured, tvar 0.3-1.0) with very different,
  strongly-super-linear masses and far larger B=1/A departure (maxB1A 0.19 -> 2.5-5.1).
- Within reach of this tile, each axisymmetric winding type appears STABLE (no psi-breaking
  negative mode found) — i.e. the catalog members are the axisymmetric windings themselves;
  no evidence (yet) that they break to platonic ground states. This is the OPPOSITE of the
  flat-space Skyrme expectation (m>=2 go platonic) and is itself a notable UDT-specific result.

## CATEGORY-A CONFIRMATION
Category-A only. Residual physics imported verbatim (value-equivalent to the committed
full3d_solver to 1.4e-14, established in off_round_solver_results.md). B=1/A FREE in every
sector (maxB1A 0.19/2.58/5.10/3.48; 2.52 at the m=2 deep floor — NOT tied). No injected term,
no linear-step-as-result, no tuning to a target. The winding charge is the topological BC, not
a patch. UNAVOIDABLE category-B moves: NONE.

## HONEST LIMITS / WHAT THIS TILE DROPS
- m=3,m=4 NOT converged to the floor at this grid (raw residuals 1e-2..1e-1) — their absolute
  M_MS and the non-monotonicity are resolution artifacts; only the m=2 mass (~59) is floor-verified.
- AXISYMMETRIC only. The live theta operator is exact for axisym shapes; a true non-axisym
  (platonic) SEARCH (m_azimuthal!=0, the SH-exact theta op) is NOT done — the E''/relax probes
  only test the LEADING psi-breaking channel, they do not exhaustively search platonic minima.
- Stability = matter-sector second variation at fixed metric + finite relax test, NOT the full
  coupled gravitational Hessian. A negative GRAVITATIONAL mode would not be caught here.
- Single (p,kap8)=(0.4,0.05); single grid family. No grid-convergence study of the masses.
- Radial-LM legacy seed builder fails for m>=2 (recorded; the analytic seed + Newton is the path).

## REUSABLE ARTIFACT
- `winding_catalog_map.py` (NEW; committed). Env knobs: NR/NTH/NPS/MS/MAXIT/RELAXIT/RELAX/P/KAP8/OUT.
  Contains: analytic_winding_seed, winding_seed (radial w/ analytic fallback), run_sector,
  secondvar_probe, relax_test, a self-contained matter-action scalar (the committed
  full3d_spectral.matter_action has a latent NameError on `n` in its return — flagged, not edited).
- JSON dumps: winding_catalog_out.json (4-sector tile), /tmp/m2_deep.json (m=2 deep cross-check).

## PROVENANCE
Build+run: Claude (Opus 4.8 1M), 2026-06-16. Verifier-before-record: PENDING (this is the
builder record; an independent adversarial verifier pass is required before banking the catalog
verdict, per Self-Hardening Protocol).
