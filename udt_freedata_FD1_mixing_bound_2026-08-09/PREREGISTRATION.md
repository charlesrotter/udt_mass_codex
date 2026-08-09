# FD1 preregistration — invariant mixing bound and ladder/multiplet compatibility

Date: 2026-08-09  
Branch: `grok`  
Mode: `OBSERVE`, data-conditioned in Phase 2  
Parent: `udt_freedata_inventory_MAP_2026-08-09.md`, CP1–CP4 accepted by Charles

## 1. Whole question

On the already declared RA1/RA2 scalar-probe realization, and across the SNe-supported P1 shape
interval, characterize how the complete `m=0,+1,-1` mode family changes as the mixing realization is
varied. Determine whether any open sampled region simultaneously:

1. remains in RA1's mixing-created limit-circle ladder class;
2. retains RA2-level dimensionless peak-position shape after the same two-parameter scale/offset
   comparison used in RA2;
3. makes the `+1/-1` splitting smaller than the published TT peak basins; and
4. keeps both `|m|=1` components inside the corresponding `m=0` peak basin, without assuming their
   source weights vanish.

The primary physical readout is the dimensionless multiplet geometry, especially

```text
eta_k = |omega_k(+1)-omega_k(-1)| / mean(omega_k(+1),omega_k(-1)).
```

Any bound on the coordinate coefficient `h0` is secondary and conditional on the RA1 areal/lock
realization. No claim that `h0` itself is an invariant `mu` is permitted.

## 2. Question type and maximum interpretation

This is metric-led background characterization with a deliberately data-conditioned observational
readout. It is not a blind CMB prediction and not a search for a desired bump, particle, action,
source, or excitation mechanism.

A compatible region would be only an `OBSERVED COMPATIBILITY WINDOW` in the declared probe/slice.
An incompatibility would mean that background mixing alone does not remove the RA2 multiplet
problem in this slice; it would leave source/population structure open rather than refuting UDT or
the metric.

## 3. Frozen premise ledger

| ID | premise | status |
|---|---|---|
| P1 | `ds^2=-A dt^2+dr^2/A+r^2 dpsi^2+2h dt dpsi`, equatorial stationary 3D, areal/lock chart | `CHOSE` RA1 declared slice; SS9 tag travels |
| P2 | `A=(1-r/R_w)^n` | data-conditioned `CHOSE` P1 family; not a native profile law |
| P3 | `inv_n=0.947 [0.9284,0.9658]`, `X_eff=2086.0 [2059.1,2113.2] Mpc`, `R_w=n X_eff` | banked SNe `OBSERVED` lead; anchor/redshift-column caveats travel |
| P4 | `h=h0 (r/R_w)^2 (1-r/R_w)^q` | `free-and-explored` within RA2's registered center-regular completion class |
| P5 | `h0/R_w>0`; sign reversal by `psi->-psi` | `DERIVED` convention; zero retained only as a limiting control |
| P6 | scalar `Box_g Psi=0` | `CHOSE` metric-native probe, not the native UDT dynamics |
| P7 | real frequency; `m=0,+1,-1`; regular center branch | `CHOSE` mode slice plus RA1 center regularity; complex modes/full sphere open |
| P8 | Dirichlet and Neumann wall representatives | two `free-and-explored` anchors of the unselected wall datum; the full Robin circle remains open |
| P9 | Planck 2018 Results I published TT peak/trough locations | external `OBSERVED` readout, opened only in Phase 2; no LCDM parameter enters |
| P10 | one fitted scale plus one fitted offset in the position comparison | inherited RA2 comparison convention; both freedoms counted |
| P11 | `R_w=1`, `c=1` in computation | unit choice; all reported primary tests dimensionless |
| P12 | no source weights assigned | deliberate background-only test; every `m=0,+/-1` component is carried geometrically |

Strong CSN, an action, carrier, matter source, field statistics, peak heights, absolute amplitude,
polarization, and a native mode-population law are not used.

## 4. Frozen parameter census

### SNe shape samples

Use the exact three banked `inv_n` values `{0.9658, 0.9470, 0.9284}` and transform by `n=1/inv_n`.
`X_eff` and `R_w` are carried in the ledger, but the normalized spectral/multiplet tests cancel the
absolute length. This cancellation must be reported; FD1 may not claim an absolute CMB scale test.

### Mixing-shape strata

For each `n`, define `q_crit=(2-n)/2`. Carry all three qualitative strata of the mixing-created LC
region `q<q_crit`:

- divergent wall mixing: `q/q_crit = {-2,-1}`;
- bounded wall mixing: `q=0`;
- decaying wall mixing: `q/q_crit = {0.25,0.50,0.75,0.95}`.

The two negative witnesses do not exhaust the unbounded `q<0` half-line; no negative conclusion may
be generalized beyond them. Exact RA1 asymptotic classification, rather than the finite grid, covers
the full sign-stratified statement.

### Mixing magnitude

Use `hbar=h0/R_w` on the fixed grid

```text
{0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0}.
```

`hbar=0` is the derived limit control, never the leading system. If a compatibility transition lies
between grid values, bracket it by bisection without changing any classification threshold.

## 5. Phase ordering

### Phase 1 — blind geometry

Before opening any new peak-width/trough value:

