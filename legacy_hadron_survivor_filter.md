# Legacy Hadron Survivor Filter

Status: working filter, not canonical.
Created: 2026-06-10.

## Purpose

This file is the filtering strategy for mining the legacy mass-emergence,
matter-recycling, pion, baryon, and hadron material in
`udt_canonical_geometry.md` without re-importing the old Dirac Form-T
scaffold.

It is a companion to `mass_emergence_canonical_geometry.md`, not a replacement.
That document is the hard audit/prosecution record. This document is the
recovery atlas: it asks which legacy structures might survive after the new
negative-phi / angular-sector rebuild.

The rule is simple:

> Do not preserve a legacy mechanism. Preserve only metric-native structure,
> exact angular/combinatorial fingerprints, or open targets that can be
> rederived from the current native geometry.

## Inputs

Primary legacy source:

- `udt_canonical_geometry.md`

Current audit/rebuild sources:

- `mass_emergence_canonical_geometry.md`
- `UDT_REBUILD.md`
- `negative_phi_native_geometry.md`

Current native pre-spectrum status:

- negative-phi matter side is a native metric region;
- positive-phi scalar side is the macro/scalar background;
- normalized angular spectrum bridges both sides;
- elementary pre-spectrum branch is the least-action mixed-Hodge harmonic
  carrier branch on `I x S2`;
- `H1` gives the rank-one angular carrier with `N = 3`;
- old `q`, `eta`, and `eta/2` inputs have collapsed into the current branch
  definition;
- full lepton/hadron spectrum coefficients are not yet derived.

## Filter Grades

Use these grades for legacy hadron material:

- `SURVIVES`: follows from current metric/angular facts without Form-T.
- `CANDIDATE`: not yet derived, but has a plausible native target.
- `FINGERPRINT`: exact integer/ratio pattern worth testing, not a mechanism.
- `QUARANTINE`: depends on Dirac Form-T, old boundary choices, fitted shape
  parameters, Standard Model naming, or linearized hadron-scale calculation.
- `DROP`: already null-rejected or contradicted by current native work.

No item may be upgraded above `CANDIDATE` without an explicit derivation from
the current metric frame.

## Hard Rules

1. No Dirac Form-T import.
2. No Standard Model mechanism import.
3. No linearized conclusion at hadronic scale.
4. No fitted mass formula promoted as derived.
5. No single-number match promoted to mechanism.
6. Preserve exact integer fingerprints as clues only.
7. Apply the orchestra frame only after each component is native or explicitly
   labeled as an unproven candidate.

The hadronic-scale warning in the legacy document is binding for this filter:
at the locked legacy depth, `exp(-2 phi0) = 5.04`, so linearization is invalid
by a factor of about five. Any future hadron calculation must use the full
nonlinear metric operator.

## Survivor Ledger

