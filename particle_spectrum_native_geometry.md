# Particle Spectrum Native Geometry

Status: working spectrum rebuild, not canonical.
Created: 2026-06-10.

## Purpose

This file starts the particle-spectrum stage after the pre-spectrum closure in
`negative_phi_native_geometry.md`.

The goal is not to recreate Standard Model mechanisms. The goal is to uncover
which particle-spectrum structures the UDT metric already supplies after the
Dirac Form-T scaffold has been removed.

## Allowed Inputs

Allowed at spectrum start:

- UDT positional-dilation metric;
- negative-phi matter region;
- positive-phi scalar/background region;
- scale-invariant normalized angular spectrum bridging both sides;
- elementary branch as the least-action mixed-Hodge harmonic carrier branch on
  `I x S2`;
- `H1` rank-one angular carrier with `N = 3`;
- pre-spectrum outputs:

```text
q=1/3
s=1/9
Delta Pi/R=1/6
eta=1/18
eta/2=1/36
```

Allowed empirical input:

- electron mass anchor, when an absolute mass scale is needed.

Not allowed:

- Dirac Form-T as a native premise;
- `kappa` labels as particle labels;
- Standard Model gauge/mechanism imports;
- linearized hadron-scale conclusions;
- old fitted hadron/lepton mass formulas as derivations.

## 1. Native H1 Operator Alphabet

Implemented in `native_h1_operator_algebra.py`.

Starting point:

```text
H1 is a real rank-3 angular carrier.
```

The first native operator space is therefore:

```text
End(H1) = H1* tensor H1
dim End(H1) = 3 x 3 = 9.
```

This is not a particle claim. It is the operator alphabet naturally available
once the metric has selected the `H1` carrier.

Exact trace split:

```text
End(H1) = scalar trace part + traceless part
9 = 1 + 8.
```

Exact `SO(3)` tensor split of the traceless part:

```text
8 = 3 + 5
```

where:

```text
3 = antisymmetric operators
5 = symmetric traceless operators.
```

The script verifies exactly over rational arithmetic:

```text
trace projector idempotent;
traceless projector idempotent;
antisymmetric projector idempotent;
symmetric-traceless projector idempotent;
trace + traceless reconstructs every operator;
trace + antisymmetric + symmetric-traceless reconstructs every operator;
commutators of traceless operators remain traceless.
```

First spectrum-stage verdict:

```text
The metric-native H1 carrier supplies an exact 9-dimensional operator alphabet.
Its first forced split is 1 + 8, with 8 = 3 + 5 under angular tensor parity.
```

This upgrades the old `8` from a legacy `su(3)`-labeled clue to a native
operator-space fact, but only at the algebraic level.

Not derived here:

```text
compact SU(3);
local gauge principle;
color;
quarks;
hadrons;
closure orbit 7;
coefficient 84;
mass spectrum.
```

The safe statement is:

```text
3 is native as H1;
9 is native as End(H1);
1 + 8 is native as the trace split;
3 + 5 is native as the angular tensor split of the traceless sector.
```

## 2. Immediate Consequences For Spectrum Work

The particle spectrum should now be built in layers:

1. carrier:

```text
H1, N=3
```

2. operator alphabet:

```text
End(H1), dimension 9
```

3. scalar/traceless split:

```text
1 + 8
```

4. angular tensor split:

```text
8 = 3 + 5
```

5. only then test legacy fingerprints:

```text
7, 5, 36, 63, 84, 108, 180.
```

The old hadron material should be read through this order. A coefficient such
as `84 = C(9,3)` is not derived merely because `9` is now native. It becomes a
well-posed target:

```text
Does the metric select a native 3-fold construction on End(H1)?
```

Until that selector is found, `84` remains a fingerprint, not a result.

## 3. Open Selector Problem

The new first hard problem is not mass fitting. It is selector discovery.

Question:

```text
Which native projectors, boundary filters, finite-action conditions, Hodge
operations, or nonlinear domain constraints decide which pieces of End(H1)
become admissible particle-spectrum sectors?
```

Candidate selectors already present in the current corpus:

- least-action mixed-Hodge branch;
- finite-action endpoint filter;
- Cauchy/projector admissibility;
- normalized angular spectrum common to both phi signs;
- H1 harmonic area carrier;
- scalar/traceless trace split;
- antisymmetric/symmetric-traceless angular tensor split;
- nonlinear negative-phi domain geometry.

Next work:

```text
audit which of these selectors acts on End(H1), and whether any of them forces
a 3-fold, 2-fold, or orbit-like construction.
```

This is where lepton and hadron spectrum construction should begin.

## 4. Exterior Fingerprints Of The H1 Operator Alphabet

Implemented in `native_h1_exterior_fingerprints.py`.

Given the native result:

```text
dim End(H1) = 9
```

the exterior algebra of the operator alphabet has exact dimensions:

```text
dim Lambda^0 End(H1) = 1
dim Lambda^1 End(H1) = 9
dim Lambda^2 End(H1) = 36
dim Lambda^3 End(H1) = 84
dim Lambda^4 End(H1) = 126
dim Lambda^5 End(H1) = 126
dim Lambda^6 End(H1) = 84
dim Lambda^7 End(H1) = 36
dim Lambda^8 End(H1) = 9
dim Lambda^9 End(H1) = 1
```

Immediate fingerprints:

```text
36 = dim Lambda^2 End(H1)
84 = dim Lambda^3 End(H1)
84 = dim Lambda^6 End(H1)
```

The `84` therefore has a new native-looking target:

```text
Lambda^3 End(H1)
```

