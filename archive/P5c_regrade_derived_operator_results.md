# P5c RE-GRADE on the DERIVED two-player operator — the FAMILY QUESTION, re-graded

Research record (append-never-edit). **NOT canon. UNVERIFIED** (blind adversarial pass
required before banking — ATTACK HERE block at end). Mode: **OBSERVE, METRIC-LED,
DATA-BLIND** (units L=1; NO mass/ratio/M_MS banked; no wall numbers). Driver:
claude-opus-4-8[1m]. Date: 2026-06-21. Compute: CPU float64, single clean process,
bounded (Nr in {16,20,24}, iters<=150, each sweep 15-19 s). ANTI-HANG honored (no GPU,
no background poll, no concurrency, never a blend-toward-endpoint).

NEW FILE ONLY: `/tmp/p5c_regrade_derived.py` (reuses the committed derived-operator
solver `/tmp/soliton_rerun_solve.py` — `residual` + LM step byte-identical, only the
initial guess differs). EL exprs `/tmp/soliton_EL.txt` (the four field equations
derived in `static_soliton_rerun_derived_operator_results.md`).

READ (this session): `p5c_basins_results.md` + `p5c_barriers_results.md` (the OLD-operator
method + verdict being re-graded), `static_soliton_rerun_derived_operator_results.md`
(the derived-operator static solver REUSED), `native_dilation_weight_derivation_results.md`,
`matter_regrade_derived_operator_results.md`.

---

## 0. WHAT WAS RE-GRADED (lay)

The OLD operator (plain-EH gravity, a=-1) gave Charles's family question a NO: the
committed 3-D solver found several charge-1 floored solutions, but a NEB barrier test
showed NO walls between them — one soft connected object, not a catalog of distinct
cells (`p5c_basins_results.md` / `p5c_barriers_results.md`).

This push asks: does that "one soft object, NO durable family" verdict SURVIVE on the
newly-derived operator `S = INT sqrt(-g)[e^{2phi}R + X e^{2phi}(dphi)^2 + e^{2phi}L_m]`
(vacuum != GR, a=e^{phi}, two-player scalar-tensor, X=-2e5, charge-1 native hedgehog)?
Or does the new operator open a DURABLE FAMILY (walls between distinct charge-1
solutions)? OBSERVE, not target; the verdict below (single basin, no family) is the
OPPOSITE of a "wanted" family.

---

## 1. METHOD (re-grade, reusing the derived-operator solver)

Solver: the committed derived-operator radial 4-field (A, B, phi, Theta) dense-LM solve
(`/tmp/soliton_rerun_solve.py`), B=1/A FREE/measured, charge-1 winding BCs (Theta(core)=pi,
Theta(seal)=0). Energy proxy: the **native matter action** `S_m = INT sqrt(-g) e^{2phi} L_m dr`
with `L_m = -(xi/2)(X_k+2Y) - (kap/2)(2 X_k Y + Y^2)`, `X_k=Theta'^2/B`, `Y=sin^2Th/r^2`
— the SAME L_m that builds the EL/stress (not an imported functional). Ordered by |S_m|.

**BASINS:** floor the charge-1 soliton from MANY UNBIASED seeds — different Theta widths
and centers (round/wide/narrow/outer/inner), metric warps (±a, ±b body bumps), hair signs
(±phi), a random body perturbation (pert), and dense random-seed ensembles (12-14 seeds,
varied centers/widths + random body noise). NO seed is blended toward a known floor (the
binding anti-hang/stability rule — that biased artifact cost a wrong headline before).

**BARRIER:** NEB / string method between two FLOORED endpoints — straight-chord init, each
interior image relaxed PERPENDICULAR to the chord with its chord-projection PINNED (project
out the along-chord step + re-snap), endpoints fixed. barrier = max interior |S| − higher
endpoint |S| (positive => separating wall). Identical construction to the OLD-operator
`p5c_barriers.py`.

