# P02 law-neutral local-jet atlas — audit report

Date: 2026-07-21

Base: `0167b90438fbc13679b7a043066ab990ea54aa98`

Status: `VERIFIED-WITH-CAVEATS`

Maximum conclusion: `LOCAL_KINEMATIC_SOLUTION_SPACE_CHARACTERIZED_WITHOUT_DYNAMICS`

## Result

P02 is complete in its preregistered point-local configuration-space scope. The package exactly maps
the registered zero-, first-, and second-jet strata without applying a field equation, selecting a
reciprocal plane, identifying `phi` with a metric component, choosing a physical common-scale
representative, or ranking any branch.

The most important structural result is an exact full-rank parametrization, not a preferred witness:
after normal-coordinate redundancy, every regular metric two-jet is an arbitrary 20-component
algebraic Riemann tensor. It decomposes uniquely into an arbitrary ten-component Weyl tensor plus an
arbitrary ten-component Schouten/Ricci tensor. The saved 21-by-20 bivector-component matrix has exact
rank 20 and spans the complete Bianchi kernel, including all mixed/angular entries and arbitrary
relative alignment.

Under local positive Common-Scale rescaling, the scale Hessian shifts the complete ten-component
Schouten sector at a point while Weyl remains. Thus the pre-scale local second-jet curvature content
is the ten-component Weyl sector. This is a geometric consequence of CSN bookkeeping; it does not
select a Weyl-squared action, Bach equation, vacuum condition, or physical representative.

## Exact atlas coverage

The generated ledgers contain:

- all 15 real symmetric four-dimensional metric inertia classes;
- all 36 base/screen inertia products in the conditional supplied `2+2` representation;
- eight signed-`dphi` zero, support, and causal/alignment strata;
- all 12 expansion-rank × shear-rank × twist-rank combinations;
- all seven curvature-operator ranks;
- all five Ricci-endomorphism ranks;
- all six Weyl/Petrov types `I`, `D`, `II`, `III`, `N`, and `O`; and
- an exact 20-element Weyl-plus-Schouten direct-sum basis.

The reported 89 discrete registered strata are a sum of marginal ledgers, not a false Cartesian
product or a claim that continuous geometry has only 89 points. Arbitrary tensor coefficients,
Ricci/Jordan data, Petrov invariants, and relative orientations remain live in the full direct-sum
parametrization.

## Zero jets

Every inertia triple `(n_negative,n_positive,n_zero)` summing to four has an exact witness.
`det(g)=0` remains the degeneracy/type-change locus; P01 inverse-based diagnostics are not extended
through it by a guessed generalized inverse.

For the conditional split, the exact triangular congruence proves that base and screen inertia and
rank add and that `det(g)=det(h)det(q)`, even on the degenerate closure. Exactly one of the 36 rows is
the regular P01 branch: Lorentzian base plus positive screen. No row selects that split as UDT's
reciprocal plane.

## First jets and `phi`–angular interaction

With `phi` kept as an independent signed local field, the atlas realizes zero, horizontal-only,
vertical-only, and mixed gradients in every causally available class. A nonzero null gradient is
kept separate from the zero gradient. Therefore unrestricted local configuration geometry does not
force `dphi` to be lightlike, radial, horizontal, or metric-derived.

Within a supplied split, the exact horizontal Lie derivative of the screen separates:

- expansion;
- both shear components and their rank across the two base directions; and
- vertical Frobenius twist/integrability.

All 12 rank combinations have independent exact witnesses. Positive CSN shifts expansion by an
arbitrary base gradient while preserving the screen shear endomorphism and twist. Expansion zero or
sign is therefore not a pre-scale selector. Nonzero twist is a real local nonintegrability stratum,
not a defect to be gauged away.

## Second jets and algebraic type

Every algebraic curvature tensor is converted to an exact normal-coordinate metric second jet and
reconstructed in the P01 sign convention. Exact witnesses cover curvature ranks `0..6` and Ricci
ranks `0..4` without singular-value thresholds or division by the zero branch.

All six Petrov witnesses reconstruct as real Ricci-free Weyl tensors and pass exact curvature
symmetries, Bianchi identity, invariants, nilpotency, and minimal-polynomial separation. `D` and
`II` are not collapsed. Petrov type is pre-scale local data; a Petrov label still retains continuous
moduli and supplies no EOM or preferred direction by itself.

## Verification

The deterministic main atlas reports 21/21 checks with maximum P01 regression residual
`2.220446049250313e-16`. Its result/transcript SHA-256 is:

`154c264b435004274841a144eb9ad1b853aa441628eb2b4706a6682d0a3496db`.

The separately written exact verifier reports 9/9 independent checks and 31/31 exercised corruption
catches. Its result/transcript SHA-256 is:

`9ff3a06b28397386d53a2c5f5bca0eccbfb2abe22efa3ef0dd92b76aaa6c9bde`.

A fresh adversarial model review independently generated the complete 20-dimensional Bianchi kernel,
reconstructed all normal-coordinate basis jets, rechecked the first-jet decomposition and all six
Petrov types, replayed both suites byte-for-byte in memory, found no blocking defect, and returned
`PASS`.

## What P02 does not settle

P02 shows the freedom of the local metric before founded constraints or dynamics. In particular:

- no local geometric identity forces a lightlike `phi` branch or a repeated Weyl direction;
- the conditional split remains supplied, local, and potentially nonintegrable;
- the physical CSN representative and its Ricci/expansion data remain open;
- no action, EOM, matter source, carrier, mass, boundary charge, finite-cell completion, global
  topology, or physical evolution law was selected; and
- local jets establish neither global existence nor stability.

The result constrains later reasoning: any claimed local selector must now be an additional founded
relation or dynamics law acting on this complete atlas. It cannot be credited to metric component
bookkeeping alone.

## Four banking gates

1. **Preregistered:** yes; commit `60ac1f368a18e515c435856620953436460fabc6` precedes atlas construction.
2. **Full space or bounded scope justified:** yes for the complete registered point-local jet and
   continuous curvature parametrization; global, constrained, and dynamical spaces remain outside.
3. **Independently verified on the load-bearing premise:** yes; separate exact implementation,
   31 corruption catches, P01 reconstruction, and fresh adversarial regeneration all pass.
4. **Every premise audited:** yes for the 18-row status, 16-row source, 15-row discriminant, and
   14-row coverage ledgers; every open join and authority boundary remains explicit.

Verdict: `VERIFIED-WITH-CAVEATS / LOCAL_KINEMATIC_SOLUTION_SPACE_CHARACTERIZED_WITHOUT_DYNAMICS`.