or, by Hodge duality on the 9-dimensional operator alphabet:

```text
Lambda^6 End(H1) = * Lambda^3 End(H1).
```

This does not prove that `84` is a particle coefficient. It proves only:

```text
Once H1 gives End(H1), the numbers 36 and 84 occur exactly as exterior-power
dimensions of the native operator alphabet.
```

Selector still missing:

```text
Why should the particle sector use Lambda^2 End(H1), Lambda^3 End(H1), or
their Hodge-dual partners?
```

This is a cleaner route than the legacy `Sym^3(R7)` story because it does not
require Form-T `kappa`, a legacy closure orbit, or particle labels. But it is
also stricter: without a native selector, `84` remains a fingerprint, not a
derived mass coefficient.

Fourth spectrum-stage verdict:

```text
84 now has a native operator-algebra location, but not yet a native selection
law.
```

This is progress, not closure.

## 5. Structured Splits Of 36, 84, And First Native Location For 7

Implemented in `native_h1_exterior_split_audit.py`.

The exterior fingerprints are not isolated binomial numbers. They inherit the
native splits already found:

```text
End(H1) = 1 + 8
8 = 3 + 5.
```

For the two-form sector:

```text
Lambda^2 End(H1)
  = trace wedge 8  +  Lambda^2 8
  = 8 + 28
  = 36.
```

Using `8 = 3 + 5`:

```text
Lambda^2 8
  = Lambda^2 3  +  3 tensor 5  +  Lambda^2 5
  = 3 + 15 + 10
  = 28.
```

Therefore:

```text
36 = 8 + (3 + 15 + 10).
```

For the three-form sector:

```text
Lambda^3 End(H1)
  = trace wedge Lambda^2 8  +  Lambda^3 8
  = 28 + 56
  = 84.
```

Using `8 = 3 + 5`:

```text
Lambda^3 8
  = Lambda^3 3
    + Lambda^2 3 tensor 5
    + 3 tensor Lambda^2 5
    + Lambda^3 5
  = 1 + 15 + 30 + 10
  = 56.
```

Therefore:

```text
84 = 28 + (1 + 15 + 30 + 10).
```

These are exact structural decompositions of the native operator alphabet.
They are stronger than a loose numerical coincidence because every term is
forced by:

```text
H1 dimension 3;
End(H1) trace split 1+8;
angular tensor split 8=3+5;
exterior algebra.
```

The selector is still not closed:

```text
The metric has not yet been shown to choose Lambda^2 End(H1) or
Lambda^3 End(H1) as particle sectors.
```

However, the old `7` also gets its first native-looking location. In the
9-dimensional operator alphabet:

```text
* Lambda^2 End(H1) = Lambda^7 End(H1).
```

So:

```text
7 = Hodge-complement grade of the two-form sector in End(H1).
```

This is not the old seven-position closure orbit. It is a native grade
relation:

```text
pair sector grade 2  <->  complement grade 7.
```

Fifth spectrum-stage verdict:

```text
36 and 84 are now structured exterior fingerprints of the native H1 operator
alphabet. The number 7 has a first native Hodge-grade interpretation as the
dual grade to a two-form sector. A particle-sector selector is still required.
```

## 6. Pre-Spectrum Constants As A Dimension Ladder

Implemented in `native_prespectrum_dimension_ladder.py`.

The pre-spectrum closure produced:

```text
q = 1/3
s = 1/9
Delta Pi/R = 1/6
eta = 1/18
eta/2 = 1/36
```

The native operator alphabet gives:

```text
dim H1 = 3
dim End(H1) = 9
dim Lambda^2 End(H1) = 36
```

These match exactly:

```text
q = 1 / dim H1
s = 1 / dim End(H1)
Delta Pi/R = 1 / (2 dim H1)
eta = 2 / dim Lambda^2 End(H1)
eta/2 = 1 / dim Lambda^2 End(H1)
```

This is the first nontrivial selector candidate.

The metric did not merely produce `1/36` as a free number. In the current
operator alphabet:

```text
1/36 = 1 / dim Lambda^2 End(H1).
```

Therefore the two-form sector:

```text
Lambda^2 End(H1)
```

is no longer just a legacy fingerprint target. It is the first exterior sector
whose dimension is already imprinted in the pre-spectrum C1 action.

Candidate selector statement:

```text
The elementary branch C1 action selects the normalized two-form operator
sector of End(H1).
```

Status:

```text
CANDIDATE, not yet DERIVED.
```

What is derived:

```text
the exact dimension equalities.
```

What is not yet derived:

```text
that the C1 action functionally acts on Lambda^2 End(H1);
that Lambda^2 End(H1) is a particle sector;
that its Hodge complement Lambda^7 End(H1) is the old closure orbit;
that Lambda^3 End(H1) and the coefficient 84 are selected.
```

Still, the jigsaw pattern tightened:

```text
3  -> H1
9  -> End(H1)
36 -> Lambda^2 End(H1)
7  -> Hodge-complement grade to Lambda^2 in 9D
84 -> next exterior/Hodge-paired three-form fingerprint
```

Sixth spectrum-stage verdict:

```text
The pre-spectrum constants align exactly with the native H1 operator dimension
ladder through Lambda^2 End(H1). This gives a serious native selector candidate
for the two-form sector, while leaving the three-form/84 selector open.
```

## 7. The Two-Form Match Is N=3-Locked

Implemented in `native_twoform_selector_n3_lock.py`.

For a general rank-`N` carrier `H`, the one-graph branch would give:

```text
q = 1/N
eta/2 = 1/(4N^2).
```

