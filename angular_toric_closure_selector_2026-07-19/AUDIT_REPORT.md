# Angular–Toric Closure Selector Audit — Report

Date: 2026-07-19
Base: `cc7b08381281fa104661df5b6af9fb030cabac95`
Preregistration commit: `d8b964d`
Mode: CPU-only, metric-led, bounded toric classification

## Result

`S3_AND_FREE_HOPF_ACTION_UNIQUE_CONDITIONAL_WITHIN_SUPPLIED_TORIC_CAP_PREMISES__RECIPROCITY_CSN_FINITE_CELL_AND_BOOTSTRAP_DO_NOT_SELECT_THOSE_PREMISES__FIRST_MISSING_GATE_TRANSVERSE_SPATIAL_RECIPROCAL_REALIZATION_AND_PERIODICITY__CONDITIONAL_SECOND_GATE_FINITE_CELL_CAP_COMPLETION_OPEN`

The angular–`phi` sector contains a sharper conditional selection chain than the preceding audit
could state, but its first link is still missing.

If UDT were to supply all of the following:

1. two periodic **spatial** directions carrying the reciprocal orbit block in one global integral
   torus basis;
2. a compact cohomogeneity-one interval whose two ends are smooth primitive circle collapses;
3. the globally diagonal form all the way to those ends, so the two reciprocal eigen-circles are the
   collapsing cycles;

then the first circle must collapse at one end and the second at the other. Their integral-lattice
determinant is one, and the completed three-geometry has `S3` topology. Within precisely that supplied
class, `S3` is not an aesthetic choice: it is `UNIQUE-CONDITIONAL`.

If one then additionally requires a free effective circle action with a smooth ordinary `S2`
quotient, its weights must satisfy

```text
|m|=|n|=1.
```

That leaves diagonal and anti-diagonal actions and their orientation reversals, giving conditional
unit classes `Q=+1` and `Q=-1`. This second result is also a genuine conditional uniqueness theorem.

Registered UDT does not yet supply the premises of the first theorem. Exact C0/C1 does not place its
founding temporal/parallel reciprocal comparison pair into two transverse periodic spatial slots.
Beyond fixing the physical finite mirrored-cell, monotonic-domain, and no-spatial-infinity setting,
finite-cell canon's only toric-relevant field datum is static `phi` parity/value at the seal. CSN removes positive
common scale on the interior but does not provide a cap. Bootstrap is presently an on-shell
admissibility principle, not a topology-ranking or boundary-completion equation.

Therefore the strongest honest result is a conditional chain, not a selected universe or carrier.

## Lay interpretation

The earlier audit found that UDT's reciprocal stretching has exactly the right shape to describe the
two circular directions used by a Hopf geometry. This audit asked what happens if those circles are
followed all the way to the ends.

There is a surprisingly simple answer. If the two circles really are spatial directions and the
geometry closes smoothly, one circle closes at one end while the other closes at the opposite end.
With the basic, untwisted identification, that construction is a three-sphere. No extra force or
Skyrme-like mechanism is needed to obtain that topology. It follows from the way the circles close.

Likewise, if we require the simultaneous rotation of those circles to have no hidden fixed or
exceptional points, only equal-magnitude rotations survive. Those are exactly the diagonal and
anti-diagonal Hopf rotations.

This greatly narrows where the missing idea can be. The problem is no longer the Hopf mathematics
after the angular geometry is supplied. There are two ordered missing gates. First: why UDT's
reciprocal pair should be realized as two periodic transverse spatial directions at all. Only if
that is derived does a second question arise: why the finite cell should close those directions by
smooth opposing eigen-circle collapses rather than by another boundary or gluing.

The current finite-cell and bootstrap statements do not yet say that. They allow other closures.

## The toric closure classification

Let a principal spatial orbit be a two-torus with primitive angular lattice `Z2`. At the two ends of
an interval, suppose primitive cycles

```text
v_minus=(a,b),  v_plus=(c,d)
```

collapse. The integer

