# G229 preregistration — local Lorentz-metric 3-jet realization

Date: 2026-08-23
Status: `PRE_OUTCOME__METRIC_LED__EXACT_FINITE_DIMENSIONAL`

## Frozen question

Determine whether every G227 algebraic curvature tensor `R` together with every G228
differential-Bianchi-compatible first derivative `D=nabla R` is realized by a local Lorentz-metric
3-jet in geodesic normal coordinates at one supplied event.

The result must separately classify:

1. the curvature map from the full locally inertial metric 2-jet;
2. the first-curvature-derivative map from the full locally inertial metric 3-jet;
3. the coordinate-gauge kernels of those maps;
4. the geodesic-normal-coordinate slices;
5. the conditional smooth local representative;
6. the G227/G228 null-screen and Jacobi projections.

## Frozen conventions

Use dimension four and `eta=diag(-1,1,1,1)`. Fix

```text
R^rho_(sigma mu nu)
 = partial_mu Gamma^rho_(nu sigma)
 - partial_nu Gamma^rho_(mu sigma)
 + Gamma^rho_(mu lambda) Gamma^lambda_(nu sigma)
 - Gamma^rho_(nu lambda) Gamma^lambda_(mu sigma).
```

At the origin of a locally inertial chart, `g_ab=eta_ab` and `g_ab,c=0`. Define

```text
H_ab,cd = g_ab,cd = H_ba,cd = H_ab,dc
K_ab,cde = g_ab,cde, symmetric in ab and in cde.
```

The frozen direct maps are obtained by differentiating the Christoffel definition, not by assuming
the normal-coordinate expansion:

```text
C2(H)_abcd
 = 1/2 (H_ad,bc + H_bc,ad - H_bd,ac - H_ac,bd),

C3(K)_eabcd
 = 1/2 (K_ad,bce + K_bc,ade - K_bd,ace - K_ac,bde).
```

Because `g_,c=0`, `C3(K)=partial_e R=nabla_e R` at the event.

The candidate normal-coordinate inverses to test are

```text
H^R_ab,cd = -(1/3)(R_acbd + R_adbc),

K^D_ab,cde = -Sym_(cde)[D_e,acbd],
```

where `Sym_(cde)` is the normalized average over all six permutations. The direct maps are the
source of truth if the candidate formulas fail.

## Whole finite-dimensional arenas

- `H`: all `10*10=100` coefficients, no dropped components.
- `K`: all `10*20=200` coefficients, no dropped components.
- `R`: the complete 20-dimensional algebraic-curvature space.
- `D`: the complete 60-dimensional G228 differential-Bianchi-compatible space.

Coordinate controls use identity-linear changes

```text
x^a = y^a + (1/6) A^a_bcd y^b y^c y^d
x^a = y^a + (1/24) B^a_bcde y^b y^c y^d y^e,
```

with fully symmetric lower derivative indices. Their dimensions are `4*20=80` and `4*35=140`.

Geodesic-normal constraints are generated without dropping rows from

```text
H_i(j,kl) = 0,
K_i(j,klm) = 0,
```

meaning normalized symmetrization over the parenthesized indices.

## Preregistered alternatives

```text
A_FULL_LOCAL_REALIZATION
  C2 rank 20/kernel 80; C3 rank 60/kernel 140;
  coordinate-gauge images equal both kernels;
  normal slices have dimensions 20 and 60 and both restricted maps are isomorphisms;
  the explicit inverse formulas pass; a local smooth Lorentz representative exists.

B_EXTRA_THIRD_ORDER_OBSTRUCTION
  the 2-jet result closes but C3 fails to reach the complete 60-dimensional G228 module or the
  normal 3-jet slice has a nontrivial kernel/cokernel.

C_SECOND_ORDER_REALIZATION_FAILURE
  the complete algebraic-curvature space is not reached from the declared metric 2-jet arena.

D_GAUGE_OR_TYPING_FAILURE
  a rank count is explained by an incomplete coordinate kernel, wrong normal constraint,
  convention mismatch, or another type defect, so no realization verdict is banked.
```

No alternative may be changed after the preregistration commit.

## Certification contract

Production must provide exact matrices and ranks for `C2`, `C3`, both coordinate-gauge maps, both
normal-constraint maps, both restricted maps, and both inverse compositions. It must save
machine-readable evidence and deterministic matrix hashes.

An independent implementation must:

- use standard-library rational arithmetic rather than SymPy elimination;
- construct the maps from index definitions independently;
- reproduce all load-bearing ranks and hashes or explain any representation-dependent hash;
- verify the explicit inverse formulas on complete exact target bases, not random samples.

Hostile controls must catch at least:

1. a sign or term deletion in `C2`;
2. a sign or term deletion in `C3`;
3. an omitted normal-coordinate constraint family;
4. a truncated cubic or quartic coordinate gauge;
5. a non-Bianchi `D` promoted as realizable;
6. a normal-coordinate uniqueness claim made before fixing the tangent frame;
7. a smooth/global-history promotion beyond the local point-jet result.

The bounded result requires preregistration, the complete declared finite-dimensional arenas,
independent exact verification, hostile catches, and a fresh adversarial review before banking.

## Maximum conclusion

At most G229 may prove that G227/G228-compatible **supplied point data** are locally realizable by a
Lorentz metric through cubic Taylor order, and possibly by a smooth local metric representative.
It may not generate the values, select a metric history, prove compatibility of prescribed fields
across a finite region, populate observers or branches, choose transport, derive dynamics, action,
source, matter, bootstrap, boundary, `X_max`, transfer, observation, mass, or signalling.