The operator alphabet would have:

```text
dim End(H) = N^2
dim Lambda^2 End(H) = C(N^2,2).
```

The C1 side action matches the reciprocal two-form dimension only if:

```text
1/(4N^2) = 1/C(N^2,2)
```

equivalently:

```text
C(N^2,2) = 4N^2
N^2(N^2-1)/2 = 4N^2
N^2 - 1 = 8
N = 3.
```

Thus:

```text
eta/2 = 1/dim Lambda^2 End(H)
```

is not a generic dimension coincidence. It is locked to:

```text
dim H = 3.
```

Seventh spectrum-stage verdict:

```text
The projected C1 side action selects the reciprocal of the two-form operator
dimension only on the H1/N=3 branch. This strengthens Lambda^2 End(H1) as the
first native exterior-sector candidate.
```

Still not claimed:

```text
the C1 functional has been proven to act on Lambda^2 End(H1);
Lambda^2 End(H1) is a particle sector;
the Hodge-dual grade 7 is a closure orbit;
Lambda^3 End(H1), dimension 84, is selected.
```

## 8. Functional Selector Audit

Implemented in `native_twoform_functional_selector_audit.py`.

The current evidence for `Lambda^2 End(H1)` has two parts:

```text
exact dimension match:
    eta/2 = 1/dim Lambda^2 End(H1)

N=3 lock:
    this match happens only for dim H = 3.
```

That is strong, but it is still a dimensional selector candidate. A functional
selector must show that a native action, boundary form, curvature, or source
operator actually acts on:

```text
Lambda^2 End(H1).
```

Candidate routes:

```text
1. dimension ladder
   status: strong dimensional selector candidate
   gap: does not prove functional action on Lambda^2 End(H1)

2. C1 boundary symplectic form
   status: native two-form exists
   gap: it acts on boundary phase-space pairs delta Pi wedge delta f,
        not yet on unordered pairs of End(H1) operator directions

3. H1 harmonic area carrier
   status: native exterior/top-form structure on H1
   gap: selects Lambda^3 H1 -> dOmega_S2, not Lambda^2 End(H1)

4. angular connection/curvature
   status: promising native route
   gap: S2/H1 connection first acts in the antisymmetric 3; must show whether
        the full End(H1) pair space is involved

5. scalar/vector/tensor metric perturbation split
   status: possible orchestra ingredient
   gap: gives sector ingredients, not a two-form selector by itself
```

Functional-selector verdict:

```text
No route currently proves a functional Lambda^2 End(H1) particle-sector
selector.
```

Superseded immediately by the commutator audit in section 9:

```text
the operator commutator does provide a native functional two-form map.
The remaining gap is not existence of a two-form map, but C1 coupling to it.
```

Best next target:

```text
derive an End(H1)-valued boundary field, curvature, or source-overlap operator
whose native action is an alternating two-form over the 9-dimensional operator
alphabet.
```

This is now the bottleneck between pre-spectrum and particle-sector spectrum:

```text
dimension ladder: strong;
functional selector: open.
```

## 9. Native Commutator Two-Form On End(H1)

Implemented in `native_endh1_commutator_twoform.py`.

There is a canonical alternating operation on the operator alphabet:

```text
[A,B] = AB - BA.
```

Since it is antisymmetric in `(A,B)`, it defines a native map:

```text
Lambda^2 End(H1) -> End(H1).
```

Because every commutator is traceless, the image actually lands in:

```text
T8 = traceless End(H1).
```

Exact ranks:

```text
rank [End(H1), End(H1)] = 8
rank [T8, T8] = 8
rank [trace, T8] = 0
```

Thus:

```text
Lambda^2 End(H1) -> T8
36-dimensional domain -> 8-dimensional image.
```

The trace-wedge part is central:

```text
trace wedge T8 has dimension 8
[trace, T8] = 0.
```

The active commutator domain is:

```text
Lambda^2 T8
```

with:

```text
dim Lambda^2 T8 = 28
kernel dimension = 20
image dimension = 8.
```

Using the angular tensor split:

```text
T8 = A3 + S5
```

the bracket ranks are:

```text
[A3, A3] -> A3 rank 3
[A3, S5] -> S5 rank 5
[S5, S5] -> A3 rank 3
```

This is important because it is a genuine native functional two-form structure:

```text
Lambda^2 End(H1) -> T8.
```

It uses only operator composition on the already-native `H1` carrier. It does
not require:

```text
Form-T;
kappa;
quarks;
color;
local gauge principle;
Standard Model imports.
```

Updated selector status:

```text
dimension selector:
    eta/2 = 1/dim Lambda^2 End(H1), N=3-locked

functional two-form:
    commutator map Lambda^2 End(H1) -> T8

remaining gap:
    show that the C1 side action weights or normalizes this commutator
    two-form in the particle sector.
```

Ninth spectrum-stage verdict:

```text
The native operator alphabet now supplies both:
1. a C1-imprinted two-form dimension, dim Lambda^2 End(H1)=36;
2. a functional alternating two-form map, Lambda^2 End(H1)->T8.

This is the first concrete bridge from pre-spectrum constants to a native
operator-sector mechanism. It is not yet a mass spectrum.
```

## 10. Isotropic Commutator Projection And C1 Domain Weight

Implemented in `native_commutator_isotropy_c1_weight.py`.

Let:

```text
B: Lambda^2 End(H1) -> T8
```

be the commutator map:

```text
B(A wedge C) = [A,C].
```

Using the standard trace/Frobenius pairing on `End(H1)`, the exact audit gives:

