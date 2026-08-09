# FD2 preregistration — background-profile response and joint CMB/SNe readout

Date: 2026-08-09  
Branch: `grok`  
Parent HEAD at registration: `7c9ff2fe8c27e674e6e6d32021004d2f3a2d4cbf`  
Mode: `MAP -> OBSERVE`; CPU only; no `LIVE.md` or `CANON.md` edit authorized

## 1. Whole question and bounded slice

Question: in the already declared RA1/FD1 stationary equatorial scalar-probe slice, what
first-order and directly recomputed changes in the seven `m=0` cavity frequencies are produced by
generic localized perturbations of the radial profile `A(r)`? After the response surface is frozen,
does any such profile requirement reduce the attributed Planck TT peak-position residual pattern,
and what does the same profile do to the previously registered Pantheon+ SNe readout?

This is a **data-conditioned inversion and compatibility audit**, not a prediction and not an
explanation of the CMB. It characterizes background freedom already left open by the fitted P1
profile. It does not add a source, matter law, carrier, action, coupling, population law, or
boundary completion.

Bounded metric/probe slice:

```text
ds^2 = -A dt^2 + dr^2/A + r^2 dpsi^2 + 2 h dt dpsi,
h = hbar r^2 (1-r)^q,
Box_g Psi = 0,
Psi = R(r) exp[i(m psi - omega t)],
R_w = c = 1 in the mode computation.
```

The four FD1 strict-interior background realizations are all carried:

| q/qcrit | wall | hbar |
|---:|:---:|---:|
| 0.75 | D | 0.01 |
| 0.75 | N | 0.01 |
| 0.95 | D | 0.5 |
| 0.95 | N | 0.5 |

The blind response atlas uses central `1/n=0.9470`. Direct verification repeats the selected
numerical-validation set at all three registered SNe-conditioned values
`1/n={0.9658,0.9470,0.9284}`. This is one bounded continuation tile, not the complete UDT metric.

## 2. Profile family frozen before the response is inspected

Write `s=r/R_w`, `u=1-s`, and perturb the P1 profile multiplicatively:

```text
A_c(s) = u^n exp[c B(s)].
```

`B` is selected from two generic compactly supported motif classes. Neither class is designed from
the TT residual signs.

1. `BUMP`: the normalized C-infinity compact bump
   `exp(1-1/(1-xi^2))` for `|xi|<1`, zero otherwise.
2. `DIPOLE`: `xi` times the same compact bump, normalized to unit maximum absolute value. This is a
   compensated/sign-changing first wavelet companion to `BUMP`.

Here `xi=(s-center)/halfwidth`. Every motif vanishes with all derivatives at its support boundary,
so the observer anchor `A(0)=1`, the wall `A(1)=0`, and the leading wall exponent `n` remain
unchanged. The exact frozen grid is:

| halfwidth | centers |
|---:|---|
| 0.025 | 0.05, 0.10, ..., 0.95 |
| 0.05 | 0.10, 0.20, ..., 0.90 |
| 0.10 | 0.20, 0.30, ..., 0.80 |
| 0.20 | 0.30, 0.40, ..., 0.70 |

This is 40 supports x 2 motif classes x 4 backgrounds = 320 response rows per grid. Both signs are
represented by the fitted coefficient `c`; no sign is preferred. Profile monotonicity is a reported
property, not an outcome filter. A non-monotone profile remains in the census and is classified as
having a multivalued single-branch SNe readout under the registered inversion dictionary.

## 3. Phase I — blind metric response

Phase I must contain no Planck peak/trough values and load no SNe magnitudes. For every row it will
compute the first seven `m=0` frequencies at `c=0`, `+delta`, `-delta`, `+delta/2`, and `-delta/2`,
with `delta=1e-4`. The centered derivative

```text
J_k = [omega_k(+delta)-omega_k(-delta)]/(2 delta)
```

