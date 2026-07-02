# First build — Class-A FREE (H=0) finite-mirror cell, N=1, Z ∈ {1, 8}

**Date:** 2026-07-01. **Mode:** OBSERVE (the pre-registered first build; discreteness_preregistration.md
Class-A FREE, AMENDMENT 2026-07-01b). **Driver:** Claude Code session. **Scripts:**
`cell_solver_f2d_first_build.py` (the scan + stability filter), reusing the CAS-verified operators of
`cell_solver_f2d.py`; `verify_f2d_reduction.py` (now 11/11, incl. the ported scale-symmetry check).
**Status:** UNLABELED observation. N=1 ONLY — one tile of the charter grid (§7 MAP). **NOT a
discreteness verdict, and NOT a frame verdict.** **BLIND-VERIFIED 2026-07-01 (agent aa88d488): the
N=1 negative is CONFIRMED + bankable as a scoped N=1 tile; the build was spec-faithful; BUT the
stability filter is NOT yet ready for N≥2 — see the ⚠️ note in "What was built" §2 and the VERIFIER
section.** The two doc overstatements it flagged are corrected below.

**Fixed values (all tagged):** N=1 (DERIVED-topological); ξ=κ=1 (CHOSE-units); Z∈{1,8} run BOTH
(CHOSE-fixed, pre-reg amendment; Z=8 = OBS-2 Route-A-structure-carrying-Route-B-number); Nr=16,
Nth=12 scan grid, {12,16,24} for grid-independence (CHOSE, anti-hang bound); L∈[0.45,2.0], 9 points
(CHOSE scan range); 3 distinct seeds amp∈{0.05,0.40,1.00} (CHOSE; criterion 2). No per-solution
retuning; Z held fixed within each scan (criterion 5 intact).

---

## Headline (lay first)

At **N=1**, the derived round static free-f(r,θ) cell with the minimal {L2,L4} matter and a Class-A
smooth mirror seal **produces no isolated stable finite cell.** From every starting guess, at every
cell size, at both Z, the fields relax the SAME way: the knot unwinds back to rigid (the matter
deformation u = f−θ drains to zero), and the geometry then runs away — the depth field φ heads to
−∞ and the size field ρ heads to +∞ — to suppress the leftover source of the (now rigid) knot. There
is **no finite resting size.** The free-boundary closure condition H(seal)=0 is **never met**: H(seal)
stays pinned negative (≈ −0.95, → −1) across the whole scanned range and never changes sign, so the
isolated-closure set is **EMPTY**. This is exactly what Step-0's virial analysis anticipated (rigid is
a strict energy minimum of the matter at N=1 → radial structure is never spontaneously favored; seeds
slide toward collapse) and it CONFIRMS, now with the knot fully free in (r,θ), the previously-banked
rigid-hedgehog collapse. The free solve was mandatory to reach this conclusion and it has now been done.

This is a **scoped negative on ONE tile** (N=1). Step-0 V1/OBS-3 proved rigid is stationary ONLY at
N=1; for N≥2 the θ-profile must deform (I_4θ ≠ 1), which moves the collapse balance BEFORE any radial
structure — so the N≥2 tiles are genuinely open and are the clear next runs (relax θ first). The frame
verdict is NOT reached.

---

## What was built (spec-faithful)

1. **Closure-MANIFOLD map (MAP §4 + §9.3).** For a grid of cell size L, the **fixed-L SQUARE field
   BVP** is solved (φ'=ρ'=0 and f_r=0 at BOTH mirror ends; the H=0 row dropped and L-as-unknown
   dropped — the well-conditioned square system). At each L, launched from **≥3 distinct seeds**. The
   H=0 closure would be where H(seal)(L)=0 along a converged branch (sign change → Newton/secant
   polish). Both the closure set AND the H≠0 continuum are reported.