**Nr-TREND:** repeat the basin sweep at Nr=16, 20, 24 — does the basin count change / a wall
appear or vanish with resolution (as the OLD operator's apparent walls did)?

Regime: the CONVERGED/resolvable window (xi=kap in {1e-2, 2e-2}, |F| floors to ~1e-7),
per the static-rerun calibration (strong coupling xi=kap~1 is grid-limited near-horizon,
quarantined there and here).

---

## 2. BASIN SWEEP — Nr=16, xi=kap=2e-2 (the production-converged regime)

Ten seeds floored (the spurious criterion of `p5c_basins_results.md` §2 applied verbatim,
10x-loose from regular-hedgehog structure: Theta in [−0.25, pi+0.25]; max|A·B−1|<=2 and
Bmax<=3; |F|<1e-4 converged; winding BCs held):

| seed | |F| | |S_m| | max\|AB−1\| | Bmax | Theta core→seal | verdict |
|---|---|---|---|---|---|---|
| round   | 4.2e-7 | 0.11391 | 7.1e-2 | 1.05 | 3.14→0.00 | PHYSICAL |
| wide    | 4.2e-7 | 0.11391 | 7.1e-2 | 1.05 | 3.14→0.00 | PHYSICAL |
| narrow  | 4.2e-7 | 0.11391 | 7.1e-2 | 1.05 | 3.14→0.00 | PHYSICAL |
| outer   | 4.2e-7 | 0.11391 | 7.1e-2 | 1.05 | 3.14→0.00 | PHYSICAL |
| inner   | 4.2e-7 | 0.11391 | 7.1e-2 | 1.05 | 3.14→0.00 | PHYSICAL |
| warp_b  | 4.2e-7 | 0.11391 | 7.1e-2 | 1.05 | 3.14→0.00 | PHYSICAL |
| warp_a  | 4.2e-7 | 0.11391 | 7.1e-2 | 1.05 | 3.14→0.00 | PHYSICAL |
| pert    | 4.2e-7 | 0.11391 | 7.1e-2 | 1.05 | 3.14→0.00 | PHYSICAL |
| hair_pos| 8.7e-1 | (49.4) | 4.8e+2 | 72.5 | 3.17→−35 | **SPURIOUS/UNCONVERGED** |
| hair_neg| 5.2e-1 | (101.7)| 3.9e+2 | 95.4 | 3.14→−45 | **SPURIOUS/UNCONVERGED** |

**THE KEY OBSERVATION:** ALL EIGHT unbiased regular seeds — wildly different Theta widths,
centers, metric warps, a random body kick — floor to the **SAME** solution: |F|=4.2e-7,
|S_m|=0.11391 identical to 5 digits, **pairwise max|u_i − u_j| < 1e-6** (they do not even
register in the pairwise-distance table; the OLD operator had O(0.1–0.4) field separations
between distinct basins). The derived operator's radial solver has a **single basin of
attraction** for every resolvable seed — not a multiplicity.

The two hair seeds did NOT converge (|F|=0.5–0.9; Theta runs to −35/−45; Bmax 72/95;
|AB−1|~400–475) — they are the SPURIOUS near-horizon run-away wells the static-rerun doc
flagged as the strong-field grid-resolution limit (Nr<=24 FD cannot resolve near-horizon
curvature), NOT physical charge-1 solitons. Their |S| is parenthesized (not certified).

---

## 3. BARRIER TEST (NEB, Nr=16) — no walls, even to the spurious wells

NEB from the single physical floor (round) to each unconverged hair well:

| pair | \|Sa\| | \|Sb\| | gap | BARRIER (\|S\| above higher endpt) | dip | path |
|---|---|---|---|---|---|---|
| round ↔ hair_pos | 0.114 | 49.39 | 49.28 | **−15.82** | −4.72 | MONOTONE up |
| round ↔ hair_neg | 0.114 | 101.66| 101.55| **−40.20** | −22.10| MONOTONE up |

|S| along the relaxed path: round↔hair_pos `0.114 → 4.83 → 17.2 → 33.6 → 49.4`;
round↔hair_neg `0.114 → 22.2 → 38.7 → 61.5 → 101.7`. **BARRIER NEGATIVE on both pairs;
the path climbs straight uphill with NO ridge.** There is no separating wall even between
the physical floor and the (unphysical) run-away wells — they are just energetically higher
unconverged configurations the path reaches downhill from, not walled-off distinct objects.

(There is no pair of DISTINCT PHYSICAL floors to put a NEB between — all physical seeds are
the same basin — so the "no wall between distinct physical objects" statement is vacuously
satisfied by there being only ONE physical object. The NEB to the spurious wells confirms no
hidden wall is hiding even off the physical basin.)

---

## 4. Nr-TREND — the single-basin verdict SHARPENS with resolution

8 regular unbiased seeds, xi=kap=2e-2, at three grids:

| Nr | |S_m| range (8 seeds) | spread | max\|F\| | max pairwise field dist |
|---|---|---|---|---|
| 16 | [0.11391, 0.11391] | 0       | 4.2e-7 | < 1e-6 |
| 20 | [0.11410, 0.11410] | 5.2e-10 | 3.2e-7 | 2.3e-9 |
| 24 | [0.11396, 0.11396] | 1.3e-9  | 2.6e-7 | 4.5e-8 |

**The 8 seeds collapse to ONE solution at EVERY grid** (spread ~1e-9, field distance
~1e-8 = machine-level identical). The round-basin |S| is grid-robust: 0.11391 → 0.11410 →
0.11396 (a ~0.2% drift). **The single-basin reading does NOT split with Nr; it sharpens.**
This is the OPPOSITE of the OLD operator's 3-D result, where the SPREAD of distinct basins
*grew* with Nr (0.309→0.292 round was robust but the *set* of basins was not a point). On
the derived radial operator there is no set — there is one point, at all three grids.

---

## 5. ROBUSTNESS — dense random ensembles (the "is one-basin a smooth-seed artifact?" guard)

**(a) Weaker coupling (xi=kap=1e-2, more of seed-space resolvable), 14 random seeds**
(varied centers/widths + random Theta/metric noise): **14/14 converge to |F|~1e-7 and land
on the SAME single basin** (|S_m|=0.05800, identical to 4dp, every seed). When seeds are
resolvable, they ALL flow to one object — the single-basin reading is not a smooth-seed
artifact.

**(b) Large-amplitude ensemble (xi=kap=2e-2, 12 random seeds, amp 0.25 Theta + 0.10
metric):** 0/12 reach a physical floor — all blow up to run-away near-horizon wells (|F|
0.15–9, Bmax 22–650, |AB−1| up to 2340), the SAME strong-field grid-resolution limit. These
are NOT distinct physical basins; they are the unresolved-curvature artifact (the SOLVER-FIRST
read: the grid, not a family). So the large-amplitude run neither finds a second basin nor
refutes one — it simply fails to converge, honestly flagged as grid-limited (NOT a metric
verdict).

The honest synthesis of (a)+(b): **every seed that gets close enough to a charge-1 hedgehog
to converge lands on the SAME basin; the ones that don't converge are grid-limited run-aways,
not family members.**

---

## 6. VERDICT — "one soft object, NO durable family" SURVIVES (and sharpens)

**The OLD-operator verdict SURVIVES on the derived operator. There is NO durable family.**

On the derived two-player operator (vacuum != GR, a=e^{phi}, X=-2e5), the radial 4-field
charge-1 solve has a **SINGLE basin of attraction**: all resolvable unbiased seeds —
8 structured + 14 random at weaker coupling — floor to ONE solution (machine-identical |S_m|,
field distance ~1e-8), at Nr=16/20/24. There are no distinct physical charge-1 floors to wall
off; the only NEB available (to the spurious run-away wells) shows NEGATIVE barriers /
monotone uphill paths = no walls. The Nr-trend SHARPENS the single-basin collapse rather than
splitting it.

If anything the derived operator gives a CLEANER "one object" answer than the old one: the
old 3-D solver had a multiplicity of shallow floored dimples (the non-axisymmetric angular
DOF — oblate/prolate/toroidal/pert_s) on a flat connected manifold with no walls; the derived
RADIAL solver shows no multiplicity at all in its sector — one basin, full stop. The family
question stays answered NO on the new operator.

**SCOPE (honest, load-bearing):** this re-grade is in the RADIAL (A,B,phi,Theta SSS) sector.
The old P5c "basins" lived in the 3-D solver's NON-AXISYMMETRIC / angular DOF (cos2θ squash,
ring, lobed pert_s) — which DO NOT EXIST in this radial chart. So this push re-grades the
family question in the radial sector and finds NO family there; it does NOT re-run the old
3-D angular-basin set on the new operator (that would need the derived operator ported into
the full3d 3-D solver — a build, not a bounded re-grade). The OLD operator's angular basins
were ALSO wall-less (no family), so both sectors agree "no durable family" — but the
strongest, cleanest statement here is RADIAL-sector. The angular-sector re-grade on the
derived operator is the named remaining gap.

