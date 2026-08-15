# Preregistration — all-instruments-live correction

Date: 2026-08-14

Mode: `MAP -> OBSERVE -> PONDER -> DERIVE`; metric-led exact symbolic/CPU correction

## 1. Reason for correction

The first G90 report used **fully live** for families in which every factor had an explicit complete
lift and at least the reciprocal block `B` and mixing block `S` varied. That phrase was too strong.
The registered flat and monotone witnesses fixed `Q=I`, `Y=I`, and `Z=0`; the quiet-middle witness
varied `Q,S` but fixed `Y=I,Z=0`.

The existing witnesses therefore answer the explicit-lift question but do not answer the stricter
question raised by Charles:

> Does loud-ends/quiet-middle become selected when the complete metric and pair orchestra is not
> represented by silent or frozen blocks?

No result from this correction may be described as physical history selection merely because all
chart factors vary. A field present in a theory may admit a constant or zero value on a special
solution unless a native law excludes it.

## 2. Exact arena

Retain the G89 evaluator without compression:

```text
E=[[B,0],[Q S,Q]],
J=[Y;Z],
U=B Y,
R=S Y+Z,
A=Q R,
h=U^T eta_2 U+A^T A.
```

The reciprocal parameter is `t=exp(phi)>0`. The audit is local on a regular open interval about a
declared rational control point `t0`; global endpoints are classified separately.

## 3. Three activity classes

The following classes must not be conflated.

### C0 — explicit complete lift

`B,Q,S,Y,Z` are all explicitly supplied. Some may be constant or zero. This is the class already
tested by the original G90 flat and monotone witnesses.

### C1 — block-live in the declared triangular calibration

At `t0`, each of

```text
dot B, dot Q, dot S, dot Y, dot Z
```

is nonzero. `B,Q` remain in the registered upper-triangular positive-diagonal chart; `Y` is
invertible. Every one of the four entries of `S` must have nonzero derivative at `t0`.

This is a chart-level condition. It is not automatically frame invariant.

### C2 — contribution-live in the same calibrated chart

Writing `dot h` as the exact sum of factor contributions,

```text
H_B = (dot B Y)^T eta U + U^T eta (dot B Y),
H_Q = (dot Q R)^T A + A^T (dot Q R),
H_S = (Q dot S Y)^T A + A^T (Q dot S Y),
H_Y = (B dot Y)^T eta U + U^T eta (B dot Y)
      +(Q S dot Y)^T A + A^T (Q S dot Y),
H_Z = (Q dot Z)^T A + A^T (Q dot Z),
dot h=H_B+H_Q+H_S+H_Y+H_Z,
```

require every `H_X` to be nonzero at `t0`. Also require both columns of `A` nonzero, both reciprocal
pair columns present, `dot g` nonzero for `g=E^T eta_4 E`, and the pair metric regular.

Nonzero at `t0` plus smoothness proves activity on some open neighborhood. C2 is stronger than C1
but remains conditional on the declared complete-coframe and pair calibration; it is not called a
gauge-independent physical selector.

## 4. Questions

1. Can an exact C2 family have constant terminal modulation `M=phi_pair-phi`?
2. Can an exact C2 family have strictly monotone terminal modulation?
3. Can an exact C2 family have loud ends and a quiet middle?
4. Do the O1 live chart-overlap identities continue to hold for a nonidentity `R(t)`?
5. Is there a general exact factorization showing why activity alone can or cannot select the
   terminal response?

## 5. Required constructions

No scalar Gram history may be asserted without an explicit `B,Q,S,Y,Z` lift.

At least one C2 counterfamily and one C2 quiet-middle family must be constructed, or their absence
must be proved. A counterfamily may not pass merely because a block is fixed, zero, rank deficient,
or absent. Exact cancellations are allowed but must be exposed rather than hidden; they establish
kinematic nonselection, not a physical mechanism.

The strongest admissible general construction is:

```text
choose regular E(t) and a target pair coframe V_*(t),
set J(t)=E(t)^-1 V_*(t),
then h(t)=V_*(t)^T eta_4 V_*(t).
```

If used, the audit must prove that the resulting `Y,Z` meet C1/C2 at an exact control point and must
state that physical ownership of this query realization remains open.

## 6. Falsification and certification

- `ALL_INSTRUMENTS_ACTIVITY_ALONE_SELECTS_LOUD_QUIET_LOUD` is falsified by one exact regular C2 flat
  or monotone family.
- It is not certified by excluding only C0 witnesses.
- `LOUD_QUIET_LOUD_SURVIVES_ALL_INSTRUMENTS_ACTIVITY` requires one exact regular C2 witness with the
  registered two-ended/interior-minimum behavior.
- Any failure of `dot h=sum H_X`, the uncompressed evaluator, regularity, or exact overlap covariance
  is an algebraic failure.
- A C2 result cannot be promoted to a physical history, dynamics, bootstrap selection, `X_max`,
  microphysics, or cosmology.

## 7. Preregistered landings

The primary landing must be exactly one of:

1. `ALL_INSTRUMENTS_ACTIVITY_ALONE_SELECTS_LOUD_QUIET_LOUD_ON_DECLARED_C2_CLASS`;
2. `ALL_INSTRUMENTS_ACTIVITY_ALONE_DOES_NOT_SELECT_RESPONSE_SHAPE`;
3. `DECLARED_ACTIVITY_CLASS_IS_GAUGE_OR_TYPE_INVALID`;
4. `ALGEBRA_OR_REGULARITY_FAILURE`.

The secondary quiet-middle landing must be exactly one of:

- `LOUD_QUIET_LOUD_SURVIVES_DECLARED_ALL_ACTIVE_CLASS`;
- `LOUD_QUIET_LOUD_NOT_CONSTRUCTED_ON_DECLARED_ALL_ACTIVE_CLASS`.

Maximum conclusion: a bounded statement about kinematic activity in the supplied complete-coframe
and pair-realization chart. Physical score selection remains `OPEN` unless an independently owned
nonidentity history law excludes the counterfamilies.
