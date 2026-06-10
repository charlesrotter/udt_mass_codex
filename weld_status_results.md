# Weld Status Results

Status: working audit, not canonical.
Created: 2026-06-10.
Script: `native_weld_status_derivation.py` (53 symbolic/exact +
numerical PASSes); new 2026-06-10, amended same-day per the verifier
record below. Alters nothing existing; new files only.

## Headline: phase 1 of the weld program is COMPLETE

Phase 1 of the weld program (the CANON C-3 redirect) is complete — the
rung-2 weld's native status is SETTLED, grade (d): the native C1 system
produces its OWN phi-angular weld, algebraic, distinct from the
Einstein form — and on sourced matter cells it leaves a real-frequency
oscillation window open.

## Part 1: the kinematic reduction (W1)

`B = 1/A` at perturbed level (the UDT structure `g_tt = -e^{-2phi}`,
`g_rr = e^{+2phi}` with `phi = phi0 + delta-phi·Y`) ties the RW
amplitudes automatically:

```text
H0 = -2 delta-phi,    H2 = +2 delta-phi    (H0 = -H2),
```

and `g_tt·g_rr = -1` holds exactly at all perturbative orders — the tie
is automatic, not imposed.

`K` is NOT pure gauge for `ell >= 2` (the G-harmonic obstruction
`Theta·(Y'' - cot th·Y') = 0` forces `Theta = 0`; the unique K-removing
areal re-chart generates `g_{r theta} =/= 0`, exiting the P0/RW class).
But the perturbed-level R-areal canon (CANON C-1) forces `K = 0` as a
CONFIGURATION RESTRICTION, not a gauge choice. Independently, K's EL
equation is parametrization-ambiguous by exactly

```text
EL_K[param II] − EL_K[param I] = T^th_th[bg]·r²·K
```

— the perturbative face of the proven theta-theta Einstein refusal
(the banked Einstein-tension object, now biting at perturbed level).
Matter-side fields after W1: **(delta-phi, H1)**.

## Part 2: the native weld (W3 + verifier identification)

The exact second-order C1 action makes H1 AUXILIARY — it contains no
H1 derivatives (structural: a matter-type action carries no metric
derivatives). Its EL equation is the ALGEBRAIC weld

```text
f·phi0'·H1 = 2 d_t(delta-phi)    ⟺    f'·H1 = -4 d_t(delta-phi)
```

— the SAME coupling pair (H1 ↔ d_t delta-phi) as the Einstein weld,
but algebraic (no d_r H1) and K-free. Verified inequivalent to the
Einstein differential weld by explicit witness.

**Verifier structural identification (explains why grade (d) was
forced):** identically,

```text
EL_H1 = -r²·(delta T_tr) ,
```

so the native weld is first-order VANISHING RADIAL ENERGY FLUX
(`T_tr = 0`) — the matter-only remnant of GR's (t,r) slot. In GR,
H1-variation yields the (t,r) Einstein equation, never the (t,theta)
weld; the (t,theta) form only arrives via Bianchi plus the rest of the
Einstein system — which W4 closes off natively.

Eliminating the auxiliary H1 through its own weld flips the time-kinetic
sign EXACTLY (the `-B²/4A` mechanism: `+(c/2) → -(c/2)`), giving the
on-shell native equation

```text
+ r² d_t²(delta-phi) + d_r(r² f² d_r delta-phi)
− 4 r² f² E0·delta-phi − lambda·f·delta-phi = 0,

E0 := phi0'' + 2 phi0'/r − 2 phi0'²
```

(`E0 = 0` on vacuum; `E0 =` the angular source on sourced collars).

## Part 3: the spectrum structure

On VACUUM backgrounds (`E0 = 0`) — and more generally wherever
pointwise `lambda·f + 4r²f²E0 >= 0` — the quadratic form is
positive-definite: NO real-omega modes (relaxation only,
`omega² < 0`).

