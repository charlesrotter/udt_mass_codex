# Preregistration — R17 path-labelled connection decomposition audit

Date: 2026-08-10
Base commit: `400087612d5ec6db91534b0063913572d295937f`
Mode: CPU-only exact algebra; metric-led characterization, not a target search.

## Whole question

On the supplied smooth regular stationary R17/W01 C01--C06 coframes, the clock/ruler plane `E`
already integrates into `R x S1` pair leaves and the metric-projected normal connection is known
along `E`. Determine whether projection of the complete Levi--Civita connection onto the rank-two
normal bundle `H` defines one smooth path-labelled metric connection for arbitrary supplied
piecewise-smooth paths in the complete four-dimensional geometry. Derive all vertical,
horizontal, and mixed curvature components, their gauge/global meanings, and their chart and
finite-cell compatibility.

This asks what connection the supplied metric owns. It does not ask which path, leaf, branch,
winding, or observer comparison is physically preferred.

## Exact bounded arena

The supplied coframe is

```text
theta0 = u^-1 (dt + a sigma3)
theta1 = u sigma3
theta2 = v sigma1
theta3 = v sigma2
u = exp(phi), v = exp(lambda phi), T(phi)=0.
```

`E=span(e0,e1)` and `H=span(e2,e3)`. The complete projected connection is defined without a new
action or transport postulate by

```text
D_X s = P_H(nabla^LC_X s),  s in H,
A_i = g(D_{e_i} e2,e3),
F_ij = e_i(A_j)-e_j(A_i)-A([e_i,e_j]).
```

The six supplied `lambda` strata `-2,-1,0,1/2,1,2` and both Maurer--Cartan signs are retained.
`phi` is an arbitrary smooth stationary field, represented by compatible noncommuting frame jets;
no profile or field equation is imposed.

## Preregistered decomposition

- vertical/leafwise: `F_01`;
- mixed: `F_02,F_03,F_12,F_13`;
- horizontal: `F_23`.

The audit will also test metricity, path composition and reversal after a path is supplied,
`SO(2)` gauge covariance, `O(2)` representative-free observables, Hopf-chart overlap behavior,
descent to the base where meaningful, and the distinction between local flatness and global
winding holonomy.

## Falsification/certification contract

The positive connection claim fails if the complete projected derivative is not a well-typed
metric connection on `H`, if its restriction does not reproduce the banked leafwise formula, if
its path transport fails identity/composition/reversal, or if its local representatives fail the
connection transformation law on overlaps.

Any claimed simplification or special stratum must be an exact identity for arbitrary compatible
stationary jets. A numerical witness can refute an identity but cannot establish one. Every
curvature component and special locus must be independently reconstructed without importing the
production formulas. Mutation catches must reject erased mixed sectors, an imposed path, a
selected `lambda`, a signed-angle invariant, and promotion to the physical observer arrow.

## Maximum conclusion

At most this audit may derive and classify the complete metric-projected connection on `H` and its
path-labelled transport/curvature within the supplied regular stationary R17 family. It may find
special or degenerate strata without selecting them. It must stop before a unique physical path,
leaf, branch, `lambda`, reset, non-isometric observer arrow, universal mixed-geometry `c_eff`,
action, source, matter law, bootstrap selection, `X_max` value, CMB prediction, signalling law,
or dynamics.
