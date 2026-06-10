# Sector-Weight Spectral Probe Results

Status: working audit, not canonical.
Created: 2026-06-10.
Script: `native_sector_weight_spectral_probe.py` (all numbers below reproduce
from it).
Alters nothing existing; new files only.

## Purpose

`particle_spectrum_native_geometry.md` sections 23-26 declared radial
coupling the next legitimate frontier: does the negative-phi radial sector
couple to the operator-sector action weights `W(A3)=1/4`, `W(S5)=5/12`,
`W(T8)=2/3`? Section 25 derived the weak form (projector-weighted action on
the common `q=1/3` branch, `A(P)=Tr(P)/12=W(P)`) and stated the stronger
hypothesis — a sector-dependent radial exponent `q(P)` selected by
`S_C1(q_P)/R = W(P)` — which section 26 explicitly **parked** as "a possible
excitation mechanism until a boundary condition derives them."

This audit is the first direct computational test of that parked gate: if
the sector-dependent `q(P)` hypothesis is a real mechanism, the eigenvalue
ladder of the native spectral probe on the `q_P` backgrounds should read the
weights `W(P)` in some pre-declared functional form. No fitting, no tuning,
no post-hoc transform shopping.

## Method

Backgrounds are pure self-similar cells `f(r) = (R_cell/r)^q` — exact
solutions of the collar equation `f_xx + f_x + 2sf = 0` (`x = ln r`) with
`s = q(1-q)/2` — no shell, no window, no tail. The probe is the repo's
native radial operator

```text
-(r^2 f R')' + Lambda R = omega^2 (r^2/f) R,
```

assembled by a vertex-centered control-volume scheme on a grid uniform in
`x = ln r` (second order; BCs sit exactly on boundary nodes). Inner BC
zero-flux at `r_min = R_cell e^{-12}`; outer BC both Dirichlet and zero-flux.
The repo's legacy ghost-node assembly was independently re-run and gives
identical ratio verdicts, so nothing below depends on the scheme choice.

Pre-declared candidates for the observed `omega_1` ratios, with a 0.1
percent match threshold declared up front:

- **(a)** `W(P)` ratios
- **(b)** `exp(W(P))` ratios
- **(c)** `sqrt(W(P))` ratios
- **(d)** no relation.

Pre-declared acceptance rule: a candidate counts as a coupling law only if
it holds across its **entire** comparison family (same experiment, same
outer BC, same reference sector). A single ratio inside threshold whose
family partners fail is pinned at high resolution and reported as an
isolated coincidence, not a coupling.

Three forward experiments:

- **EXP1.** Baseline spectra on the common `q=1/3` cell, `Lambda` in
  `{0, 2, 6}`, lowest 4 modes, both outer BCs, plus convergence checks.
- **EXP2.** Sector-depth hypothesis: same probe at `Lambda=2` on the `q_P`
  backgrounds solving `S_C1(q_P)/R = W(P)`:
  `q(A3) = sqrt(2)-1`, `q(S5) = (2 sqrt(10)-5)/3`,
  `q(T8) = (2 sqrt(22)-8)/3` (verified exact to ~1e-15 in the script).
- **EXP3.** Weight-as-potential: common `q=1/3` cell with
  `Lambda_eff = Lambda * Tr(P)`, `Tr(P)` in `{3, 5, 8}`.

Controls: flat-box sanity (`f=1, Lambda=0` reproduces `omega = n pi` to
max rel. dev. 8.6e-6); scale covariance (`omega_1 * R_cell` invariant to
~12 matched digits between `R_cell=1` and `R_cell=2`); `r_min`
insensitivity (7 matched digits when `r_min` is held fixed instead of
scaled). All reported modes grid-stable to >= 4.2 digits under grid
doubling and `xspan` deepening.

## Findings

### F1. The headline: verdict (d), no relation

No candidate relation (a)-(c) holds as a family-consistent coupling law at
the 0.1 percent threshold anywhere in EXP2 or EXP3. Systematic couplings
found: **NONE**.

### F2. EXP2: the spectrum is nearly insensitive to the sector depths

The `omega_1` shifts between the `q_P` backgrounds and the common branch
are tiny — observed ratios 1.014 to 1.041 (Dirichlet: 2.6/3.5/4.1 percent
for A3/S5/T8; flux: 1.4/1.8/2.2 percent) — where the candidates demand 18
to 700 percent (smallest candidate `exp(1/4-1/12) = 1.18`, largest
`W(T8)/W(common) = 8`). The best candidate anywhere in EXP2 is
`exp(W)` for A3/common (Dirichlet) at **13.1 percent** off — more than two
orders of magnitude outside threshold. The sector-depth hypothesis does not
imprint the weights on the ladder; it barely moves the ladder at all.

### F3. EXP3: a generic sqrt(Lambda) trend, one isolated coincidence

The `Lambda * Tr(P)` insertions shift `omega_1` by the generic amount a
growing potential shifts any such ladder (trending toward `sqrt(Lambda)`
scaling), with best-candidate deviations from 2.2 to 43 percent across the
twelve ratios — except one:

