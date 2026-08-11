# Exact derivation — causality in a co-present calibrated pair geometry

Date: 2026-08-10
Mode: metric-led, exact analytic/CPU
Preregistration commit: `86380447`
Pre-review grade: `LEAD`

## 1. Result first

On every supplied regular calibrated observer-pair family, the complete shifted Lorentzian cone
derives an exact causal interpretation of the reciprocal channel:

```text
cone center              = -beta,
centered cone half-width = L/T = exp(+2 phi_pair),
c_eff^(pair)/c_E         = T/L = exp(-2 phi_pair).
```

This identifies `phi_pair` as the logarithmic centered opening of the complete pair cone and
`beta` as its tilt. Time, angular, screen, shift, and mixing structure all enter through the full
induced pair metric before this reading is made.

Local causal preservation does not select a local transition or calibration on an already supplied
pair family. Local causal type is automatic for every regular pullback immersion. The full smooth
local time-oriented causal-isomorphism class retains two arbitrary monotone functions—independent
reparameterizations of the two null directions. Reciprocity, three-observer composition, `c_E`
anchoring at one observer, and both reciprocal asymptotes leave that functional freedom nonempty.
These witnesses do not by themselves prove that several ambiently distinct physical pair
immersions exist; the physical immersion/family remains an open construction problem.

Scoped landing:

```text
PAIR_CONE_DERIVES_EXACT_SHIFT_NEUTRAL_PHI_CEFF_JOIN_ON_A_SUPPLIED_CALIBRATED_FAMILY__
INDUCED_LOCAL_CAUSALITY_IS_AUTOMATIC__
SMOOTH_LOCAL_TIME_ORIENTED_CAUSAL_ISOMORPHISMS_RETAIN_INFINITE_NULL_REPARAMETRIZATION_FREEDOM__
RECIPROCITY_COMPOSITION_CE_ANCHOR_AND_BOTH_ASYMPTOTES_DO_NOT_SELECT_THE_LOCAL_TRANSITION_OR_
CALIBRATION_CLASS_ON_A_SUPPLIED_FAMILY__AMBIENT_PHYSICAL_FAMILY_GLOBAL_CAUSAL_FAITHFULNESS_AND_
ON_SHELL_OWNER_OPEN.
```

## 2. Complete shifted pair cone

On one supplied regular pair family use the already-derived decomposition

```text
h = -T^2(dy^0 + beta dy^1)^2 + L^2(dy^1)^2,
T>0, L>0,
y^0=c_E tau_A.
```

For a tangent direction written as

```text
v = r partial_0 + partial_1,
r = dy^0/dy^1,
```

the null equation is

```text
0 = h(v,v)
  = -T^2(r+beta)^2 + L^2.
```

Therefore the two exact inverse coordinate speeds are

```text
r_+ = -beta + L/T,
r_- = -beta - L/T.                                      (1)
```

Their center and half-width are

```text
C = (r_+ + r_-)/2 = -beta,
W = (r_+ - r_-)/2 = L/T.                                (2)
```

Equivalently, define the branch-specific direct coordinate speeds
`w_+ := (dy^1/dy^0)_+ = 1/r_+` and `w_- := (dy^1/dy^0)_- = 1/r_-`. Then

```text
(1/2)(1/w_+ - 1/w_-) = L/T.                             (3)
```

The already-derived terminal pair coordinate is

```text
phi_pair = (1/2)log(L/T).
```

Equations (2)--(3) now give the causal join directly:

```text
W = exp(2 phi_pair),
c_eff^(pair)/c_E := 1/W = exp(-2 phi_pair).              (4)
```

Thus the pair readout is not either one-way shifted coordinate speed. It is the inverse centered
opening of both null branches. The shift remains physical pair state but cancels from the balanced
reciprocal reading without being set to zero.

## 3. Complete orchestra and time dependence remain live

For a complete pair immersion `F:Sigma->M`,

```text
h_ij = g(F_*partial_i,F_*partial_j)
     = eta_ab V_i^a V_j^b.
```

Every complete-coframe column can contribute to `h`. On the regular stratum,

```text
phi_pair = (1/4)log[(-det h)/h_00^2],
beta     = h_01/h_00.
```

