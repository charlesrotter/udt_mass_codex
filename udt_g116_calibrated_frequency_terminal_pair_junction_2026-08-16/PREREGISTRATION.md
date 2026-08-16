# G116 preregistration — calibrated frequency / terminal-pair junction

Date: 2026-08-16

Status: `PREREGISTERED_BEFORE_CONFIRMATORY_IMPLEMENTATION`

## Whole question and bounded regime

For the exact G115 smooth central spherical time-live two-jet and its supplied central observer,
outgoing radial-null branch, and smooth source congruence, determine whether the founding
reciprocal-`c_E` semantics and complete metric derive a coefficient-free junction between:

1. terminal reciprocal pair depth `phi_pair`;
2. source/observer frequency depth `zeta=log(omega_s/omega_o)`;
3. pair `c_eff/c_E=exp(-2 phi_pair)`; and
4. the optical/relative-drift channels already derived from the same metric and query.

This is a local two-jet calculation through `O(R^2)`. It is not a history solve, fit, global branch,
finite-radius result, radiation law, or observational validation.

## Mode

Metric-led. No target curve, redshift formula, SNe outcome, BAO/CMB datum, action, source dynamics,
bootstrap condition, matter model, or `X_max` realization may be used.

## Exact pins and free data

| Item | Status | Scope |
|---|---|---|
| `T=c_E t` | `pinned-by-THEORY/OBSERVED` | measured clock/ruler calibration |
| smooth central areal two-jet | `pinned-by-THEORY` | G115 regularity/parity class |
| outgoing radial-null orientation | `free-and-explored/CHOSE_QUERY` | reverse branch checked separately |
| source congruence `v=qR+O(R^3)` | `free-and-explored/CONDITIONAL_QUERY` | no source dynamics |
| active sky drift `w_A` | `free-and-explored/CONDITIONAL_QUERY` | passive relabeling excluded as gauge |
| `n,ell,b,q` | `free-and-explored/GAUGE_REPRESENTATIVES` | only invariant combinations may enter conclusions |
| terminal fixed-label and quotient depths | `pinned-by-THEORY` | both retained and not silently identified |
| spectroscopic name `1+z` | `OMITTED/SEALED` | only invariant frequency ratio `Z` is calculated |

No value is `pinned-by-HABIT`.

## Design-stage pilot disclosure

Before this preregistration, hand algebra suggested defining

```text
v_rel = b-q,
A_opt = 2 ell+2 n+dot(b),
phi_pair^quotient = p2 R^2+O(R^3),
```

and testing the candidate identity

```text
zeta = v_rel R + [p2-A_opt/4+dot(v_rel)]R^2+O(R^3).
```

For the fixed-label readout the candidate replaces `p2` by `p2_fixed-|w|^2/2`. This pilot is
disclosed and does not count as confirmatory evidence.

## Required derivation and type checks

1. Reconstruct `phi_pair`, `c_eff/c_E`, `zeta`, `v_rel`, and `A_opt` independently from the declared
   metric/query inputs.
2. Prove or reject residual areal-time-slicing invariance of every displayed combination.
3. Prove or reject the candidate junction symbolically without assigning numerical coefficients.
4. Check the exact pure reciprocal stationary reduction. The preregistered expected reduction is
   `v_rel=0`, `A_opt=0`, `zeta=phi_pair`, and `c_eff/c_E=exp(-2 zeta)`.
5. Classify neutrality, reversal, and matched-middle composition for frequency ratios separately
   from terminal-pair calibration composition.
6. Enumerate all smooth algebraic monomial junctions allowed by neutrality, reversal, composition,
   and pure-reciprocal normalization; do not assume those gates imply uniqueness.
7. Reject any expression that counts the same metric contribution twice or identifies a supplied
   source clock with the terminal tape clock without a boundary condition.
8. Freeze the resulting low-distance series. Do not open either SNe dataset in G116.

## Omitted sectors and limits

Excluded: higher radial jets; finite-radius evolution; nonspherical shear; caustics/cut loci;
multiple branches; global calibration descent; radiation transfer and energy ownership; source
population; physical history selection; SNe/BAO/CMB outcomes; `X_max`; action; bootstrap; matter;
mass; signalling.

## Certification and falsification contract

- exact symbolic reconstruction with all identities reduced to zero;
- implementation-distinct standard-library rational or randomized numerical verification;
- hostile mutations deleting relative drift, optical correction, sky correction, or one time
  derivative must be caught;
- a fresh adversarial context must test type ownership and any uniqueness claim;
- package rerun, source hashes, repository premise verifier, tests, and `git diff --check` must pass.

The candidate is falsified if it is not algebraically identical to the independently reconstructed
frequency contraction, fails residual-gauge invariance, fails the pure reciprocal control, or
requires an observationally chosen coefficient.

## Preregistered landings

One of:

- `COEFFICIENT_FREE_METRIC_QUERY_JUNCTION_DERIVED_CONDITIONALLY`;
- `LAWFUL_JUNCTION_FAMILY_NONUNIQUE_UNDER_FOUNDING_GATES`;
- `TERMINAL_AND_FREQUENCY_CHANNELS_REMAIN_TYPED_BUT_UNJOINED`;
- `CANDIDATE_JUNCTION_REJECTED`.

These may coexist when the algebraic junction is unique for a supplied query but the physical
observed-redshift owner remains unselected.

## Maximum conclusion

A local gauge-invariant metric/query identity and its exact type/composition scope, or a precise
nonuniqueness/type obstruction. No physical history, empirical redshift law, SNe result, global
profile, `X_max`, BAO/CMB prediction, action, source dynamics, bootstrap, matter, mass, or
signalling claim.
