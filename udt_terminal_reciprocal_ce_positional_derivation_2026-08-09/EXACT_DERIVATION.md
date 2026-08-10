# Exact derivation — reciprocal `c_E` as the terminal positional evaluator

Date: 2026-08-09
Mode: metric-led, exact analytic/CPU
Current grade: **VERIFIED-WITH-CAVEATS**

## 1. The type reversal

The previous solder audit asked the metric to transport already-normalized endpoint clock/ruler
frames and then looked for dilation in that transport. Metric-compatible transport preserves the
norms of normalized frames, so the result was necessarily zero.

The corrected order is:

```text
complete metric/coframe
+ an A-calibrated ordered observer-pair relation
    -> complete induced pair metric
    -> clock density + orthogonal ruler density + shift
    -> terminal reciprocal-c_E readout
    -> reciprocal log-imbalance coordinate
    -> conditional pair-calibration c_eff readout.
```

The dilation is not a deformation applied after a distance is known. It is the reciprocal
anisotropy of the complete calibrated pair relation. The angular and mixing sectors enter before
the final readout.

Once a physically calibrated pair surface or comparison Jacobian is supplied, no additional
scalar calibration variable is needed to perform the local algebraic readout. This re-expresses
the needed calibration state in the supplied pair-map parameterization; it does **not** derive the
physical calibration-state realization or observer/event-pair map from the complete metric alone.

## 2. The complete pair metric

Let `Sigma` be a two-dimensional comparison surface for an ordered observer query, and let

```text
F: Sigma -> (M,g)
```

be a regular pair map. Use dimension-matched comparison coordinates

```text
y^0 = c_E tau_A,
y^1 = s_A,
```

where `tau_A` is observer A's proper clock parameter and `s_A` is a ruler parameter calibrated at
A. The induced pair metric is

```text
h = F^* g.
```

For a complete coframe `theta^a` and pair-map tangents `J_i=F_*(partial_i)`, define

```text
V_i^a = theta^a(J_i),
h_ij  = eta_ab V_i^a V_j^b.
```

This formula retains every coframe slot. Clock-screen, ruler-screen, angular, shift, twist, and
global-branch effects can all alter `V_i^a` and therefore alter `h`. No angular correction is
attached after the fact.

The object is invariant under local Lorentz changes of complete coframe because

```text
V_i -> Lambda V_i,
Lambda^T eta Lambda=eta,
```

leaves `h_ij` unchanged. It is also spacetime-diffeomorphism natural because it is a pullback
metric.

The physical premise lies in `F` and its calibration, not in a coordinate component identity.
Arbitrary endpoint charts do not qualify.

## 3. Unique clock–ruler–shift decomposition

On the regular stratum

```text
h_00 < 0,
det h < 0,
```

there are unique positive functions `T,L` and one real shift `beta` such that

```text
h = -T^2 (dy^0 + beta dy^1)^2 + L^2 (dy^1)^2.
```

They are read directly from the complete pair metric:

```text
T^2    = -h_00,
beta   = h_01/h_00,
L^2    = h_11 - h_01^2/h_00,
T L    = sqrt(-det h).
```

`T` is the clock-line density. `L` is the ruler density after the ruler direction is
orthogonalized against the clock line inside the complete pair plane. The shift is not thrown
away; it is separated as its own exact datum.

Now decompose the two positive densities uniquely as

```text
T = sigma exp(-phi),
L = sigma exp(+phi).
```

Solving gives

```text
sigma = sqrt(T L) = (-det h)^(1/4),

phi = (1/2) log(L/T)
    = (1/4) log(-det h) - (1/2) log(-h_00)
    = (1/4) log[(-det h)/h_00^2].
```

This is not an ansatz. It is the unique positive common-scale/reciprocal-depth decomposition of
the regular pair metric relative to its calibrated clock line.

The algebra has the exact required symmetries:

- common scaling `(T,L)->(Omega T,Omega L)` changes `sigma` and leaves `phi` fixed;
- reciprocal scaling `(T,L)->(exp(-a)T,exp(+a)L)` leaves `sigma` fixed and sends
  `phi->phi+a`;
- abstract channel exchange sends `phi->-phi` and leaves `sigma` fixed;
- ruler orientation reversal leaves all density quantities unchanged.

The common-scale cancellation is an algebraic property of this readout. It is **not** a restored
claim that the physical metric is fundamentally scale free. `c_E` explicitly calibrates `y^0`.

### Sharp uniqueness and calibration scope

The uniqueness statement is exact but scoped. `phi` is the unique **reciprocal-channel coordinate**
in the displayed common-scale/reciprocal/shift decomposition, equivalently the previously derived
graded-density character. It is not a theorem forbidding somebody from defining a different
higher-derivative or nonlocal scalar such as `phi+f(curvature)`; that would be an additional
physical law, not the primary reciprocal positional channel.