```text
p=|det(v_minus,v_plus)|=|a d-b c|
```

controls the lattice quotient. In the standard orientable toric completion:

- `p=1` gives the determinant-one `S3` class;
- `p>1` gives lens-space classes, with the additional gluing integer distinguishing `q`;
- `p=0` leaves a nontrivial free circle and gives `S2 x S1` in the standard orientable same-cycle
  completion;

Primitivity of each endpoint cycle ensures local smooth-manifold collapse; it does not force their
mutual determinant to one.

Even if an angular exchange mirror is supplied by hand, it does not select `p=1`. For

```text
v_minus=(a,b),  v_plus=(b,a),
```

the determinant is `a^2-b^2`. Exact primitive examples include:

| Pair | `p` |
|---|---:|
| `(1,1)` and `(1,1)` | 0 |
| `(1,0)` and `(0,1)` | 1 |
| `(2,1)` and `(1,2)` | 3 |
| `(3,2)` and `(2,3)` | 5 |
| `(4,3)` and `(3,4)` | 7 |
| `(3,1)` and `(1,3)` | 8 |
| `(5,4)` and `(4,5)` | 9 |
| `(4,1)` and `(1,4)` | 15 |

The exact script independently verifies the determinants, primitivity, and Smith normal forms.
These are exemplars rather than a complete mirror census. Thus even an angular interpretation of
Reciprocity as circle exchange is weaker than a global cap rule.

### The conditional `S3` theorem

Now restrict further to the exact globally diagonal candidate

```text
G=Omega(phi)^2 diag(exp(-2 phi),exp(2 phi))
```

in one fixed integral angular basis, with positive `Omega` on the principal region and smooth compact
caps at the two reciprocal extremes. A diagonal coefficient can vanish only along its corresponding
coordinate circle. If the two opposite eigen-circles collapse primitively at opposite ends, the
cycles are `(1,0)` and `(0,1)`, whose determinant is one.

That proves `S3_UNIQUE_CONDITIONAL_WITHIN_SUPPLIED_TORIC_CAP_PREMISES`.

It does not prove the premises. A general toric completion may rotate the collapsing cycle through
off-diagonal metric data or use multiple integral charts near a cap. C1 explicitly leaves the
transverse block and off-diagonal terms open. Primitive determinant-`p` lens alternatives therefore
remain admissible countermodels to a foundation-level uniqueness claim, even though they are outside
the single-global-basis diagonal subfamily.

The `p=3` and `p=5` rows are catch-proofs, not the whole lens family. The family ledger separately
retains every primitive `p>1` lens class with its admissible gluing integer `q`, as well as incomplete
or noncompact toric ends. Local reciprocal kinematics does not supply a completeness theorem that
removes those alternatives.

## Finite mirror witnesses without caps

The algebraic parity statement and an angular exchange do not themselves require a circle to
collapse. An exact compact double-cover/local-parity witness is

```text
h=d sigma^2 + exp[-2 sin(sigma)] dxi1^2 + exp[+2 sin(sigma)] dxi2^2
```

on `S1 x T2`. Its determinant is one, its orbit coefficients are positive everywhere, and

```text
sigma -> -sigma,
xi1 <-> xi2
```

is an isometry. The scalar `phi=sin(sigma)` is odd and vanishes at the mirror seal, yet there are no
caps and the spatial topology is not `S3`.

This is not a direct countermodel to the complete physical finite-cell canon: its base is a
boundaryless circle and `phi=sin(sigma)` is globally nonmonotone. It is retained only as an exact
double-cover/local-parity witness showing that oddness plus exchange contains no algebraic cap
condition. It is not proposed as the physical UDT universe, and its angular slot and exchange remain
conditional.

A finite interval times `T2` with monotone reciprocal depth and positive orbit coefficients is the
foundation-compatible bounded no-cap family when a physical boundary is retained. The boundary
functional is currently open, so that family cannot be excluded by silently choosing a cap. This
interval family, rather than the periodic witness, carries the foundation-level nonselection result.

