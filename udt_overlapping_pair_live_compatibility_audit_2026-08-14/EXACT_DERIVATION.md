# Exact derivation — overlapping complete-pair live compatibility

Date: 2026-08-14

Scope: exact local overlap, shared-seam, middle-state, joint-Gram, and reciprocal-response
classification for supplied complete metric and pair families

## 1. Result first

The preregistered primary landing is

```text
OVERLAP_SUPPLIES_NONIDENTITY_SIMULTANEOUS_COMPATIBILITY_BUT_NOT_LIVE_REGIME_SELECTION
```

The secondary loud/quiet landing is

```text
LOUD_ENDS_QUIET_MIDDLE_CONDITIONAL_SURVIVOR_NOT_SELECTED
```

The complete metric does impose real consistency conditions when several pair relations are
claimed to coexist:

- genuine chart overlaps obey exact zero- and first-order gluing laws;
- a literally shared observer tangent fixes the shared clock entry;
- a literal common terminal state must match, or an explicit middle reset remains;
- every simultaneous tangent collection is one four-dimensional Lorentz Gram matrix, with rank at
  most four and negative index at most one.

These conditions reject inconsistent simultaneous assemblies. They do not select a live metric or
pair history. Exact explicitly lifted overlap-compatible histories exist with:

1. constant normalized orchestra loading and constant terminal modulation;
2. strictly monotone loading and modulation; and
3. a two-ended response with a quiet middle.

Thus the loud-ends/quiet-middle structure is genuinely present as a metric-native reciprocal
response family. It is not forced by overlap compatibility alone.

## 2. One supplied complete metric, many pair cells

Use the externally checked complete coframe and pair Jacobian

```text
E=[[B,0],[Q S,Q]],
J_alpha=[Y_alpha;Z_alpha],
V_alpha=E J_alpha,
h_alpha=V_alpha^T eta_4 V_alpha.
```

For every pair cell this retains all of `B,Q,S,Y_alpha,Z_alpha` before the terminal readout. The
ambient blocks are common only when the pair cells are declared to lie in the same coframe patch;
the pair Jacobians remain query-specific.

## 3. O1 — exact live chart gluing

Suppose two charts describe one supplied pair surface:

```text
F_alpha=F_beta o psi_ba,
R_ba=d psi_ba.
```

The chain rule gives exactly

```text
J_alpha=J_beta R_ba,
V_alpha=V_beta R_ba,
h_alpha=R_ba^T h_beta R_ba.                       (1)
```

When every object depends on a live parameter,

```text
dot J_alpha=dot J_beta R_ba+J_beta dot R_ba,
dot V_alpha=dot V_beta R_ba+V_beta dot R_ba,       (2)

dot h_alpha
 =R_ba^T dot h_beta R_ba
  +dot R_ba^T h_beta R_ba
  +R_ba^T h_beta dot R_ba.                         (3)
```

On a triple overlap, transition Jacobians compose. Production symbolic algebra and a separate exact
Fraction replay verify (1)--(3), including a nonidentity live shear

```text
R(t)=[[1,t],[0,1]].
```

Omitting either `dot R` term produces the exact residual

```text
[[0,-3/4],[-3/4,-9/4]]
```

on the hostile witness. Equations (1)--(3) are nontrivial compatibility checks for proposed chart
data, but they are identities after one arbitrary smooth `E,J_beta,R_ba` has been supplied. They do
not restrict the arbitrary base history.

## 4. O2 — sharing an observer does not fix the complete pair

At one Minkowski event take

```text
u =(1,0,0,0),
r1=(0,1,0,0),
r2=(0,2,1,0),
J1=[u,r1],
J2=[u,r2].
```

Both pair planes are regular and share the exact same calibrated clock tangent. Their pullbacks are

```text
h1=[[-1,0],[0,1]],
h2=[[-1,0],[0,5]].                                 (4)
```

Therefore

```text
(h1)00=(h2)00=-1,
phi1=0,
phi2=(1/4)log(5).                                  (5)
```

The metric derives the shared clock entry. It does not derive a shared ruler, cross term, or
terminal depth merely from the fact that two pair surfaces meet the same observer. A complete
common pair state is a stronger gluing condition.

## 5. O3 and O4 — middle matching versus path holonomy

For independently rebuilt middle terminal coframes

```text
B_in =[[2,1],[0,3]],
B_out=[[1,1/2],[0,4]],
```

the exact reset is

```text
M_B=B_out B_in^-1=diag(1/2,4/3).                   (6)
```

For the registered outer arrows, including (6) gives

