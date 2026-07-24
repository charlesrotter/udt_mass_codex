# Hopf realization deformation audit

## Result

The complete metric contains more phase-related structure than the prior
rank-one seed bridge exposed, but it does not yet supply a native Hopf
carrier deformation space.

The exact scoped ruling is:

```text
RESTRICTED_CONDITIONAL_SEED_DEFORMATION_ONLY
GLOBAL_REALIZATION_REMAINS_COMPLETION_AND_SECTION_DEPENDENT
```

This is a structural classification, not carrier emergence.

## 1. The supplied seed has the expected two-dimensional tangent plane

For

```text
n(phi,delta) = (
  sech(2phi) cos(delta),
  sech(2phi) sin(delta),
  -tanh(2phi)
),
```

the two coordinate tangent vectors are orthogonal and have Gram matrix

```text
diag(4 sech(2phi)^2, sech(2phi)^2).
```

Therefore the map is locally rank two for finite `phi` **if both `phi` and an
independent phase field `delta` are supplied**.

Writing `tan(eta)=exp(2phi)` gives

```text
n=(sin(2eta)cos(delta),sin(2eta)sin(delta),cos(2eta))
```

and Gram matrix `diag(4,sin(2eta)^2)`. The azimuth coordinate degenerates at
the poles, as ordinary polar coordinates do; the target tangent plane itself
does not disappear. A second target chart is required there.

This confirms the capacity of the supplied round-`S2` map. It does not show
that the metric supplies both inputs.

## 2. The actually established coframe bridge is rank one

The complete registered chart has ten coframe fields:

```text
three base + three angular + four shifts,
```

plus an independent scalar `phi`.

On the exact aligned bridge domain with fixed
`delta=xi1-xi2`, differentiating with respect to all eleven fields gives one
nonzero column: angular reciprocal depth. If the separate scalar is chosen
instead, there is again one nonzero column, now the scalar column. Their
identification is conditional source data, not a derived eleventh-field
equation.

Thus:

```text
established aligned bridge: rank-one latitude image
```

The angular shear direction is not another zero column. It points outside
the aligned submanifold on which the existing bridge was defined. Therefore
there is no honest full-chart differential to rank until a shear-compatible,
representative-independent bridge is supplied.

## 3. Angular shear carries a local phase-like angle

For the normalized angular coframe

```text
D = [[exp(-phi), shear],
     [0,        exp(+phi)]],
```

the determinant-normalized angular metric has a traceless pair

```text
X = H11-H22,
Y = 2 H12.
```

Away from isotropy, the angle of `(X,Y)` changes under a shear variation.
This is a genuine local chart-level phase candidate. Its squared magnitude
is basis invariant, while the pair rotates with twice the angular basis
angle.

Two obstructions remain exact:

1. at `phi=0` and zero shear, `X=Y=0`, so the eigenaxis angle is undefined;
2. its components are angular-basis dependent, and no current law solders
   that spin-two eigenaxis angle to the target phase `delta`.

The static seal has `phi=0` but does not force shear to vanish. Where the
angular metric is actually isotropic, however, this candidate cannot define
a section. The result is:

```text
LOCAL_CHART_PHASE_CANDIDATE_NOT_DESCENDED
```

This is a useful ingredient, not a carrier field.

## 4. The four shifts form a phase connection

The exact complete coframe can be written

```text
theta_ang = D(dxi + S dx).
```

Taking the difference of the two rows of `S` gives a base one-form `b` that
enters the phase differential as

```text
d(xi1-xi2) + b.
```

Under a base-dependent torus-coordinate change

```text
xi_i' = xi_i + lambda_i(x),
```

the shift changes by `S_i' = S_i-dlambda_i`, so

```text
b' = b-d(lambda1-lambda2),
db' = db.
```

The curvature and global holonomy are therefore genuine connection data.
They are not a scalar phase:

