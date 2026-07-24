# Dual-systole global transport audit

Date: 2026-07-24

Base: `7feec2b301de9c9626aaac4b513268e7c8ec165a`

Preregistration: `a99096e34ed5df16873d9a5b7f5a4e4cc8429652`

Mode: CPU-only, metric-led, exact continuous algebra plus independent controls

## Result first

The parent atlas's sampled shortest-character candidate is now classified
over the **complete continuous local angular-metric shape space**.

Where an integral torus lattice exists, the complete metric derives a global
set-valued invariant

```text
W_min(H)=argmin {w^T H^-1 w : primitive w in Z^2}/(w~-w).
```

Its chamber complex is exact:

- every independent pair tied for shortest is unimodular;
- every admissible wall is a `GL(2,Z)` image of one standard wall segment;
- a wall interior has exactly two shortest unoriented lines;
- a wall vertex has exactly three;
- no point has four or more.

A unique unoriented character line exists only on tie-free toric branches.
Its projected connection is covariant, but its sign, phase section, and
physical use remain `OPEN`.

The exact shear-free reciprocal path necessarily changes from one primitive
character to the reciprocal one through a two-way tie at `phi=0`. The metric
therefore does **not** give a unique metric-only phase continuation through
that seal. This is a derived obstruction and useful selection datum, not a
physical failure or an adopted carrier.

## Exact derivation

The angular metric is mapped bijectively to the upper half-plane by

```text
tau = shear exp(phi) + i exp(2 phi).
```

For `w=(p,q)`,

```text
L_w = |p tau-q|^2/Im(tau).
```

The equality locus for `w=(p,q)` and `v=(r,u)` is

```text
(p^2-r^2)(x^2+y^2)-2x(pq-ru)+(q^2-u^2)=0.
```

The determinant/Hermite argument in `EXACT_DERIVATION.md` proves that every
independent co-shortest pair has determinant magnitude one. In its basis,

```text
Q = [[L,B],[B,L]],
L^2-B^2=1,
|B|<=L/2.
```

Thus the standard wall is

```text
x^2+y^2=1, |x|<=1/2, y>0,
```

with three-way vertices at `x=+/-1/2`, `y=sqrt(3)/2`.

## Global transport through the registered completions

All twelve registered completion classes were classified exactly once in
`GLOBAL_TRANSPORT_ATLAS.tsv`; none was preferred or filtered.

- Boundary and one-cap cases require boundary/cap data.
- Dependent two-cap cases can retain a residual circle, subject to holonomy.
- Two independent unimodular caps admit no nonzero character annihilating
  both collapsed cycles; a phase alone cannot globalize without amplitude
  vanishing or patching.
- Lens/orbifold cases impose quotient or stabilizer compatibility.
- Periodic torus bundles retain the set-valued invariant, while a unique
  line requires a tie-free monodromy-preserved sub-local-system.
- Mirror and nonorientable cases can exchange or conjugate a line.
- Rank loss terminates the object.
- A nonintegrable plane distribution supplies no global integral torus
  character lattice.
- The reciprocal diagonal crosses a selector wall exactly.

These are completion-scoped mathematical rulings. They do not select a
completion or physical phase.

## Verification

Production:

- 16 frozen source hashes matched;
- 14 continuous analytic objects classified;
- 5 exact standard-wall controls passed;
- 6 `GL(2,Z)` covariance controls passed;
- 3 reciprocal-diagonal segments classified;
- 12/12 completion classes covered.

Independent standard-library implementation:

- did not import the production module;
- inverted the metric chart at 35 deterministic points;
- repeated lattice enumeration to coefficient bound 50 with a positive
  exterior lower bound;
- checked 9 reduced-wall points;
- reproduced all 6 `GL(2,Z)` shortest-set transformations;
- checked projected-connection covariance with exact fractions;
- reproduced all 12 completion identities;
- rejected all 16 injected failure cases.

Repository and frozen-evidence gates are recorded separately in
`REPOSITORY_GATES.json`.

## Premise and authority audit

The local angular metric and its integral character lattice are distinct
inputs. The latter is `CONDITIONAL` and is asserted only on genuinely toric
regions. Identifying `w` with `-w` is a mathematical line convention, not an
orientation or physical phase.

No registered use of Reciprocity, CSN, finite-cell structure, or bootstrap
currently breaks the tie or promotes shortestness into physical selection.
No external field equation, round-`S^2` carrier, `L2+L4` action, density
law, matter source, mass rule, or GPU result entered the derivation.

## Honest scientific grade

`DERIVED`:

- the complete continuous dual-systole chamber/wall/vertex complex;
- pair unimodularity and tie multiplicity at most three;
- `GL(2,Z)` covariance of the set and projected connection;
- local constancy on tie-free branches;
- the reciprocal diagonal's mandatory tie crossing.

`CONDITIONAL`:

- a global unique unoriented line on a tie-free toric branch preserved by
  monodromy.

`OPEN`:

- sign/orientation;
- phase section and boundary framing;
- physical selection of the shortest character;
- any density-to-geometry or bootstrap rule;
- carrier, action, source, boundary completion, mass, and matter.

Nothing in this package is canonized.