## Smoothness does not choose the round metric

The round witness is

```text
h_round=d eta^2 + cos(eta)^2 dxi1^2 + sin(eta)^2 dxi2^2.
```

The audit constructs the explicit non-round family member

```text
H(eta)=1+(1/3) sin(2 eta)^2,
h_nonround=H(eta)^2 d eta^2 + cos(eta)^2 dxi1^2 + sin(eta)^2 dxi2^2.
```

Both are mirror-symmetric under `eta -> pi/2-eta` with circle exchange. Both have the same smooth
primitive cap slopes. More strongly, exact even/odd identities of `H`, the collapsing radius, and
the spectator radius at both endpoints establish analytic cap parity to all orders. Both have
exactly the same independently normalized orbit block

```text
diag(cot eta,tan eta)
=diag(exp(-2 phi),exp(2 phi)),
tan eta=exp(2 phi).
```

They are not related by a positive full-metric conformal rescaling. Their scale-invariant
radial/orbit ratio differs by `14/9` at `eta=pi/4`. Smoothness therefore constrains endpoint jets but
does not select the round radial completion. An action or other field equation would be needed to
rank the remaining functions.

## Conditional circle-action uniqueness

On the supplied `S3` witness, consider the effective weighted action

```text
exp(i theta):(z1,z2) -> (exp(i m theta) z1, exp(i n theta) z2).
```

At the circle where `z2=0`, the stabilizer is the finite root group `mu_|m|` when `m` is nonzero
and the full `U(1)` when `m=0`; the analogous statement with `n` holds where `z1=0`. Consequently
the action is free everywhere only when

```text
|m|=|n|=1.
```

Primitive weights such as `(1,2)`, `(2,1)`, and `(2,3)` are effective but have exceptional
stabilizers. Their quotients are weighted/orbifold alternatives, not an ordinary principal
circle bundle over a smooth `S2`. Zero-weight actions such as `(0,1)` or `(1,0)` have a fixed
exceptional circle and are separately retained in the family census.

For the four free sign choices, the normalized metric-dual connection is common-scale independent.
The exact script obtains

```text
integral A wedge dA = -4 pi^2 m n,
Q = m n.
```

Thus diagonal signs give `Q=+1`, anti-diagonal signs give `Q=-1`. Freeness conditionally selects the
weight magnitudes, not the chirality and not the physical requirement that UDT possess this quotient.

## What the registered UDT selectors actually do

### Reciprocity

Reciprocity supplies the determinant-one exponential comparison pair. Within the Hopf-coordinate
witness, `phi -> -phi` exchanges the two orbit scale factors. It does not universally duplicate or
reassign the founding temporal/parallel pair into a transverse spatial torus, declare those
directions periodic, or specify their collapse lattice.

### Common-Scale Neutrality

CSN removes a positive common factor from the interior orbit block and from the normalized
metric-dual connection. At a genuine cap, an orbit coefficient or determinant representative
degenerates. Smooth cap completion is additional global/boundary information, not a positive CSN
gauge transformation through zero.

### Finite-cell structure

The binding canon fixes a monotone finite domain terminated by a physical mirrored boundary/fold,
with no spatial infinity. Within that setting, its only toric-relevant field datum is the static
`phi` condition: `phi` is odd at the seal, its value is zero, and its normal derivative remains free.
It expressly does not select the boundary functional or the boundary data of other fields. It says
nothing about a transverse torus lattice, angular exchange, endpoint collapse cycles, or a quotient
action.

### Bootstrap

The current bootstrap principle says the realized matter-bearing universe must be a complete
self-consistent global solution in a narrow total-density window. The full time-live volume,
physical boundary, equations, action, and stability gates remain open. The bootstrap-variation audit
also finds no off-shell representative-selection or matching map. There is therefore no registered
operator that compares and ranks `T3`, `S3`, lens, boundary-cylinder, round, or non-round closures.

