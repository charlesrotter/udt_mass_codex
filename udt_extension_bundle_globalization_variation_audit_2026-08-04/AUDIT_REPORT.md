# UDT extension-bundle globalization and variation-domain audit

Date: 2026-08-04

Status: **VERIFIED_WITH_CAVEATS**

## Result first

The registered local whole-spacetime skeleton admits a coherent global bundle interpretation without
requiring one global coframe. Conditional on smooth reciprocal and screen bundles `N,Q` over the
total pair-frame query bundle—or over spacetime after a supplied nondegenerate rank-two reduction and
smooth split—the remaining `3+4` extension data are:

```text
positive screen metric h in SPD(Q)
plus mixing sigma in Hom(N,Q).
```

Both fibers are contractible. A positive screen metric exists on a nontrivial rank-two screen bundle
by partition-of-unity gluing, and the mixing vector bundle has a canonical zero section. Therefore
these extension fibers add **no independent existence obstruction** after the smooth split has been
supplied. This does not derive the split, and it does not select a particular screen metric or
zero/nonzero mixing.

The audit localizes rather than closes the real gap. Still open are the physical reciprocal
realization, whether it is query data or a field, the global `phi` assignment, actual cover and
transition data, completion topology and boundary glue, rank-changing strata, variation ownership,
and the native law.

## Exact findings

1. Physical and reference coframe overlaps require the exact two-sided rule

   ```text
   E_j = L_ij E_i R_ij^-1.
   ```

   Compatible left and right cocycles make this associative on triple overlaps. Arbitrary ambient
   `GL(4)` transitions do not automatically preserve the local triangular `3+4` slice; the global
   tensor-level transition laws after a supplied split are

   ```text
   h_j=Q_ij^-T h_i Q_ij^-1,
   sigma_j=Q_ij sigma_i P_ij^-1.
   ```
2. The right logarithmic variation factorizes exactly:

   ```text
   delta(E) E^-1 = [[delta(A) A^-1,                 0],
                    [D delta(S) A^-1, delta(D) D^-1]].
   ```

3. With varying transitions,

   ```text
   e_j = ell_ij + Ad(L_ij)e_i - Ad(E_j)r_ij.
   ```

   The corresponding left and right linearized cocycles were independently replayed.
4. The three screen-metric and four mixing directions remain seven local chart tangents. They are
   not seven propagating modes.
5. The abstract `Z2` reciprocal reversal algebra remains valid. Identity-required cocycle products
   have even reversal parity, while a noncontractible loop may carry odd `Z2` monodromy. Its physical
   metric/boundary lift is still conditional; the constant swap is not an ordinary Lorentz isometry
   of the diagonal two-channel readout.
6. A global coframe and a parallel pair-screen split are stronger witnesses, not requirements for a
   global metric/configuration bundle.
7. Query-bundle, realized-field, and branch-derived-section ontologies remain distinct. The same
   vertical change cannot be called a physical field variation in all three.

## Retained branches and obstructions

All seven preregistered transition families remain in `TRANSITION_FAMILY_LEDGER.tsv`. No topology,
screen shape, mixing value, boundary type, or desired physical branch was filtered. The exact
obstruction and section distinctions are in `BUNDLE_OBSTRUCTION_LEDGER.tsv`; admissible and blocked
variation types are in `VARIATION_DOMAIN_LEDGER.tsv`.

## Algebraic evidence

- production SymPy implementation: 26/26 exact checks pass;
- independent standard-library rational implementation: 16/16 checks pass;
- fresh zero-context semantic review: `ACCEPT_WITH_REQUIRED_REPAIRS`;
- read-only repair closure replay: `REPAIRS_ACCEPTED`, with all R01–R06 rows closed;
- the independent implementation imports neither the production script nor a third-party algebra
  package.

These checks certify the stated sparse identities only. They do not certify a physical action or
global solution.

## Premise stamps

- reciprocal character and additive composition: `DERIVED` algebraically;
- physical local/global `phi` assignment: `OPEN`;
- pair-frame query bundle on a supplied regular metric: `DERIVED` container, no global pair section;
- realized reciprocal field: `OPEN`;
- screen metric and mixing extension existence after a reciprocal reduction: `DERIVED` standard
  bundle fact;
- physical screen/mixing selection: `OPEN`;
- channel reversal: abstract algebra `DERIVED`, physical lift `CONDITIONAL`;
- global coframe or parallel split: `CONDITIONAL`, not required;
- action, source, carrier, boundary law and dynamics: `OPEN` or retain their prior conditional stamps;
- `S^2` carrier: `POSIT`, unchanged;
- strong local CSN: inactive unless Charles explicitly reauthorizes it.

## Four banking gates

1. Preregistered: **yes**, commit `5399d850`.
2. Full space or bounded scope justified: **yes for the smooth fixed-rank globalization tile**; all
   seven transition families retained, while rank-changing strata are explicitly outside this tile.
3. Independently verified on the load-bearing premise: **yes**; exact algebra has an independent
   implementation, and the fresh semantic adversary accepted all six repairs on replay.
4. Every premise audited: **yes within the bounded tile; physical ownership and native law remain
   explicitly open**.

All four gates are satisfied for the bounded smooth fixed-rank globalization tile. The result remains
`VERIFIED_WITH_CAVEATS`, not a native law or global physical-branch theorem.

## Maximum conclusion

```text
BOUNDED_EQUIVARIANT_EXTENSION_BUNDLE_AND_VARIATION_TYPE_CLASSIFICATION;
GLOBAL_RECIPROCAL_REDUCTION_OBSTRUCTION_LOCALIZED_OR_RETAINED_OPEN;
NO_NATIVE_LAW_OR_PHYSICAL_BRANCH_SELECTED.
```

No update to `LIVE.md` or `CANON.md` is authorized or made.
