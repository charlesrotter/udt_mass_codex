# Complete-branch angular-generator census

Date: 2026-07-23
Mode: preregistered metric-led exact CPU algebra and twelve-family branch audit
Grade: `VERIFIED-WITH-CAVEATS`

## Result first

None of the twelve registered global completion families naturally forces a
full angular generator with eigenvalues `{-1,+1}` throughout its complete
regular domain.

The exact local calculation is nevertheless highly restrictive. Write the
positive angular metric in a supplied angular bundle and depth flow as

```text
q = exp(2w) R(theta)^T diag(exp(-2u),exp(2u)) R(theta),
T(phi)=1.
```

Its metric strain generator is

```text
H = (1/2) q^{-1} Lie_T(q).
```

Let

```text
J = H-(trace(H)/2)I
```

be its trace-free shape part. Exact algebra gives

```text
trace(H) = 2 w_p,
J^2 = sigma^2 I,
sigma^2 = u_p^2 + theta_p^2 sinh(2u)^2.
```

Thus the full symmetric angular generator has eigenvalues

```text
w_p-sigma, w_p+sigma.
```

It matches the reciprocal `{-1,+1}` spectrum if and only if both

```text
w_p = 0,
sigma^2 = 1.
```

These have a simple geometric meaning:

1. angular area must have zero rate relative to the reciprocal clock/ruler
   area; and
2. angular conformal shape must move at unit reciprocal speed.

The registered reciprocal-toric control, FC12, has

```text
q = Omega(phi)^2 diag(exp(-2phi),exp(2phi)).
```

Its trace-free shape is exactly reciprocal for every positive `Omega`, but
its full generator is

```text
H = (d log Omega/dphi) I + diag(-1,+1).
```

Therefore FC12 contains an exact constant-relative-`Omega` matched
subfamily. FC12 as registered permits arbitrary positive `Omega`, so it does
not force the match.

Maximum conclusion:

```text
THE_FULL_METRIC_ANGULAR_STRAIN_MATCHES_THE_RECIPROCAL_MINUS1_PLUS1_
SPECTRUM_IFF_ITS_RELATIVE_MEAN_SCALE_RATE_VANISHES_AND_ITS_CSN_SHAPE_
SPEED_HAS_UNIT_MAGNITUDE__THE_REGISTERED_FC12_PROFILE_SUPPLIES_AN_EXACT_
CONSTANT_RELATIVE_SCALE_SUBFAMILY_BUT_ARBITRARY_OMEGA_TOPOLOGY_SEAL_
MONODROMY_AND_CURRENT_BOOTSTRAP_DO_NOT_FORCE_OR_SELECT_IT
```

## Correction made before banking

The first preregistration proposed testing only the trace-free `J`. Source
replay against the full Common-Scale Neutrality postulate exposed that as
too weak.

CSN removes a conformal rescaling shared by the entire metric. It does not
erase angular expansion relative to the reciprocal block. Under a full
common rescaling, the mean generators of both two-dimensional blocks shift
by the same scalar. Their difference is invariant:

```text
a_rel =
  trace(H_ang)/2 - trace(H_rec)/2.
```

The reciprocal gauge has `trace(H_rec)=0`, so `a_rel=w_p`. The correction was
separately preregistered and pushed before any generated ruling was changed.
The original preregistration remains historical evidence.

This correction is scientifically material: it changes FC12 from
“conditionally forced throughout its profile class” to “an exact matched
subfamily inside a larger unmatched family.”

## The complete metric and `c`

For the reciprocal block

```text
h_rec = diag(-c^2 exp(-2phi), exp(2phi)),
```

the complete block-diagonal control has

```text
det(g) = -c^2 exp(4w).
```

The observed `c` anchor is therefore explicit in every complete metric
control. It does not enter the dimensionless shape speed because that speed
is differentiated with respect to dimensionless `phi`.

The invariant relative-area rate can be written without fixing a common
conformal representative:

