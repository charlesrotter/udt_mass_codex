# N02 radial-anchor admissibility — audit report

## Current verdict

`VERIFIED-WITH-CAVEATS`.

## Result

No already-banked P1 profile supplies a smooth complete C1/C2 center-to-wall convergence anchor.
The full C1 curvature, including leading regular-order mixing, has

```text
lim r RicciScalar = -6a,
```

where `A=1+a r+...`. Since P1 has `a=-n`, all three registered backgrounds obey
`RicciScalar~6n/r`. The corrected `h~r^2` family passes only the necessary collapsing-orbit order;
the RA1 literal `h~constant` center fails it. Neither cancels the P1 curvature cusp.

The wall is separately informative. All 21 nonzero-mixing exponent strata have `B->infinity`,
finite Liouville distance, and sub-inverse-square finite-block matrix potentials. They are
limit-circle and require a free self-adjoint extension family; D/N are merely two unselected
control members. The round `h=0`, `n>1` wall instead lies at infinite Liouville distance and is
limit-point, so D/N are not free wall data there.

The complete census contains 45 profile strata, representing all 210 corrected nonzero-mixing
profiles plus the three round and 21 RA1-lineage controls, and 24 endpoint strata. No row was ranked
by spectrum, tractability, or observational resemblance.

## Status boundary

This is a source-role and complete-metric compatibility correction, not a negative verdict on the
SNe/P1 relational fit and not a reversal of N01's local angular algebra. It blocks only the silent
promotion of P1 into a regular full-spherical center-to-wall metric and therefore blocks N02's
proposed eigensolve.

No replacement profile, inner cutoff, boundary functional, eigensolver, FD2 restart, data fit, or
GPU work is authorized.

## Verification

The final production replay passes 20/20 keys. The separately implemented verifier recomputes the
full-center curvature residue and all endpoint exponents, reconstructs every TSV field exactly,
and catches 23/23 registered corruptions. A fresh zero-context adversarial reviewer independently
confirmed the center and wall conclusions and required five fail-closed checker repairs. After
those repairs, the same reviewer directly exercised and accepted every formerly escaping mutation.
See `EXTERNAL_ADVERSARIAL_REVIEW.md`.

## Four banking gates

1. **Preregistered:** yes, at commit `c73eb657`; the source/candidate freeze predates derivation.
2. **Space covered:** the full frozen candidate universe is covered (45 profile strata, including
   all 210 R1 profiles, and 24 endpoint strata). The wall theorem is explicitly bounded to each
   fixed finite harmonic block; alternate radial families and a uniform infinite-basis theorem are
   not covered.
3. **Independently verified:** yes; independent tensor/asymptotic recomputation plus a fresh
   zero-context adversarial review, with all required repairs accepted.
4. **Premises audited:** yes; C1/C2, scalar `Box_g`, P1 provenance, mixing order, endpoint domain,
   and boundary ownership retain their explicit `CONDITIONAL`/`CHOSE`/`OPEN` scopes. G33 enforces
   the nonpromotion boundary.