For any live direction `partial_a`, including physical pair time,

```text
partial_a phi_pair
  = (1/4)partial_a log(-det h) - (1/2)partial_a log(-h_00),

partial_a beta
  = (h_00 partial_a h_01 - h_01 partial_a h_00)/h_00^2. (5)
```

No time derivative or orchestra component is frozen in (5). This is an algebraically time-live
identity, not an on-shell time-live solution: no native evolution equation has been supplied.

An exact nonstationary screen-graph witness in ambient Minkowski geometry is

```text
F(t,s)=(t,s,q t s,0).
```

It gives

```text
h_00=-1+q^2 s^2,
h_01=q^2 t s,
h_11=1+q^2 t^2,
det h=-1-q^2 t^2+q^2 s^2.
```

On its regular domain, both `phi_pair` and `beta` depend on time and ruler position. This witness is
a solution-space counterexample to frozen/diagonal selection; it is not proposed as UDT dynamics.

## 4. What induced causality does—and does not—select

By definition of a pullback metric,

```text
h(v,v)=g(F_*v,F_*v).                                    (6)
```

Therefore a tangent vector is timelike, null, or spacelike on the pair surface exactly when its
image has that type in the complete geometry. Local causal preservation is automatic after a
regular timelike pair immersion `F` is supplied. Equation (6) does not choose `F`; infinitely many
regular timelike immersions can satisfy it.

There is a stronger global question. A causal curve lying in the pair surface is an ambient causal
curve, but the ambient geometry may contain additional causal curves that leave the surface and
return. Requiring the pair relation to reflect the complete ambient order is not automatic.
Causal convexity of the image is one sufficient condition, not a presently derived UDT rule and
not proven necessary for every possible query construction.

This yields a hierarchy:

1. induced tangent causal type — automatic;
2. causal-curve preservation into the ambient geometry — automatic;
3. ambient-order reflection / causal faithfulness — nontrivial and global;
4. material signalling — additionally requires a principal symbol, coupling, and admissible data.

Co-presence is whole-solution membership. It does not mean causal access, and it does not collapse
this hierarchy.

## 5. Full local causal-isomorphism class

Every smooth two-dimensional Lorentzian metric is locally expressible in null coordinates as

```text
h = -Omega^2(du tensor dv + dv tensor du).
```

Let a smooth invertible transition that preserves the cone in both directions have null-coordinate
Jacobian

```text
J = [[a,b],[c,d]].
```

Preserving the two null axes up to a positive conformal multiplier gives

```text
J^T [[0,-1],[-1,0]] J
 = [[-2ac, -(ad+bc)], [-(ad+bc), -2bd]].                (7)
```

The diagonal entries in (7) must vanish. Invertibility leaves exactly two local components:

```text
I.   b=c=0,  ad != 0,
II.  a=d=0,  bc != 0.                                  (8)
```

Integrability of the identity component gives the complete local form

```text
u' = f(u),
v' = g(v),
f'>0, g'>0                                             (9)
```

for time orientation and fixed null-branch orientation. The second component exchanges the null
branches:

```text
u'=f(v),
v'=g(u).                                               (10)
```

Thus the local causal-isomorphism family is infinite-dimensional. This class is narrower than
one-way cone-inclusion maps: causal preservation by a map whose inverse need not be causal is not
classified here. Composition and inversion are exact:

```text
(f_2,g_2)o(f_1,g_1)=(f_2 o f_1, g_2 o g_1),
(f,g)^-1=(f^-1,g^-1).                                  (11)
```

Equation (11) establishes a groupoid after domains and branch labels are retained. It does not
select `f` or `g`.

## 6. Calibration and Reciprocity do not remove the freedom

Fixing the ordinary calibration at one observer can impose

```text
f(0)=g(0)=0,
f'(0)=g'(0)=1.
```

The exact family

```text
f_epsilon(u)=u+epsilon u^3,  epsilon>=0,
g(v)=v
```

obeys those conditions, stays strictly monotone, and is nonidentity for every `epsilon>0`.
Consequently one-point `c_E` calibration leaves an infinite local transition/calibration family.
This family may still contain gauge-equivalent descriptions; it is not an ambient-immersion
multiplicity theorem.

