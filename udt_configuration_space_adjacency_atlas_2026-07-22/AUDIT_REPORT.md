# UDT Configuration-Space Adjacency Atlas

Date: 2026-07-23

Status: `VERIFIED_WITH_REGISTERED_SCOPE`

Maximum conclusion:

`BOUNDED_REGISTERED_CONFIGURATION-SPACE_BANK-EDGE_ADJACENCY_CHARACTERIZED`

## Result first

The causal sectors found in the preceding phi atlas are adjacent—not disconnected—inside both
registered complete-coframe configuration charts.

The full census is:

| chart-sheet class | count |
|---|---:|
| uniformly spacelike same-sector sheet | 2,304 |
| one forced regular null graph on a cross-sector sheet | 2,304 |
| multiple graph, tangency, zero-gradient interface, causal pocket, metric degeneracy, or unresolved sheet | 0 |

These are 4,608 chart presentations of 2,304 matched endpoint pairs, not 4,608 universes. Each
endpoint pair holds the deformation vector and active mask fixed and joins one pair of registered
banks. J1 interpolates the analytic generators and coordinates; J2 interpolates the evaluated
cofields. Both retain all ten metric fields, all angular fields, all four shifts, and `dphi`.

The three spacelike banks form a constructively connected triangle along every registered matched
edge in both charts. Every edge from one of those banks to the timelike bank crosses exactly one
regular `s=0` graph, where

```text
s = g^-1(dphi,dphi).
```

Thus the earlier absence of a null point on any individual bank chord did not mean that the two
causal types occupy disconnected configuration components. A complete continuous coframe path can
join them, and on every registered cross-sector path the null separator is unavoidable.

This is configuration geometry, not a time evolution or a selected universe.

## What is exact and what is certified

Exact:

```text
det(g) = -exp(2*(a+c+d+f)) < 0
```

at every finite point in both charts. The metric never degenerates or changes Lorentzian signature.
Continuity plus opposite endpoint signs forces at least one null point. At a regular null point with
`dphi` nonzero,

```text
D = grad(phi) tensor dphi,
D^2 = s D = 0,
```

so `D` is a nonzero rank-one nilpotent endomorphism. Division by `s` remains forbidden there.

Certified over the complete registered sheets:

- all same-sector boxes have `s>0`;
- all cross-sector outer regions have the endpoint-consistent signs;
- every cross-sector root band has `partial_lambda s<0`;
- at least one component of `dphi` excludes zero throughout every certified root-band box;
- therefore every cross-sector fiber has exactly one transverse root, and the roots assemble into
  one regular graph over `u`.

The null graph's existence and multiplicity agree between J1 and J2. Its lambda location and shape
are chart-dependent. The padded certificate envelopes are proof enclosures, not measurements of a
physical transition location.

## Complete coverage

The frozen universe contains:

- 48 deformation vectors;
- eight active masks `M8` through `MF`;
- 384 matched carrier/mask groups;
- six bank pairs per group;
- 2,304 endpoint pairs;
- two charts per pair;
- 4,608 complete sheet presentations.

All were retained. The directed binary64 interval pass used outward `nextafter` rounding after every
elementary operation and the preregistered dyadic refinement ladder. The final census has zero
unresolved cells. The most adverse cell in every chart/bank-pair class was replayed at 80 decimal
digits.

A domain-boundary defect in the first unbanked implementation pass was caught: outward rounding had
been applied after clipping and could nudge a bound just outside `[0,1]`. The correction was recorded
and committed before the accepted rerun. Final evaluation bounds are outward-rounded and then
clamped to the registered closed sheet.

## Independent full-matrix route

The independent verifier does not import the production builder or reuse its inverse-coframe norm
formula. It builds the complete 4-by-4 coframe matrix, forms

```text
g = E^T diag(-1,1,1,1) E,
```

and evaluates `dphi^T g^-1 dphi`.

It independently checked:

- 195,840 same-sector matrix values;
- 11,520 cross-sector matrix roots and crossing derivatives;
- all 4,608 saved classifications;
- twelve worst-class 80-digit interval cells through
  `dphi^T adj(g) dphi / det(g)`.

Eleven high-precision cells certified directly. The exceptionally tight J2 `B1-B2` same-sector
cell certified after a complete two-box subdivision. An exercised shift-sector omission changes a
matrix probe by `7.105081822443983e-07` and is rejected; the angular/shift orchestra is therefore
present and non-vacuous.

## Structural meaning

What was learned is modest but real:

1. The registered spacelike banks are not isolated islands.
2. The registered timelike bank is not separated by metric failure.
3. In two substantially different configuration charts, the causal change occurs through a simple
   transverse null interface rather than a pocket, tangency, branching event, or degeneracy.
4. The existence of a separator is topological and chart-robust; its detailed placement is not.

This makes the null interface a genuine structural object of the bounded metric atlas. It does not
make it a particle surface, a force boundary, a clock transition, a cosmic background, or a
bootstrap-selected seam.

## What remains open

- whether the full unrestricted configuration space has the same adjacency;
- whether bank-simplex interiors contain additional components or interfaces;
- whether any complete finite-cell solution realizes one of these paths;
- whether UDT's registered premises select J1, J2, another path, or no path;
- whether the separator persists under native dynamics;
- any physical interpretation of the two causal sectors;
- the action, source, carrier, boundary completion, physical scale, and mass law.

No action, matter carrier, source, density, scale, empirical fit, `c/G` calibration, SNe data, or
physical regime label was loaded. Existing SNe and particle-lane results are unchanged. CPU only;
GPU runs: zero.

## Four banking gates

1. Preregistered: **YES**, including the numerical-method and closed-domain implementation
   corrections before the accepted full census.
2. Full space or bounded scope justified: **YES** for every matched registered bank edge in both
   charts; not exhaustive outside the frozen analytic atlas or inside the bank simplex.
3. Independently verified: **YES WITH CLAIM-SPECIFIC SCOPE** through a separately written complete
   4-by-4 matrix route, 207,360 matrix probes/roots, twelve 80-digit adjugate anchors, and exercised
   corruption catches.
4. Every premise audited: **YES** in `PREMISE_STATUS_LEDGER.tsv`; no physical selector or global
   solution is claimed.

This is verified structural evidence with a registered scope, not canonization.
