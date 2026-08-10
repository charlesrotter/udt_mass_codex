# Exact derivation — multi-channel observer-relation assembly

Date: 2026-08-10

Mode: metric-led, exact analytic/CPU

Final scoped grade: `VERIFIED-WITH-CAVEATS`; fresh sealed external review returned
`CONDITIONAL_MULTICHANNEL_ASSEMBLY_ONLY`.

## 1. Result first

The bounded stationary R17 evidence does not describe one scalar instrument. On a supplied regular
`A`-calibrated pair relation, it naturally separates into:

1. a complete Lorentzian pair metric `h`, equivalently three unique local state coordinates
   `(kappa,phi,beta)`;
2. the metric-owned clock/ruler/screen projector typing and supplied branch label `lambda`; and
3. a path-labelled normal isometry `U_gamma` in the angular screen bundle.

Here

```text
kappa=log(sigma)       common-scale density,
phi                   reciprocal clock/ruler imbalance,
beta                  clock-ruler shift,
U_gamma               angular normal transport.
```

The first two logarithmic density coordinates give exact endpoint characters on matched calibrated
pair states:

```text
Delta_kappa=kappa(q)-kappa(p),
Delta_phi=phi(q)-phi(p).
```

The shift is a genuine component of the supplied pair state, but not a standalone group character;
it composes only through the full pair map/Jacobian or matched endpoint state. The angular channel
is not real-valued at all: it composes in the oriented normal-isometry groupoid. This is the typed
reason that forcing all complete information into one real one-form produced nonuniqueness.

Let `F:Sigma->M` be the supplied calibrated pair map and let `bar_gamma` be a declared curve in
`Sigma`, with spacetime path `gamma=F o bar_gamma`. The exact minimal object for the
**already-banked pair-metric plus normal-transport data tied together by that common query** is a
state-decorated path groupoid:

```text
object x = (h_x equivalently (kappa_x,phi_x,beta_x), R_x, lambda),
arrow gamma:x->y carries (Delta_kappa,Delta_phi,U_gamma).
```

This is conditional on the supplied calibrated pair relation, a declared curve in its image,
regular stationary R17 branch, and matched middle state. A pair metric from one map and transport
along an unrelated path do not form this assembled object. It is not the physical observer arrow
and not a complete encoding of the spacetime embedding or all metric jets.

## 2. Unique three-channel decomposition of the pair metric

On the regular pair-metric stratum

```text
h00<0, det(h)<0,
```

the terminal audit proves the unique decomposition

```text
h=-T^2(dy0+beta dy1)^2+L^2(dy1)^2,

T^2=-h00,
beta=h01/h00,
L^2=h11-h01^2/h00,
```

with `T,L>0`. Write

```text
T=sigma exp(-phi),
L=sigma exp(+phi),
sigma>0.
```

Then

```text
kappa=log sigma=(1/4)log(-det h),
phi=(1/4)log[(-det h)/h00^2].
```

Conversely,

```text
h00=-exp(2kappa-2phi),
h01=-beta exp(2kappa-2phi),
h11=exp(2kappa+2phi)-beta^2 exp(2kappa-2phi).
```

The Jacobian of `(kappa,phi,beta)->(h00,h01,h11)` is exactly

```text
-8 exp(6kappa-2phi),
```

which never vanishes on the regular stratum. Thus the three coordinates are not an ansatz or a
linearized split. They are a global coordinate system on each connected calibrated regular
pair-metric fiber.

This refines the prior reciprocal-only framing. `phi` is the unique reciprocal coordinate, but it
is not the whole pair metric. `kappa` was previously invisible to the reciprocal ratio because
common scale cancels from that ratio. With strong local CSN inactive and the physical tape
calibrated by `c_E`, cancellation does not authorize deleting `kappa` from the complete state.

## 3. Two exact real characters, not one

For two matched calibrated states let

```text
b1=log[T(q)/T(p)],
b2=log[T(q)L(q)/(T(p)L(p))].
```

Using `T=exp(kappa-phi)` and `L=exp(kappa+phi)` gives

```text
b1=Delta_kappa-Delta_phi,
b2=2 Delta_kappa.
```

Therefore

```text
Delta_kappa=(1/2)b2,
Delta_phi=(1/2)b2-b1.                              (1)
```

Norm and area ratios telescope through a matched intermediate state, so both coordinates obey

```text
Delta_kappa(2,0)=Delta_kappa(2,1)+Delta_kappa(1,0),
Delta_phi(2,0)=Delta_phi(2,1)+Delta_phi(1,0).        (2)
```