1. rederive the exact radial quadratic pencil from the RA1 metric;
2. derive the exact `q=0` splitting relation and the scale-free multiplet observables;
3. compute the frozen `(n,q,hbar,wall datum)` spectral atlas for `m=0,+1,-1`;
4. save convergence and cutoff controls plus raw tables;
5. freeze and commit the Phase-1 package.

The already banked RA2 peak positions may not enter Phase 1 either; the Phase-1 script must contain
no Planck peak or trough number.

### Phase 2 — attributed observational readout

Only after the Phase-1 commit, open the same Planck 2018 Results I published TT peaks-and-troughs
table attributed by RA2. For each peak having two adjacent published troughs define

```text
B_k = min(ell_peak-ell_left_trough, ell_right_trough-ell_peak)
```

and the conservative basin-containment condition for a pair centered on the predicted `m=0` line:

```text
max(|ell_(k,+1)-ell_(k,0)|, |ell_(k,-1)-ell_(k,0)|) <= B_k.
```

This is a morphology/basin bound, not a Planck-likelihood exclusion or instrumental-resolution
claim. Edge peaks without two published adjacent troughs are reported but excluded from the primary
all-peak conjunction.

For the `m=0` position shape, fit scale and offset exactly as in RA2 and report all residuals. The
historical RA2 maximum fractional residual `3.1%` is a named comparison line, not a merit filter;
the complete residual surface is preserved.

## 6. Numerical contract

- CPU float64 workhorse; no GPU.
- Quadratic eigenvalue pencil solved without dropping the linear-in-frequency mixing term.
- Common geometric grids in `r/R_w`, center regularity applied identically to `m=+1,-1`.
- Wall cutoff chosen from the mixing crossover and repeated at 10x and 100x smaller cutoff on all
  transition candidates.
- Grid convergence at two resolutions on every reported boundary/transition witness.
- Mode association checked by eigenvector overlap or continuity, not order alone when a crossing is
  possible.
- Exact `q=0` algebra and the RA2 witness values are regression anchors, not independent evidence.
- An independent implementation must recompute every load-bearing transition before banking.

No result may be discarded for failing a desired shape. Divergence, continuum approach, crossings,
extra lines, ill-conditioning, and wall-datum sensitivity are classifications.

## 7. Preregistered classifications

- `FD1-OPEN-COMPATIBILITY-WINDOW`: an open sampled neighborhood satisfies ladder classification,
  RA2-level shape, splitting, and full multiplet containment in the declared slice.
- `FD1-SPLITTING-ONLY-WINDOW`: the `+/-1` doublet separation becomes small, but centrifugal/branch
  displacement leaves one or both components outside the `m=0` peak basin.
- `FD1-KNIFE-EDGE`: compatibility occurs only on a grid boundary or loses under convergence,
  cutoff, SNe-interval, or wall-datum variation.
- `FD1-NO-BACKGROUND-WINDOW-IN-SLICE`: no sampled intersection; source/population structure remains
  required in this slice.
- `FD1-OBSTRUCTED`: invariant interpretation, mode association, observational width definition, or
  numerical certification cannot be completed honestly.
- `FD1-MIXED`: different strata/wall data land differently; preserve the full map.

## 8. Falsifiers and anti-epicycle gates

- `F-SPLIT-ONLY`: claiming success from small `+/-1` splitting while ignoring displacement from the
  `m=0` comb fires.
- `F-H0-INVARIANT`: promoting the chart coefficient `h0` to invariant `mu` fires.
- `F-MUOFF`: deriving from `h=0` first or treating the zero limit as the physical system fires.
- `F-POPULATION`: silently setting `|m|>0` weights to zero fires.
- `F-IMPOSE`: adding or tuning a profile feature to manufacture a peak pattern fires.
- `F-RETRO`: changing grids, q strata, width definition, comparison threshold, or classifications
  after opening trough values fires.
- `F-SCOPE`: “explains/predicts CMB,” native dynamics, source closure, or full-sphere conclusions
  fire.

## 9. Completeness-map stamp

Covered: one stationary equatorial metric slice; one scalar probe; P1 backgrounds across the banked
SNe shape interval; one registered center-regular mixing class; `m=0,+/-1`; two wall-datum anchors;
static spectral geometry and a data-conditioned morphology readout.

Dropped and still capable of carrying structure: full 4D/spherical nonseparable modes, higher
`|m|`, the full Robin family, complex frequencies, time-live backgrounds, other admissible profile
families, source/statistical weights, peak heights/amplitudes, polarization, native action/source,
and the complete physical pair-depth law. This push is one tile, not CMB closure.

## 10. Certification and maximum conclusion

Before banking: frozen preregistration; Phase-1-before-width timeline; full bounded atlas preserved;
independent recomputation; two adversarial semantic/numerical reviews if available; premise audit;
`verify_current_scientific_premises.py`; full pytest; raw outputs and SHA-256 manifest.

Maximum conclusion:

```text
DATA_CONDITIONED_MULTIPLET_COMPATIBILITY_CLASSIFICATION_IN_THE_DECLARED_RA1_SCALAR_SLICE;
NO_NATIVE_CMB_SOURCE_DYNAMICS_OR_UNIQUE_BACKGROUND_PROFILE_DERIVED.
```
