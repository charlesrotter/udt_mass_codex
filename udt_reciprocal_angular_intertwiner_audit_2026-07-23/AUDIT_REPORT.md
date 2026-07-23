# Complete-metric reciprocal–angular intertwiner audit

Date: 2026-07-23

## Result first

The complete metric admits an exact **conditional** non-block-diagonal
reciprocal–angular structure once a matched angular representation is
supplied, but it does not select that representation or structure across
the registered solution space.

Let the dimension-matched reciprocal coframe be

```text
theta_rec=(c dt,dx_parallel),
D(phi)=exp(phi L),
L=diag(-1,+1).
```

Let a candidate angular two-plane carry a regular one-parameter action

```text
A(phi)=exp(phi B).
```

For an angular-to-reciprocal map `S`, exact equivariance is

```text
L S = S B.
```

For a bilinear non-block metric pairing `C`, exact invariance is

```text
L^T C + C B = 0.
```

The complete real `2x2` classification gives the same sharp existence
condition for a full-rank object in either covariance type:

```text
B is similar to diag(-1,+1)
<=> trace(B)=0 and det(B)=-1.
```

The map and bilinear pairings attach the reciprocal weights differently:

- if `B=L`, equivariant maps are diagonal while invariant bilinear cross
  blocks are anti-diagonal;
- if `B=-L`, equivariant maps are anti-diagonal while invariant bilinear
  cross blocks are diagonal; and
- a change of angular basis conjugates these families without changing the
  theorem.

Adding a matched mirror action sharpens each two-parameter family to one
scalar:

```text
same assignment:       S=s I,       C=epsilon F,
inverse assignment:    S=s F,       C=epsilon I,
F=[[0,1],[1,0]].
```

Thus, **if** the angular sector independently carries the reciprocal
continuous-plus-mirror representation, its relationship to the reciprocal
backbone is essentially rigid: only one relative normalization remains.

That is the positive result. The missing premise is equally exact: no
registered UDT rule selects that angular representation or its relative
normalization.

Maximum conclusion:

```text
NONBLOCK_RECIPROCAL_ANGULAR_INTERTWINERS_EXIST_EXACTLY_FOR_MATCHED_
REPRESENTATIONS_BUT_THE_COMPLETE_METRIC_RECIPROCITY_CSN_C_ANCHOR_
SEAL_AND_FINITE_CELL_DO_NOT_SELECT_THE_MATCH__C_FIXES_CLOCK_RULER_
CONVERSION_NOT_ANGULAR_NORMALIZATION
```

## The general theorem

Write

```text
B=[[p,q],[r,z]].
```

The four linear equations for `L S=S B` have coefficient determinant

```text
det(B-I) det(B+I)
= (p z-p-q r-z+1)(p z+p-q r+z+1).
```

Each row of `S` is a left eigenvector of `B`, with eigenvalue `-1` or `+1`.
Consequently:

- no `+/-1` angular weight gives only `S=0`;
- one matching angular weight gives rank-one maps only;
- repeated `+1` or repeated `-1` weights also give rank-one maps only;
- an invertible map requires independent `-1` and `+1` angular
  eigendirections; and
- in two real dimensions this is exactly `trace(B)=0`, `det(B)=-1`.

For the bilinear cross block, the angular weight is paired
contragrediently. Since `L` and `-L` are similar, the full-rank existence
condition is the same, although the diagonal and anti-diagonal assignments
exchange.

[GENERATOR_INTERTWINER_ATLAS.tsv](GENERATOR_INTERTWINER_ATLAS.tsv) and
[BILINEAR_CROSS_INVARIANT_ATLAS.tsv](BILINEAR_CROSS_INVARIANT_ATLAS.tsv)
record identity, reciprocal, inverse, repeated-weight, rotation, Jordan,
one-weight, generic, and conjugate controls.

## Why the mirror matters

The continuous character alone leaves two independent scales: one on each
reciprocal weight line. A compatible mirror exchanges those two lines.