The reciprocal-root character is exactly the second linear combination in (1). The first is the
common-scale character that reciprocal normalization intentionally cancels. The metric supplies
both after the pair relation and its calibration are supplied.

This does not restore strong CSN or claim that common scale is a new force. It simply preserves a
piece of the pair metric that the reciprocal projection does not measure.

## 4. Shift is an independent state channel

The founding pair-relation audit supplies the exact flat calibrated family

```text
h_q=[[-1,-q],[-q,1-q^2]],
det h_q=-1.
```

For every real `q`,

```text
sigma=1,
phi=0,
beta=q.
```

Thus neither common-scale density nor reciprocal depth reconstructs the event-pairing shift. A
local tape shear can remove a displayed cross term only by changing the declared event pairing or
ruler evolution. On a supplied calibrated pair query that is a different comparison, not a free
endpoint-frame gauge.

Under ruler-orientation reversal `beta` reverses sign. It is therefore an orientation-typed query
state. It does not have a standalone additive law under arbitrary comparison composition; the full
pair map or its Jacobian must be retained.

## 5. Angular transport is a different mathematical species

For a supplied path `gamma:p->q`, the projected metric connection gives

```text
U_gamma:H_p->H_q,
U_(gamma2 o gamma1)=U_gamma2 U_gamma1,
U_(gamma^-1)=U_gamma^-1.
```

This is an isometry between endpoint screen fibers. In oriented local screen frames it is an
`SO(2)` matrix, but an open-path matrix is endpoint-gauge covariant rather than a real scalar.
Closed-loop or two-path relative holonomy is representative-free up to the appropriate
orientation/conjugacy typing.

The constant-depth control has

```text
Delta_phi(loop)=0,
F23=-4097/2048 !=0.
```

Therefore reciprocal depth cannot reconstruct angular return. Conversely independent endpoint
screen rotations can change the matrix representing an open `U_gamma` while leaving every real
density character fixed. The two channel types are irreducible.

The only continuous real character of the local `R x SO(2)` depth/rotation group normalized on the
reciprocal factor remains `Delta_phi`. That theorem does not erase `U_gamma`; it proves that
angular information cannot be faithfully squeezed into an additive real number.

## 6. Exact composition of the assembled arrow shadow

On matched stationary R17 objects with fixed `lambda`, all arising from one declared calibrated
pair map and composable curves in its image, define the arrow shadow

```text
K(gamma)=(Delta_kappa(gamma),Delta_phi(gamma),U_gamma).
```

Then

```text
K(gamma2 o gamma1)
 =(Delta_kappa_2+Delta_kappa_1,
   Delta_phi_2+Delta_phi_1,
   U_2 U_1).                                      (3)
```

The connected order-zero structure is direct product. A continuous depth-driven semidirect action
on `SO(2)` is impossible because continuous automorphisms of `SO(2)` form the discrete two-element
set `{identity,inversion}`. Orientation reversal may invert the angular channel, but it is a
separate discrete/local-system operation.

The complete R17 coframe fixes how the reciprocal depth is represented on screen vectors and
covectors:

```text
screen vectors:   exp(-lambda Delta_phi) U_gamma,
screen covectors: exp(+lambda Delta_phi) U_gamma.   (4)
```

Equation (4) is reconstructed from `Delta_phi`, `U_gamma`, the tensor variance, and the supplied
object label `lambda`. It is not an additional independent channel. The screen-alignment bitorsor
is likewise composition infrastructure: it balances intermediate gauge and selects no physical
phase.

## 7. Four exact omission witnesses

The retained roles are minimal for reconstructing the declared banked pair-metric and angular
transport layers:

1. **Omit common scale.** `diag(-1,1)` and `diag(-4,4)` have the same `phi=0` and `beta=0`, but
   different `sigma=1,2`.
2. **Omit reciprocal depth.** `diag(-1,1)` and `diag(-1/4,4)` have the same `sigma=1` and `beta=0`,
   but different `phi=0,log 2`.
3. **Omit shift.** The flat family in section 4 has identical `sigma=1`, `phi=0` for all `q`, but
   different `beta=q`.
4. **Omit angular transport.** The zero-depth curved normal loop has unchanged endpoint scalar
   state and nontrivial angular return.

This is a bounded minimality theorem. It does not claim that `(kappa,phi,beta,U)` reconstructs the
pair-map embedding, extrinsic curvature, all complete-coframe jets, or a physical matter response.

## 8. Where mixing and the G52 one-forms belong