```text
B B^T = 3 P_T8
```

where:

```text
P_T8 = projector onto the traceless 8-dimensional subspace.
```

Therefore the commutator two-form is isotropic onto `T8`. After normalization:

```text
(1/sqrt(3)) B
```

is a coisometry onto `T8`.

Exact data:

```text
dim Lambda^2 End(H1) = 36
rank image = 8
kernel dimension = 28
trace(B B^T) = 24
singular square on T8 = 3
```

The C1 side action is:

```text
eta/2 = 1/36.
```

So the C1 side action is exactly the uniform unit weight over the
two-form operator domain:

```text
eta/2 = 1 / dim Lambda^2 End(H1).
```

This sharpens the selector picture:

```text
domain measure:
    C1 supplies uniform weight 1/36 over Lambda^2 End(H1)

functional map:
    commutator sends Lambda^2 End(H1) isotropically onto T8

normalized image:
    (1/sqrt(3))[.,.] is the canonical coisometric projection onto T8
```

This is a native bridge between:

```text
pre-spectrum C1 side action
and
operator-sector traceless dynamics.
```

Still not claimed:

```text
particle masses;
hadron spectrum;
local gauge principle;
quarks/color;
that every Lambda^2 End(H1) cell is physically occupied;
that the kernel has been interpreted physically.
```

Tenth spectrum-stage verdict:

```text
The C1 side action now has a precise native operator meaning: it is the
uniform domain weight on Lambda^2 End(H1), whose commutator map projects
isotropically onto the traceless 8-sector. This closes the existence and
normalization parts of the two-form selector, leaving physical sector
interpretation and mass readout open.
```

## 11. Kernel/Image Split Of The Commutator Selector

Implemented in `native_commutator_kernel_image_split.py`.

The full two-form domain decomposes as:

```text
Lambda^2 End(H1)
  = trace wedge T8
    + Lambda^2 A3
    + A3 wedge S5
    + Lambda^2 S5
```

with dimensions:

```text
8 + 3 + 15 + 10 = 36.
```

The commutator acts as:

```text
[trace, T8] = 0
[A3, A3] -> A3
[A3, S5] -> S5
[S5, S5] -> A3
```

Exact block ranks:

```text
trace wedge T8:
    domain 8, image 0, kernel 8

Lambda^2 A3:
    domain 3, image 3, kernel 0

A3 wedge S5:
    domain 15, image 5, kernel 10

Lambda^2 S5:
    domain 10, image 3, kernel 7
```

Combined active sector:

```text
Lambda^2 T8:
    domain 28, image 8, kernel 20
```

Full selector:

```text
Lambda^2 End(H1):
    domain 36, image 8, kernel 28
```

Interpretation:

```text
The C1-weighted two-form domain is larger than the active image.
The commutator filters it down to the traceless 8-sector.
The image keeps the angular tensor split:
    A3 image + S5 image = 3 + 5.
```

This gives a native operator-orchestra pattern:

```text
domain: 36 two-form cells
central silent sector: 8
active traceless domain: 28
internal active kernel: 20
image: 8 = 3 + 5
```

No particle labels are needed for this statement.

Eleventh spectrum-stage verdict:

```text
The metric-native operator algebra now supplies a weighted two-form domain,
an isotropic commutator projection, and an intrinsic kernel/image filter.
The first active spectrum alphabet is the traceless image T8=3+5, not the full
36-dimensional two-form domain.
```

## 12. Native Three-Form Location For 84

Implemented in `native_commutator_threeform_84_audit.py`.

The commutator and trace pairing define a canonical alternating three-form:

```text
Omega(A,B,C) = Tr(A[B,C]).
```

Its natural full domain is:

```text
Lambda^3 End(H1)
```

with:

```text
dim Lambda^3 End(H1) = 84.
```

Therefore `84` now has a native functional location:

```text
84 = dimension of the full domain of Tr(A[B,C]).
```

But the form kills trace arguments:

```text
Omega(trace, X, Y) = 0.
```

So:

```text
trace wedge Lambda^2 T8
```

is a 28-dimensional kernel, and the active domain is:

```text
Lambda^3 T8
```

with:

```text
dim Lambda^3 T8 = 56.
```

Using:

```text
T8 = A3 + S5
```

the active three-form domain splits as:

```text
Lambda^3 T8
  = Lambda^3 A3
    + Lambda^2 A3 wedge S5
    + A3 wedge Lambda^2 S5
    + Lambda^3 S5
```

with dimensions:

```text
1 + 15 + 30 + 10 = 56.
```

The exact audit finds nonzero three-form support in:

```text
Lambda^3 A3:
    domain 1, nonzero

A3 wedge Lambda^2 S5:
    domain 30, nonzero
```

and zero support in:

```text
Lambda^2 A3 wedge S5:
    domain 15, zero

Lambda^3 S5:
    domain 10, zero.
```

This is another native filter:

```text
full three-form domain: 84
trace kernel: 28
active T8 domain: 56
nonzero support: Lambda^3 A3 plus A3 wedge Lambda^2 S5
```

Twelfth spectrum-stage verdict:

```text
84 is no longer only a legacy fingerprint: it is the full native domain
dimension of the canonical three-form Tr(A[B,C]) on End(H1). However, the
active nonzero three-form is filtered to the traceless sector, with a 28D trace
kernel and 56D active domain. This is a native functional location for 84, not
yet a mass coefficient or particle count.
```

## 13. Native Dimension Fractions From The Commutator Filter

Implemented in `native_commutator_dimension_fractions.py`.

The two-form selector gives exact domain/image/kernel fractions.

