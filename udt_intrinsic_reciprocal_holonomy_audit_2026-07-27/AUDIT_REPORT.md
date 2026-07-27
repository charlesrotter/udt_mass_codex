# Intrinsic reciprocal-screen holonomy audit

Date: 2026-07-27

Preregistration commit: `68f8303` (base `ff3d936`)

Status: **VERIFIED-WITH-CAVEATS, BOUNDED OFF-SHELL METRIC RESULT**

## Result first

The complete twisted-`S3` witness does **not** preserve the full intrinsic reciprocal-screen lift as
an endpoint-only object.  The obstruction is exact and local, not merely a numerical loop mismatch:

```text
(nabla_E0 X_lambda)^0_1=-3/25
```

at P00 for every real `lambda` on the frozen profile.  In all 18 sampled branch/event cases, the six
curvature endomorphisms already span full `so(1,3)`.  An independent coordinate calculation confirms
rank six in all 18 cases.

All 36 preregistered closed loops return nonidentity Lorentz holonomy and all 36 fail ordinary
`U X U^-1=X` closure.  No sampled `X_lambda` is Lorentz-conjugate to `-X_lambda`, so these ordinary
holonomies are not hidden reciprocal inversions.

What survives is cleanly separated:

- the stationary scalar clock ratio remains endpoint-exact, `log Q=phi(q)-phi(p)`;
- the full clock–ruler–screen structure transports exactly only with its path label;
- path concatenation still gives an exact groupoid cocycle.

This is progress because it removes a false global shortcut.  It does not select a seam, quotient,
branch, action, source, carrier, density, or physical universe.

## Premise stamps

```text
COPRESENCE = WORKING_INTERPRETIVE_FRAME
METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL
INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED
COMPLETE_WHOLE_SOLUTION_LAW = OPEN
```

No co-presence or signalling premise entered the computation.

## Complete bounded census

- 6/6 frozen `lambda` branches retained: `-2,-1,0,1/2,1,2`.
- 3/3 local events retained per branch: 18 connection/curvature rows.
- 6/6 loops retained per branch: 36 closed transports.
- Loops comprise all three left-invariant great circles and all three registered small
  stereographic coordinate-plane circles.
- No branch, event, or loop was filtered by outcome.

## Local connection result

All 18 local rows have nonzero clock–ruler `nabla X`.  Exact P00 arithmetic gives `-3/25`, independent
of `lambda`.  The full sampled `max|nabla X|` range is `0.12` to `3.4316086668305337`.

The `lambda=-1` and `lambda=+1` degeneracies suppress one connection block each, exactly as the
abstract centralizer atlas anticipated.  Neither suppresses the lambda-independent clock–ruler
block, so neither makes `X_lambda` parallel.

## Curvature and holonomy-algebra result

Production frame curvature:

```text
curvature span rank  = 6 in 18/18 rows
Lie closure rank     = 6 in 18/18 rows
Lorentz residual max = 2.220446049250313e-16
```

Independent coordinate/Torch curvature:

```text
independent span rank       = 6 in 18/18 rows
frame/coordinate scaled max = 2.0532409106266414e-10
```

The commuting subalgebra inside actual holonomy has dimension three at `lambda=-1,+1` and dimension
one for the other four weights.  It is always proper; the full six-dimensional holonomy does not
centralize `X_lambda`.

## Loop result

Across all 36 transports:

```text
nonidentity max-norm range       0.13071754167344443 .. 1.9323417245550665
ordinary closure residual range 0.006996391463313088 .. 1.7994548912612047
maximum Lorentz residual        7.549516567451064e-15
maximum two-half residual       2.886579864025407e-15
maximum fine/coarse residual    7.327471962526033e-15
RK4/DOP853 holdout maximum      4.428124533717437e-13
```

The smallest ordinary residual occurs in the sampled `lambda=1` branch, consistent with its larger
spatial centralizer, but it is nonzero and the curvature algebra remains full.  This ranking does
not select `lambda=1`.

All six sampled `X_lambda`/`-X_lambda` eigenspace-signature comparisons fail Lorentz conjugacy.  The
minimum numerical odd residual is greater than two, but the exact signature obstruction—not that
finite loop sample—is the load-bearing conclusion.

## Interpretation

The parent abstract holonomy atlas said `lambda=+1` could close if actual holonomy reduced to spatial
rotations, and `lambda=-1` could close if it reduced to the complementary `SO(1,2)`.  The complete
nonconstant witness supplies neither reduction: its actual sampled curvature already generates the
full Lorentz algebra.

Therefore an endpoint-only full reciprocal lift is not native to this off-shell witness.  A
path-labeled lift remains exact.  A different on-shell metric could have reduced holonomy, but that
must emerge from its complete geometry rather than be assumed.

No registered current premise in the audited source scope chooses ordinary endpoint closure,
twisted closure, a reciprocal seam, or a quotient.  The choice therefore remains `OPEN`.

## Evidence gates

1. **Preregistered:** yes, committed and pushed before outcome calculation.
2. **Full space or bounded scope justified:** bounded scope justified; complete registered 6 x 3
   local and 6 x 6 loop censuses, not all profiles or loops.
3. **Independently verified load-bearing premise:** yes; coordinate/Torch curvature, exact rational
   local anchor, and fixed-step RK4 transport holdouts.
4. **Every premise audited:** yes; see `PREMISE_LEDGER.tsv`.

Grade remains `VERIFIED-WITH-CAVEATS` because the configurations are off shell, the atlas is bounded,
and no fresh external-model semantic adjudication was run.

## Authority boundary

No startup control, `CANON.md`, research artifact outside this package, frozen evidence, action,
source, carrier, density, bootstrap, mass, `X_max`, dynamics, signalling law, observation fit, GPU
work, or repository organization was changed or selected.