2. **Stability filter (MAP §9.3/§4c/criterion 8) — the decisive step, MACHINERY built; FORMULATION
   NOT YET CORRECT (⚠️ must fix before N≥2).** At each H=0 closure solution the code forms the
   symmetric Hessian of the reduced action S = ∫ L̄ dr (per 4π) w.r.t. the interior field DOF
   (δφ, δρ, δu), via `torch.func.hessian`; real spectrum (`eigvalsh`); classify near-zero (flat →
   continuous family → not isolated), negative (Morse index), positive-definite (isolated stable).
   **⚠️ FORMULATION ERROR (blind verifier aa88d488):** the object is the Hessian of the ACTION, but
   pre-reg criterion 8 / MAP §9.3 name the reduced **ENERGY**. The action Hessian is **structurally
   ~90% indefinite even on a benign smooth config** (n_neg ≈ 130/144), driven by the wrong-sign
   geometry kinetic term −2e^{−2φ}ρ'² and the minus-signed matter potential. So "positive-definite ⇒
   isolated stable" essentially NEVER fires and a genuine cell would be MISCLASSIFIED unstable. The toy
   sanity check (below) validates the eigensolver MACHINERY only — it never exercises `action_S`, so it
   does not validate the physics object. **This is inconsequential at N=1 (no cells to classify) but
   LOAD-BEARING at N≥2 and MUST be reformulated first** — to the reduced ENERGY / a constraint-reduced
   Hessian gated on gradnorm≈0, AND/OR the project's banked constraint-respecting perturb-and-coupled-
   resolve test (`gravitating-soliton-stability-test`: the fixed-metric Hessian OVER-COUNTS
   instabilities for a gravitating soliton; the over-count guard here re-solves only the single
   most-negative eigenvector — grossly insufficient against ~130 negatives). — Built + run on a
   representative relaxed (NON-cell) config only; there were no genuine closures to filter at N=1.
3. **Robustness gates (MAP §9.4):** (a) ≥3 seeds; (b) grid-independence Nr∈{12,16,24} + a
   finite-difference radial-derivative cross-check; (c) Derrick + H-drift as artifact filters.

### Stability-Hessian SANITY CHECK (passed)
A manufactured quadratic action S(x)=½ xᵀA x with A having an exact null vector (1,1,0) returns
eigenvalues {0.000, 2.000, 2.000}; Hessian symmetric (err 0); Hessian == A (err 0); eigenvalues real;
the flat direction is detected as a zero mode. So the machinery correctly detects a continuous-family
zero mode. (Caveat stated: no exact continuous symmetry of the PHYSICAL system exists at fixed L, so a
physical near-zero eigenvalue is interpreted as a flat direction, with the toy validating detection.)

---

## What is there — N=1, Z=1 and Z=8 (identical up to the runaway endpoint)

**Seed-independence (criterion 2).** All 3 seeds, at the mid cell size, relax to a matter-decoupled
**stall/runaway** (never a converged stationary cell): the knot deformation u drains to ~0 (max|u| →
0), φ goes negative, ρ grows. Seeds land at different runaway endpoints (φ_c≈−2.7, ρ_c≈3.0 for the
low-amp seeds; φ_c≈−0.4, ρ_c≈12 for the amp=1.0 seed) but the OUTCOME is the same — no cell, H(seal)<0.
So the outcome is seed-independent even though the runaway destination is not.

**The continuum (H≠0 context, spec-required).** Relaxing across the full L grid (continuation):

| L | outcome | φ_c | ρ_c | max\|u\| | H(seal) | H-drift | ΔDerrick |
|---|---------|-----|-----|--------|---------|---------|----------|
| 0.45 | stall | −1.59 | 2.38 | 0.000 | −0.912 | 1e−8 | +0.49 |
| 0.84 | stall | −2.02 | 2.63 | 0.000 | −0.928 | 3e−8 | +0.90 |
| 1.23 | stall | −2.54 | 2.91 | 0.000 | −0.941 | 2e−8 | +1.30 |
| 1.61 | stall | −3.06 | 3.18 | 0.000 | −0.950 | 1e−8 | +1.69 |
| 2.00 | stall | −3.06 | 3.18 | 0.000 | −0.950 | 2e−8 | +2.10 |

H(seal) **on this converged continuation continuum** ∈ [−0.950, −0.912] — **NO sign change → NO H=0
closure.** (Scoping correction, verifier aa88d488: H(seal) does take a wide range incl. sign changes
on OTHER, NON-converged configs across the adversarial seed/L span — but closure counts ONLY on
converged branches, of which there are ZERO, so the "no closure" conclusion stands; the earlier
unqualified "never changes sign" phrasing over-generalized.) (Z=8 numerically identical to Z=1 to 3
digits — cell EXISTENCE is Z-independent, as the amendment expected.)