On SOURCED collars the E0 term can flip the balance. Verifier
counterexample, reproduced numerically in the script (W3(e'), three
checks):

```text
phi0 = -3(r - 3/2)²  on [1, 2],  ell = 2, Dirichlet:
    real mode      omega² = +7.53   (E0 < 0 throughout)
vacuum control on the same cell:
    top eigenvalue omega² = -12.6   (no real modes, as the
                                     E0 >= 0 theorem demands)
```

**THE FINDING:** the native phi-angular oscillation window exists
exactly where the angular source lives — matter cells with active H1
sources are the candidate home of native oscillation modes. The source
that softens the core can open its own oscillation window. This is the
phi-angular interaction hunch surviving in its sharpest form yet:
source-enabled, weld-coupled, finite-cell oscillations.

## Part 4: the Einstein weld's status (W2/W4)

`delta-G^t_theta` is confirmed EXACTLY on general profiles (the
AUDIT.md S116 'Step 1' operator cross-checked at arbitrary `f`,
K-coefficient exactly +1, ell-flat). But the C1 stress has a
first-order conservation leak,

```text
(nabla T)_theta = c f² (E0 − phi0'²)·delta-phi·d_theta Y ,
```

independent of H1 and K — so the full Einstein theta-row would force
`delta-phi = 0`: Bianchi cannot deliver the Einstein weld natively. It
is a freestanding import at BOTH scopes structurally (the non-C1 macro
content changes the source term, not the constraint's pedigree; macro
total-conservation self-consistency is unverified). Macro support is
empirical and CHANNEL-SPECIFIC: phase/interleaving/TE PASSED; the EE
amplitude is the standing ~2x overshoot. And the validated phase
signature (H1 in quadrature with delta-phi) follows from
`H1 ∝ d_t(delta-phi)` in TIME structure, which BOTH welds supply — the
macro phase channel may not discriminate the two welds.

## The readings fork + phase 2 plan

- **Reading A — native** (algebraic weld, elliptic with the E0
  window). **PRIORITY:** compute cell spectra on the banked sourced
  backgrounds (`eta = 1/18`, `ell = 1` source) and determine whether
  the physical E0 sign/magnitude opens real modes, with the `phi = 0`
  interface BCs per CANON C-2.
- **Reading B — H1 excluded** (strict diagonal P0 reading): hyperbolic
  breathing with characteristic speed `dr/dt = f`. Compute alongside.
- **Reading C — Einstein weld transplanted**: graded import, compute
  for comparison only.

Plus the macro discriminator: rerun the macro projection with the
native algebraic weld `H1 = -4·d_t(delta-phi)/f'` and compare the
RADIAL structure against the CMB record.

State plainly: whether the physical sourced cell sits inside the
oscillation window is now a COMPUTABLE question — and it is the single
highest-leverage computation in the program.

## Verifier record

Blind adversarial verifier, 2026-06-10, agent `a709e4306bdf91b3a`.
Outcome:

- All five claims **independently re-derived** (own metric
  conventions, analytic 2x2 block inverse, own Christoffel/Einstein
  routine, own witnesses).
- Danger zones checked: the O(H1²) terms from the g^rr second order
  and sqrt(−g) **partially cancel to the load-bearing
  `+(c/4)f²r²phi0'²H1²`**; the variation rule is consistent; RW gauge
  rigidity for `ell >= 2` re-confirmed — **the algebraic weld is
  dynamics, not gauge-fixing**.
- The no-real-omega claim **CORRECTED to E0 >= 0 scope**, with an
  explicit E0 < 0 real-mode counterexample (`omega² = +7.53`).
- The **`EL_H1 = -r²·delta-T_tr` identification supplied** (vanishing
  radial energy flux — why grade (d) was forced).
- Macro-scope wording **tightened** (equally an import structurally;
  channel-specific validation; the phase channel may not discriminate).
- **Three amendments implemented same-day** (framing/printed text;
  existing checks unweakened; five checks added, including the
  numerical reproduction of the counterexample — 48 → 53 PASSes).

## Next targets

1. **The Reading-A spectra on the banked sourced backgrounds**
   (`eta = 1/18`, `ell = 1` source; CANON C-2 interface BCs) — does the
   physical cell sit inside the E0 < 0 oscillation window? Highest
   leverage in the program.
2. **Readings B and C alongside** (hyperbolic control; graded import
   comparison).
3. **The macro discriminator** — native-weld CMB projection (radial
   structure) vs the record; the EE ~2x overshoot stays on the books as
   the channel either weld must still face.