```text
a_rel =
  (1/4) T log(det(q)/abs(det(h_rec))).
```

In the registered reciprocal gauge, constant `c` and
`det(h_rec)=-c^2` give `a_rel=w_p`. This does not set `c=1`, remove its
physical clock/ruler conversion, or use `c` to set angular size.

## Pointwise shape result

The general formula separates three notions that previous work could only
list as open:

1. **relative mean scale:** `w_p`;
2. **shape spectrum:** `sigma`; and
3. **eigendirection transport:** not determined by the metric strain alone.

Fixed-axis matched and inverse profiles give `sigma=1` exactly. A spectator
gives `sigma=0`. A variable shear such as `u=phi^2` gives
`sigma^2=4phi^2`, so it meets the target only at isolated depths.

A rotating-axis profile can also have the correct pointwise spectrum:

```text
u=u0,
theta_p=1/sinh(2u0)
```

gives `sigma=1`. But its eigendirections rotate. Pointwise `{-1,+1}` does
not by itself provide the constant angular representation required by the
intertwiner theorem; a compatible metric-selected transport remains a
separate gate.

The exact controls are in
[POINTWISE_GENERATOR_CONTROLS.tsv](POINTWISE_GENERATOR_CONTROLS.tsv).

## Twelve completion families

The branch-level census is:

| completion | ruling | decisive reason |
|---|---|---|
| FC01 boundary–boundary | `ALLOWED_NOT_FORCED` | boundary data leave both area rate and shape speed free |
| FC02 one cap | `UNDEFINED_AT_REQUIRED_STRATUM` | rank-two angular metric collapses at the cap |
| FC03 two caps, `p=0` | `UNDEFINED_AT_REQUIRED_STRATUM` | both caps lose rank; interior profiles remain free |
| FC04 two caps, `p=1`/`S3` | `UNDEFINED_AT_REQUIRED_STRATUM` | topology fixes cap arithmetic, not generator rates |
| FC05 lens caps | `UNDEFINED_AT_REQUIRED_STRATUM` | lens determinant does not fix the interior profile |
| FC06 nonprimitive cap | `UNDEFINED_AT_REQUIRED_STRATUM` | singular/orbifold stratum has no rank-two extension |
| FC07 periodic torus bundle | `UNDEFINED_AT_REQUIRED_STRATUM` | real single-valued `phi` has a critical point on `S1`; general monodromy also fails |
| FC08 mirror double | `ALLOWED_NOT_FORCED` | exchange/reflection lifts can allow the pattern; `+I/-I` block it at the fixed seal |
| FC09 nonorientable glue | `ALLOWED_NOT_FORCED` | only a signed-monomial monodromy subfamily preserves reciprocal eigenlines |
| FC10 stratified projector | `UNDEFINED_AT_REQUIRED_STRATUM` | the fine rank-two bundle fails at a merger/split |
| FC11 nonintegrable distribution | `INSUFFICIENT_METRIC_DATA` | no global angular orbit bundle, depth flow, or fiber transport is supplied |
| FC12 reciprocal-toric diagonal | `ALLOWED_NOT_FORCED` | exact match only when relative `Omega` is constant |

Counts:

```text
ALLOWED_NOT_FORCED:             4
UNDEFINED_AT_REQUIRED_STRATUM:  7
INSUFFICIENT_METRIC_DATA:       1
FORCED_PERSISTENT_REGULAR:      0
```

The full records, including matched witnesses and unmatched
counterprofiles, are in
[BRANCH_GENERATOR_ATLAS.tsv](BRANCH_GENERATOR_ATLAS.tsv).

## Mirrors

At a mirror fixed point the first angular metric jet obeys

```text
-q_p = R^T q_p R.
```

The exact symmetric-jet dimensions are:

```text
angular +I:          0
angular -I:          0
axis reflection:     1
axis exchange:       1
```