```text
R_BC M_B R_AB=[[1,-4/9],[0,2]],
```

while silently using identity gives

```text
R_BC R_AB=[[2,-1/18],[0,3/2]].                     (7)
```

Thus exact common-middle matching is a real simultaneous compatibility condition. Neither `c_E`
nor endpoint decomposition selects `M_B` when the two middle objects were independently rebuilt.
Path-labelled direct and composite arrows may also differ by lawful holonomy; this audit does not
impose universal flat descent.

## 6. The joint ambient Gram law

Collect every simultaneously retained tangent vector into one `4 x m` matrix `mathcal J`. Their
complete mutual Gram matrix is

```text
mathcal K=mathcal J^T g mathcal J
         =(E mathcal J)^T eta_4(E mathcal J).       (8)
```

Consequently

```text
rank(mathcal K)<=4,
negative_index(mathcal K)<=1.                      (9)
```

Every `5 x 5` Gram determinant therefore vanishes. Literal shared columns impose literal equality
of the associated rows and entries.

The exact five-vector witness

```text
mathcal J=[e0,e1,e2,e3,e0+e1]
```

has

```text
rank(mathcal K)=4,
det(mathcal K)=0,
inertia(mathcal K)=(negative,positive,zero)=(1,3,1). (10)
```

By contrast, the abstract target `diag(-1,1,1,1,1)` has rank five and determinant `-1`; it cannot
be the joint Gram data of five tangent channels in one four-dimensional metric even though many of
its `2 x 2` restrictions are individually regular.

Equations (8)--(10) are the nonidentity result of this audit: the metric constrains which pair cells
can coexist as one simultaneous assembly. They do not constrain the arbitrary smooth history of a
realizable `E mathcal J`; any such history automatically retains the same rank/inertia laws.

## 7. LQ1 — fixed reciprocal-response control

On the invertible-`Y`, A-calibrated quotient write

```text
B=[[T,T beta],[0,L]],
T=sigma exp(-phi),
L=sigma exp(+phi),
P=[[a,d],[d,e]]>=0,
n_beta=e-2 beta d+beta^2 a,
Pi=B^-T P B^-1.
```

The fixed-`P,sigma,beta` trace control is

```text
A_trace
 =[a exp(+2phi)+n_beta exp(-2phi)]/sigma^2.        (11)
```

If both projections are nonzero, `a>0` and `n_beta>0`, then

```text
partial_phi A_trace
 =2[a exp(+2phi)-n_beta exp(-2phi)]/sigma^2,

partial_phi^2 A_trace=4 A_trace>0,

phi_star=(1/4)log(n_beta/a).                       (12)
```

Thus the trace control has one strict quiet middle and grows toward both algebraic reciprocal ends.
This covers rank two and rank one with both projections present. If only one projection survives,
the response is one-sided. `P=0` is silent.

### 7.1 Terminal modulation, not only the trace

Define

```text
x=a exp(2phi)/sigma^2,
y=n_beta exp(-2phi)/sigma^2,
z=(d-beta a)/sigma^2,
q=xy,
Delta=xy-z^2=det(P)/sigma^4.
```

On the regular A-clock domain `0<x<1`, the terminal modulation is

```text
M_terminal=phi_pair-phi
 =(1/4)log{[1-Delta+y-x]/(1-x)^2}.                 (13)
```

It diverges at both ends of the regular two-projection domain:

- as `x->0`, `y=q/x->infinity`;
- as `x->1^-`, the denominator vanishes; when `z=0` the numerator loses only one factor and the
  ratio still diverges.

The stationary numerator is the cubic

```text
f(x)=-x^3+(1-2Delta)x^2+3qx-q.                    (14)
```

It obeys

```text
f(0)=-q<0,
f(1)=2(q-Delta)=2z^2>=0,
f'(x)=-3x^2+2(1-2Delta)x+3q.                      (15)
```

The two roots of `f'` have product `-q<0`, so exactly one is positive. Hence `f` first increases
and then decreases on the positive axis. Equations (15) and the positive-domain boundary signs
give exactly one interior zero; when `z=0`, `x=1` is an additional boundary root and the interior
root remains unique. The terminal modulation therefore also has one interior minimum.

Its minimum need not occur at the trace minimum. The meaning of “quiet middle” is robust on the
fixed-response two-projection slice, while its exact location is readout-dependent.

Boundary strata are exact:

- `a=0` forces `d=0`: `M=(1/4)log(1+y)`, ruler-side only;
- `n_beta=0` forces `z=0`: `M=-(1/4)log(1-x)`, clock-side only;
- `P=0`: `M=0`.