- if `db` is nonzero, no local scalar `chi` can satisfy `b=dchi`;
- on a contractible one-dimensional interval, `b` is integrable, but its
  exact part is removable by a torus-coordinate gauge unless a physical
  section or boundary framing fixes it;
- on a periodic base, a nonzero period blocks a single-valued global phase.

Thus:

```text
SHIFT_SECTOR_SUPPLIES_PHASE_CONNECTION_NOT_SELECTED_PHASE_SECTION
```

This cleanly separates “how phases compare” from “which phase is physically
present.”

## 5. Fiber dimension is not induced-image rank

The timelike nonnull-`dphi` geometry has an intrinsic unit-direction `S2`
fiber. Its vertical tangent space is two-dimensional. An arbitrary supplied
section, and the independently posited round-`S2` carrier, also have two
local variation functions.

Those facts do not establish a metric-selected section. The stabilizer and
local-Lorentz descent obstructions remain. Counting the dimension of the
available fiber as the rank of a map from metric configurations would be a
type error.

## 6. Global completion census

All twelve registered completion classes were retained and classified in
`GLOBAL_COMPLETION_OUTCOMES.tsv`.

- Boundary, one-cap, `p=0`, lens, singular, periodic, mirror,
  nonorientable, stratified, and nonintegrable classes each retain their
  exact boundary, monodromy, orientation, regularity, or coordinate
  dependencies.
- `FC04_TWO_CAP_P1` supplies the exact conditional `S3` seed only after the
  already disclosed caps, integral basis, quotient, orientation, full range,
  and phase are supplied.
- `FC12_RECIPROCAL_TORIC_DIAGONAL` is an overlapping control family. Only
  its `FC04`-like subcase has that exact seed; its other endpoint classes
  remain live.

No registered completion class supplies a **native full carrier deformation
space**. This is not an absolute theorem over unregistered future higher-jet
or nonlocal laws.

## 7. Bootstrap

Bootstrap remains close to the work, but outside the local assembly:

- local tangent algebra needs no bootstrap;
- current bootstrap may later filter already complete matter-bearing global
  solutions;
- a future explicit `Sigma` could select a section or representative;
- a future explicitly varied global functional could feed closure into
  equations.

Neither future object exists now. No density scan was run, and total proper
density is not operational before complete action, source, mass, volume,
boundary, and global solutions exist.

## What was gained

The missing bridge is more structured than “find a second coordinate.”

The metric currently supplies:

```text
reciprocal depth              -> conditional latitude motion
angular shear                 -> chart-level spin-two axis angle
base-angular shifts           -> phase connection/holonomy
timelike nonnull-dphi geometry -> an S2 fiber
```

What it does not yet supply is the frame-independent assembly rule turning
those ingredients into one selected global section. That is a narrower and
more geometric open problem than postulating a carrier configuration space
from scratch.

## Verification and evidence grade

- SymPy production controller: 15/15 exact/source/census checks pass.
- Independent stdlib/Fraction implementation: 11/11 exact checks, 15/15
  fail-closed catches, and 6/6 agreement checks pass.
- The independent implementation does not import SymPy or the controller.
- All ten source manifests replay byte-exactly.

No fresh zero-context model review was launched because this task did not
authorize additional agents. The package is therefore
`VERIFIED-WITH-CAVEATS`, not fully blind-verified.

## Four banking gates

1. **Preregistered:** yes, commit `7bb7d13`, before outcome algebra ran.
2. **Full or bounded:** complete for all eleven registered field directions,
   twenty preregistered deformation candidates, and twelve registered
   completion classes; arbitrary future nonlocal/higher-jet laws remain
   open.
3. **Independently verified:** yes by a separate exact implementation, but
   no fresh zero-context model review; caveat retained.
4. **Premises audited:** yes in `PREMISE_LEDGER.tsv`; every supplied toric,
   carrier, boundary, bootstrap, and action premise remains visible.

No canonization follows.
