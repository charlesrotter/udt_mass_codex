# G120 audit report — exact spherical screen and imported-transfer SNe recomposition

Date: 2026-08-16

Preregistration commit: `8f9e9b53`

Current status: `BLIND_VERIFIED_WITH_CAVEATS`

## Result

G119's exact central-spherical theorem gives `d_A=R`. With the explicitly imported temporary
radiative bridge

```text
eta=1,
epsilon=1/Z,
T=eta epsilon=1/Z,
```

G94 reduces exactly to

```text
d_L=Z^2 R.
```

The frozen P1 luminosity relation is therefore exactly equivalent, in this declared conditional
interface, to

```text
R_P1(Z)=n X_eff [1-Z^(-2/n)].
```

No independent P1 screen matrix or after-the-fact angular correction remains.
This radius interpretation is only for the outgoing catalog orientation `Z>=1` (all evaluated rows
have `Z>1`). The formula is not a physical areal-radius branch for `0<Z<1`.

## Frozen observational replay

- no optimizer and no new coefficient;
- Pantheon+: `1260.8480887274907 / 1366` nominal dof;
- DES-SN5YR: `1444.1864417504896 / 1622` nominal dof, retaining its low-chi-square warning;
- maximum curve mismatch from G117: below `3.6e-15` magnitude;
- independent precision-domain likelihood replay: PASS;
- no Lambda-CDM distance relation used.

Pantheon+ remains the calibration sample, not a holdout. Its original fitted-`n` provenance has
1365 degrees of freedom; 1366 applies only to this fixed-`n`, one-offset replay.

The wrong `T=1` shortcut is not innocuous. It creates a nonconstant magnitude error and raises the
profiled chi-squares to about `2279.76` and `2135.47`.

## Interpretation

This is a genuine scaffold removal. In the central spherical point-observer class, the data and
temporary light bridge now constrain one scalar areal-radius history component rather than an
arbitrary tensor-valued screen ansatz. The result still does not select the complete orbit metric,
frequency-to-affine map, terminal depth, physical branch population, native transfer, or global
history.

The formal P1 radius limit `n X_eff = 2202.6331050379085 Mpc` is an extrapolated family property,
not a measurement of `X_max` and not a derived global endpoint.

## Evidence and caveats

- 15 preregistered source hashes pass;
- exact symbolic transfer reduction passes;
- all frozen curve, likelihood, row-count, and fixed-parameter gates pass;
- implementation-distinct covariance/precision replay passes;
- one pre-output JSON type repair and one exact-algebra gate correction are disclosed in
  `CORRECTION_RECORD.md`;
- fresh blind read-only review independently reproduced the load-bearing values, required three
  scope/evidence repairs, and verified all repairs; no external transmission was used.

## Maximum conclusion

`CONDITIONAL_RADIUS_FREQUENCY_RECOMPOSITION_PRESERVES_DUAL_SNE`.

No native UDT light theory, complete physical metric history, `X_max`, CMB/BAO result, action,
bootstrap, matter, mass, or signalling law follows.
