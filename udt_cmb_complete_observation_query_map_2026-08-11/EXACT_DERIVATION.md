# Complete CMB observation-query map — exact derivation

## 1. The observed object and the theory-side object are different types

The observational TT object can be represented, without importing a cosmological dynamics, as a
real scalar field on the observer's celestial screen,

```text
Theta(n) = T(n)/T_bar - 1,
a_lm = integral Theta(n) conjugate(Y_lm(n)) dOmega,
C_l^TT = (1/(2l+1)) sum_m |a_lm|^2.
```

This is an `OBSERVED/COMPARISON` definition of the reported angular statistic. It does not say
what produced `Theta`, how a comparison structure is related to the observer's sky, or which UDT
geometry is physical.

A UDT-native prediction of that object would require, at minimum, the following typed chain:

```text
ordered observer-sky query
    -> one or more regular relation realizations
    -> terminal pair state plus screen map and allowed transport
    -> conditional/native response or mode structure
    -> state/source covariance and normalization
    -> scalar sky field or its covariance
    -> C_l^TT and its peak positions/heights.
```

The arrows mean typed dependency, not material signal travel. This audit remains entirely about
inter-observational-frame relations in a co-present geometry. Local calibration remains `c_E`.

## 2. Exact separation of spectrum and power

Let a conditional operator supply modes `e_j` with spectral locations `omega_j`. A scalar sky field
expanded in their projected images has coefficients `a_j`. Its quadratic power reads the second
moments `E[a_j conjugate(a_k)]`, not merely `omega_j`.

Hold the operator and spectrum fixed. Three admissible algebraic covariance assignments are

```text
W_A = diag(1,0,1,0),
W_B = diag(0,1,0,1),
W_0 = 0.
```

They produce different nonzero mode supports, and the last produces no power at all, while the
spectrum is identical. Therefore:

```text
mode existence does not derive nonzero angular power;
the spectrum alone does not identify which modes form observed peaks;
peak heights and overall amplitude require additional state/source information.
```

`verify_spectrum_power_nonuniqueness.py` checks this finite countermodel exactly. It is not a
physical source model; it is a type/no-uniqueness proof.

## 3. What the historical CMB calculation actually read

The corrected F00 atlas owns `10,080` roots of a `CHOSE` stationary equatorial scalar operator,
conditioned on the P1 shape family, sampled mixing, real `m=-1,0,+1`, and free D/N wall
representatives. The attributed phase then fit each ladder to seven published TT peak locations
with two affine freedoms.

Consequently its map is

```text
conditional C0 scalar roots
    -> two-parameter affine location comparison
    -> attributed TT position residuals.
```

It did not construct the physical CMB observer query, a screen/Jacobi map, a native response
kernel, a state covariance, peak power, or polarization. The result remains a compatibility
diagnostic. The corrected three-ladder atlas also withdraws the earlier centered-multiplet reading.

## 4. Complete-query channel typing

Once a regular pair immersion `F` is supplied, the metric owns

```text
h = F* g,
kappa_pair = (1/4) log(-det h),
phi_pair = (1/4) log((-det h)/h_00^2),
beta_pair = h_01/h_00.
```

The conditional pair cone then has

```text
c_eff^(pair)/c_E = exp(-2 phi_pair).
```

This is an inter-observer readout, not a local material speed. It does not by itself create a
celestial angular map. That requires a screen Jacobi map or a mathematically equivalent component
of the actual query realization. Ambient transport exists after a path is supplied. Normal/screen
transport exists after a pair immersion is supplied.

For a scalar TT observable, a pure `SO(2)` rotation of the screen basis does not alter the scalar
temperature value. Therefore normal holonomy is not a direct scalar-TT modulation merely because
it exists. An orientation-sensitive polarization field is different: it requires a screen-frame
carry or equivalent connection and a spin-sensitive source/statistical rule. The runnable finite
check records this distinction without claiming a polarization dynamics.

## 5. Exact family census

The frozen `F00`--`F17` universe is reproduced one-for-one in
`FAMILY_REALIZATION_ATLAS.tsv`.

- `F00` is the incomplete equatorial control and the only family with the historical attributed
  position diagnostic.
- `F01` is the round `SO(3)` local control.
- `F02` is the conditional axis-regular C1 screen; its `15,420` coupling-matrix elements are banked,
  but no eigenvalue solve or physical profile is selected.
- `F03`--`F04` are general screen envelopes without selected profiles.
- `F05`--`F14` are conditional S3 controls that may not be spliced into the WR-L radial background.
- `F15` is the degenerate no-inverse control.
- `F16` is the global non-toric availability countercontrol.
- `F17` is the general positive-screen algebra envelope, not a physical completion.

None of these ambient-geometry families supplies a physical CMB observer-pair query or pair
immersion. Hence none currently owns the terminal pair state, observer-sky Jacobi map, same-query
ambient/normal transports, source covariance, TT power prediction, or polarization prediction.
This is not evidence that such a realization does not exist. It is an ownership result over the
frozen registered universe.

## 6. What does and does not follow

The complete metric has much richer angular structure than the old equatorial slice: generic
screens mix `ell`, may mix `m`, and contain a shift-divergence term absent from the axial shortcut.
That structure remains live. But its existence is not yet a rule selecting a physical screen,
population, or observed peak.

The low-redshift P1 SNe result travels only as a compatibility anchor after a CMB pair profile is
constructed. It cannot be copied into a centered CMB lapse. `X_max` travels only as the working
observer-pair positional-dilation asymptote. It is not a local wall, a boundary condition, a path,
or a family selector.

## 7. Smallest next calculation

The next calculation should construct one identical, explicit observer-sky query protocol on each
of two nonphysical controls:

1. the round `F01` geometry;
2. the axis-regular mixing-on `F02` geometry.

For each, derive the query's pair immersion/correspondence and screen Jacobi map from the same
metric realization before any eigenvalue solve. The comparison is a control pair, not a contest to
choose the universe. It will test which old affine projection freedom is replaced by geometry and
which freedom remains query- or source-owned. Only after that map exists can FD2 be reformulated
without postselecting a ladder.