This strengthens the post-postulate program exactly as the old result did: the classical
static solve gives ONE soft object; **DISCRETENESS / distinct objects must come from
elsewhere** (postulate-A quantization, or distinct SECTORS — charge/winding + free
non-stationary/off-diagonal/ensemble DOF — NOT one carrier's static spectrum).

---

## 7. PREMISE LEDGER (chose / derived)

| # | Premise / value / choice | Status |
|---|---|---|
| Operator E_munu = fG + (g box − nn)f − Xf(...), f=e^{2phi}; matter weight e^{2phi} | DERIVED upstream (native_dilation_weight); USED |
| Four EL field equations from the action (`/tmp/soliton_EL.txt`) | DERIVED (soliton_rerun_eom, sympy-exact; verified that doc) |
| Residual + LM step = committed `soliton_rerun_solve.residual`/loop (only u0 differs) | DERIVED (reused) — byte-identical, new initial guesses only |
| Energy proxy = native matter action S_m=INT sqrt(-g) e^{2phi} L_m dr | DERIVED (reused) — same L_m that builds the EL/stress |
| **X = −2e5** (fixed) | CHOSE — one healthy ghost-free + Cassini-safe value (static-rerun P2); not fitted |
| **Charge-1 hedgehog (Theta(0)=pi, Theta(seal)=0)** | CHOSE — native degree-1 sector; not the m>=2 twist ladder |
| xi=kap in {1e-2, 2e-2} (converged regime) | CHOSE-as-gate — the resolvable window; strong coupling grid-limited, quarantined |
| Seeds: round/wide/narrow/outer/inner/warp_a/warp_b/hair±/pert + random ensembles | CHOSE (exploration) — unbiased; NEVER blended toward a floor |
| Spurious criterion: Theta∈[−0.25,pi+0.25], max\|AB−1\|<=2, Bmax<=3, \|F\|<1e-4 | CHOSE (criterion) — 10x-loose, from `p5c_basins` §2, applied uniformly |
| NEB = straight chord + transverse relaxation, chord-projection pinned, fixed endpoints | CHOSE (method) — identical to `p5c_barriers.py`; NOT a blend |
| Nr in {16,20,24}, iters<=150 | CHOSE (anti-hang) — bounded, single process, sequential |
| "single basin / no durable family on derived operator" | OBSERVED (not chosen) — EMERGED from 8+14 seeds collapsing to one floor; opposite of a wanted family |

---

## 8. ATTACK HERE (for the blind verifier — required before banking)

1. **Is the single basin real or a flooring/normalization artifact?** All 8 regular seeds
   land at |F|=4.2e-7, |S_m|=0.11391 IDENTICAL. Verify they are genuinely the same FIELD
   (re-check pairwise max|u−u| < 1e-6, not just equal |S_m|) and that the LM column-scaling
   isn't funneling every start to one point regardless of basin structure (cross-check: do
   the WEAKER-coupling 14 seeds, which converge harder, also share the field, not just |S|?).