Consequently `+I` and `-I` force zero angular first jet and cannot carry the
reciprocal spectrum at the fixed seal. Axis reflection and exchange admit a
one-parameter jet, whose amplitude may be reciprocal but is not fixed.
Because several lifts remain registered, the mirror does not select one.

See
[MIRROR_LIFT_GENERATOR_ATLAS.tsv](MIRROR_LIFT_GENERATOR_ATLAS.tsv).

## Monodromy and persistence

A constant reciprocal generator `L=diag(-1,+1)` descends through angular
monodromy `M` only when

```text
M^{-1} L M = L
```

for oriented generator preservation, or `+/-L` when only the unordered
eigenline pair and a possible depth reversal are retained.

Identity, minus identity, and signed axis reflections commute with `L`.
Exchange anticommutes and can preserve only the unordered lines unless depth
orientation also reverses. Generic parabolic, hyperbolic, and
orientation-reversing shear matrices do neither. The complete `GL(2,Z)`
family therefore does not force persistence.

There is an independent global obstruction on a periodic base: a real
single-valued `phi` on `S1` has a critical point, where no flow satisfying
`T(phi)=1` exists. A circle-valued `phi` or nontrivial cover could avoid that
statement but is not registered UDT data.

See [MONODROMY_GENERATOR_ATLAS.tsv](MONODROMY_GENERATOR_ATLAS.tsv).

## What was and was not calculated

The audit is complete for:

- every positive real `2x2` angular metric on a supplied regular angular
  bundle;
- its full symmetric strain and trace-free shape;
- all twelve registered parametric completion families;
- all registered mirror-lift classes;
- general monodromy compatibility plus exact controls; and
- caps, rank changes, and critical-`phi` fail-closed cases.

The registered “complete branches” are completion families, not twelve
solved on-shell `(g,phi)` universes. They usually specify topology and
endpoint/glue type while leaving the metric profiles free. The audit records
that absence rather than fabricating a generator.

There remain zero complete on-shell `(g,phi)` branch witnesses in this
registry. The skew angular-frame generator, a selected transport,
field equations, and a branch selector also remain open.

## Scientific interpretation

The reciprocal angular match has been reduced to two scalar geometric
conditions:

```text
relative angular area rate = 0,
angular shape speed squared = 1.
```

That is more informative than merely saying that the angular sector is
underdetermined. It identifies exactly what any native metric law would have
to produce and what every candidate complete branch can be tested against.

It does not justify adding either condition as a new postulate. The current
metric premises, Reciprocity, CSN, finite-cell structure, seal, and
bootstrap have not yet derived them.

## Verification

- pinned SymPy `1.14.0` exact derivation;
- separate standard-library `Fraction` implementation;
- independent finite-difference reconstruction of the general formula;
- three rational generator controls;
- `c=2`, `3`, and `299792458` complete-determinant controls;
- exact mirror-jet rank reconstruction;
- nine monodromy controls;
- all fifteen source identities replayed;
- 20/20 production mutation catches; and
- 20/20 independent mutation catches.

No GPU work was performed.

## Four evidence gates

1. **Preregistered:** yes. The original preregistration was committed at
   `12d296a`; the full-metric CSN correction was committed at `863c2c8`
   before regenerating outcomes.
2. **Full or bounded:** complete for the general regular positive angular
   metric and the twelve registered parametric completion families. No
   on-shell complete metric profile is available for eleven families, and
   cap/rank-degenerate strata intentionally remain undefined.
3. **Independently verified:** yes for the algebra, branch cardinality,
   mirrors, monodromy, source lineage, and corruption catches. No fresh
   zero-context semantic review was run, so the banked grade retains a
   caveat.
4. **Every premise audited:** yes. Complete-metric versus angular-only CSN,
   `c`, relative scale, shape, transport, `dphi`, topology, cap regularity,
   mirror, monodromy, bootstrap, action, carrier, source, and mass are
   separated.

No action, carrier, source, mass, density selector, physical boundary,
time-live equation, canonization, or complete universe follows.

