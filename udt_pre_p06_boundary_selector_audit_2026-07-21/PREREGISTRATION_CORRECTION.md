# Preregistration correction before derivation

Date: 2026-07-21

The initial preregistration commit `3048b1d` transcribed the wrong manifest hash for
`c2_finite_cell_boundary_variation_2026-07-20/SHA256SUMS.txt`.

- initially transcribed: `848db01c3524a45f15854228549d45dac4ac7b10cd07aa06924dffd406b3c9d4`
- independently observed: `2be362cd50cc5102960cb6a1e8745196cad956799b851c3e71a212b01d70d83e`

`848db...` belongs to `c2_rigidity_three_route_zoomout_2026-07-20`, not the boundary-variation
package. The parent path, candidate universe, outcome classes, falsification contract, and maximum
conclusion are unchanged. This correction is recorded before any new outcome algebra or generated
classification tables.