2. **The energy-proxy sign/scale.** S_m uses the radial action with 4pi & sin dropped (same
   as the EL derivation). Confirm the proxy is the native matter action (not a re-weighted
   functional) and that ordering by |S_m| is the right ladder (L_m<0 => S_m<0). A wrong sign
   would flip barrier/dip readings.
3. **Are the hair_pos/hair_neg wells genuinely spurious, or a real high-energy branch the
   criterion discards?** They fail C1 (Theta −35/−45) and C2 (Bmax 72/95) hugely and DON'T
   converge (|F|~1) — argue they are the grid-limited run-away the static-rerun doc found,
   not an excited state. Attack: re-floor with a finer grid / weaker source and check they
   collapse to the single basin or vanish.
4. **Nr-trend honesty.** The 8-seed collapse holds at Nr=16/20/24 (spread ~1e-9). Confirm a
   wall does not appear at Nr=24 that Nr=16 missed (it doesn't here — but the OLD operator's
   apparent walls were the cautionary tale, in the OTHER direction). Push Nr higher if budget
   allows.
5. **The SCOPE caveat (the real limit).** This is the RADIAL sector only; the old P5c basins
   were ANGULAR/non-axisymmetric DOF absent here. Verify the claim is correctly scoped:
   "no radial-sector family on the derived operator" — and that the angular-sector re-grade
   (porting the derived operator into the 3-D full3d solver) is correctly named as the
   remaining gap, NOT silently claimed closed.