**Runaway is a genuine attractor, not a fixed point.** Extending the iteration budget 50→900 drives
φ_c monotonically −2.26 → −3.09 and ρ_c 2.83 → 3.24 with u≡0 and Phi decreasing but never reaching
machine-zero (iters always = maxit). The absolute residual is small only because e^{2φ}→0 suppresses
the unbalanced rigid ρ-source; the config is **not stationary.** The honest convergence gate therefore
requires Phi<1e−11 AND iters<maxit AND |φ| bounded (a loose absolute-Phi gate FALSE-PASSES the
runaway — a trap that was caught and fixed).

**Genuine H=0 closure set: EMPTY** (0 converged branches, 0 closures) at both Z.

**NON-cell characterization (what the relaxed endpoint is).** Running the stability filter on the
representative relaxed (stalled) config: the action-Hessian is massively indefinite (index n_neg ≈ 199
of 224 DOF; λ ∈ [−1.6e5, +1.9e3]) — consistent with "not a stable cell," as expected for a config
drifting down a runaway rather than sitting at a stationary point.

**Artifact filters (criterion, MAP §9.4c).** H-drift is tiny everywhere (≤ ~4e−8 → the discrete H is
well-conserved, operators sound). The Derrick residual ΔS is large and grows with L (+0.5 → +2.1) —
the Derrick identity S_a=S_b is a **necessary condition of a TRUE solution**, and these configs are not
true solutions, so a large ΔS is the CORRECT diagnostic reading (it flags them as non-solutions), not a
contradiction. There is no genuine solution for the artifact filter to reject or admit.

**Grid-independence of the negative (criterion 4).** The runaway persists at Nr∈{12,16,24} (Nθ scaled
10/14/22): all stall, all H(seal)≈−0.94, max|u|=0. The exact runaway endpoint (φ_c, ρ_c) drifts with
Nr because it is a runaway (no fixed point to converge to), but the QUALITATIVE outcome — stall,
matter-decoupled, H(seal)<0, no closure — is grid-independent. **FD-vs-spectral φ′ cross-check:** max
error 8e−12 → 7e−11 across the three grids (the spectral radial operator is validated against an
independent finite-difference derivative).

---

## Reading against the 9 pre-registered criteria (Class-A FREE, N=1)

- **(1) Isolated vs continuum:** N/A in the intended sense — there are **no stable finite cells at
  all** at N=1; the scanned manifold is a runaway continuum with H(seal)<0 throughout (no closure).
- **(2) Same solutions from different seeds:** the OUTCOME (no cell → runaway) is seed-independent;
  the runaway destination is seed-dependent. Consistent with "no cell," not with "a cell."
- **(3) Stability without imposed targets:** no cell holds together; nothing imposed.
- **(4) Grid/method independence:** the negative is grid-independent (Nr 12/16/24); FD cross-check ✓.
- **(5) No hidden fitting knobs:** Z held fixed per scan; run at BOTH Z∈{1,8}; existence is
  Z-independent; no per-solution retuning.
- **(6) Quantized flux:** N/A (Class-A FREE is q=0 by construction; no cell anyway).
- **(7) Branch consistency:** interior P only (Class-A FREE, closed mirror; no G-exterior/seal-flux in
  this sub-class); the derived interior EOMs are satisfied to the stall tolerance but there is no
  stationary cell.
- **(8) Perturbation survival:** the stability-filter MACHINERY is built (eigensolver validated on a
  toy) but its physics FORMULATION is not yet correct (§2 ⚠️ — action not energy); no genuine cell to
  test at N=1 anyway. Must be reformulated before it can classify N≥2 cells.
- **(9) Blind classification:** output is UNLABELED; no particle comparison.

**KEY ACCEPTANCE TEST (Class A):** "do the mirror-seal conditions close only at isolated cell sizes,
or can every nearby size be adjusted to close?" — **Neither**: at N=1 the conditions close at NO cell
size; the free-boundary H=0 is never satisfied by any relaxed configuration.

---

## Provenance / discipline

