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