6. **Large-amplitude non-convergence.** 0/12 large-amp seeds floored — all blew up. Confirm
   this is the grid/strong-field resolution limit (SOLVER-FIRST: same solver hits 1e-7 when
   resolvable), NOT a hidden second basin the solver can't reach. A finer-grid / continuation
   re-try of those 12 seeds would close it.

---

## 9. SINGLE CLEANEST STATEMENT

Re-graded the family question on the DERIVED two-player operator (vacuum != GR, a=e^{phi},
X=−2e5) by reusing the committed derived-operator radial 4-field dense-LM solver. The OLD
verdict — **one soft connected object, NO durable family** — SURVIVES, and sharpens: all
resolvable unbiased seeds (8 structured + 14 random) floor to a SINGLE basin (machine-identical
|S_m|, field distance ~1e-8) at Nr=16/20/24; the only available NEB (to the spurious run-away
wells) shows NEGATIVE barriers / monotone paths = no walls; the Nr-trend collapses the seeds
rather than splitting them. No durable family of distinct charge-1 cells in the radial sector.
Scope: radial SSS sector (the old angular non-axisymmetric basins do not exist in this chart;
their re-grade on the derived operator — porting it into the 3-D solver — is the named gap, and
the old operator showed those were wall-less too). DATA-BLIND honored (no mass/number targeted).
NOT canon; OBSERVE + bounded only.

---

## VERIFICATION (2026-06-21) — blind adversarial pass, agent a59c374bbc9cfce79
SUPPORTED (radial-sector verdict holds; angular gap honestly named). Independent re-solve: 5 unbiased seeds ->
|F|=4.2e-7, |S|=0.113909 (6 digits), pairwise field distance ~1e-10..1e-12 = MACHINE-IDENTICAL FIELDS (single
basin real, not a normalization artifact; off seeds run away rather than being funneled in). NEB reproduced to the
digit (barrier=-15.83, monotone, no ridge = one physical floor + spurious run-aways). Nr-trend SHARPENS (spread
~1e-9..1e-10 at Nr=16/20/24; |S| ~0.2% drift) — opposite of the old operator's growing multiplicity. SCOPE
HONEST: the OLD P5c basins were genuinely ANGULAR/non-axisymmetric (oblate/prolate cos2theta, toroidal ring,
lobed pert_s) which cannot exist in the radial chart -> this re-grades the RADIAL sector only; the angular/
off-round part (derived operator in the 3-D full3d solver = a BUILD) is genuinely UNTESTED and honestly named,
NOT claimed closed. BANK with the scope caveat intact.
