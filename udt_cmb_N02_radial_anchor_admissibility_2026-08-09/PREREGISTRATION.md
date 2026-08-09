# N02 radial-anchor admissibility — preregistration

Date: 2026-08-09
Mode: bounded CPU `MAP/DERIVE`; design and endpoint audit only
Base: `9fc8ab412612d907172e945573468b69c01f2659`

## Whole question

Does the banked conditional profile evidence supply any honest round/C1 radial and endpoint family
that can later anchor a low-basis convergence census without selecting a desired screen, boundary,
or spectrum? Determine this before writing or running an eigensolver.

This is metric-led admissibility work. It may derive center and wall asymptotics of the already-
conditional C1 scalar matrix expression. It may not select C1, a physical profile, a self-adjoint
extension, a mode, or an observationally useful result.

## Frozen candidate universe

All candidates use `u=1-r`, `0<=r<1`, and the data-conditioned but unselected P1 family
`A=u^n`, with the complete frozen exponent grid

```text
1/n = {0.9658, 0.9470, 0.9284},
q/qcrit = {-2,-1,0,0.25,0.50,0.75,0.95},
qcrit=(2-n)/2.
```

No candidate is ranked by spectral or CMB merit.

1. `R0_ROUND`: conditional C2 control `h=0`, all three `n` values.
2. `R1_CENTER_REGULAR_C1`: `h=hbar r^2 u^q`, every registered `n,q` pair and every nonzero
   `hbar={0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.5,1}`. Magnitudes are retained as
   `free-and-explored`; exponent/endpoint strata may be classified family-wise only where the
   algebra proves magnitude-independence.
3. `R2_RA1_LITERAL_LINEAGE`: `h=h0 u^q`, retained as a provenance/control family because it occurs
   in RA1 lineage. It must pass complete C1 center regularity before it can enter any radial solve.
4. Wall labels `D` and `N` from corrected FD1 are candidate external controls only. Neither is a
   physical selection, and neither may be inherited from C0 without a C1 endpoint-domain proof.

The regular C1 center, the ideal wall/asymptote, both parities, `|m|=0..3`, and all N01 matrix terms
remain in scope. No radial truncation size, frequency, or harmonic cutoff is chosen in this audit.

## Required classifications

Every candidate family/stratum receives exactly one execution disposition:

- `ADMISSIBLE_CONTROL_FAMILY_NO_PHYSICAL_SELECTION`;
- `REQUIRES_FREE_EXTENSION_CENSUS`;
- `UNIQUE_ENDPOINT_DOMAIN_DERIVED`;
- `BLOCKED_C1_CENTER_REGULARITY`;
- `BLOCKED_C1_ENDPOINT_CLASSIFICATION`;
- `BLOCKED_PROFILE_PROVENANCE_OR_JOIN`.

The independent axes `profile provenance`, `center regularity`, `wall endpoint character`,
`boundary ownership`, and `later numerical convergence safety` must not be collapsed.

## Premise ledger

| input | status |
|---|---|
| C1/C2 metrics and N01 matrix equation | `CHOSE` conditional representatives; equation derived inside them |
| scalar `Box_g` | `CHOSE` diagnostic, not native UDT dynamics |
| P1 `A=u^n` and three `n` values | data-conditioned `CHOSE/OBSERVED`, not a native profile law |
| `h=hbar r^2 u^q` grid | banked `free-and-explored` conditional family |
| RA1 literal `h=h0 u^q` | lineage control; complete-C1 regularity unproved at registration |
| regular center | `pinned-by-THEORY` only where derived from the complete C1 expression |
| wall/asymptotic domain | `OPEN`; must be classified from C1, not inherited from C0 |
| D/N labels | `free-and-explored` external boundary representatives only if mathematically admitted |
| basis sizes, eigenfrequencies, data | excluded |

## Certification and falsification contract

1. Freeze and verify all source hashes at the preregistration commit.
2. Reproduce the exact `B=h^2/(Ar^2)` exponent strata for every registered `(n,q)` row.
3. Derive complete-C1 center behavior. A nonzero-mixing profile cannot be solve-admissible merely
   because it was legal in the equatorial C0 slice.
4. Derive the matrix coefficient scalings at the wall for `B->0`, finite nonzero `B`, and
   `B->infinity`. Do not assume the C0 Weyl classification transfers.
5. State whether endpoint ownership is uniform across retained `m`, parity, harmonic directions,
   and frequency-polynomial terms. Any unclosed dependence blocks an eigensolve but remains a
   characterized branch.
6. D and N may both survive as free control extensions only if the C1 domain admits them. A
   limit-point/unique endpoint must not receive an invented boundary condition.
7. Do not choose an anchor row, wall, `m`, parity, `ell`, or basis size by spectral resemblance or
   computational convenience.
8. Fail-closed catches must reject: missing candidate rows; C0-to-C1 wall inheritance; RA1 literal
   center promotion; D or N physical selection; omitted `B` stratum; profile postselection;
   eigensolve authorization; C1 or scalar-probe promotion; and FD2/GPU/data authorization.

## Maximum allowed conclusion and stop boundary

The maximum conclusion is an independently verified admissibility/design map. It may authorize a
future, separately preregistered **control-family convergence census** only if profile and endpoint
ownership are complete without postselection. It cannot authorize a physical spectrum or boundary.

Stop after the classification tables, exact asymptotic derivation, independent verifier, premise
audit, reports, hashes, commit, and push. Do not write or run an eigensolver; do not launch FD2,
GPU work, source/population/polarization work, or data comparison.
