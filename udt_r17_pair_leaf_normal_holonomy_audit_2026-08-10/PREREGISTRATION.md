# Preregistration — R17 pair-leaf normal connection and holonomy

Date: 2026-08-10

Mode: `MAP -> OBSERVE -> DERIVE`, metric-led, exact analytic/CPU

Base: `5be00ec479f3a275f719291a3c96443d2fefad7c`

## Whole question

On the already-derived intrinsic `R x S1` pair leaves of the supplied smooth regular stationary
R17/W01 C01--C06 coframes, determine what the complete metric itself supplies for the rank-two
angular normal bundle:

1. the projected normal connection along each leaf;
2. its curvature on the leaf;
3. holonomy of contractible and Hopf-wound loops;
4. representative-free observables under screen rotations and reflections;
5. dependence on the Hopf-base leaf, the stationary depth field and its derivatives, and all six
   supplied `lambda` strata; and
6. whether cross-leaf comparison is already fixed or still requires a horizontal path query.

This observes the complete supplied geometry. It does not target trivial holonomy, a preferred
`lambda`, a physical path, a CMB pattern, or a matter mechanism.

## Frozen arena

```text
theta0=u^-1(dt+a sigma3)
theta1=u sigma3
theta2=v sigma1
theta3=v sigma2
u=exp(phi)>0
v=exp(lambda phi)>0
lambda in {-2,-1,0,1/2,1,2}
E=span(e0,e1)=span(T,Z)
H=span(e2,e3)=span(X,Y)
```

The metric-projected connection is

```text
D_V s = H(nabla_V s),  s in H,
```

with `nabla` the Levi--Civita connection of the supplied complete metric. No alternative
connection, action, equation, source, or observer mechanics may be introduced.

The analytic theorem must be stated for arbitrary smooth stationary `phi`. The existing
`phi=(1/50)F_GENERIC` and `a=1/64` are retained only as the already-frozen global witness; they are
not promoted to a field-equation solution or fitted profile.

Both Maurer--Cartan sign conventions must be checked. A screen orientation may be chosen for local
calculation, but the banked observable must survive its reversal or be explicitly orientation-
conditional.

## Candidate outcomes

- `FLAT_NORMAL_CONNECTION_ON_EACH_LEAF`
- `CURVED_NORMAL_CONNECTION_WITH_CONTRACTIBLE_HOLONOMY`
- `STRATIFIED_BY_LAMBDA_OR_DPHI`
- `WINDING_ONLY_FLAT_HOLONOMY_ON_A_SUBSTRATUM`
- `NO_REPRESENTATIVE_FREE_NORMAL_OBSERVABLE`
- `REPRESENTATIVE_FREE_CONJUGACY_OR_CURVATURE_DATA_DERIVED`
- `TYPE_FAILURE_OR_PRIOR_FOLIATION_ERROR`

These outcomes characterize rather than filter the solution space. More than one may apply on
different strata.

## Certification contract

The result may be banked only if:

1. the connection is derived from the coframe and Maurer--Cartan brackets, not assigned;
2. its curvature is independently reconstructed from the resulting connection and bracket;
3. the `lambda=-1`, generic-`lambda`, constant-depth, twist-off, screen-rotation, and screen-
   reflection controls are all classified;
4. wound-loop holonomy is separated from contractible-loop holonomy and from ambient Lorentz
   holonomy;
5. all six supplied `lambda` values are retained without selection;
6. mutation catches reject a wrong connection coefficient, wrong curvature coefficient, erased
   path/winding dependence, orientation-dependent quantity called invariant, selected leaf or
   `lambda`, and promotion to a physical observer arrow; and
7. source manifests, frozen manifests, current-path/frontier gates, startup links, premise guards,
   and the documented test baseline pass.

## Maximum conclusion

At most:

```text
CONDITIONAL_METRIC_OWNED_NORMAL_CONNECTION_AND_REPRESENTATIVE_FREE_HOLONOMY_DATA_ON_SUPPLIED_R17_PAIR_LEAVES
```

or a precise scoped obstruction.

No physical path, leaf, winding, branch, `lambda`, reset, complete observer arrow, universal
mixed-geometry `c_eff`, action, source, matter, bootstrap law, `X_max`, CMB observable, signalling
law, or dynamics may be inferred.
