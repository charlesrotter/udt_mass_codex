# Exact derivation — complete-history regime-continuation ownership

Date: 2026-08-15

## 1. Landing

```text
PERMITTED_NOT_OWNED
```

The existing complete UDT equations admit lawful flat, monotone, and loud–quiet–loud regime
continuations. They do not select one of them. This is a constructive nonselection theorem on the
declared regular source universe, not a claim that every conceivable future UDT completion is
underdetermined.

## 2. The decisive factorization

For any supplied regular complete coframe history

```text
E(t)=[[B,0],[Q S,Q]]
```

and any supplied regular target pair coframe `V_*(t)`, define

```text
J(t)=E(t)^-1 V_*(t)=[Y(t);Z(t)].                 (1)
```

Then identically

```text
E J=V_*,
h=J^T E^T eta_4 E J=V_*^T eta_4 V_*.            (2)
```

Thus, while the physical pair realization `J` remains supplied, complete-coframe activity cannot
select a terminal pair history. A coordinated query realization can carry any regular target pair
coframe through any regular `E`.

This does **not** say that a physically owned query would remain arbitrary. For a fixed observer,
initial screen, geodesic rule, and metric history, the Jacobi problem can determine its own `J`.
Equation (1) proves only that current kinematic completeness or “all instruments active” is not the
missing joint. The theory still needs ownership of the physical history and query family or a law
relating them.

## 3. Three exact separating continuations

Use the same all-factor-live complete coframe

```text
sigma=1+t/31,
beta=t/37,
B=[[sigma/t,sigma*beta/t],[0,sigma*t]],
Q=[[1+t/7,t/11],[0,1+t/13]],
S=[[t/17,t^2/19],[t^3/23,t^4/29]].               (3)
```

Every `B,Q,S` block varies and every entry of `S` varies. Choose target pair coframes with nonzero
base and screen components and apply (1). The exact reconstruction verifies that `Y` and `Z` also
vary and that the resulting pair metrics are:

```text
flat:              h=diag(-t^-2,t^2),
monotone:          h=diag(-t^-2,t^4),
loud-quiet-loud:   h=diag(-t^-2,t^2/w^4),
w=(t-1/2)(3/2-t).                                 (4)
```

With base reciprocal coordinate `phi=log(t)`, the terminal modulation

```text
M=phi_pair-phi
```

is exactly

```text
flat:              M=0,
monotone:          M=(1/2)log(t),
loud-quiet-loud:   M=-log(w).                     (5)
```

The last family has one strict minimum at `t=1` and diverges as `t` approaches `1/2` or `3/2` from
inside. All three are regular at the shared control and satisfy the complete factorization. The
primary symbolic calculation proves the identities and derivative/limit statements. A separate
standard-library `Fraction` implementation independently reconstructs the matrices at
`t=3/4,1,5/4`, with exact fourth-power modulation samples:

```text
flat:              1, 1, 1
monotone:          9/16, 1, 25/16
loud-quiet-loud:   65536/81, 256, 65536/81.       (6)
```

## 4. Why each existing equation stops short

### Complete pullback and first variation

They compute `h`, `dot h`, `phi_pair`, and `dot phi_pair` after `E,J` are supplied. They are exact
evaluators, not equations for those histories.

### Maurer-Cartan, Cartan, and Bianchi

`dE E^-1` satisfies Maurer-Cartan identically for every smooth full-rank coframe. On a time-only
base there is no nonzero two-form, so it imposes no temporal restriction. Cartan constructs the
connection and curvature of a supplied metric; Bianchi is again an identity. No currently owned
response equation sets a curvature combination equal to a source or to zero.

### Overlap and joint-Gram laws

These are genuine coexistence constraints: charts must glue and simultaneous tangent collections
must fit one rank-at-most-four, index-at-most-one Lorentz Gram matrix. However, once `E,J` are a
realizable smooth assembly, all three histories in (4) retain those constraints. They reject bad
assemblies, not temporal shapes.

### Endpoint composition

`B_j B_i^-1` composes and the endpoint reciprocal character telescopes after one matched global
state family is supplied. It does not construct that family.

### Jacobi and holonomy channels

They derive propagation and transport on a supplied metric and typed query. They can sharply
distinguish histories after the history is supplied, but they are not an equation selecting the
metric history.

### Global completion

G85 demonstrates that regularity has real force but leaves multiple completion archetypes. The
registered global layer therefore does not collapse the local multiplicity to one history.

### Action, source, and bootstrap candidates

EH is `CONDITIONAL_NOT_SELECTED`; C2/Bach is inactive without the challenged strong-CSN premise;
the complete action/source/boundary law is open; bootstrap is a working, presently equation-free
hypothesis. None is an active history owner in this audit.

### G97 observation

G97 strongly disfavors one preselected control under provisional transfer. That is useful empirical
information, but it is applied after a history is supplied. It cannot be relabelled as the native
metric equation that generated the history.

## 5. Exact conclusion

The current structure does two different jobs well:

1. it defines which complete observer-pair histories are geometrically coherent; and
2. it evaluates their reciprocal, angular, Jacobi, and provisional observational outputs.

It does not perform the third job of choosing a physical complete history. The quiet-middle
continuation is a genuine metric-native survivor, not a selected solution. Flat and monotone
survivors prove the distinction.

The most economical forward step is therefore explicit rather than disguised: either find a new
source-owned nonidentity history/query law, or adopt a minimal observationally calibrated history
premise and reserve independent data for falsification. More kinematic completion scans cannot
manufacture the missing owner.
