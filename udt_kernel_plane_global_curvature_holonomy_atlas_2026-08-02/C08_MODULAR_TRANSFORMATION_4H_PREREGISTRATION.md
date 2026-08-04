# C08 modular transformation certificate — four-hour continuation preregistration

Date: 2026-08-04
Branch: `grok`
Base before this preregistration: `41eb1a98`

## Disclosed prior return

The original exact modular transformation attempt stopped at its preregistered 7,200-second wall
limit with no matrix, no stderr, a 27,943,104-KiB peak aggregate RSS, at least 113,130,472 KiB host
memory available, and 3,328 KiB maximum swap use. It moved through multiple memory phases and ended
on a roughly 14.8-GiB plateau. That evidence is frozen in commit `41eb1a98` and remains
`OPEN_RESOURCE_BOUNDED_TRANSFORMATION_ATTEMPT`.

This continuation is justified only as a bounded test of whether the same healthy computation needs
more wall time. It is not a retroactive extension of the original contract and does not assume that
four hours will be sufficient.

## Whole bounded question

Can an unchanged restart of the modular `liftstd` transformation method return, within four hours,
an exact rational matrix `T` satisfying all nine identities

```text
G_j = sum_i I_i T_ij,  i=1,...,6, j=1,...,9,
```

for the same frozen C08 all-zero ideal and the same nine-polynomial target basis?

This addresses only `<G> subset <I>` for that frozen branch. It does not test real roots, nonzero-A
charts, global C08, or physics.

## Frozen method and restart semantics

- restart from the beginning; Singular/modular supplied no reusable checkpoint;
- same committed production input, SHA-256
  `bf6e00b8f98b7313844139a284b76faff4364579b342356eec60104c5f4db044`;
- same `QQ[z,y]` ring, variable order, `dp` ordering, six inputs, nine targets, modular callbacks,
  unlucky-prime logic, reconstruction, and exact final identity;
- same four worker processes, one thread per worker, and CPU-only execution;
- same nontrivial exact toy and coefficient-mutation gate before production;
- separate `*_4H_*` toy, stdout, stderr, monitor, and process artifacts; no overwrite of the
  two-hour evidence;
- no changed polynomial, order, prime policy, normalization, coefficient, tolerance, or desired
  answer.

## Resource and stop contract

Stop and return OPEN on any of:

1. 14,400 seconds wall time;
2. 64 GiB aggregate descendant RSS;
3. host available memory at or below 32 GiB;
4. 8 GiB swap use;
5. failed source/hash or nontrivial-toy gate, internal error, or nonzero exit;
6. unstable matrix dimensions or leading-monomial order across retained primes;
7. failed exact basis, transformation, mutation, or certificate identity.

There is no automatic retry, further extension, alternate order, changed ideal, fallback algebra
engine, or root isolation. This continuation is one fresh restart.

## Certification and independence

A production return counts only if Singular reports a 7-by-9 transformation package, verifies the
target basis, verifies all source reductions, expands `matrix(I)*T-matrix(G)` exactly to zero, and
catches the registered coefficient mutation.

If such a matrix returns, the already committed independent Python verifier must parse all 54
entries and recompute all nine polynomial identities using its own sparse exact-rational arithmetic.
No matrix means that independent certificate verification is not reached. Fresh cold adversarial
review remains absent unless separately authorized.

## Four-gate ceiling and maximum conclusion

The attempt is preregistered and premise-bounded, but it cannot satisfy independent verification
unless a matrix actually returns. A time/resource stop remains OPEN and is not evidence against
containment.

If production and independent exact verification pass, this continuation may establish
`<G> subset <I>`. Together with the previously verified opposite containment it may establish exact
ideal equality for the frozen C08 all-zero branch, pending fresh cold review. It cannot establish a
real-root count, complete branch classification, selection, carrier, action, source, boundary,
bootstrap, matter, mass, or dynamics.
