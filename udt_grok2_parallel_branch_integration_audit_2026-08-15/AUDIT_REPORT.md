# Audit report — `grok2` parallel-branch integration

Date: 2026-08-15

## Landing

```text
GROK2_PARTIALLY_INTEGRATED_WITH_REGRADING
__OBSERVER_CENTERED_TWO_SOURCE_QUERY_CLARIFIED
__MEGAMASER_LOCAL_SLOPE_RETAINED_AS_SOURCE_LEAD
__TANH_XMAX_FLUX_AND_SCALAR_MU_PROMOTIONS_REJECTED
```

`origin/grok2` is not a continuation of current `grok`. It forked at `b343566a` before the G93--G100
kernel, transfer, and observational work and added four parallel commits ending at `13921e81`.
Merging it wholesale would restore stale startup prose and weaker scientific typing. No merge or
cherry-pick was performed.

## What survives

### 1. Observer-centred BAO query correction

The branch correctly rejects the picture of two distant galaxies directly performing the UDT
observer comparison. The measured angular statistic is assembled at one observer from source
directions on that observer's sky.

The branch's single Earth--source arrow is nevertheless incomplete for the existing BOSS lane.
The frozen estimator counts angular pairs. The minimal typed observational query is therefore

```text
(observer O, source q1, source q2, redshift selection, angular separation, weighting/statistic).
```

Equivalently, it joins two complete observer--source relations at a common observer before the
two-point statistic is formed. This is an operational query correction, not a standard-ruler,
galaxy--galaxy signalling, BAO-origin, or UDT-response theorem.

### 2. Megamaser local-slope lead

The cited primary megamaser result reports

```text
H0 = 73.9 +/- 3.0 km s^-1 Mpc^-1,
```

which corresponds arithmetically to

```text
c/H0 = 4056.73 +/- 164.68 Mpc.
```

The frozen G99 P1 radial calibration has origin slope

```text
dr_P1/dz|0 = 2 X_eff = 4171.92 Mpc.
```

The central values differ by about 2.84 percent. This is a useful source-level consonance between
an independent geometric-distance Hubble measurement and the conditional G99 low-redshift slope.
It is not yet a data-level replay: `grok2` contains no local maser table, uncertainty calculation,
code, or artifact manifest, and G99's absolute scale carries its registered luminosity anchor and
conditional transfer.

This observation is also not new scale ownership. The earlier M4 package already identified
`2 X_eff` as the P1 quantity playing the local `c/H0` role. `grok2` contributes a specific
independent primary-source comparison, not a newly derived UDT constant.

## The decisive regrading

Let `Z=1+z`. The `grok2` chosen profile is

```text
r_tanh(Z) = X_tanh (Z^2-1)/(Z^2+1).
```

Its origin slope and asymptote are both `X_tanh`:

```text
dr_tanh/dz|0 = X_tanh,
lim_(Z->infinity) r_tanh = X_tanh.
```

The frozen conditional G99 P1 radius is

```text
r_P1(Z) = n X_eff [1-Z^(-2/n)],
```

with

```text
dr_P1/dz|0 = 2 X_eff,
lim_(Z->infinity) r_P1 = n X_eff.
```

Matching only the nearby slope forces `X_tanh=2 X_eff`. It then leaves the asymptotes separated by

```text
X_tanh/(n X_eff) = 2/n = 1.894059... .
```

Thus the approximately 4 Gpc maser value determines a local derivative only. Calling it `X_max`
first assumes the `tanh` profile whose global shape is still unowned. Nearby masers cannot test the
bend or distinguish these profiles. The `grok2` `X_max` inference is therefore circular at the
profile-selection step.

## Claims not integrated

| `grok2` claim | Current regrade | Reason |
|---|---|---|
| `phi_rad=artanh(r/X)` from finite maximum comparison | `CHOSE` profile family | G14 keeps the exact profile and value of `X_max` open |
| masers determine `X` near 4 Gpc | `OBSERVED_SOURCE_LEAD` for local slope only | local slope does not own the asymptote without a profile law |
| `d_L=rho Z^2` derived by Liouville | `CONDITIONAL` | G94--G95 leave physical transfer open; `Z^2` needs the registered extra carrier assumptions |
| August `mu_lock` is the angular comparison arrow | `VERIFIED_WITH_CAVEATS` restricted slice only | G92 maps it to one component of a supplied endpoint transition; modern `S` has four components |
| static `k`/`mu_lock` formula supplies complete BAO response | `OPEN` | no selected complete history, physical pair realization, or two-source response |
| 2.725 K bath is a redshifted starlight screen | `POSIT_NOT_ACTIVATED` | source, spectrum, transfer, and sky coherence are not derived |
| `grok2` startup surface should replace current files | `REJECTED` | it predates and conflicts with G93--G100 |

## Evidence gates

1. **Preregistered:** no. This is a post-existing-source integration audit, not a blind discovery
   test. No claim is graded above `INTERNALLY_VERIFIED_WITH_CAVEATS`.
2. **Full or bounded:** full for the five-file `grok2` scientific package and its explicit claims;
   bounded against the cited current G92/G94/G95/G99 and BAO method authorities.
3. **Independently verified:** exact profile identities, slopes, asymptotes, and numerical
   translations were recomputed by a standalone standard-library script. No independent raw
   megamaser data replay was possible from the branch artifacts.
4. **Premises audited:** yes for the bounded integration. Profile choice, local slope, asymptote,
   transfer, complete mixing, observer query, source interpretation, and startup authority are
   separated.

## Maximum conclusion

The branch contributes a useful observer-centred query correction and a promising independent
local-slope cross-check. It does not close `X_max`, select a complete metric history, derive the
flux law, complete the angular/mixing orchestra, or supply BAO/CMB/source physics.

## Next bounded action

Use the corrected BAO query type when deriving the preregistered observable map:

```text
one observer + two complete observer--source relations + angular statistic.
```

Do not read the frozen BAO curves while deriving that map. Keep the maser value as a later local
derivative check, not an asymptotic calibration.
