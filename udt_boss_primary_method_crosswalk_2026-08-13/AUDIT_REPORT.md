# BOSS primary-researcher method crosswalk

Date: 2026-08-13
Status: `VERIFIED-WITH-CAVEATS__METHOD_AND_INPUT_CONSISTENT__NO_EXACT_PUBLISHED_CURVE_MATCH`

## Result first

The frozen R0--R2 observer-coordinate pipeline is methodologically consistent with the official
BOSS DR12 catalog construction and with a primary thin-shell angular-correlation analysis in every
layer that has the same mathematical type.

This is a useful positive control. The local curves were not produced by an invented catalog
weight, malformed random footprint, or incorrect Landy--Szalay denominator.

It is not a feature validation. No primary publication supplies the exact same frozen query, so no
published curve or peak was numerically compared.

## What passed

### Exact catalog lineage

The eight local filenames and byte sizes exactly match the official DR12 BOSS LSS SAS listing. The
official data models identify the same LOWZ/CMASS and North/South product partitions and the same
required coordinate and weight fields. An independent Astropy reader recovered the frozen row
counts and every required schema field from all eight files.

The local SHA-256 hashes remain the authoritative local identity pins; the public listing provides
an independent name-and-size cross-check.

### Redshift envelopes

The DR12 catalog paper prints strict notation (`0.15 < z < 0.43` for LOWZ and
`0.43 < z < 0.7` for CMASS), whereas the frozen local expressions include the outer lower/upper
endpoints. A full independent scan of all four measured catalogs found no row whose inclusion
changes. The realized local and publication-notation masks are identical for these files:

| sample/cap | rows in scope | differing rows |
|---|---:|---:|
| CMASS North | 568,776 | 0 |
| CMASS South | 208,426 | 0 |
| LOWZ North | 248,237 | 0 |
| LOWZ South | 113,525 | 0 |

The notation difference is therefore recorded but has no realized effect on R0--R2.

### Weight ownership

The collaboration's total observational weight is

```text
WEIGHT_SYSTOT * (WEIGHT_CP + WEIGHT_NOZ - 1).
```

That is exactly the local `W3_OFFICIAL_OBS` lane. It is the primary-source-supported unbiased
observational lane because the same weight was used when random redshifts were assigned.

The other three lanes are still lawful preregistered controls, but their status is now sharper:

- `W0_UNIT`: unit-weight diagnostic;
- `W1_SPECTRO`: fiber-collision/redshift-failure diagnostic;
- `W2_IMAGING`: angular-systematics diagnostic;
- `W3_OFFICIAL_OBS`: official combined observational weighting.

They must not be described as four equally official estimators.

The paper also explicitly makes FKP optional. When it is omitted, the consistent weights are the
total observational galaxy weight and unity random weights, exactly as used by W3 locally. Thus the
absence of `WEIGHT_FKP` and `NZ` is a supported non-optimal observational choice, not an error. It
also keeps the frozen location measurement free of the catalog's fiducial-comoving-density factor.

### Randoms, masks, and vetoes

The official random catalogs sample the angular footprint in proportion to sector completeness,
have vetoed regions removed, and receive redshifts drawn from the measured galaxy distribution with
the total observational weights. The local files are those final released random products.

The local 5x, 10x, and 20x sets are deterministic coordinate-blind subsets of the official roughly
50x parent. This is a declared numerical transform rather than a published BOSS product. It remains
acceptable only as the frozen nested random-density control already measured in R2 and propagated
into R3; it is not promoted into survey methodology.

### Angular estimator

The closest primary thin-shell analysis uses the same spherical angular separation, weighted
finite-sample normalizations,

```text
DD_total = ((sum w_D)^2 - sum(w_D^2))/2
DR_total = (sum w_D)(sum w_R)
RR_total = ((sum w_R)^2 - sum(w_R^2))/2,
```

and the same Landy--Szalay combination. With unity random weights, its DR and RR denominators reduce
exactly to the local formulas. Direct finite enumeration independently confirmed all three
identities.

## Why no published curve was used

The closest published angular analysis differs from the local query in several load-bearing ways:

- North only rather than both North and South;
- a different BOSS/eBOSS luminous-red-galaxy sample construction;
- shell centers separated by 0.02 with widths from 0.005 to 0.02 rather than the frozen local
  0.01/0.02/0.04 unions;
- FKP included;
- 0.3-degree angular bins over 1.5--7 degrees rather than 0.25-degree bins over 0.25--30 degrees;
- downstream mock covariance, a phenomenological peak template, zero-width extrapolation, and bias
  corrections.

Consequently, its estimator is a strong architectural cross-check, but its plotted curves and
reported peak locations are not the same object. Using them as a target would violate the frozen
comparison contract.

## What this says about the next long stage

The cross-check removes a worthwhile early failure mode before R3 finishes: the pipeline's catalog
and estimator foundations are sound. It does not make the R3 covariance run unnecessary. R3 is
still required to decide whether any structure in the 2,328 local curves is reproducible across
data-only spatial resamples rather than random-catalog or finite-sample noise.

## Maximum justified conclusion

`VERIFIED-WITH-CAVEATS`: the frozen R0--R2 pipeline is consistent with official BOSS DR12 catalog,
weight, random, mask, and estimator semantics. W3 is the official observational lane; W0--W2 are
diagnostic controls; the nested random sets are local numerical controls. No exact published raw
curve exists for the frozen query, and all published acoustic/peak/model products remain
`NONCOMPARABLE_MODEL_TRANSFORM`.

This audit does not detect BAO, validate UDT, select a feature, supply covariance or significance,
infer a physical scale, or determine `X_max`.
