# G250 preregistration — absolute-scale anchor type and ownership

Date: 2026-08-24

## Frozen question

Classify, without reading numerical outcomes, which already authorized anchor types can calibrate
the single positive homothety parameter left by G249 after a complete dimensionless history and
regular branch are supplied.

## Frozen theorem test

For `Q_ell = ell^w Q_bar` with `ell>0`:

1. if `w=0`, `Q` cannot determine `ell`;
2. if `w!=0`, `Q_bar!=0`, and a nonzero same-object observation `Q_*` has the compatible sign or
   positivity required for a real positive root, then `ell=(Q_*/Q_bar)^(1/w)` is unique;
3. a second nonzero-weight anchor is a consistency test of the supplied dimensionless history, not
   automatically a second scale parameter;
4. dimensional eligibility without a model-to-observation attachment law is insufficient for
   operational calibration.

## Frozen candidate classifications to test

- `c_E`, `phi`, redshift, clock ratios, causal cones, and normalized Jacobi shape: weight-zero or
  conversion-only; insufficient for absolute scale.
- direct proper-time/length/Jacobi/area/volume observations on a registered matched object:
  conditionally sufficient with weights `1,1,1,2,k`.
- a nonzero curvature/tidal scalar with length dimension `L^-p`: conditionally sufficient with
  weight `-p`; zero curvature is insufficient.
- `c_E` plus `G_obs`: no length monomial.
- adding mass, mass density, or energy density permits the G132/G202 length candidates, but these
  remain dimensional candidates until a lawful bridge identifies a metric quantity and any
  dimensionless proportionality.
- G236/G237 relative SNe state: insufficient because its additive release offsets remove absolute
  normalization.
- G99 `X_eff`: dimensionally capable only under its external `M_B`, P1, and imported-transfer
  conditions; historical conditional cross-check, forbidden as native G249 construction input.

## Certification contract

The production implementation must:

1. solve dimensional-exponent systems exactly with rational arithmetic;
2. verify homothety inversion and two-anchor consistency identities exactly;
3. emit a machine-readable candidate classification with provenance and attachment gates;
4. reject hostile mutations that promote `c_E+G_obs`, relative SNe shape, or G99 to native scale
   owners, or that erase same-object placement and nonzero conditions;
5. read no observational outcome artifact and import no protected or forbidden package.

An independent implementation must rebuild the exponent and weight classifications without
importing production code or production output.

## Falsification

The proposed landing fails if:

- any weight-zero candidate uniquely fixes `ell`;
- `c_E` and `G_obs` alone admit a mass-neutral length monomial;
- any preregistered direct nonzero-weight matched anchor fails to fix the one-dimensional scale;
- the same scale cannot be checked consistently by a second anchor;
- a candidate is declared operationally sufficient using dimensions alone;
- the conclusion requires an observational value, fitted coefficient, source law, history choice,
  or forbidden input.

## Maximum conclusion

At most: one registered nonzero-weight direct metric anchor conditionally calibrates the single
G249 scale; additional independent anchors test the supplied dimensionless history. Current
`c_E`, `G_obs`, and relative SNe information do not by themselves close it. Composite mass or
density scales and G99 remain conditional rather than native. No scale value or history is selected.