Complete clock/screen and ruler/screen mixing acts upstream by changing the pullback pair metric.
For the first exact mixed Jacobian,

```text
h=[[-3/16,0],[0,4]],
det h=-3/4.
```

Both common scale and reciprocal depth differ from the pure block readout. For the second,

```text
h=[[-3/16,1/12],[1/12,37/9]],
det h=-7/9,
beta=-4/9,
L^2=112/27.
```

Thus mixing need not be promoted to an extra scalar channel: it modulates several established
pair-metric channels together. A separately owned mixing observable could still exist, but no
current query or dynamics selects one.

The G52 families

```text
dphi+c H*dphi,
dphi+c dJ
```

are therefore classified as unselected scalarizations or microphone settings, not irreducible
members of the minimal banked assembly. Their arbitrary coefficient remains evidence that no
local scalar microphone is selected. They may later acquire operational meaning, but that would
require the open query/measurement owner.

Likewise:

- unit clock/ruler forms type the local state;
- the connection potential is gauge representative;
- curvature is the infinitesimal field strength controlling angular transport;
- strain spectra are useful arrow diagnostics but not compositional characters; and
- `lambda`, causal type, rank, orientation and relation-family identity are object/domain data.

## 9. Geometric activity strata, not yet physical regimes

The complete metric already permits distinct channel-activity patterns:

| Stratum | Active pattern |
|---|---|
| coincidence | all normalized/trivial |
| pure reciprocal pair metric | reciprocal depth only |
| common-scale control | common scale only |
| flat event-pairing family | shift only |
| zero-depth curved loop | angular holonomy only |
| pair-pure `H*dphi=0` | G52 screen-gradient scalarizations vanish; other channels may survive |
| complete mixed pair map | common scale, reciprocal depth and shift can change together |
| flat normal connection | local angular carry may descend, while wound holonomy can survive |
| generic stationary R17 | full path-labelled `SO(2)` angular channel |
| null/degenerate pair cell | regular channel decomposition fails or diverges |

This proves that different channel combinations can dominate or disappear geometrically. It does
not identify any row as microscopic, terrestrial, solar, or cosmological. That assignment needs a
physical pair map, on-shell branch/profile, and scale calibration. No hand threshold or switch is
introduced.

## 10. Calibration and the possible “conductor”

The current roles are sharply separated:

- `c_E` calibrates `y0=c_E tau_A` and the A-ruler tape. It normalizes the ordinary reciprocal
  reading but does not select `h`, `beta`, `U_gamma`, a path, or a branch.
- `G_obs` has no active role until a native curvature-to-mass readout exists.
- electron mass `m_e` remains a legitimate future observational normalization candidate after a
  native stable mass branch is independently identified. It is not used here.
- `hbar` is absent.

No single director is derived. The off-shell complete metric determines the available channel
values after a pair map and path are supplied. The observer query determines what comparison is
made. A future on-shell/global/bootstrap rule may select the realized metric, profile, branch, and
admissible query family. The present audit neither requires nor derives that larger owner.

## 11. Bounded landing

```text
REGULAR_CALIBRATED_PAIR_METRIC_HAS_UNIQUE_COMMON_SCALE_RECIPROCAL_DEPTH_AND_SHIFT_CHANNELS__
MATCHED_COMMON_SCALE_AND_RECIPROCAL_LOG_DENSITIES_COMPOSE_ADDITIVELY__
NORMAL_ANGULAR_TRANSPORT_COMPOSES_AS_A_DISTINCT_PATH_GROUPOID_ARROW__
COMPLETE_R17_SCREEN_WEIGHT_IS_A_DERIVED_REPRESENTATION_NOT_AN_EXTRA_CHANNEL__
G52_COEFFICIENT_FAMILIES_ARE_UNSELECTED_SCALARIZATIONS_NOT_CORE_CHANNELS__
CONDITIONAL_MINIMAL_STATE_DECORATED_MULTICHANNEL_ASSEMBLY_DERIVED_FOR_BANKED_R17_KINEMATICS__
GEOMETRIC_ACTIVITY_STRATA_DERIVED__PHYSICAL_REGIME_MAP_QUERY_PATH_PHYSICAL_ARROW_AND_
ON_SHELL_GLOBAL_BOOTSTRAP_SELECTION_OPEN.
```

No action, source, matter, mass, stability theorem, bootstrap closure, physical regime assignment,
universal mixed-geometry `c_eff`, `X_max` value, CMB observable, signalling law, or dynamics follows.