- **Observing, not targeting:** the run reports where the metric drains; no lump/mass/size was sought.
- **Solver-first (before any "no cell" reading):** (1) left out? — the matter basis is the
  pre-registered minimal {L2,L4}; X²/L6 are the explicitly-registered NEXT in-frame freedom (P4), not
  wrongly omitted. (2) numeric? — the runaway is monotone, seed-independent, grid-independent, and the
  operators are CAS-verified (11/11) with H-drift ≤4e−8 and FD-φ′ agreement ~1e−11; not a conditioning
  artifact. (3) frozen DOF? — φ, ρ, u all free; L scanned; both mirror ends free-natural; nothing
  frozen (Class-B seal and off-round are separate, later, registered tiles). (4) whole space? — 3
  seeds × 9 L × 2 Z, all consistent. The negative is solver-complete FOR THIS TILE.
- **Derived backstop:** Step-0 V7 (blind-verified) proves rigid is a strict local min of the matter
  energy at fixed geometry ⇒ u→0 is DERIVED, not a solver failure; and round_matter_reduction
  (banked) already showed the rigid hedgehog collapses. This build supplies the missing free-f(r,θ)
  confirmation that freeing the knot does not rescue it at N=1.
- **Scope:** N=1 only. Next tiles (open, not verdicts): **N≥2 with θ relaxed first** (Step-0 V1 —
  I_4θ≠1 changes the balance), then the in-frame freedoms X²/L6 (P4), then Class-B (charged/pinned
  seal), then off-round h, then time-live. Any null here propagates ONLY along the N=1, L2+L4, Class-A,
  round, static row (MAP §7).

## CAS additions this build
`verify_f2d_reduction.py`: added check (d) — the vacuum-P scale symmetry [OBS-1] (geometry + entire
ξ-sector scale-invariant, weight 0; κ-sector breaks it, weight λ⁻²). Now **11/11 PASS** (the original
10 unchanged). This closes the last CAS item owed by MAP §9.5.

## VERIFIER
**Blind adversarial + spec-faithfulness pass — 2026-07-01, agent `aa88d488`.**
**MANDATE 1 (spec faithfulness): YES, faithful** — closure-manifold map (≥3 seeds, both directions),
both Z∈{1,8}, grid-independence + FD, Derrick/H-drift artifact filters, H=0 (not H_amb), Class-A FREE
first — all FOLLOWED. Two flagged deviations: (a) it scans fixed-L square field solves reading
H(seal)(L) rather than the module's monolithic H=0+free-L residual — DEFENSIBLE (arguably more faithful
to §4; the verifier ran the monolithic solver itself and it ALSO fails to converge → the substitution
masks no solution); (b) the stability filter uses the action not the energy (see §2 ⚠️).
**MANDATE 2 (is the N=1 negative real?): PASS-WITH-CAVEATS.**
- **Runaway REAL, not a conditioning stall — CONFIRMED independently:** the verifier's own sweep got
  **0 converged fixed-L solves out of 100** adversarial (seed×L) attempts across both Z, φ0∈[−2,+1],
  ρ0∈[0.3,2.0], amp∈[0,3.0] + random u-kicks; budget probe (maxit 20→400) shows φ_c deepening
  −0.68→−3.57 monotonically, Phi→1.86e−11 but iters always = maxit; the spec module's OWN monolithic
  (H=0, free-L) residual also never converges (drives L→10⁸ / |φ|→13 / ρ_min<0). Robust to solve strategy.
- **Convergence gate CORRECT** (Phi<1e−11 ∧ iters<maxit ∧ ρ_min>1e−4 ∧ |φ|<8): it catches the textbook
  false-pass (Phi=7e−14 at L=3e8) and does NOT false-negative a genuine bounded cell.
- **Scoping HONEST** — no frame/discreteness overclaim; "N≥2 is the open decisive case" is load-bearing.
- **Caveats:** the stability filter is NOT ready for N≥2 (§2 ⚠️ — action not energy, ~90% indefinite,
  toy-only sanity check); the build under-sampled the far-from-rigid seed region (amp≤1.0; verifier
  pushed to amp=3.0 + kicks, still nothing — gap closed but noted); "H(seal) never changes sign" scoped
  (above). **BANKABLE as a scoped, blind-verified N=1 negative. The build is NOT yet trustworthy for
  N≥2 until the stability filter is reformulated.**