The pair-map calibration is load-bearing. A common rescaling of both tape coordinates changes only
`sigma`, while an independent reciprocal rescaling changes `phi` by the rescaling depth. The latter
is not gauge once `y^0=c_E tau_A` and the ruler parameter are physically fixed. Merely requiring
`h=eta` at A is insufficient if arbitrary endpoint-dependent reparameterizations remain allowed;
the supplied pair map must carry its A-fixed proper-time/affine-ruler parameterization to B.

## 4. Reciprocal `c_E` is the terminal evaluator

The two null slopes of the induced pair metric are

```text
w_+ = dy^1/dy^0 =  T/(L-T beta),
w_- = dy^1/dy^0 = -T/(L+T beta).
```

The orientation-balanced inverse-slope combination is exact:

```text
(1/2)(1/w_+ - 1/w_-) = L/T.
```

Hence define the conditional geometric pair-calibration readout

```text
c_eff^(pair)/c_E = T/L = exp(-2 phi),

phi = -(1/2) log[c_eff^(pair)/c_E].
```

This implements the user's proposed order on a supplied calibrated pair map: its full pullback
metric is assembled first; the fixed reciprocal `c_E` conversion then assigns a terminal readout
to the supplied B on A's calibrated clock/ruler tape. The shift is removed by an intrinsic two-way
combination, not by setting it to zero.

This `c_eff^(pair)` is a **conditional geometric pair-calibration readout**. On mixed complete
geometries, identifying it with the universal physical `c_eff` ratio remains open because the
physical pair map and calibration-state owner remain open. No statement about material signals,
information propagation, or source dynamics follows.

On the founded pure reciprocal branch,

```text
h = diag(-exp(-2phi), exp(+2phi)),
```

the determinant is `-1`, `T=exp(-phi)`, `L=exp(+phi)`, and every displayed formula returns the
original `phi` and `c_eff/c_E=exp(-2phi)` exactly.

## 5. Endpoint-relative depth and the role of A

At two points on one consistently calibrated pair surface, write

```text
T_i=sigma_i exp(-phi_i),
L_i=sigma_i exp(+phi_i).
```

The relative reciprocal depth is

```text
delta_AB
 = (1/2) log[(L_B/T_B)/(L_A/T_A)]
 = phi_B-phi_A.
```

All endpoint common scales cancel even when `sigma_A != sigma_B`. Choosing A's proper clock and
ruler calibration sets `phi_A=0` on the tape origin, so the terminal value at B is `phi_AB`.

This explains why the older factorization counterexamples do not refute the new result. Those
examples allowed independent reciprocal refactorizations at each endpoint. Once one physical
A-calibrated pair tape is supplied, such a refactorization changes the tape and is not a
presentation gauge. Common scaling remains harmless; reciprocal rescaling is precisely the depth
being measured.

## 6. Exact supplied-Jacobian angular/mixing witnesses

For the registered complete lower-mixing columns

```text
J_0=(1/2,0,1/4,0),
J_1=(0,2,0,0),
eta=diag(-1,1,1,1),
```

the complete induced pair metric is

```text
h=[[-3/16,0],[0,4]],
det h=-3/4.
```

The terminal depth is

```text
phi_pair=(1/4)log(64/3)=0.7650676986728905...,
```

not the bare reciprocal-block value `log 2`.

For a second witness with screen content in both pair columns,

```text
J_0=(1/2,0,1/4,0),
J_1=(0,2,1/3,0),
```

one obtains

```text
h=[[-3/16,1/12],[1/12,37/9]],
det h=-7/9,
L^2=112/27,
phi_pair=(1/4)log(1792/81)=0.7741596097156093....
```

The angular/screen component creates both a nonzero shift and a changed ruler density. The terminal
formula sees both through the full pullback metric. Rational endpoint Lorentz boosts and screen
rotations leave these induced metrics and depths exactly unchanged.

These are structural existence witnesses on supplied complete pair Jacobians, not a selection of
the physical observer-pair law. They exhibit the precise possible `phi+orchestra` join: the
orchestra changes the complete pair metric first; its reciprocal coordinate is then read from that
whole metric, not from a radial solo with an angular term appended later.

## 7. What composition really requires

The founding identity proves

```text
D(a_2)D(a_1)=D(a_1+a_2)
```

for carried reciprocal channel scalings. The density formula likewise composes when the target
clock/ruler state of one leg is the source state of the next.

It does **not** follow that independently rebuilt observer-pair tapes must define a real additive
groupoid cocycle on every path and every complete `GL(4)` arrow. The July 27 semantics audit
already left endpoint-versus-path realization open. The full-`GL` cold reviews then showed why the
universal arrow-only cocycle demand is too strong.

The correct distinction is:

```text
compatible carried tape/channel composition: exact;
arbitrary observer-pair assignment additivity: not founded;
physical nonnegative separation: may be symmetric and nonadditive;
orientation/sign channel: separate typed datum where needed.
```

Therefore a terminal pair readout is not disqualified because metric distance, `dexp`, or a pair
surface fails arbitrary subdivision additivity. Those objects still cannot be silently promoted to
the physical pair map; their admissibility is tested by the map's own type, covariance, calibration,
and global regularity.

