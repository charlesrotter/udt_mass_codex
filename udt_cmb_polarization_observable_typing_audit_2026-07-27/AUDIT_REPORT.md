# CMB-polarization observable-typing audit

Date: 2026-07-27

Verdict: **VERIFIED-WITH-CAVEATS**.

```text
CMB_POLARIZATION_IS_A_PROMISING_FUTURE_GUIDEPOST;
NO_CURRENT_NATIVE_UDT_CMB_PREDICTION;
POWER_SPECTRA_ALONE_ARE_DIRECTIONALLY_INSUFFICIENT;
MAP_OFFDIAGONAL_AND_FULL_UNAVERAGED_REAL_SPACE_TYPES_RETAIN_MORE_RELEVANT_INFORMATION.
```

No extension was selected, no polarization carrier or source was imported, and no CMB fit was
performed.

## Main result

CMB polarization is scientifically relevant to the open angular/mixing extension, but only as a
future discriminator. The current metric supplies conditional screen geometry and transport after
an observer, event, path, and screen are supplied. It does **not** thereby supply physical
polarization. The native carrier, source interaction, global sky section, and native statistical or
single-sky prediction remain open.

The complete-coframe atlas also supplies only pointwise upstream geometric potential and controls.
It does not yet supply a local-Lorentz-descended path action or global sky transport. Exactly 56
extension/observable cells were corrected to this pointwise scope before banking.

Consequently no same-branch chain presently reaches an observable CMB prediction.

## Exact mathematical findings

1. The external `Q/U` pair carries a spin-two screen-basis action. Its rotation composes and
   reverses exactly.
2. `E/B` is a nonlocal global spin-harmonic decomposition, not a pair of local basis components.
3. The isotropic `C_ell` operation is noninjective. Two distinct real-harmonic coefficient vectors
   at `ell=2` give exactly the same `C_2=1/5`. It therefore discards directional and phase
   information needed to identify a generic path- or holonomy-dependent pattern.
4. A supplied uniform polarization rotation mixes `E/B`, making `EB/TB` rotation-sensitive, but an
   exact additive degeneracy remains between physical rotation and angle calibration.
5. A schematic component-sum check illustrates nonuniqueness of a total `B` amplitude; it is not an
   independent physical decomposition proof. The physical source/lensing/foreground/instrument
   degeneracy is supported by the cited external multicomponent analyses.

## Mechanical census

- `12` observable types received all `14` gates: `168` cells.
- `12` registered extension rows were crossed with all `12` observables: `144` cells.
- `56` map/directional cells are pointwise upstream potential or pointwise controls only.
- `40` isotropic-spectrum cells are downstream-blocked by native-source/statistical dependence and
  directional compression.
- E01 is incomplete; E10 is inactive; E11 descent and E12 global completion remain open in all 12
  observables.
- Every observable has the selected-extension, physical-domain, physical-carrier, native-source,
  global-sky, native-statistical-rule, unique-signature, and active-prediction gates open or
  unavailable.

The production and no-production-read implementations agree mechanically on all `312` structured
cells. Their matching status functions are a regression reconstruction, not independent semantic
authority; the fresh source-first adversarial review independently audited the meanings and forced
the pointwise-scope and dependency-layer corrections.

## Ranked guideposts

The first tier is a three-way tie by information retention, not a physical-priority claim:

1. position-dependent rotation (`O09`);
2. off-diagonal harmonic covariance (`O10`);
3. full unaveraged pair-/orientation-dependent spin correlations (`O11`).

An isotropically binned `xi(theta)` is `C_ell`-equivalent and compressed, so it does not retain the
same information as the full `O11` object.

Map-level `Q/U`, `E/B`, and multi-frequency consistency are the second tier. `TB`, `EB`, and `BB`
spectra are sensitive but highly degenerate. Detailed `EE/TE` peak phase and amplitude are powerful
late consilience tests only after UDT supplies a native matter/polarization source and history.

This ranking says which readouts preserve potentially relevant structure after the native chain is
derived. It is not a UDT prediction of rotation, anisotropy, parity violation, or any CMB anomaly.

## External-readout provenance

The external sources are used only to type observations and active systematics:

- Planck 2018 constructs likelihoods from polarization maps and spectra with polarization-efficiency,
  leakage, component-separation, noise, mask, and simulation controls.
- ACT DR6 publishes multi-frequency maps, beams, passbands, masks, spectra, covariances, and
  likelihood products; its spectrum analysis explicitly models foregrounds.
- The current ACT DR6 birefringence analysis uses `EB/TB` while carrying polarization-angle priors,
  residual leakage, and unresolved systematic caveats.
- BICEP/Keck `BB` inference is explicitly multicomponent and foreground/lensing dependent.

None of those external theories or likelihoods supplies affirmative UDT physics.

## Dependency correction

The final chain keeps evidence layers separate:

- native global `Q/U`: `OPEN`, layer `L3`;
- observed external `Q/U` maps: `OBSERVED_EXTERNAL_READOUT`, layer `L2`;
- mathematical `E/B` and spin-correlation transforms: `DEFINED_EXTERNAL_MATHEMATICAL_TYPE`, layer
  `L0`;
- native statistical or deterministic prediction: `OPEN`, layer `L3`;
- calibrated external comparison: layer `L2` and unavailable as a UDT test until the native chain
  closes.

## Next scientific boundary

This audit does not replace the current metric-led selector task. The two parallel early gates are:

```text
active UDT-authoritative complete-extension selector with transition semantics,
physical observer/event/path/screen variation domain.
```

Only afterward is it meaningful to test whether UDT supplies a native physical polarization
carrier and propagation/source law. The CMB contract should remain preregistered and dormant until
then, with map/off-diagonal/unaveraged statistics preserved before any isotropic compression.

## Evidence gates

1. **Preregistered:** yes, commit `d2da791ecb972639e6b5a964fcc4ceb557009f78`, before external-source
   inspection or outcome classification.
2. **Full space or bounded scope justified:** yes for the frozen 12 observable types, 14 gates, 12
   extension rows, and 4 evidence layers; not all future statistics, sources, foregrounds, or metric
   branches.
3. **Independently verified:** exact spin-two composition, spectrum noninjectivity, calibration
   degeneracy, matrix coverage, and status reconstruction were independently replayed; the fresh
   source-first review supplied the semantic adversary.
4. **Premises audited:** yes; observer/path/screen, extension, carrier, source, completion,
   statistics, calibration, and foreground premises remain explicit.

The audit is one observable-typing tile. It covers no action, equations, solution branch, dynamical
evolution, stability spectrum, or physical fit.
