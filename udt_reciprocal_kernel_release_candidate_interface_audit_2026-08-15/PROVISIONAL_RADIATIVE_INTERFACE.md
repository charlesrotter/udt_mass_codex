# Provisional observational radiative interface

Date: 2026-08-15
Status: `POSIT__CONDITIONAL__CHARLES_AUTHORIZED__NOT_UDT_DERIVED`

This interface is temporary scaffolding for observational evaluation while UDT lacks a complete
electromagnetic or particle sector. It does not modify the metric, pair evaluator, Jacobi map, or
reciprocal kernel.

On a supplied regular transparent null observer-query branch, posit:

```text
P_rad_1: eta=1
```

The physical radiative amount used in G94 is carried without absorption, scattering, creation,
loss, or exchange with another branch between the declared source and observer sections.

Also posit:

```text
P_rad_2: epsilon=1/Z
```

The received-to-emitted energy per carried unit equals the observer-measured endpoint frequency
ratio of one supplied transported null covector, as typed conditionally in G95.

Together with the G94 geometry theorem,

```text
F_o=L_Omega eta epsilon/(Z^3 d_A^2),
```

these premises imply only on the declared branch

```text
F_o=L_Omega/(Z^4 d_A^2),
d_L=Z^2 d_A
```

after source isotropy and the definition of luminosity distance are separately supplied.

These statements are not a Maxwell derivation, a photon theory, an opacity theorem, or a claim
through caustics and multiple-image aggregation. Every result using them remains conditional and
must retain this file as a load-bearing premise. A future native UDT radiation/matter law may derive,
refine, or reject either statement.
