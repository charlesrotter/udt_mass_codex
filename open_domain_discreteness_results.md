# Open Domain Discreteness Results

Status: working audit, not canonical.
Created: 2026-06-10.
Scripts: `native_open_domain_threshold_theorem.py` and
`native_open_cell_resonance_scan.py` (all numbers below reproduce from
them; both new 2026-06-10, amended same-day per the verifier record below).
Alters nothing existing; new files only.

## Headline: the box-control mystery is SOLVED — it was a theorem, not a numerical artifact

The box modes `omega ~ 1/R_max` that haunted earlier spectra were artifacts
of the box, full stop. On the open matter side (`f >= 1`, `f -> 1 + a/r`),
the massless metric-native probe

```text
−(r²f R')' + ell(ell+1) R = omega² (r²/f) R,    weight w = r²/f
```

has **EMPTY POINT SPECTRUM (Friedrichs class) for every `ell >= 1` and any
interior structure** of the banked profile family (bounded or finite-action
softened core `f ~ C r^(−p)`, `0 <= p < 1/2`). Verified case by case in
`native_open_domain_threshold_theorem.py` (14 symbolic/exact PASSes):

- **`omega² < 0` dies by operator/weight positivity.** The quadratic form
  `Q[R] = ∫[r²f(R')² + ell(ell+1)R²]dr` is strictly positive (`f >= 1`
  gives `Q >= ell(ell+1)∫R²`), while the weight side is negative —
  contradiction. Boundary fluxes vanish by exact exponent identities at
  both ends.
- **`omega² > 0` has amplitude exactly `1/r`** — a Coulomb-like log phase
  `exp(±i[omega·r − a·omega·ln r])` is the ONLY effect of the `a/r` tail.
  The dangerous hydrogen-analogy attack (an attractive `~1/r` tail
  generically carries a Rydberg ladder accumulating at threshold) **fails
  here because the `a/r` tail sits in the WEIGHT, not the operator**: the
  effective Coulomb charge is `Z_eff = a·kappa²`, which vanishes at the
  threshold `kappa -> 0`, so there is no Rydberg accumulation. Verified
  three independent ways (see verifier record). The weighted norm of every
  oscillatory solution diverges linearly.
- **`omega = 0` forces `R = 0`** for `ell >= 1` (the form is a sum of
  non-negative terms with `ell(ell+1) >= 2`).

Caveat carried explicitly (verifier amendment): for softened cores
`0 < p < 1/2` the center endpoint is **limit-circle** in the weighted L²,
so "empty point spectrum" is specific to the **Friedrichs extension** —
the finite-form-energy condition in the function class is load-bearing,
not cosmetic. Non-Friedrichs boundary conditions are branch (iv) below.

## Second result: the resonance escape route is CLOSED for the banked background family

`native_open_cell_resonance_scan.py` (no box anywhere) measured the only
discrete frequency data the open linear cell could still own — scattering
resonances:

- **Tortoise potential derived exactly** (general `f`, `f'` terms
  included): `u'' + [omega² − V]u = 0` with

  ```text
  V(r) = f·( lambda/r² + f'/r )
  ```

  The Schwarzschild control `f = 1 − 2M/r` reproduces the scalar
  Regge–Wheeler potential **exactly** — the `f'` term is real, not guessed.
- **NO potential pocket anywhere.** Every background/probe combination is
  "barrier only" or monotone. The softened-core center is attractive
  subcritical inverse-square, `V ~ −g/rho²` with

  ```text
  g = p/(1+p)² = 3/16 < 1/4   exactly at p = 1/3,
  ```

  and `g <= 2/9 < 1/4` on the **whole** finite-action branch `p < 1/2` —
  a nontrivial consistency with the positivity theorem (a supercritical
  center would have contradicted it).
- **Scattering scan over `omega ∈ [0.15, 30]`** (step 0.01, units
  `c/R_core`): Wigner time delay featureless and monotone (`tau_max` sits
  at the long-wavelength grid edge — a smooth rise, independently
  confirmed monotone, not a feature); **zero peaks** above prominence 0.3;
  **zero stable complex poles** in four conditioning-matched strips down
  to `Im omega = −2`. Fake pole ladders appeared and were diagnosed as
  `e^(2|Im omega|·rho_m)` tail-truncation artifacts: their spacing tracks
  `pi/rho_m` exactly, they shift with the artificial parameter `rho_m`,
  and all were rejected by the pre-registered battery (residual < 1e-8,
  `rho_m`×1.5 and grid×2 stability, conditioning window, real-axis
  consistency).
- **Verdict: BROAD-ONLY (clean negative)** in every sector, per the
  pre-registered rule printed before any result. Formal reach:
  `Gamma >~ 4e-3` (ultra-narrow poles below that width are outside the
  scanned strips; with no potential pocket such trapping is structurally
  unavailable, but the reach is stated, not hidden).

