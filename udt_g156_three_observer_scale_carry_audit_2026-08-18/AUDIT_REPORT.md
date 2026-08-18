# G156 audit report — three-observer common-scale carrier and carry

Date: 2026-08-18

## Primary landing

`PAIR_METRIC_CANONICALLY_SUPPLIES_POSITIVE_HALF_DENSITY_SECTION__ANY_SUPPLIED_TYPED_CARRY_INDUCES_GAUGE_INVARIANT_LOG_DETERMINANT_CHARACTER__FULL_CLOSURE_IMPLIES_BUT_IS_NOT_IMPLIED_BY_SCALE_CLOSURE__OWNED_CHART_OVERLAP_AND_LEVI_CIVITA_CARRIES_ARE_SCALE_FLAT__ARBITRARY_SUPPLIED_NONISOMETRIC_CARRIES_NEED_NOT_BE_FLAT__NO_METRIC_OWNED_CROSS_QUERY_CARRY_OR_KAPPA_HISTORY`

Preregistered outcome class: `CONDITIONAL_FLAT_SCALE_CARRY`. That class applies only to the
already-owned chart, genuine-overlap, and Levi-Civita regimes; it does not say every supplied carry
is flat.

## What was learned

G155's question about a missing common-scale carrier has a positive, metric-native answer. A
supplied regular observer-pair plane has a half-density vector line and positive ray; its pair
metric supplies the canonical positive section

\[
\ell_h=(-\det h)^{1/4}|dy^0\wedge dy^1|^{1/2}.
\]

In calibrated coordinates its coefficient is \(e^\kappa\). Thus \(\kappa\) is best understood as
the logarithm of the metric half-density coefficient in a chosen local trivialization, not as an
independent scalar pasted onto the reciprocal sector.

When a typed carry \(M_{BA}\) is supplied, the joined comparison

\[
C_{BA}=R_BM_{BA}R_A^{-1}
\]

has the exact invariant scale character

\[
\boxed{
\sigma_{BA}=\frac12\log|\det C_{BA}|
=\kappa_B-\kappa_A+\frac12\log|\det M_{BA}|.
}
\]

This is equivalent to \(M_{BA}^*\ell_B=e^{\sigma_{BA}}\ell_A\). Endpoint gauge changes alter the
separate endpoint and carry terms but cancel from the total.

## The three-observer theorem

For \(A\to B\to C\),

\[
\boxed{
\Omega^{\rm sc}_{ABC}
=\sigma_{BA}+\sigma_{CB}-\sigma_{CA}
=\frac12\log|\det(M_{CB}M_{BA}M_{CA}^{-1})|.
}
\]

All endpoint \(\kappa\) values cancel. Full carry closure forces \(\Omega^{\rm sc}=0\), but zero
scale defect does not force full carry closure: an unmatched determinant-one shear is invisible to
the scale character. The scalar scale channel therefore checks only the determinant quotient; it
cannot replace the full reciprocal/shift/orchestra carry.

## Existing owned cases

- One calibrated query chart owns endpoint-exact scale carry. Recharting changes its matrices but
  the total comparison and three-observer closure remain exact.
- A proved genuine overlap between two query presentations is isometric and has zero total scale
  character. Merely sharing observers or endpoints does not prove such an overlap.
- Levi-Civita transport preserves the metric half-density, so its scale character is zero. It can
  carry other path holonomy but cannot produce nonisometric positional scale by itself.
- Separately supplied nonisometric carries can have a nonzero determinant triangle defect. Calling
  that holonomy additionally requires a declared path/loop functor. The metric identities evaluate
  the supplied carries but do not select them.

## What this resolves and what it does not

This is a real simplification. The local common-scale carrier is not another missing postulate. It
is already contained in the complete pair metric. The exact scalar readout is also not missing; it
is the determinant character of the complete carried comparison.

The unresolved issue is now smaller and better typed:

1. the metric does not currently select a nonisometric carry between unrelated query sheets;
2. G156 does not restrict or evolve the metric half-density section, so G155's rank-zero result for
   the physical \(\kappa\) history remains intact;
3. scalar scale closure is not enough to close the complete observer relation because determinant-one
   reciprocal, shear, and mixing structure can survive in its kernel.

## Evidence

- preregistration committed before outcome inspection: `7075abcc`;
- 19 exact sources verified by path, byte count, and SHA-256 at source commit `b42c771d`;
- 12 exact symbolic checks;
- independent standard-library exact-rational replay with 500 composition, gauge, and
  half-density trials;
- explicit determinant-one nonclosure and nonzero scale-defect witnesses;
- 8 mutation catches and a fresh adversarial repair gate;
- premise and package verification recorded separately.

## Maximum conclusion

G156 derives the metric half-density carrier and the conditional scalar scale-carry law on the
registered regular pair arena. It does not select a universe, derive a physical nonisometric
cross-query functor, evolve common scale, fix \(X_{\max}\), derive observations or dynamics, or
canonize a result. No canonization is requested or performed.