Bootstrap could eventually select among complete solutions after that missing law exists. It cannot
presently be used as the missing law itself.

## Mechanical adjudication

| Question | Ruling | Reason |
|---|---|---|
| Does reciprocal angular form alone select topology? | `NO` | The determinant-normalized form is generic and local. |
| Does angular exchange mirror select `S3`? | `NO` | Primitive mirror pairs realize multiple determinant classes. |
| Do global diagonal reciprocal eigen-caps select `S3`? | `YES, UNIQUE-CONDITIONAL` | Opposing primitive coordinate cycles have determinant one. |
| Does smoothness select the round completion? | `NO` | An explicit smooth non-round, non-conformal family shares the same orbit block and cap jets. |
| Does a free smooth circle quotient select the Hopf weights? | `YES, UNIQUE-CONDITIONAL` | Freeness at both exceptional circles requires `|m|=|n|=1`. |
| Does it choose chirality? | `NO` | Diagonal and anti-diagonal actions give opposite unit classes. |
| Does finite-cell canon supply toric caps? | `NO` | Beyond its physical finite mirrored/monotone/no-infinity setting, its toric-relevant datum is only static `phi` parity/value; no torus lattice, cap cycle, or boundary functional follows. |
| Does bootstrap currently rank closures? | `NO` | It supplies no off-shell or topology-selection map. |
| Is the carrier/action derived? | `NO / OPEN` | A canonical quotient witness is not `Map(S3,S2)` or its dynamics. |

The detailed eighteen-row classification is `STATUS_LEDGER.tsv`; the complete fifteen-family
disposition is `CANDIDATE_FAMILY.tsv`.

## Ordered missing selectors

The missing objects should not be invented or named as new postulates. Descriptively, the first
absent rule is:

> a rule deriving how the reciprocal comparison representation enters the **transverse spatial
> metric**, including whether its directions are periodic.

Call this the `TRANSVERSE_SPATIAL_RECIPROCAL_REALIZATION_AND_PERIODICITY` gate only as a ledger
description, not as an adopted principle.

Only after that first gate passes does the separate `FINITE_CELL_CAP_COMPLETION` gate arise. If the
two together produce a global diagonal two-torus with smooth opposing primitive eigen-caps, the rest
of the topological chain is nearly automatic: `S3` follows, and a separately required free smooth
quotient reduces the circle weights to diagonal/anti-diagonal choices. If either gate produces a
different transverse block or boundary, the Hopf route may remain only a conditional control.

## Completeness and exclusions

This audit classifies one bounded toric spatial-geometry tile:

- fields: only a candidate spatial three-metric orbit structure;
- action/equations: absent and explicitly open;
- domain: toric cohomogeneity one, including caps, finite boundaries, generic lens/gluing families,
  incomplete/noncompact ends, and a periodic local-parity witness;
- topology: determinant-zero, determinant-one, and determinant-`p` toric classes;
- dynamics/stability/mass: not entered;
- off-toric geometries: not classified and still live.

No result here is a full metric solution-space theorem.

## What is not claimed

- No transverse spatial torus was derived from C0/C1.
- No temporal direction was compactified or relabeled as an angular circle.
- No global `S3`, `T3`, lens space, cap, or boundary was adopted.
- No carrier, configuration space, action, source, mass, or time-live law was derived.
- No existing soliton or particle evidence was used as a selection criterion.
- No GPU work, canonization, repository reorganization, startup update, or `grok` integration was
  performed.

## Four evidence gates

1. Preregistered: yes, commit `d8b964d`, before additional scientific-source inspection and
   countermodel construction.
2. Scope: bounded toric closure classification; off-toric metrics and all dynamics remain open.
3. Verification: deterministic exact algebra and source/status catch-proofs, plus a fresh
   adversarial review recorded separately.
4. Premises: frozen in `PREREGISTRATION.md`, `SOURCE_INVENTORY.tsv`, `CANDIDATE_FAMILY.tsv`, and
   `STATUS_LEDGER.tsv`.
