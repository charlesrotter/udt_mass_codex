# Exact derivation — R17 magnitude-to-grading selection

Date: 2026-08-10

Mode: metric-led, exact analytic/CPU

Current grade: **VERIFIED-WITH-CAVEATS; CORRECTED EXTERNAL REVIEW ACCEPTED**

## 1. Result first

The R17 selection seam splits into two mathematically different joints.

Conditional on each supplied complete R17 off-shell coframe C01--C06, the founding reciprocal character and the
branch-owned endpoint magnitude force the clock/ruler part of a nonzero vertical calibration lift.
The complete R17 coframe then fixes the symmetric screen scaling to that configuration's supplied
`lambda`. The resulting projector-preserving vertical **metric** lift is

```text
L_p(delta)=exp(delta X_lambda(p)),
X_lambda=-P_u+P_n+lambda H,
```

unique modulo the already-known `SO(2)` screen-rotation presentation freedom.

This does not select a raw complete observer arrow. The physical path/query, isometric carry,
carried-to-intrinsic reset, and integrated pair surface remain open. The previously audited full
semidirect formula remains a lawful conditional assembly, not a branch-selected physical law.

Accepted conditional landing:

```text
COMPLETE_COFRAME_CONDITIONAL_VERTICAL_RECIPROCAL_METRIC_CLASS_MOD_SO2__
FULL_PHYSICAL_ARROW_OPEN
```

## 2. The type split that removes the false zero/nonzero fork

There are three distinct objects:

1. a metric-compatible transport `U_gamma`, which carries geometry and holonomy but has zero
   reciprocal magnitude;
2. a vertical calibration action `L_p(delta)` inside an already supplied enriched source state;
3. a cross-fibre physical observer arrow, which must combine vertical calibration with a typed
   source-to-target relation.

The identity is a valid zero-magnitude transport or vertical action at `delta=0`. It is not a
realization of the founded character at nonzero `delta`. Calling identity and
`exp(delta X_lambda)` two competing lifts of the same nonzero depth was therefore a type error.

## 3. What founding Reciprocity fixes

On the abstract clock/ruler channels, the founded action is

```text
D(delta)=diag(exp(-delta),exp(+delta)).
```

R17 supplies intrinsic projectors `P_u` and `P_n` soldering those abstract channel labels to one
timelike clock line and one twist-selected spacelike ruler line. Therefore any vertical lift that
claims to realize the branch-owned nonzero `delta_K` must restrict to

```text
exp(-delta_K) P_u + exp(+delta_K) P_n.
```

The zero lift fails this normalization whenever `delta_K != 0`.

Founding Reciprocity alone says nothing about the screen. A smooth projector-preserving lift may
have

```text
Y=-P_u+P_n+B_H
```

with a free screen generator `B_H`. Smooth exact composition makes the lift a one-parameter
representation `L(delta)=exp(delta Y)`, but it does not by itself determine `B_H`.

Thus the pair-only theorem is deliberately weaker:

```text
CLOCK_RULER_WEIGHTS_FIXED__SCREEN_RESPONSE_OPEN.
```

## 4. What the complete R17 coframe adds

The complete branch coframe has the exact finite factor

```text
F_lambda(phi)
 =exp(-phi)P_u+exp(+phi)P_n+exp(lambda phi)H
 =exp(phi X_lambda).
```

On R17 the same metric owns

```text
delta_K(p,q)=log[N(p)/N(q)]=phi(q)-phi(p).
```

Consequently the relative finite factor is the exact quotient

```text
F_lambda(phi(q)) F_lambda(phi(p))^-1
 =F_lambda(phi(q)-phi(p))
 =exp(delta_K(p,q) X_lambda).
```

No Taylor approximation enters.

The six configurations carry the already supplied values

```text
lambda in {-2,-1,0,1/2,1,2}.
```

This audit does not select one value across the family. It applies configuration by configuration.

## 5. Exact uniqueness class on the screen

Let the screen block of a smooth projector-preserving generator be

```text
B=[[b11,b12],[b21,b22]].
```