```text
EXP3, flux BC:  omega_1(Tr=8)/omega_1(Tr=3) = 1.5156069
                exp(W(T8) - W(A3)) = exp(5/12) = 1.5168968
                rel. dev. = 8.5e-4   (inside the 0.1 percent threshold)
```

Pinned at 4x and 8x grid resolution: the ratio is stable to 7.1 digits at
1.5156069136, i.e. the 8.5e-4 offset is a real converged nonzero offset
that merely lands inside the declared tolerance. Its family partner
(`Tr=5/Tr=3`, same BC, same candidate) fails at 5.0 percent — ~59x the
hit's deviation — and every other `exp(W)` ratio in EXP3 fails at 2 to 43
percent. Per the pre-declared family-consistency rule this is classified as
an **isolated numerical coincidence, not a coupling.** (This is exactly the
failure mode the rule was declared in advance to catch.)

### F4. Out of 60 candidate deviations, exactly one is inside threshold

20 observed ratios (10 in EXP2, 10 in EXP3, both BCs) x 3 candidates = 60
pre-declared comparisons. 59 fail, most by one to three orders of
magnitude; the single pass is the F3 coincidence. There is no near-miss
cluster suggesting a slightly wrong functional form.

## Verdicts

1. **Clean negative.** The parked sector-dependent `q` gate
   (`S_C1(q_P)/R = W(P)`) does **not** couple to the sector weights `W(P)`
   through the eigenvalue ladder of the native spectral probe on pure
   self-similar cells — not as `W` ratios, not as `exp(W)` ratios, not as
   `sqrt(W)` ratios. EXP2 fails by two orders of magnitude; EXP3's single
   threshold hit is a family-inconsistent coincidence.
2. **Scope limits, stated precisely.** This kills the eigenvalue-ladder
   readout of the gate, not the gate's every possible role: `W(P)` could
   still enter through non-spectral channels (action normalization, anchor
   scale, transfer ladders), and the result is specific to this operator,
   these BCs, and pure self-similar backgrounds. What it rules out is the
   cheapest and most natural readout.
3. **Status upgrade for section 26.** The spectrum doc already graded
   sector-dependent `q(P)` as hypothesis-only ("parked ... until a boundary
   condition derives them"). This audit moves it from "parked hypothesis"
   to **"tested and failed as an eigenvalue-ladder mechanism."** Future
   sessions should not spend spectral-probe effort on `q_P` backgrounds.
4. **Where the radial-coupling search should go next.** Of the five routes
   catalogued in section 24, route 1 (projector-weight coupling) has now
   had its spectral form tested and rejected. The search should move to the
   remaining routes — two-form channel coupling, three-form support, kernel
   energy — or to non-spectral readouts of `W(P)` (the weak section-25 form
   `A(P) = Tr(P)/12` on the common branch remains intact and untouched).

## Verifier record

Blind adversarial verifier, 2026-06-10, agent `ac46ffbc01358daff`,
instructed to independently re-derive the spectra and attack the negative
verdict. Outcome:

- Operator assembly, boundary conditions, and background construction
  **CONFIRMED** correct against the stated continuum problem.
- Eigenvalues independently reproduced to >= 5.5 digits by **three**
  methods: the analytic Bessel closed form for `Lambda=0`
  (`omega_n = (1+q) j_{nu,n}` with `nu = (1-q)/(2(1+q))`), a shooting
  method, and a uniform-in-r finite-difference assembly with Richardson
  extrapolation.
- The legacy ghost-node assembly was re-run and gives the identical
  verdict pattern (ratios agree to ~1e-5 with the control-volume scheme),
  so no scheme bias.
- All 60 candidate deviations recomputed independently: exactly one inside
  threshold, and it is correctly classified — its family partners fail the
  same candidate by ~50x.
- The scale-covariance control was checked to be mathematically necessary
  (the pure power-law cell has no intrinsic scale besides `R_cell`) and
  passed.
- Minor notes, neither affecting the verdict: the legacy scheme's
  convergence is ~3.1 digits (the script's self-report of ~2.3 was
  pessimistic), and the `Lambda=0` spectra have the exact Bessel closed
  form above, which the script could cite as a fourth control.
- Overall: **negative verdict STANDS.**

## Relation to existing docs

This audit does not downgrade anything in
`particle_spectrum_native_geometry.md` — section 26 already classified
sector-dependent `q(P)` as "not derived" and parked it; this audit supplies
the missing forward test and returns a clean negative for its
eigenvalue-ladder form. The weak coupling of section 25
(`A(P) = Tr(P) * S_C1/R = W(P)` on the common `q=1/3` branch) is not
touched: it is an action identity, not a spectral claim, and nothing here
bears on it. The section-24 route table should be read with route 1's
spectral readout now crossed off; routes 2 (two-form channels), 3
(three-form support), and 5 (kernel energy) — and non-spectral readouts of
route 1 — are where the radial-coupling effort should go. Methodologically
this audit is the spectral-side companion of
`dimension_ladder_null_audit.md`: pre-declared candidates, declared
thresholds, family-consistency discipline, and a blind adversarial
verifier, applied before any result is banked.