This correction is deliberately narrow. Any claimed **physical signed reciprocal depth** must
still own a compatible cocycle-type composition law on its properly typed query space. The present
pair-metric readout neither supplies nor withdraws that missing physical ownership theorem.

## 8. The pair map: conditional positive construction and remaining joint

A conditional local metric-natural example exists after an observer query supplies enough data. Given
observer A's worldline `z_A(tau)`, a unit spatial ruler direction `n(tau)`, and a declared event
pairing, define on a regular normal neighborhood

```text
F(tau,s)=Exp_{z_A(tau)}[s n(tau)].
```

With `y^0=c_E tau` and `y^1=s`, this is an A-calibrated pair-surface candidate. Its complete
pullback metric is a lawful input to the terminal formula. A Fermi-Walker or query-supplied
evolution of `n` is extra mathematical comparison data, not a new UDT action and not selected by
the two founding postulates.

This construction is conditional because the two founding postulates do not yet select:

- observer worldlines or the event pairing;
- orthogonal-exponential versus another pair relation;
- the direction update through an intermediate observer;
- one branch at a cut locus or caustic; or
- a global completion of the pair surface.

The open object is therefore smaller and more physical than the previous “calibration-state
functor”:

```text
(complete solved metric/coframe, ordered observers, event pairing, branch/path data)
    -> calibrated complete pair surface or comparison Jacobian.
```

Once that object and its calibration are supplied, the reciprocal log-imbalance coordinate is no
longer algebraically open: the terminal formula determines it uniquely on every regular Lorentzian
pair cell. Its identification with the universal physical `phi_AB` remains conditional on the
still-open physical pair-map and signed-composition ownership.

## 9. Affine development is not enough by itself

Cartan/affine development of one path composes in the affine semidirect product. Its translation
component records a displacement. But a logarithmic ratio of translation coordinates is:

- nonadditive even for two collinear equal-ratio translations;
- divergent on a pure spacelike translation; and
- undefined/degenerate on a pure timelike translation.

Therefore one developed path does not supply the terminal clock/ruler densities. A **family** of
nearby developed paths—its comparison Jacobian—can supply a pair metric. This is exactly why the
two-dimensional pair surface, rather than one affine displacement vector, is the right home.

## 10. The nature of `phi`

The derivation supports three distinct statements:

1. **Abstract founded depth:** the parameter of `D(phi)` on supplied reciprocal channels remains
   derived.
2. **Relational pair coordinate:** on a supplied A-calibrated complete pair metric, the candidate
   `phi_AB` is the unique reciprocal log imbalance of the complete clock and orthogonal-ruler
   densities within that fixed calibration and pair map.
3. **Pointwise field:** a scalar `phi(x)` is a potential/coordinate representation only when a
   compatible family of pair surfaces shares a common reference and descends endpoint-exactly.

Thus `phi` is neither a random placeholder nor automatically an independent universal scalar
field. Its primary physical type is relational. A pointwise profile is a special organized family
of those relational readouts.

## 11. `X_max` and degenerate strata

On any branch where both the working observer-pair asymptote and the physical identification of
the conditional pair readout are realized,

```text
phi_AB -> +infinity
    iff
T/L -> 0
    iff
c_eff^(pair)/c_E -> 0.
```

This identifies the asymptotic channel degeneration. It does not derive the separation function,
the finite value of `X_max`, its directional variations, or the global profile approaching it.

The regular formula has exact boundaries:

| Stratum | Result |
|---|---|
| coincidence on a calibrated smooth pair map | `h=eta` at A and `phi=0` |
| clock line becomes null (`h_00=0`) | log readout diverges/fails |
| pair plane degenerates (`det h=0`) | ruler density vanishes; readout diverges/fails |
| pair map loses rank | no regular pair metric |
| cut locus / multiple comparison surfaces | branch-valued `phi_AB`; no silent branch selection |
| no global pair surface | local/query readout survives; global profile does not |
| endpoint level set has several members | readout locates a level, not a unique B |

No cutoff is introduced at any failure stratum.

## 12. Exact landing

```text
TERMINAL_RECIPROCAL_CE_PAIR_METRIC_DECOMPOSITION_DERIVED_ON_SUPPLIED_REGULAR_A_CALIBRATED_PAIR_METRICS;
RELATIONAL_PHI_IS_THE_UNIQUE_RECIPROCAL_LOG_IMBALANCE_ONLY_WITHIN_THAT_FIXED_CALIBRATION_AND_PAIR_MAP;
ANGULAR_AND_MIXING_MODULATION_ARE_STRUCTURALLY_VISIBLE_IN_SUPPLIED_PAIR_JACOBIANS_BEFORE_READOUT;
NO_GENERAL_PHYSICAL_CEFF_RATIO_OR_CALIBRATION_STATE_REALIZATION_IS_DERIVED;
PAIR_SURFACE_OR_COMPARISON_JACOBIAN_OWNER_ENDPOINT_SELECTION_PATH_REALIZATION_AND_XMAX_PROFILE_REMAIN_OPEN.
```

No action, source, carrier, matter, mass, bootstrap equation, boundary completion, `X_max` value,
CMB spectrum, signal law, or canonization follows.