Reproducing the complete R17 metric response requires

```text
B+B^T=2 lambda I.
```

Exact solution gives

```text
B=lambda I+wJ,
J=[[0,-1],[1,0]],
```

for one real constant `w`. Since `I` and `J` commute,

```text
exp(delta B)=exp(lambda delta) R(w delta).
```

The rotation `R` is an `SO(2)` isometry of the positive screen, commutes with the reciprocal lift,
and changes neither the induced metric nor the terminal reciprocal density. It is precisely the
screen phase already classified by the alignment bitorsor.

Therefore:

- the raw coframe lift is not unique under endpoint-frame covariance;
- the projector-preserving vertical **metric** lift is unique modulo `SO(2)` screen rotation; and
- fixing named `sigma_1,sigma_2` axes would set `w=0` only as a coframe-representative choice, not a
  metric-natural physical selection.

An arbitrary screen scale `a != lambda` still reproduces the founded clock/ruler block, but changes
the complete metric screen factor from `exp(2 lambda delta)` to `exp(2 a delta)`. It therefore
fails the complete-coframe realization gate.

## 6. Composition, reversal, and terminal compatibility

Because `X_lambda` is fixed at the source enriched state,

```text
L(delta_2)L(delta_1)=L(delta_1+delta_2),
L(-delta)=L(delta)^-1,
L(0)=I.
```

For the exact witness `exp(delta)=2`, `lambda=1/2`, the density arguments are

```text
(rho_1,rho_2,Q)=(1/4,1,16),
```

so both the reciprocal-root and normalized terminal pair readouts return `delta=log 2`.
Screen rotation leaves all three values unchanged.

This is compatibility of the vertical factor with already-banked terminal algebra. It is not a
universal mixed-geometry `c_eff` theorem.

## 7. Why the complete physical arrow remains open

To turn the source-fibre factor into a cross-fibre arrow one may write, conditionally,

```text
A_gamma=U_gamma exp(delta_K X_p).
```

The earlier R17 audit proves this formula composes exactly when the target state is the carried
state. Nothing in the present derivation selects:

- one physical path or path family;
- Levi-Civita carry as the physical observer comparison;
- equality of the carried grading and the independently rebuilt intrinsic grading at the endpoint;
- one representative of the endpoint alignment bitorsor; or
- an integrated calibrated pair surface whose Jacobian is the displayed linear arrow.

Full R17 holonomy makes the carried and rebuilt gradings generically unequal. The alignment
bitorsor resolves projector-level existence and gauge composition, but its members are isometries
and generate no magnitude. These facts are retained, not erased.

Thus the present conditional result refines G42/G45 rather than reversing their ownership ruling:
inside a supplied complete R17 coframe, the vertical reciprocal metric action is fixed modulo
screen rotation. The complete coframe itself remains an off-shell branch input, and the full
physical semidirect observer arrow remains conditional.

## 8. Candidate classification

| Candidate | Founded pair | Complete R17 metric | Composition | Physical selection |
|---|---|---|---|---|
| identity at nonzero depth | fail | fail | pass | not a depth realization |
| `exp[delta(-P_u+P_n+aH)]` | pass | pass only at `a=lambda` | pass | screen open pair-only |
| `exp[delta(X_lambda+wJ)]` | pass | pass for all `w` | pass | one metric class; screen phase free |
| `U_gamma exp(delta X_p)` | pass conditionally | pass | pass on carried states | full arrow not selected |
| alignment bitorsor member | zero depth | isometric only | balanced composition | transport, not generator |
| supplied pair Jacobian | may pass | query dependent | type dependent | physical pair surface unowned |

## 9. Scope and maximum conclusion

This is one exact conditional kinematic tile: R17/W01 C01--C06, regular fixed-rank off-shell configurations,
with their supplied configuration values of `lambda`. It does not test an on-shell law, dynamics,
boundary conditions, topology selection, degenerate/null strata, or the other 23 branch identities.

No action, source, carrier, matter, mass, bootstrap return, `X_max` value, CMB spectrum, signalling
law, or GPU work follows.
