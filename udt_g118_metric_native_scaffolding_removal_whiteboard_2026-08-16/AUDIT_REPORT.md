# G118 audit report — metric-native scaffolding removal

Date: 2026-08-16

Preregistration: `f977b2e8`

Status: `VERIFIED_WITH_CAVEATS__BLIND_REVIEW_REPAIRS_IMPLEMENTED`

## Result

The recent simplification is real. The current observer architecture is not a collection of
independently tuned instruments. For one supplied point-observer exponential query, the complete
metric and one full observer differential provide the smallest local geometric assembly:

\[
(g,Q)\longmapsto F\longmapsto dF\longmapsto H=F^*g.
\]

The terminal pair metric, true angular Jacobi block, and mixed contractions are distinct blocks of
that one pullback. Frequency additionally requires the ray covector and source/observer velocities;
network composition additionally requires the full Jacobi phase carrier and calibrated source
junctions. Thus `dF` removes independent local orchestra knobs, but it does not own the source,
transfer, query, branch, or physical history.

## Strongest new simplification

The banked exact static central-radial result and the banked regular time-live central two-jet use a
spherical areal-radius metric,

\[
g=h_{ab}(x)dx^a dx^b+R(x)^2d\Omega^2,
\]

and give, in matched orthonormal endpoint bases within those respective scopes,

\[
D_{\rm sky}=R\,I_2,
\qquad d_A^2=|\det D_{\rm sky}|=R^2.
\]

In arbitrary orthonormal endpoint bases the matrix is `R` times the basis-identification
orthogonal map; only the determinant statement is basis-free. The exact static theorem is banked
in G113 and the regular time-live central two-jet in G115. An exact arbitrary finite-radius
time-live theorem is not yet banked.

This removes the independent tensor-valued P1 isotropic screen ansatz only inside the already-banked
static and local-two-jet scopes. An arbitrary finite-radius time-live theorem is the proposed G119,
not a current result. None of these scopes selects the scalar radius-frequency history, transfer,
branch, or global metric.

## Correct radiometric reduction

Let

\[
Z_\omega=\frac{-g(k,U_s)}{-g(k,U_o)},
\qquad \mathcal T=\eta\epsilon.
\]

G94's regular one-branch Wronskian and clock factorization gives

\[
F_o=\frac{L_\Omega\mathcal T}{Z_\omega^3d_A^2}.
\]

On those banked central spherical scopes this becomes

\[
\boxed{F_o=\frac{L_\Omega\mathcal T}{Z_\omega^3R^2}}.
\]

Only with a directional luminosity-distance convention or supplied source isotropy may this be
rewritten as

\[
d_L^2=\frac{Z_\omega^3R^2}{\mathcal T}.
\]

The complete metric/query owns the geometric-clock denominator `Z_omega^3 R^2`; it does not own
`mathcal T`. The transfer character counterfamily in G94 proves that no rearrangement of the metric
alone can select it.

## Exact P1 retyping

The frozen conditional P1 curve is

\[
d_L^{\rm P1}=n Z^2\left(1-Z^{-2/n}\right)=Z^2\lambda_A(Z).
\]

Combining it with the general spherical factorization yields

\[
\boxed{
\frac{R(Z)}{\sqrt{\mathcal T(Z)}}
=Z^{1/2}\lambda_A(Z)
=nZ^{1/2}\left(1-Z^{-2/n}\right)
}.
\]

Equivalently, define the interface quotient

\[
\Lambda=\frac{R}{\sqrt{Z\mathcal T}};
\]

then the frozen P1 interface says `Lambda=lambda_A`. Only under the additional transparent
null-momentum closure `mathcal T=1/Z` does `lambda_A=R` and `d_L=Z^2R` follow.

Therefore P1 is not currently an independently owned screen matrix or a selected radius history.
It is a conditional release-coordinate-to-effective-screen chord. SNe constrains its standardized
brightness shape only after adopting the processed release coordinate for `Z_omega` and supplying
source/branch calibration. It does not separately identify `R`, `mathcal T`, terminal `phi_pair`,
or the G116 history coefficients.

## Interface fiber, not gauge

At fixed `Z` the scalar brightness interface is invariant under

\[
(R,\mathcal T)\mapsto(aR,a^2\mathcal T),\qquad a>0.
\]

This is an inverse-interface non-identifiability across possible histories and transfers, not a
metric gauge transformation and not proof that every member is globally realizable. If transfer is
required to compose on an observer network, the allowed `a` must obey the corresponding descent or
character law; an arbitrary function is too broad.

## What was removed

- universal pointwise `phi` ownership;
- an orchestra correction bolted on after terminal readout;
- literal identification of pair-screen and sky-Jacobi matrices;
- arbitrary independent point-vertex Jacobi data;
- G107 constant representation coefficients as a physical score;
- universal `Z=exp(phi_pair)` and `c_eff/c_E=Z^-2` on live queries;
- P1 as a smooth static central history;
- P1 as an independent tensor-valued screen law in the banked static and central-two-jet scopes;
- inverse-Jacobi/Riccati charts as the complete caustic carrier.

## What is irreducible or still open

- the operational query and active instrument protocol;
- direct-frequency adoption of processed release coordinates;
- physical complete history and finite/global continuation;
- source congruence, luminosity, phase state, occupancy, and branch weights;
- radiative transfer `mathcal T`;
- nonspherical shear/rotation, extended sources, caustics, and branch aggregation;
- common reciprocal calibration across a network;
- action, source dynamics, `X_max`, bootstrap, matter, mass, and signalling.

## Ranked simplification program

1. Prove the exact finite-radius time-live spherical theorem `D_sky=R O` and its basis-free
   determinant, extending the banked static and local-jet scopes.
2. Use the full phase carrier rather than inverse-screen/Riccati variables whenever caustics or
   network composition are load-bearing.
3. Keep terminal depth, direct frequency, and transfer as typed outputs/inputs; never replace them
   by a fitted universal scalar mixture.

## Maximum conclusion

```text
PRIORITIZED_METRIC_NATIVE_SIMPLIFICATION_PROGRAM
__ONE_FULL_OBSERVER_DIFFERENTIAL_OWNS_LOCAL_PAIR_ANGULAR_AND_MIXED_GEOMETRY
__CENTRAL_SPHERICAL_SCREEN_MATRIX_REDUCES_TO_AREAL_RADIUS_WITHIN_BANKED_STATIC_AND_LOCAL_JET_SCOPES
__P1_RETYPED_AS_A_CONDITIONAL_EFFECTIVE_SCREEN_CHORD
__TRANSFER_HISTORY_QUERY_AND_GLOBAL_SELECTION_REMAIN_OPEN
```

No observational prediction, selected history, new postulate, or downstream physics follows.
