# Rho-Dynamics Derivation Results

Status: working audit, not canonical.
Created: 2026-06-10.
Scripts: `native_rho_dynamics_gr_balance_test.py` (Route A, 60
symbolic/exact PASSes) and
`native_positional_dilation_distance_readings.py` (Route C, 42
symbolic/exact PASSes); both new 2026-06-10, amended same-day per the
verifier record below. Alters nothing existing; new files only.

## Headline: the rho-dynamics derivation CONVERGED

The entire branch-(iii) decision now sits in ONE function — the areal
potential `beta(rho)` — and both forks of
`branch_iii_hunt_results.md` are realized inside a SINGLE candidate
native action. The `J = 0` leaf of that action reproduces exactly the
banked vacuum (the first action in the program that SELECTS the banked
P0 configuration instead of assuming it); the `J ≠ 0` leaves carry
exact throat geometries and — settled by the verifier — exact
threshold-lifting members with masses from angular eigenvalues.

## Part 1: Route A — the balance test (60/60 symbolic/exact PASSes)

`native_rho_dynamics_gr_balance_test.py`, on the generalized static
metric `ds² = −f dt² + f⁻¹ dr² + rho(r)² dΩ²`:

### (a) No C1 + EH-remainder system admits the banked vacuum

With `S_total = kappa·∫(2 − 2f·rho·rho'')dr + (1/4)∫rho²(f')² dr`, the
banked configuration (`rho = r`, `f = C + a/r`) leaves the exact
residual

```text
EL_rho[total]|banked = a²/(2r³)   for EVERY kappa
```

— the EH side vanishes identically on the banked family, so no
coefficient can balance the C1 obstruction. Adopting the theta-theta
Einstein equation as-is breaks UDT's own vacuum.

### (b) The Einstein tension: rho-dynamics is NOT secretly EH

The theta-theta Einstein VACUUM equation coincides with the banked
f-equation:

```text
G^th_th = (r²f')'/(2r²)   ⟹   G^th_th ≡ 0 on f = C + a/r.
```

With the C1 scalar as honest source (stress by metric variation), the
Einstein tension on the banked vacuum is

```text
Delta(r) = G^th_th − 8pi T^th_th[C1] = pi c a²/r⁴  >  0  strictly,
```

