# G154 fresh adversarial review

Date: 2026-08-18
Reviewer context: fresh bounded repository context; read-only; protected local packages excluded
Verdict: REPAIR_REQUIRED

## Decisive finding

The original fixed-leaf-scale claim was circular. The derivation assumed a dimensionful Mobius law
with one fixed \(X_*\), then used \(\operatorname{artanh}(x/X_*)\). The production code verified the
same already-fixed-\(X_*\) identity. Neither operation proves that the adopted normalized law owns a
fixed dimensionful scale.

The strongest valid theorem is conditional: if a leaf is additionally supplied with a fixed-scale
dimensionful Mobius law, continuity and unit slope give

\[
x=X_*\tanh\phi,
\]

and any presentation \(x=X(\phi)\tanh\phi\) has \(X=X_*\) on that leaf.

Required primary landing:

    EVEN_FIXED_LEAF_SCALE_NOT_DERIVED__RESPONSE_CLASS_NOT_SELECTED

## Results independently retained

The fixed-\(X_*\) response counterfamilies replay exactly, conditionally on that fixed-scale type.
They retain identical \(\phi,\rho,X_*\), vary only the common metric scale, and realize:

- quiet response for \(\ell=1/2\);
- finite response \(\epsilon4X_*/3\) for \(\ell=1/3\);
- signed divergence for \(\ell=1/4\);
- subsequences \(\epsilon2X_*\) and \(\epsilon2X_*/3\) for the oscillatory critical witness.

Both signs and the temporal dual work. The live-\(dX\) endpoint, nonconvergence, and exact
cancellation witnesses are also algebraically correct. Live \(dX\) is excluded only after a
fixed-scale premise is supplied, not by the active normalized law.

Reciprocity and additive composition constrain sign and values against additive depth. They do not
constrain \(V(\phi)\) against a normalized clock or ruler, and no response-class selector was found.
The sign reversal of \(V(\rho)\) requires a carried normalized-frame convention and is not a
universal consequence of endpoint reversal alone.

## Evidence cautions

- Preregistration commit f5946fa0 is valid and contains only the preregistration and manifest.
- All seven source hashes matched.
- The original independent verifier began with closed response formulas, omitted oscillatory
  limits, and checked cancellation only through constant \(\rho\).
- The package verifier required the disputed landing, so its mutation tests could not expose the
  circular premise.

## Required repairs

1. Replace every fixed-scale-derived claim with the conditional theorem.
2. Retain G153 live \(dX\) until fixed-scale descent is independently supplied or derived.
3. Add a normalized-composition countermodel with nonconstant \(X\).
4. Independently reconstruct responses from \(T,L\), cover both oscillatory duals, and verify the
   two nonzero cancellation terms separately.

