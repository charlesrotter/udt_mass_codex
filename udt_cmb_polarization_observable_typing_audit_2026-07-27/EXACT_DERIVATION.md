# Exact derivation — CMB polarization observable typing

## 1. Metric screen geometry is not physical polarization

Given a typed observer and a supplied null direction, the complete Lorentzian metric defines a
two-dimensional screen quotient transverse to the observer and ray. The Levi-Civita connection can
transport screen vectors, screen tensors, and the registered first-order Jacobi state along a
supplied path. This is `METRIC_GEOMETRIC_CAPABILITY`.

A measured linear polarization field is additional physical data. Calling a transported screen
vector or trace-free screen tensor “photon polarization” requires a native carrier and propagation
law. In standard comparison theory that role is supplied by Maxwell geometric optics; current UDT
does not derive or adopt that field. Therefore

```text
metric screen bundle and transport != native physical polarization field.
```

The difference is load-bearing. It prevents a geometric holonomy calculation from being promoted
directly to a CMB prediction.

## 2. Exact spin-two readout algebra

For externally supplied Stokes data in a chosen oriented screen basis, define

```text
P_plus  = Q+iU,
P_minus = Q-iU.
```

Under a screen-basis rotation by angle `psi`, these transform with twice the angle, with the sign
depending on convention:

```text
P_plus  -> exp(-2 i psi) P_plus,
P_minus -> exp(+2 i psi) P_minus.
```

The factor-of-two representation composes and reverses exactly. The production derivation verifies
the symbolic trigonometric group law; the independent verifier uses exact Gaussian-rational unit
complex numbers and no production code.

The all-sky `E/B` decomposition is a nonlocal spin-harmonic change of representation. Under a
uniform supplied rotation `alpha`, one conventional sign choice gives

```text
[E']   [ cos(2 alpha)  -sin(2 alpha)] [E]
[B'] = [ sin(2 alpha)   cos(2 alpha)] [B].
```

This identifies `EB` and `TB` as rotation-sensitive external readouts. It does not identify the
origin of the rotation, select a UDT extension, or distinguish physical rotation from an overall
polarization-angle calibration error.

## 3. Exact information loss in isotropic power spectra

For real harmonic coefficients at fixed `ell`, an isotropic power estimate has the form

```text
C_ell = (1/(2 ell+1)) sum_m |a_ell_m|^2.
```

At `ell=2`, take two distinct real-harmonic coefficient vectors

```text
A=(1,0,0,0,0),
B=(0,1,0,0,0).
```

Both give exactly `C_2=1/5`. Hence the map-to-spectrum operation is noninjective: it loses which
directional harmonic component carried the power. Phases and many off-diagonal correlations are
also discarded.

Consequently `EE`, `BB`, `TE`, `TB`, and `EB` spectra under an isotropic diagonal compression cannot
by themselves certify a direction-dependent or path-dependent holonomy law. A spatially varying
rotation multiplies the sky field in position space and therefore generically couples different
harmonic modes; the natural readout then includes off-diagonal covariance or real-space spin
correlation, not only diagonal `C_ell`.

## 4. Exact and schematic nonuniqueness controls

### Polarization-angle calibration

If the measured uniform rotation is

```text
alpha_observed=alpha_physical+alpha_calibration,
```

then `(1,2)` and `(2,1)` give the same observed angle. `EB/TB` sensitivity alone cannot select the
physical contribution. Current ACT DR6 birefringence work explicitly keeps angle calibration and
residual leakage in its inference, so this is an active observational—not merely philosophical—gate.

### B-mode decomposition

One total `B` amplitude can be decomposed, schematically, into source, geometric/transport, lensing,
foreground, and instrument pieces. Even the three-term exact controls

```text
(3,0,0) and (1,1,1)
```

have the same total. This is a schematic algebraic sanity check, not an independent proof of the
physical `BB` decomposition. The physical nonuniqueness is supported externally by multicomponent
BICEP/Keck, Planck, and ACT analyses. Thus nonzero `BB` is not a unique holonomy signature.
Multi-frequency maps, calibration, delensing/foreground controls, and a native source law remain
required.

## 5. Mechanical observable chain

The dependency graph is not one closed line. Two parallel early inputs meet at screen transport:

```text
selected complete coframe extension ---------+
                                               -> typed geometric screen transport
physical observer/event/path/screen domain --+

typed geometric screen transport ------------+
native physical polarization carrier --------+ -> native source/propagation -> native global Q/U sky
native matter interaction/source -------------+

native global Q/U sky -> mathematical E/B or correlations -> native statistical prediction
observed external Q/U maps -> same mathematical transforms -> calibrated multi-frequency comparison.
```

The complete-coframe atlas is classified but no member is selected. The physical observer/path/
screen variation domain is also open. Screen transport exists conditionally after those inputs.
The carrier and native source are independently open. Therefore there is no current same-branch
UDT-to-CMB prediction chain.

## 6. Complete atlas outcome

All twelve observable types receive all fourteen gates (`168` cells), and every one of the twelve
extension rows is crossed with all twelve observables (`144` cells).

- E01 is incomplete for a physical screen action.
- E02–E05 and E09 have only pointwise upstream geometric potential; local-Lorentz descent, path
  action, and global sky behavior remain open.
- E06 is only a conditional pointwise spectator control.
- E07 and E08 are pointwise counterfamily controls demonstrating that non-spectator angular and
  mixing behavior remains possible.
- E10 is inactive because strong local CSN is not active authority.
- E11 leaves local-Lorentz physical descent open.
- E12 leaves path, profile, boundary, and global sky completion open.
- All isotropically compressed spectra remain downstream-blocked by source/statistical dependence
  and directional information loss.

Capability is not prediction. No cell selects an extension or supplies a carrier/source.

## 7. Ranked future discriminator types

The ranking concerns information retained after the native chain exists; it is not evidence for a
present UDT effect.

1. `O09/O10/O11`: position-dependent rotation, off-diagonal covariance, and full unaveraged
   pair-/orientation-dependent real-space spin correlations retain the most direct path, screen,
   direction, and holonomy information. Isotropically binned `xi(theta)` is compressed and does not
   share this advantage.
2. `O01/O02/O03/O12`: map-level `Q/U`, `E/B`, and multi-frequency consistency retain much more
   structure than spectra but require global basis, carrier, and calibration control.
3. `O07/O08/O05`: `TB`, `EB`, and `BB` are sensitive but degenerate with source physics, lensing,
   foregrounds, leakage, and angle calibration.
4. `O04/O06`: detailed `EE` and `TE` peaks are powerful late consilience tests but depend strongly
   on a native source, matter interaction, and history that UDT does not yet possess.

Thus CMB polarization is a promising future guidepost. The complex power spectra are not currently
an input capable of closing the complete-coframe selector.

## 8. Smallest honest next object

The CMB audit does not replace the current metric-led task. The first required geometric objects
remain:

```text
active UDT-authoritative complete-extension selector with transition semantics,
physical observer/event/path/screen variation domain.
```

Only after those exist can UDT ask whether its metric supplies a native physical polarization
carrier/propagation law. A preregistered observable contract can then compare rotation,
off-diagonal covariance, and real-space spin correlations without fitting the selector to the sky.
