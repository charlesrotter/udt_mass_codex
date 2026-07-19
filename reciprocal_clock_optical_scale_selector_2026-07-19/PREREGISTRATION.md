# Reciprocal Clock–Optical–Scale Selector — Preregistration

Date: 2026-07-19  
Branch: `codex/reciprocal-clock-optical-scale-selector-2026-07-19`  
Base: `2092a047da4b1267eabdb6be59e5b50b41e3db62`

## Scope and authority

This isolated CPU-only derivation tests the owner's hypothesis that UDT agrees with ordinary GR-like clock flow across terrestrial and solar scales, while relational dilation changes the effective optical speed at extremely small and cosmological scales. It also tests the proposed identification of cosmological time dilation, redshift, apparent mass increase, and effective light-speed change.

No canonization, GPU work, repository reorganization, artifact movement, `grok` integration, new action, matter source, carrier coupling, or numerical fit is authorized.

The July-1 provenance firewall remains binding. Affirmative UDT physics may come only from the post-firewall foundation and adjudication chain. The original dirty checkout is metadata-only and its dirty file contents must not be read.

## Exact question

Given a static radial metric decomposition

\[
ds^2=-N^2c_0^2dt^2+B^2dr^2,
\]

which relations among clock rate, ruler dilation, static redshift, coordinate null slope, optical travel, and energy/mass readouts are mathematically derived? Which additional relations are selected by UDT Reciprocity (`NB=1`), and can a relational scale variable replace coordinate position without adding unregistered structure?

## Registered hypothesis classes

### J0 — general clock/ruler decomposition

Keep `N` and `B` independent. This class tests whether time dilation by itself determines coordinate light speed or optical distance.

### J1 — UDT reciprocal static block

Impose the already conditional reciprocal representative

\[
N=e^{-\phi},\qquad B=e^{+\phi},\qquad NB=1.
\]

Test the exact redshift, coordinate-slope, and optical-stretch relations. This is not permission to promote the metric representative into a universal observer, line, action, or material-coupling theorem.

### J2 — time-only and common-scale countermodels

Compare:

- time-only dilation: `B=1`;
- common conformal dilation: `B=N`;
- reciprocal dilation: `B=1/N`.

These must show whether the phrase “time dilation and effective speed are the same thing” is universal, conditional, or false.

### J3 — operational energy and mass readings

Separate local invariant rest mass, local Compton frequency, Killing/coordinate energy, received photon energy, inferred mass parameters, and any native UDT mass. No mass increase may be asserted without an explicit operational definition and coupling/dynamics.

### J4 — relational-scale realization

Introduce a provisional resolution/separation label `ell`, distinct from coordinate position `r`, and test only the kinematic consequences of a scale-indexed `phi(ell)`:

- GR-like plateau: `phi(ell) approximately 0` over ordinary scales;
- UV branch: `phi(ell)<0`, if apparent optical speed exceeds `c0`;
- IR branch: `phi(ell)>0`, if apparent optical speed falls below `c0`;
- optional dual-scale rule `phi(ell_dual)=-phi(ell)`.

The derivation must state whether `g(x;ell)`, a bilocal object, or coarse-grained metric is required. It must not silently treat scale dependence as an ordinary scalar field on spacetime.

### J5 — one-sided fallback

If no UV speedup is selected, test the branch `c_eff<=c0`. In that branch `c0` is a speed ceiling, while unity may be the floor of optical stretch/slowness. Terminology must be corrected explicitly.

## Registered outcomes

Exactly one top-level outcome must be returned:

1. `TIME_DILATION_UNIVERSALLY_IDENTICAL_TO_EFFECTIVE_LIGHT_SPEED`
2. `RECIPROCAL_CLOCK_OPTICAL_LINK_DERIVED_SCALE_REALIZATION_AND_MASS_OPEN`
3. `CLOCK_AND_OPTICAL_EFFECTS_INDEPENDENT_IN_REGISTERED_CLASSES`
4. `OPEN_IN_REGISTERED_CLASSES`
5. `INCONSISTENT_IN_REGISTERED_CLASSES`

The expected but not forced result is outcome 2.

## Required derivations

1. Derive `d tau=N dt`, `d ell=B dr`, and `dr/dt=c0 N/B` for metric-null curves.
2. Derive the static Killing-frequency redshift between emitter and observer.
3. Relate the coordinate-slope ratio to the redshift ratio for general `N,B`.
4. Under `NB=1`, test whether the slope ratio is the inverse square of `1+z` and whether optical stretch is its square.
5. Show explicitly that time-only, common-scale, and reciprocal ruler responses produce different coordinate slopes for the same clock factor.
6. Audit invariance under radial reparameterization, time/Killing normalization, and CSN rescaling preserving the static flow.
7. Separate local rest mass from photon/Killing energy and any remotely inferred mass.
8. Determine the minimum new structure required for `phi(ell)` at fixed spacetime event.
9. Test a broad ordinary-scale plateau without selecting its thresholds or fitting data.
10. Test dual-scale Reciprocity without inventing a preferred pivot scale.
11. State the no-signalling and universal-coupling obligations of a UV `c_eff>c0` branch.
12. Preserve all existing open action, source, carrier, boundary, CMB, wall, and time-live conclusions.

## Required catch-proofs

The verifier must reject at least:

- deriving coordinate speed from `N` without specifying `B`;
- calling coordinate speed a scalar or a locally measured varying constant;
- claiming common conformal dilation changes the null slope;
- missing the reciprocal square relation;
- treating redshift and coordinate speed as numerically identical rather than linked observables;
- treating local rest mass as increased by static redshift;
- calling Killing/received energy a native mass derivation;
- identifying coordinate position `r` with resolution scale `ell`;
- representing genuine probe-scale-dependent cones with an ordinary single local metric without explanation;
- selecting a UV/IR pivot or plateau thresholds from convention;
- authorizing observable superluminal signalling;
- treating `c0` as a speed floor in the one-sided `c_eff<=c0` branch;
- promoting static results to the CMB, time-live cosmology, action, source, carrier, substrate, or recycling dynamics;
- mutating frozen packages, navigation registries, or dirty-checkout contents.

## Verification and stop conditions

- Use exact runnable algebra with `sympy==1.13.1` in an isolated CPU dependency environment.
- Add an independent fail-closed verifier and two fresh read-only adversarial reviews.
- Replay six frozen manifests, current-path/frontier/link gates, the documented test baseline, and the 54-path dirty metadata gate.
- Freeze, hash, commit, and push only this isolated branch.
- Stop before data fitting, action construction, scale-threshold selection, GPU work, canonization, `grok` integration, or substrate/recycling continuation.
