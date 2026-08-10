# R17 pair-leaf normal connection and holonomy audit

Date: 2026-08-10

## Result

Local verification lands on:

```text
CONDITIONAL_METRIC_OWNED_NORMAL_CONNECTION_AND_REPRESENTATIVE_FREE_HOLONOMY_DATA_ON_SUPPLIED_R17_PAIR_LEAVES__PHYSICAL_PATH_AND_COMPLETE_ARROW_OPEN
```

For the supplied regular stationary R17/W01 coframe family, the Levi--Civita connection projected
onto the rank-two metric normal bundle gives, up to Maurer--Cartan orientation sign,

```text
A(e0) = a/(u v^2)
A(e1) = 2/u - u/v^2
F_perp(e0,e1) = 2 a (1+lambda) Z(phi)/(u^2 v^2).
```

The signed connection angle is frame-representative dependent.  Its curvature square and the
`O(2)` conjugacy class of closed-loop holonomy are representative-free.

## New structural separation

- `lambda=-1` has flat leafwise normal connection for every smooth stationary `phi`, while wound
  loops may still carry nontrivial global holonomy.
- `lambda=0` makes `q_H=v^2(sigma1^2+sigma2^2)` Hopf-basic for every smooth stationary `phi`.
- Generic other lambdas are locally curved wherever `a Z(phi)` is nonzero.

These are different geometric roles.  The audit selects neither branch and does not infer that the
roles must coincide.

## Cross-leaf boundary

The normal plane also supplies the usual horizontal complement to the Hopf-fiber direction.  Given
a base path and starting point, it supports a horizontal lift.  It does not choose a unique base
path or yield the complete non-isometric physical observer-pair arrow.

## Evidence

- exact symbolic reconstruction: 10/10 checks;
- independent standard-library Fraction/Dual reconstruction: 72/72 checks across six lambdas and
  both Maurer--Cartan signs;
- all six lambda strata retained without selection;
- mutation and repository gates are recorded separately.

Until a fresh external adversarial review is incorporated, this package is a
`LOCAL_VERIFIED_LEAD`, not a settled result.

## Four banking gates

1. Preregistered: **yes**, commit `a85f93f4cd648881831ce1ffb4673cbfbe7d22c7`.
2. Full space or bounded scope: **bounded and explicit**—all six supplied regular stationary
   C01--C06 lambdas, arbitrary smooth stationary `phi`; no time-live or degenerate strata.
3. Independently verified: **yes locally**, with an implementation that imports neither the
   production controller nor SymPy; fresh external adversarial review remains pending.
4. Every premise audited: **yes for the bounded claim**, with downstream ownership questions left
   `OPEN` or `EXCLUDED`.