| Legacy item | Filter grade | Why it matters now | Rebuild target |
| --- | --- | --- | --- |
| `H1` triplet / `N = 3` angular carrier | `SURVIVES` | Already native in the current mixed-Hodge branch. Repeated appearance of `3` is no longer just numerology. | Use as first hadron angular carrier before importing any particle labels. |
| Traceless `H1` operator algebra, `3^2 - 1 = 8` | `CANDIDATE` | Legacy `su(3)` language is contaminated by labels, but the dimension count may be native angular operator algebra. | Recompute from the current `H1` projector/domain, not from quark/color assumptions. |
| `3 + 8 = 11` angular coefficient | `FINGERPRINT` | May be a native operator-count identity behind old running/coupling claims. | Test whether it arises from scalar plus traceless `H1` angular operators under positional dilation. |
| Closure/orbit size `7` | `CANDIDATE` | Old origin used `kappa`, but the repeated `7` may encode a native boundary graph, quotient, or angular closure orbit. | Rebuild as a metric/angular boundary graph, not a Form-T `kappa` orbit. |
| Gap/interior number `5` | `FINGERPRINT` | Appears with `7`, golden-ratio/pentagonal structure, and nuclear/hadron factors. | Check whether it is a native interior/endpoint count after the `7`-graph is rederived. |
| `9 = 3^2` | `SURVIVES` as arithmetic, `CANDIDATE` as physics | Natural from `H1` pair/operator space. | Determine which part is scalar, vector, traceless, symmetric, or Hodge-dual in the current branch. |
| `36 = C(9,2)` | `FINGERPRINT` | Appears in old EM/coupling and vector-decay constants. | Test as two-form or pair-count on the native 9-dimensional angular/operator space. |
| `84 = C(9,3)` | `FINGERPRINT` | Old pion coefficient; prior audits already found no operator-pinning derivation. Still a strong combinatorial clue. | Look for a native third exterior/symmetric/Hodge count after the current `H1` domain is fixed. |
| `63 = 9 x 7` | `FINGERPRINT` | Old deuteron denominator; channel-blind as mechanism, but may combine `H1` operator area with closure orbit. | Treat as orchestra clue only: derive both `9` and `7` natively before using the product. |
| `108 = 36 x 3`, `180 = 36 x 5`, ratios such as `5/3` | `FINGERPRINT` | May be mixed pair-count plus carrier/interior counts. | Test only after `36`, `3`, and `5` have native meanings. |
| Baryon sub-cavity and `r*/r_b ~= golden ratio` | `CANDIDATE` | Old derivation used Form-T nodes, but the stable partition could indicate a native negative-phi subdomain split. | Search for a nonlinear metric/domain condition that creates the split without Dirac nodes. |
| Scalar/vector/tensor metric perturbation sectors | `CANDIDATE` | Less dependent on Form-T than spinor eigenmodes; possible hadron orchestra components. | Recompute under positional dilation and full nonlinear negative-phi geometry. |
| Three-exchange nuclear potential | `QUARANTINE` as mechanism, `CANDIDATE` as metric-sector clue | Old version borrows nuclear phenomenology and has channel/form-factor gaps, but the scalar/vector/tensor split may be native. | Replace with native metric perturbation/source-overlap operators. |
| Deuteron `C/63` match | `QUARANTINE` as prediction, `FINGERPRINT` as integer | Existing audit says one-point channel-blind algebraic match. | Use only as a later consistency target after channel operators exist. |
| Single-particle baryon/meson Form-T eigenvalues | `QUARANTINE` | Depend directly on imported Dirac Form-T and fitted boundary choices. | Do not use in the native hadron build. |
| `kappa` as charge/color/flavor mechanism | `QUARANTINE` | Form-T-specific and SM-shaped. | Replace with native angular graph/projector labels only if derived. |
| Neumann-wall confinement | `QUARANTINE` | Boundary condition/mechanism import. | Look for native endpoint, finite-action, Cauchy/projector, or nonlinear domain filters. |
| Linearized hadron calculations | `DROP` for conclusions | Legacy itself flags linearization as invalid at hadronic scale. | Redo with full nonlinear metric operator only. |

## Spectrum-Stage Update: H1 Operator Alphabet

Added 2026-06-10; see `particle_spectrum_native_geometry.md`.

The first spectrum-stage rebuild gives:

```text
H1 dimension = 3
End(H1) dimension = 9
End(H1) = trace 1 + traceless 8
traceless 8 = antisymmetric 3 + symmetric-traceless 5
```

This upgrades the native status of the `9` and `1 + 8` fingerprints:

```text
9 is native as End(H1);
1 + 8 is native as trace/traceless split;
3 + 5 is native as angular tensor split.
```

The exterior algebra of `End(H1)` also gives exact fingerprint locations:

```text
dim Lambda^2 End(H1) = 36
dim Lambda^3 End(H1) = 84
dim Lambda^6 End(H1) = 84
```

This does not yet derive hadron coefficients. The missing step is still the
native selector:

```text
Why should the particle sector use Lambda^2 End(H1), Lambda^3 End(H1), or
their Hodge-dual partners?
```

Therefore the updated status is:

```text
36 and 84 have native operator-algebra locations;
36 and 84 do not yet have native particle-sector selection laws.
```

Additional split audit:

```text
Lambda^2 End(H1) = 8 + 28 = 8 + (3 + 15 + 10) = 36
Lambda^3 End(H1) = 28 + 56 = 28 + (1 + 15 + 30 + 10) = 84
```

The old `7` also has a first native-looking replacement target:

```text
Lambda^2 End(H1) is Hodge-dual to Lambda^7 End(H1).
```

So `7` may be the Hodge-complement grade of a two-form sector in the native
9-dimensional operator alphabet. This is not yet the old seven-position orbit.
It is a candidate native interpretation to test before any legacy orbit
language is restored.

