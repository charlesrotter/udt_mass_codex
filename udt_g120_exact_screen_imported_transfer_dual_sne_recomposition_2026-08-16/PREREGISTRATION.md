# G120 preregistration — exact screen plus imported-transfer dual-SNe recomposition

Date: 2026-08-16

## Whole question and bounded regime

On the exact G119 central-spherical radial point-observer class, replace the former independently
supplied isotropic P1 screen by the metric theorem `d_A=R`. Explicitly import, only as a temporary
radiative bridge, conserved carried amount and endpoint-frequency energy,

```text
eta=1,
epsilon=1/Z,
T=eta epsilon=1/Z.
```

Recompose the frozen Pantheon+ and DES-SN5YR P1 likelihoods without changing `n`, adding a shape
coefficient, or importing a Lambda-CDM distance relation. Determine whether the old luminosity
curve becomes exactly the conditional areal-radius history

```text
R_P1(Z)=n X_eff [1-Z^(-2/n)]
```

under `d_L=Z^2 R`, and whether both frozen numerical returns are preserved.

The test is limited to the published processed release coordinates already conditionally adopted
in G117 (`zCMB` for Pantheon+, `zHD` for DES), one central spherical regular branch, and the
registered SNe cuts. It is not a nonspherical, off-center, multiple-image, native-light, global,
or `X_max` calculation.

## Ownership ledger before outcomes

### `pinned-by-THEORY`

- G119: `D_sky=R O` and `d_A=R` on every finite regular branch of the declared query class.
- G94: `d_L^2=Z^3 d_A^2/(eta epsilon)` after source isotropy is supplied.
- Positivity and regularity of `Z`, `R`, and the declared branch.

### `IMPORTED_CONDITIONAL`

- transparent null-momentum transfer: `eta=1`, `epsilon=1/Z`, hence `T=1/Z`;
- standardized-source luminosity interpretation and the existing catalog corrections;
- processed release coordinates occupy the frequency-ratio slot.

These imports are observational bridge assumptions, not UDT derivations. In particular `T=1` is
not the chosen transparent closure and must not be silently substituted.

### `pinned-by-OBSERVATION`

- Pantheon+ and DES released vectors and covariance products;
- frozen Pantheon+ calibration `n=1.0559332414320268` and conditional `X_eff`;
- existing row cuts and redshift-column choices.

### `free-and-explored`

- exactly one additive magnitude offset per frozen likelihood, analytically profiled as before;
- no shape, transfer, history, or cosmological parameter is free.

### `pinned-by-HABIT`

- none.

## Omitted sectors and boundaries

Displaced observers, nonspherical perturbations, extended beams, source evolution, absorption,
scattering, detector-bandpass reconstruction, multiple-image weights, caustic aggregation, direct
terminal-depth inference, a complete `h_ab` history, `X_max`, CMB, BAO, bootstrap, action, matter,
mass, and signalling are omitted.

## Preregistered checks and tolerances

1. Verify all 15 exact source hashes before evaluating the likelihoods.
2. Algebraically verify that G94 plus G119 plus the imported transfer gives `d_L=Z^2 R`.
3. Reconstruct `R_P1` and require its distance-modulus shape to agree with the frozen G117 P1
   curve to `1e-12` magnitude in both catalogs.
4. Use no optimizer. Keep `n` bit-identical. Profile only the registered additive offsets.
5. Reproduce Pantheon+ chi-square within `3e-5` and offset within `3e-6` of G117.
6. Reproduce DES chi-square within `2e-6` and offset within `2e-9` of G117.
7. Verify `R(1)=0`, `dR/dZ>0` for `Z>0`, origin slope `dR/dz=2 X_eff`, and
   `lim_(Z->infinity) R=n X_eff` for the conditional P1 family.
8. Demonstrate that the hostile `T=1` replacement changes the magnitude shape and is not absorbed
   by one constant offset over either catalog.
9. Independently replay the load-bearing curve and both likelihoods by an implementation-distinct
   precision-domain route.

## Falsification and classification contract

- Any source-hash, row-count, fixed-parameter, algebraic, curve, likelihood, or independent-replay
  gate failure lands `G120_GATE_FAILURE`.
- Exact curve and likelihood preservation lands
  `CONDITIONAL_RADIUS_FREQUENCY_RECOMPOSITION_PRESERVES_DUAL_SNE`.
- A numerical pass cannot upgrade P1 into a metric-selected history, derive the imported transfer,
  identify terminal `phi_pair`, or identify the finite P1 radius asymptote with `X_max`.

## Maximum conclusion

At most G120 may show that, on the exact G119 central-spherical screen and the explicitly imported
transparent-transfer bridge, the frozen dual-SNe luminosity relation is exactly equivalent to one
conditional empirical areal-radius-versus-frequency curve and preserves both banked likelihoods.
It cannot establish a complete physical metric history, a native UDT theory of light, `X_max`, or
downstream cosmology.