Full two-form domain:

```text
Lambda^2 End(H1):
    domain = 36
    image = 8
    kernel = 28
```

Therefore:

```text
image/full domain = 8/36 = 2/9
kernel/full domain = 28/36 = 7/9
```

The central trace kernel is:

```text
trace wedge T8 = 8
```

so:

```text
central kernel/full domain = 8/36 = 2/9
active domain/full domain = 28/36 = 7/9.
```

Inside the active traceless two-form domain:

```text
Lambda^2 T8:
    domain = 28
    image = 8
    kernel = 20
```

Therefore:

```text
image/active domain = 8/28 = 2/7
kernel/active domain = 20/28 = 5/7.
```

Block fractions:

```text
Lambda^2 A3:
    image fraction = 3/3 = 1

A3 wedge S5:
    image fraction = 5/15 = 1/3
    kernel fraction = 10/15 = 2/3

Lambda^2 S5:
    image fraction = 3/10
    kernel fraction = 7/10
```

Three-form fractions:

```text
Lambda^3 End(H1):
    full domain = 84
    trace kernel = 28
    active domain = 56
```

so:

```text
trace kernel/full domain = 1/3
active domain/full domain = 2/3.
```

This creates a native home for old `7`-family fingerprints:

```text
2/7 = active two-form image fraction
5/7 = active two-form kernel fraction
7/9 = active two-form domain fraction inside Lambda^2 End(H1)
```

These are not imported nuclear couplings or particle labels. They are exact
fractions of the native commutator selector.

Thirteenth spectrum-stage verdict:

```text
The number 7 now appears natively in the active two-form filter, not as a
seven-position legacy orbit: Lambda^2 T8 filters to image/kernel fractions
2/7 and 5/7. Legacy uses of 2/7, 5/7, and 7 should be retested against this
commutator-filter origin.
```

## 14. Legacy Composite Fingerprint Audit

Implemented in `native_legacy_composite_fingerprint_audit.py`.

The new native hierarchy gives:

```text
dim H1 = 3
dim End(H1) = 9
T8 = A3 + S5 = 3 + 5
dim Lambda^2 End(H1) = 36
dim Lambda^2 T8 = 28
dim Lambda^3 End(H1) = 84
dim Lambda^3 T8 = 56
```

Retesting old composite fingerprints:

```text
84 = dim Lambda^3 End(H1)
84 = H1 * Lambda^2 T8 = 3 * 28
84 = trace kernel 28 + active three-form domain 56
```

So `84` is now native as a full three-form domain.

The old `108` and `180` fingerprints also have a clean native reading:

```text
108 = A3 * Lambda^2 End(H1) = 3 * 36
180 = S5 * Lambda^2 End(H1) = 5 * 36
```

Therefore:

```text
180 / 108 = 5/3 = S5 / A3.
```

This means:

```text
108 and 180 are C1 two-form-domain composites weighted by the active image
split 3+5.
```

But no readout rule has yet mapped them to observables.

The old `63` is weaker:

```text
63 = End(H1) * active-two-form denominator = 9 * 7.
```

That is a native fingerprint, but not yet a native dimension of a constructed
operator space or a trace/invariant.

Fourteenth spectrum-stage verdict:

```text
84, 108, 180, and 5/3 now have native operator-algebra fingerprints. 84 is a
genuine three-form domain. 108 and 180 are two-form-domain composites weighted
by A3 and S5. 63 remains only a weaker 9*7 fingerprint until a native readout
or operator space produces it directly.
```

## 15. C1 Weight Closure Through The Commutator

Implemented in `native_commutator_c1_weight_closure.py`.

The two-form selector has:

```text
dim Lambda^2 End(H1) = 36
eta/2 = 1/36.
```

The commutator isotropy result gives:

```text
B B^T = 3 P_T8.
```

Therefore uniform C1 side weight over the two-form domain pushes forward to:

```text
(1/36) B B^T = (1/12) P_T8.
```

But:

```text
S_C1/R = 1/12
```

for the self-similar `q=1/3` branch before H1 projection, while:

```text
(S_C1/R)/3 = 1/36 = eta/2.
```

So the same C1 action appears in two equivalent native forms:

```text
H1-projected side action:
    1/36 on Lambda^2 End(H1)

commutator-projected image action:
    1/12 on each T8 image direction.
```

The total image weight is:

```text
8 * (1/12) = 2/3.
```

This matches the three-form filter:

```text
dim Lambda^3 T8 / dim Lambda^3 End(H1) = 56/84 = 2/3.
```

and:

```text
trace-kernel fraction = 28/84 = 1/3.
```

Fifteenth spectrum-stage verdict:

```text
The C1 side action, the commutator two-form selector, and the three-form
trace filter now share one exact normalization pattern:

1/36 -> commutator isotropy -> 1/12 on T8,
total T8 image weight 2/3 = active three-form fraction.

This is a native normalization bridge between the two-form and three-form
operator layers. It is still not a mass readout.
```

## 16. Particle Alphabet Status Before Mass Readout

Implemented in `native_particle_alphabet_status.py`.

Current derived/native alphabet:

```text
H1:
    rank 3 harmonic angular carrier

End(H1):
    dimension 9
    split 1 + 8

T8:
    active traceless commutator image
    split 3 + 5

Lambda^2 End(H1):
    C1-weighted selector domain
    dimension 36
    uniform side weight eta/2 = 1/36

commutator selector:
    Lambda^2 End(H1) -> T8
    isotropic with B B^T = 3 P_T8

Lambda^3 End(H1):
    native three-form domain for Tr(A[B,C])
    dimension 84

Lambda^3 T8:
    active three-form domain
    dimension 56
    active fraction 2/3
```