Pre-spectrum dimension-ladder consilience:

```text
q = 1/3 = 1 / dim H1
s = 1/9 = 1 / dim End(H1)
Delta Pi/R = 1/6 = 1 / (2 dim H1)
eta = 1/18 = 2 / dim Lambda^2 End(H1)
eta/2 = 1/36 = 1 / dim Lambda^2 End(H1)
```

This gives `Lambda^2 End(H1)` the first serious selector candidacy. The
remaining proof obligation is functional:

```text
show that the C1 action actually acts on, or projects through,
Lambda^2 End(H1), rather than merely sharing its dimension.
```

The match is also `N=3`-locked:

```text
eta/2 = 1/(4N^2)
dim Lambda^2 End(H) = C(N^2,2)
1/(4N^2) = 1/C(N^2,2) only when N=3.
```

So the current candidate hierarchy is:

```text
first exterior candidate: Lambda^2 End(H1), dimension 36
Hodge-complement grade: 7
next unselected fingerprint: Lambda^3 End(H1), dimension 84
```

Functional selector status:

```text
dimension ladder: strong
N=3 lock: strong
functional Lambda^2 End(H1) map: present through commutator
C1 weighting of that map: open
```

Native commutator map:

```text
[A,B]=AB-BA
Lambda^2 End(H1) -> T8
36-dimensional two-form domain -> 8-dimensional traceless image
trace wedge T8 lies in the kernel
active bracket domain Lambda^2 T8 has dimension 28
```

Isotropic commutator projection:

```text
B: Lambda^2 End(H1) -> T8
B B^T = 3 P_T8
(1/sqrt(3)) B is coisometric onto T8
```

C1 weighting:

```text
eta/2 = 1/36 = 1 / dim Lambda^2 End(H1)
```

So the current two-form selector status is:

```text
C1 supplies uniform domain weight over Lambda^2 End(H1);
the native commutator maps that domain isotropically onto T8;
physical sector interpretation and mass readout remain open.
```

Kernel/image hierarchy:

```text
Lambda^2 End(H1): domain 36, image 8, kernel 28
trace wedge T8: central kernel 8
Lambda^2 T8: active domain 28, image 8, internal kernel 20
image T8: 8 = A3 + S5 = 3 + 5
```

This means old hadron-sector `36` clues should be read first as the C1-weighted
two-form domain, not as the active particle alphabet itself. The first active
operator image is:

```text
T8 = 3 + 5.
```

Three-form / `84` update:

```text
Omega(A,B,C) = Tr(A[B,C])
Omega: Lambda^3 End(H1) -> scalar
dim Lambda^3 End(H1) = 84
```

The trace sector is killed:

```text
trace wedge Lambda^2 T8: kernel 28
active domain Lambda^3 T8: dimension 56
```

Active support under `T8=A3+S5`:

```text
Lambda^3 A3: nonzero
A3 wedge Lambda^2 S5: nonzero
Lambda^2 A3 wedge S5: zero
Lambda^3 S5: zero
```

Updated `84` status:

```text
native functional domain: yes
active full 84-dimensional particle sector: no
mass coefficient: not derived
```

Native `7`-family fractions:

```text
Lambda^2 End(H1):
    image/full domain = 2/9
    kernel/full domain = 7/9

Lambda^2 T8:
    image/active domain = 2/7
    kernel/active domain = 5/7
```

Updated `7` status:

```text
native commutator-filter denominator: yes
legacy seven-position orbit: not restored
hadron/nuclear coefficient: not derived
```

Composite fingerprint update:

```text
84 = dim Lambda^3 End(H1)
84 = 3 * dim Lambda^2 T8 = 3 * 28

108 = A3 * dim Lambda^2 End(H1) = 3 * 36
180 = S5 * dim Lambda^2 End(H1) = 5 * 36
180/108 = 5/3 = S5/A3
```

Updated composite status:

```text
84: native three-form domain, not a mass coefficient
108: native A3-weighted two-form-domain fingerprint, no readout rule
180: native S5-weighted two-form-domain fingerprint, no readout rule
5/3: native S5/A3 image-split ratio, not a coupling by itself
63: weaker 9*7 fingerprint, not yet a native dimension
```

C1 normalization bridge:

