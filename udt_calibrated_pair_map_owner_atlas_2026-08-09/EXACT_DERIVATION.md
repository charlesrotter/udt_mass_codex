# Exact derivation — calibrated observer-pair map owner atlas

Date: 2026-08-09
Mode: metric-led, exact analytic/CPU
Current grade: **VERIFIED-WITH-CAVEATS**

## 1. What this audit does and does not ask

The terminal reciprocal-`c_E` result starts after a regular calibrated pair map has supplied

```text
F: Sigma -> (M,g),
h = F* g,
y^0 = c_E tau_A,
y^1 = s_A.
```

It then derives, uniquely on `h_00<0` and `det h<0`,

```text
T^2 = -h_00,
L^2 = h_11 - h_01^2/h_00,
phi_pair = (1/2) log(L/T)
         = (1/4) log[(-det h)/h_00^2].
```

That result does not select `F`. This audit asks which pair-map families the metric can construct,
what other data each family needs, and whether any one family is already the universal physical
owner of the terminal readout.

The frozen arena contains six families and eleven axes per family. All 66 cells are retained in
`PAIR_MAP_ATLAS.tsv`. No family is accepted because it resembles a desired universe and none is
discarded because it is branch-valued or singular.

## 2. The common mathematical object

Let `z_A(y)` be A's declared observer curve, parameterized so `y=c_E tau_A`. Let `n(y)` be a declared
unit spacelike direction orthogonal to A's unit tangent. In a regular exponential neighborhood,

```text
F(y,s) = Exp_{z_A(y)}[s n(y)]
```

is a geometric local pair map. Its Jacobian columns are Jacobi fields and therefore depend on the
complete metric curvature, A's acceleration history, and the evolution of `n`. The pullback
`h=F*g` is diffeomorphism-natural and independent of an endpoint orthonormal-frame presentation.

At the origin `s=0`, proper-time and affine-ruler calibration gives

```text
h_00=-1, h_01=0, h_11=1.
```

Off the origin, however, the metric does not by itself choose:

- the observer curve or which event on B is paired with an event on A;
- the initial ruler direction when several directions reach B;
- how that direction is carried along an accelerated observer history;
- a branch after the exponential map ceases to be injective; or
- how two independently constructed A–B and B–C tapes identify their middle calibration.

Those are not coordinate artifacts. They distinguish genuinely different geometric maps.

## 3. P01 — orthogonal exponential/Fermi tubes

### Local result

Given a complete ordered observer query containing A's worldline, A's proper-time parameter, a
smooth A-orthogonal unit spacelike direction field, and a regular exponential branch, `F` above is
a metric-natural local map. If B is defined by a unique transverse intersection with that tube,
the local event pairing is also fixed. This is `DERIVED_FROM_METRIC_AND_DECLARED_QUERY`, not derived
from the metric plus two bare endpoint events.

An exact flat accelerating control is

```text
F(y,s)=((a^-1+s)sinh(ay),(a^-1+s)cosh(ay)),
h=-(1+as)^2 dy^2+ds^2.
```

Thus even in flat geometry the pair metric records the declared observer history. At `a=0` the
inertial result is recovered. At `1+as=0`, the clock column becomes null and the regular terminal
readout ends. The calculation is geometry, not imported acceleration dynamics.

### Scope

Normal-neighborhood uniqueness is local. At conjugate points the Jacobian loses rank; at cut loci
several branches can represent the same endpoint. No current premise silently promotes the
shortest, smoothest, or first branch.

## 4. P02 — integral surfaces of a coframe-selected two-plane

Suppose a declared complete-coframe split supplies a rank-two distribution `E=span(e_0,e_1)`. A
pair surface tangent to `E` exists locally only if the Frobenius condition holds:

```text
[e_0,e_1] belongs to E.
```

This is not automatic. In flat spacetime choose a time-dependent spatially rotated presentation

```text
e_1=cos(omega y) partial_x + sin(omega y) partial_z,
e_2=-sin(omega y) partial_x + cos(omega y) partial_z.
```

The metric remains flat, while

```text
[e_0,e_1]=omega e_2
```

is transverse to `span(e_0,e_1)` for nonzero `omega`. At `omega=0` the plane is integrable.

Therefore an arbitrary orthonormal coframe presentation cannot select a metric-only pair plane.
If UDT separately owns a physical reciprocal two-plane reduction, then its integral leaves remain
a valid **conditional** family, subject to Frobenius, calibration, rank, and global-foliation gates.
The audit does not reject a physical complete-coframe split; it rejects treating any presentation
split as already metric-owned.

## 5. P03 — stationary Killing-flow surfaces

On a branch carrying an intrinsic nonzero timelike Killing field `K`, choose a transverse curve
`c(s)` and define

```text
F(y,s)=Flow_K^y(c(s)).
```

For those declared inputs the flow theorem gives a unique local surface. In A-normalized stationary
coordinates its complete pullback may be written

```text
h=-N^2(dy+beta ds)^2+R^2 ds^2.
```

The terminal pair depth is

```text
phi_pair=(1/2)log(R/N),
```

whereas the A-referenced Killing-norm depth is

```text
delta_K=-log N.
```

Their difference is exact:

```text
phi_pair-delta_K=(1/2)log(NR)=(1/2)log(TL).
```

They coincide only when the additional reciprocal-area condition `T L=N R=1` holds. The stationary
Killing construction is consequently a useful conditional positive control for calibration and
composition, but a Killing clock ratio is not generically the complete UDT clock/ruler readout.

