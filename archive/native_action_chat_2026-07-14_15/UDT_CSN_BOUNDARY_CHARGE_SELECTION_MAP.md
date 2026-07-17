# UDT CSN finite-boundary charge selection — frozen derivation map

## Hygiene

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Mode | Analytic DERIVE + dependency-free exact audit; DATA-BLIND |
| Immediate predecessor | UDT_ELECTRON_CALIBRATION_BRIDGE_DERIVATION_RESULTS.md |
| GPU | Not authorized unless a unique continuum boundary problem emerges |
| Banking | None; LIVE.md and CANON.md remain untouched |

## Question

Does Common-Scale Neutrality, differentiability, flat-reference subtraction, or the existing UDT
boundary ontology select a unique finite-cell charge with inverse-\(X\) scaling? In particular, is
the Euler \(4/X\) readout a physical boundary generator or an artifact of ending the conditional
static patch at the WR-L causal horizon?

## Allowed premises

1. Owner-locked Common-Scale Neutrality.
2. WR-L:
   \[
   A=1-r/X.
   \]
3. The conditional reciprocal \(C^2\) bulk reduction:
   \[
   L_C=\gamma W^2/r^2,\qquad
   W=r^2A''-2rA'+2(A-1).
   \]
4. The exact Euler radial primitive:
   \[
   r^2E_4=\frac{d}{dr}[4(A-1)A'].
   \]
5. The current boundary taxonomy:
   - WR-L \(A=0\): causal horizon with continuation, not automatically a hard boundary;
   - canonical odd fold: \(\phi=0\), hence \(A=1\);
   - exact quotient, one-copy boundary, matched interface, and numerical box remain distinct.
6. Exact higher-derivative endpoint variation and dimensional homogeneity.

No EH/GR boundary term, ADM charge, observed mass, target \(X\), fitted coefficient, new boundary
field, or carrier identity may be imported.

## Pre-registered tests

### T1. Scale-neutral boundary form

For a local reciprocal static endpoint functional depending on \(A,A',r\), derive the most general
form allowed by global common-scale homogeneity:

\[
B(A,A',r)=\frac{\gamma}{r}\,b(A,rA').
\]

Determine whether CSN fixes the dimensionless function \(b\) or only its weight.

### T2. Differentiability classes

Combine

\[
\delta S_{\rm bulk}\big|_\partial
=P_0\delta A+P_1\delta A'
\]

with \(\delta B\). Test fixed \((A,A')\), fixed \(A\), fixed \(A'\), and free-jet endpoint variations.
At WR-L, where \(P_0=P_1=0\), determine which values or derivatives of \(b\) are constrained.

### T3. Flat reference and counterfamily

Impose the possible reference convention

\[
B(1,0,r)=0.
\]

Construct an explicit CSN-homogeneous family that also has vanishing first derivatives at the WR-L
endpoint but retains arbitrary \(B_{\rm WR-L}=k\gamma/X\). This is an inverse-problem
counterexample, not a candidate action.

### T4. Moving endpoint and clock scaling

Evaluate the complete static boundary action over a time interval. Check whether varying \(X\) at
fixed coordinate time spuriously breaks CSN, and whether fixing dimensionless duration
\(\Delta\tau=c\Delta t/X\) restores scale invariance.

### T5. Boundary ontology

Evaluate the Euler primitive at:

1. the WR-L horizon \(A=0\);
2. the canonical fold \(A=1\);
3. a matched internal interface with opposite orientations.

Determine whether the one-sided \(4/X\) value survives under the live boundary ontology.

### T6. Normalization

Test whether multiplying the entire action or adding an allowed boundary improvement changes the
finite charge without changing the vacuum equation. Distinguish additive reference choice,
multiplicative normalization, and a derived dimensionless mass ratio.

## Acceptance gates

- A static-patch horizon may not be called the physical finite-cell boundary without a new premise.
- Differentiability conditions on derivatives of \(b\) may not be claimed to fix its value.
- Scale weight \(-1\) may not be claimed to fix a numerical coefficient.
- The time interval must transform consistently under CSN.
- A one-sided total derivative may not be banked as a global charge until interface/horizon
  cancellation and boundary completion are audited.
- Reduced counterfamilies must be labeled as nonuniqueness proofs, not UDT proposals.

## Possible outcomes

1. **UNIQUE NATIVE CHARGE:** current principles select \(b\), its coefficient, boundary ontology, and
   normalization.
2. **RIGHT WEIGHT, FUNCTION/NORMALIZATION OPEN:** inverse-\(X\) scaling is forced but its coefficient
   is not.
3. **WR-L HORIZON READOUT INAPPLICABLE:** the \(4/X\) endpoint is not the live physical boundary or
   cancels across the completion.
4. **NO SCALE-NEUTRAL BOUNDARY CHARGE:** all admissible boundary values vanish.

