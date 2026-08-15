# Exact correction — all instruments live does not by itself select the score

Date: 2026-08-14

Preregistered in commit: `ef881e7a`

## Corrected terminology

The original G90 flat and monotone families were **explicit complete lifts**, not fully live
orchestras. They varied `B,S` while fixing `Q=I,Y=I,Z=0`. The original quiet-middle family varied
`Q,S` while fixing `Y=I,Z=0`.

The phrases **fully live flat**, **fully live monotone**, and **universal quiet-middle falsified in
the declared fully live class** are withdrawn. They overstated what those first witnesses tested.

## Stricter test

The correction preregistered a C2 contribution-live class. At the rational control point `t=1`, it
requires:

- `dot B,dot Q,dot S,dot Y,dot Z` all nonzero;
- all four entries of `dot S` nonzero;
- the five separately differentiated contributions `H_B,H_Q,H_S,H_Y,H_Z` to `dot h` all nonzero;
- exact `dot h=H_B+H_Q+H_S+H_Y+H_Z`;
- live ambient metric `dot g`, both base and screen pair columns, regular rank-two pair metric, and
  a nonidentity live chart overlap.

This is stricter than merely retaining all symbols. It remains conditional on the declared
triangular coframe and pair calibration and therefore is not called a gauge-independent dynamics.

## General factorization

For any supplied regular complete coframe history

```text
E(t)=[[B,0],[Q S,Q]]
```

and any supplied regular target pair coframe

```text
V_*(t)=[U_*(t);A_*(t)],
```

define

```text
J(t)=E(t)^-1 V_*(t)=[Y(t);Z(t)].
```

Then exactly

```text
E J=V_*,
h=J^T E^T eta_4 E J=V_*^T eta_4 V_*.
```

Equivalently,

```text
Y=B^-1 U_*,
Z=Q^-1 A_*-S Y.
```

This theorem is the decisive type result. Until a physical query/history law owns `J`, nonzero
activity of every factor cannot select the terminal response: a live realization can coherently
carry any regular target pair coframe.

The construction is not promoted to a physical mechanism. It exposes the remaining ownership
freedom.

## Exact all-active witnesses

All three witnesses use

```text
sigma=1+t/31,
beta=t/37,
B=[[sigma/t,sigma beta/t],[0,sigma t]],
Q=[[1+t/7,t/11],[0,1+t/13]],
S=[[t/17,t^2/19],[t^3/23,t^4/29]].
```

Thus `B,Q,S` vary, every entry of `S` varies, and the induced `Y,Z` from the exact factorization also
vary. At `t=1`, every registered C2 contribution norm is a strictly positive rational number in
`ALL_INSTRUMENTS_LIVE_DERIVATION_RESULT.json`.

The target coframe uses rational timelike and spacelike norm parametrizations, keeping both screen
columns and both base columns nonzero.

### C2 flat modulation

Choose target pair scales

```text
T_pair=t^-1,
L_pair=t.
```

Then

```text
h=diag(-t^-2,t^2),
phi_pair=log t=phi,
M_terminal=phi_pair-phi=0.
```

The normalized trace is also exactly constant. Every C2 activity gate passes at `t=1`, and by
continuity on an open neighborhood.

### C2 monotone modulation

Choose

```text
T_pair=t^-1,
L_pair=t^2.
```

Then

```text
h=diag(-t^-2,t^4),
phi_pair=(3/2)log t,
M_terminal=(1/2)log t,
```

which is strictly increasing. Every C2 activity gate again passes.

### C2 loud-quiet-loud

On `1/2<t<3/2`, define

```text
w=(t-1/2)(3/2-t),
T_pair=t^-1,
L_pair=t/w^2.
```

Then

```text
M_terminal=-log w.
```

It diverges at both ends and has a strict minimum at `t=1`. A separately varying screen ratio was
chosen so the independently preregistered normalized trace also diverges at both ends and has a
strict minimum at `t=1`. Every C2 activity gate passes.

## Exact overlap

For the nonidentity chart transition

```text
R(t)=[[1,t],[0,1]],
J_a=J_b R,
```

all three witnesses satisfy both

```text
h_a=R^T h_b R
```

and its complete first-derivative law, including both `dot R` terms.

## Landing

Primary:

```text
ALL_INSTRUMENTS_ACTIVITY_ALONE_DOES_NOT_SELECT_RESPONSE_SHAPE
```

Secondary:

```text
LOUD_QUIET_LOUD_SURVIVES_DECLARED_ALL_ACTIVE_CLASS
```

This does **not** mean that UDT physics selects flat or monotone behavior. It means the opposite:
mere activation of every kinematic instrument is still not the missing physical score. A native
law tying the complete metric history to the physical pair realization could exclude the
constructed cancellations; no such owner was used here.

## Evidence

- exact SymPy derivation: every registered check passes for all three families;
- independent NumPy assembly and finite-difference decomposition: every registered check passes;
- one valid baseline plus six hostile mutations catch frozen `Q,Y,Z`, one frozen `S` component, an omitted `H_Q`, and the
  promotion of one quiet survivor to universal selection.

No observational, `X_max`, bootstrap, action, source, matter, or signalling conclusion follows.