Killing horizons, zeros of `K`, failure of transversality, incomplete orbits, and absence of a
global cross-section delimit the construction.

## 6. P04 — general accelerated tubes

Once an observer history and a direction-evolution law are declared, the exponential tube is again
metric-natural. The metric does not select those histories or laws. An exact flat control makes the
nonuniqueness visible without curvature:

```text
F_+(y,s)=(y,s cos(omega y), s sin(omega y),0),
F_-(y,s)=(y,s cos(omega y),-s sin(omega y),0).
```

These are distinct maps for generic `y,s,omega`, but both give

```text
h=(-1+omega^2 s^2)dy^2+ds^2.
```

Hence even the complete terminal pair metric need not identify one unique embedding. The clock
column becomes null at `|omega s|=1`. This is a query-family fact, not a failure of covariance.

## 7. P05 — exponential/Jacobi branch relation

The metric naturally supplies the full relation of regular exponential branches. It does not in
general supply one global single-valued map. For a constant-curvature scalar Jacobi control, the
position block has the factor

```text
j(x)=sin(x)/x.
```

It does not subdivide multiplicatively:

```text
j(pi/6)^2 != j(pi/3),
```

and it vanishes at the conjugate value `x=pi`. The full two-component Jacobi phase propagator does
compose,

```text
M(q)M(p)=M(p+q),
```

but it acts on enlarged position–derivative data and is not itself the two-dimensional pair map or
terminal signed depth. Thus `dExp` is useful differential data, not the missing universal arrow.

At a cut locus the honest metric-derived object is a branch-labelled relation. A choice of one
branch would require additional physical or query data.

## 8. P06 — carried versus rebuilt tapes

Pair surfaces are maps into spacetime. `F_AB` and `F_BC` do not have a canonical binary function
composition, because the codomain of one is not the domain of the other.

The reciprocal calibration channels themselves compose when the state is carried:

```text
D(b)D(a)=D(a+b).
```

But if B independently rebuilds its tape, a reciprocal reset `r` can be inserted:

```text
D(b)D(r)D(a)=D(a+b+r).
```

The reset is not removed by endpoint-frame covariance or by common-scale cancellation. A common
scale at B cancels from the log imbalance; a reciprocal rescaling shifts it by `r`. Therefore a
physical composition law requires an enriched object—such as a calibrated pair germ or carried
clock/ruler state—with an owned middle transition. The metric supplies each separate pullback but
does not, from the present premises, select that transition.

This does not revive an independent scalar field after the pair map is supplied. It distinguishes
two levels:

1. **local terminal evaluator:** the supplied calibrated `h` uniquely gives `phi_pair`;
2. **global composition owner:** a rule must say how calibrated pair relations are carried, rebuilt,
   or branched through another observer.

## 9. Complete atlas landing

The 66 preregistered classifications contain:

| Disposition | Count |
|---|---:|
| `DERIVED_FROM_METRIC_AND_DECLARED_QUERY` | 16 |
| `CONDITIONAL_QUERY_DATA` | 12 |
| `CONDITIONAL_BRANCH_STRUCTURE` | 9 |
| `LOCAL_ONLY_BRANCH_VALUED` | 8 |
| `FAILS_REQUIRED_TYPE` | 4 |
| `OPEN_NOT_DECIDED_BY_CURRENT_FOUNDATION` | 17 |

The strongest surviving construction is the local A-orthogonal exponential tube **after** a full
observer query supplies the worldline, proper clock, ruler direction/evolution, event pairing or
intersection rule, and a regular branch. The metric then fills in the complete geometry and the
terminal evaluator reads the resulting clock/ruler imbalance.

No unique universal pair map follows from the complete metric plus bare ordered endpoint events.
The complete-coframe plane requires a physical split and integrability. Stationary Killing flow is
conditional. Accelerated tubes form a real query-dependent family. Cut loci require a branch atlas.
Separate pair surfaces do not compose as arrows without carried calibration state.

The smallest remaining joint is therefore not another formula for `phi`. It is the **physical
calibrated pair-relation functor**: the typed rule that says what an ordered observer query contains,
which local/global branch relates the observers, and how its calibration state is carried through
an intermediate observer.

## 10. Maximum conclusion and exclusions

This audit derives and classifies the frozen six-family arena. It does **not** prove that no other
metric-natural pair relation exists. It proves nonuniqueness within the declared inputs by exact
counterexamples and identifies where additional query, branch, or calibration ownership enters.

It does not derive an action, source, carrier, matter law, boundary, bootstrap optimizer, `X_max`
value/profile, physical signalling rule, or CMB prediction. `c_E` remains the measured calibration
of the pair tape. `X_max` remains a working asymptotic frame, not a pair-map selector.

## 11. Reproduction

Primary exact controller:

```bash
python3 udt_calibrated_pair_map_owner_atlas_2026-08-09/derive_pair_map_owner_atlas.py
```

Independent standard-library implementation:

```bash
python3 udt_calibrated_pair_map_owner_atlas_2026-08-09/verify_pair_map_owner_atlas_independent.py
```

Current results: 67/67 exact-controller checks and 45/45 independent checks pass. A fresh
read-only gpt-5.4 review independently reran both controllers, accepted the bounded landing, and
required no load-bearing correction. See `EXTERNAL_REVIEW.md`.