Native fingerprints now explained or partly explained:

```text
3:
    H1 and A3

5:
    S5

7:
    active two-form image/kernel denominator

8:
    T8 image

9:
    End(H1)

36:
    C1-weighted Lambda^2 End(H1)

84:
    Lambda^3 End(H1) domain

108:
    3 * 36

180:
    5 * 36

5/3:
    S5/A3
```

Still weak:

```text
63:
    9 * 7 fingerprint only;
    not yet a native dimension or invariant.
```

Still open:

```text
mass readout rule.
```

Sixteenth spectrum-stage verdict:

```text
The native particle alphabet is now substantially constrained before any mass
formula is attempted. The next legitimate step is not to fit masses, but to
derive a readout rule from this operator hierarchy to spectrum observables.
```

## 17. Projector-Trace Readout Candidate

Implemented in `native_projector_trace_readout_candidate.py`.

The C1-weighted commutator selector gives:

```text
(1/36) B B^T = (1/12) P_T8.
```

Therefore every active `T8` image direction carries the same native weight:

```text
1/12.
```

The only label-free scalar readout available from a canonical image-sector
projector `P` is its trace. This suggests the candidate rule:

```text
W(P) = Tr(P) / 12.
```

For the canonical angular tensor split:

```text
T8 = A3 + S5
```

the projector traces are:

```text
Tr(P_A3) = 3
Tr(P_S5) = 5
Tr(P_T8) = 8.
```

So the readout weights are:

```text
W(A3) = 3/12 = 1/4
W(S5) = 5/12
W(T8) = 8/12 = 2/3.
```

Exact consequences:

```text
W(S5) / W(A3) = 5/3
W(S5) - W(A3) = 1/6
W(A3) + W(S5) = W(T8) = 2/3.
```

This is the first native readout candidate because it uses only:

```text
C1 side action;
commutator isotropy;
canonical projector trace.
```

It does not use:

```text
particle labels;
Standard Model charges/couplings;
legacy kappa;
fitted mass data.
```

Seventeenth spectrum-stage verdict:

```text
The metric now supplies a minimal scalar readout candidate on the active
operator image: W(P)=Tr(P)/12. It produces native weights 1/4, 5/12, and 2/3
for A3, S5, and T8 respectively. This is a readout rule candidate, not yet a
mass formula.
```

## 18. Readout Mode Audit

Implemented in `native_readout_mode_audit.py`.

The same operator hierarchy supplies several different scalar-looking outputs.
They must not be conflated.

For `P = A3, S5, T8`:

```text
rank readout:
    D(P)=Tr(P)

C1 action readout:
    W(P)=Tr(P)/12

domain composite count:
    C(P)=dim Lambda^2 End(H1) * Tr(P)

inverse weight:
    1/W(P)
```

Outputs:

```text
A3:
    rank = 3
    W = 1/4
    composite count = 108
    inverse weight = 4

S5:
    rank = 5
    W = 5/12
    composite count = 180
    inverse weight = 12/5

T8:
    rank = 8
    W = 2/3
    composite count = 288
    inverse weight = 3/2
```

Current status:

```text
C1 action readout:
    best current native scalar readout candidate

rank:
    dimension ledger only

domain composite count:
    fingerprint only; produces 108 and 180 but no observable rule yet

inverse weight:
    not selected; do not use without a variational or spectral reason
```

Eighteenth spectrum-stage verdict:

```text
The only current native action readout candidate is W(P)=Tr(P)/12. Counts such
as 108 and 180 remain fingerprints, not mass coefficients, until the metric
selects count readout rather than action readout.
```

## 19. Count-Readout Gate

Implemented in `native_count_readout_gate.py`.

There is a tempting count mode:

```text
C(P) = dim Lambda^2 End(H1) * Tr(P)
     = 36 * Tr(P).
```

This gives:

```text
C(A3) = 36 * 3 = 108
C(S5) = 36 * 5 = 180
C(T8) = 36 * 8 = 288.
```

But this is not the same as the current commutator action readout:

```text
W(P)=Tr(P)/12.
```

The current commutator selector couples the two-form domain to the `T8` image:

```text
Lambda^2 End(H1) -> T8.
```

It does not by itself provide an independent tensor-product trace over:

```text
Lambda^2 End(H1) cells x image-sector labels.
```

Therefore:

```text
108 and 180 require an additional product-trace readout rule.
```

Possible native sources for such a rule:

```text
boundary gluing trace;
source-overlap trace;
separate partition trace;
independent domain/image factorization.
```

None is derived here.

Nineteenth spectrum-stage verdict:

```text
The current native action readout is W(P)=Tr(P)/12. The composite counts 108
and 180 are available only if the metric supplies an independent product-trace
readout. That product-trace rule is now the proof obligation before using those
numbers as observable coefficients.
```

## 20. Product Trace Versus Commutator Gate

Implemented in `native_product_trace_vs_commutator_gate.py`.

Existing pre-spectrum work supports:

```text
single internal trace:
    phi0 internal gluing + induced S2 measure
    operation: Tr over an internal boundary label
```

It also supports product traces only conditionally:

```text
product trace:
    Tr(K1 tensor K2) = Tr(K1) Tr(K2)
    gate: independent local transfer slots must be derived.
```

The current spectrum operator is different:

```text
commutator selector:
    Lambda^2 End(H1) -> T8
```

This map couples and quotients the two-form domain into:

```text
image + kernel.
```