Solving both

```text
L S=S B,
F S=S R_ang
```

leaves one invertible basis element for each matched reciprocal dihedral
pair. The bilinear equations do the same. In contrast:

- angular `+I` and `-I` seal lifts admit only rank-one maps under the
  discrete seal equation alone;
- a reciprocal continuous action paired with angular `+I` at the mirror is
  inconsistent with an invertible soldering; and
- an angular spectator (`B=0`) has no nonzero continuous reciprocal
  intertwiner at all.

The exact cases are in
[COMBINED_DIHEDRAL_INTERTWINER_ATLAS.tsv](COMBINED_DIHEDRAL_INTERTWINER_ATLAS.tsv)
and
[COMBINED_DIHEDRAL_BILINEAR_ATLAS.tsv](COMBINED_DIHEDRAL_BILINEAR_ATLAS.tsv).

This is a conditional rigidity theorem, not a selection theorem. The
registered finite-cell seal supplies the reciprocal mirror action, but it
does not say that the angular sector carries the matching continuous action
or matching mirror lift.

## Exact local full-metric witnesses

The conditional result is not merely an abstract bundle possibility.
Full `4x4` local non-block Lorentzian metric witnesses exist.

In the dimension-matched coframe, use a matched angular reciprocal block and

```text
C=epsilon F
```

or the inverse assignment with

```text
C=epsilon I.
```

After returning to raw coordinates with

```text
C_c=diag(c,1),
```

the temporal row of the cross block acquires the required factor of `c`.
For both assignments the exact determinant is

```text
-c^2 (1+epsilon^2)(1-epsilon^2).
```

The metric has Lorentz signature for positive finite `c` and
`|epsilon|<1`. At `epsilon=1/2` the determinant is

```text
-15 c^2/16.
```

The zero-cross-block member also remains Lorentzian under the same matched
angular representation. Therefore both zero and nonzero branches are
mathematically admissible; no current equation forces `epsilon` to be
nonzero or fixes its value.

These are algebraic local witnesses, not solved on-shell finite-cell
geometries. The witnesses and their unit caveat are recorded in
[CONDITIONAL_NONBLOCK_WITNESSES.tsv](CONDITIONAL_NONBLOCK_WITNESSES.tsv).
The angular coframe normalization is set to one only for these existence
controls. It is not a physical radius selection.

## What `c` does—and does not do

The audit keeps the observational anchor explicit:

```text
theta_rec=(c dt,dx_parallel),
g_tt=-c^2 exp(-2 phi).
```

The conversion map `C_c` commutes with the dimensionless reciprocal
character. Changing the positive numerical value of `c` therefore changes
the physical clock-to-ruler conversion and the raw metric coefficients, but
not the rank or existence of an intertwiner.

An angular coframe instead has a separate length normalization, schematically

```text
theta_ang=R_ang times dimensionless angular coframe.
```

Nothing in the conversion `c:T -> L` fixes `R_ang`. Positive CSN removes a
common calibration; it does not remove this relative angular normalization
or the dimensionless mixing `epsilon`.

Thus `c` has not disappeared from the solution space. It supplies an actual
clock–ruler scale everywhere. It does not, by itself, set every length in
the universe.

## Why arbitrary metric cross terms are not the answer

A general complete metric can be written in a supplied split as

```text
g=[[H,C],[C^T,Q]].
```

But the label “cross block” already presupposes reciprocal and angular
projectors. An exact cross-chart control starts with

```text
diag(-c^2,1,R^2,R^2)
```

and produces a nonzero reciprocal–angular component

```text
g_02=-c^2 kappa
```

without changing the determinant or underlying metric. A component-level
nonzero `C` is therefore not a full-frame invariant.

Once a reciprocal subbundle is supplied, the metric can construct its
orthogonal complement and invariant cross diagnostics. It cannot use that
construction to derive the initially supplied subbundle without circularity.
Likewise, contracting the abstract reciprocal endomorphism `D` with the
spacetime metric requires a bundle map between their domains; that map is
the soldering being sought.

