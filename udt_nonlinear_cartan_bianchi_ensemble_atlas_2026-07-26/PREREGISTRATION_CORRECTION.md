# Post-result terminology correction to the preregistration

The committed preregistration at `c5e343a` is preserved unchanged as the
historical before-algebra record. Two occurrences of **independent** there are
too strong and are superseded as follows:

- “all 24 independent Levi-Civita connection coefficients” means **all 24
  antisymmetric connection coefficient slots**. They are uniquely solved;
  18 are generically nonzero and six are identically zero in this coframe.
- “all 36 independent curvature two-form coefficients” means **all 36
  pair-labeled curvature two-form slots**. All are generically nonzero here,
  but Riemann pair symmetry and the first Bianchi identity leave 20 algebraic
  slots for a generic four-dimensional Riemann tensor; this restricted family
  may have further functional relations.

This correction changes no equation, table entry, result count, or scope. It
prevents a slot census from being mistaken for an independence theorem.

The production second-Bianchi control is also classified precisely: it is an
exact graded-algebra proof of the universal identity, not an independent
component-by-component replay of the calculated curvature table.
