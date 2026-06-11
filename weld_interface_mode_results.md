# Weld Interface Mode Results

Status: working audit, not canonical.
Created: 2026-06-10.
Script: `native_weld_interface_mode_spectrum.py` (57 symbolic/exact +
numerical PASSes); new 2026-06-10, amended same-day per the verifier
record below. Alters nothing existing; new files only.

## Headline: weld phase 2 is COMPLETE — NEGATIVE, WITH AN EXACT THRESHOLD MAP

The phase-1 oscillation window (`weld_status_results.md`: real-omega
modes possible where `lambda f + 4r²f²E0 < 0`) is REAL but UNOCCUPIED
by the banked single cell. On the banked background (self-similar
sourced collar `q = 1/3`, `s = q(1-q)/2 = 1/9`, zero-tail flat
exterior per CANON C-2):

- the physical bulk source has `E0 = s/r² > 0` — the window needs
  negative `E0`, which the banked source does NOT supply;
- the only attractive structure is the zero-tail interface shell, the
  delta `-(q/2R)·delta(r-R)` with jump strength `gamma = 2q = 2/3`;
- binding requires `gamma > gamma_c`, with the EXACT closed form
  (verifier contribution):

```text
gamma_c(BC-c, native no-flux)        = L0
gamma_c(BC-a, reservoir matching)    = L0 + (ell+1)
gamma_c(BC-b, Dirichlet)             = +infinity (no gamma binds)

L0 = -(1-2q)/2 + (q·tau0/2)·I'_nu(tau0)/I_nu(tau0),
nu = sqrt(1+4q(1-q))/q = sqrt(17) at q = 1/3,   tau0 = 2·sqrt(lambda)/q
```

(the interior zero-energy problem Liouville-transforms to the modified
Bessel equation; the Friedrichs branch is `I_nu`; closed form matches
shooting to ~1e-14).

**The deficits** (`L0 = 1.33835009 / 2.29931870 / 3.28396540` at
`lambda = 2/6/12`): factor **2.0075** (lambda=2, BC-c — genuinely NOT
2: off by 0.376%, null-test recorded as a non-match) up to **10.93**
(BC-a, lambda=12). No `q` in (0, 1/2) closes the gap for ANY integer
`ell >= 1` on the physical tie `gamma = 2q` (BC-a excluded at theorem
level); the would-be window needs `lambda < lambda_c = 0.267787` —
inside the excluded monopole gap.

All three interface ontologies give relaxation-only spectra at banked
parameters:

```text
BC-b (Dirichlet dissolution):    omega² = -27.334956 (lam=2), -41.213694 (lam=6)
BC-c (native no-flux Robin):     omega² = -3.4667814 (lam=2), -10.376405 (lam=6)
BC-a (reservoir-field matching): no discrete point; box artifact only
```

The BC selection question is thereby **MOOT at the single-cell level**
— all three ontologies are negative; nothing needs to be picked yet.

## Machinery validation (the negative is not a numerics failure)

- Boosted-gamma validation modes pass EVERY pre-registered
  discriminator: BC-c at `gamma = 1.5·gamma_c`: `omega² = +4.0701100`
  (FD = shooting to 4+ digits, scale-covariant); BC-a at
  `gamma = 1.2·gamma_c`: `omega² = +0.9872447` (domain-doubling
  stable, exact-Bessel exterior shooting cross-check).
- Scale covariance exact: `omega²R²` invariant (symbolic R-elimination
  + 4-5 digit numerics on independently generated meshes).
- FD vs independent shooting agree 4+ digits everywhere; r_min/r_max
  controls pass; no-delta controls consistent with the bulk-positivity
  theorem.

## The non-Friedrichs loophole: computed and closed

The core endpoint is limit circle (both indicial roots weight-L²), so
the Friedrichs extension is a choice. Upgraded from caveat to computed
result (verifier amendment): the non-Friedrichs (`a_minus = K_nu`)
core extension DOES bind at physical strength — BC-c lambda=2:
`omega²R² = +1.14939`. BUT the `gamma = 0` control shows it binds even
with the interface delta REMOVED (`omega²R² = +0.56259`): a
**core-attached artifact**, not weld-interface binding; excluded by
the finite-action charter (the `a-` branch has infinite core form
energy). The interface threshold map is extension-independent in
substance.

## Verifier record

Blind adversarial verifier, 2026-06-10, agent `ae8caa64ef3d4b1ff`.
Outcome:

- All claims **reproduced to 7-9 digits** by independent methods:
  closed-form Bessel evaluation + Chebyshev collocation +
  exact-seeded shooting.
- `gamma_c = L0` sharpened to ~9 digits.
- The **exact Bessel closed form** (C2b) and the **non-Friedrichs
  loophole computation** (C2c) were verifier contributions,
  implemented same-day (existing checks unweakened; five checks added,
  52 → 57 PASSes; check count made self-counting).

## Consequences

1. **Reading A's single-cell, single-shell structure cannot bind
   oscillation modes.** The native weld system is real but needs MORE
   structure than one cell provides.
2. **The deficit is a clean factor ~2 at the most natural BC** (BC-c,
   lambda=2: 2.0075) — and the banked corpus contains TWO-SIDED
   interface structure (internal gluing, two-sided half action:
   `native_internal_gluing_symplectic_form.py`,
   `native_two_sided_half_action_status.py`,
   `native_half_action_from_symmetric_gluing.py`). A compound /
   two-sided shell is the sharpest next candidate. **Do NOT promote:**
   candidate only — the factor-2 match must survive the null-test
   discipline, given that 2.0075 != 2 (0.376% off, recorded).
3. **Ensembles / multi-cell (the orchestra) remain** untested: shared
   exterior, multiple shells.
4. **The transfer-ladder route is untouched** by this negative.

## Next targets

1. **Two-sided / compound interface audit**: does the banked
   internal-gluing structure supply a second shell, and what TOTAL
   gamma does it deliver?
2. **Ensemble of cells** (shared exterior, multiple interface shells).
3. **The macro discriminator** — native-weld CMB projection — still
   queued from phase 1.
