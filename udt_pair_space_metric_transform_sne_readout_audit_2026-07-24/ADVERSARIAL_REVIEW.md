# Adversarial review

## Strongest overclaim challenge

The tempting conclusion is that the SNe preference for
`d_L/X=z(z+2)` selects the exponential pair-distance transform.

That conclusion is false. The scored WR-L quantity uses
`r/X=1-exp(-2phi)` as areal distance. The registered WR-L proper radial
distance is `D_prop/(2X)=1-exp(-phi)`. The two are different metric readouts.

## Countermodel to profile uniqueness

For any supplied metric `d`, each of

```text
X tanh(kappa d),
X[1-exp(-kappa d)],
X(2/pi)atan(sinh(2kappa d))
```

is a bounded metric. Therefore boundedness, symmetry, and the triangle
inequality do not select one profile.

## Countermodel to local-length interpretation

For every accepted strictly concave profile and every positive `s`,

```text
2 f(s/2) > f(s).
```

The sum of transformed half-segments exceeds the transformed endpoint
distance. The pair metric is not generally the length of the subdivided
curve.

## Data firewall challenge

B19, FC12, WR-L proper distance, and the temporal-phi family have no complete
registered SNe clock/areal/optical readout. Assigning them a score would add
the missing physics through the comparison itself. They are retained as open,
not declared observational failures.

## Independence caveat

The exact profile algebra was checked with SymPy and separately with
standard-library numerical evaluations. The covariance score was evaluated
with SciPy Cholesky and separately with NumPy direct solves. This is
implementation independence, not a fresh isolated model-family audit.
Accordingly the grade is `VERIFIED-WITH-CAVEATS`, not canon or settled
physics.