Therefore the count:

```text
dim Lambda^2 End(H1) * Tr(P)
```

is not licensed by the commutator selector. It would require:

```text
Lambda^2 End(H1) cells
```

and:

```text
image-sector labels
```

to be independent internal trace slots.

Allowed now:

```text
W(P)=Tr(P)/12;
single internal trace over canonical image projectors.
```

Not allowed yet:

```text
108=36*3 as an observable coefficient;
180=36*5 as an observable coefficient;
mass formulas using domain*image count.
```

Twentieth spectrum-stage verdict:

```text
The metric currently licenses commutator-coupled action readout, not
independent product-count readout. Upgrading 108 or 180 from fingerprints to
observable coefficients requires a separate derivation of independent
domain/image transfer slots.
```

## 21. Quarter Source Reinterpretation

Implemented in `native_quarter_source_reinterpretation.py`.

The legacy corpus contained a recurring:

```text
source ~= 1/4
```

in Form-T / `kappa` language.

The new native readout gives:

```text
W(A3)=Tr(P_A3)/12.
```

Since:

```text
Tr(P_A3)=3
```

we get:

```text
W(A3)=3/12=1/4.
```

Inputs:

```text
T8=A3+S5;
commutator image unit = 1/12;
projector trace Tr(P_A3)=3.
```

Updated status:

```text
1/4 has a native projector-weight interpretation.
```

Quarantine remains:

```text
do not restore kappa;
do not restore Form-T source machinery;
do not treat A3 as a particle label yet;
do not treat 1/4 as a mass coefficient.
```

Twenty-first spectrum-stage verdict:

```text
The old quarter source can be reinterpreted natively as the A3 projector trace
weight under the C1-normalized commutator readout. This preserves the number
while replacing the mechanism.
```

## 22. First Native Particle-Taxonomy Skeleton

Implemented in `native_particle_taxonomy_skeleton.py`.

Lay framing:

```text
The negative-phi metric supplies the mass-emergence container.
The H1/operator/commutator structure supplies the first taxonomy of what can
live inside that container.
```

Native alphabet:

```text
End(H1) = trace + A3 + S5
        = 1 + 3 + 5.
```

The trace sector is:

```text
dimension 1;
value/normalization scalar;
central under the commutator;
not part of the active T8 image.
```

The active image is:

```text
T8 = A3 + S5.
```

Primary active sectors:

```text
A3:
    dimension 3
    antisymmetric / rotation-like traceless image
    readout weight W(A3)=1/4

S5:
    dimension 5
    symmetric-traceless / shape-like traceless image
    readout weight W(S5)=5/12

T8:
    dimension 8
    full active traceless image
    readout weight W(T8)=2/3
```

Two-form interaction taxonomy:

```text
trace wedge T8:
    domain 8
    image 0
    kernel 8
    central silent channel

A3 wedge A3:
    domain 3
    image 3
    kernel 0
    self-interaction returns A3

A3 wedge S5:
    domain 15
    image 5
    kernel 10
    mixed interaction returns S5

S5 wedge S5:
    domain 10
    image 3
    kernel 7
    shape-shape interaction returns A3
```

Three-form support taxonomy:

```text
trace wedge Lambda^2 T8:
    domain 28
    support 0
    trace kernel

Lambda^3 A3:
    domain 1
    nonzero
    orientation-like A3 triple support

Lambda^2 A3 wedge S5:
    domain 15
    support 0
    filtered out

A3 wedge Lambda^2 S5:
    domain 30
    nonzero
    mixed A3/S5 support

Lambda^3 S5:
    domain 10
    support 0
    pure S5 triple filtered out
```

Twenty-second spectrum-stage verdict:

```text
The metric now supplies a taxonomy before particle names:

container -> alphabet -> active image -> active sector split -> interaction
channels -> three-form support.

This is more than a ratio ladder. It is the first native sorting machinery for
mass-emergent sectors. The map from this taxonomy to observed particle species
and masses remains open.
```

## 23. Spectrum Path Decision

Implemented in `native_spectrum_path_decision.py`.

Three possible next paths:

```text
lepton first:
    available:
        C1 action readout W(P)
        A3/S5/T8 projector weights
        electron anchor allowed
    missing:
        native depth ladder or radial readout coupling to W(P)
        generation/typing rule
    risk:
        fitting ratios before deriving the depth rule

hadron first:
    available:
        A3/S5 active image
        two-form interaction channels
        three-form support
        localized legacy fingerprints 84/108/180
    missing:
        product-trace readout
        source-overlap/domain partition rule
        mass readout
    risk:
        importing particle labels too early

taxonomy first:
    available:
        operator taxonomy skeleton
        action readout candidate
        product-count gate
    missing:
        radial/negative-phi coupling to sector weights
```

Decision:

```text
taxonomy first -> radial coupling audit -> lepton/hadron branch.
```

Reason:

```text
The operator taxonomy is native, but mass readout requires showing how
negative-phi radial/depth structure couples to the sector weights.
```

Twenty-third spectrum-stage verdict:

```text
The next legitimate frontier is radial coupling: determine whether the
negative-phi mass-emergence side couples to W(A3), W(S5), W(T8), two-form
channels, or three-form support. Particle labels remain premature.
```

## 24. Radial Coupling Audit

Implemented in `native_radial_coupling_audit.py`.

Candidate coupling routes:

```text
1. projector-weight coupling
   form:
       radial action/depth depends on W(P)=Tr(P)/12
   native support:
       C1 side action;
       commutator isotropy;
       projector trace readout.
   missing:
       operator equation coupling radial negative-phi depth to W(P)

2. two-form channel coupling
   form:
       radial readout depends on two-form channel image/kernel fractions
   native support:
       2/7 and 5/7 active filter;
       channel rules A3-A3, A3-S5, S5-S5.
   missing:
       physical meaning of kernel/image energy or source overlap

3. three-form support coupling
   form:
       radial readout depends on Tr(A[B,C]) support
   native support:
       84 full domain;
       56 active domain;
       nonzero A3^3 and A3*S5^2 support.
   missing:
       why radial depth reads a three-form scalar

4. product-count coupling
   form:
       radial readout depends on 36*Tr(P)
   missing:
       independent product trace

5. kernel-energy coupling
   form:
       radial readout depends on filtered-out modes
   missing:
       native rule assigning energy/action to kernel modes
```

Decision:

```text
best first test:
    projector-weight coupling

reason:
    it is the only candidate with a native scalar action readout already
    derived.
```

Next proof target:

```text
derive or reject an equation where radial negative-phi depth/action is
multiplied, shifted, or constrained by W(P).
```

Twenty-fourth spectrum-stage verdict:

```text
The taxonomy is ready for a radial coupling test. The least speculative path
is to ask whether the radial negative-phi sector reads the projector action
weights W(A3), W(S5), or W(T8). Do not use product counts, kernels, or
three-form support as mass inputs unless their radial coupling is derived.
```

## 25. Radial Projector-Weight Coupling

Implemented in `native_radial_projector_weight_coupling.py`.

The self-similar C1 radial branch has:

```text
q = 1/3
S_C1/R = q^2/[4(1-2q)] = 1/12.
```

For a canonical active image projector `P`, the sector action on the fixed
radial branch is:

```text
A(P) = Tr(P) * S_C1/R
     = Tr(P) / 12
     = W(P).
```

Therefore:

```text
A(A3) = 3 * 1/12 = 1/4
A(S5) = 5 * 1/12 = 5/12
A(T8) = 8 * 1/12 = 2/3.
```

This is a derived radial coupling in the following limited sense:

```text
the common radial C1 branch supplies the unit action 1/12;
the active operator taxonomy supplies projector traces;
their product gives W(P).
```

It does **not** mean each sector has a different radial exponent.

Stronger but unproved hypothesis:

```text
sector-dependent radial exponent q(P) selected by:
    S_C1(q_P)/R = W(P).
```

This would give finite-action candidate exponents:

```text
A3:
    q = sqrt(2) - 1 ~= 0.4142135624

S5:
    q = (2 sqrt(10) - 5)/3 ~= 0.4415184401

T8:
    q = (2 sqrt(22) - 8)/3 ~= 0.4602771732
```

All satisfy:

```text
0 < q < 1/2.
```

But the equation:

```text
S_C1(q_P)/R = W(P)
```

has not been derived as a boundary condition, variational principle, or
Calderon/Cauchy projector rule.

Twenty-fifth spectrum-stage verdict:

```text
The metric currently supports projector-weighted action readout on the common
q=1/3 radial branch. Sector-dependent radial depths are a mathematically clean
hypothesis, but not yet a derived result.
```

## 26. Sector-Dependent q Gate

Implemented in `native_sector_dependent_q_gate.py`.

The stronger hypothesis:

```text
S_C1(q_P)/R = W(P)
```

gives finite-action exponents for `A3`, `S5`, and `T8`, but all differ from:

```text
q = 1/3.
```

They also change the momentum/readout chain:

```text
eta = q/6
eta/2 = q/12.
```

Therefore sector-dependent `q(P)` cannot be used inside the current elementary
branch while keeping:

```text
q=1/3
eta=1/18
eta/2=1/36.
```

Current classification:

```text
common q=1/3:
    elementary ground taxonomy

sector-dependent q(P):
    possible radial excitation/depth branch
    not derived
```

Twenty-sixth spectrum-stage verdict:

```text
The current taxonomy keeps the common q=1/3 radial branch and reads sectors by
projector-weighted action. Sector-dependent radial depths are parked as a
possible excitation mechanism until a boundary condition derives them.
```

## 27. Two-Form Channel Action Balance

Implemented in `native_twoform_channel_action_balance.py`.

Use:

```text
domain unit = eta/2 = 1/36
image unit = S_C1/R = 1/12.
```

For each two-form channel, compare:

```text
domain load = channel domain dimension * 1/36
image action = commutator image rank * 1/12.
```

Results:

```text
trace wedge T8:
    domain load = 8/36 = 2/9
    image action = 0
    residual = 2/9

A3 wedge A3 -> A3:
    domain load = 3/36 = 1/12
    image action = 3/12 = 1/4
    residual = -1/6

A3 wedge S5 -> S5:
    domain load = 15/36 = 5/12
    image action = 5/12
    residual = 0

S5 wedge S5 -> A3:
    domain load = 10/36 = 5/18
    image action = 3/12 = 1/4
    residual = 1/36
```

Native identities:

```text
A3 wedge S5 is exactly balanced.

S5 wedge S5 residual = eta/2.

A3 wedge A3 deficit = -1/6 = -q/2.
```

Interpretation:

```text
The two-form taxonomy is not just dimensions. Its C1 domain load and
commutator image action have structured balances and residuals.
```

Twenty-seventh spectrum-stage verdict:

```text
The mixed A3-S5 channel is the first internally balanced interaction channel.
The pure S5-S5 and A3-A3 channels leave residuals equal to already-native C1
quantities. This is a channel-coupling clue, not yet a particle force or mass
formula.
```