```text
eta/2 = 1/36 on Lambda^2 End(H1)
B B^T = 3 P_T8 for the commutator map
(1/36) B B^T = (1/12) P_T8
```

The value `1/12` is exactly the unprojected self-similar C1 action:

```text
S_C1/R = 1/12
(S_C1/R)/3 = 1/36
```

Total image weight:

```text
8 * (1/12) = 2/3
```

matches:

```text
dim Lambda^3 T8 / dim Lambda^3 End(H1) = 56/84 = 2/3.
```

Updated selector status:

```text
C1 normalization bridge: present
mass readout rule: open
```

Projector-trace readout candidate:

```text
W(P)=Tr(P)/12
```

on canonical projectors inside the active `T8` image. This gives:

```text
W(A3)=3/12=1/4
W(S5)=5/12
W(T8)=8/12=2/3
W(S5)/W(A3)=5/3
W(S5)-W(A3)=1/6
```

Updated readout status:

```text
native scalar readout candidate: present
mass mapping: open
```

Readout mode audit:

```text
action readout:
    W(P)=Tr(P)/12
    current best native scalar readout candidate

rank readout:
    Tr(P)
    dimension ledger only

domain composite count:
    dim Lambda^2 End(H1) * Tr(P)
    gives 108 and 180 as fingerprints only

inverse weight:
    1/W(P)
    not selected
```

Guardrail:

```text
Do not promote 108 or 180 to mass coefficients unless the metric derives
count readout rather than action readout.
```

Count-readout gate:

```text
current action readout:
    W(P)=Tr(P)/12

unselected product-count readout:
    C(P)=36*Tr(P)
    C(A3)=108
    C(S5)=180
```

Proof obligation before using `108` or `180` as observable coefficients:

```text
derive an independent product trace over
Lambda^2 End(H1) cells x image-sector labels
from boundary gluing, source overlap, partition trace, or another native
metric readout.
```

Product trace versus commutator gate:

```text
single internal trace:
    supported by phi0 gluing + induced S2 measure

product trace:
    conditional on independent local transfer slots

commutator selector:
    Lambda^2 End(H1) -> T8
    couples/quotients the two-form domain
```

Therefore:

```text
W(P)=Tr(P)/12 is currently licensed;
36*Tr(P) is not yet licensed as an observable coefficient.
```

Quarter-source reinterpretation:

```text
W(A3)=Tr(P_A3)/12=3/12=1/4
```

Updated status:

```text
old source ~= 1/4:
    native projector-weight candidate
    old Form-T/kappa mechanism remains quarantined
```

Taxonomy skeleton update:

```text
mass-emergence container:
    negative-phi region with H1 carrier

operator alphabet:
    End(H1)=trace + A3 + S5 = 1+3+5

active image:
    T8=A3+S5

current readout:
    W(A3)=1/4
    W(S5)=5/12
    W(T8)=2/3

two-form interaction channels:
    A3 wedge A3 -> A3
    A3 wedge S5 -> S5
    S5 wedge S5 -> A3
    trace wedge T8 -> kernel

three-form support:
    Lambda^3 A3 nonzero
    A3 wedge Lambda^2 S5 nonzero
    pure/misaligned S5-heavy blocks filtered
```

Updated high-level status:

```text
native taxonomy skeleton: present
observed particle ID map: open
mass readout: open
```

Best next target:

```text
test whether W(P)=Tr(P)/12 is only a dimension ledger or whether it couples to
radial/negative-phi mass readout in a way that can produce observed spectrum
quantities.
```

Radial coupling route order:

```text
1. test projector-weight coupling W(P)
2. then test two-form channel coupling
3. defer three-form support, product counts, and kernel-energy readings
   until a metric coupling rule selects them
```

Radial projector-weight coupling update:

```text
common radial branch:
    q = 1/3
    S_C1/R = 1/12

sector action on common branch:
    A(P)=Tr(P) * S_C1/R = Tr(P)/12 = W(P)
```

So:

```text
A(A3)=1/4
A(S5)=5/12
A(T8)=2/3
```

Status:

```text
common-branch projector-weighted action: derived
sector-dependent radial exponents q(P): hypothesis only
```

Sector-dependent q gate:

```text
q(P) from S_C1(q_P)/R = W(P):
    finite-action candidates
    but not equal to q=1/3
    would change eta=q/6 and eta/2=q/12
```

Therefore:

