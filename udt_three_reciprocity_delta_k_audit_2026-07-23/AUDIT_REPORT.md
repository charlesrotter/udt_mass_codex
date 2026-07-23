# Three-reciprocity `Delta_K` audit

Date: 2026-07-23
Base/preregistration commit:
`51a355a746fab82baa9760ceaf564f20ab2e1099`

## Result

The three UDT reciprocities are mutually compatible, but their registered
content does **not** derive either missing premise of the prior angular
closure theorem.

```text
Delta_K = K_eff_angular - K_rec = 0        NOT DERIVED
two regular reciprocal mirror seals        NOT DERIVED
```

The useful positive result is a sharper conditional reduction. Under the
strongest charitable additions—supplied regular screen, central angular
source, translation homogeneity in the normalized depth, favorable
negative source sign, parallel transport, nonsingular flow, and two area
seals—the open tensor source reduces to one dimensionless scalar
`lambda`. The seals force the initial angular shear magnitude to equal
`lambda`; they do not force `lambda=1`.

Grade: `VERIFIED-WITH-CAVEATS`.

## Keep the three meanings separate

The exact role map is
[THREE_RECIPROCITY_ROLE_MAP.tsv](THREE_RECIPROCITY_ROLE_MAP.tsv).

1. **Reciprocal-c** supplies the clock/ruler pair and its generator

   ```text
   L = diag(-1,+1),       K_rec = -L^2 = -I.
   ```

   This is an exact reference source in the abstract reciprocal pair. It
   is not by itself an equation for the complete metric's angular source.

2. **Observer-frame reciprocity** says ordinary-regime descriptions carry
   the same law without a preferred observer. For a supplied frame action,

   ```text
   Delta_K' = S Delta_K S^-1.
   ```

   Therefore `Delta_K=0` is frame independent. But covariance does not
   require zero: `Delta_K=mu I` is unchanged by every conjugation.

3. **Xmax reciprocity** is still a working global-limit posit plus a
   chosen conditional bounded group:

   ```text
   xi ⊕ eta = (xi+eta)/(1+xi eta),
   phi = atanh(xi).
   ```

   It supplies an exact reversal and additive coordinate inside the chosen
   realization. It is not yet joined to absolute metric `phi`, and
   `xi=+1` and `xi=-1` are excluded limits. Their mutual composition has
   zero denominator, so they are not a derived pair of regular seals.

## Exact countermodels

[COUNTERFAMILY_ATLAS.tsv](COUNTERFAMILY_ATLAS.tsv) records four
load-bearing families.

The smallest is

```text
Delta_K = mu I.
```

It leaves the reciprocal-c reference pair intact, is covariant under every
frame conjugation, and is even under Xmax reversal. Thus the combined
symmetries permit a nonzero mismatch.

Even imposing formal endpoint agreement does not repair this:

```text
Delta_K = mu (1-xi^2)^2 I
```

vanishes toward both Xmax limits while remaining nonzero in the bulk.
Without an independently registered angular-isotropy premise, the
reversal-even anisotropic family

```text
Delta_K = nu xi (1-xi^2)^2 L
```

also survives. These are source/metric-jet counterfamilies, not claimed
complete on-shell universes.

## Strongest charitable scalar reduction

To expose the smallest remaining seam, the audit adds rather than derives
centrality, depth homogeneity, a favorable sign, a parallel regular screen,
and nonsingular flow:

```text
K_eff = -lambda^2 I,
 B_phi + B^2 - lambda^2 I = 0.
```

For a first area-neutral seal

```text
B0 = J0,       J0^2 = s^2 I,
t = tanh(lambda Delta_phi),
```

the exact solution is

```text
B = lambda (B0+lambda t I)(lambda I+t B0)^-1.
```

Its invariant area and shape diagnostics are

```text
A_rel =
  lambda t (lambda^2-s^2)/(lambda^2-s^2 t^2),

S_shape =
  lambda^4 s^2 (1-t^2)^2/(lambda^2-s^2 t^2)^2.
```

At a second nontrivial area-neutral seal, regularity gives

```text
s^2 = lambda^2.
```

Then throughout the branch

```text
A_rel = 0,       S_shape = lambda^2.
```

Exact witnesses `lambda=2` and `lambda=3` give `S_shape=4` and `9`.
Consequently even the granted two-seal theorem does not select the unit
normalization.

## What became simpler

At current premise strength, the missing object remains a covariant
angular source tensor. If one additionally grants the most symmetry-
friendly central and homogeneous completion, the ambiguity contracts to
one number:

```text
lambda = relative normalization between the reciprocal source
         and the angular Jacobi source.
```

This is genuine narrowing. It is not closure. `c` fixes the clock/ruler
conversion and the normalization of reciprocal `phi`; `G` supplies a
dimensional gravitational anchor. CSN removes common scale. None of these
registered facts fixes this remaining dimensionless inter-sector ratio.

## Global and bootstrap rulings

The conditional Xmax group acts on an open interval, not on its limiting
ends. The current repository also retains unresolved joins between
observer-relative depth, absolute static `phi`, physical position, and the
finite-cell seal. Therefore Xmax reversal cannot currently be promoted to
a complete metric boundary condition.

The finite-cell and bootstrap premises contain no registered executable
boundary functional, response map, or stationarity equation that evaluates
`lambda`. They remain potential owners of the missing selection, not
present derivations of it.

All fourteen route rulings are in
[ROUTE_RULING_MATRIX.tsv](ROUTE_RULING_MATRIX.tsv), and every load-bearing
join is exposed in [JOIN_LEDGER.tsv](JOIN_LEDGER.tsv).

## Verification

- preregistered before production algebra: **yes**;
- whole solution space: **bounded exact symmetry/source audit**, not the
  space of complete on-shell universes;
- independent load-bearing verification: **yes**, a standard-library
  rational implementation importing no production code;
- premise audit: **yes**, with founding, owner-locked, working, chosen,
  conditional, and open premises separated;
- production catch-proofs: **18/18**;
- independent catches: **18/18**;
- reciprocal covariance controls: **6**;
- Xmax group controls: **13**;
- constant-`lambda` transport controls: **32**;
- source hashes replayed independently: **20**;
- compute: CPU only.

The caveat in the grade is semantic independence: project policy forbids
delegating to a fresh agent unless the user explicitly requests agents.
The algebra was independently reimplemented, but no separate zero-context
model adjudication was performed.

## Status

```text
reciprocal-c pair and generator                 DERIVED_IN_ABSTRACT_PAIR
reference K_rec=-I                             DERIVED_REFERENCE_SOURCE
ordinary observer-frame covariance             OWNER_LOCKED_ORDINARY_REGIME
Delta_K zero is frame independent              DERIVED
observer covariance forces Delta_K zero         NOT DERIVED
one global Xmax                                WORKING POSIT
fractional Xmax group                          CHOSE / CONDITIONAL
Xmax-to-absolute-phi join                       OPEN
Xmax endpoints are regular seals               NOT DERIVED
three reciprocities force Delta_K zero          NOT DERIVED
central homogeneous reduction to lambda         CONDITIONAL
two seals imply s^2=lambda^2                   DERIVED / CONDITIONAL
lambda=1                                       OPEN
complete action/source/boundary                 OPEN
```

No equations, physics labels, startup controls, frozen evidence, action,
carrier, source, mass claim, or canon were changed.