is compared with its half-step counterpart. All rows are retained. Production grids are 180 and
240 nodes. Raw generalized-eigenproblem backward residual, mode ordering, zero-perturbation
agreement with FD1, finite-difference step drift, and inter-grid drift are recorded.

Numerical certification gates (physics-blind):

- exactly 320 unique response rows per grid;
- seven positive ordered modes per solve;
- no nonfinite frequency or response;
- maximum raw backward residual `<1e-8`;
- zero-profile frequencies reproduce the corresponding frozen FD1 row to `<5e-4` relative;
- response rows with half-step drift above 2% or grid drift above 5% are retained but marked
  numerically unresolved and cannot carry the existence headline.

## 4. Phase II — attributed TT inversion

Only after both Phase-I atlases and their hashes are committed may Phase II load the same attributed
Planck 2018 Results I Table 5 TT peak positions and diagonal one-sigma values used by FD1:

```text
ell = [220.6, 538.1, 809.8, 1147.8, 1446.8, 1779.0, 2075.0]
sigma = [0.6, 1.3, 1.0, 2.3, 1.6, 3.0, 8.0].
```

For each frozen response row, weighted least squares fits

```text
ell_k = a [omega_k(0) + c J_k] + b
```

with three continuous fitted freedoms `(a,b,c)`. Positive `a` is required by the registered
orientation. Both the unconstrained linear-response solution and the bounded diagnostic
`c in [-0.5,0.5]` are retained. Report diagonal chi-square, RMS and maximum fractional residual,
the required-residual/response correlation after affine projection, and the residual sign sequence.

Anti-epicycle accounting travels on every summary: the best-of-atlas choice additionally shops over
background, motif class, center, and width. Therefore even a small residual is a **required-profile
characterization**, never a parameter-poor confirmation.

Direct nonlinear verification is a preregistered numerical resource check, not an outcome filter:
for each of the four backgrounds, recompute the four lowest predicted-chi-square rows from each
motif class (eight per background; 32 total), whether good or bad. Use the bounded fitted `c`, solve
the perturbed metric directly at grids 180 and 240, and repeat at all three registered `n` values.
Recompute `m=-1,0,+1` for those rows to determine whether the FD1 low-|m| multiplet compatibility
survives; do not suppress any partner.

## 5. Phase III — independent SNe cross-anchor

For every directly recomputed profile, apply the existing metric readout, not a new cosmology:

```text
A_c(s(z)) = (1+z)^(-2),
d_L proportional to (1+z)^2 s(z).
```

Use the frozen Pantheon+ `zCMB`, `m_b_corr`, calibrator exclusion, `z>0.023` cut, and full subset
covariance. Reprofile only the additive magnitude offset, exactly as in registered shape mode A.
The CMB-inverted motif parameters are not refit to SNe. Record chi-square relative to (i) unperturbed
P1 at the same `n` and (ii) the banked best P1 `chi2=1260.8480887040496`. Descriptive cross-anchor
bands, frozen before evaluation, are `Delta chi2 <=1`, `(1,4]`, and `>4`; raw values remain primary.
Non-monotone profiles are retained as `MULTIVALUED_REGISTERED_SNE_READOUT`, not discarded.

The direct solver and SNe readout must be independently reimplemented for verification rather than
calling the production functions. Mutation catch-proofs must break a frequency, a motif identity,
an FD1 background, the mode count, the CMB target, profile monotonicity status, and the SNe offset
profiling check.

## 6. Premise ledger