Three distinct operations must not be conflated:

1. spatial orientation reversal exchanges the two geometric null branches and changes the sign of
   the cone tilt;
2. arrow inversion exchanges ordered endpoints and reverses the endpoint depth difference;
3. founding clock/ruler exchange is an abstract reciprocal-channel involution sending the signed
   reciprocal grading `delta -> -delta`.

The third is not derived by merely swapping the physical causal null lines. It is already-owned
founding structure whose complete realization remains conditional on the calibrated pair query.
Applying it, reversal, and (11) preserves the causal family but does not choose one member.

## 7. The three reciprocal limits

From (4), on a supplied calibrated family:

```text
phi_pair = 0             => W=1,        c_eff^(pair)=c_E,
phi_pair -> +infinity    => W->infinity,c_eff^(pair)/c_E->0,
phi_pair -> -infinity    => W->0,       c_eff^(pair)/c_E->infinity.  (12)
```

These are exact mathematical sectors, not physical assignments to ordinary, cosmological, or
microscopic phenomena. The individual one-way slopes still depend on how `beta` scales; only the
centered width and balanced readout have the shift-independent limits in (12).

The asymptotic gates do not choose a profile. For `-1<z<1`,

```text
phi_p(z)=atanh(z)+p z(1-z^2), |p|<1/2,                 (13)
```

is a continuous family with the same center, the same two infinite-depth endpoints, and positive
derivative. Thus even both reciprocal infinities plus the `c_E` anchor leave a continuum. The
positive endpoint may be required to realize the working `X_max` asymptote on a physical branch;
that requirement is necessary but not sufficient, and `X_max` is not a wall or boundary term.

## 8. Global causality is a real filter, not yet a selector

Chronology, causality, strong causality, causal simplicity, and global hyperbolicity are properties
of a supplied global pair/ambient completion. Local cone algebra does not imply global chronology
or any stronger condition.

These conditions can exclude branches containing closed causal curves, missing domains, or bad
global identifications. They still do not generally select one calibrated coordinate profile on a
supplied family. For example,
on `R^2`, every smooth bounded compactly supported function `p(x)` gives

```text
h_p=-dt^2+exp(4p(x))dx^2.
```

The coordinate `X=int exp(2p(x))dx` makes this a globally hyperbolic Minkowski metric, while the
calibrated `x` tapes retain distinct reciprocal profiles. These metrics are isometric, so this is
deliberately a calibration/gauge nonselection witness, not evidence for distinct physical ambient
pair families. Abstract causal geometry alone cannot decide which ruler calibration is physical.

The genuinely sharper candidate condition is global causal faithfulness of the complete family:
the pair construction and its transitions should preserve and adequately reflect the ambient
causal order across angular alternatives, paths, and overlaps. Current premises do not yet define
or select that complete construction.

## 9. Branches, paths, and R17

At a cut locus or wherever several pair surfaces join the same endpoints, each regular branch has
its own cone and derived `phi_pair`. Causality can discard a branch that loses time orientation or
regular Lorentzian rank. It does not choose among several regular causally lawful branches.

R17 remains a control: it supplies a global family of stationary pair leaves and path-labelled
normal holonomy, but no current result proves that those leaves are the physical all-observer
causal family, causally convex in the complete geometry, or uniquely selected on shell.

## 10. What is learned and what remains open

Derived within the declared class:

- exact causal meaning of `phi_pair` and conditional `c_eff^(pair)`;
- exact separation of cone tilt `beta` from centered reciprocal opening;
- complete local smooth bidirectional causal-isomorphism classification;
- closure under composition and reversal;
- constructive local transition/calibration nonuniqueness after ordinary calibration and both
  asymptotes;
- the distinction between automatic local causal preservation and global causal faithfulness.

Open:

- the physical calibrated pair immersion/family;
- lawful transitions among independently built families;
- all-observer global causal faithfulness and branch/path selection;
- an on-shell native law or bootstrap/global-completion owner;
- material principal symbol, coupling, response, and signalling;
- global topology and degenerate/null continuation.

No GR field equation or observer mechanics was imported. No action, source, matter, mass,
`X_max` value, CMB spectrum, or physical signal law is derived.
