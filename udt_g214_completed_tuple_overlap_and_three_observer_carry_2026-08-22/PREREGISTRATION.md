# G214 preregistration — completed-tuple descent and carry

Date: 2026-08-22

## Frozen question

Test whether G213 completion is a natural, density-faithful change of variables on the groupoid of
regular calibrated pair charts, and determine exactly what this does and does not imply for
three-observer composition.

## Premise ledger

1. `SUPPLIED`: regular Lorentzian pair pullback \(h_\sigma\), with \(h_{00}<0\) and \(\det h<0\).
2. `SUPPLIED`: calibrated clock/ruler split, orientations, and upper-triangular overlap maps.
3. `WORKING_FOUNDATIONAL_CLARIFICATION`: completed-pair Dual Reciprocity, hence
   \(m=\sqrt{-\det h_\sigma}>0\) and \(\det h_s=-1\).
4. `DERIVED_CONDITIONAL`: G213 local bijection between \(h_\sigma\) and typed \((m,h_s)\).
5. `DERIVED_BOUNDED`: G170/G171 endpoint-relative reversal and matched scalar composition.
6. `OPEN`: physical germ population, cross-pair incidence matching, network values, and global
   realization.

## Preregistered candidate conclusions

### C1 — overlap naturality

For every declared positive calibrated transition, the density-completed tuple is equivariant and
reconstructs the same tensor transition exactly. The induced completed transition has determinant
one and obeys the same cocycle order on triple overlaps.

### C2 — reparameterization and reversal

Pure ruler reparameterization is absorbed entirely by the density. Spatial orientation reversal
requires the retained ruler orientation and flips the shift by congruence; it is not observer-pair
endpoint reversal. Same-pair endpoint reversal negates the endpoint-relative scalar by swapping the
same completed incidence values.

### C3 — G130 transfer ceiling

G130 lawful overlap descent transfers to a smooth compatible network of typed density-completed
tuples without information loss. This is reconstruction of a supplied valuation, not generation of
its values.

### C4 — three-observer boundary

Arbitrary `AB`, `BC`, and `AC` completed pair metrics do not possess a native matrix product.
Scalar depths telescope only on the matched-incidence subfamily already typed by G171, or when
explicit incidence transition maps make those matches. Shared observer identity alone is
insufficient. Cross-pair carry therefore remains a compatibility datum unless the metric/query
construction supplies the required incidence identifications.

## Registered falsifiers

The candidate theorem fails if any of the following occurs in the bounded arena:

1. \(m_j\ne(\det P_{ij})m_i\) for a positive transition;
2. \(\det C_{ij}\ne1\);
3. completed congruence followed by reconstruction differs from \(P_{ij}^Th_iP_{ij}\);
4. \(C_{ij}C_{jk}\ne C_{ik}\) when \(P_{ij}P_{jk}=P_{ik}\);
5. a pure ruler reparameterization changes \(h_s\);
6. deleting \(m\) remains faithful under positive spatial rescaling;
7. the G171 nonmatched three-pair witness is forced to telescope by tuple completion alone.

## Hostile controls

The verifier must catch at least these mutations:

- omit the clock factor from the density weight;
- use \(m_j=(\det P)^{-1}m_i\);
- reverse a transition-product order;
- treat \(h_s\) as invariant under every upper-triangular rechart;
- drop the density during reconstruction;
- identify a shared observer with a matched pair incidence;
- multiply pair metrics as if they were comparison arrows.

## Verification contract

- production: dependency-free exact rational algebra with explicit two- and three-chart witnesses;
- independent: separately coded exact `Fraction` replay over 10,000 regular rational metrics and
  transitions, including reconstruction, determinant, cocycle, pure-reparameterization, and
  density-blind controls;
- hostile: explicit mutation catches;
- source hashes: all 14 frozen load-bearing source files must match;
- no-write package replay and raw residual/equality gate;
- no observational data or protected package may enter.

## Maximum conclusion

At most:

```text
TYPED_DENSITY_COMPLETED_TUPLE_DESCENDS_FUNCTORIALLY_ON_SUPPLIED_CALIBRATED_PAIR_COVERS
__G130_RECONSTRUCTION_TRANSFERS_WITHOUT_DENSITY_LOSS
__ARBITRARY_THREE_OBSERVER_FULL_TUPLE_COMPOSITION_REMAINS_NOT_DERIVED
```

No physical germ population, cross-query carry owner, history-value evolution, global completion,
`X_max`, transfer, source, action, matter, mass, bootstrap, observation, or signalling conclusion is
permitted.
