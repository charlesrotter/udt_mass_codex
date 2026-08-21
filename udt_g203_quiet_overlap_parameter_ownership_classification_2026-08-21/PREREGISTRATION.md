# G203 preregistration

Date: 2026-08-21

## Claims to test

1. Vanishing order at the quiet overlap is invariant under every analytic local coordinate change
   with nonzero first derivative.
2. Once \(r\) is the positive areal radius, a radial chart change that retains the same areal form
   cannot move the quiet sphere: its area and \(r_0\) are geometric descriptors of a supplied
   history.
3. With founded depth normalization and log-areal coordinate fixed, the first nonzero Taylor
   coefficient is a dimensionless local metric descriptor.
4. The reciprocal representation, reversal, composition, and quiet-jet condition do not select
   numerical values of the order, areal location, or coefficient.
5. A family indexed by every odd \(n\ge3\), every \(r_0>0\), and every \(a>0\) supplies exact
   regular monotone two-sided counterexamples to uniqueness.
6. Reciprocal reversal alone does not force the entire radial profile to be globally odd unless a
   separate involution acts on the radial/history argument.
7. Observations may calibrate these invariant descriptors or coefficients inside a declared
   finite family; dimensional availability is not theoretical selection.

## Outcome classes

- `FOUNDING_SELECTS_ALL_THREE`;
- `FOUNDING_SELECTS_A_PROPER_SUBSET`;
- `INVARIANT_DESCRIPTORS_BUT_UNSELECTED__OBSERVATIONS_MAY_CALIBRATE`;
- `DESCRIPTORS_ARE_CALIBRATION_GAUGE`;
- `TYPE_OR_EXISTENCE_FAILURE`.

## Certification contract

Production must verify symbolically:

- quiet jets, monotonicity, sign crossing, and endpoint growth for the exact counterfamily;
- invariant vanishing order and leading-coefficient transformation under an analytic germ change;
- rigidity of positive areal radius under preservation of the spherical orbit metric;
- invariance of \(n,r_0,|a_n|\) under the declared lawful identity/reversal operations, with every
  broader transformation separately typed;
- dimensional exponent systems for \(c_E,G_{\rm obs}\), mass, and density.

An independent implementation must not import production code or read its output. It must use
exact integer/rational arithmetic for at least 20,000 distinct parameter/germ cases and explicitly
distinguish histories with different \(n\), \(r_0\), or \(a\).

Hostile checks must catch at least:

1. even order called sign-changing;
2. linear or quadratic order called quiet;
3. the areal radius called a removable radial gauge;
4. founded depth normalization called radial-steepness normalization;
5. observer reversal called a proof of global profile oddness;
6. one mass/density combination promoted to a UDT scale law;
7. finite anchors called unrestricted-history derivation;
8. \(X_{\max}\) inserted into the local kernel;
9. the witness family called the selected physical solution.

## Falsification

The proposed landing fails if a current founded premise fixes any of the three descriptors, if a
lawful areal-preserving calibration maps distinct descriptor triples into one another, or if the
registered exact family fails quietness, monotonicity, sign crossing, reciprocity, or regularity on
its declared domain.

## Maximum conclusion

At most this audit may classify the three local descriptors as derived, gauge, or calibration
data. It may not select a global profile, fit observations, derive \(X_{\max}\), or add dynamics.