```text
common q=1/3:
    current elementary taxonomy

q(P):
    parked as possible excitation/depth branch
```

Two-form channel balance:

```text
domain unit = 1/36
image unit = 1/12

A3 wedge S5 -> S5:
    domain load 15/36 = 5/12
    image action 5/12
    balanced

S5 wedge S5 -> A3:
    residual = +1/36 = eta/2

A3 wedge A3 -> A3:
    residual = -1/6 = -q/2

trace wedge T8:
    load 2/9, no image
```

Status:

```text
native channel-coupling clue: present
particle force/mass interpretation: open
```

Channel local/global quotient:

```text
local channel image ranks:
    A3^A3 -> 3
    A3^S5 -> 5
    S5^S5 -> 3
    total local image = 11

global image:
    T8 = 8

overlap:
    11 - 8 = 3 = repeated A3 image
```

Action correction:

```text
overlap action = 3/12 = 1/4 = W(A3)
local residual = 1/12
global residual = 1/3
1/12 + 1/4 = 1/3
```

Guardrail:

```text
use local channel balances to diagnose interaction structure;
use global quotient T8 for spectrum readout.
```

Taxonomy grammar:

```text
container -> alphabet -> local channels -> global quotient -> readout
```

Blocked shortcuts:

```text
local channel counts -> masses
domain*image product counts -> observables
sector-dependent q(P) -> ground spectrum
kernel dimensions -> hidden energy
```

First branch gate:

```text
first spectrum test:
    single-sector action readout
    W(A3), W(S5), W(T8) on common q=1/3 branch

first interaction test:
    balanced A3 wedge S5 -> S5 channel

defer:
    pure residual channels
    three-form support
    product-count coefficients
```

Single-sector action ladder:

```text
A3 = 1/4
S5 = 5/12
T8 = 2/3

order:
    A3 < S5 < T8

gaps:
    S5-A3 = 1/6
    T8-S5 = 1/4
    T8-A3 = 5/12

shares in T8:
    A3/T8 = 3/8
    S5/T8 = 5/8
```

Status:

```text
classification ladder seed: present
mass ladder: not derived
```

Sector share/channel consistency:

```text
A3/T8 = 3/8
S5/T8 = 5/8

A3 share:
    quotient-overlap share

S5 share:
    balanced A3 wedge S5 channel image share
```

Status:

```text
3/5 split is channel-consistent;
particle assignment remains open.
```

Single-sector to interaction handoff:

```text
W(S5)=5/12
A3 wedge S5 -> S5:
    domain load = 5/12
    image action = 5/12
    residual = 0
```

Status:

```text
S5 is the first composable taxonomy object:
    single-sector readout
    balanced mixed-channel output
```

Pure channel residual ledger:

```text
S5 wedge S5 -> A3:
    residual = +1/36 = eta/2

A3 wedge A3 -> A3:
    residual = -1/6 = -q/2

A3 wedge S5 -> S5:
    residual = 0
```

Status:

```text
pure channels require source/boundary accounting;
mixed A3-S5 remains the only balanced interaction branch.
```

Pure-channel boundary roles:

```text
S5 wedge S5 residual:
    +1/36 = eta/2
    one-sided projected C1 action

A3 wedge A3 residual:
    -1/6 = -q/2
    negative unprojected C1 boundary momentum
```

Status:

```text
residuals are native C1 boundary quantities;
source accounting remains open.
```

Pure-channel source accounting gate:

```text
A3 wedge A3 residual:
    -1/6 + q/2 = 0
    typed role: scalar C1 boundary-momentum deficit

S5 wedge S5 residual:
    +1/36 - eta/2 = 0
    typed role: one-sided H1 transfer surplus

pure pair with typed boundary supply/export:
    (-1/6 + 1/36) + q/2 - eta/2 = 0
```

Status:

```text
pure-channel residuals pass a necessary native accounting gate;
they are still not particle assignments or mass coefficients.
```

Two-form channel admissibility classes:

```text
A3 wedge S5 -> S5:
    freely balanced interaction

S5 wedge S5 -> A3:
    one-sided-transfer coupled
    closes only with eta/2 export

A3 wedge A3 -> A3:
    boundary-momentum coupled
    closes only with q/2 supply

trace wedge T8:
    silent kernel load
    parked until trace-kernel readout is derived
```