## 8. LQ2/LQ3 — explicit lifted histories (terminology corrected)

**Correction:** the three original constructions below are explicit complete lifts, but they are
not all-instruments-live histories. The flat and monotone families fix `Q,Y,Z`; the quiet-middle
family fixes `Y,Z`. Their algebra remains valid, but the phrases “fully live” and “universal
quiet-middle falsified in the declared fully live class” are withdrawn. The preregistered stricter
test and exact replacement witnesses are in `ALL_INSTRUMENTS_LIVE_CORRECTION.md`.

Set

```text
t=exp(phi)>0,
B(t)=diag(1/t,t),
Q=I,
Y=I,
Z=0.
```

Every family below is a complete explicit `Q,S,Y,Z` lift, not an invented scalar `P(t)`.

### 8.1 Flat response with live mixing but fixed `Q,Y,Z`

Choose

```text
S(t)=(1/2)B(t).
```

Then

```text
P=S^T S=(1/4)B^T B,
Pi=(1/4)I,
A_trace=1/2,

h=diag[-3/(4t^2),5t^2/4],
det(h)=-15/16,
M_terminal=(1/4)log(5/3).                          (16)
```

The family is regular for every `t>0`; `S` is genuinely live. With the nonidentity chart overlap
`R(t)=[[1,t],[0,1]]`, equations (1)--(3) hold exactly. It has neither loud ends nor a distinguished
quiet middle.

### 8.2 Strictly monotone response with fixed `Q,Y,Z`

Choose

```text
s(t)=(2t+1)/[4(t+1)],
S(t)=s(t)B(t).
```

Then `0<s<1/2`, so the pair metric remains regular, and

```text
Pi=s(t)^2 I,
A_trace=(2t+1)^2/[8(t+1)^2],

dA_trace/dt=(2t+1)/[4(t+1)^3]>0.                  (17)
```

The exact terminal derivative is

```text
dM_terminal/dt
 =16(t+1)(2t+1)
  /[(2t+3)(6t+5)(20t^2+36t+17)]>0.                (18)
```

Thus both preregistered readouts are strictly monotone on an explicitly lifted regular history.

### 8.3 Quiet-middle survivor with `Q` and `S` both live

Choose

```text
Q(t)=diag(t,1/t),
S(t)=diag[1/(2t),t/2].
```

Both instruments vary, while

```text
Q S=(1/2)I,
P=(1/4)I,

A_trace=(t^4+1)/(4t^2)
       =(1/4)(t^2+t^-2).                           (19)
```

Equation (19) has a strict minimum at `t=1`. The regular terminal branch is `0<t<2`; its terminal
modulation diverges toward `t->0` and `t->2^-` and has one interior minimum by the fixed-response
proof. Independent samples reproduce the middle depression in both readouts.

This proves the desired architecture remains admissible after the uncompressed and overlap
corrections. Equations (16)--(18) prove it is not selected by those corrections.

## 9. What overlap accomplished

Overlap did not merely return “anything goes.” It supplied a hierarchy:

```text
one pair cell       -> complete terminal evaluator;
one surface overlap -> exact live chart gluing;
one observer seam   -> shared-clock constraint;
one common network  -> exact middle-state matching/reset typing;
many simultaneous tangents -> 4D Lorentz Gram rank/inertia constraints.
```

These are useful building rules for a coherent observer network. They reduce inconsistent
assemblies, but every one is satisfied by infinitely many smooth complete histories, including the
flat, monotone, and quiet-middle families above.

## 10. Ownership and conclusion ceiling

Premise-stamped result:

- overlap/gluing and joint-Gram laws: `DERIVED CONDITIONAL` on supplied overlap types;
- fixed-response two-ended quiet-middle theorem: `DERIVED CONDITIONAL CONTROL`;
- quiet-middle live family: `DERIVED/OBSERVED CONDITIONAL SURVIVOR`;
- universal quiet-middle selection from overlap/activity: `NOT DERIVED`; the original
  all-instruments wording was overbroad, while the correction independently proves that C2
  activity alone permits flat, monotone, and quiet-middle families;
- physical complete history, pair family, regime locations, and any scalar `mu`: `OPEN`;
- `X_max`, observations, dynamics, action, source, matter, and bootstrap: inactive.

No statement here rejects the physical loud-ends/quiet-middle hypothesis. It identifies the exact
additional burden: a later owner must distinguish the quiet family from equally compatible flat
and monotone histories without inserting the desired pattern.
