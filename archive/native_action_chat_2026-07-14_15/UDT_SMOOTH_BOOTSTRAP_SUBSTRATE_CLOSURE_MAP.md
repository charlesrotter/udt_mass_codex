# UDT smooth bootstrap-substrate closure — frozen derivation map

## Hygiene

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Mode | Analytic global-substrate closure; DATA-BLIND |
| Immediate predecessor | `UDT_BOOTSTRAP_BACKGROUND_CARRIER_COUPLING_DERIVATION_RESULTS.md` |
| Macro firewall | WR-L remains DERIVED in the separate macro/readout lane; it is not overwritten |
| Substrate branch | Static reciprocal spherical, smooth center, universal endpoint, conditional metric-only `C^2` action |
| Empirical densities | Not loaded; first derive the geometric source-like profile and normalization |
| GPU | Not authorized; exact minimizer and operator first |
| Banking | None; `LIVE.md` and `CANON.md` untouched |

## 1. Question

Can the pre-matter bootstrap background be selected uniquely by the already derived conditional
metric action, global endpoint `X`, and smoothness—so that the density-like reciprocal-depth profile
is an output rather than a postulate?

## 2. Functional and domain

Use

\[
I[A]=\int_0^Xdr\,\frac{W[A]^2}{r^2},
\qquad
W[A]=r^2A''-2rA'+2(A-1),
\]

with

\[
A(0)=1,
\qquad A'(0)=0,
\qquad A(X)=0,
\]

and sufficient regularity for the radial Cartesian metric to be smooth at the seat and `I` finite.

These are a candidate **global substrate** conditions, not a revision of the exact residual WR-L
macro conditions.

## 3. Pre-registered tests

### T1. Positivity and zero-action set

Prove `I>=0`. Solve `W=0` completely and determine whether the three substrate conditions leave one
or several zero-action configurations.

### T2. Full-equation check

Check the selected zero-action configuration against the unrestricted Bach constraint already
derived for the reciprocal spherical family. Do not rely only on the reduced minimum.

### T3. Reciprocal flux

Define the metric identity

\[
q=A^{-1},
\qquad
J_q=\frac{q'}{q^2}=-A'.
\]

Compute

\[
\mathcal D_q=\frac1{r^2}\frac{d}{dr}(r^2J_q).
\]

Determine whether `D_q` is uniform and whether its normalization follows from `X`.

### T4. Counterprofile sieve

Use

\[
A_m=1-(r/X)^m
\]

to distinguish what is forced by endpoint/smoothness, what is selected by `C^2`, and what would
require a separate uniform-density premise.

### T5. Carrier bridge

Insert the selected `q` into the exact background-derived coefficients

\[
K_\parallel=\frac{2(q-1)}{3q}J_q',
\qquad
c_\parallel=\frac{4(q-1)^2}{3q^2}.
\]

Audit signs, dimensions, and the formal three-dimensional scale balance.

### T6. Ontology and lane discipline

State explicitly whether the smooth configuration is:

- a replacement for WR-L;
- a particle core;
- or a candidate pre-matter/global substrate on which the separate carrier lane lives.

Only the third interpretation is tested here.

## 4. Acceptance gates

- No declaration that `D_q` is physical mass density without a normalized charge law.
- No Standard Model or observed density values in selecting `A`.
- No merger of the macro and particle lanes.
- No stable-soliton claim without the full 3D carrier, topology, backreaction, and raw stability
  calculation.
- A zero-action minimum must still pass the full tensor equation.

## 5. Possible verdicts

1. **SMOOTH BOOTSTRAP SUBSTRATE SELECTED:** one smooth fixed-endpoint minimum exists and supplies a
   coefficient-free background carrier coupling.
2. **SUBSTRATE MODULUS REMAINS:** several smooth minima survive.
3. **REDUCED/FULL EQUATION CONFLICT:** the minimum fails unrestricted variation.
4. **CLOSURE UNRESOLVED:** regularity or endpoint assumptions are inconsistent.