Trace-kernel bridge audit:

```text
trace wedge T8 has no commutator image,
but its domain load is exact:

    8 * (1/36) = 2/9
    2/9 = 8 * (eta/2)
    2/9 = 4 * eta
    2/9 = q * W(T8)
```

Status:

```text
not an interaction image;
candidate scalar/trace bridge to the active T8 alphabet.
```

Metric fan-out atlas:

```text
negative phi -> phi=0 boundary -> H1 -> End(H1) -> T8
```

with channel roads:

```text
A3 wedge S5 -> S5:
    freely balanced

S5 wedge S5 -> A3:
    eta/2 transfer-coupled

A3 wedge A3 -> A3:
    q/2 boundary-momentum-coupled

trace wedge T8:
    scalar/trace bridge candidate
```

Status:

```text
this is a native admissibility atlas;
not yet a particle assignment.
```

Trace-image pairing:

```text
dim(trace wedge T8) = dim(image T8) = 8

trace-kernel load = q * active image action
    2/9 = (1/3) * (2/3)

trace load + image action:
    2/9 + 2/3 = 8/9

remaining normalized unit:
    1 - 8/9 = 1/9 = s
```

Status:

```text
candidate scalar-background/active-image quotient rule;
not a mass formula.
```

Scalar-anchor residue:

```text
End(H1) = trace + T8
normalized shares:
    trace = 1/9 = s
    T8 = 8/9

trace-kernel load + active image action:
    2/9 + 2/3 = 8/9

remaining unit:
    1 - 8/9 = 1/9 = trace share
```

Status:

```text
candidate End(H1) quotient identity:
active angular share plus scalar trace anchor.
```

Two-form quotient completion:

```text
scalar anchor : trace bridge : active image
    = 1/9 : 2/9 : 6/9
    = 1 : 2 : 6 in End(H1) ninth-units

completion:
    1/9 + 2/9 + 6/9 = 1
```

Status:

```text
closed quotient/load accounting layer;
not the local channel ledger and not a mass formula.
```

Quotient-channel unit bridge:

```text
trace bridge = trace wedge T8 domain load
    2/9 = 8 domain units

active image = global T8 image action
    2/3 = 8 image units = 24 domain units

scalar anchor = 1/9 = 4 domain units = 2 eta
```

Guard:

```text
scalar anchor is not a missing local two-form channel;
it is the central End(H1) normalization anchor.
```

## Working Hypothesis

The useful legacy hadron material is probably not the old particle mechanism.
It is the integer and operator atlas left behind by the angular sector:

- `3` from the native `H1` carrier;
- `8` from traceless angular operators, if rederived;
- `9` from the `H1` operator/pair space;
- `7` from a still-unrecovered closure or boundary graph;
- `5` from an interior/gap/pentagonal remnant;
- `36`, `63`, `84`, `108`, `180` as composite fingerprints.

This is compatible with the orchestra metaphor. A later hadron result may come
from several native components acting together:

- negative-phi nonlinear domain geometry;
- scale-invariant angular bridge;
- `H1` carrier/projector structure;
- closure/boundary graph structure;
- scalar/vector/tensor metric perturbation sectors;
- finite-action or Cauchy-data filters;
- source-overlap/domain partition effects.

The filter does not assume these components are particles, forces, quarks,
gluons, or Standard Model analogs. Those words are labels only until the metric
demands them.

## Immediate Next Work

1. Audit how negative-phi radial/depth structure couples to the taxonomy:
   `W(A3)`, `W(S5)`, `W(T8)`, two-form channels, or three-form support.
2. Only after radial coupling is known, choose lepton-first or hadron-first
   spectrum construction.
3. Keep `108` and `180` as fingerprints unless an independent product-trace
   readout is derived.
4. Revisit baryon sub-cavity/golden splitting only after the operator/radial
   readout is clear enough to avoid importing Form-T node structure.
5. Attempt mass-spectrum construction only after taxonomy plus radial readout
   are both native.

## Relation To The Existing Audit

`mass_emergence_canonical_geometry.md` remains correct as the skeptical audit:
it shows that the old quantitative hadron spectrum did not survive as an
unfittable prediction.

This file asks a different question:

> After the failed mechanism is removed, which exact metric/angular footprints
> are still worth trying to uncover natively?

That makes this file a forward filter, not a canonization.
