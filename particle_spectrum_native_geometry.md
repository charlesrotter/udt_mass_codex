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
