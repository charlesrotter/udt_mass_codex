# Exact registered-branch distance-profile compatibility derivation

## 1. This is an overlay, not another branch census

The prior complete census already contains:

```text
12 finite-cell completion rows
28 equation/evidence families
3 calculated transnormal controls
0 complete clock/angular/event-pair/global-diameter witnesses
```

Those classifications are replayed unchanged. No pieces from separate
families are spliced into a new branch.

## 2. Three exact bounded profile structures

Normalize each bounded one-sided profile to run from zero to one.

### Projective reciprocal display

```text
P_t(phi) = tanh(phi)
B_t(phi) = cosh(phi)^4/Dmax^2
1-P_t ~ 2 exp(-2phi)
```

This is exact given the anchored projective interpretation. It is not
selected as physical proper distance.

### WR-L local proper-distance slice

```text
P_e(phi) = 1-exp(-phi)
B_e(phi) = exp(2phi)/Dmax^2
1-P_e = exp(-phi)
```

This is an exact conditional local clock-depth profile. The supplied slice
does not contain a complete global observer-pair diameter.

### Conditional round `B19` angular-depth branch

For every finite positive relative depth unit `kappa`,

```text
P_r(phi;kappa) = (2/pi) atan[sinh(2 kappa phi)]
B_r(phi;kappa) = cosh(2 kappa phi)^2/(b^2 kappa^2)
1-P_r = (4/pi) atan[exp(-2 kappa phi)]
           ~ (4/pi) exp(-2 kappa phi).
```

At `kappa=1`, this branch has the same endpoint exponent `2` as the
projective `tanh` profile. It is nevertheless a third distinct function.
Its `phi` is angular reciprocal depth and its clock lapse is constant.

## 3. Exact inequivalence under constant depth rescaling

For an endpoint-normalized profile `P`, define origin-shape invariants

```text
J2 = P''(0)/P'(0)^2,
J3 = P'''(0)/P'(0)^3.
```

These are unchanged by any positive constant replacement
`phi -> a phi`. The three profiles give

| profile | `J2` | `J3` |
|---|---:|---:|
| projective `tanh` | `0` | `-2` |
| WR-L exponential | `-1` | `1` |
| round `B19`, every `kappa>0` | `0` | `-pi^2/4` |

Therefore all three are pairwise inequivalent under a positive constant
depth-unit change. In particular, the shared `exp(-2phi)` endpoint rate of
the unit-`kappa` projective and round profiles does not make them the same
law.

The same conclusion follows from two simpler incompatible requirements.
Matching the round normalized origin slope to either unit-slope profile
requires

```text
kappa = pi/4.
```

Matching the projective endpoint exponent requires `kappa=1`; matching the
WR-L endpoint exponent requires `kappa=1/2`. No positive `kappa` satisfies
either pair of requirements.

## 4. Why the open toric family does not select

For the reciprocal-toric `FC12` control,

```text
B=1/A(phi)^2,
D(phi)=integral A(phi)dphi.
```

It can reproduce every listed profile by choosing:

```text
A_t = Dmax sech(phi)^2
A_e = Dmax exp(-phi)
A_r = b kappa sech(2 kappa phi)
A_linear = L
A_fullframe = L exp(phi).
```

No registered equation selects any of these `A` functions. This is exact
compatibility by choice, not derivation or branch selection. Its angular
common factor and global completion also remain necessary for a diameter.

## 5. What the complete registry says

- WR-L co-locates clock depth and a local exponential proper-distance
  profile, but lacks complete angular/global observer-pair geometry.
- `B19` co-locates a conditional complete round spatial metric, angular
  reciprocal depth, and calculable diameter, but has constant lapse.
- `FC12` supplies a complete metric form with free radial and angular
  profiles, but no selected equation or endpoint.
- The other finite-cell rows and equation families do not supply a common
  calculable witness.

Thus the exact profile-extraction machinery is not the missing object.
The missing object remains one coherent metric branch carrying the founding
clock depth, complete angular/global geometry, event pairing, and global
diameter.