| ID | choice | status |
|---|---|---|
| P1 | stationary equatorial lock-form metric | `CHOSE`; RA1/FD1 slice |
| P2 | scalar `Box_g` probe | metric-native probe `CHOSE`; not UDT dynamics |
| P3 | P1 neighborhood `A=u^n exp(cB)` | `CHOSE`; profile-characterization family |
| P4 | compact BUMP/DIPOLE menu and grid | `free-and-explored` within frozen atlas; chart-dependent |
| P5 | four FD1 backgrounds | prior independently verified conditional witnesses; not selected physics |
| P6 | D/N wall anchors | `free-and-explored`; physical boundary completion open |
| P7 | Planck Table 5 TT positions/errors | attributed `OBSERVED` readout, Phase II only |
| P8 | affine `(a,b)` projection | `CHOSE`, two fitted freedoms; offset remains load-bearing unless disproved |
| P9 | coefficient `c` | data-inverted `CHOSE`; no native profile law |
| P10 | Pantheon+ mode-A construction | prior `OBSERVED` readout with BBC/LCDM-adjacent caveat |
| P11 | profile-to-SNe dictionary | metric-readout relation from the registered P1 lane; conditional outside it |
| P12 | no source/population weights | deliberate background-only audit; no mode removed |

Not covered: full sphere, higher `|m|`, vector/tensor probes, Robin boundary circle, time-live
background response, native action/dynamics/source, peak heights, damping, polarization, field
statistics, native projection, unique profile, or a physical matter-density law.

## 7. Landings and maximum allowed conclusion

- `OPEN_BACKGROUND_PROFILE_WITNESS_IN_SLICE`: at least one numerically resolved direct profile has
  lower TT position residuals, retains all three low-|m| partners in their basins, and lies in the
  registered SNe `Delta chi2<=1` band. This means only that such background freedom exists.
- `CMB_SNE_PROFILE_TENSION_IN_SLICE`: the directly verified TT-responsive motifs all lie outside the
  registered SNe bands or lose a single-valued readout.
- `NO_SINGLE_COMPACT_MOTIF_IN_SCANNED_SLICE`: no resolved motif materially changes the alternating
  residual. This does not prove the effect source-side or exclude other profile classes.
- `NONUNIQUE_OR_NUMERICALLY_OPEN`: multiple incompatible motif requirements survive, or numerical
  response/direct recomputation fails its gates.

No landing may say UDT predicts or explains the CMB, derives matter content, selects `A(r)`, or
establishes a source, polarization channel, native action, `X_max`, or mass-density closure.

## 8. Frozen parent hashes

```text
9050e0f5a803dae0a456c2d6fc38dd87d9016dff919e77036ea2800f6c3a097c  udt_freedata_inventory_MAP_2026-08-09.md
4e303c290eca1fa66f3cfa39e7245c97f78b958e4c0ca1510c08e6dcdeaf4711  udt_roadA_RA1_muon_modes_2026-08-08/derive_ra1.py
f0249178721016d990f3cd6a6b89b2b14e91d0f003a90f62c47f92faa717060c  udt_freedata_FD1_mixing_bound_2026-08-09/derive_phase1.py
534713dea58c7a99a0b5ed149c33c08972f458d558bedb681f67c0d3f376110d  udt_freedata_FD1_mixing_bound_2026-08-09/phase1_atlas_g240.json
117b447bd0a9be7701be43a177ffd7bf184eecf8592585790c104dae5d7d5605  udt_freedata_FD1_mixing_bound_2026-08-09/phase2_comparison.json
16e189fa6925926341144d46865a70e689bcb45fe78018ef27eb22bb3b0b319b  udt_xmax_scale_observational_M2_build_2026-08-07/v_sne.py
a6b8837114cb4be10248cd6cc6803ee34642e25d25e315193a9843e853ae2211  udt_xmax_scale_observational_M3_runs_2026-08-07/sne_results.json
1cb0fc379ef066afdc2ffd1857681cc478024570d8a3eba284fb645775198cf8  Data/Pantheon+SH0ES.dat
abf806d966485e64afdb359c87bffc0ecc00d05eff0a31ced66f247385df0fdc  Data/Pantheon+SH0ES_STAT+SYS.cov
```

## 9. Four banking gates

Preregistration is this commit. Bounded scope is explicit. No verdict is banked until an independent
implementation verifies the load-bearing direct profile and SNe readout, all premises are audited,
the current-premise verifier and repository tests pass, and preserved failures are included. In the
absence of a fresh external-context review, the maximum grade remains `VERIFIED-WITH-CAVEATS`.