The only nonzero map natural under completely independent reciprocal and
angular frame freedom is none: invariance under a single independent angular
rescaling by two already forces `S=0`.

## Relation to the field-assisted `3+3` backbone

On nonnull-`dphi` strata, the complete `(g,phi)` data intrinsically produce
two rank-three two-form sectors. They do not canonically produce a rank-two
angular plane inside either rank-three sector. A transverse direction,
section, quotient, or equivalent reduction remains free.

The new intertwiner theorem therefore complements rather than supersedes the
`3+3` result:

```text
intrinsic reciprocal 3+3 sectors
    -> no unique angular two-plane

supplied angular reciprocal representation
    -> exact non-block map/cross pairing
    -> one relative scale after matched mirror
```

The missing join is now narrower: derive the angular reciprocal
representation from the complete metric, rather than merely allowing it.

## Twelve completion families

All twelve registered completion rows remain unselected.

- The mirror-double row supplies several discrete angular lifts but no
  unique continuous angular reciprocal character.
- The periodic torus-bundle row supplies general `GL(2,Z)` monodromy, not a
  required continuous weight match.
- Boundary, cap, lens, nonorientable, stratified, and nonintegrable rows do
  not manufacture the missing representation.
- The reciprocal-toric row supplies a matched representation conditionally.
  It therefore supports the exact intertwiner family, but its integral
  basis, periods, reciprocal assignment, endpoints, and physical ownership
  remain inputs.

None of the rows contains a complete on-shell `(g,phi)` witness. See
[COMPLETION_SOLDERING_ATLAS.tsv](COMPLETION_SOLDERING_ATLAS.tsv).

## Scientific meaning

The audit does not close reciprocal–angular soldering, but it changes the
open question from an arbitrary search into a precise test.

A candidate complete branch need not be searched for arbitrary “coupling.”
Its angular generator can be computed. A full native soldering is possible
at this linear representation layer exactly when

```text
B^2=I, trace(B)=0, det(B)=-1.
```

If a future metric equation or global bootstrap selects that branch and a
compatible mirror, the remaining local map is already rigid up to relative
normalization. If it selects another angular representation, this
particular soldering route is excluded.

No action, source, carrier, Hopf section, density response, mass, absolute
angular scale, or completion selector follows from this theorem.

## Verification before fresh review

- pinned SymPy `1.14.0` exact derivation;
- 10 continuous map cases;
- 10 bilinear cross-invariant cases;
- five discrete seal cases;
- five continuous-plus-seal map cases;
- five continuous-plus-seal bilinear cases;
- three local full-metric witness rows;
- all twelve completion rows;
- 25 source identities;
- 29/29 exercised mutation catches; and
- separate standard-library `Fraction` row reduction with no production
  import or SymPy.

## Four evidence gates

1. **Preregistered:** yes, commit `0d7b06d`.
2. **Full space or bounded scope:** complete for all real regular linear
   two-dimensional angular generators, all registered constant seal lifts,
   and all twelve registered completion rows; arbitrary nonlinear
   field-dependent/higher-jet representations remain open.
3. **Independently verified:** exact separate row-reduction implementation,
   direct full-metric witness reconstruction, source replay, and 29 catches
   pass. A fresh zero-context review independently re-solved both covariance
   types, the mirror reduction, and both witness signatures. Its optional
   sidecar stalled after the substantive checks and was interrupted, so the
   transcript rather than a normally completed final return is preserved.
4. **Every premise audited:** yes; `c`, CSN, angular representation,
   decomposition, metric cross blocks, seal, completion, `dphi`, action,
   carrier, density, mass, and scale are separated.

Banking grade:
`VERIFIED-WITH-CAVEATS-BOUNDED`. The caveat concerns review completion
provenance and the absence of an on-shell finite-cell witness, not a failed
algebraic check.