C-INDEPENDENT, falling as `1/r⁴`; `Delta ≡ 0` only at `c = 0` (trivial
scalar), checked through general phi-normalizations. UDT's deliberate
departure from the full Einstein equations off the tt/rr block is now
quantified exactly for the first time. (Honest extras: the tt/rr block
fails with this source too, and the C1 stress is not conserved on the
banked vacuum — UDT's C1 sector is structurally NOT "GR + scalar
matter".)

### (c) EXISTENCE: the forced completion and the candidate action

Requiring the banked TWO-PARAMETER vacuum family (all `C`, all `a`) to
survive forces — within the declared class, at most quadratic in first
derivatives; quartic alternatives exist and are recorded below — the
unique completion

```text
L_C1 + D* = (1/4)[(f·rho)']²,    D* = (1/4)f²(rho')² + (1/2)rho f f'rho'
```

— a PERFECT SQUARE in the dilation-weighted radius `u := f·rho` — plus
a fully solved homogeneous family, of which the load-bearing member is
the areal potential term `beta(rho)(1 + (rho')²)` with exact first
integral

```text
beta(rho)(1 − (rho')²) = J .
```

The `J = 0` leaf is EXACTLY `rho = r` (up to gauge) with
`f = C + a/r`: the first action in the program that SELECTS the banked
P0 configuration instead of assuming it.

CLASS-RELATIVITY (verifier amendment, load-bearing): D*-uniqueness and
the perfect square are statements relative to the declared
quadratic-in-first-derivatives class. An explicit QUARTIC
counter-family,

```text
q1 f²(rho')⁴ + q2 rho f f'(rho')³ + q3 rho²(f')²(rho')²
with q1 = q3 + 1/12,  q2 = 2q3 + 1/6,
```

cancels the obstruction with NO D* and NO perfect square.

## Part 2: the threshold gate — SETTLED (by the verifier)

The `J ≠ 0` leaves realize BOTH forks of the branch-(iii) decision:

- **`beta = b0 rho²`** gives exact throats `rho = sqrt(J + r²)`,
  `f = (alpha r + gamma)/rho` — and the throat requires `beta = b0 rho²`
  EXACTLY (for `J ≠ 0`), not generic beta. This is an apparently NEW
  exact metric: anti-Fisher signature, effective `Q² = −J/2 < 0`,
  NEC-violating at the neck, NOT the Ellis drainhole, one-sided horizon
  for `alpha ≠ 0`. But it NEVER lifts the continuum threshold
  (`V(∞) = 0`).
- **`beta` with a positive critical value DOES lift it.** Verified
  member: `beta(rho) = J/(1 − (rho_∞ − rho)²)` with exact solution
  `rho = rho_∞ − e^{−r}`, `f = gamma/rho` (the `alpha = 0` branch of
  `(f rho)' = alpha`); both EL equations satisfied, first integral `J`
  exact, and

  ```text
  V(∞) = f_∞·lambda/rho_∞²  >  0
  ```

  — masses from angular eigenvalues, the phi–angular interaction
  realized.

The criterion is exact: a `J ≠ 0` leaf lifts the threshold iff `beta`
has a positive critical value approached as a local minimum
(`beta''/J > 0`) AND `alpha = 0`; `beta = b0 rho²` never lifts.

OPEN (carried with the settlement): global finite-action existence of
the lifting orbit (the inner boundary is log-divergent on the exhibited
member); and the lifting member has BOUNDED total dilation — in tension
with the unbounded-growth canon of Part 3 (the dynamics and the
principle reading must be canonized together).

## Part 3: Route C — the readings theorem (42/42 symbolic/exact PASSes)

`native_positional_dilation_distance_readings.py` interrogates the
PRINCIPLE (P0) rather than the action. P0's invariant content is WHICH
physical coordinate carries `B = 1/A`:

- **Lemma 1 (existence):** `B = 1/A` is achievable in SOME chart for
  ANY static spherical metric — the condition alone is contentless.
- **Lemma 2 (uniqueness):** the `B = 1/A` chart is unique up to ±,
  shift, AND Killing-time rescaling `t -> kt` (which maps
  `r -> ±r/k + const`, `(C, a) -> (k²C, ka)`); the slope-1 in
  `rho = ±r + const` is a time-unit convention; the downstream binary
  verdicts are gauge-invariant.

**THEOREM:** `[B = 1/A in the areal chart] ⟺ rho = ±r + const` — the
banked P0 IS the areal reading and FORCES `rho = r`. R-proper
degenerates (`B = 1/A` in the proper-distance chart forces `phi ≡ 0`,
no dilation at all); R-other leaves `rho` free and the principle
INCOMPLETE without an independent distance definition.

**Monotonicity audit:** the banked vacuum is strictly monotone for ALL
`r` (both `C > 0` and `C = 0`); growth is BOUNDED for `C > 0`
(saturating at `−(1/2)ln C`) and unbounded only at `C = 0`. Therefore
an "unbounded total dilation" canon selects `C = 0` in vacuum AND kills
threshold-lifting throats (which have bounded total dilation), while a
strict-monotonicity-only canon admits them — and (verifier sharpening)
has bite only against the `alpha ≠ 0` neck members of the A3 throat
class, which violate even strict monotonicity near the neck
(`f' > 0` for `r < alpha·J/gamma`); the conditional verdict concerns
monotone-f cylinder ends.

## The canonization fork (for Charles — this is the deliverable)

Three linked choices now carry everything:

1. **The READING of "distance" in P0.** Areal ⟹ `rho = r` forced ⟹
   branch (iii) dead in statics. Other ⟹ the `(f, rho)` dynamics live.
2. **The GROWTH canon.** Unbounded total dilation ⟹ `C = 0` vacuum +
   no lifting throats. Strict monotonicity only ⟹ lifting members
   admitted.
3. **The AREAL POTENTIAL `beta(rho)`.** `b0 rho²` ⟹ selection of the
   banked vacuum + no lifting. Positive critical value ⟹ native
   discreteness with `m² = f_∞·lambda/rho_∞²`.

These are NOT independent: the lifting scenario requires reading-other
PLUS the weak growth canon PLUS critical beta. The native-derivation
target is now maximally sharp: **derive `beta(rho)` from
positional-dilation first principles — everything else is fixed by
exactness.**

## Verifier record

Blind adversarial verifier, 2026-06-10, agent `ae8a655ed2fa4045f`.
Outcome:

- The perfect square `L_C1 + D* = (1/4)[(f rho)']²` **verified by
  direct expansion**.
- Both solution families (banked `J = 0` leaf; throat `J ≠ 0` member)
  **verified against independently derived EL equations**.
- The first integral `beta(1 − (rho')²) = J` **verified as an exact
  identity on the solution shell** (no missing f-coupling).
- The uniqueness of D* **re-derived by a different route** (identical
  six conditions), with the class-boundary caveat made LOAD-BEARING:
  the quartic counter-family constructed (`q1 = q3 + 1/12`,
  `q2 = 2q3 + 1/6`).
- The Einstein tension `Delta = pi c a²/r⁴` **verified exactly by a
  two-route stress derivation**.
- The C2 theorem **verified with the Killing-time amendment** (chart
  uniqueness up to ±/shift/rescale; binary verdicts gauge-invariant).
- C4 **confirmed and sharpened** (`alpha ≠ 0` neck members violate
  strict monotonicity; conditional verdict scoped to monotone-f ends).
- **Novelty checks:** `u = f·rho` appears nowhere in the 497-file
  corpus; the throat metric is apparently new (anti-Fisher-like, not
  the Ellis drainhole).
- **The deferred threshold gate SETTLED** with a fully verified lifting
  member (`beta = J/(1 − (rho_∞ − rho)²)`, `rho = rho_∞ − e^{−r}`,
  `f = gamma/rho`, `V(∞) = f_∞·lambda/rho_∞² > 0`) and the exact
  criterion (positive critical value of beta, local minimum, `alpha = 0`).
- **Six amendments required and implemented same-day** (all
  framing/printed-text; algebra untouched).

## Next targets

1. **Derive `beta(rho)` natively** — the single remaining function.
   Candidates: (a) the H1 sector's induced areal energy; (b) the flux
   sector on the `(f, rho)` family revisited with the perfect-square
   variable `u = f·rho`; (c) positional-dilation first principles for
   the "areal stiffness".
2. **Global finite-action analysis of lifting orbits** (the inner
   boundary log-divergence of the exhibited member).
3. **Put the canonization fork to Charles** (reading × growth canon ×
   beta — three linked choices, consequences exact on every branch).