## Bonus exact finding: the face-value ell=2 sourced background does not exist

At face value the `ell = 2` source gives `s = eta·lambda = 6/18 = 1/3`,
which exceeds the finite-action bound `1/8`. The deep-core indicial roots
are **complex**: `p = 1/2 ± i·sqrt(15)/6`. Consequence (exact, and
strengthened by the verifier from power laws to all solutions): **every
interior solution** of the deep-core equation is
`f = r^(−1/2)·[A cos(nu·ln r) + B sin(nu·ln r)]` — it oscillates in
`ln r`, crosses zero infinitely often, and violates `f >= 1`. There is
**no valid `s = 1/3` sourced background at all**. At `eta = 1/18`,
**`ell = 1` is the ONLY ordinary sector with a valid sourced background**
— an independent consistency echo of the `N=3`/`H1` selection.
(The `ell = 2` probe was honestly run on the capped `s = 1/9` background
instead; also BROAD-ONLY.)

## The structural consequence (the zoom-out)

Native discreteness on the matter side, if it exists, must come from one
of exactly **FOUR branches** — and two of them are now closed:

| Branch | Status |
| --- | --- |
| (i) open-cell resonances | **CLOSED** for this background family at the stated reach (`Gamma >~ 4e-3`) |
| (ii) truly compact probe domain | OPEN — requires the `a_tail = 0` zero-tail mechanism AND genuine compactness of the probe domain; a flat exterior alone does NOT escape the theorem (A2 applies verbatim with `a = 0`) |
| (iii) modified asymptotic threshold | OPEN — an uncovered metric function altering the omega-dispersion at infinity |
| (iv) non-Friedrichs center boundary condition | closed by the finite-action charter (any such bound state costs infinite probe energy) unless a dynamical selection mechanism is derived |

**Branch (iii) is the precise mathematical form of Charles's standing
hunch** (phi–angular interaction via a metric function not yet uncovered):
the uncovered object must contribute an effective-mass-like term to the
probe's asymptotic dispersion, pushing the continuum threshold up and
opening a window `(0, m_eff)` where genuine L² states can exist. It must
be uncovered from the metric/action, never imported (principle 1).

Scope exclusions recorded: nonstationary / breather-like configurations
are outside the theorem entirely; `ell = 0` is delegated to the repo's
endpoint audits; metric-ansatz generalizations (`g_tt·g_rr != −1`) are not
covered and live in branch (iii).

## Verifier record

Blind adversarial verifier, 2026-06-10, agent `af9521a23d0456a7a`. Outcome:

- Probe equation **re-derived from the wave operator** (residual 0);
  A1–A3 re-derived independently.
- The Coulomb-tail (hydrogen-analogy) attack — the strongest attack
  mounted — **resolved in the theorem's favor on three independent
  grounds**: (1) the definite-pair argument (the `a/r` tail enters the
  weight; `Z_eff = a·kappa² -> 0` at threshold); (2) the exact tortoise
  form has **zero `1/rho` coefficient** at infinity; (3) numerical
  Friedrichs diagonalization found **no negative eigenvalues** at
  L = 200 and L = 800.
- `V(r) = f·(lambda/r² + f'/r)` and `g = 3/16` confirmed from scratch.
- The `s = 1/3` nonexistence **strengthened**: every interior solution
  oscillates (not just the power-law representatives).
- Scan phases reproduced by a **fully independent integrator to
  3e-8 rad**; `a_tail` to 7.6e-11; time delay confirmed **monotone**.
- Fake-pole ladder spacing verified to track `pi/rho_m` empirically —
  the artifact diagnosis stands.
- **Four amendments required and implemented same-day** in the committed
  scripts: (1) limit-circle/Friedrichs status of the center endpoint made
  explicit, with the non-Friedrichs extension promoted to structural
  branch (iv); (2) nonlinear corollary weakened to `omega² > 0` tails only
  — static (`omega = 0`) lumps have normalizable `r^(−ell−1)` tails and
  need the repo's separate (linear-only) global no-gos; (3) nonstationary
  configurations and `g_tt·g_rr != −1` generalizations recorded as scope
  exclusions / branch (iii); (4) `tau_max`-at-grid-edge note added to the
  scan output (smooth monotone rise, not a feature).

## Next targets

1. **Branch (iii) hunt** — GR-corpus mining under positional dilation
   (principle 4) for metric functions / cross terms that modify the
   asymptotic dispersion. Candidates to examine natively: phi–angular
   cross metric components; the two-form flux sector's contribution to
   the effective wave operator; `g_tt·g_rr != −1` deformations.
2. **Branch (ii)** — the `a_tail = 0` zero-tail mechanism (the Matter
   Cell Postulate's nonlinear global condition), plus what could make the
   probe domain genuinely compact (a flat exterior alone is not enough).
