# Branch (iii) Hunt Results

Status: working audit, not canonical.
Created: 2026-06-10.
Scripts: `native_threshold_rigidity_theorem.py` and
`native_areal_function_field_equations.py` (all results below reproduce
from them; both new 2026-06-10, amended same-day per the verifier record
below). Alters nothing existing; new files only.

## Headline: the branch-(iii) hunt is COMPLETE for the static sector

The hunt opened by `open_domain_discreteness_results.md` — branch (iii),
"an uncovered metric function altering the omega-dispersion at infinity,"
the precise mathematical form of Charles's standing hunch — now has a
complete three-part map of the static sector.

### Part 1: the threshold rigidity theorem (34/34 symbolic/exact PASSes)

On the P0 ansatz (`rho = r`), `native_threshold_rigidity_theorem.py`
proves a chain with no slack in it:

```text
finite exterior C1 action  ⟹  f → const  ⟹  V ∈ L¹(tortoise)
                           ⟹  continuum threshold exactly 0
                           ⟹  (with the prior theorem) EMPTY point spectrum.
```

The power-law classification is exact: for `f ~ c·r^k`,

- `k < 1`: `V(∞) = 0` — threshold stays at zero, no bound states;
- `k = 1`: `V(∞) = c²` — the UNIQUE threshold-lifting power;
- `k > 1`: confining (`V → ∞`).

And **every growing profile `k > 0` costs INFINITE C1 action** — the
unique lifter at `k = 1` is excluded by the finite-action charter, not by
fiat. The native vacuum family `f = C + 2/r` passes every check. Verdict:

**Branch (iii) is CLOSED within
`{static, spherical, rho = r, finite action, single structure}`.**

### Part 2: the unique static escape, identified

The rigidity theorem's own E1 section locates the one unaudited P0
component: **`rho = r` itself — the areal function**. On the generalized
static metric

```text
ds² = −f dt² + f⁻¹ dr² + rho(r)² dΩ²,
```

the probe potential is (exact, re-verified in both scripts)

```text
V = f·lambda/rho² + f·(f·rho')'/rho .
```

A SATURATING areal function (`rho → rho_∞` finite, `f → f_∞ > 0`) lifts
the continuum threshold to `f_∞·lambda/rho_∞²` at FINITE action — masses
from angular eigenvalues `lambda = ell(ell+1)`. This is the precise
candidate for Charles's "metric function we have yet to uncover," and
recon confirms it was never audited: `rho = r` is silent inside P0, and
"throat" appears nowhere in the corpus.

### Part 3: the (f, rho) native field equations (53/53 symbolic/exact PASSes)

`native_areal_function_field_equations.py` frees `rho` under the TOTAL
banked native action (C1 + native two-form flux + H1 collar source;
conditionality flagged per piece; nothing imported, nothing linearized).
The structural fact driving everything: **no native sector carries
`rho'`**, so rho's Euler–Lagrange equation is ALGEBRAIC, not an ODE:

```text
δf:   (rho²f')' + 2sW f = 0          δrho:   rho⁴(f')² = 4K  (algebraic).
```

Results:

- **(a) Pure C1 (`q = 0, W = 0`):** the rho-variation forces `f' ≡ 0` —
  the entire banked vacuum family dies. **`rho = r` is NOT derived**; P0's
  areal choice is a genuine KINEMATIC postulate ("rho is not a varied
  field"), not a theorem.
- **(b) With native flux (`q ≠ 0`):** the algebraic rho-equation IMPLIES
  the f-equation, and the system is consistent ONLY on the
  **EXTREMALITY LOCK**

  ```text
  |a| = 2√K = c_q·|q|
  ```

  — the tail coefficient of `f` locked to the flux charge. This is
  in-repo novel (no prior two-function variational treatment or
  `|a| ∝ |q|` relation anywhere in the corpus). It structurally echoes
  the extremal Reissner–Nordström relation `M ∝ |Q|`, but the derivation
  route differs: it arises from consistency of an underdetermined native
  variational system, and NO `Q²/r²` term appears in `f` — the native
  flux does not gravitate in `f` at all, acting only through the
  rho-equation. On the lock the system is then **EXACTLY
  UNDERDETERMINED**: `rho(r)` is a free function — and the
  underdetermination is **DEMONSTRATED physical by curvature invariants**
  (not gauge): two lock members with identical `(C, a, K)` —
  `(rho = r, f = C + a/r)` vs `(rho = r², f = C + a/(3r³))` — have
  different curvature invariants as functions of areal radius (at `C = 1`
  the first is scalar-flat, `R ≡ 0`; the second has `R ≠ 0`).
- **(c) With the H1 source (`W ≠ 0`):** the source is forced
  rho-independent by its own banked `rho = r` limit, so it cannot break
  the degeneracy — instead the system is **OVERDETERMINED**: no solution
  anywhere on the source support.
- **(d) NO native throat:** threshold-lifting cylinder ends
  (`f → f_∞ > 0, rho → rho_∞`) are FORBIDDEN by the lock for every
  `q ≠ 0` (`rho²f' = −a ≠ 0` contradicts `f' → 0`); the surviving charged
  cylinders are horizon-capped (threshold → 0) or confining at INFINITE
  action; at `q = 0` the throat is allowed only as an unselected member
  of the fully undetermined sector. The E1 escape has no determined
  native realization under the current action inventory.
- **(e) The MISSING EQUATION, identified:** the EH density on the
  (f, rho) metric, computed from scratch,

  ```text
  rho²R = −d/dr[rho²f' + 2f·rho·rho'] + 2 − 2f·rho·rho'' ,
  ```

  is **NOT a boundary term off `rho = r`** (it is one exactly at
  `rho = r` — consistent with the banked diagnostic
  `native_eh_total_boundary_diagnostic.py`, which is why it is invisible
  in every existing `rho = r` calculation). It carries exactly the
  `(rho')²` / `rho''` structure that would supply rho's dynamics — but it
  is **guardrail-FORBIDDEN as an import**
  (`native_positional_dilation_gr_guardrail.py`, principle 1). Deriving
  an equivalent object NATIVELY is now the sharpest named target of the
  hunt.

## Consequences (the zoom-out)

The four-branch map of `open_domain_discreteness_results.md` updates:

| Branch | Status |
| --- | --- |
| (i) open-cell resonances | CLOSED (prior audit, unchanged) |
| (ii) truly compact probe domain | OPEN — zero-tail mechanism still needed |
| (iii) modified asymptotic threshold | **STATIC SECTOR CLOSED except through rho-dynamics** — rigidity theorem on `rho = r`; freed-rho system underdetermined/overdetermined with no determined throat |
| (iv) non-Friedrichs center condition | closed by finite-action charter (unchanged) |

The remaining branch-(iii) question is a single fork, and **either
outcome is decisive**. Whatever supplies rho's equation natively:

- either **derives `rho = r`** — P0 is vindicated as a theorem, branch
  (iii) is fully dead, and the hunt redirects to branch (ii), ensembles,
  and nonstationary configurations;
- or **selects throat-like ends** — native discreteness with masses
  `~ lambda/rho_∞²`, the phi–angular interaction realized exactly as
  Charles's hunch anticipated.

Also recorded on its own merits: the **extremality lock `|a| = c_q|q|`
stands independently as the first exact native mass(tail)–charge
relation** in the repo. Flagged for future spectrum work regardless of
how the rho-dynamics fork resolves.

## Verifier record

Blind adversarial verifier, 2026-06-10, agent `a608fda4bab0fc2b7`.
Outcome:

- The EH density **re-derived from scratch by an independent route**
  (explicit Riemann tensor + warped-product cross-check) — exact match,
  including both EL expressions and the `rho = r` collapse to the banked
  total derivative.
- The underdetermination **UPGRADED from argued to demonstrated** via the
  invariant computation (two lock members, identical `(C, a, K)`,
  different curvature invariants vs areal radius; the `C = 1`
  scalar-flat case decisive). Reproduced as an in-script check.
- The lock chain (algebraic rho-equation ⟹ f-equation ⟹ `|a| = 2√K`)
  **verified by hand**.
- **Sign anchoring amendment required and implemented**: the flux piece
  `K/rho²` is f-blind, so no banked `rho = r` limit anchors its sign —
  it is fixed by the energy-functional reading plus self-consistency
  (the opposite sign makes the rho-equation a sum of positives with no
  solution, flipping the verdict to 'inconsistent'). The docstring
  header now says so.
- The rigidity bound **re-derived and numerically stress-tested** on
  three profiles, including an oscillatory one — the bound is tight.
- The `k`-classification and the E1 potential
  `V = f·lambda/rho² + f(f·rho')'/rho` **independently confirmed**.
- **Novelty confirmed**: no prior two-function variational treatment and
  no `|a| ∝ |q|` relation anywhere in the corpus.

## Next targets

1. **Derive rho-dynamics natively.** Candidates: (a) the C1 action at
   full metric-perturbation level — does integrating out the banked
   angular Hessian blocks induce an effective `(rho')²` term?; (b) the
   H1 carrier's gradient energy evaluated on the (f, rho) background;
   (c) a native re-derivation of the EH remainder `2 − 2f·rho·rho''`
   from positional-dilation first principles (principle 4).
2. **If rho-dynamics resists, redirect**: branch (ii)'s `a_tail = 0`
   zero-tail mechanism and the multi-cell/ensemble asymptotics (the
   orchestra).
